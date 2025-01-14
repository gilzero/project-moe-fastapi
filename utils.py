# utils.py
import os
from dotenv import load_dotenv
from typing import Dict, Any, List, Tuple
import logging
import asyncio
from config_loader import load_config, Config
from llm_factory import LLMFactory
from expert import ExpertFactory, Expert
from models import WorkflowResults
from fastapi import HTTPException
import markdown
from constants import ModelNames
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configure logging


# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Generate log file name with timestamp
log_filename = f"logs/logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(log_filename), logging.StreamHandler()])

class APIKeyManager:
    """Manages API keys."""

    def __init__(self):
        """Initializes the APIKeyManager and loads API keys."""
        self.api_keys = {}
        self._load_api_keys()

    def _load_api_keys(self):
        """Loads API keys from environment variables or Google Colab userdata."""
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
        xai_api_key = os.environ.get("XAI_API_KEY")
        google_api_key = os.environ.get("GOOGLE_API_KEY")

        try:
            from google.colab import userdata
            if not openai_api_key:
                openai_api_key = userdata.get("OPENAI_API_KEY")
            if not anthropic_api_key:
                anthropic_api_key = userdata.get("ANTHROPIC_API_KEY")
            if not xai_api_key:
                xai_api_key = userdata.get("XAI_API_KEY")
            if not google_api_key:
                google_api_key = userdata.get("GOOGLE_API_KEY")
        except ImportError:
            logging.warning("google.colab module not found. Using environment variables for API keys.")

        self.api_keys = {
            "OPENAI_API_KEY": openai_api_key,
            "ANTHROPIC_API_KEY": anthropic_api_key,
            "XAI_API_KEY": xai_api_key,
            "GOOGLE_API_KEY": google_api_key,
        }

    def get_api_keys(self) -> Dict[str, str]:
        """Returns the API keys."""
        return self.api_keys

class WorkflowManager:
    """Manages the workflow."""

    def __init__(self):
        """Initializes the WorkflowManager and loads configuration."""
        try:
            self.config: Config = load_config()
        except Exception as e:
            logging.error(f"Failed to load configuration: {e}")
            raise HTTPException(status_code=500, detail="Failed to load configuration")

        self.api_key_manager = APIKeyManager()
        self.llm_factory = LLMFactory(self.api_key_manager.get_api_keys())
        self.expert_factory = ExpertFactory(self.config, self.llm_factory)
        self.experts: Dict[str, Expert] = self.expert_factory.create_experts()

    async def invoke_llm(self, model: Any, role: str, content: str, task: str) -> str:
        """
        Invokes an LLM with a system prompt.

        Args:
            model (Any): The LLM model to invoke.
            role (str): The role of the LLM.
            content (str): The content to be processed by the LLM.
            task (str): The task to be performed by the LLM.

        Returns:
            str: The response from the LLM.
        """
        logging.info(f"🚀 Invoking LLM as {role} to {task}")
        prompt: List[Tuple[str, str]] = [
            ("system", getattr(self.config.prompts, f"{role}_system", f"You are a supervisor {role}. {task}")),
            ("user", content)
        ]
        try:
            response = await model.ainvoke(prompt)
            return response.content
        except Exception as e:
            logging.error(f"❌ Error invoking LLM: {e}")
            raise HTTPException(status_code=500, detail=f"Error invoking LLM for {task}: {e}")

    async def get_expert_responses(self, query: str) -> Dict[str, str]:
        """
        Gathers responses from different expert LLMs asynchronously.

        Args:
            query (str): The user query to be analyzed by the experts.

        Returns:
            Dict[str, str]: The responses from the expert LLMs.
        """
        logging.info("🤖 Gathering insights from our AI experts...")
        tasks = [
            self.experts["openai_expert"].invoke(query),
            self.experts["anthropic_expert"].invoke(query),
            self.experts["xai_expert"].invoke(query)
        ]
        responses = await asyncio.gather(*tasks)
        return {
            "OpenAI": responses[0],
            "Anthropic": responses[1],
            "xAI": responses[2]
        }

    async def analyze_responses(self, responses: Dict[str, str], analysis_type: str) -> str:
        """
        Analyzes the responses using a specific analysis type asynchronously.

        Args:
            responses (Dict[str, str]): The responses from the expert LLMs.
            analysis_type (str): The type of analysis to be performed.

        Returns:
            str: The result of the analysis.
        """
        logging.info(f"🕵️‍♂️ Performing {analysis_type} analysis...")
        task = getattr(self.config.prompts, f"{analysis_type}_task", f"✨ Perform {analysis_type} analysis.")
        content = "\n".join([f"💡 {name}: {resp}" for name, resp in responses.items()]) if analysis_type == "consensus" else f"📝 Content:\n\n{responses}"
        role = f"🔍 analyzing {analysis_type}"
        supervisor_model = self.llm_factory.create_model(ModelNames.GOOGLE, self.config.supervisor_config)
        return await self.invoke_llm(supervisor_model, role, content, task)

    async def run_full_workflow(self, query: str) -> WorkflowResults:
        """
        Runs the full analysis workflow asynchronously.

        Args:
            query (str): The user query to be analyzed.

        Returns:
            WorkflowResults: The results of the full workflow analysis.
        """
        logging.info("🚀 Initiating the full analysis workflow...")
        responses = await self.get_expert_responses(query)
        combined_responses = "\n".join([f"{name}:\n{resp}" for name, resp in responses.items()])

        results = WorkflowResults(
            OpenAI=responses.get("OpenAI", ""),
            Anthropic=responses.get("Anthropic", ""),
            xAI=responses.get("xAI", ""),
            Consensus_Analysis=await self.analyze_responses(responses, "consensus"),
            Charts_Mindmaps=await self.analyze_responses(combined_responses, "charts"),
            Analysis_Tools=await self.analyze_responses(combined_responses, "tools"),
            Related_Questions=await self.analyze_responses(combined_responses, "questions"),
            Meta_Analysis=await self.analyze_responses(combined_responses, "meta")
        )
        return results

    def markdown_to_html(self, text: str) -> str:
        """Converts markdown text to HTML."""
        return markdown.markdown(text)

# Create a single instance of WorkflowManager
workflow_manager = WorkflowManager()

async def run_full_workflow(query: str) -> WorkflowResults:
    """
    Entry point to run the full workflow.

    Args:
        query (str): The user query to be analyzed.

    Returns:
        WorkflowResults: The results of the full workflow analysis.
    """
    return await workflow_manager.run_full_workflow(query)