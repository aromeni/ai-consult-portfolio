"""Report section generators — Build 5.

Phase 1 placeholder functions are kept for backward compatibility.
Phase 6 adds full deterministic section generators for all eleven
client-facing consulting report sections.
"""

from __future__ import annotations

# ── Constants ──────────────────────────────────────────────────────────────────

_RESPONSIBLE_USE_TEXT = (
    "This report is generated from synthetic/demo audit data only. "
    "It must not be used with real client records, learner data, safeguarding case details, "
    "staff HR data, personal data, confidential data, or regulated information without "
    "appropriate governance, approvals, and responsible owners.\n\n"
    "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
    "financial, academic-integrity, or professional advice.\n\n"
    "Human review remains required before any real-world use.\n\n"
    "This report is a consulting support artefact, not a final approved organisational policy, "
    "legal opinion, compliance judgement, safeguarding assessment, HR decision, "
    "or financial recommendation."
)

_PROTOTYPE_NOTE = (
    "This report is produced by a deterministic prototype. All outputs must be reviewed, "
    "validated, and approved by a qualified consultant before client delivery."
)

_SECTION_ORDER = [
    "executive_summary",
    "organisation_context",
    "readiness_interpretation",
    "key_findings",
    "risk_summary",
    "opportunity_summary",
    "roadmap_summary",
    "training_needs",
    "governance_recommendations",
    "immediate_next_steps",
    "responsible_use",
]

_GOVERNANCE_RECOMMENDATIONS = [
    "Define approved and prohibited AI use cases in a written AI Use Policy.",
    "Clarify data boundaries — specify which data types may never be entered into AI tools.",
    "Clarify safeguarding escalation routes — AI must not be used for safeguarding decisions.",
    "Assign AI governance ownership to a named responsible owner.",
    "Require human review and sign-off for all AI-generated outputs before use.",
    "Define an incident and near-miss reporting process for AI-related concerns.",
    "Document the approved tools list and ensure staff use only approved, contracted tools.",
    "Run staff training and awareness before scaling AI use beyond the pilot.",
    "Review pilot outputs and evidence before approving further AI adoption.",
    "Obtain a Data Processing Agreement with any AI tool that may touch personal data.",
]

