"""
Gap Analysis — AI Governance Policy Checker
Build 6 · BrightPath ChatGPT Mastery Project

Identifies missing, weak, and partially covered governance domains from coverage results.
Generates gap severity, priority scores, risk statements, missing evidence, and action hints.

Deterministic only. No external AI, LLM, or API calls.
Synthetic/demo data only.
"""

_RESPONSIBLE_USE_NOTE = (
    "This gap analysis is generated from synthetic/demo policy text only. "
    "It must not be used with real client policies, learner data, safeguarding "
    "case details, staff HR data, personal data, confidential data, or regulated "
    "information without appropriate governance, approvals, and responsible owners."
)

_PROTOTYPE_NOTE = (
    "This prototype does not provide legal, safeguarding, HR, compliance, "
    "data-protection, financial, medical, academic-integrity, or professional "
    "governance advice. This is a deterministic policy review support tool, "
    "not a compliance certification system."
)

_RISK_STATEMENTS = {
    "Data Protection and Confidentiality": (
        "If this domain is weak or missing, staff may be unclear about whether personal, "
        "confidential, or sensitive information can be used with AI tools. This increases the "
        "risk of inappropriate data disclosure or uncontrolled use of sensitive information."
    ),
    "Learner and Client Data Boundaries": (
        "If this domain is weak or missing, staff may not know whether learner names, client "
        "records, case details, or identifiable information can be entered into AI tools. This "
        "increases privacy, safeguarding, and trust risks."
    ),
    "Safeguarding Boundaries": (
        "If this domain is weak or missing, staff may misunderstand the boundary between "
        "AI-assisted drafting and human-led safeguarding decisions. Safeguarding concerns must "
        "remain human-led and escalated through approved routes."
    ),
    "Human Review and Accountability": (
        "If this domain is weak or missing, AI-assisted outputs may be used without clear human "
        "sign-off, increasing the risk of inaccurate, inappropriate, or unaccountable outputs."
    ),
    "Accuracy and Hallucination Control": (
        "If this domain is weak or missing, staff may rely on AI outputs without checking "
        "accuracy, source evidence, or suitability for the audience."
    ),
    "Bias, Fairness, and Inclusion": (
        "If this domain is weak or missing, AI outputs may introduce or amplify bias, "
        "exclusionary language, or unfair treatment without staff noticing."
    ),
    "Escalation and Incident Reporting": (
        "If this domain is weak or missing, staff may not know how to report AI-related "
        "concerns, near misses, inappropriate outputs, or data/safeguarding issues."
    ),
}

_FALLBACK_RISK = (
    "If this domain is weak or missing, the organisation may lack clear policy evidence for "
    "this responsible AI governance area, increasing the risk of inconsistent or unsafe AI use."
)


def classify_gap_severity(coverage_level: str, priority_level: str) -> str:
    """Map coverage level and domain priority to a gap severity label."""
    if coverage_level == "Strong coverage":
        return "No significant gap"

    if coverage_level == "Not covered":
        if priority_level == "High":
            return "Critical gap"
        elif priority_level == "Medium":
            return "High gap"
        else:
            return "Medium gap"

    if coverage_level == "Weak coverage":
        if priority_level == "High":
            return "High gap"
        elif priority_level == "Medium":
            return "Medium gap"
        else:
            return "Low gap"

    if coverage_level == "Partial coverage":
        if priority_level == "High":
            return "Medium gap"
        else:
            return "Low gap"

    return "No significant gap"


def calculate_gap_priority_score(coverage_score: float, priority_level: str) -> int:
    """Return an integer gap urgency score between 0 and 100."""
    safe_score = max(0.0, min(100.0, float(coverage_score)))
    base = 100.0 - safe_score
    if priority_level == "High":
        base += 20
    elif priority_level == "Medium":
        base += 10
    return int(min(100, max(0, base)))


def generate_gap_id(index: int) -> str:
    """Return a gap ID in the format GAP-001."""
    return f"GAP-{index:03d}"


def identify_gap_type(domain_result: dict) -> str:
    """Map a coverage level to a gap type label."""
    coverage_level = domain_result.get("coverage_level", "")
    mapping = {
        "Not covered": "Missing policy evidence",
        "Weak coverage": "Weak policy evidence",
        "Partial coverage": "Partial policy evidence",
        "Strong coverage": "Covered sufficiently",
    }
    return mapping.get(coverage_level, "Unknown")


def generate_gap_risk_statement(domain_result: dict) -> str:
    """Return a deterministic consulting-style risk statement for a gap domain."""
    domain_name = domain_result.get("domain_name", "")
    for key, statement in _RISK_STATEMENTS.items():
        if key.lower() in domain_name.lower() or domain_name.lower() in key.lower():
            return statement
    return _FALLBACK_RISK


def generate_missing_evidence_statement(domain_result: dict) -> str:
    """Return a statement describing what evidence is missing for the domain."""
    expected = domain_result.get("expected_policy_evidence", []) or []
    if expected:
        items = "; ".join(str(e) for e in expected[:5])
        return f"The policy pack should include clearer evidence of: {items}."
    return (
        "The policy pack should include clearer wording, examples, ownership, controls, "
        "and review expectations for this governance area."
    )


def generate_gap_action_hint(domain_result: dict) -> str:
    """Return short first-step guidance for addressing the gap."""
    coverage_level = domain_result.get("coverage_level", "")
    priority_level = domain_result.get("priority_level", "")

    if coverage_level == "Not covered":
        hint = (
            "Add a dedicated policy section or procedure that clearly covers this "
            "governance domain."
        )
    elif coverage_level == "Weak coverage":
        hint = (
            "Strengthen the existing wording with clearer controls, examples, owners, "
            "and review expectations."
        )
    elif coverage_level == "Partial coverage":
        hint = (
            "Clarify the current wording and add missing operational details so staff "
            "know what to do in practice."
        )
    else:
        hint = "Review the domain wording for completeness and operational clarity."

    if priority_level == "High":
        hint += " Review this gap before scaling AI use or approving wider staff adoption."

    return hint


def generate_domain_gap(domain_result: dict, index: int) -> dict:
    """Generate a structured gap dict for a single domain result."""
    coverage_level = domain_result.get("coverage_level", "Not covered")
    priority_level = domain_result.get("priority_level", "Medium")
    coverage_score = domain_result.get("coverage_score", 0.0)

    return {
        "gap_id": generate_gap_id(index),
        "domain_id": domain_result.get("domain_id", ""),
        "domain_name": domain_result.get("domain_name", ""),
        "priority_level": priority_level,
        "coverage_score": coverage_score,
        "coverage_level": coverage_level,
        "gap_type": identify_gap_type(domain_result),
        "gap_severity": classify_gap_severity(coverage_level, priority_level),
        "gap_priority_score": calculate_gap_priority_score(coverage_score, priority_level),
        "matched_policies": domain_result.get("matched_policies", []),
        "matched_keywords": domain_result.get("matched_keywords", []),
        "evidence_snippets": domain_result.get("evidence_snippets", []),
        "expected_policy_evidence": domain_result.get("expected_policy_evidence", []),
        "missing_evidence": generate_missing_evidence_statement(domain_result),
        "risk_statement": generate_gap_risk_statement(domain_result),
        "action_hint": generate_gap_action_hint(domain_result),
        "review_note": (
            "This gap is identified through deterministic keyword matching of synthetic "
            "policy text only. Human review is required before any real-world use."
        ),
    }


def _derive_gap_themes(gaps: list) -> list:
    """Derive broad theme labels from the list of gaps."""
    themes = []
    domain_names = [g.get("domain_name", "").lower() for g in gaps]

    if any("data" in n for n in domain_names):
        themes.append("Data protection and confidentiality")
    if any("safeguarding" in n for n in domain_names):
        themes.append("Safeguarding governance")
    if any("learner" in n or "client" in n for n in domain_names):
        themes.append("Learner and client data boundaries")
    if any("human" in n or "accountability" in n for n in domain_names):
        themes.append("Human review and accountability")
    if any("escalation" in n or "incident" in n for n in domain_names):
        themes.append("Incident escalation and reporting")
    if any("training" in n or "capability" in n for n in domain_names):
        themes.append("Staff training and awareness")
    if any("bias" in n or "fairness" in n for n in domain_names):
        themes.append("Bias, fairness, and inclusion")
    if any("accuracy" in n or "hallucination" in n for n in domain_names):
        themes.append("Accuracy and hallucination controls")
    if any("strategy" in n or "ownership" in n for n in domain_names):
        themes.append("AI governance strategy and ownership")
    if any("monitoring" in n or "improvement" in n for n in domain_names):
        themes.append("Monitoring and continuous improvement")
    if any("approved" in n or "prohibited" in n for n in domain_names):
        themes.append("Approved and prohibited AI uses")

    return themes if themes else ["General governance gaps"]


