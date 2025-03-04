from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from typing import Dict, Any, List
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AgenticPipeline:
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.7):
        """Initialize the agentic pipeline with configuration"""
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.memory = ConversationBufferMemory()
        self.nodes = self._initialize_nodes()
        
    def _initialize_nodes(self) -> Dict[str, LLMChain]:
        """Initialize workflow nodes with their respective prompts"""
        nodes = {}
        
        # Node 1: Task Planner
        planner_prompt = PromptTemplate(
            input_variables=["input"],
            template="""You are an AI task planner. Given the input: {input}
            Create a detailed plan with steps to accomplish this task.
            Return the plan as a numbered list."""
        )
        nodes["planner"] = LLMChain(llm=self.llm, prompt=planner_prompt, verbose=True)

        # Node 2: Research Agent
        research_prompt = PromptTemplate(
            input_variables=["plan"],
            template="""You are a research agent. Based on this plan: {plan}
            Gather relevant information and insights for each step.
            Return structured information with sources (simulated)."""
        )
        nodes["research"] = LLMChain(llm=self.llm, prompt=research_prompt, verbose=True)

        # Node 3: Analysis Agent
        analysis_prompt = PromptTemplate(
            input_variables=["research"],
            template="""You are an analysis agent. Given this research: {research}
            Analyze the information and provide actionable insights.
            Return a concise analysis with key findings."""
        )
        nodes["analysis"] = LLMChain(llm=self.llm, prompt=analysis_prompt, verbose=True)

        # Node 4: Output Generator
        output_prompt = PromptTemplate(
            input_variables=["analysis"],
            template="""You are an output generator. Based on this analysis: {analysis}
            Create a professional, well-formatted final output.
            Return the result in markdown format."""
        )
        nodes["output"] = LLMChain(llm=self.llm, prompt=output_prompt, verbose=True)

        return nodes

    def execute_pipeline(self, input_task: str) -> Dict[str, str]:
        """Execute the complete pipeline with error handling"""
        results = {}
        
        try:
            # Step 1: Planning
            logger.info("Executing planning node...")
            results["plan"] = self.nodes["planner"].run(input=input_task)
            self.memory.save_context({"input": input_task}, {"output": results["plan"]})
            
            # Step 2: Research
            logger.info("Executing research node...")
            results["research"] = self.nodes["research"].run(plan=results["plan"])
            
            # Step 3: Analysis
            logger.info("Executing analysis node...")
            results["analysis"] = self.nodes["analysis"].run(research=results["research"])
            
            # Step 4: Output Generation
            logger.info("Executing output node...")
            results["output"] = self.nodes["output"].run(analysis=results["analysis"])
            
            return results
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}")
            raise

    def get_pipeline_state(self) -> Dict[str, Any]:
        """Return current state of the pipeline"""
        return {
            "memory": self.memory.buffer,
            "model_config": {
                "model_name": self.llm.model_name,
                "temperature": self.llm.temperature
            }
        }

# Example usage
def main():
    # Initialize pipeline
    pipeline = AgenticPipeline(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Example task
    task = "Create a marketing strategy for a new tech gadget"
    
    try:
        # Execute pipeline
        results = pipeline.execute_pipeline(task)
        
        # Print results
        print("\n=== Pipeline Results ===")
        print("\nPlan:")
        print(results["plan"])
        print("\nResearch:")
        print(results["research"])
        print("\nAnalysis:")
        print(results["analysis"])
        print("\nFinal Output:")
        print(results["output"])
        
        # Print pipeline state
        print("\n=== Pipeline State ===")
        state = pipeline.get_pipeline_state()
        print(f"Memory buffer: {state['memory']}")
        print(f"Model config: {state['model_config']}")
        
    except Exception as e:
        logger.error(f"Error in pipeline execution: {str(e)}")

if __name__ == "__main__":
    # Make sure to set your OpenAI API key in .env file
    # OPENAI_API_KEY=your-api-key-here
    main()