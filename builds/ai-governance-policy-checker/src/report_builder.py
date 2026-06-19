"""
Governance Report Builder — AI Governance Policy Checker
Build 6 · BrightPath ChatGPT Mastery Project

Assembles a complete client-facing AI governance policy review report from all
previously generated Build 6 outputs: synthetic policy pack, governance framework,
coverage review, gap analysis, recommendations, and maturity summary.

Deterministic only. No external AI, LLM, or API calls.
Synthetic/demo data only.
"""

import datetime

_RESPONSIBLE_USE_NOTE = (
    "This governance report is generated from synthetic/demo policy text only. "
    "It must not be used with real client policies, learner data, safeguarding "
    "case details, staff HR data, personal data, confidential data, or regulated "
    "information without appropriate governance, approvals, and responsible owners."
)

_PROTOTYPE_NOTE = (
    "This prototype does not provide legal, safeguarding, HR, compliance, "
    "data-protection, financial, medical, academic-integrity, or professional "
    "governance advice. Suggested wording directions are not legally approved "
    "policy text. They require review by appropriate responsible owners before "
    "real-world use. This is a deterministic governance review support tool, "
    "not a compliance certification system. Human review remains required before "
    "any real-world use."
)

_REQUIRED_SECTIONS = ["policy_pack"]

_RECOMMENDED_SECTIONS = [
    "governance_framework",
    "coverage_results",
    "gap_analysis",
    "policy_recommendations",
    "governance_maturity",
]

_ALL_REPORT_SECTIONS = [
    "executive_summary",
    "policy_pack",
    "governance_framework",
    "coverage_review",
    "gap_analysis",
    "recommendations",
    "maturity_summary",
    "next_steps",
    "responsible_use",
    "prototype_limitations",
    "appendices",
]

_SECTION_LABELS = {
    "executive_summary": "Executive Summary",
    "policy_pack": "Policy Pack Overview",
    "governance_framework": "Responsible AI Governance Framework",
    "coverage_review": "Policy Coverage Review",
    "gap_analysis": "Policy Gap Analysis",
    "recommendations": "Policy Improvement Recommendations",
    "maturity_summary": "Governance Score and Maturity Summary",
    "next_steps": "Recommended Next Steps",
    "responsible_use": "Responsible-Use Boundaries",
    "prototype_limitations": "Prototype Limitations",
    "appendices": "Appendices",
}

_NEXT_STEPS_POOL = [
    "Review the highest-priority gaps with responsible owners.",
    "Clarify approved and prohibited AI use cases in the AI Acceptable Use Policy.",
    "Strengthen learner and client data boundary wording in the Data Protection and AI Use Guidance.",
    "Clarify safeguarding boundary wording and confirm AI must never lead safeguarding decisions.",
    "Add or strengthen human review and accountability controls in the AI Output Review Checklist.",
    "Confirm incident and near-miss reporting routes are clear in the AI Incident and Escalation Procedure.",
    "Review suggested wording directions with appropriate responsible owners before any policy change.",
    "Communicate policy expectations through staff training — see Build 4 for training generation support.",
    "Re-run the governance review after policy updates to confirm coverage improvements.",
    "Use Build 5 to include this governance review in a wider AI consulting report.",
]


def get_governance_report_required_sections() -> list[str]:
    """Return the list of required section keys for a minimal governance report."""
    return list(_REQUIRED_SECTIONS)


def get_governance_report_optional_sections() -> list[str]:
    """Return all available section keys for a complete governance report."""
    return list(_ALL_REPORT_SECTIONS)


def check_governance_report_readiness(session_state: dict) -> dict:
    """
    Inspect session state and return a readiness summary.

    Returns:
        is_ready: True if minimum required data is present.
        available_sections: list of data keys confirmed in session state.
        missing_sections: list of recommended keys not yet in session state.
        recommended_next_steps: guidance on what to complete first.
    """
    available = []
    missing = []

    checks = [
        ("policy_pack", "Load BrightPath synthetic policy pack from Policy Library."),
        ("governance_framework", "Load the governance framework from Governance Framework page."),
        ("coverage_results", "Run Policy Checker to generate the coverage review."),
        ("coverage_summary", "Run Policy Checker to generate the coverage summary."),
        ("gap_analysis", "Run Gap Analysis to generate gap findings."),
        ("gap_summary", "Run Gap Analysis to generate the gap summary."),
        ("policy_recommendations", "Run Recommendations to generate policy improvement recommendations."),
        ("recommendation_summary", "Run Recommendations to generate the recommendation summary."),
        ("governance_maturity", "Run Governance Maturity to generate the maturity summary."),
        ("governance_maturity_summary", "Run Governance Maturity to generate the maturity statistics."),
    ]

    recommended_next_steps = []
    for key, guidance in checks:
        if key in session_state:
            available.append(key)
        else:
            missing.append(key)
            recommended_next_steps.append(guidance)

    is_ready = "policy_pack" in session_state
    # Deduplicate next steps while preserving order
    seen = set()
    deduped = []
    for step in recommended_next_steps:
        if step not in seen:
            seen.add(step)
            deduped.append(step)

    return {
        "is_ready": is_ready,
        "available_sections": available,
        "missing_sections": missing,
        "recommended_next_steps": deduped,
    }


