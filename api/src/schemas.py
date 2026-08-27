from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class TicketCreateRequest(BaseModel):
    customer_email: str
    customer_name: str | None = None
    subject: str = Field(..., min_length=3, max_length=500)
    body: str = Field(..., min_length=5)
    customer_tier: str = Field(default="standard")


class AIPredictionResponse(BaseModel):
    predicted_category: str
    predicted_intent: str
    predicted_priority: str
    confidence_score: float
    retrieval_quality: float
    generated_response: str
    decision: str
    risk_level: str
    reason: str


class TicketProcessResponse(BaseModel):
    ticket_id: str
    status: str
    customer_email: str
    subject: str
    prediction: AIPredictionResponse
    created_at: datetime = Field(default_factory=datetime.utcnow)
