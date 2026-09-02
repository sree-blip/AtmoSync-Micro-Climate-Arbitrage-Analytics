
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
