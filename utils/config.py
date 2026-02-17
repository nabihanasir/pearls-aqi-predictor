from dotenv import load_dotenv
import os
load_dotenv()  
api_key = os.getenv("API_KEY")
AQICN_API_KEY = api_key
CITY = "Islamabad"
RAW_DATA_PATH = "data/raw_aqi.csv"
HOPSWORKS_API_KEY = os.getenv("HOPSWORKS_API_KEY")
HOPSWORKS_PROJECT = os.getenv("HOPSWORKS_PROJECT")

FEATURE_GROUP_NAME = "aqi_hourly_features"
FEATURE_GROUP_VERSION = 1