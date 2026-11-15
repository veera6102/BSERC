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
from streamlit_folium import st_folium
from utils.data_loader import load_data
from utils.map_utils import create_base_map, add_marker_cluster

# ==============================================================================
# 3. INTERACTIVE MAP RENDERING
# ==============================================================================
st.title("🗺️ Global Threat Intelligence Map")
st.markdown("Visualizing tactical hotspots and geo-spatial operation distribution patterns globally.")

# Fetch cached dataset framework
df = load_data()

# Add a year filter sidebar tool to make the map super responsive
st.sidebar.subheader("Map Visual Filters")
years = sorted(df["iyear"].unique().tolist(), reverse=True)
selected_year = st.sidebar.selectbox("Select Target Year Focus", years, index=0)

# Filter dataframe based on selection
map_df = df[df["iyear"] == selected_year]

st.subheader(f"📍 Operational Mapping Layer — Year {selected_year}")

# Generate maps using your utilities
base_map = create_base_map()
final_map = add_marker_cluster(base_map, map_df)

# Render map directly inside your Streamlit UI frame
st_folium(final_map, width=1100, height=600, returned_objects=[])