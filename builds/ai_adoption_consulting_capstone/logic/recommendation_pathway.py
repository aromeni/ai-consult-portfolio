"""Consulting recommendation pathway engine for Build 9 Phase 4."""

PATHWAY_OPTIONS = [
    "Ready for capstone presentation",
    "Prepare client-facing follow-up",
    "Strengthen weak evidence",
    "Complete missing journey stages",
    "Run focused improvement sprint",
]

COMMERCIAL_NEXT_STEPS = [
    "Portfolio demonstration",
    "Paid implementation review",
    "Governance improvement sprint",
    "Training and adoption support package",
    "Document intelligence upgrade",
    "Delivery tracking retainer",
]

_PRIORITY_ORDER = {
    "High priority": 1,
    "Medium priority": 2,
    "Low priority": 3,
}


def classify_capstone_readiness(client_summary: dict) -> str:
    health = client_summary.get("journey_health", "")
    rate = client_summary.get("stage_completion_rate", 0.0)
    avg = client_summary.get("average_evidence_score", 0.0)
    if health == "Strong journey" and rate >= 85 and avg >= 3.5:
        return "Capstone ready"
    if health in ("Strong journey", "Healthy journey") and rate >= 70 and avg >= 3.0:
        return "Nearly ready"
    if health in ("Developing journey", "Needs review"):
        return "Needs strengthening"
    if health == "Blocked journey":
        return "Not ready"
    return "Needs strengthening"


def identify_consulting_pathway(client_summary: dict) -> str:
    health = client_summary.get("journey_health", "")
    if health == "Blocked journey":
        return "Complete missing journey stages"
    if health == "Needs review":
        return "Run focused improvement sprint"
    if health == "Developing journey":
        return "Strengthen weak evidence"
    if health == "Healthy journey":
        return "Prepare client-facing follow-up"
    if health == "Strong journey":
        return "Ready for capstone presentation"
    return "Strengthen weak evidence"


def identify_commercial_next_step(client_summary: dict) -> str:
    health = client_summary.get("journey_health", "")
    if health == "Strong journey":
        return "Portfolio demonstration"
    if health == "Healthy journey":
        return "Paid implementation review"
    if health == "Needs review":
        return "Governance improvement sprint"
    if health == "Developing journey":
        return "Training and adoption support package"
    if health == "Blocked journey":
        return "Document intelligence upgrade"
    return "Delivery tracking retainer"


def identify_primary_improvement_area(client_summary: dict) -> str:
    weakest = client_summary.get("weakest_stage", "")
    if not weakest or weakest == "No stages available":
        return "Review full client journey"
    return weakest


def classify_recommendation_priority(client_summary: dict) -> str:
    health = client_summary.get("journey_health", "")
    if health in ("Blocked journey", "Needs review"):
        return "High priority"
    if health == "Developing journey":
        return "Medium priority"
    return "Low priority"


def build_consulting_recommendation_summary(client_summary: dict) -> dict:
    """Return one client-level consulting recommendation summary."""
    return {
        "client_id": client_summary.get("client_id", ""),
        "organisation_name": client_summary.get("organisation_name", ""),
        "sector": client_summary.get("sector", ""),
        "capstone_stage": client_summary.get("capstone_stage", ""),
        "journey_health": client_summary.get("journey_health", ""),
        "stage_completion_rate": client_summary.get("stage_completion_rate", 0.0),
        "average_evidence_score": client_summary.get("average_evidence_score", 0.0),
        "weakest_stage": client_summary.get("weakest_stage", ""),
        "capstone_readiness": classify_capstone_readiness(client_summary),
        "consulting_pathway": identify_consulting_pathway(client_summary),
        "commercial_next_step": identify_commercial_next_step(client_summary),
        "primary_improvement_area": identify_primary_improvement_area(client_summary),
        "recommendation_priority": classify_recommendation_priority(client_summary),
        "recommended_next_step": client_summary.get("recommended_next_step", "Not available"),
    }


def build_all_consulting_recommendations(client_summaries: list[dict]) -> list[dict]:
    """Return one recommendation summary per client."""
    return [build_consulting_recommendation_summary(cs) for cs in client_summaries]


def summarise_recommendation_pathways(recommendations: list[dict]) -> dict:
    """Return counts by readiness, pathway, and priority."""
    return {
        "total_clients": len(recommendations),
        "capstone_ready_count": sum(1 for r in recommendations if r["capstone_readiness"] == "Capstone ready"),
        "nearly_ready_count": sum(1 for r in recommendations if r["capstone_readiness"] == "Nearly ready"),
        "needs_strengthening_count": sum(1 for r in recommendations if r["capstone_readiness"] == "Needs strengthening"),
        "not_ready_count": sum(1 for r in recommendations if r["capstone_readiness"] == "Not ready"),
        "high_priority_count": sum(1 for r in recommendations if r["recommendation_priority"] == "High priority"),
        "medium_priority_count": sum(1 for r in recommendations if r["recommendation_priority"] == "Medium priority"),
        "low_priority_count": sum(1 for r in recommendations if r["recommendation_priority"] == "Low priority"),
    }


def prioritise_recommendations(recommendations: list[dict]) -> list[dict]:
    """Return recommendation summaries sorted by priority."""
    return sorted(
        recommendations,
        key=lambda r: (
            _PRIORITY_ORDER.get(r["recommendation_priority"], 99),
            r["stage_completion_rate"],
            r["average_evidence_score"],
        ),
    )


def generate_consulting_recommendation_text(recommendation: dict) -> str:
    readiness = recommendation.get("capstone_readiness", "")
    if readiness == "Capstone ready":
        return (
            "This client journey is strong enough to use as a capstone demonstration. "
            "Prepare a polished client-facing narrative and evidence pack."
        )
    if readiness == "Nearly ready":
        return (
            "This client journey is close to portfolio-ready. Strengthen the remaining "
            "evidence before presenting it as a complete capstone story."
        )
    if readiness == "Needs strengthening":
        return (
            "This client journey needs more evidence before it can be used confidently. "
            "Focus on the weakest stage and improve the supporting outputs."
        )
    if readiness == "Not ready":
        return (
            "This client journey should not yet be presented as complete. Resolve missing "
            "or blocked stages before using it as capstone evidence."
        )
    return "Review the capstone readiness classification before making a recommendation."


def add_consulting_recommendation_text(recommendations: list[dict]) -> list[dict]:
    """Return new recommendations with consulting_recommendation added. Do not mutate originals."""
    return [
        {**r, "consulting_recommendation": generate_consulting_recommendation_text(r)}
        for r in recommendations
    ]


def build_recommendation_pathway_matrix(recommendations: list[dict]) -> list[dict]:
    """Return simplified matrix rows for dashboard display."""
    return [
        {
            "organisation_name": r["organisation_name"],
            "capstone_readiness": r["capstone_readiness"],
            "consulting_pathway": r["consulting_pathway"],
            "commercial_next_step": r["commercial_next_step"],
            "primary_improvement_area": r["primary_improvement_area"],
            "recommendation_priority": r["recommendation_priority"],
        }
        for r in recommendations
    ]
