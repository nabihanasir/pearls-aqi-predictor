import pandas as pd
from utils.config import RAW_DATA_PATH


def build_features(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    # Time features
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.day
    df["month"] = df["timestamp"].dt.month
    df["weekday"] = df["timestamp"].dt.weekday

    # Derived features
    df["aqi_change_rate"] = df["aqi"].diff()
    df["aqi_roll_3h"] = df["aqi"].rolling(3).mean()

    # Targets
    df["target_aqi_1h"] = df["aqi"].shift(-1)
    df["target_aqi_24h"] = df["aqi"].shift(-24)
    df["target_aqi_72h"] = df["aqi"].shift(-72)

    df = df.dropna()
    return df


if __name__ == "__main__":
    raw_df = pd.read_csv(RAW_DATA_PATH)
    feature_df = build_features(raw_df)
    print(feature_df.head())
    print(f"Feature rows: {len(feature_df)}")
