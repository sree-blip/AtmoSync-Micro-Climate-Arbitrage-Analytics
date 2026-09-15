import json
import os
import random
import time
from datetime import datetime, timezone
from kafka import KafkaProducer

# Configurable Parameters via Environment Variables
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "climate-sensor-data")
STREAM_DELAY = float(os.getenv("STREAM_DELAY", "0.01"))  # Default 10ms (~100 events/sec)
TOTAL_RECORDS = int(os.getenv("TOTAL_RECORDS", "50000"))
TEMP_ANOMALY_RATIO = int(os.getenv("TEMP_ANOMALY_RATIO", "30"))  # 1 in 30
ROUTE_ANOMALY_RATIO = int(os.getenv("ROUTE_ANOMALY_RATIO", "50"))  # 1 in 50

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    linger_ms=10,
    batch_size=16384 * 4,
)

SENSORS = [f"SENSOR_{i}" for i in range(101, 111)]
BASE_LAT = 16.5062
BASE_LON = 80.6480


def generate_sensor_telemetry():
    print(
        f"⚙️ Day 14: Parameters Fine-Tuned (Delay: {STREAM_DELAY}s, Total: {TOTAL_RECORDS})..."
    )
    start_time = time.time()

    for i in range(TOTAL_RECORDS):
        sensor_id = random.choice(SENSORS)

        # Base Realistic Telemetry Distributions
        temp = round(random.uniform(20.0, 32.0), 2)
        humidity = round(random.uniform(45.0, 75.0), 2)
        vibration = round(random.uniform(0.1, 0.8), 2)
        current_lat = round(BASE_LAT + random.uniform(-0.02, 0.02), 6)
        current_lon = round(BASE_LON + random.uniform(-0.02, 0.02), 6)
        anomaly_type = "NORMAL"

        # Fine-Tuned Anomaly Triggers
        if i % TEMP_ANOMALY_RATIO == 0:
            temp = round(random.uniform(45.0, 65.0), 2)
            anomaly_type = "TEMP_BREAKDOWN"
        elif i % ROUTE_ANOMALY_RATIO == 0:
            current_lat = round(BASE_LAT + random.uniform(0.5, 1.5), 6)
            current_lon = round(BASE_LON + random.uniform(0.5, 1.5), 6)
            anomaly_type = "ROUTE_DEVIATION"

        payload = {
            "sensor_id": sensor_id,
            "temperature": temp,
            "humidity": humidity,
            "vibration": vibration,
            "latitude": current_lat,
            "longitude": current_lon,
            "status": anomaly_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        producer.send(TOPIC_NAME, payload)

        if STREAM_DELAY > 0:
            time.sleep(STREAM_DELAY)

        if (i + 1) % 5000 == 0:
            print(f"📊 Progress: [{i + 1}/{TOTAL_RECORDS}] records processed...")

    producer.flush()
    elapsed = round(time.time() - start_time, 2)
    print(f"✅ Fine-Tuned Telemetry Run Completed in {elapsed}s!")


if __name__ == "__main__":
    generate_sensor_telemetry()