def build_governance_report_data_from_session_state(session_state: dict) -> dict:
    """
    Build the report data dict from all available session state outputs.

    Missing outputs are represented as None. The report generator handles each
    section gracefully when data is absent.
    """
    policy_pack = session_state.get("policy_pack") or {}
    org_name = policy_pack.get("organisation_name", "Unnamed organisation")

    source_outputs_available = {
        "policy_pack": "policy_pack" in session_state,
        "governance_framework": "governance_framework" in session_state,
        "coverage_results": "coverage_results" in session_state,
        "gap_analysis": "gap_analysis" in session_state,
        "policy_recommendations": "policy_recommendations" in session_state,
        "governance_maturity": "governance_maturity" in session_state,
    }

    return {
        "report_title": "AI Governance Policy Review Report",
        "organisation_name": org_name,
        "generated_date": datetime.date.today().isoformat(),
        "policy_pack": session_state.get("policy_pack"),
        "policy_pack_summary": session_state.get("policy_pack_summary"),
        "governance_framework": session_state.get("governance_framework"),
        "governance_framework_summary": session_state.get("governance_framework_summary"),
        "coverage_results": session_state.get("coverage_results"),
        "coverage_summary": session_state.get("coverage_summary"),
        "gap_analysis": session_state.get("gap_analysis"),
        "gap_summary": session_state.get("gap_summary"),
        "policy_recommendations": session_state.get("policy_recommendations"),
        "recommendation_summary": session_state.get("recommendation_summary"),
        "governance_maturity": session_state.get("governance_maturity"),
        "governance_maturity_summary": session_state.get("governance_maturity_summary"),
        "source_outputs_available": source_outputs_available,
        "responsible_use_note": _RESPONSIBLE_USE_NOTE,
        "prototype_note": _PROTOTYPE_NOTE,
    }


# ---------------------------------------------------------------------------
# Individual section generators
# ---------------------------------------------------------------------------

def generate_report_cover_section(report_data: dict) -> str:
    """Generate the cover page Markdown for the governance report."""
    org = report_data.get("organisation_name", "Unnamed organisation")
    date = report_data.get("generated_date", datetime.date.today().isoformat())
    policy_pack = report_data.get("policy_pack") or {}
    pack_title = policy_pack.get("policy_pack_title", "Unnamed policy pack")
    org_type = policy_pack.get("organisation_type", "")
    sector = policy_pack.get("sector", "")
    country = policy_pack.get("country_context", "")

    lines = [
        "## Cover Page",
        "",
        f"**{report_data.get('report_title', 'AI Governance Policy Review Report')}**",
        "",
        f"**Organisation:** {org}",
    ]
    if org_type:
        lines.append(f"**Organisation type:** {org_type}")
    if sector:
        lines.append(f"**Sector:** {sector}")
    if country:
        lines.append(f"**Country context:** {country}")
    lines += [
        f"**Policy pack:** {pack_title}",
        f"**Date generated:** {date}",
        "",
        "**Prototype status:** Production-style AI governance review prototype, not a production "
        "compliance, legal, safeguarding, HR, data-protection, or professional advisory system.",
        "",
        "> This report is generated from synthetic/demo policy text only. "
        "Human review is required before any real-world use.",
    ]
    return "\n".join(lines)


def generate_report_table_of_contents(
    report_data: dict,
    include_sections: dict | None = None,
) -> str:
    """Generate a Markdown table of contents for the report."""
    sections = [
        ("1", "Executive Summary"),
        ("2", "Policy Pack Overview"),
        ("3", "Responsible AI Governance Framework"),
        ("4", "Policy Coverage Review"),
        ("5", "Policy Gap Analysis"),
        ("6", "Policy Improvement Recommendations"),
        ("7", "Governance Score and Maturity Summary"),
        ("8", "Recommended Next Steps"),
        ("9", "Responsible-Use Boundaries"),
        ("10", "Prototype Limitations"),
        ("11", "Appendices"),
    ]
    lines = ["## Table of Contents", ""]
    for num, title in sections:
        lines.append(f"{num}. {title}")
    lines.append("")
    return "\n".join(lines)


