import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, max, round as spark_round
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BooleanType, TimestampType

TELEMETRY_SCHEMA = StructType([
    StructField("sequence_id", DoubleType(), True),
    StructField("sensor_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("humidity", DoubleType(), True),
    StructField("vibration", DoubleType(), True),
    StructField("is_anomaly", BooleanType(), True),
    StructField("anomaly_type", StringType(), True)
])

def start_spark_analytics():
    kafka_server = os.getenv("KAFKA_SERVER", "kafka:29092")
    
    print("🚀 Initializing Spark Session inside Docker...")

    spark = SparkSession.builder \
        .appName("AtmoSync-Windowed-Analytics") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    raw_kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_server) \
        .option("subscribe", "climate-sensor-data") \
        .option("startingOffsets", "earliest") \
        .load()

    parsed_df = raw_kafka_df \
        .selectExpr("CAST(value AS STRING) as json_payload") \
        .select(from_json(col("json_payload"), TELEMETRY_SCHEMA).alias("data")) \
        .select("data.*") \
        .withColumn("event_time", col("timestamp").cast(TimestampType()))

    windowed_aggregates = parsed_df \
        .withWatermark("event_time", "2 minutes") \
        .groupBy(
            window(col("event_time"), "1 minute", "30 seconds"),
            col("sensor_id")
        ) \
        .agg(
            spark_round(avg("temperature"), 2).alias("avg_temp"),
            spark_round(avg("humidity"), 2).alias("avg_humidity"),
            spark_round(max("vibration"), 2).alias("max_vibration")
        )

    print("📊 Starting Real-Time Windowed Aggregations Stream...")
    query = windowed_aggregates.writeStream \
        .outputMode("complete") \
        .format("console") \
        .option("truncate", "false") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    start_spark_analytics()