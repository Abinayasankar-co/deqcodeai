import os
from fastapi import FastAPI
from services.llm import QuantmLLM
from services.algassertprod import QuirkCircuitGenerator
from services.quirk_circuit_generator import QuantumLLM


app = FastAPI()
api_key = os.environ("GROQ_API_KEY")

@app.get("/health")
def app_health():
    return {"health":"DeqcodeAI"}

app.post("/design-circuit")
def design_circuit():
    quantum_verifier = QuantmLLM()
    resposnes = quantum_verifier.llm_request()
    return {"Response":resposnes}

@app.post("/generate_circuit")
async def generate_circuit(parameters: list, gates: list):
    llm = QuantumLLM(api_key)
    response = llm.llm_request(parameters, gates)
    generator = QuirkCircuitGenerator()
    generator.add_qubits(3)
    generator.add_gate("H", [0])
    generator.add_gate("CX", [1], controls=[0])
    generator.add_gate("RZ", [2], params=[1.57])
    quirk_json = generator.generate_json()
    quirk_url = generator.generate_quirk_url()
    return {"llm_response": response, "quirk_json": quirk_json, "quirk_url": quirk_url}
