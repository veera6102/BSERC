import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

# 1. Page Configuration
st.set_page_config(
    page_title="Home Dashboard | Threat Intelligence",
    page_icon="🏠",
    layout="wide"
)

st.markdown("<h1 class='glow-text'>🏠 Operational Intelligence Summary Index</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8;font-size:1.1rem;'>Global Overview, High-Value Metrics Summary, and Macro Incident Trajectories.</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:rgba(59, 130, 246, 0.2);'>", unsafe_allow_html=True)

# 2. Safely Load Master Data Context
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Failed to initialize core dataset pipeline on Home view: {e}")
    st.stop()

# 3. Core KPI Card Aggregation Metrics
st.subheader("📊 Global High-Level Vector Totals")
col1, col2, col3, col4 = st.columns(4)

total_incidents = len(df)
total_fatalities = int(df['nkill'].fillna(0).sum()) if 'nkill' in df.columns else 0
total_injuries = int(df['nwound'].fillna(0).sum()) if 'nwound' in df.columns else 0
overall_success_rate = (df['success'].sum() / total_incidents * 100) if 'success' in df.columns and total_incidents > 0 else 0.0

with col1:
    st.metric(label="Aggregated Records Logged", value=f"{total_incidents:,}")
with col2:
    st.metric(label="Confirmed Fatalities (NKILL)", value=f"{total_fatalities:,}")
with col3:
    st.metric(label="Reported Injuries (NWOUND)", value=f"{total_injuries:,}")
with col4:
    st.metric(label="Overall Operational Success Rate", value=f"{overall_success_rate:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# 4. Macro Layout Matrix Split (Yearly Volume Trend & Top 5 Risk Regions)
st.subheader("📈 Macroscopic Frequency & Risk Concentrations")
left_col, right_col = st.columns(2)

with left_col:
    st.markdown("#### Chronological Global Incident Volume (1970-2020)")
    yearly_counts = df.groupby('iyear').size().reset_index(name='Incident Count')
    
    fig_yearly = px.line(
        yearly_counts,
        x='iyear',
        y='Incident Count',
        labels={'iyear': 'Historical Year', 'Incident Count': 'Incidents Count'},
        markers=True
    )
    fig_yearly.update_traces(line=dict(color='#3b82f6', width=3), marker=dict(size=4, color='#ef4444'))
    fig_yearly.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        margin=dict(l=40, r=40, t=20, b=40),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
    )
    st.plotly_chart(fig_yearly, use_container_width=True)

with right_col:
    st.markdown("#### Top 5 Highest Concentration Regional Zones")
    region_col = "region_txt" if "region_txt" in df.columns else "region"
    top_regions = df[region_col].value_counts().reset_index().head(5)
    top_regions.columns = [region_col, 'Count']
    
    fig_regions = px.bar(
        top_regions,
        x='Count',
        y=region_col,
        orientation='h',
        labels={region_col: 'Geographical Region', 'Count': 'Incident Counts'},
        color='Count',
        color_continuous_scale="Blugrn"
    )
    fig_regions.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        margin=dict(l=40, r=40, t=20, b=40),
        coloraxis_showscale=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig_regions, use_container_width=True)

# 5. Methodological Safeguard Notice
st.markdown("<br><hr style='border-color:rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
st.warning(
    """
    **⚠️ METHODOLOGICAL SAFEGUARD NOTICE:** All global metrics, counts, and statistical trendlines displayed 
    on this platform consist entirely of rule-based historical summaries derived from the Global Terrorism Database (GTD). 
    
    These metrics represent strictly retrospective patterns spanning historical data limits (1970-2020). 
    They do not factor in dynamic real-world intelligence updates or changing localized defensive postures, 
    and **must never** be leveraged to model forward-looking physical threats or assets risks.
    """
)