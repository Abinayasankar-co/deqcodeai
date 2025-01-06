from services.supportivegates import ElementsRequired

class QuantumPrompt:
    def get_prompt(statement : str)->str:
        supportive_gates = ElementsRequired()
        supported_gates = supportive_gates.supportive_gates()
        example_prompt , json_structured_ouput = supportive_gates.sample_prompt()
        return f""" Imagine yourself as a Quantum Circuit designer and load more complex quantum circuits at your Cache like shore algorithm and so on.
                    You must Generate circuits w.r.t these gates {supported_gates} and provide only the explanation for the circuit.
                    Provide a circuit gates for quantum circuit for generating a solution for the given problem statement {statement}.
                    Think Smart before generating the gates and check for the easiest , smallest and shortest way of generating the circuit with minimal gates.
                    Note: The circuit with minimal gates of more optimized approach is of more importance.
                    The output should only be in the json as mentioning the parameters and the gates.
                    The keys of json are shown here as {json_structured_ouput}.
                    Example of output generation is provided as {example_prompt}.
                    Refer Algassert gates and formulas for producing the output.Kindly verify the format and then generate the json always.
                    Avoid Parser Errors and ensure that returned json output is correct. 
                    Note : 1. You should only provide the json in the Output no other explanations needed.
                           2.Provide consistency in generating the json output Object format."""
