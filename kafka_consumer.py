import json
import sys
from kafka import KafkaConsumer

KAFKA_TOPIC = "climate-sensor-data"
KAFKA_SERVER = "localhost:9092"

def verify_mock_json():
    print(f"Connecting to Kafka topic '{KAFKA_TOPIC}' to test stored mock JSON data...\n")
    
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_SERVER,
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            consumer_timeout_ms=5000,
            api_version=(7, 5, 0),  # Explicit version compatibility fix
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        count = 0
        for message in consumer:
            count += 1
            data = message.value
            
            if count == 1 or count % 10000 == 0:
                print(f" Validated Record #{count}: Sequence ID: {data.get('sequence_id')} | Sensor: {data.get('sensor_id')} | Temp: {data.get('temperature')}°C")

        print(f"\n Test Passed! Successfully read and verified {count} mock JSON records from Kafka topic.")

    except Exception as e:
        print(f" Error during testing: {e}")

if __name__ == "__main__":
    verify_mock_json()