import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from utils.risk_calculator import calculate_risk, get_posture_recommendations
from utils.charts import risk_gauge_chart
from utils.dashboard_metrics import render_page_header, render_footer

st.set_page_config(
    page_title="Threat Level Calculator | Threat Intelligence",
    page_icon="🚨",
    layout="wide",
)

render_page_header(
    title="🚨 Operational Threat Level Calculator",
    subtitle="Dynamic 0–120 Risk Speedometer, Factor Attribution Audit & Defensive Posture Guidance",
    badge_text="RISK SCORING ENGINE",
)

try:
    df = load_data()
    available_weapons = sorted(df["weaptype1_txt"].dropna().unique())
    available_targets = sorted(df["targtype1_txt"].dropna().unique())
except Exception as e:
    st.error(f"❌ Failed to load dataset context for inputs: {e}")
    available_weapons = ["Explosives", "Firearms", "Incendiary", "Melee", "Chemical", "Biological", "Unknown"]
    available_targets = ["Military", "Police", "Government (General)", "Private Citizens & Property", "Business", "Utilities"]
    df = None

st.subheader("📋 Scenario Parameter Selection")
col1, col2, col3 = st.columns(3)

with col1:
    weapon = st.selectbox(
        "⚡ Weapon Type Profile",
        options=available_weapons,
        help="Select the specific attack method asset class used.",
    )
    target = st.selectbox(
        "🎯 Target Environment Profile",
        options=available_targets,
        help="Select the primary administrative or societal victim segment classification.",
    )

with col2:
    success = st.selectbox(
        "⚙️ Operational Success Status",
        options=[1, 0],
        format_func=lambda x: "Yes (Incident Objective Achieved)" if x == 1 else "No (Aborted / Contained)",
    )
    suicide = st.selectbox(
        "🪂 High-Intensity Tactical Profile (Suicide)",
        options=[0, 1],
        format_func=lambda x: "No (Standard Execution)" if x == 0 else "Yes (Suicide Attack Mode)",
    )

with col3:
    casualties = st.number_input(
        "📊 Total Casualties (Fatalities + Injuries)",
        min_value=0,
        max_value=10000,
        value=5,
        step=1,
        help="Combined total of confirmed casualties (Injuries + Fatalities).",
    )

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 Calculate Audit Risk Profile", type="primary", width='stretch'):
    with st.spinner("Evaluating data-driven lethality weights and computing threat index..."):
        score, level, reasons, breakdown = calculate_risk(
            weapon, target, success, suicide, casualties, df=df, return_breakdown=True
        )

        color_map = {
            "LOW": "#10b981",
            "MODERATE": "#f59e0b",
            "HIGH": "#f97316",
            "CRITICAL": "#ef4444",
        }
        level_color = color_map.get(level, "#3b82f6")

        g_col, b_col = st.columns([1.1, 1.2])
        with g_col:
            st.plotly_chart(risk_gauge_chart(score, level), width='stretch')

        with b_col:
            bd_df = pd.DataFrame({
                "Risk Factor": list(breakdown.keys()),
                "Points Contributed": list(breakdown.values()),
            })
            fig_bd = px.bar(
                bd_df,
                x="Points Contributed",
                y="Risk Factor",
                orientation="h",
                title="Component Weight Attribution Breakdown",
                color="Points Contributed",
                color_continuous_scale="Reds",
                template="plotly_dark",
            )
            fig_bd.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15, 23, 42, 0.5)",
                height=300,
                margin=dict(l=20, r=20, t=45, b=20),
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig_bd, width='stretch')

        audit_col, rec_col = st.columns(2)
        with audit_col:
            st.subheader("🔍 Transparent Audit Ledger")
            for reason in reasons:
                st.markdown(f"**✔** `{reason}`")

        with rec_col:
            st.subheader("🛡️ Recommended Analytical & Security Posture")
            st.markdown(
                f"<div style='border-left:4px solid {level_color}; padding-left:14px;'>",
                unsafe_allow_html=True,
            )
            for rec in get_posture_recommendations(level):
                st.markdown(f"- {rec}")
            st.markdown("</div>", unsafe_allow_html=True)

render_footer(
    "**⚠️ METHODOLOGICAL DISCLAIMER:** This platform calculates algorithmic danger thresholds through a mathematical, "
    "rule-based formula calibrated against historical GTD variance. It serves strictly as an explainable decision-support utility."
)
