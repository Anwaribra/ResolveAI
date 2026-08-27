WITH source AS (
    SELECT * FROM {{ source('resolveai', 'tickets') }}
)
SELECT
    ticket_id,
    customer_id,
    product_id,
    subject,
    status,
    priority,
    created_at,
    updated_at
FROM source
