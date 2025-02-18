import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

class QuantumApplicationMapper:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))

        # Quantum application areas
        self.quantum_applications = {
            "optimization": ["QAOA", "variational circuits", "qubit efficiency"],
            "cryptography": ["quantum key distribution", "Shor’s algorithm", "Grover’s algorithm"],
            "machine learning": ["quantum neural networks", "data encoding", "quantum kernels"],
            "physics simulation": ["Schrodinger equation", "wave functions", "quantum Monte Carlo"],
            "finance": ["portfolio optimization", "risk analysis", "Monte Carlo simulation"],
            "drug discovery": ["molecular simulation", "quantum chemistry", "variational eigen solver"]
        }

        # Quantum computing dependencies
        self.quantum_dependencies = {
            "QAOA": ["Hadamard", "CNOT", "Phase gates"],
            "Shor’s algorithm": ["Quantum Fourier Transform", "Modular exponentiation"],
            "quantum key distribution": ["Bell states", "Entanglement"],
            "quantum neural networks": ["Variational circuits", "Quantum kernels"],
            "molecular simulation": ["Hamiltonian encoding", "Qubit-to-orbital mapping"]
        }

    def preprocess(self, text):
        """Tokenizes and cleans the input text."""
        text = text.lower()
        text = re.sub(r"\s+", " ", text)  # Remove extra spaces
        text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words]
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        return tokens

    def detect_application(self, tokens):
        """Detects quantum application type based on keywords."""
        application = None
        dependencies = []
        for app, keywords in self.quantum_applications.items():
            if any(token in keywords for token in tokens):
                application = app
                dependencies.extend(keywords)
                break  
        return application, dependencies

    def map_dependencies(self, dependencies):
        """Maps dependencies to relevant quantum computing elements."""
        mapped_elements = []
        for dep in dependencies:
            if dep in self.quantum_dependencies:
                mapped_elements.extend(self.quantum_dependencies[dep])
        
        return list(set(mapped_elements))  # Remove duplicates

    def generate_chain_of_thought_prompt(self, application, dependencies, quantum_elements):
        """Generates a structured prompt for LLM-based QASM/Qiskit generation."""
        cot_prompt = "### Quantum Circuit Design for Application ###\n"
        cot_prompt += f"We need to design a quantum circuit for the application: **{application}**.\n"
        cot_prompt += f"- **Constraints & Requirements**: {', '.join(dependencies) if dependencies else 'Unknown'}\n"
        cot_prompt += f"- **Quantum Elements Needed**: {', '.join(quantum_elements) if quantum_elements else 'Standard Gates'}\n"
        cot_prompt += "\n#### Chain of Thought Reasoning ####\n"
        cot_prompt += "1. **Define Qubits**: Assign qubits based on the problem's requirements.\n"
        cot_prompt += f"2. **Apply Quantum Gates**: Use {', '.join(quantum_elements)} to process the information.\n"
        cot_prompt += "3. **Introduce Interactions**: Implement entanglement and cross-qubit operations.\n"
        cot_prompt += "4. **Measure System State**: Extract the final computation result.\n"
        cot_prompt += "\nGenerate the corresponding QASM or Qiskit code based on this structured reasoning.\n"

        return cot_prompt

# Example Usage
if __name__ == "__main__":
    user_query = "Generate a random number circuit for 2 qubits"

    processor = QuantumApplicationMapper()
    
    # Step 1: Preprocess the query
    tokens = processor.preprocess(user_query)

    # Step 2: Detect application and dependencies
    application, dependencies = processor.detect_application(tokens)

    # Step 3: Map dependencies to quantum computing elements
    quantum_elements = processor.map_dependencies(dependencies)

    # Step 4: Generate structured chain-of-thought prompt
    cot_prompt = processor.generate_chain_of_thought_prompt(application, dependencies, quantum_elements)

    print("Structured Prompt for LLM:\n", cot_prompt)
