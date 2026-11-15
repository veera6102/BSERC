import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

# 1. Page Configuration
st.set_page_config(
    page_title="Weapon Analysis | Threat Intelligence",
    page_icon="⚔️",
    layout="wide"
)

st.markdown("<h1 class='glow-text'>⚔️ Weapon Profile & Tactical Vector Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8;font-size:1.1rem;'>Analyze historical weapon types, distribution metrics, and chronological development trends.</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:rgba(59, 130, 246, 0.2);'>", unsafe_allow_html=True)

# 2. Safely Load Master Data Context
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Failed to initialize core dataset pipeline: {e}")
    st.stop()

# Ensure standard weapon column mapping
weap_col = "weaptype1_txt" if "weaptype1_txt" in df.columns else "weapon_type"
df_clean = df[df[weap_col].notna() & (df[weap_col] != "Unknown")].copy()

# 3. Macro Metrics & Global Breakdown
unique_weapons = df_clean[weap_col].nunique()
st.metric(label="Total Unique Weapon Frameworks Categorized", value=f"{unique_weapons}")

st.markdown("---")
st.subheader("📊 Top Weapon Types (Overall Volume)")

# Aggregate top overall weapon types
top_weapons = df_clean[weap_col].value_counts().reset_index()
top_weapons.columns = [weap_col, 'Count']

fig_top_weapons = px.bar(
    top_weapons.head(10),
    x='Count',
    y=weap_col,
    orientation='h',
    title="Top Weapon Profile Classifications",
    labels={weap_col: 'Weapon Classification', 'Count': 'Incident Volume'},
    color='Count',
    color_continuous_scale="Reds"
)
fig_top_weapons.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15, 23, 42, 0.5)",
    coloraxis_showscale=False,
    yaxis={'categoryorder': 'total ascending'}
)
st.plotly_chart(fig_top_weapons, use_container_width=True)

st.markdown("---")

# 4. Filter Selection Framework
st.subheader("🔍 Weapon Type Specific Deep Dive")
available_weapons = sorted(df_clean[weap_col].unique())

# Set default selection to "Explosives" or similar common class if available
default_idx = available_weapons.index("Explosives") if "Explosives" in available_weapons else 0

selected_weapon = st.selectbox(
    "Select Weapon Category to Profile:",
    options=available_weapons,
    index=default_idx
)

# Isolate historical data slice matching selection
filtered_df = df_clean[df_clean[weap_col] == selected_weapon].copy()

# 5. Dual Column Chart Layout (Yearly Trend & Geographic Distribution)
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Yearly Trend (Line Chart)")
    yearly_trend = filtered_df.groupby('iyear').size().reset_index(name='Incident Count')
    
    if not yearly_trend.empty:
        fig_trend = px.line(
            yearly_trend,
            x='iyear',
            y='Incident Count',
            title=f"Chronological Timeline Trajectory for: {selected_weapon}",
            labels={'iyear': 'Timeline Year', 'Incident Count': 'Incident Volume'},
            markers=True
        )
        fig_trend.update_traces(line=dict(color='#ef4444', width=3))
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
    st.markdown("#### Top Countries (Bar Chart)")
    country_col = "country_txt" if "country_txt" in filtered_df.columns else "country"
    top_countries = filtered_df[country_col].value_counts().reset_index().head(10)
    top_countries.columns = [country_col, 'Count']
    
    if not top_countries.empty:
        fig_countries = px.bar(
            top_countries,
            x='Count',
            y=country_col,
            orientation='h',
            title=f"Highest Utilization Risk Regions: {selected_weapon}",
            labels={country_col: 'Country Jurisdiction', 'Count': 'Incident Volume'},
            color='Count',
            color_continuous_scale="Oranges"
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
        st.info("No jurisdiction metadata entries found for this weapon subset.")

st.markdown("---")

# 6. Raw Filtered Data Frame Summary View
st.subheader("📋 Filtered Data Table Reference")
st.markdown("Review operational micro-level records filtered under current weapon profile:")

# Safely extract core reference rows
display_cols = [c for c in ['iyear', 'country_txt', 'region_txt', 'gname', 'attacktype1_txt', 'targtype1_txt', 'nkill', 'nwound'] if c in filtered_df.columns]
if not filtered_df.empty:
    st.dataframe(
        filtered_df[display_cols].head(100),
        use_container_width=True
    )
else:
    st.info("No database line entries found matching target weapon boundaries.")

# 7. Methodological Safeguard Disclaimer
st.markdown("<br><hr style='border-color:rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
st.warning(
    """
    **⚠️ METHODOLOGICAL SAFEGUARD NOTICE:** Weapon metrics and deployment trend frequencies displayed on this 
    interface consist entirely of historical rule-based data summaries computed from the Global Terrorism Database (GTD). 
    
    These visualizations are provided to analyze historical vector patterns for security research and retrospectives. 
    They do not model dynamic military capabilities, active weapon trade flows, or real-time asset logistics, 
    and **must not** be utilized to derive tactical counter-measures or forecast current deployment risks.
    """
)