import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

t = np.linspace(0, 1, 1000)
true_signal = 5 * np.sin(2 * np.pi * 1.5 * t)

noise = np.random.normal(0, 0.2, true_signal.shape)

raw_sensor_data = true_signal + noise

sampling_rate = 1000  
nyquist_freq = sampling_rate / 2
cutoff_freq = 5.0    
filter_order = 4      

normalized_cutoff = cutoff_freq / nyquist_freq

b, a = butter(filter_order, normalized_cutoff, btype='low', analog=False)

clean_data = filtfilt(b, a, raw_sensor_data)

plt.figure(figsize=(10, 4))

plt.plot(t, raw_sensor_data, label="Raw Sensor Data (Interference)", color="red", alpha=0.6)

plt.plot(t, true_signal, label="True Signal (Target)", color="black", linewidth=2)

plt.plot(t, clean_data, label="Filtered Output (Butterworth)", color="blue", linewidth=3)
plt.title("Simulated Industrial/Biological Sensor Data")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)

plt.show()