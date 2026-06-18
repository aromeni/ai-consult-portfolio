"""Client report builder — Build 5 Phase 7.

Assembles all generated Build 5 outputs into a complete client-facing
AI consulting report in Markdown format.
"""

from datetime import date

# ── Constants ──────────────────────────────────────────────────────────────────

_REPORT_TITLE = "AI Readiness and Responsible AI Adoption Report"

_RESPONSIBLE_USE_TEXT = (
    "This client report is generated from synthetic/demo audit data only. "
    "It must not be used with real client records, learner data, safeguarding case details, "
    "staff HR data, personal data, confidential data, or regulated information without "
    "appropriate governance, approvals, and responsible owners.\n\n"
    "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
    "financial, academic-integrity, or professional advice.\n\n"
    "Human review remains required before any real-world use.\n\n"
    "This report is a consulting support artefact, not a final approved organisational policy, "
    "legal opinion, compliance judgement, safeguarding assessment, HR decision, "
    "financial recommendation, or certified professional advice."
)

_PROTOTYPE_NOTE = (
    "This report is produced by a deterministic prototype. All outputs must be reviewed, "
    "validated, and approved by a qualified consultant before client delivery."
)

_PROTOTYPE_LIMITATIONS = [
    "Synthetic/demo audit data only — no real client data is used.",
    "Deterministic and template-based generation — no external AI or LLM API calls.",
    "No real client validation — outputs are based on the BrightPath demo scenario.",
    "No legal, compliance, safeguarding, HR, or financial approval.",
    "Not production-deployed — local prototype only.",
    "No authentication or audit logging.",
    "No persistent storage — outputs are lost on app restart.",
    "Outputs require responsible human review before any real-world use.",
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

_RECOMMENDED_KEYS = [
    "readiness_summary",
    "risk_register",
    "risk_register_summary",
    "opportunity_portfolio",
    "opportunity_summary",
    "implementation_roadmap",
    "implementation_roadmap_summary",
    "report_sections",
]

# ── Helpers ────────────────────────────────────────────────────────────────────


def _s(val, default: str = "") -> str:
    if val is None:
        return default
    return str(val).strip() or default


def _section_content(report_sections, section_id: str) -> dict:
    """Return a section dict from report_sections, or empty dict."""
    if not report_sections:
        return {}
    sections = report_sections.get("sections") or {}
    return sections.get(section_id) or {}


# ── Section list helpers ───────────────────────────────────────────────────────


def get_client_report_required_sections() -> list:
    """Return section IDs that are always included."""
    return [
        "executive_summary",
        "organisation_context",
        "responsible_use",
        "prototype_limitations",
    ]


def get_client_report_optional_sections() -> list:
    """Return section IDs that are included when data is available."""
    return [
        "readiness_summary",
        "key_findings",
        "risk_register_summary",
        "opportunity_summary",
        "roadmap_summary",
        "training_needs",
        "governance_recommendations",
        "next_steps",
        "appendices",
    ]


# ── Readiness check ────────────────────────────────────────────────────────────


def check_client_report_readiness(session_state: dict) -> dict:
    """Inspect session state and return a readiness report."""
    ss = session_state or {}
    has_audit = bool(ss.get("audit_data"))
    available = [k for k in _RECOMMENDED_KEYS if ss.get(k) is not None]
    missing = [k for k in _RECOMMENDED_KEYS if ss.get(k) is None]

    steps = []
    if not has_audit:
        steps = [
            "Go to Audit Data.",
            "Load the BrightPath demo audit data.",
            "Return to Client Report.",
        ]
    else:
        if "readiness_summary" in missing:
            steps.append("Run the Readiness Summary page to enrich the report.")
        if "risk_register" in missing:
            steps.append("Run the Risk Register page to include risk data.")
        if "opportunity_portfolio" in missing:
            steps.append("Run the Opportunity and Pilot Recommendations page.")
        if "implementation_roadmap" in missing:
            steps.append("Run the Roadmap page to include the 30/60/90-day plan.")
        if "report_sections" in missing:
            steps.append("Run the Report Sections page to include structured sections.")

    return {
        "is_ready": has_audit,
        "available_sections": available,
        "missing_sections": missing,
        "recommended_next_steps": steps,
    }


# ── Build report data ──────────────────────────────────────────────────────────


def build_client_report_data_from_session_state(session_state: dict) -> dict:
    """Collect all session state outputs into a single report data dict."""
    ss = session_state or {}
    audit = ss.get("audit_data") or {}
    org_name = (
        audit.get("organisation_profile", {}).get("organisation_name")
        or "Unnamed organisation"
    )

    return {
        "report_title": _REPORT_TITLE,
        "organisation_name": org_name,
        "generated_date": date.today().isoformat(),
        "audit_data": audit,
        "readiness_summary": ss.get("readiness_summary"),
        "risk_register": ss.get("risk_register"),
        "risk_register_summary": ss.get("risk_register_summary"),
        "opportunity_portfolio": ss.get("opportunity_portfolio"),
        "opportunity_summary": ss.get("opportunity_summary"),
        "implementation_roadmap": ss.get("implementation_roadmap"),
        "implementation_roadmap_summary": ss.get("implementation_roadmap_summary"),
        "report_sections": ss.get("report_sections"),
        "source_outputs_available": {
            "audit_data": bool(audit),
            "readiness_summary": ss.get("readiness_summary") is not None,
            "risk_register": ss.get("risk_register") is not None,
            "opportunity_portfolio": ss.get("opportunity_portfolio") is not None,
            "implementation_roadmap": ss.get("implementation_roadmap") is not None,
            "report_sections": ss.get("report_sections") is not None,
        },
        "responsible_use_note": _RESPONSIBLE_USE_TEXT,
        "prototype_note": _PROTOTYPE_NOTE,
    }


# ── Section generators ─────────────────────────────────────────────────────────


def generate_report_cover_section(report_data: dict) -> str:
    """Return Markdown for the report cover page."""
    rd = report_data or {}
    title = rd.get("report_title") or _REPORT_TITLE
    org = rd.get("organisation_name") or "Unnamed organisation"
    audit = rd.get("audit_data") or {}
    profile = audit.get("organisation_profile") or {}
    org_type = _s(profile.get("organisation_type"))
    sector = _s(profile.get("sector"))
    staff = profile.get("staff_count")
    country = _s(profile.get("country_context"))
    date_str = rd.get("generated_date") or date.today().isoformat()

    lines = [
        f"**Report Title:** {title}",
        f"**Organisation:** {org}",
    ]
    if org_type:
        lines.append(f"**Organisation Type:** {org_type}")
    if sector:
        lines.append(f"**Sector:** {sector}")
    if staff is not None:
        lines.append(f"**Staff Count:** {staff}")
    if country:
        lines.append(f"**Country Context:** {country}")
    lines.append(f"**Generated Date:** {date_str}")
    lines.append(
        "**Status:** Production-style AI consulting report prototype. "
        "Not a production consulting, legal, safeguarding, HR, compliance, "
        "financial, or professional advisory system."
    )
    return "\n\n".join(lines)


def generate_report_table_of_contents(
    report_data: dict,
    include_sections: dict | None = None,
) -> str:
    """Return Markdown for the table of contents."""
    inc = include_sections or {}

    all_sections = [
        ("1", "Executive Summary", True),
        ("2", "Organisation Context", True),
        ("3", "AI Readiness Summary", inc.get("readiness_summary", True)),
        ("4", "Key Findings", inc.get("key_findings", True)),
        ("5", "AI Risk Register Summary", inc.get("risk_register_summary", True)),
        ("6", "AI Opportunity and Pilot Recommendations", inc.get("opportunity_summary", True)),
        ("7", "30/60/90-Day Implementation Roadmap", inc.get("roadmap_summary", True)),
        ("8", "Training and Capability Needs", inc.get("training_needs", True)),
        ("9", "Governance Recommendations", inc.get("governance_recommendations", True)),
        ("10", "Immediate Next Steps", inc.get("next_steps", True)),
        ("11", "Responsible-Use Boundaries", True),
        ("12", "Prototype Limitations", True),
        ("13", "Appendices", inc.get("appendices", True)),
    ]

    return "\n".join(
        f"{num}. {title}" for num, title, included in all_sections if included
    )


def generate_report_executive_summary_section(report_data: dict) -> str:
    """Return Markdown for the executive summary."""
    rd = report_data or {}
    org = rd.get("organisation_name") or "Unnamed organisation"
    rs = rd.get("report_sections")
    sec = _section_content(rs, "executive_summary")

    if sec.get("content"):
        lines = [sec["content"]]
        key_points = sec.get("key_points") or []
        if key_points:
            lines.append("\n**Key Points:**")
            lines.extend(f"- {kp}" for kp in key_points)
        recs = sec.get("recommendations") or []
        if recs:
            lines.append("\n**Recommendations:**")
            lines.extend(f"- {r}" for r in recs)
        return "\n".join(lines)

    # Fallback from audit data
    audit = rd.get("audit_data") or {}
    profile = audit.get("organisation_profile") or {}
    scores = audit.get("readiness_scores") or {}
    overall = scores.get("overall_readiness_score", "")
    risk_count = len(audit.get("risk_findings") or [])
    pilot_count = len(audit.get("pilot_recommendations") or [])

    readiness_text = ""
    if overall:
        readiness_text = (
            f" The overall AI readiness score is {overall}/100."
        )

    return (
        f"{org} is beginning to explore AI adoption across its operations. "
        f"This report summarises the findings from an AI readiness audit and provides "
        f"structured recommendations for responsible AI adoption.{readiness_text} "
        f"The audit identified {risk_count} AI risk(s) and {pilot_count} pilot recommendation(s). "
        f"The recommended direction is to strengthen governance and data controls before "
        f"running structured pilots in low-risk workflows.\n\n"
        f"**Recommendation:** All outputs require human review and responsible-owner approval "
        f"before any real-world implementation."
    )


def generate_report_context_section(report_data: dict) -> str:
    """Return Markdown for the organisation context section."""
    rd = report_data or {}
    audit = rd.get("audit_data") or {}
    profile = audit.get("organisation_profile") or {}
    rs = rd.get("report_sections")
    sec = _section_content(rs, "organisation_context")

    if sec.get("content"):
        return sec["content"]

    # Build from audit profile
    org = _s(profile.get("organisation_name"), "Unnamed organisation")
    org_type = _s(profile.get("organisation_type"))
    sector = _s(profile.get("sector"))
    staff = profile.get("staff_count")
    country = _s(profile.get("country_context"))
    depts = profile.get("departments") or []
    goals = profile.get("main_business_goals") or []
    current_ai = _s(profile.get("current_ai_use"))

    lines = []
    if org_type and sector:
        lines.append(f"{org} is a {org_type} in the {sector} sector.")
    elif org_type:
        lines.append(f"{org} is a {org_type}.")
    if staff:
        lines.append(f"The organisation employs {staff} staff.")
    if country:
        lines.append(f"Operating context: {country}.")
    if depts:
        lines.append("**Departments:** " + ", ".join(depts) + ".")
    if current_ai:
        lines.append(f"**Current AI use:** {current_ai}")
    if goals:
        lines.append("**Main business goals:**")
        lines.extend(f"- {g}" for g in goals)

    return "\n\n".join(lines) if lines else f"Organisation profile for {org}."


def generate_report_readiness_section(report_data: dict) -> str:
    """Return Markdown for the AI readiness summary section."""
    rd = report_data or {}
    rs = rd.get("report_sections")
    sec = _section_content(rs, "readiness_interpretation")

    if sec.get("content"):
        lines = [sec["content"]]
        kps = sec.get("key_points") or []
        if kps:
            lines.append("\n**Key Points:**")
            lines.extend(f"- {kp}" for kp in kps)
        recs = sec.get("recommendations") or []
        if recs:
            lines.append("\n**Recommendations:**")
            lines.extend(f"- {r}" for r in recs)
        return "\n".join(lines)

    readiness = rd.get("readiness_summary")
    if not readiness:
        return (
            "No Readiness Summary is available yet. "
            "Run the Readiness Summary page to include this section."
        )

    overall = readiness.get("overall_score", "")
    level = readiness.get("overall_level", "")
    description = readiness.get("overall_description", "")
    interp = readiness.get("strategic_interpretation", "")
    recs = readiness.get("recommendations") or []
    ranked = readiness.get("ranked_categories") or []

    lines = []
    if overall and level:
        lines.append(f"**Overall Score:** {int(overall)}/100 — {level}")
    if description:
        lines.append(description)
    if interp:
        lines.append(f"\n**Strategic Interpretation:** {interp}")

    if ranked:
        lines.append("\n**Category Scores:**")
        for cat in ranked:
            lines.append(
                f"- {cat.get('label', '')}: {int(cat.get('score', 0))}/100 "
                f"({cat.get('level', '')})"
            )

    if recs:
        lines.append("\n**Recommendations:**")
        for r in recs:
            lines.append(f"- {r}")

    return "\n\n".join(lines) if lines else "Readiness summary not yet available."


def generate_report_risk_section(report_data: dict) -> str:
    """Return Markdown for the risk register summary section."""
    rd = report_data or {}
    rs = rd.get("report_sections")
    sec = _section_content(rs, "risk_summary")

    if sec.get("content"):
        lines = [sec["content"]]
        kps = sec.get("key_points") or []
        if kps:
            lines.append("\n**Key Points:**")
            lines.extend(f"- {kp}" for kp in kps)
        recs = sec.get("recommendations") or []
        if recs:
            lines.append("\n**Recommendations:**")
            lines.extend(f"- {r}" for r in recs)
        return "\n".join(lines)

    risk_summary = rd.get("risk_register_summary")
    risk_register = rd.get("risk_register")

    if not risk_summary and not risk_register:
        return (
            "No Risk Register is available yet. "
            "Run the Risk Register page to include this section."
        )

    lines = []
    if risk_summary:
        total = risk_summary.get("total_risks", 0)
        critical = risk_summary.get("critical_risks", 0)
        high = risk_summary.get("high_risks", 0)
        medium = risk_summary.get("medium_risks", 0)
        low = risk_summary.get("low_risks", 0)
        position = risk_summary.get("overall_risk_position", "")
        focus = risk_summary.get("recommended_focus") or []

        lines.append(
            f"**Total Risks:** {total} "
            f"(Critical: {critical} | High: {high} | Medium: {medium} | Low: {low})"
        )
        if position:
            lines.append(f"\n**Overall Risk Position:** {position}")
        if focus:
            lines.append("\n**Recommended Focus Areas:**")
            lines.extend(f"- {f}" for f in focus)

    if risk_register:
        prioritised = sorted(
            risk_register,
            key=lambda r: r.get("risk_score", 0),
            reverse=True,
        )
        top = prioritised[:3]
        if top:
            lines.append("\n**Top Risks:**")
            for r in top:
                lines.append(
                    f"- **{r.get('risk_id', '')} — {r.get('risk_title', '')}** "
                    f"| Level: {r.get('risk_level', '')} | Score: {r.get('risk_score', '')}/25"
                )
                control = r.get("recommended_control", "")
                if control:
                    lines.append(f"  Control: {control}")

    return "\n\n".join(lines) if lines else "Risk data not available."


def generate_report_opportunity_section(report_data: dict) -> str:
    """Return Markdown for the opportunity and pilot recommendations section."""
    rd = report_data or {}
    rs = rd.get("report_sections")
    sec = _section_content(rs, "opportunity_summary")

    if sec.get("content"):
        lines = [sec["content"]]
        kps = sec.get("key_points") or []
        if kps:
            lines.append("\n**Key Points:**")
            lines.extend(f"- {kp}" for kp in kps)
        recs = sec.get("recommendations") or []
        if recs:
            lines.append("\n**Recommendations:**")
            lines.extend(f"- {r}" for r in recs)
        return "\n".join(lines)

    opp_summary = rd.get("opportunity_summary")
    opp_portfolio = rd.get("opportunity_portfolio")

    if not opp_summary and not opp_portfolio:
        return (
            "No Opportunity Portfolio is available yet. "
            "Run the Opportunity and Pilot Recommendations page to include this section."
        )

    lines = []
    if opp_summary:
        total_opps = opp_summary.get("total_opportunities", 0)
        total_pilots = opp_summary.get("total_pilots", 0)
        first_pilot = opp_summary.get("recommended_first_pilot_name", "")
        position = opp_summary.get("overall_opportunity_position", "")
        focus = opp_summary.get("recommended_focus") or []

        lines.append(
            f"**Total Opportunities:** {total_opps} | **Pilots Recommended:** {total_pilots}"
        )
        if first_pilot:
            lines.append(f"**Recommended First Pilot:** {first_pilot}")
        if position:
            lines.append(f"\n**Overall Position:** {position}")
        if focus:
            lines.append("\n**Recommended Focus Areas:**")
            lines.extend(f"- {f}" for f in focus)

    if opp_portfolio:
        sequence = opp_portfolio.get("recommended_pilot_sequence") or []
        if sequence:
            lines.append("\n**Recommended Pilot Sequence:**")
            for item in sequence:
                lines.append(
                    f"- **{item.get('position', '')}. {item.get('pilot_name', '')}** "
                    f"| {item.get('suggested_timeline', '')} "
                    f"| Complexity: {item.get('complexity', '')} "
                    f"| Risk: {item.get('risk_level', '')}"
                )

    return "\n\n".join(lines) if lines else "Opportunity data not available."


def generate_report_roadmap_section(report_data: dict) -> str:
    """Return Markdown for the 30/60/90-day roadmap section."""
    rd = report_data or {}
    rs = rd.get("report_sections")
    sec = _section_content(rs, "roadmap_summary")

    if sec.get("content"):
        lines = [sec["content"]]
        kps = sec.get("key_points") or []
        if kps:
            lines.append("\n**Key Points:**")
            lines.extend(f"- {kp}" for kp in kps)
        recs = sec.get("recommendations") or []
        if recs:
            lines.append("\n**Recommendations:**")
            lines.extend(f"- {r}" for r in recs)
        return "\n".join(lines)

    rm_summary = rd.get("implementation_roadmap_summary")
    roadmap = rd.get("implementation_roadmap")

    if not rm_summary and not roadmap:
        return (
            "No Implementation Roadmap is available yet. "
            "Run the Roadmap page to include this section."
        )

    lines = []
    if rm_summary:
        total = rm_summary.get("total_actions", 0)
        d30 = rm_summary.get("day_30_actions", 0)
        d60 = rm_summary.get("day_60_actions", 0)
        d90 = rm_summary.get("day_90_actions", 0)
        high_pri = rm_summary.get("high_priority_actions", 0)
        first_pilot = rm_summary.get("recommended_first_pilot", "")
        position = rm_summary.get("overall_roadmap_position", "")
        deps = rm_summary.get("key_dependencies") or []
        risks = rm_summary.get("key_risks_to_manage") or []

        lines.append(
            f"**Total Actions:** {total} "
            f"(Day 30: {d30} | Day 60: {d60} | Day 90: {d90}) "
            f"| **High Priority:** {high_pri}"
        )
        if first_pilot:
            lines.append(f"**Recommended First Pilot:** {first_pilot}")
        if position:
            lines.append(f"\n**Overall Roadmap Position:** {position}")
        if deps:
            lines.append("\n**Key Dependencies:**")
            lines.extend(f"- {d}" for d in deps)
        if risks:
            lines.append("\n**Key Risks to Manage:**")
            lines.extend(f"- {r}" for r in risks)

    if roadmap:
        phase_30 = roadmap.get("phase_30_days") or []
        phase_60 = roadmap.get("phase_60_days") or []
        phase_90 = roadmap.get("phase_90_days") or []

        if phase_30:
            lines.append("\n**First 30 Days — Foundation and Risk Control:**")
            for act in phase_30[:5]:
                lines.append(
                    f"- [{act.get('priority', '')}] {act.get('action_id', '')} "
                    f"— {act.get('title', '')} (Owner: {act.get('owner', '')})"
                )
            if len(phase_30) > 5:
                lines.append(f"  ...and {len(phase_30) - 5} more actions.")

        if phase_60:
            lines.append("\n**Days 31–60 — Pilot Preparation and Controlled Delivery:**")
            for act in phase_60[:5]:
                lines.append(
                    f"- [{act.get('priority', '')}] {act.get('action_id', '')} "
                    f"— {act.get('title', '')} (Owner: {act.get('owner', '')})"
                )
            if len(phase_60) > 5:
                lines.append(f"  ...and {len(phase_60) - 5} more actions.")

        if phase_90:
            lines.append("\n**Days 61–90 — Review, Refine, and Scale Decision:**")
            for act in phase_90[:5]:
                lines.append(
                    f"- [{act.get('priority', '')} ] {act.get('action_id', '')} "
                    f"— {act.get('title', '')} (Owner: {act.get('owner', '')})"
                )
            if len(phase_90) > 5:
                lines.append(f"  ...and {len(phase_90) - 5} more actions.")

    return "\n\n".join(lines) if lines else "Roadmap data not available."


def generate_report_training_needs_section(report_data: dict) -> str:
    """Return Markdown for the training and capability needs section."""
    rd = report_data or {}
    rs = rd.get("report_sections")
    sec = _section_content(rs, "training_needs")

    if sec.get("content"):
        lines = [sec["content"]]
        kps = sec.get("key_points") or []
        if kps:
            lines.append("\n**Key Points:**")
            lines.extend(f"- {kp}" for kp in kps)
        recs = sec.get("recommendations") or []
        if recs:
            lines.append("\n**Recommendations:**")
            lines.extend(f"- {r}" for r in recs)
        lines.append(
            "\n*These training needs can be converted into workshop materials using "
            "Build 4: AI Staff Training and Workshop Generator.*"
        )
        return "\n".join(lines)

    audit = rd.get("audit_data") or {}
    training_needs = audit.get("training_needs") or []

    if not training_needs:
        return "No training needs identified in the audit data."

    lines = [
        f"The audit identified {len(training_needs)} training topic(s) "
        f"for the organisation to address before and during AI adoption."
    ]

    for t in training_needs:
        topic = _s(t.get("topic"))
        audience = _s(t.get("audience"))
        priority = _s(t.get("priority"))
        reason = _s(t.get("reason"))
        fmt = _s(t.get("recommended_format"))

        if topic:
            lines.append(
                f"\n**{topic}** (Priority: {priority})\n"
                f"Audience: {audience}\n"
                f"Reason: {reason}\n"
                f"Recommended format: {fmt}"
            )

    lines.append(
        "\n*These training needs can be converted into workshop materials using "
        "Build 4: AI Staff Training and Workshop Generator.*"
    )

    return "\n\n".join(lines)


def generate_report_governance_section(report_data: dict) -> str:
    """Return Markdown for the governance recommendations section."""
    rd = report_data or {}
    rs = rd.get("report_sections")
    sec = _section_content(rs, "governance_recommendations")

    if sec.get("content"):
        lines = [sec["content"]]
        kps = sec.get("key_points") or []
        if kps:
            lines.append("\n**Key Points:**")
            lines.extend(f"- {kp}" for kp in kps)
        recs = sec.get("recommendations") or []
        if recs:
            lines.append("\n**Recommendations:**")
            lines.extend(f"- {r}" for r in recs)
        return "\n".join(lines)

    # Fallback — use standard governance recommendations
    audit = rd.get("audit_data") or {}
    gaps = audit.get("governance_gaps") or []

    lines = []
    if gaps:
        lines.append(
            f"The audit identified {len(gaps)} governance gap(s) "
            f"that should be addressed before scaling AI use."
        )
        for g in gaps:
            lines.append(
                f"\n**{_s(g.get('gap_title'))}** (Priority: {_s(g.get('priority'))})\n"
                f"Current state: {_s(g.get('current_state'))}\n"
                f"Why it matters: {_s(g.get('why_it_matters'))}\n"
                f"Recommended action: {_s(g.get('recommended_action'))}"
            )

    lines.append("\n**Standard Governance Recommendations:**")
    for rec in _GOVERNANCE_RECOMMENDATIONS:
        lines.append(f"- {rec}")

    return "\n\n".join(lines)


def generate_report_next_steps_section(report_data: dict) -> str:
    """Return Markdown for the immediate next steps section."""
    rd = report_data or {}
    rs = rd.get("report_sections")
    sec = _section_content(rs, "immediate_next_steps")

    if sec.get("content"):
        lines = [sec["content"]]
        kps = sec.get("key_points") or []
        if kps:
            lines.append("\n**Key Points:**")
            lines.extend(f"- {kp}" for kp in kps)
        recs = sec.get("recommendations") or []
        if recs:
            lines.append("\n**Recommendations:**")
            lines.extend(f"- {r}" for r in recs)
        return "\n".join(lines)

    # Fallback — use standard next steps, weave in first pilot name if available
    opp_summary = rd.get("opportunity_summary")
    rm_summary = rd.get("implementation_roadmap_summary")
    first_pilot = ""
    if opp_summary:
        first_pilot = opp_summary.get("recommended_first_pilot_name", "")
    elif rm_summary:
        first_pilot = rm_summary.get("recommended_first_pilot", "")

    steps = list(_NEXT_STEPS)
    if first_pilot:
        steps[6] = f"Run the controlled pilot ({first_pilot}) with human review at every step."

    lines = [
        "The following actions should be taken in the immediate term to progress "
        "responsible AI adoption:"
    ]
    for i, step in enumerate(steps, 1):
        lines.append(f"{i}. {step}")

    return "\n\n".join(lines)


def generate_report_appendices_section(report_data: dict) -> str:
    """Return Markdown for the appendices section."""
    rd = report_data or {}
    audit = rd.get("audit_data") or {}
    profile = audit.get("organisation_profile") or {}
    scores = audit.get("readiness_scores") or {}
    risk_register = rd.get("risk_register")
    opp_portfolio = rd.get("opportunity_portfolio")
    rm_summary = rd.get("implementation_roadmap_summary")
    source_available = rd.get("source_outputs_available") or {}

    lines = ["### Appendix A — Audit Data Summary"]
    org = _s(profile.get("organisation_name"), "Unnamed organisation")
    staff = profile.get("staff_count")
    risk_count = len(audit.get("risk_findings") or [])
    pilot_count = len(audit.get("pilot_recommendations") or [])
    training_count = len(audit.get("training_needs") or [])
    gov_count = len(audit.get("governance_gaps") or [])

    lines.append(f"Organisation: {org}")
    if staff is not None:
        lines.append(f"Staff: {staff}")
    lines.append(f"Risk findings: {risk_count}")
    lines.append(f"Pilot recommendations: {pilot_count}")
    lines.append(f"Training needs: {training_count}")
    lines.append(f"Governance gaps: {gov_count}")

    if scores:
        lines.append("\n### Appendix B — Readiness Category Scores")
        score_labels = {
            "strategy_score": "Strategy",
            "data_governance_score": "Data Governance",
            "staff_capability_score": "Staff Capability",
            "workflow_opportunity_score": "Workflow Opportunity",
            "risk_management_score": "Risk Management",
            "leadership_alignment_score": "Leadership Alignment",
        }
        for key, label in score_labels.items():
            val = scores.get(key)
            if val is not None:
                lines.append(f"- {label}: {val}/100")
        overall = scores.get("overall_readiness_score")
        if overall is not None:
            lines.append(f"- **Overall: {overall}/100**")

    if risk_register:
        lines.append("\n### Appendix C — Risk Register Summary Table")
        lines.append("| Risk ID | Risk Title | Level | Score |")
        lines.append("|---|---|---|---|")
        for r in sorted(risk_register, key=lambda x: x.get("risk_score", 0), reverse=True):
            lines.append(
                f"| {r.get('risk_id', '')} "
                f"| {r.get('risk_title', '')} "
                f"| {r.get('risk_level', '')} "
                f"| {r.get('risk_score', '')}/25 |"
            )

    if opp_portfolio:
        pilots = opp_portfolio.get("pilots") or []
        if pilots:
            lines.append("\n### Appendix D — Pilot Recommendation Summary Table")
            lines.append("| Pilot ID | Pilot Name | Priority | Complexity | Risk | Timeline |")
            lines.append("|---|---|---|---|---|---|")
            for p in pilots:
                lines.append(
                    f"| {p.get('pilot_id', '')} "
                    f"| {p.get('pilot_name', '')} "
                    f"| {p.get('pilot_priority', '')} "
                    f"| {p.get('complexity', '')} "
                    f"| {p.get('risk_level', '')} "
                    f"| {p.get('suggested_timeline', '')} |"
                )

    if rm_summary:
        lines.append("\n### Appendix E — Roadmap Action Summary")
        lines.append(
            f"Total actions: {rm_summary.get('total_actions', 0)} | "
            f"Day 30: {rm_summary.get('day_30_actions', 0)} | "
            f"Day 60: {rm_summary.get('day_60_actions', 0)} | "
            f"Day 90: {rm_summary.get('day_90_actions', 0)}"
        )

    lines.append("\n### Appendix F — Source Outputs Available")
    for key, available in source_available.items():
        status = "✓ Available" if available else "✗ Not generated"
        lines.append(f"- {key.replace('_', ' ').title()}: {status}")

    return "\n\n".join(lines)


def generate_report_responsible_use_section() -> str:
    """Return Markdown for the responsible-use boundaries section."""
    return _RESPONSIBLE_USE_TEXT


def generate_report_key_findings_section(report_data: dict) -> str:
    """Return Markdown for the key findings section."""
    rd = report_data or {}
    rs = rd.get("report_sections")
    sec = _section_content(rs, "key_findings")

    if sec.get("content"):
        lines = [sec["content"]]
        kps = sec.get("key_points") or []
        if kps:
            lines.append("\n**Key Points:**")
            lines.extend(f"- {kp}" for kp in kps)
        recs = sec.get("recommendations") or []
        if recs:
            lines.append("\n**Recommendations:**")
            lines.extend(f"- {r}" for r in recs)
        return "\n".join(lines)

    # Fallback deterministic findings
    audit = rd.get("audit_data") or {}
    wf_count = len(audit.get("workflow_findings") or [])
    risk_count = len(audit.get("risk_findings") or [])
    gov_count = len(audit.get("governance_gaps") or [])
    training_count = len(audit.get("training_needs") or [])

    findings = [
        "Informal AI use is already occurring without a policy or approved tools list — "
        "clear guidance is needed to reduce risk and ensure responsible use.",
        f"Workflow opportunities exist across {wf_count} identified area(s) — "
        "these represent real potential time savings in low-risk, text-heavy tasks.",
        "Sensitive data boundaries need to be defined before AI tools process any "
        "client, learner, or staff information.",
        f"{training_count} training need(s) identified — staff training on responsible "
        "AI use is required before scaling pilots.",
        "Controlled pilots in the safest, lowest-complexity workflows are recommended "
        "before broader rollout.",
    ]
    if risk_count:
        findings.append(
            f"{risk_count} AI risk(s) identified — the risk register should be reviewed "
            "and acted on before wider AI adoption."
        )
    if gov_count:
        findings.append(
            f"{gov_count} governance gap(s) identified — policy, approved tools list, "
            "and safeguarding routes are priority gaps to close."
        )

    lines = ["The following key findings emerged from the AI readiness audit:"]
    for i, f in enumerate(findings, 1):
        lines.append(f"{i}. {f}")

    return "\n\n".join(lines)


# ── Full report assembly ───────────────────────────────────────────────────────


def generate_markdown_client_report(
    report_data: dict,
    include_sections: dict | None = None,
) -> str:
    """Assemble and return the full client report as Markdown."""
    rd = report_data or {}
    inc = include_sections or {}
    title = rd.get("report_title") or _REPORT_TITLE
    org = rd.get("organisation_name") or "Unnamed organisation"

    def _is_included(key: str, default: bool = True) -> bool:
        return inc.get(key, default)

    parts = [f"# {title}"]

    # Cover
    parts.append("## Cover Page")
    parts.append(generate_report_cover_section(rd))

    # Table of Contents
    parts.append("## Table of Contents")
    parts.append(generate_report_table_of_contents(rd, inc))

    # 1. Executive Summary
    parts.append("## 1. Executive Summary")
    parts.append(generate_report_executive_summary_section(rd))

    # 2. Organisation Context
    parts.append("## 2. Organisation Context")
    parts.append(generate_report_context_section(rd))

    # 3. Readiness Summary
    if _is_included("readiness_summary"):
        parts.append("## 3. AI Readiness Summary")
        parts.append(generate_report_readiness_section(rd))

    # 4. Key Findings
    if _is_included("key_findings"):
        parts.append("## 4. Key Findings")
        parts.append(generate_report_key_findings_section(rd))

    # 5. Risk Register Summary
    if _is_included("risk_register_summary"):
        parts.append("## 5. AI Risk Register Summary")
        parts.append(generate_report_risk_section(rd))

    # 6. Opportunities
    if _is_included("opportunity_summary"):
        parts.append("## 6. AI Opportunity and Pilot Recommendations")
        parts.append(generate_report_opportunity_section(rd))

    # 7. Roadmap
    if _is_included("roadmap_summary"):
        parts.append("## 7. 30/60/90-Day Implementation Roadmap")
        parts.append(generate_report_roadmap_section(rd))

    # 8. Training Needs
    if _is_included("training_needs"):
        parts.append("## 8. Training and Capability Needs")
        parts.append(generate_report_training_needs_section(rd))

    # 9. Governance
    if _is_included("governance_recommendations"):
        parts.append("## 9. Governance Recommendations")
        parts.append(generate_report_governance_section(rd))

    # 10. Next Steps
    if _is_included("next_steps"):
        parts.append("## 10. Immediate Next Steps")
        parts.append(generate_report_next_steps_section(rd))

    # 11. Responsible-Use — always included
    parts.append("## 11. Responsible-Use Boundaries")
    parts.append(generate_report_responsible_use_section())

    # 12. Prototype Limitations — always included
    parts.append("## 12. Prototype Limitations")
    proto_lines = [
        f"- {lim}" for lim in _PROTOTYPE_LIMITATIONS
    ]
    parts.append("\n".join(proto_lines))

    # 13. Appendices
    if _is_included("appendices"):
        parts.append("## 13. Appendices")
        parts.append(generate_report_appendices_section(rd))

    # Footer
    parts.append(
        f"---\n\n"
        f"*{org} · AI Readiness and Responsible AI Adoption Report*\n\n"
        f"*All scenarios are synthetic. Outputs require human review before real-world use.*\n\n"
        f"*{_PROTOTYPE_NOTE}*"
    )

    return "\n\n".join(parts)


# ── Summary and filename ───────────────────────────────────────────────────────


def summarise_client_report(report_data: dict) -> dict:
    """Return a summary dict for the assembled client report."""
    rd = report_data or {}
    org = rd.get("organisation_name") or "Unnamed organisation"
    source = rd.get("source_outputs_available") or {}

    sections_available = sum(1 for v in source.values() if v)
    sections_missing = sum(1 for v in source.values() if not v)

    risk_register = rd.get("risk_register") or []
    risks_included = len(risk_register)

    opp_portfolio = rd.get("opportunity_portfolio") or {}
    opps_list = opp_portfolio.get("opportunities") or []
    opportunities_included = len(opps_list)
    pilots_list = opp_portfolio.get("pilots") or []
    pilots_included = len(pilots_list)

    rm_summary = rd.get("implementation_roadmap_summary") or {}
    roadmap_actions = rm_summary.get("total_actions", 0)

    all_available = all(source.values()) if source else False
    if all_available:
        readiness = (
            "The client report is ready for export, subject to human review "
            "and responsible-owner approval."
        )
    else:
        readiness = (
            "The client report can be generated as a partial draft, but it should be "
            "completed by running the missing analysis pages first."
        )

    return {
        "organisation_name": org,
        "sections_available": sections_available,
        "sections_missing": sections_missing,
        "risks_included": risks_included,
        "opportunities_included": opportunities_included,
        "pilots_included": pilots_included,
        "roadmap_actions_included": roadmap_actions,
        "report_readiness": readiness,
        "human_review_required": True,
    }


def create_client_report_filename(organisation_name: str) -> str:
    """Return a safe Markdown filename for the client report."""
    from src.utils import create_safe_filename
    slug = organisation_name or "client"
    return create_safe_filename(f"ai-consulting-report-{slug}", "md")


# ── Backward-compatible stub ───────────────────────────────────────────────────


def build_report_placeholder(audit_data: dict) -> str:
    """Return a stub report. Retained for backward compatibility."""
    org = (
        (audit_data or {})
        .get("organisation_profile", {})
        .get("organisation_name", "Unknown Organisation")
    )
    return (
        f"# AI Consulting Report — {org}\n\n"
        "Full report generation will be implemented in a later phase.\n\n"
        "*Synthetic scenario prototype. Human review required before use.*\n"
    )
