# Evaluation Layer — ResolveAI

Contains metrics calculation and dataset evaluation harnesses.

## Key Safety Metric
- **False Auto-Resolution Rate**: Ratio of auto-resolved tickets that were incorrect or reopened.

## Offline Evaluation
- `evaluator.py`: Runs golden test datasets against the AI Agent and Decision Engine to compute accuracy, retrieval precision, and groundedness.
