with margins as (
    select * from {{ ref('fct_arbitrage_margins') }}
),

ranked_options as (
    select
        sequence_id,
        sensor_id,
        reading_time,
        temperature_c,
        humidity_pct,
        vibration_g,
        decay_multiplier,
        current_quality_index,
        
        market_id as recommended_market_id,
        market_name as recommended_market_name,
        transit_hours as remaining_transit_hours,
        predicted_arrival_quality,
        predicted_quality_grade as expected_arrival_grade,
        
        cargo_value,
        original_market_value,
        rerouting_cost,
        spoilage_arbitrage as net_arbitrage_margin,
        
        -- Rank profitable options per container event to identify the maximum arbitrage payout
        row_number() over (
            partition by sequence_id, sensor_id 
            order by spoilage_arbitrage desc
        ) as arbitrage_rank
    from margins
    -- Filter out options yielding less than our standard spoilage arbitrage threshold
    where spoilage_arbitrage >= {{ var('spoilage_arbitrage_threshold') }}
)

select
    sequence_id,
    sensor_id,
    reading_time,
    temperature_c,
    humidity_pct,
    vibration_g,
    decay_multiplier,
    current_quality_index,
    
    recommended_market_id,
    recommended_market_name,
    remaining_transit_hours,
    predicted_arrival_quality,
    expected_arrival_grade,
    
    cargo_value,
    original_market_value,
    rerouting_cost,
    net_arbitrage_margin
from ranked_options
where arbitrage_rank = 1
