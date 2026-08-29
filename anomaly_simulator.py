import json
import random
import time
from datetime import datetime

OUTPUT_FILE = "sensor_data_spiked.json"
NUM_RECORDS = 50000  # Refined 50k dataset with injected anomalies

def generate_spiked_telemetry():
    print("⚡ Generating IoT telemetry data with injected spikes & anomalies...")
    
    sensors = [f"SENSOR_00{i}" for i in range(1, 6)]
    records = []
    
    for seq in range(1, NUM_RECORDS + 1):
        sensor_id = random.choice(sensors)
        
        # Base Normal Values
        temp = round(random.uniform(20.0, 32.0), 2)
        humidity = round(random.uniform(40.0, 65.0), 2)
        vibration = round(random.uniform(0.01, 0.05), 4)
        is_spike = False
        
        # 5% Chance to inject extreme Temperature/Humidity/Vibration Spikes
        if random.random() < 0.05:  
            is_spike = True
            spike_type = random.choice(["TEMP_HEATWAVE", "HUMIDITY_DROP", "CRITICAL_VIBRATION"])
            
            if spike_type == "TEMP_HEATWAVE":
                temp = round(random.uniform(55.0, 85.0), 2)   # Extreme Heat Spike (55°C - 85°C)
            elif spike_type == "HUMIDITY_DROP":
                humidity = round(random.uniform(5.0, 15.0), 2) # Extreme Drop (5% - 15%)
            elif spike_type == "CRITICAL_VIBRATION":
                vibration = round(random.uniform(0.5, 1.8), 4) # Machine Failure Spike
                
        record = {
            "sequence_id": seq,
            "sensor_id": sensor_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "temperature": temp,
            "humidity": humidity,
            "vibration": vibration,
            "is_anomaly": is_spike
        }
        records.append(record)
        
    # Write to JSON Lines file
    with open(OUTPUT_FILE, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
            
    print(f"✅ Generated {NUM_RECORDS} records in '{OUTPUT_FILE}' with ~5% injected spikes!")

if __name__ == "__main__":
    generate_spiked_telemetry()