def generate_report_executive_summary_section(report_data: dict) -> str:
    """Generate a deterministic executive summary for the governance report."""
    org = report_data.get("organisation_name", "The organisation")
    lines = ["## 1. Executive Summary", ""]

    coverage_results = report_data.get("coverage_results")
    gap_summary = report_data.get("gap_summary")
    rec_summary = report_data.get("recommendation_summary")
    maturity = report_data.get("governance_maturity")
    maturity_sum = report_data.get("governance_maturity_summary")

    # Opening
    lines.append(
        f"This report presents the findings of an AI governance policy review for {org}. "
        "The review assessed the organisation's AI policy pack against a responsible AI "
        "governance framework covering 12 domains: strategy and ownership, approved AI tools, "
        "prohibited uses, data protection and confidentiality, learner and client data boundaries, "
        "safeguarding boundaries, human review and accountability, accuracy and hallucination "
        "control, bias, fairness and inclusion, staff training and capability, escalation and "
        "incident reporting, and monitoring and continuous improvement."
    )
    lines.append("")

    # Coverage position
    if coverage_results:
        score = coverage_results.get("overall_coverage_score", 0)
        level = coverage_results.get("overall_coverage_level", "")
        lines.append(
            f"The overall policy coverage score is **{score}/100** ({level}). "
            "This is based on deterministic keyword-based evidence matching across the "
            "synthetic policy pack — not a legal or regulatory assessment."
        )
        lines.append("")

    # Gap position
    if gap_summary:
        critical = gap_summary.get("critical_gap_count", 0)
        high = gap_summary.get("high_gap_count", 0)
        total = gap_summary.get("total_gaps", 0)
        themes = gap_summary.get("gap_themes", [])
        gap_pos = gap_summary.get("overall_gap_position", "")
        if gap_pos:
            lines.append(gap_pos)
            lines.append("")
        if themes:
            lines.append(f"Key gap themes include: {', '.join(themes[:4])}.")
            lines.append("")
        if critical > 0 or high > 0:
            lines.append(
                f"There are **{critical} critical** and **{high} high** priority gaps "
                f"across {total} total gaps identified. These should be addressed before "
                "wider AI adoption or pilot scaling."
            )
            lines.append("")

    # Recommendation position
    if rec_summary:
        urgent = rec_summary.get("urgent_count", 0)
        high_p = rec_summary.get("high_priority_count", 0)
        total_recs = rec_summary.get("total_recommendations", 0)
        if urgent > 0 or high_p > 0:
            lines.append(
                f"**{total_recs} policy improvement recommendations** have been generated, "
                f"including {urgent} urgent and {high_p} high-priority items. "
                "The recommended direction is to address high-priority policy gaps first, "
                "clarify data and safeguarding boundaries, define approved and prohibited use cases, "
                "strengthen human review and escalation routes, and communicate policy expectations "
                "through staff training."
            )
            lines.append("")

    # Maturity position
    if maturity:
        level = maturity.get("overall_maturity_level", "")
        score = maturity.get("overall_governance_score", 0)
        adoption = maturity.get("adoption_readiness_position", "")
        if level:
            lines.append(
                f"The overall AI governance maturity level is **{level}** "
                f"(score: {score}/100). {adoption}"
            )
            lines.append("")

    # Closing
    lines.append(
        "**All outputs from this review are generated from synthetic/demo policy text only. "
        "Human review and responsible-owner approval are required before any policy change, "
        "governance decision, or adoption guidance is acted upon.**"
    )
    lines.append("")
    return "\n".join(lines)


def generate_report_policy_pack_section(report_data: dict) -> str:
    """Generate the policy pack overview section."""
    lines = ["## 2. Policy Pack Overview", ""]

    policy_pack = report_data.get("policy_pack")
    summary = report_data.get("policy_pack_summary")

    if not policy_pack:
        lines.append(
            "No synthetic policy pack is available yet. "
            "Load the BrightPath synthetic policy pack from the Policy Library page."
        )
        lines.append("")
        return "\n".join(lines)

    org = policy_pack.get("organisation_name", "Unnamed organisation")
    org_type = policy_pack.get("organisation_type", "")
    sector = policy_pack.get("sector", "")
    country = policy_pack.get("country_context", "")
    pack_title = policy_pack.get("policy_pack_title", "")

    lines += [
        f"**Organisation:** {org}",
    ]
    if org_type:
        lines.append(f"**Organisation type:** {org_type}")
    if sector:
        lines.append(f"**Sector:** {sector}")
    if country:
        lines.append(f"**Country context:** {country}")
    if pack_title:
        lines.append(f"**Policy pack:** {pack_title}")
    lines.append("")

    policies = policy_pack.get("policies", [])
    if policies:
        lines += [
            "### Policies Reviewed",
            "",
            "| Policy | Type | Owner |",
            "|---|---|---|",
        ]
        for p in policies:
            lines.append(
                f"| {p.get('policy_title', '')} "
                f"| {p.get('policy_type', '')} "
                f"| {p.get('owner', '')} |"
            )
        lines.append("")

    if summary:
        risk_areas = summary.get("risk_areas", [])
        if risk_areas:
            lines.append("### Risk Areas Covered")
            lines.append("")
            for area in risk_areas:
                lines.append(f"- {area}")
            lines.append("")

    lines.append(
        "> **Synthetic data only.** This policy pack is demo content for portfolio "
        "demonstration. Not an approved organisational policy."
    )
    lines.append("")
    return "\n".join(lines)


