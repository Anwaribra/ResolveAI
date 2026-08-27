import logging
from pydantic import BaseModel, Field
from ..llm.base import LLMProvider
from ..prompts.templates import CLASSIFICATION_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class ClassificationOutput(BaseModel):
    category: str = Field(description="Predicted category")
    intent: str = Field(description="Predicted intent")
    priority: str = Field(description="Predicted priority")
    confidence_score: float = Field(description="Confidence score between 0 and 1")


class TicketClassifier:
    """Classifier evaluating ticket category, intent, and priority."""

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def classify(self, subject: str, body: str) -> ClassificationOutput:
        prompt = f"Ticket Subject: {subject}\nTicket Body: {body}"
        logger.info("Classifying ticket with subject: %s", subject)
        try:
            result = await self.provider.generate_structured(
                prompt=prompt,
                schema=ClassificationOutput,
                system_instruction=CLASSIFICATION_SYSTEM_PROMPT,
            )
            return result
        except Exception as e:
            logger.error("Classification failed: %s. Using safe fallback.", e)
            return ClassificationOutput(
                category="general_inquiry",
                intent="unknown",
                priority="medium",
                confidence_score=0.5,
            )
