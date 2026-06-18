"""Tests for Build 7 Phase 5 — Risk, Quality, and Responsible Adoption Review.

All test records are deterministic synthetic fixtures. No real client data.
"""

import pytest

from data.synthetic_adoption_data import get_synthetic_adoption_metrics
from logic.risk_quality_review import (
    add_risk_quality_recommendations,
    build_all_risk_quality_summaries,
    build_risk_quality_summary,
    calculate_total_quality_signals,
    calculate_total_risk_signals,
    classify_quality_level,
    classify_responsible_adoption_status,
    classify_risk_level,
    classify_scaling_permission,
    generate_risk_quality_recommendation,
    identify_control_need,
    prioritise_risk_quality_actions,
    summarise_risk_quality_by_organisation,
    summarise_risk_quality_by_related_build,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

WF001_RECORD = {
    "organisation_id": "ORG001",
    "organisation_name": "BrightPath Skills Training",
    "workflow_id": "WF001",
    "workflow_name": "Lesson plan drafting",
    "related_build": "Build 4",
    "staff_group": "Tutors",
    "baseline_minutes_per_task": 75,
    "ai_supported_minutes_per_task": 45,
    "weekly_task_volume": 6,
    "confidence_before": 2.4,
    "confidence_after": 3.7,
    "training_completion_rate": 0.75,
    "pilot_status": "In progress",
    "quality_issues_logged": 2,
    "risk_incidents_logged": 0,
    "near_misses_logged": 1,
    "adoption_status": "Continue",
    "review_decision": "Continue with stronger review checklist",
}

PAUSED_RECORD = {
    "organisation_id": "ORG001",
    "organisation_name": "BrightPath Skills Training",
    "workflow_id": "WF004",
    "workflow_name": "Governance policy checklist review",
    "related_build": "Build 6",
    "staff_group": "Quality lead",
    "baseline_minutes_per_task": 90,
    "ai_supported_minutes_per_task": 65,
    "weekly_task_volume": 2,
    "confidence_before": 2.1,
    "confidence_after": 3.2,
    "training_completion_rate": 0.80,
    "pilot_status": "Paused",
    "quality_issues_logged": 3,
    "risk_incidents_logged": 1,
    "near_misses_logged": 2,
    "adoption_status": "Review",
    "review_decision": "Review governance evidence before widening use",
}

GOVERNANCE_REVIEW_RECORD = {
    "organisation_id": "ORG002",
    "organisation_name": "Northside Community Advice",
    "workflow_id": "WF006",
    "workflow_name": "Draft service improvement report",
    "related_build": "Build 5",
    "staff_group": "Service managers",
    "baseline_minutes_per_task": 120,
    "ai_supported_minutes_per_task": 85,
    "weekly_task_volume": 3,
    "confidence_before": 2.3,
    "confidence_after": 3.0,
    "training_completion_rate": 0.60,
    "pilot_status": "In progress",
    "quality_issues_logged": 4,
    "risk_incidents_logged": 1,
    "near_misses_logged": 2,
    "adoption_status": "Review",
    "review_decision": "Review wording controls before producing further report drafts",
}

STOP_RECORD = {
    "organisation_id": "ORG002",
    "organisation_name": "Northside Community Advice",
    "workflow_id": "WF008",
    "workflow_name": "AI acceptable use policy review",
    "related_build": "Build 6",
    "staff_group": "Governance trustee",
    "baseline_minutes_per_task": 70,
    "ai_supported_minutes_per_task": 55,
    "weekly_task_volume": 2,
    "confidence_before": 2.0,
    "confidence_after": 2.8,
    "training_completion_rate": 0.55,
    "pilot_status": "Paused",
    "quality_issues_logged": 2,
    "risk_incidents_logged": 1,
    "near_misses_logged": 1,
    "adoption_status": "Stop",
    "review_decision": "Stop this workflow until advice-sector boundaries are approved",
}

SCALE_PERMITTED_RECORD = {
    "organisation_id": "ORG003",
    "organisation_name": "Greenacre Dental Group",
    "workflow_id": "WF011",
    "workflow_name": "Clinical admin AI boundary training",
    "related_build": "Build 4",
    "staff_group": "Reception and managers",
    "baseline_minutes_per_task": 55,
    "ai_supported_minutes_per_task": 38,
    "weekly_task_volume": 6,
    "confidence_before": 2.1,
    "confidence_after": 3.6,
    "training_completion_rate": 0.92,
    "pilot_status": "Completed",
    "quality_issues_logged": 0,
    "risk_incidents_logged": 0,
    "near_misses_logged": 0,
    "adoption_status": "Scale",
    "review_decision": "Scale refresher training to new starter induction",
}

SCALE_WITH_CONTROLS_RECORD = {
    "organisation_id": "ORG003",
    "organisation_name": "Greenacre Dental Group",
    "workflow_id": "WF009",
    "workflow_name": "Appointment admin workflow audit",
    "related_build": "Build 1",
    "staff_group": "Reception team",
    "baseline_minutes_per_task": 45,
    "ai_supported_minutes_per_task": 28,
    "weekly_task_volume": 20,
    "confidence_before": 2.7,
    "confidence_after": 3.9,
    "training_completion_rate": 0.83,
    "pilot_status": "Completed",
    "quality_issues_logged": 1,
    "risk_incidents_logged": 0,
    "near_misses_logged": 0,
    "adoption_status": "Scale",
    "review_decision": "Scale the workflow audit template to other admin processes",
}

DO_NOT_SCALE_RECORD = {
    "organisation_id": "ORG001",
    "organisation_name": "BrightPath Skills Training",
    "workflow_id": "WF003",
    "workflow_name": "Workflow readiness review",
    "related_build": "Build 1",
    "staff_group": "Operations team",
    "baseline_minutes_per_task": 60,
    "ai_supported_minutes_per_task": 40,
    "weekly_task_volume": 4,
    "confidence_before": 2.6,
    "confidence_after": 3.3,
    "training_completion_rate": 0.70,
    "pilot_status": "In progress",
    "quality_issues_logged": 0,
    "risk_incidents_logged": 0,
    "near_misses_logged": 0,
    "adoption_status": "Continue",
    "review_decision": "Continue monthly readiness reviews before adding new workflows",
}

EXPECTED_RISK_QUALITY_FIELDS = {
    "organisation_id",
    "organisation_name",
    "workflow_id",
    "workflow_name",
    "related_build",
    "staff_group",
    "quality_issues_logged",
    "risk_incidents_logged",
    "near_misses_logged",
    "total_quality_signals",
    "total_risk_signals",
    "quality_level",
    "risk_level",
    "responsible_adoption_status",
    "control_need",
    "scaling_permission",
    "training_completion_rate",
    "confidence_after",
    "adoption_status",
    "pilot_status",
    "review_decision",
}


# ---------------------------------------------------------------------------
# Test 1 — quality signals clamp negative values
# ---------------------------------------------------------------------------


def test_quality_signals_clamp_negative_values():
    record = {"quality_issues_logged": -3}
    assert calculate_total_quality_signals(record) == 0


def test_quality_signals_returns_positive_value():
    record = {"quality_issues_logged": 4}
    assert calculate_total_quality_signals(record) == 4


# ---------------------------------------------------------------------------
# Test 2 — risk signals clamp negative values
# ---------------------------------------------------------------------------


def test_risk_signals_clamp_negative_values():
    record = {"risk_incidents_logged": -1, "near_misses_logged": -2}
    assert calculate_total_risk_signals(record) == 0


def test_risk_signals_sum_positive_values():
    record = {"risk_incidents_logged": 1, "near_misses_logged": 2}
    assert calculate_total_risk_signals(record) == 3


def test_risk_signals_clamp_each_component():
    record = {"risk_incidents_logged": -1, "near_misses_logged": 3}
    assert calculate_total_risk_signals(record) == 3


# ---------------------------------------------------------------------------
# Test 3 — quality level classification
# ---------------------------------------------------------------------------


def test_quality_level_low():
    record = {"quality_issues_logged": 0}
    assert classify_quality_level(record) == "Low quality concern"


def test_quality_level_low_at_two():
    record = {"quality_issues_logged": 2}
    assert classify_quality_level(record) == "Low quality concern"


def test_quality_level_moderate_at_threshold():
    record = {"quality_issues_logged": 3}
    assert classify_quality_level(record) == "Moderate quality concern"


def test_quality_level_moderate_at_four():
    record = {"quality_issues_logged": 4}
    assert classify_quality_level(record) == "Moderate quality concern"


def test_quality_level_high_at_threshold():
    record = {"quality_issues_logged": 5}
    assert classify_quality_level(record) == "High quality concern"


def test_quality_level_high_above_threshold():
    record = {"quality_issues_logged": 8}
    assert classify_quality_level(record) == "High quality concern"


# ---------------------------------------------------------------------------
# Test 4 — risk level classification
# ---------------------------------------------------------------------------


def test_risk_level_low():
    record = {"risk_incidents_logged": 0, "near_misses_logged": 0}
    assert classify_risk_level(record) == "Low risk concern"


def test_risk_level_low_at_one_near_miss():
    record = {"risk_incidents_logged": 0, "near_misses_logged": 1}
    assert classify_risk_level(record) == "Low risk concern"


def test_risk_level_moderate_at_two_near_misses():
    record = {"risk_incidents_logged": 0, "near_misses_logged": 2}
    assert classify_risk_level(record) == "Moderate risk concern"


def test_risk_level_high_with_incident():
    record = {"risk_incidents_logged": 1, "near_misses_logged": 0}
    assert classify_risk_level(record) == "High risk concern"


def test_risk_level_high_takes_priority_over_moderate():
    record = {"risk_incidents_logged": 1, "near_misses_logged": 3}
    assert classify_risk_level(record) == "High risk concern"


# ---------------------------------------------------------------------------
# Test 5 — responsible adoption status: scale
# ---------------------------------------------------------------------------


def test_responsible_adoption_status_scale():
    assert classify_responsible_adoption_status(SCALE_PERMITTED_RECORD) == "Responsible to scale"


def test_responsible_adoption_status_scale_requires_all_conditions():
    record = {**SCALE_PERMITTED_RECORD, "confidence_after": 3.4}
    assert classify_responsible_adoption_status(record) == "Responsible to continue"


# ---------------------------------------------------------------------------
# Test 6 — responsible adoption status: governance review
# ---------------------------------------------------------------------------


def test_responsible_adoption_status_governance_review():
    assert classify_responsible_adoption_status(GOVERNANCE_REVIEW_RECORD) == "Requires governance review"


def test_responsible_adoption_status_governance_review_near_misses():
    record = {
        "adoption_status": "Continue",
        "pilot_status": "In progress",
        "risk_incidents_logged": 0,
        "near_misses_logged": 3,
        "quality_issues_logged": 0,
        "training_completion_rate": 0.80,
        "confidence_after": 3.8,
    }
    assert classify_responsible_adoption_status(record) == "Requires governance review"


# ---------------------------------------------------------------------------
# Test 7 — responsible adoption status: pause
# ---------------------------------------------------------------------------


def test_responsible_adoption_status_pause_when_pilot_paused():
    assert classify_responsible_adoption_status(PAUSED_RECORD) == "Pause adoption"


def test_responsible_adoption_status_pause_when_adoption_stopped():
    assert classify_responsible_adoption_status(STOP_RECORD) == "Pause adoption"


def test_responsible_adoption_status_pause_takes_priority_over_governance():
    record = {**STOP_RECORD, "risk_incidents_logged": 2}
    assert classify_responsible_adoption_status(record) == "Pause adoption"


# ---------------------------------------------------------------------------
# Test 8 — control need priority
# ---------------------------------------------------------------------------


def test_control_need_governance_review_for_incidents():
    record = {"risk_incidents_logged": 1, "near_misses_logged": 0, "quality_issues_logged": 0,
              "training_completion_rate": 0.80, "confidence_after": 3.8}
    assert identify_control_need(record) == "Governance review"


def test_control_need_governance_review_for_high_near_misses():
    record = {"risk_incidents_logged": 0, "near_misses_logged": 3, "quality_issues_logged": 5,
              "training_completion_rate": 0.80, "confidence_after": 3.8}
    assert identify_control_need(record) == "Governance review"


def test_control_need_quality_assurance_checklist():
    record = {"risk_incidents_logged": 0, "near_misses_logged": 0, "quality_issues_logged": 3,
              "training_completion_rate": 0.80, "confidence_after": 3.8}
    assert identify_control_need(record) == "Quality assurance checklist"


def test_control_need_incident_logging_review():
    record = {"risk_incidents_logged": 0, "near_misses_logged": 1, "quality_issues_logged": 0,
              "training_completion_rate": 0.80, "confidence_after": 3.8}
    assert identify_control_need(record) == "Incident logging review"


def test_control_need_training_reinforcement_low_training():
    record = {"risk_incidents_logged": 0, "near_misses_logged": 0, "quality_issues_logged": 0,
              "training_completion_rate": 0.60, "confidence_after": 3.8}
    assert identify_control_need(record) == "Training reinforcement"


def test_control_need_training_reinforcement_low_confidence():
    record = {"risk_incidents_logged": 0, "near_misses_logged": 0, "quality_issues_logged": 0,
              "training_completion_rate": 0.80, "confidence_after": 3.0}
    assert identify_control_need(record) == "Training reinforcement"


def test_control_need_standard_monitoring():
    assert identify_control_need(SCALE_PERMITTED_RECORD) == "Standard monitoring"


# ---------------------------------------------------------------------------
# Test 9 — scaling permission: permitted
# ---------------------------------------------------------------------------


def test_scaling_permission_permitted():
    assert classify_scaling_permission(SCALE_PERMITTED_RECORD) == "Scale permitted"


# ---------------------------------------------------------------------------
# Test 10 — scaling permission: with controls
# ---------------------------------------------------------------------------


def test_scaling_permission_with_controls_quality():
    assert classify_scaling_permission(WF001_RECORD) == "Scale with controls"


def test_scaling_permission_with_controls_near_misses():
    record = {
        "adoption_status": "Continue",
        "pilot_status": "In progress",
        "risk_incidents_logged": 0,
        "near_misses_logged": 1,
        "quality_issues_logged": 0,
        "training_completion_rate": 0.80,
        "confidence_after": 3.8,
    }
    assert classify_scaling_permission(record) == "Scale with controls"


# ---------------------------------------------------------------------------
# Test 11 — scaling permission: do not scale
# ---------------------------------------------------------------------------


def test_scaling_permission_do_not_scale_low_training():
    assert classify_scaling_permission(DO_NOT_SCALE_RECORD) == "Do not scale yet"


def test_scaling_permission_do_not_scale_low_confidence():
    record = {**SCALE_PERMITTED_RECORD, "confidence_after": 3.4}
    assert classify_scaling_permission(record) == "Do not scale yet"


def test_scaling_permission_do_not_scale_with_incident():
    record = {**SCALE_PERMITTED_RECORD, "risk_incidents_logged": 1}
    assert classify_scaling_permission(record) == "Do not scale yet"


# ---------------------------------------------------------------------------
# Test 12 — scaling permission: pause/stop
# ---------------------------------------------------------------------------


def test_scaling_permission_pause_when_paused():
    assert classify_scaling_permission(PAUSED_RECORD) == "Pause or stop"


def test_scaling_permission_pause_when_stopped():
    assert classify_scaling_permission(STOP_RECORD) == "Pause or stop"


# ---------------------------------------------------------------------------
# Test 13 — workflow summary has expected keys
# ---------------------------------------------------------------------------


def test_workflow_summary_has_expected_keys():
    summary = build_risk_quality_summary(WF001_RECORD)
    assert set(summary.keys()) == EXPECTED_RISK_QUALITY_FIELDS


def test_workflow_summary_field_count():
    summary = build_risk_quality_summary(WF001_RECORD)
    assert len(summary) == 21


def test_workflow_summary_wf001_values():
    summary = build_risk_quality_summary(WF001_RECORD)
    assert summary["workflow_id"] == "WF001"
    assert summary["total_quality_signals"] == 2
    assert summary["total_risk_signals"] == 1
    assert summary["quality_level"] == "Low quality concern"
    assert summary["risk_level"] == "Low risk concern"
    assert summary["responsible_adoption_status"] == "Continue with controls"
    assert summary["control_need"] == "Incident logging review"
    assert summary["scaling_permission"] == "Scale with controls"


# ---------------------------------------------------------------------------
# Test 14 — all summaries match input length
# ---------------------------------------------------------------------------


def test_all_summaries_match_input_length():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    assert len(summaries) == len(records)


def test_all_summaries_have_expected_keys():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    for summary in summaries:
        assert set(summary.keys()) == EXPECTED_RISK_QUALITY_FIELDS


# ---------------------------------------------------------------------------
# Test 15 — organisation summary groups correctly
# ---------------------------------------------------------------------------


def test_organisation_summary_groups_correctly():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    org_summaries = summarise_risk_quality_by_organisation(summaries)
    assert len(org_summaries) == 3


def test_organisation_summary_workflow_counts():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    org_summaries = summarise_risk_quality_by_organisation(summaries)
    org_map = {s["organisation_id"]: s for s in org_summaries}
    assert org_map["ORG001"]["workflow_count"] == 4
    assert org_map["ORG002"]["workflow_count"] == 4
    assert org_map["ORG003"]["workflow_count"] == 4


def test_organisation_summary_pause_counts():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    org_summaries = summarise_risk_quality_by_organisation(summaries)
    org_map = {s["organisation_id"]: s for s in org_summaries}
    assert org_map["ORG001"]["pause_adoption_count"] == 1
    assert org_map["ORG002"]["pause_adoption_count"] == 1
    assert org_map["ORG003"]["pause_adoption_count"] == 0


def test_organisation_summary_scale_permitted_in_org003():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    org_summaries = summarise_risk_quality_by_organisation(summaries)
    org_map = {s["organisation_id"]: s for s in org_summaries}
    assert org_map["ORG003"]["scale_permitted_count"] == 1


def test_organisation_summary_governance_review_in_org002():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    org_summaries = summarise_risk_quality_by_organisation(summaries)
    org_map = {s["organisation_id"]: s for s in org_summaries}
    assert org_map["ORG002"]["requires_governance_review_count"] == 1


def test_organisation_summary_high_risk_count():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    org_summaries = summarise_risk_quality_by_organisation(summaries)
    org_map = {s["organisation_id"]: s for s in org_summaries}
    assert org_map["ORG001"]["high_risk_concern_count"] == 1
    assert org_map["ORG002"]["high_risk_concern_count"] == 2
    assert org_map["ORG003"]["high_risk_concern_count"] == 0


# ---------------------------------------------------------------------------
# Test 16 — related-build summary groups correctly
# ---------------------------------------------------------------------------


def test_related_build_summary_groups_correctly():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    build_summaries = summarise_risk_quality_by_related_build(summaries)
    assert len(build_summaries) == 4


def test_related_build_summary_build6_pause_count():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    build_summaries = summarise_risk_quality_by_related_build(summaries)
    build_map = {s["related_build"]: s for s in build_summaries}
    assert build_map["Build 6"]["pause_adoption_count"] == 2


def test_related_build_summary_build4_scale_permitted():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    build_summaries = summarise_risk_quality_by_related_build(summaries)
    build_map = {s["related_build"]: s for s in build_summaries}
    assert build_map["Build 4"]["scale_permitted_count"] == 1


def test_related_build_summary_build5_governance_review():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    build_summaries = summarise_risk_quality_by_related_build(summaries)
    build_map = {s["related_build"]: s for s in build_summaries}
    assert build_map["Build 5"]["requires_governance_review_count"] == 1


def test_related_build_summary_build6_high_risk_count():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    build_summaries = summarise_risk_quality_by_related_build(summaries)
    build_map = {s["related_build"]: s for s in build_summaries}
    assert build_map["Build 6"]["high_risk_concern_count"] == 2


# ---------------------------------------------------------------------------
# Test 17 — prioritisation puts risky workflows first
# ---------------------------------------------------------------------------


def test_prioritisation_puts_pause_adoption_first():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    prioritised = prioritise_risk_quality_actions(summaries)
    assert prioritised[0]["responsible_adoption_status"] == "Pause adoption"


def test_prioritisation_pause_before_governance_review():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    prioritised = prioritise_risk_quality_actions(summaries)
    statuses = [s["responsible_adoption_status"] for s in prioritised]
    pause_indices = [i for i, s in enumerate(statuses) if s == "Pause adoption"]
    gov_indices = [i for i, s in enumerate(statuses) if s == "Requires governance review"]
    assert max(pause_indices) < min(gov_indices)


def test_prioritisation_within_pause_highest_risk_first():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    prioritised = prioritise_risk_quality_actions(summaries)
    pause_group = [s for s in prioritised if s["responsible_adoption_status"] == "Pause adoption"]
    assert pause_group[0]["total_risk_signals"] >= pause_group[1]["total_risk_signals"]


def test_prioritisation_responsible_to_scale_last():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    prioritised = prioritise_risk_quality_actions(summaries)
    last_status = prioritised[-1]["responsible_adoption_status"]
    assert last_status == "Responsible to scale"


# ---------------------------------------------------------------------------
# Test 18 — recommendations are added without mutation
# ---------------------------------------------------------------------------


def test_recommendations_added_to_summaries():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    enriched = add_risk_quality_recommendations(summaries)
    assert all("risk_quality_recommendation" in s for s in enriched)


def test_recommendations_do_not_mutate_originals():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    original_keys = set(summaries[0].keys())
    add_risk_quality_recommendations(summaries)
    assert set(summaries[0].keys()) == original_keys


def test_recommendation_text_governance():
    summary = {"control_need": "Governance review"}
    rec = generate_risk_quality_recommendation(summary)
    assert "governance controls" in rec.lower()


def test_recommendation_text_quality():
    summary = {"control_need": "Quality assurance checklist"}
    rec = generate_risk_quality_recommendation(summary)
    assert "quality assurance" in rec.lower()


def test_recommendation_text_incident_logging():
    summary = {"control_need": "Incident logging review"}
    rec = generate_risk_quality_recommendation(summary)
    assert "near-miss" in rec.lower()


def test_recommendation_text_training():
    summary = {"control_need": "Training reinforcement"}
    rec = generate_risk_quality_recommendation(summary)
    assert "training" in rec.lower()


def test_recommendation_text_standard_monitoring():
    summary = {"control_need": "Standard monitoring"}
    rec = generate_risk_quality_recommendation(summary)
    assert "monitoring" in rec.lower()


# ---------------------------------------------------------------------------
# Test 19 — all synthetic adoption records process without errors
# ---------------------------------------------------------------------------


def test_all_synthetic_records_process_without_errors():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    assert len(summaries) == 12
    for summary in summaries:
        assert isinstance(summary, dict)
        assert len(summary) == 21


def test_wf011_is_scale_permitted():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    wf011 = next(s for s in summaries if s["workflow_id"] == "WF011")
    assert wf011["scaling_permission"] == "Scale permitted"
    assert wf011["responsible_adoption_status"] == "Responsible to scale"


def test_wf004_and_wf008_are_pause_adoption():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    wf_map = {s["workflow_id"]: s for s in summaries}
    assert wf_map["WF004"]["responsible_adoption_status"] == "Pause adoption"
    assert wf_map["WF008"]["responsible_adoption_status"] == "Pause adoption"


def test_wf006_requires_governance_review():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    wf006 = next(s for s in summaries if s["workflow_id"] == "WF006")
    assert wf006["responsible_adoption_status"] == "Requires governance review"


def test_wf009_responsible_to_scale():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_risk_quality_summaries(records)
    wf009 = next(s for s in summaries if s["workflow_id"] == "WF009")
    assert wf009["responsible_adoption_status"] == "Responsible to scale"