def generate_report_framework_section(report_data: dict) -> str:
    """Generate the responsible AI governance framework section."""
    lines = ["## 3. Responsible AI Governance Framework", ""]

    framework = report_data.get("governance_framework")
    fw_summary = report_data.get("governance_framework_summary")

    if not framework:
        lines.append(
            "No governance framework is available yet. "
            "Open the Governance Framework page to load or review the "
            "responsible AI governance framework."
        )
        lines.append("")
        return "\n".join(lines)

    total = fw_summary.get("total_domains", len(framework)) if fw_summary else len(framework)
    high = fw_summary.get("high_priority_count", 0) if fw_summary else 0
    medium = fw_summary.get("medium_priority_count", 0) if fw_summary else 0

    lines += [
        f"The responsible AI governance framework covers **{total} domains**, "
        f"of which {high} are high priority and {medium} are medium priority.",
        "",
        "| Domain ID | Domain | Priority |",
        "|---|---|---|",
    ]
    for domain in framework:
        lines.append(
            f"| {domain.get('domain_id', '')} "
            f"| {domain.get('domain_name', '')} "
            f"| {domain.get('priority_level', '')} |"
        )
    lines.append("")
    lines.append(
        "The framework defines what good responsible AI governance looks like. "
        "Each domain specifies expected policy evidence and example controls that the "
        "policy coverage checker uses to assess the synthetic policy pack."
    )
    lines.append("")
    return "\n".join(lines)


def generate_report_coverage_section(report_data: dict) -> str:
    """Generate the policy coverage review section."""
    lines = ["## 4. Policy Coverage Review", ""]

    coverage = report_data.get("coverage_results")
    summary = report_data.get("coverage_summary")

    if not coverage:
        lines.append(
            "No Policy Coverage Review is available yet. "
            "Run the Policy Checker page to include this section."
        )
        lines.append("")
        return "\n".join(lines)

    org = report_data.get("organisation_name", "The organisation")
    score = coverage.get("overall_coverage_score", 0)
    level = coverage.get("overall_coverage_level", "")
    total_domains = coverage.get("total_domains_checked", 0)

    lines += [
        f"The policy coverage review assessed {org}'s AI policy pack against the 12 responsible "
        "AI governance domains using deterministic keyword-based evidence matching. "
        f"The overall coverage score is **{score}/100** ({level}) across {total_domains} domains.",
        "",
        f"**Overall coverage score:** {score}/100",
        f"**Overall coverage level:** {level}",
        f"**Domains checked:** {total_domains}",
        "",
    ]

    if summary:
        lines += [
            "| Coverage Level | Count |",
            "|---|---|",
            f"| Strong coverage | {summary.get('strong_count', 0)} |",
            f"| Partial coverage | {summary.get('partial_count', 0)} |",
            f"| Weak coverage | {summary.get('weak_count', 0)} |",
            f"| Not covered | {summary.get('not_covered_count', 0)} |",
            "",
        ]

        high_priority_gaps = summary.get("high_priority_gaps", [])
        if high_priority_gaps:
            lines.append("**High-priority gaps:**")
            lines.append("")
            for gap in high_priority_gaps:
                lines.append(f"- {gap}")
            lines.append("")

        recommended_focus = summary.get("recommended_focus", [])
        if recommended_focus:
            lines.append("**Recommended focus areas:**")
            lines.append("")
            for focus in recommended_focus:
                lines.append(f"- {focus}")
            lines.append("")

    domain_results = coverage.get("domain_results", [])
    if domain_results:
        lines += [
            "### Domain Coverage Results",
            "",
            "| Domain | Priority | Score | Level |",
            "|---|---|---|---|",
        ]
        for dr in domain_results:
            lines.append(
                f"| {dr.get('domain_name', '')} "
                f"| {dr.get('priority_level', '')} "
                f"| {dr.get('coverage_score', 0)}/100 "
                f"| {dr.get('coverage_level', '')} |"
            )
        lines.append("")

    lines.append(
        "> Coverage scores are based on deterministic keyword matching in synthetic "
        "policy text. They are not legal or regulatory assessments."
    )
    lines.append("")
    return "\n".join(lines)


