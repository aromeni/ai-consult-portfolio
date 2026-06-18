"""
Governance Maturity — AI Governance Policy Checker
Build 6 · BrightPath ChatGPT Mastery Project

Calculates an overall AI governance maturity score from policy coverage results,
gap analysis, and policy recommendations. Generates domain-level maturity scores,
strengths, weaknesses, maturity blockers, improvement priorities, and
adoption-readiness guidance.

Deterministic only. No external AI, LLM, or API calls.
Synthetic/demo data only.
"""

_RESPONSIBLE_USE_NOTE = (
    "This maturity summary is generated from synthetic/demo policy text only. "
    "It must not be used with real client policies, learner data, safeguarding "
    "case details, staff HR data, personal data, confidential data, or regulated "
    "information without appropriate governance, approvals, and responsible owners."
)

_PROTOTYPE_NOTE = (
    "This prototype does not provide legal, safeguarding, HR, compliance, "
    "data-protection, financial, medical, academic-integrity, or professional "
    "governance advice. This is a deterministic governance maturity support tool, "
    "not a compliance certification system. Human review remains required before "
    "any real-world use."
)

_MATURITY_LEVELS = [
    (90, "Optimised governance"),
    (75, "Managed governance"),
    (50, "Defined governance"),
    (25, "Developing governance"),
    (0, "Initial governance"),
]

_MATURITY_DESCRIPTIONS = {
    "Initial governance": (
        "AI governance is at an early stage. Policies provide little reliable evidence "
        "of responsible-use controls. The organisation should not scale AI use until "
        "core governance foundations are established."
    ),
    "Developing governance": (
        "Some responsible AI policy foundations are present, but significant gaps remain. "
        "The organisation should focus on policy clarity, ownership, data boundaries, "
        "safeguarding boundaries, and human review before wider adoption."
    ),
    "Defined governance": (
        "The organisation has a reasonable governance baseline. Controlled pilots may be "
        "appropriate, provided high-priority gaps are addressed and responsible owners "
        "review the controls."
    ),
    "Managed governance": (
        "The organisation has strong governance coverage across most reviewed areas. "
        "AI pilots and limited scaling may be appropriate with monitoring, training, "
        "incident reporting, and periodic review."
    ),
    "Optimised governance": (
        "The organisation has very strong governance coverage and review mechanisms. "
        "Continued monitoring, evidence review, and responsible-owner oversight remain required."
    ),
}

_MATURITY_COLOURS = {
    "Initial governance": "red",
    "Developing governance": "orange",
    "Defined governance": "blue",
    "Managed governance": "green",
    "Optimised governance": "green",
}

_ADOPTION_READINESS = {
    "Initial governance": (
        "The organisation should not scale AI use yet. It should first establish core "
        "governance controls, approved-use guidance, data boundaries, safeguarding "
        "escalation, human review, and incident reporting."
    ),
    "Developing governance": (
        "The organisation may continue limited exploration, but controlled pilots should "
        "only proceed after high-priority gaps are addressed and responsible owners "
        "approve the pilot scope."
    ),
    "Defined governance": (
        "The organisation may be ready for narrow controlled pilots, provided priority "
        "gaps are addressed, staff are trained, and human review is required."
    ),
    "Managed governance": (
        "The organisation appears ready for structured pilots and limited scaling, "
        "subject to monitoring, staff training, and periodic governance review."
    ),
    "Optimised governance": (
        "The organisation appears well positioned for responsible AI adoption, subject "
        "to continued monitoring, evidence review, and accountable human ownership."
    ),
}

_DOMAIN_WEIGHTS = {
    "High": 1.5,
    "Medium": 1.0,
    "Low": 0.75,
}

_GAP_PENALTIES = {
    "Critical gap": 25,
    "High gap": 15,
    "Medium gap": 8,
    "Low gap": 3,
}

_REC_PENALTIES = {
    "Urgent": 15,
    "High priority": 10,
    "Medium priority": 5,
    "Low priority": 2,
}


def classify_governance_maturity_level(score: float) -> str:
    """Map a 0–100 score to a governance maturity level label."""
    for threshold, level in _MATURITY_LEVELS:
        if score >= threshold:
            return level
    return "Initial governance"


def get_maturity_level_description(maturity_level: str) -> str:
    """Return the description for a given maturity level."""
    return _MATURITY_DESCRIPTIONS.get(
        maturity_level,
        "No description available for this maturity level.",
    )


