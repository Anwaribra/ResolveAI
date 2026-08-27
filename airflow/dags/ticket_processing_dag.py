"""Airflow DAG for ResolveAI support ticket ingestion and transformation."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "resolveai",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def ingest_tickets():
    print("Ingesting new support tickets from Gmail API source...")


def run_ai_triage():
    print("Executing AI triage, RAG retrieval, and decision engine...")


def run_dbt_models():
    print("Running dbt transformation models...")


with DAG(
    "ticket_processing_dag",
    default_args=default_args,
    description="Scheduled batch ticket processing DAG",
    schedule_interval=timedelta(minutes=15),
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="ingest_tickets",
        python_callable=ingest_tickets,
    )

    t2 = PythonOperator(
        task_id="run_ai_triage",
        python_callable=run_ai_triage,
    )

    t3 = PythonOperator(
        task_id="run_dbt_models",
        python_callable=run_dbt_models,
    )

    t1 >> t2 >> t3
