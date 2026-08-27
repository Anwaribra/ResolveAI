.PHONY: help init dev docker-up docker-down test lint clean db-seed dbt-run

help:
	@echo "ResolveAI Development Commands:"
	@echo "  make init        - Install project dependencies in editable mode"
	@echo "  make dev         - Run local FastAPI server"
	@echo "  make dashboard   - Run local Streamlit dashboard"
	@echo "  make docker-up   - Start Docker containers (Postgres, API, Dashboard)"
	@echo "  make docker-down - Stop Docker containers"
	@echo "  make test        - Run unit and integration tests"
	@echo "  make lint        - Run ruff linter & code formatting check"
	@echo "  make seed-kb     - Seed knowledge base into pgvector"
	@echo "  make dbt-run     - Run dbt transformation models"

init:
	pip install -e ".[dev,eval]"

dev:
	uvicorn api.src.main:app --reload --port 8000

dashboard:
	streamlit run dashboard/src/app.py

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

test:
	pytest tests/ -v

lint:
	ruff check .

seed-kb:
	python scripts/seed_knowledge.py

dbt-run:
	cd dbt && dbt run --profiles-dir .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
