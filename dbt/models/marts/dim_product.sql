SELECT
    product_id,
    name,
    category,
    created_at
FROM {{ source('resolveai', 'products') }}
