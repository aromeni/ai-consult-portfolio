"""Decision Tracker and Client Follow-up Evidence engine for Build 7 Phase 6.

Converts adoption evidence into structured consulting decisions:
Stop, Pause, Continue, Continue with controls, Scale, Scale with monitoring,
or Review later. Also generates synthetic client follow-up evidence notes.

All figures are based on synthetic demo data only. No real client data.
"""

MIN_TRAINING_FOR_SCALE = 0.75
MIN_CONFIDENCE_FOR_SCALE = 3.5
MIN_TRAINING_FOR_HIGH_SCALE = 0.9
MIN_CONFIDENCE_FOR_HIGH_SCALE = 4.0
NEAR_MISS_CONTROL_THRESHOLD = 1
QUALITY_CONTROL_THRESHOLD = 3

_DECISION_OUTCOME_PRIORITY = {
    "Stop": 0,
    "Pause": 1,
    "Continue with controls": 2,
    "Review later": 3,
    "Continue": 4,
    "Scale with monitoring": 5,
    "Scale": 6,
}


def classify_decision_outcome(record: dict) -> str:
    """Return the consulting decision outcome for a workflow record.

    Priority order: Stop > Pause > Continue with controls > Scale >
    Scale with monitoring > Continue > Review later.
    """
    adoption_status = record.get("adoption_status", "")
    pilot_status = record.get("pilot_status", "")
    incidents = max(record.get("risk_incidents_logged", 0), 0)
    near_misses = max(record.get("near_misses_logged", 0), 0)
    quality = max(record.get("quality_issues_logged", 0), 0)
    training = record.get("training_completion_rate", 0.0)
    confidence_after = record.get("confidence_after", 0.0)

    if adoption_status == "Stop":
        return "Stop"

    if pilot_status == "Paused":
        return "Pause"

    if incidents > 0 or near_misses > NEAR_MISS_CONTROL_THRESHOLD or quality >= QUALITY_CONTROL_THRESHOLD:
        return "Continue with controls"

    if (
        adoption_status == "Scale"
        and training >= MIN_TRAINING_FOR_HIGH_SCALE
        and confidence_after >= MIN_CONFIDENCE_FOR_HIGH_SCALE
        and quality == 0
        and incidents == 0
        and near_misses == 0
    ):
        return "Scale"

    if (
        adoption_status == "Scale"
        and training >= MIN_TRAINING_FOR_SCALE
        and confidence_after >= MIN_CONFIDENCE_FOR_SCALE
        and incidents == 0
    ):
        return "Scale with monitoring"

    if adoption_status == "Continue":
        return "Continue"

    return "Review later"


def classify_decision_confidence(record: dict) -> str:
    """Classify the confidence level of the consulting decision.

    High: training >= 0.75, confidence_after >= 3.5, pilot active or complete.
    Moderate: training >= 0.6, confidence_after >= 3.0.
    Low: anything else.
    """
    training = record.get("training_completion_rate", 0.0)
    confidence_after = record.get("confidence_after", 0.0)
    pilot_status = record.get("pilot_status", "")

    if (
        training >= MIN_TRAINING_FOR_SCALE
        and confidence_after >= MIN_CONFIDENCE_FOR_SCALE
        and pilot_status in ("In progress", "Completed")
    ):
        return "High confidence decision"

    if training >= 0.6 and confidence_after >= 3.0:
        return "Moderate confidence decision"

    return "Low confidence decision"


