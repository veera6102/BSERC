import sys
import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from config import METRICS_JSON_PATH, PERFORMANCE_METRICS_PATH
from utils.dashboard_metrics import render_page_header, render_kpi_card, render_footer

st.set_page_config(
    page_title="Model Performance Metrics | Threat Intelligence",
    page_icon="🧠",
    layout="wide",
)

render_page_header(
    title="🧠 Model Performance & Calibration Audit",
    subtitle="Multi-Class Evaluation Metrics, Confusion Matrix Heatmap & Feature Importance Weights",
    badge_text="ML CALIBRATION AUDIT",
)


def main():
    metrics = {}
    perf_pkl = {}

    if PERFORMANCE_METRICS_PATH.exists():
        try:
            perf_pkl = joblib.load(PERFORMANCE_METRICS_PATH)
        except Exception:
            perf_pkl = {}

    if METRICS_JSON_PATH.exists():
        try:
            with open(METRICS_JSON_PATH, "r", encoding="utf-8") as f:
                metrics = json.load(f)
        except Exception:
            metrics = {}

    if not metrics and not perf_pkl:
        st.warning("⚠️ No calibrated model metrics found. Please initialize the ML pipeline on the Command Center homepage.")
        return

    best_model = metrics.get("best_model") or perf_pkl.get("best_model", "XGBoost Tactical Classifier")
    acc = float(metrics.get("accuracy", perf_pkl.get("accuracy", 0.0)))
    prec = float(metrics.get("precision", perf_pkl.get("precision", acc)))
    rec = float(metrics.get("recall", perf_pkl.get("recall", acc)))
    f1 = float(metrics.get("f1_score", perf_pkl.get("f1_score", acc)))

    st.subheader("🎯 Core Model Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        render_kpi_card("Optimal Classifier", str(best_model), "Champion Architecture", "#3b82f6")
    with col2:
        render_kpi_card("Accuracy Score", f"{acc * 100:.2f}%" if acc <= 1.0 else f"{acc:.2f}%", "Holdout Test Set", "#10b981")
    with col3:
        render_kpi_card("Weighted Precision", f"{prec * 100:.2f}%" if prec <= 1.0 else f"{prec:.2f}%", "Positive Predictive Value", "#06b6d4")
    with col4:
        render_kpi_card("Weighted Recall", f"{rec * 100:.2f}%" if rec <= 1.0 else f"{rec:.2f}%", "Sensitivity Coverage", "#f59e0b")
    with col5:
        render_kpi_card("Balanced F1-Score", f"{f1 * 100:.2f}%" if f1 <= 1.0 else f"{f1:.2f}%", "Harmonic Mean", "#a855f7")

    feature_data = metrics.get("feature_importances") or perf_pkl.get("feature_importances_map")
    if not feature_data and "feature_names" in perf_pkl and "feature_importances" in perf_pkl:
        feature_data = dict(zip(perf_pkl["feature_names"], perf_pkl["feature_importances"]))

    cm = perf_pkl.get("confusion_matrix") or metrics.get("confusion_matrix")
    target_classes = perf_pkl.get("target_classes") or metrics.get("target_classes")

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("🧬 Feature Importance Mapping")
        if feature_data:
            fi_df = pd.DataFrame({
                "Feature": list(feature_data.keys()),
                "Importance": list(feature_data.values()),
            }).sort_values(by="Importance", ascending=True)
            fi_df["Feature Label"] = fi_df["Feature"].apply(
                lambda x: x.replace("_txt", "").replace("iyear", "Timeline Year").title()
            )
            fig_fi = px.bar(
                fi_df,
                x="Importance",
                y="Feature Label",
                orientation="h",
                title=f"Relative Feature Information Gain ({best_model})",
                color="Importance",
                color_continuous_scale="Blugrn",
                template="plotly_dark",
            )
            fig_fi.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15, 23, 42, 0.5)",
                coloraxis_showscale=False,
                height=440,
            )
            st.plotly_chart(fig_fi, width='stretch')

    with right_col:
        st.subheader("🧩 Multi-Class Confusion Matrix")
        if cm and target_classes:
            fig_cm = px.imshow(
                cm,
                x=target_classes,
                y=target_classes,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="Blues",
                labels=dict(x="Predicted Attack Class", y="Actual Attack Class", color="Count"),
                title="Test Holdout Confusion Matrix",
            )
            fig_cm.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15, 23, 42, 0.5)",
                height=440,
            )
            st.plotly_chart(fig_cm, width='stretch')
        else:
            st.info("Confusion matrix will appear after running the training calibration pipeline.")

    if "per_class_report" in perf_pkl and isinstance(perf_pkl["per_class_report"], dict):
        st.markdown("---")
        st.subheader("📋 Per-Class Precision, Recall & F1 Audit Ledger")
        rows = []
        for cls_name, stats in perf_pkl["per_class_report"].items():
            if isinstance(stats, dict) and cls_name not in ("accuracy", "macro avg", "weighted avg"):
                rows.append({
                    "Attack Classification": cls_name,
                    "Precision": f"{stats.get('precision', 0.0):.2%}",
                    "Recall": f"{stats.get('recall', 0.0):.2%}",
                    "F1-Score": f"{stats.get('f1-score', 0.0):.2%}",
                    "Test Support (Rows)": int(stats.get("support", 0)),
                })
        if rows:
            st.dataframe(pd.DataFrame(rows), width='stretch', hide_index=True)

    render_footer(
        "**⚠️ CALIBRATION NOTICE:** Evaluation metrics are computed on a stratified 20% holdout split of the active GTD dataset."
    )


if __name__ == "__main__":
    main()
