import os
import logging
from typing import TypeVar
from pydantic import BaseModel
from .base import LLMProvider

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


class GeminiProvider(LLMProvider):
    """Google Gemini LLM implementation using official google-genai SDK."""

    def __init__(self, api_key: str | None = None, model: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        self._client = None

    def _get_client(self):
        if self._client is None:
            if not self.api_key or self.api_key.startswith("your_"):
                logger.warning("No valid Gemini API key configured, using mock mode.")
                return None
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning("Could not initialize google-genai Client (%s), using mock mode.", e)
                return None
        return self._client

    async def generate_text(self, prompt: str, system_instruction: str | None = None) -> str:
        client = self._get_client()
        if client:
            config = {}
            if system_instruction:
                config["system_instruction"] = system_instruction
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config if config else None,
            )
            return response.text
        return f"[Gemini Mock Response for: {prompt[:30]}...]"

    async def generate_structured(
        self, prompt: str, schema: type[T], system_instruction: str | None = None
    ) -> T:
        client = self._get_client()
        if client:
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": schema,
                    **({"system_instruction": system_instruction} if system_instruction else {}),
                },
            )
            return schema.model_validate_json(response.text)
        
        # Fallback dummy for testing when API key isn't present
        dummy_data = {}
        for field_name, field_info in schema.model_fields.items():
            annotation = field_info.annotation
            if annotation is float or annotation == float:
                dummy_data[field_name] = 0.90
            elif annotation is int or annotation == int:
                dummy_data[field_name] = 1
            else:
                dummy_data[field_name] = "account_access" if field_name == "category" else "sample_value"
        return schema.model_construct(**dummy_data)
