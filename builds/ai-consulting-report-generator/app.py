"""AI Consulting Report Generator — Build 5
BrightPath ChatGPT Mastery Project

Phases 1–9 complete: audit data, readiness summary, risk register,
opportunity portfolio, roadmap, report sections, client report,
export centre (PDF/PPTX/charts), and completion review.
"""

import streamlit as st

st.set_page_config(
    page_title="AI Consulting Report Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.ui_components import (
    apply_global_styles,
    render_completion_badge,
    render_info_card,
    render_metric_row,
    render_page_header,
    render_prototype_notice,
    render_responsible_use_warning,
    render_status_box,
)
from src.sample_data import get_brightpath_audit_data
from src import audit_data_manager as adm
from src import scoring_summary as ss
from src import risk_register as rr
from src import opportunity_generator as og
from src import roadmap_generator as rg
from src import report_sections as rsec
from src import report_builder as rb
from src import export_centre as ec
from src import report_analytics as ra
from src import chart_utils as cu
from src import completion_review as cr
from src.utils import create_safe_filename

apply_global_styles()

# ── Sidebar ────────────────────────────────────────────────────────────────────
PAGES = [
    "Home",
    "Audit Data",
    "Readiness Summary",
    "Risk Register",
    "Opportunity and Pilot Recommendations",
    "Roadmap",
    "Report Sections",
    "Client Report",
    "Export Centre",
    "Completion Review",
]

with st.sidebar:
    st.markdown("### AI Consulting Report Generator")
    st.markdown("**Build 5** · ChatGPT Mastery Project")
    st.markdown("---")
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")
    st.markdown("---")
    render_completion_badge("Audit Data", "audit_data" in st.session_state)
    render_completion_badge("Readiness Summary", "readiness_summary" in st.session_state)
    render_completion_badge("Risk Register", "risk_register" in st.session_state)
    render_completion_badge("Opportunities", "opportunity_portfolio" in st.session_state)
    render_completion_badge("Roadmap", "implementation_roadmap" in st.session_state)
    render_completion_badge("Report Sections", "report_sections" in st.session_state)
    render_completion_badge("Client Report", "client_report_markdown" in st.session_state)
    render_completion_badge("Export Centre", "export_data" in st.session_state)
    render_completion_badge("Completion Review", "completion_review" in st.session_state)
    st.markdown("---")
    st.markdown(
        '<p style="font-size:0.75rem; color:#94a3b8;">Synthetic scenarios only. '
        "Human review required.</p>",
        unsafe_allow_html=True,
    )


