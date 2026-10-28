"""
SkillAdapt - AI Performance Prediction Model Training Script
Trains a regression model on student performance metrics using Scikit-learn,
evaluates performance metrics (MAE, RMSE, R-squared), and saves the trained pipeline.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
import sys
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

DATA_PATH = os.path.join(BASE_DIR, "data", "student_performance.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "performance_predictor.joblib")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")

def train_and_evaluate():
    print("=== Training SkillAdapt AI Performance Predictor ===")
    os.makedirs(MODEL_DIR, exist_ok=True)

    # 1. Check/load dataset
    if not os.path.exists(DATA_PATH):
        print(f"[!] Dataset not found at {DATA_PATH}. Triggering seed_data generator...")
        from seed_data import seed_all
        seed_all()

    df = pd.read_csv(DATA_PATH)
    print(f"[INFO] Loaded {len(df)} student training samples from {DATA_PATH}")

    feature_cols = [
        "previous_score",
        "quiz_accuracy",
        "attempts_count",
        "completion_rate",
        "study_hours"
    ]
    target_col = "future_score"

    X = df[feature_cols]
    y = df[target_col]

    # 2. Train-test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    print(f"[INFO] Training set size: {len(X_train)} | Test set size: {len(X_test)}")

    # 3. Build & fit pipeline with standard scaling and regularized Ridge regression
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("regressor", Ridge(alpha=1.0, random_state=42))
    ])

    pipeline.fit(X_train, y_train)

    # 4. Evaluate on test set
    y_pred = pipeline.predict(X_test)
    y_pred = np.clip(y_pred, 0.0, 100.0)

    mae = float(mean_absolute_error(y_test, y_pred))
    mse = float(mean_squared_error(y_test, y_pred))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_test, y_pred))

    # Coefficients for feature interpretability
    regressor = pipeline.named_steps["regressor"]
    feature_weights = dict(zip(feature_cols, [float(w) for w in regressor.coef_]))

    metrics = {
        "model_type": "Ridge Regression with StandardScaler",
        "dataset_samples": len(df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "features": feature_cols,
        "mae": round(mae, 3),
        "mse": round(mse, 3),
        "rmse": round(rmse, 3),
        "r2_score": round(r2, 4),
        "feature_weights": {k: round(v, 4) for k, v in feature_weights.items()},
        "intercept": round(float(regressor.intercept_), 4)
    }

    # 5. Save model and metrics
    joblib.dump(pipeline, MODEL_PATH)
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("\n--- Model Evaluation Results ---")
    print(f"Mean Absolute Error (MAE): {metrics['mae']:.3f} points")
    print(f"Root Mean Squared Error (RMSE): {metrics['rmse']:.3f} points")
    print(f"Coefficient of Determination (R^2): {metrics['r2_score']:.4f}")
    print("\nNormalized Feature Importance Weights:")
    for feat, weight in metrics["feature_weights"].items():
        print(f"  * {feat:18s}: {weight:+.4f}")
    print(f"\n[OK] Model serialized to: {MODEL_PATH}")
    print(f"[OK] Metrics saved to: {METRICS_PATH}")
    return metrics

if __name__ == "__main__":
    train_and_evaluate()
