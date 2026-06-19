"""UI helper functions for the Document Intelligence / RAG Demo.

All rendering uses st.markdown with unsafe_allow_html=True for custom HTML/CSS.
No external dependencies beyond Streamlit.
"""

import streamlit as st

# ── Global CSS ────────────────────────────────────────────────────────────────

_CSS = """<style>

/* ── App background ── */
.stApp { background-color: #f8fafc; }

/* ── Headings ── */
h1 { color: #1a2744 !important; font-weight: 800 !important; letter-spacing: -0.02em; }
h2 { color: #1a2744 !important; font-weight: 700 !important; }
h3 { color: #1e3a5f !important; font-weight: 700 !important; }

/* ── Sidebar (dark navy) ── */
section[data-testid="stSidebar"] { background: #1a2744 !important; }
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div { color: #cbd5e1 !important; }
section[data-testid="stSidebar"] h1 {
    color: #f1f5f9 !important;
    font-size: 1.15rem !important;
    font-weight: 800 !important;
}
section[data-testid="stSidebar"] [data-testid="stCaption"] {
    color: #64748b !important;
    font-size: 0.75rem !important;
}
section[data-testid="stSidebar"] hr { border-color: #334155 !important; }

/* ── Native metric value/label ── */
[data-testid="stMetricValue"] { color: #2563eb !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.8rem !important; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.15s ease;
}
.stDownloadButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* ── Divider ── */
hr { border-color: #e2e8f0 !important; margin: 1rem 0 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] { font-weight: 600 !important; }
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid #e2e8f0;
    margin-bottom: 0.5rem;
}

/* ── Expander ── */
[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: #1e3a5f !important;
}

/* ── ─────────────────────────────────────── ── */
/* ── Custom HTML components (dp- prefix)    ── */
/* ── ─────────────────────────────────────── ── */

/* Page header */
.dp-page-header {
    padding-bottom: 0.75rem;
    border-bottom: 3px solid #3b6cf7;
    margin-bottom: 1.5rem;
}
.dp-page-header h1 {
    font-size: 1.75rem !important;
    color: #1a2744 !important;
    margin-bottom: 0.15rem !important;
}
.dp-page-subtitle {
    color: #4a5568;
    font-size: 0.95rem;
    margin: 0;
}

/* Safety warning card */
.dp-safety {
    background: #fffbeb;
    border: 1.5px solid #f59e0b;
    border-left: 5px solid #f59e0b;
    border-radius: 8px;
    padding: 0.85rem 1rem;
    margin-bottom: 1.25rem;
    color: #78350f;
    font-size: 0.9rem;
    line-height: 1.55;
}

/* Prototype / info notice */
.dp-notice {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 4px solid #3b6cf7;
    border-radius: 8px;
    padding: 0.85rem 1rem;
    margin-bottom: 1rem;
    color: #1e3a5f;
    font-size: 0.9rem;
    line-height: 1.55;
}

/* Generic white card */
.dp-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.dp-card h4 {
    color: #1a2744;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
}
.dp-card p {
    color: #4a5568;
    font-size: 0.9rem;
    margin: 0;
    line-height: 1.55;
}

/* Evidence / search result card */
.dp-evidence {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #3b6cf7;
    border-radius: 8px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.65rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.dp-ev-meta {
    font-size: 0.8rem;
    color: #4a5568;
    margin-bottom: 0.35rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    align-items: center;
}
.dp-ev-doc { font-weight: 700; color: #1a2744; }
.dp-ev-sep { color: #cbd5e1; }
.dp-ev-snippet {
    color: #1e293b;
    font-size: 0.9rem;
    line-height: 1.55;
    border-left: 2px solid #cbd5e1;
    padding-left: 0.65rem;
    margin: 0.4rem 0;
}
.dp-ev-kw { font-size: 0.78rem; color: #64748b; margin-top: 0.3rem; }

/* Answer card */
.dp-answer {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
    color: #1e3a5f;
    font-size: 0.95rem;
    line-height: 1.65;
}

/* Badge / chip */
.dp-badge {
    display: inline-block;
    background: #e0e7ff;
    color: #3730a3;
    border-radius: 20px;
    padding: 0.15rem 0.65rem;
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 0.3rem;
    margin-bottom: 0.25rem;
}
.dp-badge-green { background: #dcfce7; color: #166534; }
.dp-badge-amber { background: #fef3c7; color: #92400e; }
.dp-badge-red   { background: #fee2e2; color: #991b1b; }
.dp-badge-slate { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }

/* Safeguard checklist rows */
.dp-sg-item {
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
    padding: 0.4rem 0;
    border-bottom: 1px solid #f1f5f9;
    font-size: 0.9rem;
    color: #1e293b;
    line-height: 1.45;
}
.dp-sg-item:last-child { border-bottom: none; }
.dp-sg-check { color: #16a34a; font-weight: 700; flex-shrink: 0; margin-top: 0.05rem; }

/* Workflow pipeline */
.dp-workflow {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    flex-wrap: wrap;
    padding: 0.75rem 0 1rem 0;
}
.dp-wf-step {
    background: #1a2744;
    color: #f1f5f9;
    border-radius: 8px;
    padding: 0.45rem 0.9rem;
    font-size: 0.85rem;
    font-weight: 600;
    white-space: nowrap;
}
.dp-wf-arrow { color: #94a3b8; font-size: 1rem; padding: 0 0.1rem; }

/* Feature card (Home page) */
.dp-feature-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-top: 3px solid #3b6cf7;
    border-radius: 10px;
    padding: 1.1rem 1.15rem;
    height: 100%;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.dp-feature-card .dp-fc-icon { font-size: 1.4rem; margin-bottom: 0.4rem; }
.dp-feature-card h4 {
    color: #1a2744;
    font-size: 0.95rem;
    font-weight: 700;
    margin: 0 0 0.3rem 0;
}
.dp-feature-card p {
    color: #4a5568;
    font-size: 0.85rem;
    margin: 0;
    line-height: 1.5;
}

/* Boundary notice on Home */
.dp-boundary {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.85rem 1rem;
    margin-top: 0.5rem;
    font-size: 0.85rem;
    color: #4a5568;
    line-height: 1.55;
}
.dp-boundary strong { color: #1a2744; }

</style>"""


