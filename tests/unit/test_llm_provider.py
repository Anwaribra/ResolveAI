import pytest
from agent.src.llm.gemini import GeminiProvider
from agent.src.llm.openrouter import OpenRouterProvider


@pytest.mark.asyncio
async def test_gemini_provider_fallback():
    provider = GeminiProvider(api_key=None)
    response = await provider.generate_text("Hello Gemini")
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_openrouter_provider_fallback():
    provider = OpenRouterProvider(api_key=None)
    response = await provider.generate_text("Hello OpenRouter")
    assert isinstance(response, str)
    assert len(response) > 0
