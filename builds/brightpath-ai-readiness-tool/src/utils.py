"""
Shared utilities for the BrightPath AI Readiness + Workflow Audit Tool.
"""

import streamlit as st

# ── Legacy Phase 1 helpers ────────────────────────────────────────────────────

RISK_COLOURS = {
    "Low": "Low",
    "Medium": "Medium",
    "High": "High",
    "Critical": "Critical",
}

SUITABILITY_LABELS = {
    True: "Suitable",
    False: "Not suitable",
    None: "Borderline",
}


def init_session_state():
    defaults = {
        "profile": {},
        "readiness_responses": {},
        "workflows": [],
        "band": {},
        "workflow_summary": {},
        "pilot_candidates": [],
        # Standardised computed-score keys written by each assessment page
        "readiness_score": None,
        "readiness_category": None,
        "workflow_score": None,
        "workflow_category": None,
        "workflow_name": None,
        "workflow_owner": None,
        "proposed_ai_support": None,
        "highest_risk_level": None,
        "critical_risk_count": None,
        "high_risk_count": None,
        "key_risk_notes": None,
        "ai_use_summary": None,
        "main_concerns": None,
        "pilot_recommendation": None,
        "pilot_explanation": None,
        "recommended_safeguards": None,
        "next_actions": None,
        "consultant_notes": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def responsible_use_notice():
    """Legacy alias — kept for compatibility."""
    render_responsible_use()


def score_bar(score: int, max_score: int = 5, label: str = "") -> None:
    pct = int((score / max_score) * 100)
    colour = (
        "#2ecc71" if pct >= 70
        else "#f39c12" if pct >= 40
        else "#e74c3c"
    )
    st.markdown(
        f"""
        <div style="margin-bottom:4px;font-size:0.85em">{label}</div>
        <div style="background:#eee;border-radius:4px;height:14px;width:100%">
          <div style="background:{colour};width:{pct}%;height:14px;
                      border-radius:4px;transition:width 0.3s"></div>
        </div>
        <div style="font-size:0.8em;color:#555;margin-bottom:8px">{score} / {max_score}</div>
        """,
        unsafe_allow_html=True,
    )


# ── CSS ───────────────────────────────────────────────────────────────────────

_CSS = """
<style>
/* ── Layout ── */
.main .block-container { padding-top: 1.5rem; padding-bottom: 3rem; }

/* ── Sidebar (dark navy) ── */
section[data-testid="stSidebar"] { background: #1a2744 !important; }
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div { color: #cbd5e1 !important; }
section[data-testid="stSidebar"] strong,
section[data-testid="stSidebar"] b { color: #f1f5f9 !important; }
section[data-testid="stSidebar"] hr { border-color: #334155 !important; }
section[data-testid="stSidebar"] .stRadio label { color: #e2e8f0 !important; font-size: 0.88rem !important; }
section[data-testid="stSidebar"] [data-testid="stCaption"] { color: #94a3b8 !important; font-size: 0.75rem !important; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.75rem 1rem !important;
}

/* ── Page header ── */
.bp-header {
    padding: 0.15rem 0 0.85rem;
    border-bottom: 3px solid #1e3a5f;
    margin-bottom: 1.25rem;
}
.bp-header h2 {
    margin: 0 0 0.15rem;
    color: #1e3a5f;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.015em;
}
.bp-header .bp-subtitle { color: #4a5568; font-size: 0.92rem; margin: 0; line-height: 1.5; }

/* ── Feature grid (Home) ── */
.bp-feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin: 1rem 0 0.5rem;
}
.bp-feature-card {
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.bp-feature-card .card-icon { font-size: 1.5rem; line-height: 1; margin-bottom: 0.45rem; }
.bp-feature-card .card-title { font-size: 0.87rem; font-weight: 600; color: #1e3a5f; margin: 0 0 0.3rem; }
.bp-feature-card .card-desc { font-size: 0.8rem; color: #718096; line-height: 1.4; margin: 0; }

/* ── Demo step guide ── */
.bp-step-row {
    display: flex;
    align-items: flex-start;
    gap: 0.65rem;
    padding: 0.5rem 0.85rem;
    background: #f7fafc;
    border-left: 3px solid #3182ce;
    border-radius: 0 8px 8px 0;
    margin-bottom: 0.4rem;
    font-size: 0.875rem;
}
.bp-step-num {
    background: #2b6cb0;
    color: white;
    min-width: 1.35rem;
    height: 1.35rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
    flex-shrink: 0;
    margin-top: 0.1rem;
}
.bp-step-text { color: #2d3748; line-height: 1.45; }
.bp-step-text strong { color: #1e3a5f; }

/* ── Risk badges ── */
.risk-badge {
    display: inline-block;
    padding: 0.14rem 0.6rem;
    border-radius: 9999px;
    font-size: 0.77rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.risk-low      { background: #c6f6d5; color: #22543d; }
.risk-moderate { background: #fefcbf; color: #744210; }
.risk-high     { background: #fed7d7; color: #742a2a; }
.risk-critical { background: #feb2b2; color: #63171b; outline: 1px solid #fc8181; }

/* ── Risk summary table ── */
.bp-risk-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    margin: 0.75rem 0;
}
.bp-risk-table th {
    background: #2d5282;
    color: white;
    padding: 0.55rem 0.85rem;
    text-align: left;
    font-weight: 600;
    font-size: 0.8rem;
    letter-spacing: 0.025em;
}
.bp-risk-table th.center, .bp-risk-table td.center { text-align: center; }
.bp-risk-table td {
    padding: 0.5rem 0.85rem;
    border-bottom: 1px solid #edf2f7;
    color: #2d3748;
}
.bp-risk-table tr:last-child td { border-bottom: none; }
.bp-risk-table tr:nth-child(even) td { background: #f7fafc; }

/* ── Score hero ── */
.score-hero {
    text-align: center;
    padding: 1.2rem 1rem;
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
}
.score-hero .sh-num { font-size: 2.4rem; font-weight: 700; color: #2563eb; line-height: 1; }
.score-hero .sh-max { font-size: 1.1rem; color: #718096; }
.score-hero .sh-label { font-size: 0.82rem; color: #718096; margin-top: 0.3rem; }

/* ── Safety notice ── */
.bp-safety {
    background: #fffbeb;
    border-left: 4px solid #f6ad55;
    padding: 0.65rem 1rem;
    border-radius: 0 8px 8px 0;
    font-size: 0.875rem;
    color: #744210;
    margin: 0.5rem 0 1rem;
    line-height: 1.5;
}

/* ── Responsible use footer ── */
.bp-ru-notice {
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.8rem 1.1rem;
    margin-top: 2.5rem;
    font-size: 0.82rem;
    color: #718096;
    line-height: 1.55;
}

/* ── Profile card ── */
.bp-profile-card {
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1rem 1.35rem;
    margin-top: 0.5rem;
}
.bp-profile-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0;
    border-bottom: 1px solid #edf2f7;
    font-size: 0.9rem;
    gap: 1rem;
}
.bp-profile-item:last-child { border-bottom: none; }
.bp-profile-label { color: #718096; font-weight: 500; min-width: 9rem; flex-shrink: 0; }
.bp-profile-value { color: #1a202c; text-align: right; }
.flag-yes { background: #c6f6d5; color: #22543d; border-radius: 4px; padding: 0.1rem 0.5rem; font-size: 0.82rem; font-weight: 600; }
.flag-no  { background: #fed7d7; color: #742a2a; border-radius: 4px; padding: 0.1rem 0.5rem; font-size: 0.82rem; font-weight: 600; }

/* ── Scale legend ── */
.scale-legend {
    display: inline-flex;
    gap: 1.25rem;
    background: #edf2f7;
    border-radius: 6px;
    padding: 0.4rem 0.9rem;
    font-size: 0.81rem;
    color: #4a5568;
    margin-bottom: 0.75rem;
    flex-wrap: wrap;
}

/* ── Section heading ── */
.bp-section {
    font-size: 0.98rem;
    font-weight: 600;
    color: #1e3a5f;
    padding: 0.4rem 0 0.3rem;
    border-bottom: 1px solid #e2e8f0;
    margin: 1rem 0 0.75rem;
}

/* ── Recommendation banner ── */
.rec-banner { border-radius: 10px; padding: 1.2rem 1.4rem; margin: 0.5rem 0 1rem; }
.rec-banner h3 { margin: 0 0 0.45rem; font-size: 1.05rem; }
.rec-banner p  { margin: 0; font-size: 0.9rem; line-height: 1.55; }
.rec-error   { background: #fff5f5; border: 2px solid #fc8181; color: #742a2a; }
.rec-warning { background: #fffff0; border: 2px solid #ecc94b; color: #744210; }
.rec-info    { background: #ebf8ff; border: 2px solid #63b3ed; color: #2c5282; }
.rec-success { background: #f0fff4; border: 2px solid #68d391; color: #22543d; }

/* ── Next actions / safeguards lists ── */
.actions-box, .safeguards-box {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
}
.action-item {
    display: flex;
    gap: 0.6rem;
    align-items: flex-start;
    padding: 0.4rem 0;
    font-size: 0.875rem;
    color: #2d3748;
    line-height: 1.45;
    border-bottom: 1px solid #edf2f7;
}
.action-item:last-child { border-bottom: none; }
.action-num {
    background: #2b6cb0;
    color: white;
    min-width: 1.3rem;
    height: 1.3rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: 700;
    flex-shrink: 0;
    margin-top: 0.1rem;
}
.safeguard-item {
    padding: 0.38rem 0;
    font-size: 0.875rem;
    color: #2d3748;
    border-bottom: 1px solid #edf2f7;
    line-height: 1.45;
}
.safeguard-item:last-child { border-bottom: none; }
</style>
"""


# ── UI helpers ────────────────────────────────────────────────────────────────

def inject_custom_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = None) -> None:
    sub = f'<p class="bp-subtitle">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f'<div class="bp-header"><h2>{title}</h2>{sub}</div>',
        unsafe_allow_html=True,
    )


