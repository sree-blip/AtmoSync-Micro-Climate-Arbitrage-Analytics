{{
    config(
        materialized='view'
    )
}}

with containers as (
    select * from {{ ref('dim_containers') }}
),

alerts as (
    select
        sensor_id,
        count(*) as active_arbitrage_alerts
    from {{ ref('fct_arbitrage_alerts') }}
    group by sensor_id
)

select
    c.sensor_id,
    c.total_reading_count,
    c.first_reading_time,
    c.last_reading_time,
    c.last_recorded_temperature_c,
    c.last_recorded_humidity_pct,
    c.last_recorded_vibration_g,
    c.last_recorded_decay_multiplier,
    c.last_recorded_quality_index,
    c.current_cargo_status,
    coalesce(a.active_arbitrage_alerts, 0) as total_active_alerts
from containers c
left join alerts a on c.sensor_id = a.sensor_id
