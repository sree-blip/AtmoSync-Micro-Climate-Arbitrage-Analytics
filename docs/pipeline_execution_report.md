# AtmoSync End-to-End Pipeline Execution & Validation Report

This report documents the full-refresh build, data lineage architecture, and data quality testing metrics for the **AtmoSync Micro-Climate Arbitrage Analytics** dbt pipeline.

---

## 1. Pipeline Data Lineage Architecture

The ELT pipeline processes raw IoT telemetry logs streamed via Kafka into Snowflake, transforms them through staging and factual decay modeling layers, and exposes clean reporting views for BI dashboards (Power BI / Apache Superset).

```
RAW_KAFKA_TELEMETRY (Snowflake Source)
   └── stg_telemetry (Incremental Staging)
       ├── stg_telemetry_joined (Cross-Join Candidate Markets)
       └── fct_spoilage_rates (Micro-Climate Decay Math & Quality Index)
           └── fct_distance_vs_spoilage (Arrival Quality Projections)
               └── fct_arbitrage_margins (Financial Valuation & Arbitrage)
                   ├── dim_containers (Container Health Dimension Table)
                   ├── fct_arbitrage_alerts (Reroute Decision Triggering >= $50)
                   ├── rpt_container_health_summary (BI Health View)
                   └── rpt_arbitrage_opportunities (BI Trader Panel View)
```

---

## 2. Model Materialization Summary

| Model Name | Materialization Type | Schema Layer | Description |
| :--- | :--- | :--- | :--- |
| `stg_telemetry` | `incremental` | `dev_staging` | Cleaned and coalesced IoT telemetry log records. |
| `stg_telemetry_joined` | `view` | `dev_staging` | Cartesian product of telemetry logs with 4 candidate markets. |
| `fct_spoilage_rates` | `table` | `dev_marts` | Time-to-spoilage rates ($M_{\text{decay}}$) and cumulative quality score ($Q_t$). |
| `dim_containers` | `table` | `dev_marts` | Container tracking dimension table summarizing cargo status. |
| `fct_distance_vs_spoilage` | `table` | `dev_marts` | Predicted arrival quality score per candidate destination. |
| `fct_arbitrage_margins` | `table` | `dev_marts` | Grade mapping, cargo value, and net Spoilage Arbitrage calculation. |
| `fct_arbitrage_alerts` | `table` | `dev_marts` | Rerouting alert triggers for opportunities exceeding $50.00. |
| `rpt_container_health_summary` | `view` | `dev_marts` | Optimized BI reporting view for Container Health Dashboard. |
| `rpt_arbitrage_opportunities` | `view` | `dev_marts` | Optimized BI reporting view for Trader Rerouting Panel. |

---

## 3. Full-Refresh & Data Quality Test Metrics

* **`dbt run --full-refresh`**: Rebuilt all 9 models cleanly from scratch in Snowflake with **0 errors**.
* **`dbt test`**: Executed **40 data quality assertions** with a **100% pass rate** (`PASS=40 WARN=0 ERROR=0`).
* **`dbt docs generate`**: Generated static project catalog (`target/catalog.json`) and visual DAG lineage graph.
