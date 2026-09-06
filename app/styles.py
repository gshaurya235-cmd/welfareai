"""
WelfareAI - Modern UI Styling System
Responsive defense & tactical visual styling with dark/slate aesthetic.
"""

def get_custom_css() -> str:
    return """
    <style>
    /* -------------------------------------------------------------
       WelfareAI Design System - Modern Tactical Defense Aesthetics
       ------------------------------------------------------------- */
    
    /* Import modern clean font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Top branding header container */
    .wf-topbar {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    .wf-topbar-title-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 14px;
    }

    .wf-logo-group {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .wf-shield-icon {
        font-size: 2.3rem;
        background: rgba(30, 58, 138, 0.4);
        padding: 8px 14px;
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }

    .wf-app-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #F8FAFC;
        margin: 0;
        line-height: 1.2;
    }

    .wf-app-subtitle {
        font-size: 0.95rem;
        font-weight: 500;
        color: #94A3B8;
        margin: 0;
        margin-top: 3px;
    }

    .wf-badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 5px 12px;
        border-radius: 9999px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    .wf-pill-tactical {
        background: rgba(30, 58, 138, 0.35);
        color: #93C5FD;
        border: 1px solid rgba(96, 165, 250, 0.3);
    }

    .wf-pill-demo {
        background: rgba(245, 158, 11, 0.15);
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .wf-pill-secure {
        background: rgba(16, 185, 129, 0.15);
        color: #6EE7B7;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    /* Disclaimer alert banner */
    .wf-disclaimer-banner {
        background: rgba(15, 23, 42, 0.85);
        border-left: 4px solid #3B82F6;
        border-right: 1px solid rgba(148, 163, 184, 0.15);
        border-top: 1px solid rgba(148, 163, 184, 0.15);
        border-bottom: 1px solid rgba(148, 163, 184, 0.15);
        padding: 12px 18px;
        border-radius: 8px;
        font-size: 0.84rem;
        color: #CBD5E1;
        line-height: 1.5;
        margin-bottom: 20px;
    }

    /* Cards */
    .wf-card {
        background: #1E293B;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }

    .wf-card-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F1F5F9;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Metric Boxes */
    .wf-metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 14px;
        margin-bottom: 20px;
    }

    .wf-metric-card {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 16px 20px;
        text-align: left;
    }

    .wf-metric-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 6px;
    }

    .wf-metric-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #F8FAFC;
        font-family: 'JetBrains Mono', monospace;
    }

    .wf-metric-sub {
        font-size: 0.78rem;
        color: #64748B;
        margin-top: 4px;
    }

    /* Risk Banners */
    .wf-risk-banner-low {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 1px solid #10B981;
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 18px;
    }

    .wf-risk-banner-mod {
        background: linear-gradient(90deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.05) 100%);
        border: 1px solid #F59E0B;
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 18px;
    }

    .wf-risk-banner-high {
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.05) 100%);
        border: 1px solid #EF4444;
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 18px;
    }

    /* Recommendations grid */
    .wf-rec-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 16px;
        margin-top: 14px;
    }

    .wf-rec-card {
        background: #0F172A;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 10px;
        padding: 16px;
        position: relative;
    }

    .wf-rec-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .wf-rec-desc {
        font-size: 0.85rem;
        color: #94A3B8;
        line-height: 1.5;
    }

    /* Personnel Header Strip */
    .wf-personnel-strip {
        background: #1E293B;
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 10px;
        padding: 12px 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 18px;
    }

    .wf-strip-item {
        display: flex;
        flex-direction: column;
    }

    .wf-strip-label {
        font-size: 0.72rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
    }

    .wf-strip-value {
        font-size: 0.92rem;
        color: #E2E8F0;
        font-weight: 600;
    }

    /* Streamlit overrides for polished look */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 12px 28px;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
        transition: all 0.2s ease;
        width: 100%;
    }

    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
        transform: translateY(-1px);
    }

    /* Mobile Responsive Adjustments */
    @media (max-width: 768px) {
        .wf-topbar {
            padding: 16px 18px;
        }
        .wf-app-title {
            font-size: 1.45rem;
        }
        .wf-app-subtitle {
            font-size: 0.85rem;
        }
        .wf-metric-grid {
            grid-template-columns: 1fr;
        }
        .wf-personnel-strip {
            flex-direction: column;
            align-items: flex-start;
        }
        .wf-rec-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """
