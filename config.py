import os
from pathlib import Path
import streamlit as st

# ==============================================================================
# 1. DYNAMIC CORE PLATFORM PATHS
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
ASSETS_DIR = BASE_DIR / "assets"

DATA_CSV_PATH = DATA_DIR / "globalterrorism.csv"
DATA_XLSX_PATH = DATA_DIR / "globalterrorism.xlsx"

DATA_PATH = str(DATA_CSV_PATH if DATA_CSV_PATH.exists() else DATA_XLSX_PATH)

ATTACK_MODEL_PATH = MODEL_DIR / "attack_prediction_model.pkl"
PREDICTION_MODEL_PATH = str(ATTACK_MODEL_PATH)
RISK_MODEL_PATH = str(MODEL_DIR / "risk_model.pkl")
FEATURE_ENCODER_PATH = MODEL_DIR / "feature_encoders.pkl"
TARGET_ENCODER_PATH = MODEL_DIR / "target_encoder.pkl"
PERFORMANCE_METRICS_PATH = MODEL_DIR / "performance_metrics.pkl"
METRICS_JSON_PATH = MODEL_DIR / "metrics.json"
LOGO_PATH = ASSETS_DIR / "logo.png"

# Ordered Master Registry of All Platform Pages
PAGE_REGISTRY = [
    {"id": "home_hub", "num": "00", "title": "Command Center Hub", "icon": "🌐", "path": "app.py", "group": "COMMAND & GEOSPATIAL", "desc": "System telemetry, ML calibration hub, global snapshot & module launcher."},
    {"id": "exec_sum", "num": "01", "title": "Executive Summary", "icon": "🏠", "path": "pages/1_Home.py", "group": "COMMAND & GEOSPATIAL", "desc": "Global KPIs, dual incident/casualty trajectories, seasonality & regional risk."},
    {"id": "geo_map", "num": "02", "title": "Global Threat Map", "icon": "🗺️", "path": "pages/2_Global_Threat_Map.py", "group": "COMMAND & GEOSPATIAL", "desc": "Interactive Folium pinpoint clusters & thermal casualty density heatmaps."},
    {"id": "country", "num": "03", "title": "Country Intelligence", "icon": "📊", "path": "pages/3_Country_Analysis.py", "group": "TACTICAL PROFILING", "desc": "National security briefings, city hotspots & bilateral country comparison."},
    {"id": "orgs", "num": "08", "title": "Threat Organizations", "icon": "🪖", "path": "pages/8_Organization_Analysis.py", "group": "TACTICAL PROFILING", "desc": "Perpetrator group activity timelines, lethality ratios, weapons & targets."},
    {"id": "weapons", "num": "09", "title": "Weaponry & Lethality", "icon": "⚔️", "path": "pages/9_Weapon_Analysis.py", "group": "TACTICAL PROFILING", "desc": "Weapon classifications, per-incident casualty efficiency & country breakdown."},
    {"id": "targets", "num": "10", "title": "Target Vulnerability", "icon": "🎯", "path": "pages/10_Target_Analysis.py", "group": "TACTICAL PROFILING", "desc": "Infrastructure sector exposure, casualty burden & chronological trends."},
    {"id": "ml_pred", "num": "04", "title": "ML Attack Predictor", "icon": "🔮", "path": "pages/4_Attack_Prediction.py", "group": "AI & PREDICTIVE SUITE", "desc": "XGBoost tactical vector simulator, confidence distribution & historical analogues."},
    {"id": "risk_calc", "num": "05", "title": "Threat Risk Calculator", "icon": "🚨", "path": "pages/5_Threat_Level.py", "group": "AI & PREDICTIVE SUITE", "desc": "0–120 risk speedometer gauge, weight attribution & security posture guidance."},
    {"id": "forecast", "num": "06", "title": "Trend Forecasting", "icon": "📈", "path": "pages/6_Forecasting.py", "group": "AI & PREDICTIVE SUITE", "desc": "Rolling averages, linear regression projections & ±1σ volatility envelopes."},
    {"id": "ml_audit", "num": "12", "title": "ML Model Audit", "icon": "🧠", "path": "pages/12_Model_Performance.py", "group": "AI & PREDICTIVE SUITE", "desc": "Holdout accuracy/F1 metrics, feature importance & multi-class confusion matrix."},
    {"id": "ai_report", "num": "07", "title": "AI Dossier Export", "icon": "📄", "path": "pages/7_AI_Report.py", "group": "DOSSIERS & DEEP LABS", "desc": "Live executive intelligence briefing preview, PDF dossier & CSV export."},
    {"id": "explorer", "num": "11", "title": "Master Data Explorer", "icon": "🔍", "path": "pages/11_Data_Explorer.py", "group": "DOSSIERS & DEEP LABS", "desc": "Multi-filter incident search grid, keyword lookup & Pearson correlation matrix."},
    {"id": "net_lab", "num": "13", "title": "Threat Network & Sim Lab", "icon": "🕸️", "path": "pages/13_Threat_Simulation_Lab.py", "group": "DOSSIERS & DEEP LABS", "desc": "Multi-vector Sankey/Sunburst flow, 3-scenario war-gaming & anomaly detector."},
]

