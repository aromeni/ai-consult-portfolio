"""
BrightPath AI Readiness + Workflow Audit Tool
Streamlit prototype — v0.7 (Polish Step 4: UI refresh)
"""

import streamlit as st
import pandas as pd

from src.utils import (
    init_session_state,
    inject_custom_css,
    render_page_header,
    render_safety_notice,
    render_responsible_use,
    get_risk_badge,
    render_risk_table,
    render_score_hero,
    render_recommendation_card,
    render_next_actions,
    render_safeguards,
    render_section_heading,
)
from src.sample_data import (
    BRIGHTPATH_PROFILE,
    BRIGHTPATH_READINESS_RESPONSES,
    BRIGHTPATH_READINESS_SCORES,
    BRIGHTPATH_WORKFLOWS,
    BRIGHTPATH_SAMPLE_WORKFLOW,
    BRIGHTPATH_SAMPLE_WORKFLOW_SCORES,
    BRIGHTPATH_RISK_PROFILE,
    BRIGHTPATH_PILOT_EXAMPLE,
    BRIGHTPATH_MINI_REPORT_SAMPLE,
)
from src.scoring import (
    DIMENSION_LABELS,
    READINESS_DIMENSIONS,
    WORKFLOW_SCORING_DIMENSIONS,
    RISK_CATEGORIES,
    total_readiness_score,
    readiness_band,
    workflow_summary,
    pilot_workflow_candidates,
    calculate_readiness_score,
    get_readiness_level,
    get_readiness_category,
    get_readiness_explanation,
    get_next_action,
    calculate_workflow_suitability_score,
    get_workflow_suitability_level,
    get_workflow_suitability_category,
    get_workflow_suitability_explanation,
    get_workflow_next_action,
    calculate_risk_score,
    get_risk_level,
    get_risk_level_explanation,
    get_risk_safeguard,
    calculate_overall_risk_summary,
    _PILOT_ALERT_TYPES,
    get_pilot_recommendation,
    get_pilot_recommendation_explanation,
    get_pilot_next_actions,
    get_pilot_safeguards,
)
from src.report_generator import (
    generate_text_report,
    generate_markdown_report,
    generate_pdf_report_bytes,
    format_safeguards,
    format_next_actions,
    create_report_filename,
    create_pdf_report_filename,
)

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="BrightPath AI Readiness Tool",
    page_icon="📋",
    layout="wide",
)

# ── Session state + CSS ───────────────────────────────────────────────────────

init_session_state()
inject_custom_css()

# ── Sidebar navigation ────────────────────────────────────────────────────────

PAGES = [
    "🏠  Home",
    "🏢  Organisation Profile",
    "📊  AI Readiness Assessment",
    "⚙️  Workflow Audit",
    "⚠️  Risk Assessment",
    "🚀  Pilot Recommendation",
    "📄  Mini Report",
]

