from typing import Union, Callable, Dict, Any, List, Tuple
import cirq
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import numpy as np
from mitiq import zne, cdr, pec
from mitiq.interface import convert_to_mitiq
from mitiq.pec.representations.depolarizing import represent_operation_with_local_depolarizing_noise
from pydantic import BaseModel
import logging
import hashlib

# Configure logging for production use
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuantumErrorMitigator:
    def __init__(self, circuit: Union[cirq.Circuit, QuantumCircuit], backend_type: str, noise_level: float = 0.01):
        self.circuit = circuit
        self.backend_type = backend_type.lower()
        self.noise_level = noise_level
        self.validate_input()
        self.mitiq_circuit, _ = self._convert_to_mitiq()
        self.circuit_id = self._generate_circuit_id()
        logger.info(f"Initialized mitigator for {self.backend_type} circuit with ID: {self.circuit_id}")

    def validate_input(self) -> None:
        if self.backend_type not in ['cirq', 'qiskit']:
            raise ValueError("Backend must be 'cirq' or 'qiskit'")
        if not isinstance(self.circuit, (cirq.Circuit, QuantumCircuit)):
            raise ValueError(f"Invalid circuit type for {self.backend_type}")

    def _generate_circuit_id(self) -> str:
        circuit_str = str(self.circuit)
        return hashlib.md5(circuit_str.encode()).hexdigest()

    def _convert_to_mitiq(self) -> Tuple[Any, str]:
        if self.backend_type == 'cirq':
            return convert_to_mitiq(cirq.Circuit(self._get_operations()))
        return convert_to_mitiq(self.circuit)

    def _is_clifford_gate(self, gate: Any) -> bool:
        if not gate:
            return False
        if self.backend_type == 'cirq':
            clifford_types = (type(cirq.H), type(cirq.CNOT), type(cirq.S), type(cirq.Z))
            return isinstance(gate, clifford_types) or \
                   (isinstance(gate, cirq.XPowGate) and gate.exponent in {0.5, 1, -1, -0.5})
        return getattr(gate, 'name', '') in ['h', 'cx', 's', 'sdg', 'z']

    def _get_operations(self) -> List[Any]:
        if self.backend_type == 'cirq':
            return list(self.circuit.all_operations())
        return [instr.operation for instr in self.circuit.data]

    def _count_gate_types(self) -> Tuple[int, int]:
        clifford_count = non_clifford_count = 0
        for op in self._get_operations():
            gate = getattr(op, 'gate', op) if self.backend_type == 'cirq' else op
            if self._is_clifford_gate(gate):
                clifford_count += 1
            elif gate is not None:
                non_clifford_count += 1
        return clifford_count, non_clifford_count

    def _select_mitigation_strategy(self) -> Callable:
        clifford_count, non_clifford_count = self._count_gate_types()
        total_gates = clifford_count + non_clifford_count
        if total_gates == 0:
            logger.warning(f"Circuit {self.circuit_id} is empty; defaulting to ZNE")
            return zne.execute_with_zne
        if non_clifford_count == 0:
            return cdr.execute_with_cdr
        elif non_clifford_count <= 2:
            return pec.execute_with_pec
        return zne.execute_with_zne

    def _execute_cirq(self, circuit: Any, noise_level: float = 0.0) -> float:
        if not isinstance(circuit, cirq.Circuit):
            circuit = cirq.Circuit(circuit)
        simulator = cirq.DensityMatrixSimulator(
            noise=cirq.depolarize(p=noise_level) if noise_level > 0 else None
        )
        result = simulator.simulate(circuit)
        observable = np.kron(np.eye(2), np.array([[1, 0], [0, -1]], dtype=complex))
        return float(np.real(np.trace(result.final_density_matrix @ observable)))

    def _execute_qiskit(self, circuit: QuantumCircuit, noise_level: float = 0.0) -> float:
        sim = AerSimulator(method='statevector')
        circuit_with_save = circuit.copy()
        circuit_with_save.save_statevector()
        if noise_level > 0:
            noise_model = NoiseModel()
            error_1q = depolarizing_error(noise_level, 1)
            error_2q = depolarizing_error(noise_level, 2)
            noise_model.add_all_qubit_quantum_error(error_1q, ['h', 't'])
            noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])
            sim.set_options(noise_model=noise_model)
        result = sim.run(circuit_with_save).result()
        state = result.get_statevector()
        state_array = state.data
        observable = np.kron(np.eye(2), np.array([[1, 0], [0, -1]], dtype=complex))
        return float(np.real(state_array.conj().T @ observable @ state_array))

    def execute_raw(self, noise_level: float = None) -> float:
        executor = self._execute_cirq if self.backend_type == 'cirq' else self._execute_qiskit
        return executor(self.circuit, noise_level or self.noise_level)

    def execute_ideal(self) -> float:
        return self.execute_raw(0.0)

    def mitigate_error(self) -> float:
        mitigation_func = self._select_mitigation_strategy()
        executor = self._execute_cirq if self.backend_type == 'cirq' else self._execute_qiskit
        operations = self._get_operations()

        if mitigation_func == cdr.execute_with_cdr:
            try:
                return mitigation_func(
                    circuit=self.mitiq_circuit,
                    executor=lambda circ: executor(circ, self.noise_level),
                    simulator=lambda circ: executor(circ, 0.0),
                    num_training_circuits=5,
                    scale_factors=(1, 3)
                )
            except Exception as e:
                logger.error(f"CDR failed for circuit {self.circuit_id}: {str(e)}")
                return self.execute_raw()

        elif mitigation_func == pec.execute_with_pec:
            reps = {}
            for idx, op in enumerate(operations):
                op_key = f"{self.circuit_id}_{idx}"  # Use a string key to avoid unhashable Circuit
                if self.backend_type == 'cirq':
                    gate = getattr(op, 'gate', None)
                    if gate and not isinstance(gate, cirq.MeasurementGate):
                        circ = cirq.Circuit(op)
                        reps[op_key] = represent_operation_with_local_depolarizing_noise(circ, 0.001)
                else:
                    if op.name in ['h', 't', 'cx']:
                        q0, q1 = cirq.LineQubit.range(2)
                        cirq_op = {
                            'h': cirq.H(q0),
                            't': cirq.T(q0),
                            'cx': cirq.CNOT(q0, q1)
                        }.get(op.name)
                        if cirq_op:
                            circ = cirq.Circuit(cirq_op)
                            reps[op_key] = represent_operation_with_local_depolarizing_noise(circ, 0.001)
            if not reps:
                logger.warning(f"No valid PEC representations for circuit {self.circuit_id}; falling back to ZNE")
                factory = zne.inference.RichardsonFactory([1.0, 1.5, 2.0])
                return zne.execute_with_zne(
                    circuit=self.mitiq_circuit,
                    executor=lambda circ: executor(circ, self.noise_level),
                    factory=factory,
                    scale_noise=zne.scaling.fold_gates_at_random
                )
            try:
                return mitigation_func(
                    circuit=self.mitiq_circuit,
                    executor=lambda circ: executor(circ, self.noise_level),
                    representations=reps,
                    num_samples=50
                )
            except Exception as e:
                logger.error(f"PEC failed for circuit {self.circuit_id}: {str(e)}")
                return self.execute_raw()

        else:
            factory = zne.inference.RichardsonFactory([1.0, 1.5, 2.0])
            try:
                return zne.execute_with_zne(
                    circuit=self.mitiq_circuit,
                    executor=lambda circ: executor(circ, self.noise_level),
                    factory=factory,
                    scale_noise=zne.scaling.fold_gates_at_random
                )
            except Exception as e:
                logger.error(f"ZNE failed for circuit {self.circuit_id}: {str(e)}")
                return self.execute_raw()

    def get_results(self) -> Dict[str, float]:
        try:
            results = {
                "ideal": self.execute_ideal(),
                "raw": self.execute_raw(),
                "mitigated": self.mitigate_error()
            }
            logger.info(f"Results for circuit {self.circuit_id}: {results}")
            return results
        except Exception as e:
            logger.error(f"Error computing results for circuit {self.circuit_id}: {str(e)}")
            return {"ideal": 0.0, "raw": 0.0, "mitigated": 0.0}

class CircuitInput(BaseModel):
    backend_type: str
    noise_level: float = 0.01

def create_cirq_circuit() -> cirq.Circuit:
    q0, q1 = cirq.LineQubit.range(2)
    return cirq.Circuit(cirq.H(q0), cirq.T(q0), cirq.CNOT(q0, q1))

def create_qiskit_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.t(0)
    qc.cx(0, 1)
    return qc

if __name__ == "__main__":
    for backend in ['cirq', 'qiskit']:
        circuit = create_cirq_circuit() if backend == 'cirq' else create_qiskit_circuit()
        mitigator = QuantumErrorMitigator(circuit, backend)
        results = mitigator.get_results()
        print(f"{backend.capitalize()} Results:", {k: round(v, 4) for k, v in results.items()})