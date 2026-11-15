import folium
from folium.plugins import MarkerCluster, HeatMap


def create_base_map(center_lat=20.0, center_lon=0.0, zoom_start=2):
    """Initializes a standard dark-themed Folium map for intelligence visualization."""
    return folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles="cartodbdarkmatter",
        control_scale=True,
    )


def add_marker_cluster(folium_map, df, max_points=1000):
    """Groups and renders individual interactive incident pinpoint clusters onto the map."""
    coord_data = df.dropna(subset=["latitude", "longitude"]).copy()
    if coord_data.empty:
        return folium_map

    marker_cluster = MarkerCluster(name="Incident Clusters").add_to(folium_map)
    sample_df = coord_data.head(max_points)

    for _, row in sample_df.iterrows():
        country = row.get("country_txt", "Unknown")
        city = row.get("city", "Unknown")
        year = row.get("iyear", "Unknown")
        group = row.get("gname", "Unknown")
        attack = row.get("attacktype1_txt", "Unknown")
        weapon = row.get("weaptype1_txt", "Unknown")
        kills = int(row.get("nkill", 0) or 0)
        wounds = int(row.get("nwound", 0) or 0)
        casualties = kills + wounds

        pin_color = "darkred" if casualties >= 20 else ("red" if casualties > 0 else "orange")

        popup_text = f"""
        <div style='font-family: Segoe UI, Arial, sans-serif; font-size: 12px; color: #0f172a; line-height: 1.45;'>
            <div style='font-weight: 700; font-size: 13px; color: #1e3a8a; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-bottom: 6px;'>
                📍 {city}, {country} ({year})
            </div>
            <b>Perpetrator:</b> {group}<br>
            <b>Attack Vector:</b> {attack}<br>
            <b>Weapon Class:</b> {weapon}<br>
            <b>Casualties:</b> <span style='color:#dc2626; font-weight:700;'>{kills} Killed / {wounds} Wounded</span>
        </div>
        """

        folium.Marker(
            location=[float(row["latitude"]), float(row["longitude"])],
            popup=folium.Popup(popup_text, max_width=320),
            tooltip=f"{city}, {country} • {attack} ({casualties} casualties)",
            icon=folium.Icon(color=pin_color, icon="info-sign"),
        ).add_to(marker_cluster)

    return folium_map


def add_heatmap_layer(folium_map, df, max_points=3000):
    """Renders a thermal geospatial density and casualty-weighted heatmap layer."""
    coord_data = df.dropna(subset=["latitude", "longitude"]).copy()
    if coord_data.empty:
        return folium_map

    sample_df = coord_data.head(max_points)
    heat_data = []
    for _, row in sample_df.iterrows():
        lat = float(row["latitude"])
        lon = float(row["longitude"])
        weight = float((row.get("nkill", 0) or 0) + (row.get("nwound", 0) or 0) + 1.0)
        heat_data.append([lat, lon, min(weight, 50.0)])

    HeatMap(
        heat_data,
        name="Thermal Threat Density",
        radius=16,
        blur=22,
        min_opacity=0.35,
    ).add_to(folium_map)

    return folium_map
