"""Deterministic blocker, risk, and dependency review for Build 8 Phase 3."""


BLOCKER_KEYWORDS = {
    "governance": [
        "governance",
        "sign-off",
        "signoff",
        "approval",
        "policy",
        "control",
    ],
    "training": ["training", "confidence", "coaching", "guidance", "staff"],
    "client": ["client", "check-in", "review", "agreement", "feedback"],
    "quality": ["quality", "checklist", "criteria", "standard", "review"],
    "ownership": ["owner", "ownership", "role", "responsibility"],
}

SEVERITY_ORDER = {
    "Critical blocker": 1,
    "High blocker": 2,
    "Moderate blocker": 3,
    "Low blocker": 4,
    "No blocker": 5,
}

DELIVERY_RISK_ORDER = {
    "High delivery risk": 1,
    "Moderate delivery risk": 2,
    "Low delivery risk": 3,
}

PRIORITY_ORDER = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4,
}

BLOCKER_TYPE_LABELS = {
    "governance": "Governance blocker",
    "training": "Training blocker",
    "client": "Client decision blocker",
    "quality": "Quality blocker",
    "ownership": "Ownership blocker",
}


def has_blocker(action: dict) -> bool:
    """Return True if status is Blocked or blocker text is non-empty."""
    return (
        action.get("status") == "Blocked"
        or bool(str(action.get("blocker", "")).strip())
    )


def classify_blocker_type(action: dict) -> str:
    """Classify blocker text using the configured keyword groups."""
    if not has_blocker(action):
        return "No blocker"

    blocker_text = str(action.get("blocker", "")).strip().lower()
    for blocker_type, keywords in BLOCKER_KEYWORDS.items():
        if any(keyword in blocker_text for keyword in keywords):
            return BLOCKER_TYPE_LABELS[blocker_type]

    return "General delivery blocker"


def classify_blocker_severity(action: dict) -> str:
    """Return the blocker severity for one implementation action."""
    if not has_blocker(action):
        return "No blocker"

    status = action.get("status")
    priority = action.get("priority")
    due_in_days = action.get("due_in_days", 0)

    if status == "Blocked" and priority == "Critical":
        return "Critical blocker"
    if (
        status == "Blocked"
        or priority == "Critical"
        or due_in_days <= 7
    ):
        return "High blocker"
    if priority == "High" or due_in_days <= 14:
        return "Moderate blocker"
    return "Low blocker"


def calculate_dependency_count(action: dict) -> int:
    """Count governance, training, and client check-in dependencies."""
    dependency_fields = (
        "governance_signoff_required",
        "training_followup_required",
        "client_checkin_required",
    )
    return sum(bool(action.get(field)) for field in dependency_fields)


def classify_dependency_need(action: dict) -> str:
    """Classify the action's primary implementation dependency."""
    dependencies = [
        (
            "Governance dependency",
            bool(action.get("governance_signoff_required")),
        ),
        (
            "Training dependency",
            bool(action.get("training_followup_required")),
        ),
        (
            "Client check-in dependency",
            bool(action.get("client_checkin_required")),
        ),
    ]
    active_dependencies = [
        label for label, is_required in dependencies if is_required
    ]

    if len(active_dependencies) >= 2:
        return "Multiple dependencies"
    if len(active_dependencies) == 1:
        return active_dependencies[0]
    return "No major dependency"


def classify_delivery_risk_level(action: dict) -> str:
    """Return the delivery risk level for one implementation action."""
    blocker_severity = classify_blocker_severity(action)
    dependency_count = calculate_dependency_count(action)
    priority = action.get("priority")

    if blocker_severity == "Critical blocker" or (
        dependency_count >= 2 and priority in {"Critical", "High"}
    ):
        return "High delivery risk"
    if (
        blocker_severity == "High blocker"
        or dependency_count >= 1
        or (
            action.get("due_in_days", 0) <= 7
            and action.get("status") != "Completed"
        )
    ):
        return "Moderate delivery risk"
    return "Low delivery risk"


def requires_escalation(action: dict) -> bool:
    """Return True when blocker severity, risk, or due pressure needs escalation."""
    blocker_severity = classify_blocker_severity(action)
    delivery_risk_level = classify_delivery_risk_level(action)

    return (
        blocker_severity in {"Critical blocker", "High blocker"}
        or delivery_risk_level == "High delivery risk"
        or (
            action.get("status") == "Blocked"
            and action.get("due_in_days", 0) <= 14
        )
    )


