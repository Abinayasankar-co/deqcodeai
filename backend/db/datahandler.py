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
   created_dt: Optional[datetime] = datetime.now()
   modified_by: Optional[str] = None
   modified_dt: Optional[datetime] = None

class DeqcodeUserLogin(BaseModel):
    username : str = Form(...)
    password : str = Form(...)

class CircuitViewer(BaseModel):
    username :str = Form(...)

class UserQuery(BaseModel):
    username :str = Form(...)
    querymsg :str = Form(...)
    imgdata : Optional[UploadFile] = None
