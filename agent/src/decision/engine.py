from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class DecisionOutcome(str, Enum):
    AUTO_RESOLVE = "AUTO_RESOLVE"
    ESCALATE = "ESCALATE"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class DecisionInput:
    confidence_score: float
    retrieval_quality: float
    category: str
    priority: str
    customer_tier: str = "standard"
    historical_category_success_rate: float = 0.90
    has_relevant_knowledge: bool = True


@dataclass
class DecisionResult:
    decision: DecisionOutcome
    risk_level: RiskLevel
    reason: str
    confidence_threshold_met: bool
    retrieval_threshold_met: bool


class DecisionEngine:
    """Independent Decision & Governance Layer for Support Ticket Auto-Resolution.

    Decides whether a ticket can be automatically resolved or must be escalated
    to a human agent based on confidence, retrieval quality, risk, and priority.
    """

    HIGH_RISK_CATEGORIES = {
        "security_breach",
        "legal_threat",
        "account_deletion",
        "billing_dispute",
    }

    CONFIDENCE_THRESHOLD = 0.85
    RETRIEVAL_THRESHOLD = 0.80

    def evaluate(self, input_data: DecisionInput) -> DecisionResult:
        logger.info(
            "Evaluating decision for category=%s, priority=%s, confidence=%.2f, retrieval=%.2f",
            input_data.category,
            input_data.priority,
            input_data.confidence_score,
            input_data.retrieval_quality,
        )

        conf_met = input_data.confidence_score >= self.CONFIDENCE_THRESHOLD
        retrieval_met = input_data.retrieval_quality >= self.RETRIEVAL_THRESHOLD

        # 1. Check for High-Risk Categories
        if input_data.category.lower() in self.HIGH_RISK_CATEGORIES:
            return DecisionResult(
                decision=DecisionOutcome.ESCALATE,
                risk_level=RiskLevel.HIGH,
                reason=f"Category '{input_data.category}' is classified as high-risk.",
                confidence_threshold_met=conf_met,
                retrieval_threshold_met=retrieval_met,
            )

        # 2. Check for Urgent Priority
        if input_data.priority.lower() == "urgent":
            return DecisionResult(
                decision=DecisionOutcome.ESCALATE,
                risk_level=RiskLevel.HIGH,
                reason="Urgent priority tickets require immediate human agent review.",
                confidence_threshold_met=conf_met,
                retrieval_threshold_met=retrieval_met,
            )

        # 3. Check for Lack of Knowledge Context
        if not input_data.has_relevant_knowledge or not retrieval_met:
            return DecisionResult(
                decision=DecisionOutcome.ESCALATE,
                risk_level=RiskLevel.MEDIUM,
                reason="Knowledge retrieval score is below safety threshold (0.80).",
                confidence_threshold_met=conf_met,
                retrieval_threshold_met=retrieval_met,
            )

        # 4. Check Classification Confidence
        if not conf_met:
            return DecisionResult(
                decision=DecisionOutcome.ESCALATE,
                risk_level=RiskLevel.MEDIUM,
                reason="AI classification confidence is below safety threshold (0.85).",
                confidence_threshold_met=conf_met,
                retrieval_threshold_met=retrieval_met,
            )

        # 5. Check Historical Category Success Rate
        if input_data.historical_category_success_rate < 0.75:
            return DecisionResult(
                decision=DecisionOutcome.ESCALATE,
                risk_level=RiskLevel.MEDIUM,
                reason=f"Historical success rate for '{input_data.category}' is below threshold (0.75).",
                confidence_threshold_met=conf_met,
                retrieval_threshold_met=retrieval_met,
            )

        # All safety checks passed
        return DecisionResult(
            decision=DecisionOutcome.AUTO_RESOLVE,
            risk_level=RiskLevel.LOW,
            reason="High confidence prediction with strong knowledge retrieval and low-risk category.",
            confidence_threshold_met=True,
            retrieval_threshold_met=True,
        )