def generate_report_gap_analysis_section(report_data: dict) -> str:
    """Generate the policy gap analysis section."""
    lines = ["## 5. Policy Gap Analysis", ""]

    gap_analysis = report_data.get("gap_analysis")
    gap_summary = report_data.get("gap_summary")

    if not gap_analysis:
        lines.append(
            "No Gap Analysis is available yet. "
            "Run the Gap Analysis page to include this section."
        )
        lines.append("")
        return "\n".join(lines)

    org = report_data.get("organisation_name", "The organisation")
    lines += [
        f"The gap analysis reviewed {org}'s AI policy pack against the 12 responsible AI "
        "governance domains, identifying areas where policy coverage is absent, weak, or "
        "insufficient. Gaps are classified by severity and domain priority to support the "
        "consulting conversation about where to focus the organisation's policy review effort.",
        "",
    ]

    if gap_summary:
        total = gap_summary.get("total_gaps", 0)
        critical = gap_summary.get("critical_gap_count", 0)
        high = gap_summary.get("high_gap_count", 0)
        medium = gap_summary.get("medium_gap_count", 0)
        low = gap_summary.get("low_gap_count", 0)
        covered = gap_summary.get("covered_domain_count", 0)
        position = gap_summary.get("overall_gap_position", "")
        themes = gap_summary.get("gap_themes", [])
        focus = gap_summary.get("recommended_focus", [])

        lines += [
            f"**Total gaps identified:** {total}",
            f"**Critical gaps:** {critical}",
            f"**High gaps:** {high}",
            f"**Medium gaps:** {medium}",
            f"**Low gaps:** {low}",
            f"**Domains with sufficient coverage:** {covered}",
            "",
        ]

        if position:
            lines += [position, ""]

        if themes:
            lines.append("**Gap themes:**")
            lines.append("")
            for theme in themes:
                lines.append(f"- {theme}")
            lines.append("")

        if focus:
            lines.append("**Recommended focus areas:**")
            lines.append("")
            for f in focus:
                lines.append(f"- {f}")
            lines.append("")

    prioritised = gap_analysis.get("prioritised_gaps", [])
    if prioritised:
        lines += [
            "### Prioritised Gaps",
            "",
            "| Gap ID | Domain | Severity | Priority | Score |",
            "|---|---|---|---|---|",
        ]
        for gap in prioritised:
            lines.append(
                f"| {gap.get('gap_id', '')} "
                f"| {gap.get('domain_name', '')} "
                f"| {gap.get('gap_severity', '')} "
                f"| {gap.get('priority_level', '')} "
                f"| {gap.get('coverage_score', 0)}/100 |"
            )
        lines.append("")

    lines.append(
        "> Gap severity classifications are indicative only. "
        "A Critical gap does not mean the organisation is non-compliant. "
        "Qualified human review is required."
    )
    lines.append("")
    return "\n".join(lines)


def generate_report_recommendations_section(report_data: dict) -> str:
    """Generate the policy improvement recommendations section."""
    lines = ["## 6. Policy Improvement Recommendations", ""]

    recs = report_data.get("policy_recommendations")
    rec_summary = report_data.get("recommendation_summary")

    if not recs:
        lines.append(
            "No Policy Recommendations are available yet. "
            "Run the Recommendations page to include this section."
        )
        lines.append("")
        return "\n".join(lines)

    org = report_data.get("organisation_name", "The organisation")
    lines += [
        f"This section sets out policy improvement recommendations for {org}, "
        "derived from the gap analysis findings. Each recommendation identifies a target policy, "
        "suggested responsible owner, and a wording direction to guide the policy review. "
        "Recommendations are prioritised by gap severity and domain priority so that the most "
        "important actions are visible at a glance.",
        "",
    ]

    if rec_summary:
        total = rec_summary.get("total_recommendations", 0)
        urgent = rec_summary.get("urgent_count", 0)
        high = rec_summary.get("high_priority_count", 0)
        medium = rec_summary.get("medium_priority_count", 0)
        low = rec_summary.get("low_priority_count", 0)
        quick_wins = rec_summary.get("quick_win_count", 0)
        position = rec_summary.get("overall_recommendation_position", "")

        lines += [
            f"**Total recommendations:** {total}",
            f"**Urgent:** {urgent}",
            f"**High priority:** {high}",
            f"**Medium priority:** {medium}",
            f"**Low priority:** {low}",
            f"**Quick wins:** {quick_wins}",
            "",
        ]

        if position:
            lines += [position, ""]

        themes = rec_summary.get("top_policy_update_themes", [])
        if themes:
            lines.append("**Policy update themes:**")
            lines.append("")
            for theme in themes:
                lines.append(f"- {theme}")
            lines.append("")

        owners = rec_summary.get("top_owners", [])
        if owners:
            lines.append("**Key responsible owners:**")
            lines.append("")
            for owner in owners:
                lines.append(f"- {owner}")
            lines.append("")

    # Quick wins
    quick_win_list = recs.get("quick_wins", [])
    if quick_win_list:
        lines += ["### Quick Wins", ""]
        for qw in quick_win_list:
            lines.append(
                f"- **{qw.get('recommendation_id', '')}** — "
                f"{qw.get('recommendation_title', '')} "
                f"({qw.get('recommendation_priority', '')})"
            )
        lines.append("")

    # Prioritised table
    prioritised = recs.get("prioritised_recommendations", [])
    if prioritised:
        lines += [
            "### Prioritised Recommendations",
            "",
            "| ID | Domain | Priority | Action | Owner |",
            "|---|---|---|---|---|",
        ]
        for rec in prioritised:
            lines.append(
                f"| {rec.get('recommendation_id', '')} "
                f"| {rec.get('domain_name', '')} "
                f"| {rec.get('recommendation_priority', '')} "
                f"| {rec.get('policy_action_type', '')} "
                f"| {rec.get('suggested_owner', '')} |"
            )
        lines.append("")

    lines.append(
        "> **Wording directions are not legally approved policy text.** "
        "They are starting points for review by appropriate responsible owners. "
        "Human review is required before any policy change."
    )
    lines.append("")
    return "\n".join(lines)


