import json
import time
from kafka import KafkaConsumer

KAFKA_SERVER = "localhost:9092"
TOPICS = ["climate-sensor-data", "climate-alerts"]

def run_multi_topic_consumer():
    print(f"📡 Subscribing to topics: {TOPICS}...")
    
    consumer = KafkaConsumer(
        *TOPICS,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="multi-topic-monitor-group",
        api_version=(2, 5, 0)
    )

    print("🚀 Listening for continuous multi-topic telemetry & alerts...\n")
    
    try:
        for msg in consumer:
            payload = msg.value
            topic = msg.topic
            
            if topic == "climate-alerts":
                print(f"⚠️ [ALERT TOPIC] Anomaly Detected! Sensor: {payload.get('sensor_id')} | Temp: {payload.get('temperature')}°C | Humidity: {payload.get('humidity')}%")
            else:
                print(f"📊 [TELEMETRY TOPIC] Seq: {payload.get('sequence_id')} | Sensor: {payload.get('sensor_id')} | Temp: {payload.get('temperature')}°C")

    except KeyboardInterrupt:
        print("\n⏹️ Stopping multi-topic consumer.")
    finally:
        consumer.close()

if __name__ == "__main__":
    run_multi_topic_consumer()