"""
WelfareAI - Predictive Personnel Stress and Welfare Monitoring System for Uniformed Forces
AI-Based Early-Warning Decision Support System (SIH Prototype).

IMPORTANT NOTICE:
- All pre-seeded historical records are strictly marked as 'Sample / Demo Data'
  for prototype evaluation and do not represent real personnel records.
- WelfareAI provides a prototype operational welfare and fatigue risk assessment,
  NOT a clinical or medical diagnosis.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

# Ensure local modules can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.styles import get_custom_css
from app.components import (
    render_topbar,
    render_disclaimer,
    render_personnel_strip,
    render_risk_result,
    render_factor_breakdown_chart,
    render_recommendations,
    render_trend_charts
)
from model.welfare_model import evaluate_welfare_status
from data.checkin_store import (
    load_checkin_history,
    save_new_checkin,
    reset_to_sample_data,
    DEMO_PERSONNEL_ID,
    DEMO_PERSONNEL_NAME,
    DEMO_UNIT,
    DEMO_RANK
)

# -----------------------------------------------------------------------------
# Streamlit Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="WelfareAI - Personnel Stress & Welfare System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom defense & tactical CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
if "personnel" not in st.session_state:
    st.session_state.personnel = {
        "service_id": DEMO_PERSONNEL_ID,
        "name": DEMO_PERSONNEL_NAME,
        "rank": DEMO_RANK,
        "unit": DEMO_UNIT,
        "force": "Central Armed Police Forces (CAPF)"
    }

if "latest_assessment" not in st.session_state:
    st.session_state.latest_assessment = None

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Daily Check-in"

# -----------------------------------------------------------------------------
# Sidebar: Personnel Login & Identification Screen
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🪪 Personnel Identification")
    st.caption("Active Session & Unit Assignment")

    id_mode = st.radio(
        "Identification Mode",
        ["Use Sample Personnel Profile (Demo)", "Custom Personnel Login"],
        index=0,
        help="Switch between pre-loaded sample profile and custom personnel credentials."
    )

    if id_mode == "Use Sample Personnel Profile (Demo)":
        st.info("💡 Active Profile: **Sample / Demo Data Profile** (Synthetic records for SIH prototype evaluation).")
        st.session_state.personnel = {
            "service_id": DEMO_PERSONNEL_ID,
            "name": DEMO_PERSONNEL_NAME,
            "rank": DEMO_RANK,
            "unit": DEMO_UNIT,
            "force": "Central Armed Police Forces (CAPF)"
        }
    else:
        with st.form("custom_login_form"):
            service_id = st.text_input("Service / Badge Number", value="FORCE-91024")
            name = st.text_input("Personnel Full Name", value="Inspector A. Sharma")
            rank = st.selectbox(
                "Rank / Designation",
                ["Constable", "Head Constable", "Assistant Sub-Inspector", "Sub-Inspector", "Inspector", "Assistant Commandant", "Deputy Commandant", "Commandant", "Major", "Captain", "Other"],
                index=3
            )
            force = st.selectbox(
                "Uniformed Force / Organization",
                ["Central Armed Police Forces (CRPF/BSF/CISF/ITBP/SSB)", "Indian Army", "Indian Navy", "Indian Air Force", "State Police Force", "Special Task Force"],
                index=0
            )
            unit = st.text_input("Battalion / Unit / Station", value="7th Frontier Coy")
            
            submit_login = st.form_submit_button("Update Identification")
            if submit_login:
                st.session_state.personnel = {
                    "service_id": service_id,
                    "name": name,
                    "rank": rank,
                    "unit": unit,
                    "force": force
                }
                st.success(f"Logged in as {name} ({service_id})")
                st.rerun()

    st.divider()

    st.markdown("### ⚙️ Demo Data Controls")
    st.caption("Historical dataset management for demonstration:")
    if st.button("🔄 Reset to Fresh Sample Data"):
        reset_to_sample_data()
        st.session_state.latest_assessment = None
        st.success("Sample data reset successfully!")
        st.rerun()

    st.divider()

    st.markdown("### 🔒 Privacy Guarantee")
    st.caption(
        "• End-to-end encrypted records\n"
        "• Strictly for fatigue & welfare monitoring\n"
        "• Non-punitive administrative shield\n"
        "• Non-medical prototype disclaimer"
    )

# -----------------------------------------------------------------------------
# Main Dashboard Area
# -----------------------------------------------------------------------------
render_topbar()
render_disclaimer()
render_personnel_strip(st.session_state.personnel)

# Load current check-in records
history_df = load_checkin_history()

# Quick Overview Metrics Bar
st.markdown('<div class="wf-metric-grid">', unsafe_allow_html=True)
avg_sleep = history_df['sleep_hours'].mean() if not history_df.empty else 7.0
avg_duty = history_df['duty_hours'].mean() if not history_df.empty else 8.0
total_night = int(history_df['night_duty_count'].iloc[0]) if not history_df.empty else 2
current_readiness = int(history_df['welfare_index'].iloc[0]) if not history_df.empty else 85

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown(f"""
    <div class="wf-metric-card">
        <div class="wf-metric-label">Avg Sleep (Last 14d)</div>
        <div class="wf-metric-val">{avg_sleep:.1f} <span style="font-size: 1rem; color: #64748B;">hrs</span></div>
        <div class="wf-metric-sub">{"🟢 Adequate baseline" if avg_sleep >= 6.5 else "🟡 Sub-optimal rest"}</div>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
    <div class="wf-metric-card">
        <div class="wf-metric-label">Avg Duty Load</div>
        <div class="wf-metric-val">{avg_duty:.1f} <span style="font-size: 1rem; color: #64748B;">hrs</span></div>
        <div class="wf-metric-sub">{"🟢 Standard duty" if avg_duty <= 9 else "🟡 Elevated shift load"}</div>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown(f"""
    <div class="wf-metric-card">
        <div class="wf-metric-label">Night Duties (Month)</div>
        <div class="wf-metric-val">{total_night} <span style="font-size: 1rem; color: #64748B;">shifts</span></div>
        <div class="wf-metric-sub">Circadian load indicator</div>
    </div>
    """, unsafe_allow_html=True)