# ==============================================================================
# 2. CYBER-INTELLIGENCE UI THEME & TYPOGRAPHY SYSTEM
# ==============================================================================
CSS_STYLE = """
<style>
    /* Hide raw default Streamlit multipage file list in sidebar */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Global Dashboard Dark UI Background Canvas */
    .stApp {
        background: radial-gradient(circle at 12% 8%, #101d38 0%, #0a1122 52%, #060a14 100%);
        color: #f1f5f9;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080f1e 0%, #0d162b 100%);
        border-right: 1px solid rgba(56, 189, 248, 0.18);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1.5rem;
    }

    /* Sidebar Page Link Navigation Buttons */
    div[data-testid="stPageLink"] a {
        background: rgba(15, 23, 42, 0.72) !important;
        border: 1px solid rgba(59, 130, 246, 0.20) !important;
        border-radius: 9px !important;
        padding: 7px 12px !important;
        margin-bottom: 3px !important;
        transition: all 0.18s ease !important;
        text-decoration: none !important;
    }

    div[data-testid="stPageLink"] a:hover {
        background: linear-gradient(90deg, rgba(37, 99, 235, 0.32) 0%, rgba(14, 165, 233, 0.18) 100%) !important;
        border-color: rgba(56, 189, 248, 0.65) !important;
        transform: translateX(3px);
        box-shadow: 0 4px 14px rgba(14, 165, 233, 0.2);
    }

    div[data-testid="stPageLink"] a[aria-current="page"] {
        background: linear-gradient(90deg, rgba(37, 99, 235, 0.48) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border-left: 4px solid #38bdf8 !important;
        border-color: rgba(56, 189, 248, 0.65) !important;
        font-weight: 700 !important;
    }

    /* Action Buttons Styling */
    .stButton > button, .stDownloadButton > button {
        background: linear-gradient(135deg, #1d4ed8 0%, #0284c7 100%) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(56, 189, 248, 0.45) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        padding: 0.55rem 1.1rem !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.28) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%) !important;
        border-color: #7dd3fc !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.4) !important;
    }

    /* Tabs Styling */
    button[data-baseweb="tab"] {
        background: rgba(15, 23, 42, 0.65) !important;
        border-radius: 8px 8px 0 0 !important;
        margin-right: 6px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
    }

    /* Blue Neon Glow Title Accentuation Header */
    .glow-text {
        background: linear-gradient(90deg, #f8fafc 0%, #60a5fa 55%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 24px rgba(59, 130, 246, 0.30);
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-top: 0px;
        margin-bottom: 4px;
    }

    .subtitle-text {
        color: #94a3b8;
        font-size: 1.02rem;
        margin-top: 0px;
        margin-bottom: 10px;
    }

    /* High-Contrast Glassmorphism KPI Cards */
    .kpi-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.72) 0%, rgba(15, 23, 42, 0.90) 100%);
        border: 1px solid rgba(59, 130, 246, 0.22);
        border-left: 4px solid #3b82f6;
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 14px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.5);
        box-shadow: 0 12px 28px rgba(14, 165, 233, 0.16);
    }

    .kpi-title {
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }

    .kpi-value {
        color: #f8fafc;
        font-size: 1.65rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 4px;
    }

    .kpi-sub {
        color: #64748b;
        font-size: 0.78rem;
        font-weight: 500;
    }

    /* Module Feature Grid Cards on Landing Page */
    .module-card {
        background: linear-gradient(160deg, rgba(30, 41, 59, 0.70) 0%, rgba(11, 19, 37, 0.92) 100%);
        border: 1px solid rgba(56, 189, 248, 0.20);
        border-top: 3px solid #3b82f6;
        border-radius: 12px;
        padding: 18px;
        min-height: 128px;
        margin-bottom: 8px;
        transition: all 0.2s ease;
    }

    .module-card:hover {
        border-color: rgba(56, 189, 248, 0.65);
        box-shadow: 0 8px 24px rgba(14, 165, 233, 0.18);
    }

    /* Sidebar Section Category Header */
    .nav-group-header {
        font-size: 0.70rem;
        font-weight: 800;
        color: #38bdf8;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        margin: 12px 0 5px 4px;
        opacity: 0.9;
    }

    /* Status Pill Badges */
    .status-badge {
        display: inline-block;
        padding: 4px 11px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .badge-online {
        background: rgba(16, 185, 129, 0.16);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .badge-warn {
        background: rgba(245, 158, 11, 0.16);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .badge-crit {
        background: rgba(239, 68, 68, 0.16);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }

    /* Insight Banner Box */
    .insight-box {
        background: linear-gradient(90deg, rgba(30, 58, 138, 0.32) 0%, rgba(15, 23, 42, 0.80) 100%);
        border: 1px solid rgba(56, 189, 248, 0.32);
        border-left: 4px solid #38bdf8;
        border-radius: 10px;
        padding: 15px 20px;
        margin: 12px 0 18px 0;
    }

    /* Standardized Footer Container */
    .footer-container {
        text-align: center;
        margin-top: 36px;
        padding: 18px;
        color: #64748b;
        font-size: 0.82rem;
        border-top: 1px solid rgba(148, 163, 184, 0.12);
    }
</style>
"""


def apply_page_style():
    """Injects the global Cyber-Intelligence CSS theme onto the active Streamlit page."""
    st.markdown(CSS_STYLE, unsafe_allow_html=True)
