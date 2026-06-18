"""Reusable Streamlit UI helpers for the AI Staff Training and Workshop Generator."""

import html as _html
import streamlit as st


def _e(text: str) -> str:
    return _html.escape(str(text))


# ── Global CSS ──────────────────────────────────────────────────────────────────

_CSS = """<style>
/* ─── Base ────────────────────────────────────────────────────────────────── */
.stApp { background-color: #f8fafc; }
.block-container { padding-top: 1.5rem; padding-bottom: 2.5rem; max-width: 1200px; }

/* ─── Headings ────────────────────────────────────────────────────────────── */
h1 { color: #1a2744 !important; font-weight: 800 !important; letter-spacing: -0.02em; }
h2 { color: #1a2744 !important; font-weight: 700 !important; }
h3 { color: #1e3a5f !important; font-weight: 700 !important; }
h4 { color: #1e3a5f !important; font-weight: 600 !important; }

/* ─── Sidebar ─────────────────────────────────────────────────────────────── */
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
/* Workflow status badges — higher specificity beats the sidebar span rule */
section[data-testid="stSidebar"] .wf-done { color: #4ade80 !important; font-size: 0.85rem; font-weight: 600; }
section[data-testid="stSidebar"] .wf-todo { color: #94a3b8 !important; font-size: 0.85rem; }

/* ─── Metrics ─────────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
}
[data-testid="stMetricValue"] { color: #1a2744 !important; font-weight: 800 !important; font-size: 1.5rem !important; }
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

/* ─── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button { border-radius: 8px !important; font-weight: 600 !important; font-size: 0.85rem !important; transition: all 0.15s ease-out !important; }
.stButton > button[kind="primary"] { background: #1a2744 !important; border-color: #1a2744 !important; }
.stButton > button[kind="primary"]:hover { background: #243a6e !important; border-color: #243a6e !important; transform: translateY(-1px); }
.stButton > button:hover, .stDownloadButton > button:hover { transform: translateY(-1px); box-shadow: 0 2px 6px rgba(15, 23, 42, 0.12); }
.stDownloadButton > button { border-radius: 8px !important; font-weight: 600 !important; }

/* ─── Inputs ──────────────────────────────────────────────────────────────── */
.stTextInput > div > div > input { border-radius: 8px !important; border-color: #cbd5e1 !important; font-size: 0.9rem !important; }
.stTextArea textarea { border-radius: 8px !important; border-color: #cbd5e1 !important; font-size: 0.88rem !important; }
.stSelectbox > div > div { border-radius: 8px !important; border-color: #cbd5e1 !important; }
.stNumberInput > div > div > input { border-radius: 8px !important; }

/* ─── Tabs ────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab"] { font-weight: 600 !important; }

/* ─── Expanders ───────────────────────────────────────────────────────────── */
[data-testid="stExpander"] { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; }
.streamlit-expanderHeader { font-weight: 600 !important; color: #1e3a5f !important; }

/* ─── Dataframes ──────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] { border: 1px solid #e2e8f0; border-radius: 10px; }

/* ─── Dividers ────────────────────────────────────────────────────────────── */
hr { border-color: #e2e8f0 !important; margin: 1.25rem 0 !important; }

/* ─── Page header ─────────────────────────────────────────────────────────── */
.dp-header { padding-bottom: 0.75rem; border-bottom: 3px solid #3b6cf7; margin-bottom: 1.5rem; }
.dp-header h1 { font-size: 1.75rem !important; color: #1a2744 !important; margin-bottom: 0.1rem !important; }
.dp-subtitle { color: #64748b; font-size: 0.92rem; margin: 0; }

/* ─── Safety / caution / notice ───────────────────────────────────────────── */
.dp-safety {
    background: #fffbeb; border: 1.5px solid #f59e0b;
    border-left: 5px solid #f59e0b; border-radius: 8px;
    padding: 0.8rem 1rem; margin-bottom: 1.25rem;
    color: #78350f; font-size: 0.87rem; line-height: 1.55;
}
.dp-caution {
    background: #fff1f2; border: 1.5px solid #f43f5e;
    border-left: 5px solid #f43f5e; border-radius: 8px;
    padding: 0.8rem 1rem; margin-bottom: 0.75rem;
    color: #881337; font-size: 0.9rem; font-weight: 600; line-height: 1.5;
}
.dp-notice {
    background: #eff6ff; border: 1px solid #bfdbfe;
    border-left: 4px solid #3b6cf7; border-radius: 8px;
    padding: 0.8rem 1rem; margin-bottom: 1rem;
    color: #1e3a5f; font-size: 0.87rem; line-height: 1.55;
}

/* ─── Inline badges ───────────────────────────────────────────────────────── */
.dp-badge { display: inline-block; background: #e0e7ff; color: #3730a3; border-radius: 20px; padding: 0.15rem 0.65rem; font-size: 0.78rem; font-weight: 600; margin-right: 0.3rem; margin-bottom: 0.2rem; }
.dp-badge-slate { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }
.dp-badge-green { background: #dcfce7; color: #166534; }
.dp-badge-amber { background: #fef9c3; color: #713f12; }

/* ─── Status badges ───────────────────────────────────────────────────────── */
.badge-complete { color: #16a34a; font-weight: 600; }
.badge-pending  { color: #94a3b8; }

/* ─── Placeholder ─────────────────────────────────────────────────────────── */
.dp-placeholder {
    background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 10px;
    padding: 1.5rem; text-align: center; color: #64748b; margin-bottom: 1rem;
}
.dp-placeholder h4 { color: #1a2744; font-size: 1rem; margin-bottom: 0.4rem; }
.dp-placeholder p { font-size: 0.88rem; margin: 0; line-height: 1.55; }
</style>"""


