"""Deterministic implementation progress report builder for Build 8 Phase 7."""

from data.synthetic_implementation_data import get_synthetic_delivery_organisations
from logic.action_tracker import (
    add_action_recommendations,
    prioritise_actions,
)
from logic.blocker_review import (
    add_blocker_recommendations,
    prioritise_blockers_for_resolution,
)
from logic.client_checkin import (
    build_all_client_checkin_summaries,
    build_client_checkin_summary,
)
from logic.governance_tracker import (
    add_governance_recommendations,
    prioritise_governance_actions,
)
from logic.training_followup import (
    add_training_followup_recommendations,
    prioritise_training_followup_actions,
)


def get_organisation_actions(
    actions: list[dict],
    organisation_id: str,
) -> list[dict]:
    """Return all actions for one organisation."""
    return [
        action
        for action in actions
        if action.get("organisation_id") == organisation_id
    ]


def build_markdown_table(rows: list[dict], columns: list[str]) -> str:
    """Return a simple Markdown table.

    Preserves column order, converts values to strings, handles empty rows.
    """
    if not rows:
        return "_No records to display._\n"

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    data_rows = [
        "| " + " | ".join(str(row.get(col, "")) for col in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *data_rows]) + "\n"


def build_report_title(organisation_name: str | None = None) -> str:
    """Return report title.

    Examples:
        # AI Adoption Implementation Progress Report
        # AI Adoption Implementation Progress Report — BrightPath Skills Training
    """
    base = "# AI Adoption Implementation Progress Report"
    if organisation_name:
        return f"{base} — {organisation_name}"
    return base


def build_report_disclaimer() -> str:
    """Return synthetic-data disclaimer."""
    return (
        "> **Disclaimer:** This report uses synthetic portfolio data only. "
        "It is for demonstration purposes and does not contain real client, "
        "staff, learner, safeguarding, HR, personal, confidential, or regulated data.\n"
    )


def build_executive_summary(actions: list[dict]) -> str:
    """Return concise Markdown executive summary."""
    total = len(actions)
    completed = sum(a.get("status") == "Completed" for a in actions)
    blocked = sum(a.get("status") == "Blocked" for a in actions)
    high_or_critical = sum(
        a.get("priority") in {"Critical", "High"} for a in actions
    )
    governance = sum(bool(a.get("governance_signoff_required")) for a in actions)
    training = sum(bool(a.get("training_followup_required")) for a in actions)
    checkin = sum(bool(a.get("client_checkin_required")) for a in actions)

    lines = [
        "## Executive Summary",
        "",
        f"- Total implementation actions: **{total}**",
        f"- Completed: **{completed}**",
        f"- Blocked: **{blocked}**",
        f"- High or critical priority: **{high_or_critical}**",
        f"- Governance sign-off required: **{governance}**",
        f"- Training follow-up required: **{training}**",
        f"- Client check-in required: **{checkin}**",
        "",
    ]
    return "\n".join(lines)


def build_delivery_progress_section(actions: list[dict]) -> str:
    """Return Markdown delivery progress section."""
    summaries = add_action_recommendations(prioritise_actions(actions))
    columns = [
        "action_title",
        "owner_role",
        "priority",
        "status",
        "due_in_days",
        "delivery_state",
        "attention_level",
        "action_recommendation",
    ]
    return "## Delivery Progress\n\n" + build_markdown_table(summaries, columns)


def build_blocker_dependency_section(actions: list[dict]) -> str:
    """Return Markdown blocker and dependency section."""
    summaries = add_blocker_recommendations(
        prioritise_blockers_for_resolution(actions)
    )
    columns = [
        "action_title",
        "blocker_type",
        "blocker_severity",
        "dependency_need",
        "delivery_risk_level",
        "requires_escalation",
        "blocker_recommendation",
    ]
    return (
        "## Blocker and Dependency Review\n\n"
        + build_markdown_table(summaries, columns)
    )


def build_governance_section(actions: list[dict]) -> str:
    """Return Markdown governance sign-off section."""
    summaries = add_governance_recommendations(
        prioritise_governance_actions(actions)
    )
    columns = [
        "action_title",
        "signoff_urgency",
        "control_area",
        "control_readiness",
        "governance_delivery_risk",
        "governance_recommendation",
    ]
    return (
        "## Governance Sign-off Position\n\n"
        + build_markdown_table(summaries, columns)
    )


