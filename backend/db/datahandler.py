from pydantic import BaseModel
from dataclasses import dataclass
from fastapi import Form

@dataclass
class PreviousCircuits(BaseModel):
    status_code : int 
    circuits : list[dict] 


@dataclass
class QuibitsGeneratorinput(BaseModel):
    username : str = Form(...)
    statements : str = Form(...)

@dataclass
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

@dataclass
class DeqcodeUserLogin(BaseModel):
    username : str = Form(...)
    password : str = Form(...)


@dataclass
class CircuitViewer(BaseModel):
    username :str = Form(...)
