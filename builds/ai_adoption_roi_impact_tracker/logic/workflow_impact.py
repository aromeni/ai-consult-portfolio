"""Workflow Impact and Bottleneck Analysis engine for Build 7 Phase 3.

Identifies which AI-supported workflows are working well, which are blocked
by training, quality, or risk signals, and which require governance review.

All figures are based on synthetic demo data only. No real client data.
"""

from logic.adoption_metrics import calculate_confidence_change
from logic.roi_summary import (
    calculate_efficiency_gain_percent,
    calculate_weekly_hours_saved,
)

LOW_TRAINING_COMPLETION_THRESHOLD = 0.6
LOW_CONFIDENCE_CHANGE_THRESHOLD = 0.5
HIGH_QUALITY_ISSUE_THRESHOLD = 3
HIGH_NEAR_MISS_THRESHOLD = 2
HIGH_EFFICIENCY_GAIN_THRESHOLD = 30.0
LOW_EFFICIENCY_GAIN_THRESHOLD = 10.0

_STATUS_PRIORITY = {
    "Stop or pause": 0,
    "Needs governance review": 1,
    "Needs improvement": 2,
    "Positive but monitor": 3,
    "Ready to scale": 4,
}


def calculate_quality_issue_rate_per_10_tasks(record: dict) -> float:
    """Calculate quality issues per 10 weekly tasks.

    Returns 0.0 if weekly_task_volume is zero or below.
    """
    volume = record.get("weekly_task_volume", 0)
    if volume <= 0:
        return 0.0
    issues = record.get("quality_issues_logged", 0)
    return round(issues / volume * 10, 2)


def calculate_risk_signal_count(record: dict) -> int:
    """Return the total number of risk signals (incidents + near misses).

    Negative values are clamped to zero.
    """
    incidents = max(record.get("risk_incidents_logged", 0), 0)
    near_misses = max(record.get("near_misses_logged", 0), 0)
    return incidents + near_misses


def classify_training_bottleneck(record: dict) -> str:
    """Classify whether the workflow has a training bottleneck.

    Returns one of: 'No training bottleneck', 'Possible training bottleneck',
    'Clear training bottleneck'.
    """
    training_rate = record.get("training_completion_rate", 0.0)
    confidence_change = calculate_confidence_change(record)

    low_training = training_rate < LOW_TRAINING_COMPLETION_THRESHOLD
    low_confidence = confidence_change < LOW_CONFIDENCE_CHANGE_THRESHOLD

    if low_training and low_confidence:
        return "Clear training bottleneck"
    if low_training or low_confidence:
        return "Possible training bottleneck"
    return "No training bottleneck"


def classify_quality_bottleneck(record: dict) -> str:
    """Classify whether the workflow has a quality bottleneck.

    Returns one of: 'No quality bottleneck', 'Possible quality bottleneck',
    'Clear quality bottleneck'.
    """
    issues = record.get("quality_issues_logged", 0)
    rate = calculate_quality_issue_rate_per_10_tasks(record)

    if issues > HIGH_QUALITY_ISSUE_THRESHOLD or rate >= 4.0:
        return "Clear quality bottleneck"
    if (1 <= issues <= HIGH_QUALITY_ISSUE_THRESHOLD) or (2.0 <= rate < 4.0):
        return "Possible quality bottleneck"
    return "No quality bottleneck"


def classify_risk_bottleneck(record: dict) -> str:
    """Classify whether the workflow has a risk bottleneck.

    Returns one of: 'No risk bottleneck', 'Possible risk bottleneck',
    'Clear risk bottleneck'.
    """
    incidents = record.get("risk_incidents_logged", 0)
    near_misses = record.get("near_misses_logged", 0)

    if incidents > 0 or near_misses > HIGH_NEAR_MISS_THRESHOLD:
        return "Clear risk bottleneck"
    if 1 <= near_misses <= HIGH_NEAR_MISS_THRESHOLD:
        return "Possible risk bottleneck"
    return "No risk bottleneck"


def classify_efficiency_bottleneck(record: dict) -> str:
    """Classify whether the workflow has an efficiency bottleneck.

    Returns one of: 'No efficiency bottleneck', 'Possible efficiency bottleneck',
    'Clear efficiency bottleneck'.
    """
    gain = calculate_efficiency_gain_percent(record)

    if gain < LOW_EFFICIENCY_GAIN_THRESHOLD:
        return "Clear efficiency bottleneck"
    if gain < HIGH_EFFICIENCY_GAIN_THRESHOLD:
        return "Possible efficiency bottleneck"
    return "No efficiency bottleneck"


