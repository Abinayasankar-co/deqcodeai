from typing import Union, Callable, Dict, Any, List, Tuple
import cirq
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import numpy as np
from mitiq import zne, cdr, pec
from mitiq.interface import convert_to_mitiq
from mitiq.pec.representations.depolarizing import represent_operation_with_local_depolarizing_noise
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import hashlib
import json

# Configure logging for production use
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuantumCircuitTranspiler:
    def __init__(self, circuit_input: Union[cirq.Circuit, QuantumCircuit, str], input_backend: str, noise_level: float = 0.01):
        self.input_backend = input_backend.lower()
        self.noise_level = noise_level
        self.circuit = self._parse_circuit(circuit_input)
        self.validate_input()
        self.mitiq_circuit, _ = self._convert_to_mitiq()
        self.circuit_id = self._generate_circuit_id()
        self.num_qubits = self._get_num_qubits()
        logger.info(f"Initialized transpiler for {self.input_backend} circuit with ID: {self.circuit_id}, {self.num_qubits} qubits")

    def _parse_circuit(self, circuit_input: Union[cirq.Circuit, QuantumCircuit, str]) -> Union[cirq.Circuit, QuantumCircuit]:
        if isinstance(circuit_input, str):
            if self.input_backend == 'cirq':
                return cirq.read_json(json_text=circuit_input)
            elif self.input_backend == 'qiskit':
                return QuantumCircuit.from_qasm_str(circuit_input)
        return circuit_input

    def validate_input(self) -> None:
        if self.input_backend not in ['cirq', 'qiskit']:
            raise ValueError("Input backend must be 'cirq' or 'qiskit'")
        if not isinstance(self.circuit, (cirq.Circuit, QuantumCircuit)):
            raise ValueError(f"Invalid circuit type for {self.input_backend}")

    def _generate_circuit_id(self) -> str:
        circuit_str = str(self.circuit)
        return hashlib.md5(circuit_str.encode()).hexdigest()

    def _convert_to_mitiq(self) -> Tuple[Any, str]:
        if self.input_backend == 'cirq':
            return convert_to_mitiq(cirq.Circuit(self._get_operations()))
        return convert_to_mitiq(self.circuit)

    def _get_num_qubits(self) -> int:
        if self.input_backend == 'cirq':
            qubits = set()
            for op in self.circuit.all_operations():
                qubits.update(op.qubits)
            return len(qubits)
        return self.circuit.num_qubits

    def _get_operations(self) -> List[Any]:
        if self.input_backend == 'cirq':
            return list(self.circuit.all_operations())
        return [instr.operation for instr in self.circuit.data]

    def _is_clifford_gate(self, gate: Any) -> bool:
        if not gate:
            return False
        if self.input_backend == 'cirq':
            clifford_types = (type(cirq.H), type(cirq.CNOT), type(cirq.S), type(cirq.Z), type(cirq.X), type(cirq.Y))
            return isinstance(gate, clifford_types) or \
                   (isinstance(gate, cirq.XPowGate) and gate.exponent in {0.5, 1, -1, -0.5})
        return getattr(gate, 'name', '') in ['h', 'cx', 's', 'sdg', 'z', 'x', 'y']

    def _count_gate_types(self) -> Tuple[int, int]:
        clifford_count = non_clifford_count = 0
        for op in self._get_operations():
            gate = getattr(op, 'gate', op) if self.input_backend == 'cirq' else op
            if self._is_clifford_gate(gate):
                clifford_count += 1
            elif gate is not None:
                non_clifford_count += 1
        return clifford_count, non_clifford_count

    def _select_mitigation_strategy(self) -> Callable:
        clifford_count, non_clifford_count = self._count_gate_types()
        total_gates = clifford_count + non_clifford_count
        if total_gates == 0:
            logger.info(f"Circuit {self.circuit_id} is empty; using ZNE")
            return zne.execute_with_zne
        if non_clifford_count == 0:
            return cdr.execute_with_cdr
        elif non_clifford_count <= 2:
            return pec.execute_with_pec
        return zne.execute_with_zne

    def _execute_cirq(self, circuit: Any, noise_level: float = 0.0) -> Tuple[float, float]:
        if not isinstance(circuit, cirq.Circuit):
            circuit = cirq.Circuit(circuit)
        simulator = cirq.DensityMatrixSimulator(
            noise=cirq.depolarize(p=noise_level) if noise_level > 0 else None
        )
        result = simulator.simulate(circuit)
        z_observable = np.kron(np.eye(2), np.array([[1, 0], [0, -1]], dtype=complex)) if self.num_qubits >= 2 else np.array([[1, 0], [0, -1]], dtype=complex)
        energy_hamiltonian = sum(
            np.kron(np.eye(2**i), np.kron(np.array([[1, 0], [0, -1]], dtype=complex), np.eye(2**(self.num_qubits - i - 1))))
            for i in range(self.num_qubits)
        )
        exp_val = float(np.real(np.trace(result.final_density_matrix @ z_observable)))
        energy = float(np.real(np.trace(result.final_density_matrix @ energy_hamiltonian)))
        return exp_val, energy

    def _execute_qiskit(self, circuit: QuantumCircuit, noise_level: float = 0.0) -> Tuple[float, float]:
        sim = AerSimulator(method='statevector')
        circuit_with_save = circuit.copy()
        circuit_with_save.save_statevector()
        if noise_level > 0:
            noise_model = NoiseModel()
            error_1q = depolarizing_error(noise_level, 1)
            error_2q = depolarizing_error(noise_level, 2)
            noise_model.add_all_qubit_quantum_error(error_1q, ['h', 't', 'x', 'y', 'z', 'rx', 'ry', 'rz', 's', 'sdg'])
            noise_model.add_all_qubit_quantum_error(error_2q, ['cx', 'swap'])
            sim.set_options(noise_model=noise_model)
        result = sim.run(circuit_with_save).result()
        state = result.get_statevector()
        state_array = state.data
        z_observable = np.kron(np.eye(2), np.array([[1, 0], [0, -1]], dtype=complex)) if self.num_qubits >= 2 else np.array([[1, 0], [0, -1]], dtype=complex)
        energy_hamiltonian = sum(
            np.kron(np.eye(2**i), np.kron(np.array([[1, 0], [0, -1]], dtype=complex), np.eye(2**(self.num_qubits - i - 1))))
            for i in range(self.num_qubits)
        )
        exp_val = float(np.real(state_array.conj().T @ z_observable @ state_array))
        energy = float(np.real(state_array.conj().T @ energy_hamiltonian @ state_array))
        return exp_val, energy

    def execute_raw(self, noise_level: float = None) -> Tuple[float, float]:
        executor = self._execute_cirq if self.input_backend == 'cirq' else self._execute_qiskit
        return executor(self.circuit, noise_level or self.noise_level)

    def execute_ideal(self) -> Tuple[float, float]:
        return self.execute_raw(0.0)

    def mitigate_error(self) -> Tuple[float, float]:
        mitigation_func = self._select_mitigation_strategy()
        executor = self._execute_cirq if self.input_backend == 'cirq' else self._execute_qiskit
        operations = self._get_operations()

        def mitigated_executor(circ: Any, noise: float) -> float:
            exp_val, _ = executor(circ, noise)
            return exp_val

        if mitigation_func == cdr.execute_with_cdr:
            mitigated_exp = mitigation_func(
                circuit=self.mitiq_circuit,
                executor=lambda circ: mitigated_executor(circ, self.noise_level),
                simulator=lambda circ: mitigated_executor(circ, 0.0),
                num_training_circuits=10,
                scale_factors=(1, 2, 3)
            )
            _, energy = executor(self.circuit, self.noise_level)
            return mitigated_exp, energy
        elif mitigation_func == pec.execute_with_pec:
            reps = {}
            for op in operations:
                if self.input_backend == 'cirq':
                    gate = getattr(op, 'gate', None)
                    if gate and not isinstance(gate, cirq.MeasurementGate):
                        circ = cirq.Circuit(op)
                        reps[circ] = represent_operation_with_local_depolarizing_noise(circ, 0.001)
                else:
                    if op.name in ['h', 't', 'cx', 'x', 'y', 'z', 'rx', 'ry', 'rz', 's', 'sdg', 'swap']:
                        q0, q1 = cirq.LineQubit.range(2)
                        cirq_op_map = {
                            'h': cirq.H(q0),
                            't': cirq.T(q0),
                            'cx': cirq.CNOT(q0, q1),
                            'x': cirq.X(q0),
                            'y': cirq.Y(q0),
                            'z': cirq.Z(q0),
                            'rx': cirq.rx(op.params[0])(q0) if op.params else cirq.X(q0),
                            'ry': cirq.ry(op.params[0])(q0) if op.params else cirq.Y(q0),
                            'rz': cirq.rz(op.params[0])(q0) if op.params else cirq.Z(q0),
                            's': cirq.S(q0),
                            'sdg': cirq.S(q0) ** -1,
                            'swap': cirq.SWAP(q0, q1)
                        }
                        cirq_op = cirq_op_map.get(op.name)
                        if cirq_op:
                            circ = cirq.Circuit(cirq_op)
                            reps[circ] = represent_operation_with_local_depolarizing_noise(circ, 0.001)
            mitigated_exp = mitigation_func(
                circuit=self.mitiq_circuit,
                executor=lambda circ: mitigated_executor(circ, self.noise_level),
                representations=reps,
                num_samples=100
            )
            _, energy = executor(self.circuit, self.noise_level)
            return mitigated_exp, energy
        else:
            factory = zne.inference.LinearFactory([1.0, 2.0, 3.0])
            mitigated_exp = zne.execute_with_zne(
                circuit=self.mitiq_circuit,
                executor=lambda circ: mitigated_executor(circ, self.noise_level),
                factory=factory,
                scale_noise=zne.scaling.fold_global
            )
            _, energy = executor(self.circuit, self.noise_level)
            return mitigated_exp, energy

    def transpile(self) -> Dict[str, str]:
        cirq_code = ["import cirq", f"circuit = cirq.Circuit()", f"qubits = [cirq.LineQubit(i) for i in range({self.num_qubits})]"]
        qiskit_code = ["from qiskit import QuantumCircuit", f"qc = QuantumCircuit({self.num_qubits})"]

        operations = self._get_operations()
        for op in operations:
            if self.input_backend == 'cirq':
                gate = getattr(op, 'gate', None)
                if gate:
                    qubits = [q.id for q in op.qubits]
                    if isinstance(gate, cirq.H):
                        cirq_code.append(f"circuit.append(cirq.H(qubits[{qubits[0]}]))")
                        qiskit_code.append(f"qc.h({qubits[0]})")
                    elif isinstance(gate, cirq.X):
                        cirq_code.append(f"circuit.append(cirq.X(qubits[{qubits[0]}]))")
                        qiskit_code.append(f"qc.x({qubits[0]})")
                    elif isinstance(gate, cirq.Y):
                        cirq_code.append(f"circuit.append(cirq.Y(qubits[{qubits[0]}]))")
                        qiskit_code.append(f"qc.y({qubits[0]})")
                    elif isinstance(gate, cirq.Z):
                        cirq_code.append(f"circuit.append(cirq.Z(qubits[{qubits[0]}]))")
                        qiskit_code.append(f"qc.z({qubits[0]})")
                    elif isinstance(gate, cirq.T):
                        cirq_code.append(f"circuit.append(cirq.T(qubits[{qubits[0]}]))")
                        qiskit_code.append(f"qc.t({qubits[0]})")
                    elif isinstance(gate, cirq.S):
                        cirq_code.append(f"circuit.append(cirq.S(qubits[{qubits[0]}]))")
                        qiskit_code.append(f"qc.s({qubits[0]})")
                    elif isinstance(gate, cirq.S**-1):
                        cirq_code.append(f"circuit.append(cirq.S(qubits[{qubits[0]}])**-1)")
                        qiskit_code.append(f"qc.sdg({qubits[0]})")
                    elif isinstance(gate, cirq.CNOT):
                        cirq_code.append(f"circuit.append(cirq.CNOT(qubits[{qubits[0]}], qubits[{qubits[1]}]))")
                        qiskit_code.append(f"qc.cx({qubits[0]}, {qubits[1]})")
                    elif isinstance(gate, cirq.SWAP):
                        cirq_code.append(f"circuit.append(cirq.SWAP(qubits[{qubits[0]}], qubits[{qubits[1]}]))")
                        qiskit_code.append(f"qc.swap({qubits[0]}, {qubits[1]})")
                    elif isinstance(gate, cirq.Rx):
                        theta = gate._angle
                        cirq_code.append(f"circuit.append(cirq.rx({theta})(qubits[{qubits[0]}]))")
                        qiskit_code.append(f"qc.rx({theta}, {qubits[0]})")
                    elif isinstance(gate, cirq.Ry):
                        theta = gate._angle
                        cirq_code.append(f"circuit.append(cirq.ry({theta})(qubits[{qubits[0]}]))")
                        qiskit_code.append(f"qc.ry({theta}, {qubits[0]})")
                    elif isinstance(gate, cirq.Rz):
                        theta = gate._angle
                        cirq_code.append(f"circuit.append(cirq.rz({theta})(qubits[{qubits[0]}]))")
                        qiskit_code.append(f"qc.rz({theta}, {qubits[0]})")
            else:
                name = op.name
                qubits = [q.index for q in op.qubits]
                params = op.params
                if name == 'h':
                    cirq_code.append(f"circuit.append(cirq.H(qubits[{qubits[0]}]))")
                    qiskit_code.append(f"qc.h({qubits[0]})")
                elif name == 'x':
                    cirq_code.append(f"circuit.append(cirq.X(qubits[{qubits[0]}]))")
                    qiskit_code.append(f"qc.x({qubits[0]})")
                elif name == 'y':
                    cirq_code.append(f"circuit.append(cirq.Y(qubits[{qubits[0]}]))")
                    qiskit_code.append(f"qc.y({qubits[0]})")
                elif name == 'z':
                    cirq_code.append(f"circuit.append(cirq.Z(qubits[{qubits[0]}]))")
                    qiskit_code.append(f"qc.z({qubits[0]})")
                elif name == 't':
                    cirq_code.append(f"circuit.append(cirq.T(qubits[{qubits[0]}]))")
                    qiskit_code.append(f"qc.t({qubits[0]})")
                elif name == 's':
                    cirq_code.append(f"circuit.append(cirq.S(qubits[{qubits[0]}]))")
                    qiskit_code.append(f"qc.s({qubits[0]})")
                elif name == 'sdg':
                    cirq_code.append(f"circuit.append(cirq.S(qubits[{qubits[0]}])**-1)")
                    qiskit_code.append(f"qc.sdg({qubits[0]})")
                elif name == 'cx':
                    cirq_code.append(f"circuit.append(cirq.CNOT(qubits[{qubits[0]}], qubits[{qubits[1]}]))")
                    qiskit_code.append(f"qc.cx({qubits[0]}, {qubits[1]})")
                elif name == 'swap':
                    cirq_code.append(f"circuit.append(cirq.SWAP(qubits[{qubits[0]}], qubits[{qubits[1]}]))")
                    qiskit_code.append(f"qc.swap({qubits[0]}, {qubits[1]})")
                elif name == 'rx' and params:
                    cirq_code.append(f"circuit.append(cirq.rx({params[0]})(qubits[{qubits[0]}]))")
                    qiskit_code.append(f"qc.rx({params[0]}, {qubits[0]})")
                elif name == 'ry' and params:
                    cirq_code.append(f"circuit.append(cirq.ry({params[0]})(qubits[{qubits[0]}]))")
                    qiskit_code.append(f"qc.ry({params[0]}, {qubits[0]})")
                elif name == 'rz' and params:
                    cirq_code.append(f"circuit.append(cirq.rz({params[0]})(qubits[{qubits[0]}]))")
                    qiskit_code.append(f"qc.rz({params[0]}, {qubits[0]})")

        cirq_code.append("print(circuit)")
        qiskit_code.append("print(qc)")
        return {
            "cirq": "\n".join(cirq_code),
            "qiskit": "\n".join(qiskit_code)
        }

    def analyze_circuit(self) -> Dict[str, Any]:
        ideal_exp, ideal_energy = self.execute_ideal()
        raw_exp, raw_energy = self.execute_raw()
        mitigated_exp, mitigated_energy = self.mitigate_error()
        transpiled = self.transpile()
        results = {
            "results": {
                "ideal": {"expectation": ideal_exp, "energy": ideal_energy},
                "raw": {"expectation": raw_exp, "energy": raw_energy},
                "mitigated": {"expectation": mitigated_exp, "energy": mitigated_energy}
            },
            "transpiled_code": transpiled
        }
        logger.info(f"Analysis for circuit {self.circuit_id}: {results}")
        return results