with col_m4:
    st.markdown(f"""
    <div class="wf-metric-card">
        <div class="wf-metric-label">Welfare Readiness</div>
        <div class="wf-metric-val" style="color: {'#10B981' if current_readiness>=75 else ('#F59E0B' if current_readiness>=50 else '#EF4444')};">
            {current_readiness} <span style="font-size: 1rem; color: #64748B;">/100</span>
        </div>
        <div class="wf-metric-sub">Prototype Operational Index</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Main Navigation Tabs
# -----------------------------------------------------------------------------
tab_checkin, tab_analytics, tab_history, tab_protocols = st.tabs([
    "📝 Daily Welfare Check-in",
    "📊 Stress & Welfare Trends",
    "📜 Check-in History & Logs",
    "🛡️ Operational Protocols & Support"
])

# -----------------------------------------------------------------------------
# TAB 1: Daily Welfare Check-in Form & Prediction
# -----------------------------------------------------------------------------
with tab_checkin:
    col_form, col_preview = st.columns([5, 4])

    with col_form:
        st.markdown("""
        <div class="wf-card">
            <div class="wf-card-header">
                📝 Personnel Daily Welfare Check-in Form
            </div>
            <p style="font-size: 0.88rem; color: #94A3B8; margin-bottom: 16px;">
                Complete your daily operational check-in. All inputs are strictly confidential and used for fatigue early-warning.
            </p>
        """, unsafe_allow_html=True)

        with st.form("welfare_checkin_form"):
            # Sleep hours input (Preserving original parameter)
            sleep = st.slider(
                "🛌 How many hours did you sleep last night?",
                min_value=0.0,
                max_value=12.0,
                value=6.5,
                step=0.5,
                help="Recommended minimum rest for operational alertness is 7-8 hours."
            )

            # Duty hours input (Preserving original parameter)
            duty_hours = st.slider(
                "⏱️ How many hours were you on duty today?",
                min_value=0,
                max_value=24,
                value=9,
                step=1,
                help="Consecutive hours of active duty/patrol/standby."
            )

            # Workload level input (Preserving original parameter)
            workload = st.slider(
                "💼 How would you rate your workload intensity today?",
                min_value=1,
                max_value=10,
                value=5,
                help="1 = Very Light / Administrative, 10 = High Intensity Field Operation / Combat Alert."
            )

            col_sub1, col_sub2 = st.columns(2)
            with col_sub1:
                # Night-duty count input (Preserving original parameter)
                night_duty = st.number_input(
                    "🌙 Night duties completed this month",
                    min_value=0,
                    max_value=31,
                    value=3,
                    help="Total night shifts in the past 30 days."
                )

            with col_sub2:
                # Rest days input (Preserving original parameter)
                rest_days = st.number_input(
                    "🏖️ Rest days taken this month",
                    min_value=0,
                    max_value=31,
                    value=6,
                    help="Mandatory rest or off-duty recuperation days in past 30 days."
                )

            # Stress level input (Preserving original parameter)
            stress = st.slider(
                "🧠 How would you rate your current stress level?",
                min_value=1,
                max_value=10,
                value=4,
                help="1 = Completely Calm / Energized, 10 = Severely Strained / Overwhelmed."
            )

            notes = st.text_input(
                "📝 Optional Observations / Physical Notes",
                placeholder="e.g. Extended traffic standing, mild hydration headache, feeling alert...",
                help="Non-mandatory personal notes for tracking wellbeing."
            )

            st.markdown("<br>", unsafe_allow_html=True)
            # Requested button name
            predict_button = st.form_submit_button("🛡️ Predict Welfare Status", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if predict_button:
            with st.spinner("Analyzing operational fatigue and stress indicators..."):
                assessment = evaluate_welfare_status(
                    sleep_hours=sleep,
                    duty_hours=duty_hours,
                    workload=workload,
                    night_duty_count=night_duty,
                    rest_days=rest_days,
                    stress_level=stress
                )
                st.session_state.latest_assessment = assessment

                # Save new check-in to CSV as a live user entry
                save_new_checkin(
                    personnel_id=st.session_state.personnel['service_id'],
                    personnel_name=st.session_state.personnel['name'],
                    rank=st.session_state.personnel['rank'],
                    unit=st.session_state.personnel['unit'],
                    sleep_hours=sleep,
                    duty_hours=duty_hours,
                    workload=workload,
                    night_duty_count=night_duty,
                    rest_days=rest_days,
                    stress_level=stress,
                    risk_level=assessment.risk_level,
                    welfare_index=assessment.welfare_index,
                    notes=notes
                )
                st.success("✅ Welfare check-in recorded successfully!")

    with col_preview:
        if st.session_state.latest_assessment:
            res = st.session_state.latest_assessment
            render_risk_result(res)
            render_factor_breakdown_chart(res.factor_breakdown)
        else:
            st.markdown("""
            <div class="wf-card" style="text-align: center; padding: 45px 20px;">
                <div style="font-size: 3rem; margin-bottom: 12px;">🛡️</div>
                <h3 style="color: #F8FAFC; margin-bottom: 8px;">Awaiting Daily Check-in</h3>
                <p style="font-size: 0.88rem; color: #94A3B8; max-width: 320px; margin: 0 auto 16px auto;">
                    Adjust the sliders on the left and click <strong>Predict Welfare Status</strong> to generate real-time stress assessment, factor explainability, and personalized countermeasures.
                </p>
                <div style="font-size: 0.78rem; color: #64748B; border-top: 1px solid rgba(148,163,184,0.1); padding-top: 14px;">
                    ⚡ Prototype Risk Assessment Engine Active
                </div>
            </div>
            """, unsafe_allow_html=True)

    # If an assessment is available, render recommendations full width below
    if st.session_state.latest_assessment:
        render_recommendations(st.session_state.latest_assessment.recommendations)

# -----------------------------------------------------------------------------
# TAB 2: Stress & Welfare Analytics & Trends
# -----------------------------------------------------------------------------
with tab_analytics:
    st.markdown("""
    <div style="margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div>
            <h3 style="color: #F8FAFC; margin: 0;">📈 Personnel Welfare & Stress Trajectory</h3>
            <p style="color: #94A3B8; font-size: 0.88rem; margin: 4px 0 0 0;">
                Visual indicators and longitudinal trends to identify cumulative fatigue patterns.
            </p>
        </div>
        <div>
            <span class="wf-badge-pill wf-pill-demo">🧪 Includes Synthetic Sample Data</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("⚠️ Note: Historical baseline includes simulated demo records for SIH prototype evaluation and does not represent real personnel records.")
    render_trend_charts(history_df)

# -----------------------------------------------------------------------------
# TAB 3: Check-in History & Logs
# -----------------------------------------------------------------------------
with tab_history:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 14px;">
        <div>
            <h3 style="color: #F8FAFC; margin: 0;">📜 Recent Personnel Check-In History</h3>
            <p style="color: #94A3B8; font-size: 0.88rem; margin: 4px 0 0 0;">
                Historical log entries. Records marked 'Sample / Demo Data' are simulated evaluation cases.
            </p>
        </div>
        <div>
            <span class="wf-badge-pill wf-pill-demo">🧪 Clearly Labeled Demo Records</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="wf-disclaimer-banner" style="border-left-color: #F59E0B;">
        <strong>⚠️ Data Source Notice:</strong>
        Records with <code>data_source = Sample / Demo Data</code> are synthetically generated for hackathon prototype testing.
        Only entries marked <code>Live User Session</code> represent data submitted during this session.
    </div>
    """, unsafe_allow_html=True)

    if not history_df.empty:
        # Reorder and format display columns
        display_df = history_df[[
            "timestamp", "data_source", "personnel_name", "risk_level",
            "welfare_index", "sleep_hours", "duty_hours", "workload",
            "night_duty_count", "rest_days", "stress_level", "notes"
        ]].copy()

        display_df.columns = [
            "Timestamp", "Data Source", "Personnel", "Risk Level",
            "Welfare Index (0-100)", "Sleep (h)", "Duty (h)", "Workload (1-10)",
            "Night Duties", "Rest Days", "Stress (1-10)", "Notes"
        ]

        # Display table with Streamlit data editor / dataframe
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Check-In History (CSV)",
            data=csv_data,
            file_name="welfareai_checkin_history_demo.csv",
            mime="text/csv"
        )
    else:
        st.info("No check-in history found.")

# -----------------------------------------------------------------------------
# TAB 4: Operational Protocols & Support
# -----------------------------------------------------------------------------
with tab_protocols:
    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown("""
        <div class="wf-card">
            <div class="wf-card-header">
                🫁 Tactical Box Breathing Guide (4-4-4-4)
            </div>
            <p style="font-size: 0.88rem; color: #94A3B8;">
                Combat-proven autonomic nervous system regulation technique used by special operations to reset physiological stress arousal:
            </p>
            <ol style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.8;">
                <li><strong>Step 1: Inhale Slowly</strong> through the nose for <strong>4 seconds</strong>, expanding diaphragmatic breathing.</li>
                <li><strong>Step 2: Hold Breath</strong> comfortably with full lungs for <strong>4 seconds</strong>.</li>
                <li><strong>Step 3: Smooth Exhale</strong> completely through the mouth for <strong>4 seconds</strong>.</li>
                <li><strong>Step 4: Hold Empty</strong> lungs in relaxed stillness for <strong>4 seconds</strong>.</li>
                <li>Repeat cycle for 3-5 minutes whenever stress levels exceed 7/10.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="wf-card">
            <div class="wf-card-header">
                💧 High-Duty Hydration & Nutrition Standards
            </div>
            <ul style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.8;">
                <li><strong>Baseline:</strong> 3.0 to 3.5 Liters of pure water per 24 hours during standard field or checkpoint duty.</li>
                <li><strong>Electrolytes:</strong> Add oral rehydration salts (ORS) during high-humidity or perimeter patrol shifts.</li>
                <li><strong>Caffeine Discipline:</strong> Cease strong tea/coffee intake at least 4-5 hours prior to barrack sleep.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_p2:
        st.markdown("""
        <div class="wf-card">
            <div class="wf-card-header">
                📞 Confidential Personnel Welfare & Peer Support
            </div>
            <p style="font-size: 0.88rem; color: #94A3B8;">
                Support channels for uniformed personnel experiencing extreme fatigue or acute personal stress:
            </p>
            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 14px;">
                <div style="background: #0F172A; padding: 12px; border-radius: 8px; border: 1px solid rgba(148,163,184,0.15);">
                    <div style="font-size: 0.8rem; color: #64748B; text-transform: uppercase; font-weight: 600;">Unit Level</div>
                    <div style="color: #F8FAFC; font-weight: 700;">Battalion Welfare Officer & Peer Buddy Network</div>
                    <div style="font-size: 0.82rem; color: #94A3B8;">Confidential, internal welfare counseling.</div>
                </div>
                <div style="background: #0F172A; padding: 12px; border-radius: 8px; border: 1px solid rgba(148,163,184,0.15);">
                    <div style="font-size: 0.8rem; color: #64748B; text-transform: uppercase; font-weight: 600;">Tele-MANAS (Govt. of India)</div>
                    <div style="color: #F8FAFC; font-weight: 700;">Toll-Free Helpline: 14416 / 1800-891-4416</div>
                    <div style="font-size: 0.82rem; color: #94A3B8;">24/7 Multi-lingual psychological support and counseling.</div>
                </div>
                <div style="background: #0F172A; padding: 12px; border-radius: 8px; border: 1px solid rgba(148,163,184,0.15);">
                    <div style="font-size: 0.8rem; color: #64748B; text-transform: uppercase; font-weight: 600;">KIRAN Mental Health Helpline</div>
                    <div style="color: #F8FAFC; font-weight: 700;">Helpline: 1800-599-0019</div>
                    <div style="font-size: 0.82rem; color: #94A3B8;">National helpline by Ministry of Social Justice & Empowerment.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Footer Disclaimers
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.78rem; line-height: 1.6; padding: 10px 0 20px 0;">
    <strong>WelfareAI Prototype (Smart India Hackathon Evaluation Edition)</strong><br>
    Designed for Uniformed Forces Stress & Fatigue Early-Warning.<br>
    <em>Disclaimer: WelfareAI provides an operational risk assessment and does not provide clinical or medical diagnosis. All sample records are synthetic demo data.</em>
</div>
""", unsafe_allow_html=True)