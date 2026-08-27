SELECT DISTINCT
    predicted_category AS category_name,
    CASE 
        WHEN predicted_category IN ('legal_threat', 'security_breach', 'account_deletion') THEN 'high'
        WHEN predicted_category IN ('billing_issue', 'payment_failed') THEN 'medium'
        ELSE 'low'
    END AS risk_level
FROM {{ ref('stg_ai_predictions') }}
