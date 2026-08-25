with telemetry as (
    select * from {{ ref('stg_telemetry') }}
),

time_intervals as (
    select
        sequence_id,
        sensor_id,
        reading_time,
        temperature_c,
        humidity_pct,
        vibration_g,
        -- Calculate time difference in hours between logs per container (default to 0.0 for first log)
        coalesce(
            datediff(
                'second', 
                lag(reading_time) over (partition by sensor_id order by reading_time), 
                reading_time
            ) / 3600.0, 
            0.0
        ) as delta_t_hours
    from telemetry
),

decay_calculations as (
    select
        sequence_id,
        sensor_id,
        reading_time,
        temperature_c,
        humidity_pct,
        vibration_g,
        delta_t_hours,
        
        -- Decay multiplier: exp(k_t * (T - T_opt)) * exp(k_h * (H - H_opt))
        exp(
            {{ var('k_t') }} * (temperature_c - {{ var('opt_temp') }})
        ) * exp(
            {{ var('k_h') }} * (humidity_pct - {{ var('opt_humidity') }})
        ) as decay_multiplier
    from time_intervals
),

cumulative_decay as (
    select
        sequence_id,
        sensor_id,
        reading_time,
        temperature_c,
        humidity_pct,
        vibration_g,
        delta_t_hours,
        decay_multiplier,
        
        -- Interval decay: Base Decay Rate * Decay Multiplier * delta_t_hours
        {{ var('base_decay_rate') }} * decay_multiplier * delta_t_hours as interval_decay,
        
        -- Cumulative sum of interval decays per container ordered by reading time
        sum(interval_decay) over (
            partition by sensor_id 
            order by reading_time 
            rows between unbounded preceding and current row
        ) as accumulated_decay
    from decay_calculations
),

final as (
    select
        sequence_id,
        sensor_id,
        reading_time,
        temperature_c,
        humidity_pct,
        vibration_g,
        delta_t_hours,
        decay_multiplier,
        interval_decay,
        accumulated_decay,
        
        -- Bounded Quality index: between 0.0 (spoiled) and 1.0 (fresh)
        greatest(0.0, least(1.0, 1.0 - accumulated_decay)) as quality_index
    from cumulative_decay
)

select * from final
