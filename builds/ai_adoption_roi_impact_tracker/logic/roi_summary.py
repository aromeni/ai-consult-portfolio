"""ROI summary engine for Build 7 Phase 2.

Converts synthetic adoption metrics into practical consulting indicators:
time saving, efficiency gain, and value-equivalent estimates.

All figures are synthetic consulting estimates for portfolio demonstration only.
They are not audited financial ROI and do not use real client data.
"""

from logic.adoption_metrics import (
    calculate_confidence_change,
    calculate_minutes_saved_per_task,
    calculate_weekly_minutes_saved,
)

WEEKS_PER_MONTH = 4.33
WEEKS_PER_YEAR = 52

SYNTHETIC_HOURLY_VALUE_BY_STAFF_GROUP = {
    # Staff groups used in the synthetic adoption data
    "Tutors": 28.0,
    "Tutors and administrators": 26.0,
    "Operations team": 24.0,
    "Quality lead": 32.0,
    "Advice supervisors": 27.0,
    "Service managers": 33.0,
    "Volunteer coordinators": 24.0,
    "Governance trustee": 38.0,
    "Reception team": 22.0,
    "Practice administrators": 24.0,
    "Reception and managers": 28.0,
    "Practice manager": 32.0,
    # Generic lookup keys retained for backward compatibility
    "Advisers": 26.0,
    "Administrators": 22.0,
    "Operations": 24.0,
    "Managers": 35.0,
    "Governance Lead": 38.0,
    "Clinical Administration": 30.0,
    "Default": 25.0,
}


def get_synthetic_hourly_value(record: dict) -> float:
    """Return the synthetic hourly value assumption for the record's staff group.

    Falls back to the Default value for unknown or missing staff groups.
    These are synthetic value-equivalent assumptions only — not real salaries
    or client costs.
    """
    staff_group = record.get("staff_group", "")
    return SYNTHETIC_HOURLY_VALUE_BY_STAFF_GROUP.get(
        staff_group,
        SYNTHETIC_HOURLY_VALUE_BY_STAFF_GROUP["Default"],
    )


def calculate_weekly_hours_saved(record: dict) -> float:
    """Calculate weekly hours saved for the workflow record."""
    weekly_minutes = calculate_weekly_minutes_saved(record)
    return round(weekly_minutes / 60, 2)


def calculate_monthly_hours_saved(record: dict) -> float:
    """Calculate monthly hours saved."""
    return round(calculate_weekly_hours_saved(record) * WEEKS_PER_MONTH, 2)


def calculate_annual_hours_saved(record: dict) -> float:
    """Calculate annual hours saved."""
    return round(calculate_weekly_hours_saved(record) * WEEKS_PER_YEAR, 2)


def calculate_efficiency_gain_percent(record: dict) -> float:
    """Calculate efficiency gain as a percentage of baseline task time.

    Returns 0.0 if baseline is zero or below to avoid division by zero.
    """
    baseline = record.get("baseline_minutes_per_task", 0)
    if baseline <= 0:
        return 0.0
    minutes_saved = calculate_minutes_saved_per_task(record)
    return round(minutes_saved / baseline * 100, 2)


def estimate_weekly_value_equivalent(
    record: dict,
    hourly_value: float | None = None,
) -> float:
    """Estimate weekly value equivalent using synthetic hourly value assumptions.

    This is a synthetic consulting estimate, not audited financial ROI.
    """
    if hourly_value is None:
        hourly_value = get_synthetic_hourly_value(record)
    value = calculate_weekly_hours_saved(record) * hourly_value
    return round(max(value, 0.0), 2)


def estimate_monthly_value_equivalent(
    record: dict,
    hourly_value: float | None = None,
) -> float:
    """Estimate monthly value equivalent using synthetic hourly value assumptions.

    This is a synthetic consulting estimate, not audited financial ROI.
    """
    if hourly_value is None:
        hourly_value = get_synthetic_hourly_value(record)
    value = calculate_monthly_hours_saved(record) * hourly_value
    return round(max(value, 0.0), 2)


def estimate_annual_value_equivalent(
    record: dict,
    hourly_value: float | None = None,
) -> float:
    """Estimate annual value equivalent using synthetic hourly value assumptions.

    This is a synthetic consulting estimate, not audited financial ROI.
    """
    if hourly_value is None:
        hourly_value = get_synthetic_hourly_value(record)
    value = calculate_annual_hours_saved(record) * hourly_value
    return round(max(value, 0.0), 2)


def classify_time_saving_band(weekly_hours_saved: float) -> str:
    """Classify weekly hours saved into a time-saving impact band.

    Bands:
        0 to < 1 hour   → Low
        1 to < 3 hours  → Moderate
        3 to < 7 hours  → High
        7 hours or more → Very high
    """
    if weekly_hours_saved < 1:
        return "Low"
    if weekly_hours_saved < 3:
        return "Moderate"
    if weekly_hours_saved < 7:
        return "High"
    return "Very high"


