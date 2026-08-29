with source as (
    select * from {{ source('raw', 'RAW_KAFKA_TELEMETRY') }}
),

parsed as (
    select
        -- Use TRY_PARSE_JSON to safely parse raw payload string as variant (returns null if malformed)
        try_parse_json(payload) as json_payload,
        ingested_at
    from source
),

cleaned as (
    select
        json_payload:event_id::varchar as sequence_id,
        json_payload:container_id::varchar as sensor_id,
        
        -- Standardize to TIMESTAMP_NTZ (non-timezone aware UTC) to prevent time-offset calculation issues
        cast(ingested_at as timestamp_ntz) as reading_time,
        
        -- Clean nulls by defaulting missing readings to optimal transport parameters (5.0C temp, 85% hum, 0.0G vib)
        coalesce(json_payload:temperature::float, 5.0) as temperature_c,
        coalesce(json_payload:humidity::float, 85.0) as humidity_pct,
        coalesce(json_payload:vibration::float, 0.0) as vibration_g
    from parsed
    -- Enforce data integrity by discarding records missing critical identification logs
    where json_payload:container_id is not null 
      and ingested_at is not null
)

select * from cleaned
