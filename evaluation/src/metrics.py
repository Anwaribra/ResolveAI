"""Metric definitions for ResolveAI AI and operational performance evaluation."""


def calculate_false_auto_resolution_rate(
    total_auto_resolved: int, incorrect_auto_resolved: int
) -> float:
    """Calculate critical safety metric: False Auto-Resolution Rate.

    Formula: Incorrect Auto-Resolved Tickets / Total Auto-Resolved Tickets
    """
    if total_auto_resolved == 0:
        return 0.0
    return incorrect_auto_resolved / total_auto_resolved


def calculate_auto_resolution_rate(
    total_tickets: int, auto_resolved_tickets: int
) -> float:
    """Calculate proportion of incoming tickets resolved automatically."""
    if total_tickets == 0:
        return 0.0
    return auto_resolved_tickets / total_tickets


def calculate_escalation_rate(
    total_tickets: int, escalated_tickets: int
) -> float:
    """Calculate proportion of incoming tickets escalated to human agents."""
    if total_tickets == 0:
        return 0.0
    return escalated_tickets / total_tickets
