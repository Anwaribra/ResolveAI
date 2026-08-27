import json
import logging
from dataclasses import dataclass
from pathlib import Path
from .metrics import calculate_auto_resolution_rate, calculate_escalation_rate, calculate_false_auto_resolution_rate

logger = logging.getLogger(__name__)


@dataclass
class EvaluationReport:
    total_samples: int
    classification_accuracy: float
    auto_resolution_rate: float
    escalation_rate: float
    false_auto_resolution_rate: float


class ModelEvaluator:
    """Evaluates agent performance against golden ground-truth test datasets."""

    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)

    def load_dataset(self) -> list[dict]:
        if not self.dataset_path.exists():
            logger.warning("Dataset path %s does not exist", self.dataset_path)
            return []
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def run_evaluation(self) -> EvaluationReport:
        dataset = self.load_dataset()
        if not dataset:
            return EvaluationReport(0, 0.0, 0.0, 0.0, 0.0)

        correct_categories = 0
        auto_resolved = 0
        escalated = 0
        false_auto_resolutions = 0

        for item in dataset:
            # Stub evaluation logic
            correct_categories += 1
            if item.get("expected_decision") == "AUTO_RESOLVE":
                auto_resolved += 1
            else:
                escalated += 1

        total = len(dataset)
        return EvaluationReport(
            total_samples=total,
            classification_accuracy=correct_categories / total if total > 0 else 0.0,
            auto_resolution_rate=calculate_auto_resolution_rate(total, auto_resolved),
            escalation_rate=calculate_escalation_rate(total, escalated),
            false_auto_resolution_rate=calculate_false_auto_resolution_rate(
                auto_resolved, false_auto_resolutions
            ),
        )
