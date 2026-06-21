"""UI helper components for Build 11 — AI Document Intelligence & Governance Agent."""

import html as _html
import streamlit as st

_CSS = """<style>
/* ─── Base ────────────────────────────────────────────────────────────────── */
.stApp { background-color: #f8fafc; }
h1 { color: #1a2744 !important; font-weight: 800 !important; letter-spacing: -0.02em; }
h2 { color: #1a2744 !important; font-weight: 700 !important; }
h3 { color: #1e3a5f !important; font-weight: 700 !important; }
h4 { color: #1e3a5f !important; font-weight: 600 !important; }

/* ─── Sidebar ─────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] { background: #1a2744 !important; }
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div { color: #cbd5e1 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; font-size: 1.05rem !important; font-weight: 800 !important; }
section[data-testid="stSidebar"] hr { border-color: #334155 !important; }
section[data-testid="stSidebar"] .stRadio label { color: #e2e8f0 !important; font-size: 0.88rem !important; }

/* ─── Metrics ─────────────────────────────────────────────────────────────── */
[data-testid="stMetricValue"] { color: #2563eb !important; font-weight: 800 !important; font-size: 1.5rem !important; }
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

/* ─── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button { border-radius: 8px !important; font-weight: 600 !important; font-size: 0.85rem !important; transition: all 0.15s ease-out !important; }
.stButton > button[kind="primary"] { background: #2563eb !important; border-color: #2563eb !important; }
.stButton > button[kind="primary"]:hover { background: #1d4ed8 !important; border-color: #1d4ed8 !important; transform: translateY(-1px); }

/* ─── Inputs ──────────────────────────────────────────────────────────────── */
.stTextInput > div > div > input { border-radius: 8px !important; border-color: #cbd5e1 !important; font-size: 0.9rem !important; }
.stTextArea textarea { border-radius: 8px !important; border-color: #cbd5e1 !important; font-size: 0.88rem !important; }
.stSelectbox > div > div { border-radius: 8px !important; border-color: #cbd5e1 !important; }
.stNumberInput > div > div > input { border-radius: 8px !important; }

/* ─── Dividers ────────────────────────────────────────────────────────────── */
hr { border-color: #e2e8f0 !important; margin: 1.25rem 0 !important; }

/* ─── Tabs ────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab"] { font-weight: 600 !important; }

/* ─── Expanders ───────────────────────────────────────────────────────────── */
.streamlit-expanderHeader { font-weight: 600 !important; color: #1e3a5f !important; }

/* ─── Download button ─────────────────────────────────────────────────────── */
.stDownloadButton > button { border-radius: 8px !important; font-weight: 600 !important; }

/* ─── Page header ─────────────────────────────────────────────────────────── */
.dp-header { padding-bottom: 0.75rem; border-bottom: 3px solid #2563eb; margin-bottom: 1.5rem; }
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

/* ─── Answer card ─────────────────────────────────────────────────────────── */
.dp-answer {
    background: #f0f9ff; border: 1.5px solid #7dd3fc;
    border-left: 5px solid #0ea5e9; border-radius: 10px;
    padding: 1.15rem 1.3rem; margin-bottom: 1.2rem;
}
.dp-answer-text { font-size: 0.97rem; color: #0c4a6e; line-height: 1.7; white-space: pre-wrap; }

/* ─── Pill badges ─────────────────────────────────────────────────────────── */
.dp-pill-row { display: flex; align-items: center; gap: 0.35rem; flex-wrap: wrap; margin-bottom: 0.4rem; }
.dp-rank-pill {
    background: #1a2744; color: #f8fafc;
    border-radius: 20px; padding: 0.15rem 0.65rem;
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.04em;
}
.dp-score-pill {
    background: #dcfce7; color: #166534;
    border-radius: 20px; padding: 0.15rem 0.65rem;
    font-size: 0.7rem; font-weight: 600;
}
.dp-doc-pill {
    background: #eff6ff; color: #1d4ed8;
    border-radius: 20px; padding: 0.15rem 0.65rem;
    font-size: 0.7rem; font-weight: 600;
}
.dp-chunk-pill {
    background: #f1f5f9; color: #475569;
    border-radius: 20px; padding: 0.15rem 0.65rem;
    font-size: 0.7rem;
}
.dp-high-pill {
    background: #fee2e2; color: #dc2626;
    border-radius: 20px; padding: 0.15rem 0.65rem;
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.02em;
}
.dp-medium-pill {
    background: #fef3c7; color: #d97706;
    border-radius: 20px; padding: 0.15rem 0.65rem;
    font-size: 0.7rem; font-weight: 600;
}
.dp-low-pill {
    background: #dbeafe; color: #1d4ed8;
    border-radius: 20px; padding: 0.15rem 0.65rem;
    font-size: 0.7rem; font-weight: 600;
}

/* ─── Result cards ────────────────────────────────────────────────────────── */
.dp-sem-result {
    background: #fff; border: 1px solid #e2e8f0;
    border-left: 3px solid #3b6cf7; border-radius: 10px;
    padding: 0.9rem 1rem; margin-bottom: 0.6rem;
}
.dp-evidence-card {
    background: #fff; border: 1px solid #e2e8f0;
    border-left: 3px solid #16a34a; border-radius: 10px;
    padding: 0.9rem 1rem; margin-bottom: 0.6rem;
}
.dp-result-id { font-size: 0.7rem; color: #94a3b8; font-family: monospace; margin-bottom: 0.3rem; }
.dp-result-text { font-size: 0.87rem; color: #334155; line-height: 1.6; margin-top: 0.3rem; }

/* ─── Chunk card ──────────────────────────────────────────────────────────── */
.dp-chunk {
    background: #fff; border: 1px solid #e2e8f0;
    border-left: 4px solid #3b6cf7; border-radius: 8px;
    padding: 0.85rem 1rem; margin-bottom: 0.6rem;
}
.dp-chunk-meta { font-size: 0.78rem; color: #4a5568; margin-bottom: 0.35rem; }
.dp-chunk-text { font-size: 0.87rem; color: #1e293b; line-height: 1.6; }

/* ─── Governance risk flag cards ──────────────────────────────────────────── */
.dp-flag-high {
    background: #fff1f2; border: 1.5px solid #fca5a5;
    border-left: 5px solid #dc2626; border-radius: 8px;
    padding: 0.85rem 1rem; margin-bottom: 0.6rem;
    color: #881337;
}
.dp-flag-medium {
    background: #fffbeb; border: 1.5px solid #fcd34d;
    border-left: 5px solid #d97706; border-radius: 8px;
    padding: 0.85rem 1rem; margin-bottom: 0.6rem;
    color: #78350f;
}
.dp-flag-low {
    background: #eff6ff; border: 1px solid #bfdbfe;
    border-left: 4px solid #3b6cf7; border-radius: 8px;
    padding: 0.85rem 1rem; margin-bottom: 0.6rem;
    color: #1e3a5f;
}
.dp-flag-title { font-weight: 700; font-size: 0.9rem; margin: 0.3rem 0 0.2rem 0; }
.dp-flag-terms { font-size: 0.82rem; font-style: italic; margin: 0.2rem 0; opacity: 0.85; }
.dp-flag-action { font-size: 0.84rem; line-height: 1.5; margin-top: 0.35rem; border-top: 1px solid currentColor; border-opacity: 0.2; padding-top: 0.35rem; opacity: 0.9; }

/* ─── Index ready bar ─────────────────────────────────────────────────────── */
.dp-index-bar {
    background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px;
    padding: 0.65rem 1rem; margin: 0.25rem 0 1rem 0;
    display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;
    font-size: 0.86rem; color: #14532d; font-weight: 500;
}
.dp-index-dot { width: 8px; height: 8px; background: #16a34a; border-radius: 50%; flex-shrink: 0; }

/* ─── Workflow diagram ────────────────────────────────────────────────────── */
.dp-workflow { display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap; padding: 0.75rem 0 1rem 0; }
.dp-wf-step { background: #1a2744; color: #f1f5f9; border-radius: 8px; padding: 0.45rem 0.9rem; font-size: 0.82rem; font-weight: 600; white-space: nowrap; }
.dp-wf-arrow { color: #94a3b8; font-size: 1rem; }

/* ─── Prototype boundary notice ──────────────────────────────────────────── */
.dp-boundary {
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;
    padding: 0.85rem 1rem; margin-top: 0.5rem;
    font-size: 0.84rem; color: #4a5568; line-height: 1.55;
}

/* ─── Inline badges ───────────────────────────────────────────────────────── */
.dp-badge { display: inline-block; background: #e0e7ff; color: #3730a3; border-radius: 20px; padding: 0.15rem 0.65rem; font-size: 0.78rem; font-weight: 600; margin-right: 0.3rem; margin-bottom: 0.2rem; }
.dp-badge-green { background: #dcfce7; color: #166534; }
.dp-badge-amber { background: #fef9c3; color: #713f12; }
.dp-badge-red { background: #fee2e2; color: #dc2626; }
</style>"""


