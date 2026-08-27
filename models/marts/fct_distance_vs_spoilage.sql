with spoilage_rates as (
    select * from {{ ref('fct_spoilage_rates') }}
),

telemetry_joined as (
    select * from {{ ref('stg_telemetry_joined') }}
),

calculations as (
    select
        s.sequence_id,
        s.sensor_id,
        s.reading_time,
        s.temperature_c,
        s.humidity_pct,
        s.vibration_g,
        s.decay_multiplier,
        s.quality_index as current_quality_index,
        
        t.market_id,
        t.market_name,
        t.transit_hours,
        t.price_premium,
        t.price_standard,
        t.price_substandard,
        t.rerouting_cost,
        
        -- Predicted quality decay during additional transit hours to the candidate market
        -- Hourly Decay Rate = Base Decay Rate * Current Decay Multiplier
        ( {{ var('base_decay_rate') }} * s.decay_multiplier ) * t.transit_hours as predicted_transit_decay,
        
        -- Predicted quality index upon arrival at candidate market (bounded between 0.0 and 1.0)
        greatest(0.0, least(1.0, s.quality_index - ( ( {{ var('base_decay_rate') }} * s.decay_multiplier ) * t.transit_hours ))) as predicted_arrival_quality
    from spoilage_rates s
    inner join telemetry_joined t 
        on s.sequence_id = t.sequence_id 
       and s.sensor_id = t.sensor_id
)

select * from calculations
