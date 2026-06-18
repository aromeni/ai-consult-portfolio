"""Capstone dashboard context builder for Build 9 Phase 5."""

from logic.capstone_overview import (
    get_indicator_for_client,
    get_stages_for_client,
    summarise_phase_1_capstone,
)
from logic.client_journey import (
    add_journey_recommendations,
    build_all_client_journey_summaries,
    build_client_journey_summary,
    summarise_journey_health,
)
from logic.cross_build_insights import (
    add_cross_build_recommendations,
    build_all_cross_build_summaries,
    summarise_cross_build_insights,
)
from logic.recommendation_pathway import (
    add_consulting_recommendation_text,
    build_all_consulting_recommendations,
    build_consulting_recommendation_summary,
    summarise_recommendation_pathways,
)


def build_client_dashboard_context(
    client: dict,
    stages: list[dict],
    indicators: list[dict],
) -> dict:
    """Return all dashboard context for one client."""
    client_id = client.get("client_id", "")
    client_stages = get_stages_for_client(stages, client_id)
    indicator = get_indicator_for_client(indicators, client_id)
    journey_summary = build_client_journey_summary(client, client_stages, indicator)
    recommendation_summary = build_consulting_recommendation_summary(journey_summary)
    return {
        "client": client,
        "client_stages": client_stages,
        "indicator": indicator,
        "journey_summary": journey_summary,
        "recommendation_summary": recommendation_summary,
    }


def build_portfolio_dashboard_context(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
) -> dict:
    """Return all dashboard context for the portfolio-level dashboard."""
    phase_1_summary = summarise_phase_1_capstone(clients, stages, indicators)
    journey_summaries = add_journey_recommendations(
        build_all_client_journey_summaries(clients, stages, indicators)
    )
    journey_health_summary = summarise_journey_health(journey_summaries)
    cross_build_summaries = add_cross_build_recommendations(
        build_all_cross_build_summaries(stages)
    )
    cross_build_insight_summary = summarise_cross_build_insights(cross_build_summaries)
    recommendations = add_consulting_recommendation_text(
        build_all_consulting_recommendations(journey_summaries)
    )
    recommendation_pathway_summary = summarise_recommendation_pathways(recommendations)
    return {
        "clients": clients,
        "stages": stages,
        "indicators": indicators,
        "phase_1_summary": phase_1_summary,
        "journey_summaries": journey_summaries,
        "journey_health_summary": journey_health_summary,
        "cross_build_summaries": cross_build_summaries,
        "cross_build_insight_summary": cross_build_insight_summary,
        "recommendations": recommendations,
        "recommendation_pathway_summary": recommendation_pathway_summary,
    }


def classify_dashboard_status(context: dict) -> str:
    """
    Return one of:
    - "Strong capstone dashboard"
    - "Portfolio-ready dashboard"
    - "Developing dashboard"
    - "Needs review"
    """
    rec = context.get("recommendation_pathway_summary", {})
    journey = context.get("journey_health_summary", {})
    builds = context.get("cross_build_insight_summary", {})

    capstone_ready = rec.get("capstone_ready_count", 0)
    nearly_ready = rec.get("nearly_ready_count", 0)
    strong_journey = journey.get("strong_journey_count", 0)
    blocked_journey = journey.get("blocked_journey_count", 0)
    weak_evidence = builds.get("weak_evidence_count", 0)

    if capstone_ready >= 1 and strong_journey >= 1 and weak_evidence == 0:
        return "Strong capstone dashboard"
    if nearly_ready + capstone_ready >= 1 and blocked_journey == 0:
        return "Portfolio-ready dashboard"
    if blocked_journey > 0 or weak_evidence > 0:
        return "Needs review"
    return "Developing dashboard"


def identify_dashboard_focus(context: dict) -> str:
    """Return deterministic dashboard focus text."""
    rec = context.get("recommendation_pathway_summary", {})
    journey = context.get("journey_health_summary", {})
    builds = context.get("cross_build_insight_summary", {})

    weak_evidence = builds.get("weak_evidence_count", 0)
    blocked_journey = journey.get("blocked_journey_count", 0)
    capstone_ready = rec.get("capstone_ready_count", 0)
    nearly_ready = rec.get("nearly_ready_count", 0)

    if weak_evidence > 0:
        return "Strengthen weak build evidence before final presentation."
    if blocked_journey > 0:
        return "Resolve blocked client journeys before presenting the capstone."
    if capstone_ready > 0:
        return "Prepare the strongest client journey for capstone demonstration."
    if nearly_ready > 0:
        return "Polish the strongest client journey and close remaining evidence gaps."
    return "Continue improving the capstone evidence base."


