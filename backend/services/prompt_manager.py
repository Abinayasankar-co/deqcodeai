class QuantumPrompt:
    @staticmethod
    def get_prompt(statement : str)->str:
        json_structured_ouput = """
           {{
                   "Parameters":[{{
                             0:{parameters[0]}
                             1:{parameters[1]}
                             }}
                            ],
                   "gates":[
                             0:{gates[0]}
                             1:{gates[1]}            
                          ],
                   "code":This contains the relevant qiskit code for this
                }}
 
        """
        return f""" Imagine yourself as a Quantum Circuit designer and load more complex quantum circuits at your Cache like shore algorithm and so on.
                    Provide a circuit gates for quantum circuit for generating a solution for the given problem statement {statement}.
                    The output should only be in the json as mentioning the parameters and the gates.
                    The keys of json are shown here as {json_structured_ouput}
                    Refer Algassert gates and formulas for producing the output.
                    Avoid Parser Errors and ensure the json output is correct. 
                    Note : 1. You should only provide the json in the Output no other explanations needed.
                           2. Always ensure that your json output Object format is correct which is of high importance.
                           3. The Opening and closing tags and structure of json should be maintained strictly without any compensation.
                           4. The code should be in the form of qiskit code."""
