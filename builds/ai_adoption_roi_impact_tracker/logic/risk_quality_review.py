"""Risk, Quality, and Responsible Adoption Review engine for Build 7 Phase 5.

Checks whether AI-supported workflows are safe enough to continue, scale,
pause, or review, based on quality issues, risk incidents, near misses,
governance review needs, and responsible adoption status.

All figures are based on synthetic demo data only. No real client data.
"""

QUALITY_ISSUE_WARNING_THRESHOLD = 3
QUALITY_ISSUE_HIGH_THRESHOLD = 5
NEAR_MISS_WARNING_THRESHOLD = 2
RISK_INCIDENT_BLOCK_THRESHOLD = 1
MIN_TRAINING_FOR_SCALE = 0.75
MIN_CONFIDENCE_FOR_SCALE = 3.5

_ADOPTION_STATUS_PRIORITY = {
    "Pause adoption": 0,
    "Requires governance review": 1,
    "Continue with controls": 2,
    "Responsible to continue": 3,
    "Responsible to scale": 4,
}


def calculate_total_quality_signals(record: dict) -> int:
    """Return quality_issues_logged, clamped at zero."""
    return max(record.get("quality_issues_logged", 0), 0)


def calculate_total_risk_signals(record: dict) -> int:
    """Return risk_incidents_logged + near_misses_logged, clamped at zero."""
    incidents = max(record.get("risk_incidents_logged", 0), 0)
    near_misses = max(record.get("near_misses_logged", 0), 0)
    return incidents + near_misses


def classify_quality_level(record: dict) -> str:
    """Classify quality concern level.

    High: quality_issues_logged >= 5
    Moderate: quality_issues_logged >= 3
    Low: otherwise
    """
    issues = max(record.get("quality_issues_logged", 0), 0)
    if issues >= QUALITY_ISSUE_HIGH_THRESHOLD:
        return "High quality concern"
    if issues >= QUALITY_ISSUE_WARNING_THRESHOLD:
        return "Moderate quality concern"
    return "Low quality concern"


def classify_risk_level(record: dict) -> str:
    """Classify risk concern level.

    High: risk_incidents_logged >= 1
    Moderate: near_misses_logged >= 2
    Low: otherwise
    """
    incidents = max(record.get("risk_incidents_logged", 0), 0)
    near_misses = max(record.get("near_misses_logged", 0), 0)
    if incidents >= RISK_INCIDENT_BLOCK_THRESHOLD:
        return "High risk concern"
    if near_misses >= NEAR_MISS_WARNING_THRESHOLD:
        return "Moderate risk concern"
    return "Low risk concern"


def classify_responsible_adoption_status(record: dict) -> str:
    """Classify the responsible adoption status for a workflow record.

    Priority order: Pause adoption > Requires governance review >
    Continue with controls > Responsible to scale > Responsible to continue.
    """
    adoption_status = record.get("adoption_status", "")
    pilot_status = record.get("pilot_status", "")
    incidents = max(record.get("risk_incidents_logged", 0), 0)
    near_misses = max(record.get("near_misses_logged", 0), 0)
    quality = max(record.get("quality_issues_logged", 0), 0)
    training = record.get("training_completion_rate", 0.0)
    confidence_after = record.get("confidence_after", 0.0)

    if adoption_status == "Stop" or pilot_status == "Paused":
        return "Pause adoption"

    if incidents >= RISK_INCIDENT_BLOCK_THRESHOLD or near_misses > NEAR_MISS_WARNING_THRESHOLD:
        return "Requires governance review"

    if quality >= QUALITY_ISSUE_WARNING_THRESHOLD or near_misses >= 1:
        return "Continue with controls"

    if (
        adoption_status == "Scale"
        and training >= MIN_TRAINING_FOR_SCALE
        and confidence_after >= MIN_CONFIDENCE_FOR_SCALE
        and quality < QUALITY_ISSUE_WARNING_THRESHOLD
        and incidents == 0
        and near_misses <= 1
    ):
        return "Responsible to scale"

    return "Responsible to continue"


