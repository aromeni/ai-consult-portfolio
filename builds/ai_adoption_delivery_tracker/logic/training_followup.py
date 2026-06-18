"""Deterministic training follow-up and support planning for Build 8 Phase 5."""


TRAINING_URGENT_DAYS = 7
TRAINING_SOON_DAYS = 14

TRAINING_KEYWORDS = {
    "foundation": [
        "foundation",
        "basic",
        "introduction",
        "safe prompting",
        "confidence",
    ],
    "workflow": [
        "workflow",
        "task",
        "example",
        "template",
        "drafting",
        "checklist",
    ],
    "quality": ["quality", "review", "criteria", "standard", "sample"],
    "governance": [
        "governance",
        "policy",
        "responsible",
        "approval",
        "control",
    ],
    "coaching": [
        "coaching",
        "support",
        "practice",
        "guidance",
        "demonstration",
    ],
}

TRAINING_SUPPORT_LABELS = {
    "foundation": "Foundation AI training",
    "workflow": "Workflow-specific coaching",
    "quality": "Quality review training",
    "governance": "Responsible AI guidance",
    "coaching": "Practical coaching",
}

TRAINING_RISK_ORDER = {
    "High training delivery risk": 1,
    "Moderate training delivery risk": 2,
    "Low training delivery risk": 3,
}

TRAINING_URGENCY_ORDER = {
    "Urgent training follow-up": 1,
    "Training follow-up due soon": 2,
    "Routine training follow-up": 3,
    "No training follow-up required": 4,
}

SUPPORT_INTENSITY_ORDER = {
    "High support": 1,
    "Moderate support": 2,
    "Light support": 3,
    "No support required": 4,
}

PRIORITY_ORDER = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4,
}


def requires_training_followup(action: dict) -> bool:
    """Return True if training follow-up is explicitly required."""
    return action.get("training_followup_required") is True


def classify_training_followup_urgency(action: dict) -> str:
    """Classify how soon an explicit training follow-up is required."""
    if not requires_training_followup(action):
        return "No training follow-up required"

    due_in_days = action.get("due_in_days", 0)
    if due_in_days <= TRAINING_URGENT_DAYS:
        return "Urgent training follow-up"
    if due_in_days <= TRAINING_SOON_DAYS:
        return "Training follow-up due soon"
    return "Routine training follow-up"


def _combined_training_text(action: dict) -> str:
    """Return action text used for deterministic training keyword matching."""
    return " ".join(
        str(action.get(field, ""))
        for field in ("action_title", "action_description", "blocker")
    ).lower()


def classify_training_support_type(action: dict) -> str:
    """Classify the training support type using action and blocker text."""
    combined_text = _combined_training_text(action)

    for support_type, keywords in TRAINING_KEYWORDS.items():
        if any(keyword in combined_text for keyword in keywords):
            return TRAINING_SUPPORT_LABELS[support_type]

    if requires_training_followup(action):
        return "General support"
    return "No training support"


def classify_training_support_intensity(action: dict) -> str:
    """Classify the level of training support needed."""
    followup_required = requires_training_followup(action)
    support_type = classify_training_support_type(action)
    due_in_days = action.get("due_in_days", 0)

    if (
        followup_required and action.get("status") == "Blocked"
    ) or (
        action.get("priority") in {"Critical", "High"}
        and followup_required
        and due_in_days <= TRAINING_URGENT_DAYS
    ):
        return "High support"
    if (
        followup_required and due_in_days <= TRAINING_SOON_DAYS
    ) or support_type in {
        "Foundation AI training",
        "Workflow-specific coaching",
        "Responsible AI guidance",
    }:
        return "Moderate support"
    if followup_required:
        return "Light support"
    return "No support required"


def identify_training_delivery_need(action: dict) -> str:
    """Return the most appropriate training delivery method."""
    support_intensity = classify_training_support_intensity(action)
    support_type = classify_training_support_type(action)

    if support_intensity == "High support":
        return "Immediate coaching session"
    if support_type == "Workflow-specific coaching":
        return "Practical workflow demonstration"
    if support_type == "Quality review training":
        return "Quality review practice"
    if support_type == "Responsible AI guidance":
        return "Responsible-use refresher"
    if requires_training_followup(action):
        return "Peer support or office hours"
    return "No training delivery needed"


def classify_training_delivery_risk(action: dict) -> str:
    """Return the training delivery risk for one action."""
    support_intensity = classify_training_support_intensity(action)

    if support_intensity == "High support" or (
        requires_training_followup(action)
        and action.get("status") == "Blocked"
    ):
        return "High training delivery risk"
    if support_intensity == "Moderate support" or (
        requires_training_followup(action)
        and action.get("due_in_days", 0) <= TRAINING_SOON_DAYS
    ):
        return "Moderate training delivery risk"
    return "Low training delivery risk"


