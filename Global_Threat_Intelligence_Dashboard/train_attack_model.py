import sys
import os
from pathlib import Path

# ==============================================================================
# 1. BASE SYSTEM PATH RESOLUTION
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix

from utils.data_loader import load_data
from utils.preprocessing import prepare_ml_data
from config import ATTACK_MODEL_PATH, MODEL_DIR

# Define metric paths for UI performance page
FEATURE_ENCODER_PATH = MODEL_DIR / "feature_encoders.pkl"
TARGET_ENCODER_PATH = MODEL_DIR / "target_encoder.pkl"
PERFORMANCE_METRICS_PATH = MODEL_DIR / "performance_metrics.pkl"

os.makedirs(MODEL_DIR, exist_ok=True)

def train_pipeline():
    print("🚀 Initializing Threat Analytics Intelligence ML Pipeline...")
    raw_df = load_data()
    ml_data = prepare_ml_data(raw_df)
    
    target_column = "attacktype1_txt"
    feature_columns = [col for col in ml_data.columns if col != target_column]
    
    X = ml_data[feature_columns].copy()
    y = ml_data[target_column].copy()
    
    # Categorical Label Encoding
    feature_encoders = {}
    for col in X.columns:
        if X[col].dtype == 'object' or isinstance(X[col].dtype, pd.CategoricalDtype):
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            feature_encoders[col] = le
            
    target_encoder = LabelEncoder()
    y = target_encoder.fit_transform(y.astype(str))
    
    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    from xgboost import XGBClassifier
    champion_model = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, eval_metric="mlogloss")
    
    print("⏳ Training Champion XGBoost Classifier...")
    champion_model.fit(X_train, y_train)
    
    preds = champion_model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"🎯 Champion Accuracy: {acc:.4f}")
    
    # Generate Evaluation Metrics Matrix
    cm = confusion_matrix(y_test, preds)
    feature_importances = champion_model.feature_importances_.tolist()
    
    metrics_payload = {
        "accuracy": acc,
        "confusion_matrix": cm.tolist(),
        "feature_importances": feature_importances,
        "feature_names": feature_columns,
        "target_classes": target_encoder.classes_.tolist()
    }
    
    # Export artifacts to disk storage space
    print("💾 Exporting optimized deployment matrices artifacts...")
    joblib.dump(champion_model, ATTACK_MODEL_PATH)
    joblib.dump(feature_encoders, FEATURE_ENCODER_PATH)
    joblib.dump(target_encoder, TARGET_ENCODER_PATH)
    joblib.dump(metrics_payload, PERFORMANCE_METRICS_PATH)
    
    print("✅ Full Pipeline Sequence Complete. Binaries secured.")

if __name__ == "__main__":
    train_pipeline()