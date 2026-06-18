"""Tests for Build 7 Phase 2 ROI summary engine.

All test data is deterministic and uses synthetic demo records only.
No real client data, personal data, or regulated information is used.
"""

import pytest

from data.synthetic_adoption_data import get_synthetic_adoption_metrics
from logic.roi_summary import (
    SYNTHETIC_HOURLY_VALUE_BY_STAFF_GROUP,
    WEEKS_PER_MONTH,
    WEEKS_PER_YEAR,
    build_all_workflow_roi_summaries,
    build_workflow_roi_summary,
    calculate_adoption_value_indicator,
    calculate_annual_hours_saved,
    calculate_efficiency_gain_percent,
    calculate_monthly_hours_saved,
    calculate_weekly_hours_saved,
    classify_confidence_improvement,
    classify_time_saving_band,
    estimate_annual_value_equivalent,
    estimate_monthly_value_equivalent,
    estimate_weekly_value_equivalent,
    get_synthetic_hourly_value,
    summarise_portfolio_roi,
    summarise_roi_by_organisation,
)

# ---------------------------------------------------------------------------
# Shared test fixtures
# ---------------------------------------------------------------------------

WF001_RECORD = {
    "organisation_id": "ORG001",
    "organisation_name": "BrightPath Skills Training",
    "workflow_id": "WF001",
    "workflow_name": "Lesson plan drafting",
    "related_build": "Build 4",
    "baseline_minutes_per_task": 75,
    "ai_supported_minutes_per_task": 45,
    "weekly_task_volume": 6,
    "staff_group": "Tutors",
    "confidence_before": 2.4,
    "confidence_after": 3.7,
    "training_completion_rate": 0.75,
    "pilot_status": "In progress",
    "quality_issues_logged": 2,
    "risk_incidents_logged": 0,
    "near_misses_logged": 1,
    "adoption_status": "Continue",
    "review_decision": "Continue with stronger review checklist",
    "evidence_note": "Tutors report faster first drafts.",
}

# Strong value: large time saving, high confidence change, good training, few quality issues
STRONG_VALUE_RECORD = {
    "organisation_id": "TESTORG",
    "organisation_name": "Test Organisation",
    "workflow_id": "TWFX",
    "workflow_name": "High-impact workflow",
    "related_build": "Build 1",
    "baseline_minutes_per_task": 75,
    "ai_supported_minutes_per_task": 25,
    "weekly_task_volume": 8,
    "staff_group": "Tutors",
    "confidence_before": 2.0,
    "confidence_after": 3.5,
    "training_completion_rate": 0.80,
    "pilot_status": "In progress",
    "quality_issues_logged": 1,
    "risk_incidents_logged": 0,
    "near_misses_logged": 0,
    "adoption_status": "Continue",
    "review_decision": "Continue",
    "evidence_note": "Test record for strong value.",
}

# Needs review: has a logged risk incident
RISK_INCIDENT_RECORD = {
    "organisation_id": "TESTORG",
    "organisation_name": "Test Organisation",
    "workflow_id": "TWFY",
    "workflow_name": "High-risk workflow",
    "related_build": "Build 6",
    "baseline_minutes_per_task": 60,
    "ai_supported_minutes_per_task": 40,
    "weekly_task_volume": 5,
    "staff_group": "Administrators",
    "confidence_before": 2.5,
    "confidence_after": 3.5,
    "training_completion_rate": 0.70,
    "pilot_status": "In progress",
    "quality_issues_logged": 2,
    "risk_incidents_logged": 1,
    "near_misses_logged": 0,
    "adoption_status": "Continue",
    "review_decision": "Continue with review",
    "evidence_note": "One incident logged.",
}

# ---------------------------------------------------------------------------
# 1. get_synthetic_hourly_value — known staff groups
# ---------------------------------------------------------------------------


def test_hourly_value_tutors():
    record = {**WF001_RECORD, "staff_group": "Tutors"}
    assert get_synthetic_hourly_value(record) == 28.0


def test_hourly_value_advisers():
    record = {**WF001_RECORD, "staff_group": "Advisers"}
    assert get_synthetic_hourly_value(record) == 26.0


def test_hourly_value_administrators():
    record = {**WF001_RECORD, "staff_group": "Administrators"}
    assert get_synthetic_hourly_value(record) == 22.0


