SELECT
    resolution_id,
    ticket_id,
    resolved_by,
    final_category,
    satisfaction_score,
    resolved_at
FROM {{ source('resolveai', 'resolutions') }}
