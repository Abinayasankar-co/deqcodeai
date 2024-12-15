import json
import urllib.parse

class QuirkCircuitGenerator:
    def __init__(self):
        # Supported Quirk gates
        self.supported_gates = {
            "H", "X", "Y", "Z", "S", "T", "CX", "CCX", "SWAP", "RX", "RY", "RZ",
            "Measure", "InputA", "InputB", "InputC"
        }
        self.circuit = []  # Stores the circuit configuration
        self.qubit_count = 0

    def add_qubits(self, count):
        """
        Sets the number of qubits for the circuit.
        """
        self.qubit_count = count

    def validate_gate(self, gate):
        """
        Validates whether the gate is supported by Quirk.
        """
        if gate not in self.supported_gates:
            raise ValueError(f"Gate '{gate}' is not supported by Quirk.")

    def add_gate(self, gate, targets, controls=None, params=None):
        """
        Adds a gate to the circuit.

        :param gate: The name of the gate (e.g., 'H', 'X', 'RZ').
        :param targets: A list of target qubit indices.
        :param controls: A list of control qubit indices, if any.
        :param params: A list of parameters for the gate (e.g., angles for RX, RY, RZ).
        """
        # Validate gate
        self.validate_gate(gate)

        # Validate qubit indices
        all_indices = (targets if targets else []) + (controls if controls else [])
        if any(index >= self.qubit_count for index in all_indices):
            raise ValueError("Target or control index out of range.")

        # Add gate to the circuit
        gate_dict = {"id": gate, "targets": targets}
        if controls:
            gate_dict["controls"] = controls
        if params:
            gate_dict["params"] = params
        self.circuit.append([gate_dict])

    def generate_json(self):
        """
        Generates the JSON configuration for Quirk.
        """
        return json.dumps({"cols": self.circuit}, indent=2)

    def generate_quirk_url(self):
        """
        Generates a Quirk URL with the circuit encoded as a query parameter.
        """
        quirk_data = {"cols": self.circuit}
        encoded_data = urllib.parse.quote(json.dumps(quirk_data))
        return f"https://algassert.com/quirk#circuit={encoded_data}"

# Example Usage
if __name__ == "__main__":
    # Initialize the generator
    generator = QuirkCircuitGenerator()
    generator.add_qubits(3)  # Define 3 qubits

    # Add gates to the circuit
    try:
        generator.add_gate("H", [0])                 # Hadamard gate on qubit 0
        generator.add_gate("CX", [1], controls=[0]) # CNOT with control 0 and target 1
        generator.add_gate("RZ", [2], params=[1.57]) # RZ rotation on qubit 2 with π/2
    except ValueError as e:
        print(f"Error: {e}")

    # Generate JSON and Quirk URL
    quirk_json = generator.generate_json()
    quirk_url = generator.generate_quirk_url()

    # Print results
    print("Quirk JSON:")
    print(quirk_json)
    print("\nQuirk URL:")
    print(quirk_url)