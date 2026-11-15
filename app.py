import sys
import subprocess
import streamlit as st
from config import (
    DATA_CSV_PATH,
    DATA_XLSX_PATH,
    ATTACK_MODEL_PATH,
    FEATURE_ENCODER_PATH,
    TARGET_ENCODER_PATH,
    PAGE_REGISTRY,
)
from utils.data_loader import load_data
from utils.dashboard_metrics import (
    render_page_header,
    render_kpi_card,
    compute_executive_summary,
    render_footer,
)

# 1. Configure the Streamlit Page Layout
st.set_page_config(
    page_title="SENTINEL // Global Threat Intelligence Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_page_header(
    title="🌐 Global Threat Intelligence Command Center",
    subtitle="Enterprise Analytics, Geospatial Telemetry & Predictive ML Suite • Global Terrorism Database (GTD)",
    badge_text="COMMAND CENTER ACTIVE",
)

# 2. Dynamic Pipeline Verification Logic
data_exists = DATA_CSV_PATH.exists() or DATA_XLSX_PATH.exists()
models_exist = (
    ATTACK_MODEL_PATH.exists()
    and FEATURE_ENCODER_PATH.exists()
    and TARGET_ENCODER_PATH.exists()
)

if not data_exists:
    st.error(f"❌ Missing primary dataset file at `{DATA_CSV_PATH}` or `{DATA_XLSX_PATH}`.")
    st.stop()

df = load_data()
summary = compute_executive_summary(df)

# 3. Executive Snapshot KPI Strip
st.subheader("📡 Global Operational Telemetry Snapshot")
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    render_kpi_card(
        "Logged GTD Incidents",
        f"{summary['total_incidents']:,}",
        f"Peak Activity Year: {summary['peak_year']}",
        "#3b82f6",
    )
with k2:
    render_kpi_card(
        "Total Casualties",
        f"{summary['total_casualties']:,}",
        f"{summary['total_fatalities']:,} Killed • {summary['total_injuries']:,} Wounded",
        "#ef4444",
    )
with k3:
    render_kpi_card(
        "Jurisdictions Impacted",
        f"{summary['active_countries']:,} Countries",
        f"Primary Zone: {summary['top_region']}",
        "#06b6d4",
    )
with k4:
    render_kpi_card(
        "Identified Threat Actors",
        f"{summary['active_groups']:,} Groups",
        f"Top Vector: {summary['top_attack']}",
        "#f59e0b",
    )
with k5:
    render_kpi_card(
        "Operational Success Rate",
        f"{summary['success_rate']:.1f}%",
        f"Dominant Weapon: {summary['top_weapon']}",
        "#10b981",
    )

# 4. System Overview & ML Calibration Control Row
left_col, right_col = st.columns([1.55, 1])

