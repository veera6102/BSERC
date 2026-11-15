import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_data
from utils.prediction import models_are_ready, predict_attack_profile
from utils.risk_calculator import calculate_risk
from utils.dashboard_metrics import render_page_header, render_kpi_card, render_footer

st.set_page_config(
    page_title="Threat Network & Simulation Lab | Threat Intelligence",
    page_icon="🕸️",
    layout="wide",
)

render_page_header(
    title="🕸️ Threat Network & Multi-Scenario War-Gaming Lab",
    subtitle="Multi-Dimensional Attack Flow Topology, 3-Scenario Tactical War-Gaming & Statistical Anomaly Detection",
    badge_text="ADVANCED WAR-GAMING LAB",
)

df = load_data()

tab_flow, tab_wargame, tab_anomaly = st.tabs([
    "🕸️ Multi-Vector Threat Topology (Sankey / Sunburst)",
    "⚔️ 3-Scenario Tactical War-Gaming Simulator",
    "🚨 High-Severity Statistical Anomaly Detector",
])

# ==============================================================================
# TAB 1: MULTI-VECTOR THREAT TOPOLOGY
# ==============================================================================
with tab_flow:
    st.subheader("🕸️ Hierarchical Threat Vector Topology")
    st.markdown("Explore how **Regions**, **Attack Vectors**, **Weapon Classes**, and **Target Sectors** interconnect across historical incidents.")

    f_col1, f_col2 = st.columns([1, 2])
    with f_col1:
        top_n_flow = st.slider("Top Categories Depth", min_value=4, max_value=10, value=6)
        region_opts = ["All Regions"] + sorted(df["region_txt"].dropna().unique().tolist())
        sel_reg_flow = st.selectbox("Scope Region for Topology", region_opts, index=0)

    flow_df = df.copy()
    if sel_reg_flow != "All Regions":
        flow_df = flow_df[flow_df["region_txt"] == sel_reg_flow]

    # Filter to top categories for visual clarity
    for col in ["region_txt", "attacktype1_txt", "weaptype1_txt", "targtype1_txt"]:
        top_vals = flow_df[col].value_counts().head(top_n_flow).index
        flow_df = flow_df[flow_df[col].isin(top_vals)]

    c_sun, c_par = st.columns(2)
    with c_sun:
        if not flow_df.empty:
            sun_agg = (
                flow_df.groupby(["region_txt", "attacktype1_txt", "weaptype1_txt"])
                .size()
                .reset_index(name="Incidents")
            )
            fig_sun = px.sunburst(
                sun_agg,
                path=["region_txt", "attacktype1_txt", "weaptype1_txt"],
                values="Incidents",
                color="Incidents",
                color_continuous_scale="Blues",
                title="Sunburst Hierarchy: Region → Attack Method → Weapon",
                template="plotly_dark",
            )
            fig_sun.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=45, b=10),
                height=460,
            )
            st.plotly_chart(fig_sun, width='stretch')

    with c_par:
        if not flow_df.empty:
            fig_par = px.parallel_categories(
                flow_df.head(600),
                dimensions=["region_txt", "attacktype1_txt", "weaptype1_txt", "targtype1_txt"],
                color="total_casualties",
                color_continuous_scale="Turbo",
                labels={
                    "region_txt": "Region",
                    "attacktype1_txt": "Attack Vector",
                    "weaptype1_txt": "Weapon",
                    "targtype1_txt": "Target Sector",
                },
                title="Multi-Vector Alluvial Flow (Colored by Casualties)",
            )
            fig_par.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=25, r=25, t=50, b=20),
                height=460,
            )
            st.plotly_chart(fig_par, width='stretch')

