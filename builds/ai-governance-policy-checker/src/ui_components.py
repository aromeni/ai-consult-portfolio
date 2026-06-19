import streamlit as st


def apply_global_styles():
    st.markdown("""
    <style>
    /* ─── Rashid AI Consult — Portfolio Theme ─────────────────────────────── */
    .main .block-container { padding-top: 1.5rem; padding-bottom: 3rem; }

    /* Sidebar */
    section[data-testid="stSidebar"] { background: #1a2744 !important; }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div { color: #cbd5e1 !important; }
    section[data-testid="stSidebar"] strong,
    section[data-testid="stSidebar"] b { color: #f1f5f9 !important; }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; }
    section[data-testid="stSidebar"] hr { border-color: #334155 !important; }
    section[data-testid="stSidebar"] .stRadio label { color: #e2e8f0 !important; font-size: 0.88rem !important; }
    section[data-testid="stSidebar"] [data-testid="stCaption"] { color: #94a3b8 !important; font-size: 0.75rem !important; }

    /* Headers */
    h1 { color: #0f172a !important; font-weight: 800 !important; letter-spacing: -0.02em; }
    h2 { color: #1a2744 !important; font-weight: 700 !important; border-left: 4px solid #2563eb; padding-left: 0.65rem; }
    h3 { color: #1e3a5f !important; font-weight: 600 !important; }

    /* Metrics */
    [data-testid="stMetric"] { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 0.7rem 1rem; box-shadow: 0 1px 2px rgba(15,23,42,0.05); }
    [data-testid="stMetricValue"] { color: #2563eb !important; font-weight: 800 !important; font-size: 1.5rem !important; }
    [data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600 !important; }

    /* Buttons */
    .stButton > button { border-radius: 8px !important; font-weight: 600 !important; transition: all 0.15s ease-out !important; }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 2px 6px rgba(15,23,42,0.12); }
    .stDownloadButton > button { border-radius: 8px !important; font-weight: 600 !important; }

    /* Inputs */
    .stTextInput > div > div > input { border-radius: 8px !important; border-color: #cbd5e1 !important; }
    .stSelectbox > div > div { border-radius: 8px !important; border-color: #cbd5e1 !important; }

    /* Dividers / Tabs / Expanders / Frames */
    hr { border-color: #e2e8f0 !important; margin: 1.25rem 0 !important; }
    .stTabs [data-baseweb="tab"] { font-weight: 600 !important; }
    [data-testid="stExpander"] { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; }
    .streamlit-expanderHeader { font-weight: 600 !important; color: #1e3a5f !important; }
    [data-testid="stDataFrame"] { border: 1px solid #e2e8f0; border-radius: 10px; }

    /* Info card component */
    .info-card {
        background: #eff6ff;
        border-left: 4px solid #2563eb;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #1e3a5f;
    }

    /* Status pills for governance */
    .gov-pill {
        display: inline-block;
        padding: 0.15rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.03em;
    }
    .gov-pill-high    { background: #fee2e2; color: #991b1b; }
    .gov-pill-medium  { background: #fef9c3; color: #854d0e; }
    .gov-pill-low     { background: #dcfce7; color: #166534; }
    .gov-pill-done    { background: #dbeafe; color: #1e40af; }
    .gov-pill-missing { background: #f1f5f9; color: #475569; }
    </style>
    """, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = ""):
    st.title(title)
    if subtitle:
        st.markdown(f"*{subtitle}*")
    st.divider()


def render_responsible_use_warning():
    st.warning(
        "**Responsible Use:** This prototype uses synthetic/demo data only. "
        "Do not use with real client records, learner data, safeguarding case details, "
        "staff HR data, personal data, confidential data, or regulated information. "
        "Outputs are not legal, safeguarding, HR, compliance, or professional advice. "
        "Human review is required before any real-world use."
    )


def render_prototype_notice():
    st.info(
        "**Prototype:** Production-style AI governance review prototype, not a production "
        "compliance, legal, safeguarding, HR, data-protection, or professional advisory system."
    )


def render_info_card(title: str, body: str):
    st.markdown(
        f'<div class="info-card"><strong>{title}</strong><br>{body}</div>',
        unsafe_allow_html=True,
    )


def render_status_box(message: str, status_type: str = "info"):
    if status_type == "warning":
        st.warning(message)
    elif status_type == "success":
        st.success(message)
    elif status_type == "error":
        st.error(message)
    else:
        st.info(message)


def render_metric_row(metrics: list):
    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            col.metric(
                label=metric.get("label", ""),
                value=metric.get("value", ""),
                delta=metric.get("delta", None),
            )


def render_completion_badge(label: str, is_complete: bool):
    prefix = "Yes" if is_complete else "-"
    st.sidebar.markdown(f"{prefix} {label}")


def render_workflow_steps(steps: list, current_step: int = 0):
    for i, step in enumerate(steps):
        if i < current_step:
            st.markdown(f"~~{step}~~")
        elif i == current_step:
            st.markdown(f"**→ {step}**")
        else:
            st.markdown(f"- {step}")
