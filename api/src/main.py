import uuid
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .schemas import AIPredictionResponse, TicketCreateRequest, TicketProcessResponse
from agent.src.decision.engine import DecisionEngine, DecisionInput
from agent.src.llm.gemini import GeminiProvider
from agent.src.classification.classifier import TicketClassifier
from agent.src.retrieval.retriever import PGVectorRetriever
from agent.src.generation.generator import GroundedResponseGenerator

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="ResolveAI — Support Ticket Triage & Auto-Resolution Agent REST API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

decision_engine = DecisionEngine()
llm_provider = GeminiProvider(api_key=settings.gemini_api_key)
classifier = TicketClassifier(provider=llm_provider)
retriever = PGVectorRetriever()
generator = GroundedResponseGenerator(provider=llm_provider)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment,
        "llm_provider": settings.primary_llm_provider,
    }


@app.post("/api/v1/tickets", response_model=TicketProcessResponse, status_code=status.HTTP_201_CREATED)
async def process_ticket(payload: TicketCreateRequest):
    ticket_id = str(uuid.uuid4())

    # 1. Classification
    cls_output = await classifier.classify(payload.subject, payload.body)

    # 2. Retrieval
    retrieved_chunks = await retriever.retrieve(f"{payload.subject} {payload.body}")
    retrieval_quality = retriever.calculate_retrieval_quality(retrieved_chunks)

    # 3. Generation
    generated_response = await generator.generate(payload.subject, payload.body, retrieved_chunks)

    # 4. Decision Engine Governance
    dec_input = DecisionInput(
        confidence_score=cls_output.confidence_score,
        retrieval_quality=retrieval_quality,
        category=cls_output.category,
        priority=cls_output.priority,
        customer_tier=payload.customer_tier,
        has_relevant_knowledge=len(retrieved_chunks) > 0,
    )
    dec_result = decision_engine.evaluate(dec_input)

    final_status = "AUTO_RESOLVED" if dec_result.decision == "AUTO_RESOLVE" else "ESCALATED"

    prediction = AIPredictionResponse(
        predicted_category=cls_output.category,
        predicted_intent=cls_output.intent,
        predicted_priority=cls_output.priority,
        confidence_score=cls_output.confidence_score,
        retrieval_quality=retrieval_quality,
        generated_response=generated_response,
        decision=dec_result.decision.value,
        risk_level=dec_result.risk_level.value,
        reason=dec_result.reason,
    )

    return TicketProcessResponse(
        ticket_id=ticket_id,
        status=final_status,
        customer_email=payload.customer_email,
        subject=payload.subject,
        prediction=prediction,
        created_at=datetime.now(timezone.utc),
    )
