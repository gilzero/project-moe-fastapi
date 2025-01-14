# expert.py
from typing import Callable, Any, Dict
import logging
from llm_factory import LLMFactory
from config_loader import Config
from constants import ModelNames

class Expert:
    """Represents an expert LLM with a specific style."""

    def __init__(self, model: Any, style: str):
        self.model = model
        self.style = style
        self.style_prompt = f"You are an expert with style: {style}."

    async def invoke(self, query: str) -> str:
        """Invokes the expert LLM with a given query."""
        try:
            response = await self.model.ainvoke([("system", self.style_prompt), ("user", query)])
            return response.content
        except Exception as e:
            logging.error(f"Error invoking expert: {e}")
            return f"Error: Could not invoke expert"

class ExpertFactory:
    def __init__(self, config: Config, llm_factory: LLMFactory):
        self.config = config
        self.llm_factory = llm_factory

    def create_expert(self, model_name: ModelNames, style: str) -> Expert:
        # Notice we use model_name.value here
        model_config = getattr(self.config, f"{model_name.value}_config")
        model = self.llm_factory.create_model(model_name, model_config)
        if not model:
            raise ValueError(f"Could not create model for expert {model_name}")
        return Expert(model, style)

    def create_experts(self) -> Dict[str, Expert]:
        experts = {}
        # Notice we pass the enum itself, not the raw string
        experts["openai_expert"] = self.create_expert(ModelNames.OPENAI, self.config.expert_styles.technical)
        experts["anthropic_expert"] = self.create_expert(ModelNames.ANTHROPIC, self.config.expert_styles.creative)
        experts["xai_expert"] = self.create_expert(ModelNames.XAI, self.config.expert_styles.business)
        return experts