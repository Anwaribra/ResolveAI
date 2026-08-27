WITH source AS (
    SELECT * FROM {{ source('resolveai', 'ai_predictions') }}
)
SELECT
    prediction_id,
    ticket_id,
    predicted_category,
    predicted_intent,
    predicted_priority,
    confidence_score,
    retrieval_quality,
    generated_response,
    decision,
    model_version,
    prompt_version,
    created_at
FROM source
