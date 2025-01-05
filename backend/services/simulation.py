from qiskit import Aer, execute, QuantumCircuit
import cirq
from functools import singledispatchmethod

class QuantumSimulator:
    @singledispatchmethod
    def simulate(self, code: str) -> str:
        raise ValueError("Unsupported quantum framework. Use Qiskit or Cirq.")

    @simulate.register
    def _(self, code: str, framework: str = "qiskit") -> str:
        exec_globals = {"QuantumCircuit": QuantumCircuit, "Aer": Aer, "execute": execute}
        exec(code, exec_globals)

        if "qc" not in exec_globals:
            raise ValueError("Qiskit code must define a QuantumCircuit named 'qc'")
        
        qc = exec_globals["qc"]
        simulator = Aer.get_backend("qasm_simulator")
        job = execute(qc, simulator)
        result = job.result().get_counts()
        return f"Qiskit simulation result: {result}"

    @simulate.register
    def _(self, code: str, framework: str = "cirq") -> str:
        exec_globals = {"cirq": cirq}
        exec(code, exec_globals)

        if "circuit" not in exec_globals:
            raise ValueError("Cirq code must define a Circuit named 'circuit'")
        
        circuit = exec_globals["circuit"]
        simulator = cirq.Simulator()
        result = simulator.run(circuit)
        return f"Cirq simulation result: {result}"
