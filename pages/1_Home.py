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
from utils.dashboard_metrics import (
    render_page_header,
    render_kpi_card,
    compute_executive_summary,
    render_footer,
)
from utils.charts import donut_chart, bar_chart

# 1. Page Configuration
st.set_page_config(
    page_title="Home Dashboard | Threat Intelligence",
    page_icon="🏠",
    layout="wide",
)

render_page_header(
    title="🏠 Operational Intelligence Summary Index",
    subtitle="Global Macro Indicators, Multi-Vector Trajectories, Seasonality & Regional Risk Concentrations",
    badge_text="EXECUTIVE OVERVIEW",
)

# 2. Safely Load Master Data Context
try:
    raw_df = load_data()
except Exception as e:
    st.error(f"❌ Failed to initialize core dataset pipeline on Home view: {e}")
    st.stop()

# Sidebar Interactive Scope Filters
st.sidebar.header("🎛️ Executive Scope Filters")
min_y, max_y = int(raw_df["iyear"].min()), int(raw_df["iyear"].max())
if min_y < max_y:
    year_range = st.sidebar.slider("Timeline Range (Years)", min_y, max_y, (min_y, max_y))
else:
    year_range = (min_y, max_y)

region_col = "region_txt" if "region_txt" in raw_df.columns else "region"
all_regions = sorted(raw_df[region_col].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect(
    "Filter Geographical Regions",
    options=all_regions,
    default=all_regions,
)

df = raw_df[(raw_df["iyear"] >= year_range[0]) & (raw_df["iyear"] <= year_range[1])]
if selected_regions:
    df = df[df[region_col].isin(selected_regions)]

if df.empty:
    st.warning("⚠️ No incident records match the selected sidebar filters.")
    st.stop()

summary = compute_executive_summary(df)

# 3. Core KPI Card Aggregation Metrics (6 Cards)
st.subheader("📊 Global High-Level Vector Totals")
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    render_kpi_card("Incidents Logged", f"{summary['total_incidents']:,}", f"Peak Year: {summary['peak_year']}", "#3b82f6")
with c2:
    render_kpi_card("Confirmed Fatalities", f"{summary['total_fatalities']:,}", "Total NKILL", "#ef4444")
with c3:
    render_kpi_card("Reported Injuries", f"{summary['total_injuries']:,}", "Total NWOUND", "#f97316")
with c4:
    render_kpi_card("Combined Casualties", f"{summary['total_casualties']:,}", "Fatalities + Injuries", "#dc2626")
with c5:
    render_kpi_card("Success Rate", f"{summary['success_rate']:.1f}%", "Tactical Completion", "#10b981")
with c6:
    render_kpi_card("Suicide Attack Ratio", f"{summary['suicide_rate']:.2f}%", f"{summary['active_countries']} Countries", "#a855f7")

# Automated Intelligence Insight Callout
st.markdown(
    f"""
    <div class='insight-box'>
        <strong>🧠 Automated Intelligence Brief:</strong> Across the selected scope,
        <strong>{summary['top_region']}</strong> recorded the highest concentration of incidents, with
        <strong>{summary['top_country']}</strong> as the most impacted jurisdiction.
        The predominant tactical method was <strong>{summary['top_attack']}</strong> utilizing
        <strong>{summary['top_weapon']}</strong>, primarily targeting <strong>{summary['top_target']}</strong>.
    </div>
    """,
    unsafe_allow_html=True,
)

# 4. Macro Layout Matrix Split
tab1, tab2, tab3 = st.tabs([
    "📈 Chronological & Regional Concentration",
    "🎯 Attack Vector & Target Breakdown",
    "📅 Monthly Seasonality & Lethality Matrix",
])

with tab1:
    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown("#### Chronological Incident & Casualty Trajectory")
        yearly_stats = (
            df.groupby("iyear")
            .agg(
                Incidents=("eventid", "count"),
                Casualties=("total_casualties", "sum"),
            )
            .reset_index()
        )

        fig_yearly = go.Figure()
        fig_yearly.add_trace(
            go.Scatter(
                x=yearly_stats["iyear"],
                y=yearly_stats["Incidents"],
                mode="lines+markers",
                name="Incident Count",
                line=dict(color="#3b82f6", width=3),
                marker=dict(size=6, color="#60a5fa"),
            )
        )
        fig_yearly.add_trace(
            go.Scatter(
                x=yearly_stats["iyear"],
                y=yearly_stats["Casualties"],
                mode="lines+markers",
                name="Total Casualties",
                line=dict(color="#ef4444", width=2.5, dash="dot"),
                marker=dict(size=5, color="#f87171"),
            )
        )
        fig_yearly.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            margin=dict(l=30, r=30, t=25, b=35),
            hovermode="x unified",
            legend=dict(orientation="h", y=1.08, x=1, xanchor="right"),
            xaxis=dict(title="Year", gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(title="Volume", gridcolor="rgba(255,255,255,0.06)"),
        )
        st.plotly_chart(fig_yearly, width='stretch')

    with right_col:
        st.markdown("#### Highest Concentration Regional Zones")
        top_regions = df[region_col].value_counts().reset_index().head(8)
        top_regions.columns = [region_col, "Count"]

        fig_regions = px.bar(
            top_regions,
            x="Count",
            y=region_col,
            orientation="h",
            labels={region_col: "Geographical Region", "Count": "Incident Count"},
            color="Count",
            color_continuous_scale="Blugrn",
        )
        fig_regions.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            margin=dict(l=30, r=30, t=25, b=35),
            coloraxis_showscale=False,
            yaxis={"categoryorder": "total ascending"},
        )
        st.plotly_chart(fig_regions, width='stretch')

