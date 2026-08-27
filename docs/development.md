# Development Guide — ResolveAI

Guide for setting up, running, testing, and developing ResolveAI locally.

---

## Environment Setup

### 1. Prerequisites
- Python 3.12+
- Docker & Docker Compose
- Make

### 2. Quickstart
```bash
git clone https://github.com/Anwaribra/ResolveAI.git
cd ResolveAI
cp .env.example .env
make init
make docker-up
```

### 3. Database Initialization
```bash
python scripts/seed_knowledge.py
```

### 4. Running Tests
```bash
make test
```

### 5. Running dbt Transformation Models
```bash
make dbt-run
```

### 6. Linting & Formatting
```bash
make lint
```
