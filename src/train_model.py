import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from utils.hopsworks_utils import get_feature_store, get_model_registry, get_feature_group_name

# Features based on your Islamabad dataset
FEATURES = [
    "pm25", "pm10", "no2", "so2", "co", 
    "hour", "day", "month", "weekday",
    "aqi_change_rate", "aqi_roll_3h"
]

# The three time horizons for Islamabad
TARGETS = ["target_aqi_1h", "target_aqi_24h", "target_aqi_72h"]

def train():
    # 1. Connect to Hopsworks
    fs = get_feature_store()
    fg_name, fg_version = get_feature_group_name()
    fg = fs.get_feature_group(fg_name, version=fg_version)

    # 2. Read and Prep Data
    print("Reading data from Feature Store...")
    df = fg.read()
    if df is None or df.empty:
        raise ValueError("Feature Group is empty!")
    
    # Drop rows without targets (the last 3 days of data)
    df = df.dropna(subset=TARGETS)

    X = df[FEATURES]
    y = df[TARGETS]

    # Time-series split (no shuffle!)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    # 3. Define the Challengers
    models_to_test = {
        "RandomForest": RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
        "XGBoost": MultiOutputRegressor(XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=6)),
        "GradientBoosting": MultiOutputRegressor(GradientBoostingRegressor(n_estimators=100, learning_rate=0.05))
    }

    best_model = None
    best_mae = float("inf")
    best_model_name = ""
    performance_metrics = {}

    # 4. The Model Battle
    print("\n--- ⚔️ Starting Model Battle ⚔️ ---")
    for name, model in models_to_test.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        
        # Calculate MAE for all 3 targets averaged
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        
        print(f"{name:16} | Avg MAE: {mae:.2f} | Avg R2: {r2:.2f}")
        
        if mae < best_mae:
            best_mae = mae
            best_model = model
            best_model_name = name
            performance_metrics = {
                "avg_mae": round(mae, 2),
                "avg_r2": round(r2, 2)
            }

    print(f"\n🏆 Champion: {best_model_name}")

    # 5. Save and Register
    os.makedirs("models", exist_ok=True)
    model_path = "models/aqi_model.pkl"
    joblib.dump(best_model, model_path)

    mr = get_model_registry()
    model_meta = mr.sklearn.create_model(
        name="aqi_predictor",
        metrics=performance_metrics,
        description=f"Multi-output {best_model_name} for Islamabad 3-day forecast."
    )
    model_meta.save(model_path)
    print(f"✅ Registered {best_model_name} in Model Registry.")

if __name__ == "__main__":
    train()