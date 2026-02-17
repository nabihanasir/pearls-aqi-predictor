


# Islamabad AQI Forecasting System

### End-to-End ML Pipeline with Feature Store, Model Registry, CI/CD, and Interactive Dashboard


## Overview

This project is a complete end-to-end Air Quality Index (AQI) forecasting system built for Islamabad. The system predicts AQI for the next:

* **1 hour**
* **24 hours**
* **72 hours**

The objective was not just to train a model, but to design a production-oriented machine learning system with:

* Automated feature ingestion
* Daily retraining
* Model registry integration
* CI/CD automation
* Interactive dashboard
* Model explainability (SHAP)
* Hazard alert logic

The final system reflects real-world ML engineering practices rather than a notebook-based experiment.



## System Architecture

```
Data Sources
     ↓
Feature Engineering
     ↓
Hopsworks Feature Store
     ↓
Daily Model Training (GitHub Actions)
     ↓
Model Registry
     ↓
Streamlit Dashboard
     ↓
Real-Time Predictions + Alerts
```

Automation Layer: **GitHub Actions**

* Feature pipeline: Hourly
* Training pipeline: Daily



## Tech Stack

* Python
* Streamlit (dashboard)
* scikit-learn
* XGBoost
* Hopsworks Feature Store
* Hopsworks Model Registry
* SHAP (model explainability)
* GitHub Actions (CI/CD)
* Plotly + Matplotlib



## Project Structure

```
.
├── src/
│   ├── app.py
│   ├── train_model.py
│   ├── predict.py
│   ├── feature_pipeline.py
│   └── utils/
│       └── hopsworks_utils.py
├── models/
├── .github/
│   └── workflows/
│       ├── feature_pipeline.yml
│       └── training_pipeline.yml
├── requirements.txt
└── README.md
```



## Feature Engineering

### Features Used

* `pm25`
* `pm10`
* `no2`
* `so2`
* `co`
* `hour`
* `day`
* `month`
* `weekday`
* `aqi_change_rate`
* `aqi_roll_3h`

### Targets

* `target_aqi_1h`
* `target_aqi_24h`
* `target_aqi_72h`

The feature pipeline:

* Fetches latest environmental data
* Computes rolling statistics
* Computes change rates
* Updates Hopsworks Feature Store

This pipeline runs automatically **every hour** via GitHub Actions.



## Model Development

Multiple forecasting models were implemented and compared:

* `RandomForestRegressor`
* `XGBoost` (via `MultiOutputRegressor`)
* `GradientBoostingRegressor`

### Training Process

1. Pulls data from Feature Store
2. Drops incomplete target rows
3. Applies time-series split (no shuffle)
4. Trains multiple models
5. Compares MAE and R²
6. Selects best-performing model
7. Registers model in Model Registry

Training runs automatically **every day** via CI/CD.



## Dashboard

Built using **Streamlit**.

### Features

* Forecast metrics (1h, 24h, 72h)
* Interactive AQI trend visualization
* SHAP-based feature importance
* Health recommendations based on AQI thresholds
* Hazard alerts (AQI ≥ 300)

The dashboard dynamically loads:

* Latest features from Feature Store
* Latest registered model

This ensures prediction consistency and real-time relevance.



## CI/CD Automation

Two GitHub Actions workflows were implemented.

### 1. Hourly Feature Pipeline

Runs every hour:

* Installs dependencies
* Connects securely to Hopsworks
* Executes `feature_pipeline.py`
* Updates Feature Store



### 2. Daily Training Pipeline

Runs every day:

* Installs dependencies
* Connects using GitHub Secrets
* Executes `train_model.py`
* Registers best model in Model Registry

This creates a fully automated ML lifecycle.



## Key Engineering Challenges Faced

### 1. Model Path Resolution Issue

**Problem:**
Streamlit could not find `aqi_model.pkl`.

**Root Cause:**
The model was saved in the project root while Streamlit was executed from the `src/` directory, causing relative path mismatch.

**Fix:**
Replaced static relative paths with dynamic base directory resolution:

```python
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
```

This ensured consistent path resolution regardless of execution context.



### 2. Matplotlib Plots Not Rendering in Streamlit

**Problem:**
`plt.show()` did not render plots inside Streamlit.

**Fix:**
Replaced with:

```python
st.pyplot(fig)
```

Streamlit requires explicit rendering of matplotlib figures.



### 3. Feature Store Connection in CI

**Problem:**
Training failed in GitHub Actions due to missing credentials.

**Fix:**
Configured GitHub Secrets:

* `HOPSWORKS_API_KEY`
* `HOPSWORKS_PROJECT`

Accessed securely via environment variables.

This made the pipeline secure and reproducible.



### 4. Scheduled Workflows Not Triggering

**Observation:**
GitHub scheduled workflows operate in UTC and only run on the default branch.

**Resolution:**
Ensured workflow files were inside `.github/workflows/` and manually triggered using `workflow_dispatch` during testing.



## What This Project Demonstrates

* End-to-end ML system design
* Feature Store integration
* Model Registry usage
* Automated retraining
* CI/CD integration
* Multi-model benchmarking
* Explainability integration
* Alert system design
* Production debugging and system thinking

This project reflects the ability to move beyond experimentation and build structured, automated, production-aware machine learning systems.



## Future Improvements

* Add LSTM model for deep learning comparison
* Add data drift detection
* Add model performance monitoring
* Containerize with Docker
* Add REST API using FastAPI



## Final Deliverables

* End-to-end AQI prediction system
* Automated feature + training pipelines
* Interactive dashboard
* CI/CD workflows
* Documented engineering process



