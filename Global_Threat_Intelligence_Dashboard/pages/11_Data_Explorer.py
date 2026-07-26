import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.data_loader import load_data

# 1. Page Configuration
st.set_page_config(
    page_title="Data Explorer | Threat Intelligence",
    page_icon="🔍",
    layout="wide"
)

st.markdown("<h1 class='glow-text'>🔍 Master Data Explorer & Distribution Matrix</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8;font-size:1.1rem;'>Query raw database line entries, explore record distributions, and audit statistical data attribute correlations.</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:rgba(59, 130, 246, 0.2);'>", unsafe_allow_html=True)

# 2. Safely Load Master Data Context
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Failed to initialize core dataset pipeline: {e}")
    st.stop()

# 3. Sidebar/Filter Panel Controls
st.sidebar.subheader("🛠️ Data Grid Filtering Options")

# Numerical Year Filtering Slider Bounds
min_year = int(df['iyear'].min()) if 'iyear' in df.columns else 1970
max_year = int(df['iyear'].max()) if 'iyear' in df.columns else 2020
selected_years = st.sidebar.slider("Select Timeline Coverage Bounds:", min_year, max_year, (min_year, max_year))

# Categorical Country Filter Scope
country_col = "country_txt" if "country_txt" in df.columns else "country"
available_countries = ["All"] + sorted(df[country_col].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Filter Target Country Jurisdiction:", options=available_countries)

# Apply Active Selection Logic Filters
filtered_df = df[(df['iyear'] >= selected_years[0]) & (df['iyear'] <= selected_years[1])]
if selected_country != "All":
    filtered_df = filtered_df[filtered_df[country_col] == selected_country]

# 4. Macro Metric Callouts
st.subheader("🎯 Active Dataset Overview")
col1, col2, col3, col4 = st.columns(4)

total_filtered = len(filtered_df)
fatalities = int(filtered_df['nkill'].fillna(0).sum()) if 'nkill' in filtered_df.columns else 0
injuries = int(filtered_df['nwound'].fillna(0).sum()) if 'nwound' in filtered_df.columns else 0
success_count = int(filtered_df['success'].sum()) if 'success' in filtered_df.columns else 0

with col1:
    st.metric(label="Isolated Record Count", value=f"{total_filtered:,}")
with col2:
    st.metric(label="Aggregated Fatalities (NKILL)", value=f"{fatalities:,}")
with col3:
    st.metric(label="Reported Injuries (NWOUND)", value=f"{injuries:,}")
with col4:
    st.metric(label="Successful Incidents Logged", value=f"{success_count:,}")

st.markdown("<br>", unsafe_allow_html=True)

# 5. Searchable Interactive Streamlit Dataframe Table
st.subheader("📋 Searchable Global Incident Grid Matrix")
st.markdown("Use the filtering search box below or download the parsed slice via standard file options:")

# Clean and slice visible columns array map safely
display_columns = [c for c in ['iyear', 'country_txt', 'region_txt', 'provstate', 'city', 'gname', 'attacktype1_txt', 'weaptype1_txt', 'targtype1_txt', 'nkill', 'nwound', 'success'] if c in filtered_df.columns]

if not filtered_df.empty:
    st.dataframe(
        filtered_df[display_columns].head(250), # Limit layout rendering cap for page responsiveness
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("⚠️ No cataloged dataset rows matched your filter parameter criteria sequence.")

st.markdown("<br><hr style='border-color:rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

# 6. Statistical Correlation Matrix Layout Heatmap
st.subheader("🧬 Variable Correlation Matrix Breakdown")
st.markdown("Analyzes the operational linear correlation weights across localized data metrics:")

# Isolate clean numerical properties explicitly
numeric_cols = [c for c in ['iyear', 'extended', 'crit1', 'crit2', 'crit3', 'success', 'suicide', 'attacktype1', 'targtype1', 'weaptype1', 'nkill', 'nwound'] if c in filtered_df.columns]

if len(numeric_cols) > 1 and not filtered_df.empty:
    # Calculate DataFrame Correlation Coefficients
    corr_matrix = filtered_df[numeric_cols].corr().fillna(0)
    
    # Generate Interactive Heatmap Configuration
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=".2f",
        aspect="auto",
        title="Pearson Correlation Coefficient Grid Mapping",
        color_continuous_scale="RdBu_r",
        range_color=[-1, 1],
        labels=dict(color="Correlation Score")
    )
    
    fig_corr.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("Insufficient variance metrics available under current filters to compute a Pearson coefficient heat matrix.")

# 7. Methodological Safeguard Disclaimer Notice
st.markdown("<br><hr style='border-color:rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
st.warning(
    """
    **⚠️ METHODOLOGICAL SAFEGUARD NOTICE:** The records, data properties, dataframes, and correlation metrics 
    displayed on this interface consist of historical data attributes from the Global Terrorism Database (GTD). 
    
    Statistical alignments and correlations represent strictly retrospective observation patterns (1970-2020) and **must never** 
    be processed as direct real-time causality links, prospective tactical intelligence projections, or structural forecasts.
    """
)