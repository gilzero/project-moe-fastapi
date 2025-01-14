# config_loader.py
import yaml
import logging
from pydantic import BaseModel, field_validator
from typing import Dict, Any

class LLMConfig(BaseModel):
    model: str
    temperature: float = 0.0
    max_tokens: int = 512

class ExpertStyles(BaseModel):
    technical: str
    creative: str
    business: str

class PromptsConfig(BaseModel):
    consensus_task: str
    charts_task: str
    tools_task: str
    questions_task: str
    meta_task: str

class Config(BaseModel):
    openai_model: str
    anthropic_model: str
    xai_model: str
    supervisor_model: str
    openai_config: LLMConfig
    anthropic_config: LLMConfig
    xai_config: LLMConfig
    supervisor_config: LLMConfig
    expert_styles: ExpertStyles
    prompts: PromptsConfig

    @field_validator('*')
    def check_none(cls, value):
        if value is None:
            raise ValueError("Configuration value cannot be None")
        return value

def load_config(config_path: str = "config.yaml") -> Config:
    """Loads and validates the configuration from a YAML file."""
    try:
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)
        config = Config(**config_data)
        return config
    except FileNotFoundError:
        logging.error(f"Error: config.yaml not found at {config_path}. Please create a config.yaml file.")
        raise
    except yaml.YAMLError as e:
        logging.error(f"Error parsing config.yaml: {e}")
        raise
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        raise