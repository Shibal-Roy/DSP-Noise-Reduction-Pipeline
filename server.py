from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt

app = FastAPI(title="DSP Analytics Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
)

@app.get("/process")
def process_data(rate: int = 20, cutoff: float = 2.0, order: int = 4):
    """
    This endpoint catches web requests, runs the DSP math, 
    and returns a JSON package to the dashboard.
    """
    dataframe = pd.read_csv('sensor_data.csv')
    t = dataframe['timestamp'].to_numpy()
    raw_sensor_data = dataframe['raw_voltage'].to_numpy()
    
    nyquist_freq = rate / 2
    normalized_cutoff = cutoff / nyquist_freq
    b, a = butter(order, normalized_cutoff, btype='low', analog=False)
    clean_data = filtfilt(b, a, raw_sensor_data)
    
    destroyed_noise = raw_sensor_data - clean_data
    signal_power = np.mean(clean_data ** 2)
    noise_power = np.mean(destroyed_noise ** 2)
    snr_db = float(10 * np.log10(signal_power / noise_power))
    
    total_raw_variance = np.var(raw_sensor_data)
    clean_variance = np.var(clean_data)
    improvement_percent = float(((total_raw_variance - clean_variance) / total_raw_variance) * 100)
    
    return {
        "metrics": {
            "snr_db": round(snr_db, 2),
            "improvement_percent": round(improvement_percent, 1)
        },
        "graph_data": {
            "time": t.tolist(),
            "raw": raw_sensor_data.tolist(),
            "clean": clean_data.tolist()
        }
    }