def identify_primary_bottleneck(record: dict) -> str:
    """Identify the primary bottleneck for one workflow record.

    Priority order: Risk > Quality > Training > Efficiency > No major bottleneck.

    Returns one of: 'Risk', 'Quality', 'Training', 'Efficiency',
    'No major bottleneck'.
    """
    risk = classify_risk_bottleneck(record)
    if risk in ("Clear risk bottleneck", "Possible risk bottleneck"):
        return "Risk"

    quality = classify_quality_bottleneck(record)
    if quality in ("Clear quality bottleneck", "Possible quality bottleneck"):
        return "Quality"

    training = classify_training_bottleneck(record)
    if training in ("Clear training bottleneck", "Possible training bottleneck"):
        return "Training"

    efficiency = classify_efficiency_bottleneck(record)
    if efficiency in ("Clear efficiency bottleneck", "Possible efficiency bottleneck"):
        return "Efficiency"

    return "No major bottleneck"


def classify_workflow_impact_status(record: dict) -> str:
    """Classify the overall workflow impact status.

    Returns one of: 'Ready to scale', 'Positive but monitor',
    'Needs improvement', 'Needs governance review', 'Stop or pause'.
    """
    adoption_status = record.get("adoption_status", "")
    pilot_status = record.get("pilot_status", "")
    risk_incidents = record.get("risk_incidents_logged", 0)
    near_misses = record.get("near_misses_logged", 0)
    training_rate = record.get("training_completion_rate", 0.0)
    quality_issues = record.get("quality_issues_logged", 0)
    confidence_change = calculate_confidence_change(record)
    efficiency_gain = calculate_efficiency_gain_percent(record)

    if adoption_status == "Stop" or pilot_status == "Paused":
        return "Stop or pause"

    if risk_incidents > 0 or near_misses > HIGH_NEAR_MISS_THRESHOLD or adoption_status == "Review":
        return "Needs governance review"

    if (
        adoption_status == "Scale"
        and efficiency_gain >= HIGH_EFFICIENCY_GAIN_THRESHOLD
        and confidence_change >= 1.0
        and training_rate >= 0.75
        and quality_issues <= HIGH_QUALITY_ISSUE_THRESHOLD
        and risk_incidents == 0
    ):
        return "Ready to scale"

    if (
        efficiency_gain >= LOW_EFFICIENCY_GAIN_THRESHOLD
        and confidence_change > 0
        and risk_incidents == 0
    ):
        return "Positive but monitor"

    return "Needs improvement"


def build_workflow_impact_summary(record: dict) -> dict:
    """Build a full workflow impact summary dict for one adoption record."""
    efficiency_gain = calculate_efficiency_gain_percent(record)
    weekly_hours = calculate_weekly_hours_saved(record)
    confidence_change = calculate_confidence_change(record)
    quality_rate = calculate_quality_issue_rate_per_10_tasks(record)
    risk_signal_count = calculate_risk_signal_count(record)

    training_bottleneck = classify_training_bottleneck(record)
    quality_bottleneck = classify_quality_bottleneck(record)
    risk_bottleneck = classify_risk_bottleneck(record)
    efficiency_bottleneck = classify_efficiency_bottleneck(record)
    primary_bottleneck = identify_primary_bottleneck(record)
    workflow_impact_status = classify_workflow_impact_status(record)

    return {
        "organisation_id": record.get("organisation_id", ""),
        "organisation_name": record.get("organisation_name", ""),
        "workflow_id": record.get("workflow_id", ""),
        "workflow_name": record.get("workflow_name", ""),
        "related_build": record.get("related_build", ""),
        "staff_group": record.get("staff_group", ""),
        "weekly_task_volume": record.get("weekly_task_volume", 0),
        "efficiency_gain_percent": efficiency_gain,
        "weekly_hours_saved": weekly_hours,
        "confidence_change": confidence_change,
        "training_completion_rate": record.get("training_completion_rate", 0.0),
        "quality_issues_logged": record.get("quality_issues_logged", 0),
        "quality_issue_rate_per_10_tasks": quality_rate,
        "risk_incidents_logged": record.get("risk_incidents_logged", 0),
        "near_misses_logged": record.get("near_misses_logged", 0),
        "risk_signal_count": risk_signal_count,
        "training_bottleneck": training_bottleneck,
        "quality_bottleneck": quality_bottleneck,
        "risk_bottleneck": risk_bottleneck,
        "efficiency_bottleneck": efficiency_bottleneck,
        "primary_bottleneck": primary_bottleneck,
        "workflow_impact_status": workflow_impact_status,
        "adoption_status": record.get("adoption_status", ""),
        "pilot_status": record.get("pilot_status", ""),
        "review_decision": record.get("review_decision", ""),
    }


