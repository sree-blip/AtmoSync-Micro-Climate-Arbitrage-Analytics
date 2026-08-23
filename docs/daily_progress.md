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

## Day 4
- Configured project-wide variables in `dbt_project.yml` for spoilage decay equations and arbitrage threshold.
- Created `packages.yml` to import the standard `dbt-utils` library dependency.
- Wrote custom macro `generate_schema_name.sql` to override Snowflake schema suffixes.
- Ran `dbt deps` successfully to download and lock dbt package dependencies.

## Day 5
- Created dbt source configuration `models/staging/sources.yml` defining the raw telemetry database schema.
- Built the initial dbt staging SQL model `models/staging/stg_telemetry.sql` to clean and cast the raw variant JSON.

## Day 6
- Implemented robust JSON parsing logic in `stg_telemetry.sql` using Snowflake's `TRY_PARSE_JSON` function.
- Structured staging queries into a parser CTE to safely process string-formatted Kafka streams.

## Day 7
- Refined `stg_telemetry.sql` to standardize timestamps to the `TIMESTAMP_NTZ` data type.
- Implemented null cleaning filters, defaulting missing telemetry readings to optimal transport parameters (5°C, 85% humidity).
- Enforced data integrity constraints by discarding records lacking critical identification properties.

## Day 8
- Created seed file `seeds/market_pricing.csv` containing transit times and prices per quality grade for candidate markets.
- Built the integrated staging model `models/staging/stg_telemetry_joined.sql` performing a cross join between telemetry and pricing metadata.

## Day 9
- Created dbt testing configurations in `models/staging/schema.yml`.
- Applied standard tests (`unique`, `not_null`) for staging fields in `stg_telemetry`.
- Configured custom multi-column test (`dbt_utils.unique_combination_of_columns`) to validate cross-joined primary keys in `stg_telemetry_joined`.