def get_maturity_level_colour(maturity_level: str) -> str:
    """Return a colour label (red/orange/blue/green) for a maturity level."""
    return _MATURITY_COLOURS.get(maturity_level, "blue")


def calculate_domain_maturity_score(
    domain_result: dict,
    related_gaps: list[dict] | None = None,
    related_recommendations: list[dict] | None = None,
) -> dict:
    """
    Calculate maturity score for a single governance domain.

    Starts from coverage_score and applies penalties for gaps and recommendations.
    Adds an extra penalty for High-priority domains below 50.
    """
    domain_id = domain_result.get("domain_id", "")
    domain_name = domain_result.get("domain_name", "")
    priority_level = domain_result.get("priority_level", "Medium")
    coverage_score = int(domain_result.get("coverage_score", 0))
    coverage_level = domain_result.get("coverage_level", "Not covered")

    score = float(coverage_score)

    related_gap_severity = ""
    if related_gaps:
        gap = related_gaps[0]
        related_gap_severity = gap.get("gap_severity", "")
        penalty = _GAP_PENALTIES.get(related_gap_severity, 0)
        score -= penalty

    related_recommendation_priority = ""
    if related_recommendations:
        rec = related_recommendations[0]
        related_recommendation_priority = rec.get("recommendation_priority", "")
        penalty = _REC_PENALTIES.get(related_recommendation_priority, 0)
        score -= penalty

    if priority_level == "High" and coverage_score < 50:
        score -= 10

    maturity_score = max(0, min(100, int(round(score))))
    maturity_level = classify_governance_maturity_level(maturity_score)

    maturity_explanation = _build_domain_explanation(
        domain_name,
        coverage_level,
        coverage_score,
        maturity_score,
        maturity_level,
        related_gap_severity,
        related_recommendation_priority,
    )

    recommended_focus = _build_domain_recommended_focus(
        maturity_level, related_gap_severity, domain_name
    )

    return {
        "domain_id": domain_id,
        "domain_name": domain_name,
        "priority_level": priority_level,
        "coverage_score": coverage_score,
        "coverage_level": coverage_level,
        "maturity_score": maturity_score,
        "maturity_level": maturity_level,
        "related_gap_severity": related_gap_severity,
        "related_recommendation_priority": related_recommendation_priority,
        "maturity_explanation": maturity_explanation,
        "recommended_focus": recommended_focus,
    }


def _build_domain_explanation(
    domain_name: str,
    coverage_level: str,
    coverage_score: int,
    maturity_score: int,
    maturity_level: str,
    gap_severity: str,
    rec_priority: str,
) -> str:
    parts = [
        f"{domain_name} has a coverage score of {coverage_score}/100 ({coverage_level}).",
    ]
    if gap_severity:
        parts.append(f"A {gap_severity.lower()} has been identified.")
    if rec_priority:
        parts.append(
            f"A {rec_priority.lower()} recommendation is in place to address this gap."
        )
    parts.append(
        f"The domain maturity score is {maturity_score}/100, "
        f"classified as {maturity_level}."
    )
    return " ".join(parts)


def _build_domain_recommended_focus(
    maturity_level: str, gap_severity: str, domain_name: str
) -> str:
    if maturity_level in ("Initial governance", "Developing governance"):
        if gap_severity in ("Critical gap", "High gap"):
            return (
                f"Address the {gap_severity.lower()} in {domain_name} as a priority. "
                "Establish or strengthen policy coverage before wider AI use."
            )
        return (
            f"Strengthen policy coverage for {domain_name} to raise maturity level."
        )
    if maturity_level == "Defined governance":
        return (
            f"Review and clarify {domain_name} policy wording to move towards Managed governance."
        )
    if maturity_level == "Managed governance":
        return f"Monitor {domain_name} controls and review periodically."
    return f"Maintain and review {domain_name} governance evidence regularly."


def calculate_overall_governance_score(domain_scores: list[dict]) -> float:
    """
    Calculate a weighted average maturity score across all domains.

    High-priority domains are weighted 1.5, Medium 1.0, Low 0.75.
    Returns 0.0 if no valid scores exist.
    """
    if not domain_scores:
        return 0.0

    total_weighted = 0.0
    total_weight = 0.0

    for ds in domain_scores:
        weight = _DOMAIN_WEIGHTS.get(ds.get("priority_level", "Medium"), 1.0)
        maturity_score = ds.get("maturity_score", 0)
        total_weighted += maturity_score * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return round(total_weighted / total_weight, 1)


