# 🌍 Global Threat Intelligence Dashboard

A web-based Threat Intelligence Dashboard developed using **Python**, **Streamlit**, and **Machine Learning** to analyze historical terrorism incidents from the **Global Terrorism Database (GTD)**. The dashboard provides interactive visualizations, threat analysis, attack prediction, forecasting, and report generation to help users understand global terrorism patterns.

---

# 📌 Table of Contents

- Project Overview
- Objectives
- Features
- Technologies Used
- Dataset
- Project Architecture
- Project Workflow
- Folder Structure
- Installation
- Running the Project
- Dashboard Pages
- Machine Learning Model
- Results
- Future Enhancements
- Screenshots
- Author

---

# 📖 Project Overview

The Global Threat Intelligence Dashboard is designed to analyze historical terrorism incidents using data visualization and machine learning techniques.

The dashboard allows users to:

- Explore terrorism incidents worldwide
- Analyze country-wise attack statistics
- Predict attack types
- Calculate threat levels
- View historical trends
- Analyze organizations, weapons, and targets
- Download intelligence reports

The application is built with a simple and user-friendly interface using Streamlit.

---

# 🎯 Objectives

The main objectives of this project are:

- Analyze terrorism incidents using historical data.
- Visualize attack patterns with interactive charts and maps.
- Predict attack types using Machine Learning.
- Calculate threat levels for selected incidents.
- Generate downloadable intelligence reports.
- Help students and researchers understand global terrorism trends.

---

# ✨ Features

## 🏠 Home Dashboard

- Dashboard overview
- Total incidents
- Total countries
- Total organizations
- Key statistics

---

## 🌍 Global Threat Map

- Interactive world map
- Terrorism incident locations
- Country-wise visualization

---

## 🌎 Country Analysis

- Country selection
- Number of attacks
- Most common attack types
- Most active terrorist organizations
- Year-wise trends

---

## 🤖 Attack Prediction

Machine Learning predicts attack type using:

- Country
- Region
- Weapon Type
- Target Type

Predicted Output:

- Bombing
- Armed Assault
- Assassination
- Kidnapping
- Hijacking
- Other Attack Types

---

## 🚨 Threat Level Calculator

Calculates threat level using:

- Number of attacks
- Casualties
- Target importance

Threat Levels:

- Low
- Medium
- High
- Critical

---

## 📈 Forecasting

Shows:

- Historical attack trends
- Year-wise incident growth
- Future trend estimation

---

## 📄 AI Intelligence Report

Generate downloadable PDF reports containing:

- Incident summary
- Threat level
- Country analysis
- Recommendations

---

## 🏴 Organization Analysis

Analyze terrorist organizations by:

- Total attacks
- Active countries
- Attack trends
- Most used attack types

---

## 🔫 Weapon Analysis

Shows:

- Most used weapons
- Weapon trends
- Countries using specific weapons
- Weapon statistics

---

## 🎯 Target Analysis

Analyze:

- Government targets
- Military
- Police
- Civilians
- Business
- Infrastructure

---

## 📊 Data Explorer

Features:

- Search incidents
- Filter by year
- Filter by country
- Download filtered dataset

---

## ℹ️ About Page

Contains:

- Project details
- Technologies
- Dataset information
- Developer details

---

# 🛠 Technologies Used

## Programming Language

- Python

## Frontend

- Streamlit

## Data Processing

- Pandas
- NumPy

## Visualization

- Plotly
- Folium
- Matplotlib

## Machine Learning

- Scikit-learn

## Model Storage

- Joblib

## Report Generation

- ReportLab

---

# 📂 Dataset

Dataset Used:

**Global Terrorism Database (GTD)**

The dataset contains historical terrorism incident records including:

- Country
- Region
- City
- Attack Type
- Weapon Type
- Target Type
- Terrorist Organization
- Casualties
- Year

---

# 🏗 Project Architecture

```
                 GTD Dataset
                      │
                      ▼
           Data Preprocessing
                      │
                      ▼
        Machine Learning Training
                      │
                      ▼
          Trained ML Model (.pkl)
                      │
                      ▼
              Streamlit Dashboard
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
 Visualizations   Prediction      Reports
```

---

# 🔄 Project Workflow

```
Collect Dataset
        │
        ▼
Preprocess Data
        │
        ▼
Train ML Model
        │
        ▼
Save Model
        │
        ▼
Build Dashboard
        │
        ▼
Visualize Data
        │
        ▼
Generate Reports
```

---

# 📁 Project Structure

```
Global_Threat_Intelligence_Dashboard/

│
├── assets/
│   └── logo.png
│
├── data/
│   └── globalterrorism.csv
│
├── models/
│   ├── attack_prediction_model.pkl
│   ├── feature_encoders.pkl
│   ├── target_encoder.pkl
│   └── metrics.json
│
├── pages/
│   ├── 1_Home.py
│   ├── 2_Global_Threat_Map.py
│   ├── 3_Country_Analysis.py
│   ├── 4_Attack_Prediction.py
│   ├── 5_Threat_Level.py
│   ├── 6_Forecasting.py
│   ├── 7_AI_Report.py
│   ├── 8_Organization_Analysis.py
│   ├── 9_Weapon_Analysis.py
│   ├── 10_Target_Analysis.py
│   ├── 11_Data_Explorer.py
│   └── 12_About.py
│
├── utils/
│   ├── charts.py
│   ├── data_loader.py
│   ├── forecasting.py
│   ├── prediction.py
│   ├── preprocessing.py
│   ├── report_generator.py
│   └── risk_calculator.py
│
├── reports/
│
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Global_Threat_Intelligence_Dashboard.git
```

Move into the project folder

```bash
cd Global_Threat_Intelligence_Dashboard
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Running the Project

Run the Streamlit application

```bash
streamlit run app.py
```

Open the browser

```
http://localhost:8501
```

---

# 🤖 Machine Learning Model

Algorithm Used:

- Random Forest Classifier *(or replace with the model you actually trained, e.g., XGBoost)*

Input Features:

- Country
- Region
- Weapon Type
- Target Type

Output:

- Predicted Attack Type

Model files are stored inside:

```
models/
```

---

# 📊 Results

The dashboard successfully provides:

- Interactive global visualization
- Country-wise analysis
- Attack prediction
- Threat level assessment
- Historical trend analysis
- Organization analysis
- Weapon analysis
- Target analysis
- Downloadable reports

---

# 🚀 Future Enhancements

Possible improvements include:

- Live threat intelligence feeds
- Real-time news integration
- AI chatbot assistant
- Deep learning prediction models
- User authentication
- Cloud deployment
- Advanced analytics
- Mobile-responsive interface

---

# 📸 Screenshots

Add screenshots here after running the project.

Example:

```
screenshots/

Home.png

Global_Map.png

Country_Analysis.png

Attack_Prediction.png

Threat_Level.png

Forecasting.png

Organization.png

Weapon.png

Target.png

Explorer.png
```

---

# 👨‍💻 Author

**CHOPPARAPU VEERA BRAHMAM**

B.Tech Artificial Intelligence & Machine Learning

Vasireddy Venkatadri Institute of Technology (VVIT)

---

# 📄 License

This project is developed for educational and learning purposes.

---

# ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub.

Thank you for visiting this repository!