def test_hourly_value_operations():
    record = {**WF001_RECORD, "staff_group": "Operations"}
    assert get_synthetic_hourly_value(record) == 24.0


def test_hourly_value_managers():
    record = {**WF001_RECORD, "staff_group": "Managers"}
    assert get_synthetic_hourly_value(record) == 35.0


def test_hourly_value_governance_lead():
    record = {**WF001_RECORD, "staff_group": "Governance Lead"}
    assert get_synthetic_hourly_value(record) == 38.0


def test_hourly_value_clinical_administration():
    record = {**WF001_RECORD, "staff_group": "Clinical Administration"}
    assert get_synthetic_hourly_value(record) == 30.0


# ---------------------------------------------------------------------------
# 2. get_synthetic_hourly_value — unknown staff group returns default
# ---------------------------------------------------------------------------


def test_hourly_value_unknown_staff_group_returns_default():
    record = {**WF001_RECORD, "staff_group": "Unknown group"}
    assert get_synthetic_hourly_value(record) == SYNTHETIC_HOURLY_VALUE_BY_STAFF_GROUP["Default"]


def test_hourly_value_missing_staff_group_returns_default():
    record = {k: v for k, v in WF001_RECORD.items() if k != "staff_group"}
    assert get_synthetic_hourly_value(record) == SYNTHETIC_HOURLY_VALUE_BY_STAFF_GROUP["Default"]


# ---------------------------------------------------------------------------
# 3. calculate_weekly_hours_saved
# ---------------------------------------------------------------------------


def test_weekly_hours_saved_wf001():
    # minutes_saved_per_task = 30, weekly_volume = 6
    # weekly_minutes = 180, weekly_hours = 180 / 60 = 3.0
    result = calculate_weekly_hours_saved(WF001_RECORD)
    assert result == 3.0


def test_weekly_hours_saved_zero_saving():
    record = {**WF001_RECORD, "baseline_minutes_per_task": 45, "ai_supported_minutes_per_task": 45}
    assert calculate_weekly_hours_saved(record) == 0.0


# ---------------------------------------------------------------------------
# 4. calculate_monthly_hours_saved
# ---------------------------------------------------------------------------


def test_monthly_hours_saved_wf001():
    # weekly_hours = 3.0, WEEKS_PER_MONTH = 4.33
    expected = round(3.0 * WEEKS_PER_MONTH, 2)
    result = calculate_monthly_hours_saved(WF001_RECORD)
    assert result == expected


def test_monthly_hours_saved_zero_saving():
    record = {**WF001_RECORD, "baseline_minutes_per_task": 45, "ai_supported_minutes_per_task": 45}
    assert calculate_monthly_hours_saved(record) == 0.0


# ---------------------------------------------------------------------------
# 5. calculate_annual_hours_saved
# ---------------------------------------------------------------------------


def test_annual_hours_saved_wf001():
    # weekly_hours = 3.0, WEEKS_PER_YEAR = 52
    expected = round(3.0 * WEEKS_PER_YEAR, 2)
    result = calculate_annual_hours_saved(WF001_RECORD)
    assert result == expected


def test_annual_hours_saved_zero_saving():
    record = {**WF001_RECORD, "baseline_minutes_per_task": 45, "ai_supported_minutes_per_task": 45}
    assert calculate_annual_hours_saved(record) == 0.0


# ---------------------------------------------------------------------------
# 6. calculate_efficiency_gain_percent
# ---------------------------------------------------------------------------


def test_efficiency_gain_percent_wf001():
    # baseline = 75, saved = 30, gain = 30/75 * 100 = 40.0
    result = calculate_efficiency_gain_percent(WF001_RECORD)
    assert result == 40.0


def test_efficiency_gain_percent_partial():
    record = {**WF001_RECORD, "baseline_minutes_per_task": 120, "ai_supported_minutes_per_task": 90}
    # saved = 30, gain = 30/120 * 100 = 25.0
    assert calculate_efficiency_gain_percent(record) == 25.0


# ---------------------------------------------------------------------------
# 7. Baseline zero returns 0.0 efficiency gain
# ---------------------------------------------------------------------------


