from pydantic import BaseModel
from fastapi import FastAPI,Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from services.algassertprod import QuantumCircuitGenerator
from db.db_handler import dbhandles
from services.quirk_circuit_generator import QuantumLLM

app = FastAPI()


class QuibitsGeneratorinput(BaseModel):
    username : str = Form(...)
    statements : str = Form(...)

class DeqcodeUser(BaseModel):
   username : str = Form(...)
   password : str = Form(...)
   competency : str = Form(...)
   purpose : str = Form(...)
   education : str = Form(...)
   foundby : str = Form(...)
   review : str = Form(...)
   notesbyuser : str = Form(...)
   preference : str = Form(...)
   dateofjoin : str = Form(...)

class DeqcodeUserLogin(BaseModel):
    username : str = Form(...)
    password : str = Form(...)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify the exact origin(s) you want to allow
    allow_credentials=True,
    allow_methods=["*"],  # Explicitly allow specific methods
    allow_headers=["*"],  # Allows all headers, you can specify specific headers as well
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

@app.post("/design-circuit")
def design_circuit(QuiBitsGeneratorinput: QuibitsGeneratorinput):
    try:
      quantum_verifier = QuantumLLM()
      db = dbhandles()
      print(QuiBitsGeneratorinput.statements)
      resposnes = quantum_verifier.llm_request(QuiBitsGeneratorinput.statements)
      qc, quirk_url = QuantumCircuitGenerator.generate_circuit_from_json(resposnes)
      print(qc)
      result = {"Response":resposnes,"url":quirk_url,"content":resposnes.get("explanation")}
      db.storing_circuit_info(result)
      return result
    except Exception as e:
     raise HTTPException(status_code=500,detail=f"{e}")
    
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
