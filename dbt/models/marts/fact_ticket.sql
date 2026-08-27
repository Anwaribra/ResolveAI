SELECT
    t.ticket_id,
    t.customer_id,
    t.product_id,
    t.subject,
    t.status,
    t.priority,
    t.created_at,
    t.updated_at
FROM {{ ref('stg_tickets') }} t
