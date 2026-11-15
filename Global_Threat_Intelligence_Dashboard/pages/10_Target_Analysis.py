import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

# 1. Page Configuration
st.set_page_config(
    page_title="Target Analysis | Threat Intelligence",
    page_icon="🎯",
    layout="wide"
)

st.markdown("<h1 class='glow-text'>🎯 Target Analysis & Asset Vulnerability Profiles</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8;font-size:1.1rem;'>Investigate historical distribution matrices, timeline trends, and geographic vulnerabilities by target infrastructure sector.</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:rgba(59, 130, 246, 0.2);'>", unsafe_allow_html=True)

# 2. Safely Load Master Data Context
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Failed to initialize core dataset pipeline: {e}")
    st.stop()

# Ensure standard target column mapping
targ_col = "targtype1_txt" if "targtype1_txt" in df.columns else "target_type"
df_clean = df[df[targ_col].notna() & (df[targ_col] != "Unknown")].copy()

# 3. Macro Metrics KPI Block
unique_targets = df_clean[targ_col].nunique()
st.metric(label="Total Unique Target Environments Categorized", value=f"{unique_targets}")

st.markdown("---")

# 4. Top 10 Target Classes Bar Chart Breakdown
st.subheader("📊 Top Target Types (Overall Volume)")

top_targets = df_clean[targ_col].value_counts().reset_index()
top_targets.columns = [targ_col, 'Count']

fig_top_targets = px.bar(
    top_targets.head(10),
    x='Count',
    y=targ_col,
    orientation='h',
    title="Top 10 Targeted Infrastructure Sectors",
    labels={targ_col: 'Target Environment Sector', 'Count': 'Incident Volume'},
    color='Count',
    color_continuous_scale="Viridis"
)
fig_top_targets.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15, 23, 42, 0.5)",
    coloraxis_showscale=False,
    yaxis={'categoryorder': 'total ascending'}
)
st.plotly_chart(fig_top_targets, use_container_width=True)

st.markdown("---")

# 5. Interactive Select Target Filter Dropdown
st.subheader("🎯 Deep Dive Filter Profile")
available_targets = sorted(df_clean[targ_col].unique())

# Default dropdown placement safely set to "Private Citizens & Property" or similar common node
default_idx = available_targets.index("Private Citizens & Property") if "Private Citizens & Property" in available_targets else 0

selected_target = st.selectbox(
    "Select Target Profile to Inspect:",
    options=available_targets,
    index=default_idx,
    key="target_selector_dropdown"
)

# Isolate selection dataset rows
filtered_df = df_clean[df_clean[targ_col] == selected_target].copy()

# 6. Dual Visualization Grid (Timeline Trend & Top Impacted Countries)
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Chronological Target Trend (Line Chart)")
    yearly_trend = filtered_df.groupby('iyear').size().reset_index(name='Incident Count')
    
    if not yearly_trend.empty:
        fig_trend = px.line(
            yearly_trend,
            x='iyear',
            y='Incident Count',
            title=f"Incident Frequency Trajectory for: {selected_target}",
            labels={'iyear': 'Timeline Year', 'Incident Count': 'Incident Volume'},
            markers=True
        )
        fig_trend.update_traces(line=dict(color='#3b82f6', width=3), marker=dict(size=6, color='#ef4444'))
        fig_trend.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No timeline trajectory elements cataloged for this segment selection.")

with col2:
    st.markdown("#### Top Impacted Jurisdictions (Bar Chart)")
    country_col = "country_txt" if "country_txt" in filtered_df.columns else "country"
    top_countries = filtered_df[country_col].value_counts().reset_index().head(10)
    top_countries.columns = [country_col, 'Count']
    
    if not top_countries.empty:
        fig_countries = px.bar(
            top_countries,
            x='Count',
            y=country_col,
            orientation='h',
            title=f"Highest Risk Concentration Areas: {selected_target}",
            labels={country_col: 'Country Jurisdiction', 'Count': 'Incident Volume'},
            color='Count',
            color_continuous_scale="MutedBlues"
        )
        fig_countries.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            coloraxis_showscale=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_countries, use_container_width=True)
    else:
        st.info("No jurisdiction metadata entries found for this target infrastructure subset.")

st.markdown("---")

# 7. Raw Filtered Data View Matrix Table
st.subheader("📋 Filtered Data (Table Source Reference)")
st.markdown("Review operational micro-level metrics extracted under current environment filters:")

# Pick standard column array targets safely
display_cols = [c for c in ['iyear', 'country_txt', 'region_txt', 'gname', 'attacktype1_txt', 'weaptype1_txt', 'nkill', 'nwound'] if c in filtered_df.columns]
if not filtered_df.empty:
    st.dataframe(
        filtered_df[display_cols].head(100),
        use_container_width=True
    )
else:
    st.info("No database line entries found matching target filter criteria boundaries.")

# 8. Methodological Safeguard Disclaimer
st.markdown("<br><hr style='border-color:rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
st.warning(
    """
    **⚠️ METHODOLOGICAL SAFEGUARD NOTICE:** Target categorization trends and risk frequencies displayed on this 
    interface consist entirely of historical rule-based data summaries computed from the Global Terrorism Database (GTD). 
    
    These visualizations are provided to identify macroscopic retrospective vulnerability vectors for civil defense research and audits. 
    They do not model forward-looking vectors, security gaps, or real-time asset conditions, and **must not** be utilized to derive 
    tactical infrastructure protection measures or forecast active physical threats.
    """
)