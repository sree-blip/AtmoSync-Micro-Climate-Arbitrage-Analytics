import os
import json
import time
import random
from datetime import datetime, timezone
from kafka import KafkaProducer

KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'localhost:9092')
TOPIC_SENSOR = 'climate-sensor-data'
TOPIC_ALERTS = 'climate-alerts'
TOTAL_RECORDS = 50000  # Exact 50,000 limit

def generate_live_record(sequence_id):
    """Generates a single live telemetry record with ~5% anomaly chance."""
    is_anomaly = random.random() < 0.05
    anomaly_type = None

    temp = round(random.uniform(20.0, 30.0), 2)
    humidity = round(random.uniform(40.0, 70.0), 2)
    vibration = round(random.uniform(0.1, 0.5), 2)

    if is_anomaly:
        anomaly_choice = random.choice(['heatwave', 'humidity_drop', 'vibration_spike'])
        if anomaly_choice == 'heatwave':
            temp = round(random.uniform(45.0, 55.0), 2)
            anomaly_type = 'Heatwave Spike'
        elif anomaly_choice == 'humidity_drop':
            humidity = round(random.uniform(5.0, 15.0), 2)
            anomaly_type = 'Humidity Drop'
        elif anomaly_choice == 'vibration_spike':
            vibration = round(random.uniform(3.5, 8.0), 2)
            anomaly_type = 'Vibration Spike'

    return {
        "sequence_id": sequence_id,
        "sensor_id": f"SENSOR_{random.randint(101, 105)}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": temp,
        "humidity": humidity,
        "vibration": vibration,
        "is_anomaly": is_anomaly,
        "anomaly_type": anomaly_type
    }

def create_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_SERVER,
                api_version=(2, 8, 0),
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print(f"✅ Successfully connected to Kafka Broker at {KAFKA_SERVER}")
            return producer
        except Exception as e:
            print(f"Waiting for Kafka Broker ({KAFKA_SERVER})... Error: {e}")
            time.sleep(3)

def start_streaming():
    producer = create_kafka_producer()
    print(f"🚀 Telemetry Batch Streaming Started (Target: {TOTAL_RECORDS} records)...")
    
    # 50,000 records exact loop
    for sequence_id in range(1, TOTAL_RECORDS + 1):
        record = generate_live_record(sequence_id)
        
        # Standard Telemetry Stream
        producer.send(TOPIC_SENSOR, value=record)
        
        # High-Priority Alert Stream
        if record.get("is_anomaly", False):
            producer.send(TOPIC_ALERTS, value=record)

        # Progress tracker print every 5000 records
        if sequence_id % 5000 == 0:
            print(f"📊 Processed {sequence_id}/{TOTAL_RECORDS} messages...")

    # Flush all remaining buffered messages to Kafka before exiting
    producer.flush()
    print(f"🎉 Successfully streamed all {TOTAL_RECORDS} records! Producer process complete.")

if __name__ == "__main__":
    start_streaming()