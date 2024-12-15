class QuantumPrompt:
    @staticmethod
    def get_prompt(parameters, gates):
        return f"""Provide a circuit gates for quantum circuit for generating random numbers.
                   The output should only be in the json as mentioning the parameters and the gates.
                   The keys of json are {{
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
                Note : You should only provide the json in the Output no other explanations needed.
                Always ensure that your json output Object format is correct which is of high importance
"""