def classify_confidence_improvement(confidence_change: float) -> str:
    """Classify confidence change into an improvement band.

    Bands:
        ≤ 0         → No improvement
        > 0 to < 0.5  → Small improvement
        0.5 to < 1.0  → Moderate improvement
        ≥ 1.0         → Strong improvement
    """
    if confidence_change <= 0:
        return "No improvement"
    if confidence_change < 0.5:
        return "Small improvement"
    if confidence_change < 1.0:
        return "Moderate improvement"
    return "Strong improvement"


def calculate_adoption_value_indicator(record: dict) -> str:
    """Return a deterministic adoption value indicator for one workflow record.

    Returns one of: Strong value / Clear value / Emerging value / Low value / Needs review.
    """
    adoption_status = record.get("adoption_status", "")
    risk_incidents = record.get("risk_incidents_logged", 0)
    near_misses = record.get("near_misses_logged", 0)

    if adoption_status in ("Stop", "Review") or risk_incidents > 0 or near_misses > 2:
        return "Needs review"

    weekly_hours = calculate_weekly_hours_saved(record)
    confidence_change = calculate_confidence_change(record)
    training_rate = record.get("training_completion_rate", 0.0)
    quality_issues = record.get("quality_issues_logged", 0)

    if (
        weekly_hours >= 5
        and confidence_change >= 1.0
        and training_rate >= 0.75
        and quality_issues <= 3
    ):
        return "Strong value"

    if weekly_hours >= 2 and confidence_change >= 0.5 and training_rate >= 0.6:
        return "Clear value"

    if weekly_hours > 0 and confidence_change > 0:
        return "Emerging value"

    return "Low value"


def build_workflow_roi_summary(record: dict) -> dict:
    """Build a full ROI summary dict for a single workflow adoption record."""
    hourly_value = get_synthetic_hourly_value(record)
    weekly_hours = calculate_weekly_hours_saved(record)
    monthly_hours = calculate_monthly_hours_saved(record)
    annual_hours = calculate_annual_hours_saved(record)
    confidence_change = calculate_confidence_change(record)

    return {
        "organisation_id": record.get("organisation_id", ""),
        "organisation_name": record.get("organisation_name", ""),
        "workflow_id": record.get("workflow_id", ""),
        "workflow_name": record.get("workflow_name", ""),
        "related_build": record.get("related_build", ""),
        "staff_group": record.get("staff_group", ""),
        "baseline_minutes_per_task": record.get("baseline_minutes_per_task", 0),
        "ai_supported_minutes_per_task": record.get("ai_supported_minutes_per_task", 0),
        "weekly_task_volume": record.get("weekly_task_volume", 0),
        "minutes_saved_per_task": calculate_minutes_saved_per_task(record),
        "weekly_hours_saved": weekly_hours,
        "monthly_hours_saved": monthly_hours,
        "annual_hours_saved": annual_hours,
        "efficiency_gain_percent": calculate_efficiency_gain_percent(record),
        "synthetic_hourly_value": hourly_value,
        "weekly_value_equivalent": estimate_weekly_value_equivalent(record, hourly_value),
        "monthly_value_equivalent": estimate_monthly_value_equivalent(record, hourly_value),
        "annual_value_equivalent": estimate_annual_value_equivalent(record, hourly_value),
        "confidence_change": confidence_change,
        "time_saving_band": classify_time_saving_band(weekly_hours),
        "confidence_improvement_band": classify_confidence_improvement(confidence_change),
        "adoption_value_indicator": calculate_adoption_value_indicator(record),
        "adoption_status": record.get("adoption_status", ""),
        "pilot_status": record.get("pilot_status", ""),
        "review_decision": record.get("review_decision", ""),
    }


def build_all_workflow_roi_summaries(records: list[dict]) -> list[dict]:
    """Return ROI summaries for all workflow adoption records."""
    return [build_workflow_roi_summary(record) for record in records]


