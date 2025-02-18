import json
import math
import urllib.parse
from qiskit import QuantumCircuit

class QuantumCircuitGenerator:
    supported_gates = {
        "H", "X", "Y", "Z", "S", "T", "CX", "CCX", "SWAP", "RX", "RY", "RZ",
        "Measure", "InputA", "InputB", "InputC", "Ryft", "ZDetector", "YDetector", "ZDetectControlReset"
    }
    def __init__(self):
        self.circuit = []
    def add_qubits(self, count):
        self.qubit_count = count
    def validate_gate(self, gate):
        if gate not in self.supported_gates:
            raise ValueError(f"Gate '{gate}' is not supported by Quirk.")
    def add_gate(self, gate, targets, controls=None, params=None):
        self.validate_gate(gate)
        all_indices = (targets if targets else []) + (controls if controls else [])
        if any(index >= self.qubit_count for index in all_indices):
            raise ValueError("Target or control index out of range.")
        gate_dict = {"id": gate, "targets": targets}
        if controls:
            gate_dict["controls"] = controls
        if params:
            gate_dict["params"] = params
        self.circuit.append([gate_dict])
    def generate_json(self):
        return json.dumps({"cols": self.circuit}, indent=2)
    def generate_quirk_url(self):
        quirk_data = {"cols": self.circuit}
        parsed_data = urllib.parse.quote(json.dumps(quirk_data))
        return f"https://algassert.com/quirk#circuit={parsed_data}"
    @staticmethod
    def generate_circuit_from_json(input_data):
        parameters = input_data.get("Parameters", [{}])[0]
        n = parameters.get("n", 1)
        qc = QuantumCircuit(n)
        generator = QuantumCircuitGenerator()
        generator.add_qubits(n)
        for gate_info in input_data.get("gates", []):
            gate = gate_info.get("gate")
            qubits = gate_info.get("qubits", [])
            if isinstance(qubits, int):
                qubits = [qubits]
            elif not qubits:
                qubits = [gate_info.get("qubit", 0)]
            params = gate_info.get("params", [])
            if isinstance(params, (int, float)):
                params = [params]
            if gate in QuantumCircuitGenerator.supported_gates:
                try:
                    if gate == "H":
                        qc.h(qubits[0])
                    elif gate == "X":
                        qc.x(qubits[0])
                    elif gate == "Y":
                        qc.y(qubits[0])
                    elif gate == "Z":
                        qc.z(qubits[0])
                    elif gate == "S":
                        qc.s(qubits[0])
                    elif gate == "T":
                        qc.t(qubits[0])
                    elif gate == "CX":
                        qc.cx(qubits[0], qubits[1])
                    elif gate == "CCX":
                        qc.ccx(qubits[0], qubits[1], qubits[2])
                    elif gate == "SWAP":
                        qc.swap(qubits[0], qubits[1])
                    elif gate == "RX":
                        angle = params[0] if params else 0
                        qc.rx(angle, qubits[0])
                    elif gate == "RY":
                        angle = params[0] if params else 0
                        qc.ry(angle, qubits[0])
                    elif gate == "RZ":
                        angle = params[0] if params else 0
                        qc.rz(angle, qubits[0])
                    elif gate == "Ryft":
                        pass
                    elif gate == "ZDetector":
                        pass
                    elif gate == "YDetector":
                        pass
                    elif gate == "ZDetectControlReset":
                        pass
                    elif gate == "Measure":
                        qc.measure_all()
                    generator.add_gate(gate, qubits, params=params)
                except IndexError as e:
                    print(f"Warning: Missing parameters for gate {gate}: {e}")
                    continue
        quirk_url = generator.generate_quirk_url()
        return qc, quirk_url


if __name__ == "__main__":
    # Example input
    inputs_data = {
        "Parameters": [
            {
                "n": 2
            }
        ],
        "gates": [
            {"gate": "H", "qubits": [0]},
            {"gate": "CX", "qubits": [0, 1]},
            {"gate": "RX", "params": [math.pi/2], "qubits": [0]},
            {"gate": "Measure", "qubits": [0, 1]}
        ]
    }
    input_data = {
    "Parameters": [
        {
            "n_qubits": 3,
            "num_samples": 1
        }
    ],
    "gates": [
        {
            "gate": "InputC",
            "qubit": 0
        },
        {
            "gate": "RY",
            "params": [0.5],
            "qubit": 0
        },
        {
            "gate": "RY",
            "params": [0.5],
            "qubit": 1
        },
        {
            "gate": "RY",
            "params": [0.5],
            "qubit": 2
        },
        {
            "gate": "CCX",
            "control_qubit": 0,
            "target_qubit": 1
        },
        {
            "gate": "CCX",
            "control_qubit": 0,
            "target_qubit": 2
        },
        {
            "gate": "CCX",
            "control_qubit": 1,
            "target_qubit": 2
        },
        {
            "gate": "Measure",
            "qubit": 0
        },
        {
            "gate": "Measure",
            "qubit": 1
        },
        {
            "gate": "Measure",
            "qubit": 2
        }
    ]}

    # Generate the circuit and Quirk URL
    qc, quirk_url = QuantumCircuitGenerator.generate_circuit_from_json(input_data)
    print(qc.draw())
    print("Quirk URL:", quirk_url)