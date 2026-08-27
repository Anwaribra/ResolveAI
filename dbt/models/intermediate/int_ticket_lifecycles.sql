WITH tickets AS (
    SELECT * FROM {{ ref('stg_tickets') }}
),
predictions AS (
    SELECT * FROM {{ ref('stg_ai_predictions') }}
)
SELECT
    t.ticket_id,
    t.customer_id,
    t.product_id,
    t.status AS current_status,
    t.priority AS ticket_priority,
    p.prediction_id,
    p.predicted_category,
    p.predicted_intent,
    p.predicted_priority,
    p.confidence_score,
    p.retrieval_quality,
    p.decision AS ai_decision,
    t.created_at AS ticket_created_at,
    p.created_at AS prediction_created_at
FROM tickets t
LEFT JOIN predictions p ON t.ticket_id = p.ticket_id
