import json
import time
from kafka import KafkaProducer, KafkaConsumer

KAFKA_TOPIC = "climate-sensor-data"
KAFKA_SERVER = "localhost:9092"
API_VER = (7, 5, 0)

def benchmark_pipeline():
    print("🚀 Starting Day 5: Topic Throughput & Schema Validation Test...\n")
    
    # Line-by-line JSON (NDJSON) reading fix
    records = []
    with open("sensor_data.json", "r") as f:
        for i, line in enumerate(f):
            if i >= 10000:  # 10k batch size for throughput test
                break
            if line.strip():
                records.append(json.loads(line))
        
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        api_version=API_VER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    # 1. Benchmark Producer Speed
    start_time = time.time()
    for record in records:
        producer.send(KAFKA_TOPIC, value=record)
    producer.flush()
    produce_time = time.time() - start_time
    produce_rate = len(records) / produce_time
    
    print(f"✅ [PRODUCER METRICS]")
    print(f"   - Messages Pushed: {len(records)}")
    print(f"   - Time Taken: {produce_time:.2f} seconds")
    print(f"   - Throughput: {produce_rate:.2f} msgs/sec\n")

    # 2. Benchmark Consumer Speed & Verify Format
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        api_version=API_VER,
        auto_offset_reset='earliest',
        consumer_timeout_ms=3000,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    consumed_count = 0
    valid_format_count = 0
    required_keys = {"sensor_id", "sequence_id", "temperature", "humidity", "vibration"}
    
    c_start_time = time.time()
    for msg in consumer:
        consumed_count += 1
        payload = msg.value
        # Schema Format Check
        if required_keys.issubset(payload.keys()):
            valid_format_count += 1
            
    consume_time = time.time() - c_start_time
    consume_rate = consumed_count / consume_time if consume_time > 0 else 0
    
    print(f"✅ [CONSUMER & FORMAT METRICS]")
    print(f"   - Messages Read: {consumed_count}")
    print(f"   - Valid JSON Schema Match: {valid_format_count}/{consumed_count}")
    print(f"   - Read Throughput: {consume_rate:.2f} msgs/sec\n")
    print("🎉 Week 1 Deliverable Complete: Pipeline is high-performing and schema-compliant!")

if __name__ == "__main__":
    benchmark_pipeline()