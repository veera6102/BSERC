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
    page_title="Data Explorer | Threat Intelligence",
    page_icon="🔍",
    layout="wide",
)

render_page_header(
    title="🔍 Master Data Explorer & Correlation Matrix",
    subtitle="Multi-Dimensional Incident Querying, Keyword Search, CSV Export & Pearson Correlation Auditing",
    badge_text="DATABASE EXPLORER",
)

try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Failed to initialize core dataset pipeline: {e}")
    st.stop()

st.sidebar.subheader("🛠️ Data Grid Filtering Options")

min_year = int(df["iyear"].min()) if "iyear" in df.columns else 1970
max_year = int(df["iyear"].max()) if "iyear" in df.columns else 2020
if min_year < max_year:
    selected_years = st.sidebar.slider("Timeline Coverage Bounds:", min_year, max_year, (min_year, max_year))
else:
    selected_years = (min_year, max_year)

country_col = "country_txt" if "country_txt" in df.columns else "country"
available_countries = ["All"] + sorted(df[country_col].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Filter Country Jurisdiction:", options=available_countries)

attack_col = "attacktype1_txt" if "attacktype1_txt" in df.columns else "attacktype1"
available_attacks = ["All"] + sorted(df[attack_col].dropna().unique().tolist())
selected_attack = st.sidebar.selectbox("Filter Attack Method:", options=available_attacks)

keyword_query = st.sidebar.text_input("🔎 Keyword Search (City, Group, Target, Summary):", "")

filtered_df = df[(df["iyear"] >= selected_years[0]) & (df["iyear"] <= selected_years[1])]
if selected_country != "All":
    filtered_df = filtered_df[filtered_df[country_col] == selected_country]
if selected_attack != "All":
    filtered_df = filtered_df[filtered_df[attack_col] == selected_attack]

if keyword_query.strip():
    q = keyword_query.strip().lower()
    search_cols = [c for c in ["city", "provstate", "gname", "target1", "summary"] if c in filtered_df.columns]
    if search_cols:
        mask = pd.Series(False, index=filtered_df.index)
        for c in search_cols:
            mask = mask | filtered_df[c].astype(str).str.lower().str.contains(q, na=False)
        filtered_df = filtered_df[mask]

st.subheader("🎯 Active Dataset Overview")
col1, col2, col3, col4 = st.columns(4)

total_filtered = len(filtered_df)
fatalities = int(filtered_df["nkill"].fillna(0).sum()) if "nkill" in filtered_df.columns else 0
injuries = int(filtered_df["nwound"].fillna(0).sum()) if "nwound" in filtered_df.columns else 0
success_count = int(filtered_df["success"].sum()) if "success" in filtered_df.columns else 0

with col1:
    render_kpi_card("Isolated Record Count", f"{total_filtered:,}", "Matching Active Query", "#3b82f6")
with col2:
    render_kpi_card("Aggregated Fatalities", f"{fatalities:,}", "Total NKILL", "#ef4444")
with col3:
    render_kpi_card("Reported Injuries", f"{injuries:,}", "Total NWOUND", "#f59e0b")
with col4:
    render_kpi_card("Successful Incidents", f"{success_count:,}", "Tactical Completion", "#10b981")

st.subheader("📋 Searchable Global Incident Grid Matrix")
display_columns = [
    c
    for c in [
        "iyear",
        "imonth",
        "iday",
        "country_txt",
        "region_txt",
        "provstate",
        "city",
        "gname",
        "attacktype1_txt",
        "weaptype1_txt",
        "targtype1_txt",
        "nkill",
        "nwound",
        "success",
    ]
    if c in filtered_df.columns
]

if not filtered_df.empty:
    st.dataframe(
        filtered_df[display_columns].head(300),
        width='stretch',
        hide_index=True,
    )
    csv_export = filtered_df[display_columns].to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"📥 Export Filtered Records ({len(filtered_df):,} rows) as CSV",
        data=csv_export,
        file_name="GTD_Filtered_Records.csv",
        mime="text/csv",
    )
else:
    st.warning("⚠️ No cataloged dataset rows matched your filter parameter criteria sequence.")

st.markdown("---")
st.subheader("🧬 Variable Correlation Matrix Breakdown")

numeric_cols = [
    c
    for c in ["iyear", "extended", "crit1", "crit2", "crit3", "success", "suicide", "attacktype1", "targtype1", "weaptype1", "nkill", "nwound"]
    if c in filtered_df.columns
]

if len(numeric_cols) > 1 and not filtered_df.empty:
    corr_matrix = filtered_df[numeric_cols].corr().fillna(0)
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=".2f",
        aspect="auto",
        title="Pearson Correlation Coefficient Grid Mapping",
        color_continuous_scale="RdBu_r",
        range_color=[-1, 1],
        labels=dict(color="Correlation Score"),
    )
    fig_corr.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        margin=dict(l=40, r=40, t=50, b=40),
    )
    st.plotly_chart(fig_corr, width='stretch')
else:
    st.info("Insufficient variance metrics available under current filters to compute a Pearson coefficient heat matrix.")

render_footer(
    "**⚠️ METHODOLOGICAL SAFEGUARD NOTICE:** Statistical alignments and correlations represent strictly retrospective "
    "observation patterns from the GTD and must never be processed as real-time causality links."
)