def _derive_recommended_focus(gaps: list) -> list:
    """Derive recommended focus actions from the gap list."""
    if not gaps:
        return ["Review partial coverage areas for clarity and completeness."]

    focus = []
    has_critical = any(g.get("gap_severity") == "Critical gap" for g in gaps)
    has_high = any(g.get("gap_severity") == "High gap" for g in gaps)
    domain_names = [g.get("domain_name", "").lower() for g in gaps]

    if has_critical or has_high:
        focus.append("Address high-priority gaps first.")
    if any("learner" in n or "client" in n for n in domain_names):
        focus.append("Clarify learner/client data boundaries.")
    if any("safeguarding" in n for n in domain_names):
        focus.append("Clarify safeguarding boundaries and escalation routes.")
    if any("human" in n or "accountability" in n for n in domain_names):
        focus.append("Strengthen human review and accountability wording.")
    if any("escalation" in n or "incident" in n for n in domain_names):
        focus.append("Add incident and near-miss reporting process.")
    if any("training" in n or "capability" in n for n in domain_names):
        focus.append("Improve staff training and approved-tool guidance.")

    if not focus:
        focus.append("Review medium and low gaps for operational completeness.")

    return focus


def generate_policy_gap_analysis(coverage_results: dict) -> dict:
    """
    Generate a full gap analysis from policy coverage results.

    Returns gaps only for Not covered, Weak coverage, and Partial coverage domains.
    Strong coverage domains are listed separately in covered_domains.
    """
    if not isinstance(coverage_results, dict):
        coverage_results = {}

    org_name = coverage_results.get("organisation_name", "Unnamed organisation")
    pack_title = coverage_results.get("policy_pack_title", "")
    overall_score = coverage_results.get("overall_coverage_score", 0.0)
    overall_level = coverage_results.get("overall_coverage_level", "Not covered")
    domain_results = coverage_results.get("domain_results", []) or []
    responsible_use_note = coverage_results.get("responsible_use_note", _RESPONSIBLE_USE_NOTE)
    prototype_note = coverage_results.get("prototype_note", _PROTOTYPE_NOTE)

    gap_levels = {"Not covered", "Weak coverage", "Partial coverage"}

    gaps: list = []
    covered_domains: list = []
    gap_index = 1

    for domain_result in domain_results:
        if not isinstance(domain_result, dict):
            continue
        level = domain_result.get("coverage_level", "Not covered")
        if level in gap_levels:
            gap = generate_domain_gap(domain_result, gap_index)
            gaps.append(gap)
            gap_index += 1
        else:
            covered_domains.append({
                "domain_id": domain_result.get("domain_id", ""),
                "domain_name": domain_result.get("domain_name", ""),
                "coverage_score": domain_result.get("coverage_score", 0.0),
                "coverage_level": level,
                "priority_level": domain_result.get("priority_level", ""),
            })

    prioritised_gaps = prioritise_gaps(gaps)

    critical_gaps = [g for g in gaps if g["gap_severity"] == "Critical gap"]
    high_gaps = [g for g in gaps if g["gap_severity"] == "High gap"]
    medium_gaps = [g for g in gaps if g["gap_severity"] == "Medium gap"]
    low_gaps = [g for g in gaps if g["gap_severity"] == "Low gap"]

    high_priority_gaps = [g for g in gaps if g["priority_level"] == "High"]

    gap_themes = _derive_gap_themes(gaps)
    recommended_focus = _derive_recommended_focus(gaps)

    return {
        "organisation_name": org_name,
        "policy_pack_title": pack_title,
        "overall_coverage_score": overall_score,
        "overall_coverage_level": overall_level,
        "total_domains_reviewed": len(domain_results),
        "total_gaps": len(gaps),
        "critical_gaps": critical_gaps,
        "high_gaps": high_gaps,
        "medium_gaps": medium_gaps,
        "low_gaps": low_gaps,
        "prioritised_gaps": prioritised_gaps,
        "covered_domains": covered_domains,
        "high_priority_gaps": high_priority_gaps,
        "gap_themes": gap_themes,
        "recommended_focus": recommended_focus,
        "responsible_use_note": responsible_use_note,
        "prototype_note": prototype_note,
    }


