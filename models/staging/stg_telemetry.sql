{{
    config(
        materialized='incremental',
        unique_key='sequence_id'
    )
}}

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
        -- Coalesce to support both the streaming engineer's keys (sequence_id/sensor_id) 
        -- and the warehouse engineer's dummy test keys (event_id/container_id)
        coalesce(
            json_payload:sequence_id::varchar, 
            json_payload:event_id::varchar
        ) as sequence_id,
        
        coalesce(
            json_payload:sensor_id::varchar, 
            json_payload:container_id::varchar
        ) as sensor_id,
        
        -- Coalesce timestamp: use payload timestamp if available, fallback to Snowflake ingestion time
        coalesce(
            cast(json_payload:timestamp::varchar as timestamp_ntz),
            cast(ingested_at as timestamp_ntz)
        ) as reading_time,
        
        -- Clean nulls by defaulting missing readings to optimal transport parameters (5.0C temp, 85% hum, 0.0G vib)
        coalesce(json_payload:temperature::float, 5.0) as temperature_c,
        coalesce(json_payload:humidity::float, 85.0) as humidity_pct,
        coalesce(json_payload:vibration::float, 0.0) as vibration_g
    from parsed
    -- Enforce data integrity by discarding records missing critical identification logs
    where coalesce(json_payload:sensor_id::varchar, json_payload:container_id::varchar) is not null 
      and coalesce(cast(json_payload:timestamp::varchar as timestamp_ntz), cast(ingested_at as timestamp_ntz)) is not null

    {% if is_incremental() %}
    -- Filter to process only newly ingested records during incremental execution
    and coalesce(cast(json_payload:timestamp::varchar as timestamp_ntz), cast(ingested_at as timestamp_ntz)) > (select max(reading_time) from {{ this }})
    {% endif %}
)

select * from cleaned
