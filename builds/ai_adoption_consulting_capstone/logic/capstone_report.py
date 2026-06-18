"""Capstone report builder for Build 9 Phase 6."""

from logic.capstone_dashboard import (
    build_capstone_snapshot,
    build_portfolio_dashboard_context,
)
from logic.capstone_overview import get_stages_for_client, summarise_phase_1_capstone
from logic.client_journey import (
    add_journey_recommendations,
    build_all_client_journey_summaries,
)
from logic.cross_build_insights import (
    add_cross_build_recommendations,
    build_all_cross_build_summaries,
)
from logic.recommendation_pathway import (
    add_consulting_recommendation_text,
    build_all_consulting_recommendations,
)


def build_markdown_table(rows: list[dict], columns: list[str]) -> str:
    """Return a simple Markdown table."""
    if not rows:
        return "_No data available._\n"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body_lines = []
    for row in rows:
        cells = " | ".join(str(row.get(col, "")) for col in columns)
        body_lines.append(f"| {cells} |")
    return "\n".join([header, separator] + body_lines) + "\n"


def get_client_by_id(clients: list[dict], client_id: str) -> dict | None:
    """Return one client by client_id."""
    for client in clients:
        if client.get("client_id") == client_id:
            return client
    return None


def get_report_clients(
    clients: list[dict], client_id: str | None = None
) -> list[dict]:
    """Return all clients, or the selected client when client_id is provided."""
    if client_id is None:
        return clients
    client = get_client_by_id(clients, client_id)
    return [client] if client else []


def get_report_stages_for_client(
    stages: list[dict], client_id: str | None = None
) -> list[dict]:
    """Return all stages, or stages for one client if client_id is provided."""
    if client_id is None:
        return stages
    return get_stages_for_client(stages, client_id)


def get_report_indicators_for_client(
    indicators: list[dict], client_id: str | None = None
) -> list[dict]:
    """Return all indicators, or indicators for one client if client_id is provided."""
    if client_id is None:
        return indicators
    return [i for i in indicators if i.get("client_id") == client_id]


def build_report_title(client: dict | None = None) -> str:
    """Return Markdown report title."""
    if client:
        name = client.get("organisation_name", "")
        return f"# AI Adoption Consulting Capstone Report — {name}\n"
    return "# AI Adoption Consulting Capstone Report\n"


def build_report_disclaimer() -> str:
    """Return synthetic-data disclaimer."""
    return (
        "> **Disclaimer:** This report uses synthetic portfolio data only. "
        "It is for demonstration purposes and does not contain real client, "
        "staff, learner, safeguarding, HR, personal, confidential, or regulated data.\n"
    )


def build_executive_summary(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
    client_id: str | None = None,
) -> str:
    """Return concise Markdown executive summary."""
    report_clients = get_report_clients(clients, client_id)
    report_stages = get_report_stages_for_client(stages, client_id)
    report_indicators = get_report_indicators_for_client(indicators, client_id)

    phase_1 = summarise_phase_1_capstone(
        report_clients, report_stages, report_indicators
    )
    context = build_portfolio_dashboard_context(
        report_clients, report_stages, report_indicators
    )
    snapshot = build_capstone_snapshot(context)
    build_insights = context.get("cross_build_insight_summary", {})

    if client_id:
        client = report_clients[0] if report_clients else {}
        org_line = (
            f"- **Organisation:** {client.get('organisation_name', 'Not available')} "
            f"({client.get('sector', 'Not available')})"
        )
        readiness_label = "Client readiness"
    else:
        org_line = f"- **Clients in scope:** {phase_1['total_clients']}"
        readiness_label = "Portfolio readiness"

    lines = [
        "## Executive Summary\n",
        org_line,
        f"- **Journey stages:** {phase_1['total_cross_build_stages']} total, "
        f"{phase_1['completed_stage_count']} completed",
        f"- **Strongest build area:** {build_insights.get('strongest_build_area', 'Not available')}",
        f"- **Weakest build area:** {build_insights.get('weakest_build_area', 'Not available')}",
        f"- **{readiness_label}:** {snapshot['dashboard_status']}",
        f"- **Recommended next step:** {snapshot['recommended_dashboard_next_step']}",
    ]
    return "\n".join(lines) + "\n"


def build_client_overview_section(
    clients: list[dict],
    client_id: str | None = None,
) -> str:
    """Return Markdown client overview section."""
    report_clients = get_report_clients(clients, client_id)

    columns = [
        "organisation_name",
        "sector",
        "staff_count",
        "capstone_stage",
        "primary_ai_goal",
        "consulting_priority",
    ]
    rows = [{col: c.get(col, "") for col in columns} for c in report_clients]
    return "## Client Overview\n\n" + build_markdown_table(rows, columns)


def build_ai_adoption_journey_section(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
    client_id: str | None = None,
) -> str:
    """Return Markdown AI adoption journey section."""
    report_clients = get_report_clients(clients, client_id)
    report_stages = get_report_stages_for_client(stages, client_id)
    report_indicators = get_report_indicators_for_client(indicators, client_id)
    summaries = add_journey_recommendations(
        build_all_client_journey_summaries(
            report_clients, report_stages, report_indicators
        )
    )

    columns = [
        "organisation_name",
        "journey_health",
        "stage_completion_rate",
        "average_evidence_score",
        "weakest_stage",
        "next_journey_step",
        "overall_capstone_status",
    ]
    rows = [{col: s.get(col, "") for col in columns} for s in summaries]
    return "## AI Adoption Journey\n\n" + build_markdown_table(rows, columns)


