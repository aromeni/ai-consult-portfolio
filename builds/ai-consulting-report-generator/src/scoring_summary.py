"""AI readiness scoring, classification, and interpretation — Build 5."""

from __future__ import annotations

_CATEGORY_KEYS = [
    "strategy_score",
    "data_governance_score",
    "staff_capability_score",
    "workflow_opportunity_score",
    "risk_management_score",
    "leadership_alignment_score",
]

_CATEGORY_LABELS = {
    "strategy_score": "Strategy and leadership",
    "data_governance_score": "Data governance",
    "staff_capability_score": "Staff capability",
    "workflow_opportunity_score": "Workflow opportunity",
    "risk_management_score": "Risk management",
    "leadership_alignment_score": "Leadership alignment",
    "overall_readiness_score": "Overall AI readiness",
}

_LEVEL_DESCRIPTIONS = {
    "Low readiness": (
        "The organisation is at an early stage of AI readiness. Foundational governance, skills, "
        "process clarity, and risk controls should be established before wider AI adoption."
    ),
    "Developing readiness": (
        "The organisation has some foundations in place but needs clearer governance, staff "
        "guidance, workflow prioritisation, and risk controls before scaling AI use."
    ),
    "Moderate readiness": (
        "The organisation has useful foundations and can begin structured pilots, but should "
        "improve governance, measurement, staff capability, and risk management."
    ),
    "Strong readiness": (
        "The organisation appears well positioned for structured AI adoption, subject to continued "
        "governance, monitoring, staff training, and responsible-owner review."
    ),
}

_LEVEL_COLOURS = {
    "Low readiness": "#dc2626",
    "Developing readiness": "#f59e0b",
    "Moderate readiness": "#3b82f6",
    "Strong readiness": "#16a34a",
}

_STRENGTH_REASONS = {
    "strategy_score": "A strategic foundation for AI adoption appears to be in place.",
    "data_governance_score": "Data governance foundations appear relatively strong for this stage.",
    "staff_capability_score": "Staff capability is strong — a good foundation for structured pilots.",
    "workflow_opportunity_score": "Strong workflow opportunity suggests clear AI use cases are available.",
    "risk_management_score": "Risk management foundations appear relatively strong.",
    "leadership_alignment_score": "Leadership alignment supports responsible AI adoption.",
}

_GAP_RISKS = {
    "strategy_score": "Without a clear AI strategy, adoption may be fragmented and ungoverned.",
    "data_governance_score": "Poor data governance increases GDPR risk and may expose sensitive or personal data.",
    "staff_capability_score": "Staff may misuse AI tools or fail to recognise output errors without training.",
    "workflow_opportunity_score": "Low workflow opportunity may limit the business case for AI investment.",
    "risk_management_score": "Inadequate risk controls could lead to misuse, harm, or compliance breaches.",
    "leadership_alignment_score": "Without leadership alignment, governance and resource allocation may stall.",
}

_GAP_ACTIONS = {
    "strategy_score": "Define an AI vision, governance framework, and approved-use policy.",
    "data_governance_score": "Establish data classifications, DPIA requirements, and approved AI tool criteria.",
    "staff_capability_score": (
        "Deliver targeted AI awareness training covering safe prompting, data boundaries, "
        "approved tools, and escalation routes."
    ),
    "workflow_opportunity_score": "Identify and map repetitive, low-risk workflows suitable for AI assistance.",
    "risk_management_score": (
        "Complete a risk register, assign owners, and define acceptable-use and incident-reporting processes."
    ),
    "leadership_alignment_score": (
        "Secure executive sponsorship and assign a named responsible owner for AI governance."
    ),
}