def build_blocker_review_summary(action: dict) -> dict:
    """Return one action-level blocker review summary."""
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
        "blocker": action.get("blocker", ""),
        "has_blocker": has_blocker(action),
        "blocker_type": classify_blocker_type(action),
        "blocker_severity": classify_blocker_severity(action),
        "dependency_need": classify_dependency_need(action),
        "dependency_count": calculate_dependency_count(action),
        "delivery_risk_level": classify_delivery_risk_level(action),
        "requires_escalation": requires_escalation(action),
        "governance_signoff_required": action.get(
            "governance_signoff_required",
            False,
        ),
        "training_followup_required": action.get(
            "training_followup_required",
            False,
        ),
        "client_checkin_required": action.get(
            "client_checkin_required",
            False,
        ),
    }


def build_all_blocker_review_summaries(actions: list[dict]) -> list[dict]:
    """Return a blocker review summary for every action."""
    return [build_blocker_review_summary(action) for action in actions]


def _summarise_group(group: list[dict]) -> dict:
    """Return shared blocker and dependency counts for one action group."""
    summaries = build_all_blocker_review_summaries(group)

    return {
        "total_actions": len(summaries),
        "blocked_action_count": sum(
            summary["has_blocker"] for summary in summaries
        ),
        "critical_blocker_count": sum(
            summary["blocker_severity"] == "Critical blocker"
            for summary in summaries
        ),
        "high_blocker_count": sum(
            summary["blocker_severity"] == "High blocker"
            for summary in summaries
        ),
        "escalation_required_count": sum(
            summary["requires_escalation"] for summary in summaries
        ),
        "high_delivery_risk_count": sum(
            summary["delivery_risk_level"] == "High delivery risk"
            for summary in summaries
        ),
        "governance_dependency_count": sum(
            summary["governance_signoff_required"] for summary in summaries
        ),
        "training_dependency_count": sum(
            summary["training_followup_required"] for summary in summaries
        ),
        "client_checkin_dependency_count": sum(
            summary["client_checkin_required"] for summary in summaries
        ),
    }


def summarise_blockers_by_organisation(actions: list[dict]) -> list[dict]:
    """Return blocker exposure grouped by organisation."""
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


def summarise_blockers_by_related_build(actions: list[dict]) -> list[dict]:
    """Return blocker exposure grouped by related portfolio build."""
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


def prioritise_blockers_for_resolution(actions: list[dict]) -> list[dict]:
    """Return blocker summaries ordered by escalation, severity, risk, and due pressure."""
    summaries = build_all_blocker_review_summaries(actions)
    return sorted(
        summaries,
        key=lambda summary: (
            not summary["requires_escalation"],
            SEVERITY_ORDER.get(summary["blocker_severity"], 99),
            DELIVERY_RISK_ORDER.get(summary["delivery_risk_level"], 99),
            summary["due_in_days"],
            PRIORITY_ORDER.get(summary["priority"], 99),
        ),
    )


def generate_blocker_resolution_recommendation(summary: dict) -> str:
    """Return deterministic blocker resolution guidance."""
    recommendations = {
        "Governance blocker": (
            "Escalate governance approval or control clarification before "
            "this action proceeds."
        ),
        "Training blocker": (
            "Resolve the training gap through focused support, examples, or coaching."
        ),
        "Client decision blocker": (
            "Use the next client check-in to secure a clear decision or agreed direction."
        ),
        "Quality blocker": (
            "Clarify quality criteria and agree a review standard before continuing."
        ),
        "Ownership blocker": (
            "Confirm ownership and accountability before this action can progress."
        ),
        "General delivery blocker": (
            "Review the blocker with the action owner and agree the next delivery step."
        ),
        "No blocker": (
            "No blocker-specific action required. Continue standard delivery monitoring."
        ),
    }
    return recommendations.get(
        summary.get("blocker_type"),
        recommendations["General delivery blocker"],
    )


def add_blocker_recommendations(summaries: list[dict]) -> list[dict]:
    """Return copied summaries with blocker recommendations added."""
    return [
        {
            **summary,
            "blocker_recommendation": (
                generate_blocker_resolution_recommendation(summary)
            ),
        }
        for summary in summaries
    ]