with tab2:
    c_left, c_right = st.columns(2)
    with c_left:
        atk_col = "attacktype1_txt" if "attacktype1_txt" in df.columns else "attacktype1"
        atk_df = df[atk_col].value_counts().head(7).reset_index()
        atk_df.columns = ["Attack Type", "Count"]
        st.plotly_chart(
            donut_chart(atk_df, "Attack Type", "Count", "Primary Attack Method Share"),
            width='stretch',
        )
    with c_right:
        targ_col = "targtype1_txt" if "targtype1_txt" in df.columns else "targtype1"
        targ_df = df[targ_col].value_counts().head(8).reset_index()
        targ_df.columns = ["Target Sector", "Count"]
        st.plotly_chart(
            bar_chart(targ_df, "Target Sector", "Count", "Top 8 Targeted Sectors", orientation="h", color_scale="Tealgrn"),
            width='stretch',
        )

with tab3:
    m_left, m_right = st.columns(2)
    with m_left:
        if "imonth" in df.columns:
            month_map = {
                1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
            }
            m_df = df[df["imonth"].isin(range(1, 13))].copy()
            m_counts = m_df.groupby("imonth").size().reindex(range(1, 13), fill_value=0).reset_index(name="Incidents")
            m_counts["Month"] = m_counts["imonth"].map(month_map)
            fig_m = px.bar(
                m_counts,
                x="Month",
                y="Incidents",
                title="Monthly Operational Tempo (Seasonality)",
                color="Incidents",
                color_continuous_scale="Blues",
                template="plotly_dark",
            )
            fig_m.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15, 23, 42, 0.5)",
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig_m, width='stretch')
    with m_right:
        top_c = (
            df.groupby("country_txt")
            .agg(Incidents=("eventid", "count"), Casualties=("total_casualties", "sum"))
            .sort_values(by="Incidents", ascending=False)
            .head(10)
            .reset_index()
        )
        fig_c = px.bar(
            top_c,
            x="country_txt",
            y=["Incidents", "Casualties"],
            barmode="group",
            title="Top 10 Countries: Incidents vs. Total Casualties",
            labels={"value": "Volume", "country_txt": "Country"},
            template="plotly_dark",
            color_discrete_sequence=["#3b82f6", "#ef4444"],
        )
        fig_c.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
        )
        st.plotly_chart(fig_c, width='stretch')

render_footer(
    "**⚠️ METHODOLOGICAL SAFEGUARD NOTICE:** All global metrics, counts, and statistical trendlines displayed "
    "on this platform consist entirely of rule-based historical summaries derived from the Global Terrorism Database (GTD). "
    "They represent strictly retrospective patterns and must never be leveraged to forecast forward-looking physical threats."
)
