import streamlit as st

st.set_page_config(
    page_title="WelfareAI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ WelfareAI")
st.subheader("AI-Based Predictive Personnel Stress & Welfare Monitoring System")

st.write(
    "An AI-powered early-warning system designed to support "
    "personnel welfare through stress-risk prediction."
)

st.divider()

st.header("Daily Welfare Check-in")

sleep = st.slider(
    "How many hours did you sleep last night?",
    0.0, 12.0, 7.0
)

duty_hours = st.slider(
    "How many hours were you on duty today?",
    0, 24, 8
)

workload = st.slider(
    "How would you rate your workload?",
    1, 10, 5
)

night_duty = st.number_input(
    "Number of night duties this month",
    min_value=0,
    max_value=31,
    value=2
)

rest_days = st.number_input(
    "Number of rest days this month",
    min_value=0,
    max_value=31,
    value=8
)

stress = st.slider(
    "How would you rate your current stress level?",
    1, 10, 5
)

if st.button("🔍 Analyze Welfare Risk"):

    st.divider()
    st.subheader("Welfare Risk Assessment")

    if stress >= 8 or (sleep < 5 and workload >= 8):
        st.error("🔴 HIGH RISK")

    elif stress >= 5 or sleep < 6:
        st.warning("🟡 MODERATE RISK")

    else:
        st.success("🟢 LOW RISK")

    st.info(
        "This prototype is intended to support welfare monitoring "
        "and should not be used for disciplinary decisions."
    )