with left_col:
    st.markdown(
        f"""
        <div class='kpi-card' style='text-align: left; padding: 22px;'>
            <h3 style='color:#60a5fa; margin-top:0px;'>🛡️ STRATEGIC PLATFORM OVERVIEW</h3>
            <p style='color:#cbd5e1; line-height:1.6;'>
                <strong>SENTINEL // GTI</strong> synthesizes historical incident records from the
                <strong>Global Terrorism Database (GTD)</strong> into an integrated decision-support workspace featuring
                geospatial cluster/heatmap tracking, bilateral country comparison, perpetrator profiling,
                multi-scenario war-gaming, and XGBoost tactical classification.
            </p>
            <div style='display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-top:14px;'>
                <div style='background:rgba(15,23,42,0.65); padding:12px; border-radius:8px; border:1px solid rgba(59,130,246,0.18);'>
                    <div style='color:#94a3b8; font-size:0.74rem; font-weight:700;'>ACTIVE DATASET SCOPE</div>
                    <div style='color:#f8fafc; font-weight:700; font-size:0.95rem;'>{summary['total_incidents']:,} Validated Records ({int(df['iyear'].min())}–{int(df['iyear'].max())})</div>
                </div>
                <div style='background:rgba(15,23,42,0.65); padding:12px; border-radius:8px; border:1px solid rgba(59,130,246,0.18);'>
                    <div style='color:#94a3b8; font-size:0.74rem; font-weight:700;'>PRIMARY VULNERABILITY SECTOR</div>
                    <div style='color:#f8fafc; font-weight:700; font-size:0.95rem;'>{summary['top_target']}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_col:
    st.markdown(
        """
        <div class='kpi-card' style='text-align: left; padding: 20px; border-left-color:#10b981;'>
            <h3 style='color:#10b981; margin-top:0px;'>🤖 ML ENGINE CALIBRATION HUB</h3>
            <p style='color:#cbd5e1; font-size:0.90rem; margin-bottom:0;'>
                Calibrate or refresh the multi-class <strong>XGBoost Tactical Classifier</strong>, feature encoders,
                and holdout confusion matrices against the active dataset.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if models_exist:
        st.success("✅ Prediction models & encoders are calibrated and online.")
    else:
        st.warning("⚠️ Machine Learning models require calibration before running predictions.")

    btn_label = (
        "🔄 Recalibrate ML Classifier Pipeline"
        if models_exist
        else "🚀 Initialize & Train ML Models"
    )
    if st.button(btn_label, type="primary", width='stretch'):
        with st.spinner("Training XGBoost classifier and exporting encoders & evaluation matrices..."):
            try:
                result = subprocess.run(
                    [sys.executable, "train_attack_model.py"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                st.cache_resource.clear()
                st.success("✅ ML Models calibrated and saved successfully!")
                st.toast("Models ready for tactical inference.")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Training pipeline failed: {e}")
                if "result" in locals() and result.stderr:
                    st.code(result.stderr)

# 5. Categorized Module Directory Workspace
st.subheader("🧭 Interactive Command Modules & Analytical Workspaces")

workspace_pages = [p for p in PAGE_REGISTRY if p["num"] != "00"]
t_all, t_cmd, t_tac, t_ai, t_lab = st.tabs([
    "🌐 All Workspaces (13)",
    "⚡ Command & Geospatial",
    "🕵️ Tactical Profiling",
    "🤖 AI & Predictive Suite",
    "📂 Dossiers & Sim Lab",
])


def _render_module_cards(items):
    for row_start in range(0, len(items), 3):
        cols = st.columns(3)
        for idx, item in enumerate(items[row_start : row_start + 3]):
            with cols[idx]:
                st.markdown(
                    f"""
                    <div class='module-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;'>
                            <span style='font-weight:800; font-size:1.02rem; color:#f8fafc;'>{item['icon']} {item['title']}</span>
                            <span style='font-size:0.72rem; font-weight:700; color:#38bdf8; background:rgba(56,189,248,0.14); padding:2px 8px; border-radius:6px;'>MOD-{item['num']}</span>
                        </div>
                        <div style='color:#94a3b8; font-size:0.84rem; line-height:1.45;'>{item['desc']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.page_link(item["path"], label=f"Launch {item['title']} →")


with t_all:
    _render_module_cards(workspace_pages)
with t_cmd:
    _render_module_cards([p for p in workspace_pages if p["group"] == "COMMAND & GEOSPATIAL"])
with t_tac:
    _render_module_cards([p for p in workspace_pages if p["group"] == "TACTICAL PROFILING"])
with t_ai:
    _render_module_cards([p for p in workspace_pages if p["group"] == "AI & PREDICTIVE SUITE"])
with t_lab:
    _render_module_cards([p for p in workspace_pages if p["group"] == "DOSSIERS & DEEP LABS"])

render_footer(
    "⚠️ **DISCLAIMER:** This platform is designed strictly for academic and retrospective analytical research. "
    "All metrics and ML outputs reflect mathematical patterns in historical GTD records and must not be used to forecast real-world tactical events."
)
