# Staging Pipeline Verification & Testing Plan

This document outlines the testing procedures and validation queries for the AtmoSync staging pipeline (`stg_telemetry` and `stg_telemetry_joined`).

---

## 1. Automated pipeline execution

Once the Snowflake database connection in `profiles.yml` is active, the staging models can be compiled and validated using the following sequence:

```bash
# 1. Load the candidate market pricing metadata seed table
dbt seed

# 2. Run the staging models
dbt run --select staging

# 3. Execute the 12 staging validation tests (unique, not_null, composite keys)
dbt test --select staging
```

---

## 2. Snowflake Manual SQL Assertions

To manually verify the parsed JSON fields and data cleaning transformations in Snowflake, run the following diagnostic queries:

### Query A: Telemetry Extraction & Default Value Check
Verify that the `TRY_PARSE_JSON` logic, timestamp conversions, and null default replacements are operating correctly.

```sql
SELECT
    sensor_id,
    reading_time,
    temperature_c,
    humidity_pct,
    vibration_g,
    -- Assert that standard defaults were applied for missing values:
    CASE WHEN temperature_c = 5.0 THEN 'Defaulted optimal temp' ELSE 'Real temp' END AS temp_status,
    CASE WHEN humidity_pct = 85.0 THEN 'Defaulted optimal humidity' ELSE 'Real humidity' END AS humidity_status
FROM {{ ref('stg_telemetry') }}
LIMIT 100;
```

### Query B: Data Integrity Integrity Check
Ensure that the telemetry cleaner successfully discarded logs lacking critical identification information.

```sql
-- This assertion query should return 0 rows.
SELECT COUNT(*) 
FROM {{ ref('stg_telemetry') }}
WHERE sensor_id IS NULL 
   OR reading_time IS NULL;
```

### Query C: Cross-Join Validation Check
Ensure that for every telemetry log, a pricing option is mapped for each candidate market (Cartesian product).

```sql
-- This check should show exactly 4 rows (markets) per sequence_id.
SELECT 
    sequence_id, 
    COUNT(DISTINCT market_id) AS market_count
FROM {{ ref('stg_telemetry_joined') }}
GROUP BY sequence_id
HAVING COUNT(DISTINCT market_id) <> 4;
-- Output should be empty, verifying every record maps to all 4 destinations.
```
