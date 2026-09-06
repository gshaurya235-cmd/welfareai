# 🛡️ WelfareAI: Predictive Personnel Stress & Welfare Monitoring System

> **AI-Based Predictive Personnel Stress and Welfare Monitoring System for Uniformed Forces**  
> *(Armed Forces, Central Armed Police Forces, and State Police)*

[![Streamlit](https://img.shields.io/badge/Streamlit-1.62+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Prototype](https://img.shields.io/badge/Status-SIH%20Prototype-orange)](#)

---

## 🎯 Executive Overview

Uniformed personnel in defense and police organizations undergo prolonged operational shifts, demanding physical exertion, erratic sleep cycles, and critical decision-making under high-stress conditions. 

**WelfareAI** is an early-warning, proactive welfare monitoring decision-support tool. It computes a multi-factor operational fatigue index and predicts welfare risk levels before physical or cognitive exhaustion escalates, enabling commanders and personnel to apply targeted rest, workload adjustment, and hydration protocols.

> [!IMPORTANT]  
> **Privacy & Non-Medical Assessment Disclaimer**:  
> WelfareAI is an operational fatigue monitoring decision-support tool. **It does NOT provide a medical, clinical, or psychiatric diagnosis.** Check-in records are confidential and intended purely for preventive welfare and duty scheduling, never for disciplinary or punitive actions.

---

## 🌟 Key Capabilities & Features

1. **Military & Tactical UI / UX**:
   - Modern slate/tactical dark palette designed for defense forces.
   - Fully responsive across desktop workstations, laptops, tablets, and smartphones.

2. **Personnel Identification / Login Screen**:
   - Captures Service ID, Full Name, Rank, Force/Branch (e.g. CRPF, BSF, Army, State Police), and Battalion/Unit.
   - Quick toggle to inspect sample demo personnel profiles or log in with custom credentials.

3. **Daily Welfare Check-In Form**:
   - **Sleep hours** (last 24 hours)
   - **Duty hours** (consecutive active hours)
   - **Workload intensity rating** ($1 - 10$)
   - **Night-duty count** (past 30 days)
   - **Rest days taken** (past 30 days)
   - **Self-rated stress level** ($1 - 10$)
   - Personal physical notes and observations

4. **Predictive Welfare Status Engine**:
   - Triggered via the **"Predict Welfare Status"** button.
   - Computes an explainable operational risk: **🟢 Low Risk**, **🟡 Moderate Risk**, or **🔴 High Risk**.
   - Generates a **Welfare Readiness Index** ($0 - 100$) and **Stress Load Score** ($0 - 10$).

5. **Transparent Explainability**:
   - Pinpoints primary risk drivers (e.g., severe sleep deficit, extended shift exposure, circadian rhythm strain from night duties).
   - Visual factor strain breakdown chart illustrating impact of each operational component.

6. **Personalized Actionable Recommendations**:
   - 🛌 **Rest & Recovery Protocol**: Sleep hygiene, mandatory post-shift recovery windows.
   - ⚖️ **Workload & Duty Rotation**: Shift reallocation, task prioritization.
   - 💧 **Hydration & Nutrition**: Electrolyte intake targets, caffeine tapering.
   - 🧠 **Mental Resilience & Peer Support**: Tactical Box Breathing (4-4-4-4 guide), peer counselor network, Tele-MANAS helpline.

7. **Longitudinal Trend Analytics**:
   - 14-day interactive Plotly visualizations tracking Sleep vs Stress correlation.
   - Duty hours thresholds and fatigue limits.
   - Risk distribution donut chart.

8. **Check-In History & Clearly Labeled Demo Records**:
   - Pre-seeded with 14-day synthetic records clearly flagged as **`Sample / Demo Data`** for immediate demonstration during hackathon evaluations.
   - Appends new check-ins in real-time as `Live User Session` records with CSV export capabilities.

---

## 🚀 How to Run Locally

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Clone / Open Repository
```bash
git clone https://github.com/your-username/welfareai.git
cd welfareai
```

### 3. Install Dependencies
Run in your PowerShell or Command Prompt:
```bash
python -m pip install -r requirements.txt
```

### 4. Launch the Streamlit Application
```bash
python -m streamlit run app/main.py
```

Streamlit will launch the web application and automatically open your browser at:
```
Local URL: http://localhost:8501
Network URL: http://<your-local-ip>:8501
```

---

## 📂 Project Architecture

```
welfareai/
├── app/
│   ├── main.py             # Main Streamlit application and navigation
│   ├── styles.py           # Custom modern CSS design system & responsive layout
│   └── components.py       # Visual headers, metrics, risk cards & Plotly charts
├── model/
│   └── welfare_model.py    # Multi-factor predictive assessment & explainability engine
├── data/
│   ├── checkin_store.py    # CSV persistence store with labeled sample demo data
│   └── checkins.csv        # Check-in log store (generated on launch)
├── requirements.txt        # Python package dependencies
└── README.md               # Project documentation and run guide
```

---

## 🧪 Demonstration & Hackathon Testing Guide

- **Step 1:** Launch the app. Notice the active sample personnel profile (`DEMO-CRPF-4829`, Constable R. Kumar) and the 14-day historical trend charts pre-populated with clearly labeled **Sample / Demo Data**.
- **Step 2:** In the **Daily Welfare Check-in** tab, test the predictive model:
  - **Scenario A (High Fatigue):** Set Sleep = 4.0 hrs, Duty = 15 hrs, Workload = 9, Night Duties = 9, Rest Days = 2, Stress = 8. Click **Predict Welfare Status**. Observe the `🔴 HIGH RISK` warning, factor explainability breakdown, and tailored emergency rest/rotation protocols.
  - **Scenario B (Balanced Duty):** Set Sleep = 7.5 hrs, Duty = 8 hrs, Workload = 4, Night Duties = 2, Rest Days = 7, Stress = 3. Click **Predict Welfare Status**. Observe the `🟢 LOW RISK` status and optimal readiness index.
- **Step 3:** Switch to **Check-in History & Logs** to see your live submission recorded alongside the sample baseline, and export to CSV.