def identify_control_need(record: dict) -> str:
    """Identify the primary control need for a workflow record.

    Priority order: Governance review > Quality assurance checklist >
    Incident logging review > Training reinforcement > Standard monitoring.
    """
    incidents = max(record.get("risk_incidents_logged", 0), 0)
    near_misses = max(record.get("near_misses_logged", 0), 0)
    quality = max(record.get("quality_issues_logged", 0), 0)
    training = record.get("training_completion_rate", 0.0)
    confidence_after = record.get("confidence_after", 0.0)

    if incidents > 0 or near_misses > NEAR_MISS_WARNING_THRESHOLD:
        return "Governance review"

    if quality >= QUALITY_ISSUE_WARNING_THRESHOLD:
        return "Quality assurance checklist"

    if near_misses >= 1:
        return "Incident logging review"

    if training < MIN_TRAINING_FOR_SCALE or confidence_after < MIN_CONFIDENCE_FOR_SCALE:
        return "Training reinforcement"

    return "Standard monitoring"


def classify_scaling_permission(record: dict) -> str:
    """Classify the scaling permission for a workflow record.

    Priority order: Pause or stop > Do not scale yet >
    Scale with controls > Scale permitted.
    """
    adoption_status = record.get("adoption_status", "")
    pilot_status = record.get("pilot_status", "")
    incidents = max(record.get("risk_incidents_logged", 0), 0)
    near_misses = max(record.get("near_misses_logged", 0), 0)
    quality = max(record.get("quality_issues_logged", 0), 0)
    training = record.get("training_completion_rate", 0.0)
    confidence_after = record.get("confidence_after", 0.0)

    if adoption_status == "Stop" or pilot_status == "Paused":
        return "Pause or stop"

    if (
        incidents > 0
        or near_misses > NEAR_MISS_WARNING_THRESHOLD
        or training < MIN_TRAINING_FOR_SCALE
        or confidence_after < MIN_CONFIDENCE_FOR_SCALE
    ):
        return "Do not scale yet"

    if (1 <= quality <= QUALITY_ISSUE_WARNING_THRESHOLD) or (
        1 <= near_misses <= NEAR_MISS_WARNING_THRESHOLD
    ):
        return "Scale with controls"

    if (
        quality == 0
        and incidents == 0
        and near_misses == 0
        and training >= MIN_TRAINING_FOR_SCALE
        and confidence_after >= MIN_CONFIDENCE_FOR_SCALE
    ):
        return "Scale permitted"

    return "Do not scale yet"


def build_risk_quality_summary(record: dict) -> dict:
    """Build a full risk and quality summary dict for one adoption record."""
    return {
        "organisation_id": record.get("organisation_id", ""),
        "organisation_name": record.get("organisation_name", ""),
        "workflow_id": record.get("workflow_id", ""),
        "workflow_name": record.get("workflow_name", ""),
        "related_build": record.get("related_build", ""),
        "staff_group": record.get("staff_group", ""),
        "quality_issues_logged": max(record.get("quality_issues_logged", 0), 0),
        "risk_incidents_logged": max(record.get("risk_incidents_logged", 0), 0),
        "near_misses_logged": max(record.get("near_misses_logged", 0), 0),
        "total_quality_signals": calculate_total_quality_signals(record),
        "total_risk_signals": calculate_total_risk_signals(record),
        "quality_level": classify_quality_level(record),
        "risk_level": classify_risk_level(record),
        "responsible_adoption_status": classify_responsible_adoption_status(record),
        "control_need": identify_control_need(record),
        "scaling_permission": classify_scaling_permission(record),
        "training_completion_rate": record.get("training_completion_rate", 0.0),
        "confidence_after": record.get("confidence_after", 0.0),
        "adoption_status": record.get("adoption_status", ""),
        "pilot_status": record.get("pilot_status", ""),
        "review_decision": record.get("review_decision", ""),
    }


def build_all_risk_quality_summaries(records: list[dict]) -> list[dict]:
    """Return one risk and quality summary per adoption record."""
    return [build_risk_quality_summary(record) for record in records]


