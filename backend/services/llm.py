#Sample Code this code  have not been included in production
import os
import json
from fastapi.exceptions import HTTPException
from groq import Groq
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from services.prompt_manager import QuantumPrompt
from services.util import extract_json_from_content
from dotenv import load_dotenv


load_dotenv()

load_dotenv()

api_key = os.environ["GROQ_API_KEY"]

class QuantmLLM:
    def  __init__(self):
        self.quantum = Groq(api_key=api_key)
        pass

    def llm_request(self):
        messages=[
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        {
            "role": "user",
            "content":"""Provide a circiut gates for quantum circuit for generating random numbers.
             The output should only be in the json as mentioning the parameters and the gates.
             The keys of json are {
             "Parameters":[{
                0:First params to be included
                1:second params to be included
             }
             ],
             "gates":[
                0:The first gate invloved in operation
                1:The second gate involved in operation            
             ],
             "code":This contains the relevant quiskit code for this
             }
             Note : You should only provide the json in the Output no other explanations needed.
             Always ensure that your json output Object format is correct which is of high importance
             """,
         }
        ]
        responses = self.quantum.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
        )
        return responses
    
class QuantumLLM:
    def __init__(self):
        self.quantum = ChatGroq(api_key=api_key)

    def llm_request(self,statements : str) -> object:
        try:
          user_input = QuantumPrompt.get_prompt(statement=statements)
          messages = [
             SystemMessage(content="you are a helpful assistant providing answers only in a strucutred Valid json format."),
             HumanMessage(content=user_input)
          ]
          response = self.quantum.invoke(messages, model="llama3-8b-8192", temperature=0.5, max_tokens=3000, top_p=1)
          content_str = response.content 
          print(content_str)
          try:
                content = extract_json_from_content(content_str)
                print(content)
          except json.JSONDecodeError as json_err:
                raise HTTPException(status_code=500, detail=f"JSON decode error: {json_err}")
          print(content)
          return content
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"{e}")
        
