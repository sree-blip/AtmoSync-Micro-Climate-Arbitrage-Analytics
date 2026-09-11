import json
import time
import random
import os
from datetime import datetime, timezone
from kafka import KafkaProducer

# Kafka broker setup
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9092")
TOPIC = "climate-sensor-data"

def create_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

def generate_telemetry_data():
    producer = create_kafka_producer()
    sensors = [f"SENSOR_{i}" for i in range(101, 111)]
    
    total_records = 50000
    print(f"🚀 Day 11: Starting High-Frequency Telemetry Stream ({total_records} records)...")
    print("⚡ Frequency Scaled to 10 Hz (0.1s delay between events)\n")

    for i in range(1, total_records + 1):
        sensor_id = random.choice(sensors)
        
        # Telemetry metrics payload
        payload = {
            "sensor_id": sensor_id,
            "temperature": round(random.uniform(20.0, 35.0), 2),
            "humidity": round(random.uniform(40.0, 80.0), 2),
            "vibration": round(random.uniform(0.1, 1.0), 2),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        # Send event to Kafka topic
        producer.send(TOPIC, payload)

        if i % 500 == 0:
            print(f"📡 Sent {i}/{total_records} events to Kafka...")

        # Day 11 Scaling: 0.1 seconds delay (10 events/sec real-time condition)
        time.sleep(0.1)

    producer.flush()
    print("\n✅ Continuous high-frequency telemetry stream completed successfully!")

if __name__ == "__main__":
    generate_telemetry_data()