def test_efficiency_gain_zero_baseline():
    record = {**WF001_RECORD, "baseline_minutes_per_task": 0, "ai_supported_minutes_per_task": 0}
    assert calculate_efficiency_gain_percent(record) == 0.0


def test_efficiency_gain_negative_baseline():
    record = {**WF001_RECORD, "baseline_minutes_per_task": -10, "ai_supported_minutes_per_task": 0}
    assert calculate_efficiency_gain_percent(record) == 0.0


# ---------------------------------------------------------------------------
# 8. estimate_weekly_value_equivalent
# ---------------------------------------------------------------------------


def test_weekly_value_equivalent_wf001():
    # weekly_hours = 3.0, hourly_value = 28.0
    result = estimate_weekly_value_equivalent(WF001_RECORD)
    assert result == 84.0


def test_weekly_value_equivalent_custom_hourly_value():
    result = estimate_weekly_value_equivalent(WF001_RECORD, hourly_value=30.0)
    assert result == 90.0


def test_weekly_value_equivalent_never_negative():
    record = {**WF001_RECORD, "baseline_minutes_per_task": 0, "ai_supported_minutes_per_task": 0}
    assert estimate_weekly_value_equivalent(record) >= 0.0


# ---------------------------------------------------------------------------
# 9. estimate_monthly_value_equivalent
# ---------------------------------------------------------------------------


def test_monthly_value_equivalent_wf001():
    # monthly_hours = 12.99, hourly_value = 28.0
    expected = round(calculate_monthly_hours_saved(WF001_RECORD) * 28.0, 2)
    result = estimate_monthly_value_equivalent(WF001_RECORD)
    assert result == expected


def test_monthly_value_equivalent_custom_hourly_value():
    expected = round(calculate_monthly_hours_saved(WF001_RECORD) * 30.0, 2)
    result = estimate_monthly_value_equivalent(WF001_RECORD, hourly_value=30.0)
    assert result == expected


# ---------------------------------------------------------------------------
# 10. estimate_annual_value_equivalent
# ---------------------------------------------------------------------------


def test_annual_value_equivalent_wf001():
    # annual_hours = 156.0, hourly_value = 28.0
    result = estimate_annual_value_equivalent(WF001_RECORD)
    assert result == 4368.0


def test_annual_value_equivalent_custom_hourly_value():
    expected = round(calculate_annual_hours_saved(WF001_RECORD) * 30.0, 2)
    result = estimate_annual_value_equivalent(WF001_RECORD, hourly_value=30.0)
    assert result == expected


# ---------------------------------------------------------------------------
# 11. classify_time_saving_band
# ---------------------------------------------------------------------------


def test_time_saving_band_low_zero():
    assert classify_time_saving_band(0.0) == "Low"


def test_time_saving_band_low_half_hour():
    assert classify_time_saving_band(0.5) == "Low"


def test_time_saving_band_low_boundary():
    assert classify_time_saving_band(0.99) == "Low"


def test_time_saving_band_moderate_at_one():
    assert classify_time_saving_band(1.0) == "Moderate"


def test_time_saving_band_moderate_mid():
    assert classify_time_saving_band(2.5) == "Moderate"


def test_time_saving_band_high_at_three():
    assert classify_time_saving_band(3.0) == "High"


def test_time_saving_band_high_mid():
    assert classify_time_saving_band(5.0) == "High"


def test_time_saving_band_high_boundary():
    assert classify_time_saving_band(6.99) == "High"


def test_time_saving_band_very_high_at_seven():
    assert classify_time_saving_band(7.0) == "Very high"


def test_time_saving_band_very_high_large():
    assert classify_time_saving_band(15.0) == "Very high"


# ---------------------------------------------------------------------------
# 12. classify_confidence_improvement
# ---------------------------------------------------------------------------


def test_confidence_band_no_improvement_negative():
    assert classify_confidence_improvement(-0.5) == "No improvement"


def test_confidence_band_no_improvement_zero():
    assert classify_confidence_improvement(0.0) == "No improvement"


def test_confidence_band_small_improvement():
    assert classify_confidence_improvement(0.1) == "Small improvement"


def test_confidence_band_small_improvement_boundary():
    assert classify_confidence_improvement(0.49) == "Small improvement"


def test_confidence_band_moderate_improvement():
    assert classify_confidence_improvement(0.5) == "Moderate improvement"


