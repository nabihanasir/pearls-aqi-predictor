import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import streamlit as st
import plotly.express as px
from predict import predict_three_days

st.set_page_config(page_title="Islamabad AQI Predictor", layout="wide", page_icon="🌍")

# Custom CSS for better metric visibility
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 45px; }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.title("🌍 Islamabad 3-Day AQI Forecast")
st.markdown("Real-time air quality forecasting for Islamabad using **XGBoost/RandomForest** models and **Hopsworks** Feature Store.")

# --- Sidebar ---

st.sidebar.header("System Status")
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
model_exists = os.path.exists(os.path.join(BASE_DIR, "models", "aqi_model.pkl"))
if model_exists:
    st.sidebar.success("✅ Model Loaded")
else:
    st.sidebar.error("❌ Model Missing (Run train_model.py)")

st.sidebar.divider()
st.sidebar.info("Data: Open-Meteo & AQICN\n\nPlatform: Hopsworks AI")

# --- Main Logic ---
if st.button("Generate Forecast", type="primary"):
    if not model_exists:
        st.error("Cannot generate forecast: `aqi_model.pkl` not found in the `models/` directory.")
    else:
        try:
            with st.spinner("Connecting to Hopsworks and analyzing latest trends..."):
                # Fetch predictions from your existing script
                predictions = predict_three_days()
                
                # 1. Metric Display
                st.subheader("Current Forecasts")
                col1, col2, col3 = st.columns(3)
                
                # We use delta to show it's a prediction relative to "now"
                col1.metric("Next Hour", f"{predictions[0]:.1f} AQI")
                col2.metric("Tomorrow (24h)", f"{predictions[1]:.1f} AQI")
                col3.metric("Day 3 (72h)", f"{predictions[2]:.1f} AQI")

                # 2. Visual Trend Chart
                st.divider()
                st.subheader("📈 Forecast Trend")
                
                chart_data = pd.DataFrame({
                    "Timeframe": ["1 Hour", "24 Hours", "72 Hours"],
                    "Predicted AQI": predictions
                })
                
                fig = px.line(
                    chart_data, 
                    x="Timeframe", 
                    y="Predicted AQI", 
                    markers=True,
                    template="plotly_dark",
                    labels={"Predicted AQI": "AQI Level"}
                )
                
                # Add a reference line for "Unhealthy" threshold (150)
                fig.add_hline(y=150, line_dash="dot", line_color="orange", annotation_text="Unhealthy Threshold")
                fig.update_layout(yaxis_range=[0, max(max(predictions) + 40, 200)])
                
                st.plotly_chart(fig, use_container_width=True)

                # 3. Health Advice Logic
                st.divider()
                max_aqi = max(predictions)
                st.subheader("🛡️ Health Recommendation")
                
                if max_aqi >= 300:
                    st.error("### **Hazardous**\nSerious risk for everyone. Avoid all outdoor physical activities. Wear N95 masks if transit is necessary.")
                elif max_aqi >= 200:
                    st.warning("### **Very Unhealthy**\nSignificant health risk. Stay indoors and keep windows closed.")
                elif max_aqi >= 150:
                    st.warning("### **Unhealthy**\nSensitive groups (children, elderly) should avoid outdoor exertion. General public should limit time outside.")
                elif max_aqi >= 100:
                    st.info("### **Moderate**\nAir quality is acceptable; however, sensitive individuals should monitor symptoms like coughing or shortness of breath.")
                else:
                    st.success("### **Good**\nAir quality is satisfactory. It's a great time for outdoor activities in Islamabad!")

        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")

else:
    st.info("Click the button above to fetch the latest data and generate a 3-day forecast.")