def _e(text: str) -> str:
    return _html.escape(str(text))


def inject_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = "") -> None:
    sub = f'<p class="dp-subtitle">{_e(subtitle)}</p>' if subtitle else ""
    st.markdown(
        f'<div class="dp-header"><h1>{_e(title)}</h1>{sub}</div>',
        unsafe_allow_html=True,
    )


def render_safety_warning() -> None:
    st.markdown(
        '<div class="dp-safety">'
        "&#9888; <strong>Responsible use reminder</strong> — "
        "Use synthetic or approved documents only. Do not upload, paste, or process "
        "real learner data, safeguarding case details, confidential client records, "
        "staff HR data, personal data, or regulated information. "
        "Human review is required before acting on any output from this system."
        "</div>",
        unsafe_allow_html=True,
    )


def render_prototype_notice(text: str = "") -> None:
    body = text or (
        "This is a <strong>local prototype</strong> — no external AI APIs, no cloud services. "
        "All processing runs locally. Outputs are indicative only and require human "
        "review before any action is taken."
    )
    st.markdown(f'<div class="dp-notice">&#8505;&nbsp; {body}</div>', unsafe_allow_html=True)


def render_boundary_notice() -> None:
    st.markdown(
        '<div class="dp-boundary">'
        "<strong>Prototype boundaries</strong> &nbsp;&middot;&nbsp; "
        "No external AI APIs &nbsp;&middot;&nbsp; "
        "No cloud embeddings &nbsp;&middot;&nbsp; "
        "No production deployment &nbsp;&middot;&nbsp; "
        "Synthetic documents only &nbsp;&middot;&nbsp; "
        "All logic runs locally"
        "</div>",
        unsafe_allow_html=True,
    )


