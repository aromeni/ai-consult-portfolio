"""Client journey overview engine for Build 9 Phase 2."""

from logic.capstone_overview import get_indicator_for_client, get_stages_for_client

JOURNEY_STAGE_ORDER = [
    "Readiness diagnosis",
    "Document intelligence review",
    "Staff training",
    "Consulting report",
    "Governance review",
    "Impact measurement",
    "Delivery tracking",
]

STATUS_SCORE = {
    "Completed": 3,
    "In progress": 2,
    "Needs review": 1,
    "Not started": 0,
}

EVIDENCE_SCORE = {
    "Very strong": 4,
    "Strong": 3,
    "Moderate": 2,
    "Weak": 1,
}

_HEALTH_PRIORITY = {
    "Blocked journey": 1,
    "Needs review": 2,
    "Developing journey": 3,
    "Healthy journey": 4,
    "Strong journey": 5,
}


def sort_stages_by_journey_order(stages: list[dict]) -> list[dict]:
    """Return stages sorted by JOURNEY_STAGE_ORDER. Unknown stages go to the end."""
    order_map = {stage: i for i, stage in enumerate(JOURNEY_STAGE_ORDER)}
    return sorted(
        stages,
        key=lambda s: order_map.get(s.get("journey_stage", ""), len(JOURNEY_STAGE_ORDER)),
    )


def calculate_stage_completion_rate(stages: list[dict]) -> float:
    """Return percentage of stages with stage_status == 'Completed'."""
    if not stages:
        return 0.0
    completed = sum(1 for s in stages if s.get("stage_status") == "Completed")
    return round(completed / len(stages) * 100, 2)


def calculate_average_evidence_score(stages: list[dict]) -> float:
    """Return average evidence score using EVIDENCE_SCORE."""
    if not stages:
        return 0.0
    total = sum(EVIDENCE_SCORE.get(s.get("evidence_strength", ""), 0) for s in stages)
    return round(total / len(stages), 2)


def classify_journey_health(stages: list[dict]) -> str:
    statuses = [s.get("stage_status", "") for s in stages]
    if "Not started" in statuses:
        return "Blocked journey"
    needs_review_count = sum(1 for st in statuses if st == "Needs review")
    if needs_review_count >= 2:
        return "Needs review"
    rate = calculate_stage_completion_rate(stages)
    avg_evidence = calculate_average_evidence_score(stages)
    if rate >= 85 and avg_evidence >= 3.5:
        return "Strong journey"
    if rate >= 70 and avg_evidence >= 3.0:
        return "Healthy journey"
    return "Developing journey"


def identify_next_journey_step(stages: list[dict]) -> str:
    statuses = [s.get("stage_status", "") for s in stages]
    if "Not started" in statuses:
        return "Start the missing journey stage before presenting this as complete."
    if "Needs review" in statuses:
        return "Review the weakest journey stage before moving to final client presentation."
    if "In progress" in statuses:
        return "Complete the in-progress journey stage and gather final evidence."
    if stages and all(st == "Completed" for st in statuses):
        return "Prepare the capstone client-facing summary and portfolio evidence pack."
    return "Review the journey data before deciding the next step."


def identify_weakest_stage(stages: list[dict]) -> str:
    if not stages:
        return "No stages available"
    return min(
        stages,
        key=lambda s: (
            STATUS_SCORE.get(s.get("stage_status", ""), 0)
            + EVIDENCE_SCORE.get(s.get("evidence_strength", ""), 0)
        ),
    ).get("journey_stage", "Unknown")


def build_client_journey_summary(
    client: dict,
    stages: list[dict],
    indicator: dict | None,
) -> dict:
    """Return one client-level journey summary. Stages are sorted by JOURNEY_STAGE_ORDER."""
    stages = sort_stages_by_journey_order(stages)
    statuses = [s.get("stage_status", "") for s in stages]
    return {
        "client_id": client.get("client_id", ""),
        "organisation_name": client.get("organisation_name", ""),
        "sector": client.get("sector", ""),
        "staff_count": client.get("staff_count", 0),
        "capstone_stage": client.get("capstone_stage", ""),
        "primary_ai_goal": client.get("primary_ai_goal", ""),
        "consulting_priority": client.get("consulting_priority", ""),
        "total_stages": len(stages),
        "completed_stage_count": statuses.count("Completed"),
        "in_progress_stage_count": statuses.count("In progress"),
        "needs_review_stage_count": statuses.count("Needs review"),
        "not_started_stage_count": statuses.count("Not started"),
        "stage_completion_rate": calculate_stage_completion_rate(stages),
        "average_evidence_score": calculate_average_evidence_score(stages),
        "journey_health": classify_journey_health(stages),
        "weakest_stage": identify_weakest_stage(stages),
        "next_journey_step": identify_next_journey_step(stages),
        "overall_capstone_status": (
            indicator.get("overall_capstone_status", "Not available")
            if indicator
            else "Not available"
        ),
        "recommended_next_step": (
            indicator.get("recommended_next_step", "Not available")
            if indicator
            else "Not available"
        ),
    }


def build_all_client_journey_summaries(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
) -> list[dict]:
    """Return one journey summary per client."""
    return [
        build_client_journey_summary(
            client=client,
            stages=get_stages_for_client(stages, client.get("client_id", "")),
            indicator=get_indicator_for_client(indicators, client.get("client_id", "")),
        )
        for client in clients
    ]


def summarise_journey_health(summaries: list[dict]) -> dict:
    """Return counts by journey health."""
    return {
        "total_clients": len(summaries),
        "strong_journey_count": sum(1 for s in summaries if s["journey_health"] == "Strong journey"),
        "healthy_journey_count": sum(1 for s in summaries if s["journey_health"] == "Healthy journey"),
        "developing_journey_count": sum(1 for s in summaries if s["journey_health"] == "Developing journey"),
        "needs_review_count": sum(1 for s in summaries if s["journey_health"] == "Needs review"),
        "blocked_journey_count": sum(1 for s in summaries if s["journey_health"] == "Blocked journey"),
    }


def prioritise_clients_for_review(summaries: list[dict]) -> list[dict]:
    """Return client summaries sorted by review priority."""
    return sorted(
        summaries,
        key=lambda s: (
            _HEALTH_PRIORITY.get(s["journey_health"], 99),
            s["stage_completion_rate"],
            s["average_evidence_score"],
        ),
    )


def generate_client_journey_recommendation(summary: dict) -> str:
    health = summary.get("journey_health", "")
    if health == "Blocked journey":
        return (
            "Resolve missing journey stages before presenting this client as a "
            "complete capstone example."
        )
    if health == "Needs review":
        return (
            "Review weak or uncertain stages before converting this into a "
            "client-facing portfolio story."
        )
    if health == "Developing journey":
        return (
            "Continue building evidence across the journey before positioning "
            "this as a strong consulting asset."
        )
    if health == "Healthy journey":
        return (
            "Prepare a clear client-facing narrative and confirm remaining evidence gaps."
        )
    if health == "Strong journey":
        return (
            "Use this as a strong capstone example for demonstrating the end-to-end "
            "AI adoption consulting pathway."
        )
    return "Review the journey health classification before making a recommendation."


def add_journey_recommendations(summaries: list[dict]) -> list[dict]:
    """Return new summaries with journey_recommendation added. Do not mutate originals."""
    return [
        {**s, "journey_recommendation": generate_client_journey_recommendation(s)}
        for s in summaries
    ]
