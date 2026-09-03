# AtmoSync Production Deployment & Configuration Guide

This guide details the deployment configurations, environment profile variables, and scheduled orchestration setups for deploying the **AtmoSync** dbt pipeline into a production Snowflake environment.

---

## 1. Environment Variable Profile Setup (`profiles.yml`)

For production deployment (CI/CD / Airflow / GitHub Actions), connection credentials should be passed dynamically using environment variables:

```yaml
atmosync_profile:
  target: prod
  outputs:
    prod:
      type: snowflake
      account: "{{ env_var('DBT_SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('DBT_SNOWFLAKE_USER') }}"
      password: "{{ env_var('DBT_SNOWFLAKE_PASSWORD') }}"
      role: "{{ env_var('DBT_SNOWFLAKE_ROLE', 'ANALYTICS_ADMIN') }}"
      warehouse: "{{ env_var('DBT_SNOWFLAKE_WAREHOUSE', 'ATMOSYNC_WH') }}"
      database: "{{ env_var('DBT_SNOWFLAKE_DATABASE', 'ATMOSYNC_DB') }}"
      schema: PROD_MARTS
      threads: 4
```

---

## 2. Scheduled Pipeline Orchestration

To maintain fresh data and continuous alert generation for traders, execute the pipeline on a scheduled cron cadence:

```bash
# Hourly Incremental Processing & Alert Refresh
dbt run --models staging.stg_telemetry marts.fct_spoilage_rates marts.fct_distance_vs_spoilage marts.fct_arbitrage_margins marts.fct_arbitrage_alerts marts.dim_containers

# Daily Data Quality Assertion Audit
dbt test

# Weekly Full Refresh Audit
dbt run --full-refresh
```

---

## 3. Production Readiness Checklist

- [x] **Source Schema Integration**: Connected to raw stream table `ATMOSYNC_DB.RAW.RAW_KAFKA_TELEMETRY`.
- [x] **Materialization Strategy**: Staging set to `incremental`/`view`, marts set to `table` (pre-computed window functions).
- [x] **BI Reporting Layer**: `rpt_container_health_summary` and `rpt_arbitrage_opportunities` created with read access permissions granted.
- [x] **Data Quality Assurance**: 40 automated data tests verified with 100% pass rate.