app = FastAPI()

class CircuitInput(BaseModel):
    circuit: str  # QASM, Cirq JSON, or native circuit string
    backend_type: str
    noise_level: float = 0.01

def create_sample_circuit(backend: str) -> Union[cirq.Circuit, QuantumCircuit]:
    if backend == 'cirq':
        q0, q1 = cirq.LineQubit.range(2)
        return cirq.Circuit(cirq.H(q0), cirq.T(q0), cirq.CNOT(q0, q1), cirq.rx(np.pi/2)(q1))
    else:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.t(0)
        qc.cx(0, 1)
        qc.rx(np.pi/2, 1)
        return qc

@app.post("/analyze")
async def analyze_circuit(input: CircuitInput):
    try:
        transpiler = QuantumCircuitTranspiler(input.circuit, input.backend_type, input.noise_level)
        analysis = transpiler.analyze_circuit()
        return {
            "status": "success",
            "circuit": str(transpiler.circuit),
            "circuit_id": transpiler.circuit_id,
            "results": {
                "ideal": {
                    "expectation": round(analysis["results"]["ideal"]["expectation"], 4),
                    "energy": round(analysis["results"]["ideal"]["energy"], 4)
                },
                "raw": {
                    "expectation": round(analysis["results"]["raw"]["expectation"], 4),
                    "energy": round(analysis["results"]["raw"]["energy"], 4)
                },
                "mitigated": {
                    "expectation": round(analysis["results"]["mitigated"]["expectation"], 4),
                    "energy": round(analysis["results"]["mitigated"]["energy"], 4)
                }
            },
            "transpiled_code": analysis["transpiled_code"]
        }
    except Exception as e:
        logger.error(f"Error processing circuit: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    for backend in ['cirq', 'qiskit']:
        circuit = create_sample_circuit(backend)
        transpiler = QuantumCircuitTranspiler(circuit, backend)
        analysis = transpiler.analyze_circuit()
        print(f"{backend.capitalize()} Results:", {
            "results": {k: {sub_k: round(sub_v, 4) for sub_k, sub_v in v.items()} for k, v in analysis["results"].items()},
            "transpiled_code": analysis["transpiled_code"]
        })