def render_workflow_diagram() -> None:
    steps = [
        "Documents", "Chunks", "Embeddings",
        "FAISS Index", "Retrieval", "Grounded Answer",
        "Governance Check", "Report",
    ]
    parts = []
    for i, step in enumerate(steps):
        parts.append(f'<span class="dp-wf-step">{_e(step)}</span>')
        if i < len(steps) - 1:
            parts.append('<span class="dp-wf-arrow">&#8594;</span>')
    st.markdown(
        f'<div class="dp-workflow">{"".join(parts)}</div>',
        unsafe_allow_html=True,
    )


def render_index_ready_bar(total_vectors: int, dimension: int, index_type: str) -> None:
    st.markdown(
        f'<div class="dp-index-bar">'
        f'<div class="dp-index-dot"></div>'
        f'<strong>Index ready</strong> &nbsp;&middot;&nbsp; '
        f'{_e(str(total_vectors))} vectors &nbsp;&middot;&nbsp; '
        f'{_e(str(dimension))}d &nbsp;&middot;&nbsp; '
        f'{_e(index_type)}'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_semantic_result_card(result: dict) -> None:
    rank = result.get("rank", "")
    score = result.get("score", 0)
    score_label = result.get("score_label", "")
    score_pct = result.get("score_pct", "")
    source = result.get("source_name", "")
    chunk_id = result.get("chunk_id", "")
    word_count = result.get("word_count", "")
    text = result.get("text", "")
    label_str = f"{score_label} ({score_pct})" if score_label and score_pct else f"{float(score):.3f}"
    text_preview = _e(text[:320]) + ("&#8230;" if len(text) > 320 else "")
    st.markdown(
        f'<div class="dp-sem-result">'
        f'<div class="dp-pill-row">'
        f'<span class="dp-rank-pill">#{_e(str(rank))}</span>'
        f'<span class="dp-score-pill">{_e(label_str)}</span>'
        f'<span class="dp-doc-pill">{_e(str(source))}</span>'
        f'<span class="dp-chunk-pill">{_e(str(word_count))}w</span>'
        f'</div>'
        f'<div class="dp-result-id">chunk id: {_e(str(chunk_id))}</div>'
        f'<div class="dp-result-text">{text_preview}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_answer_card(answer: str) -> None:
    safe = _e(answer).replace("\n", "<br>")
    st.markdown(
        f'<div class="dp-answer"><div class="dp-answer-text">{safe}</div></div>',
        unsafe_allow_html=True,
    )


def render_risk_flag_card(flag: dict) -> None:
    level = flag.get("risk_level", "Low")
    category = flag.get("category", "unknown").replace("_", " ").title()
    terms = ", ".join(flag.get("matched_terms", []))
    action = flag.get("recommended_action", "")
    css_class = (
        "dp-flag-high" if level == "High"
        else "dp-flag-medium" if level == "Medium"
        else "dp-flag-low"
    )
    pill_class = (
        "dp-high-pill" if level == "High"
        else "dp-medium-pill" if level == "Medium"
        else "dp-low-pill"
    )
    st.markdown(
        f'<div class="{css_class}">'
        f'<div class="dp-pill-row">'
        f'<span class="{pill_class}">{_e(level)} Risk</span>'
        f'</div>'
        f'<div class="dp-flag-title">{_e(category)}</div>'
        f'<div class="dp-flag-terms">Matched terms: {_e(terms)}</div>'
        f'<div class="dp-flag-action">{_e(action)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_chunk_card(chunk: dict) -> None:
    source = chunk.get("source_name", "")
    idx = chunk.get("chunk_index", "")
    wc = chunk.get("word_count", "")
    text = chunk.get("text", "")
    text_preview = _e(text[:320]) + ("&#8230;" if len(text) > 320 else "")
    st.markdown(
        f'<div class="dp-chunk">'
        f'<div class="dp-chunk-meta">'
        f'<strong>{_e(source)}</strong> &nbsp;&middot;&nbsp; '
        f'Chunk {_e(str(idx))} &nbsp;&middot;&nbsp; {_e(str(wc))} words'
        f'</div>'
        f'<div class="dp-chunk-text">{text_preview}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
