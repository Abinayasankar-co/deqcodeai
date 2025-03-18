from pymongo import MongoClient
from fastapi import HTTPException
from dotenv import load_dotenv
from services.util import hash_password 
from bloom_filter2 import BloomFilter
import bcrypt
import os
import urllib.parse

load_dotenv()

class dbhandles:
        def __init__(self,username=os.environ["MONGO_USERNAME"],password=os.environ["MONGO_PASSWORD"]) -> None:
          self.encoded_username = urllib.parse.quote_plus(username)
          self.encoded_password = urllib.parse.quote_plus(password)
          self.Client = MongoClient(f"mongodb+srv://{self.encoded_username}:{self.encoded_password}@alsadocs.2uqmgxl.mongodb.net/?retryWrites=true&w=majority&appName=ALSADOCS")
          self.database = self.Client["DEQODE_DB"]
          self.bloom = BloomFilter(max_elements=1000, error_rate=0.001)
        
        def is_username_present(self,username:str) -> bool:
            if username in self.bloom:
                return True
            return False

        async def create_user(self,deqcodeuser):
            try:
             collections = self.database["DEQODE_USER_LIST"]
             pack = "" 
             circuit_count = 0 
             user_document = {
               "user_name": deqcodeuser.username,
               "email":deqcodeuser.email,
               "password" : hash_password(deqcodeuser.password),
               "competency" : deqcodeuser.competency,
               "purpose" : deqcodeuser.purpose,
               "education": deqcodeuser.education,
               "pack": pack if pack else "freetrail",
               "foundby": deqcodeuser.foundby,
               "circuit_count": circuit_count,
               "Review": deqcodeuser.review,
               "Notesbyuser":deqcodeuser.notesbyuser,
               "created_dt": deqcodeuser.created_dt,
               "modified_by":deqcodeuser.modified_by,
               "modified_dt":deqcodeuser.modified_dt
             }
             self.bloom.add(deqcodeuser.username)
             insert_deqcode_user = collections.insert_one(user_document)
             if insert_deqcode_user.acknowledged:
                return {"Message":"Success!, Your a part of Deqcode"}
            except Exception as e:
                raise  HTTPException(status_code=500,detail=f"{e}")
            
        async def login_user(self, Deqcodelogger):
            try: 
                collections = self.database["DEQODE_USER_LIST"] 
                user = collections.find_one({"user_name": Deqcodelogger.username}) 
                if user: 
                    if bcrypt.checkpw(Deqcodelogger.password.encode('utf-8'), user["password"].encode('utf-8')): 
                            return  {"username": user["user_name"]} 
                    else: 
                        raise HTTPException(status_code=401, detail="Invalid password") 
                else: 
                    raise HTTPException(status_code=404, detail="User not found") 
            except Exception as e: 
                raise HTTPException(status_code=500, detail=f"Error during login: {e}")

        async def get_store_circuit(self,username : str,circuit : dict):
            try:
                collections = self.database["DEQODE_CIRCUIT_CAPTURE"] 
                user = collections.find_one({"user_name": username})
                print(user) 
                if user: # Directly push the circuit to the user's circuits list, allowing duplicates 
                    collections.update_one( {'user_name': username}, {"$push": {"circuits": circuit}}, upsert=True ) 
                else: 
                    collections.insert_one({"user_name":username,"circuits":[circuit]})
                return {"Message": "Circuit has been stored"}
            except Exception as e:
                raise HTTPException(status_code=500,detail=f"{e}")

        async def storing_circuit_info(self, username: str, circuit: dict): # Testing Portal No Repetation of Circuits will be Allowed
            try:
                collections = self.database["DEQODE_CIRCUIT_CAPTURE"]
                user = collections.find_one({"user_name": username})
                if user:
                    if not any(circuit == existing_circuit for existing_circuit in user.get("circuits",[])):
                        collections.update_one(
                         {'user_name': username, "circuits": circuit},
                         {"$set": {"circuits": circuit}}
                        )
                    if collections.find_one({'user_name': username, "circuits": circuit}) is None:
                      collections.update_one(
                        {'user_name': username},
                        {"$push": {"circuits": circuit}},
                        upsert=True
                    )
                else:
                    raise HTTPException(status_code=400, detail="User not found")
                return {"Message": "Circuit has been stored"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"{e}")

        async def get_circuit_info(self,username:str) -> dict:
            try:
                collections = self.database["DEQODE_CIRCUIT_CAPTURE"]
                user = collections.find_one({"user_name": username})
                if user:
                    return 200 , user["circuits"]
                else:
                   return 404 ,{"Message":"No Circuits Found for this User"}
            except Exception as e:
                raise HTTPException(status_code=500,detail=f"{e}")
         
        async def del_user_logs(self):
            pass
         
        async def user_input_logs(self):
            pass
        
        async def get_users(self):
            pass

        async def releasing_circuit_info(self): #Deleted Circuits
            pass

        async def apply_credits(self,applycredits):
            try:
                pass
            except Exception as e:
                raise HTTPException(f"{e}")
    
  


""""
session_token = create_session_token(Deqcodelogger.username) 
                            collections.update_one(
                                {'user_name': user["user_name"]},
                                { "$push": { "tokens": [session_token , datetime.now()] } } 
                            ) 
"""