def identify_maturity_strengths(
    domain_scores: list[dict],
    threshold: int = 75,
) -> list[dict]:
    """Return domains with maturity_score >= threshold, sorted descending by score."""
    strengths = [
        ds for ds in domain_scores if ds.get("maturity_score", 0) >= threshold
    ]
    return sorted(strengths, key=lambda x: x.get("maturity_score", 0), reverse=True)


def identify_maturity_weaknesses(
    domain_scores: list[dict],
    threshold: int = 50,
) -> list[dict]:
    """Return domains with maturity_score < threshold, sorted ascending by score."""
    weaknesses = [
        ds for ds in domain_scores if ds.get("maturity_score", 0) < threshold
    ]
    return sorted(weaknesses, key=lambda x: x.get("maturity_score", 0))


def identify_maturity_blockers(
    gap_analysis: dict | None = None,
    recommendations: dict | None = None,
) -> list[dict]:
    """
    Identify critical gaps, high gaps, urgent recommendations, and high-priority
    recommendations as maturity blockers.
    """
    blockers = []
    blocker_num = 1

    if gap_analysis:
        prioritised_gaps = gap_analysis.get("prioritised_gaps", [])
        for gap in prioritised_gaps:
            severity = gap.get("gap_severity", "")
            if severity in ("Critical gap", "High gap"):
                blockers.append({
                    "blocker_id": f"BLOCKER-{blocker_num:03d}",
                    "domain_name": gap.get("domain_name", ""),
                    "blocker_type": severity,
                    "reason": (
                        f"{gap.get('domain_name', '')} has a {severity.lower()} "
                        f"(coverage score: {gap.get('coverage_score', 0)}/100). "
                        f"{gap.get('risk_statement', '')}"
                    ),
                    "recommended_action": gap.get("action_hint", "Address this gap before wider AI rollout."),
                })
                blocker_num += 1

    if recommendations:
        prioritised_recs = recommendations.get("prioritised_recommendations", [])
        for rec in prioritised_recs:
            priority = rec.get("recommendation_priority", "")
            if priority in ("Urgent", "High priority"):
                domain = rec.get("domain_name", "")
                # Skip if already captured via gap blocker for same domain
                already = any(b["domain_name"] == domain for b in blockers)
                if not already:
                    blockers.append({
                        "blocker_id": f"BLOCKER-{blocker_num:03d}",
                        "domain_name": domain,
                        "blocker_type": f"{priority} recommendation",
                        "reason": (
                            f"A {priority.lower()} recommendation is in place for {domain}. "
                            f"{rec.get('rationale', '')}"
                        ),
                        "recommended_action": (
                            f"Action: {rec.get('policy_action_type', '')} — "
                            f"Target: {rec.get('target_policy', '')}."
                        ),
                    })
                    blocker_num += 1

    return blockers


def generate_maturity_improvement_priorities(maturity_summary: dict) -> list[str]:
    """Generate a prioritised list of improvement actions from maturity summary."""
    priorities = []

    blockers = maturity_summary.get("maturity_blockers", [])
    for blocker in blockers[:3]:
        priorities.append(
            f"Address {blocker['blocker_type'].lower()} in "
            f"{blocker['domain_name']} — {blocker['recommended_action']}"
        )

    weaknesses = maturity_summary.get("maturity_weaknesses", [])
    for weakness in weaknesses[:3]:
        name = weakness.get("domain_name", "")
        score = weakness.get("maturity_score", 0)
        if not any(name in p for p in priorities):
            priorities.append(
                f"Strengthen {name} policy coverage (current maturity score: {score}/100)."
            )

    level = maturity_summary.get("overall_maturity_level", "")
    if level in ("Initial governance", "Developing governance"):
        priorities.append(
            "Establish clear AI policy ownership and senior leadership accountability."
        )
        priorities.append(
            "Define data boundaries, safeguarding escalation routes, and human review requirements."
        )
    elif level == "Defined governance":
        priorities.append(
            "Move towards Managed governance by adding staff training, "
            "monitoring, and incident reporting."
        )
    elif level == "Managed governance":
        priorities.append(
            "Review and evidence monitoring, training, and continuous improvement cycles "
            "to move towards Optimised governance."
        )

    return priorities[:8]