_CATEGORY_INTERPRETATIONS = {
    "strategy_score": {
        "low": (
            "AI strategy appears to be underdeveloped. The organisation should define its AI vision, "
            "governance framework, and responsible-use boundaries before broader adoption."
        ),
        "developing": (
            "AI strategy is emerging but not yet formalised. Defining approved use cases, "
            "governance roles, and success criteria will support safe, structured adoption."
        ),
        "moderate": (
            "A strategic foundation exists. Strengthening governance documentation, leadership "
            "ownership, and measurable outcomes will support the next stage of AI adoption."
        ),
        "strong": (
            "Strong strategic foundations are in place. Continue refining governance, "
            "monitoring outcomes, and updating the AI strategy as tools and regulations evolve."
        ),
    },
    "data_governance_score": {
        "low": (
            "Data governance appears to be a key constraint. The organisation should clarify what "
            "data can and cannot be used with AI tools, define approval routes, and avoid using "
            "sensitive or personal data in uncontrolled systems."
        ),
        "developing": (
            "Data governance is developing but needs strengthening. Clear policies on approved "
            "data types, GDPR compliance for AI tools, and data classification will reduce risk."
        ),
        "moderate": (
            "Data governance foundations exist. Completing DPIAs for AI tools, defining a data "
            "classification schema, and training staff on data boundaries will strengthen controls."
        ),
        "strong": (
            "Strong data governance is in place. Maintain and audit governance as AI tools and "
            "their data agreements evolve."
        ),
    },
    "staff_capability_score": {
        "low": (
            "Staff may need practical training before AI adoption can scale safely. Training "
            "should cover safe prompting, output checking, data boundaries, approved tools, "
            "and escalation routes."
        ),
        "developing": (
            "Some staff have capability, but consistent understanding is not yet organisation-wide. "
            "A structured awareness programme and practical workshops will build confidence safely."
        ),
        "moderate": (
            "Staff capability is reasonable. Focused workshops on specific use cases, "
            "hallucination risks, and data boundaries will build on existing foundations."
        ),
        "strong": (
            "Staff appear capable. Continue building through peer learning, updated guidance "
            "as tools evolve, and embedding responsible-use practices."
        ),
    },
    "workflow_opportunity_score": {
        "low": (
            "Workflow opportunity appears limited at this stage. Identifying specific repetitive, "
            "low-risk, text-heavy tasks — with clear human review processes — is the recommended start."
        ),
        "developing": (
            "Some workflow opportunities have been identified. Prioritising low-risk, high-volume "
            "tasks for early pilots will build evidence and confidence before broader adoption."
        ),
        "moderate": (
            "Good workflow opportunity exists. Structured pilots in identified areas with clear "
            "success measures and human review will demonstrate value safely."
        ),
        "strong": (
            "There appears to be strong potential for AI-assisted workflow improvement, especially "
            "where tasks are repetitive, text-heavy, low-risk, and subject to human review."
        ),
    },
    "risk_management_score": {
        "low": (
            "Risk management should be strengthened before wider deployment. This may include "
            "acceptable-use guidance, incident reporting, human review rules, and clear ownership."
        ),
        "developing": (
            "Risk management awareness is developing. Formalising risk controls, assigning owners, "
            "and defining acceptable-use policies will reduce exposure during pilots."
        ),
        "moderate": (
            "Risk management foundations exist. Completing the risk register, assigning risk owners, "
            "and introducing incident reporting will build a robust control environment."
        ),
        "strong": (
            "Strong risk management foundations support responsible AI adoption. Continue monitoring, "
            "updating controls as tools evolve, and maintaining incident reporting."
        ),
    },
    "leadership_alignment_score": {
        "low": (
            "Leadership alignment may be a barrier to responsible AI adoption. Securing executive "
            "sponsorship, defining a responsible owner, and setting clear governance expectations "
            "are essential first steps."
        ),
        "developing": (
            "Some leadership engagement exists. Building a shared understanding of risks, "
            "opportunities, and governance responsibilities will accelerate responsible adoption."
        ),
        "moderate": (
            "Reasonable leadership alignment is in place. Formalising governance roles, "
            "sponsoring pilots, and reviewing outcomes at leadership level will strengthen adoption."
        ),
        "strong": (
            "Strong leadership alignment supports responsible AI adoption. Maintain this "
            "engagement as the organisation moves from pilots to broader adoption."
        ),
    },
}


def _safe_score(scores: dict, key: str) -> float | None:
    val = scores.get(key)
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def calculate_average_readiness_score(scores: dict) -> float:
    """Calculate the mean of all individual category scores (excluding overall)."""
    values = []
    for k in _CATEGORY_KEYS:
        v = _safe_score(scores, k)
        if v is not None:
            values.append(v)
    if not values:
        return 0.0
    return round(sum(values) / len(values), 1)


def classify_readiness_level(score: float) -> str:
    """Return a readiness band label for a score."""
    if score >= 80:
        return "Strong readiness"
    elif score >= 60:
        return "Moderate readiness"
    elif score >= 40:
        return "Developing readiness"
    else:
        return "Low readiness"


def get_readiness_level_description(level: str) -> str:
    """Return a plain-English description of a readiness band."""
    return _LEVEL_DESCRIPTIONS.get(
        level,
        "Readiness level could not be determined. Review the category scores for context.",
    )


def get_readiness_band_colour(level: str) -> str:
    """Return a hex colour for a readiness band (for UI display)."""
    return _LEVEL_COLOURS.get(level, "#64748b")


def rank_readiness_categories(scores: dict) -> list:
    """Return category score dicts sorted highest to lowest."""
    items = []
    for key in _CATEGORY_KEYS:
        score = _safe_score(scores, key)
        if score is None:
            continue
        items.append({
            "key": key,
            "label": _CATEGORY_LABELS.get(key, key),
            "score": score,
            "level": classify_readiness_level(score),
            "interpretation": generate_category_interpretation(key, score),
        })
    return sorted(items, key=lambda x: x["score"], reverse=True)