def inject_css():
    """Inject the global custom CSS. Call once at app startup after set_page_config."""
    st.markdown(_CSS, unsafe_allow_html=True)


# ── Page header ───────────────────────────────────────────────────────────────

def page_header(title: str, subtitle: str = ""):
    sub = f'<p class="dp-page-subtitle">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f'<div class="dp-page-header"><h1>{title}</h1>{sub}</div>',
        unsafe_allow_html=True,
    )


# ── Safety warning ────────────────────────────────────────────────────────────

def safety_warning():
    st.markdown(
        '<div class="dp-safety">'
        "<strong>Safe use reminder</strong> — Use synthetic or approved documents only. "
        "Do not upload or paste real learner data, safeguarding case details, "
        "confidential client records, staff HR data, personal data, or regulated information."
        "</div>",
        unsafe_allow_html=True,
    )


# ── Prototype notice ──────────────────────────────────────────────────────────

def prototype_notice(text: str = ""):
    body = text or (
        "This is a <strong>deterministic prototype</strong> — "
        "no external AI APIs, no embeddings, no vector database. "
        "All matching uses keyword search and topic mapping. "
        "Every result is transparent and auditable."
    )
    st.markdown(f'<div class="dp-notice">{body}</div>', unsafe_allow_html=True)


# ── Generic info card ─────────────────────────────────────────────────────────

def info_card(title: str, body: str):
    st.markdown(
        f'<div class="dp-card"><h4>{title}</h4><p>{body}</p></div>',
        unsafe_allow_html=True,
    )


# ── Workflow diagram (Home page pipeline) ─────────────────────────────────────

def workflow_diagram():
    steps = ["Documents", "Search", "Evidence", "Risks", "Brief", "Q&A"]
    parts = []
    for i, step in enumerate(steps):
        parts.append(f'<span class="dp-wf-step">{step}</span>')
        if i < len(steps) - 1:
            parts.append('<span class="dp-wf-arrow">→</span>')
    st.markdown(
        f'<div class="dp-workflow">{"".join(parts)}</div>',
        unsafe_allow_html=True,
    )


# ── Badge helpers ─────────────────────────────────────────────────────────────

