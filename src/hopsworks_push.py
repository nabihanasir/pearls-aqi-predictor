import pandas as pd
import hopsworks
from utils.config import (
    RAW_DATA_PATH,
    HOPSWORKS_API_KEY,
    HOPSWORKS_PROJECT,
    FEATURE_GROUP_NAME,
    FEATURE_GROUP_VERSION,
)
from src.feature_pipeline import build_features


project = hopsworks.login(
    project=HOPSWORKS_PROJECT,
    api_key_value=HOPSWORKS_API_KEY
)
fs = project.get_feature_store()

fg = fs.get_or_create_feature_group(
    name=FEATURE_GROUP_NAME,
    version=FEATURE_GROUP_VERSION,
    primary_key=["timestamp"],
    event_time="timestamp",
    description="Hourly AQI features and targets"
)

raw_df = pd.read_csv(RAW_DATA_PATH)
feature_df = build_features(raw_df)

fg.insert(feature_df)
print("Features pushed to Hopsworks")
