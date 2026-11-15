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
    page_title="Target Analysis | Threat Intelligence",
    page_icon="🎯",
    layout="wide",
)

render_page_header(
    title="🎯 Target Analysis & Asset Vulnerability Profiles",
    subtitle="Infrastructure Vulnerability Matrices, Sector Casualty Severity & Geographic Exposure",
    badge_text="ASSET VULNERABILITY",
)

try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Failed to initialize core dataset pipeline: {e}")
    st.stop()

targ_col = "targtype1_txt" if "targtype1_txt" in df.columns else "target_type"
df_clean = df[df[targ_col].notna() & (df[targ_col] != "Unknown")].copy()

unique_targets = df_clean[targ_col].nunique()
top_targ_name = str(df_clean[targ_col].mode().iloc[0]) if not df_clean.empty else "N/A"
sector_stats = (
    df_clean.groupby(targ_col)
    .agg(
        Incidents=("eventid", "count"),
        Casualties=("total_casualties", "sum"),
        Avg_Casualties=("total_casualties", "mean"),
    )
    .reset_index()
)
highest_cas_sector = (
    str(sector_stats.sort_values(by="Casualties", ascending=False).iloc[0][targ_col])
    if not sector_stats.empty
    else "N/A"
)

k1, k2, k3 = st.columns(3)
with k1:
    render_kpi_card("Categorized Target Sectors", f"{unique_targets}", "Distinct Infrastructure Classes", "#3b82f6")
with k2:
    render_kpi_card("Most Frequently Targeted", top_targ_name, "Highest Historical Volume", "#ef4444")
with k3:
    render_kpi_card("Highest Casualty Burden", highest_cas_sector, "Cumulative Killed + Wounded", "#10b981")

st.markdown("---")
st.subheader("📊 Top Target Sectors: Incident Volume vs. Total Casualties")

t_col1, t_col2 = st.columns(2)
with t_col1:
    top_targets = df_clean[targ_col].value_counts().reset_index()
    top_targets.columns = [targ_col, "Count"]

    fig_top_targets = px.bar(
        top_targets.head(10),
        x="Count",
        y=targ_col,
        orientation="h",
        title="Top 10 Targeted Infrastructure Sectors (Incident Count)",
        labels={targ_col: "Target Environment Sector", "Count": "Incident Volume"},
        color="Count",
        color_continuous_scale="Viridis",
    )
    fig_top_targets.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        coloraxis_showscale=False,
        yaxis={"categoryorder": "total ascending"},
    )
    st.plotly_chart(fig_top_targets, width='stretch')

with t_col2:
    fig_cas_targets = px.bar(
        sector_stats.sort_values(by="Casualties", ascending=False).head(10),
        x="Casualties",
        y=targ_col,
        orientation="h",
        title="Top 10 Sectors by Cumulative Casualties",
        labels={targ_col: "Target Environment Sector", "Casualties": "Total Casualties"},
        color="Casualties",
        color_continuous_scale="Magma",
    )
    fig_cas_targets.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        coloraxis_showscale=False,
        yaxis={"categoryorder": "total ascending"},
    )
    st.plotly_chart(fig_cas_targets, width='stretch')

st.markdown("---")
st.subheader("🎯 Deep Dive Filter Profile")
available_targets = sorted(df_clean[targ_col].unique())
default_idx = (
    available_targets.index("Private Citizens & Property")
    if "Private Citizens & Property" in available_targets
    else 0
)

selected_target = st.selectbox(
    "Select Target Profile to Inspect:",
    options=available_targets,
    index=default_idx,
    key="target_selector_dropdown",
)

filtered_df = df_clean[df_clean[targ_col] == selected_target].copy()

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Chronological Target Trend")
    yearly_trend = filtered_df.groupby("iyear").size().reset_index(name="Incident Count")

    if not yearly_trend.empty:
        fig_trend = px.line(
            yearly_trend,
            x="iyear",
            y="Incident Count",
            title=f"Incident Frequency Trajectory for: {selected_target}",
            labels={"iyear": "Timeline Year", "Incident Count": "Incident Volume"},
            markers=True,
        )
        fig_trend.update_traces(line=dict(color="#3b82f6", width=3), marker=dict(size=6, color="#ef4444"))
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
    st.markdown("#### Top Impacted Jurisdictions")
    country_col = "country_txt" if "country_txt" in filtered_df.columns else "country"
    top_countries = filtered_df[country_col].value_counts().reset_index().head(10)
    top_countries.columns = [country_col, "Count"]

    if not top_countries.empty:
        fig_countries = px.bar(
            top_countries,
            x="Count",
            y=country_col,
            orientation="h",
            title=f"Highest Risk Concentration Areas: {selected_target}",
            labels={country_col: "Country Jurisdiction", "Count": "Incident Volume"},
            color="Count",
            color_continuous_scale="Blues",
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
        st.info("No jurisdiction metadata entries found for this target infrastructure subset.")

st.markdown("---")
st.subheader("📋 Filtered Data (Table Source Reference)")
display_cols = [
    c
    for c in ["iyear", "country_txt", "region_txt", "gname", "attacktype1_txt", "weaptype1_txt", "nkill", "nwound"]
    if c in filtered_df.columns
]
if not filtered_df.empty:
    st.dataframe(filtered_df[display_cols].head(100), width='stretch', hide_index=True)
else:
    st.info("No database line entries found matching target filter criteria boundaries.")

render_footer(
    "**⚠️ METHODOLOGICAL SAFEGUARD NOTICE:** Target categorization trends and risk frequencies displayed on this "
    "interface consist entirely of historical rule-based data summaries computed from the Global Terrorism Database (GTD)."
)
