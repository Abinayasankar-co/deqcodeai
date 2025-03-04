# Robust AI agentic pipeline with reward model and user recommendation using Grok Llama70b

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from transformers import pipeline
from typing import Dict, Any
import os
from dotenv import load_dotenv
import logging
import torch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class AgenticPipelineWithReward:
    def __init__(self, model_name: str = "llama-70b", temperature: float = 0.7, reward_threshold: float = 0.7):
        self.llm = ChatGroq(
            model_name=model_name,
            temperature=temperature,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.memory = ConversationBufferMemory()
        self.nodes = self._initialize_nodes()
        self.reward_model = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=0 if torch.cuda.is_available() else -1
        )
        self.reward_threshold = reward_threshold
        self.max_iterations = 3

    def _initialize_nodes(self) -> Dict[str, LLMChain]:
        nodes = {}
        
        planner_prompt = PromptTemplate(
            input_variables=["input", "feedback"],
            template="""You are an AI task planner. Given the input: {input}
            {feedback}
            Create a detailed plan with steps to accomplish this task.
            Return the plan as a numbered list."""
        )
        nodes["planner"] = LLMChain(llm=self.llm, prompt=planner_prompt, verbose=True)

        research_prompt = PromptTemplate(
            input_variables=["plan", "feedback"],
            template="""You are a research agent. Based on this plan: {plan}
            {feedback}
            Gather relevant information and insights for each step.
            Return structured information with sources (simulated)."""
        )
        nodes["research"] = LLMChain(llm=self.llm, prompt=research_prompt, verbose=True)

        analysis_prompt = PromptTemplate(
            input_variables=["research", "feedback"],
            template="""You are an analysis agent. Given this research: {research}
            {feedback}
            Analyze the information and provide actionable insights.
            Return a concise analysis with key findings."""
        )
        nodes["analysis"] = LLMChain(llm=self.llm, prompt=analysis_prompt, verbose=True)

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
        result = self.reward_model(text)[0]
        score = result['score'] if result['label'] == 'POSITIVE' else 1 - result['score']
        return score

    def _generate_feedback(self, text: str, score: float) -> str:
        if score < self.reward_threshold:
            return f"Previous output scored {score:.2f} (below threshold {self.reward_threshold}). Please improve clarity, detail, and overall quality."
        return ""

    def _get_user_approval(self, results: Dict[str, str]) -> bool:
        print("\n=== Generated Output ===")
        print(results["output"])
        print(f"\nReward Score: {results['last_score']:.2f}")
        response = input("Is this output acceptable? (yes/no): ").lower().strip()
        return response == "yes"

    def execute_pipeline(self, input_task: str) -> Dict[str, str]:
        results = {}
        iteration = 0
        
        while iteration < self.max_iterations:
            feedback = "" if iteration == 0 else self._generate_feedback(
                results.get("output", ""), 
                results.get("last_score", 0.0)
            )
            
            results["plan"] = self.nodes["planner"].run(input=input_task, feedback=feedback)
            results["research"] = self.nodes["research"].run(plan=results["plan"], feedback=feedback)
            results["analysis"] = self.nodes["analysis"].run(research=results["research"], feedback=feedback)
            results["output"] = self.nodes["output"].run(analysis=results["analysis"], feedback=feedback)
            
            reward_score = self._evaluate_reward(results["output"])
            results["last_score"] = reward_score
            
            if reward_score >= self.reward_threshold:
                if self._get_user_approval(results):
                    logger.info("User approved the output. Proceeding with execution plan.")
                    break
                else:
                    logger.info("User rejected the output. Refining...")
                    feedback = "User feedback: Output rejected. Please enhance the quality and relevance."
            
            iteration += 1
        
        if iteration == self.max_iterations:
            logger.warning("Maximum iterations reached without user approval")
        
        return results

    def get_pipeline_state(self) -> Dict[str, Any]:
        return {
            "memory": self.memory.buffer,
            "model_config": {
                "model_name": self.llm.model_name,
                "temperature": self.llm.temperature,
                "reward_threshold": self.reward_threshold
            }
        }

def main():
    pipeline = AgenticPipelineWithReward(
        model_name="llama-70b",
        temperature=0.7,
        reward_threshold=0.7
    )
    
    task = "Create a marketing strategy for a new tech gadget"
    
    results = pipeline.execute_pipeline(task)
    
    print("\n=== Final Pipeline Results ===")
    print("\nFinal Plan:")
    print(results["plan"])
    print("\nFinal Research:")
    print(results["research"])
    print("\nFinal Analysis:")
    print(results["analysis"])
    print("\nFinal Output:")
    print(results["output"])
    print(f"\nFinal Reward Score: {results['last_score']:.2f}")
    
    print("\n=== Pipeline State ===")
    state = pipeline.get_pipeline_state()
    print(f"Memory buffer: {state['memory']}")
    print(f"Model config: {state['model_config']}")

if __name__ == "__main__":
    main()