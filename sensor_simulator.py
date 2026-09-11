import json
import random
import time
from datetime import datetime, timezone
from kafka import KafkaProducer

# Kafka Server Configuration
KAFKA_SERVER = "localhost:9092"
TOPIC_NAME = "climate-sensor-data"

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# Sensor List Definitions
SENSORS = [f"SENSOR_{i}" for i in range(101, 111)]

# Day 12 Base Geo-Location Coordinates (Vijayawada Center Point)
BASE_LAT = 16.5062
BASE_LON = 80.6480


def generate_sensor_telemetry():
    print("🚀 Starting Dynamic Geo-Location Telemetry Stream (Day 12)...")

    # Generate 50,000 real-time records
    for i in range(50000):
        sensor_id = random.choice(SENSORS)

        # Day 12: Dynamic GPS Offset simulation for moving transit route
        current_lat = round(BASE_LAT + random.uniform(-0.05, 0.05), 6)
        current_lon = round(BASE_LON + random.uniform(-0.05, 0.05), 6)

        # Telemetry Data Payload
        payload = {
            "sensor_id": sensor_id,
            "temperature": round(random.uniform(20.0, 35.0), 2),
            "humidity": round(random.uniform(40.0, 80.0), 2),
            "vibration": round(random.uniform(0.1, 1.0), 2),
            "latitude": current_lat,  # Day 12 New Field
            "longitude": current_lon,  # Day 12 New Field
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Send event payload to Kafka topic
        producer.send(TOPIC_NAME, payload)

        # Day 11: Scaled High-Frequency Streaming (0.1s delay = 10 events/sec)
        time.sleep(0.1)

        # Logging output every 100 messages
        if (i + 1) % 100 == 0:
            print(
                f"[{i + 1}/50000] Sent payload: Sensor={sensor_id}, Lat={current_lat}, Lon={current_lon}"
            )

    producer.flush()
    print("✅ High-frequency streaming batch with dynamic geo-location completed.")


if __name__ == "__main__":
    generate_sensor_telemetry()