def summarise_gap_analysis(gap_analysis: dict) -> dict:
    """Return a compact summary of the gap analysis results."""
    if not isinstance(gap_analysis, dict):
        gap_analysis = {}

    critical_gaps = gap_analysis.get("critical_gaps", []) or []
    high_gaps = gap_analysis.get("high_gaps", []) or []
    medium_gaps = gap_analysis.get("medium_gaps", []) or []
    low_gaps = gap_analysis.get("low_gaps", []) or []

    critical_count = len(critical_gaps)
    high_count = len(high_gaps)
    medium_count = len(medium_gaps)
    low_count = len(low_gaps)
    total_gaps = critical_count + high_count + medium_count + low_count

    covered_count = len(gap_analysis.get("covered_domains", []) or [])

    prioritised = gap_analysis.get("prioritised_gaps", []) or (
        critical_gaps + high_gaps + medium_gaps + low_gaps
    )
    highest_priority_gap = prioritised[0] if prioritised else {}
    top_gap_domains = [g.get("domain_name", "") for g in prioritised[:3]]

    if critical_count > 0 or high_count > 0:
        overall_gap_position = (
            "The policy pack has priority governance gaps that should be addressed "
            "before wider AI adoption is encouraged."
        )
    elif medium_count > 0 or low_count > 0:
        overall_gap_position = (
            "The policy pack contains useful foundations, but several areas need clearer "
            "operational detail before scaling AI use."
        )
    else:
        overall_gap_position = (
            "The policy pack appears to cover most framework areas, subject to human "
            "review and responsible-owner approval."
        )

    return {
        "total_gaps": total_gaps,
        "critical_gap_count": critical_count,
        "high_gap_count": high_count,
        "medium_gap_count": medium_count,
        "low_gap_count": low_count,
        "covered_domain_count": covered_count,
        "highest_priority_gap": highest_priority_gap,
        "top_gap_domains": top_gap_domains,
        "gap_themes": gap_analysis.get("gap_themes", []),
        "overall_gap_position": overall_gap_position,
        "recommended_focus": gap_analysis.get("recommended_focus", []),
    }


def prioritise_gaps(gaps: list) -> list:
    """Return gaps sorted by gap_priority_score descending."""
    if not gaps:
        return []
    return sorted(gaps, key=lambda g: g.get("gap_priority_score", 0), reverse=True)


def _render_gap_section_md(title: str, gaps: list) -> list:
    """Render a gap severity section as Markdown lines."""
    lines = ["", "---", "", f"## {title}", ""]
    if not gaps:
        lines.append(f"No {title.lower()} identified.")
        return lines
    for gap in gaps:
        matched = gap.get("matched_policies", [])
        snippets = gap.get("evidence_snippets", [])
        lines.extend([
            f"### {gap.get('gap_id', '')} — {gap.get('domain_name', '')}",
            "",
            f"**Domain:** {gap.get('domain_id', '')} — {gap.get('domain_name', '')}",
            f"**Priority:** {gap.get('priority_level', '')}",
            f"**Coverage score:** {gap.get('coverage_score', 0)}/100",
            f"**Coverage level:** {gap.get('coverage_level', '')}",
            f"**Gap type:** {gap.get('gap_type', '')}",
            f"**Gap severity:** {gap.get('gap_severity', '')}",
            f"**Priority score:** {gap.get('gap_priority_score', 0)}/100",
            "",
            f"**Missing evidence:** {gap.get('missing_evidence', '')}",
            "",
            f"**Risk statement:** {gap.get('risk_statement', '')}",
            "",
            f"**Action hint:** {gap.get('action_hint', '')}",
            "",
            (
                f"**Matched policies:** {', '.join(matched)}"
                if matched else "**Matched policies:** None found"
            ),
            "",
        ])
        if snippets:
            lines.append("**Evidence snippets:**")
            for s in snippets:
                lines.append(f"> {s}")
            lines.append("")
        lines.append(f"*{gap.get('review_note', '')}*")
        lines.append("")
    return lines


