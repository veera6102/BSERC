import streamlit as st
import os
import subprocess
# This import statement now resolves flawlessly without raising exceptions
from config import CSS_STYLE, PREDICTION_MODEL_PATH, RISK_MODEL_PATH, DATA_PATH

# 1. Configure the Streamlit Page Layout
st.set_page_config(
    page_title="Global Threat Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global custom dark theme adjustments via Markdown injection
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# 2. Application Header
st.markdown("<h1 class='glow-text'>🌐 Global Threat Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8;font-size:1.1rem;'>Advanced Analytics Platform for Global Terrorism Database (GTD) • Strategic Insights & Predictive Modeling</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:rgba(59, 130, 246, 0.2);'>", unsafe_allow_html=True)

# 3. Dynamic Pipeline Verification Logic
models_exist = os.path.exists(PREDICTION_MODEL_PATH) and os.path.exists(RISK_MODEL_PATH)
data_exists = os.path.exists(DATA_PATH)

if data_exists:
    st.sidebar.markdown("<p style='color:#10b981;font-weight:bold;'>✓ SYSTEM ONLINE</p>", unsafe_allow_html=True)
    st.sidebar.info("Database connected and operational.")
    
    if not models_exist:
        st.warning("⚠️ Machine Learning models require calibration.")
        st.info("Initialize prediction models by running the training pipeline:")
        
        if st.button("🚀 Initialize ML Models (RF, XGBoost, LightGBM)", use_container_width=True):
            with st.spinner("Training classifiers and optimizing model parameters..."):
                try:
                    result = subprocess.run(["python", "train_attack_model.py"], capture_output=True, text=True, check=True)
                    st.success("✅ ML Models calibrated and saved successfully.")
                    st.toast("Models ready for inference.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Training pipeline failed: {e}")
                    if 'result' in locals() and result.stderr:
                        st.code(result.stderr)
    else:
        st.sidebar.markdown("<p style='color:#10b981;font-weight:bold;'>🤖 ML MODELS READY</p>", unsafe_allow_html=True)
        st.sidebar.success("Prediction systems operational.")
else:
    st.sidebar.markdown("<p style='color:#ef4444;font-weight:bold;'>❌ DATABASE OFFLINE</p>", unsafe_allow_html=True)
    st.sidebar.error(f"Missing primary file asset at: {DATA_PATH}")

# 4. System Overview Panel Layout
st.markdown(f"""
<div class='kpi-card' style='text-align: left; padding: 25px;'>
    <h3 style='color:#3b82f6; margin-top:0px;'>SYSTEM OVERVIEW</h3>
    <p>This professional intelligence analytics platform leverages the Global Terrorism Database (GTD) to provide comprehensive security insights, threat evaluation, and predictive modeling capabilities.</p>
    <p><strong>Data Coverage:</strong> 1970-2020 (209,706 incidents analyzed)</p>
    <p><strong>Navigation Index:</strong> Access specialized modules via the sidebar layout index.</p>
    <p style='color: #f59e0b; font-weight: bold; margin-top: 20px; font-size:0.9rem;'>
        ⚠️ DISCLAIMER: This platform is for analytical research only. All predictions are based strictly on historical mathematical patterns and should not be interpreted as forecasts of real-world tactical events.
    </p>
</div>
""", unsafe_allow_html=True)

# 5. Fixed Page Layout Footer
st.markdown("""
<div class='footer-container'>
    <p>Global Threat Intelligence Dashboard • Advanced Analytics Platform</p>
</div>
""", unsafe_allow_html=True)