def identify_readiness_strengths(scores: dict, threshold: int = 70) -> list:
    """Return categories at or above threshold as strengths, sorted highest first."""
    strengths = []
    for key in _CATEGORY_KEYS:
        score = _safe_score(scores, key)
        if score is None:
            continue
        if score >= threshold:
            strengths.append({
                "category": _CATEGORY_LABELS.get(key, key),
                "score": score,
                "reason": _STRENGTH_REASONS.get(key, "This area is a relative strength."),
            })
    return sorted(strengths, key=lambda x: x["score"], reverse=True)


def identify_readiness_gaps(scores: dict, threshold: int = 60) -> list:
    """Return categories below threshold as priority gaps, sorted lowest first."""
    gaps = []
    for key in _CATEGORY_KEYS:
        score = _safe_score(scores, key)
        if score is None:
            continue
        if score < threshold:
            gaps.append({
                "category": _CATEGORY_LABELS.get(key, key),
                "score": score,
                "risk": _GAP_RISKS.get(key, "This area may present a risk if left unaddressed."),
                "recommended_action": _GAP_ACTIONS.get(key, "Review and address this area before proceeding."),
            })
    return sorted(gaps, key=lambda x: x["score"])


def generate_category_interpretation(category: str, score: float) -> str:
    """Return a practical consulting-style interpretation for a category score."""
    interpretations = _CATEGORY_INTERPRETATIONS.get(category)
    if not interpretations:
        return (
            f"Score: {score}/100. Review this area in the context of the overall readiness assessment."
        )
    if score >= 80:
        return interpretations["strong"]
    elif score >= 60:
        return interpretations["moderate"]
    elif score >= 40:
        return interpretations["developing"]
    else:
        return interpretations["low"]


def generate_readiness_recommendations(summary: dict) -> list:
    """Return practical improvement recommendations derived from the summary."""
    gaps = summary.get("gaps", [])
    strengths = summary.get("strengths", [])
    overall_score = summary.get("overall_score", 0)

    gap_labels = {g["category"] for g in gaps}
    recommendations = []

    if "Data governance" in gap_labels:
        recommendations.append(
            "Define what data can and cannot be used with AI tools. "
            "Complete DPIAs for any tools that may handle personal or learner data."
        )

    if "Risk management" in gap_labels:
        recommendations.append(
            "Assign responsible owners for AI risk management. "
            "Define acceptable-use rules and an incident-reporting process."
        )

    if "Strategy and leadership" in gap_labels:
        recommendations.append(
            "Define an AI use policy covering approved tools, prohibited uses, and human review requirements."
        )

    if "Leadership alignment" in gap_labels:
        recommendations.append(
            "Secure executive sponsorship for AI governance. "
            "Assign a named responsible owner for AI policy and oversight."
        )

    if "Staff capability" in gap_labels:
        recommendations.append(
            "Deliver AI awareness training covering safe prompting, hallucination risk, "
            "data boundaries, approved tools, and escalation routes."
        )

    has_workflow_strength = any("workflow" in s["category"].lower() for s in strengths)
    has_workflow_gap = any("workflow" in g["category"].lower() for g in gaps)

    if has_workflow_strength:
        recommendations.append(
            "Run a low-risk AI pilot in an identified workflow area — such as document drafting, "
            "email template creation, or admin summarisation. Ensure human review at every step."
        )
    elif not has_workflow_gap:
        recommendations.append(
            "Identify specific workflow tasks that could benefit from AI assistance, starting "
            "with repetitive, low-risk, text-heavy activities."
        )

    recommendations.append(
        "Track pilot outcomes with measurable success criteria: time saved, quality issues, "
        "staff confidence, and any risk incidents."
    )
    recommendations.append(
        "Review and update AI policy and governance after each pilot cycle. "
        "Do not scale AI use until governance, training, and risk controls are confirmed."
    )

    if overall_score >= 70:
        recommendations.append(
            "Consider expanding beyond initial pilots with a structured rollout plan, "
            "maintained governance oversight, and ongoing staff training."
        )

    return recommendations


def _build_strategic_interpretation(
    overall_score: float,
    overall_level: str,
    strengths: list,
    gaps: list,
    org_name: str = "",
) -> str:
    """Build a short deterministic strategic interpretation narrative."""
    org = org_name if org_name else "The organisation"
    top_strength = strengths[0]["category"] if strengths else None
    top_gap = gaps[0]["category"] if gaps else None

    level_narratives = {
        "Low readiness": (
            f"{org} shows low overall AI readiness. Foundational governance, policy, and "
            "staff capability work is required before AI adoption can proceed safely."
        ),
        "Developing readiness": (
            f"{org} shows developing AI readiness. Some foundations are in place, but "
            "governance, staff guidance, and risk controls need strengthening before "
            "structured AI pilots begin."
        ),
        "Moderate readiness": (
            f"{org} shows moderate AI readiness. Useful foundations exist and structured "
            "pilots are feasible, provided governance, staff training, and risk controls "
            "are strengthened."
        ),
        "Strong readiness": (
            f"{org} shows strong AI readiness. The organisation is well positioned to move "
            "beyond pilots, provided governance, monitoring, and responsible-owner oversight continue."
        ),
    }

    base = level_narratives.get(
        overall_level,
        f"{org} has an overall readiness score of {overall_score}/100.",
    )

    add_ons = []
    if top_strength:
        add_ons.append(f"{top_strength} is a relative strength that can support early pilots.")
    if top_gap:
        add_ons.append(
            f"{top_gap} is the most significant gap and should be addressed as an immediate priority."
        )

    if add_ons:
        base += " " + " ".join(add_ons)

    return base


def generate_readiness_summary(scores: dict, org_name: str = "") -> dict:
    """Return a fully structured readiness summary from a scores dict.

    If overall_readiness_score is missing, it is calculated from category averages.
    Missing or invalid category scores are safely skipped.
    """
    overall = _safe_score(scores, "overall_readiness_score")
    if overall is None:
        overall = calculate_average_readiness_score(scores)

    overall_level = classify_readiness_level(overall)
    overall_description = get_readiness_level_description(overall_level)

    category_scores = []
    for key in _CATEGORY_KEYS:
        score = _safe_score(scores, key)
        if score is None:
            continue
        category_scores.append({
            "key": key,
            "label": _CATEGORY_LABELS.get(key, key),
            "score": score,
            "level": classify_readiness_level(score),
            "interpretation": generate_category_interpretation(key, score),
        })

    ranked_categories = sorted(category_scores, key=lambda x: x["score"], reverse=True)
    strengths = identify_readiness_strengths(scores)
    gaps = identify_readiness_gaps(scores)
    strategic_interpretation = _build_strategic_interpretation(
        overall, overall_level, strengths, gaps, org_name=org_name
    )

    summary: dict = {
        "overall_score": overall,
        "overall_level": overall_level,
        "overall_description": overall_description,
        "category_scores": category_scores,
        "ranked_categories": ranked_categories,
        "strengths": strengths,
        "gaps": gaps,
        "strategic_interpretation": strategic_interpretation,
        "recommendations": [],
        "responsible_use_note": (
            "This readiness summary is generated from synthetic/demo audit data only. "
            "It must not be used with real client records, learner data, safeguarding case details, "
            "staff HR data, personal data, confidential data, or regulated information without "
            "appropriate governance, approvals, and responsible owners."
        ),
        "prototype_note": (
            "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
            "financial, academic-integrity, or professional advice. Human review remains required "
            "before any real-world use."
        ),
    }

    summary["recommendations"] = generate_readiness_recommendations(summary)
    return summary


def format_readiness_summary_as_markdown(summary: dict) -> str:
    """Return a full Markdown document for the readiness summary."""
    lines = [
        "# AI Readiness Summary",
        "",
        "## Overall Readiness",
        "",
        f"**Score:** {summary.get('overall_score', 0)}/100",
        f"**Level:** {summary.get('overall_level', '')}",
        "",
        summary.get("overall_description", ""),
        "",
        "## Category Scores",
        "",
        "| Category | Score | Level |",
        "|---|---|---|",
    ]
    for cat in summary.get("category_scores", []):
        lines.append(f"| {cat['label']} | {int(cat['score'])} | {cat['level']} |")

    lines += ["", "## Strengths", ""]
    strengths = summary.get("strengths", [])
    if strengths:
        for s in strengths:
            lines.append(f"**{s['category']}** ({int(s['score'])}/100)")
            lines.append(s["reason"])
            lines.append("")
    else:
        lines += ["No areas above the strength threshold at this stage.", ""]

    lines += ["## Priority Gaps", ""]
    gaps = summary.get("gaps", [])
    if gaps:
        for g in gaps:
            lines.append(f"**{g['category']}** ({int(g['score'])}/100)")
            lines.append(f"Risk: {g['risk']}")
            lines.append(f"Recommended action: {g['recommended_action']}")
            lines.append("")
    else:
        lines += ["No significant gaps identified at this stage.", ""]

    lines += [
        "## Strategic Interpretation",
        "",
        summary.get("strategic_interpretation", ""),
        "",
        "## Recommendations",
        "",
    ]
    for rec in summary.get("recommendations", []):
        lines.append(f"- {rec}")

    lines += [
        "",
        "## Responsible-Use Boundaries",
        "",
        summary.get("responsible_use_note", ""),
        "",
        summary.get("prototype_note", ""),
        "",
        "---",
        "",
        "*Synthetic scenario data. Human review required before real-world use.*",
    ]

    return "\n".join(lines)
