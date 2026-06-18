"""Reusable UI components for Build 5 — AI Consulting Report Generator.

Matches the professional dark-navy styling established in Build 4.
"""

import html as _html
import streamlit as st


def _e(text: str) -> str:
    return _html.escape(str(text))


_CSS = """<style>
/* Base */
.stApp { background-color: #f8fafc; }
.block-container { padding-top: 1.5rem; padding-bottom: 2.5rem; max-width: 1200px; }

/* Headings */
h1 { color: #1a2744 !important; font-weight: 800 !important; letter-spacing: -0.02em; }
h2 { color: #1a2744 !important; font-weight: 700 !important; }
h3 { color: #1e3a5f !important; font-weight: 700 !important; }
h4 { color: #1e3a5f !important; font-weight: 600 !important; }

/* Sidebar */
section[data-testid="stSidebar"] { background: #1a2744 !important; }
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div { color: #cbd5e1 !important; }
section[data-testid="stSidebar"] span { color: #cbd5e1; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; font-size: 1.05rem !important; font-weight: 800 !important; }
section[data-testid="stSidebar"] hr { border-color: #334155 !important; }
section[data-testid="stSidebar"] .stRadio label { color: #e2e8f0 !important; font-size: 0.88rem !important; }
section[data-testid="stSidebar"] .wf-done { color: #4ade80 !important; font-size: 0.85rem; font-weight: 600; }
section[data-testid="stSidebar"] .wf-todo { color: #94a3b8 !important; font-size: 0.85rem; }

/* Metrics */
[data-testid="stMetric"] { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 0.7rem 1rem; box-shadow: 0 1px 2px rgba(15,23,42,0.05); }
[data-testid="stMetricValue"] { color: #1a2744 !important; font-weight: 800 !important; font-size: 1.5rem !important; }
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.05em; }

/* Buttons */
.stButton > button { background: #3b6cf7 !important; color: #ffffff !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; padding: 0.5rem 1.25rem !important; transition: background 0.15s ease; }
.stButton > button:hover { background: #2a55d6 !important; }
.stDownloadButton > button { background: #1a2744 !important; color: #ffffff !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; }

/* Expanders */
.streamlit-expanderHeader { background: #f1f5f9 !important; border-radius: 8px !important; font-weight: 600 !important; color: #1e3a5f !important; }
.streamlit-expanderContent { background: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 0 0 8px 8px !important; }

/* Page header */
.dp-header { padding-bottom: 0.75rem; border-bottom: 3px solid #3b6cf7; margin-bottom: 1.5rem; }
.dp-header h1 { font-size: 1.75rem !important; color: #1a2744 !important; margin-bottom: 0.1rem !important; }
.dp-subtitle { color: #64748b; font-size: 0.92rem; margin: 0; }

/* Status cards */
.dp-safety { background: #fffbeb; border: 1.5px solid #f59e0b; border-left: 5px solid #f59e0b; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 1.25rem; color: #78350f; font-size: 0.87rem; line-height: 1.55; }
.dp-notice { background: #eff6ff; border: 1px solid #bfdbfe; border-left: 4px solid #3b6cf7; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 1rem; color: #1e3a5f; font-size: 0.87rem; line-height: 1.55; }
.dp-success { background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #16a34a; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 1rem; color: #14532d; font-size: 0.87rem; line-height: 1.55; }
.dp-error { background: #fef2f2; border: 1px solid #fecaca; border-left: 4px solid #dc2626; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 1rem; color: #7f1d1d; font-size: 0.87rem; line-height: 1.55; }

/* Info card */
.dp-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(15,23,42,0.06); }
.dp-card-title { font-weight: 700; color: #1a2744; font-size: 0.95rem; margin-bottom: 0.35rem; }
.dp-card-body { color: #334155; font-size: 0.87rem; line-height: 1.6; }

/* Risk level pills */
.dp-pill { display: inline-block; border-radius: 20px; padding: 0.15rem 0.7rem; font-size: 0.76rem; font-weight: 700; letter-spacing: 0.03em; }
.dp-pill-critical { background: #fee2e2; color: #991b1b; }
.dp-pill-high { background: #ffedd5; color: #9a3412; }
.dp-pill-medium { background: #fef9c3; color: #854d0e; }
.dp-pill-low { background: #dcfce7; color: #14532d; }
</style>"""


def apply_global_styles() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = "") -> None:
    sub = f'<p class="dp-subtitle">{_e(subtitle)}</p>' if subtitle else ""
    st.markdown(
        f'<div class="dp-header"><h1>{_e(title)}</h1>{sub}</div>',
        unsafe_allow_html=True,
    )


def render_responsible_use_warning() -> None:
    st.markdown(
        '<div class="dp-safety">'
        "⚠ <strong>Responsible use</strong> — All scenarios in this prototype are synthetic. "
        "Do not enter real learner data, safeguarding information, HR records, confidential "
        "client records, personal data, or regulated information. Outputs require human review "
        "before real-world use. This prototype does not provide legal, safeguarding, HR, "
        "compliance, financial, or professional advice."
        "</div>",
        unsafe_allow_html=True,
    )


def render_prototype_notice() -> None:
    st.markdown(
        '<div class="dp-notice">'
        "ℹ <strong>Prototype status</strong> — This is a production-style consulting report "
        "prototype, not a production consulting or compliance system. All outputs are indicative "
        "only. Human expert review is required before any real-world use."
        "</div>",
        unsafe_allow_html=True,
    )


def render_info_card(title: str, body: str) -> None:
    st.markdown(
        f'<div class="dp-card">'
        f'<div class="dp-card-title">{_e(title)}</div>'
        f'<div class="dp-card-body">{_e(body)}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def render_status_box(message: str, status_type: str = "info") -> None:
    css_class = {
        "info": "dp-notice",
        "success": "dp-success",
        "warning": "dp-safety",
        "error": "dp-error",
    }.get(status_type, "dp-notice")
    st.markdown(f'<div class="{css_class}">{_e(message)}</div>', unsafe_allow_html=True)


def render_metric_row(metrics: list) -> None:
    if not metrics:
        return
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            st.metric(
                label=m.get("label", ""),
                value=m.get("value", ""),
                delta=m.get("delta"),
            )


def render_completion_badge(label: str, is_complete: bool) -> None:
    if is_complete:
        st.markdown(f"<span class='wf-done'>✓ {_e(label)}</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span class='wf-todo'>○ {_e(label)}</span>", unsafe_allow_html=True)
