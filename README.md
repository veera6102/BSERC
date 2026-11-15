# 🌍 Global Threat Intelligence Dashboard (`SENTINEL // GTI v2.4`)

![Sentinel Command Emblem](assets/logo.png)

A full-stack, enterprise-styled **Global Threat Intelligence & Predictive Analytics Platform** developed using **Python**, **Streamlit**, **Plotly**, **Folium**, **ReportLab**, and **XGBoost Machine Learning** to analyze historical terrorism incidents from the **Global Terrorism Database (GTD)**.

The platform combines interactive geospatial telemetry, bilateral country intelligence, perpetrator group profiling, weapon/target lethality auditing, statistical trend extrapolation, multi-class ML attack prediction, 3-scenario tactical war-gaming, Z-score anomaly detection, and automated PDF intelligence dossier generation.

---

# 📌 Table of Contents

- [📖 Project Overview](#-project-overview)
- [🎯 Objectives](#-objectives)
- [🔄 Project Evolution: Previous (v1.0) vs. Updated (v2.4)](#-project-evolution-previous-v10-vs-updated-v24)
- [✨ Comprehensive Module Features (14 Views)](#-comprehensive-module-features-14-views)
- [🛠 Technologies Used](#-technologies-used)
- [📂 Dataset](#-dataset)
- [🏗 Project Architecture](#-project-architecture)
- [🔄 Project Workflow](#-project-workflow)
- [📁 Folder Structure](#-folder-structure)
- [⚙ Installation](#-installation)
- [▶ Running the Project](#-running-the-project)
- [🤖 Machine Learning Model & Calibration Metrics](#-machine-learning-model--calibration-metrics)
- [📊 Results](#-results)
- [🚀 Future Enhancements](#-future-enhancements)
- [📸 Screenshots](#-screenshots)
- [👨‍💻 Author](#-author)
- [📄 License & Disclaimer](#-license--disclaimer)

---

# 📖 Project Overview

The **Global Threat Intelligence Dashboard (`SENTINEL // GTI v2.4`)** is designed to transform raw historical terrorism incident records into actionable visual intelligence, risk audits, and explainable machine-learning insights.

The platform enables researchers, analysts, and students to:

- **Explore global incident telemetry** across interactiveKPI scorecards, seasonal tempo charts, and regional risk distributions.
- **Visualize geospatial hotspots** using dual-layer **Folium Marker Clusters** and **Thermal Casualty Density Heatmaps**.
- **Conduct national & bilateral comparisons** with side-by-side **Country-vs-Country** trajectory and lethality matrices.
- **Predict tactical attack methods** using a calibrated multi-class **XGBoost Classifier** (`90.91% Accuracy`, `89.84% F1-Score`) paired with a **Historical GTD Precedent Matcher**.
- **Audit operational risk scores (`0–120`)** via an interactive **Speedometer Risk Gauge**, component weight attribution chart, and defensive posture advisor.
- **Forecast macro trajectories** with configurable rolling averages, linear regression trendlines, and shaded **`±1σ` historical volatility envelopes**.
- **Profile threat organizations, weaponry, and infrastructure targets** by both incident volume and per-incident casualty lethality.
- **Run multi-scenario war-gaming & anomaly detection** using Sunburst/Alluvial vector flows, a **3-Scenario Simultaneous Simulator**, and a **Z-Score Statistical Anomaly Detector**.
- **Compile downloadable PDF dossiers** and export filtered CSV slices with 1-click controls.

---

# 🎯 Objectives

The primary objectives of this project are:

- Analyze historical terrorism incidents from the **Global Terrorism Database (GTD)** using structured statistical and visual pipelines.
- Provide an intuitive **Cyber-Intelligence Command UI** with categorized sidebar navigation and instant quick-jump controls.
- Predict likely attack vector classifications from operational scenario parameters using supervised **Machine Learning (XGBoost)**.
- Quantify incident severity (`LOW`, `MODERATE`, `HIGH`, `CRITICAL`) using a transparent, data-driven `0–120` risk scoring formula.
- Empower comparative security research with bilateral country comparisons, multi-vector topology flows, and statistical outlier detection.
- Generate production-grade **Executive Intelligence Briefing PDFs** and **Combined Master Project Documentation PDFs** via ReportLab.

---

# 🔄 Project Evolution: Previous (`v1.0`) vs. Updated (`v2.4`)

| System Dimension | Previous Baseline (`v1.0`) | Updated Release (`SENTINEL // GTI v2.4`) | Status |
| :--- | :--- | :--- | :--- |
| **UI & Branding** | Basic dark background; stretched world map image on `app.py` only | Custom **SENTINEL Cyber-Radar Emblem (`assets/logo.png`)**, glassmorphic KPI cards & glowing headers across all 14 views | **Upgraded** |
| **Navigation System** | Raw Streamlit filename list (`1, 10, 11, 14, 2...`) | **4-Category Command Sidebar Menu** + **6-Button Top Quick-Jump Bar** + **5-Tab Module Launcher** | **New UI** |
| **Dataset Pipeline** | Uncached `globalterrorism.csv` reader (failed when only `.xlsx` existed) | `@st.cache_data` dual-format loader supporting both `.csv` and `.xlsx` with automatic CSV caching | **Fixed & Cached** |
| **Home Overview (`MOD-01`)** | 4 static metrics and 2 basic charts | Sidebar Year/Region filters, **6 Glass KPIs**, **Automated Intelligence Brief**, and **3 Analytical Tabs** (Dual-Trend, Donut, Monthly Seasonality) | **Enhanced** |
| **Global Threat Map (`MOD-02`)** | MarkerCluster only, single-year filter | Dual-layer **MarkerCluster + Thermal Casualty Heatmap**, Region/Attack filters & 4 Hotspot KPIs | **Enhanced** |
| **Country Analysis (`MOD-03`)** | Single-country view only | Added **Bilateral Country-vs-Country Comparison Mode**, Top Impacted Cities & Active Groups tables | **New Feature** |
| **Attack Prediction (`MOD-04`)** | Manual region selection; probability table only | Auto-synced Region, **Plotly Probability Distribution Bar Chart**, Secondary Vector card & **Historical Precedent Matcher** | **New Feature** |
| **Threat Level (`MOD-05`)** | Text score `/120` and bullet list | Interactive **`0–120` Speedometer Gauge**, **Component Weight Attribution Chart** & **Defensive Posture Advisor** | **New Visuals** |
| **Forecasting (`MOD-06`)** | Global linear regression line only | **Global / Region / Country** scope selectors + shaded **`±1σ` Historical Volatility Envelope** | **Enhanced** |
| **AI Report (`MOD-07`)** | Single PDF download button without preview | **Live On-Screen Executive Preview**, Scoped Briefing PDF, Scoped CSV Export & **Combined Master Project Documentation PDF** | **New Feature** |
| **Org / Weapon / Target (`08–10`)** | Volume bar charts only | Volume-ranked perpetrator groups, Org KPI strip, Target breakdown & **Per-Incident Weapon/Target Lethality Rankings** | **Enhanced** |
| **Data Explorer (`MOD-11`)** | Year/Country filter and static 250-row table | Added Attack Method filter, multi-column **Keyword Search**, **1-Click CSV Export** & Pearson Correlation Heatmap | **Enhanced** |
| **Model Audit (`MOD-12`)** | Static mock `metrics.json`; no confusion matrix | Live calibrated metrics (**90.91% Accuracy**), **Multi-Class Confusion Matrix Heatmap** & **Per-Class Precision/Recall/F1 Table** | **Calibrated** |
| **Threat Sim Lab (`MOD-13`)** | *Not present in v1.0* | **Brand-new module:** Sunburst & Alluvial Threat Topology, **3-Scenario War-Gaming Simulator** & **Z-Score Anomaly Detector** | **Brand New** |

---

# ✨ Comprehensive Module Features (14 Views)

## 🌐 `MOD-00` • Command Center Hub (`app.py`)
- Live 5-card global telemetry snapshot (Total Incidents, Total Casualties, Jurisdictions Impacted, Identified Threat Actors, Operational Success Rate).
- **ML Engine Calibration Hub** to train or recalibrate the multi-class XGBoost classifier with 1 click.
- Interactive **5-Tab Workspace Launcher** (`All Workspaces`, `Command & Geospatial`, `Tactical Profiling`, `AI & Predictive Suite`, `Dossiers & Sim Lab`).

## 🏠 `MOD-01` • Executive Summary (`pages/1_Home.py`)
- Interactive sidebar **Timeline Range** and **Geographical Region** filters.
- 6 KPI Cards: Incidents Logged, Confirmed Fatalities (`NKILL`), Reported Injuries (`NWOUND`), Combined Casualties, Success Rate, and Suicide Attack Ratio.
- **Automated Intelligence Brief** banner dynamically summarizing peak year, top region/country, primary tactic, and dominant weapon.
- 3 Analytical Tabs: Chronological Dual-Trajectory, Attack Vector Donut & Target Sector Bar Chart, and Monthly Operational Seasonality.

## 🗺️ `MOD-02` • Global Threat Map (`pages/2_Global_Threat_Map.py`)
- Interactive dark-themed **Folium Map** (`CartoDB Dark_Matter`).
- 3 Visualization Layer Modes: **Cluster Markers + Thermal Heatmap**, **Incident Marker Clusters Only**, or **Thermal Density Heatmap Only**.
- Multi-criteria sidebar filters for **Year**, **Region**, **Attack Vector**, and **Max Plotted Coordinates**.
- 4 Geospatial Hotspot KPIs (Filtered Incidents, Primary Hotspot Country, Epicenter Urban Node, Zone Casualties).

## 📊 `MOD-03` • Country Intelligence & Bilateral Comparison (`pages/3_Country_Analysis.py`)
- Localized country security briefing with Incident, Threat Group, Casualty, and Tactical Success Rate KPIs.
- **⚖️ Bilateral Country-vs-Country Comparison Mode**: Compare any two countries side-by-side with overlaid chronological timelines and operational metric tables.
- Localized breakdowns for Top 7 Attack Typologies, Dominant Weapon Categories, Target Vulnerability Sectors, **Most Impacted Cities**, and **Most Active Perpetrator Groups**.

## 🔮 `MOD-04` • ML Attack Type Modeler (`pages/4_Attack_Prediction.py`)
- Interactive scenario simulator powered by the trained **XGBoost Multi-Class Classifier**.
- Automatically resolves the geographic **Region** when a **Country** is selected.
- Outputs Top Predicted Tactical Vector, Classifier Confidence `%`, Secondary Alternative Vector, an interactive **Probability Distribution Bar Chart**, and a **Historical GTD Precedents Table** matching the selected target/weapon profile.

## 🚨 `MOD-05` • Operational Threat Level Calculator (`pages/5_Threat_Level.py`)
- Evaluates Weapon Lethality (`10–40 pts`), Target Vulnerability (`10–40 pts`), Operational Success (`+10 pts`), Suicide Modality (`+15 pts`), and Casualty Thresholds (`0–30 pts`).
- Displays an interactive **`0–120` Plotly Speedometer Gauge** across `LOW`, `MODERATE`, `HIGH`, and `CRITICAL` zones.
- Renders a **Component Weight Attribution Bar Chart**, **Transparent Audit Ledger**, and **Recommended Security Posture** checklist.

## 📈 `MOD-06` • Historical Trend Forecasting (`pages/6_Forecasting.py`)
- Supports **Global**, **Regional**, and **Country-specific** forecasting scopes across `Incident Count`, `Fatalities`, and `Casualties`.
- Plots Observed Historical Data, configurable `N-Year Rolling Average`, Linear Regression Fit, Future Trend Extrapolation, and a shaded **`±1σ` Historical Volatility Envelope**.

## 📄 `MOD-07` • Strategic AI Intelligence Report & Documentation (`pages/7_AI_Report.py`)
- Scope selector for **Global Overview**, **By Specific Country**, or **By Specific Region**.
- Renders a **Live On-Screen Executive Briefing Preview** prior to export.
- 3 Export Engines:
  1. **📥 Compile & Download Executive PDF Dossier** (via ReportLab).
  2. **📘 Download Combined Master Project Documentation PDF** (`v1.0 Legacy + v2.4 Upgrade`).
  3. **📊 Export Scoped Dataset Slice (CSV)**.

## 🪖 `MOD-08` • Perpetrator Organization Profiles (`pages/8_Organization_Analysis.py`)
- Ranks perpetrator groups by actual historical incident volume (excluding `"Unknown"`).
- Displays Organization KPIs (Attributed Incidents, Active Year Span, Total Casualties, Primary Theatre, Execution Success Rate), chronological timeline, Preferred Weapons, Primary Attack Vectors, and Targeted Victim Sectors.

## ⚔️ `MOD-09` • Weapon Profile & Lethality Analysis (`pages/9_Weapon_Analysis.py`)
- Compares global weapon classifications by **Total Incident Volume** vs. **Average Casualties per Incident (Lethality Efficiency)**.
- Interactive single-weapon deep dive with chronological deployment trajectory, top 10 countries, and 100-row filtered incident reference table.

## 🎯 `MOD-10` • Target Analysis & Asset Vulnerability (`pages/10_Target_Analysis.py`)
- Compares infrastructure sectors by **Incident Frequency** vs. **Cumulative Casualty Burden**.
- Interactive target-sector deep dive with yearly frequency trajectory, top 10 impacted countries, and filtered incident table.

## 🔍 `MOD-11` • Master Data Explorer & Correlation Matrix (`pages/11_Data_Explorer.py`)
- Multi-dimensional filters for **Timeline Range**, **Country**, **Attack Method**, and **Multi-Column Keyword Search** (`City`, `Province`, `Group`, `Target`, `Summary`).
- Interactive 300-row preview grid with **1-Click Filtered CSV Download** and a **Pearson Correlation Heatmap** across numerical GTD attributes.

## 🧠 `MOD-12` • ML Model Performance & Calibration Audit (`pages/12_Model_Performance.py`)
- Displays holdout evaluation KPIs: **Optimal Classifier**, **Accuracy (`90.91%`)**, **Weighted Precision (`89.26%`)**, **Weighted Recall (`90.91%`)**, and **Balanced F1-Score (`89.84%`)**.
- Renders the **Relative Feature Information Gain Bar Chart**, **Multi-Class Holdout Confusion Matrix Heatmap**, and **Per-Class Precision/Recall/F1 Audit Table**.

## 🕸️ `MOD-13` • Threat Network & Multi-Scenario War-Gaming Lab (`pages/13_Threat_Simulation_Lab.py`)
- **Tab 1 — Multi-Vector Threat Topology**: Interactive **Sunburst Hierarchy** (`Region → Attack Method → Weapon`) and **Parallel Categories Alluvial Flow** (`Region → Attack Vector → Weapon → Target Sector`) colored by casualty severity.
- **Tab 2 — 3-Scenario Tactical War-Gaming Simulator**: Configure and compare 3 simultaneous operational scenarios (`Alpha`, `Bravo`, `Charlie`) side-by-side across ML Predicted Attack Vector, Confidence `%`, `0–120` Risk Score, and Threat Level.
- **Tab 3 — Statistical Mass-Casualty Anomaly Detector**: Isolates extreme historical casualty outliers using configurable **Z-Score thresholds (`+1σ` to `+5σ`)** with an interactive bubble timeline and outlier ledger.

---

# 🛠 Technologies Used

| Layer | Technology / Library | Purpose |
| :--- | :--- | :--- |
| **Programming Language** | Python 3.10+ / 3.14 | Core application logic, data engineering & ML pipelines |
| **Frontend Framework** | Streamlit (`>=1.40.0`) | Multi-page Cyber-Intelligence web interface & interactive widgets |
| **Data Processing** | Pandas, NumPy, OpenPyXL | High-speed `.csv` / `.xlsx` ingestion, aggregation & statistical modeling |
| **Interactive Visualization** | Plotly Express & Graph Objects | Dark-themed timelines, gauges, sunbursts, alluvial flows & heatmaps |
| **Geospatial Mapping** | Folium, Streamlit-Folium | Interactive `CartoDB Dark_Matter` marker clusters & thermal heatmaps |
| **Machine Learning** | XGBoost, LightGBM, Scikit-Learn | Multi-class tactical attack classification, label encoding & regression |
| **Artifact Serialization** | Joblib | Persistence of trained classifiers, encoders & evaluation matrices |
| **PDF Dossier Synthesis** | ReportLab, Pillow (PIL) | Automated executive intelligence briefings & project documentation PDFs |

---

# 📂 Dataset

**Global Terrorism Database (GTD)**
- Stored in `data/globalterrorism.csv` and `data/globalterrorism.xlsx`.
- Key analytical attributes utilized across the platform:
  - **Temporal & Geospatial:** `iyear`, `imonth`, `iday`, `country_txt`, `region_txt`, `provstate`, `city`, `latitude`, `longitude`
  - **Tactical & Organizational:** `gname`, `attacktype1_txt`, `weaptype1_txt`, `targtype1_txt`, `success`, `suicide`
  - **Severity & Impact:** `nkill` (Confirmed Fatalities), `nwound` (Reported Injuries), `total_casualties` (`nkill + nwound`)

---

# 🏗 Project Architecture

```text
                 Global Terrorism Database (CSV / XLSX)
                                   │
                                   ▼
             Cached Data Loader & Preprocessing Pipeline
               (utils/data_loader.py & preprocessing.py)
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
  XGBoost ML Training Pipeline                   Analytical & Risk Engines
    (train_attack_model.py)                      (utils/risk_calculator.py,
         │                                        forecasting.py, map_utils.py)
         ▼                                                   │
  Serialized Model Artifacts (.pkl / .json)                  │
  (attack_prediction_model, encoders, metrics)               │
         └─────────────────────────┬─────────────────────────┘
                                   ▼
         SENTINEL // GTI Streamlit Command Center (14 Views)
                                   │
       ┌───────────────────┬───────┴───────────┬───────────────────┐
       ▼                   ▼                   ▼                   ▼
  Geospatial &       ML Inference &      Multi-Scenario      ReportLab PDF
Tactical Charts     Risk Speedometer     War-Gaming Lab     Dossier Exports
```

---

# 🔄 Project Workflow

```text
1. Ingest GTD Dataset (.csv / .xlsx) with @st.cache_data
         │
         ▼
2. Clean & Encode 7 Core Tactical Features + Target Class
         │
         ▼
3. Train Stratified Multi-Class XGBoost Classifier (train_attack_model.py)
         │
         ▼
4. Export Calibrated Binaries (.pkl) & Evaluation Matrices (metrics.json)
         │
         ▼
5. Render Unified Cyber-Intelligence UI & 4-Category Command Navigation
         │
         ▼
6. Execute Interactive Analytics, Geospatial Mapping, War-Gaming & PDF Export
```

---

# 📁 Folder Structure

```text
Global_Threat_Intelligence_Dashboard/
│
├── assets/
│   └── logo.png                                        # Custom SENTINEL Cyber-Radar Emblem
│
├── data/
│   ├── globalterrorism.csv                             # Primary high-speed CSV dataset
│   └── globalterrorism.xlsx                            # Excel source dataset backup
│
├── models/
│   ├── attack_prediction_model.pkl                     # Trained XGBoost multi-class classifier
│   ├── feature_encoders.pkl                            # LabelEncoders for categorical inputs
│   ├── target_encoder.pkl                              # LabelEncoder for attacktype1_txt classes
│   ├── performance_metrics.pkl                         # Confusion matrix & per-class report payload
│   └── metrics.json                                    # Synchronized JSON evaluation ledger
│
├── pages/
│   ├── 1_Home.py                                       # MOD-01: Executive Summary & Seasonality
│   ├── 2_Global_Threat_Map.py                          # MOD-02: Cluster & Thermal Heatmap
│   ├── 3_Country_Analysis.py                           # MOD-03: National & Bilateral Comparison
│   ├── 4_Attack_Prediction.py                          # MOD-04: XGBoost Predictor & Analogues
│   ├── 5_Threat_Level.py                               # MOD-05: 0-120 Risk Speedometer & Posture
│   ├── 6_Forecasting.py                                # MOD-06: Trend & ±1σ Volatility Forecast
│   ├── 7_AI_Report.py                                  # MOD-07: Live Preview & PDF Dossier Export
│   ├── 8_Organization_Analysis.py                      # MOD-08: Perpetrator Group Profiling
│   ├── 9_Weapon_Analysis.py                            # MOD-09: Weapon Volume & Lethality Analysis
│   ├── 10_Target_Analysis.py                           # MOD-10: Target Sector Vulnerability Audit
│   ├── 11_Data_Explorer.py                             # MOD-11: Search Grid, CSV Export & Correlation
│   ├── 12_Model_Performance.py                         # MOD-12: Confusion Matrix & Feature Audit
│   └── 13_Threat_Simulation_Lab.py                     # MOD-13: Network Flow, War-Gaming & Anomalies
│
├── reports/
│   └── Global_Threat_Intelligence_Project_Documentation.pdf
│
├── utils/
│   ├── charts.py                                       # Dark-themed Plotly line, bar, donut & gauge builders
│   ├── dashboard_metrics.py                            # Branded header, sidebar nav & KPI card components
│   ├── data_loader.py                                  # Cached CSV/XLSX loader & derived column builder
│   ├── forecasting.py                                  # Rolling average, linear regression & ±1σ band engine
│   ├── map_utils.py                                    # Folium MarkerCluster & HeatMap layer builders
│   ├── organization_analysis.py                        # Perpetrator group ranking & KPI aggregators
│   ├── prediction.py                                   # XGBoost inference & historical analogue lookup
│   ├── preprocessing.py                                # Feature extraction & cleaning for ML training
│   ├── project_doc_generator.py                        # Combined Legacy + v2.4 Master Documentation PDF builder
│   ├── report_generator.py                             # Scoped Executive Intelligence Briefing PDF builder
│   └── risk_calculator.py                              # Data-driven 0-120 risk scoring & posture advisor
│
├── app.py                                              # MOD-00: Main Command Center Hub entrypoint
├── config.py                                           # Path registry, PAGE_REGISTRY & global Cyber-UI CSS
├── train_attack_model.py                               # End-to-end XGBoost training & calibration script
├── Global_Threat_Intelligence_Project_Documentation.pdf# Combined Master Technical Documentation PDF
├── requirements.txt                                    # Core Python package dependencies
└── README.md                                           # Project documentation
```

---

# ⚙ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/veera6102/Global_Threat_Intelligence_Dashboard.git
   cd Global_Threat_Intelligence_Dashboard
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Train / Recalibrate the Machine Learning Classifier:**
   ```bash
   python train_attack_model.py
   ```

---

# ▶ Running the Project

Launch the Streamlit Command Center:

```powershell
# Using the workspace virtual environment
.\.venv\Scripts\streamlit.exe run app.py

# Or using standard Python / Streamlit CLI
streamlit run app.py
```

Open your browser at:
```text
http://localhost:8501
```

---

# 🤖 Machine Learning Model & Calibration Metrics

- **Champion Classifier:** `XGBClassifier` (`n_estimators=120`, `max_depth=6`, `learning_rate=0.1`, `eval_metric="mlogloss"`)
- **Input Features (7):**
  1. `country_txt` (Target Jurisdiction)
  2. `region_txt` (Geographic Region)
  3. `targtype1_txt` (Target Classification Sector)
  4. `weaptype1_txt` (Primary Weapon Class)
  5. `iyear` (Operational Timeline Year)
  6. `success` (Mission Execution Condition)
  7. `suicide` (Suicide Operational Mode)
- **Target Variable:** `attacktype1_txt` (Multi-class tactical method profile: *Bombing/Explosion, Armed Assault, Assassination, Hostage Taking (Kidnapping), Facility/Infrastructure Attack, Hijacking, Unarmed Assault, etc.*)
- **Holdout Evaluation Performance (Stratified 80/20 Split):**
  - **Accuracy Score:** `90.91%`
  - **Weighted Precision:** `89.26%`
  - **Weighted Recall:** `90.91%`
  - **Balanced F1-Score:** `89.84%`

---

# 📊 Results

The upgraded **SENTINEL // GTI v2.4** platform delivers:

- **14 Integrated Analytical Views** with unified Cyber-Intelligence styling, custom radar emblem branding, and categorized navigation.
- **Dual-Layer Geospatial Mapping** combining interactive pin clusters with casualty-weighted thermal heatmaps.
- **Bilateral Country Comparisons** and **Multi-Scenario War-Gaming** (`Scenario Alpha`, `Bravo`, `Charlie`).
- **Calibrated Multi-Class ML Inference** with probability distributions, confusion matrix auditing, and historical GTD precedent matching.
- **Automated PDF Synthesis** for both scoped intelligence briefings and the [Combined Master Project Documentation PDF](Global_Threat_Intelligence_Project_Documentation.pdf).

---

# 🚀 Future Enhancements

- Integration with live OSINT / ACLED security feeds for real-time event ingestion.
- Natural-language LLM analyst assistant (RAG over historical GTD summaries).
- Deep-learning temporal graph networks (spatio-temporal GNNs) for regional contagion modeling.
- Role-based authentication and multi-analyst workspace annotations.

---

# 📸 Screenshots

Project execution screenshots are available in the repository / documentation archive:
- `Command Center Hub & Telemetry Snapshot`
- `Executive Summary & Monthly Seasonality`
- `Global Threat Map (Cluster + Thermal Heatmap)`
- `Country Intelligence & Bilateral Comparison`
- `XGBoost Attack Predictor & Historical Precedents`
- `Threat Risk Speedometer Gauge & Posture Advisor`
- `Trend Forecasting with ±1σ Volatility Envelope`
- `Threat Network Topology & 3-Scenario War-Gaming Lab`

---

# 👨‍💻 Author

**CHOPPARAPU VEERA BRAHMAM**  
*B.Tech — Artificial Intelligence & Machine Learning*  
**Vasireddy Venkatadri Institute of Technology (VVIT)**

---

# 📄 License & Disclaimer

This project is developed strictly for **educational, academic, and retrospective analytical research purposes**. All statistical trendlines, risk scores, and machine-learning predictions are derived exclusively from historical patterns in the Global Terrorism Database (GTD) and must never be used to forecast real-world tactical events.

---

# ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub!
