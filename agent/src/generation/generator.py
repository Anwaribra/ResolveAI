import logging
from ..llm.base import LLMProvider
from ..prompts.templates import GROUNDED_RAG_SYSTEM_PROMPT
from ..retrieval.retriever import RetrievedChunk

logger = logging.getLogger(__name__)


class GroundedResponseGenerator:
    """Generates RAG response grounded strictly in retrieved context."""

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def generate(self, ticket_subject: str, ticket_body: str, chunks: list[RetrievedChunk]) -> str:
        context_str = "\n---\n".join(
            [f"Doc: {c.document_title}\nContent: {c.content}" for c in chunks]
        ) if chunks else "No relevant knowledge context found."

        system_instruction = GROUNDED_RAG_SYSTEM_PROMPT.format(context=context_str)
        user_prompt = f"Customer Query:\nSubject: {ticket_subject}\nMessage: {ticket_body}"

        logger.info("Generating grounded response using LLM provider")
        response = await self.provider.generate_text(
            prompt=user_prompt,
            system_instruction=system_instruction,
        )
        return response
