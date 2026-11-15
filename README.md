# 🌐 SENTINEL // Global Threat Intelligence Dashboard (v2.4)

An enterprise-grade **Streamlit Analytics, Geospatial Telemetry & Multi-Class Machine Learning Command Suite** built on the **Global Terrorism Database (GTD)**.

![Sentinel Emblem](assets/logo.png)

---

## 🚀 Key Platform Capabilities

- **🌐 Command Center Hub (`app.py`)**: Live global operational telemetry snapshot, 1-click XGBoost ML Calibration Hub, and 5-tab workspace launcher across all 13 analytical modules.
- **🏠 Executive Summary (`MOD-01`)**: Interactive timeline & regional scope filters, 6 glassmorphic KPI cards, automated intelligence brief banner, dual incident/casualty trajectory, attack method donut, and monthly seasonality.
- **🗺️ Global Geospatial Threat Map (`MOD-02`)**: Dual-layer **Folium MarkerCluster + Thermal Casualty Density Heatmap** with year, region, and attack-vector filters.
- **📊 Country Intelligence & Bilateral Comparison (`MOD-03`)**: National security briefings, **Country-vs-Country comparative analytics**, top impacted cities, and active perpetrator groups.
- **🔮 ML Attack Type Modeler (`MOD-04`)**: Multi-class **XGBoost Classifier** (`90.91% Accuracy`, `89.84% F1-Score`) with probability breakdown chart and **Historical GTD Precedent Matcher**.
- **🚨 Threat Level & Risk Calculator (`MOD-05`)**: Interactive `0–120` **Risk Speedometer Gauge**, component weight attribution bar chart, and defensive posture recommendations.
- **📈 Historical Trend Forecasting (`MOD-06`)**: Global, Regional, or Country rolling averages, linear regression projections, and shaded `±1σ` historical volatility envelopes.
- **📄 AI Intelligence Dossier & Documentation (`MOD-07`)**: Live on-screen executive briefing preview, ReportLab PDF dossier generator, CSV slice export, and **Combined Master Project Documentation PDF**.
- **🪖 Organization, ⚔️ Weapon & 🎯 Target Profiling (`MOD-08` to `MOD-10`)**: Volume-ranked perpetrator group profiles, per-incident weapon/target casualty lethality rankings, and geographic breakdowns.
- **🔍 Master Data Explorer (`MOD-11`)**: Multi-dimensional filtering, keyword search, CSV export, and Pearson correlation heatmap.
- **🧠 ML Model Performance Audit (`MOD-12`)**: Holdout evaluation KPIs, feature importance gain, **Multi-Class Confusion Matrix Heatmap**, and per-class Precision/Recall/F1 ledger.
- **🕸️ Threat Network & Multi-Scenario War-Gaming Lab (`MOD-13`)**: Interactive **Sunburst & Alluvial Threat Topology**, **3-Scenario Simultaneous War-Gaming Simulator**, and **Z-Score Statistical Anomaly Detector**.

---

## 🛠️ Quick Start & Execution

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Recalibrate ML Classifier & Encoders
python train_attack_model.py

# 3. Launch the Streamlit Command Suite
streamlit run app.py
```

---

## 📄 Documentation
See [Global_Threat_Intelligence_Project_Documentation.pdf](Global_Threat_Intelligence_Project_Documentation.pdf) for the combined **Legacy v1.0 Baseline + Present v2.4 Upgrade** technical documentation.
