SELECT
    escalation_id,
    ticket_id,
    reason,
    assigned_agent_id,
    escalated_at
FROM {{ source('resolveai', 'escalations') }}
