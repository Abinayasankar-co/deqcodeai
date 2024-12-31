import json5
from datetime import datetime, timedelta
import random
import re
import jwt
import bcrypt
from fastapi import HTTPException

def extract_json_from_content(content_str: str) -> dict:
    try:
        start = content_str.find('{')
        end = content_str.rfind('}')
        if start == -1 or end == -1:
            raise ValueError("No JSON structure found")
        json_str = content_str[start:end + 1]
        json_str = re.sub(r'\\n', '', json_str)
        json_str = re.sub(r'\\\"', '"', json_str)
        parsed_json = json5.loads(json_str) # Parse the JSON string using json5
        if not isinstance(parsed_json, dict):
            raise ValueError("Invalid JSON structure") 
        return parsed_json
    except Exception as e:
        returned_result = {"content": content_str}
        raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}- {returned_result}")

def hash_password(password: str) -> str:
        try:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            return hashed.decode('utf-8')
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"While Processing Request :{e}") 
        
def create_session_token(username: str) -> str:
    payload = {
        "sub" : username,
        "iot" : datetime.now().isoformat(),
        "exp": datetime.now() + timedelta(hours=2)
    }
    token_secret = lambda username : ''.join(random.shuffle(list(username)))
    token = jwt.encode(payload, token_secret, algorithm="SHA256")
    return token
        