def build_cross_build_evidence_section(stages: list[dict]) -> str:
    """Return Markdown cross-build evidence section."""
    summaries = add_cross_build_recommendations(build_all_cross_build_summaries(stages))
    columns = [
        "build_number",
        "build_domain",
        "completion_rate",
        "average_evidence_score",
        "evidence_health",
        "build_gap",
        "cross_build_recommendation",
    ]
    rows = [{col: s.get(col, "") for col in columns} for s in summaries]
    return "## Cross-Build Evidence\n\n" + build_markdown_table(rows, columns)


def build_recommendation_pathway_section(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
    client_id: str | None = None,
) -> str:
    """Return Markdown recommendation pathway section."""
    report_clients = get_report_clients(clients, client_id)
    report_stages = get_report_stages_for_client(stages, client_id)
    report_indicators = get_report_indicators_for_client(indicators, client_id)
    journey_summaries = build_all_client_journey_summaries(
        report_clients, report_stages, report_indicators
    )
    recommendations = add_consulting_recommendation_text(
        build_all_consulting_recommendations(journey_summaries)
    )

    columns = [
        "organisation_name",
        "capstone_readiness",
        "consulting_pathway",
        "commercial_next_step",
        "primary_improvement_area",
        "recommendation_priority",
        "consulting_recommendation",
    ]
    rows = [{col: r.get(col, "") for col in columns} for r in recommendations]
    return "## Consulting Recommendation Pathway\n\n" + build_markdown_table(rows, columns)


def build_capstone_snapshot_section(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
    client_id: str | None = None,
) -> str:
    """Return Markdown capstone snapshot section, scoped to one client if client_id is provided."""
    report_clients = get_report_clients(clients, client_id)
    report_stages = get_report_stages_for_client(stages, client_id)
    report_indicators = get_report_indicators_for_client(indicators, client_id)
    context = build_portfolio_dashboard_context(
        report_clients, report_stages, report_indicators
    )
    snapshot = build_capstone_snapshot(context)
    lines = [
        "## Capstone Snapshot\n",
        f"- **Dashboard status:** {snapshot['dashboard_status']}",
        f"- **Dashboard focus:** {snapshot['dashboard_focus']}",
        f"- **Strongest build area:** {snapshot['strongest_build_area']}",
        f"- **Weakest build area:** {snapshot['weakest_build_area']}",
        f"- **Recommended next step:** {snapshot['recommended_dashboard_next_step']}",
    ]
    return "\n".join(lines) + "\n"


def build_consulting_interpretation_section() -> str:
    """Return deterministic consulting interpretation."""
    return (
        "## Consulting Interpretation\n\n"
        "This capstone report brings the separate portfolio builds into one consulting "
        "narrative. It shows how readiness, document intelligence, training, reporting, "
        "governance, ROI, and delivery tracking can form a practical AI adoption service "
        "for small organisations.\n"
    )


def build_next_steps_section(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
    client_id: str | None = None,
) -> str:
    """Return Markdown next steps section."""
    report_clients = get_report_clients(clients, client_id)
    report_stages = get_report_stages_for_client(stages, client_id)
    report_indicators = get_report_indicators_for_client(indicators, client_id)
    journey_summaries = build_all_client_journey_summaries(
        report_clients, report_stages, report_indicators
    )
    recommendations = add_consulting_recommendation_text(
        build_all_consulting_recommendations(journey_summaries)
    )

    _readiness_bullets = {
        "Capstone ready": "prepare a polished portfolio evidence pack and presentation.",
        "Nearly ready": "polish remaining evidence and tighten the consulting recommendations.",
        "Needs strengthening": "focus on the weakest journey stage and improve supporting outputs.",
        "Not ready": "resolve blocked or missing journey stages before presenting as complete.",
    }

    lines = ["## Next Steps\n"]
    for rec in recommendations:
        org = rec.get("organisation_name", "")
        readiness = rec.get("capstone_readiness", "")
        bullet = _readiness_bullets.get(readiness, "review the capstone readiness classification.")
        lines.append(f"- **{org}:** {bullet}")
    return "\n".join(lines) + "\n"


def build_full_capstone_report(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
    client_id: str | None = None,
) -> str:
    """
    Build a complete Markdown capstone report.

    If client_id is provided, report only on that client.
    If None, build a portfolio-level report.
    """
    client = get_client_by_id(clients, client_id) if client_id else None
    report_stages = get_report_stages_for_client(stages, client_id)

    sections = [
        build_report_title(client),
        build_report_disclaimer(),
        build_executive_summary(clients, stages, indicators, client_id),
        build_client_overview_section(clients, client_id),
        build_capstone_snapshot_section(clients, stages, indicators, client_id),
        build_ai_adoption_journey_section(clients, stages, indicators, client_id),
        build_cross_build_evidence_section(report_stages),
        build_recommendation_pathway_section(clients, stages, indicators, client_id),
        build_consulting_interpretation_section(),
        build_next_steps_section(clients, stages, indicators, client_id),
    ]
    return "\n".join(sections)
