from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import io
import base64
import cirq

class QuantumSimulator:
    def qiskit_code_simulate(self, code: str):
        try:
            exec_globals = {"QuantumCircuit": QuantumCircuit}
            exec(code, exec_globals)
            if "qc" not in exec_globals:
                raise ValueError("Qiskit code must define a QuantumCircuit named 'qc'")
            qc = exec_globals["qc"]
            simulator = AerSimulator()
            compiled_circuit = transpile(qc, simulator)
            result = simulator.run(compiled_circuit).result()
            counts = result.get_counts()
            print(f"Qiskit simulation result: {counts}")
            return counts
        except Exception as e:
            return f"Qiskit Simulation Error: {e}"

    def cirq_code_simulate(self, code: str):
        try:
            exec_globals = {"cirq": cirq}
            exec(code, exec_globals)
            if "circuit" not in exec_globals:
                raise ValueError("Cirq code must define a Circuit named 'circuit'")
            circuit = exec_globals["circuit"]
            simulator = cirq.Simulator()

            # Execute the circuit on the simulator
            result = simulator.run(circuit, repetitions=10)
            return f"Cirq simulation result: {result}"
        except Exception as e:
            return f"Cirq Simulation Error: {e}"
    
    def generate_qiskit_histogram(self,qiskit_result:dict):
        try:
          fig = plot_histogram(qiskit_result)
          buffer = io.BytesIO()
          fig.savefig(buffer,format='png')
          plt.close(fig)
          buffer.seek(0)
          img_str = base64.b64encode(buffer.read()).decode('utf-8')
          print(img_str) #comment if not neccesary
          return img_str
        except Exception as e:
            print(f"{e}")

    def generate_cirq_histogram(cirq_result):
        hist = cirq.plot_state_histogram(cirq_result)
        buffer = io.BytesIO()
        hist.figure.savefig(buffer,format="png")
        plt.close(hist.figure)
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode("utf-8")
        print(img_str)
        return img_str

#Example Usage   
if __name__ == "__main__":
    simulator = QuantumSimulator()
    qiskit_code = """
       qc = QuantumCircuit(2, 2)
       qc.h(0)
       qc.cx(0, 1)
       qc.measure([0, 1], [0, 1])
    """

    cirq_code = """
        q0, q1 = cirq.LineQubit.range(2)
        circuit = cirq.Circuit(
            cirq.H(q0),
            cirq.CX(q0, q1),
            cirq.measure(q0, q1, key='result')
        )
    """

    qiskit_result = simulator.qiskit_code_simulate(qiskit_code)
    print(qiskit_result)

    cirq_result = simulator.cirq_code_simulate(cirq_code)
    print(cirq_result)


    qiskit_codes = """
    import numpy as np
    from qiskit.circuit.library import QFT
    n_count = 3
    theta = 1/3
    qc = QuantumCircuit(n_count + 1, n_count)
    for q in range(n_count):
      qc.h(q)
    for q in range(n_count):
        repetitions = 2**q  # 1, 2, 4,... (powers of 2)
        for _ in range(repetitions):
           qc.cp(2 * np.pi * theta, q, n_count)  # Controlled phase rotation
    qc.append(QFT(n_count, do_swaps=False).inverse(), range(n_count))
    qc.measure(range(n_count), range(n_count))
    """

    qiskit_codes_2 = """
    from qiskit import QuantumCircuit
    import math
    qc = QuantumCircuit(5)
    qc.h(0)
    qc.h(1)
    qc.h(2)
    qc.h(3)
    qc.h(4)
    qc.z(0, math.pi)
    qc.z(1, math.pi)
    qc.z(2, math.pi)
    qc.z(3, math.pi)
    qc.z(4, math.pi)
    qc.measure_all()
    """

    print(simulator.qiskit_code_simulate(qiskit_codes))