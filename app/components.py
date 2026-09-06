"""
WelfareAI - UI Components & Visualizations
Provides reusable visual widgets, Plotly analytics, and defense-styled layouts.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Any

def render_topbar():
    """Renders the top branding header with tactical identity and badges."""
    st.markdown("""
    <div class="wf-topbar">
        <div class="wf-topbar-title-row">
            <div class="wf-logo-group">
                <div class="wf-shield-icon">🛡️</div>
                <div>
                    <h1 class="wf-app-title">WelfareAI</h1>
                    <p class="wf-app-subtitle">AI-Based Predictive Personnel Stress & Welfare Monitoring System</p>
                </div>
            </div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <span class="wf-badge-pill wf-pill-tactical">🛡️ Uniformed Forces Edition</span>
                <span class="wf-badge-pill wf-pill-secure">🔒 Confidential & Encrypted</span>
                <span class="wf-badge-pill wf-pill-demo">🧪 Prototype Demo</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_disclaimer():
    """Renders the non-medical operational welfare disclaimer."""
    st.markdown("""
    <div class="wf-disclaimer-banner">
        <strong>🔒 Privacy & Non-Medical Assessment Notice:</strong>
        WelfareAI is designed strictly as an operational fatigue monitoring and predictive welfare early-warning tool for uniformed forces.
        <strong>This system provides an operational prototype risk assessment and does NOT provide a medical or psychiatric diagnosis.</strong>
        Data collected is confidential and intended solely to support personnel welfare and duty scheduling, never for disciplinary or punitive actions.
    </div>
    """, unsafe_allow_html=True)

