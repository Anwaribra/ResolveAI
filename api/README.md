# REST API Backend — ResolveAI

FastAPI application providing endpoints for ticket ingestion, prediction retrieval, and system status checks.

## Endpoints
- `GET /health`: Health check endpoint.
- `POST /api/v1/tickets`: Ingest and process a new support ticket.
- `GET /api/v1/tickets/{ticket_id}`: Retrieve ticket status, audit trail, and AI decision.
