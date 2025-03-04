from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from transformers import pipeline
from typing import Dict, Any
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AgenticPipelineWithReward:
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.7, reward_threshold: float = 0.7):
        """Initialize the agentic pipeline with reward mechanism"""
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.memory = ConversationBufferMemory()
        self.nodes = self._initialize_nodes()
        self.reward_model = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=0 if torch.cuda.is_available() else -1
        )
        self.reward_threshold = reward_threshold
        self.max_iterations = 3  # Maximum refinement iterations

    def _initialize_nodes(self) -> Dict[str, LLMChain]:
        """Initialize workflow nodes with their respective prompts"""
        nodes = {}
        
        # Node 1: Task Planner
        planner_prompt = PromptTemplate(
            input_variables=["input", "feedback"],
            template="""You are an AI task planner. Given the input: {input}
            {feedback}
            Create a detailed plan with steps to accomplish this task.
            Return the plan as a numbered list."""
        )
        nodes["planner"] = LLMChain(llm=self.llm, prompt=planner_prompt, verbose=True)

        # Node 2: Research Agent
        research_prompt = PromptTemplate(
            input_variables=["plan", "feedback"],
            template="""You are a research agent. Based on this plan: {plan}
            {feedback}
            Gather relevant information and insights for each step.
            Return structured information with sources (simulated)."""
        )
        nodes["research"] = LLMChain(llm=self.llm, prompt=research_prompt, verbose=True)

        # Node 3: Analysis Agent
        analysis_prompt = PromptTemplate(
            input_variables=["research", "feedback"],
            template="""You are an analysis agent. Given this research: {research}
            {feedback}
            Analyze the information and provide actionable insights.
            Return a concise analysis with key findings."""
        )
        nodes["analysis"] = LLMChain(llm=self.llm, prompt=analysis_prompt, verbose=True)

        # Node 4: Output Generator
        output_prompt = PromptTemplate(
            input_variables=["analysis", "feedback"],
            template="""You are an output generator. Based on this analysis: {analysis}
            {feedback}
            Create a professional, well-formatted final output.
            Return the result in markdown format."""
        )
        nodes["output"] = LLMChain(llm=self.llm, prompt=output_prompt, verbose=True)

        return nodes

    def _evaluate_reward(self, text: str) -> float:
        """Evaluate text using the reward model"""
        try:
            result = self.reward_model(text)[0]
            # Convert sentiment score to a 0-1 scale (assuming positive sentiment is desired)
            score = result['score'] if result['label'] == 'POSITIVE' else 1 - result['score']
            return score
        except Exception as e:
            logger.error(f"Reward evaluation failed: {str(e)}")
            return 0.0

    def _generate_feedback(self, text: str, score: float) -> str:
        """Generate feedback for improvement based on reward score"""
        if score < self.reward_threshold:
            return f"Previous output scored {score:.2f} (below threshold {self.reward_threshold}). Please improve clarity, detail, and overall quality."
        return ""

    def execute_pipeline(self, input_task: str) -> Dict[str, str]:
        """Execute the pipeline with reward-based refinement"""
        results = {}
        iteration = 0
        
        while iteration < self.max_iterations:
            feedback = "" if iteration == 0 else self._generate_feedback(
                results.get("output", ""), 
                results.get("last_score", 0.0)
            )
            
            try:
                # Step 1: Planning
                logger.info(f"Iteration {iteration + 1} - Executing planning node...")
                results["plan"] = self.nodes["planner"].run(input=input_task, feedback=feedback)
                
                # Step 2: Research
                logger.info(f"Iteration {iteration + 1} - Executing research node...")
                results["research"] = self.nodes["research"].run(plan=results["plan"], feedback=feedback)
                
                # Step 3: Analysis
                logger.info(f"Iteration {iteration + 1} - Executing analysis node...")
                results["analysis"] = self.nodes["analysis"].run(research=results["research"], feedback=feedback)
                
                # Step 4: Output Generation
                logger.info(f"Iteration {iteration + 1} - Executing output node...")
                results["output"] = self.nodes["output"].run(analysis=results["analysis"], feedback=feedback)
                
                # Evaluate reward
                reward_score = self._evaluate_reward(results["output"])
                results["last_score"] = reward_score
                logger.info(f"Reward score: {reward_score:.2f}")
                
                if reward_score >= self.reward_threshold:
                    logger.info("Output meets quality threshold")
                    break
                    
                iteration += 1
                logger.info("Output below threshold, initiating refinement...")
                
            except Exception as e:
                logger.error(f"Pipeline execution failed: {str(e)}")
                raise
                
        if iteration == self.max_iterations:
            logger.warning("Maximum iterations reached without meeting threshold")
            
        return results

    def get_pipeline_state(self) -> Dict[str, Any]:
        """Return current state of the pipeline"""
        return {
            "memory": self.memory.buffer,
            "model_config": {
                "model_name": self.llm.model_name,
                "temperature": self.llm.temperature,
                "reward_threshold": self.reward_threshold
            }
        }

# Example usage
def main():
    # Initialize pipeline
    pipeline = AgenticPipelineWithReward(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        reward_threshold=0.7
    )
    
    # Example task
    task = "Create a marketing strategy for a new tech gadget"
    
    try:
        # Execute pipeline
        results = pipeline.execute_pipeline(task)
        
        # Print results
        print("\n=== Pipeline Results ===")
        print("\nFinal Plan:")
        print(results["plan"])
        print("\nFinal Research:")
        print(results["research"])
        print("\nFinal Analysis:")
        print(results["analysis"])
        print("\nFinal Output:")
        print(results["output"])
        print(f"\nFinal Reward Score: {results['last_score']:.2f}")
        
        # Print pipeline state
        print("\n=== Pipeline State ===")
        state = pipeline.get_pipeline_state()
        print(f"Memory buffer: {state['memory']}")
        print(f"Model config: {state['model_config']}")
        
    except Exception as e:
        logger.error(f"Error in pipeline execution: {str(e)}")

if __name__ == "__main__":
    # Requirements: pip install langchain openai transformers torch python-dotenv
    import torch  # Imported here for cuda check
    main()