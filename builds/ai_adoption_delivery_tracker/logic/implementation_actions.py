"""Validation and summary helpers for Build 8 implementation actions."""


REQUIRED_FIELDS = [
    "action_id",
    "organisation_id",
    "organisation_name",
    "workflow_id",
    "workflow_name",
    "related_build",
    "action_title",
    "action_description",
    "owner_role",
    "priority",
    "status",
    "due_in_days",
    "blocker",
    "governance_signoff_required",
    "training_followup_required",
    "client_checkin_required",
    "evidence_note",
]

ALLOWED_PRIORITIES = ("Low", "Medium", "High", "Critical")
ALLOWED_STATUSES = (
    "Not started",
    "In progress",
    "Blocked",
    "Completed",
    "Deferred",
)

BOOLEAN_FIELDS = (
    "governance_signoff_required",
    "training_followup_required",
    "client_checkin_required",
)


def validate_implementation_action(action: dict) -> list[str]:
    """Return validation warnings for one implementation action."""
    warnings = []

    for field in REQUIRED_FIELDS:
        if field not in action:
            warnings.append(f"Missing required field: {field}")

    if "priority" in action and action["priority"] not in ALLOWED_PRIORITIES:
        warnings.append(
            f"priority must be one of: {', '.join(ALLOWED_PRIORITIES)}"
        )

    if "status" in action and action["status"] not in ALLOWED_STATUSES:
        warnings.append(f"status must be one of: {', '.join(ALLOWED_STATUSES)}")

    if "due_in_days" in action:
        due_in_days = action["due_in_days"]
        if not isinstance(due_in_days, int) or isinstance(due_in_days, bool):
            warnings.append("due_in_days must be an integer")
        elif due_in_days < 0:
            warnings.append("due_in_days cannot be negative")

    for field in BOOLEAN_FIELDS:
        if field in action and not isinstance(action[field], bool):
            warnings.append(f"{field} must be a boolean")

    if "action_title" in action and not str(action["action_title"]).strip():
        warnings.append("action_title cannot be empty")

    if "owner_role" in action and not str(action["owner_role"]).strip():
        warnings.append("owner_role cannot be empty")

    return warnings


def validate_all_implementation_actions(actions: list[dict]) -> dict:
    """Validate all actions and return an action-level summary."""
    warnings = []
    actions_with_warnings = 0

    for action in actions:
        action_warnings = validate_implementation_action(action)
        if action_warnings:
            actions_with_warnings += 1
            action_id = action.get("action_id", "Unknown action")
            warnings.extend(
                f"{action_id}: {warning}" for warning in action_warnings
            )

    total_actions = len(actions)
    return {
        "total_actions": total_actions,
        "valid_actions": total_actions - actions_with_warnings,
        "actions_with_warnings": actions_with_warnings,
        "warnings": warnings,
    }


def calculate_action_counts_by_status(actions: list[dict]) -> dict:
    """Return counts for every allowed implementation status."""
    return {
        status: sum(1 for action in actions if action.get("status") == status)
        for status in ALLOWED_STATUSES
    }


def calculate_action_counts_by_priority(actions: list[dict]) -> dict:
    """Return counts for every allowed implementation priority."""
    return {
        priority: sum(
            1 for action in actions if action.get("priority") == priority
        )
        for priority in ALLOWED_PRIORITIES
    }


def summarise_phase_1_delivery_actions(actions: list[dict]) -> dict:
    """Return calculated Phase 1 delivery headline figures."""
    status_counts = calculate_action_counts_by_status(actions)
    priority_counts = calculate_action_counts_by_priority(actions)

    return {
        "total_actions": len(actions),
        "not_started_count": status_counts["Not started"],
        "in_progress_count": status_counts["In progress"],
        "blocked_count": status_counts["Blocked"],
        "completed_count": status_counts["Completed"],
        "deferred_count": status_counts["Deferred"],
        "critical_count": priority_counts["Critical"],
        "high_count": priority_counts["High"],
        "medium_count": priority_counts["Medium"],
        "low_count": priority_counts["Low"],
        "governance_signoff_required_count": sum(
            1 for action in actions if action.get("governance_signoff_required")
        ),
        "training_followup_required_count": sum(
            1 for action in actions if action.get("training_followup_required")
        ),
        "client_checkin_required_count": sum(
            1 for action in actions if action.get("client_checkin_required")
        ),
    }


def get_actions_by_organisation(
    actions: list[dict],
    organisation_id: str,
) -> list[dict]:
    """Return all actions belonging to one organisation."""
    return [
        action
        for action in actions
        if action.get("organisation_id") == organisation_id
    ]
