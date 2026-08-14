import json
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError

KAFKA_TOPIC = "climate-sensor-data"
KAFKA_SERVER = "localhost:9092"
DATA_FILE = "sensor_data.json"

def create_kafka_producer():
    """Retries connection until Kafka broker is available."""
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_SERVER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("Connected to Kafka Broker successfully!")
            return producer
        except Exception as e:
            print(f"Waiting for Kafka Broker... Error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    producer = create_kafka_producer()
    print(f"Streaming data from '{DATA_FILE}' to Kafka topic '{KAFKA_TOPIC}'...\n")

    try:
        with open(DATA_FILE, "r") as f:
            count = 0
            for line in f:
                if line.strip():
                    payload = json.loads(line.strip())
                    producer.send(KAFKA_TOPIC, value=payload)
                    count += 1
                    
                    if count % 1000 == 0:
                        print(f"Pushed {count} records to Topic: {KAFKA_TOPIC}")
                        producer.flush()  # Forces push to broker batch-wise
                        time.sleep(0.2)

            producer.flush()
            print(f"\nCompleted! Total {count} records streamed into Kafka topic '{KAFKA_TOPIC}'.")

    except FileNotFoundError:
        print(f"Error: {DATA_FILE} not found. Ensure Day-2 file exists!")
    except KeyboardInterrupt:
        print("\nStreaming paused manually.")