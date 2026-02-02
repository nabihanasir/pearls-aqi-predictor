from dotenv import load_dotenv
import os
load_dotenv()  
api_key = os.getenv("API_KEY")
AQICN_API_KEY = api_key
CITY = "Islamabad"
RAW_DATA_PATH = "data/raw_aqi.csv"

