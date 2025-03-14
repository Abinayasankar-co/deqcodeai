from abc import ABC, abstractmethod
from qiskit import QuantumCircuit
from qiskit.qasm2 import loads as qiskit_qasm_loads
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CommutativeCancellation, CXDirection, Optimize1qGatesDecomposition
import pyzx as zx
import cirq
from typing import Union, Optional
import logging

#https://grok.com/share/bGVnYWN5_be6274e6-3d9b-4cb5-89e8-8c0d0349287d

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CircuitConverter:
    """Handles conversion between different quantum circuit formats."""
    
    @staticmethod
    def to_qiskit(circuit: Union[QuantumCircuit, cirq.Circuit, str]) -> QuantumCircuit:
        """Convert input circuit to Qiskit QuantumCircuit."""
        if isinstance(circuit, QuantumCircuit):
            return circuit
        elif isinstance(circuit, cirq.Circuit):
            # Convert Cirq circuit to OpenQASM, then to Qiskit
            qasm_str = cirq.qasm(circuit)
            return qiskit_qasm_loads(qasm_str)
        elif isinstance(circuit, str):
            # Assume string is OpenQASM
            try:
                return qiskit_qasm_loads(circuit)
            except Exception as e:
                raise ValueError(f"Invalid OpenQASM string: {str(e)}")
        else:
            raise ValueError(f"Unsupported circuit type: {type(circuit)}")

    @staticmethod
    def from_qiskit(circuit: QuantumCircuit, target_format: str) -> Union[QuantumCircuit, cirq.Circuit, str]:
        """Convert Qiskit circuit back to the target format."""
        if target_format.lower() == "qiskit":
            return circuit
        elif target_format.lower() == "cirq":
            qasm_str = circuit.qasm()
            return cirq.read_qasm(qasm_str)
        elif target_format.lower() == "openqasm":
            return circuit.qasm()
        else:
            raise ValueError(f"Unsupported target format: {target_format}")

class QuantumCircuitOptimizerBase(ABC):
    """Abstract base class for quantum circuit optimizers."""
    
    @abstractmethod
    def optimize(self, circuit: QuantumCircuit) -> QuantumCircuit:
        """Optimize a Qiskit QuantumCircuit."""
        pass

    def _validate_circuit(self, circuit: QuantumCircuit) -> None:
        """Validate the Qiskit circuit for tensor shape consistency."""
        if not isinstance(circuit, QuantumCircuit):
            raise ValueError("Input must be a Qiskit QuantumCircuit object.")
        if circuit.num_qubits == 0:
            raise ValueError("Circuit must have at least one qubit.")
        logging.info(f"Validated circuit with {circuit.num_qubits} qubits and {circuit.size()} gates.")

class SmallCircuitOptimizer(QuantumCircuitOptimizerBase):
    """Optimizer for small circuits (<= 50 gates) using Qiskit passes."""
    
    def __init__(self):
        self._pass_manager = PassManager([
            CommutativeCancellation(),
            CXDirection(),
            Optimize1qGatesDecomposition()
        ])
        logging.info("Initialized SmallCircuitOptimizer with Qiskit passes.")

    def optimize(self, circuit: QuantumCircuit) -> QuantumCircuit:
        """Optimize small circuits using Qiskit passes."""
        self._validate_circuit(circuit)
        try:
            optimized_circuit = self._pass_manager.run(circuit)
            logging.info(f"Optimized small circuit: {circuit.size()} -> {optimized_circuit.size()} gates.")
            return optimized_circuit
        except Exception as e:
            raise RuntimeError(f"Small circuit optimization failed: {str(e)}")

class LargeCircuitOptimizer(QuantumCircuitOptimizerBase):
    """Optimizer for large circuits (> 50 gates) using ZX-calculus."""
    
    def __init__(self):
        logging.info("Initialized LargeCircuitOptimizer with PyZX.")

    def optimize(self, circuit: QuantumCircuit) -> QuantumCircuit:
        """Optimize large circuits using PyZX ZX-calculus."""
        self._validate_circuit(circuit)
        try:
            zx_circuit = zx.Circuit.from_qiskit(circuit)
            zx_graph = zx_circuit.to_graph()
            zx.simplify.full_reduce(zx_graph)
            optimized_circuit = zx.extract_circuit(zx_graph).to_qiskit()
            logging.info(f"Optimized large circuit: {circuit.size()} -> {optimized_circuit.size()} gates.")
            return optimized_circuit
        except Exception as e:
            raise RuntimeError(f"Large circuit optimization failed: {str(e)}")