def generate_adoption_readiness_position(
    maturity_level: str,
    blockers: list[dict],
) -> str:
    """Generate practical consulting guidance on AI adoption readiness."""
    base = _ADOPTION_READINESS.get(
        maturity_level,
        "Adoption readiness cannot be determined from the current data.",
    )

    critical_blockers = [
        b for b in blockers if b.get("blocker_type") in ("Critical gap", "High gap")
    ]
    if critical_blockers:
        blocker_names = ", ".join(
            b["domain_name"] for b in critical_blockers[:3]
        )
        return (
            f"{base} Critical blockers are present in: {blocker_names}. "
            "These should be addressed before wider AI use or pilot scaling."
        )

    return base


def _get_recommended_next_step(maturity_level: str, blockers: list[dict]) -> str:
    if blockers:
        first = blockers[0]
        return (
            f"Address the {first['blocker_type'].lower()} in {first['domain_name']} "
            f"as the immediate next step. {first['recommended_action']}"
        )
    next_steps = {
        "Initial governance": (
            "Establish a named AI governance owner and draft core policy controls "
            "covering approved use, data boundaries, safeguarding, and human review."
        ),
        "Developing governance": (
            "Close the highest-priority policy gaps and confirm responsible owners "
            "for each governance domain before proceeding to controlled pilots."
        ),
        "Defined governance": (
            "Address remaining medium-priority gaps and strengthen staff training, "
            "monitoring, and incident reporting to move towards Managed governance."
        ),
        "Managed governance": (
            "Evidence monitoring cycles and continuous improvement reviews "
            "to consolidate Managed governance maturity."
        ),
        "Optimised governance": (
            "Maintain periodic evidence review, update policies as AI tools and "
            "guidance evolve, and ensure continued responsible-owner oversight."
        ),
    }
    return next_steps.get(maturity_level, "Review the maturity summary and act on the highest-priority recommendations.")


def generate_governance_maturity_summary(
    coverage_results: dict,
    gap_analysis: dict | None = None,
    recommendations: dict | None = None,
) -> dict:
    """
    Build a full governance maturity summary from coverage results, gap analysis,
    and policy recommendations.
    """
    organisation_name = coverage_results.get("organisation_name", "Unnamed organisation")
    policy_pack_title = coverage_results.get("policy_pack_title", "Unnamed policy pack")

    domain_results = coverage_results.get("domain_results", [])
    if not domain_results:
        return _empty_maturity_summary(organisation_name, policy_pack_title)

    # Index gaps and recommendations by domain_name for quick lookup
    gaps_by_domain: dict[str, list[dict]] = {}
    if gap_analysis:
        for gap in gap_analysis.get("prioritised_gaps", []):
            name = gap.get("domain_name", "")
            gaps_by_domain.setdefault(name, []).append(gap)

    recs_by_domain: dict[str, list[dict]] = {}
    if recommendations:
        for rec in recommendations.get("prioritised_recommendations", []):
            name = rec.get("domain_name", "")
            recs_by_domain.setdefault(name, []).append(rec)

    domain_scores = []
    for dr in domain_results:
        name = dr.get("domain_name", "")
        related_gaps = gaps_by_domain.get(name)
        related_recs = recs_by_domain.get(name)
        ds = calculate_domain_maturity_score(dr, related_gaps, related_recs)
        domain_scores.append(ds)

    overall_score = calculate_overall_governance_score(domain_scores)
    maturity_level = classify_governance_maturity_level(overall_score)
    maturity_description = get_maturity_level_description(maturity_level)

    strengths = identify_maturity_strengths(domain_scores)
    weaknesses = identify_maturity_weaknesses(domain_scores)
    blockers = identify_maturity_blockers(gap_analysis, recommendations)

    partial_summary = {
        "overall_maturity_level": maturity_level,
        "maturity_blockers": blockers,
        "maturity_weaknesses": weaknesses,
    }
    improvement_priorities = generate_maturity_improvement_priorities(partial_summary)
    adoption_position = generate_adoption_readiness_position(maturity_level, blockers)
    recommended_next_step = _get_recommended_next_step(maturity_level, blockers)

    return {
        "organisation_name": organisation_name,
        "policy_pack_title": policy_pack_title,
        "overall_governance_score": overall_score,
        "overall_maturity_level": maturity_level,
        "maturity_description": maturity_description,
        "domain_maturity_scores": domain_scores,
        "maturity_strengths": strengths,
        "maturity_weaknesses": weaknesses,
        "maturity_blockers": blockers,
        "improvement_priorities": improvement_priorities,
        "adoption_readiness_position": adoption_position,
        "recommended_next_step": recommended_next_step,
        "responsible_use_note": _RESPONSIBLE_USE_NOTE,
        "prototype_note": _PROTOTYPE_NOTE,
    }


