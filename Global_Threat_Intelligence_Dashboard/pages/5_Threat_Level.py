import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.risk_calculator import calculate_risk

# 1. Page Configuration
st.set_page_config(
    page_title="Threat Level Calculator | Threat Intelligence",
    page_icon="🚨",
    layout="wide"
)

st.markdown("<h1 class='glow-text'>🚨 Operational Threat Level Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8;font-size:1.1rem;'>Dynamic Risk Scoring & Tactical Vulnerability Auditing System based on Empirical GTD Features.</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:rgba(59, 130, 246, 0.2);'>", unsafe_allow_html=True)

# 2. Safely Load Master Data for Dropdowns
try:
    df = load_data()
    available_weapons = sorted(df["weaptype1_txt"].dropna().unique())
    available_targets = sorted(df["targtype1_txt"].dropna().unique())
except Exception as e:
    st.error(f"❌ Failed to load dataset context for inputs: {e}")
    # Robust baseline fallbacks if data pipeline fails
    available_weapons = ["Explosives", "Firearms", "Incendiary", "Melee", "Chemical", "Biological", "Unknown"]
    available_targets = ["Military", "Police", "Government (General)", "Private Citizens & Property", "Business", "Utilities"]
    df = None

# 3. Input Form Grid Design
st.subheader("📋 Scenario Parameter Selection")
col1, col2 = st.columns(2)

with col1:
    weapon = st.selectbox(
        "⚡ Weapon Type Profile",
        options=available_weapons,
        help="Select the specific attack method asset class used."
    )
    
    target = st.selectbox(
        "🎯 Target Environment Profile",
        options=available_targets,
        help="Select the primary administrative or societal victim segment classification."
    )

with col2:
    success = st.selectbox(
        "⚙️ Operational Success Status",
        options=[1, 0],
        format_func=lambda x: "Yes (Incident Objective Achieved)" if x == 1 else "No (Aborted / Failed / Neutralized)",
        help="Indicate whether tactical execution achieved technical intent."
    )
    
    suicide = st.selectbox(
        "🪂 High-Intensity Tactical Profile (Suicide)",
        options=[0, 1],
        format_func=lambda x: "No" if x == 0 else "Yes (Active Suicide Profile Detected)",
        help="Indicate whether the incident involves the certain death of the perpetrator during execution."
    )

# Casualties spans across full layout width under columns
casualties = st.number_input(
    "📊 Quantifiable Severity Impact (Total Casualties)",
    min_value=0,
    max_value=10000,
    value=0,
    step=1,
    help="Combined total of confirmed casualties (Injuries + Fatalities)."
)

st.markdown("<br>", unsafe_allow_html=True)

# 4. Process Logic & Visual Score Representation
if st.button("🚀 Calculate Audit Risk Profile", type="primary", use_container_width=True):
    with st.spinner("Processing architectural rules and balancing metrics..."):
        score, level, reasons = calculate_risk(weapon, target, success, suicide, casualties, df=df)
        
        # Color configuration based on classified threat level severity
        color_map = {
            "LOW": "#10b981",       # Emerald Green
            "MODERATE": "#f59e0b",  # Amber/Yellow
            "HIGH": "#f97316",      # Orange
            "CRITICAL": "#ef4444"   # Red
        }
        level_color = color_map.get(level, "#f1f5f9")
        
        # Display Core Metric Dashboard Summary Boxes
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(label="Calculated Dynamic Score", value=f"{score} / 120")
        with res_col2:
            st.markdown(
                f"""
                <div style='background-color:rgba(15,23,42,0.6); padding:10px 20px; border-radius:8px; border-left:5px solid {level_color};'>
                    <p style='margin:0; font-size:0.85rem; color:#94a3b8; font-weight:bold; letter-spacing:0.05em;'>THREAT LEVEL CLASSIFICATION</p>
                    <h2 style='margin:0; color:{level_color}; font-size:2rem; font-weight:bold;'>{level}</h2>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 5. Expandable Transparent Explainability Ledger
        st.subheader("🔍 Transparent Audit Ledger & Factor Attribution")
        st.markdown("Review the logic trace behind this calculation to explain decisions clearly:")
        
        for reason in reasons:
            st.markdown(f"**✔** `{reason}`")

# 6. Operational Risk Disclaimers
st.markdown("<br><hr style='border-color:rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
st.warning(
    """
    **⚠️ METHODOLOGICAL DISCLAIMER:** This platform calculates algorithmic danger thresholds through a mathematical, rule-based formula 
    calibrated against data-driven historical statistical variance from the Global Terrorism Database (GTD). 
    
    It serves strictly as an explainable decision support utility for analytical retrospective research. It must never be utilized 
    to forecast prospective dynamic tactical incidents or real-world events.
    """
)