import base64
import streamlit as st
import pandas as pd
from config import (
    apply_page_style,
    DATA_CSV_PATH,
    DATA_XLSX_PATH,
    ATTACK_MODEL_PATH,
    FEATURE_ENCODER_PATH,
    TARGET_ENCODER_PATH,
    LOGO_PATH,
    PAGE_REGISTRY,
)


@st.cache_data(show_spinner=False)
def _get_logo_b64() -> str:
    """Loads assets/logo.png as a base64 string for crisp HTML embedding."""
    if LOGO_PATH.exists():
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


def _safe_page_link(path: str, label: str, sidebar: bool = False):
    """Renders st.page_link safely whether launched via app.py or standalone."""
    target = st.sidebar if sidebar else st
    try:
        target.page_link(path, label=label)
    except Exception:
        pass


def render_page_header(title: str, subtitle: str, badge_text: str = "LIVE TELEMETRY"):
    """
    Injects global dark-theme CSS, renders the branded sidebar navigation & logo,
    and displays a sleek top header banner with quick-jump navigation controls.
    """
    apply_page_style()
    render_sidebar_navigation()

    st.markdown(
        f"""
        <div style='background:linear-gradient(90deg, rgba(15,23,42,0.92) 0%, rgba(30,41,59,0.65) 100%);
                    border:1px solid rgba(56,189,248,0.24); border-left:5px solid #38bdf8;
                    border-radius:14px; padding:18px 24px; margin-bottom:14px;
                    display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;
                    box-shadow: 0 8px 26px rgba(0,0,0,0.35);'>
            <div>
                <div style='font-size:0.72rem; color:#38bdf8; font-weight:800; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:2px;'>
                    🛡️ SENTINEL // GLOBAL THREAT INTELLIGENCE SUITE
                </div>
                <h1 class='glow-text' style='font-size:1.95rem; margin:0;'>{title}</h1>
                <p class='subtitle-text' style='margin:4px 0 0 0;'>{subtitle}</p>
            </div>
            <div style='display:flex; flex-direction:column; align-items:flex-end; gap:6px;'>
                <span class='status-badge badge-online'>● {badge_text}</span>
                <span style='font-size:0.72rem; color:#64748b;'>GTD ANALYTICAL CORE v2.4</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Compact Top Quick-Jump Bar
    q1, q2, q3, q4, q5, q6 = st.columns(6)
    with q1:
        _safe_page_link("app.py", label="🌐 Command Hub")
    with q2:
        _safe_page_link("pages/1_Home.py", label="🏠 Summary")
    with q3:
        _safe_page_link("pages/2_Global_Threat_Map.py", label="🗺️ Threat Map")
    with q4:
        _safe_page_link("pages/4_Attack_Prediction.py", label="🔮 ML Predictor")
    with q5:
        _safe_page_link("pages/5_Threat_Level.py", label="🚨 Risk Gauge")
    with q6:
        _safe_page_link("pages/13_Threat_Simulation_Lab.py", label="🕸️ Sim Lab")

    st.markdown("<hr style='border-color:rgba(59, 130, 246, 0.18); margin-top:6px; margin-bottom:18px;'>", unsafe_allow_html=True)


def render_sidebar_navigation():
    """Renders the branded logo crest, system status telemetry, and categorized sidebar navigation."""
    logo_b64 = _get_logo_b64()
    if logo_b64:
        st.sidebar.markdown(
            f"""
            <div style='margin-bottom:10px; text-align:center;'>
                <img src='data:image/png;base64,{logo_b64}' style='width:100%; border-radius:12px; box-shadow:0 4px 16px rgba(0,0,0,0.45);' alt='Sentinel GTI Logo'/>
            </div>
            """,
            unsafe_allow_html=True,
        )

    data_ok = DATA_CSV_PATH.exists() or DATA_XLSX_PATH.exists()
    models_ok = (
        ATTACK_MODEL_PATH.exists()
        and FEATURE_ENCODER_PATH.exists()
        and TARGET_ENCODER_PATH.exists()
    )

    data_badge = (
        "<span class='status-badge badge-online'>✓ DATA ONLINE</span>"
        if data_ok
        else "<span class='status-badge badge-crit'>✕ DATA OFFLINE</span>"
    )
    ml_badge = (
        "<span class='status-badge badge-online'>✓ ML READY</span>"
        if models_ok
        else "<span class='status-badge badge-warn'>⚠ ML UNCALIBRATED</span>"
    )

    st.sidebar.markdown(
        f"""
        <div style='background:rgba(15,23,42,0.82); border:1px solid rgba(56,189,248,0.22); border-radius:10px; padding:10px 12px; margin-bottom:10px;'>
            <div style='display:flex; justify-content:space-between; align-items:center; gap:6px; flex-wrap:wrap;'>
                {data_badge}
                {ml_badge}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Categorized Navigation Menu
    groups = [
        "COMMAND & GEOSPATIAL",
        "TACTICAL PROFILING",
        "AI & PREDICTIVE SUITE",
        "DOSSIERS & DEEP LABS",
    ]
    for grp in groups:
        st.sidebar.markdown(f"<div class='nav-group-header'>▸ {grp}</div>", unsafe_allow_html=True)
        for item in PAGE_REGISTRY:
            if item["group"] == grp:
                label = (
                    f"{item['icon']} {item['title']}"
                    if item["num"] == "00"
                    else f"{item['icon']} {item['num']} • {item['title']}"
                )
                _safe_page_link(item["path"], label=label, sidebar=True)

    st.sidebar.markdown("<hr style='border-color:rgba(59,130,246,0.18); margin:12px 0;'>", unsafe_allow_html=True)


def render_kpi_card(title: str, value: str, subtitle: str = "", accent_color: str = "#3b82f6"):
    """Renders a sleek glassmorphic KPI metric card with customizable left border accent."""
    st.markdown(
        f"""
        <div class='kpi-card' style='border-left: 4px solid {accent_color};'>
            <div class='kpi-title'>{title}</div>
            <div class='kpi-value'>{value}</div>
            <div class='kpi-sub'>{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def compute_executive_summary(df: pd.DataFrame) -> dict:
    """Computes high-level intelligence indicators from a GTD DataFrame slice."""
    if df is None or df.empty:
        return {
            "total_incidents": 0,
            "total_fatalities": 0,
            "total_injuries": 0,
            "total_casualties": 0,
            "success_rate": 0.0,
            "suicide_rate": 0.0,
            "active_countries": 0,
            "active_groups": 0,
            "top_region": "N/A",
            "top_country": "N/A",
            "top_attack": "N/A",
            "top_weapon": "N/A",
            "top_target": "N/A",
            "peak_year": "N/A",
        }

    total_incidents = len(df)
    total_fatalities = int(df["nkill"].fillna(0).sum()) if "nkill" in df.columns else 0
    total_injuries = int(df["nwound"].fillna(0).sum()) if "nwound" in df.columns else 0
    total_casualties = total_fatalities + total_injuries

    success_rate = (
        float(df["success"].fillna(0).mean() * 100)
        if "success" in df.columns and total_incidents > 0
        else 0.0
    )
    suicide_rate = (
        float(df["suicide"].fillna(0).mean() * 100)
        if "suicide" in df.columns and total_incidents > 0
        else 0.0
    )

    active_countries = int(df["country_txt"].nunique()) if "country_txt" in df.columns else 0
    if "gname" in df.columns:
        known_groups = df[df["gname"].notna() & (df["gname"] != "Unknown")]["gname"]
        active_groups = int(known_groups.nunique())
    else:
        active_groups = 0

    def top_val(col):
        if col in df.columns and not df[col].dropna().empty:
            s = df[col].dropna()
            s = s[s != "Unknown"] if (s != "Unknown").any() else s
            return str(s.mode().iloc[0]) if not s.empty else "N/A"
        return "N/A"

    peak_year = (
        int(df["iyear"].value_counts().idxmax())
        if "iyear" in df.columns and not df["iyear"].dropna().empty
        else "N/A"
    )

    return {
        "total_incidents": total_incidents,
        "total_fatalities": total_fatalities,
        "total_injuries": total_injuries,
        "total_casualties": total_casualties,
        "success_rate": success_rate,
        "suicide_rate": suicide_rate,
        "active_countries": active_countries,
        "active_groups": active_groups,
        "top_region": top_val("region_txt"),
        "top_country": top_val("country_txt"),
        "top_attack": top_val("attacktype1_txt"),
        "top_weapon": top_val("weaptype1_txt"),
        "top_target": top_val("targtype1_txt"),
        "peak_year": peak_year,
    }


def render_footer(disclaimer_text: str = None):
    """Renders a standardized methodological safeguard banner and footer."""
    if disclaimer_text:
        st.markdown("<br>", unsafe_allow_html=True)
        st.warning(disclaimer_text)

    st.markdown(
        """
        <div class='footer-container'>
            🛡️ <strong>SENTINEL // Global Threat Intelligence Dashboard</strong> • Strategic GTD Analytics & Predictive Modeling Suite • For Analytical Research Only
        </div>
        """,
        unsafe_allow_html=True,
    )
