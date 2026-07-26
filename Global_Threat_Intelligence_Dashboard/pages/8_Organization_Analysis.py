import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.organization_analysis import (
    top_organizations,
    organization_yearly,
    organization_attack_types,
    organization_weapons
)

# 1. Page Configuration
st.set_page_config(
    page_title="Organization Analysis | Threat Intelligence",
    page_icon="🪖",
    layout="wide"
)

st.markdown("<h1 class='glow-text'>🪖 Perpetrator Organization Tactical Profiles</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8;font-size:1.1rem;'>Analyze historical timeline trajectories, attack volumes, and tactical signatures for specific perpetrator groups.</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:rgba(59, 130, 246, 0.2);'>", unsafe_allow_html=True)

# 2. Load Core Data Stream Safely
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Failed to initialize dataset pipeline: {e}")
    st.stop()

# 3. Organization Filter Selection Panel
st.subheader("🔍 Select Target Group Profile")
top_orgs_list = top_organizations(df, n=50)

selected_org = st.selectbox(
    "Choose Perpetrator Organization for Profiling:",
    options=top_orgs_list,
    index=0,
    help="Select an organization to dissect its tactical fingerprint based on historical data parameters."
)

st.markdown("<br>", unsafe_allow_html=True)

# 4. Generate Analytics Arrays via utils layer
df_yearly = organization_yearly(df, selected_org)
df_attacks = organization_attack_types(df, selected_org)
df_weapons = organization_weapons(df, selected_org)

# 5. Historical Timeline Trend Line Plot
st.subheader("📈 Historical Activity Timeline Trajectory")
if not df_yearly.empty:
    fig_timeline = px.line(
        df_yearly,
        x='Year',
        y='Count',
        title=f"Chronological Incident Frequency Pattern for {selected_org} (1970-2020)",
        labels={'Year': 'Timeline Year', 'Count': 'Incident Volume'},
        markers=True
    )
    fig_timeline.update_traces(line=dict(color='#3b82f6', width=3), marker=dict(size=6, color='#ef4444'))
    fig_timeline.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)"
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
else:
    st.info("No timeline metrics cataloged for selection.")

st.markdown("<br>", unsafe_allow_html=True)

# 6. Tactical Breakdown Split View Layout Columns
st.subheader("🧬 Tactical Signature & Vector Analysis")
left_chart, right_chart = st.columns(2)

with left_chart:
    st.markdown("#### Preferred Weapon Framework Profiles")
    if not df_weapons.empty:
        fig_weapon = px.bar(
            df_weapons.head(10),
            x='Count',
            y='Weapon',
            orientation='h',
            color='Count',
            color_continuous_scale="Reds"
        )
        fig_weapon.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15, 23, 42, 0.5)", coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_weapon, use_container_width=True)

with right_chart:
    st.markdown("#### Primary Attack Vector Frameworks")
    if not df_attacks.empty:
        fig_attack = px.bar(
            df_attacks.head(10),
            x='Count',
            y='Attack Type',
            orientation='h',
            color='Count',
            color_continuous_scale="Blues"
        )
        fig_attack.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15, 23, 42, 0.5)", coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_attack, use_container_width=True)

# 7. Safeguard Disclaimer Notice
st.markdown("<br><hr style='border-color:rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
st.warning(
    "⚠️ **METHODOLOGICAL SAFEGUARD NOTICE:** Target categorization trends and risk frequencies displayed on this "
    "dashboard represent retrospective risk patterns and **must not** be utilized to derive prospective dynamic tactical intelligence calculations."
)