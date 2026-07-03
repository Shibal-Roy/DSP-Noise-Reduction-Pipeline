import numpy as np
import pandas as pd

print("Forging mass biometric dataset...")

sampling_rate = 20  
duration_seconds = 5 
total_samples = sampling_rate * duration_seconds

t = np.linspace(0, duration_seconds, total_samples)

true_heartbeat = np.sin(2 * np.pi * 1.5 * t)

noise = np.random.normal(0, 0.5, true_heartbeat.shape)
raw_sensor_data = true_heartbeat + noise

df = pd.DataFrame({
    'timestamp': t,
    'raw_voltage': raw_sensor_data
})

df.to_csv('sensor_data.csv', index=False)

print(f"Success! Exported {total_samples} rows of raw data to sensor_data.csv.")