# Daily Progress Log

## Day 1
- Created python virtual environment (`.venv`) and installed `dbt-snowflake` & `dbt-core` (v1.12.0).
- Verified dbt installation.
- Created `.gitignore` and `requirements.txt`.
- Configured root `dbt_project.yml`.
- Created dbt directories skeleton (with `.gitkeep` placeholders).
- Created environment setup documentation (`dbt_setup.md`).

## Day 2
- Studied and documented avocado spoilage decay curve equations.
- Defined schemas and mapping fields for commodity pricing dataset joins.
- Formulated the Spoilage Arbitrage decision-making rule and logic.

## Day 3
- Defined the structure for raw telemetry IoT JSON payload data.
- Established clean target schemas for the Snowflake staging tables (`stg_telemetry`).
- Mapped JSON paths to specific SQL data types (sequence ID, sensor ID, temperature, humidity, vibration).
- Aligned the mapping schema with the actual sensor simulation payload structure pushed to the streaming branch.
- Documented dbt/Snowflake extraction SQL syntax in `docs/raw_to_clean_mapping.md`.
