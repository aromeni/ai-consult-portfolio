"""Deterministic action tracking and prioritisation for Build 8 Phase 2."""


URGENT_DUE_DAYS = 7
SOON_DUE_DAYS = 14
LONG_DUE_DAYS = 30

STATUS_PRIORITY = {
    "Blocked": 1,
    "In progress": 2,
    "Not started": 3,
    "Deferred": 4,
    "Completed": 5,
}

PRIORITY_WEIGHT = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1,
}


def classify_due_window(action: dict) -> str:
    """Classify an action by the number of days until it is due."""
    due_in_days = action.get("due_in_days", 0)

    if due_in_days <= URGENT_DUE_DAYS:
        return "Due now"
    if due_in_days <= SOON_DUE_DAYS:
        return "Due soon"
    if due_in_days <= LONG_DUE_DAYS:
        return "Due later"
    return "No immediate pressure"


def classify_action_attention_level(action: dict) -> str:
    """Return the delivery attention level for one action."""
    if action.get("status") == "Blocked" or action.get("priority") == "Critical":
        return "Critical attention"
    if (
        action.get("priority") == "High"
        or action.get("due_in_days", 0) <= URGENT_DUE_DAYS
    ):
        return "High attention"
    if (
        action.get("status") in {"In progress", "Not started"}
        or action.get("due_in_days", 0) <= SOON_DUE_DAYS
    ):
        return "Medium attention"
    return "Low attention"


def is_action_blocked(action: dict) -> bool:
    """Return True when status or blocker text indicates a blocked action."""
    return (
        action.get("status") == "Blocked"
        or bool(str(action.get("blocker", "")).strip())
    )


def is_action_complete(action: dict) -> bool:
    """Return True when the action status is Completed."""
    return action.get("status") == "Completed"


def classify_delivery_state(action: dict) -> str:
    """Return a normalised delivery state for one action."""
    if is_action_complete(action):
        return "Completed"
    if is_action_blocked(action):
        return "Blocked"
    if action.get("status") == "In progress":
        return "Active"
    if action.get("status") == "Not started":
        return "Waiting"
    if action.get("status") == "Deferred":
        return "Deferred"
    return "Waiting"


def calculate_action_score(action: dict) -> int:
    """Calculate a deterministic delivery priority score."""
    score = PRIORITY_WEIGHT.get(action.get("priority"), 0) * 10
    due_in_days = action.get("due_in_days", 0)

    if is_action_blocked(action):
        score += 20
    if due_in_days <= URGENT_DUE_DAYS:
        score += 10
    if due_in_days <= SOON_DUE_DAYS:
        score += 5
    if is_action_complete(action):
        score -= 10

    return max(score, 0)


def build_action_tracker_summary(action: dict) -> dict:
    """Return one action-level tracking summary."""
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
        "due_window": classify_due_window(action),
        "delivery_state": classify_delivery_state(action),
        "attention_level": classify_action_attention_level(action),
        "action_score": calculate_action_score(action),
        "blocker": action.get("blocker", ""),
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


def build_all_action_tracker_summaries(actions: list[dict]) -> list[dict]:
    """Return an action tracker summary for every action."""
    return [build_action_tracker_summary(action) for action in actions]


def prioritise_actions(actions: list[dict]) -> list[dict]:
    """Return action summaries sorted by score, status priority, and due days."""
    summaries = build_all_action_tracker_summaries(actions)
    return sorted(
        summaries,
        key=lambda summary: (
            -summary["action_score"],
            STATUS_PRIORITY.get(summary["status"], 99),
            summary["due_in_days"],
        ),
    )


def _summarise_group(group: list[dict]) -> dict:
    """Return shared delivery counts for one grouped set of actions."""
    summaries = build_all_action_tracker_summaries(group)
    total_actions = len(summaries)

    return {
        "total_actions": total_actions,
        "completed_count": sum(
            summary["delivery_state"] == "Completed" for summary in summaries
        ),
        "blocked_count": sum(
            summary["delivery_state"] == "Blocked" for summary in summaries
        ),
        "active_count": sum(
            summary["delivery_state"] == "Active" for summary in summaries
        ),
        "waiting_count": sum(
            summary["delivery_state"] == "Waiting" for summary in summaries
        ),
        "deferred_count": sum(
            summary["delivery_state"] == "Deferred" for summary in summaries
        ),
        "critical_attention_count": sum(
            summary["attention_level"] == "Critical attention"
            for summary in summaries
        ),
        "high_attention_count": sum(
            summary["attention_level"] == "High attention"
            for summary in summaries
        ),
        "average_action_score": round(
            sum(summary["action_score"] for summary in summaries) / total_actions,
            2,
        )
        if total_actions
        else 0.0,
    }


def summarise_actions_by_organisation(actions: list[dict]) -> list[dict]:
    """Return action tracking counts grouped by organisation."""
    grouped_actions: dict[str, list[dict]] = {}

    for action in actions:
        grouped_actions.setdefault(action.get("organisation_id", ""), []).append(
            action
        )

    organisation_summaries = []
    for organisation_id, group in grouped_actions.items():
        organisation_summaries.append(
            {
                "organisation_id": organisation_id,
                "organisation_name": group[0].get("organisation_name", ""),
                **_summarise_group(group),
            }
        )

    return organisation_summaries


def summarise_actions_by_related_build(actions: list[dict]) -> list[dict]:
    """Return action tracking counts grouped by related portfolio build."""
    grouped_actions: dict[str, list[dict]] = {}

    for action in actions:
        grouped_actions.setdefault(action.get("related_build", ""), []).append(
            action
        )

    build_summaries = []
    for related_build, group in grouped_actions.items():
        build_summaries.append(
            {
                "related_build": related_build,
                **_summarise_group(group),
            }
        )

    return build_summaries


def generate_action_tracker_recommendation(summary: dict) -> str:
    """Return deterministic delivery guidance for one action summary."""
    if summary.get("delivery_state") == "Completed":
        return (
            "No further delivery action required unless follow-up evidence is needed."
        )
    if summary.get("attention_level") == "Critical attention":
        return (
            "Escalate this action. It is blocked, critical, or requires "
            "immediate delivery attention."
        )
    if summary.get("attention_level") == "High attention":
        return "Prioritise this action in the next delivery check-in."
    if summary.get("attention_level") == "Medium attention":
        return "Keep this action moving and confirm progress at the next review."
    return "Monitor this action as part of standard delivery tracking."


def add_action_recommendations(summaries: list[dict]) -> list[dict]:
    """Return copied summaries with deterministic recommendations added."""
    return [
        {
            **summary,
            "action_recommendation": generate_action_tracker_recommendation(
                summary
            ),
        }
        for summary in summaries
    ]
