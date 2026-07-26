import folium
from folium.plugins import MarkerCluster, HeatMap

def create_base_map(center_lat=20.0, center_lon=0.0, zoom_start=2):
    """
    Initializes a standard dark-themed Folium map for intelligence visualization.
    """
    return folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles="cartodbdarkmatter",
        control_scale=True
    )

def add_marker_cluster(folium_map, df):
    """
    Groups and renders individual interactive incident pinpoint clusters onto the map.
    """
    # Filter rows with valid coordinates
    coord_data = df.dropna(subset=["latitude", "longitude"])
    
    marker_cluster = MarkerCluster(name="Incident Clusters").add_to(folium_map)
    
    # Limit to top 1000 records for map performance if dataset is massive
    sample_df = coord_data.head(1000)
    
    for _, row in sample_df.iterrows():
        country = row.get("country_txt", "Unknown")
        year = row.get("iyear", "Unknown")
        group = row.get("gname", "Unknown")
        attack = row.get("attacktype1_txt", "Unknown")
        
        popup_text = f"""
        <div style='font-family: Arial, sans-serif; font-size: 12px; color: #333;'>
            <b>Year:</b> {year}<br>
            <b>Country:</b> {country}<br>
            <b>Group:</b> {group}<br>
            <b>Attack Type:</b> {attack}
        </div>
        """
        
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(marker_cluster)
        
    return folium_map