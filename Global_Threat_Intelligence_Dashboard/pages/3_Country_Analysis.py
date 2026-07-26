import sys
from pathlib import Path

# ==============================================================================
# 1. PATH RESOLUTION INJECTION (Must stand before custom local imports)
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# ==============================================================================
# 2. APPLICATION IMPORTS
# ==============================================================================
import streamlit as st
from utils.data_loader import load_data
from utils.charts import line_chart, bar_chart

# ==============================================================================
# 3. INTERACTIVE COUNTRY BREIFING MODULE
# ==============================================================================
st.title("📊 Country Intelligence Analysis")
st.markdown("Select a specific country from the sidebar to view localized timelines, tactical profiles, and targeting vulnerabilities.")

# Fetch cached dataset framework
df = load_data()

# Identify the correct country column name
country_col = "country_txt" if "country_txt" in df.columns else "country"

# -----------------------------
# Sidebar Configuration Filters
# -----------------------------
st.sidebar.subheader("Country Analysis Filter")
country_list = sorted(df[country_col].dropna().unique().tolist())

# Default to India if available, otherwise pick the first item
default_index = country_list.index("India") if "India" in country_list else 0
selected_country = st.sidebar.selectbox("Select Target Country", country_list, index=default_index)

# Filter dataframe specifically for the selected country
country_df = df[df[country_col] == selected_country]

st.markdown("---")
st.header(f"🌍 Security Briefing: {selected_country}")

# -----------------------------
# Localized Metrics Summary Matrix
# -----------------------------
total_local_incidents = len(country_df)
local_groups = country_df["gname"].nunique() if "gname" in country_df.columns else 0
local_casualties = int(country_df["nkill"].fillna(0).sum() + country_df["nwound"].fillna(0).sum())

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="💥 Country Incidents", value=f"{total_local_incidents:,}")
with col2:
    st.metric(label="👥 Active Groups Detected", value=f"{local_groups:,}")
with col3:
    st.metric(label="☠️ Localized Casualties", value=f"{local_casualties:,}")

st.markdown("---")

# -----------------------------
# Visual Analytics Sub-Grid
# -----------------------------
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("📈 Localized Incident Timeline")
    yearly_local = country_df.groupby("iyear").size().reset_index(name="Incident Count")
    
    # Render modular line chart
    fig_local_trend = line_chart(
        df=yearly_local,
        x_col="iyear",
        y_col="Incident Count",
        title=f"Incident Progression over Time in {selected_country}"
    )
    st.plotly_chart(fig_local_trend, use_container_width=True)

with right_col:
    st.subheader("⚔️ Primary Attack Typologies")
    attack_col = "attacktype1_txt" if "attacktype1_txt" in country_df.columns else "attacktype"
    attack_types = country_df[attack_col].value_counts().head(7).reset_index()
    attack_types.columns = [attack_col, "Count"]
    
    # Render modular horizontal bar chart
    fig_attack_bar = bar_chart(
        df=attack_types,
        x_col=attack_col,
        y_col="Count",
        title=f"Top 7 Operational Tactics in {selected_country}",
        orientation="h"
    )
    st.plotly_chart(fig_attack_bar, use_container_width=True)

# -----------------------------
# Secondary Visual Breakdown Row
# -----------------------------
st.markdown("---")
lower_left_col, lower_right_col = st.columns(2)

with lower_left_col:
    st.subheader("🔫 Dominant Weapons Architecture")
    weapon_col = "weaptype1_txt" if "weaptype1_txt" in country_df.columns else "weaptype"
    weapon_types = country_df[weapon_col].value_counts().head(7).reset_index()
    weapon_types.columns = [weapon_col, "Count"]
    
    # Render modular vertical bar chart
    fig_weapon_bar = bar_chart(
        df=weapon_types,
        x_col=weapon_col,
        y_col="Count",
        title="Weapon Categories Utilized",
        orientation="v"
    )
    st.plotly_chart(fig_weapon_bar, use_container_width=True)

with lower_right_col:
    st.subheader("🎯 Threat Vulnerability Targets")
    target_col = "targtype1_txt" if "targtype1_txt" in country_df.columns else "targtype"
    target_types = country_df[target_col].value_counts().head(7).reset_index()
    target_types.columns = [target_col, "Count"]
    
    # Render modular horizontal bar chart
    fig_target_bar = bar_chart(
        df=target_types,
        x_col=target_col,
        y_col="Count",
        title="Sector Vulnerability Profiles",
        orientation="h"
    )
    st.plotly_chart(fig_target_bar, use_container_width=True)