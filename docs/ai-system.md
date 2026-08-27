# AI System Architecture & Decision Engine — ResolveAI

The AI layer in ResolveAI automates ticket classification, policy knowledge retrieval, response generation, and automated resolution decisioning while remaining modular and provider-independent.

---

## 1. Provider Abstraction Architecture

To avoid vendor lock-in, ResolveAI uses an abstract `LLMProvider` interface:

```python
class LLMProvider(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str, system_instruction: str | None = None) -> str:
        ...

    @abstractmethod
    async def generate_structured(self, prompt: str, schema: type[BaseModel]) -> BaseModel:
        ...
```

- **Gemini Provider (`GeminiProvider`)**: Uses `google-genai` SDK with `gemini-2.5-flash`.
- **OpenRouter Provider (`OpenRouterProvider`)**: Uses REST HTTP client for OpenAI-compatible OpenRouter endpoints as fallback.

---

## 2. RAG Pipeline (Knowledge Retrieval)

1. **Document Ingestion**: Markdown documents in `knowledge_base/documents/` are chunked into 500-token sections with 50-token overlap.
2. **Embedding & Vector Storage**: Chunks are stored in PostgreSQL using `pgvector`.
3. **Similarity Search**: Queries retrieve top-$k$ ($k=3$) relevant chunks using cosine similarity (`<=>` operator).
4. **Grounded Prompting**: The LLM prompt combines retrieved chunks as explicit context:
   ```text
   You are ResolveAI Support Assistant.
   Answer the customer query ONLY using the provided Knowledge Base context.
   If the answer cannot be determined from the context, state that human support is required.
   ```

---

## 3. Decision & Risk Engine (`/agent/src/decision/engine.py`)

The Decision Engine acts as a strict governance barrier between AI output and auto-resolution:

```python
@dataclass
class DecisionInput:
    confidence_score: float
    retrieval_quality: float
    category: str
    priority: str
    customer_tier: str
    historical_category_success_rate: float

class DecisionEngine:
    def evaluate(self, input_data: DecisionInput) -> DecisionResult:
        ...
```

### Governance Rules:
- **Auto-Resolve Conditions**:
  - `confidence_score >= 0.85`
  - `retrieval_quality >= 0.80`
  - `category` is NOT in high-risk categories (e.g., `account_deletion`, `legal_threat`, `security_breach`).
  - `priority` != `urgent`.
- If any condition fails, the engine outputs `ESCALATE`.
