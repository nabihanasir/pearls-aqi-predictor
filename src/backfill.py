import requests
import pandas as pd
from utils.config import RAW_DATA_PATH

def backfill_islamabad():
    # Islamabad Coordinates
    lat, lon = 33.72148, 73.04329
    
    # Open-Meteo Air Quality API (No API Key required for historical)
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=pm2_5,pm10,nitrogen_dioxide,sulphur_dioxide,carbon_monoxide&past_days=30"
    
    print(f"Fetching 30 days of data for Islamabad...")
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error fetching data from Open-Meteo")
        return

    data = response.json()["hourly"]
    df = pd.DataFrame(data)

    # Rename columns to match your Hopsworks schema
    df = df.rename(columns={
        "time": "timestamp",
        "pm2_5": "pm25",
        "nitrogen_dioxide": "no2",
        "sulphur_dioxide": "so2",
        "carbon_monoxide": "co"
    })

    # Add a simplified AQI column (Proxy calculation)
    # PM2.5 is the main driver of AQI in Islamabad
    df["aqi"] = df["pm25"] * 1.5 
    
    # Ensure timestamp is correct format
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Save to your raw data path
    df.to_csv(RAW_DATA_PATH, index=False)
    print(f"Done! Saved {len(df)} rows to {RAW_DATA_PATH}")

if __name__ == "__main__":
    backfill_islamabad()