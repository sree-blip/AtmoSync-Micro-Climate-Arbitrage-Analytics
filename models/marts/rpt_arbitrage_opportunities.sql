{{
    config(
        materialized='view'
    )
}}

select
    sequence_id,
    sensor_id,
    reading_time,
    temperature_c,
    humidity_pct,
    vibration_g,
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
from {{ ref('fct_arbitrage_alerts') }}
