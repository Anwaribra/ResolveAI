# Data Model & Warehouse Architecture — ResolveAI

ResolveAI uses a dual database model:
1. **OLTP Relational Data Model**: PostgreSQL + pgvector for operational workflow, vector similarity search, and ticket state transitions.
2. **Analytical Warehouse Model**: Star-schema dimensional data models generated via `dbt Core`.

---

## 1. OLTP Database Schema (`/warehouse/schema.sql`)

### Entities

#### `customers`
- `customer_id` (UUID, Primary Key)
- `email` (VARCHAR, Unique)
- `name` (VARCHAR)
- `tier` (VARCHAR: `standard`, `premium`, `enterprise`)
- `created_at` (TIMESTAMP)

#### `products`
- `product_id` (UUID, Primary Key)
- `name` (VARCHAR)
- `category` (VARCHAR)
- `created_at` (TIMESTAMP)

#### `tickets`
- `ticket_id` (UUID, Primary Key)
- `customer_id` (UUID, Foreign Key)
- `product_id` (UUID, Foreign Key)
- `subject` (VARCHAR)
- `status` (VARCHAR: `NEW`, `CLASSIFIED`, `RETRIEVED`, `RESPONSE_GENERATED`, `DECISION_PENDING`, `AUTO_RESOLVED`, `ESCALATED`, `HUMAN_RESOLVED`)
- `priority` (VARCHAR: `low`, `medium`, `high`, `urgent`)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

#### `ticket_messages`
- `message_id` (UUID, Primary Key)
- `ticket_id` (UUID, Foreign Key)
- `sender_type` (VARCHAR: `customer`, `agent`, `ai`)
- `body` (TEXT)
- `created_at` (TIMESTAMP)

#### `ticket_events`
- `event_id` (UUID, Primary Key)
- `ticket_id` (UUID, Foreign Key)
- `event_type` (VARCHAR: `status_changed`, `ai_prediction_created`, `escalated`, `resolved`)
- `payload` (JSONB)
- `created_at` (TIMESTAMP)

#### `ai_predictions`
- `prediction_id` (UUID, Primary Key)
- `ticket_id` (UUID, Foreign Key)
- `predicted_category` (VARCHAR)
- `predicted_intent` (VARCHAR)
- `predicted_priority` (VARCHAR)
- `confidence_score` (NUMERIC)
- `retrieval_quality` (NUMERIC)
- `generated_response` (TEXT)
- `retrieved_chunk_ids` (JSONB)
- `decision` (VARCHAR: `AUTO_RESOLVE`, `ESCALATE`)
- `model_version` (VARCHAR)
- `prompt_version` (VARCHAR)
- `created_at` (TIMESTAMP)

#### `resolutions`
- `resolution_id` (UUID, Primary Key)
- `ticket_id` (UUID, Foreign Key)
- `resolved_by` (VARCHAR: `ai`, `human_agent`)
- `final_category` (VARCHAR)
- `satisfaction_score` (INTEGER, Nullable)
- `resolved_at` (TIMESTAMP)

#### `escalations`
- `escalation_id` (UUID, Primary Key)
- `ticket_id` (UUID, Foreign Key)
- `reason` (VARCHAR)
- `assigned_agent_id` (UUID, Nullable)
- `escalated_at` (TIMESTAMP)

#### `knowledge_documents` & `knowledge_chunks`
- `document_id` (UUID, Primary Key)
- `title` (VARCHAR)
- `file_path` (VARCHAR)
- `chunk_id` (UUID, Primary Key)
- `document_id` (UUID, Foreign Key)
- `content` (TEXT)
- `embedding` (`vector(1536)` or `vector(768)` via pgvector)

---

## 2. Analytical Warehouse Star Schema (`/dbt/models`)

```text
       ┌───────────────┐          ┌───────────────┐
       │ dim_customer  │          │  dim_product  │
       └───────┬───────┘          └───────┬───────┘
               │                          │
               │    ┌────────────────┐    │
               ├───►│  fact_ticket   │◄───┤
               │    └────────┬───────┘    │
               │             │            │
               ▼             ▼            ▼
┌──────────────────┐  ┌───────────────┐  ┌─────────────────┐
│fact_ai_prediction│  │fact_resolution│  │ fact_escalation │
└──────────────────┘  └───────────────┘  └─────────────────┘
```

### Analytical Marts Overview
- `dim_customer`: Customer segmentation, tier, lifecycle history.
- `dim_product`: Product taxonomy and ticket association.
- `dim_category`: Support ticket category metadata and risk weights.
- `fact_ticket`: Aggregated ticket volume, state durations, and resolution channels.
- `fact_ai_prediction`: Prediction accuracy, confidence scores, and decision distribution.
- `fact_resolution`: Time to resolution (TTR), first contact resolution (FCR), and resolution source.
- `fact_escalation`: Escalation reason breakdown and agent routing latency.