def apply_global_styles() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def inject_global_css() -> None:
    """Backwards-compatible alias for apply_global_styles()."""
    apply_global_styles()


# ── Page layout ─────────────────────────────────────────────────────────────────

def render_page_header(title: str, subtitle: str = "") -> None:
    sub = f'<p class="dp-subtitle">{_e(subtitle)}</p>' if subtitle else ""
    st.markdown(
        f'<div class="dp-header"><h1>{_e(title)}</h1>{sub}</div>',
        unsafe_allow_html=True,
    )


def render_responsible_use_warning() -> None:
    st.markdown(
        '<div class="dp-safety">'
        "⚠ <strong>Responsible use</strong> — Use synthetic or approved scenarios only. "
        "Do not enter real learner data, safeguarding case details, "
        "confidential client records, staff HR data, personal data, "
        "or regulated information. "
        "All outputs require human review before use."
        "</div>",
        unsafe_allow_html=True,
    )


def render_prototype_notice() -> None:
    st.markdown(
        '<div class="dp-notice">'
        "ℹ <strong>Prototype status</strong> — This is a production-style training prototype, "
        "not a production training compliance system. "
        "Outputs are starting points for human review — not final authority."
        "</div>",
        unsafe_allow_html=True,
    )


# ── Cards and status ────────────────────────────────────────────────────────────

def render_info_card(title: str, body: str) -> None:
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.markdown(body)


def render_status_box(message: str, status_type: str = "info") -> None:
    """status_type: "info" | "success" | "warning" | "error" """
    if status_type == "success":
        st.success(message)
    elif status_type == "warning":
        st.warning(message)
    elif status_type == "error":
        st.error(message)
    else:
        st.info(message)


def render_section_card(title: str, body: str) -> None:
    st.markdown(f"#### {title}")
    st.markdown(body)


def render_completion_badge(label: str, is_complete: bool) -> None:
    if is_complete:
        st.markdown(f"<span class='badge-complete'>✓ {_e(label)}</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span class='badge-pending'>○ {_e(label)}</span>", unsafe_allow_html=True)


# ── Metric row ──────────────────────────────────────────────────────────────────

def render_metric_row(metrics: list) -> None:
    """metrics: list of dicts with keys "label" and "value"."""
    if not metrics:
        return
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        col.metric(m.get("label", ""), m.get("value", ""))


# ── Workflow display ────────────────────────────────────────────────────────────

def render_workflow_steps(steps: list, current_step: str | None = None) -> None:
    """steps: list of step title strings. current_step: title of the active step."""
    parts = []
    for step in steps:
        if step == current_step:
            parts.append(f"**{step}**")
        else:
            parts.append(step)
    st.markdown(" → ".join(parts))


# ── Download panel ──────────────────────────────────────────────────────────────

def render_download_panel(title: str, description: str) -> None:
    st.markdown(f"#### {title}")
    st.caption(description)


# ── Report presentation ─────────────────────────────────────────────────────────

def render_report_preview_card(title: str, body: str) -> None:
    with st.container(border=True):
        st.markdown(f"#### {title}")
        with st.expander("Preview report content"):
            st.markdown(body)


def render_export_panel(
    title: str,
    markdown_available: bool = True,
    pdf_available: bool = True,
) -> None:
    formats = []
    if markdown_available:
        formats.append("Markdown")
    if pdf_available:
        formats.append("PDF")
    st.markdown(f"#### {title}")
    if formats:
        st.caption(
            f"Available formats: {' · '.join(formats)}. "
            "All exports use synthetic scenario content and require human review before use."
        )


def render_quality_checklist(items: list) -> None:
    """items: list of dicts with keys "label" and "complete" (bool)."""
    for item in items or []:
        label = item.get("label", "")
        if item.get("complete"):
            st.markdown(
                f"<span class='badge-complete'>✓ {_e(label)}</span>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<span class='badge-pending'>○ {_e(label)}</span>",
                unsafe_allow_html=True,
            )


# ── Report quality notice ───────────────────────────────────────────────────────

def render_report_quality_notice() -> None:
    st.markdown(
        '<div class="dp-notice">'
        "ℹ <strong>Report quality</strong> — All content is generated from the synthetic scenario. "
        "Review each section before use. Human review is required before real training delivery."
        "</div>",
        unsafe_allow_html=True,
    )


def render_export_options_panel() -> None:
    st.markdown("#### Export Options")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Markdown**  \nFull training pack as Markdown — editable, version-controllable, portable.")
    with col2:
        st.markdown("**PDF**  \nFormatted PDF with cover page, sections, and analytics charts — client-ready.")
    with col3:
        st.markdown("**PowerPoint**  \nPresenter-ready PPTX with 11 slides — suitable for stakeholder review.")
