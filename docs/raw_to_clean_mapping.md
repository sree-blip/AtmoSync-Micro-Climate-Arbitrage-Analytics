# Raw JSON to Clean SQL Schema Mapping

This document establishes the schema mapping between the raw IoT container JSON events and the clean Snowflake staging tables.

---

## 1. Raw Telemetry JSON Payload Structure

The IoT container sensors stream telemetry records matching the following JSON structure:

```json
{
  "sequence_id": 49950,
  "sensor_id": "SENSOR_003",
  "timestamp": "2026-08-13T06:48:02.837218+00:00",
  "temperature": 31.14,
  "humidity": 51.62,
  "vibration": 1.612
}
```

---

## 2. Staging Table Schema (`stg_telemetry`)

The raw JSON payload will be loaded into a Snowflake raw table as a `VARIANT` column type. The following SQL mapping extracts and cleans the flat JSON fields:

| Raw JSON Key | Target SQL Column | SQL Data Type | Cleaning & Mapping Rule |
| :--- | :--- | :--- | :--- |
| `sequence_id` | `sequence_id` | `INTEGER` | Extract sequential log ID. |
| `sensor_id` | `sensor_id` | `VARCHAR` | Cast to string (identifies container sensor). |
| `timestamp` | `reading_time` | `TIMESTAMP` | Convert ISO-8601 string to standard UTC timestamp. |
| `temperature` | `temperature_c` | `FLOAT` | Cast to float. |
| `humidity` | `humidity_pct` | `FLOAT` | Cast to float. |
| `vibration` | `vibration_g` | `FLOAT` | Cast to float. |

---

## 3. Reference Extraction SQL (Snowflake)

To parse the raw JSON data in the dbt model, the SQL will query the flat JSON keys directly from the variant column (e.g., `raw_payload`):

```sql
SELECT
    raw_payload:sequence_id::INTEGER AS sequence_id,
    raw_payload:sensor_id::VARCHAR AS sensor_id,
    TO_TIMESTAMP(raw_payload:timestamp::VARCHAR) AS reading_time,
    raw_payload:temperature::FLOAT AS temperature_c,
    raw_payload:humidity::FLOAT AS humidity_pct,
    raw_payload:vibration::FLOAT AS vibration_g
FROM {{ source('raw', 'raw_container_telemetry') }}
```
