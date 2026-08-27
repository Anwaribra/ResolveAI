import pytest
from agent.src.decision.engine import DecisionEngine, DecisionInput, DecisionOutcome, RiskLevel


def test_decision_engine_auto_resolve():
    engine = DecisionEngine()
    input_data = DecisionInput(
        confidence_score=0.92,
        retrieval_quality=0.88,
        category="account_access",
        priority="medium",
        has_relevant_knowledge=True,
    )
    result = engine.evaluate(input_data)
    assert result.decision == DecisionOutcome.AUTO_RESOLVE
    assert result.risk_level == RiskLevel.LOW
    assert result.confidence_threshold_met is True
    assert result.retrieval_threshold_met is True


def test_decision_engine_escalate_high_risk_category():
    engine = DecisionEngine()
    input_data = DecisionInput(
        confidence_score=0.99,
        retrieval_quality=0.95,
        category="security_breach",
        priority="medium",
    )
    result = engine.evaluate(input_data)
    assert result.decision == DecisionOutcome.ESCALATE
    assert result.risk_level == RiskLevel.HIGH
    assert "high-risk" in result.reason.lower()


def test_decision_engine_escalate_low_confidence():
    engine = DecisionEngine()
    input_data = DecisionInput(
        confidence_score=0.60,
        retrieval_quality=0.90,
        category="general_inquiry",
        priority="low",
    )
    result = engine.evaluate(input_data)
    assert result.decision == DecisionOutcome.ESCALATE
    assert result.confidence_threshold_met is False


def test_decision_engine_escalate_urgent_priority():
    engine = DecisionEngine()
    input_data = DecisionInput(
        confidence_score=0.95,
        retrieval_quality=0.90,
        category="billing",
        priority="urgent",
    )
    result = engine.evaluate(input_data)
    assert result.decision == DecisionOutcome.ESCALATE
    assert "urgent" in result.reason.lower()