_NEXT_STEPS = [
    "Confirm responsible owners for AI governance and the pilot programme.",
    "Review and act on the risk register before scaling AI use.",
    "Approve the scope of the first pilot and document its boundaries.",
    "Define success measures and a review date for the pilot.",
    "Prepare and deliver staff training on responsible AI use.",
    "Confirm the approved tools list and communicate it to all staff.",
    "Run the controlled pilot with human review at every step.",
    "Review pilot outcomes against success measures before any further scaling.",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _s(val, default: str = "") -> str:
    """Return str(val) or default if val is None/empty."""
    if val is None:
        return default
    return str(val).strip() or default


def _section(
    section_id: str,
    section_title: str,
    section_purpose: str,
    content: str,
    key_points: list | None = None,
    recommendations: list | None = None,
    source_outputs_used: list | None = None,
    review_note: str | None = None,
) -> dict:
    return {
        "section_id": section_id,
        "section_title": section_title,
        "section_purpose": section_purpose,
        "content": content,
        "key_points": key_points or [],
        "recommendations": recommendations or [],
        "source_outputs_used": source_outputs_used or [],
        "review_note": review_note or "Human review required before client delivery.",
    }


# ── Phase 6: Full Section Generators ─────────────────────────────────────────

def generate_executive_summary(
    audit_data: dict,
    readiness_summary: dict | None = None,
    risk_summary: dict | None = None,
    opportunity_summary: dict | None = None,
    roadmap_summary: dict | None = None,
) -> dict:
    """Generate the executive summary section."""
    audit_data = audit_data or {}
    profile = audit_data.get("organisation_profile", {})
    org_name = _s(profile.get("organisation_name"), "the organisation")

    if readiness_summary:
        overall_score = readiness_summary.get("overall_score", "—")
        level = _s(readiness_summary.get("overall_level"), "Developing readiness")
        ranked = readiness_summary.get("ranked_categories", [])
        strongest = ranked[0]["label"] if ranked else "Workflow opportunity"
        weakest = ranked[-1]["label"] if ranked else "Risk management"
        strongest_score = int(ranked[0]["score"]) if ranked else "—"
        weakest_score = int(ranked[-1]["score"]) if ranked else "—"
    else:
        scores = audit_data.get("readiness_scores", {})
        overall_score = scores.get("overall_readiness_score", "—")
        level = "Developing readiness"
        strongest = "Workflow opportunity"
        weakest = "Risk management"
        strongest_score = scores.get("workflow_opportunity_score", "—")
        weakest_score = scores.get("risk_management_score", "—")

    if risk_summary:
        total_risks = risk_summary.get("total_risks", 0)
        critical_risks = risk_summary.get("critical_risks", 0)
        high_risks = risk_summary.get("high_risks", 0)
        if critical_risks > 0:
            risk_statement = (
                f"The audit identified {total_risks} AI risks, including "
                f"{critical_risks} critical risk(s) requiring immediate management attention."
            )
        elif high_risks > 0:
            risk_statement = (
                f"The audit identified {total_risks} AI risks, including "
                f"{high_risks} high-priority risk(s) that should be addressed before "
                f"scaling AI adoption."
            )
        else:
            risk_statement = (
                f"The audit identified {total_risks} AI risk(s) at manageable levels."
            )
    else:
        risk_count = len(audit_data.get("risk_findings", []))
        risk_statement = (
            f"The audit identified {risk_count} AI risk area(s) requiring management attention."
        )

    if opportunity_summary:
        first_pilot = _s(
            opportunity_summary.get("recommended_first_pilot_name"), "a controlled pilot"
        )
    else:
        pilots = audit_data.get("pilot_recommendations", [])
        first_pilot = (
            _s(pilots[0].get("pilot_name"), "a controlled pilot") if pilots else "a controlled pilot"
        )

    content = (
        f"{org_name} is beginning to explore informal AI use across lesson planning, emails, "
        f"and report drafting. The audit indicates that AI may offer practical value in "
        f"low-risk, text-heavy workflows, but adoption should remain controlled until governance, "
        f"staff guidance, data boundaries, and human-review expectations are clearer.\n\n"
        f"The overall AI readiness score is {overall_score}/100 ({level}). "
        f"The strongest area is {strongest} ({strongest_score}/100); "
        f"the area requiring most attention is {weakest} ({weakest_score}/100).\n\n"
        f"{risk_statement}\n\n"
        f"The recommended direction is to begin with a narrow, low-risk pilot supported by "
        f"staff training, approved-tool guidance, risk controls, and clear escalation routes. "
        f"AI should support drafting, planning, summarising, and workflow assistance, but should "
        f"not be used for safeguarding decisions, learner-specific judgement, HR matters, "
        f"legal/compliance decisions, or processing sensitive data without appropriate controls.\n\n"
        f"The recommended first pilot is {first_pilot}."
    )

    source_outputs_used = ["audit_data"]
    if readiness_summary:
        source_outputs_used.append("readiness_summary")
    if risk_summary:
        source_outputs_used.append("risk_summary")
    if opportunity_summary:
        source_outputs_used.append("opportunity_summary")
    if roadmap_summary:
        source_outputs_used.append("roadmap_summary")

    return _section(
        "executive_summary",
        "Executive Summary",
        "A concise overview of AI readiness, key findings, recommended direction, and immediate priorities.",
        content,
        key_points=[
            "AI use is currently informal and ungoverned — governance must come first.",
            f"{strongest} ({strongest_score}/100) is a relative strength that supports early pilots.",
            f"{weakest} ({weakest_score}/100) is the most significant gap and requires immediate attention.",
            "A narrow, low-risk pilot is recommended as the first controlled step.",
            "All AI-generated outputs must be reviewed by a named person before use.",
            "Safeguarding decisions, learner data, HR matters, and regulated information must remain outside AI tools.",
        ],
        recommendations=[
            "Establish AI governance and an approved-tools list before scaling.",
            f"Start with {first_pilot} as the first controlled pilot.",
            "Ensure all staff complete safeguarding and data-protection AI awareness training.",
            "Define clear data boundaries — no learner names, IDs, or sensitive records in AI tools.",
            "Require human review and sign-off for all AI-generated content before use.",
            "Review pilot outcomes before any further AI adoption.",
        ],
        source_outputs_used=source_outputs_used,
        review_note=(
            "Human review required. Consultant should adapt tone and emphasis "
            "for the specific client relationship before delivery."
        ),
    )


def generate_organisation_context_section(audit_data: dict) -> dict:
    """Generate the organisation context section."""
    audit_data = audit_data or {}
    profile = audit_data.get("organisation_profile", {})
    org_name = _s(profile.get("organisation_name"), "Unnamed organisation")
    org_type = _s(profile.get("organisation_type"), "Not specified")
    sector = _s(profile.get("sector"), "Not specified")
    country = _s(profile.get("country_context"), "Not specified")
    staff_count = profile.get("staff_count", "Not recorded")
    departments = profile.get("departments", [])
    current_ai_use = _s(profile.get("current_ai_use"), "Not described.")
    goals = profile.get("main_business_goals", [])

    dept_text = ", ".join(departments) if departments else "Not listed"
    goals_lines = "\n".join(f"- {g}" for g in goals) if goals else "Not recorded."

    content = (
        f"{org_name} is a {org_type} operating in the {sector} sector in {country}. "
        f"The organisation has approximately {staff_count} staff across the following "
        f"departments: {dept_text}.\n\n"
        f"**Current AI Use:**\n{current_ai_use}\n\n"
        f"**Main Business Goals:**\n{goals_lines}"
    )

    ai_use_short = current_ai_use[:100] + "..." if len(current_ai_use) > 100 else current_ai_use

    return _section(
        "organisation_context",
        "Organisation Context",
        "A description of the organisation, its sector, staff, departments, current AI use, and business goals.",
        content,
        key_points=[
            f"{org_name} operates in the {sector} sector with approximately {staff_count} staff.",
            f"Current AI use is informal: {ai_use_short}",
            "No formal AI governance or approved tools list is currently in place.",
        ],
        recommendations=[
            "Establish a clear baseline of current AI use through a structured staff survey.",
            "Align AI adoption goals with the organisation's main business objectives.",
        ],
        source_outputs_used=["audit_data"],
        review_note=(
            "Human review required. Verify organisational details with the client before delivery."
        ),
    )


def generate_readiness_interpretation_section(
    readiness_summary: dict | None = None,
) -> dict:
    """Generate the AI readiness interpretation section."""
    if not readiness_summary:
        return _section(
            "readiness_interpretation",
            "AI Readiness Interpretation",
            "Interpretation of the organisation's AI readiness scores across six dimensions.",
            (
                "The Readiness Summary has not yet been generated. "
                "Navigate to the Readiness Summary page to generate a full score interpretation, "
                "strengths analysis, gaps analysis, and strategic recommendations."
            ),
            key_points=["Readiness summary not yet available."],
            recommendations=[
                "Run the Readiness Summary page to generate a full interpretation."
            ],
            source_outputs_used=[],
            review_note=(
                "Generate the Readiness Summary before finalising this section."
            ),
        )

    overall_score = readiness_summary.get("overall_score", "—")
    level = _s(readiness_summary.get("overall_level"), "—")
    overall_desc = _s(readiness_summary.get("overall_description"), "")
    strategic_interp = _s(readiness_summary.get("strategic_interpretation"), "")
    ranked = readiness_summary.get("ranked_categories", [])
    gaps = readiness_summary.get("gaps", [])
    recommendations = readiness_summary.get("recommendations", [])
    strengths = readiness_summary.get("strengths", [])

    category_lines = [
        f"- **{cat['label']}:** {int(cat['score'])}/100 ({cat['level']})"
        for cat in ranked
    ]
    gap_lines = [
        f"- **{g['category']}** ({int(g['score'])}/100): {g['recommended_action']}"
        for g in gaps
    ]

    content_parts = [
        f"**Overall AI Readiness Score:** {overall_score}/100 — {level}",
        "",
        overall_desc,
        "",
        "**Category Scores:**",
        "\n".join(category_lines) if category_lines else "No category scores available.",
    ]
    if strategic_interp:
        content_parts += ["", "**Strategic Interpretation:**", strategic_interp]
    if gap_lines:
        content_parts += ["", "**Priority Gaps:**", "\n".join(gap_lines)]

    key_points = []
    if ranked:
        key_points.append(
            f"Strongest area: {ranked[0]['label']} ({int(ranked[0]['score'])}/100)."
        )
        key_points.append(
            f"Weakest area: {ranked[-1]['label']} ({int(ranked[-1]['score'])}/100)."
        )
    if strengths:
        key_points.append(f"{len(strengths)} relative strength(s) identified.")
    if gaps:
        key_points.append(f"{len(gaps)} priority gap(s) requiring attention.")

    return _section(
        "readiness_interpretation",
        "AI Readiness Interpretation",
        "Interpretation of the organisation's AI readiness scores across six dimensions.",
        "\n".join(content_parts),
        key_points=key_points,
        recommendations=list(recommendations),
        source_outputs_used=["readiness_summary"],
        review_note=(
            "Human review required. Verify score interpretations with the client before delivery."
        ),
    )


def generate_key_findings_section(
    audit_data: dict,
    readiness_summary: dict | None = None,
    risk_summary: dict | None = None,
    opportunity_summary: dict | None = None,
) -> dict:
    """Generate the key findings section from all available outputs."""
    audit_data = audit_data or {}
    workflow_count = len(audit_data.get("workflow_findings", []))
    governance_gaps = audit_data.get("governance_gaps", [])
    critical_gaps = [
        g for g in governance_gaps if _s(g.get("priority", "")).lower() == "critical"
    ]
    training_needs = audit_data.get("training_needs", [])
    high_training = [
        t for t in training_needs if _s(t.get("priority", "")).lower() == "high"
    ]

    key_points = [
        "AI use is emerging informally and requires clearer governance before further adoption.",
    ]

    if workflow_count:
        key_points.append(
            f"{workflow_count} workflow opportunity/ies identified in low-risk, "
            f"text-heavy tasks."
        )

    if readiness_summary:
        level = _s(readiness_summary.get("overall_level"), "")
        if level:
            key_points.append(
                f"Overall AI readiness is {level} — governance and training are "
                f"the main adoption constraints."
            )
    else:
        key_points.append(
            "Staff capability and safe-use guidance are important adoption constraints."
        )

    key_points.append(
        "Data protection and safeguarding boundaries require explicit controls "
        "before any pilot."
    )
    key_points.append(
        "Human review is required before AI-assisted outputs are used in any context."
    )

    if risk_summary:
        high_risks = risk_summary.get("high_risks", 0)
        critical_risks = risk_summary.get("critical_risks", 0)
        if critical_risks > 0:
            key_points.append(
                f"{critical_risks} critical risk(s) identified — immediate management action required."
            )
        elif high_risks > 0:
            key_points.append(
                f"{high_risks} high-priority risk(s) should be resolved before scaling AI adoption."
            )
    else:
        risk_count = len(audit_data.get("risk_findings", []))
        if risk_count:
            key_points.append(
                f"{risk_count} AI risk area(s) identified — risk register recommended "
                f"before scaling."
            )

    key_points.append(
        "A narrow pilot is safer than broad rollout at this stage of AI readiness."
    )

    if len(high_training) >= 2:
        key_points.append(
            f"{len(high_training)} high-priority training need(s) identified — "
            f"training must come before scale."
        )

    if critical_gaps:
        key_points.append(
            f"{len(critical_gaps)} critical governance gap(s) identified — "
            f"policy action required before piloting."
        )

    content = "The audit identified the following key findings:\n\n" + "\n".join(
        f"- {finding}" for finding in key_points
    )

    source_outputs_used = ["audit_data"]
    if readiness_summary:
        source_outputs_used.append("readiness_summary")
    if risk_summary:
        source_outputs_used.append("risk_summary")
    if opportunity_summary:
        source_outputs_used.append("opportunity_summary")

    return _section(
        "key_findings",
        "Key Findings",
        "The most important findings from the AI readiness audit and analysis.",
        content,
        key_points=key_points,
        recommendations=[
            "Address critical governance gaps before any pilot begins.",
            "Complete high-priority staff training before scaling AI use.",
            "Treat data protection and safeguarding controls as non-negotiable prerequisites.",
            "Start with a narrow, controlled pilot and review before expanding.",
        ],
        source_outputs_used=source_outputs_used,
        review_note=(
            "Human review required. Consultant should prioritise findings "
            "by organisational context."
        ),
    )


def generate_risk_summary_section(
    risk_register: list | None = None,
    risk_summary: dict | None = None,
) -> dict:
    """Generate the risk summary section."""
    if not risk_summary and not risk_register:
        return _section(
            "risk_summary",
            "Risk Summary",
            "A summary of the AI risks identified in the audit and recommended controls.",
            (
                "The Risk Register has not yet been generated. "
                "Navigate to the Risk Register page to generate a full risk assessment with "
                "likelihood, impact, risk levels, recommended controls, and owners."
            ),
            key_points=["Risk register not yet available."],
            recommendations=[
                "Run the Risk Register page to generate a full risk summary."
            ],
            source_outputs_used=[],
            review_note="Generate the Risk Register before finalising this section.",
        )

    total = risk_summary.get("total_risks", 0) if risk_summary else len(risk_register or [])
    critical = risk_summary.get("critical_risks", 0) if risk_summary else 0
    high = risk_summary.get("high_risks", 0) if risk_summary else 0
    medium = risk_summary.get("medium_risks", 0) if risk_summary else 0
    overall_position = _s(
        (risk_summary or {}).get("overall_risk_position"),
        "Risk assessment not available.",
    )
    focus_areas = (risk_summary or {}).get("recommended_focus", [])

    register = risk_register or []
    top_risk_lines = []
    for risk in register[:3]:
        ctrl = _s(risk.get("recommended_control", ""))
        ctrl_short = ctrl[:80] + "..." if len(ctrl) > 80 else ctrl
        top_risk_lines.append(
            f"- **{risk.get('risk_id', '')} — {risk.get('risk_title', '')}**: "
            f"{risk.get('risk_level', '')} (score {risk.get('risk_score', '')}/25) — "
            f"{ctrl_short}"
        )

    content_parts = [
        f"The risk assessment identified {total} AI risks: "
        f"{critical} critical, {high} high, {medium} medium.",
        "",
        f"**Overall Risk Position:** {overall_position}",
    ]
    if top_risk_lines:
        content_parts += ["", "**Top Risks:**"] + top_risk_lines
    if focus_areas:
        content_parts += ["", "**Recommended Focus Areas:**"]
        for f in focus_areas:
            content_parts.append(f"- {f}")

    key_points = [
        f"{total} AI risks identified: {critical} critical, {high} high, {medium} medium."
    ]
    if critical > 0:
        key_points.append(f"{critical} critical risk(s) require immediate management attention.")
    if high > 0:
        key_points.append(f"{high} high-priority risk(s) should be resolved before scaling.")

    source = []
    if risk_register:
        source.append("risk_register")
    if risk_summary:
        source.append("risk_summary")

    return _section(
        "risk_summary",
        "Risk Summary",
        "A summary of the AI risks identified in the audit and recommended controls.",
        "\n".join(content_parts),
        key_points=key_points,
        recommendations=[
            "Address all critical and high risks before running any AI pilot.",
            "Assign named owners to every risk in the register.",
            "Review risk controls monthly during the pilot period.",
            "Document any risk incidents or near-misses for governance evidence.",
        ],
        source_outputs_used=source,
        review_note=(
            "Human review required. Risk owners should confirm controls before client delivery."
        ),
    )


def generate_opportunity_summary_section(
    opportunity_portfolio: dict | None = None,
    opportunity_summary: dict | None = None,
) -> dict:
    """Generate the opportunity and pilot summary section."""
    if not opportunity_portfolio and not opportunity_summary:
        return _section(
            "opportunity_summary",
            "Opportunity and Pilot Summary",
            "A summary of the AI workflow opportunities and recommended pilots.",
            (
                "The Opportunity Portfolio has not yet been generated. "
                "Navigate to the Opportunity and Pilot Recommendations page to generate a full "
                "opportunity assessment with scored opportunities, pilot sequencing, "
                "success measures, and responsible-use controls."
            ),
            key_points=["Opportunity portfolio not yet available."],
            recommendations=[
                "Run the Opportunity and Pilot Recommendations page first."
            ],
            source_outputs_used=[],
            review_note=(
                "Generate the Opportunity Portfolio before finalising this section."
            ),
        )

    summary = opportunity_summary or {}
    total_opps = summary.get("total_opportunities", 0)
    total_pilots = summary.get("total_pilots", 0)
    first_pilot = _s(summary.get("recommended_first_pilot_name"), "Not identified")
    opp_position = _s(summary.get("overall_opportunity_position"), "")
    focus_areas = summary.get("recommended_focus", [])

    sequence = (opportunity_portfolio or {}).get("recommended_pilot_sequence", [])
    seq_lines = [
        f"- **{item['position']}. {item['pilot_name']}** — "
        f"{item['complexity']} complexity, {item['risk_level']} risk, "
        f"{item['suggested_timeline']}"
        for item in sequence
    ]

    content_parts = [
        f"The opportunity assessment identified {total_opps} AI workflow opportunity/ies "
        f"and {total_pilots} recommended pilot(s).",
        "",
    ]
    if opp_position:
        content_parts += [f"**Opportunity Position:** {opp_position}", ""]
    content_parts.append(f"**Recommended First Pilot:** {first_pilot}")
    if seq_lines:
        content_parts += ["", "**Recommended Pilot Sequence:**"] + seq_lines
    if focus_areas:
        content_parts += ["", "**Recommended Focus:**"]
        for f in focus_areas:
            content_parts.append(f"- {f}")

    source = []
    if opportunity_portfolio:
        source.append("opportunity_portfolio")
    if opportunity_summary:
        source.append("opportunity_summary")

    return _section(
        "opportunity_summary",
        "Opportunity and Pilot Summary",
        "A summary of the AI workflow opportunities and recommended pilots.",
        "\n".join(content_parts),
        key_points=[
            f"{total_opps} AI workflow opportunity/ies identified.",
            f"{total_pilots} pilot(s) recommended.",
            f"Recommended first pilot: {first_pilot}.",
            "Pilots are sequenced by complexity and risk — safest first.",
            "Responsible-use controls and success measures are defined for each pilot.",
        ],
        recommendations=[
            f"Start with {first_pilot} as the first controlled pilot.",
            "Define success measures and a named pilot lead before launch.",
            "Require human review at every step of the pilot.",
            "Review pilot outcomes before progressing to the next pilot.",
        ],
        source_outputs_used=source,
        review_note=(
            "Human review required. Pilot scope and success measures should be "
            "agreed with the client."
        ),
    )


def generate_roadmap_summary_section(
    implementation_roadmap: dict | None = None,
    roadmap_summary: dict | None = None,
) -> dict:
    """Generate the 30/60/90-day roadmap summary section."""
    if not implementation_roadmap and not roadmap_summary:
        return _section(
            "roadmap_summary",
            "30/60/90-Day Roadmap Summary",
            "A summary of the staged AI implementation roadmap.",
            (
                "The Implementation Roadmap has not yet been generated. "
                "Navigate to the Roadmap page to generate a full 30/60/90-day implementation "
                "plan with actions, owners, success measures, dependencies, and "
                "responsible-use controls."
            ),
            key_points=["Implementation roadmap not yet available."],
            recommendations=["Run the Roadmap page to generate a full roadmap summary."],
            source_outputs_used=[],
            review_note="Generate the Implementation Roadmap before finalising this section.",
        )

    summary = roadmap_summary or {}
    total_actions = summary.get("total_actions", 0)
    day_30 = summary.get("day_30_actions", 0)
    day_60 = summary.get("day_60_actions", 0)
    day_90 = summary.get("day_90_actions", 0)
    high_priority = summary.get("high_priority_actions", 0)
    first_pilot = _s(summary.get("recommended_first_pilot"), "—")
    overall_position = _s(summary.get("overall_roadmap_position"), "")
    key_deps = summary.get("key_dependencies", [])
    key_risks = summary.get("key_risks_to_manage", [])

    content_parts = [
        f"The implementation roadmap covers {total_actions} actions across three phases:",
        f"- **First 30 days** (Foundation and risk control): {day_30} actions",
        f"- **Days 31–60** (Pilot preparation and controlled delivery): {day_60} actions",
        f"- **Days 61–90** (Review, refine, and scale decision): {day_90} actions",
        "",
        f"**High-priority actions:** {high_priority}",
        f"**Recommended first pilot:** {first_pilot}",
    ]
    if overall_position:
        content_parts += ["", f"**Roadmap Position:** {overall_position}"]
    if key_deps:
        content_parts += ["", "**Key Dependencies:**"]
        for d in key_deps[:3]:
            content_parts.append(f"- {d}")
    if key_risks:
        content_parts += ["", "**Key Risks to Manage:**"]
        for r in key_risks[:3]:
            content_parts.append(f"- {r}")

    source = []
    if implementation_roadmap:
        source.append("implementation_roadmap")
    if roadmap_summary:
        source.append("roadmap_summary")

    return _section(
        "roadmap_summary",
        "30/60/90-Day Roadmap Summary",
        "A summary of the staged AI implementation roadmap.",
        "\n".join(content_parts),
        key_points=[
            f"{total_actions} actions across three phases.",
            f"First 30 days: establish governance foundations ({day_30} actions).",
            f"Days 31–60: prepare and run the first pilot ({day_60} actions).",
            f"Days 61–90: review evidence and decide on next steps ({day_90} actions).",
            f"{high_priority} high-priority actions across all phases.",
        ],
        recommendations=[
            "Prioritise Day 1–30 governance and training actions before launching the pilot.",
            "Assign named owners to every roadmap action.",
            "Use the Day 61–90 review to make a stop/continue/scale decision based on evidence.",
            "Do not scale before pilot evidence is reviewed and approved.",
        ],
        source_outputs_used=source,
        review_note=(
            "Human review required. Confirm timelines and owners with the client."
        ),
    )


def generate_training_needs_section(audit_data: dict) -> dict:
    """Generate the training and capability needs section."""
    audit_data = audit_data or {}
    training_needs = audit_data.get("training_needs", [])

    if not training_needs:
        return _section(
            "training_needs",
            "Training and Capability Needs",
            "Training topics, audiences, priorities, and recommended formats identified in the audit.",
            "No training needs recorded in the audit data.",
            source_outputs_used=["audit_data"],
        )

    lines = []
    for t in training_needs:
        topic = _s(t.get("topic"), "Unnamed topic")
        audience = _s(t.get("audience"), "All staff")
        priority = _s(t.get("priority"), "Medium")
        reason = _s(t.get("reason"), "")
        fmt = _s(t.get("recommended_format"), "")
        lines.append(
            f"- **{topic}** — Audience: {audience} · Priority: {priority}\n"
            f"  Reason: {reason}\n"
            f"  Format: {fmt}"
        )

    high_count = sum(
        1 for t in training_needs if _s(t.get("priority", "")).lower() == "high"
    )

    content = (
        "The following training topics were identified in the audit:\n\n"
        + "\n".join(lines)
        + "\n\nTraining recommendations can later be turned into workshop materials "
        "using Build 4: AI Staff Training and Workshop Generator."
    )

    return _section(
        "training_needs",
        "Training and Capability Needs",
        "Training topics, audiences, priorities, and recommended formats identified in the audit.",
        content,
        key_points=[
            f"{len(training_needs)} training topic(s) identified.",
            f"{high_count} high-priority training need(s) should be completed before scaling AI use.",
            "Training must cover responsible use, data protection, and safeguarding AI boundaries.",
        ],
        recommendations=[
            "Deliver high-priority training before any AI pilot launches.",
            "Include safeguarding and data-protection AI modules for all staff.",
            "Use Build 4: AI Staff Training and Workshop Generator to create workshop materials.",
            "Track training completion and retain evidence for governance and compliance.",
        ],
        source_outputs_used=["audit_data"],
        review_note="Human review required. Confirm training priorities with the client.",
    )


def generate_governance_recommendations_section(
    audit_data: dict,
    risk_summary: dict | None = None,
    readiness_summary: dict | None = None,
) -> dict:
    """Generate the governance recommendations section."""
    audit_data = audit_data or {}
    governance_gaps = audit_data.get("governance_gaps", [])
    critical_gaps = [
        g for g in governance_gaps if _s(g.get("priority", "")).lower() == "critical"
    ]
    high_gaps = [
        g for g in governance_gaps if _s(g.get("priority", "")).lower() == "high"
    ]

    gap_lines = [
        f"- **{_s(g.get('gap_title'), 'Gap')}** ({_s(g.get('priority'), '')}): "
        f"{_s(g.get('recommended_action'), '')}"
        for g in governance_gaps
    ]

    content_parts = []
    if gap_lines:
        content_parts += [
            f"The audit identified {len(governance_gaps)} governance gap(s) "
            f"({len(critical_gaps)} critical, {len(high_gaps)} high):",
            "",
        ] + gap_lines + [""]

    content_parts.append("**Governance Recommendations:**")
    for i, rec in enumerate(_GOVERNANCE_RECOMMENDATIONS, 1):
        content_parts.append(f"{i}. {rec}")

    source = ["audit_data"]
    if risk_summary:
        source.append("risk_summary")
    if readiness_summary:
        source.append("readiness_summary")

    return _section(
        "governance_recommendations",
        "Governance Recommendations",
        "Governance actions required before and during AI adoption.",
        "\n".join(content_parts),
        key_points=[
            f"{len(governance_gaps)} governance gap(s) identified in the audit.",
            f"{len(critical_gaps)} critical gap(s) require immediate action.",
            "AI governance must be established before scaling beyond a controlled pilot.",
            "Data boundaries and safeguarding restrictions must be documented in policy.",
        ],
        recommendations=list(_GOVERNANCE_RECOMMENDATIONS),
        source_outputs_used=source,
        review_note=(
            "Human review required. Governance recommendations should be validated by "
            "a responsible owner and legal/compliance advisor before adoption."
        ),
    )


def generate_immediate_next_steps_section(
    audit_data: dict,
    readiness_summary: dict | None = None,
    risk_summary: dict | None = None,
    opportunity_summary: dict | None = None,
    roadmap_summary: dict | None = None,
) -> dict:
    """Generate the immediate next steps section."""
    audit_data = audit_data or {}

    if opportunity_summary:
        first_pilot = _s(
            opportunity_summary.get("recommended_first_pilot_name"), "a controlled pilot"
        )
    else:
        pilots = audit_data.get("pilot_recommendations", [])
        first_pilot = (
            _s(pilots[0].get("pilot_name"), "a controlled pilot") if pilots else "a controlled pilot"
        )

    steps = list(_NEXT_STEPS)
    steps[6] = (
        f"Run the controlled pilot ({first_pilot}) with human review at every step."
    )

    content = "The following immediate next steps are recommended:\n\n" + "\n".join(
        f"{i}. {step}" for i, step in enumerate(steps, 1)
    )

    source = ["audit_data"]
    if readiness_summary:
        source.append("readiness_summary")
    if risk_summary:
        source.append("risk_summary")
    if opportunity_summary:
        source.append("opportunity_summary")
    if roadmap_summary:
        source.append("roadmap_summary")

    return _section(
        "immediate_next_steps",
        "Immediate Next Steps",
        "Practical short-term actions to begin responsible AI adoption.",
        content,
        key_points=[
            "Governance owners must be confirmed before any pilot begins.",
            "Risk register actions must be completed before scaling.",
            f"The recommended first pilot is {first_pilot}.",
            "Staff training must come before pilot launch.",
            "Pilot outcomes must be reviewed before any further scaling.",
        ],
        recommendations=steps,
        source_outputs_used=source,
        review_note=(
            "Human review required. Timelines and owners should be agreed with the client "
            "before finalising next steps."
        ),
    )


def generate_responsible_use_section() -> dict:
    """Generate the responsible-use boundaries section."""
    return _section(
        "responsible_use",
        "Responsible-Use Boundaries",
        "Boundaries and limitations on the use of this report and its outputs.",
        _RESPONSIBLE_USE_TEXT,
        key_points=[
            "This report uses synthetic/demo audit data only.",
            "No real client, learner, HR, safeguarding, or personal data has been used.",
            "Human review is required before any real-world use.",
            "This report does not constitute legal, compliance, HR, or professional advice.",
            "Production use requires governance, DPIA, security, and responsible-owner approval.",
        ],
        recommendations=[
            "Do not use this report with real client records without appropriate governance.",
            "Obtain legal and compliance review before implementing any recommendations.",
            "Ensure a named responsible owner approves all AI adoption decisions.",
            "Complete a DPIA before processing any personal data through AI tools.",
        ],
        source_outputs_used=[],
        review_note=_PROTOTYPE_NOTE,
    )


def generate_all_report_sections(
    audit_data: dict,
    readiness_summary: dict | None = None,
    risk_register: list | None = None,
    risk_summary: dict | None = None,
    opportunity_portfolio: dict | None = None,
    opportunity_summary: dict | None = None,
    implementation_roadmap: dict | None = None,
    roadmap_summary: dict | None = None,
) -> dict:
    """Generate all report sections and return the full report sections dict."""
    audit_data = audit_data or {}
    profile = audit_data.get("organisation_profile", {})
    org_name = _s(profile.get("organisation_name"), "Unnamed organisation")

    sections = {
        "executive_summary": generate_executive_summary(
            audit_data, readiness_summary, risk_summary, opportunity_summary, roadmap_summary
        ),
        "organisation_context": generate_organisation_context_section(audit_data),
        "readiness_interpretation": generate_readiness_interpretation_section(readiness_summary),
        "key_findings": generate_key_findings_section(
            audit_data, readiness_summary, risk_summary, opportunity_summary
        ),
        "risk_summary": generate_risk_summary_section(risk_register, risk_summary),
        "opportunity_summary": generate_opportunity_summary_section(
            opportunity_portfolio, opportunity_summary
        ),
        "roadmap_summary": generate_roadmap_summary_section(
            implementation_roadmap, roadmap_summary
        ),
        "training_needs": generate_training_needs_section(audit_data),
        "governance_recommendations": generate_governance_recommendations_section(
            audit_data, risk_summary, readiness_summary
        ),
        "immediate_next_steps": generate_immediate_next_steps_section(
            audit_data, readiness_summary, risk_summary, opportunity_summary, roadmap_summary
        ),
        "responsible_use": generate_responsible_use_section(),
    }

    return {
        "organisation_name": org_name,
        "report_title": "AI Readiness and Responsible AI Adoption Report",
        "sections": sections,
        "section_order": list(_SECTION_ORDER),
        "source_outputs_available": {
            "audit_data": bool(audit_data),
            "readiness_summary": readiness_summary is not None,
            "risk_register": risk_register is not None,
            "opportunity_portfolio": opportunity_portfolio is not None,
            "implementation_roadmap": implementation_roadmap is not None,
        },
        "prototype_note": _PROTOTYPE_NOTE,
    }


def summarise_report_sections(report_sections: dict) -> dict:
    """Summarise the report sections into a compact metrics dict."""
    report_sections = report_sections or {}
    sections = report_sections.get("sections", {})
    total = len(sections)
    with_content = sum(1 for s in sections.values() if _s(s.get("content")))

    used: set = set()
    for s in sections.values():
        used.update(s.get("source_outputs_used", []))

    source_available = report_sections.get("source_outputs_available", {})
    missing = [k for k, v in source_available.items() if not v]

    if not missing:
        readiness = (
            "The report sections are ready to be assembled into the full client report, "
            "subject to human review and responsible-owner approval."
        )
    else:
        readiness = (
            "The report sections can be generated, but the final report will be stronger "
            "after completing the missing analysis pages."
        )

    return {
        "total_sections": total,
        "sections_with_content": with_content,
        "source_outputs_used": sorted(used),
        "missing_source_outputs": missing,
        "review_required": True,
        "overall_report_readiness": readiness,
    }


def format_report_sections_as_markdown(report_sections: dict) -> str:
    """Format the full report sections dict as a Markdown document."""
    report_sections = report_sections or {}
    org_name = _s(report_sections.get("organisation_name"), "Unnamed organisation")
    report_title = _s(report_sections.get("report_title"), "AI Consulting Report")
    sections = report_sections.get("sections", {})
    section_order = report_sections.get("section_order", list(_SECTION_ORDER))
    source_available = report_sections.get("source_outputs_available", {})
    prototype_note = _s(report_sections.get("prototype_note"), _PROTOTYPE_NOTE)

    _MD_HEADINGS = {
        "executive_summary": "## Executive Summary",
        "organisation_context": "## Organisation Context",
        "readiness_interpretation": "## AI Readiness Interpretation",
        "key_findings": "## Key Findings",
        "risk_summary": "## Risk Summary",
        "opportunity_summary": "## Opportunity and Pilot Summary",
        "roadmap_summary": "## 30/60/90-Day Roadmap Summary",
        "training_needs": "## Training and Capability Needs",
        "governance_recommendations": "## Governance Recommendations",
        "immediate_next_steps": "## Immediate Next Steps",
        "responsible_use": "## Responsible-Use Boundaries",
    }

    lines = [
        "# AI Consulting Report Sections",
        "",
        f"**{report_title}**",
        f"**Organisation:** {org_name}",
        "",
        "---",
        "",
        "## Report Overview",
        "",
        (
            f"This document contains the generated consulting report sections for {org_name}. "
            "Each section is generated from synthetic audit data and optional analysis outputs. "
            "All sections require human review and responsible-owner approval before client delivery."
        ),
        "",
        "---",
        "",
        "## Source Outputs Used",
        "",
    ]

    for key, available in source_available.items():
        status = "Available" if available else "Not yet generated"
        lines.append(f"- **{key.replace('_', ' ').title()}:** {status}")

    lines += ["", "---", ""]

    for section_id in section_order:
        section = sections.get(section_id)
        if not section:
            continue

        heading = _MD_HEADINGS.get(
            section_id, f"## {section.get('section_title', section_id)}"
        )
        lines.append(heading)
        lines.append("")

        purpose = _s(section.get("section_purpose"), "")
        if purpose:
            lines += [f"*{purpose}*", ""]

        content = _s(section.get("content"), "")
        if content:
            lines += [content, ""]

        key_points = section.get("key_points", [])
        if key_points:
            lines.append("**Key Points:**")
            for kp in key_points:
                lines.append(f"- {kp}")
            lines.append("")

        recommendations = section.get("recommendations", [])
        if recommendations:
            lines.append("**Recommendations:**")
            for rec in recommendations:
                lines.append(f"- {rec}")
            lines.append("")

        review_note = _s(section.get("review_note"), "")
        if review_note:
            lines += [f"*Review note: {review_note}*", ""]

        lines += ["---", ""]

    lines += [
        f"*{prototype_note}*",
        "",
        "*Build 5 · AI Consulting Report Generator · BrightPath ChatGPT Mastery Project*",
        "*All scenarios are synthetic. Outputs require human review before real-world use.*",
    ]

    return "\n".join(lines)


# ── Phase 1 Placeholder Functions (kept for backward compatibility) ────────────

def generate_executive_summary_placeholder(audit_data: dict) -> str:
    """Return a placeholder executive summary section."""
    profile = (audit_data or {}).get("organisation_profile", {})
    scores = (audit_data or {}).get("readiness_scores", {})
    org_name = _s(profile.get("organisation_name"), "the organisation")
    overall = scores.get("overall_readiness_score", "—")
    risk_count = len((audit_data or {}).get("risk_findings", []))
    pilot_count = len((audit_data or {}).get("pilot_recommendations", []))

    return (
        f"## Executive Summary\n\n"
        f"This report presents the findings of an AI readiness audit for {org_name}. "
        f"The organisation received an overall AI readiness score of {overall}/100. "
        f"The audit identified {risk_count} risk areas and {pilot_count} recommended pilot "
        f"opportunities. Immediate action is required on governance and data protection "
        f"before AI adoption proceeds.\n\n"
        f"*[Full executive summary will be generated in a later phase.]*"
    )


def generate_context_section_placeholder(audit_data: dict) -> str:
    """Return a placeholder organisation context section."""
    profile = (audit_data or {}).get("organisation_profile", {})
    org_name = _s(profile.get("organisation_name"), "Unknown Organisation")
    org_type = _s(profile.get("organisation_type"))
    sector = _s(profile.get("sector"))
    staff_count = profile.get("staff_count", "—")
    current_ai_use = _s(profile.get("current_ai_use"), "Not described.")

    lines = ["## Organisation Context", "", f"**Organisation:** {org_name}"]
    if org_type:
        lines.append(f"**Type:** {org_type}")
    if sector:
        lines.append(f"**Sector:** {sector}")
    lines += [
        f"**Staff count:** {staff_count}",
        "",
        "**Current AI use:**",
        current_ai_use,
        "",
        "*[Full context section will be generated in a later phase.]*",
    ]
    return "\n".join(lines)


def generate_risk_section_placeholder(audit_data: dict) -> str:
    """Return a placeholder key risks section."""
    risk_findings = (audit_data or {}).get("risk_findings", [])
    if not risk_findings:
        return (
            "## Key Risks\n\nNo risk findings loaded.\n\n"
            "*[Full risk section will be generated in a later phase.]*"
        )

    lines = ["## Key Risks", ""]
    for rf in risk_findings:
        title = _s(rf.get("risk_title"), "Unnamed Risk")
        level = _s(rf.get("risk_level"), "Unknown")
        category = _s(rf.get("risk_category"))
        suffix = f" ({category})" if category else ""
        lines.append(f"- **{title}** — Level: {level}{suffix}")

    lines += [
        "",
        "*[Full risk section with detailed analysis will be generated in a later phase.]*",
    ]
    return "\n".join(lines)


def generate_opportunity_section_placeholder(audit_data: dict) -> str:
    """Return a placeholder AI opportunities section."""
    workflow_findings = (audit_data or {}).get("workflow_findings", [])
    pilots = (audit_data or {}).get("pilot_recommendations", [])

    lines = ["## Recommended AI Opportunities", ""]

    if workflow_findings:
        lines.append("**Workflow Opportunities:**")
        for wf in workflow_findings:
            name = _s(wf.get("workflow_name"), "Unnamed Workflow")
            opp = _s(wf.get("ai_opportunity"))
            if opp:
                lines.append(f"- **{name}:** {opp}")
        lines.append("")

    if pilots:
        lines.append("**Recommended Pilots:**")
        for p in pilots:
            name = _s(p.get("pilot_name"), "Unnamed Pilot")
            timeline = _s(p.get("suggested_timeline"))
            lines.append(f"- **{name}**" + (f" — {timeline}" if timeline else ""))
        lines.append("")

    lines.append("*[Full opportunity section will be generated in a later phase.]*")
    return "\n".join(lines)


def generate_recommendations_section_placeholder(audit_data: dict) -> str:
    """Return a placeholder recommendations section."""
    governance_gaps = (audit_data or {}).get("governance_gaps", [])
    training_needs = (audit_data or {}).get("training_needs", [])

    lines = ["## Recommendations", ""]

    critical_gaps = [
        g for g in governance_gaps
        if _s(g.get("priority", "")).lower() == "critical"
    ]
    if critical_gaps:
        lines.append("**Critical Actions (Immediate):**")
        for g in critical_gaps:
            title = _s(g.get("gap_title"))
            action = _s(g.get("recommended_action"))
            lines.append(f"- **{title}:** {action}")
        lines.append("")

    high_training = [
        t for t in training_needs
        if _s(t.get("priority", "")).lower() == "high"
    ]
    if high_training:
        lines.append("**High-Priority Training:**")
        for t in high_training:
            topic = _s(t.get("topic"))
            audience = _s(t.get("audience"))
            lines.append(f"- {topic} — {audience}")
        lines.append("")

    lines.append("*[Full recommendations section will be generated in a later phase.]*")
    return "\n".join(lines)
