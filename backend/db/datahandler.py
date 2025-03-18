from pydantic import BaseModel
from fastapi import Form,UploadFile
from typing import List
from typing import Optional
from datetime import datetime

class PricingPlan(BaseModel):
    status_code : int
    pricing : List
class CodeRequest(BaseModel):
    code: str
    simulator: str
class PreviousCircuits(BaseModel):
    status_code : int 
    circuits : Optional[List[dict]]
    message : Optional[str] 

class DeqcodeLoginCredentials(BaseModel):
    message : str
    username : str 
    session_key : str

class QuibitsGeneratorinput(BaseModel):
    username : str = Form(...)
    statements : str = Form(...)

class DeqcodeUser(BaseModel):
   username : str = Form(...)
   email:str = Form(...)
   password : str = Form(...)
   competency : str = Form(...)
   purpose : str = Form(...)
   education : str = Form(...)
   foundby : str = Form(...)
   review : str = Form(...)
   notesbyuser : str = Form(...)
   preference : str = Form(...)
   enterprise : Optional[bool] = False
   shared : Optional[List] = []
   created_dt: Optional[datetime] = datetime.now()
   modified_by: Optional[str] = None
   modified_dt: Optional[datetime] = None

class DeqcodeUserLogin(BaseModel):
    username : str = Form(...)
    password : str = Form(...)

class CircuitViewer(BaseModel):
    username :str = Form(...)
    #companyname : Optional[str] = Form(...)

class UserQuery(BaseModel):
    username :str = Form(...)
    querymsg :str = Form(...)
    imgdata : Optional[UploadFile] = None

class CircuitInput(BaseModel):
    circuit : str
    backend_type: str
    noise_level: float = 0.01

class Enterprise(BaseModel):
    companyname : str
    password : str
    Owner: str
    activeplan : str
    Members: List[str]
    Circuits : List[object]
    Circuitcount : int
    paidlastmonth : bool = False
    paidmonths : List
    nonpaidmonths : List
    isindeactivation : bool = False
    warned : bool = False
    planvalidity : datetime 
    billing : List
    dateofjoining : datetime = datetime.now()


class EnterpriseMembers(BaseModel):
   companyname : str
   totalcount : int
   Owner : str
   memberscount : int 
   memberslist : str

class Applycredits(BaseModel):
    ownername: Optional[str] = Form(None),
    companyname: Optional[str] = Form(None),
    companyaddress: Optional[str] = Form(None),
    usagelimit: Optional[int] = Form(None),
    username: Optional[str] = Form(None),
    projectscope: Optional[str] = Form(None),
    projectduration: Optional[int] = Form(None),
    purpose: Optional[str] = Form(None),
    researchtopic: Optional[str] = Form(None),
    expecteddatapoints: Optional[int] = Form(None),
    researchduration: Optional[int] = Form(None),
    samplesize: Optional[int] = Form(None)

