from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from services.algassertprod import QuantumCircuitGenerator
from db.db_handler import dbhandles
from db.datahandler import QuibitsGeneratorinput,DeqcodeUser,DeqcodeUserLogin,PreviousCircuits
from services.quirk_circuit_generator import QuantumLLM

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.get("/health")
def app_health():
    return {"health":"DeqcodeAI"}

@app.post('/register')
async def deqcode_user_registeration(DeqcodeUser : DeqcodeUser):
        try:          
          db_user = dbhandles()
          user_message = await db_user.create_user(DeqcodeUser)
          return user_message
        except Exception as e:
          raise HTTPException(status_code=500,detail=f"{e}") 

@app.post('/login')
async def deqcode_user_login(DeqcodeUserLogin : DeqcodeUserLogin):
        try:
          db_user = dbhandles()
          logger_message = await db_user.login_user(DeqcodeUserLogin)
          return logger_message
        except Exception as e:
          raise HTTPException(status_code=500,detail=f"{e}")  

@app.post('/viewcircuits')
async def view_circuits():
    try:
      db = dbhandles()
      circuits = await db.get_circuit_info()
      return  PreviousCircuits(
         status_code=200,
         circuits=circuits
      )
    except Exception as e:
      raise HTTPException(status_code=500,detail=f"{e}")

@app.post("/design-circuit")
async def design_circuit(QuiBitsGeneratorinput: QuibitsGeneratorinput):
    try:
      quantum_verifier = QuantumLLM()
      db = dbhandles()
      print(QuiBitsGeneratorinput.statements)
      resposnes = quantum_verifier.llm_request(QuiBitsGeneratorinput.statements)
      qc, quirk_url = QuantumCircuitGenerator.generate_circuit_from_json(resposnes)
      print(qc)
      result = {"Response":resposnes,"url":quirk_url,"content":resposnes.get("explanation")}
      await db.storing_circuit_info(QuiBitsGeneratorinput.username,result)
      return result
    except Exception as e:
      raise HTTPException(status_code=500,detail=f"{e}")

# Testing not a valid api recorded for production - caution : Don't use in documentation
@app.post('/store-circuit')
async def storing_circuit():
   try:
    json_content = {
     "Parameters": [
         {
             "n": 2,
             "p": 0.5
         }
     ],
     "gates": [
        {
              "gate": "H",
             "qubit": 0
         },
         {
            "gate": "H",
             "qubit": 1
         }, 
         {
            "gate": "RX",
            "qubit": 0,
            "angle": "acos(sqrt(p))"
        },
        {
            "gate": "RX",
            "qubit": 1,
            "angle": "acos(sqrt(p))"
        },
        {
            "gate": "CX",
            "control_qubit": 0,
            "target_qubit": 1
        },
        {
            "gate": "Measure",
            "qubit": 0
        },
        {
            "gate": "Measure",
            "qubit": 1
        }
        ],
        "explanation": "This circuit generates a random number by applying Hadamard gates, RX gates with a probability p, and measuring the qubits."        
     }
    content = "This circuit generates a random number by applying Hadamard gates, entangling the qubits using CCX gate and measuring the qubits."
    url = "https://algassert.com/quirk#circuit=%7B%22cols%22%3A%20%5B%5B%7B%22id%22%3A%20%22H%22%2C%20%22targets%22%3A%20%5B0%5D%7D%5D%2C%20%5B%7B%22id%22%3A%20%22H%22%2C%20%22targets%22%3A%20%5B1%5D%7D%5D%2C%20%5B%7B%22id%22%3A%20%22Measure%22%2C%20%22targets%22%3A%20%5B0%5D%7D%5D%2C%20%5B%7B%22id%22%3A%20%22Measure%22%2C%20%22targets%22%3A%20%5B1%5D%7D%5D%5D%7D"
    db = dbhandles()
    circuit = {"Response":json_content,"url":url,"content":content}
    result =  await db.storing_circuit_info("Abinayasankar",circuit)
    return result
   except Exception as e:
     raise HTTPException(status_code=500,detail=f"All is not fine{e}")  

#Testing not a valid circuit api for production - caution : Don't use in documentation
@app.post("/generate_circuit")
async def generate_circuit(parameters: list, gates: list):
    llm = QuantumLLM()
    response = llm.llm_request(parameters, gates)
    generator = QuantumCircuitGenerator()
    generator.add_qubits(3)
    generator.add_gate("H", [0])
    generator.add_gate("CX", [1], controls=[0])
    generator.add_gate("RZ", [2], params=[1.57])
    quirk_json = generator.generate_json()
    quirk_url = generator.generate_quirk_url()
    return {"llm_response": response, "quirk_json": quirk_json, "quirk_url": quirk_url}
