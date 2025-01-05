import jwt
from fastapi import FastAPI , Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from db.db_handler import dbhandles
from db.datahandler import QuibitsGeneratorinput,DeqcodeUser,DeqcodeUserLogin,CodeRequest
from db.datahandler import PreviousCircuits,CircuitViewer,PricingPlan,DeqcodeLoginCredentials
from services.quirk_circuit_generator import QuantumLLM
from services.simulation import QuantumSimulator
from services.algassertprod import QuantumCircuitGenerator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="session_token")


@app.get("/health")
def app_health():
    return {"health":"DeqcodeAI"}

@app.get('/priceplan')
def pricing_plan():
   try:
      return PricingPlan(
         status_code=200,
         pricing=["free","premium","enterprise"]
      )
   except Exception as e:
      raise HTTPException(status_code=500,detail=f"{e}")

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
          return DeqcodeLoginCredentials(
             message=logger_message.get("message"),
             username=logger_message.get("username"),
             session_key=logger_message.get("session_key")
          )
        except Exception as e:
          raise HTTPException(status_code=500,detail=f"{e}")  
        
#Need more work on it     
@app.get("/api/verify-token")
async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, algorithms=["HS256"]) #Secret_key needs to be added
        return {"username": payload.get("sub")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post('/viewcircuits')
async def view_circuits(viewer : CircuitViewer):
    try:
      db = dbhandles()
      code , circuits = await db.get_circuit_info(viewer.username)
      #print(code, circuits)
      if code == 200:
          return PreviousCircuits(
           status_code= code,
           circuits=circuits,
           message="Successfull"
          )
      if code == 404:
         return PreviousCircuits(
            status_code=404,
            circuits=None,
            message=circuits.get("Message")
         )
      else:
         raise HTTPException(status_code=400,detail="No circuits Found")
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
      storage_circuit = await db.get_store_circuit(QuiBitsGeneratorinput.username,result)
      if storage_circuit: return result
    except Exception as e:
      raise HTTPException(status_code=500,detail=f"{e}")

@app.post("/simulate")
async def simulate_code(request: CodeRequest):
    simulator = QuantumSimulator()

    if not request.code or not request.simulator:
        raise HTTPException(status_code=400, detail="Code and simulator type are required")

    try:
        result = simulator.simulate(request.code, request.simulator)
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
