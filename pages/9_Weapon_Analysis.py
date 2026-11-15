import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from utils.dashboard_metrics import render_page_header, render_kpi_card, render_footer

st.set_page_config(
    page_title="Weapon Analysis | Threat Intelligence",
    page_icon="⚔️",
    layout="wide",
)

render_page_header(
    title="⚔️ Weapon Profile & Lethality Vector Analysis",
    subtitle="Historical Weapon Typologies, Casualty Lethality Ratios & Chronological Deployment Trajectories",
    badge_text="WEAPONRY TELEMETRY",
)

try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Failed to initialize core dataset pipeline: {e}")
    st.stop()

weap_col = "weaptype1_txt" if "weaptype1_txt" in df.columns else "weapon_type"
df_clean = df[df[weap_col].notna() & (df[weap_col] != "Unknown")].copy()

unique_weapons = df_clean[weap_col].nunique()
top_weap_name = str(df_clean[weap_col].mode().iloc[0]) if not df_clean.empty else "N/A"
lethality_df = (
    df_clean.groupby(weap_col)
    .agg(
        Incidents=("eventid", "count"),
        Casualties=("total_casualties", "sum"),
        Avg_Casualties=("total_casualties", "mean"),
    )
    .reset_index()
)
deadliest_weap = (
    str(lethality_df.sort_values(by="Avg_Casualties", ascending=False).iloc[0][weap_col])
    if not lethality_df.empty
    else "N/A"
)

k1, k2, k3 = st.columns(3)
with k1:
    render_kpi_card("Unique Weapon Categories", f"{unique_weapons}", "Excluding Unknown Classes", "#3b82f6")
with k2:
    render_kpi_card("Most Deployed Weapon Class", top_weap_name, "Highest Volume Vector", "#ef4444")
with k3:
    render_kpi_card("Highest Avg Casualties / Incident", deadliest_weap, "Peak Per-Event Lethality", "#f59e0b")

st.markdown("---")
st.subheader("📊 Global Weapon Volume vs. Average Lethality")

g_col1, g_col2 = st.columns(2)
with g_col1:
    top_weapons = df_clean[weap_col].value_counts().reset_index()
    top_weapons.columns = [weap_col, "Count"]

    fig_top_weapons = px.bar(
        top_weapons.head(10),
        x="Count",
        y=weap_col,
        orientation="h",
        title="Top Weapon Classifications by Incident Volume",
        labels={weap_col: "Weapon Classification", "Count": "Incident Volume"},
        color="Count",
        color_continuous_scale="Reds",
    )
    fig_top_weapons.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        coloraxis_showscale=False,
        yaxis={"categoryorder": "total ascending"},
    )
    st.plotly_chart(fig_top_weapons, width='stretch')

with g_col2:
    fig_lethality = px.bar(
        lethality_df.sort_values(by="Avg_Casualties", ascending=False).head(10),
        x="Avg_Casualties",
        y=weap_col,
        orientation="h",
        title="Average Casualties per Incident by Weapon Class",
        labels={weap_col: "Weapon Classification", "Avg_Casualties": "Mean Casualties / Incident"},
        color="Avg_Casualties",
        color_continuous_scale="OrRd",
    )
    fig_lethality.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        coloraxis_showscale=False,
        yaxis={"categoryorder": "total ascending"},
    )
    st.plotly_chart(fig_lethality, width='stretch')

st.markdown("---")

st.subheader("🔍 Weapon Type Specific Deep Dive")
available_weapons = sorted(df_clean[weap_col].unique())
default_idx = available_weapons.index("Explosives") if "Explosives" in available_weapons else 0

selected_weapon = st.selectbox(
    "Select Weapon Category to Profile:",
    options=available_weapons,
    index=default_idx,
)

filtered_df = df_clean[df_clean[weap_col] == selected_weapon].copy()

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Yearly Deployment Trajectory")
    yearly_trend = filtered_df.groupby("iyear").size().reset_index(name="Incident Count")

    if not yearly_trend.empty:
        fig_trend = px.line(
            yearly_trend,
            x="iyear",
            y="Incident Count",
            title=f"Chronological Timeline Trajectory for: {selected_weapon}",
            labels={"iyear": "Timeline Year", "Incident Count": "Incident Volume"},
            markers=True,
        )
        fig_trend.update_traces(line=dict(color="#ef4444", width=3))
        fig_trend.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        )
        st.plotly_chart(fig_trend, width='stretch')
    else:
        st.info("No timeline trajectory elements cataloged for this segment selection.")

with col2:
    st.markdown("#### Top Impacted Countries")
    country_col = "country_txt" if "country_txt" in filtered_df.columns else "country"
    top_countries = filtered_df[country_col].value_counts().reset_index().head(10)
    top_countries.columns = [country_col, "Count"]

    if not top_countries.empty:
        fig_countries = px.bar(
            top_countries,
            x="Count",
            y=country_col,
            orientation="h",
            title=f"Highest Utilization Jurisdictions: {selected_weapon}",
            labels={country_col: "Country Jurisdiction", "Count": "Incident Volume"},
            color="Count",
            color_continuous_scale="Oranges",
        )
        fig_countries.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            coloraxis_showscale=False,
            yaxis={"categoryorder": "total ascending"},
        )
        st.plotly_chart(fig_countries, width='stretch')
    else:
        st.info("No jurisdiction metadata entries found for this weapon subset.")

st.markdown("---")
st.subheader("📋 Filtered Data Table Reference")
display_cols = [
    c
    for c in ["iyear", "country_txt", "region_txt", "gname", "attacktype1_txt", "targtype1_txt", "nkill", "nwound"]
    if c in filtered_df.columns
]
if not filtered_df.empty:
    st.dataframe(filtered_df[display_cols].head(100), width='stretch', hide_index=True)
else:
    st.info("No database line entries found matching target weapon boundaries.")

render_footer(
    "**⚠️ METHODOLOGICAL SAFEGUARD NOTICE:** Weapon metrics and deployment trend frequencies displayed on this "
    "interface consist entirely of historical rule-based data summaries computed from the Global Terrorism Database (GTD)."
)
