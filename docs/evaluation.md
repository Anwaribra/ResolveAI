# Evaluation Framework & Metrics — ResolveAI

Evaluation in ResolveAI measures model accuracy, retrieval quality, answer groundedness, and business safety.

---

## 1. Safety & Operational Metrics

### False Auto-Resolution Rate (Primary Safety Metric)
Calculates the proportion of auto-resolved tickets that were resolved incorrectly (e.g., ticket reopened within 48 hours or customer requested agent escalation post-auto-resolution).

$$\text{False Auto-Resolution Rate} = \frac{\text{False Auto-Resolutions}}{\text{Total Auto-Resolved Tickets}}$$

- **Target Threshold**: $< 2.0\%$

### Escalation Rate
$$\text{Escalation Rate} = \frac{\text{Escalated Tickets}}{\text{Total Ingested Tickets}}$$

---

## 2. AI & RAG Metrics

1. **Classification Accuracy**:
   - Intent Accuracy (% matching target intent)
   - Category Accuracy (% matching ground truth category)
   - Priority Precision/Recall
2. **Retrieval Performance**:
   - Context Precision (% of retrieved chunks that are relevant)
   - Context Recall (% of ground truth chunks retrieved)
3. **Response Quality**:
   - Groundedness (Ragas/DeepEval metric evaluating claim verification against retrieved context)
   - Answer Relevance (Cosine similarity between query embedding and answer embedding)
