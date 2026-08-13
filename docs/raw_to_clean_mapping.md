# Raw JSON to Clean SQL Schema Mapping

This document establishes the schema mapping between the raw IoT container JSON events and the clean Snowflake staging tables.

---

## 1. Raw Telemetry JSON Payload Structure

The IoT container sensors stream telemetry records matching the following JSON structure:

```json
{
  "container_id": "CONT-1002",
  "timestamp": "2026-08-13T14:30:00Z",
  "sensor_readings": {
    "temperature": 8.4,
    "humidity": 87.5,
    "vibration": 0.15
  },
  "coordinates": {
    "latitude": 34.0522,
    "longitude": -118.2437
  }
}
```

---

## 2. Staging Table Schema (`stg_telemetry`)

The raw JSON payload will be loaded into a Snowflake raw table as a `VARIANT` column type. The following SQL mapping extracts and cleans the nested JSON fields:

| Raw JSON Key | Target SQL Column | SQL Data Type | Cleaning & Mapping Rule |
| :--- | :--- | :--- | :--- |
| `container_id` | `container_id` | `VARCHAR` | Cast to string. |
| `timestamp` | `reading_time` | `TIMESTAMP` | Convert string ISO-8601 to standard UTC timestamp. |
| `sensor_readings.temperature`| `temperature_c` | `FLOAT` | Extract from nested object and cast to float. |
| `sensor_readings.humidity` | `humidity_pct` | `FLOAT` | Extract from nested object and cast to float. |
| `sensor_readings.vibration` | `vibration_g` | `FLOAT` | Extract from nested object and cast to float. |
| `coordinates.latitude` | `latitude` | `FLOAT` | Extract location coordinates. |
| `coordinates.longitude` | `longitude` | `FLOAT` | Extract location coordinates. |

---

## 3. Reference Extraction SQL (Snowflake)

To parse the raw JSON data in the dbt model, the SQL will query the JSON variant column (e.g., `raw_payload`):

```sql
SELECT
    raw_payload:container_id::VARCHAR AS container_id,
    TO_TIMESTAMP(raw_payload:timestamp::VARCHAR) AS reading_time,
    raw_payload:sensor_readings.temperature::FLOAT AS temperature_c,
    raw_payload:sensor_readings.humidity::FLOAT AS humidity_pct,
    raw_payload:sensor_readings.vibration::FLOAT AS vibration_g,
    raw_payload:coordinates.latitude::FLOAT AS latitude,
    raw_payload:coordinates.longitude::FLOAT AS longitude
FROM {{ source('raw', 'raw_container_telemetry') }}
```