def test_confidence_band_moderate_improvement_upper():
    assert classify_confidence_improvement(0.99) == "Moderate improvement"


def test_confidence_band_strong_improvement():
    assert classify_confidence_improvement(1.0) == "Strong improvement"


def test_confidence_band_strong_improvement_large():
    assert classify_confidence_improvement(2.0) == "Strong improvement"


# ---------------------------------------------------------------------------
# 13. calculate_adoption_value_indicator — Strong value
# ---------------------------------------------------------------------------


def test_adoption_value_indicator_strong_value():
    # weekly_hours = (75-25)*8/60 = 400/60 ≈ 6.67 ≥ 5
    # confidence_change = 3.5 - 2.0 = 1.5 ≥ 1.0
    # training_completion_rate = 0.80 ≥ 0.75
    # quality_issues = 1 ≤ 3
    assert calculate_adoption_value_indicator(STRONG_VALUE_RECORD) == "Strong value"


def test_adoption_value_indicator_clear_value():
    # weekly_hours = 3.0 ≥ 2, confidence = 1.3 ≥ 0.5, training = 0.75 ≥ 0.6
    assert calculate_adoption_value_indicator(WF001_RECORD) == "Clear value"


def test_adoption_value_indicator_emerging_value():
    record = {
        **WF001_RECORD,
        "baseline_minutes_per_task": 60,
        "ai_supported_minutes_per_task": 50,
        "weekly_task_volume": 3,
        "confidence_before": 2.0,
        "confidence_after": 2.3,
        "training_completion_rate": 0.40,
        "risk_incidents_logged": 0,
        "near_misses_logged": 0,
        "adoption_status": "Continue",
    }
    # weekly_hours = 10*3/60 = 0.5 > 0, confidence_change = 0.3 > 0
    # but < 2 hrs and < 0.5 confidence, so not Clear
    assert calculate_adoption_value_indicator(record) == "Emerging value"


def test_adoption_value_indicator_low_value():
    record = {
        **WF001_RECORD,
        "baseline_minutes_per_task": 60,
        "ai_supported_minutes_per_task": 60,
        "weekly_task_volume": 5,
        "confidence_before": 2.5,
        "confidence_after": 2.5,
        "risk_incidents_logged": 0,
        "near_misses_logged": 0,
        "adoption_status": "Continue",
    }
    # no time saved, no confidence change
    assert calculate_adoption_value_indicator(record) == "Low value"


# ---------------------------------------------------------------------------
# 14. calculate_adoption_value_indicator — Needs review
# ---------------------------------------------------------------------------


def test_adoption_value_indicator_needs_review_risk_incident():
    assert calculate_adoption_value_indicator(RISK_INCIDENT_RECORD) == "Needs review"


def test_adoption_value_indicator_needs_review_stop_status():
    record = {**WF001_RECORD, "adoption_status": "Stop", "risk_incidents_logged": 0}
    assert calculate_adoption_value_indicator(record) == "Needs review"


def test_adoption_value_indicator_needs_review_review_status():
    record = {**WF001_RECORD, "adoption_status": "Review", "risk_incidents_logged": 0}
    assert calculate_adoption_value_indicator(record) == "Needs review"


def test_adoption_value_indicator_needs_review_high_near_misses():
    record = {**WF001_RECORD, "near_misses_logged": 3, "risk_incidents_logged": 0}
    assert calculate_adoption_value_indicator(record) == "Needs review"


def test_adoption_value_indicator_two_near_misses_not_needs_review():
    # exactly 2 near misses should NOT trigger Needs review
    record = {**WF001_RECORD, "near_misses_logged": 2, "risk_incidents_logged": 0}
    result = calculate_adoption_value_indicator(record)
    assert result != "Needs review"


# ---------------------------------------------------------------------------
# 15. build_workflow_roi_summary — returns all expected fields
# ---------------------------------------------------------------------------