def generate_report_maturity_section(report_data: dict) -> str:
    """Generate the governance maturity summary section."""
    lines = ["## 7. Governance Score and Maturity Summary", ""]

    maturity = report_data.get("governance_maturity")
    maturity_sum = report_data.get("governance_maturity_summary")

    if not maturity:
        lines.append(
            "No Governance Maturity Summary is available yet. "
            "Run the Governance Maturity page to include this section."
        )
        lines.append("")
        return "\n".join(lines)

    org = report_data.get("organisation_name", "The organisation")
    score = maturity.get("overall_governance_score", 0)
    level = maturity.get("overall_maturity_level", "")
    description = maturity.get("maturity_description", "")
    adoption = maturity.get("adoption_readiness_position", "")
    next_step = maturity.get("recommended_next_step", "")

    lines += [
        f"This section presents the AI governance maturity assessment for {org}. "
        "The maturity score is derived from policy coverage scores, with penalties applied for "
        "identified gap severity and recommendation priority, giving a calibrated picture of "
        "governance readiness across the 12 assessed domains.",
        "",
        f"**Overall governance score:** {score}/100",
        f"**Maturity level:** {level}",
        "",
        description,
        "",
    ]

    if adoption:
        lines += ["**Adoption readiness position:**", "", adoption, ""]

    if next_step:
        lines += ["**Recommended next step:**", "", f"> {next_step}", ""]

    # Strengths and weaknesses
    strengths = maturity.get("maturity_strengths", [])
    weaknesses = maturity.get("maturity_weaknesses", [])

    if strengths:
        lines += ["**Governance strengths:**", ""]
        for s in strengths:
            lines.append(
                f"- **{s.get('domain_name', '')}** — "
                f"{s.get('maturity_score', 0)}/100 ({s.get('maturity_level', '')})"
            )
        lines.append("")

    if weaknesses:
        lines += ["**Governance weaknesses:**", ""]
        for w in weaknesses:
            lines.append(
                f"- **{w.get('domain_name', '')}** — "
                f"{w.get('maturity_score', 0)}/100 ({w.get('maturity_level', '')})"
            )
        lines.append("")

    # Domain maturity table
    domain_scores = maturity.get("domain_maturity_scores", [])
    if domain_scores:
        lines += [
            "### Domain Maturity Scores",
            "",
            "| Domain | Priority | Coverage | Maturity Score | Maturity Level |",
            "|---|---|---|---|---|",
        ]
        for ds in domain_scores:
            lines.append(
                f"| {ds.get('domain_name', '')} "
                f"| {ds.get('priority_level', '')} "
                f"| {ds.get('coverage_score', 0)}/100 "
                f"| {ds.get('maturity_score', 0)}/100 "
                f"| {ds.get('maturity_level', '')} |"
            )
        lines.append("")

    lines.append(
        "> Maturity levels are indicative score bands, not formal compliance ratings "
        "or regulatory assessments. Human review is required."
    )
    lines.append("")
    return "\n".join(lines)


def generate_report_next_steps_section(report_data: dict) -> str:
    """Generate the recommended next steps section."""
    lines = ["## 8. Recommended Next Steps", ""]

    maturity = report_data.get("governance_maturity")
    gap_analysis = report_data.get("gap_analysis")
    recs = report_data.get("policy_recommendations")

    # Derive targeted next steps where possible
    targeted = []

    if maturity:
        next_step = maturity.get("recommended_next_step", "")
        if next_step:
            targeted.append(next_step)
        for p in maturity.get("improvement_priorities", [])[:3]:
            if p not in targeted:
                targeted.append(p)

    if gap_analysis:
        prioritised = gap_analysis.get("prioritised_gaps", [])
        for gap in prioritised[:2]:
            hint = gap.get("action_hint", "")
            if hint and hint not in targeted:
                targeted.append(hint)

    # Pad with pool steps up to 8
    for step in _NEXT_STEPS_POOL:
        if len(targeted) >= 8:
            break
        if step not in targeted:
            targeted.append(step)

    targeted = targeted[:8]

    for i, step in enumerate(targeted, 1):
        lines.append(f"{i}. {step}")
    lines.append("")

    lines.append(
        "> All next steps should be reviewed and approved by qualified responsible owners "
        "before any real-world action is taken."
    )
    lines.append("")
    return "\n".join(lines)


