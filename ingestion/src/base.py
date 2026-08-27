from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field


class TicketPayload(BaseModel):
    source_ticket_id: str
    customer_email: str
    customer_name: str | None = None
    subject: str
    body: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    raw_metadata: dict[str, Any] = Field(default_factory=dict)


class TicketSource(ABC):
    """Abstract base class for all ticket ingestion sources."""

    @abstractmethod
    async def fetch_new_tickets(self, limit: int = 50) -> list[TicketPayload]:
        """Fetch raw unread or unprocessed support tickets from source."""
        pass

    @abstractmethod
    async def acknowledge_ticket(self, source_ticket_id: str) -> bool:
        """Acknowledge ticket ingestion in source system."""
        pass