def build_dashboard_metric_summary(context: dict) -> dict:
    """Return headline dashboard metrics."""
    clients = context.get("clients", [])
    phase_1 = context.get("phase_1_summary", {})
    journey = context.get("journey_health_summary", {})
    builds = context.get("cross_build_insight_summary", {})
    rec = context.get("recommendation_pathway_summary", {})
    return {
        "total_clients": len(clients),
        "total_build_areas": builds.get("total_build_areas", 0),
        "total_cross_build_stages": phase_1.get("total_cross_build_stages", 0),
        "capstone_ready_count": rec.get("capstone_ready_count", 0),
        "nearly_ready_count": rec.get("nearly_ready_count", 0),
        "needs_strengthening_count": rec.get("needs_strengthening_count", 0),
        "not_ready_count": rec.get("not_ready_count", 0),
        "strong_journey_count": journey.get("strong_journey_count", 0),
        "healthy_journey_count": journey.get("healthy_journey_count", 0),
        "developing_journey_count": journey.get("developing_journey_count", 0),
        "needs_review_count": journey.get("needs_review_count", 0),
        "blocked_journey_count": journey.get("blocked_journey_count", 0),
        "very_strong_evidence_count": builds.get("very_strong_evidence_count", 0),
        "strong_evidence_count": builds.get("strong_evidence_count", 0),
        "developing_evidence_count": builds.get("developing_evidence_count", 0),
        "weak_evidence_count": builds.get("weak_evidence_count", 0),
    }


_SNAPSHOT_NEXT_STEPS = {
    "Strong capstone dashboard": "Prepare capstone report and exportable portfolio evidence pack.",
    "Portfolio-ready dashboard": "Polish recommendations and prepare client-facing report.",
    "Developing dashboard": "Strengthen journey evidence before final export.",
    "Needs review": "Resolve weak or blocked areas before final positioning.",
}


def build_capstone_snapshot(context: dict) -> dict:
    """Return one concise portfolio snapshot."""
    status = classify_dashboard_status(context)
    builds = context.get("cross_build_insight_summary", {})
    return {
        "dashboard_status": status,
        "dashboard_focus": identify_dashboard_focus(context),
        "strongest_build_area": builds.get("strongest_build_area", "Not available"),
        "weakest_build_area": builds.get("weakest_build_area", "Not available"),
        "recommended_dashboard_next_step": _SNAPSHOT_NEXT_STEPS.get(
            status, "Review the dashboard status before deciding next steps."
        ),
    }


def build_client_selector_options(clients: list[dict]) -> list[str]:
    """Return selector labels for Streamlit."""
    return [
        f"{c.get('organisation_name', '')} — {c.get('sector', '')}"
        for c in clients
    ]


def get_client_by_selector_label(clients: list[dict], label: str) -> dict | None:
    """Return matching client by selector label."""
    for client in clients:
        option = f"{client.get('organisation_name', '')} — {client.get('sector', '')}"
        if option == label:
            return client
    return None


def build_dashboard_table_rows(context: dict) -> dict:
    """Return table-ready rows for client journeys, cross-build summaries, and recommendations."""
    journey_summaries = context.get("journey_summaries", [])
    cross_build_summaries = context.get("cross_build_summaries", [])
    recommendations = context.get("recommendations", [])

    client_journey_rows = [
        {
            "Organisation": s.get("organisation_name", ""),
            "Journey Health": s.get("journey_health", ""),
            "Completion %": s.get("stage_completion_rate", 0.0),
            "Avg Evidence Score": s.get("average_evidence_score", 0.0),
            "Weakest Stage": s.get("weakest_stage", ""),
            "Next Journey Step": s.get("next_journey_step", ""),
        }
        for s in journey_summaries
    ]

    cross_build_rows = [
        {
            "Build": s.get("build_number", ""),
            "Domain": s.get("build_domain", ""),
            "Evidence Health": s.get("evidence_health", ""),
            "Completion %": s.get("completion_rate", 0.0),
            "Build Gap": s.get("build_gap", ""),
        }
        for s in cross_build_summaries
    ]

    recommendation_rows = [
        {
            "Organisation": r.get("organisation_name", ""),
            "Capstone Readiness": r.get("capstone_readiness", ""),
            "Consulting Pathway": r.get("consulting_pathway", ""),
            "Commercial Next Step": r.get("commercial_next_step", ""),
            "Priority": r.get("recommendation_priority", ""),
        }
        for r in recommendations
    ]

    return {
        "client_journey_rows": client_journey_rows,
        "cross_build_rows": cross_build_rows,
        "recommendation_rows": recommendation_rows,
    }
