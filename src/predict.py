import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import joblib
import pandas as pd
from utils.hopsworks_utils import get_feature_store, get_feature_group_name
# Must match the FEATURES used in train_model.py exactly
FEATURES = [
    "pm25", "pm10", "no2", "so2", "co", 
    "hour", "day", "month", "weekday",
    "aqi_change_rate", "aqi_roll_3h"
]

def predict_three_days():
    # 1. Connect and get the most recent data point
    fs = get_feature_store()
    fg_name, fg_version = get_feature_group_name()
    fg = fs.get_feature_group(fg_name, version=fg_version)

    # We read the latest data. Note: 'timestamp' or 'datetime' depends on your FG
    df = fg.read().sort_values("timestamp")
    latest_data = df.iloc[-1:][FEATURES]
    last_time = df.iloc[-1]["timestamp"]

  
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    model_path = os.path.join(BASE_DIR, "models", "aqi_model.pkl")
    model = joblib.load(model_path)
    
    # 3. Predict
    predictions = model.predict(latest_data)[0] # Returns [1h, 24h, 72h]

    print(f"\n--- Islamabad AQI Forecast (Based on data from {last_time}) ---")
    print(f"Next Hour Prediction:      {predictions[0]:.2f}")
    print(f"Tomorrow (24h) Prediction: {predictions[1]:.2f}")
    print(f"Day 3 (72h) Prediction:    {predictions[2]:.2f}")
    
    return predictions

if __name__ == "__main__":
    predict_three_days()