def generate_report_appendices_section(report_data: dict) -> str:
    """Generate the appendices section."""
    lines = ["## 11. Appendices", ""]

    # A: Policy list
    lines += ["### A. Policy List", ""]
    policy_pack = report_data.get("policy_pack")
    if policy_pack:
        for p in policy_pack.get("policies", []):
            lines.append(
                f"- **{p.get('policy_id', '')}** — "
                f"{p.get('policy_title', '')} "
                f"(Owner: {p.get('owner', '')})"
            )
    else:
        lines.append("Policy pack not available.")
    lines.append("")

    # B: Governance domain list
    lines += ["### B. Governance Domain List", ""]
    framework = report_data.get("governance_framework")
    if framework:
        for d in framework:
            lines.append(
                f"- **{d.get('domain_id', '')}** — "
                f"{d.get('domain_name', '')} "
                f"({d.get('priority_level', '')} priority)"
            )
    else:
        lines.append("Governance framework not available.")
    lines.append("")

    # C: Coverage results table
    lines += ["### C. Coverage Results", ""]
    coverage = report_data.get("coverage_results")
    if coverage and coverage.get("domain_results"):
        lines += [
            "| Domain | Score | Level |",
            "|---|---|---|",
        ]
        for dr in coverage["domain_results"]:
            lines.append(
                f"| {dr.get('domain_name', '')} "
                f"| {dr.get('coverage_score', 0)}/100 "
                f"| {dr.get('coverage_level', '')} |"
            )
    else:
        lines.append("Coverage results not available.")
    lines.append("")

    # D: Prioritised gap table
    lines += ["### D. Prioritised Gap Table", ""]
    gap_analysis = report_data.get("gap_analysis")
    if gap_analysis and gap_analysis.get("prioritised_gaps"):
        lines += [
            "| Gap ID | Domain | Severity | Score |",
            "|---|---|---|---|",
        ]
        for gap in gap_analysis["prioritised_gaps"]:
            lines.append(
                f"| {gap.get('gap_id', '')} "
                f"| {gap.get('domain_name', '')} "
                f"| {gap.get('gap_severity', '')} "
                f"| {gap.get('coverage_score', 0)}/100 |"
            )
    else:
        lines.append("Gap analysis not available.")
    lines.append("")

    # E: Recommendation table
    lines += ["### E. Recommendation Table", ""]
    recs = report_data.get("policy_recommendations")
    if recs and recs.get("prioritised_recommendations"):
        lines += [
            "| ID | Domain | Priority | Action |",
            "|---|---|---|---|",
        ]
        for rec in recs["prioritised_recommendations"]:
            lines.append(
                f"| {rec.get('recommendation_id', '')} "
                f"| {rec.get('domain_name', '')} "
                f"| {rec.get('recommendation_priority', '')} "
                f"| {rec.get('policy_action_type', '')} |"
            )
    else:
        lines.append("Policy recommendations not available.")
    lines.append("")

    # F: Maturity score table
    lines += ["### F. Domain Maturity Score Table", ""]
    maturity = report_data.get("governance_maturity")
    if maturity and maturity.get("domain_maturity_scores"):
        lines += [
            "| Domain | Maturity Score | Maturity Level |",
            "|---|---|---|",
        ]
        for ds in maturity["domain_maturity_scores"]:
            lines.append(
                f"| {ds.get('domain_name', '')} "
                f"| {ds.get('maturity_score', 0)}/100 "
                f"| {ds.get('maturity_level', '')} |"
            )
    else:
        lines.append("Governance maturity summary not available.")
    lines.append("")

    # G: Source outputs checklist
    lines += ["### G. Source Outputs Availability", ""]
    available = report_data.get("source_outputs_available", {})
    labels = {
        "policy_pack": "Synthetic policy pack",
        "governance_framework": "Responsible AI governance framework",
        "coverage_results": "Policy coverage review",
        "gap_analysis": "Policy gap analysis",
        "policy_recommendations": "Policy improvement recommendations",
        "governance_maturity": "Governance maturity summary",
    }
    for key, label in labels.items():
        tick = "Yes" if available.get(key) else "Not generated"
        lines.append(f"- {tick} {label}")
    lines.append("")

    return "\n".join(lines)


def generate_report_responsible_use_section() -> str:
    """Generate the responsible-use boundaries section."""
    lines = [
        "## 9. Responsible-Use Boundaries",
        "",
        _RESPONSIBLE_USE_NOTE,
        "",
        _PROTOTYPE_NOTE,
        "",
        "Suggested wording directions are not legally approved policy text. "
        "They require review by appropriate responsible owners before real-world use.",
        "",
        "**Human review remains required before any real-world use.**",
        "",
    ]
    return "\n".join(lines)