with st.sidebar:
    st.markdown(
        '<div style="padding:0.5rem 0 0.65rem">'
        '<p style="font-size:1.05rem;font-weight:700;color:#1e3a5f;margin:0;line-height:1.2">BrightPath</p>'
        '<p style="font-size:0.78rem;color:#718096;margin:0.2rem 0 0;line-height:1.3">'
        "AI Readiness + Workflow Audit</p>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    page = st.radio("Navigate to:", PAGES, label_visibility="collapsed")
    st.markdown("---")
    st.markdown(
        '<p style="font-size:0.76rem;color:#a0aec0;line-height:1.65;margin:0">'
        "<strong style='color:#718096'>Prototype v0.7</strong> · Polish Step 4<br>"
        "⚠️ Synthetic data only.<br>"
        "No real personal or confidential data."
        "</p>",
        unsafe_allow_html=True,
    )

# ── Home ──────────────────────────────────────────────────────────────────────

if page == PAGES[0]:
    render_page_header(
        "BrightPath AI Readiness + Workflow Audit Tool",
        "A structured AI readiness diagnostic for small UK training providers.",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pages", "7")
    with col2:
        st.metric("Readiness dimensions", "10")
    with col3:
        st.metric("Sample workflows", str(len(BRIGHTPATH_WORKFLOWS)))

    st.markdown(
        """
        <div class="bp-feature-grid">
          <div class="bp-feature-card">
            <div class="card-icon">📊</div>
            <div class="card-title">AI Readiness Assessment</div>
            <div class="card-desc">Score the organisation across 10 dimensions. Total out of 100 with five readiness bands.</div>
          </div>
          <div class="bp-feature-card">
            <div class="card-icon">⚙️</div>
            <div class="card-title">Workflow Audit</div>
            <div class="card-desc">Score one workflow for AI suitability across 10 dimensions. Total out of 50.</div>
          </div>
          <div class="bp-feature-card">
            <div class="card-icon">⚠️</div>
            <div class="card-title">Risk Assessment</div>
            <div class="card-desc">Rate 10 risk categories by likelihood × impact. Safeguards per category.</div>
          </div>
          <div class="bp-feature-card">
            <div class="card-icon">🚀</div>
            <div class="card-title">Pilot Recommendation</div>
            <div class="card-desc">Combines all three scores into one of six evidence-based recommendations.</div>
          </div>
          <div class="bp-feature-card">
            <div class="card-icon">📄</div>
            <div class="card-title">Mini Report</div>
            <div class="card-desc">Editable 9-section Markdown report. Preview and download in one click.</div>
          </div>
          <div class="bp-feature-card">
            <div class="card-icon">🛡️</div>
            <div class="card-title">Responsible AI</div>
            <div class="card-desc">Safety notices on every page. No real personal or learner data required.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    render_section_heading("How to use this tool")

    steps = [
        ("Home", "Load the BrightPath demo data below to see a complete worked example instantly."),
        ("Organisation Profile", "Review the organisation's details and governance gaps at a glance."),
        ("AI Readiness Assessment", "Rate the organisation across 10 readiness dimensions (0–10 each)."),
        ("Workflow Audit", "Score one workflow for AI suitability across 10 suitability dimensions."),
        ("Risk Assessment", "Rate 10 risk categories by likelihood and impact (1–5 each)."),
        ("Pilot Recommendation", "See the combined recommendation, next actions, and safeguards."),
        ("Mini Report", "Review, edit, and download the structured Markdown report."),
    ]
    steps_html = "".join(
        f'<div class="bp-step-row">'
        f'<div class="bp-step-num">{i}</div>'
        f'<div class="bp-step-text"><strong>{title}</strong> — {desc}</div>'
        f"</div>"
        for i, (title, desc) in enumerate(steps, 1)
    )
    st.markdown(steps_html, unsafe_allow_html=True)

    st.divider()
    render_section_heading("Load demo data")
    st.markdown(
        "Load the synthetic BrightPath Skills Training profile to see a complete worked "
        "example without filling in every field manually."
    )

    if st.button("▶  Load BrightPath demo data", type="primary"):
        st.session_state["profile"] = BRIGHTPATH_PROFILE.copy()
        st.session_state["readiness_responses"] = BRIGHTPATH_READINESS_RESPONSES.copy()
        st.session_state["workflows"] = BRIGHTPATH_WORKFLOWS.copy()

        score = total_readiness_score(st.session_state["readiness_responses"])
        st.session_state["band"] = readiness_band(score)
        st.session_state["workflow_summary"] = workflow_summary(st.session_state["workflows"])
        st.session_state["pilot_candidates"] = pilot_workflow_candidates(st.session_state["workflows"])

        for dim in READINESS_DIMENSIONS:
            st.session_state[f"slider_{dim['key']}"] = (
                BRIGHTPATH_READINESS_SCORES.get(dim["key"], 0)
            )

        # Pre-populate standardised score keys from demo data
        _demo_r = sum(BRIGHTPATH_READINESS_SCORES.get(d["key"], 0) for d in READINESS_DIMENSIONS)
        st.session_state["readiness_score"] = _demo_r
        st.session_state["readiness_category"] = get_readiness_category(_demo_r)

        _demo_w = sum(
            BRIGHTPATH_SAMPLE_WORKFLOW_SCORES.get(d["key"], 0) for d in WORKFLOW_SCORING_DIMENSIONS
        )
        st.session_state["workflow_score"] = _demo_w
        st.session_state["workflow_category"] = get_workflow_suitability_category(_demo_w)
        st.session_state["workflow_name"] = BRIGHTPATH_SAMPLE_WORKFLOW["name"]
        st.session_state["proposed_ai_support"] = BRIGHTPATH_SAMPLE_WORKFLOW["ai_support_idea"]

        _demo_risk_rows = [
            {
                "level": get_risk_level(
                    calculate_risk_score(
                        BRIGHTPATH_RISK_PROFILE["scores"][c["key"]]["likelihood"],
                        BRIGHTPATH_RISK_PROFILE["scores"][c["key"]]["impact"],
                    )
                )
            }
            for c in RISK_CATEGORIES
        ]
        _demo_risk_summary = calculate_overall_risk_summary(_demo_risk_rows)
        st.session_state["highest_risk_level"] = _demo_risk_summary["highest_level"]
        st.session_state["critical_risk_count"] = _demo_risk_summary["counts"]["Critical"]
        st.session_state["high_risk_count"] = _demo_risk_summary["counts"]["High"]

        # Context and narrative fields for Mini Report
        st.session_state["ai_use_summary"] = BRIGHTPATH_MINI_REPORT_SAMPLE["ai_use_summary"]
        st.session_state["main_concerns"] = BRIGHTPATH_MINI_REPORT_SAMPLE["main_concerns"]
        st.session_state["workflow_owner"] = BRIGHTPATH_SAMPLE_WORKFLOW["owner"]
        st.session_state["key_risk_notes"] = BRIGHTPATH_MINI_REPORT_SAMPLE["key_risk_notes"]
        st.session_state["consultant_notes"] = BRIGHTPATH_MINI_REPORT_SAMPLE["consultant_notes"]

        # Pilot recommendation fields
        _demo_rec = get_pilot_recommendation(
            _demo_r, _demo_w,
            _demo_risk_summary["highest_level"],
            _demo_risk_summary["counts"]["Critical"] > 0,
            _demo_risk_summary["counts"]["High"] > 0,
        )
        _demo_rec_exp = get_pilot_recommendation_explanation(
            _demo_rec, _demo_r, _demo_w, _demo_risk_summary["highest_level"]
        )
        st.session_state["pilot_recommendation"] = _demo_rec
        st.session_state["pilot_explanation"] = _demo_rec_exp
        st.session_state["recommended_safeguards"] = format_safeguards(get_pilot_safeguards(_demo_rec))
        st.session_state["next_actions"] = format_next_actions(get_pilot_next_actions(_demo_rec))

        st.success("BrightPath demo data loaded. Use the sidebar to navigate through each section.")

    render_responsible_use()

# ── Organisation Profile ──────────────────────────────────────────────────────

elif page == PAGES[1]:
    render_page_header(
        "Organisation Profile",
        "Profile for the current session. Load demo data from the Home page to see a worked example.",
    )
    render_safety_notice(
        "Review profile details at an organisation level only. "
        "Do not enter names, learner records, or personal information."
    )

    if st.session_state.get("profile"):
        p = st.session_state["profile"]
        tools = p.get("current_ai_tools", [])
        tools_str = ", ".join(tools) if tools else "None reported"
        ai_policy = (
            '<span class="flag-yes">Yes</span>'
            if p.get("has_ai_policy")
            else '<span class="flag-no">No</span>'
        )
        approved_tools = (
            '<span class="flag-yes">Yes</span>'
            if p.get("has_approved_tools")
            else '<span class="flag-no">No</span>'
        )
        dpo = (
            '<span class="flag-yes">Yes</span>'
            if p.get("has_dpo_or_lead")
            else '<span class="flag-no">No</span>'
        )
        st.markdown(
            f"""
            <div class="bp-profile-card">
              <div class="bp-profile-item">
                <span class="bp-profile-label">Organisation</span>
                <span class="bp-profile-value">{p.get("org_name", "—")}</span>
              </div>
              <div class="bp-profile-item">
                <span class="bp-profile-label">Type</span>
                <span class="bp-profile-value">{p.get("org_type", "—")}</span>
              </div>
              <div class="bp-profile-item">
                <span class="bp-profile-label">Sector</span>
                <span class="bp-profile-value">{p.get("sector", "—")}</span>
              </div>
              <div class="bp-profile-item">
                <span class="bp-profile-label">Staff</span>
                <span class="bp-profile-value">{p.get("staff_count", "—")}</span>
              </div>
              <div class="bp-profile-item">
                <span class="bp-profile-label">AI tools in use</span>
                <span class="bp-profile-value">{tools_str}</span>
              </div>
              <div class="bp-profile-item">
                <span class="bp-profile-label">AI policy in place</span>
                <span class="bp-profile-value">{ai_policy}</span>
              </div>
              <div class="bp-profile-item">
                <span class="bp-profile-label">Approved AI tools list in place</span>
                <span class="bp-profile-value">{approved_tools}</span>
              </div>
              <div class="bp-profile-item">
                <span class="bp-profile-label">DPO / data lead</span>
                <span class="bp-profile-value">{dpo}</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if p.get("notes"):
            st.caption(f"**Context notes:** {p['notes']}")

        if not p.get("has_ai_policy") or not p.get("has_approved_tools"):
            st.warning(
                "**Governance gap:** This organisation has some data responsibility in place, "
                "but does not yet have a formal AI policy and/or approved AI tools list. "
                "Any AI pilot should begin with clear data boundaries, approved tool guidance, "
                "and human review."
            )
    else:
        st.info(
            "No profile loaded yet. Go to the **Home** page and click "
            "**Load BrightPath demo data** to see a worked example."
        )

    render_responsible_use()

# ── AI Readiness Assessment ───────────────────────────────────────────────────

elif page == PAGES[2]:
    render_page_header(
        "AI Readiness Assessment",
        "Rate the organisation across 10 dimensions. Total score out of 100 determines the readiness category.",
    )
    render_safety_notice(
        "Rate the organisation using general, role-level observations only. "
        "Do not enter names, learner data, client details, safeguarding information, "
        "or any personal or confidential data."
    )

    st.markdown(
        '<div class="scale-legend">'
        "<span><strong>0</strong> = Not in place</span>"
        "<span><strong>5</strong> = Partially in place</span>"
        "<span><strong>10</strong> = Fully established</span>"
        "</div>",
        unsafe_allow_html=True,
    )

    scores = {}
    for dim in READINESS_DIMENSIONS:
        scores[dim["key"]] = st.slider(
            dim["question"],
            min_value=0,
            max_value=10,
            key=f"slider_{dim['key']}",
            help=dim["hint"],
        )

    st.divider()
    render_section_heading("Results")

    total = calculate_readiness_score(scores)
    level = get_readiness_level(total)
    st.session_state["readiness_score"] = total
    st.session_state["readiness_category"] = level["category"]

    col1, col2 = st.columns([1, 2])
    with col1:
        render_score_hero(total, 100, "AI Readiness Score")
    with col2:
        alert_fn = getattr(st, level["alert_type"], st.info)
        alert_fn(f"**{level['category']}**\n\n{level['explanation']}")
        st.info(f"💡 **Suggested next action:** {level['next_action']}")

    st.divider()
    render_section_heading("Dimension scores")

    chart_df = pd.DataFrame(
        {"Score (0–10)": [scores[d["key"]] for d in READINESS_DIMENSIONS]},
        index=[d["label"] for d in READINESS_DIMENSIONS],
    )
    st.bar_chart(chart_df)

    with st.expander("View as table"):
        st.dataframe(
            pd.DataFrame(
                [{"Dimension": d["label"], "Score": scores[d["key"]], "Max": 10}
                 for d in READINESS_DIMENSIONS]
            ),
            use_container_width=True,
            hide_index=True,
        )

    render_responsible_use()

# ── Workflow Audit ────────────────────────────────────────────────────────────

elif page == PAGES[3]:
    render_page_header(
        "Workflow Audit",
        "Describe one workflow and score it across 10 suitability dimensions. Score out of 50.",
    )
    render_safety_notice(
        "Describe workflows at a role and process level only. "
        "Do not enter names, learner records, client details, safeguarding information, "
        "financial data, or any personal or confidential information."
    )

    # ── Load sample button — must sit above all keyed widgets ─────────────────

    if st.button("Load BrightPath sample workflow (Generic lesson planning support)"):
        wf = BRIGHTPATH_SAMPLE_WORKFLOW
        st.session_state["wf_name"] = wf["name"]
        st.session_state["wf_owner"] = wf["owner"]
        st.session_state["wf_description"] = wf["description"]
        st.session_state["wf_tools"] = wf["tools"]
        st.session_state["wf_frequency"] = wf["frequency"]
        st.session_state["wf_time_spent"] = wf["time_spent"]
        st.session_state["wf_pain_points"] = wf["pain_points"]
        st.session_state["wf_data_sensitivity"] = wf["data_sensitivity"]
        st.session_state["wf_ai_support_idea"] = wf["ai_support_idea"]
        for dim in WORKFLOW_SCORING_DIMENSIONS:
            st.session_state[f"ws_{dim['key']}"] = (
                BRIGHTPATH_SAMPLE_WORKFLOW_SCORES.get(dim["key"], 0)
            )
        _wf_total = sum(
            BRIGHTPATH_SAMPLE_WORKFLOW_SCORES.get(d["key"], 0) for d in WORKFLOW_SCORING_DIMENSIONS
        )
        st.session_state["workflow_score"] = _wf_total
        st.session_state["workflow_category"] = get_workflow_suitability_category(_wf_total)
        st.session_state["workflow_name"] = wf["name"]
        st.session_state["proposed_ai_support"] = wf["ai_support_idea"]
        st.session_state["workflow_owner"] = wf["owner"]
        st.rerun()

    st.divider()
    render_section_heading("1. Workflow information")
    st.caption(
        "Describe the workflow at a process and role level. "
        "Use fictional or anonymised descriptions — do not enter real names or case details."
    )

    col1, col2 = st.columns(2)
    with col1:
        wf_name = st.text_input(
            "Workflow name",
            placeholder="e.g. Generic lesson planning support",
            key="wf_name",
        )
    with col2:
        wf_owner = st.text_input(
            "Current owner or team",
            placeholder="e.g. Tutor team",
            key="wf_owner",
        )

    col3, col4 = st.columns(2)
    with col3:
        wf_tools = st.text_input(
            "Current tools used",
            placeholder="e.g. Word processor, email, spreadsheet",
            key="wf_tools",
        )
    with col4:
        wf_frequency = st.selectbox(
            "Workflow frequency",
            options=["Daily", "Weekly", "Monthly", "Ad hoc / variable"],
            key="wf_frequency",
        )

    col5, col6 = st.columns(2)
    with col5:
        wf_time_spent = st.text_input(
            "Approximate time spent per instance",
            placeholder="e.g. ~45 minutes",
            key="wf_time_spent",
        )
    with col6:
        wf_data_sensitivity = st.selectbox(
            "Data sensitivity level",
            options=[
                "Low — no personal or confidential data",
                "Medium — organisation-level or internal data",
                "High — personal, learner, client, or regulated data",
            ],
            key="wf_data_sensitivity",
        )

    wf_description = st.text_area(
        "Workflow description",
        placeholder=(
            "Describe the workflow steps and purpose. Use role types, not individual names. "
            "e.g. 'Tutors create weekly lesson plans for standard curriculum topics.'"
        ),
        height=100,
        key="wf_description",
    )
    wf_pain_points = st.text_area(
        "Pain points or inefficiencies",
        placeholder="e.g. First draft takes too long; structure is inconsistent between tutors.",
        height=80,
        key="wf_pain_points",
    )
    wf_ai_support_idea = st.text_area(
        "Possible AI support idea",
        placeholder=(
            "e.g. Use AI to generate a first-draft structure from a curriculum topic. "
            "Tutor reviews and approves before use."
        ),
        height=80,
        key="wf_ai_support_idea",
    )

    st.divider()
    render_section_heading("2. Suitability scoring")
    st.markdown(
        '<div class="scale-legend">'
        "<span><strong>0</strong> = Not at all</span>"
        "<span><strong>3</strong> = Partially</span>"
        "<span><strong>5</strong> = Fully</span>"
        "</div>",
        unsafe_allow_html=True,
    )

    scores = {}
    for dim in WORKFLOW_SCORING_DIMENSIONS:
        scores[dim["key"]] = st.slider(
            dim["question"],
            min_value=0,
            max_value=5,
            key=f"ws_{dim['key']}",
            help=dim["hint"],
        )

    st.divider()
    render_section_heading("3. Results")

    total = calculate_workflow_suitability_score(scores)
    level = get_workflow_suitability_level(total)
    st.session_state["workflow_score"] = total
    st.session_state["workflow_category"] = level["category"]
    if st.session_state.get("wf_name"):
        st.session_state["workflow_name"] = st.session_state["wf_name"]
    if st.session_state.get("wf_ai_support_idea"):
        st.session_state["proposed_ai_support"] = st.session_state["wf_ai_support_idea"]
    if st.session_state.get("wf_owner"):
        st.session_state["workflow_owner"] = st.session_state["wf_owner"]

    if wf_name:
        meta = []
        if wf_name:
            meta.append(f"**Workflow:** {wf_name}")
        if wf_owner:
            meta.append(f"**Owner:** {wf_owner}")
        if wf_frequency:
            meta.append(f"**Frequency:** {wf_frequency}")
        st.markdown("  ·  ".join(meta))

    col1, col2 = st.columns([1, 2])
    with col1:
        render_score_hero(total, 50, "Workflow Suitability Score")
    with col2:
        alert_fn = getattr(st, level["alert_type"], st.info)
        alert_fn(f"**{level['category']}**\n\n{level['explanation']}")
        st.info(f"💡 **Recommended next action:** {level['next_action']}")

    st.divider()
    render_section_heading("Dimension scores")

    chart_df = pd.DataFrame(
        {"Score (0–5)": [scores[d["key"]] for d in WORKFLOW_SCORING_DIMENSIONS]},
        index=[d["label"] for d in WORKFLOW_SCORING_DIMENSIONS],
    )
    st.bar_chart(chart_df)

    with st.expander("View as table"):
        st.dataframe(
            pd.DataFrame(
                [{"Dimension": d["label"], "Score": scores[d["key"]], "Max": 5}
                 for d in WORKFLOW_SCORING_DIMENSIONS]
            ),
            use_container_width=True,
            hide_index=True,
        )

    render_responsible_use()

# ── Risk Assessment ───────────────────────────────────────────────────────────

elif page == PAGES[4]:
    render_page_header(
        "Risk Assessment",
        "Rate each AI adoption risk category by likelihood and impact. Score = likelihood × impact (max 25).",
    )

    st.warning(
        "⚠️ **This tool is a prototype and does not provide legal, safeguarding, HR, "
        "compliance, medical, financial, or academic-integrity advice.** "
        "Outputs are a structured starting point for conversation — not a certified audit result."
    )
    render_safety_notice(
        "Rate risks using role-level and process-level observations only. "
        "Do not enter names, learner records, client details, safeguarding case details, "
        "confidential documents, or any personal or regulated information."
    )

    # ── Load sample button — must sit above all keyed widgets ─────────────────

    if st.button("Load BrightPath sample risk profile (lesson planning)"):
        for key, vals in BRIGHTPATH_RISK_PROFILE["scores"].items():
            st.session_state[f"risk_l_{key}"] = vals["likelihood"]
            st.session_state[f"risk_i_{key}"] = vals["impact"]
        st.rerun()

    st.divider()
    render_section_heading("1. Rate each risk category")
    st.markdown(
        '<div class="scale-legend">'
        "<span><strong>Likelihood:</strong> 1 = very unlikely · 3 = possible · 5 = very likely</span>"
        "<span><strong>Impact:</strong> 1 = negligible · 3 = significant · 5 = severe</span>"
        "</div>",
        unsafe_allow_html=True,
    )

    risk_rows = []
    for cat in RISK_CATEGORIES:
        st.markdown(f"**{cat['label']}**")
        st.caption(cat["description"])
        col1, col2 = st.columns(2)
        with col1:
            likelihood = st.slider(
                "Likelihood",
                min_value=1,
                max_value=5,
                value=1,
                key=f"risk_l_{cat['key']}",
            )
        with col2:
            impact = st.slider(
                "Impact",
                min_value=1,
                max_value=5,
                value=1,
                key=f"risk_i_{cat['key']}",
            )
        score = calculate_risk_score(likelihood, impact)
        level = get_risk_level(score)
        explanation = get_risk_level_explanation(score)
        safeguard = get_risk_safeguard(cat["key"], level)
        risk_rows.append(
            {
                "key": cat["key"],
                "label": cat["label"],
                "likelihood": likelihood,
                "impact": impact,
                "score": score,
                "level": level,
                "explanation": explanation,
                "safeguard": safeguard,
            }
        )
        st.markdown("")

    st.divider()
    render_section_heading("2. Risk summary")
    render_risk_table(risk_rows)

    high_critical = [r for r in risk_rows if r["level"] in ("High", "Critical")]
    if high_critical:
        st.markdown("")
        render_section_heading("High and Critical risks — safeguards required")
        for r in high_critical:
            alert_fn = st.error if r["level"] == "Critical" else st.warning
            alert_fn(
                f"**{r['label']} — {r['level']}** (score: {r['score']})\n\n"
                f"{r['explanation']}\n\n"
                f"**Required safeguard:** {r['safeguard']}"
            )

    st.divider()
    render_section_heading("3. Overall risk summary")

    summary = calculate_overall_risk_summary(risk_rows)
    st.session_state["highest_risk_level"] = summary["highest_level"]
    st.session_state["critical_risk_count"] = summary["counts"]["Critical"]
    st.session_state["high_risk_count"] = summary["counts"]["High"]

    # Auto-generate key_risk_notes from the current risk scores
    _high_labels = [r["label"] for r in risk_rows if r["level"] in ("High", "Critical")]
    _moderate_labels = [r["label"] for r in risk_rows if r["level"] == "Moderate"]
    _note_parts = []
    if _high_labels:
        _note_parts.append(
            f"High or Critical risks identified: {', '.join(_high_labels)}. "
            "Governance controls and safeguards required before any pilot begins."
        )
    if _moderate_labels:
        _note_parts.append(
            f"Moderate risks requiring staff guidance and human review: {', '.join(_moderate_labels)}."
        )
    if not _note_parts:
        _note_parts.append("All identified risks are Low.")
    _note_parts.append(
        "Staff must not enter learner data or safeguarding information into AI tools. "
        "Human review is required before use."
    )
    st.session_state["key_risk_notes"] = " ".join(_note_parts)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Critical", summary["counts"]["Critical"])
    with col2:
        st.metric("High", summary["counts"]["High"])
    with col3:
        st.metric("Moderate", summary["counts"]["Moderate"])
    with col4:
        st.metric("Low", summary["counts"]["Low"])
    with col5:
        st.metric("Highest level", summary["highest_level"])

    highest = summary["highest_level"]
    if highest == "Critical":
        st.error(f"**Overall recommendation:** {summary['recommendation']}")
    elif highest == "High":
        st.warning(f"**Overall recommendation:** {summary['recommendation']}")
    elif highest == "Moderate":
        st.info(f"**Overall recommendation:** {summary['recommendation']}")
    else:
        st.success(f"**Overall recommendation:** {summary['recommendation']}")

    st.divider()
    with st.expander("📋 BrightPath example — lesson planning support"):
        st.markdown(f"**Use case:** {BRIGHTPATH_RISK_PROFILE['use_case']}")
        example_rows = []
        for cat in RISK_CATEGORIES:
            vals = BRIGHTPATH_RISK_PROFILE["scores"][cat["key"]]
            l_ex, i_ex = vals["likelihood"], vals["impact"]
            s_ex = calculate_risk_score(l_ex, i_ex)
            lv_ex = get_risk_level(s_ex)
            example_rows.append(
                {"Risk category": cat["label"], "Likelihood": l_ex,
                 "Impact": i_ex, "Score": s_ex, "Level": lv_ex}
            )
        st.dataframe(
            pd.DataFrame(example_rows),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown(
            """
**Key observations from this example:**

- **Data privacy and learner data** are Low — lesson plans are topic-based; no personal data is needed.
- **Safeguarding** is High — there is a meaningful risk a tutor might inadvertently include case context in a prompt.
- **Accuracy and over-reliance** are Moderate — AI-generated lesson plans require curriculum verification before use.
- **Copyright** is Moderate — awarding body unit specifications and copyrighted materials may be referenced.
- **Overall recommendation:** Pilot only with safeguards, staff guidance, and human review.
            """
        )

    render_responsible_use()

# ── Pilot Recommendation ──────────────────────────────────────────────────────

elif page == PAGES[5]:
    render_page_header(
        "Pilot Recommendation",
        "Combines readiness, workflow suitability, and risk scores into a single evidence-based recommendation.",
    )
    render_safety_notice(
        "This page uses only the scores and category labels entered on the previous pages. "
        "No personal, learner, safeguarding, or confidential data is required or shown here."
    )

    st.divider()
    render_section_heading("1. Inputs")
    st.info(
        "Values are pulled from completed assessment pages where available. "
        "If values are missing, use the manual inputs below."
    )

    # ── Read saved scores written by each assessment page ─────────────────────

    readiness_score_saved = st.session_state.get("readiness_score")
    workflow_score_saved = st.session_state.get("workflow_score")
    highest_risk_saved = st.session_state.get("highest_risk_level")
    critical_count_saved = st.session_state.get("critical_risk_count")
    high_count_saved = st.session_state.get("high_risk_count")

    has_readiness_data = readiness_score_saved is not None
    has_workflow_data = workflow_score_saved is not None
    has_risk_data = highest_risk_saved is not None

    if has_readiness_data:
        readiness_score = readiness_score_saved
        col1, col2 = st.columns(2)
        col1.metric("Readiness score", f"{readiness_score} / 100")
        col2.metric("Category", get_readiness_category(readiness_score))
    else:
        st.caption("Readiness Assessment not yet completed — enter a score below.")
        readiness_score = st.number_input(
            "Readiness score (0–100)",
            min_value=0, max_value=100, value=0,
            key="pilot_r_manual",
        )
        st.caption(f"Category: {get_readiness_category(readiness_score)}")

    st.markdown("")

    if has_workflow_data:
        workflow_score = workflow_score_saved
        col1, col2 = st.columns(2)
        col1.metric("Workflow suitability score", f"{workflow_score} / 50")
        col2.metric("Category", get_workflow_suitability_category(workflow_score))
    else:
        st.caption("Workflow Audit not yet completed — enter a score below.")
        workflow_score = st.number_input(
            "Workflow suitability score (0–50)",
            min_value=0, max_value=50, value=0,
            key="pilot_w_manual",
        )
        st.caption(f"Category: {get_workflow_suitability_category(workflow_score)}")

    st.markdown("")

    if has_risk_data:
        highest_risk = highest_risk_saved
        has_critical = critical_count_saved > 0
        has_high = high_count_saved > 0
        col1, col2, col3 = st.columns(3)
        col1.metric("Highest risk level", highest_risk)
        col2.metric("Critical risks", critical_count_saved)
        col3.metric("High risks", high_count_saved)
    else:
        _risk_rows_fallback = [
            {
                "level": get_risk_level(
                    calculate_risk_score(
                        st.session_state.get(f"risk_l_{c['key']}", 1),
                        st.session_state.get(f"risk_i_{c['key']}", 1),
                    )
                )
            }
            for c in RISK_CATEGORIES
        ]
        _risk_fallback = calculate_overall_risk_summary(_risk_rows_fallback)
        highest_risk = _risk_fallback["highest_level"]
        has_critical = _risk_fallback["counts"]["Critical"] > 0
        has_high = _risk_fallback["counts"]["High"] > 0
        col1, col2, col3 = st.columns(3)
        col1.metric("Highest risk level", highest_risk)
        col2.metric("Critical risks", _risk_fallback["counts"]["Critical"])
        col3.metric("High risks", _risk_fallback["counts"]["High"])
        st.caption(
            "Risk Assessment not yet completed — all risks default to Low. "
            "Complete the Risk Assessment page for accurate values."
        )

    st.markdown("")

    _wf_name = st.session_state.get("workflow_name") or st.session_state.get("wf_name")
    _ai_support = st.session_state.get("proposed_ai_support") or st.session_state.get("wf_ai_support_idea")

    if _wf_name:
        workflow_name = _wf_name
        st.markdown(f"**Workflow:** {workflow_name}")
    else:
        workflow_name = st.text_input(
            "Workflow name (optional)",
            placeholder="e.g. Generic lesson planning support",
            key="pilot_wf_name",
        )

    if _ai_support:
        ai_support_idea = _ai_support
        st.markdown(f"**Proposed AI support:** {ai_support_idea}")
    else:
        ai_support_idea = st.text_area(
            "Proposed AI support idea (optional)",
            placeholder=(
                "e.g. Generate first-draft lesson plans from approved curriculum topics, "
                "reviewed by tutors before use."
            ),
            height=80,
            key="pilot_ai_idea",
        )

    st.divider()
    render_section_heading("2. Pilot Recommendation")

    recommendation = get_pilot_recommendation(
        readiness_score, workflow_score, highest_risk, has_critical, has_high
    )
    explanation = get_pilot_recommendation_explanation(
        recommendation, readiness_score, workflow_score, highest_risk
    )
    next_actions = get_pilot_next_actions(recommendation)
    safeguards = get_pilot_safeguards(recommendation)

    st.session_state["pilot_recommendation"] = recommendation
    st.session_state["pilot_explanation"] = explanation
    st.session_state["recommended_safeguards"] = format_safeguards(safeguards)
    st.session_state["next_actions"] = format_next_actions(next_actions)

    alert_type = _PILOT_ALERT_TYPES.get(recommendation, "info")
    render_recommendation_card(recommendation, explanation, alert_type)

    col1, col2 = st.columns(2)
    with col1:
        render_section_heading("Recommended next actions")
        render_next_actions(next_actions)
    with col2:
        render_section_heading("Required safeguards")
        render_safeguards(safeguards)

    st.divider()
    render_section_heading("3. Summary table")

    summary_rows = [
        {"Metric": "Readiness score", "Value": f"{readiness_score} / 100",
         "Interpretation": get_readiness_category(readiness_score)},
        {"Metric": "Workflow suitability score", "Value": f"{workflow_score} / 50",
         "Interpretation": get_workflow_suitability_category(workflow_score)},
        {"Metric": "Highest risk level", "Value": highest_risk, "Interpretation": "—"},
        {"Metric": "Critical risk present", "Value": "Yes" if has_critical else "No",
         "Interpretation": "Escalate before any AI use" if has_critical else "—"},
        {"Metric": "High risk present", "Value": "Yes" if has_high else "No",
         "Interpretation": "Governance controls required first" if has_high else "—"},
        {"Metric": "Pilot recommendation", "Value": recommendation, "Interpretation": "—"},
    ]
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

    st.divider()
    with st.expander("📋 BrightPath example — lesson planning support"):
        eg = BRIGHTPATH_PILOT_EXAMPLE
        eg_rec = get_pilot_recommendation(
            eg["readiness_score"], eg["workflow_score"],
            eg["highest_risk_level"], eg["has_critical_risk"], eg["has_high_risk"],
        )
        eg_alert = _PILOT_ALERT_TYPES.get(eg_rec, "info")
        getattr(st, eg_alert, st.info)(f"**Recommendation: {eg_rec}**")
        eg_summary = [
            {"Metric": "Workflow", "Value": eg["workflow_name"], "Interpretation": "—"},
            {"Metric": "Proposed AI support", "Value": eg["ai_support_idea"], "Interpretation": "—"},
            {"Metric": "Readiness score", "Value": f"{eg['readiness_score']} / 100",
             "Interpretation": eg["readiness_category"]},
            {"Metric": "Workflow suitability score", "Value": f"{eg['workflow_score']} / 50",
             "Interpretation": eg["workflow_category"]},
            {"Metric": "Highest risk level", "Value": eg["highest_risk_level"], "Interpretation": "—"},
            {"Metric": "Critical risk", "Value": "No", "Interpretation": "—"},
            {"Metric": "High risk", "Value": "No", "Interpretation": "—"},
            {"Metric": "Recommendation", "Value": eg_rec, "Interpretation": "—"},
        ]
        st.dataframe(pd.DataFrame(eg_summary), use_container_width=True, hide_index=True)
        st.markdown(
            """
**Why Low-risk pilot candidate?**

- Readiness score of 62 clears the 51-point threshold ("Pilot ready with safeguards").
- Workflow score of 40 clears the 36-point threshold ("Good pilot candidate").
- No critical or high risks identified — highest level is Moderate.
- The three conditions for "Low-risk pilot candidate" are all met.
- Strongest conditions (71+ readiness, 43+ workflow score) are not yet met, so "Strong pilot candidate" does not apply.
            """
        )

    render_responsible_use()

# ── Mini Report ───────────────────────────────────────────────────────────────

elif page == PAGES[6]:
    from datetime import date as _date

    render_page_header(
        "Mini Report",
        "Generate a downloadable Markdown report. Fields are pre-filled from your previous pages where available.",
    )
    render_safety_notice(
        "Include only organisation-level, role-level, and process-level information. "
        "Do not include names, learner records, safeguarding case details, "
        "confidential client data, staff HR information, or regulated data."
    )

    # ── Load sample button — must sit above all keyed widgets ─────────────────

    if st.button("Load BrightPath sample report data"):
        for key, val in BRIGHTPATH_MINI_REPORT_SAMPLE.items():
            st.session_state[f"report_{key}"] = val
        st.rerun()

    st.divider()

    # ── Compute defaults from standardised session state keys ─────────────────

    _profile = st.session_state.get("profile", {})
    _r_total = (
        st.session_state["readiness_score"]
        if st.session_state.get("readiness_score") is not None
        else sum(st.session_state.get(f"slider_{d['key']}", 0) for d in READINESS_DIMENSIONS)
    )
    _w_total = (
        st.session_state["workflow_score"]
        if st.session_state.get("workflow_score") is not None
        else sum(st.session_state.get(f"ws_{d['key']}", 0) for d in WORKFLOW_SCORING_DIMENSIONS)
    )
    _highest_risk_default = st.session_state.get("highest_risk_level") or "Low"
    _critical_default = (st.session_state.get("critical_risk_count") or 0) > 0
    _high_default = (st.session_state.get("high_risk_count") or 0) > 0

    # Pre-fill report fields from standardised keys — only if the field is blank
    _text_prefills = {
        "report_ai_use_summary": (
            st.session_state.get("ai_use_summary")
            or "Staff are beginning to use ChatGPT informally for lesson planning, emails, and report drafting."
        ),
        "report_main_concerns": (
            st.session_state.get("main_concerns")
            or "Learner data, safeguarding, staff misuse, output accuracy, and whether AI will genuinely save time."
        ),
        "report_workflow_name": (
            st.session_state.get("workflow_name")
            or st.session_state.get("wf_name")
            or "Generic lesson planning support"
        ),
        "report_workflow_owner": (
            st.session_state.get("workflow_owner")
            or st.session_state.get("wf_owner")
            or "Tutor team"
        ),
        "report_ai_support_idea": (
            st.session_state.get("proposed_ai_support")
            or st.session_state.get("wf_ai_support_idea")
            or "Generate first-draft lesson plans from approved curriculum topics, reviewed by tutors before use."
        ),
        "report_key_risk_notes": (
            st.session_state.get("key_risk_notes")
            or "AI may produce inaccurate or unsuitable lesson content if not reviewed. "
               "Staff must not enter learner data or safeguarding information."
        ),
        "report_consultant_notes": (
            st.session_state.get("consultant_notes")
            or "This is a safe first pilot candidate if data boundaries and human review are enforced."
        ),
    }
    for _report_key, _source_value in _text_prefills.items():
        if not st.session_state.get(_report_key):
            st.session_state[_report_key] = _source_value

    if not st.session_state.get("report_highest_risk"):
        st.session_state["report_highest_risk"] = _highest_risk_default
    if "report_has_critical" not in st.session_state:
        st.session_state["report_has_critical"] = _critical_default
    if "report_has_high" not in st.session_state:
        st.session_state["report_has_high"] = _high_default

    # ── Section 1: Organisation ───────────────────────────────────────────────

    render_section_heading("1. Organisation")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input(
            "Organisation name",
            value=st.session_state.get("report_org_name", _profile.get("org_name", "")),
            placeholder="e.g. BrightPath Skills Training",
            key="report_org_name",
        )
    with col2:
        st.text_input(
            "Organisation type",
            value=st.session_state.get("report_org_type", _profile.get("org_type", "")),
            placeholder="e.g. Small UK training provider",
            key="report_org_type",
        )
    st.text_input(
        "Number of staff",
        value=st.session_state.get("report_staff_count", str(_profile.get("staff_count", ""))),
        placeholder="e.g. 8",
        key="report_staff_count",
    )
    st.text_area(
        "Current AI use summary",
        value=st.session_state.get("report_ai_use_summary", ""),
        placeholder=(
            "e.g. Staff are beginning to use ChatGPT informally for lesson planning, "
            "emails, and report drafting."
        ),
        height=80,
        key="report_ai_use_summary",
    )
    st.text_area(
        "Main concerns",
        value=st.session_state.get("report_main_concerns", ""),
        placeholder=(
            "e.g. Learner data, safeguarding, staff misuse, output accuracy, "
            "and whether AI will genuinely save time."
        ),
        height=80,
        key="report_main_concerns",
    )

    st.divider()

    # ── Section 2: AI Readiness ───────────────────────────────────────────────

    render_section_heading("2. AI Readiness")
    report_readiness = st.number_input(
        "Readiness score (0–100)",
        min_value=0, max_value=100,
        value=st.session_state.get("report_readiness_score", _r_total),
        key="report_readiness_score",
    )
    st.caption(f"Category: **{get_readiness_category(report_readiness)}**")

    st.divider()

    # ── Section 3: Workflow Audit ─────────────────────────────────────────────

    render_section_heading("3. Workflow Audit")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input(
            "Workflow name",
            value=st.session_state.get("report_workflow_name", st.session_state.get("wf_name", "")),
            placeholder="e.g. Generic lesson planning support",
            key="report_workflow_name",
        )
    with col2:
        st.text_input(
            "Owner / team",
            value=st.session_state.get("report_workflow_owner", st.session_state.get("wf_owner", "")),
            placeholder="e.g. Tutor team",
            key="report_workflow_owner",
        )
    st.text_area(
        "Proposed AI support",
        value=st.session_state.get("report_ai_support_idea", st.session_state.get("wf_ai_support_idea", "")),
        placeholder=(
            "e.g. Generate first-draft lesson plans from approved curriculum topics, "
            "reviewed by tutors before use."
        ),
        height=80,
        key="report_ai_support_idea",
    )
    report_workflow = st.number_input(
        "Workflow suitability score (0–50)",
        min_value=0, max_value=50,
        value=st.session_state.get("report_workflow_score", _w_total),
        key="report_workflow_score",
    )
    st.caption(f"Category: **{get_workflow_suitability_category(report_workflow)}**")

    st.divider()

    # ── Section 4: Risk Summary ───────────────────────────────────────────────

    render_section_heading("4. Risk Summary")
    report_highest_risk = st.selectbox(
        "Highest risk level",
        options=["Low", "Moderate", "High", "Critical"],
        index=["Low", "Moderate", "High", "Critical"].index(
            st.session_state.get("report_highest_risk", _highest_risk_default)
        ),
        key="report_highest_risk",
    )
    col1, col2 = st.columns(2)
    with col1:
        report_has_critical = st.checkbox(
            "Critical risk present",
            value=st.session_state.get("report_has_critical", _critical_default),
            key="report_has_critical",
        )
    with col2:
        report_has_high = st.checkbox(
            "High risk present",
            value=st.session_state.get("report_has_high", _high_default),
            key="report_has_high",
        )
    st.text_area(
        "Key risk notes",
        value=st.session_state.get("report_key_risk_notes", ""),
        placeholder=(
            "e.g. AI may produce inaccurate content if not reviewed. "
            "Staff must not enter learner data or safeguarding information."
        ),
        height=80,
        key="report_key_risk_notes",
    )

    st.divider()

    # ── Section 5: Pilot Recommendation ──────────────────────────────────────

    render_section_heading("5. Pilot Recommendation")
    report_rec = get_pilot_recommendation(
        report_readiness, report_workflow,
        report_highest_risk, report_has_critical, report_has_high,
    )
    report_rec_explanation = get_pilot_recommendation_explanation(
        report_rec, report_readiness, report_workflow, report_highest_risk
    )

    rec_alert = _PILOT_ALERT_TYPES.get(report_rec, "info")
    render_recommendation_card(report_rec, report_rec_explanation, rec_alert)

    _default_safeguards = format_safeguards(get_pilot_safeguards(report_rec))
    _default_next_actions = format_next_actions(get_pilot_next_actions(report_rec))

    st.text_area(
        "Recommended safeguards",
        value=st.session_state.get("report_safeguards_text", _default_safeguards),
        height=140,
        key="report_safeguards_text",
        help="Edit freely — each line will appear as a list item in the report.",
    )
    st.text_area(
        "Suggested next actions",
        value=st.session_state.get("report_next_actions_text", _default_next_actions),
        height=120,
        key="report_next_actions_text",
        help="Edit freely — numbered or bulleted lines will appear as-is in the report.",
    )

    st.divider()

    # ── Section 6: Consultant Notes ───────────────────────────────────────────

    render_section_heading("6. Consultant Notes")
    st.text_area(
        "Consultant notes (optional)",
        value=st.session_state.get("report_consultant_notes", ""),
        placeholder=(
            "e.g. This is a safe first pilot candidate if data boundaries "
            "and human review are enforced."
        ),
        height=100,
        key="report_consultant_notes",
    )

    st.divider()

    # ── Report generation + download ─────────────────────────────────────────

    report_data = {
        "generated_date": _date.today().strftime("%d %B %Y"),
        "org_name": st.session_state.get("report_org_name", ""),
        "org_type": st.session_state.get("report_org_type", ""),
        "staff_count": st.session_state.get("report_staff_count", ""),
        "ai_use_summary": st.session_state.get("report_ai_use_summary", ""),
        "main_concerns": st.session_state.get("report_main_concerns", ""),
        "readiness_score": report_readiness,
        "readiness_category": get_readiness_category(report_readiness),
        "workflow_name": st.session_state.get("report_workflow_name", ""),
        "workflow_owner": st.session_state.get("report_workflow_owner", ""),
        "ai_support_idea": st.session_state.get("report_ai_support_idea", ""),
        "workflow_score": report_workflow,
        "workflow_category": get_workflow_suitability_category(report_workflow),
        "highest_risk": report_highest_risk,
        "has_critical": report_has_critical,
        "has_high": report_has_high,
        "key_risk_notes": st.session_state.get("report_key_risk_notes", ""),
        "recommendation": report_rec,
        "recommendation_explanation": report_rec_explanation,
        "safeguards_text": st.session_state.get("report_safeguards_text", _default_safeguards),
        "next_actions_text": st.session_state.get("report_next_actions_text", _default_next_actions),
        "consultant_notes": st.session_state.get("report_consultant_notes", ""),
    }

    markdown_report = generate_markdown_report(report_data)
    filename = create_report_filename(report_data["org_name"])

    with st.expander("📋 Report preview"):
        st.markdown(markdown_report)

    st.caption(
        "Markdown is useful for editing and version control. "
        "PDF is better for sharing a polished report."
    )
    pdf_filename = create_pdf_report_filename(report_data["org_name"])
    pdf_bytes = generate_pdf_report_bytes(report_data)
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label=f"⬇  Download Markdown  ({filename})",
            data=markdown_report,
            file_name=filename,
            mime="text/markdown",
            type="primary",
        )
    with col_dl2:
        st.download_button(
            label=f"⬇  Download PDF  ({pdf_filename})",
            data=pdf_bytes,
            file_name=pdf_filename,
            mime="application/pdf",
        )

    render_responsible_use()
