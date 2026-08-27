# Airflow Orchestration — ResolveAI

Airflow DAGs handle scheduled batch ticket ingestion, database transformations via dbt, and offline evaluation runs.

## DAGs
- `ticket_processing_dag`: Scheduled workflow that ingests unprocessed tickets, runs AI predictions, executes dbt transformations, and logs metrics.
