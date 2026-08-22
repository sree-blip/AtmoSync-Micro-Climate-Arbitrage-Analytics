with telemetry as (
    select * from {{ ref('stg_telemetry') }}
),

pricing as (
    select * from {{ ref('market_pricing') }}
),

joined as (
    select
        -- Telemetry logs
        t.sequence_id,
        t.sensor_id,
        t.reading_time,
        t.temperature_c,
        t.humidity_pct,
        t.vibration_g,
        
        -- Market pricing candidates
        p.market_id,
        p.market_name,
        p.transit_hours,
        p.price_premium,
        p.price_standard,
        p.price_substandard,
        p.rerouting_cost
    from telemetry t
    cross join pricing p
)

select * from joined
