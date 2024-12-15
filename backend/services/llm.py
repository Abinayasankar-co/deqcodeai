from groq import Groq
import os
from dotenv import load_dotenv


load_dotenv()

class QuantmLLM:
    def  __init__(self):
        self.quantum = Groq(api_key="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")
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
        


#Example Code
quantum_verifier = QuantmLLM()
resposnes = quantum_verifier.llm_request()
print(resposnes)