def summarise_risk_quality_by_organisation(rq_summaries: list[dict]) -> list[dict]:
    """Group risk and quality summaries by organisation.

    Accepts the output of build_all_risk_quality_summaries.
    Returns one summary dict per organisation.
    """
    org_map: dict[str, dict] = {}

    for summary in rq_summaries:
        org_id = summary["organisation_id"]
        if org_id not in org_map:
            org_map[org_id] = {
                "organisation_id": org_id,
                "organisation_name": summary["organisation_name"],
                "workflow_count": 0,
                "high_quality_concern_count": 0,
                "high_risk_concern_count": 0,
                "requires_governance_review_count": 0,
                "pause_adoption_count": 0,
                "scale_permitted_count": 0,
                "scale_with_controls_count": 0,
                "do_not_scale_yet_count": 0,
            }

        org = org_map[org_id]
        org["workflow_count"] += 1

        if summary["quality_level"] == "High quality concern":
            org["high_quality_concern_count"] += 1
        if summary["risk_level"] == "High risk concern":
            org["high_risk_concern_count"] += 1

        status = summary["responsible_adoption_status"]
        if status == "Requires governance review":
            org["requires_governance_review_count"] += 1
        elif status == "Pause adoption":
            org["pause_adoption_count"] += 1

        scaling = summary["scaling_permission"]
        if scaling == "Scale permitted":
            org["scale_permitted_count"] += 1
        elif scaling == "Scale with controls":
            org["scale_with_controls_count"] += 1
        elif scaling == "Do not scale yet":
            org["do_not_scale_yet_count"] += 1

    return list(org_map.values())


def summarise_risk_quality_by_related_build(rq_summaries: list[dict]) -> list[dict]:
    """Group risk and quality summaries by related build.

    Accepts the output of build_all_risk_quality_summaries.
    Returns one summary dict per related build.
    """
    build_map: dict[str, dict] = {}

    for summary in rq_summaries:
        build = summary["related_build"]
        if build not in build_map:
            build_map[build] = {
                "related_build": build,
                "workflow_count": 0,
                "high_quality_concern_count": 0,
                "high_risk_concern_count": 0,
                "requires_governance_review_count": 0,
                "pause_adoption_count": 0,
                "scale_permitted_count": 0,
                "scale_with_controls_count": 0,
                "do_not_scale_yet_count": 0,
            }

        entry = build_map[build]
        entry["workflow_count"] += 1

        if summary["quality_level"] == "High quality concern":
            entry["high_quality_concern_count"] += 1
        if summary["risk_level"] == "High risk concern":
            entry["high_risk_concern_count"] += 1

        status = summary["responsible_adoption_status"]
        if status == "Requires governance review":
            entry["requires_governance_review_count"] += 1
        elif status == "Pause adoption":
            entry["pause_adoption_count"] += 1

        scaling = summary["scaling_permission"]
        if scaling == "Scale permitted":
            entry["scale_permitted_count"] += 1
        elif scaling == "Scale with controls":
            entry["scale_with_controls_count"] += 1
        elif scaling == "Do not scale yet":
            entry["do_not_scale_yet_count"] += 1

    return list(build_map.values())


def prioritise_risk_quality_actions(rq_summaries: list[dict]) -> list[dict]:
    """Return risk and quality summaries sorted by consulting priority.

    Priority order: Pause adoption > Requires governance review >
    Continue with controls > Responsible to continue > Responsible to scale.

    Within the same status, sorts by: total_risk_signals descending,
    total_quality_signals descending.
    """

    def sort_key(summary: dict) -> tuple:
        status = summary.get("responsible_adoption_status", "Responsible to continue")
        priority = _ADOPTION_STATUS_PRIORITY.get(status, 3)
        risk = -summary.get("total_risk_signals", 0)
        quality = -summary.get("total_quality_signals", 0)
        return (priority, risk, quality)

    return sorted(rq_summaries, key=sort_key)


def generate_risk_quality_recommendation(summary: dict) -> str:
    """Return deterministic recommendation text based on control need."""
    control_need = summary.get("control_need", "")

    if control_need == "Governance review":
        return "Review governance controls before continuing or scaling this workflow."

    if control_need == "Quality assurance checklist":
        return "Add a quality assurance checklist and sample-checking routine before wider rollout."

    if control_need == "Incident logging review":
        return "Review near-miss logging and clarify when staff should escalate concerns."

    if control_need == "Training reinforcement":
        return "Reinforce training before scaling this workflow."

    return "Continue standard monitoring of quality, risk, and staff confidence."


def add_risk_quality_recommendations(summaries: list[dict]) -> list[dict]:
    """Return new summaries with risk_quality_recommendation added.

    Does not mutate originals.
    """
    return [
        {**summary, "risk_quality_recommendation": generate_risk_quality_recommendation(summary)}
        for summary in summaries
    ]
