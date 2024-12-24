from pymongo import MongoClient
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

        async def create_user(self): # To create the user in the database
           pass
        
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
        


