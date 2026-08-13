import json
import random
import time
from datetime import datetime, timezone

SENSOR_IDS = ["SENSOR_001", "SENSOR_002", "SENSOR_003", "SENSOR_004"]
OUTPUT_FILE = "sensor_data.json"
TOTAL_LIMIT = 50000  # Exact 50,000 records limit

def generate_sensor_data(seq_id):
    return {
        "sequence_id": seq_id,
        "sensor_id": random.choice(SENSOR_IDS),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": round(random.uniform(20.0, 45.0), 2),
        "humidity": round(random.uniform(30.0, 85.0), 2),
        "vibration": round(random.uniform(0.1, 5.0), 3)
    }

if __name__ == "__main__":
    print(f"Starting IoT Data Generation... Goal: {TOTAL_LIMIT} records.")
    start_time = time.time()
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for i in range(1, TOTAL_LIMIT + 1):
            data = generate_sensor_data(i)
            f.write(json.dumps(data) + "\n")
            
            # Prathi 5,000 records ki progress update terminal lo chupisthundhi
            if i % 5000 == 0 or i == TOTAL_LIMIT:
                print(f"Progress: {i}/{TOTAL_LIMIT} records generated ({round((i/TOTAL_LIMIT)*100)}%)...")

    end_time = time.time()
    time_taken = round(end_time - start_time, 2)
    print(f"\nSuccessfully generated {TOTAL_LIMIT} records in {OUTPUT_FILE}!")
    print(f"Total time taken: {time_taken} seconds.")