"""
Recommendation Engine — AI Governance Policy Checker
Build 6 · BrightPath ChatGPT Mastery Project

Converts policy gap analysis into deterministic policy improvement recommendations.
Generates priorities, owners, target policies, wording directions, implementation steps,
review questions, and success criteria.

Deterministic only. No external AI, LLM, or API calls.
Synthetic/demo data only.
"""

_RESPONSIBLE_USE_NOTE = (
    "These recommendations are generated from synthetic/demo policy text only. "
    "They must not be used with real client policies, learner data, safeguarding "
    "case details, staff HR data, personal data, confidential data, or regulated "
    "information without appropriate governance, approvals, and responsible owners."
)

_PROTOTYPE_NOTE = (
    "This prototype does not provide legal, safeguarding, HR, compliance, "
    "data-protection, financial, medical, academic-integrity, or professional "
    "governance advice. Suggested wording directions are not legally approved "
    "policy text. They require review by appropriate responsible owners before "
    "real-world use. This is a deterministic policy review support tool, "
    "not a compliance certification system."
)

_OWNER_MAP = {
    "Strategy and Ownership": "Chief Executive Officer / Senior Leadership",
    "Approved AI Tools": "IT Lead / AI Governance Owner",
    "Prohibited AI Uses": "AI Governance Owner / Senior Manager",
    "Data Protection and Confidentiality": "Data Protection Lead / DPO / Senior Manager",
    "Learner and Client Data Boundaries": "Data Protection Lead / Operations Manager",
    "Safeguarding Boundaries": "Designated Safeguarding Lead / Senior Manager",
    "Human Review and Accountability": "Quality Lead / Senior Manager",
    "Accuracy and Hallucination Control": "Quality Lead / Manager",
    "Bias, Fairness, and Inclusion": "Equality Lead / Quality Lead / Senior Manager",
    "Staff Training and Capability": "Training Lead / Quality Lead",
    "Escalation and Incident Reporting": (
        "Senior Manager / Safeguarding Lead / Data Protection Lead"
    ),
    "Monitoring, Review, and Continuous Improvement": "AI Governance Owner / Quality Lead",
}

_TARGET_POLICY_MAP = {
    "Strategy and Ownership": "AI Acceptable Use Policy",
    "Approved AI Tools": "AI Acceptable Use Policy or Staff AI Tool Use Procedure",
    "Prohibited AI Uses": "AI Acceptable Use Policy",
    "Data Protection and Confidentiality": "Data Protection and AI Use Guidance",
    "Learner and Client Data Boundaries": "Data Protection and AI Use Guidance",
    "Safeguarding Boundaries": "Safeguarding and AI Boundary Policy",
    "Human Review and Accountability": "AI Output Review Checklist",
    "Accuracy and Hallucination Control": "AI Output Review Checklist",
    "Bias, Fairness, and Inclusion": "AI Acceptable Use Policy or AI Output Review Checklist",
    "Staff Training and Capability": "Staff AI Tool Use Procedure",
    "Escalation and Incident Reporting": "AI Incident and Escalation Procedure",
    "Monitoring, Review, and Continuous Improvement": (
        "Staff AI Tool Use Procedure or AI Incident and Escalation Procedure"
    ),
}

_WORDING_DIRECTION_MAP = {
    "Strategy and Ownership": (
        "The policy should name a responsible owner or governance lead for AI oversight, "
        "confirm senior leadership accountability, and set expectations for governance review."
    ),
    "Approved AI Tools": (
        "The policy should state which AI tools are approved for use, the approval process "
        "for new tools, and who is responsible for maintaining the approved list."
    ),
    "Prohibited AI Uses": (
        "The policy should clearly list what staff must never do with AI tools, including "
        "entering confidential data, making safeguarding decisions, and using unapproved tools."
    ),
    "Data Protection and Confidentiality": (
        "The policy should state that staff must not enter personal, confidential, "
        "sensitive, or identifiable information into AI tools unless the tool, "
        "purpose, and data handling route have been approved by the responsible owner."
    ),
    "Learner and Client Data Boundaries": (
        "The policy should state that learner names, client records, case details, "
        "assessment data, and other identifiable information must not be entered into "
        "AI tools. If anonymised data is used, this should be explicitly permitted "
        "and the anonymisation method confirmed by the responsible owner."
    ),
    "Safeguarding Boundaries": (
        "The policy should state that safeguarding concerns, case details, disclosures, "
        "and decisions must remain human-led and must be escalated through approved "
        "safeguarding routes. AI tools must not be used to make safeguarding judgements."
    ),
    "Human Review and Accountability": (
        "The policy should state that AI-assisted outputs must be checked by a responsible "
        "human before use, especially where outputs may affect learners, clients, staff, "
        "external communications, or organisational decisions."
    ),
    "Accuracy and Hallucination Control": (
        "The policy should state that AI outputs may be inaccurate, incomplete, fabricated, "
        "biased, or unsuitable, and staff must verify important information against approved "
        "sources before use."
    ),
    "Bias, Fairness, and Inclusion": (
        "The policy should require staff to review AI-assisted outputs for bias, "
        "exclusionary language, unfair assumptions, or inappropriate tone before use."
    ),
    "Staff Training and Capability": (
        "The policy should confirm what training staff must complete before using AI tools, "
        "what guidance is available, and how training completion is recorded."
    ),
    "Escalation and Incident Reporting": (
        "The policy should explain how staff report AI-related concerns, near misses, "
        "inaccurate outputs, data issues, safeguarding concerns, or inappropriate tool use, "
        "including named routes and responsible contacts."
    ),
    "Monitoring, Review, and Continuous Improvement": (
        "The policy should set out how AI use and outputs are monitored, when the policy "
        "is reviewed, who carries out the review, and how lessons learned are incorporated."
    ),
}

_FALLBACK_WORDING = (
    "The policy should include clearer wording, examples, ownership, controls, "
    "review expectations, and escalation routes for this governance area."
)

# (coverage_level, domain_keyword_or_None, action_type)
_ACTION_TYPE_RULES = [
    ("Not covered", None, "Create new policy section"),
    ("Weak coverage", "Safeguarding", "Add escalation route"),
    ("Weak coverage", "Escalation", "Add escalation route"),
    ("Weak coverage", "Human Review", "Add checklist or control"),
    ("Weak coverage", "Staff Training", "Add staff training guidance"),
    ("Weak coverage", "Monitoring", "Add monitoring and review process"),
    ("Weak coverage", None, "Strengthen existing wording"),
    ("Partial coverage", "Safeguarding", "Add escalation route"),
    ("Partial coverage", "Escalation", "Add escalation route"),
    ("Partial coverage", "Human Review", "Add checklist or control"),
    ("Partial coverage", "Monitoring", "Add monitoring and review process"),
    ("Partial coverage", None, "Review and clarify existing wording"),
]

_REVIEW_QUESTIONS_BASE = [
    "Does the policy clearly tell staff what they can and cannot do?",
    "Does the policy define who owns this area?",
    "Does the policy explain what should be escalated and to whom?",
    "Does the policy include examples that staff can understand?",
    "Does the policy explain how AI outputs should be checked?",
    "Does the policy avoid using AI for human-only decisions?",
    "Does the policy explain how issues or near misses should be reported?",
]

_SUCCESS_CRITERIA_BASE = [
    "Staff can identify the approved route for this issue.",
    "The policy includes clear permitted and prohibited examples.",
    "The responsible owner is named or role-based.",
    "Human review expectations are stated.",
    "Escalation routes are clear.",
    "Training materials reference the updated policy.",
    "The policy can be reviewed periodically by a responsible owner.",
]

_PRIORITY_ORDER = ["Urgent", "High priority", "Medium priority", "Low priority"]


def generate_recommendation_id(index: int) -> str:
    """Return a recommendation ID in the format REC-001."""
    return f"REC-{index:03d}"


def classify_recommendation_priority(
    gap_severity: str, gap_priority_score: int
) -> str:
    """Map gap severity and priority score to a recommendation priority label."""
    severity_map = {
        "Critical gap": "Urgent",
        "High gap": "High priority",
        "Medium gap": "Medium priority",
        "Low gap": "Low priority",
    }
    from_severity = severity_map.get(gap_severity, "Low priority")

    score = int(gap_priority_score)
    if score >= 85:
        from_score = "Urgent"
    elif score >= 70:
        from_score = "High priority"
    elif score >= 45:
        from_score = "Medium priority"
    else:
        from_score = "Low priority"

    idx_severity = _PRIORITY_ORDER.index(from_severity)
    idx_score = _PRIORITY_ORDER.index(from_score)
    return _PRIORITY_ORDER[min(idx_severity, idx_score)]


def suggest_policy_action_type(gap: dict) -> str:
    """Return a policy action type label for the gap."""
    coverage_level = gap.get("coverage_level", "")
    domain_name = gap.get("domain_name", "")

    for level, domain_keyword, action in _ACTION_TYPE_RULES:
        if coverage_level != level:
            continue
        if domain_keyword is None:
            return action
        if domain_keyword.lower() in domain_name.lower():
            return action

    return "Review and clarify existing wording"


def suggest_policy_owner(gap: dict) -> str:
    """Return a suggested policy owner for the gap domain."""
    domain_name = gap.get("domain_name", "")
    for key, owner in _OWNER_MAP.items():
        if key.lower() in domain_name.lower() or domain_name.lower() in key.lower():
            return owner
    return "Responsible Manager / AI Governance Owner"


def suggest_target_policy(
    gap: dict, policy_pack: dict | None = None
) -> str:
    """Return a suggested target policy for the gap."""
    domain_name = gap.get("domain_name", "")

    generic_target = "Responsible AI policy pack"
    for key, target in _TARGET_POLICY_MAP.items():
        if key.lower() in domain_name.lower() or domain_name.lower() in key.lower():
            generic_target = target
            break

    if policy_pack and isinstance(policy_pack, dict):
        policies = policy_pack.get("policies", []) or []
        for policy in policies:
            title = policy.get("policy_title", "")
            if title and title.lower() in generic_target.lower():
                return title

    return generic_target


def generate_recommendation_rationale(gap: dict) -> str:
    """Return a deterministic consulting rationale for the recommendation."""
    domain_name = gap.get("domain_name", "")
    gap_severity = gap.get("gap_severity", "")
    priority_level = gap.get("priority_level", "")
    risk_statement = gap.get("risk_statement", "")

    if risk_statement:
        base = risk_statement
    else:
        base = (
            f"The policy pack has insufficient coverage of the {domain_name} "
            "governance domain."
        )

    if gap_severity in ("Critical gap", "High gap"):
        urgency = (
            f" This is a {gap_severity.lower()} in a {priority_level.lower()}-priority "
            "governance domain and should be addressed before wider AI adoption."
        )
    elif gap_severity == "Medium gap":
        urgency = (
            " This is a medium gap that should be addressed as part of "
            "a policy review before AI use expands."
        )
    else:
        urgency = (
            " This is a lower-priority gap that should be included in a future "
            "policy review cycle."
        )

    return base + urgency


def generate_policy_wording_direction(gap: dict) -> str:
    """Return a deterministic suggested wording direction for the gap domain."""
    domain_name = gap.get("domain_name", "")
    for key, direction in _WORDING_DIRECTION_MAP.items():
        if key.lower() in domain_name.lower() or domain_name.lower() in key.lower():
            return f"Suggested wording direction: {direction}"
    return f"Suggested wording direction: {_FALLBACK_WORDING}"


def generate_implementation_steps(gap: dict) -> list:
    """Return 4–7 practical implementation steps for the recommendation."""
    coverage_level = gap.get("coverage_level", "")
    gap_severity = gap.get("gap_severity", "")
    domain_name = gap.get("domain_name", "governance area")

    steps = []

    if gap_severity in ("Critical gap", "High gap"):
        steps.append("Address this before wider AI rollout or pilot scaling.")

    steps.append("Review the current policy wording against the identified gap.")
    steps.append("Confirm the responsible policy owner.")

    if coverage_level == "Not covered":
        steps.append(
            f"Create a new policy section that clearly addresses {domain_name}."
        )
    else:
        steps.append(
            f"Strengthen or clarify the existing wording for {domain_name}."
        )

    steps.extend([
        "Include practical examples of permitted and prohibited behaviour.",
        "Add human-review, escalation, and monitoring requirements.",
        "Review the update with relevant responsible owners.",
        "Communicate the change to staff and include it in training.",
    ])

    return steps


def generate_review_questions(gap: dict) -> list:
    """Return review questions tailored to the gap domain."""
    domain_name = gap.get("domain_name", "").lower()
    questions = list(_REVIEW_QUESTIONS_BASE)

    if "safeguarding" in domain_name:
        questions.append(
            "Does the policy make clear that AI must not be used for safeguarding decisions?"
        )
    if "data" in domain_name or "learner" in domain_name or "client" in domain_name:
        questions.append(
            "Does the policy specify which types of data must not be entered into AI tools?"
        )
    if "training" in domain_name or "capability" in domain_name:
        questions.append(
            "Does the policy confirm what training staff must complete before using AI tools?"
        )

    return questions


def generate_success_criteria(gap: dict) -> list:
    """Return measurable success criteria for the recommendation."""
    domain_name = gap.get("domain_name", "").lower()
    criteria = list(_SUCCESS_CRITERIA_BASE)

    if "safeguarding" in domain_name:
        criteria.append("Safeguarding escalation routes are explicitly referenced.")
    if "incident" in domain_name or "escalation" in domain_name:
        criteria.append("Named contacts or roles are provided for incident reporting.")
    if "training" in domain_name or "capability" in domain_name:
        criteria.append("Required training is referenced with a completion expectation.")

    return criteria


def _build_recommendation_title(gap: dict) -> str:
    """Build a short recommendation title from gap data."""
    action = suggest_policy_action_type(gap)
    domain = gap.get("domain_name", "governance area")
    return f"{action}: {domain}"


def generate_recommendation_from_gap(
    gap: dict, index: int, policy_pack: dict | None = None
) -> dict:
    """Generate a structured recommendation dict from a single gap."""
    if not isinstance(gap, dict):
        gap = {}

    gap_severity = gap.get("gap_severity", "Low gap")
    gap_priority_score = gap.get("gap_priority_score", 0)
    priority = classify_recommendation_priority(gap_severity, gap_priority_score)

    return {
        "recommendation_id": generate_recommendation_id(index),
        "related_gap_id": gap.get("gap_id", ""),
        "domain_id": gap.get("domain_id", ""),
        "domain_name": gap.get("domain_name", ""),
        "gap_severity": gap_severity,
        "gap_priority_score": gap_priority_score,
        "recommendation_priority": priority,
        "policy_action_type": suggest_policy_action_type(gap),
        "target_policy": suggest_target_policy(gap, policy_pack),
        "suggested_owner": suggest_policy_owner(gap),
        "recommendation_title": _build_recommendation_title(gap),
        "rationale": generate_recommendation_rationale(gap),
        "suggested_wording_direction": generate_policy_wording_direction(gap),
        "implementation_steps": generate_implementation_steps(gap),
        "review_questions": generate_review_questions(gap),
        "success_criteria": generate_success_criteria(gap),
        "responsible_use_note": (
            "This recommendation is generated from synthetic/demo policy text only. "
            "Wording direction is indicative only and requires review by appropriate "
            "responsible owners before real-world use."
        ),
        "review_note": (
            "This recommendation is deterministic and template-based. "
            "Human review is required before any real-world policy change."
        ),
    }


def _derive_policy_update_themes(items: list) -> list:
    """Derive update themes from a list of recommendation items."""
    themes = []
    domain_names = [r.get("domain_name", "").lower() for r in items]

    if any("data" in n for n in domain_names):
        themes.append("Data protection and confidentiality")
    if any("safeguarding" in n for n in domain_names):
        themes.append("Safeguarding policy update")
    if any("learner" in n or "client" in n for n in domain_names):
        themes.append("Learner and client data boundaries")
    if any("human" in n or "accountability" in n for n in domain_names):
        themes.append("Human review controls")
    if any("escalation" in n or "incident" in n for n in domain_names):
        themes.append("Incident and escalation procedure")
    if any("training" in n or "capability" in n for n in domain_names):
        themes.append("Staff training and awareness")
    if any("bias" in n or "fairness" in n for n in domain_names):
        themes.append("Bias and fairness review")
    if any("accuracy" in n or "hallucination" in n for n in domain_names):
        themes.append("Accuracy and output review")
    if any("strategy" in n or "ownership" in n for n in domain_names):
        themes.append("AI governance ownership")
    if any("monitoring" in n or "improvement" in n for n in domain_names):
        themes.append("Monitoring and review process")
    if any("approved" in n or "prohibited" in n for n in domain_names):
        themes.append("Approved and prohibited uses policy")

    return themes if themes else ["General policy improvements"]


def _build_owner_summary(items: list) -> dict:
    """Build a dict mapping suggested owner → list of recommendation IDs."""
    summary: dict = {}
    for rec in items:
        owner = rec.get("suggested_owner", "Unknown")
        rec_id = rec.get("recommendation_id", "")
        summary.setdefault(owner, []).append(rec_id)
    return summary


def _build_recommended_sequence(items: list) -> list:
    """Group recommendations into a logical implementation sequence."""
    if not items:
        return []

    urgent_high = [
        r for r in items
        if r.get("recommendation_priority") in ("Urgent", "High priority")
    ]
    procedures = [
        r for r in items
        if r.get("recommendation_priority") == "Medium priority"
        and "training" not in r.get("domain_name", "").lower()
        and "capability" not in r.get("domain_name", "").lower()
    ]
    training_recs = [
        r for r in items
        if "training" in r.get("domain_name", "").lower()
        or "capability" in r.get("domain_name", "").lower()
    ]
    monitoring_recs = [
        r for r in items
        if "monitoring" in r.get("domain_name", "").lower()
        or "improvement" in r.get("domain_name", "").lower()
    ]

    sequence = []
    step = 1

    if urgent_high:
        sequence.append({
            "sequence_step": step,
            "title": "Immediate policy controls",
            "recommendations": [r["recommendation_id"] for r in urgent_high],
            "reason": (
                "Address urgent and high-priority gaps before AI use expands or pilots scale."
            ),
        })
        step += 1

    if procedures:
        sequence.append({
            "sequence_step": step,
            "title": "Clarify operational procedures",
            "recommendations": [r["recommendation_id"] for r in procedures],
            "reason": (
                "Strengthen operational details so staff understand expected behaviour "
                "in practice."
            ),
        })
        step += 1

    if training_recs:
        sequence.append({
            "sequence_step": step,
            "title": "Staff communication and training",
            "recommendations": [r["recommendation_id"] for r in training_recs],
            "reason": (
                "Ensure staff are aware of updated policy requirements and complete "
                "any required training."
            ),
        })
        step += 1

    if monitoring_recs:
        sequence.append({
            "sequence_step": step,
            "title": "Monitoring and review",
            "recommendations": [r["recommendation_id"] for r in monitoring_recs],
            "reason": (
                "Establish ongoing monitoring and a regular review cycle to keep "
                "policy up to date."
            ),
        })
        step += 1

    if not sequence:
        sequence.append({
            "sequence_step": 1,
            "title": "Policy review and improvement",
            "recommendations": [r["recommendation_id"] for r in items],
            "reason": (
                "Address all identified recommendations as part of a policy review cycle."
            ),
        })

    return sequence


def _identify_quick_wins(items: list) -> list:
    """Return up to 3 recommendations suitable as quick wins."""
    quick_win_actions = {
        "Add checklist or control",
        "Strengthen existing wording",
        "Add escalation route",
        "Review and clarify existing wording",
    }
    quick_win_priorities = {"Medium priority", "High priority"}

    wins = [
        r for r in items
        if r.get("policy_action_type") in quick_win_actions
        and r.get("recommendation_priority") in quick_win_priorities
    ]

    if not wins and items:
        wins = [
            r for r in items
            if r.get("recommendation_priority") in quick_win_priorities
        ][:2]

    return wins[:3]


def generate_policy_recommendations(
    gap_analysis: dict,
    policy_pack: dict | None = None,
    coverage_results: dict | None = None,
) -> dict:
    """
    Generate policy improvement recommendations from a gap analysis.

    One recommendation is generated per gap (from prioritised_gaps).
    Returns a structured recommendation package with priority groups,
    quick wins, themes, owner summary, and recommended sequence.
    """
    if not isinstance(gap_analysis, dict):
        gap_analysis = {}

    org_name = gap_analysis.get("organisation_name", "Unnamed organisation")
    pack_title = gap_analysis.get("policy_pack_title", "")
    responsible_use_note = gap_analysis.get("responsible_use_note", _RESPONSIBLE_USE_NOTE)

    # Use prioritised_gaps (already sorted) if available; else assemble from severity buckets
    prioritised_gaps = gap_analysis.get("prioritised_gaps", []) or []
    if not prioritised_gaps:
        critical = gap_analysis.get("critical_gaps", []) or []
        high = gap_analysis.get("high_gaps", []) or []
        medium = gap_analysis.get("medium_gaps", []) or []
        low = gap_analysis.get("low_gaps", []) or []
        prioritised_gaps = critical + high + medium + low

    if not prioritised_gaps:
        return {
            "organisation_name": org_name,
            "policy_pack_title": pack_title,
            "total_recommendations": 0,
            "urgent_recommendations": [],
            "high_priority_recommendations": [],
            "medium_priority_recommendations": [],
            "low_priority_recommendations": [],
            "prioritised_recommendations": [],
            "quick_wins": [],
            "policy_update_themes": [],
            "owner_summary": {},
            "recommended_sequence": [],
            "responsible_use_note": responsible_use_note,
            "prototype_note": _PROTOTYPE_NOTE,
        }

    # Generate one recommendation per gap
    items = []
    for idx, gap in enumerate(prioritised_gaps, start=1):
        if not isinstance(gap, dict):
            continue
        items.append(generate_recommendation_from_gap(gap, idx, policy_pack))

    prioritised_items = prioritise_recommendations(items)

    urgent = [r for r in prioritised_items if r["recommendation_priority"] == "Urgent"]
    high = [
        r for r in prioritised_items if r["recommendation_priority"] == "High priority"
    ]
    medium = [
        r for r in prioritised_items if r["recommendation_priority"] == "Medium priority"
    ]
    low = [r for r in prioritised_items if r["recommendation_priority"] == "Low priority"]

    return {
        "organisation_name": org_name,
        "policy_pack_title": pack_title,
        "total_recommendations": len(prioritised_items),
        "urgent_recommendations": urgent,
        "high_priority_recommendations": high,
        "medium_priority_recommendations": medium,
        "low_priority_recommendations": low,
        "prioritised_recommendations": prioritised_items,
        "quick_wins": _identify_quick_wins(prioritised_items),
        "policy_update_themes": _derive_policy_update_themes(prioritised_items),
        "owner_summary": _build_owner_summary(prioritised_items),
        "recommended_sequence": _build_recommended_sequence(prioritised_items),
        "responsible_use_note": responsible_use_note,
        "prototype_note": _PROTOTYPE_NOTE,
    }


def summarise_policy_recommendations(recommendations: dict) -> dict:
    """Return a compact summary of the recommendation package."""
    if not isinstance(recommendations, dict):
        recommendations = {}

    urgent = recommendations.get("urgent_recommendations", []) or []
    high = recommendations.get("high_priority_recommendations", []) or []
    medium = recommendations.get("medium_priority_recommendations", []) or []
    low = recommendations.get("low_priority_recommendations", []) or []
    quick_wins = recommendations.get("quick_wins", []) or []

    urgent_count = len(urgent)
    high_count = len(high)
    medium_count = len(medium)
    low_count = len(low)
    total = urgent_count + high_count + medium_count + low_count

    owner_summary = recommendations.get("owner_summary", {}) or {}
    top_owners = sorted(
        owner_summary.keys(),
        key=lambda k: len(owner_summary[k]),
        reverse=True,
    )[:3]

    themes = recommendations.get("policy_update_themes", []) or []
    top_themes = themes[:5]

    prioritised = recommendations.get("prioritised_recommendations", []) or []
    highest = prioritised[0] if prioritised else {}

    if urgent_count > 0 or high_count > 0:
        overall_position = (
            "The organisation should address urgent and high-priority policy improvements "
            "before wider AI adoption or pilot scaling."
        )
    elif medium_count > 0:
        overall_position = (
            "The policy pack has useful foundations, but operational details should be "
            "strengthened before AI use expands."
        )
    else:
        overall_position = (
            "The policy pack appears to cover most reviewed domains, subject to human "
            "review and responsible-owner approval."
        )

    focus = []
    if urgent_count > 0 or high_count > 0:
        focus.append("Address urgent/high-priority recommendations first.")
    domain_names = [
        r.get("domain_name", "").lower() for r in (urgent + high + medium)
    ]
    if any("learner" in n or "client" in n for n in domain_names):
        focus.append("Strengthen learner/client data boundaries.")
    if any("safeguarding" in n for n in domain_names):
        focus.append("Strengthen safeguarding boundaries and escalation.")
    if any("approved" in n or "prohibited" in n for n in domain_names):
        focus.append("Clarify approved and prohibited AI use cases.")
    if any("human" in n or "accountability" in n for n in domain_names):
        focus.append("Add human review and accountability controls.")
    if any("incident" in n or "escalation" in n for n in domain_names):
        focus.append("Add incident and near-miss reporting.")
    if any("training" in n or "capability" in n for n in domain_names):
        focus.append("Communicate policy changes through staff training.")
    if not focus:
        focus.append("Review medium and low recommendations in a policy review cycle.")

    return {
        "total_recommendations": total,
        "urgent_count": urgent_count,
        "high_priority_count": high_count,
        "medium_priority_count": medium_count,
        "low_priority_count": low_count,
        "quick_win_count": len(quick_wins),
        "top_policy_update_themes": top_themes,
        "top_owners": top_owners,
        "highest_priority_recommendation": highest,
        "overall_recommendation_position": overall_position,
        "recommended_focus": focus,
    }


def prioritise_recommendations(recommendation_items: list) -> list:
    """Return recommendations sorted by priority then gap_priority_score descending."""
    if not recommendation_items:
        return []
    return sorted(
        recommendation_items,
        key=lambda r: (
            _PRIORITY_ORDER.index(
                r.get("recommendation_priority", "Low priority")
                if r.get("recommendation_priority") in _PRIORITY_ORDER
                else "Low priority"
            ),
            -r.get("gap_priority_score", 0),
        ),
    )


def _render_rec_section_md(title: str, items: list) -> list:
    """Render a recommendation priority section as Markdown lines."""
    lines = ["", "---", "", f"## {title}", ""]
    if not items:
        lines.append(f"No {title.lower()} identified.")
        return lines
    for rec in items:
        steps = rec.get("implementation_steps", [])
        questions = rec.get("review_questions", [])
        criteria = rec.get("success_criteria", [])
        lines.extend([
            f"### {rec.get('recommendation_id', '')} — {rec.get('recommendation_title', '')}",
            "",
            f"**Related Gap:** {rec.get('related_gap_id', '')}",
            f"**Domain:** {rec.get('domain_id', '')} — {rec.get('domain_name', '')}",
            f"**Priority:** {rec.get('recommendation_priority', '')}",
            f"**Action type:** {rec.get('policy_action_type', '')}",
            f"**Target policy:** {rec.get('target_policy', '')}",
            f"**Suggested owner:** {rec.get('suggested_owner', '')}",
            "",
            f"**Rationale:** {rec.get('rationale', '')}",
            "",
            rec.get("suggested_wording_direction", ""),
            "",
            "**Implementation steps:**",
        ])
        for step in steps:
            lines.append(f"- {step}")
        lines.extend(["", "**Review questions:**"])
        for q in questions:
            lines.append(f"- {q}")
        lines.extend(["", "**Success criteria:**"])
        for c in criteria:
            lines.append(f"- {c}")
        lines.extend(["", f"*{rec.get('review_note', '')}*", ""])
    return lines


def format_policy_recommendations_as_markdown(
    recommendations: dict, summary: dict | None = None
) -> str:
    """Return a full Markdown policy improvement recommendations report."""
    if not isinstance(recommendations, dict):
        recommendations = {}
    if summary is None:
        summary = summarise_policy_recommendations(recommendations)

    org_name = recommendations.get("organisation_name", "Unnamed organisation")
    pack_title = recommendations.get("policy_pack_title", "")
    total = recommendations.get("total_recommendations", 0)

    lines = [
        "# AI Governance Policy Improvement Recommendations",
        "",
        "## Review Overview",
        "",
        f"**Organisation:** {org_name}",
        f"**Policy Pack:** {pack_title}",
        f"**Total recommendations:** {total}",
        "",
        "---",
        "",
        "## Recommendation Summary",
        "",
        f"**Total recommendations:** {summary.get('total_recommendations', 0)}",
        f"**Urgent:** {summary.get('urgent_count', 0)}",
        f"**High priority:** {summary.get('high_priority_count', 0)}",
        f"**Medium priority:** {summary.get('medium_priority_count', 0)}",
        f"**Low priority:** {summary.get('low_priority_count', 0)}",
        f"**Quick wins:** {summary.get('quick_win_count', 0)}",
        "",
        "---",
        "",
        "## Overall Recommendation Position",
        "",
        summary.get("overall_recommendation_position", ""),
        "",
        "---",
        "",
        "## Recommended Focus Areas",
        "",
    ]
    for focus in summary.get("recommended_focus", []):
        lines.append(f"- {focus}")

    lines.extend(["", "---", "", "## Recommended Sequence", ""])
    for seq in recommendations.get("recommended_sequence", []):
        lines.extend([
            f"### Step {seq.get('sequence_step', '')}: {seq.get('title', '')}",
            "",
            f"*{seq.get('reason', '')}*",
            "",
            "Recommendations: " + ", ".join(seq.get("recommendations", [])),
            "",
        ])

    lines.extend(["", "---", "", "## Quick Wins", ""])
    quick_wins = recommendations.get("quick_wins", [])
    if quick_wins:
        for qw in quick_wins:
            lines.append(
                f"- **{qw.get('recommendation_id', '')}** — "
                f"{qw.get('recommendation_title', '')} "
                f"({qw.get('recommendation_priority', '')})"
            )
    else:
        lines.append("No quick wins identified.")

    lines.extend(["", "---", "", "## Policy Update Themes", ""])
    for theme in summary.get("top_policy_update_themes", []):
        lines.append(f"- {theme}")

    lines.extend(["", "---", "", "## Owner Summary", ""])
    owner_summary = recommendations.get("owner_summary", {})
    if owner_summary:
        lines.extend(["| Suggested Owner | Recommendations |", "|---|---|"])
        for owner, rec_ids in owner_summary.items():
            lines.append(f"| {owner} | {', '.join(rec_ids)} |")
    else:
        lines.append("No owner assignments identified.")

    lines.extend([
        "",
        "---",
        "",
        "## Prioritised Recommendations",
        "",
        "| Rec ID | Domain | Priority | Action Type | Target Policy |",
        "|---|---|---|---|---|",
    ])
    for rec in recommendations.get("prioritised_recommendations", []):
        lines.append(
            f"| {rec.get('recommendation_id', '')} "
            f"| {rec.get('domain_name', '')} "
            f"| {rec.get('recommendation_priority', '')} "
            f"| {rec.get('policy_action_type', '')} "
            f"| {rec.get('target_policy', '')} |"
        )

    lines.extend(_render_rec_section_md(
        "Urgent Recommendations",
        recommendations.get("urgent_recommendations", []),
    ))
    lines.extend(_render_rec_section_md(
        "High-Priority Recommendations",
        recommendations.get("high_priority_recommendations", []),
    ))
    lines.extend(_render_rec_section_md(
        "Medium-Priority Recommendations",
        recommendations.get("medium_priority_recommendations", []),
    ))
    lines.extend(_render_rec_section_md(
        "Low-Priority Recommendations",
        recommendations.get("low_priority_recommendations", []),
    ))

    lines.extend([
        "",
        "---",
        "",
        "## Detailed Recommendation Notes",
        "",
        "See Urgent, High-Priority, Medium-Priority, and Low-Priority sections above "
        "for full per-recommendation detail.",
        "",
        "---",
        "",
        "## Responsible-Use Boundaries",
        "",
        _RESPONSIBLE_USE_NOTE,
        "",
        _PROTOTYPE_NOTE,
        "",
        "Suggested wording directions are not legally approved policy text. "
        "They require review by appropriate responsible owners before real-world use.",
        "",
        "Human review remains required before any real-world use.",
        "",
        "---",
        "",
        "*Build 6 · AI Governance Policy Checker · BrightPath ChatGPT Mastery Project*",
        "*Synthetic scenarios only. Human review required before any real-world use.*",
    ])

    return "\n".join(lines)