def summarise_roi_by_organisation(roi_summaries: list[dict]) -> list[dict]:
    """Group workflow ROI summaries by organisation.

    Accepts the output of build_all_workflow_roi_summaries.
    Returns one summary dict per organisation.
    """
    org_map: dict[str, dict] = {}

    for summary in roi_summaries:
        org_id = summary["organisation_id"]
        if org_id not in org_map:
            org_map[org_id] = {
                "organisation_id": org_id,
                "organisation_name": summary["organisation_name"],
                "workflow_count": 0,
                "total_weekly_hours_saved": 0.0,
                "total_monthly_hours_saved": 0.0,
                "total_annual_hours_saved": 0.0,
                "total_weekly_value_equivalent": 0.0,
                "total_monthly_value_equivalent": 0.0,
                "total_annual_value_equivalent": 0.0,
                "_sum_efficiency_gain": 0.0,
                "_sum_confidence_change": 0.0,
                "strong_or_clear_value_workflows": 0,
                "needs_review_workflows": 0,
            }

        org = org_map[org_id]
        org["workflow_count"] += 1
        org["total_weekly_hours_saved"] += summary["weekly_hours_saved"]
        org["total_monthly_hours_saved"] += summary["monthly_hours_saved"]
        org["total_annual_hours_saved"] += summary["annual_hours_saved"]
        org["total_weekly_value_equivalent"] += summary["weekly_value_equivalent"]
        org["total_monthly_value_equivalent"] += summary["monthly_value_equivalent"]
        org["total_annual_value_equivalent"] += summary["annual_value_equivalent"]
        org["_sum_efficiency_gain"] += summary["efficiency_gain_percent"]
        org["_sum_confidence_change"] += summary["confidence_change"]

        if summary["adoption_value_indicator"] in ("Strong value", "Clear value"):
            org["strong_or_clear_value_workflows"] += 1
        if summary["adoption_value_indicator"] == "Needs review":
            org["needs_review_workflows"] += 1

    result = []
    for org in org_map.values():
        count = org["workflow_count"]
        result.append(
            {
                "organisation_id": org["organisation_id"],
                "organisation_name": org["organisation_name"],
                "workflow_count": count,
                "total_weekly_hours_saved": round(org["total_weekly_hours_saved"], 2),
                "total_monthly_hours_saved": round(org["total_monthly_hours_saved"], 2),
                "total_annual_hours_saved": round(org["total_annual_hours_saved"], 2),
                "total_weekly_value_equivalent": round(org["total_weekly_value_equivalent"], 2),
                "total_monthly_value_equivalent": round(org["total_monthly_value_equivalent"], 2),
                "total_annual_value_equivalent": round(org["total_annual_value_equivalent"], 2),
                "average_efficiency_gain_percent": round(org["_sum_efficiency_gain"] / count, 2)
                if count
                else 0.0,
                "average_confidence_change": round(org["_sum_confidence_change"] / count, 2)
                if count
                else 0.0,
                "strong_or_clear_value_workflows": org["strong_or_clear_value_workflows"],
                "needs_review_workflows": org["needs_review_workflows"],
            }
        )

    return result


def summarise_portfolio_roi(roi_summaries: list[dict]) -> dict:
    """Return a portfolio-level ROI summary from all workflow ROI summaries.

    Accepts the output of build_all_workflow_roi_summaries.
    """
    if not roi_summaries:
        return {
            "organisation_count": 0,
            "workflow_count": 0,
            "total_weekly_hours_saved": 0.0,
            "total_monthly_hours_saved": 0.0,
            "total_annual_hours_saved": 0.0,
            "total_weekly_value_equivalent": 0.0,
            "total_monthly_value_equivalent": 0.0,
            "total_annual_value_equivalent": 0.0,
            "average_efficiency_gain_percent": 0.0,
            "average_confidence_change": 0.0,
            "strong_value_workflows": 0,
            "clear_value_workflows": 0,
            "emerging_value_workflows": 0,
            "low_value_workflows": 0,
            "needs_review_workflows": 0,
        }

    org_ids = {s["organisation_id"] for s in roi_summaries}
    count = len(roi_summaries)

    indicator_counts: dict[str, int] = {
        "Strong value": 0,
        "Clear value": 0,
        "Emerging value": 0,
        "Low value": 0,
        "Needs review": 0,
    }
    for s in roi_summaries:
        indicator = s.get("adoption_value_indicator", "Low value")
        if indicator in indicator_counts:
            indicator_counts[indicator] += 1

    return {
        "organisation_count": len(org_ids),
        "workflow_count": count,
        "total_weekly_hours_saved": round(
            sum(s["weekly_hours_saved"] for s in roi_summaries), 2
        ),
        "total_monthly_hours_saved": round(
            sum(s["monthly_hours_saved"] for s in roi_summaries), 2
        ),
        "total_annual_hours_saved": round(
            sum(s["annual_hours_saved"] for s in roi_summaries), 2
        ),
        "total_weekly_value_equivalent": round(
            sum(s["weekly_value_equivalent"] for s in roi_summaries), 2
        ),
        "total_monthly_value_equivalent": round(
            sum(s["monthly_value_equivalent"] for s in roi_summaries), 2
        ),
        "total_annual_value_equivalent": round(
            sum(s["annual_value_equivalent"] for s in roi_summaries), 2
        ),
        "average_efficiency_gain_percent": round(
            sum(s["efficiency_gain_percent"] for s in roi_summaries) / count, 2
        ),
        "average_confidence_change": round(
            sum(s["confidence_change"] for s in roi_summaries) / count, 2
        ),
        "strong_value_workflows": indicator_counts["Strong value"],
        "clear_value_workflows": indicator_counts["Clear value"],
        "emerging_value_workflows": indicator_counts["Emerging value"],
        "low_value_workflows": indicator_counts["Low value"],
        "needs_review_workflows": indicator_counts["Needs review"],
    }
