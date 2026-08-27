SELECT
    customer_id,
    email,
    name,
    tier,
    created_at
FROM {{ source('resolveai', 'customers') }}
