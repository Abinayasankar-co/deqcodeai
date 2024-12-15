from fastapi import FastAPI
from services.llm import QuantmLLM


app = FastAPI()


@app.get("/health")
def app_health():
    return {"health":"DeqcodeAI"}

app.post("/design-circuit")
def design_circuit():
    quantum_verifier = QuantmLLM()
    resposnes = quantum_verifier.llm_request()
    return {"Response":resposnes}
