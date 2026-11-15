import os
import sys
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage,
    PageBreak,
    KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from config import BASE_DIR, LOGO_PATH


def _draw_page_chrome(canvas, doc):
    """Draws a sleek top cyber header bar and bottom footer on every PDF page."""
    canvas.saveState()
    width, height = letter

    # Top Header Accent Band
    canvas.setFillColor(colors.HexColor("#0f172a"))
    canvas.rect(0, height - 28, width, 28, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#38bdf8"))
    canvas.rect(0, height - 30, width, 2, stroke=0, fill=1)

    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(colors.HexColor("#e2e8f0"))
    canvas.drawString(36, height - 18, "SENTINEL // GLOBAL THREAT INTELLIGENCE DASHBOARD")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#38bdf8"))
    canvas.drawRightString(width - 36, height - 18, "COMBINED MASTER DOCUMENTATION (LEGACY v1.0 + UPGRADED v2.4)")

    # Bottom Footer Band
    canvas.setStrokeColor(colors.HexColor("#cbd5e1"))
    canvas.setLineWidth(0.6)
    canvas.line(36, 34, width - 36, 34)

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(36, 20, f"Author: CHOPPARAPU VEERA BRAHMAM (B.Tech AIML, VVIT) • Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(colors.HexColor("#1e3a8a"))
    canvas.drawRightString(width - 36, 20, f"Page {doc.page}")

    canvas.restoreState()


def generate_combined_project_documentation(output_filename=None) -> str:
    """
    Generates a comprehensive, visually styled PDF combining:
      1. Previous (Legacy v1.0) Project Documentation & Root-Cause Bug Audit
      2. Side-by-Side Evolution Delta Matrix (v1.0 vs. v2.4)
      3. Present Updates, New Features, UI/UX & ML Architecture Deep-Dive
      4. Complete 14-View Module Reference Blueprint & Execution Guide
    """
    if output_filename is None:
        output_filename = str(BASE_DIR / "Global_Threat_Intelligence_Project_Documentation.pdf")

    output_dir = os.path.dirname(output_filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=46,
        bottomMargin=46,
    )

    styles = getSampleStyleSheet()
    navy = colors.HexColor("#0f172a")
    royal = colors.HexColor("#1e3a8a")
    cyan = colors.HexColor("#0284c7")
    emerald = colors.HexColor("#059669")
    amber = colors.HexColor("#d97706")
    crimson = colors.HexColor("#dc2626")
    slate = colors.HexColor("#475569")
    light_bg = colors.HexColor("#f8fafc")
    tint_blue = colors.HexColor("#eff6ff")
    tint_green = colors.HexColor("#ecfdf5")
    tint_red = colors.HexColor("#fef2f2")

    title_style = ParagraphStyle(
        "MasterTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=navy,
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "MasterSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=cyan,
        spaceAfter=12,
    )
    sec_style = ParagraphStyle(
        "SecHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=royal,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True,
    )
    subsec_style = ParagraphStyle(
        "SubSecHeading",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=navy,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )
    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=13.2,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6,
    )
    th_style = ParagraphStyle(
        "TH",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
    )
    td_style = ParagraphStyle(
        "TD",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
    )
    td_bold = ParagraphStyle(
        "TDBold",
        parent=td_style,
        fontName="Helvetica-Bold",
    )

    story = []

    # ==========================================================================
    # COVER & EXECUTIVE OVERVIEW
    # ==========================================================================
    if LOGO_PATH.exists():
        img = RLImage(str(LOGO_PATH), width=290, height=68)
        img.hAlign = "LEFT"
        story.append(img)
        story.append(Spacer(1, 8))

    story.append(Paragraph("GLOBAL THREAT INTELLIGENCE DASHBOARD", title_style))
    story.append(
        Paragraph(
            "Combined Master Technical Documentation • Part I: Legacy Baseline (v1.0) + Part II: Upgraded Sentinel Suite (v2.4)",
            subtitle_style,
        )
    )

    intro_box_text = (
        "<b>AUTHOR:</b> CHOPPARAPU VEERA BRAHMAM • B.Tech Artificial Intelligence &amp; Machine Learning • "
        "Vasireddy Venkatadri Institute of Technology (VVIT)<br/><br/>"
        "<b>DOCUMENT PURPOSE:</b> This unified technical dossier combines the complete documentation of the "
        "<b>original baseline project (v1.0)</b>—including its initial architecture, file inventory, and diagnostic audit—"
        "with the <b>present upgraded platform (SENTINEL // GTI v2.4)</b>, highlighting all newly engineered analytical modules, "
        "UI/UX navigation systems, custom branding, bug resolutions, and machine-learning calibration improvements."
    )
    intro_table = Table([[Paragraph(intro_box_text, body_style)]], colWidths=[540])
    intro_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), tint_blue),
                ("BOX", (0, 0), (-1, -1), 1.2, cyan),
                ("PADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.append(intro_table)
    story.append(Spacer(1, 10))

    # High-Contrast Executive Metric Cards Row
    kpi_cards = [
        [
            Paragraph("<font color='#0284c7'><b>ACTIVE WORKSPACES</b></font><br/><font size=14><b>14 Views</b></font><br/><font size=7 color='#64748b'>Command Hub + 13 Pages</font>", td_style),
            Paragraph("<font color='#059669'><b>ML ACCURACY / F1</b></font><br/><font size=14><b>90.91% / 89.8%</b></font><br/><font size=7 color='#64748b'>XGBoost Multi-Class</font>", td_style),
            Paragraph("<font color='#d97706'><b>BUGS RESOLVED</b></font><br/><font size=14><b>8 Critical Fixes</b></font><br/><font size=7 color='#64748b'>100% AppTest Verified</font>", td_style),
            Paragraph("<font color='#1e3a8a'><b>DATASET ENGINE</b></font><br/><font size=14><b>CSV + XLSX</b></font><br/><font size=7 color='#64748b'>Cached Dual-Format Loader</font>", td_style),
        ]
    ]
    kpi_grid = Table(kpi_cards, colWidths=[135, 135, 135, 135])
    kpi_grid.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), light_bg),
                ("GRID", (0, 0), (-1, -1), 0.8, colors.HexColor("#cbd5e1")),
                ("PADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(kpi_grid)
    story.append(Spacer(1, 12))

    # ==========================================================================
    # PART I: PREVIOUS PROJECT DOCUMENTATION (LEGACY BASELINE v1.0)
    # ==========================================================================
    story.append(Paragraph("PART I — Previous Project Documentation (Legacy Baseline v1.0)", sec_style))
    story.append(
        Paragraph(
            "Before the v2.4 overhaul, the Global Threat Intelligence Dashboard was structured as an initial prototype "
            "built on Streamlit, Pandas, Plotly, Folium, Scikit-Learn, XGBoost, and ReportLab to analyze historical records "
            "from the Global Terrorism Database (GTD).",
            body_style,
        )
    )

    story.append(Paragraph("1.1 Legacy Baseline Architecture & File Inventory", subsec_style))
    legacy_files = [
        [Paragraph("Legacy Layer", th_style), Paragraph("Original Files", th_style), Paragraph("Original Baseline Role (v1.0)", th_style)],
        [
            Paragraph("Root Entrypoints", td_bold),
            Paragraph("app.py, config.py, train_attack_model.py, init_metrics.py, requirements.txt", td_style),
            Paragraph("Basic landing page checking CSV/model existence; static CSS string; basic XGBoost script; mock metrics.json generator; 240-line unpruned pip freeze.", td_style),
        ],
        [
            Paragraph("Legacy Pages (12)", td_bold),
            Paragraph("1_Home.py to 11_Data_Explorer.py, plus 14_Model_Performance.py", td_style),
            Paragraph("Individual Streamlit pages for KPIs, MarkerCluster map, single-country view, attack prediction form, risk score, linear forecast, PDF button, org/weapon/target charts, and mock metrics display.", td_style),
        ],
        [
            Paragraph("Legacy Utils (10)", td_bold),
            Paragraph("data_loader.py, preprocessing.py, charts.py, map_utils.py, forecasting.py, organization_analysis.py, risk_calculator.py, report_generator.py, prediction.py, dashboard_metrics.py", td_style),
            Paragraph("Uncached CSV reader, 7-feature filter, basic line/bar charts, cluster map helper, linear regression helper, org filters, rule-based risk score, PDF builder. Note: dashboard_metrics.py was 0 bytes and prediction.py was a duplicate copy of Page 4.", td_style),
        ],
    ]
    t_leg = Table(legacy_files, colWidths=[95, 165, 280])
    t_leg.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), slate),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, light_bg]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(t_leg)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1.2 Diagnostic Audit of Legacy Bugs & Bottlenecks Resolved", subsec_style))
    bug_rows = [
        [Paragraph("Bug ID / Area", th_style), Paragraph("Legacy Defect in v1.0", th_style), Paragraph("Engineering Fix Applied in v2.4", th_style)],
        [
            Paragraph("BUG-01: Dataset Offline Crash", td_bold),
            Paragraph("data/ only contained globalterrorism.xlsx, but config.py and data_loader.py hardcoded globalterrorism.csv without caching.", td_style),
            Paragraph("Generated globalterrorism.csv, added dual CSV/XLSX auto-fallback, and decorated load_data() with @st.cache_data.", td_style),
        ],
        [
            Paragraph("BUG-02: Config ImportError", td_bold),
            Paragraph("train_attack_model.py & Page 4 imported ATTACK_MODEL_PATH and MODEL_DIR (as Path objects), which were missing from config.py.", td_style),
            Paragraph("Unified all paths in config.py using pathlib.Path exports (MODEL_DIR, ATTACK_MODEL_PATH, FEATURE_ENCODER_PATH, etc.).", td_style),
        ],
        [
            Paragraph("BUG-03: Missing risk_model.pkl", td_bold),
            Paragraph("app.py required models/risk_model.pkl to exist, which was never generated, keeping the ML status permanently uncalibrated.", td_style),
            Paragraph("Updated readiness verification to check attack_prediction_model.pkl, feature_encoders.pkl, and target_encoder.pkl.", td_style),
        ],
        [
            Paragraph("BUG-04: Pandas 3.0 String Crash", td_bold),
            Paragraph("In-place integer assignment into string columns (input_data.loc[0, col] = int) raised TypeError on Pandas 3.x.", td_style),
            Paragraph("Re-engineered utils/prediction.py to encode features into a typed numeric dictionary before constructing the DataFrame.", td_style),
        ],
        [
            Paragraph("BUG-05: Disconnected Metrics", td_bold),
            Paragraph("train_attack_model.py wrote performance_metrics.pkl while Page 14 read static mock data from metrics.json and omitted the confusion matrix.", td_style),
            Paragraph("Synchronized train_attack_model.py to export both files and added an interactive Confusion Matrix & Per-Class Audit table.", td_style),
        ],
        [
            Paragraph("BUG-06: Alphabetical Org Bug", td_bold),
            Paragraph("top_organizations() sorted unique names alphabetically (:50) instead of ranking by incident volume.", td_style),
            Paragraph("Updated top_organizations() to rank perpetrator groups by value_counts() frequency.", td_style),
        ],
        [
            Paragraph("BUG-07: Broken .venv & Bloat", td_bold),
            Paragraph(".venv pointed to an uninstalled Python 3.10 binary; compnents/ and tests/ were empty; requirements.txt had 240 unrelated packages.", td_style),
            Paragraph("Rebuilt .venv for Python 3.14, deleted empty/redundant files, and pruned requirements.txt to the 12 core dependencies.", td_style),
        ],
        [
            Paragraph("BUG-08: Messy Sidebar Order", td_bold),
            Paragraph("Default Streamlit sidebar listed 10, 11, 14 before 2_Global_Threat_Map and lacked CSS styling on subpages.", td_style),
            Paragraph("Hid raw stSidebarNav, numbered pages 01–13, and built a 4-category custom navigation menu + 6-button top quick-jump bar.", td_style),
        ],
    ]
    t_bugs = Table(bug_rows, colWidths=[115, 205, 220])
    t_bugs.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), crimson),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, tint_red]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#fecaca")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 5.5),
            ]
        )
    )
    story.append(t_bugs)

    story.append(PageBreak())

    # ==========================================================================
    # PART II: UNIQUE EVOLUTION DELTA MATRIX (LEGACY v1.0 vs. PRESENT v2.4)
    # ==========================================================================
    story.append(Paragraph("PART II — Visual Evolution & Delta Matrix (Legacy v1.0 → Present v2.4)", sec_style))
    story.append(
        Paragraph(
            "The matrix below presents a side-by-side transformation view comparing the previous baseline project "
            "against the present upgraded <b>SENTINEL // GTI v2.4</b> release across every architectural dimension:",
            body_style,
        )
    )

    delta_rows = [
        [
            Paragraph("System Dimension", th_style),
            Paragraph("Previous Project (Legacy v1.0)", th_style),
            Paragraph("Present Upgraded Project (SENTINEL v2.4)", th_style),
            Paragraph("Status", th_style),
        ],
        [
            Paragraph("Branding & Logo", td_bold),
            Paragraph("Stretched blue map image only on app.py.", td_style),
            Paragraph("Custom Cyber-Radar Emblem (assets/logo.png) embedded in sidebar across all 14 views.", td_style),
            Paragraph("<font color='#059669'><b>UPGRADED</b></font>", td_style),
        ],
        [
            Paragraph("Navigation System", td_bold),
            Paragraph("Raw ASCII filename list (1, 10, 11, 14, 2...); no top bar.", td_style),
            Paragraph("4-Category Sidebar Menu + 6-Button Top Quick-Jump Bar + Tabbed Command Hub.", td_style),
            Paragraph("<font color='#059669'><b>NEW UI</b></font>", td_style),
        ],
        [
            Paragraph("Executive Home (MOD-01)", td_bold),
            Paragraph("4 basic metrics and 2 static charts.", td_style),
            Paragraph("Sidebar Year/Region filters, 6 Glass KPIs, Automated Brief banner & 3 analytical tabs (Seasonality, Donut, Dual-Trend).", td_style),
            Paragraph("<font color='#059669'><b>ENHANCED</b></font>", td_style),
        ],
        [
            Paragraph("Geospatial Map (MOD-02)", td_bold),
            Paragraph("MarkerCluster only, single-year filter.", td_style),
            Paragraph("Dual-Layer MarkerCluster + Thermal Casualty Heatmap, Region/Attack filters & 4 Hotspot KPIs.", td_style),
            Paragraph("<font color='#059669'><b>ENHANCED</b></font>", td_style),
        ],
        [
            Paragraph("Country Briefing (MOD-03)", td_bold),
            Paragraph("Single country charts only.", td_style),
            Paragraph("Added Bilateral Country-vs-Country Comparative Mode + Top Impacted Cities & Active Groups tables.", td_style),
            Paragraph("<font color='#059669'><b>NEW FEATURE</b></font>", td_style),
        ],
        [
            Paragraph("ML Predictor (MOD-04)", td_bold),
            Paragraph("Manual region selection; probability table only.", td_style),
            Paragraph("Auto-synced Region, Plotly probability chart, Secondary Vector card & Historical Precedent Matcher.", td_style),
            Paragraph("<font color='#059669'><b>NEW FEATURE</b></font>", td_style),
        ],
        [
            Paragraph("Risk Calculator (MOD-05)", td_bold),
            Paragraph("Text score /120 and bullet list.", td_style),
            Paragraph("Interactive 0–120 Speedometer Gauge, Component Attribution Bar Chart & Defensive Posture Advisor.", td_style),
            Paragraph("<font color='#059669'><b>NEW VISUALS</b></font>", td_style),
        ],
        [
            Paragraph("Trend Forecast (MOD-06)", td_bold),
            Paragraph("Global linear regression line only.", td_style),
            Paragraph("Global / Region / Country scope selectors + shaded ±1σ Historical Volatility Envelope.", td_style),
            Paragraph("<font color='#059669'><b>ENHANCED</b></font>", td_style),
        ],
        [
            Paragraph("AI Report & Docs (MOD-07)", td_bold),
            Paragraph("Single PDF download button without preview.", td_style),
            Paragraph("On-screen Live Executive Preview + Scoped Briefing PDF + Scoped CSV + Master Combined Project Documentation PDF.", td_style),
            Paragraph("<font color='#059669'><b>NEW FEATURE</b></font>", td_style),
        ],
        [
            Paragraph("Org / Weapon / Target (08–10)", td_bold),
            Paragraph("Volume bar charts only.", td_style),
            Paragraph("Added Org KPI strip & Target breakdown, plus Per-Incident Weapon & Target Lethality rankings.", td_style),
            Paragraph("<font color='#059669'><b>ENHANCED</b></font>", td_style),
        ],
        [
            Paragraph("Data Explorer (MOD-11)", td_bold),
            Paragraph("Year/Country filter and static 250-row grid.", td_style),
            Paragraph("Added Attack Method filter, multi-column Keyword Search, 1-click CSV Export & Correlation Heatmap.", td_style),
            Paragraph("<font color='#059669'><b>ENHANCED</b></font>", td_style),
        ],
        [
            Paragraph("Model Audit (MOD-12)", td_bold),
            Paragraph("Read static mock metrics.json; no confusion matrix.", td_style),
            Paragraph("Live calibrated metrics (90.91% Acc), Multi-Class Confusion Matrix Heatmap & Per-Class P/R/F1 table.", td_style),
            Paragraph("<font color='#059669'><b>CALIBRATED</b></font>", td_style),
        ],
        [
            Paragraph("Threat Sim Lab (MOD-13)", td_bold),
            Paragraph("Did not exist in legacy project.", td_style),
            Paragraph("Brand-new module: Sunburst & Alluvial Threat Topology, 3-Scenario War-Gaming Simulator & Z-Score Anomaly Detector.", td_style),
            Paragraph("<font color='#0284c7'><b>BRAND NEW</b></font>", td_style),
        ],
    ]
    t_delta = Table(delta_rows, colWidths=[100, 160, 205, 75])
    t_delta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), royal),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, tint_blue]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bfdbfe")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 5.5),
            ]
        )
    )
    story.append(t_delta)
    story.append(Spacer(1, 12))

    # ==========================================================================
    # PART III: COMPLETE 14-VIEW MODULE BLUEPRINT & ML PERFORMANCE LEDGER
    # ==========================================================================
    story.append(Paragraph("PART III — Present Architecture & Complete 14-View Module Blueprint", sec_style))
    story.append(
        Paragraph(
            "All 14 views share the unified Cyber-Intelligence CSS theme (<b>config.py</b>) and telemetry header/sidebar "
            "component library (<b>utils/dashboard_metrics.py</b>). Below is the complete operational module registry:",
            body_style,
        )
    )

    mod_rows = [
        [Paragraph("Code", th_style), Paragraph("Module Title & File Path", th_style), Paragraph("Category Group", th_style), Paragraph("Primary Analytical Capabilities", th_style)],
        [Paragraph("MOD-00", td_bold), Paragraph("Command Center Hub (app.py)", td_style), Paragraph("Command & Geo", td_style), Paragraph("5-KPI global snapshot, ML Calibration Hub, and 5-tab module launcher.", td_style)],
        [Paragraph("MOD-01", td_bold), Paragraph("Executive Summary (pages/1_Home.py)", td_style), Paragraph("Command & Geo", td_style), Paragraph("6 KPIs, automated insight banner, dual trajectory, attack donut & monthly seasonality.", td_style)],
        [Paragraph("MOD-02", td_bold), Paragraph("Global Threat Map (pages/2_Global_Threat_Map.py)", td_style), Paragraph("Command & Geo", td_style), Paragraph("Folium MarkerCluster + Thermal Casualty Heatmap with year/region/attack filters.", td_style)],
        [Paragraph("MOD-03", td_bold), Paragraph("Country Analysis (pages/3_Country_Analysis.py)", td_style), Paragraph("Tactical Profiling", td_style), Paragraph("National briefing, bilateral Country-vs-Country comparison, top cities & groups.", td_style)],
        [Paragraph("MOD-04", td_bold), Paragraph("ML Attack Predictor (pages/4_Attack_Prediction.py)", td_style), Paragraph("AI & Predictive", td_style), Paragraph("XGBoost inference, class probability chart & historical GTD analogue matcher.", td_style)],
        [Paragraph("MOD-05", td_bold), Paragraph("Threat Risk Calculator (pages/5_Threat_Level.py)", td_style), Paragraph("AI & Predictive", td_style), Paragraph("0–120 risk speedometer gauge, factor attribution bar chart & posture guidance.", td_style)],
        [Paragraph("MOD-06", td_bold), Paragraph("Trend Forecasting (pages/6_Forecasting.py)", td_style), Paragraph("AI & Predictive", td_style), Paragraph("Scoped rolling averages, linear regression projection & ±1σ volatility band.", td_style)],
        [Paragraph("MOD-07", td_bold), Paragraph("AI Dossier Export (pages/7_AI_Report.py)", td_style), Paragraph("Dossiers & Labs", td_style), Paragraph("On-screen briefing preview, scoped ReportLab PDF dossier & Master Project Doc PDF.", td_style)],
        [Paragraph("MOD-08", td_bold), Paragraph("Threat Organizations (pages/8_Organization_Analysis.py)", td_style), Paragraph("Tactical Profiling", td_style), Paragraph("Volume-ranked perpetrator groups, activity timeline, weapons, tactics & targets.", td_style)],
        [Paragraph("MOD-09", td_bold), Paragraph("Weaponry & Lethality (pages/9_Weapon_Analysis.py)", td_style), Paragraph("Tactical Profiling", td_style), Paragraph("Global weapon volume vs. mean casualties/incident & weapon-specific deep dive.", td_style)],
        [Paragraph("MOD-10", td_bold), Paragraph("Target Vulnerability (pages/10_Target_Analysis.py)", td_style), Paragraph("Tactical Profiling", td_style), Paragraph("Sector incident volume vs. cumulative casualties & target-specific deep dive.", td_style)],
        [Paragraph("MOD-11", td_bold), Paragraph("Master Data Explorer (pages/11_Data_Explorer.py)", td_style), Paragraph("Dossiers & Labs", td_style), Paragraph("Multi-filter incident grid, keyword search, CSV export & Pearson correlation matrix.", td_style)],
        [Paragraph("MOD-12", td_bold), Paragraph("ML Model Audit (pages/12_Model_Performance.py)", td_style), Paragraph("AI & Predictive", td_style), Paragraph("Calibrated KPIs, feature importance gain, confusion matrix & per-class P/R/F1.", td_style)],
        [Paragraph("MOD-13", td_bold), Paragraph("Threat Network & Sim Lab (pages/13_Threat_Simulation_Lab.py)", td_style), Paragraph("Dossiers & Labs", td_style), Paragraph("Sunburst & Alluvial vector flow, 3-Scenario war-gaming & Z-score anomaly detector.", td_style)],
    ]
    t_mods = Table(mod_rows, colWidths=[50, 165, 95, 230])
    t_mods.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), navy),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, tint_green]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#a7f3d0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(t_mods)
    story.append(Spacer(1, 10))

    # ==========================================================================
    # PART IV: EXECUTION, CALIBRATION & DEPLOYMENT COMMANDS
    # ==========================================================================
    exec_box = [
        [Paragraph("PART IV — Operational Execution & CLI Reference", subsec_style)],
        [
            Paragraph(
                "<b>1. Launch Dashboard Server:</b> <font name='Courier'>.\\.venv\\Scripts\\streamlit.exe run app.py</font><br/>"
                "<b>2. Recalibrate XGBoost ML Pipeline:</b> <font name='Courier'>.\\.venv\\Scripts\\python.exe train_attack_model.py</font><br/>"
                "<b>3. Regenerate Combined PDF Documentation:</b> <font name='Courier'>.\\.venv\\Scripts\\python.exe utils/project_doc_generator.py</font>",
                body_style,
            )
        ],
    ]
    t_exec = Table(exec_box, colWidths=[540])
    t_exec.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), light_bg),
                ("BOX", (0, 0), (-1, -1), 1, emerald),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(KeepTogether(t_exec))

    doc.build(story, onFirstPage=_draw_page_chrome, onLaterPages=_draw_page_chrome)
    return output_filename


if __name__ == "__main__":
    out = generate_combined_project_documentation()
    print(f"✅ Generated combined project documentation at: {out}")
