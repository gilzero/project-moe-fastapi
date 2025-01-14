# llm_factory.py
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_xai import ChatXAI
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any, Callable
import logging
from config_loader import LLMConfig
import os
from constants import ModelNames

class LLMFactory:
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.model_map = {
            ModelNames.OPENAI: self._create_openai_model,
            ModelNames.ANTHROPIC: self._create_anthropic_model,
            ModelNames.XAI: self._create_xai_model,
            ModelNames.GOOGLE: self._create_google_model,
        }

    def create_model(self, model_name: ModelNames, model_config: LLMConfig) -> Any:
        creator = self.model_map.get(model_name)
        if not creator:
            logging.error(f"Invalid model name: {model_name}")
            raise ValueError(f"Invalid model name: {model_name}")
        return creator(model_config)

    def _create_openai_model(self, model_config: LLMConfig) -> ChatOpenAI:
        """Creates an OpenAI model instance."""
        return ChatOpenAI(
            model=model_config.model,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
            api_key=self.api_keys.get("OPENAI_API_KEY"),
        )

    def _create_anthropic_model(self, model_config: LLMConfig) -> ChatAnthropic:
        """Creates an Anthropic model instance."""
        return ChatAnthropic(
            model=model_config.model,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
            api_key=self.api_keys.get("ANTHROPIC_API_KEY"),
        )

    def _create_xai_model(self, model_config: LLMConfig) -> ChatXAI:
        """Creates an xAI model instance."""
        return ChatXAI(
            model=model_config.model,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
            api_key=self.api_keys.get("XAI_API_KEY"),
        )

    def _create_google_model(self, model_config: LLMConfig) -> ChatGoogleGenerativeAI:
        """Creates a Google model instance."""
        return ChatGoogleGenerativeAI(
            model=model_config.model,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
            api_key=self.api_keys.get("GOOGLE_API_KEY"),
        )