def generate_report_prototype_limitations_section() -> str:
    """Generate the prototype limitations section."""
    lines = [
        "## 10. Prototype Limitations",
        "",
        "This governance review prototype has the following limitations:",
        "",
        "- **Synthetic/demo policy data only.** The policy pack is demo content, not real "
        "organisational policies.",
        "- **Deterministic keyword-based coverage review.** Coverage scores are based on "
        "keyword frequency in synthetic text, not semantic, legal, or compliance analysis.",
        "- **No legal or regulatory analysis.** Coverage scores, gap severities, maturity "
        "levels, and recommendations are not legal or regulatory risk assessments.",
        "- **No external AI or LLM API calls.** All outputs are deterministic and "
        "template-based. No OpenAI, Claude, LangChain, LlamaIndex, or similar services "
        "are used.",
        "- **No real policy validation.** This tool does not validate real-world policy "
        "adequacy, compliance, or legal sufficiency.",
        "- **No legal, compliance, safeguarding, HR, or data-protection approval.** "
        "Outputs must be reviewed by qualified professionals.",
        "- **Not production deployed.** This is a local portfolio prototype with no "
        "authentication, audit logging, or persistent storage.",
        "- **Human review required.** All outputs require responsible human review before "
        "any real-world governance action.",
        "",
    ]
    return "\n".join(lines)


def generate_markdown_governance_report(
    report_data: dict,
    include_sections: dict | None = None,
) -> str:
    """
    Assemble the full Markdown governance report from all available sections.

    include_sections: dict of section_key -> bool. If None, all sections included.
    """
    if include_sections is None:
        include_sections = {s: True for s in _ALL_REPORT_SECTIONS}

    def included(key: str) -> bool:
        return include_sections.get(key, True)

    org = report_data.get("organisation_name", "Unnamed organisation")
    lines = [
        f"# {report_data.get('report_title', 'AI Governance Policy Review Report')}",
        "",
        f"**Organisation:** {org}",
        f"**Date:** {report_data.get('generated_date', '')}",
        "",
        "---",
        "",
        generate_report_cover_section(report_data),
        "",
        "---",
        "",
        generate_report_table_of_contents(report_data, include_sections),
        "",
        "---",
        "",
    ]

    if included("executive_summary"):
        lines += [generate_report_executive_summary_section(report_data), "---", ""]

    if included("policy_pack"):
        lines += [generate_report_policy_pack_section(report_data), "---", ""]

    if included("governance_framework"):
        lines += [generate_report_framework_section(report_data), "---", ""]

    if included("coverage_review"):
        lines += [generate_report_coverage_section(report_data), "---", ""]

    if included("gap_analysis"):
        lines += [generate_report_gap_analysis_section(report_data), "---", ""]

    if included("recommendations"):
        lines += [generate_report_recommendations_section(report_data), "---", ""]

    if included("maturity_summary"):
        lines += [generate_report_maturity_section(report_data), "---", ""]

    if included("next_steps"):
        lines += [generate_report_next_steps_section(report_data), "---", ""]

    if included("responsible_use"):
        lines += [generate_report_responsible_use_section(), "---", ""]

    if included("prototype_limitations"):
        lines += [generate_report_prototype_limitations_section(), "---", ""]

    if included("appendices"):
        lines += [generate_report_appendices_section(report_data), "---", ""]

    lines += [
        "",
        "*Build 6 · AI Governance Policy Checker · BrightPath ChatGPT Mastery Project*",
        "*Synthetic scenarios only. Human review required before any real-world use.*",
    ]
    return "\n".join(lines)


def summarise_governance_report(report_data: dict) -> dict:
    """Extract summary statistics from the assembled report data."""
    available = report_data.get("source_outputs_available", {})
    sections_available = sum(1 for v in available.values() if v)
    sections_missing = sum(1 for v in available.values() if not v)

    coverage = report_data.get("coverage_results") or {}
    gap_analysis = report_data.get("gap_analysis") or {}
    recs = report_data.get("policy_recommendations") or {}
    maturity = report_data.get("governance_maturity") or {}

    domains_reviewed = coverage.get("total_domains_checked", 0)
    gaps_included = gap_analysis.get("total_gaps", 0)
    recs_included = recs.get("total_recommendations", 0)
    maturity_level = maturity.get("overall_maturity_level", "")

    all_recommended_available = all(
        available.get(k, False) for k in [
            "policy_pack", "governance_framework", "coverage_results",
            "gap_analysis", "policy_recommendations", "governance_maturity",
        ]
    )
    if all_recommended_available:
        readiness = (
            "The governance report is ready for export, subject to human review "
            "and responsible-owner approval."
        )
    else:
        readiness = (
            "The governance report can be generated as a partial draft, but it should "
            "be completed by running the missing review pages first."
        )

    return {
        "organisation_name": report_data.get("organisation_name", "Unnamed organisation"),
        "sections_available": sections_available,
        "sections_missing": sections_missing,
        "domains_reviewed": domains_reviewed,
        "gaps_included": gaps_included,
        "recommendations_included": recs_included,
        "maturity_level": maturity_level,
        "report_readiness": readiness,
        "human_review_required": True,
    }


def create_governance_report_filename(organisation_name: str) -> str:
    """Create a safe snake-case Markdown filename for the governance report."""
    safe = organisation_name.lower()
    safe = "".join(c if c.isalnum() or c in (" ", "-") else "" for c in safe)
    safe = safe.strip().replace(" ", "-")
    safe = "-".join(p for p in safe.split("-") if p)
    date = datetime.date.today().isoformat()
    return f"{safe}-ai-governance-report-{date}.md"