def badge_html(label: str, style: str = "") -> str:
    """Return an HTML badge string. style: '', 'green', 'amber', 'red', 'slate'."""
    cls = f"dp-badge dp-badge-{style}" if style else "dp-badge"
    return f'<span class="{cls}">{label}</span>'


def render_badges(labels: list, style: str = ""):
    """Render a row of inline HTML badges via st.markdown."""
    if labels:
        st.markdown(
            "".join(badge_html(lbl, style) for lbl in labels),
            unsafe_allow_html=True,
        )


def kw_badges_html(keywords: list) -> str:
    """Return HTML for a row of keyword/slate badges (used inside card HTML)."""
    return "".join(badge_html(k, "slate") for k in keywords)


# ── Evidence / search result card ─────────────────────────────────────────────

def evidence_card(result: dict):
    """Render a styled evidence or keyword-search result card."""
    doc = result.get("document_name") or "—"
    line = result.get("line_number", "—")
    relevance = result.get("relevance_count", "—")
    # evidence_extractor uses 'evidence_text'; simple_search uses 'snippet'
    snippet = result.get("evidence_text") or result.get("snippet", "")
    keywords = result.get("matched_keywords") or result.get("matched_terms", [])
    kw_html = kw_badges_html(keywords)
    st.markdown(
        f'<div class="dp-evidence">'
        f'<div class="dp-ev-meta">'
        f'<span class="dp-ev-doc">{doc}</span>'
        f'<span class="dp-ev-sep">·</span>'
        f"<span>Line {line}</span>"
        f'<span class="dp-ev-sep">·</span>'
        f"<span>Relevance&nbsp;<strong>{relevance}</strong></span>"
        f"</div>"
        f'<div class="dp-ev-snippet">{snippet}</div>'
        f'<div class="dp-ev-kw">Matched: {kw_html}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


# ── Answer card ───────────────────────────────────────────────────────────────

def answer_card(text: str):
    """Render a styled blue answer / short-answer card."""
    # Convert paragraph breaks to HTML; templates use plain text, no Markdown syntax
    html_text = text.replace("\n\n", "<br><br>").replace("\n", "<br>")
    st.markdown(
        f'<div class="dp-answer">{html_text}</div>',
        unsafe_allow_html=True,
    )


# ── Safeguard checklist ───────────────────────────────────────────────────────

def safeguard_list(items: list):
    """Render a styled safeguard checklist inside a card."""
    if not items:
        return
    rows = "".join(
        f'<div class="dp-sg-item">'
        f'<span class="dp-sg-check">✓</span>'
        f"<span>{item}</span>"
        f"</div>"
        for item in items
    )
    st.markdown(
        f'<div class="dp-card" style="padding:0.75rem 1rem;">{rows}</div>',
        unsafe_allow_html=True,
    )


# ── Home page feature cards ───────────────────────────────────────────────────

def feature_cards():
    """Render the 4 feature cards on the Home page using native Streamlit columns."""
    features = [
        ("01", "Browse & Inspect", "Document library with word count, line count, and file size for each synthetic policy document."),
        ("02", "Search & Extract", "Multi-term keyword search across all documents, plus topic-based evidence extraction for 13 policy topics."),
        ("03", "Analyse & Summarise", "Deterministic risk and safeguard summary — one risk record per topic, with coverage notes and suggested owners."),
        ("04", "Brief & Q&A", "9-section downloadable Markdown brief and evidence-based Q&A with topic detection, templated answers, and limitations."),
    ]
    cols = st.columns(4, gap="small")
    for col, (icon, title, body) in zip(cols, features):
        with col:
            st.markdown(
                f'<div class="dp-feature-card">'
                f'<div class="dp-fc-icon">{icon}</div>'
                f"<h4>{title}</h4>"
                f"<p>{body}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )


def boundary_notice():
    """Render the prototype boundary notice on the Home page."""
    st.markdown(
        '<div class="dp-boundary">'
        "<strong>Prototype boundaries</strong> — "
        "No external AI APIs &nbsp;·&nbsp; "
        "No embeddings &nbsp;·&nbsp; "
        "No vector database &nbsp;·&nbsp; "
        "Synthetic policy documents only &nbsp;·&nbsp; "
        "All logic is deterministic, keyword-based, and auditable"
        "</div>",
        unsafe_allow_html=True,
    )