def _empty_maturity_summary(organisation_name: str, policy_pack_title: str) -> dict:
    return {
        "organisation_name": organisation_name,
        "policy_pack_title": policy_pack_title,
        "overall_governance_score": 0.0,
        "overall_maturity_level": "Initial governance",
        "maturity_description": get_maturity_level_description("Initial governance"),
        "domain_maturity_scores": [],
        "maturity_strengths": [],
        "maturity_weaknesses": [],
        "maturity_blockers": [],
        "improvement_priorities": [],
        "adoption_readiness_position": _ADOPTION_READINESS["Initial governance"],
        "recommended_next_step": (
            "No domain results found. Load the policy pack, governance framework, "
            "and run the policy coverage check first."
        ),
        "responsible_use_note": _RESPONSIBLE_USE_NOTE,
        "prototype_note": _PROTOTYPE_NOTE,
    }


def summarise_governance_maturity(maturity_summary: dict) -> dict:
    """Extract summary statistics from a governance maturity summary."""
    domain_scores = maturity_summary.get("domain_maturity_scores", [])

    level_counts: dict[str, int] = {
        "managed_or_optimised_domains": 0,
        "defined_domains": 0,
        "developing_domains": 0,
        "initial_domains": 0,
    }
    for ds in domain_scores:
        level = ds.get("maturity_level", "")
        if level in ("Managed governance", "Optimised governance"):
            level_counts["managed_or_optimised_domains"] += 1
        elif level == "Defined governance":
            level_counts["defined_domains"] += 1
        elif level == "Developing governance":
            level_counts["developing_domains"] += 1
        else:
            level_counts["initial_domains"] += 1

    strengths = maturity_summary.get("maturity_strengths", [])
    weaknesses = maturity_summary.get("maturity_weaknesses", [])
    blockers = maturity_summary.get("maturity_blockers", [])

    strongest = strengths[0] if strengths else {}
    weakest = weaknesses[0] if weaknesses else {}

    overall_score = maturity_summary.get("overall_governance_score", 0)
    overall_level = maturity_summary.get("overall_maturity_level", "Initial governance")

    if overall_score >= 75:
        overall_position = (
            f"Overall governance score: {overall_score}/100. "
            f"The organisation is at {overall_level}. "
            "Strong coverage across most reviewed areas."
        )
    elif overall_score >= 50:
        overall_position = (
            f"Overall governance score: {overall_score}/100. "
            f"The organisation is at {overall_level}. "
            "A reasonable baseline exists, but gaps remain."
        )
    elif overall_score >= 25:
        overall_position = (
            f"Overall governance score: {overall_score}/100. "
            f"The organisation is at {overall_level}. "
            "Significant gaps require attention before wider AI adoption."
        )
    else:
        overall_position = (
            f"Overall governance score: {overall_score}/100. "
            f"The organisation is at {overall_level}. "
            "Core governance foundations need to be established."
        )

    # Recommended focus derived from weaknesses and blockers
    recommended_focus = []
    for blocker in blockers[:2]:
        recommended_focus.append(
            f"Address {blocker['blocker_type'].lower()} in {blocker['domain_name']}"
        )
    for weakness in weaknesses[:2]:
        name = weakness.get("domain_name", "")
        if not any(name in f for f in recommended_focus):
            recommended_focus.append(f"Strengthen {name} policy coverage")
    recommended_focus = recommended_focus[:4]

    return {
        "overall_governance_score": overall_score,
        "overall_maturity_level": overall_level,
        "total_domains": len(domain_scores),
        "managed_or_optimised_domains": level_counts["managed_or_optimised_domains"],
        "defined_domains": level_counts["defined_domains"],
        "developing_domains": level_counts["developing_domains"],
        "initial_domains": level_counts["initial_domains"],
        "strength_count": len(strengths),
        "weakness_count": len(weaknesses),
        "blocker_count": len(blockers),
        "strongest_domain": strongest,
        "weakest_domain": weakest,
        "overall_position": overall_position,
        "recommended_focus": recommended_focus,
    }


