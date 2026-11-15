import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_data
from utils.charts import line_chart, bar_chart
from utils.dashboard_metrics import render_page_header, render_kpi_card, render_footer

st.set_page_config(
    page_title="Country Intelligence Analysis | Threat Intelligence",
    page_icon="📊",
    layout="wide",
)

render_page_header(
    title="📊 Country Intelligence & Comparative Analysis",
    subtitle="Localized National Security Briefings, City Hotspots, Active Groups & Bilateral Country Comparisons",
    badge_text="NATIONAL INTELLIGENCE",
)

df = load_data()
country_col = "country_txt" if "country_txt" in df.columns else "country"
country_list = sorted(df[country_col].dropna().unique().tolist())

st.sidebar.subheader("🌍 Country Selection Controls")
default_index = country_list.index("India") if "India" in country_list else (country_list.index("United States") if "United States" in country_list else 0)
selected_country = st.sidebar.selectbox("Select Primary Country", country_list, index=default_index)

compare_mode = st.sidebar.checkbox("⚖️ Enable Country-vs-Country Comparison", value=False)
second_country = None
if compare_mode:
    fallback_idx = 0 if default_index != 0 else min(1, len(country_list) - 1)
    second_country = st.sidebar.selectbox("Select Comparison Country", country_list, index=fallback_idx)

country_df = df[df[country_col] == selected_country]

st.header(f"🌍 National Security Briefing: {selected_country}")

total_local_incidents = len(country_df)
local_groups = (
    country_df[country_df["gname"] != "Unknown"]["gname"].nunique()
    if "gname" in country_df.columns
    else 0
)
local_kills = int(country_df["nkill"].fillna(0).sum())
local_wounds = int(country_df["nwound"].fillna(0).sum())
local_casualties = local_kills + local_wounds
local_success = float(country_df["success"].fillna(0).mean() * 100) if "success" in country_df.columns and total_local_incidents > 0 else 0.0

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Country Incidents", f"{total_local_incidents:,}", f"Share: {total_local_incidents / len(df) * 100:.1f}% of Global", "#3b82f6")
with c2:
    render_kpi_card("Known Threat Groups", f"{local_groups:,}", "Excluding Unattributed", "#f59e0b")
with c3:
    render_kpi_card("Localized Casualties", f"{local_casualties:,}", f"{local_kills:,} Killed • {local_wounds:,} Wounded", "#ef4444")
with c4:
    render_kpi_card("Tactical Success Rate", f"{local_success:.1f}%", f"Region: {country_df['region_txt'].iloc[0] if not country_df.empty else 'N/A'}", "#10b981")

# Optional Bilateral Country Comparison Panel
if compare_mode and second_country:
    comp_df = df[df[country_col] == second_country]
    st.markdown("---")
    st.subheader(f"⚖️ Bilateral Threat Comparison: {selected_country} vs. {second_country}")

    comp_col1, comp_col2 = st.columns(2)
    with comp_col1:
        y1 = country_df.groupby("iyear").size().reset_index(name="Incidents")
        y2 = comp_df.groupby("iyear").size().reset_index(name="Incidents")
        fig_cmp = go.Figure()
        fig_cmp.add_trace(go.Scatter(x=y1["iyear"], y=y1["Incidents"], mode="lines+markers", name=selected_country, line=dict(color="#3b82f6", width=3)))
        fig_cmp.add_trace(go.Scatter(x=y2["iyear"], y=y2["Incidents"], mode="lines+markers", name=second_country, line=dict(color="#f97316", width=3)))
        fig_cmp.update_layout(
            title="Yearly Incident Trajectory Comparison",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            hovermode="x unified",
        )
        st.plotly_chart(fig_cmp, width='stretch')

    with comp_col2:
        summary_cmp = pd.DataFrame({
            "Metric": ["Total Incidents", "Confirmed Fatalities", "Reported Injuries", "Known Threat Groups"],
            selected_country: [
                len(country_df),
                int(country_df["nkill"].sum()),
                int(country_df["nwound"].sum()),
                int(country_df[country_df["gname"] != "Unknown"]["gname"].nunique()),
            ],
            second_country: [
                len(comp_df),
                int(comp_df["nkill"].sum()),
                int(comp_df["nwound"].sum()),
                int(comp_df[comp_df["gname"] != "Unknown"]["gname"].nunique()),
            ],
        })
        st.markdown("#### Side-by-Side Operational Metrics")
        st.dataframe(summary_cmp, width='stretch', hide_index=True)