def build_all_workflow_impact_summaries(records: list[dict]) -> list[dict]:
    """Return one workflow impact summary per adoption record."""
    return [build_workflow_impact_summary(record) for record in records]


def summarise_workflow_impact_by_organisation(impact_summaries: list[dict]) -> list[dict]:
    """Group workflow impact summaries by organisation.

    Accepts the output of build_all_workflow_impact_summaries.
    Returns one summary dict per organisation.
    """
    org_map: dict[str, dict] = {}

    for summary in impact_summaries:
        org_id = summary["organisation_id"]
        if org_id not in org_map:
            org_map[org_id] = {
                "organisation_id": org_id,
                "organisation_name": summary["organisation_name"],
                "workflow_count": 0,
                "ready_to_scale_count": 0,
                "positive_but_monitor_count": 0,
                "needs_improvement_count": 0,
                "needs_governance_review_count": 0,
                "stop_or_pause_count": 0,
                "risk_bottleneck_count": 0,
                "quality_bottleneck_count": 0,
                "training_bottleneck_count": 0,
                "efficiency_bottleneck_count": 0,
                "_sum_efficiency_gain": 0.0,
                "_sum_confidence_change": 0.0,
            }

        org = org_map[org_id]
        org["workflow_count"] += 1

        status = summary["workflow_impact_status"]
        if status == "Ready to scale":
            org["ready_to_scale_count"] += 1
        elif status == "Positive but monitor":
            org["positive_but_monitor_count"] += 1
        elif status == "Needs improvement":
            org["needs_improvement_count"] += 1
        elif status == "Needs governance review":
            org["needs_governance_review_count"] += 1
        elif status == "Stop or pause":
            org["stop_or_pause_count"] += 1

        primary = summary["primary_bottleneck"]
        if primary == "Risk":
            org["risk_bottleneck_count"] += 1
        elif primary == "Quality":
            org["quality_bottleneck_count"] += 1
        elif primary == "Training":
            org["training_bottleneck_count"] += 1
        elif primary == "Efficiency":
            org["efficiency_bottleneck_count"] += 1

        org["_sum_efficiency_gain"] += summary["efficiency_gain_percent"]
        org["_sum_confidence_change"] += summary["confidence_change"]

    result = []
    for org in org_map.values():
        count = org["workflow_count"]
        result.append(
            {
                "organisation_id": org["organisation_id"],
                "organisation_name": org["organisation_name"],
                "workflow_count": count,
                "ready_to_scale_count": org["ready_to_scale_count"],
                "positive_but_monitor_count": org["positive_but_monitor_count"],
                "needs_improvement_count": org["needs_improvement_count"],
                "needs_governance_review_count": org["needs_governance_review_count"],
                "stop_or_pause_count": org["stop_or_pause_count"],
                "risk_bottleneck_count": org["risk_bottleneck_count"],
                "quality_bottleneck_count": org["quality_bottleneck_count"],
                "training_bottleneck_count": org["training_bottleneck_count"],
                "efficiency_bottleneck_count": org["efficiency_bottleneck_count"],
                "average_efficiency_gain_percent": round(org["_sum_efficiency_gain"] / count, 2)
                if count
                else 0.0,
                "average_confidence_change": round(org["_sum_confidence_change"] / count, 2)
                if count
                else 0.0,
            }
        )

    return result


