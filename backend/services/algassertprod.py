#Sample Codes for our references this code have not been included in Production
import json
import urllib.parse

class QuirkCircuitGenerator:
    def __init__(self):
        self.supported_gates = {
            "H", "X", "Y", "Z", "S", "T", "CX", "CCX", "SWAP", "RX", "RY", "RZ",
            "Measure", "InputA", "InputB", "InputC"
        }
        self.circuit = []
        self.qubit_count = 0

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
        data = json.dumps(quirk_data)
        #encoded_data = urllib.parse.quote(json.dumps(quirk_data))
        return f"https://algassert.com/quirk#circuit={data}"
    

if __name__ == "__main__":
    # Example input
    input_data = {
  'Parameters': [
    {
      'n_qubits': 1,
      'num_samples': 1024
    }
  ],
  'gates': [
    {
      'gate': 'H',
      'qubit': 0
    },
    {
      'gate': 'RZ',
      'qubit': 0,
      'params': [
        0.5
      ]
    },
    {
      'gate': 'RX',
      'qubit': 0,
      'params': [
        0.5
      ]
    },
    {
      'gate': 'H',
      'qubit': 0
    }
  ],
  'code': {
    'import': 'from qiskit import QuantumCircuit, execute',
    'qc': 'qc = QuantumCircuit(n_qubits)',
    'qc_h': 'qc.h(0)',
    'qc_rz': 'qc.rz(0.5, 0)',
    'qc_rx': 'qc.rx(0.5, 0)',
    'qc_h_again': 'qc.h(0)',
    'job': 'job = execute(qc, shots=num_samples)'
  }
}

    generator = QuirkCircuitGenerator()
    generator.add_qubits(input_data["Parameters"][0]["n_qubits"])

    for gate in input_data["gates"]:
        generator.add_gate(
            gate["gate"],
            [gate["qubit"]],
            params=gate.get("params")
        )

    quirk_json = generator.generate_json()
    quirk_url = generator.generate_quirk_url()

    print("Quirk JSON:")
    print(quirk_json)
    print("\nQuirk URL:")
    print(quirk_url)