def build_training_followup_summary(action: dict) -> dict:
    """Return one action-level training follow-up summary."""
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
        "training_followup_required": requires_training_followup(action),
        "training_followup_urgency": (
            classify_training_followup_urgency(action)
        ),
        "training_support_type": classify_training_support_type(action),
        "training_support_intensity": (
            classify_training_support_intensity(action)
        ),
        "training_delivery_need": identify_training_delivery_need(action),
        "training_delivery_risk": classify_training_delivery_risk(action),
        "blocker": action.get("blocker", ""),
    }


def build_all_training_followup_summaries(actions: list[dict]) -> list[dict]:
    """Return a training follow-up summary for every action."""
    return [build_training_followup_summary(action) for action in actions]


def _summarise_group(group: list[dict]) -> dict:
    """Return shared training support counts for one action group."""
    summaries = build_all_training_followup_summaries(group)

    return {
        "total_actions": len(summaries),
        "training_followup_required_count": sum(
            summary["training_followup_required"] for summary in summaries
        ),
        "urgent_training_followup_count": sum(
            summary["training_followup_urgency"]
            == "Urgent training follow-up"
            for summary in summaries
        ),
        "high_support_count": sum(
            summary["training_support_intensity"] == "High support"
            for summary in summaries
        ),
        "moderate_support_count": sum(
            summary["training_support_intensity"] == "Moderate support"
            for summary in summaries
        ),
        "high_training_delivery_risk_count": sum(
            summary["training_delivery_risk"]
            == "High training delivery risk"
            for summary in summaries
        ),
        "immediate_coaching_count": sum(
            summary["training_delivery_need"] == "Immediate coaching session"
            for summary in summaries
        ),
        "workflow_demonstration_count": sum(
            summary["training_delivery_need"]
            == "Practical workflow demonstration"
            for summary in summaries
        ),
    }


def summarise_training_followup_by_organisation(
    actions: list[dict],
) -> list[dict]:
    """Return training follow-up workload grouped by organisation."""
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


def summarise_training_followup_by_related_build(
    actions: list[dict],
) -> list[dict]:
    """Return training follow-up workload grouped by related portfolio build."""
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


def summarise_training_followup_by_owner_role(
    actions: list[dict],
) -> list[dict]:
    """Return training support workload grouped by action owner role."""
    grouped_actions: dict[str, list[dict]] = {}
    for action in actions:
        grouped_actions.setdefault(action.get("owner_role", ""), []).append(
            action
        )

    summaries = []
    for owner_role, group in grouped_actions.items():
        group_summary = _summarise_group(group)
        summaries.append(
            {
                "owner_role": owner_role,
                "total_actions": group_summary["total_actions"],
                "training_followup_required_count": group_summary[
                    "training_followup_required_count"
                ],
                "high_support_count": group_summary["high_support_count"],
                "moderate_support_count": group_summary[
                    "moderate_support_count"
                ],
                "high_training_delivery_risk_count": group_summary[
                    "high_training_delivery_risk_count"
                ],
            }
        )
    return summaries


def prioritise_training_followup_actions(actions: list[dict]) -> list[dict]:
    """Return training summaries sorted by risk, urgency, support, and due days."""
    summaries = build_all_training_followup_summaries(actions)
    return sorted(
        summaries,
        key=lambda summary: (
            TRAINING_RISK_ORDER.get(summary["training_delivery_risk"], 99),
            TRAINING_URGENCY_ORDER.get(
                summary["training_followup_urgency"],
                99,
            ),
            SUPPORT_INTENSITY_ORDER.get(
                summary["training_support_intensity"],
                99,
            ),
            summary["due_in_days"],
            PRIORITY_ORDER.get(summary["priority"], 99),
        ),
    )


def generate_training_followup_recommendation(summary: dict) -> str:
    """Return deterministic training follow-up guidance."""
    recommendations = {
        "Immediate coaching session": (
            "Book an immediate coaching session with the action owner before "
            "implementation progresses."
        ),
        "Practical workflow demonstration": (
            "Run a practical workflow demonstration using examples from this action."
        ),
        "Quality review practice": (
            "Provide quality review practice so staff can check AI-supported "
            "outputs consistently."
        ),
        "Responsible-use refresher": (
            "Run a short responsible-use refresher covering safe use, "
            "escalation, and review expectations."
        ),
        "Peer support or office hours": (
            "Use peer support or office hours to answer questions and reinforce "
            "adoption confidence."
        ),
        "No training delivery needed": (
            "No specific training follow-up is required. "
            "Continue standard delivery monitoring."
        ),
    }
    return recommendations.get(
        summary.get("training_delivery_need"),
        recommendations["No training delivery needed"],
    )


def add_training_followup_recommendations(
    summaries: list[dict],
) -> list[dict]:
    """Return copied summaries with training recommendations added."""
    return [
        {
            **summary,
            "training_followup_recommendation": (
                generate_training_followup_recommendation(summary)
            ),
        }
        for summary in summaries
    ]