def format_gap_analysis_as_markdown(
    gap_analysis: dict, summary: dict | None = None
) -> str:
    """Return a full Markdown gap analysis report."""
    if not isinstance(gap_analysis, dict):
        gap_analysis = {}
    if summary is None:
        summary = summarise_gap_analysis(gap_analysis)

    org_name = gap_analysis.get("organisation_name", "Unnamed organisation")
    pack_title = gap_analysis.get("policy_pack_title", "")
    overall_score = gap_analysis.get("overall_coverage_score", 0)
    overall_level = gap_analysis.get("overall_coverage_level", "")
    total_domains = gap_analysis.get("total_domains_reviewed", 0)

    lines = [
        "# AI Governance Policy Gap Analysis",
        "",
        "## Review Overview",
        "",
        f"**Organisation:** {org_name}",
        f"**Policy Pack:** {pack_title}",
        f"**Governance domains reviewed:** {total_domains}",
        f"**Overall coverage score:** {overall_score}/100",
        f"**Overall coverage level:** {overall_level}",
        "",
        "---",
        "",
        "## Gap Summary",
        "",
        f"**Total gaps identified:** {summary.get('total_gaps', 0)}",
        f"**Critical gaps:** {summary.get('critical_gap_count', 0)}",
        f"**High gaps:** {summary.get('high_gap_count', 0)}",
        f"**Medium gaps:** {summary.get('medium_gap_count', 0)}",
        f"**Low gaps:** {summary.get('low_gap_count', 0)}",
        f"**Domains with sufficient coverage:** {summary.get('covered_domain_count', 0)}",
        "",
        "---",
        "",
        "## Overall Gap Position",
        "",
        summary.get("overall_gap_position", ""),
        "",
        "---",
        "",
        "## Recommended Focus Areas",
        "",
    ]
    for focus in summary.get("recommended_focus", []):
        lines.append(f"- {focus}")

    lines.extend(["", "---", "", "## Gap Themes", ""])
    for theme in summary.get("gap_themes", []):
        lines.append(f"- {theme}")

    lines.extend([
        "",
        "---",
        "",
        "## Prioritised Gaps",
        "",
        "| Gap ID | Domain | Priority | Score | Coverage Level | Severity |",
        "|---|---|---|---|---|---|",
    ])
    for gap in gap_analysis.get("prioritised_gaps", []):
        lines.append(
            f"| {gap.get('gap_id', '')} "
            f"| {gap.get('domain_name', '')} "
            f"| {gap.get('priority_level', '')} "
            f"| {gap.get('coverage_score', 0)}/100 "
            f"| {gap.get('coverage_level', '')} "
            f"| {gap.get('gap_severity', '')} |"
        )

    lines.extend(_render_gap_section_md("Critical Gaps", gap_analysis.get("critical_gaps", [])))
    lines.extend(_render_gap_section_md("High Gaps", gap_analysis.get("high_gaps", [])))
    lines.extend(_render_gap_section_md("Medium Gaps", gap_analysis.get("medium_gaps", [])))
    lines.extend(_render_gap_section_md("Low Gaps", gap_analysis.get("low_gaps", [])))

    lines.extend([
        "",
        "---",
        "",
        "## Covered Domains",
        "",
        "| Domain | Priority | Coverage Score | Coverage Level |",
        "|---|---|---|---|",
    ])
    covered = gap_analysis.get("covered_domains", [])
    if covered:
        for d in covered:
            lines.append(
                f"| {d.get('domain_name', '')} "
                f"| {d.get('priority_level', '')} "
                f"| {d.get('coverage_score', 0)}/100 "
                f"| {d.get('coverage_level', '')} |"
            )
    else:
        lines.append("No domains with strong coverage identified.")

    lines.extend([
        "",
        "---",
        "",
        "## Detailed Gap Notes",
        "",
        "See Critical, High, Medium, and Low Gaps sections above for full per-domain detail.",
        "",
        "---",
        "",
        "## Responsible-Use Boundaries",
        "",
        _RESPONSIBLE_USE_NOTE,
        "",
        _PROTOTYPE_NOTE,
        "",
        "Human review remains required before any real-world use.",
        "",
        "---",
        "",
        "*Build 6 · AI Governance Policy Checker · BrightPath ChatGPT Mastery Project*",
        "*Synthetic scenarios only. Human review required before any real-world use.*",
    ])

    return "\n".join(lines)
