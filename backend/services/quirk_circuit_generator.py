import json
import os
from fastapi.exceptions import HTTPException
import urllib.parse
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from services.prompt_manager import QuantumPrompt
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["GROQ_API_KEY"]

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
        try:
         quirk_data = {"cols": self.circuit}
         data = json.dumps(quirk_data)
         #encoded_data = urllib.parse.quote(json.dumps(quirk_data))
         return f"https://algassert.com/quirk#circuit={data}"
        except Exception as e:
            return HTTPException(status_code=500,detail=f"{e}")

class QuantumLLM:
    def __init__(self):
        self.quantum = ChatGroq(api_key=api_key)

    def llm_request(self):
        try:
          user_input = QuantumPrompt.get_prompt()
          messages = [
             SystemMessage(content="you are a helpful assistant."),
             HumanMessage(content=user_input)
          ]
          response = self.quantum(messages, model="llama3-8b-8192", temperature=0.5, max_tokens=1024, top_p=1)
          print(response)
          return response['text']
        except Exception as e:
            return HTTPException(status_code=500,detail=f"{e}")