# ── Home ───────────────────────────────────────────────────────────────────────
if page == "Home":
    render_page_header(
        "AI Consulting Report Generator",
        "Turn an AI readiness audit into a polished client-facing consulting report.",
    )
    render_responsible_use_warning()
    render_prototype_notice()

    st.markdown("### What This Tool Does")
    st.markdown(
        "This prototype takes the findings from an AI readiness and workflow audit "
        "and converts them into a structured, professional client report covering "
        "readiness scores, risks, governance gaps, AI opportunities, pilots, training "
        "needs, and a 30/60/90-day roadmap."
    )

    st.markdown("### Consulting Workflow")
    step_cols = st.columns(8)
    steps = [
        ("1", "Audit Data"),
        ("2", "Readiness"),
        ("3", "Risks"),
        ("4", "Opportunities"),
        ("5", "Roadmap"),
        ("6", "Report"),
        ("7", "Export"),
        ("8", "Review"),
    ]
    for col, (num, label) in zip(step_cols, steps):
        with col:
            st.markdown(
                f'<div style="text-align:center;background:#1a2744;color:#f1f5f9;'
                f"border-radius:8px;padding:0.5rem 0.25rem;font-size:0.82rem;font-weight:700;\">"
                f"{num}<br>"
                f'<span style="font-weight:400;font-size:0.75rem;">{label}</span>'
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("### Connection to Builds 1–4")
    left, right = st.columns(2)
    with left:
        render_info_card(
            "Build 1 — AI Readiness and Workflow Audit",
            "Diagnosed AI readiness across six dimensions. Identified workflow opportunities, "
            "risks, and training needs. Build 5 turns those audit outputs into a client report.",
        )
        render_info_card(
            "Build 2 — Document Intelligence / Policy Analysis",
            "Extracted evidence from policy documents. Build 5 can optionally reference policy "
            "evidence in the governance gap analysis.",
        )
    with right:
        render_info_card(
            "Build 3 — Semantic RAG Policy Assistant",
            "Performed semantic retrieval over policy documents. Build 5 can optionally cite "
            "policy evidence to ground its recommendations.",
        )
        render_info_card(
            "Build 4 — AI Staff Training and Workshop Generator",
            "Generated training materials from the audit scenario. Build 5 references training "
            "needs and can link to the training pack as a recommended deliverable.",
        )

    st.markdown("---")
    st.info(
        "Build 5 is complete as a portfolio-ready local prototype. It uses synthetic "
        "BrightPath audit data only, generates the full consulting workflow, exports "
        "Markdown/PDF/PPTX deliverables, and closes with a completion review for final demo prep."
    )


# ── Audit Data ─────────────────────────────────────────────────────────────────
elif page == "Audit Data":
    render_page_header(
        "Audit Data",
        "Load and review the AI readiness audit findings.",
    )
    render_responsible_use_warning()

    if st.button("Load BrightPath Demo Audit Data", type="primary"):
        audit_data = get_brightpath_audit_data()
        is_valid, msg = adm.validate_audit_data(audit_data)
        if is_valid:
            summary = adm.summarise_audit_data(audit_data)
            _org = audit_data.get("organisation_profile", {}).get("organisation_name", "")
            readiness_summary = ss.generate_readiness_summary(
                audit_data["readiness_scores"], org_name=_org
            )
            st.session_state["audit_data"] = audit_data
            st.session_state["audit_summary"] = summary
            st.session_state["readiness_summary"] = readiness_summary
            st.success("BrightPath demo audit data loaded.")
        else:
            st.error(f"Validation failed: {msg}")

    if "audit_data" not in st.session_state:
        render_status_box(
            "No audit data loaded. Click the button above to load the BrightPath demo.", "info"
        )
        st.stop()

    audit_data = st.session_state["audit_data"]
    summary = st.session_state["audit_summary"]
    profile = audit_data["organisation_profile"]
    scores = audit_data["readiness_scores"]

    st.markdown(f"### {profile['organisation_name']}")
    st.markdown(
        f"*{profile.get('organisation_type', '')} · "
        f"{profile.get('sector', '')} · "
        f"{profile.get('country_context', '')}*"
    )

    render_metric_row([
        {"label": "Staff", "value": str(summary["staff_count"])},
        {"label": "Workflows", "value": str(summary["workflow_count"])},
        {"label": "Risks", "value": str(summary["risk_count"])},
        {"label": "Critical Risks", "value": str(summary["critical_risk_count"])},
        {"label": "Pilots", "value": str(summary["pilot_count"])},
        {"label": "Training Needs", "value": str(summary["training_count"])},
        {"label": "Gov. Gaps", "value": str(summary["governance_gap_count"])},
    ])

    st.markdown("---")
    st.markdown("### Readiness Scores")

    score_labels = {
        "strategy_score": "Strategy",
        "data_governance_score": "Data Governance",
        "staff_capability_score": "Staff Capability",
        "workflow_opportunity_score": "Workflow Opportunity",
        "risk_management_score": "Risk Management",
        "leadership_alignment_score": "Leadership Alignment",
    }
    score_cols = st.columns(3)
    for i, (key, label) in enumerate(score_labels.items()):
        with score_cols[i % 3]:
            st.metric(label=label, value=f"{scores[key]}/100")

    overall = scores.get("overall_readiness_score", 0)
    st.metric(
        label="Overall Readiness Score",
        value=f"{overall}/100",
        delta=ss.classify_readiness_level(overall),
    )

    st.markdown("---")
    st.markdown("### Workflow Findings")
    for wf in audit_data.get("workflow_findings", []):
        with st.expander(f"{wf['workflow_name']} — Risk: {wf['risk_level']}"):
            st.markdown(f"**Current process:** {wf['current_process']}")
            st.markdown("**Pain points:**")
            for p in wf.get("pain_points", []):
                st.markdown(f"- {p}")
            st.markdown(f"**AI opportunity:** {wf['ai_opportunity']}")
            st.markdown(f"**Potential value:** {wf['potential_value']}")
            st.markdown(f"**Recommended action:** {wf['recommended_action']}")

    st.markdown("---")
    st.markdown("### Risk Findings")
    for rf in audit_data.get("risk_findings", []):
        with st.expander(f"{rf['risk_title']} — Level: {rf['risk_level']}"):
            st.markdown(f"**Category:** {rf['risk_category']}")
            st.markdown(f"**Likelihood:** {rf['likelihood']} · **Impact:** {rf['impact']}")
            st.markdown(f"**Description:** {rf['description']}")
            st.markdown(f"**Recommended control:** {rf['recommended_control']}")
            st.markdown(f"**Owner:** {rf['owner']}")

    st.markdown("---")
    st.markdown("### Pilot Recommendations")
    for p in audit_data.get("pilot_recommendations", []):
        with st.expander(f"{p['pilot_name']} — Timeline: {p['suggested_timeline']}"):
            st.markdown(f"**Business problem:** {p['business_problem']}")
            st.markdown(f"**Proposed solution:** {p['proposed_solution']}")
            st.markdown("**Expected benefits:**")
            for b in p.get("expected_benefits", []):
                st.markdown(f"- {b}")
            st.markdown(f"**Complexity:** {p['complexity']} · **Risk:** {p['risk_level']}")
            st.markdown("**Success measures:**")
            for m in p.get("success_measures", []):
                st.markdown(f"- {m}")

    st.markdown("---")
    st.markdown("### Training Needs")
    for t in audit_data.get("training_needs", []):
        with st.expander(f"{t['topic']} — Priority: {t['priority']}"):
            st.markdown(f"**Audience:** {t['audience']}")
            st.markdown(f"**Reason:** {t['reason']}")
            st.markdown(f"**Recommended format:** {t['recommended_format']}")

    st.markdown("---")
    st.markdown("### Governance Gaps")
    for g in audit_data.get("governance_gaps", []):
        with st.expander(f"{g['gap_title']} — Priority: {g['priority']}"):
            st.markdown(f"**Current state:** {g['current_state']}")
            st.markdown(f"**Why it matters:** {g['why_it_matters']}")
            st.markdown(f"**Recommended action:** {g['recommended_action']}")

    st.markdown("---")
    with st.expander("View Audit Data as Markdown"):
        st.markdown(adm.format_audit_data_as_markdown(audit_data))


# ── Readiness Summary ──────────────────────────────────────────────────────────
elif page == "Readiness Summary":
    render_page_header(
        "Readiness Summary",
        "AI readiness score interpretation, strengths, gaps, and strategic recommendations.",
    )
    render_responsible_use_warning()

    if "audit_data" not in st.session_state:
        render_status_box(
            "Audit data not loaded. "
            "Steps: 1. Go to Audit Data  →  2. Load BrightPath demo audit data  →  3. Return here.",
            "info",
        )
        st.stop()

    _audit = st.session_state["audit_data"]
    _scores = _audit.get("readiness_scores", {})
    _org_name = _audit.get("organisation_profile", {}).get("organisation_name", "")

    _summary = ss.generate_readiness_summary(_scores, org_name=_org_name)
    _summary_md = ss.format_readiness_summary_as_markdown(_summary)
    st.session_state["readiness_summary"] = _summary
    st.session_state["readiness_summary_markdown"] = _summary_md

    _overall = _summary["overall_score"]
    _level = _summary["overall_level"]
    _ranked = _summary["ranked_categories"]
    _strongest_label = _ranked[0]["label"] if _ranked else "—"
    _weakest_label = _ranked[-1]["label"] if _ranked else "—"
    _gap_count = len(_summary["gaps"])

    render_metric_row([
        {"label": "Overall Score", "value": f"{int(_overall)}/100"},
        {"label": "Readiness Level", "value": _level},
        {"label": "Strongest Area", "value": _strongest_label},
        {"label": "Weakest Area", "value": _weakest_label},
        {"label": "Priority Gaps", "value": str(_gap_count)},
    ])

    # ── Overall readiness band ─────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Overall Readiness")
    _colour = ss.get_readiness_band_colour(_level)
    st.markdown(
        f'<div style="border-left:5px solid {_colour};padding:0.75rem 1rem;'
        f"background:#f8fafc;border-radius:0 8px 8px 0;margin-bottom:1.25rem;\">"
        f'<strong style="color:#1a2744;">{_level}</strong><br/>'
        f'<span style="color:#334155;font-size:0.9rem;">{_summary["overall_description"]}</span>'
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── Category scores with progress bars ────────────────────────────────────
    st.markdown("---")
    st.markdown("### Category Scores")
    for _cat in _summary["category_scores"]:
        _score_int = int(_cat["score"])
        _left, _right = st.columns([8, 2])
        with _left:
            st.markdown(f"**{_cat['label']}** — *{_cat['level']}*")
            st.progress(_score_int)
        with _right:
            st.metric(label="Score", value=f"{_score_int}/100")
        with st.expander(f"Interpretation — {_cat['label']}"):
            st.markdown(_cat["interpretation"])
        st.markdown("")

    # ── Ranked categories ─────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Category Rankings")
    _rank_cols = st.columns(2)
    for _i, _rc in enumerate(_ranked):
        with _rank_cols[_i % 2]:
            st.markdown(
                f"**{_i + 1}. {_rc['label']}** — {int(_rc['score'])}/100 · *{_rc['level']}*"
            )

    # ── Strengths ─────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Strengths")
    _strengths = _summary["strengths"]
    if _strengths:
        for _s in _strengths:
            render_info_card(
                f"{_s['category']} — {int(_s['score'])}/100",
                _s["reason"],
            )
    else:
        _top = _ranked[0] if _ranked else {}
        render_status_box(
            f"No areas score above 70/100 at this stage. "
            f"The strongest category is {_top.get('label', '—')} at {int(_top.get('score', 0))}/100.",
            "info",
        )

    # ── Priority gaps ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Priority Gaps")
    _gaps = _summary["gaps"]
    if _gaps:
        for _g in _gaps:
            with st.expander(f"{_g['category']} — {int(_g['score'])}/100"):
                st.markdown(f"**Risk:** {_g['risk']}")
                st.markdown(f"**Recommended action:** {_g['recommended_action']}")
    else:
        render_status_box("No significant gaps identified at this stage.", "success")

    # ── Strategic interpretation ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Strategic Interpretation")
    st.markdown(_summary["strategic_interpretation"])

    # ── Recommendations ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Recommendations")
    for _i, _rec in enumerate(_summary["recommendations"], 1):
        st.markdown(f"**{_i}.** {_rec}")

    # ── Responsible-use ───────────────────────────────────────────────────────
    st.markdown("---")
    render_status_box(_summary["responsible_use_note"], "warning")
    render_status_box(_summary["prototype_note"], "info")

    # ── Download ──────────────────────────────────────────────────────────────
    st.markdown("---")
    _fname = create_safe_filename(f"readiness-summary-{_org_name or 'audit'}", "md")
    st.download_button(
        label="Download Readiness Summary (Markdown)",
        data=_summary_md,
        file_name=_fname,
        mime="text/markdown",
        use_container_width=True,
    )


# ── Report Sections ────────────────────────────────────────────────────────────
elif page == "Report Sections":
    render_page_header(
        "Report Sections",
        "Generate structured sections of the client-facing AI consulting report.",
    )
    render_responsible_use_warning()

    if "audit_data" not in st.session_state:
        render_status_box(
            "Audit data not loaded. "
            "Steps: 1. Go to Audit Data  →  2. Load BrightPath demo audit data  →  3. Return here.",
            "info",
        )
        st.stop()

    _has_readiness = "readiness_summary" in st.session_state
    _has_risk = "risk_register" in st.session_state
    _has_opps = "opportunity_portfolio" in st.session_state
    _has_roadmap = "implementation_roadmap" in st.session_state

    if not (_has_readiness and _has_risk and _has_opps and _has_roadmap):
        render_status_box(
            "Tip: Run Readiness Summary, Risk Register, Opportunity Recommendations, and Roadmap "
            "first for richer report sections. Basic sections can still be generated from audit "
            "data alone.",
            "info",
        )

    _audit = st.session_state["audit_data"]
    _org_name = _audit.get("organisation_profile", {}).get("organisation_name", "")
    _readiness = st.session_state.get("readiness_summary")
    _risk_reg = st.session_state.get("risk_register")
    _risk_sum = st.session_state.get("risk_register_summary")
    _opp_port = st.session_state.get("opportunity_portfolio")
    _opp_sum = st.session_state.get("opportunity_summary")
    _roadmap_data = st.session_state.get("implementation_roadmap")
    _rm_sum = st.session_state.get("implementation_roadmap_summary")

    _report_sections = rsec.generate_all_report_sections(
        _audit, _readiness, _risk_reg, _risk_sum,
        _opp_port, _opp_sum, _roadmap_data, _rm_sum,
    )
    _rs_summary = rsec.summarise_report_sections(_report_sections)
    _rs_md = rsec.format_report_sections_as_markdown(_report_sections)

    st.session_state["report_sections"] = _report_sections
    st.session_state["report_sections_summary"] = _rs_summary
    st.session_state["report_sections_markdown"] = _rs_md

    # ── Summary metric cards ───────────────────────────────────────────────────
    _used_count = len(_rs_summary["source_outputs_used"])
    _missing_count = len(_rs_summary["missing_source_outputs"])
    render_metric_row([
        {"label": "Organisation", "value": _org_name or "—"},
        {"label": "Total Sections", "value": str(_rs_summary["total_sections"])},
        {"label": "Source Outputs Used", "value": str(_used_count)},
        {"label": "Missing Source Outputs", "value": str(_missing_count)},
        {"label": "Review Required", "value": "Yes"},
    ])

    # ── Source output availability checklist ──────────────────────────────────
    st.markdown("---")
    st.markdown("### Source Output Availability")
    _source_available = _report_sections.get("source_outputs_available", {})
    _check_cols = st.columns(len(_source_available))
    for _col, (key, available) in zip(_check_cols, _source_available.items()):
        with _col:
            _icon = "Yes" if available else "-"
            _label = key.replace("_", " ").title()
            st.markdown(
                f'<div style="text-align:center;padding:0.5rem;background:#f8fafc;'
                f'border-radius:8px;font-size:0.82rem;">'
                f'<div style="font-size:1.2rem;">{_icon}</div>'
                f'<strong>{_label}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Overall report readiness ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Overall Report Readiness")
    st.markdown(_rs_summary["overall_report_readiness"])

    # ── Report sections ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Report Sections")

    _section_order = _report_sections.get("section_order", [])
    _sections = _report_sections.get("sections", {})

    for _sid in _section_order:
        _sec = _sections.get(_sid)
        if not _sec:
            continue
        with st.expander(_sec["section_title"]):
            _purpose = _sec.get("section_purpose", "")
            if _purpose:
                st.markdown(f"*{_purpose}*")
            st.markdown("")

            _content = _sec.get("content", "")
            if _content:
                st.markdown(_content)

            _kps = _sec.get("key_points", [])
            if _kps:
                st.markdown("**Key Points:**")
                for _kp in _kps:
                    st.markdown(f"- {_kp}")

            _recs = _sec.get("recommendations", [])
            if _recs:
                st.markdown("**Recommendations:**")
                for _rec in _recs:
                    st.markdown(f"- {_rec}")

            _rnote = _sec.get("review_note", "")
            if _rnote:
                render_status_box(_rnote, "info")

    # ── Responsible-use ───────────────────────────────────────────────────────
    st.markdown("---")
    render_status_box(
        "This report is generated from synthetic/demo audit data only. "
        "It must not be used with real client records, learner data, safeguarding case details, "
        "staff HR data, personal data, confidential data, or regulated information without "
        "appropriate governance, approvals, and responsible owners. "
        "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
        "financial, academic-integrity, or professional advice. "
        "Human review remains required before any real-world use.",
        "warning",
    )

    # ── Download ──────────────────────────────────────────────────────────────
    st.markdown("---")
    _rs_fname = create_safe_filename(f"report-sections-{_org_name or 'audit'}", "md")
    st.download_button(
        label="Download Report Sections (Markdown)",
        data=_rs_md,
        file_name=_rs_fname,
        mime="text/markdown",
        use_container_width=True,
    )

elif page == "Risk Register":
    render_page_header(
        "Risk Register",
        "Client-facing AI risk register with likelihood, impact, controls, and owners.",
    )
    render_responsible_use_warning()

    if "audit_data" not in st.session_state:
        render_status_box(
            "Audit data not loaded. "
            "Steps: 1. Go to Audit Data  →  2. Load BrightPath demo audit data  →  3. Return here.",
            "info",
        )
        st.stop()

    _audit = st.session_state["audit_data"]
    _org_name = _audit.get("organisation_profile", {}).get("organisation_name", "")

    _risk_register = rr.generate_risk_register(_audit)
    _rr_summary = rr.summarise_risk_register(_risk_register)
    _prioritised = rr.prioritise_risks(_risk_register)
    _register_md = rr.format_risk_register_as_markdown(_prioritised, _rr_summary)

    st.session_state["risk_register"] = _risk_register
    st.session_state["risk_register_summary"] = _rr_summary
    st.session_state["risk_register_markdown"] = _register_md

    if not _risk_register:
        render_status_box("No risk findings found in the loaded audit data.", "info")
        st.stop()

    # ── Summary metric cards ───────────────────────────────────────────────────
    render_metric_row([
        {"label": "Total Risks", "value": str(_rr_summary["total_risks"])},
        {"label": "Critical", "value": str(_rr_summary["critical_risks"])},
        {"label": "High", "value": str(_rr_summary["high_risks"])},
        {"label": "Medium", "value": str(_rr_summary["medium_risks"])},
        {"label": "Low", "value": str(_rr_summary["low_risks"])},
    ])

    if _rr_summary["critical_risks"] > 0:
        render_status_box(
            f"{_rr_summary['critical_risks']} critical risk(s) require immediate management "
            "review before wider AI use continues.",
            "warning",
        )
    elif _rr_summary["high_risks"] > 0:
        render_status_box(
            f"{_rr_summary['high_risks']} high-priority risk(s) should be addressed before "
            "scaling AI adoption or running wider pilots.",
            "warning",
        )

    # ── Highest risk ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Highest Risk")
    _hr = _rr_summary.get("highest_risk", {})
    if _hr:
        _hr_colour = rr.get_risk_level_colour(_hr.get("risk_level", ""))
        st.markdown(
            f'<div style="border-left:5px solid {_hr_colour};padding:0.75rem 1rem;'
            f"background:#f8fafc;border-radius:0 8px 8px 0;margin-bottom:1.25rem;\">"
            f'<strong style="color:#1a2744;">{_hr.get("risk_id", "")} — {_hr.get("risk_title", "")}</strong><br/>'
            f'<span style="color:#334155;font-size:0.9rem;">'
            f'Level: <strong>{_hr.get("risk_level", "")}</strong> · Score: {_hr.get("risk_score", "")}/25 · '
            f'Likelihood: {_hr.get("likelihood", "")} · Impact: {_hr.get("impact", "")}'
            f"</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ── Overall risk position ─────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Overall Risk Position")
    st.markdown(_rr_summary["overall_risk_position"])

    # ── Recommended focus areas ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Recommended Focus Areas")
    for _focus in _rr_summary["recommended_focus"]:
        st.markdown(f"- {_focus}")

    # ── Risk register table ───────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Risk Register")

    for _risk in _prioritised:
        _colour = rr.get_risk_level_colour(_risk["risk_level"])
        with st.expander(
            f"{_risk['risk_id']} — {_risk['risk_title']}  |  "
            f"{_risk['risk_level']}  |  Score: {_risk['risk_score']}/25"
        ):
            _col_desc, _col_badge = st.columns([3, 1])
            with _col_desc:
                st.markdown(f"**Category:** {_risk['risk_category']}")
                st.markdown(f"**Description:** {_risk['description']}")
            with _col_badge:
                st.markdown(
                    f'<div style="background:{_colour};color:#ffffff;border-radius:6px;'
                    f"padding:0.4rem 0.75rem;text-align:center;font-weight:700;"
                    f'font-size:0.9rem;margin-bottom:0.5rem;">'
                    f"{_risk['risk_level']}"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                st.metric("Score", f"{_risk['risk_score']}/25")

            st.markdown("---")
            _c1, _c2, _c3 = st.columns(3)
            with _c1:
                st.markdown(f"**Likelihood:** {_risk['likelihood']} ({_risk['likelihood_score']}/5)")
                st.markdown(f"**Impact:** {_risk['impact']} ({_risk['impact_score']}/5)")
            with _c2:
                st.markdown(f"**Owner:** {_risk['owner']}")
                st.markdown(f"**Status:** {_risk['status']}")
            with _c3:
                st.markdown(f"**Priority action:** {_risk['priority_action']}")
                st.markdown(f"**Review:** {_risk['review_frequency']}")

            st.markdown("---")
            st.markdown("**Recommended control:**")
            st.markdown(_risk["recommended_control"])

    # ── Responsible-use ───────────────────────────────────────────────────────
    st.markdown("---")
    render_status_box(
        "This risk register is generated from synthetic/demo audit data only. "
        "It must not be used with real client records, learner data, safeguarding case details, "
        "staff HR data, personal data, confidential data, or regulated information without "
        "appropriate governance, approvals, and responsible owners. "
        "This prototype does not provide legal, safeguarding, HR, compliance, or professional advice. "
        "Human review remains required before any real-world use.",
        "warning",
    )

    # ── Download ──────────────────────────────────────────────────────────────
    st.markdown("---")
    _rr_fname = create_safe_filename(f"risk-register-{_org_name or 'audit'}", "md")
    st.download_button(
        label="Download Risk Register (Markdown)",
        data=_register_md,
        file_name=_rr_fname,
        mime="text/markdown",
        use_container_width=True,
    )

elif page == "Opportunity and Pilot Recommendations":
    render_page_header(
        "Opportunity and Pilot Recommendations",
        "AI opportunity portfolio with scored opportunities, pilot sequencing, success measures, and responsible-use controls.",
    )
    render_responsible_use_warning()

    if "audit_data" not in st.session_state:
        render_status_box(
            "Audit data not loaded. "
            "Steps: 1. Go to Audit Data  →  2. Load BrightPath demo audit data  →  3. Return here.",
            "info",
        )
        st.stop()

    _audit = st.session_state["audit_data"]
    _org_name = _audit.get("organisation_profile", {}).get("organisation_name", "")

    _portfolio = og.generate_ai_opportunity_portfolio(_audit)
    _opp_summary = og.summarise_opportunity_portfolio(_portfolio)
    _portfolio_md = og.format_opportunity_portfolio_as_markdown(_portfolio, _opp_summary)

    st.session_state["opportunity_portfolio"] = _portfolio
    st.session_state["opportunity_summary"] = _opp_summary
    st.session_state["opportunity_portfolio_markdown"] = _portfolio_md

    # ── Summary metric cards ───────────────────────────────────────────────────
    _strategic_and_high = (
        _opp_summary["strategic_priority_opportunities"]
        + _opp_summary["high_priority_opportunities"]
    )
    render_metric_row([
        {"label": "AI Opportunities", "value": str(_opp_summary["total_opportunities"])},
        {"label": "Pilots", "value": str(_opp_summary["total_pilots"])},
        {"label": "Strategic / High", "value": str(_strategic_and_high)},
        {"label": "Recommended First Pilot", "value": _opp_summary["recommended_first_pilot_name"]},
    ])

    # ── Overall opportunity position ───────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Overall Opportunity Position")
    st.markdown(_opp_summary["overall_opportunity_position"])

    # ── Recommended focus areas ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Recommended Focus Areas")
    for _focus in _opp_summary["recommended_focus"]:
        st.markdown(f"- {_focus}")

    # ── Recommended first pilot ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Recommended First Pilot")
    _first = _portfolio.get("recommended_first_pilot", {})
    if _first:
        _fp_colour = og.get_opportunity_priority_colour(_first.get("pilot_priority", ""))
        st.markdown(
            f'<div style="border-left:5px solid {_fp_colour};padding:0.75rem 1rem;'
            f"background:#f8fafc;border-radius:0 8px 8px 0;margin-bottom:1.25rem;\">"
            f'<strong style="color:#1a2744;">{_first.get("pilot_id", "")} — {_first.get("pilot_name", "")}</strong><br/>'
            f'<span style="color:#334155;font-size:0.9rem;">'
            f'Priority: <strong>{_first.get("pilot_priority", "")}</strong> · '
            f'Complexity: {_first.get("complexity", "")} · '
            f'Risk: {_first.get("risk_level", "")} · '
            f'Timeline: {_first.get("suggested_timeline", "")}'
            f"</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        render_status_box("No pilots identified in the audit data.", "info")

    # ── Recommended pilot sequence ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Recommended Pilot Sequence")
    _sequence = _portfolio.get("recommended_pilot_sequence", [])
    if _sequence:
        _seq_cols = st.columns(len(_sequence))
        for _col, _item in zip(_seq_cols, _sequence):
            with _col:
                _colour = og.get_opportunity_priority_colour(_item.get("pilot_priority", ""))
                st.markdown(
                    f'<div style="background:#f1f5f9;border-radius:8px;padding:0.75rem;'
                    f'text-align:center;border-top:4px solid {_colour};">'
                    f'<div style="font-size:1.4rem;font-weight:800;color:#1a2744;">{_item["position"]}</div>'
                    f'<div style="font-weight:700;color:#1e3a5f;font-size:0.87rem;margin:0.3rem 0;">'
                    f'{_item["pilot_name"]}</div>'
                    f'<div style="color:#64748b;font-size:0.78rem;">{_item["suggested_timeline"]}</div>'
                    f'<div style="color:#64748b;font-size:0.78rem;">{_item["complexity"]} complexity · '
                    f'{_item["risk_level"]} risk</div>'
                    f"</div>",
                    unsafe_allow_html=True,
                )

    # ── AI Opportunity Table ───────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### AI Opportunities")

    _opps = _portfolio.get("opportunities", [])
    if not _opps:
        render_status_box("No workflow findings found in the loaded audit data.", "info")
    else:
        for _opp in _opps:
            _opp_colour = og.get_opportunity_priority_colour(_opp["priority"])
            with st.expander(
                f"{_opp['opportunity_id']} — {_opp['workflow_name']}  |  "
                f"{_opp['priority']}  |  Score: {_opp['opportunity_score']}/20"
            ):
                _oc1, _oc2 = st.columns([3, 1])
                with _oc1:
                    st.markdown(f"**AI opportunity:** {_opp['ai_opportunity']}")
                with _oc2:
                    st.markdown(
                        f'<div style="background:{_opp_colour};color:#ffffff;border-radius:6px;'
                        f"padding:0.4rem 0.75rem;text-align:center;font-weight:700;"
                        f'font-size:0.85rem;margin-bottom:0.5rem;">'
                        f"{_opp['priority']}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                    st.metric("Score", f"{_opp['opportunity_score']}/20")

                st.markdown("---")
                _os1, _os2, _os3 = st.columns(3)
                with _os1:
                    st.markdown(f"**Value:** {_opp['potential_value']} ({_opp['value_score']}/5)")
                    st.markdown(f"**Complexity:** {_opp['complexity']} ({_opp['complexity_score']}/5)")
                with _os2:
                    st.markdown(f"**Risk:** {_opp['risk_level']} ({_opp['risk_score']}/5)")
                with _os3:
                    pass

                st.markdown("---")
                st.markdown("**Recommended action:**")
                st.markdown(_opp["recommended_action"])

                if _opp.get("success_measures"):
                    with st.expander("Success measures"):
                        for _m in _opp["success_measures"]:
                            st.markdown(f"- {_m}")

                if _opp.get("responsible_use_controls"):
                    with st.expander("Responsible-use controls"):
                        for _c in _opp["responsible_use_controls"]:
                            st.markdown(f"- {_c}")

    # ── Pilot Recommendations ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Pilot Recommendations")

    _pilots = _portfolio.get("pilots", [])
    if not _pilots:
        render_status_box("No pilot recommendations found in the loaded audit data.", "info")
    else:
        for _pilot in _pilots:
            _pilot_colour = og.get_opportunity_priority_colour(_pilot["pilot_priority"])
            with st.expander(
                f"{_pilot['pilot_id']} — {_pilot['pilot_name']}  |  "
                f"{_pilot['pilot_priority']}  |  Timeline: {_pilot['suggested_timeline']}"
            ):
                _pc1, _pc2 = st.columns([3, 1])
                with _pc1:
                    st.markdown(f"**Business problem:** {_pilot['business_problem']}")
                    st.markdown(f"**Proposed solution:** {_pilot['proposed_solution']}")
                with _pc2:
                    st.markdown(
                        f'<div style="background:{_pilot_colour};color:#ffffff;border-radius:6px;'
                        f"padding:0.4rem 0.75rem;text-align:center;font-weight:700;"
                        f'font-size:0.85rem;margin-bottom:0.5rem;">'
                        f"{_pilot['pilot_priority']}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                if _pilot.get("expected_benefits"):
                    st.markdown("**Expected benefits:**")
                    for _b in _pilot["expected_benefits"]:
                        st.markdown(f"- {_b}")

                st.markdown("---")
                _pp1, _pp2 = st.columns(2)
                with _pp1:
                    st.markdown(f"**Complexity:** {_pilot['complexity']}")
                    st.markdown(f"**Risk level:** {_pilot['risk_level']}")
                with _pp2:
                    st.markdown(f"**Suggested timeline:** {_pilot['suggested_timeline']}")
                    st.markdown(f"**Recommended scope:** {_pilot['recommended_scope']}")

                if _pilot.get("success_measures"):
                    with st.expander("Success measures"):
                        for _m in _pilot["success_measures"]:
                            st.markdown(f"- {_m}")

                if _pilot.get("responsible_use_controls"):
                    with st.expander("Responsible-use controls"):
                        for _c in _pilot["responsible_use_controls"]:
                            st.markdown(f"- {_c}")

                if _pilot.get("human_review_requirements"):
                    with st.expander("Human review requirements"):
                        for _h in _pilot["human_review_requirements"]:
                            st.markdown(f"- {_h}")

    # ── Responsible-use ───────────────────────────────────────────────────────
    st.markdown("---")
    render_status_box(
        "This opportunity portfolio is generated from synthetic/demo audit data only. "
        "It must not be used with real client records, learner data, safeguarding case details, "
        "staff HR data, personal data, confidential data, or regulated information without "
        "appropriate governance, approvals, and responsible owners. "
        "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
        "financial, academic-integrity, or professional advice. "
        "Human review remains required before any real-world use.",
        "warning",
    )

    # ── Download ──────────────────────────────────────────────────────────────
    st.markdown("---")
    _opp_fname = create_safe_filename(f"opportunity-portfolio-{_org_name or 'audit'}", "md")
    st.download_button(
        label="Download Opportunity Portfolio (Markdown)",
        data=_portfolio_md,
        file_name=_opp_fname,
        mime="text/markdown",
        use_container_width=True,
    )


elif page == "Roadmap":
    render_page_header(
        "Roadmap",
        "30/60/90-day staged AI implementation plan with actions, owners, success measures, and responsible-use controls.",
    )
    render_responsible_use_warning()

    if "audit_data" not in st.session_state:
        render_status_box(
            "Audit data not loaded. "
            "Steps: 1. Go to Audit Data  →  2. Load BrightPath demo audit data  →  3. Return here.",
            "info",
        )
        st.stop()

    # Collect enrichment data from prior pages
    _has_readiness = "readiness_summary" in st.session_state
    _has_risk = "risk_register_summary" in st.session_state
    _has_opps = "opportunity_portfolio" in st.session_state
    if not (_has_readiness and _has_risk and _has_opps):
        render_status_box(
            "Tip: Run Readiness Summary, Risk Register, and Opportunity and Pilot Recommendations "
            "first for the richest roadmap. A basic roadmap can still be generated from the audit data alone.",
            "info",
        )

    _audit = st.session_state["audit_data"]
    _org_name = _audit.get("organisation_profile", {}).get("organisation_name", "")
    _readiness = st.session_state.get("readiness_summary")
    _risk_reg = st.session_state.get("risk_register")
    _risk_sum = st.session_state.get("risk_register_summary")
    _opp_port = st.session_state.get("opportunity_portfolio")

    _roadmap = rg.generate_implementation_roadmap(
        _audit, _readiness, _risk_reg, _risk_sum, _opp_port
    )
    _rm_summary = rg.summarise_implementation_roadmap(_roadmap)
    _rm_md = rg.format_implementation_roadmap_as_markdown(_roadmap, _rm_summary)

    st.session_state["implementation_roadmap"] = _roadmap
    st.session_state["implementation_roadmap_summary"] = _rm_summary
    st.session_state["implementation_roadmap_markdown"] = _rm_md

    # ── Summary metric cards ───────────────────────────────────────────────────
    render_metric_row([
        {"label": "Organisation", "value": _roadmap.get("organisation_name", "")},
        {"label": "Total Actions", "value": str(_rm_summary["total_actions"])},
        {"label": "High Priority", "value": str(_rm_summary["high_priority_actions"])},
        {"label": "Phases", "value": "3"},
        {"label": "Recommended First Pilot", "value": _rm_summary["recommended_first_pilot"]},
    ])

    # ── Overall roadmap position ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Overall Roadmap Position")
    st.markdown(_rm_summary["overall_roadmap_position"])

    # ── Recommended first pilot ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Recommended First Pilot")
    _fp = _roadmap.get("recommended_first_pilot") or {}
    if _fp:
        st.markdown(
            f'<div style="border-left:5px solid #166534;padding:0.75rem 1rem;'
            f"background:#f0fdf4;border-radius:0 8px 8px 0;margin-bottom:1.25rem;\">"
            f'<strong style="color:#1a2744;">{_fp.get("pilot_name", "—")}</strong><br/>'
            f'<span style="color:#334155;font-size:0.9rem;">'
            f'Complexity: {_fp.get("complexity", "—")} · '
            f'Risk: {_fp.get("risk_level", "—")} · '
            f'Timeline: {_fp.get("suggested_timeline", "—")}'
            f"</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ── Phase sections ─────────────────────────────────────────────────────────
    def _render_phase(phase_label, phase_focus, actions, phase_colour):
        st.markdown("---")
        st.markdown(
            f'<div style="border-left:5px solid {phase_colour};padding:0.5rem 1rem;'
            f"background:#f8fafc;border-radius:0 8px 8px 0;margin-bottom:1rem;\">"
            f'<strong style="color:{phase_colour};font-size:1.05rem;">{phase_label}</strong>'
            f'<span style="color:#64748b;font-size:0.85rem;"> — {phase_focus}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )
        if not actions:
            render_status_box("No actions generated for this phase.", "info")
            return
        for _act in actions:
            _prio = _act.get("priority", "Medium")
            _prio_colour = rg.get_priority_colour(_prio)
            with st.expander(
                f"{_act['action_id']} — {_act['title']}  |  {_prio}"
            ):
                _ac1, _ac2 = st.columns([3, 1])
                with _ac1:
                    st.markdown(_act["description"])
                with _ac2:
                    st.markdown(
                        f'<div style="background:{_prio_colour};color:#ffffff;border-radius:6px;'
                        f"padding:0.4rem 0.75rem;text-align:center;font-weight:700;"
                        f'font-size:0.85rem;">{_prio}</div>',
                        unsafe_allow_html=True,
                    )
                st.markdown("---")
                _a1, _a2 = st.columns(2)
                with _a1:
                    st.markdown(f"**Owner:** {_act['owner']}")
                with _a2:
                    st.markdown(f"**Success measure:** {_act['success_measure']}")
                if _act.get("dependency"):
                    st.markdown(f"**Dependency:** {_act['dependency']}")
                if _act.get("risk_reduction"):
                    st.markdown(f"**Risk reduction:** {_act['risk_reduction']}")
                if _act.get("related_output"):
                    st.markdown(f"**Related output:** {_act['related_output']}")

    _phase_defs = rg.get_roadmap_phase_definitions()
    _phase_data = {
        "First 30 days": _roadmap.get("phase_30_days", []),
        "Days 31–60": _roadmap.get("phase_60_days", []),
        "Days 61–90": _roadmap.get("phase_90_days", []),
    }
    for _pd in _phase_defs:
        _render_phase(
            _pd["phase_label"],
            _pd["phase_focus"],
            _phase_data.get(_pd["phase_label"], []),
            _pd["colour"],
        )

    # ── Cross-cutting controls ─────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Cross-Cutting Controls")
    for _ctrl in _roadmap.get("cross_cutting_controls", []):
        st.markdown(f"- {_ctrl}")

    # ── Success measures ──────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Success Measures")
    for _sm in _roadmap.get("success_measures", []):
        st.markdown(f"- {_sm}")

    # ── Dependencies ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Dependencies")
    for _dep in _roadmap.get("dependencies", []):
        st.markdown(f"- {_dep}")

    # ── Risks to manage ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Risks to Manage")
    for _r in _roadmap.get("risks_to_manage", []):
        st.markdown(f"- {_r}")

    # ── Responsible-use ───────────────────────────────────────────────────────
    st.markdown("---")
    render_status_box(
        "This roadmap is generated from synthetic/demo audit data only. "
        "It must not be used with real client records, learner data, safeguarding case details, "
        "staff HR data, personal data, confidential data, or regulated information without "
        "appropriate governance, approvals, and responsible owners. "
        "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
        "financial, academic-integrity, or professional advice. "
        "Human review remains required before any real-world use.",
        "warning",
    )

    # ── Download ──────────────────────────────────────────────────────────────
    st.markdown("---")
    _rm_fname = create_safe_filename(f"ai-roadmap-{_org_name or 'audit'}", "md")
    st.download_button(
        label="Download Implementation Roadmap (Markdown)",
        data=_rm_md,
        file_name=_rm_fname,
        mime="text/markdown",
        use_container_width=True,
    )

elif page == "Client Report":
    render_page_header(
        "Client Report",
        "Assemble a complete client-facing AI consulting report from all generated outputs.",
    )
    render_responsible_use_warning()
    render_prototype_notice()

    if "audit_data" not in st.session_state:
        render_status_box(
            "Audit data not loaded. "
            "Steps: 1. Go to Audit Data  →  2. Load BrightPath demo audit data  →  3. Return here.",
            "info",
        )
        st.stop()

    # ── Readiness check ────────────────────────────────────────────────────────
    _cr_readiness = rb.check_client_report_readiness(dict(st.session_state))
    st.session_state["client_report_readiness"] = _cr_readiness

    # ── Source availability checklist ──────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Report Readiness Checklist")
    _source_keys = {
        "readiness_summary": "Readiness Summary",
        "risk_register": "Risk Register",
        "risk_register_summary": "Risk Register Summary",
        "opportunity_portfolio": "Opportunity Portfolio",
        "opportunity_summary": "Opportunity Summary",
        "implementation_roadmap": "Implementation Roadmap",
        "implementation_roadmap_summary": "Roadmap Summary",
        "report_sections": "Report Sections",
    }
    _check_cols = st.columns(4)
    for _i, (key, label) in enumerate(_source_keys.items()):
        _available = st.session_state.get(key) is not None
        with _check_cols[_i % 4]:
            _icon = "Yes" if _available else "-"
            st.markdown(
                f'<div style="text-align:center;padding:0.5rem;background:#f8fafc;'
                f'border-radius:8px;font-size:0.78rem;margin-bottom:0.5rem;">'
                f'<div style="font-size:1.1rem;">{_icon}</div>'
                f'<strong>{label}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if _cr_readiness["recommended_next_steps"]:
        st.markdown("**To get the richest report, run these pages first:**")
        for _step in _cr_readiness["recommended_next_steps"]:
            st.markdown(f"- {_step}")

    # ── Section selection ──────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Select Report Sections")

    _has_readiness = st.session_state.get("readiness_summary") is not None
    _has_risk = st.session_state.get("risk_register") is not None
    _has_opps = st.session_state.get("opportunity_portfolio") is not None
    _has_roadmap = st.session_state.get("implementation_roadmap") is not None

    _sc1, _sc2 = st.columns(2)
    with _sc1:
        _inc_readiness = st.checkbox("AI Readiness Summary", value=_has_readiness)
        _inc_key_findings = st.checkbox("Key Findings", value=True)
        _inc_risk = st.checkbox("Risk Register Summary", value=_has_risk)
        _inc_training = st.checkbox("Training and Capability Needs", value=True)
        _inc_governance = st.checkbox("Governance Recommendations", value=True)
    with _sc2:
        _inc_opps = st.checkbox("Opportunity and Pilot Recommendations", value=_has_opps)
        _inc_roadmap = st.checkbox("30/60/90-Day Roadmap", value=_has_roadmap)
        _inc_next_steps = st.checkbox("Immediate Next Steps", value=True)
        _inc_appendices = st.checkbox("Appendices", value=True)

    _include_sections = {
        "readiness_summary": _inc_readiness,
        "key_findings": _inc_key_findings,
        "risk_register_summary": _inc_risk,
        "opportunity_summary": _inc_opps,
        "roadmap_summary": _inc_roadmap,
        "training_needs": _inc_training,
        "governance_recommendations": _inc_governance,
        "next_steps": _inc_next_steps,
        "appendices": _inc_appendices,
    }

    # ── Generate report ────────────────────────────────────────────────────────
    st.markdown("---")
    _report_data = rb.build_client_report_data_from_session_state(dict(st.session_state))
    _cr_markdown = rb.generate_markdown_client_report(_report_data, _include_sections)
    _cr_summary = rb.summarise_client_report(_report_data)
    _cr_filename = rb.create_client_report_filename(
        _report_data.get("organisation_name", "audit")
    )

    st.session_state["client_report_data"] = _report_data
    st.session_state["client_report_markdown"] = _cr_markdown
    st.session_state["client_report_filename"] = _cr_filename

    # ── Summary metric cards ───────────────────────────────────────────────────
    _sections_inc = sum(1 for v in _include_sections.values() if v) + 4  # +4 always-on
    _sections_miss = sum(1 for v in _include_sections.values() if not v)
    render_metric_row([
        {"label": "Organisation", "value": _report_data.get("organisation_name", "—")},
        {"label": "Sections Included", "value": str(_sections_inc)},
        {"label": "Missing Recommended", "value": str(len(_cr_readiness["missing_sections"]))},
        {"label": "Risks Included", "value": str(_cr_summary["risks_included"])},
        {"label": "Pilots Included", "value": str(_cr_summary["pilots_included"])},
    ])

    # ── Report readiness statement ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Report Readiness")
    st.markdown(_cr_summary["report_readiness"])

    # ── Markdown preview ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Report Preview")
    with st.expander("View Full Client Report (Markdown)", expanded=False):
        st.markdown(_cr_markdown)

    # ── Download ───────────────────────────────────────────────────────────────
    st.markdown("---")
    st.download_button(
        label="Download Client Report (Markdown)",
        data=_cr_markdown,
        file_name=_cr_filename,
        mime="text/markdown",
        use_container_width=True,
    )

elif page == "Export Centre":
    render_page_header(
        "Export Centre",
        "Export the complete AI consulting report as Markdown, PDF, and PowerPoint.",
    )
    render_responsible_use_warning()
    render_prototype_notice()

    # ── Guard: audit data ──────────────────────────────────────────────────────
    if "audit_data" not in st.session_state:
        render_status_box(
            "Audit data not loaded. "
            "Steps: 1. Go to Audit Data  →  2. Load BrightPath demo audit data  →  "
            "3. Generate earlier outputs  →  4. Generate Client Report  →  5. Return here.",
            "info",
        )
        st.stop()

    # ── Guard: client report ───────────────────────────────────────────────────
    if "client_report_markdown" not in st.session_state:
        render_status_box(
            "Client report not generated. "
            "Steps: 1. Go to Client Report  →  2. Generate the report  →  3. Return here.",
            "info",
        )
        st.stop()

    # ── Build export data ──────────────────────────────────────────────────────
    _export_data = ec.build_export_data_from_session_state(dict(st.session_state))
    _ex_readiness = ec.check_export_readiness(dict(st.session_state))
    st.session_state["export_data"] = _export_data
    st.session_state["export_readiness"] = _ex_readiness

    # ── Analytics ──────────────────────────────────────────────────────────────
    _analytics = ra.build_client_report_analytics(_export_data)
    st.session_state["client_report_analytics"] = _analytics

    # ── Charts ────────────────────────────────────────────────────────────────
    _chart_paths = {}
    try:
        _chart_paths = cu.generate_all_export_charts(_analytics, "outputs/charts")
    except Exception:
        pass
    st.session_state["client_report_chart_paths"] = _chart_paths

    # ── Summary metric cards ───────────────────────────────────────────────────
    _ex_summary = ec.summarise_export_package(_export_data)
    render_metric_row([
        {"label": "Organisation", "value": _ex_summary["organisation_name"]},
        {"label": "Outputs Available", "value": str(_ex_summary["sections_available"])},
        {"label": "Missing Outputs", "value": str(_ex_summary["sections_missing"])},
        {"label": "Risks Included", "value": str(_ex_summary["risks_included"])},
        {"label": "Pilots Included", "value": str(_ex_summary["pilots_included"])},
        {"label": "Roadmap Actions", "value": str(_ex_summary["roadmap_actions_included"])},
    ])

    # ── Export readiness checklist ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Export Readiness Checklist")
    _quality = ec.generate_export_quality_checklist(_export_data)
    _q_cols = st.columns(3)
    for _qi, _check in enumerate(_quality):
        with _q_cols[_qi % 3]:
            _icon = "Yes" if _check["passed"] else "No"
            st.markdown(f"{_icon} {_check['item']}")

    if _ex_readiness["recommended_next_steps"]:
        with st.expander("Recommended steps to enrich the export"):
            for _step in _ex_readiness["recommended_next_steps"]:
                st.markdown(f"- {_step}")

    # ── Analytics summary ──────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Analytics Summary")
    _an_cols = st.columns(2)

    with _an_cols[0]:
        st.markdown("**Report Output Completion**")
        for output, done in (_analytics.get("completion_status") or {}).items():
            st.markdown(f"- {output}")

    with _an_cols[1]:
        st.markdown("**Readiness Scores**")
        for cat, score in (_analytics.get("readiness_score_breakdown") or {}).items():
            st.markdown(f"- {cat}: **{score}/100**")

    _an_cols2 = st.columns(3)
    with _an_cols2[0]:
        st.markdown("**Risks by Level**")
        for level, count in (_analytics.get("risk_level_counts") or {}).items():
            st.markdown(f"- {level}: {count}")
    with _an_cols2[1]:
        st.markdown("**Opportunities by Priority**")
        for priority, count in (_analytics.get("opportunity_priority_counts") or {}).items():
            st.markdown(f"- {priority}: {count}")
    with _an_cols2[2]:
        st.markdown("**Roadmap Actions by Phase**")
        for phase, count in (_analytics.get("roadmap_action_counts") or {}).items():
            st.markdown(f"- {phase}: {count}")

    # ── Chart previews ─────────────────────────────────────────────────────────
    if _chart_paths:
        st.markdown("---")
        st.markdown("### Chart Previews")
        _chart_labels = {
            "completion_status": "Output Completion",
            "readiness_scores": "Readiness Scores",
            "risk_levels": "Risk Distribution",
            "opportunity_priorities": "Opportunity Priorities",
            "roadmap_actions": "Roadmap Actions",
        }
        _chart_cols = st.columns(min(3, len(_chart_paths)))
        for _ci, (key, path) in enumerate(_chart_paths.items()):
            with _chart_cols[_ci % 3]:
                try:
                    with open(path, "rb") as _f:
                        st.image(_f.read(), caption=_chart_labels.get(key, key))
                except Exception:
                    st.markdown(f"*{_chart_labels.get(key, key)} — chart not available*")
    else:
        render_status_box(
            "Charts could not be generated. Downloads still work without charts.", "info"
        )

    # ── Prepare exports ────────────────────────────────────────────────────────
    _md_text, _md_fname = ec.prepare_markdown_export(_export_data)

    _pdf_bytes = b""
    _pdf_fname = ""
    try:
        _pdf_bytes, _pdf_fname = ec.prepare_pdf_export(
            _export_data, _analytics, _chart_paths
        )
    except Exception:
        pass

    _pptx_bytes = b""
    _pptx_fname = ""
    try:
        _pptx_bytes, _pptx_fname = ec.prepare_pptx_export(
            _export_data, _analytics, _chart_paths
        )
    except Exception:
        pass

    st.session_state["client_report_pdf_bytes"] = _pdf_bytes
    st.session_state["client_report_pdf_filename"] = _pdf_fname
    st.session_state["client_report_pptx_bytes"] = _pptx_bytes
    st.session_state["client_report_pptx_filename"] = _pptx_fname

    # ── Download buttons ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Export Downloads")

    _dl1, _dl2, _dl3 = st.columns(3)

    with _dl1:
        st.download_button(
            label="Download Markdown Report",
            data=_md_text,
            file_name=_md_fname,
            mime="text/markdown",
            use_container_width=True,
        )

    with _dl2:
        if _pdf_bytes:
            st.download_button(
                label="Download PDF Consulting Report",
                data=_pdf_bytes,
                file_name=_pdf_fname,
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            render_status_box("PDF export not available. Check reportlab is installed.", "info")

    with _dl3:
        if _pptx_bytes:
            st.download_button(
                label="Download PowerPoint Executive Deck",
                data=_pptx_bytes,
                file_name=_pptx_fname,
                mime=(
                    "application/vnd.openxmlformats-officedocument"
                    ".presentationml.presentation"
                ),
                use_container_width=True,
            )
        else:
            render_status_box("PPTX export not available. Check python-pptx is installed.", "info")

    # ── Responsible-use ────────────────────────────────────────────────────────
    st.markdown("---")
    render_status_box(
        "All exports are generated from synthetic/demo audit data only. "
        "They must not be used with real client records, learner data, safeguarding case "
        "details, staff HR data, personal data, or regulated information. "
        "Human review remains required before any real-world use.",
        "warning",
    )

elif page == "Completion Review":
    render_page_header(
        "Completion Review",
        "Review Build 5 readiness, documentation, portfolio value, and final demo actions.",
    )
    render_responsible_use_warning()
    render_prototype_notice()

    _review = cr.generate_build5_completion_review(dict(st.session_state), base_path=".")
    _portfolio_summary = cr.generate_portfolio_summary()
    _case_study_summary = cr.generate_case_study_summary()
    _completion_md = cr.format_completion_review_as_markdown(_review)
    _portfolio_md = cr.format_portfolio_notes_as_markdown(
        _portfolio_summary, _case_study_summary
    )

    st.session_state["completion_review"] = _review
    st.session_state["completion_review_markdown"] = _completion_md
    st.session_state["portfolio_notes"] = {
        "portfolio_summary": _portfolio_summary,
        "case_study_summary": _case_study_summary,
    }
    st.session_state["portfolio_notes_markdown"] = _portfolio_md

    _status = _review["completion_status"]
    _outputs = _review["output_status"]
    _docs = _review["documentation_status"]

    render_metric_row([
        {"label": "Overall Status", "value": _status["overall_status"]},
        {"label": "Phase Completion", "value": f"{_status['phase_completion_percentage']}%"},
        {"label": "Output Completion", "value": f"{_status['output_completion_percentage']}%"},
        {
            "label": "Documentation Completion",
            "value": f"{_status['documentation_completion_percentage']}%",
        },
    ])

    st.markdown("### Final Readiness")
    render_status_box(_status["final_readiness_label"], "success" if _status["overall_status"] == "Complete" else "info")

    _p_cols = st.columns(3)
    with _p_cols[0]:
        st.markdown("**Phases**")
        st.progress(int(_status["phase_completion_percentage"]))
    with _p_cols[1]:
        st.markdown("**Session Outputs**")
        st.progress(int(_status["output_completion_percentage"]))
    with _p_cols[2]:
        st.markdown("**Documentation**")
        st.progress(int(_status["documentation_completion_percentage"]))

    st.markdown("---")
    st.markdown("### Phase Completion Checklist")
    _phase_cols = st.columns(3)
    for _idx, _phase in enumerate(_review["phase_checklist"]):
        with _phase_cols[_idx % 3]:
            with st.expander(f"{_phase['phase']} - {_phase['name']}", expanded=False):
                st.markdown(f"**Status:** {_phase['status']}")
                st.markdown(f"**Purpose:** {_phase['purpose']}")
                st.markdown(f"**Evidence:** {_phase['evidence']}")

    st.markdown("---")
    st.markdown("### Output Completion Status")
    render_metric_row([
        {"label": "Available Outputs", "value": str(_outputs["available_count"])},
        {"label": "Missing Outputs", "value": str(_outputs["missing_count"])},
        {"label": "Expected Outputs", "value": str(_outputs["total_expected"])},
    ])

    with st.expander("Available Outputs", expanded=False):
        if _outputs["available_outputs"]:
            for _item in _outputs["available_outputs"]:
                st.markdown(f"- {_item['label']} ({_item['page']})")
        else:
            st.markdown("No workflow outputs are available yet. Start with Audit Data.")

    with st.expander("Missing Outputs", expanded=_outputs["missing_count"] > 0):
        if _outputs["missing_outputs"]:
            for _item in _outputs["missing_outputs"]:
                st.markdown(f"- {_item['label']} ({_item['page']})")
        else:
            st.markdown("All expected session outputs are available.")

    st.markdown("---")
    st.markdown("### Documentation Checklist")
    render_metric_row([
        {"label": "Docs Available", "value": str(_docs["existing_count"])},
        {"label": "Docs Missing", "value": str(_docs["missing_count"])},
        {"label": "Docs Expected", "value": str(_docs["total_expected"])},
    ])

    _doc_cols = st.columns(2)
    with _doc_cols[0]:
        st.markdown("**Existing documentation**")
        for _file in _docs["existing_files"]:
            st.markdown(f"- {_file}")
    with _doc_cols[1]:
        st.markdown("**Missing documentation**")
        if _docs["missing_files"]:
            for _file in _docs["missing_files"]:
                st.markdown(f"- {_file}")
        else:
            st.markdown("All expected documentation files are present.")

    st.markdown("---")
    _value_cols = st.columns(2)
    with _value_cols[0]:
        render_info_card("Portfolio Value", _review["portfolio_value"])
        render_info_card("Technical Value", _review["technical_value"])
    with _value_cols[1]:
        render_info_card("Commercial Value", _review["commercial_value"])
        render_info_card("Responsible-Use Position", _review["responsible_use_position"])

    st.markdown("### Recommended Final Actions")
    for _action in _review["recommended_final_actions"]:
        st.markdown(f"- {_action}")

    st.markdown("---")
    with st.expander("Completion Review Markdown Preview", expanded=False):
        st.markdown(_completion_md)

    with st.expander("Portfolio Notes Markdown Preview", expanded=False):
        st.markdown(_portfolio_md)

    _review_file = create_safe_filename("build-5-completion-review", "md")
    _portfolio_file = create_safe_filename("build-5-portfolio-notes", "md")

    _download_cols = st.columns(2)
    with _download_cols[0]:
        st.download_button(
            label="Download Completion Review",
            data=_completion_md,
            file_name=_review_file,
            mime="text/markdown",
            use_container_width=True,
        )
    with _download_cols[1]:
        st.download_button(
            label="Download Portfolio Notes",
            data=_portfolio_md,
            file_name=_portfolio_file,
            mime="text/markdown",
            use_container_width=True,
        )
