with source as (
    select * from {{ source('raw', 'raw_container_telemetry') }}
),

parsed as (
    select
        -- Use TRY_PARSE_JSON to safely parse raw payload string as variant (returns null if malformed)
        try_parse_json(raw_payload) as json_payload
    from source
),

cleaned as (
    select
        json_payload:sequence_id::integer as sequence_id,
        json_payload:sensor_id::varchar as sensor_id,
        
        -- Standardize to TIMESTAMP_NTZ (non-timezone aware UTC) to prevent time-offset calculation issues
        cast(json_payload:timestamp::varchar as timestamp_ntz) as reading_time,
        
        -- Clean nulls by defaulting missing readings to optimal transport parameters (5.0C temp, 85% hum, 0.0G vib)
        coalesce(json_payload:temperature::float, 5.0) as temperature_c,
        coalesce(json_payload:humidity::float, 85.0) as humidity_pct,
        coalesce(json_payload:vibration::float, 0.0) as vibration_g
    from parsed
    -- Enforce data integrity by discarding records missing critical identification logs
    where json_payload:sensor_id is not null 
      and json_payload:timestamp is not null
)

select * from cleaned
