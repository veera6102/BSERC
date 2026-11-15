import streamlit as st
import pandas as pd  
import plotly.express as px
import json
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Model Performance Metrics | Threat Intelligence",
    page_icon="📊",
    layout="wide"
)

st.markdown("<h1 class='glow-text'>📊 Model Performance & Calibration Audit</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8;font-size:1.1rem;'>Technical Evaluation Metrics, Confusion Matrix Insights, and Feature Importance Mapping.</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:rgba(59, 130, 246, 0.2);'>", unsafe_allow_html=True)

def main():
    METRICS_DIR = "models"
    METRICS_PATH = os.path.join(METRICS_DIR, "metrics.json")
    
    # 2. AUTO-INITIALIZE PLACEHOLDER LEDGER IF NOT FOUND
    if not os.path.exists(METRICS_PATH):
        # Dynamically create the directory structure if missing
        os.makedirs(METRICS_DIR, exist_ok=True)
        
        # Safe structural fallback logs for visual development
        mock_metrics = {
            "best_model": "LightGBM (Baseline Mock)",
            "accuracy": 0.914,
            "precision": 0.908,
            "recall": 0.895,
            "f1_score": 0.891,
            "feature_importances": {
                "weaptype1_txt": 0.385,
                "targtype1_txt": 0.242,
                "country_txt": 0.183,
                "region_txt": 0.110,
                "iyear": 0.051,
                "suicide": 0.019,
                "success": 0.010
            }
        }
        try:
            with open(METRICS_PATH, "w") as f:
                json.dump(mock_metrics, f, indent=4)
            st.info("💡 *Notice: Initialized page using safe local baseline metrics. Recalibrate models on the App landing page to update with actual dataset coefficients.*")
        except Exception as e:
            st.error(f"❌ Could not create mock data fallback file: {e}")
            st.stop()
        
    try:
        with open(METRICS_PATH, "r") as f:
            metrics = json.load(f)
    except Exception as e:
        st.error(f"❌ Failed to parse metrics ledger: {e}")
        st.stop()

    # 3. Model Overview & KPI Summary Cards
    st.subheader("🎯 Core Model Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(label="Optimal Classifier", value=metrics.get("best_model", "N/A"))
    with col2:
        acc = metrics.get("accuracy", 0.0)
        st.metric(label="Accuracy Score", value=f"{acc * 100:.1f}%" if acc <= 1.0 else f"{acc}%")
    with col3:
        prec = metrics.get("precision", 0.0)
        st.metric(label="Weighted Precision", value=f"{prec * 100:.1f}%" if prec <= 1.0 else f"{prec}%")
    with col4:
        rec = metrics.get("recall", 0.0)
        st.metric(label="Weighted Recall", value=f"{rec * 100:.1f}%" if rec <= 1.0 else f"{rec}%")
    with col5:
        f1 = metrics.get("f1_score", 0.0)
        st.metric(label="F1-Score (Balanced)", value=f"{f1 * 100:.1f}%" if f1 <= 1.0 else f"{f1}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Feature Importance Visualization
    st.subheader("🧬 Feature Importance Mapping")
    st.markdown("The chart below illustrates the structural weight and informational gain provided by each core feature during historical pattern analysis classification:")

    feature_data = metrics.get("feature_importances", {})

    # Generate a baseline DataFrame using the corrected Pandas integration
    fi_df = pd.DataFrame({
        "Feature": list(feature_data.keys()),
        "Importance": list(feature_data.values())
    }).sort_values(by="Importance", ascending=True)

    # Format column naming labels for clean presentation
    fi_df["Feature Label"] = fi_df["Feature"].apply(lambda x: x.replace("_txt", "").replace("iyear", "Year").title())

    # Build Interactive Plotly Figure
    fig = px.bar(
        fi_df,
        x="Importance",
        y="Feature Label",
        orientation="h",
        title=f"Statistical Feature Coefficients ({metrics.get('best_model', 'Classifier')})",
        labels={"Importance": "Relative Informational Gain", "Feature Label": "Evaluated Metric"},
        color="Importance",
        color_continuous_scale="Blugrn"
    )

    # Style Plotly Chart to match Dashboard Dark Theme Layout
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        margin=dict(l=40, r=40, t=50, b=40),
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()