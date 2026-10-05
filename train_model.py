import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

print("1. Loading battery dataset...")
df = pd.read_csv("battery_data.csv")

# Input features (Voltage, Minutes Elapsed, Sag Rate)
X = df[["voltage_v", "time_elapsed_min", "sag_rate_mv_min"]]

# Outputs to predict (Remaining Minutes until 3.0V cutoff, and Health %)
y_runtime = df["remaining_runtime_min"]
y_soh = df["soh_percent"]

# Split data: 80% for training, 20% for testing
X_train, X_test, y_rt_train, y_rt_test, y_soh_train, y_soh_test = (
    train_test_split(X, y_runtime, y_soh, test_size=0.2, random_state=42)
)

print("2. Training Machine Learning Regressors...")
# Model 1: Backup Runtime Predictor
runtime_model = RandomForestRegressor(
    n_estimators=100, max_depth=12, random_state=42
)
runtime_model.fit(X_train, y_rt_train)

# Model 2: Battery Health (SoH %) Predictor
soh_model = RandomForestRegressor(
    n_estimators=100, max_depth=8, random_state=42
)
soh_model.fit(X_train, y_soh_train)

# Evaluate accuracy
rt_pred = runtime_model.predict(X_test)
print(f"Model Accuracy (R^2 Score): {r2_score(y_rt_test, rt_pred)*100:.2f}%")
print(f"Average Error: {mean_absolute_error(y_rt_test, rt_pred):.2f} minutes")

# Save the trained model to disk
joblib.dump(
    {"runtime_model": runtime_model, "soh_model": soh_model},
    "battery_model.pkl",
)
print("SUCCESS: Model saved to 'battery_model.pkl'!")