
-- AtmoSync Project
-- Day 1: Snowflake Setup

-- Create database
CREATE DATABASE IF NOT EXISTS ATMOSYNC_DB;

-- Use database
USE DATABASE ATMOSYNC_DB;

-- Create warehouse
CREATE WAREHOUSE IF NOT EXISTS ATMOSYNC_WH
WAREHOUSE_SIZE = 'X-SMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE;

-- Use warehouse
USE WAREHOUSE ATMOSYNC_WH;

-- Verify database
SHOW DATABASES;

-- Verify warehouse
SHOW WAREHOUSES;


-- ============================================
-- Day 2: Create Data Warehouse Schemas
-- ============================================

USE DATABASE ATMOSYNC_DB;

-- Create RAW schema
CREATE SCHEMA  RAW;

-- Create STAGING schema
CREATE SCHEMA  STAGING;

-- Create ANALYTICS schema
CREATE SCHEMA  ANALYTICS;

-- Check schemas
SHOW SCHEMAS;


-- ============================================
-- Day 3: Create RAW IoT Tables
-- ============================================

USE DATABASE ATMOSYNC_DB;

USE SCHEMA RAW;

-- Create internal stage
CREATE STAGE IF NOT EXISTS IOT_STAGE;

-- Create RAW telemetry table
CREATE TABLE IF NOT EXISTS RAW_TELEMETRY (
    EVENT_ID VARCHAR,
    CONTAINER_ID VARCHAR,
    TEMPERATURE FLOAT,
    HUMIDITY FLOAT,
    VIBRATION FLOAT,
    LATITUDE FLOAT,
    LONGITUDE FLOAT,
    EVENT_TIMESTAMP TIMESTAMP,
    RAW_DATA VARIANT,
    INGESTED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Check table
SHOW TABLES;

-- Check stage
SHOW STAGES;


-- ============================================
-- Day 4: Kafka-Snowflake Ingestion Test
-- ============================================

USE DATABASE ATMOSYNC_DB;

USE SCHEMA RAW;

-- Table for incoming Kafka JSON payload
CREATE TABLE IF NOT EXISTS RAW_KAFKA_TELEMETRY (
    RECORD_ID NUMBER AUTOINCREMENT,
    PAYLOAD VARIANT,
    INGESTED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Insert sample Kafka JSON
INSERT INTO RAW_KAFKA_TELEMETRY (PAYLOAD)
SELECT PARSE_JSON('
{
    "event_id": "EVT001",
    "container_id": "CONT001",
    "temperature": 7.5,
    "humidity": 65,
    "vibration": 0.2,
    "latitude": 15.85,
    "longitude": 74.50
}
');

-- Check incoming data
SELECT *
FROM RAW_KAFKA_TELEMETRY;



-- ============================================
-- Day 5: RAW Telemetry Validation
-- ============================================

USE DATABASE ATMOSYNC_DB;

USE SCHEMA RAW;

-- Count records
SELECT COUNT(*) AS TOTAL_RECORDS
FROM RAW_KAFKA_TELEMETRY;

-- Check latest records
SELECT *
FROM RAW_KAFKA_TELEMETRY
ORDER BY INGESTED_AT DESC
LIMIT 10;

-- Check important JSON fields
SELECT
    PAYLOAD:event_id::STRING AS EVENT_ID,
    PAYLOAD:container_id::STRING AS CONTAINER_ID,
    PAYLOAD:temperature::FLOAT AS TEMPERATURE,
    PAYLOAD:humidity::FLOAT AS HUMIDITY,
    PAYLOAD:vibration::FLOAT AS VIBRATION
FROM RAW_KAFKA_TELEMETRY;

-- Check missing event IDs
SELECT COUNT(*) AS MISSING_EVENT_ID
FROM RAW_KAFKA_TELEMETRY
WHERE PAYLOAD:event_id IS NULL;

-- Check missing container IDs
SELECT COUNT(*) AS MISSING_CONTAINER_ID
FROM RAW_KAFKA_TELEMETRY
WHERE PAYLOAD:container_id IS NULL;


-- ============================================
-- Day 6: RAW Ingestion Optimization
-- ============================================

USE DATABASE ATMOSYNC_DB;

-- Check warehouse
SHOW WAREHOUSES;

-- Configure warehouse for efficient usage
ALTER WAREHOUSE ATMOSYNC_WH
SET
    WAREHOUSE_SIZE = 'X-SMALL',
    AUTO_SUSPEND = 60,
    AUTO_RESUME = TRUE;

-- Use warehouse
USE WAREHOUSE ATMOSYNC_WH;

-- Check RAW record count
SELECT COUNT(*) AS RAW_RECORD_COUNT
FROM RAW.RAW_KAFKA_TELEMETRY;

-- Check recent ingestion
SELECT
    RECORD_ID,
    INGESTED_AT
FROM RAW.RAW_KAFKA_TELEMETRY
ORDER BY INGESTED_AT DESC
LIMIT 10;



-- ============================================
-- Day 7: Create STAGING Table
-- ============================================

USE DATABASE ATMOSYNC_DB;

USE SCHEMA STAGING;

-- Create staging telemetry table
CREATE TABLE IF NOT EXISTS STG_TELEMETRY (
    EVENT_ID VARCHAR,
    CONTAINER_ID VARCHAR,
    TEMPERATURE FLOAT,
    HUMIDITY FLOAT,
    VIBRATION FLOAT,
    LATITUDE FLOAT,
    LONGITUDE FLOAT,
    EVENT_TIMESTAMP TIMESTAMP,
    INGESTED_AT TIMESTAMP
);

-- Load JSON data from RAW into STAGING
INSERT INTO STG_TELEMETRY (
    EVENT_ID,
    CONTAINER_ID,
    TEMPERATURE,
    HUMIDITY,
    VIBRATION,
    LATITUDE,
    LONGITUDE,
    EVENT_TIMESTAMP,
    INGESTED_AT
)
SELECT
    PAYLOAD:event_id::STRING,
    PAYLOAD:container_id::STRING,
    PAYLOAD:temperature::FLOAT,
    PAYLOAD:humidity::FLOAT,
    PAYLOAD:vibration::FLOAT,
    PAYLOAD:latitude::FLOAT,
    PAYLOAD:longitude::FLOAT,
    CURRENT_TIMESTAMP(),
    INGESTED_AT
FROM RAW.RAW_KAFKA_TELEMETRY;

-- Check staging data
SELECT *
FROM STG_TELEMETRY;

-- ============================================
-- Day 8: Snowflake Warehouse Monitoring
-- ============================================

USE DATABASE ATMOSYNC_DB;

-- Check warehouses
SHOW WAREHOUSES;

-- Check RAW records
SELECT
    COUNT(*) AS RAW_RECORDS
FROM RAW.RAW_KAFKA_TELEMETRY;

-- Check STAGING records
SELECT
    COUNT(*) AS STAGING_RECORDS
FROM STAGING.STG_TELEMETRY;

-- Check storage metrics
SELECT
    TABLE_SCHEMA,
    TABLE_NAME,
    ACTIVE_BYTES,
    TIME_TRAVEL_BYTES
FROM ATMOSYNC_DB.INFORMATION_SCHEMA.TABLE_STORAGE_METRICS
ORDER BY ACTIVE_BYTES DESC;

-- Check recent RAW ingestion
SELECT
    COUNT(*) AS RECORDS_LAST_24_HOURS
FROM RAW.RAW_KAFKA_TELEMETRY
WHERE INGESTED_AT >= DATEADD(HOUR, -24, CURRENT_TIMESTAMP());
