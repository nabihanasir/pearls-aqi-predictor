import requests
import pandas as pd
from datetime import datetime
from utils.config import AQICN_API_KEY, CITY, RAW_DATA_PATH

def fetch_aqi():
    url = f"https://api.waqi.info/feed/{CITY}/?token={AQICN_API_KEY}"
    response = requests.get(url, timeout=10)
    data = response.json()

    iaqi = data["data"]["iaqi"]

    row = {
        "datetime": datetime.now(),
        "aqi": data["data"]["aqi"],
        "pm25": iaqi.get("pm25", {}).get("v"),
        "pm10": iaqi.get("pm10", {}).get("v"),
        "no2": iaqi.get("no2", {}).get("v"),
        "so2": iaqi.get("so2", {}).get("v"),
        "temp": iaqi.get("t", {}).get("v"),
        "humidity": iaqi.get("h", {}).get("v"),
    }

    return pd.DataFrame([row])

if __name__ == "__main__":
    df = fetch_aqi()

    try:
        old = pd.read_csv(RAW_DATA_PATH)
        df = pd.concat([old, df])
    except FileNotFoundError:
        pass

    df.to_csv(RAW_DATA_PATH, index=False)
    print("AQI data fetched and saved")
