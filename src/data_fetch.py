import requests
import pandas as pd
from datetime import datetime
from utils.config import AQICN_API_KEY, CITY, RAW_DATA_PATH


def fetch_aqi():
    url = f"https://api.waqi.info/feed/{CITY}/?token={AQICN_API_KEY}"
    response = requests.get(url)
    data = response.json()

    iaqi = data["data"]["iaqi"]

    record = {
        "datetime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "aqi": data["data"]["aqi"],
        "pm25": iaqi.get("pm25", {}).get("v"),
        "pm10": iaqi.get("pm10", {}).get("v"),
        "no2": iaqi.get("no2", {}).get("v"),
        "o3": iaqi.get("o3", {}).get("v"),
        "so2": iaqi.get("so2", {}).get("v"),
        "co": iaqi.get("co", {}).get("v"),
    }

    return record


if __name__ == "__main__":
    record = fetch_aqi()
    df = pd.DataFrame([record])

    try:
        old = pd.read_csv(RAW_DATA_PATH)
        df = pd.concat([old, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_csv(RAW_DATA_PATH, index=False)
    print("Hourly AQI data saved")
