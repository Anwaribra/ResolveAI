import os
import logging
from typing import TypeVar
import httpx
from pydantic import BaseModel
from .base import LLMProvider

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


class OpenRouterProvider(LLMProvider):
    """OpenRouter API adapter for multi-model fallback access."""

    def __init__(self, api_key: str | None = None, model: str = "anthropic/claude-3.5-sonnet"):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    async def generate_text(self, prompt: str, system_instruction: str | None = None) -> str:
        if not self.api_key:
            return f"[OpenRouter Mock Response for: {prompt[:30]}...]"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(self.base_url, headers=headers, json=payload, timeout=30.0)
            resp.raise_for_request()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    async def generate_structured(
        self, prompt: str, schema: type[T], system_instruction: str | None = None
    ) -> T:
        text = await self.generate_text(prompt, system_instruction)
        return schema.model_validate_json(text)
