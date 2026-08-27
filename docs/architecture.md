# System Architecture — ResolveAI

ResolveAI is designed as an enterprise joint Data Engineering and AI Engineering platform for support ticket triage, RAG response generation, and automated resolution decisioning.

---

## Complete End-to-End Data & Execution Flow

```text
Customer Email / Ticket
         │
         ▼
┌─────────────────────────┐
│ Ingestion Layer         │ (GmailSource / Webhook API)
└────────┬────────────────┘
         │ Writes raw payload
         ▼
┌─────────────────────────┐
│ OLTP PostgreSQL DB      │ (Tables: tickets, ticket_messages, ticket_events)
└────────┬────────────────┘
         │ Emits event: CLASSIFIED
         ▼
┌─────────────────────────┐
│ AI Classification Engine│ (Category, Intent, Priority)
└────────┬────────────────┘
         │ Emits event: RETRIEVED
         ▼
┌─────────────────────────┐
│ pgvector Retriever      │ (Similarity search over knowledge_chunks)
└────────┬────────────────┘
         │ Emits event: RESPONSE_GENERATED
         ▼
┌─────────────────────────┐
│ Grounded LLM Generator  │ (Gemini / OpenRouter Provider)
└────────┬────────────────┘
         │ Emits event: DECISION_PENDING
         ▼
┌─────────────────────────┐
│ Decision Engine         │ (Evaluates Confidence, Retrieval Quality, Risk)
└────────┬────────┬───────┘
         │        │
  AUTO_RESOLVE  ESCALATE
         │        │
         ▼        ▼
┌─────────────┐ ┌──────────────┐
│ Final State │ │ Human Queue  │
└──────┬──────┘ └──────┬───────┘
       │               │
       └───────┬───────┘
               ▼
┌─────────────────────────┐
│ dbt Analytics Warehouse │ (Star Schema: facts & dimensions)
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Evaluation & Dashboard  │ (Streamlit & Ragas/DeepEval metrics)
└─────────────────────────┘
```

---

## Layer Responsibilities

### 1. Ingestion Layer (`/ingestion`)
- Provides `TicketSource` abstraction.
- Decouples source systems (Gmail API, Zendesk, Webhooks) from downstream processing.
- Persists raw incoming payload to `tickets` and initial `ticket_messages`.

### 2. State Transition & Auditability Layer (`/warehouse`)
- Implements an explicit state machine for ticket lifecycles:
  - `NEW`
  - `CLASSIFIED`
  - `RETRIEVED`
  - `RESPONSE_GENERATED`
  - `DECISION_PENDING`
  - `AUTO_RESOLVED`
  - `ESCALATED`
  - `HUMAN_RESOLVED`
- Every transition appends an immutable event to `ticket_events`.

### 3. AI Agent Layer (`/agent`)
- **LLM Abstraction**: Implements `LLMProvider` base interface with `GeminiProvider` and `OpenRouterProvider`.
- **Classifier**: Multi-task categorization for intent, category, and priority.
- **Retriever**: `pgvector` vector similarity search against embedded policy document chunks.
- **Generator**: Grounded RAG prompt template enforcing zero external hallucinated policy answers.
- **Decision Engine**: Independent governance layer evaluating confidence thresholds and policy risk.

### 4. Data Warehouse Layer (`/dbt`)
- Transforms OLTP transactional entities into analytical dimensional models (`dim_customer`, `dim_product`, `dim_category`, `fact_ticket`, `fact_ai_prediction`, `fact_resolution`, `fact_escalation`).
- Serves as single source of truth for business metrics and false auto-resolution tracking.

### 5. Evaluation Layer (`/evaluation`)
- Evaluates offline golden datasets and live predictions against ground truth.
- Computes False Auto-Resolution Rate, Escalation Rate, Retrieval Relevance, and Groundedness.
