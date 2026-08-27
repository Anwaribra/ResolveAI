import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class RetrievedChunk:
    chunk_id: str
    document_title: str
    content: str
    similarity_score: float


class PGVectorRetriever:
    """Retriever searching knowledge base chunks via pgvector cosine similarity."""

    def __init__(self, db_connection_url: str | None = None):
        self.db_connection_url = db_connection_url

    async def retrieve(self, query: str, top_k: int = 3) -> list[RetrievedChunk]:
        logger.info("Executing pgvector retrieval for query: %s (top_k=%d)", query[:40], top_k)
        # Stub return for MVP; will query pgvector table when populated
        return [
            RetrievedChunk(
                chunk_id="stub-chunk-001",
                document_title="account_locked.md",
                content="If an account is locked after 5 failed login attempts, users can reset their password via email link.",
                similarity_score=0.92,
            )
        ]

    def calculate_retrieval_quality(self, chunks: list[RetrievedChunk]) -> float:
        if not chunks:
            return 0.0
        return sum(c.similarity_score for c in chunks) / len(chunks)
