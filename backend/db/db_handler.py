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
          self.database = self.Client["ALSA_DB"]

    def ping_user():
         pass