EXPECTED_ROI_FIELDS = {
    "organisation_id",
    "organisation_name",
    "workflow_id",
    "workflow_name",
    "related_build",
    "staff_group",
    "baseline_minutes_per_task",
    "ai_supported_minutes_per_task",
    "weekly_task_volume",
    "minutes_saved_per_task",
    "weekly_hours_saved",
    "monthly_hours_saved",
    "annual_hours_saved",
    "efficiency_gain_percent",
    "synthetic_hourly_value",
    "weekly_value_equivalent",
    "monthly_value_equivalent",
    "annual_value_equivalent",
    "confidence_change",
    "time_saving_band",
    "confidence_improvement_band",
    "adoption_value_indicator",
    "adoption_status",
    "pilot_status",
    "review_decision",
}


def test_build_workflow_roi_summary_returns_all_fields():
    result = build_workflow_roi_summary(WF001_RECORD)
    assert set(result.keys()) == EXPECTED_ROI_FIELDS


def test_build_workflow_roi_summary_wf001_values():
    result = build_workflow_roi_summary(WF001_RECORD)
    assert result["organisation_id"] == "ORG001"
    assert result["workflow_id"] == "WF001"
    assert result["minutes_saved_per_task"] == 30
    assert result["weekly_hours_saved"] == 3.0
    assert result["monthly_hours_saved"] == round(3.0 * WEEKS_PER_MONTH, 2)
    assert result["annual_hours_saved"] == round(3.0 * WEEKS_PER_YEAR, 2)
    assert result["efficiency_gain_percent"] == 40.0
    assert result["synthetic_hourly_value"] == 28.0
    assert result["weekly_value_equivalent"] == 84.0
    assert result["annual_value_equivalent"] == 4368.0
    assert result["confidence_change"] == round(3.7 - 2.4, 2)
    assert result["time_saving_band"] == "High"
    assert result["confidence_improvement_band"] == "Strong improvement"
    assert result["adoption_value_indicator"] == "Clear value"
    assert result["adoption_status"] == "Continue"


# ---------------------------------------------------------------------------
# 16. build_all_workflow_roi_summaries — returns same count as input
# ---------------------------------------------------------------------------


def test_build_all_workflow_roi_summaries_count():
    records = get_synthetic_adoption_metrics()
    results = build_all_workflow_roi_summaries(records)
    assert len(results) == len(records)


def test_build_all_workflow_roi_summaries_each_has_required_fields():
    records = get_synthetic_adoption_metrics()
    results = build_all_workflow_roi_summaries(records)
    for result in results:
        assert set(result.keys()) == EXPECTED_ROI_FIELDS


def test_build_all_workflow_roi_summaries_empty_list():
    assert build_all_workflow_roi_summaries([]) == []


# ---------------------------------------------------------------------------
# 17. summarise_roi_by_organisation — groups records correctly
# ---------------------------------------------------------------------------


def test_summarise_roi_by_organisation_returns_three_orgs():
    records = get_synthetic_adoption_metrics()
    roi_summaries = build_all_workflow_roi_summaries(records)
    org_summaries = summarise_roi_by_organisation(roi_summaries)
    assert len(org_summaries) == 3


def test_summarise_roi_by_organisation_org001_workflow_count():
    records = get_synthetic_adoption_metrics()
    roi_summaries = build_all_workflow_roi_summaries(records)
    org_summaries = summarise_roi_by_organisation(roi_summaries)
    org001 = next(s for s in org_summaries if s["organisation_id"] == "ORG001")
    assert org001["workflow_count"] == 4


def test_summarise_roi_by_organisation_required_keys():
    records = get_synthetic_adoption_metrics()
    roi_summaries = build_all_workflow_roi_summaries(records)
    org_summaries = summarise_roi_by_organisation(roi_summaries)
    expected_keys = {
        "organisation_id",
        "organisation_name",
        "workflow_count",
        "total_weekly_hours_saved",
        "total_monthly_hours_saved",
        "total_annual_hours_saved",
        "total_weekly_value_equivalent",
        "total_monthly_value_equivalent",
        "total_annual_value_equivalent",
        "average_efficiency_gain_percent",
        "average_confidence_change",
        "strong_or_clear_value_workflows",
        "needs_review_workflows",
    }
    for org in org_summaries:
        assert set(org.keys()) == expected_keys


def test_summarise_roi_by_organisation_totals_are_positive():
    records = get_synthetic_adoption_metrics()
    roi_summaries = build_all_workflow_roi_summaries(records)
    org_summaries = summarise_roi_by_organisation(roi_summaries)
    for org in org_summaries:
        assert org["total_annual_hours_saved"] > 0
        assert org["total_annual_value_equivalent"] > 0


