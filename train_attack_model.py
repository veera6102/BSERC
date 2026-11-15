import sys
import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
from xgboost import XGBClassifier

from utils.data_loader import load_data
from utils.preprocessing import prepare_ml_data
from config import (
    ATTACK_MODEL_PATH,
    FEATURE_ENCODER_PATH,
    TARGET_ENCODER_PATH,
    PERFORMANCE_METRICS_PATH,
    METRICS_JSON_PATH,
    MODEL_DIR,
)

os.makedirs(MODEL_DIR, exist_ok=True)


def train_pipeline():
    print("🚀 Initializing Threat Analytics Intelligence ML Pipeline...")
    raw_df = load_data()
    ml_data = prepare_ml_data(raw_df)

    target_column = "attacktype1_txt"
    feature_columns = [col for col in ml_data.columns if col != target_column]

    # Ensure each target class has at least 2 records for stratified splitting
    class_counts = ml_data[target_column].value_counts()
    valid_classes = class_counts[class_counts >= 2].index
    ml_data = ml_data[ml_data[target_column].isin(valid_classes)].copy()

    X = ml_data[feature_columns].copy()
    y = ml_data[target_column].copy()

    feature_encoders = {}
    for col in X.columns:
        if X[col].dtype == "object" or isinstance(X[col].dtype, pd.CategoricalDtype) or pd.api.types.is_string_dtype(X[col]):
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            feature_encoders[col] = le
        else:
            X[col] = pd.to_numeric(X[col], errors="coerce").fillna(0)

    target_encoder = LabelEncoder()
    y_encoded = target_encoder.fit_transform(y.astype(str))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    champion_model = XGBClassifier(
        n_estimators=120,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        eval_metric="mlogloss",
    )

    print("⏳ Training Champion XGBoost Classifier...")
    champion_model.fit(X_train, y_train)

    preds = champion_model.predict(X_test)
    acc = float(accuracy_score(y_test, preds))
    prec = float(precision_score(y_test, preds, average="weighted", zero_division=0))
    rec = float(recall_score(y_test, preds, average="weighted", zero_division=0))
    f1 = float(f1_score(y_test, preds, average="weighted", zero_division=0))
    print(f"🎯 Champion Accuracy: {acc:.4f} | F1: {f1:.4f}")

    labels_idx = list(range(len(target_encoder.classes_)))
    cm = confusion_matrix(y_test, preds, labels=labels_idx)
    feature_importances = [float(v) for v in champion_model.feature_importances_]
    fi_dict = {
        col: round(float(imp), 4)
        for col, imp in zip(feature_columns, feature_importances)
    }

    report_dict = classification_report(
        y_test,
        preds,
        labels=labels_idx,
        target_names=target_encoder.classes_.tolist(),
        output_dict=True,
        zero_division=0,
    )

    metrics_payload = {
        "best_model": "XGBoost Multi-Class Tactical Classifier",
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": cm.tolist(),
        "feature_importances": feature_importances,
        "feature_importances_map": fi_dict,
        "feature_names": feature_columns,
        "target_classes": target_encoder.classes_.tolist(),
        "per_class_report": report_dict,
    }

    json_metrics = {
        "best_model": "XGBoost Multi-Class Classifier",
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "feature_importances": fi_dict,
        "target_classes": target_encoder.classes_.tolist(),
        "confusion_matrix": cm.tolist(),
    }

    print("💾 Exporting optimized deployment artifacts...")
    joblib.dump(champion_model, ATTACK_MODEL_PATH)
    joblib.dump(feature_encoders, FEATURE_ENCODER_PATH)
    joblib.dump(target_encoder, TARGET_ENCODER_PATH)
    joblib.dump(metrics_payload, PERFORMANCE_METRICS_PATH)

    with open(METRICS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(json_metrics, f, indent=4)

    print("✅ Full Pipeline Sequence Complete. Binaries & metrics secured.")


if __name__ == "__main__":
    train_pipeline()
