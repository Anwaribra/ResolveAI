# Ingestion Layer — ResolveAI

The ingestion layer provides a pluggable connector model for ingesting customer support tickets into ResolveAI.

## Architecture

`TicketSource` is an abstract base class defining the required contract for ticket source connectors:

- `fetch_new_tickets()` -> Returns standardized list of unprocessed ticket data.
- `acknowledge_ticket(ticket_id)` -> Marks ticket as processed in the source system.

## Connectors

- **`GmailSource`**: Ingests support emails via Google Gmail API OAuth2 connector. (Included for MVP).
- **`FutureZendeskSource`**: Future pluggable connector for Zendesk tickets.
