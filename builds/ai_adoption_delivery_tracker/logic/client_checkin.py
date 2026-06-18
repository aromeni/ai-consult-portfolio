"""Deterministic client check-in summaries for Build 8 Phase 6."""

from logic.action_tracker import build_action_tracker_summary


PRIORITY_ORDER = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4,
}


def get_actions_for_organisation(
    actions: list[dict],
    organisation_id: str,
) -> list[dict]:
    """Return all actions for one organisation."""
    return [
        action
        for action in actions
        if action.get("organisation_id") == organisation_id
    ]


def get_checkins_for_organisation(
    checkins: list[dict],
    organisation_id: str,
) -> list[dict]:
    """Return all check-ins for one organisation."""
    return [
        checkin
        for checkin in checkins
        if checkin.get("organisation_id") == organisation_id
    ]


def build_checkin_progress_snapshot(actions: list[dict]) -> dict:
    """Return headline action progress counts for a client check-in."""
    return {
        "total_actions": len(actions),
        "completed_count": sum(
            action.get("status") == "Completed" for action in actions
        ),
        "in_progress_count": sum(
            action.get("status") == "In progress" for action in actions
        ),
        "not_started_count": sum(
            action.get("status") == "Not started" for action in actions
        ),
        "blocked_count": sum(
            action.get("status") == "Blocked" for action in actions
        ),
        "deferred_count": sum(
            action.get("status") == "Deferred" for action in actions
        ),
        "critical_or_high_priority_count": sum(
            action.get("priority") in {"Critical", "High"}
            for action in actions
        ),
    }


def _needs_checkin_attention(action: dict) -> bool:
    """Return True when an action meets a client check-in attention rule."""
    return (
        action.get("status") == "Blocked"
        or action.get("priority") in {"Critical", "High"}
        or action.get("client_checkin_required") is True
        or action.get("governance_signoff_required") is True
        or (
            action.get("training_followup_required") is True
            and action.get("due_in_days", 0) <= 14
        )
    )


def identify_checkin_attention_items(actions: list[dict]) -> list[dict]:
    """Return prioritised action summaries needing check-in attention."""
    summaries = [
        build_action_tracker_summary(action)
        for action in actions
        if _needs_checkin_attention(action)
    ]
    return sorted(
        summaries,
        key=lambda summary: (
            summary["status"] != "Blocked",
            PRIORITY_ORDER.get(summary["priority"], 99),
            summary["due_in_days"],
        ),
    )


def classify_checkin_health(actions: list[dict]) -> str:
    """Classify the current implementation health for a client check-in."""
    if any(
        action.get("status") == "Blocked"
        and action.get("priority") == "Critical"
        for action in actions
    ):
        return "Blocked"

    high_or_critical_open = sum(
        action.get("priority") in {"Critical", "High"}
        and action.get("status") != "Completed"
        for action in actions
    )
    if any(action.get("status") == "Blocked" for action in actions):
        return "At risk"
    if high_or_critical_open >= 3:
        return "At risk"

    if any(
        action.get("status") != "Completed"
        and (
            action.get("client_checkin_required") is True
            or action.get("governance_signoff_required") is True
            or action.get("training_followup_required") is True
        )
        for action in actions
    ):
        return "Needs attention"

    return "On track"


def identify_client_decision_needs(actions: list[dict]) -> list[str]:
    """Return concise, deterministic client decision needs."""
    open_actions = [
        action for action in actions if action.get("status") != "Completed"
    ]
    decisions = []

    governance_count = sum(
        action.get("governance_signoff_required") is True
        for action in open_actions
    )
    if governance_count:
        decisions.append(
            f"Confirm governance sign-off for {governance_count} open action(s)."
        )

    blocked_count = sum(
        action.get("status") == "Blocked" for action in open_actions
    )
    if blocked_count:
        decisions.append(
            f"Agree how to unblock {blocked_count} blocked action(s)."
        )

    client_count = sum(
        action.get("client_checkin_required") is True
        for action in open_actions
    )
    if client_count:
        decisions.append(
            f"Confirm client direction for {client_count} open action(s)."
        )

    training_count = sum(
        action.get("training_followup_required") is True
        for action in open_actions
    )
    if training_count:
        decisions.append(
            f"Agree training follow-up for {training_count} open action(s)."
        )

    return decisions


def build_next_review_focus(actions: list[dict]) -> str:
    """Return the highest-priority deterministic next review focus."""
    if any(
        action.get("status") == "Blocked"
        and action.get("priority") in {"Critical", "High"}
        for action in actions
    ):
        return (
            "Resolve blocked Critical or High-priority actions before wider rollout."
        )

    if any(
        action.get("governance_signoff_required") is True
        and action.get("status") != "Completed"
        for action in actions
    ):
        return "Confirm outstanding governance sign-offs and approval conditions."

    if any(
        action.get("training_followup_required") is True
        and action.get("status") != "Completed"
        for action in actions
    ):
        return "Confirm training follow-up delivery and evidence of staff support."

    if any(
        action.get("client_checkin_required") is True
        and action.get("status") != "Completed"
        for action in actions
    ):
        return "Secure the client decisions needed to keep implementation moving."

    if any(action.get("status") == "Completed" for action in actions):
        return "Review completed action evidence and confirm the next implementation step."

    return "Review standard delivery progress and confirm the next action owners."


