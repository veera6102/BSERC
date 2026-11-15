import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

import streamlit as st
from streamlit_folium import st_folium
from utils.data_loader import load_data
from utils.map_utils import create_base_map, add_marker_cluster, add_heatmap_layer
from utils.dashboard_metrics import render_page_header, render_kpi_card, render_footer

st.set_page_config(
    page_title="Global Threat Map | Threat Intelligence",
    page_icon="🗺️",
    layout="wide",
)

render_page_header(
    title="🗺️ Global Geospatial Threat Intelligence Map",
    subtitle="Interactive Pinpoint Cluster Mapping, Thermal Casualty Density Layers & Hotspot Telemetry",
    badge_text="GEO-INTELLIGENCE LAYER",
)

df = load_data()

# Sidebar Geospatial Filters
st.sidebar.subheader("🛰️ Geospatial Filter Controls")

years = ["All Years"] + sorted(df["iyear"].dropna().unique().astype(int).tolist(), reverse=True)
selected_year = st.sidebar.selectbox("Select Target Year Focus", years, index=0)

regions = ["All Regions"] + sorted(df["region_txt"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Filter Region", regions, index=0)

attacks = ["All Attack Vectors"] + sorted(df["attacktype1_txt"].dropna().unique().tolist())
selected_attack = st.sidebar.selectbox("Filter Attack Vector", attacks, index=0)

map_mode = st.sidebar.radio(
    "Visualization Layer Mode",
    options=["Cluster Markers + Thermal Heatmap", "Incident Marker Clusters Only", "Thermal Density Heatmap Only"],
    index=0,
)

max_markers = st.sidebar.slider("Max Plotted Coordinates", min_value=200, max_value=2500, value=1000, step=100)

# Apply Filters
map_df = df.copy()
if selected_year != "All Years":
    map_df = map_df[map_df["iyear"] == int(selected_year)]
if selected_region != "All Regions":
    map_df = map_df[map_df["region_txt"] == selected_region]
if selected_attack != "All Attack Vectors":
    map_df = map_df[map_df["attacktype1_txt"] == selected_attack]

coord_df = map_df.dropna(subset=["latitude", "longitude"])

# Geospatial Summary Strip
k1, k2, k3, k4 = st.columns(4)
with k1:
    render_kpi_card("Filtered Incidents", f"{len(map_df):,}", f"{len(coord_df):,} Geo-Referenced", "#3b82f6")
with k2:
    hotspot_country = str(map_df["country_txt"].mode().iloc[0]) if not map_df.empty else "N/A"
    render_kpi_card("Primary Hotspot Country", hotspot_country, "Highest Incident Density", "#ef4444")
with k3:
    hotspot_city = (
        str(map_df[map_df["city"].notna() & (map_df["city"] != "Unknown")]["city"].mode().iloc[0])
        if not map_df.empty and not map_df[map_df["city"].notna() & (map_df["city"] != "Unknown")].empty
        else "N/A"
    )
    render_kpi_card("Epicenter Urban Node", hotspot_city, "Most Frequent City", "#f59e0b")
with k4:
    total_cas = int(map_df["total_casualties"].sum()) if "total_casualties" in map_df.columns else 0
    render_kpi_card("Zone Casualties", f"{total_cas:,}", "Killed + Wounded in Scope", "#10b981")

st.subheader(f"📍 Operational Mapping Canvas — {selected_year} • {selected_region}")

if coord_df.empty:
    st.warning("⚠️ No valid latitude/longitude coordinates found for the current filter selection.")
else:
    center_lat = float(coord_df["latitude"].mean())
    center_lon = float(coord_df["longitude"].mean())
    zoom = 3 if selected_region != "All Regions" else 2

    base_map = create_base_map(center_lat=center_lat, center_lon=center_lon, zoom_start=zoom)

    if "Cluster" in map_mode:
        base_map = add_marker_cluster(base_map, coord_df, max_points=max_markers)
    if "Heatmap" in map_mode:
        base_map = add_heatmap_layer(base_map, coord_df, max_points=max_markers * 2)

    st_folium(base_map, use_container_width=True, height=580, returned_objects=[])

render_footer(
    "**⚠️ GEOSPATIAL NOTICE:** Coordinates reflect historical incident locations recorded in the GTD. "
    "Markers are capped at the configured threshold to preserve real-time browser rendering performance."
)