def summarise_workflow_impact_by_related_build(impact_summaries: list[dict]) -> list[dict]:
    """Group workflow impact summaries by related build.

    Accepts the output of build_all_workflow_impact_summaries.
    Returns one summary dict per related build.
    """
    build_map: dict[str, dict] = {}

    for summary in impact_summaries:
        build = summary["related_build"]
        if build not in build_map:
            build_map[build] = {
                "related_build": build,
                "workflow_count": 0,
                "ready_to_scale_count": 0,
                "positive_but_monitor_count": 0,
                "needs_improvement_count": 0,
                "needs_governance_review_count": 0,
                "stop_or_pause_count": 0,
                "_sum_efficiency_gain": 0.0,
                "_sum_confidence_change": 0.0,
                "_bottlenecks": [],
            }

        entry = build_map[build]
        entry["workflow_count"] += 1

        status = summary["workflow_impact_status"]
        if status == "Ready to scale":
            entry["ready_to_scale_count"] += 1
        elif status == "Positive but monitor":
            entry["positive_but_monitor_count"] += 1
        elif status == "Needs improvement":
            entry["needs_improvement_count"] += 1
        elif status == "Needs governance review":
            entry["needs_governance_review_count"] += 1
        elif status == "Stop or pause":
            entry["stop_or_pause_count"] += 1

        entry["_sum_efficiency_gain"] += summary["efficiency_gain_percent"]
        entry["_sum_confidence_change"] += summary["confidence_change"]
        entry["_bottlenecks"].append(summary["primary_bottleneck"])

    result = []
    for entry in build_map.values():
        count = entry["workflow_count"]
        dominant = _dominant_bottleneck(entry["_bottlenecks"])
        result.append(
            {
                "related_build": entry["related_build"],
                "workflow_count": count,
                "ready_to_scale_count": entry["ready_to_scale_count"],
                "positive_but_monitor_count": entry["positive_but_monitor_count"],
                "needs_improvement_count": entry["needs_improvement_count"],
                "needs_governance_review_count": entry["needs_governance_review_count"],
                "stop_or_pause_count": entry["stop_or_pause_count"],
                "average_efficiency_gain_percent": round(entry["_sum_efficiency_gain"] / count, 2)
                if count
                else 0.0,
                "average_confidence_change": round(entry["_sum_confidence_change"] / count, 2)
                if count
                else 0.0,
                "dominant_bottleneck": dominant,
            }
        )

    return result


def _dominant_bottleneck(bottlenecks: list[str]) -> str:
    """Return the most common bottleneck label, excluding 'No major bottleneck' where possible."""
    counts: dict[str, int] = {}
    for b in bottlenecks:
        if b != "No major bottleneck":
            counts[b] = counts.get(b, 0) + 1
    if not counts:
        return "No major bottleneck"
    return max(counts, key=lambda k: counts[k])


def prioritise_workflows_for_action(impact_summaries: list[dict]) -> list[dict]:
    """Return impact summaries sorted by consulting priority.

    Priority order: Stop or pause > Needs governance review > Needs improvement
    > Positive but monitor > Ready to scale.

    Within the same status, sorts by: risk_signal_count descending,
    quality_issues_logged descending, efficiency_gain_percent ascending.
    """

    def sort_key(summary: dict) -> tuple:
        status = summary.get("workflow_impact_status", "Needs improvement")
        priority = _STATUS_PRIORITY.get(status, 2)
        risk = -summary.get("risk_signal_count", 0)
        quality = -summary.get("quality_issues_logged", 0)
        efficiency = summary.get("efficiency_gain_percent", 0.0)
        return (priority, risk, quality, efficiency)

    return sorted(impact_summaries, key=sort_key)


def generate_workflow_action_recommendation(summary: dict) -> str:
    """Return a deterministic consulting recommendation for a workflow impact summary."""
    status = summary.get("workflow_impact_status", "")
    primary = summary.get("primary_bottleneck", "")

    if status in ("Stop or pause", "Needs governance review") or primary == "Risk":
        return (
            "Review governance controls before expanding this workflow. "
            "Check staff guidance, approval points, and incident logging."
        )
    if primary == "Quality":
        return (
            "Strengthen output review before scaling. "
            "Add a sample-checking routine and clarify what good output looks like."
        )
    if primary == "Training":
        return (
            "Improve staff training before expecting further gains. "
            "Repeat practical demonstrations and provide workflow-specific examples."
        )
    if primary == "Efficiency":
        return (
            "Review the workflow design. "
            "The AI-supported process is not yet saving enough time to justify wider rollout."
        )
    if status == "Ready to scale":
        return (
            "This workflow appears ready for cautious scaling, "
            "with continued monitoring of quality and risk controls."
        )
    if status == "Positive but monitor":
        return (
            "Continue the pilot and monitor quality, confidence, and risk signals "
            "before scaling further."
        )
    return "Continue reviewing this workflow using adoption, quality, training, and risk evidence."


def add_recommendations_to_impact_summaries(summaries: list[dict]) -> list[dict]:
    """Return summaries with an additional 'recommended_action' field.

    Does not mutate the original summaries.
    """
    return [
        {**summary, "recommended_action": generate_workflow_action_recommendation(summary)}
        for summary in summaries
    ]
