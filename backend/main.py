import os
import jwt
import json
import secrets
import smtplib
from fastapi import FastAPI , Depends 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from db.db_handler import dbhandles
from db.datahandler import QuibitsGeneratorinput,DeqcodeUser,DeqcodeUserLogin,CodeRequest , UserQuery
from db.datahandler import PreviousCircuits,CircuitViewer,PricingPlan,DeqcodeLoginCredentials,CircuitInput
from services.quirk_circuit_generator import QuantumLLM
from services.simulation import QuantumSimulator
from services.algassertprod import QuantumCircuitGenerator
from services.util import create_session_token , remove_code
from services.ErrorCorrectioncodes import QuantumErrorMitigator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

app = FastAPI()
secret = secrets.token_hex(32)
SECRET_KEY = secret

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="session_token")
templates = Jinja2Templates(directory="templates")

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
            if db_user.is_username_present(DeqcodeUser.username):
              user_message = await db_user.create_user(DeqcodeUser)
              token = create_session_token(DeqcodeUser.username,SECRET_KEY)
              return {
               "UserMessage" : user_message,
               "session_key" : token
              }
            else:
                raise HTTPException(status_code=404,detail="User Already Found")
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"{e}")
        
@app.post('/login')
async def deqcode_user_login(DeqcodeUserLogin : DeqcodeUserLogin):
        try:
          db_user = dbhandles()
          logger_message = await db_user.login_user(DeqcodeUserLogin)
          if not logger_message:
              raise HTTPException(status_code=400,detail="Incorrect email or password")
          username = logger_message.get("username")
          token = create_session_token(username,SECRET_KEY)
          return DeqcodeLoginCredentials(
             message="Login Successful",
             username=logger_message.get("username"),
             session_key=token
          )
        except Exception as e:
          raise HTTPException(status_code=500,detail=f"{e}")  
        
#Need more work on it     
@app.get("/verify-token")
async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=["HS256"]) #Secret_key needs to be added
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
      print(QuiBitsGeneratorinput.statements) #Comment After Execution during Production
      resposnes = quantum_verifier.llm_request(QuiBitsGeneratorinput.statements)
      try:
        code , response = remove_code(resposnes)
        qc, quirk_url = QuantumCircuitGenerator.generate_circuit_from_json(response)
        #print(qc)
      except Exception as e:
          raise HTTPException(status_code=500, detail=f"Error Qiskit:{e}")
      result = {"Response":resposnes,"url":quirk_url,"code":code,"content":resposnes.get("explanation")}
      print(QuiBitsGeneratorinput.username)
      storage_circuit = await db.get_store_circuit(QuiBitsGeneratorinput.username,result)
      if storage_circuit: return result
    except Exception as e:
      raise HTTPException(status_code=500,detail=f"Error: {e}")

@app.post("/simulate")
async def simulate_code(request: CodeRequest):
    simulator = QuantumSimulator()
    if not request.code or not request.simulator:
        raise HTTPException(status_code=400, detail="Code and simulator type are required")
    try:
        if request.simulator == "qiskit":
            result = simulator.qiskit_code_simulate(request.code)
            print(result) #comment if not neccesary
            result_map = simulator.generate_qiskit_histogram(json.loads(result))
            #print(result_map) #comment if not neccesary
            print({"result": result,"resultmap":result_map}) #Remove During Production
            return {"result": result,"resultmap":result_map}
        elif request.simulator == "cirq":
            result = simulator.cirq_code_simulate(request.code)
            result_map = simulator.generate_cirq_histogram(json.loads(result))
            return {"result":result,"resultmap":result_map}
        else:
            raise ValueError("The Framwork is not defined")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mitigate")
async def mitigate_circuit(input: CircuitInput):
    circuit = input.circuit
    mitigator = QuantumErrorMitigator(circuit, input.backend_type, input.noise_level)
    results = mitigator.get_results()
    return {
        "status": "success",
        "circuit": str(circuit),
        "circuit_id": mitigator.circuit_id,
        "results": {
            "ideal_expectation": round(results["ideal"], 4),
            "raw_expectation": round(results["raw"], 4),
            "mitigated_expectation": round(results["mitigated"], 4)
        }
    }
    
@app.post("/query")
async def query(querymsg : UserQuery):
    try:
        query_response = None
        subject = "The Query Have been Considered"
        html_content = templates.get_template("QueryResponse.html").render(
            subject = subject,
            user_name = query_response.name,
            message_body = query_response.body,
        )
        sender_email = os.environ["EMAIL_ID"]
        receiver_email = query_response.email
        password = os.environ["EMAIL_PASSWORD"]
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg.attach(MIMEText(html_content, "html"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
          server.starttls()
          server.login(sender_email, password)
          server.sendmail(sender_email, receiver_email, msg.as_string())
          return {"message": "Email sent"}

    except Exception as e:
        raise HTTPException(status_code=500,detail=f"The Mail have not been sent but the issue is Still in Progress to Resolve")

@app.post("/enterprise/details")
async def details():
    try:
        pass
    except Exception as e:
        print(f"{e}")

@app.post("/enterprise/members")
async def members():
    try:
        pass
    except Exception as e:
        print(f"{e}")

@app.post("/enterprise/shared-data")
async def shareddata():
    try:
        pass

    except Exception as e:
        print(f"{e}")

@app.post("/enterprise/circuits")
async def enterprisecircuits():
    try:
        pass
    except Exception as e:
        print(f"{e}")

@app.post("/checkbilling")
async def checkbill():
    try:
        pass
    except Exception as e:
        print(f"{e}")

@app.post("/tranfercircuit")
async def transfercircuit():
    try:
        pass
    except Exception as e:
        print(f'{e}')

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
