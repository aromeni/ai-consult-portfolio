"""UI helper functions for the Semantic RAG Policy Assistant.

Streamlit-native helpers only. No external dependencies.
"""

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
[data-testid="stMetricValue"] { color: #1a2744 !important; font-weight: 800 !important; font-size: 1.5rem !important; }
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

/* ─── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button { border-radius: 8px !important; font-weight: 600 !important; font-size: 0.85rem !important; transition: all 0.15s ease-out !important; }
.stButton > button[kind="primary"] { background: #1a2744 !important; border-color: #1a2744 !important; }
.stButton > button[kind="primary"]:hover { background: #243a6e !important; border-color: #243a6e !important; transform: translateY(-1px); }

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

/* ─── Answer card ─────────────────────────────────────────────────────────── */
.dp-answer {
    background: #f0f9ff; border: 1.5px solid #7dd3fc;
    border-left: 5px solid #0ea5e9; border-radius: 10px;
    padding: 1.15rem 1.3rem; margin-bottom: 1.2rem;
}
.dp-answer-text { font-size: 0.97rem; color: #0c4a6e; line-height: 1.65; }

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
.dp-kw-result {
    background: #fff; border: 1px solid #e2e8f0;
    border-left: 3px solid #7c3aed; border-radius: 10px;
    padding: 0.9rem 1rem; margin-bottom: 0.6rem;
}
.dp-result-id { font-size: 0.7rem; color: #94a3b8; font-family: monospace; margin-bottom: 0.3rem; }
.dp-result-text { font-size: 0.87rem; color: #334155; line-height: 1.6; margin-top: 0.3rem; }

/* ─── Chunk card (chunking explorer) ─────────────────────────────────────── */
.dp-chunk { background: #fff; border: 1px solid #e2e8f0; border-left: 4px solid #3b6cf7; border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 0.6rem; }
.dp-chunk-meta { font-size: 0.78rem; color: #4a5568; margin-bottom: 0.3rem; }
.dp-chunk-text { font-size: 0.87rem; color: #1e293b; line-height: 1.55; }

/* ─── Legacy result card (kept for backward compat) ──────────────────────── */
.dp-result { background: #fff; border: 1px solid #e2e8f0; border-left: 4px solid #16a34a; border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 0.6rem; }
.dp-result-meta { font-size: 0.78rem; color: #4a5568; margin-bottom: 0.3rem; }

/* ─── Pipeline steps ──────────────────────────────────────────────────────── */
.dp-steps { margin: 0.25rem 0 1rem 0; }
.dp-step {
    display: flex; align-items: flex-start; gap: 0.8rem;
    padding: 0.65rem 0.9rem; background: #fff;
    border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 0.4rem;
}
.dp-step-num {
    background: #1a2744; color: #f8fafc; border-radius: 50%;
    width: 1.45rem; height: 1.45rem; min-width: 1.45rem;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.7rem; font-weight: 700; margin-top: 0.1rem;
}
.dp-step-text { font-size: 0.88rem; color: #1e293b; line-height: 1.5; }

/* ─── Phase completion grid ───────────────────────────────────────────────── */
.dp-phase-row { display: flex; flex-direction: column; gap: 0.3rem; margin: 0.25rem 0 1.25rem 0; }
.dp-phase-item {
    display: flex; align-items: flex-start; gap: 0.6rem;
    padding: 0.55rem 0.9rem; background: #f0fdf4;
    border: 1px solid #bbf7d0; border-radius: 8px;
}
.dp-phase-check { color: #16a34a; font-size: 0.82rem; flex-shrink: 0; margin-top: 0.15rem; font-weight: 700; }
.dp-phase-label { font-weight: 700; color: #14532d; font-size: 0.87rem; }
.dp-phase-desc { font-size: 0.85rem; color: #166534; }

/* ─── Comparison insight ──────────────────────────────────────────────────── */
.dp-insight {
    background: #fefce8; border: 1.5px solid #fbbf24;
    border-left: 5px solid #f59e0b; border-radius: 10px;
    padding: 0.9rem 1.1rem; margin: 0.25rem 0 1rem 0;
    color: #78350f; font-size: 0.92rem; line-height: 1.6;
}

/* ─── Comparison column headers ───────────────────────────────────────────── */
.dp-col-kw {
    background: #1a2744; color: #f1f5f9; border-radius: 8px;
    padding: 0.5rem 0.9rem; font-size: 0.85rem; font-weight: 700;
    margin-bottom: 0.6rem; letter-spacing: 0.01em;
}
.dp-col-sem {
    background: #166534; color: #f0fdf4; border-radius: 8px;
    padding: 0.5rem 0.9rem; font-size: 0.85rem; font-weight: 700;
    margin-bottom: 0.6rem; letter-spacing: 0.01em;
}

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
.dp-wf-step { background: #1a2744; color: #f1f5f9; border-radius: 8px; padding: 0.45rem 0.9rem; font-size: 0.85rem; font-weight: 600; white-space: nowrap; }
.dp-wf-arrow { color: #94a3b8; font-size: 1rem; }

/* ─── Prototype boundary notice ──────────────────────────────────────────── */
.dp-boundary {
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;
    padding: 0.85rem 1rem; margin-top: 0.5rem;
    font-size: 0.84rem; color: #4a5568; line-height: 1.55;
}

/* ─── Placeholder ─────────────────────────────────────────────────────────── */
.dp-placeholder {
    background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 10px;
    padding: 1.5rem; text-align: center; color: #64748b; margin-bottom: 1rem;
}
.dp-placeholder h4 { color: #1a2744; font-size: 1rem; margin-bottom: 0.4rem; }
.dp-placeholder p { font-size: 0.88rem; margin: 0; line-height: 1.55; }

/* ─── Inline badges ───────────────────────────────────────────────────────── */
.dp-badge { display: inline-block; background: #e0e7ff; color: #3730a3; border-radius: 20px; padding: 0.15rem 0.65rem; font-size: 0.78rem; font-weight: 600; margin-right: 0.3rem; margin-bottom: 0.2rem; }
.dp-badge-slate { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }
.dp-badge-green { background: #dcfce7; color: #166534; }
.dp-badge-amber { background: #fef9c3; color: #713f12; }
</style>"""


def _e(text: str) -> str:
    """HTML-escape a string for safe injection into custom HTML."""
    return _html.escape(str(text))


def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)


# ── Page structure ─────────────────────────────────────────────────────────────

def render_page_header(title: str, subtitle: str = ""):
    sub = f'<p class="dp-subtitle">{_e(subtitle)}</p>' if subtitle else ""
    st.markdown(
        f'<div class="dp-header"><h1>{_e(title)}</h1>{sub}</div>',
        unsafe_allow_html=True,
    )


def render_safety_warning():
    st.markdown(
        '<div class="dp-safety">'
        "⚠ <strong>Responsible use reminder</strong> — Use synthetic or approved documents only. "
        "Do not upload, paste, or process real learner data, safeguarding case details, "
        "confidential client records, staff HR data, personal data, or regulated information."
        "</div>",
        unsafe_allow_html=True,
    )


def render_prototype_notice(text: str = ""):
    body = text or (
        "This is a <strong>prototype</strong> — no external AI APIs, no cloud services. "
        "All processing runs locally. Outputs are indicative only and require human review."
    )
    st.markdown(f'<div class="dp-notice">ℹ {body}</div>', unsafe_allow_html=True)


def render_placeholder(title: str, body: str):
    st.markdown(
        f'<div class="dp-placeholder"><h4>🔜 {_e(title)}</h4><p>{_e(body)}</p></div>',
        unsafe_allow_html=True,
    )


def render_boundary_notice():
    st.markdown(
        '<div class="dp-boundary">'
        "<strong>Prototype boundaries</strong> — "
        "No external AI APIs &nbsp;·&nbsp; "
        "No cloud embeddings &nbsp;·&nbsp; "
        "No production deployment &nbsp;·&nbsp; "
        "Synthetic documents only &nbsp;·&nbsp; "
        "All logic runs locally"
        "</div>",
        unsafe_allow_html=True,
    )


# ── Metric helpers ─────────────────────────────────────────────────────────────

def render_metric_card(label: str, value: str, help_text: str = ""):
    st.metric(label=label, value=value, help=help_text or None)


# ── Workflow diagram ───────────────────────────────────────────────────────────

def render_workflow_diagram():
    steps = [
        "Documents", "Chunks", "Embeddings",
        "Vector Index", "Semantic Search", "Grounded Answer", "Report",
    ]
    parts = []
    for i, step in enumerate(steps):
        parts.append(f'<span class="dp-wf-step">{_e(step)}</span>')
        if i < len(steps) - 1:
            parts.append('<span class="dp-wf-arrow">→</span>')
    st.markdown(
        f'<div class="dp-workflow">{"".join(parts)}</div>',
        unsafe_allow_html=True,
    )


# ── Phase completion list ──────────────────────────────────────────────────────

def render_phase_completion_row(phases: list):
    """Render a vertical list of completed phase items.

    Each entry in `phases` should be a (label, description) tuple.
    """
    items_html = "".join(
        f'<div class="dp-phase-item">'
        f'<div class="dp-phase-check">✓</div>'
        f'<div><span class="dp-phase-label">{_e(label)}</span>'
        f' <span class="dp-phase-desc">— {_e(desc)}</span></div>'
        f'</div>'
        for label, desc in phases
    )
    st.markdown(f'<div class="dp-phase-row">{items_html}</div>', unsafe_allow_html=True)


# ── Pipeline steps ─────────────────────────────────────────────────────────────

def render_pipeline_steps(steps: list):
    """Render numbered pipeline prerequisite steps."""
    items_html = "".join(
        f'<div class="dp-step">'
        f'<div class="dp-step-num">{i + 1}</div>'
        f'<div class="dp-step-text">{_e(step)}</div>'
        f'</div>'
        for i, step in enumerate(steps)
    )
    st.markdown(f'<div class="dp-steps">{items_html}</div>', unsafe_allow_html=True)


# ── Index ready bar ────────────────────────────────────────────────────────────

def render_index_ready_bar(total_vectors, dimension, index_type, model_name: str):
    """Render a green 'index ready' status bar."""
    short_model = model_name.split("/")[-1] if "/" in str(model_name) else model_name
    st.markdown(
        f'<div class="dp-index-bar">'
        f'<div class="dp-index-dot"></div>'
        f'<strong>Index ready</strong> &nbsp;·&nbsp; '
        f'{_e(str(total_vectors))} vectors &nbsp;·&nbsp; '
        f'{_e(str(dimension))}d &nbsp;·&nbsp; '
        f'{_e(str(index_type))} &nbsp;·&nbsp; '
        f'model: {_e(short_model)}'
        f'</div>',
        unsafe_allow_html=True,
    )


# ── Answer card ────────────────────────────────────────────────────────────────

def render_answer_card(answer: str, caution_text: str = ""):
    """Render a styled answer card, optionally preceded by a caution banner."""
    if caution_text:
        st.markdown(
            f'<div class="dp-caution">⚠ {_e(caution_text)}</div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        f'<div class="dp-answer"><div class="dp-answer-text">{_e(answer)}</div></div>',
        unsafe_allow_html=True,
    )


# ── Result cards ───────────────────────────────────────────────────────────────

def render_semantic_result_card(result: dict):
    """Render a semantic search result as a styled card."""
    rank = result.get("rank", "")
    score = result.get("score", 0)
    doc = result.get("document_name", "")
    chunk_id = result.get("chunk_id", "")
    word_count = result.get("word_count", "")
    text = result.get("text", "")
    score_str = f"{float(score):.4f}" if score else "—"
    text_preview = _e(text[:320]) + ("…" if len(text) > 320 else "")
    st.markdown(
        f'<div class="dp-sem-result">'
        f'<div class="dp-pill-row">'
        f'<span class="dp-rank-pill">#{_e(str(rank))}</span>'
        f'<span class="dp-score-pill">score {_e(score_str)}</span>'
        f'<span class="dp-doc-pill">📄 {_e(str(doc))}</span>'
        f'<span class="dp-chunk-pill">{_e(str(word_count))}w</span>'
        f'</div>'
        f'<div class="dp-result-id">chunk id: {_e(str(chunk_id))}</div>'
        f'<div class="dp-result-text">{text_preview}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_evidence_card(item: dict):
    """Render a RAG evidence item as a styled card."""
    rank = item.get("rank", "")
    score = item.get("score", 0)
    doc = item.get("document_name", "")
    chunk_id = item.get("chunk_id", "")
    chunk_index = item.get("chunk_index", "")
    text = item.get("evidence_text", item.get("text", ""))
    source_label = item.get("source_label", "")
    score_str = f"{float(score):.4f}" if score else "—"
    text_preview = _e(text[:380]) + ("…" if len(text) > 380 else "")
    source_html = (
        f'<div class="dp-result-id">source: {_e(source_label)}</div>'
        if source_label
        else ""
    )
    st.markdown(
        f'<div class="dp-evidence-card">'
        f'<div class="dp-pill-row">'
        f'<span class="dp-rank-pill">#{_e(str(rank))}</span>'
        f'<span class="dp-score-pill">score {_e(score_str)}</span>'
        f'<span class="dp-doc-pill">📄 {_e(str(doc))}</span>'
        f'<span class="dp-chunk-pill">chunk {_e(str(chunk_index))}</span>'
        f'</div>'
        f'<div class="dp-result-id">chunk id: {_e(str(chunk_id))}</div>'
        f'{source_html}'
        f'<div class="dp-result-text">{text_preview}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_keyword_result_card(result: dict, rank: int):
    """Render a keyword search result as a styled card."""
    score = result.get("score", "")
    doc = result.get("document_name", "")
    chunk_id = result.get("chunk_id", "")
    terms = result.get("matched_terms", [])
    text = result.get("text", "")
    text_preview = _e(text[:300]) + ("…" if len(text) > 300 else "")
    terms_html = "".join(
        f'<span class="dp-badge dp-badge-slate">{_e(t)}</span>' for t in terms
    )
    st.markdown(
        f'<div class="dp-kw-result">'
        f'<div class="dp-pill-row">'
        f'<span class="dp-rank-pill">#{_e(str(rank))}</span>'
        f'<span class="dp-score-pill">score {_e(str(score))}</span>'
        f'<span class="dp-doc-pill">📄 {_e(str(doc))}</span>'
        f'</div>'
        f'<div style="margin:0.3rem 0 0.25rem 0">{terms_html}</div>'
        f'<div class="dp-result-id">chunk id: {_e(str(chunk_id))}</div>'
        f'<div class="dp-result-text">{text_preview}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ── Comparison helpers ─────────────────────────────────────────────────────────

def render_comparison_insight_card(insight: str):
    """Render the retrieval comparison insight in a styled amber card."""
    st.markdown(
        f'<div class="dp-insight">💡 {_e(insight)}</div>',
        unsafe_allow_html=True,
    )


def render_comparison_col_header(title: str, method: str = "keyword"):
    """Render a styled column header for comparison page columns."""
    css_class = "dp-col-sem" if method == "semantic" else "dp-col-kw"
    st.markdown(
        f'<div class="{css_class}">{_e(title)}</div>',
        unsafe_allow_html=True,
    )


# ── Legacy helpers (kept for backward compatibility) ───────────────────────────

def render_chunk_card(chunk: dict):
    doc = chunk.get("document_name", "")
    idx = chunk.get("chunk_index", "")
    wc = chunk.get("word_count", "")
    text = chunk.get("text", "")[:300]
    st.markdown(
        f'<div class="dp-chunk">'
        f'<div class="dp-chunk-meta">📄 <strong>{_e(doc)}</strong> · Chunk {_e(str(idx))} · {_e(str(wc))} words</div>'
        f'<div class="dp-chunk-text">{_e(text)}{"…" if len(chunk.get("text","")) > 300 else ""}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def render_search_result(result: dict):
    doc = result.get("document_name", "")
    score = result.get("score", 0)
    terms = result.get("matched_terms", [])
    text = result.get("text", "")[:300]
    badges = "".join(
        f'<span class="dp-badge dp-badge-slate">{_e(t)}</span>' for t in terms
    )
    st.markdown(
        f'<div class="dp-result">'
        f'<div class="dp-result-meta">📄 <strong>{_e(doc)}</strong> · Score: <strong>{_e(str(score))}</strong> · {badges}</div>'
        f'<div class="dp-chunk-text">{_e(text)}{"…" if len(result.get("text","")) > 300 else ""}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )
