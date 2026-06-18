"""Deterministic governance sign-off and control tracking for Build 8 Phase 4."""


SIGNOFF_URGENT_DAYS = 7
SIGNOFF_SOON_DAYS = 14

CONTROL_KEYWORDS = {
    "policy": ["policy", "governance", "acceptable use", "responsible ai"],
    "approval": [
        "approval",
        "sign-off",
        "signoff",
        "authorise",
        "authorisation",
    ],
    "quality": ["quality", "checklist", "review", "standard"],
    "risk": ["risk", "incident", "near miss", "escalation"],
    "data": ["data", "confidential", "personal", "safeguarding", "learner"],
}

CONTROL_AREA_LABELS = {
    "policy": "Policy control",
    "approval": "Approval control",
    "quality": "Quality control",
    "risk": "Risk control",
    "data": "Data control",
}

GOVERNANCE_RISK_ORDER = {
    "High governance delivery risk": 1,
    "Moderate governance delivery risk": 2,
    "Low governance delivery risk": 3,
}

SIGNOFF_URGENCY_ORDER = {
    "Urgent sign-off": 1,
    "Sign-off due soon": 2,
    "Routine sign-off": 3,
    "No sign-off required": 4,
}

CONTROL_READINESS_ORDER = {
    "Control blocked": 1,
    "Control needs review": 2,
    "Control ready": 3,
    "No control required": 4,
}

PRIORITY_ORDER = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4,
}


def requires_governance_signoff(action: dict) -> bool:
    """Return True if governance sign-off is explicitly required."""
    return action.get("governance_signoff_required") is True


def classify_signoff_urgency(action: dict) -> str:
    """Classify how soon an explicit governance sign-off is required."""
    if not requires_governance_signoff(action):
        return "No sign-off required"

    due_in_days = action.get("due_in_days", 0)
    if due_in_days <= SIGNOFF_URGENT_DAYS:
        return "Urgent sign-off"
    if due_in_days <= SIGNOFF_SOON_DAYS:
        return "Sign-off due soon"
    return "Routine sign-off"


def _combined_control_text(action: dict) -> str:
    """Return action text used for deterministic control keyword matching."""
    return " ".join(
        str(action.get(field, ""))
        for field in ("action_title", "action_description", "blocker")
    ).lower()


def _blocker_mentions_control(action: dict) -> bool:
    """Return True when blocker text names a governance or control concern."""
    blocker_text = str(action.get("blocker", "")).lower()
    return any(
        keyword in blocker_text
        for keywords in CONTROL_KEYWORDS.values()
        for keyword in keywords
    )


def classify_control_area(action: dict) -> str:
    """Classify the governance control area using action and blocker text."""
    combined_text = _combined_control_text(action)

    for control_area, keywords in CONTROL_KEYWORDS.items():
        if any(keyword in combined_text for keyword in keywords):
            return CONTROL_AREA_LABELS[control_area]

    if requires_governance_signoff(action):
        return "General control"
    return "No governance control"


def classify_control_readiness(action: dict) -> str:
    """Classify whether the action's governance control is ready."""
    signoff_required = requires_governance_signoff(action)

    if signoff_required and action.get("status") == "Blocked":
        return "Control blocked"
    if signoff_required or _blocker_mentions_control(action):
        return "Control needs review"
    if (
        not signoff_required
        and action.get("status") in {"Completed", "In progress"}
        and not str(action.get("blocker", "")).strip()
    ):
        return "Control ready"
    return "No control required"


def identify_governance_owner_need(action: dict) -> str:
    """Return the governance ownership level needed for one action."""
    signoff_required = requires_governance_signoff(action)
    control_area = classify_control_area(action)

    if action.get("priority") == "Critical" and signoff_required:
        return "Senior approval needed"
    if signoff_required or control_area != "No governance control":
        return "Governance lead review needed"
    if (
        not signoff_required
        and action.get("status") in {"In progress", "Not started"}
    ):
        return "Operational owner can proceed"
    return "No governance owner needed"


def classify_governance_delivery_risk(action: dict) -> str:
    """Return the governance delivery risk for one action."""
    signoff_required = requires_governance_signoff(action)
    signoff_urgency = classify_signoff_urgency(action)
    control_readiness = classify_control_readiness(action)

    if (
        signoff_required and action.get("status") == "Blocked"
    ) or (
        signoff_urgency == "Urgent sign-off"
        and action.get("priority") in {"Critical", "High"}
    ):
        return "High governance delivery risk"
    if (
        signoff_required
        or signoff_urgency == "Sign-off due soon"
        or control_readiness == "Control needs review"
    ):
        return "Moderate governance delivery risk"
    return "Low governance delivery risk"


