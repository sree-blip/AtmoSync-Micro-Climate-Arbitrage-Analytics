import json
import os
import random
import time
from datetime import datetime, timezone
from kafka import KafkaProducer

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9092")
TOPIC_NAME = "climate-sensor-data"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    # Fast In-Memory Batching Optimizations
    linger_ms=10,
    batch_size=16384 * 4,
)

SENSORS = [f"SENSOR_{i}" for i in range(101, 111)]
BASE_LAT = 16.5062
BASE_LON = 80.6480


def generate_sensor_telemetry():
    print("⚡⚡ Max Speed (Zero-Delay) Streaming Started...")
    start_time = time.time()

    for i in range(50000):
        sensor_id = random.choice(SENSORS)
        temp = round(random.uniform(20.0, 30.0), 2)
        humidity = round(random.uniform(40.0, 70.0), 2)
        vibration = round(random.uniform(0.1, 1.0), 2)
        current_lat = round(BASE_LAT + random.uniform(-0.02, 0.02), 6)
        current_lon = round(BASE_LON + random.uniform(-0.02, 0.02), 6)
        anomaly_type = "NORMAL"

        if i % 30 == 0:
            temp = round(random.uniform(45.0, 65.0), 2)
            anomaly_type = "TEMP_BREAKDOWN"
        elif i % 50 == 0:
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

        # Send asynchronously (NO DELAY)
        producer.send(TOPIC_NAME, payload)

        if (i + 1) % 10000 == 0:
            print(f"🚀 Pushed [{i + 1}/50000] events to Kafka memory...")

    producer.flush()  # Ensures all buffered records are delivered
    end_time = time.time()
    print(
        f"✅ 50,000 Records Streamed in {round(end_time - start_time, 2)} seconds!"
    )


if __name__ == "__main__":
    generate_sensor_telemetry()