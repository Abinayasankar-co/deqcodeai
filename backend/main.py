from fastapi import FastAPI


app = FastAPI()


@app.get("/health")
def app_health():
    return {"health":"DeqcodeAI"}

app.post("/design-circuit")
def design_circuit():
    pass