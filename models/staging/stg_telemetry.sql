with source as (
    select * from {{ source('raw', 'raw_container_telemetry') }}
),

renamed as (
    select
        -- Extract JSON fields and cast to target SQL datatypes
        raw_payload:sequence_id::integer as sequence_id,
        raw_payload:sensor_id::varchar as sensor_id,
        to_timestamp(raw_payload:timestamp::varchar) as reading_time,
        raw_payload:temperature::float as temperature_c,
        raw_payload:humidity::float as humidity_pct,
        raw_payload:vibration::float as vibration_g
    from source
)

select * from renamed