def build_training_followup_section(actions: list[dict]) -> str:
    """Return Markdown training follow-up section."""
    summaries = add_training_followup_recommendations(
        prioritise_training_followup_actions(actions)
    )
    columns = [
        "action_title",
        "training_followup_urgency",
        "training_support_type",
        "training_support_intensity",
        "training_delivery_need",
        "training_followup_recommendation",
    ]
    return (
        "## Training Follow-up Plan\n\n"
        + build_markdown_table(summaries, columns)
    )


def build_client_checkin_section(
    organisation: dict | None,
    actions: list[dict],
    checkins: list[dict],
) -> str:
    """Return Markdown client check-in section."""
    lines = ["## Client Check-in Position", ""]

    if organisation is not None:
        summary = build_client_checkin_summary(organisation, actions, checkins)
        lines.extend([
            f"- **Health:** {summary['checkin_health']}",
            f"- **Attention items:** {summary['attention_item_count']}",
            (
                f"- **Latest check-in:** "
                f"{summary.get('latest_checkin_period', '')} — "
                f"{summary.get('latest_checkin_focus', '')}"
            ),
            f"- **Latest summary:** {summary.get('latest_checkin_summary', '')}",
            "",
            "**Client decisions needed:**",
            "",
        ])
        decisions = summary.get("client_decision_needs", [])
        if decisions:
            lines.extend(f"- {decision}" for decision in decisions)
        else:
            lines.append("- No specific client decisions are currently required.")
        lines.extend([
            "",
            f"**Next review focus:** {summary['next_review_focus']}",
            "",
        ])
    else:
        organisations = get_synthetic_delivery_organisations()
        summaries = build_all_client_checkin_summaries(
            organisations, actions, checkins
        )
        for summary in summaries:
            decision_count = len(summary.get("client_decision_needs", []))
            lines.extend([
                f"### {summary['organisation_name']}",
                "",
                f"- **Health:** {summary['checkin_health']}",
                f"- **Attention items:** {summary['attention_item_count']}",
                f"- **Client decisions:** {decision_count} item(s)",
                f"- **Next review focus:** {summary['next_review_focus']}",
                "",
            ])

    return "\n".join(lines)


def build_priority_next_actions_section(actions: list[dict]) -> str:
    """Return Markdown priority next actions section (top 10 actions only)."""
    summaries = add_action_recommendations(prioritise_actions(actions))[:10]
    columns = [
        "action_title",
        "organisation_name",
        "owner_role",
        "priority",
        "status",
        "due_in_days",
        "attention_level",
        "action_recommendation",
    ]
    return (
        "## Priority Next Actions\n\n"
        + build_markdown_table(summaries, columns)
    )


def build_consulting_interpretation_section() -> str:
    """Return deterministic consulting interpretation."""
    return (
        "## Consulting Interpretation\n\n"
        "This report helps a consultant move from recommendations to managed "
        "implementation. It shows which actions are progressing, which items are "
        "blocked, where governance or training support is needed, and what should "
        "be reviewed at the next client checkpoint.\n"
    )


def build_next_review_section() -> str:
    """Return deterministic next review section."""
    return (
        "## Next Review\n\n"
        "At the next review, confirm whether blocked actions have been resolved, "
        "sign-offs have been completed, training follow-up has been delivered, "
        "and high-priority actions have moved forward.\n"
    )


def build_full_progress_report(
    organisations: list[dict],
    actions: list[dict],
    checkins: list[dict],
    organisation_id: str | None = None,
) -> str:
    """Build a complete Markdown implementation progress report.

    If organisation_id is provided, report only on that organisation.
    If None, build a portfolio-level report across all synthetic records.
    """
    if organisation_id is not None:
        organisation = next(
            (
                o for o in organisations
                if o.get("organisation_id") == organisation_id
            ),
            None,
        )
        scoped_actions = get_organisation_actions(actions, organisation_id)
        org_name = organisation.get("organisation_name") if organisation else None
    else:
        organisation = None
        scoped_actions = actions
        org_name = None

    sections = [
        build_report_title(org_name),
        "",
        build_report_disclaimer(),
        build_executive_summary(scoped_actions),
        build_delivery_progress_section(scoped_actions),
        build_blocker_dependency_section(scoped_actions),
        build_governance_section(scoped_actions),
        build_training_followup_section(scoped_actions),
        build_client_checkin_section(organisation, scoped_actions, checkins),
        build_priority_next_actions_section(scoped_actions),
        build_consulting_interpretation_section(),
        build_next_review_section(),
    ]
    return "\n".join(sections)
