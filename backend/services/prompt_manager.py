from services.supportivegates import ElementsRequired

class QuantumPrompt:
    def get_prompt(statement : str)->str:
        supportive_gates = ElementsRequired()
        supported_gates = supportive_gates.supportive_gates()
        example_prompt , json_structured_ouput = supportive_gates.sample_prompt()
        return f""" Imagine yourself as a Quantum Circuit designer and load more complex quantum circuits at your Cache like shore algorithm and so on.
                    Yourself should design a Quantum circuit which is more optimized and can yield more accurate result.
                    A Statement is given as {statement}, Infere the whole statement and divide them into chunks of statements.
                    Think how to approach them in quantum and then solve the below instruction. 
                    You must Generate circuits w.r.t these gates {supported_gates} and provide the explanation for the circuit along with the code in the required format.
                    Think Smart before generating the gates and check for the different approaches with all the available gates and think about various possibilites of those parameteral gates.
                    Note: The circuit with minimal gates of more optimized approach is of more importance.
                    The output should only be in the json as mentioning the parameters and the gates.
                    The keys of json are shown here as {json_structured_ouput}.
                    Example of output generation is provided as {example_prompt}.
                    Refer Algassert gates and formulas for producing the output.Kindly verify the format and then generate the json always.
                    Avoid Parser Errors and ensure that returned json output is correct. 
                    Note : 1. You should only provide the json in the Output no other explanations needed.
                           2.Provide consistency in generating the json output Object format.
                           3. Provide the code which is relevant to the json generated."""