def format_governance_maturity_as_markdown(
    maturity_summary: dict,
    summary: dict | None = None,
) -> str:
    """Format the governance maturity summary as a Markdown report."""
    if summary is None:
        summary = summarise_governance_maturity(maturity_summary)

    org = maturity_summary.get("organisation_name", "Unnamed organisation")
    pack = maturity_summary.get("policy_pack_title", "Unnamed policy pack")
    score = maturity_summary.get("overall_governance_score", 0)
    level = maturity_summary.get("overall_maturity_level", "")
    description = maturity_summary.get("maturity_description", "")
    adoption = maturity_summary.get("adoption_readiness_position", "")
    next_step = maturity_summary.get("recommended_next_step", "")
    domain_scores = maturity_summary.get("domain_maturity_scores", [])
    strengths = maturity_summary.get("maturity_strengths", [])
    weaknesses = maturity_summary.get("maturity_weaknesses", [])
    blockers = maturity_summary.get("maturity_blockers", [])
    priorities = maturity_summary.get("improvement_priorities", [])
    responsible_use_note = maturity_summary.get("responsible_use_note", _RESPONSIBLE_USE_NOTE)
    prototype_note = maturity_summary.get("prototype_note", _PROTOTYPE_NOTE)

    lines = [
        "# AI Governance Maturity Summary",
        "",
        "---",
        "",
        "## Review Overview",
        "",
        f"**Organisation:** {org}",
        f"**Policy Pack:** {pack}",
        f"**Domains Reviewed:** {summary.get('total_domains', 0)}",
        "",
        "---",
        "",
        "## Overall Governance Score",
        "",
        f"**{score}/100**",
        "",
        "---",
        "",
        "## Maturity Level",
        "",
        f"**{level}**",
        "",
        "---",
        "",
        "## Maturity Description",
        "",
        description,
        "",
        "---",
        "",
        "## Adoption Readiness Position",
        "",
        adoption,
        "",
        "---",
        "",
        "## Recommended Next Step",
        "",
        next_step,
        "",
        "---",
        "",
        "## Governance Strengths",
        "",
    ]

    if strengths:
        for s in strengths:
            lines.append(
                f"- **{s.get('domain_name', '')}** — "
                f"maturity score {s.get('maturity_score', 0)}/100 "
                f"({s.get('maturity_level', '')})"
            )
    else:
        lines.append("No domains currently meeting the strength threshold.")

    lines += [
        "",
        "---",
        "",
        "## Governance Weaknesses",
        "",
    ]

    if weaknesses:
        for w in weaknesses:
            lines.append(
                f"- **{w.get('domain_name', '')}** — "
                f"maturity score {w.get('maturity_score', 0)}/100 "
                f"({w.get('maturity_level', '')})"
            )
    else:
        lines.append("No domains currently below the weakness threshold.")

    lines += [
        "",
        "---",
        "",
        "## Maturity Blockers",
        "",
    ]

    if blockers:
        for b in blockers:
            lines += [
                f"### {b.get('blocker_id', '')} — {b.get('domain_name', '')}",
                "",
                f"**Blocker type:** {b.get('blocker_type', '')}",
                "",
                f"**Reason:** {b.get('reason', '')}",
                "",
                f"**Recommended action:** {b.get('recommended_action', '')}",
                "",
            ]
    else:
        lines.append("No maturity blockers identified.")

    lines += [
        "",
        "---",
        "",
        "## Improvement Priorities",
        "",
    ]

    if priorities:
        for p in priorities:
            lines.append(f"- {p}")
    else:
        lines.append("No improvement priorities generated.")

    lines += [
        "",
        "---",
        "",
        "## Domain Maturity Scores",
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

    lines += [
        "",
        "---",
        "",
        "## Detailed Domain Notes",
        "",
    ]

    for ds in domain_scores:
        lines += [
            f"### {ds.get('domain_id', '')} — {ds.get('domain_name', '')}",
            "",
            ds.get("maturity_explanation", ""),
            "",
            f"**Recommended focus:** {ds.get('recommended_focus', '')}",
            "",
        ]

    lines += [
        "---",
        "",
        "## Responsible-Use Boundaries",
        "",
        responsible_use_note,
        "",
        prototype_note,
        "",
        "Human review remains required before any real-world use.",
        "",
        "---",
        "",
        "*Build 6 · AI Governance Policy Checker · BrightPath ChatGPT Mastery Project*",
        "*Synthetic scenarios only. Human review required before any real-world use.*",
    ]

    return "\n".join(lines)
