with distance_spoilage as (
    select * from {{ ref('fct_distance_vs_spoilage') }}
),

grade_pricing as (
    select
        sequence_id,
        sensor_id,
        reading_time,
        temperature_c,
        humidity_pct,
        vibration_g,
        decay_multiplier,
        current_quality_index,
        
        market_id,
        market_name,
        transit_hours,
        rerouting_cost,
        predicted_arrival_quality,
        
        -- Determine quality grade mapping and select price per box
        case
            when predicted_arrival_quality >= 0.85 then 'Premium'
            when predicted_arrival_quality >= 0.60 then 'Standard'
            else 'Substandard'
        end as predicted_quality_grade,
        
        case
            when predicted_arrival_quality >= 0.85 then price_premium
            when predicted_arrival_quality >= 0.60 then price_standard
            else price_substandard
        end as price_per_box,
        
        -- Total cargo value assuming container capacity of 1,000 boxes
        (case
            when predicted_arrival_quality >= 0.85 then price_premium
            when predicted_arrival_quality >= 0.60 then price_standard
            else price_substandard
        end) * 1000 as cargo_value
    from distance_spoilage
),

baseline_value as (
    select
        *,
        -- Extract New York (MKT_002) value as original default path baseline
        max(case when market_id = 'MKT_002' then cargo_value end) over (
            partition by sequence_id, sensor_id
        ) as original_market_value
    from grade_pricing
),

margins as (
    select
        sequence_id,
        sensor_id,
        reading_time,
        temperature_c,
        humidity_pct,
        vibration_g,
        decay_multiplier,
        current_quality_index,
        
        market_id,
        market_name,
        transit_hours,
        rerouting_cost,
        predicted_arrival_quality,
        predicted_quality_grade,
        price_per_box,
        cargo_value,
        original_market_value,
        
        -- Spoilage Arbitrage: Candidate Cargo Value - Reroute Cost - Original Cargo Value (0 for default destination)
        case
            when market_id = 'MKT_002' then 0.00
            else cargo_value - rerouting_cost - original_market_value
        end as spoilage_arbitrage
    from baseline_value
)

select * from margins