def render_personnel_strip(personnel: Dict[str, str]):
    """Renders active personnel profile identification bar."""
    st.markdown(f"""
    <div class="wf-personnel-strip">
        <div class="wf-strip-item">
            <span class="wf-strip-label">Service / Badge No</span>
            <span class="wf-strip-value">{personnel.get('service_id', 'CRPF-4829')}</span>
        </div>
        <div class="wf-strip-item">
            <span class="wf-strip-label">Personnel Name</span>
            <span class="wf-strip-value">{personnel.get('name', 'Constable R. Kumar')}</span>
        </div>
        <div class="wf-strip-item">
            <span class="wf-strip-label">Rank</span>
            <span class="wf-strip-value">{personnel.get('rank', 'Constable (GD)')}</span>
        </div>
        <div class="wf-strip-item">
            <span class="wf-strip-label">Force / Branch</span>
            <span class="wf-strip-value">{personnel.get('force', 'Central Armed Police Forces')}</span>
        </div>
        <div class="wf-strip-item">
            <span class="wf-strip-label">Unit / Battalion</span>
            <span class="wf-strip-value">{personnel.get('unit', '104 Rapid Action Battalion')}</span>
        </div>
        <div class="wf-strip-item">
            <span class="wf-strip-label">Status</span>
            <span class="wf-strip-value" style="color: #34D399;">● Active Field Duty</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_risk_result(result):
    """Renders the comprehensive risk assessment, factor explanation, and score."""
    banner_class = "wf-risk-banner-low"
    if result.risk_level == "High":
        banner_class = "wf-risk-banner-high"
    elif result.risk_level == "Moderate":
        banner_class = "wf-risk-banner-mod"

    st.markdown(f"""
    <div class="{banner_class}">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
                <span style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: {result.risk_color};">
                    PREDICTED WELFARE STATUS (PROTOTYPE RISK ASSESSMENT)
                </span>
                <h2 style="font-size: 2.2rem; font-weight: 900; margin: 4px 0 0 0; color: #F8FAFC; line-height: 1.1;">
                    {result.risk_badge}
                </h2>
            </div>
            <div style="display: flex; gap: 24px; text-align: right;">
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Welfare Readiness Index</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #F8FAFC; font-family: 'JetBrains Mono', monospace;">
                        {result.welfare_index}<span style="font-size: 1.1rem; color: #64748B;">/100</span>
                    </div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Stress Load Index</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: {result.risk_color}; font-family: 'JetBrains Mono', monospace;">
                        {result.stress_score}<span style="font-size: 1.1rem; color: #64748B;">/10</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Explanation Section
    st.markdown("""
    <div class="wf-card">
        <div class="wf-card-header">
            🔍 Explainability: Why was this result generated?
        </div>
        <p style="font-size: 0.88rem; color: #94A3B8; margin-bottom: 12px;">
            WelfareAI evaluates multiple physiological and operational strain factors to determine readiness and fatigue risk:
        </p>
    """, unsafe_allow_html=True)

    for factor in result.primary_factors:
        st.markdown(f"""
        <div style="display: flex; align-items: flex-start; gap: 10px; margin-bottom: 8px; font-size: 0.92rem; color: #E2E8F0;">
            <span style="color: {result.risk_color}; font-size: 1rem;">▶</span>
            <span>{factor}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

def render_factor_breakdown_chart(factor_breakdown: Dict[str, float]):
    """Renders a modern horizontal bar chart showing the strain impact of each operational factor."""
    factors = list(factor_breakdown.keys())
    values = list(factor_breakdown.values())

    colors = []
    for v in values:
        if v >= 65:
            colors.append("#EF4444")
        elif v >= 40:
            colors.append("#F59E0B")
        else:
            colors.append("#10B981")

    fig = go.Figure(go.Bar(
        x=values,
        y=factors,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(255, 255, 255, 0.15)', width=1)
        ),
        text=[f"{v:.0f}%" for v in values],
        textposition='outside',
        textfont=dict(color='#F8FAFC', family='Inter', size=11)
    ))

    fig.update_layout(
        title=dict(
            text="Operational Factor Strain Breakdown (% Impact)",
            font=dict(size=14, color="#E2E8F0", family="Inter")
        ),
        xaxis=dict(
            range=[0, 115],
            gridcolor="rgba(148, 163, 184, 0.1)",
            color="#94A3B8",
            tickfont=dict(family="Inter", size=10)
        ),
        yaxis=dict(
            autorange="reversed",
            color="#E2E8F0",
            tickfont=dict(family="Inter", size=11, weight="bold")
        ),
        paper_bgcolor="#1E293B",
        plot_bgcolor="#0F172A",
        margin=dict(l=130, r=40, t=45, b=30),
        height=260
    )

    st.plotly_chart(fig, use_container_width=True)

def render_recommendations(recommendations: Dict[str, List[Dict[str, str]]]):
    """Renders categorized, actionable wellness and operational recommendations."""
    st.markdown("""
    <div class="wf-card">
        <div class="wf-card-header">
            📋 Personalized Operational Welfare Recommendations
        </div>
        <p style="font-size: 0.88rem; color: #94A3B8; margin-bottom: 16px;">
            Targeted countermeasures designed to reduce fatigue and restore operational readiness:
        </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🛌 Rest & Sleep Protocol")
        for item in recommendations.get("rest", []):
            st.markdown(f"""
            <div class="wf-rec-card" style="margin-bottom: 10px;">
                <div class="wf-rec-title">💤 {item['title']}</div>
                <div class="wf-rec-desc">{item['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### ⚖️ Workload & Duty Management")
        for item in recommendations.get("workload", []):
            st.markdown(f"""
            <div class="wf-rec-card" style="margin-bottom: 10px;">
                <div class="wf-rec-title">🛡️ {item['title']}</div>
                <div class="wf-rec-desc">{item['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 💧 Hydration & Nutrition Support")
        for item in recommendations.get("hydration", []):
            st.markdown(f"""
            <div class="wf-rec-card" style="margin-bottom: 10px;">
                <div class="wf-rec-title">💧 {item['title']}</div>
                <div class="wf-rec-desc">{item['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### 🧠 Mental Resilience & Peer Support")
        for item in recommendations.get("support", []):
            st.markdown(f"""
            <div class="wf-rec-card" style="margin-bottom: 10px;">
                <div class="wf-rec-title">🤝 {item['title']}</div>
                <div class="wf-rec-desc">{item['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

def render_trend_charts(df: pd.DataFrame):
    """Renders historical trend charts with clear labeling of sample/demo records."""
    if df.empty:
        st.info("No historical check-in records available to display trends.")
        return

    # Sort chronological for plotting
    plot_df = df.copy()
    plot_df['date_dt'] = pd.to_datetime(plot_df['date'])
    plot_df = plot_df.sort_values(by='date_dt').tail(14)

    # 1. Dual Chart: Sleep Hours & Stress Score Trend
    fig1 = go.Figure()

    # Sleep Hours Line
    fig1.add_trace(go.Scatter(
        x=plot_df['date'],
        y=plot_df['sleep_hours'],
        name="Sleep Hours (hrs)",
        mode='lines+markers',
        line=dict(color='#38BDF8', width=3),
        marker=dict(size=7, symbol='circle')
    ))

    # Stress Score Line
    fig1.add_trace(go.Scatter(
        x=plot_df['date'],
        y=plot_df['stress_level'],
        name="Self-Reported Stress (1-10)",
        mode='lines+markers',
        line=dict(color='#F43F5E', width=3, dash='dot'),
        marker=dict(size=7, symbol='diamond')
    ))

    # Target Sleep Reference Line (7 hrs)
    fig1.add_hline(
        y=7.0, line_dash="dash", line_color="rgba(52, 211, 153, 0.6)",
        annotation_text="Optimal Rest (7 hrs)", annotation_position="bottom right",
        annotation_font=dict(color="#34D399", size=10)
    )

    fig1.update_layout(
        title=dict(
            text="14-Day Trajectory: Sleep Duration vs Stress Level Trend",
            font=dict(size=14, color="#E2E8F0", family="Inter")
        ),
        xaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)", color="#94A3B8"),
        yaxis=dict(title="Hours / Stress Score", gridcolor="rgba(148, 163, 184, 0.1)", color="#94A3B8"),
        paper_bgcolor="#1E293B",
        plot_bgcolor="#0F172A",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#CBD5E1")),
        margin=dict(l=40, r=30, t=50, b=40),
        height=300
    )

    st.plotly_chart(fig1, use_container_width=True)

    # 2. Split Row: Duty Load vs Rest & Risk Category Distribution
    col1, col2 = st.columns([3, 2])

    with col1:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=plot_df['date'],
            y=plot_df['duty_hours'],
            name="Daily Duty Hours",
            marker_color='#6366F1'
        ))
        fig2.add_hline(
            y=12.0, line_dash="dash", line_color="#EF4444",
            annotation_text="Fatigue Threshold (12h)", annotation_position="top left",
            annotation_font=dict(color="#EF4444", size=10)
        )
        fig2.update_layout(
            title=dict(
                text="Daily Duty Hours Distribution",
                font=dict(size=13, color="#E2E8F0", family="Inter")
            ),
            xaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)", color="#94A3B8"),
            yaxis=dict(title="Duty Hours", gridcolor="rgba(148, 163, 184, 0.1)", color="#94A3B8"),
            paper_bgcolor="#1E293B",
            plot_bgcolor="#0F172A",
            margin=dict(l=40, r=20, t=45, b=30),
            height=260
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        risk_counts = plot_df['risk_level'].value_counts().reset_index()
        risk_counts.columns = ['Risk', 'Count']
        color_map = {"Low": "#10B981", "Moderate": "#F59E0B", "High": "#EF4444"}

        fig3 = px.pie(
            risk_counts,
            names='Risk',
            values='Count',
            title="14-Day Risk Category Proportion",
            color='Risk',
            color_discrete_map=color_map,
            hole=0.45
        )
        fig3.update_layout(
            paper_bgcolor="#1E293B",
            font=dict(color="#E2E8F0", family="Inter"),
            margin=dict(l=20, r=20, t=45, b=20),
            height=260,
            showlegend=True,
            legend=dict(font=dict(color="#CBD5E1"))
        )
        st.plotly_chart(fig3, use_container_width=True)