def identify_decision_reason(record: dict) -> str:
    """Return a short deterministic reason for the decision.

    Priority order: stopped adoption > paused pilot > risk incident >
    near misses > quality issues > strong scale evidence >
    moderate positive evidence > default review reason.
    """
    adoption_status = record.get("adoption_status", "")
    pilot_status = record.get("pilot_status", "")
    incidents = max(record.get("risk_incidents_logged", 0), 0)
    near_misses = max(record.get("near_misses_logged", 0), 0)
    quality = max(record.get("quality_issues_logged", 0), 0)
    training = record.get("training_completion_rate", 0.0)
    confidence_after = record.get("confidence_after", 0.0)

    if adoption_status == "Stop":
        return "Adoption has been formally stopped."

    if pilot_status == "Paused":
        return "Pilot has been paused pending further review."

    if incidents > 0:
        return "One or more risk incidents have been logged."

    if near_misses > NEAR_MISS_CONTROL_THRESHOLD:
        return "Multiple near misses indicate elevated risk exposure."

    if quality >= QUALITY_CONTROL_THRESHOLD:
        return "Quality issues are at a level that requires controls before wider use."

    if (
        adoption_status == "Scale"
        and training >= MIN_TRAINING_FOR_HIGH_SCALE
        and confidence_after >= MIN_CONFIDENCE_FOR_HIGH_SCALE
        and quality == 0
        and incidents == 0
        and near_misses == 0
    ):
        return "Strong training, confidence, and risk evidence supports scaling."

    if adoption_status == "Scale" and training >= MIN_TRAINING_FOR_SCALE:
        return "Positive training and confidence evidence supports monitored scaling."

    if adoption_status == "Continue":
        return "Adoption is proceeding within the agreed pilot scope."

    return "Evidence is not yet strong enough for a confident continuation or scaling decision."


def identify_next_action(record: dict) -> str:
    """Return a deterministic next action recommendation."""
    outcome = classify_decision_outcome(record)

    if outcome == "Stop":
        return "Stop this workflow and review whether AI support is appropriate."

    if outcome == "Pause":
        return "Pause rollout until governance and workflow controls are reviewed."

    if outcome == "Continue with controls":
        return "Continue with stronger quality assurance and incident logging."

    if outcome == "Scale":
        return "Scale this workflow with continued monitoring and periodic review."

    if outcome == "Scale with monitoring":
        return "Scale cautiously with monitoring."

    if outcome == "Continue":
        return "Continue the pilot and review again next month."

    return "Collect more evidence before making a wider rollout decision."


def build_decision_summary(record: dict) -> dict:
    """Return a workflow-level decision summary."""
    return {
        "organisation_id": record.get("organisation_id", ""),
        "organisation_name": record.get("organisation_name", ""),
        "workflow_id": record.get("workflow_id", ""),
        "workflow_name": record.get("workflow_name", ""),
        "related_build": record.get("related_build", ""),
        "staff_group": record.get("staff_group", ""),
        "decision_outcome": classify_decision_outcome(record),
        "decision_confidence": classify_decision_confidence(record),
        "decision_reason": identify_decision_reason(record),
        "next_action": identify_next_action(record),
        "adoption_status": record.get("adoption_status", ""),
        "pilot_status": record.get("pilot_status", ""),
        "training_completion_rate": record.get("training_completion_rate", 0.0),
        "confidence_after": record.get("confidence_after", 0.0),
        "quality_issues_logged": max(record.get("quality_issues_logged", 0), 0),
        "risk_incidents_logged": max(record.get("risk_incidents_logged", 0), 0),
        "near_misses_logged": max(record.get("near_misses_logged", 0), 0),
        "review_decision": record.get("review_decision", ""),
        "evidence_note": record.get("evidence_note", ""),
    }


def build_all_decision_summaries(records: list[dict]) -> list[dict]:
    """Return one decision summary per adoption record."""
    return [build_decision_summary(record) for record in records]


