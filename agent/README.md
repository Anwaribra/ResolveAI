# AI Agent Layer — ResolveAI

Contains core AI components:
- `llm/`: LLM Provider abstraction (`GeminiProvider` primary, `OpenRouterProvider` fallback).
- `classification/`: Intent, category, and priority multi-task classification.
- `retrieval/`: pgvector document chunk similarity retriever.
- `generation/`: Grounded RAG response generator.
- `decision/`: Independent rule/risk-based decision engine.
- `prompts/`: Versioned prompt templates.
