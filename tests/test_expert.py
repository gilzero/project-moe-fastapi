import pytest
from config_loader import load_config
from llm_factory import LLMFactory
from expert import ExpertFactory

@pytest.mark.asyncio
async def test_expert_creation():
    config = load_config("config.yaml")
    llm_factory = LLMFactory({
        "OPENAI_API_KEY": "test_key",
        "ANTHROPIC_API_KEY": "test_key",
        "XAI_API_KEY": "test_key",
        "GOOGLE_API_KEY": "test_key"
    })
    expert_factory = ExpertFactory(config, llm_factory)

    experts = expert_factory.create_experts()

    assert "openai_expert" in experts
    assert "anthropic_expert" in experts
    assert "xai_expert" in experts
    assert experts["openai_expert"].style == config.expert_styles.technical
    assert experts["anthropic_expert"].style == config.expert_styles.creative
    assert experts["xai_expert"].style == config.expert_styles.business