st.markdown("---")

# Visual Analytics Sub-Grid
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("📈 Localized Incident Timeline")
    yearly_local = country_df.groupby("iyear").size().reset_index(name="Incident Count")
    fig_local_trend = line_chart(
        df=yearly_local,
        x_col="iyear",
        y_col="Incident Count",
        title=f"Incident Progression over Time in {selected_country}",
    )
    st.plotly_chart(fig_local_trend, width='stretch')

with right_col:
    st.subheader("⚔️ Primary Attack Typologies")
    attack_col = "attacktype1_txt" if "attacktype1_txt" in country_df.columns else "attacktype"
    attack_types = country_df[attack_col].value_counts().head(7).reset_index()
    attack_types.columns = [attack_col, "Count"]
    fig_attack_bar = bar_chart(
        df=attack_types,
        x_col=attack_col,
        y_col="Count",
        title=f"Top 7 Operational Tactics in {selected_country}",
        orientation="h",
        color_scale="Blues",
    )
    st.plotly_chart(fig_attack_bar, width='stretch')

st.markdown("---")
lower_left_col, lower_right_col = st.columns(2)

with lower_left_col:
    st.subheader("🔫 Dominant Weapons Architecture")
    weapon_col = "weaptype1_txt" if "weaptype1_txt" in country_df.columns else "weaptype"
    weapon_types = country_df[weapon_col].value_counts().head(7).reset_index()
    weapon_types.columns = [weapon_col, "Count"]
    fig_weapon_bar = bar_chart(
        df=weapon_types,
        x_col=weapon_col,
        y_col="Count",
        title="Weapon Categories Utilized",
        orientation="v",
        color_scale="Reds",
    )
    st.plotly_chart(fig_weapon_bar, width='stretch')

with lower_right_col:
    st.subheader("🎯 Threat Vulnerability Targets")
    target_col = "targtype1_txt" if "targtype1_txt" in country_df.columns else "targtype"
    target_types = country_df[target_col].value_counts().head(7).reset_index()
    target_types.columns = [target_col, "Count"]
    fig_target_bar = bar_chart(
        df=target_types,
        x_col=target_col,
        y_col="Count",
        title="Sector Vulnerability Profiles",
        orientation="h",
        color_scale="Tealgrn",
    )
    st.plotly_chart(fig_target_bar, width='stretch')

# Top Cities & Active Groups Row
st.markdown("---")
city_col, group_col = st.columns(2)
with city_col:
    st.subheader("🏙️ Most Impacted Cities / Jurisdictions")
    if "city" in country_df.columns:
        cities = country_df[country_df["city"].notna() & (country_df["city"] != "Unknown")]["city"].value_counts().head(8).reset_index()
        cities.columns = ["City", "Incident Count"]
        st.dataframe(cities, width='stretch', hide_index=True)
with group_col:
    st.subheader("🪖 Most Active Perpetrator Groups")
    if "gname" in country_df.columns:
        groups = country_df[country_df["gname"].notna() & (country_df["gname"] != "Unknown")]["gname"].value_counts().head(8).reset_index()
        groups.columns = ["Perpetrator Group", "Incident Count"]
        st.dataframe(groups, width='stretch', hide_index=True)

render_footer(
    "**⚠️ NATIONAL BRIEFING DISCLAIMER:** Country-level profiles reflect historical records cataloged in the GTD "
    "and are intended strictly for retrospective security research."
)