def build_client_checkin_summary(
    organisation: dict,
    actions: list[dict],
    checkins: list[dict],
) -> dict:
    """Return one organisation-level client check-in summary."""
    organisation_id = organisation.get("organisation_id", "")
    organisation_actions = get_actions_for_organisation(
        actions,
        organisation_id,
    )
    organisation_checkins = get_checkins_for_organisation(
        checkins,
        organisation_id,
    )
    attention_items = identify_checkin_attention_items(organisation_actions)
    latest_checkin = organisation_checkins[-1] if organisation_checkins else {}

    return {
        "organisation_id": organisation_id,
        "organisation_name": organisation.get("organisation_name", ""),
        "sector": organisation.get("sector", ""),
        "implementation_stage": organisation.get("implementation_stage", ""),
        "checkin_health": classify_checkin_health(organisation_actions),
        "progress_snapshot": build_checkin_progress_snapshot(
            organisation_actions
        ),
        "attention_item_count": len(attention_items),
        "client_decision_needs": identify_client_decision_needs(
            organisation_actions
        ),
        "latest_checkin_period": latest_checkin.get("checkin_period", ""),
        "latest_checkin_focus": latest_checkin.get("checkin_focus", ""),
        "latest_checkin_summary": latest_checkin.get("summary", ""),
        "next_review_focus": build_next_review_focus(organisation_actions),
    }


def build_all_client_checkin_summaries(
    organisations: list[dict],
    actions: list[dict],
    checkins: list[dict],
) -> list[dict]:
    """Return a client check-in summary for every organisation."""
    return [
        build_client_checkin_summary(organisation, actions, checkins)
        for organisation in organisations
    ]


def build_client_checkin_markdown(
    summary: dict,
    attention_items: list[dict],
) -> str:
    """Return a concise Markdown client check-in summary."""
    snapshot = summary.get("progress_snapshot", {})
    decisions = summary.get("client_decision_needs", [])

    lines = [
        f"# Client Check-in Summary — {summary.get('organisation_name', '')}",
        "",
        "## Current Health",
        "",
        f"- Health: {summary.get('checkin_health', '')}",
        f"- Implementation stage: {summary.get('implementation_stage', '')}",
        f"- Latest check-in: {summary.get('latest_checkin_period', '')}",
        f"- Latest focus: {summary.get('latest_checkin_focus', '')}",
        f"- Latest summary: {summary.get('latest_checkin_summary', '')}",
        "",
        "## Progress Snapshot",
        "",
        f"- Total actions: {snapshot.get('total_actions', 0)}",
        f"- Completed: {snapshot.get('completed_count', 0)}",
        f"- In progress: {snapshot.get('in_progress_count', 0)}",
        f"- Not started: {snapshot.get('not_started_count', 0)}",
        f"- Blocked: {snapshot.get('blocked_count', 0)}",
        f"- Deferred: {snapshot.get('deferred_count', 0)}",
        "",
        "## Key Attention Items",
        "",
    ]

    if attention_items:
        for item in attention_items:
            lines.append(
                f"- **{item.get('action_title', '')}** — "
                f"{item.get('priority', '')}, {item.get('status', '')}, "
                f"owner: {item.get('owner_role', '')}, "
                f"due in {item.get('due_in_days', 0)} day(s)."
            )
    else:
        lines.append("- No actions currently meet the check-in attention rules.")

    lines.extend(["", "## Client Decisions Needed", ""])
    if decisions:
        lines.extend(f"- {decision}" for decision in decisions)
    else:
        lines.append("- No specific client decisions are currently required.")

    lines.extend(
        [
            "",
            "## Next Review Focus",
            "",
            summary.get("next_review_focus", ""),
        ]
    )

    return "\n".join(lines)


def generate_checkin_recommendation(summary: dict) -> str:
    """Return deterministic guidance for the next client check-in."""
    recommendations = {
        "Blocked": (
            "Use the next check-in to unblock delivery before progressing "
            "wider rollout."
        ),
        "At risk": (
            "Focus the next check-in on reducing delivery risk and confirming ownership."
        ),
        "Needs attention": (
            "Use the next check-in to confirm decisions, dependencies, "
            "and follow-up actions."
        ),
        "On track": (
            "Use the next check-in to confirm progress evidence and prepare "
            "the next implementation step."
        ),
    }
    return recommendations.get(
        summary.get("checkin_health"),
        recommendations["Needs attention"],
    )


def add_checkin_recommendations(summaries: list[dict]) -> list[dict]:
    """Return copied summaries with check-in recommendations added."""
    return [
        {
            **summary,
            "checkin_recommendation": generate_checkin_recommendation(summary),
        }
        for summary in summaries
    ]
