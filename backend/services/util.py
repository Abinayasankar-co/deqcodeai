import json5
import re
from fastapi import HTTPException

def extract_json_from_content(content_str: str) -> dict:
    try:
        start = content_str.find('{')
        end = content_str.rfind('}')
        if start == -1 or end == -1:
            raise ValueError("No JSON structure found")
        json_str = content_str[start:end + 1]
        
        # Clean up the string
        json_str = re.sub(r'\\n', '', json_str)
        json_str = re.sub(r'\\\"', '"', json_str)
        
        # Parse JSON
        parsed_json = json5.loads(json_str)
        
        # Validate structure
        if not isinstance(parsed_json, dict):
            raise ValueError("Invalid JSON structure")
        
        return parsed_json
        
    except Exception as e:
        returned_result = {"content": content_str}
        raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}- {returned_result}")