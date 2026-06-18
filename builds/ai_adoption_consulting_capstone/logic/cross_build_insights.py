"""Cross-build insight aggregator for Build 9 Phase 3."""

BUILD_ORDER = [
    "Build 1",
    "Build 2/3",
    "Build 4",
    "Build 5",
    "Build 6",
    "Build 7",
    "Build 8",
]

BUILD_DOMAIN_LABELS = {
    "Build 1": "Readiness and workflow diagnosis",
    "Build 2/3": "Document intelligence and RAG",
    "Build 4": "Staff training and enablement",
    "Build 5": "Consulting report generation",
    "Build 6": "Governance and responsible use",
    "Build 7": "ROI, adoption, and impact tracking",
    "Build 8": "Delivery and implementation tracking",
}

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

_EVIDENCE_HEALTH_PRIORITY = {
    "No evidence": 1,
    "Weak evidence": 2,
    "Developing evidence": 3,
    "Strong evidence": 4,
    "Very strong evidence": 5,
}


def get_stages_for_build(stages: list[dict], build_number: str) -> list[dict]:
    """Return all stage records for one build number."""
    return [s for s in stages if s.get("build_number") == build_number]


def calculate_build_completion_rate(stages: list[dict]) -> float:
    """Return percentage of stage records marked Completed."""
    if not stages:
        return 0.0
    completed = sum(1 for s in stages if s.get("stage_status") == "Completed")
    return round(completed / len(stages) * 100, 2)


def calculate_build_average_evidence_score(stages: list[dict]) -> float:
    """Return average evidence score for a build."""
    if not stages:
        return 0.0
    total = sum(EVIDENCE_SCORE.get(s.get("evidence_strength", ""), 0) for s in stages)
    return round(total / len(stages), 2)


def classify_build_evidence_health(stages: list[dict]) -> str:
    if not stages:
        return "No evidence"
    rate = calculate_build_completion_rate(stages)
    avg = calculate_build_average_evidence_score(stages)
    if rate >= 85 and avg >= 3.5:
        return "Very strong evidence"
    if rate >= 70 and avg >= 3.0:
        return "Strong evidence"
    if rate >= 40 and avg >= 2.0:
        return "Developing evidence"
    return "Weak evidence"


def identify_build_gap(stages: list[dict]) -> str:
    if not stages:
        return "No evidence has been created for this build area."
    statuses = [s.get("stage_status", "") for s in stages]
    if "Not started" in statuses:
        return "One or more client journeys have not started this build area."
    if "Needs review" in statuses:
        return "One or more client journeys need review in this build area."
    if "In progress" in statuses:
        return "This build area is active but still needs final evidence."
    if all(st == "Completed" for st in statuses):
        return "This build area has complete synthetic evidence."
    return "Review this build area before final presentation."


def build_cross_build_summary(stages: list[dict], build_number: str) -> dict:
    """Return one build-level cross-build insight summary."""
    statuses = [s.get("stage_status", "") for s in stages]
    return {
        "build_number": build_number,
        "build_domain": BUILD_DOMAIN_LABELS.get(build_number, "Unknown"),
        "client_stage_count": len(stages),
        "completed_count": statuses.count("Completed"),
        "in_progress_count": statuses.count("In progress"),
        "needs_review_count": statuses.count("Needs review"),
        "not_started_count": statuses.count("Not started"),
        "completion_rate": calculate_build_completion_rate(stages),
        "average_evidence_score": calculate_build_average_evidence_score(stages),
        "evidence_health": classify_build_evidence_health(stages),
        "build_gap": identify_build_gap(stages),
    }


def build_all_cross_build_summaries(stages: list[dict]) -> list[dict]:
    """Return one summary for each build in BUILD_ORDER."""
    return [
        build_cross_build_summary(get_stages_for_build(stages, build), build)
        for build in BUILD_ORDER
    ]


def identify_strongest_build_area(summaries: list[dict]) -> str:
    """Return the build_number with the strongest evidence."""
    if not summaries:
        return "No build summaries available"
    return sorted(
        summaries,
        key=lambda s: (
            -s["average_evidence_score"],
            -s["completion_rate"],
            BUILD_ORDER.index(s["build_number"]) if s.get("build_number") in BUILD_ORDER else 99,
        ),
    )[0]["build_number"]


def identify_weakest_build_area(summaries: list[dict]) -> str:
    """Return the build_number with the weakest evidence."""
    if not summaries:
        return "No build summaries available"
    return sorted(
        summaries,
        key=lambda s: (
            s["average_evidence_score"],
            s["completion_rate"],
            BUILD_ORDER.index(s["build_number"]) if s.get("build_number") in BUILD_ORDER else 99,
        ),
    )[0]["build_number"]


def summarise_cross_build_insights(summaries: list[dict]) -> dict:
    """Return portfolio-level cross-build insight summary."""
    return {
        "total_build_areas": len(summaries),
        "very_strong_evidence_count": sum(1 for s in summaries if s["evidence_health"] == "Very strong evidence"),
        "strong_evidence_count": sum(1 for s in summaries if s["evidence_health"] == "Strong evidence"),
        "developing_evidence_count": sum(1 for s in summaries if s["evidence_health"] == "Developing evidence"),
        "weak_evidence_count": sum(1 for s in summaries if s["evidence_health"] == "Weak evidence"),
        "no_evidence_count": sum(1 for s in summaries if s["evidence_health"] == "No evidence"),
        "strongest_build_area": identify_strongest_build_area(summaries),
        "weakest_build_area": identify_weakest_build_area(summaries),
    }


def prioritise_build_areas_for_improvement(summaries: list[dict]) -> list[dict]:
    """Return build summaries sorted by improvement priority."""
    return sorted(
        summaries,
        key=lambda s: (
            _EVIDENCE_HEALTH_PRIORITY.get(s["evidence_health"], 99),
            s["completion_rate"],
            s["average_evidence_score"],
            BUILD_ORDER.index(s["build_number"]) if s.get("build_number") in BUILD_ORDER else 99,
        ),
    )


def generate_cross_build_recommendation(summary: dict) -> str:
    health = summary.get("evidence_health", "")
    if health == "No evidence":
        return "Create evidence for this build area before presenting the capstone as end-to-end."
    if health == "Weak evidence":
        return "Strengthen this build area with clearer outputs, examples, and portfolio notes."
    if health == "Developing evidence":
        return "Complete remaining work and improve evidence quality before final positioning."
    if health == "Strong evidence":
        return "Use this build area as supporting evidence in the capstone narrative."
    if health == "Very strong evidence":
        return "Use this build area as a leading proof point in the capstone demonstration."
    return "Review the evidence health classification before making a recommendation."


def add_cross_build_recommendations(summaries: list[dict]) -> list[dict]:
    """Return new summaries with cross_build_recommendation added. Do not mutate originals."""
    return [
        {**s, "cross_build_recommendation": generate_cross_build_recommendation(s)}
        for s in summaries
    ]


def build_client_build_matrix(clients: list[dict], stages: list[dict]) -> list[dict]:
    """Return one row per client showing status by build."""
    rows = []
    for client in clients:
        client_id = client.get("client_id", "")
        row: dict = {
            "client_id": client_id,
            "organisation_name": client.get("organisation_name", ""),
        }
        for build in BUILD_ORDER:
            stage = next(
                (
                    s for s in stages
                    if s.get("client_id") == client_id and s.get("build_number") == build
                ),
                None,
            )
            row[build] = stage["stage_status"] if stage else "Not available"
        rows.append(row)
    return rows