def summarise_decisions_by_organisation(summaries: list[dict]) -> list[dict]:
    """Group decision summaries by organisation.

    Accepts the output of build_all_decision_summaries.
    Returns one summary dict per organisation.
    """
    org_map: dict[str, dict] = {}

    for summary in summaries:
        org_id = summary["organisation_id"]
        if org_id not in org_map:
            org_map[org_id] = {
                "organisation_id": org_id,
                "organisation_name": summary["organisation_name"],
                "workflow_count": 0,
                "stop_count": 0,
                "pause_count": 0,
                "continue_count": 0,
                "continue_with_controls_count": 0,
                "scale_count": 0,
                "scale_with_monitoring_count": 0,
                "review_later_count": 0,
            }

        org = org_map[org_id]
        org["workflow_count"] += 1
        outcome = summary["decision_outcome"]

        if outcome == "Stop":
            org["stop_count"] += 1
        elif outcome == "Pause":
            org["pause_count"] += 1
        elif outcome == "Continue":
            org["continue_count"] += 1
        elif outcome == "Continue with controls":
            org["continue_with_controls_count"] += 1
        elif outcome == "Scale":
            org["scale_count"] += 1
        elif outcome == "Scale with monitoring":
            org["scale_with_monitoring_count"] += 1
        elif outcome == "Review later":
            org["review_later_count"] += 1

    return list(org_map.values())


def summarise_decisions_by_related_build(summaries: list[dict]) -> list[dict]:
    """Group decision summaries by related build.

    Accepts the output of build_all_decision_summaries.
    Returns one summary dict per related build.
    """
    build_map: dict[str, dict] = {}

    for summary in summaries:
        build = summary["related_build"]
        if build not in build_map:
            build_map[build] = {
                "related_build": build,
                "workflow_count": 0,
                "stop_count": 0,
                "pause_count": 0,
                "continue_count": 0,
                "continue_with_controls_count": 0,
                "scale_count": 0,
                "scale_with_monitoring_count": 0,
                "review_later_count": 0,
            }

        entry = build_map[build]
        entry["workflow_count"] += 1
        outcome = summary["decision_outcome"]

        if outcome == "Stop":
            entry["stop_count"] += 1
        elif outcome == "Pause":
            entry["pause_count"] += 1
        elif outcome == "Continue":
            entry["continue_count"] += 1
        elif outcome == "Continue with controls":
            entry["continue_with_controls_count"] += 1
        elif outcome == "Scale":
            entry["scale_count"] += 1
        elif outcome == "Scale with monitoring":
            entry["scale_with_monitoring_count"] += 1
        elif outcome == "Review later":
            entry["review_later_count"] += 1

    return list(build_map.values())


def prioritise_decisions_for_follow_up(summaries: list[dict]) -> list[dict]:
    """Sort decisions from most to least urgent for follow-up.

    Priority order: Stop > Pause > Continue with controls > Review later >
    Continue > Scale with monitoring > Scale.

    Secondary sort: risk_incidents descending, near_misses descending,
    quality_issues descending.
    """

    def sort_key(summary: dict) -> tuple:
        outcome = summary.get("decision_outcome", "Review later")
        priority = _DECISION_OUTCOME_PRIORITY.get(outcome, 3)
        risk = -summary.get("risk_incidents_logged", 0)
        near = -summary.get("near_misses_logged", 0)
        quality = -summary.get("quality_issues_logged", 0)
        return (priority, risk, near, quality)

    return sorted(summaries, key=sort_key)


def generate_follow_up_evidence_note(summary: dict) -> str:
    """Return deterministic follow-up evidence text based on decision outcome."""
    outcome = summary.get("decision_outcome", "")

    if outcome == "Stop":
        return "Evidence suggests this workflow should not continue without redesign."

    if outcome == "Pause":
        return "Evidence suggests rollout should pause until controls and adoption conditions improve."

    if outcome == "Continue with controls":
        return "Evidence supports continuation only with stronger controls, monitoring, and review."

    if outcome == "Scale":
        return (
            "Evidence supports cautious scaling because training, confidence, quality, "
            "and risk indicators are strong."
        )

    if outcome == "Scale with monitoring":
        return "Evidence supports limited scaling with continued monitoring."

    if outcome == "Continue":
        return "Evidence supports continuing the pilot and reviewing again after the next adoption period."

    return "Evidence is not yet strong enough for a confident scale or stop decision."


def add_follow_up_evidence_notes(summaries: list[dict]) -> list[dict]:
    """Return new summaries with follow_up_evidence_note added. Does not mutate originals."""
    return [
        {**summary, "follow_up_evidence_note": generate_follow_up_evidence_note(summary)}
        for summary in summaries
    ]