def build_governance_summary(action: dict) -> dict:
    """Return one action-level governance tracking summary."""
    return {
        "action_id": action.get("action_id", ""),
        "organisation_id": action.get("organisation_id", ""),
        "organisation_name": action.get("organisation_name", ""),
        "workflow_id": action.get("workflow_id", ""),
        "workflow_name": action.get("workflow_name", ""),
        "related_build": action.get("related_build", ""),
        "action_title": action.get("action_title", ""),
        "owner_role": action.get("owner_role", ""),
        "priority": action.get("priority", ""),
        "status": action.get("status", ""),
        "due_in_days": action.get("due_in_days", 0),
        "governance_signoff_required": requires_governance_signoff(action),
        "signoff_urgency": classify_signoff_urgency(action),
        "control_area": classify_control_area(action),
        "control_readiness": classify_control_readiness(action),
        "governance_owner_need": identify_governance_owner_need(action),
        "governance_delivery_risk": classify_governance_delivery_risk(action),
        "blocker": action.get("blocker", ""),
    }


def build_all_governance_summaries(actions: list[dict]) -> list[dict]:
    """Return a governance tracking summary for every action."""
    return [build_governance_summary(action) for action in actions]


def _summarise_group(group: list[dict]) -> dict:
    """Return shared governance workload counts for one action group."""
    summaries = build_all_governance_summaries(group)

    return {
        "total_actions": len(summaries),
        "signoff_required_count": sum(
            summary["governance_signoff_required"] for summary in summaries
        ),
        "urgent_signoff_count": sum(
            summary["signoff_urgency"] == "Urgent sign-off"
            for summary in summaries
        ),
        "control_blocked_count": sum(
            summary["control_readiness"] == "Control blocked"
            for summary in summaries
        ),
        "control_needs_review_count": sum(
            summary["control_readiness"] == "Control needs review"
            for summary in summaries
        ),
        "high_governance_risk_count": sum(
            summary["governance_delivery_risk"]
            == "High governance delivery risk"
            for summary in summaries
        ),
        "senior_approval_needed_count": sum(
            summary["governance_owner_need"] == "Senior approval needed"
            for summary in summaries
        ),
        "governance_lead_review_needed_count": sum(
            summary["governance_owner_need"]
            == "Governance lead review needed"
            for summary in summaries
        ),
    }


def summarise_governance_by_organisation(actions: list[dict]) -> list[dict]:
    """Return governance workload grouped by organisation."""
    grouped_actions: dict[str, list[dict]] = {}
    for action in actions:
        grouped_actions.setdefault(action.get("organisation_id", ""), []).append(
            action
        )

    return [
        {
            "organisation_id": organisation_id,
            "organisation_name": group[0].get("organisation_name", ""),
            **_summarise_group(group),
        }
        for organisation_id, group in grouped_actions.items()
    ]


def summarise_governance_by_related_build(actions: list[dict]) -> list[dict]:
    """Return governance workload grouped by related portfolio build."""
    grouped_actions: dict[str, list[dict]] = {}
    for action in actions:
        grouped_actions.setdefault(action.get("related_build", ""), []).append(
            action
        )

    return [
        {
            "related_build": related_build,
            **_summarise_group(group),
        }
        for related_build, group in grouped_actions.items()
    ]


def prioritise_governance_actions(actions: list[dict]) -> list[dict]:
    """Return governance summaries sorted by risk, urgency, readiness, and due days."""
    summaries = build_all_governance_summaries(actions)
    return sorted(
        summaries,
        key=lambda summary: (
            GOVERNANCE_RISK_ORDER.get(
                summary["governance_delivery_risk"],
                99,
            ),
            SIGNOFF_URGENCY_ORDER.get(summary["signoff_urgency"], 99),
            CONTROL_READINESS_ORDER.get(summary["control_readiness"], 99),
            summary["due_in_days"],
            PRIORITY_ORDER.get(summary["priority"], 99),
        ),
    )


def generate_governance_recommendation(summary: dict) -> str:
    """Return deterministic governance action guidance."""
    if (
        summary.get("governance_delivery_risk")
        == "High governance delivery risk"
    ):
        return "Escalate governance review before this delivery action proceeds."
    if summary.get("signoff_urgency") == "Urgent sign-off":
        return "Secure sign-off before the next delivery checkpoint."
    if summary.get("control_readiness") == "Control blocked":
        return "Resolve the governance blocker before continuing implementation."
    if summary.get("control_readiness") == "Control needs review":
        return "Review the relevant control, approval point, or quality standard."
    if not summary.get("governance_signoff_required"):
        return (
            "No governance sign-off is currently required. "
            "Continue standard monitoring."
        )
    return "Review the relevant control, approval point, or quality standard."


def add_governance_recommendations(summaries: list[dict]) -> list[dict]:
    """Return copied summaries with governance recommendations added."""
    return [
        {
            **summary,
            "governance_recommendation": generate_governance_recommendation(
                summary
            ),
        }
        for summary in summaries
    ]
