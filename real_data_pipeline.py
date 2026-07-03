import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from scipy.signal import butter, filtfilt

parser = argparse.ArgumentParser(description="DSP Pipeline: Butterworth Low-Pass Filter")

parser.add_argument("--rate", type=int, default=20, help="Sampling rate of the CSV data in Hz")
parser.add_argument("--cutoff", type=float, default=2.0, help="Target cutoff frequency in Hz")
parser.add_argument("--order", type=int, default=4, help="Filter order (steepness of the drop-off)")

args = parser.parse_args()
dataframe = pd.read_csv('sensor_data.csv')

t = dataframe['timestamp'].to_numpy()
raw_sensor_data = dataframe['raw_voltage'].to_numpy()

sampling_rate = args.rate
nyquist_freq = sampling_rate / 2
cutoff_freq = args.cutoff
filter_order = args.order

normalized_cutoff = cutoff_freq / nyquist_freq
b, a = butter(filter_order, normalized_cutoff, btype='low', analog=False)

clean_data = filtfilt(b, a, raw_sensor_data)

destroyed_noise = raw_sensor_data - clean_data

signal_power = np.mean(clean_data ** 2)
noise_power = np.mean(destroyed_noise ** 2)

snr_db = 10 * np.log10(signal_power / noise_power)

total_raw_variance = np.var(raw_sensor_data)
clean_variance = np.var(clean_data)
improvement_percent = ((total_raw_variance - clean_variance) / total_raw_variance) * 100

print("\n" + "="*40)
print(" ⚙️ DSP PIPELINE DIAGNOSTICS REPORT ⚙️")
print("="*40)
print(f"Total Samples Processed : {len(raw_sensor_data)}")
print(f"Target Cutoff Frequency : {cutoff_freq} Hz")
print(f"Signal-to-Noise Ratio   : {snr_db:.2f} dB")
print(f"Total Static Destroyed  : {improvement_percent:.1f}%")
print("="*40 + "\n")

plt.figure(figsize=(10, 4))
plt.plot(t, raw_sensor_data, label="Raw CSV Data (Messy Input)", color="red", marker='o')
plt.plot(t, clean_data, label="Filtered Output (Clean Data)", color="blue", linewidth=2, marker='x')

plt.title("Processed Industrial/Biometric CSV Pipeline")
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage")
plt.legend()
plt.grid(True)
plt.show()