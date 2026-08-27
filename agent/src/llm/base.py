from abc import ABC, abstractmethod
from typing import TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMProvider(ABC):
    """Abstract interface for LLM provider adapters (Gemini, OpenRouter)."""

    @abstractmethod
    async def generate_text(self, prompt: str, system_instruction: str | None = None) -> str:
        """Generate unstructured text response from prompt."""
        pass

    @abstractmethod
    async def generate_structured(
        self, prompt: str, schema: type[T], system_instruction: str | None = None
    ) -> T:
        """Generate structured response validated against Pydantic schema."""
        pass