# ---------------------------------------------------------------------------
# 18. summarise_portfolio_roi — returns correct top-level keys
# ---------------------------------------------------------------------------


EXPECTED_PORTFOLIO_KEYS = {
    "organisation_count",
    "workflow_count",
    "total_weekly_hours_saved",
    "total_monthly_hours_saved",
    "total_annual_hours_saved",
    "total_weekly_value_equivalent",
    "total_monthly_value_equivalent",
    "total_annual_value_equivalent",
    "average_efficiency_gain_percent",
    "average_confidence_change",
    "strong_value_workflows",
    "clear_value_workflows",
    "emerging_value_workflows",
    "low_value_workflows",
    "needs_review_workflows",
}


def test_summarise_portfolio_roi_returns_expected_keys():
    records = get_synthetic_adoption_metrics()
    roi_summaries = build_all_workflow_roi_summaries(records)
    portfolio = summarise_portfolio_roi(roi_summaries)
    assert set(portfolio.keys()) == EXPECTED_PORTFOLIO_KEYS


def test_summarise_portfolio_roi_organisation_count():
    records = get_synthetic_adoption_metrics()
    roi_summaries = build_all_workflow_roi_summaries(records)
    portfolio = summarise_portfolio_roi(roi_summaries)
    assert portfolio["organisation_count"] == 3


def test_summarise_portfolio_roi_workflow_count():
    records = get_synthetic_adoption_metrics()
    roi_summaries = build_all_workflow_roi_summaries(records)
    portfolio = summarise_portfolio_roi(roi_summaries)
    assert portfolio["workflow_count"] == 12


def test_summarise_portfolio_roi_value_indicators_sum_to_workflow_count():
    records = get_synthetic_adoption_metrics()
    roi_summaries = build_all_workflow_roi_summaries(records)
    portfolio = summarise_portfolio_roi(roi_summaries)
    indicator_total = (
        portfolio["strong_value_workflows"]
        + portfolio["clear_value_workflows"]
        + portfolio["emerging_value_workflows"]
        + portfolio["low_value_workflows"]
        + portfolio["needs_review_workflows"]
    )
    assert indicator_total == portfolio["workflow_count"]


def test_summarise_portfolio_roi_empty_list():
    portfolio = summarise_portfolio_roi([])
    assert portfolio["organisation_count"] == 0
    assert portfolio["workflow_count"] == 0
    assert portfolio["total_annual_hours_saved"] == 0.0


# ---------------------------------------------------------------------------
# 19. Synthetic Phase 1 records process through ROI engine without errors
# ---------------------------------------------------------------------------


def test_all_synthetic_records_process_without_error():
    records = get_synthetic_adoption_metrics()
    assert len(records) == 12
    roi_summaries = build_all_workflow_roi_summaries(records)
    assert len(roi_summaries) == 12
    for summary in roi_summaries:
        assert summary["weekly_hours_saved"] >= 0
        assert summary["annual_hours_saved"] >= 0
        assert summary["efficiency_gain_percent"] >= 0
        assert summary["annual_value_equivalent"] >= 0
        assert summary["adoption_value_indicator"] in (
            "Strong value",
            "Clear value",
            "Emerging value",
            "Low value",
            "Needs review",
        )


def test_all_synthetic_records_produce_valid_org_summaries():
    records = get_synthetic_adoption_metrics()
    roi_summaries = build_all_workflow_roi_summaries(records)
    org_summaries = summarise_roi_by_organisation(roi_summaries)
    assert len(org_summaries) == 3
    for org in org_summaries:
        assert org["workflow_count"] > 0
        assert org["total_annual_hours_saved"] >= 0


def test_all_synthetic_records_produce_valid_portfolio_summary():
    records = get_synthetic_adoption_metrics()
    roi_summaries = build_all_workflow_roi_summaries(records)
    portfolio = summarise_portfolio_roi(roi_summaries)
    assert portfolio["workflow_count"] == 12
    assert portfolio["organisation_count"] == 3
    assert portfolio["total_annual_hours_saved"] > 0
    assert portfolio["average_efficiency_gain_percent"] > 0
