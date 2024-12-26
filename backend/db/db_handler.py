from pymongo import MongoClient
from fastapi import HTTPException
from dotenv import load_dotenv
import bcrypt
import urllib.parse
import base64


class dbhandles:
        def __init__(self,username="ALSA_LOGIN_MANAGER",password="Abinay@200504") -> None:
          self.encoded_username = urllib.parse.quote_plus(username)
          self.encoded_password = urllib.parse.quote_plus(password)
          self.Client = MongoClient(f"mongodb+srv://{self.encoded_username}:{self.encoded_password}@alsadocs.2uqmgxl.mongodb.net/?retryWrites=true&w=majority&appName=ALSADOCS")
          self.database = self.Client["DEQODE_DB"]

        async def create_user(self,deqcodeuser): # To create the user in the database
            try:
             collections = self.database["DEQODE_USER_LIST"]
             pack = "" #need to make the user a special request form the frontend for this area
             circuit_count = 0 
             user_document = {
               "user_name": deqcodeuser.username,
               "password" : deqcodeuser.password,
               "competency" : deqcodeuser.competency,
               "purpose" : deqcodeuser.purpose,
               "education": deqcodeuser.education,
               "pack": pack if pack else "freetrail",
               "foundby": deqcodeuser.foundby,
               "circuit_count": circuit_count,
               "Review": deqcodeuser.review,
               "Notesbyuser":deqcodeuser.notesbyuser,
               "Dateofjoin": deqcodeuser.dateofjoin
             } 
             insert_deqcode_user = collections.insert_one(user_document)
             if insert_deqcode_user.acknowledged:
                return {"Message":"Success!, Your a part of Deqcode"}
            except Exception as e:
                raise  HTTPException(status_code=500,detail=f"{e}")
            
        async def login_user(self): # To login the user in the database
            pass

        async def get_user(self):
            pass

        async def update_user_details(self):
            pass

        async def storing_circuit_info(self):
            pass

        async def releasing_circuit_info(self):
            pass

        async def get_circuit_info(self):
            pass
        
        async def del_user_logs(self):
            pass
        
        async def user_input_logs(self):
            pass

        async def static_deqode_pricing_plans(self):
            pass
        


