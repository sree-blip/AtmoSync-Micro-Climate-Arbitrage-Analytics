with source as (
    select * from {{ source('raw', 'raw_container_telemetry') }}
),

parsed as (
    select
        -- Use TRY_PARSE_JSON to safely parse raw payload string as variant (returns null if malformed)
        try_parse_json(raw_payload) as json_payload
    from source
),

renamed as (
    select
        -- Extract JSON fields and cast to target SQL datatypes from the parsed variant object
        json_payload:sequence_id::integer as sequence_id,
        json_payload:sensor_id::varchar as sensor_id,
        to_timestamp(json_payload:timestamp::varchar) as reading_time,
        json_payload:temperature::float as temperature_c,
        json_payload:humidity::float as humidity_pct,
        json_payload:vibration::float as vibration_g
    from parsed
)

select * from renamed
