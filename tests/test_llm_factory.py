import pytest
from llm_factory import LLMFactory
from config_loader import LLMConfig
from constants import ModelNames

def test_create_openai_model():
    factory = LLMFactory({"OPENAI_API_KEY": "mock_key"})
    config = LLMConfig(model="gpt-4", temperature=0.5, max_tokens=100)
    model = factory.create_model(ModelNames.OPENAI, config)
    assert model is not None

def test_invalid_model_name():
    factory = LLMFactory({})
    config = LLMConfig(model="invalid-model", temperature=0.5, max_tokens=100)
    with pytest.raises(ValueError):
        factory.create_model("non_existent_model", config)
