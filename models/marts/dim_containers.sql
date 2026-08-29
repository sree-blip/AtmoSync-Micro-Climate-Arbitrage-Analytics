with spoilage_rates as (
    select * from {{ ref('fct_spoilage_rates') }}
),

latest_telemetry as (
    select
        sensor_id,
        reading_time,
        temperature_c,
        humidity_pct,
        vibration_g,
        decay_multiplier,
        quality_index,
        row_number() over (partition by sensor_id order by reading_time desc) as row_num
    from spoilage_rates
),

container_metrics as (
    select
        sensor_id,
        count(*) as total_reading_count,
        min(reading_time) as first_reading_time,
        max(reading_time) as last_reading_time
    from spoilage_rates
    group by sensor_id
)

select
    c.sensor_id,
    c.total_reading_count,
    c.first_reading_time,
    c.last_reading_time,
    l.temperature_c as last_recorded_temperature_c,
    l.humidity_pct as last_recorded_humidity_pct,
    l.vibration_g as last_recorded_vibration_g,
    l.decay_multiplier as last_recorded_decay_multiplier,
    l.quality_index as last_recorded_quality_index,
    
    -- Cargo status classified based on current quality score
    case
        when l.quality_index >= 0.85 then 'Healthy'
        when l.quality_index >= 0.60 then 'At Risk'
        else 'Spoiled'
    end as current_cargo_status
from container_metrics c
inner join latest_telemetry l 
    on c.sensor_id = l.sensor_id 
   and l.row_num = 1
