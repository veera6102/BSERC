import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.organization_analysis import (
    top_organizations,
    organization_summary_kpis,
    organization_yearly,
    organization_attack_types,
    organization_weapons,
    organization_targets,
)
from utils.dashboard_metrics import render_page_header, render_kpi_card, render_footer

st.set_page_config(
    page_title="Organization Analysis | Threat Intelligence",
    page_icon="🪖",
    layout="wide",
)

render_page_header(
    title="🪖 Perpetrator Organization Tactical Profiles",
    subtitle="Analyze Historical Activity Timelines, Lethality Metrics, Weapon Signatures & Target Preferences",
    badge_text="THREAT ACTOR PROFILING",
)

try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Failed to initialize dataset pipeline: {e}")
    st.stop()

st.subheader("🔍 Select Target Group Profile")
top_orgs_list = top_organizations(df, n=75)

selected_org = st.selectbox(
    "Choose Perpetrator Organization for Profiling (Ranked by Incident Volume):",
    options=top_orgs_list,
    index=0,
    help="Select an organization to dissect its tactical fingerprint based on historical data parameters.",
)

org_kpis = organization_summary_kpis(df, selected_org)

# Organization KPI Strip
k1, k2, k3, k4 = st.columns(4)
with k1:
    render_kpi_card("Attributed Incidents", f"{org_kpis['incidents']:,}", f"Active Window: {org_kpis['active_span']}", "#3b82f6")
with k2:
    render_kpi_card("Total Casualties", f"{org_kpis['casualties']:,}", f"{org_kpis['kills']:,} Killed • {org_kpis['wounds']:,} Wounded", "#ef4444")
with k3:
    render_kpi_card("Primary Theatre", org_kpis["primary_country"], "Most Frequent Country", "#f59e0b")
with k4:
    render_kpi_card("Execution Success Rate", f"{org_kpis['success_rate']:.1f}%", "Historical Completion Ratio", "#10b981")

df_yearly = organization_yearly(df, selected_org)
df_attacks = organization_attack_types(df, selected_org)
df_weapons = organization_weapons(df, selected_org)
df_targets = organization_targets(df, selected_org)

st.subheader("📈 Historical Activity Timeline Trajectory")
if not df_yearly.empty:
    fig_timeline = px.line(
        df_yearly,
        x="Year",
        y="Count",
        title=f"Chronological Incident Frequency Pattern for {selected_org}",
        labels={"Year": "Timeline Year", "Count": "Incident Volume"},
        markers=True,
    )
    fig_timeline.update_traces(line=dict(color="#3b82f6", width=3), marker=dict(size=6, color="#ef4444"))
    fig_timeline.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
    )
    st.plotly_chart(fig_timeline, width='stretch')
else:
    st.info("No timeline metrics cataloged for selection.")

st.subheader("🧬 Tactical Signature & Vector Analysis")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("#### Preferred Weapon Profiles")
    if not df_weapons.empty:
        fig_weapon = px.bar(
            df_weapons.head(8),
            x="Count",
            y="Weapon",
            orientation="h",
            color="Count",
            color_continuous_scale="Reds",
        )
        fig_weapon.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            coloraxis_showscale=False,
            yaxis={"categoryorder": "total ascending"},
        )
        st.plotly_chart(fig_weapon, width='stretch')

with c2:
    st.markdown("#### Primary Attack Vectors")
    if not df_attacks.empty:
        fig_attack = px.bar(
            df_attacks.head(8),
            x="Count",
            y="Attack Type",
            orientation="h",
            color="Count",
            color_continuous_scale="Blues",
        )
        fig_attack.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            coloraxis_showscale=False,
            yaxis={"categoryorder": "total ascending"},
        )
        st.plotly_chart(fig_attack, width='stretch')

with c3:
    st.markdown("#### Targeted Victim Sectors")
    if not df_targets.empty:
        fig_target = px.bar(
            df_targets.head(8),
            x="Count",
            y="Target Sector",
            orientation="h",
            color="Count",
            color_continuous_scale="Tealgrn",
        )
        fig_target.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            coloraxis_showscale=False,
            yaxis={"categoryorder": "total ascending"},
        )
        st.plotly_chart(fig_target, width='stretch')

render_footer(
    "⚠️ **METHODOLOGICAL SAFEGUARD NOTICE:** Perpetrator organization profiles and tactical frequencies displayed on this "
    "dashboard represent retrospective historical patterns from the GTD and must not be utilized to derive prospective tactical intelligence."
)