def render_safety_notice(text: str) -> None:
    st.markdown(f'<div class="bp-safety">{text}</div>', unsafe_allow_html=True)


def render_responsible_use() -> None:
    st.markdown(
        '<div class="bp-ru-notice">'
        "<strong>Responsible use reminder:</strong> "
        "This tool provides indicative assessment guidance only. It is not legal, "
        "compliance, safeguarding, HR, or financial advice. All sample data is synthetic. "
        "No real personal or confidential data should be entered. "
        "Human review is required before any AI use in live workflows."
        "</div>",
        unsafe_allow_html=True,
    )


def get_risk_badge(level: str) -> str:
    cls = {
        "Low": "risk-low",
        "Moderate": "risk-moderate",
        "High": "risk-high",
        "Critical": "risk-critical",
    }.get(level, "risk-moderate")
    return f'<span class="risk-badge {cls}">{level}</span>'


def render_risk_table(risk_rows: list) -> None:
    rows = "".join(
        f"<tr>"
        f"<td>{r['label']}</td>"
        f"<td class='center'>{r['likelihood']}</td>"
        f"<td class='center'>{r['impact']}</td>"
        f"<td class='center'>{r['score']}</td>"
        f"<td>{get_risk_badge(r['level'])}</td>"
        f"</tr>"
        for r in risk_rows
    )
    st.markdown(
        f"""
        <table class="bp-risk-table">
          <thead><tr>
            <th>Risk Category</th>
            <th class="center">Likelihood</th>
            <th class="center">Impact</th>
            <th class="center">Score</th>
            <th>Risk Level</th>
          </tr></thead>
          <tbody>{rows}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


def render_score_hero(score: int, max_score: int, label: str) -> None:
    st.markdown(
        f'<div class="score-hero">'
        f'<div class="sh-num">{score}<span class="sh-max"> / {max_score}</span></div>'
        f'<div class="sh-label">{label}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def render_recommendation_card(recommendation: str, explanation: str, alert_type: str) -> None:
    cls = {
        "error": "rec-error",
        "warning": "rec-warning",
        "info": "rec-info",
        "success": "rec-success",
    }.get(alert_type, "rec-info")
    st.markdown(
        f'<div class="rec-banner {cls}">'
        f"<h3>Recommendation: {recommendation}</h3>"
        f"<p>{explanation}</p>"
        f"</div>",
        unsafe_allow_html=True,
    )


def render_next_actions(actions: list) -> None:
    items = "".join(
        f'<div class="action-item">'
        f'<div class="action-num">{i}</div>'
        f"<div>{a}</div>"
        f"</div>"
        for i, a in enumerate(actions, 1)
    )
    st.markdown(f'<div class="actions-box">{items}</div>', unsafe_allow_html=True)


def render_safeguards(safeguards: list) -> None:
    items = "".join(
        f'<div class="safeguard-item">✓ {s}</div>'
        for s in safeguards
    )
    st.markdown(f'<div class="safeguards-box">{items}</div>', unsafe_allow_html=True)


def render_section_heading(text: str) -> None:
    st.markdown(f'<div class="bp-section">{text}</div>', unsafe_allow_html=True)
