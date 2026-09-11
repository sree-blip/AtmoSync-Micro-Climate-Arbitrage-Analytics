import json
import time
import os
from datetime import datetime, timezone
from kafka import KafkaConsumer

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9092")
TOPIC = "climate-sensor-data"

def measure_pipeline_latency():
    print("⏱️ Starting Day 10 Pipeline Latency Testing...")
    
    # Updated: auto_offset_reset='earliest' and consumer_timeout_ms added
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        consumer_timeout_ms=5000,  # 5 sec timeout to avoid infinite freeze
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    latencies = []
    sample_count = 100

    print(f"📊 Sampling end-to-end latency for target records...\n")

    try:
        for message in consumer:
            payload = message.value
            
            # Extract timestamp payload
            event_time_str = payload.get("timestamp")
            if event_time_str:
                try:
                    event_time = datetime.fromisoformat(event_time_str.replace("Z", "+00:00"))
                    current_time = datetime.now(timezone.utc)
                    
                    # End-to-End Latency calculation (milliseconds)
                    latency_ms = abs((current_time - event_time).total_seconds() * 1000.0)
                    latencies.append(latency_ms)

                    if len(latencies) % 20 == 0:
                        print(f"[{len(latencies)}/{sample_count}] Processed Record Latency: {latency_ms:.2f} ms")

                except Exception:
                    continue

            if len(latencies) >= sample_count:
                break
    except Exception as e:
        print(f"\n⚠️ Stream collection ended: {e}")

    if not latencies:
        print("❌ No messages retrieved. Ensuring producer is publishing active metrics...")
        return

    # Metrics Calculation
    avg_latency = sum(latencies) / len(latencies)
    min_latency = min(latencies)
    max_latency = max(latencies)

    print("\n==============================================")
    print("🚀 DAY 10 PIPELINE LATENCY TESTING RESULTS")
    print("==============================================")
    print(f"Total Samples Tested : {len(latencies)}")
    print(f"Minimum Latency      : {min_latency:.2f} ms")
    print(f"Maximum Latency      : {max_latency:.2f} ms")
    print(f"Average End-to-End   : {avg_latency:.2f} ms")
    print("==============================================\n")

if __name__ == "__main__":
    measure_pipeline_latency()