class QuantumCircuitOptimizer:
    """Main optimizer class supporting multiple frameworks."""
    
    SUPPORTED_FORMATS = {"qiskit", "cirq", "openqasm"}
    
    def __init__(self, size_threshold: int = 50):
        self._size_threshold = size_threshold
        self._small_optimizer = SmallCircuitOptimizer()
        self._large_optimizer = LargeCircuitOptimizer()
        self._converter = CircuitConverter()
        self._original_circuit = None
        self._optimized_circuit: Optional[QuantumCircuit] = None
        self._input_format: Optional[str] = None
        logging.info(f"QuantumCircuitOptimizer initialized with threshold: {size_threshold} gates.")

    def _is_large_circuit(self, circuit: QuantumCircuit) -> bool:
        return circuit.size() > self._size_threshold

    def optimize(self, circuit: Union[QuantumCircuit, cirq.Circuit, str], input_format: str = "qiskit") -> any:
        """Optimize a circuit from any supported framework."""
        if input_format.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported input format: {input_format}. Supported: {self.SUPPORTED_FORMATS}")
        
        self._input_format = input_format.lower()
        # Convert to Qiskit for internal processing
        qiskit_circuit = self._converter.to_qiskit(circuit)
        self._original_circuit = qiskit_circuit.copy()
        
        # Choose optimizer based on size
        optimizer = self._large_optimizer if self._is_large_circuit(qiskit_circuit) else self._small_optimizer
        self._optimized_circuit = optimizer.optimize(qiskit_circuit)
        
        # Validate tensor shape consistency
        if self._optimized_circuit.num_qubits != self._original_circuit.num_qubits:
            raise ValueError("Optimization altered qubit count, tensor shape mismatch detected.")
        
        # Convert back to the original format
        return self._converter.from_qiskit(self._optimized_circuit, self._input_format)

    def compare_circuits(self) -> dict:
        """Compare original and optimized circuits (in Qiskit format)."""
        if not self._original_circuit or not self._optimized_circuit:
            raise ValueError("Run optimization first to compare circuits.")
        
        comparison = {
            "original_gates": self._original_circuit.size(),
            "optimized_gates": self._optimized_circuit.size(),
            "original_depth": self._original_circuit.depth(),
            "optimized_depth": self._optimized_circuit.depth()
        }
        logging.info(f"Circuit comparison: {comparison}")
        return comparison

# Example usage with different frameworks
if __name__ == "__main__":
    # Qiskit circuit
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.measure_all()

    # Cirq circuit
    qubits = cirq.LineQubit.range(3)
    cirq_circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2]),
        cirq.measure(*qubits, key="result")
    )

    # OpenQASM string
    qasm_str = """
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[3];
    h q[0];
    cx q[0],q[1];
    cx q[1],q[2];
    measure q[0] -> c[0];
    measure q[1] -> c[1];
    measure q[2] -> c[2];
    """

    optimizer = QuantumCircuitOptimizer(size_threshold=50)

    # Optimize Qiskit circuit
    print("Qiskit Circuit Optimization:")
    optimized_qiskit = optimizer.optimize(qc, input_format="qiskit")
    print(optimized_qiskit)
    print(optimizer.compare_circuits())

    # Optimize Cirq circuit
    print("\nCirq Circuit Optimization:")
    optimized_cirq = optimizer.optimize(cirq_circuit, input_format="cirq")
    print(optimized_cirq)

    # Optimize OpenQASM string
    print("\nOpenQASM Circuit Optimization:")
    optimized_qasm = optimizer.optimize(qasm_str, input_format="openqasm")
    print(optimized_qasm)