# ==============================================================================
# TAB 2: 3-SCENARIO TACTICAL WAR-GAMING SIMULATOR
# ==============================================================================
with tab_wargame:
    st.subheader("⚔️ Side-by-Side Multi-Scenario War-Gaming Matrix")
    st.markdown("Configure 3 operational scenarios simultaneously to compare **ML Predicted Attack Profiles** and **0–120 Threat Risk Scores**.")

    countries = sorted(df["country_txt"].dropna().unique().tolist())
    weapons = sorted(df["weaptype1_txt"].dropna().unique().tolist())
    targets = sorted(df["targtype1_txt"].dropna().unique().tolist())

    s_cols = st.columns(3)
    scenarios = []
    defaults = [
        ("Alpha (Urban Infrastructure)", 0, "Explosives", "Business", 1, 0, 12),
        ("Bravo (VIP / Diplomatic)", min(1, len(countries) - 1), "Firearms", "Government (General)", 1, 0, 4),
        ("Charlie (High-Intensity)", min(2, len(countries) - 1), "Explosives", "Military", 1, 1, 35),
    ]

    for idx, (s_label, c_idx, def_w, def_t, def_suc, def_sui, def_cas) in enumerate(defaults):
        with s_cols[idx]:
            st.markdown(f"#### 🛡️ Scenario {s_label}")
            sc_country = st.selectbox("Country", countries, index=c_idx, key=f"wg_c_{idx}")
            w_idx = weapons.index(def_w) if def_w in weapons else 0
            sc_weapon = st.selectbox("Weapon Class", weapons, index=w_idx, key=f"wg_w_{idx}")
            t_idx = targets.index(def_t) if def_t in targets else 0
            sc_target = st.selectbox("Target Sector", targets, index=t_idx, key=f"wg_t_{idx}")
            sc_suicide = st.selectbox("Suicide Mode", [0, 1], index=def_sui, format_func=lambda x: "Yes (1)" if x == 1 else "No (0)", key=f"wg_sui_{idx}")
            sc_cas = st.number_input("Projected Casualties", 0, 5000, def_cas, key=f"wg_cas_{idx}")

            c_regs = df[df["country_txt"] == sc_country]["region_txt"].dropna().unique().tolist()
            sc_region = c_regs[0] if c_regs else "North America"

            score, level, _ = calculate_risk(sc_weapon, sc_target, 1, sc_suicide, sc_cas, df=df)
            if models_are_ready():
                pred_cls, prob, _ = predict_attack_profile(sc_country, sc_region, sc_target, sc_weapon, 2026, 1, sc_suicide)
            else:
                pred_cls, prob = "Uncalibrated", 0.0

            scenarios.append({
                "Scenario": f"Scenario {chr(65 + idx)}",
                "Country": sc_country,
                "Weapon": sc_weapon,
                "Target": sc_target,
                "Predicted Attack Vector": pred_cls,
                "ML Confidence": f"{prob:.1%}",
                "Risk Score (/120)": score,
                "Threat Level": level,
            })

    st.markdown("---")
    res_df = pd.DataFrame(scenarios)
    r_left, r_right = st.columns([1.1, 1.3])
    with r_left:
        fig_wg = px.bar(
            res_df,
            x="Scenario",
            y="Risk Score (/120)",
            color="Threat Level",
            text="Risk Score (/120)",
            title="Comparative Scenario Risk Score (0–120)",
            color_discrete_map={"LOW": "#10b981", "MODERATE": "#f59e0b", "HIGH": "#f97316", "CRITICAL": "#ef4444"},
            template="plotly_dark",
        )
        fig_wg.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            yaxis=dict(range=[0, 125]),
        )
        st.plotly_chart(fig_wg, width='stretch')
    with r_right:
        st.markdown("#### 📊 Multi-Scenario Simulation Output Ledger")
        st.dataframe(res_df, width='stretch', hide_index=True)

# ==============================================================================
# TAB 3: STATISTICAL MASS-CASUALTY ANOMALY DETECTOR
# ==============================================================================
with tab_anomaly:
    st.subheader("🚨 Statistical Mass-Casualty Anomaly Detector (Z-Score Outliers)")
    mean_cas = float(df["total_casualties"].mean())
    std_cas = float(df["total_casualties"].std()) if df["total_casualties"].std() > 0 else 1.0

    z_thresh = st.slider("Z-Score Outlier Threshold (σ above mean casualties)", min_value=1.0, max_value=5.0, value=2.0, step=0.5)

    anom_df = df.copy()
    anom_df["z_score"] = (anom_df["total_casualties"] - mean_cas) / std_cas
    outliers = anom_df[anom_df["z_score"] >= z_thresh].sort_values(by="total_casualties", ascending=False)

    a1, a2, a3 = st.columns(3)
    with a1:
        render_kpi_card("Detected Anomaly Events", f"{len(outliers):,}", f"Exceeding +{z_thresh:.1f}σ Threshold", "#ef4444")
    with a2:
        max_cas = int(outliers["total_casualties"].max()) if not outliers.empty else 0
        render_kpi_card("Peak Single-Event Casualties", f"{max_cas:,}", "Maximum Historical Outlier", "#f97316")
    with a3:
        render_kpi_card("Baseline Dataset Mean", f"{mean_cas:.2f}", f"1σ Std Dev: {std_cas:.2f}", "#3b82f6")

    if not outliers.empty:
        fig_anom = px.scatter(
            outliers.head(150),
            x="iyear",
            y="total_casualties",
            size="total_casualties",
            color="attacktype1_txt",
            hover_data=["country_txt", "city", "gname", "weaptype1_txt", "targtype1_txt"],
            title="High-Severity Casualty Outliers by Year & Attack Vector",
            labels={"iyear": "Year", "total_casualties": "Total Casualties", "attacktype1_txt": "Attack Vector"},
            template="plotly_dark",
        )
        fig_anom.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
        )
        st.plotly_chart(fig_anom, width='stretch')

        cols = [c for c in ["iyear", "country_txt", "city", "gname", "attacktype1_txt", "weaptype1_txt", "targtype1_txt", "nkill", "nwound", "total_casualties", "z_score"] if c in outliers.columns]
        st.dataframe(outliers[cols].head(50).round({"z_score": 2}), width='stretch', hide_index=True)
    else:
        st.info("No incidents exceed the selected Z-score threshold.")

render_footer(
    "**⚠️ SIMULATION LAB DISCLAIMER:** Topology diagrams, war-gaming outputs, and Z-score anomaly calculations "
    "are retrospective mathematical analyses of the GTD and must not be treated as real-world operational intelligence."
)
