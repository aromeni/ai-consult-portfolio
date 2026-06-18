"""Tests for Build 7 Phase 3 Workflow Impact and Bottleneck Analysis.

All test data is deterministic and uses synthetic demo records only.
No real client data, personal data, or regulated information is used.
"""

from data.synthetic_adoption_data import get_synthetic_adoption_metrics
from logic.workflow_impact import (
    add_recommendations_to_impact_summaries,
    build_all_workflow_impact_summaries,
    build_workflow_impact_summary,
    calculate_quality_issue_rate_per_10_tasks,
    calculate_risk_signal_count,
    classify_efficiency_bottleneck,
    classify_quality_bottleneck,
    classify_risk_bottleneck,
    classify_training_bottleneck,
    classify_workflow_impact_status,
    generate_workflow_action_recommendation,
    identify_primary_bottleneck,
    prioritise_workflows_for_action,
    summarise_workflow_impact_by_organisation,
    summarise_workflow_impact_by_related_build,
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
    "evidence_note": "Tutors report faster first drafts but still need human review.",
}

# Ready to scale: high efficiency, high confidence, high training, few quality issues, no incidents
SCALE_READY_RECORD = {
    "organisation_id": "ORG003",
    "organisation_name": "Greenacre Dental Group",
    "workflow_id": "WF009",
    "workflow_name": "Appointment admin workflow audit",
    "related_build": "Build 1",
    "baseline_minutes_per_task": 45,
    "ai_supported_minutes_per_task": 28,
    "weekly_task_volume": 20,
    "staff_group": "Reception team",
    "confidence_before": 2.7,
    "confidence_after": 3.9,
    "training_completion_rate": 0.83,
    "pilot_status": "Completed",
    "quality_issues_logged": 1,
    "risk_incidents_logged": 0,
    "near_misses_logged": 0,
    "adoption_status": "Scale",
    "review_decision": "Scale the workflow audit template to other admin processes",
    "evidence_note": "Reception staff identified repeatable admin bottlenecks.",
}

# Needs governance review: risk incident logged
GOVERNANCE_REVIEW_RECORD = {
    "organisation_id": "ORG002",
    "organisation_name": "Northside Community Advice",
    "workflow_id": "WF006",
    "workflow_name": "Draft service improvement report",
    "related_build": "Build 5",
    "baseline_minutes_per_task": 120,
    "ai_supported_minutes_per_task": 85,
    "weekly_task_volume": 3,
    "staff_group": "Service managers",
    "confidence_before": 2.3,
    "confidence_after": 3.0,
    "training_completion_rate": 0.60,
    "pilot_status": "In progress",
    "quality_issues_logged": 4,
    "risk_incidents_logged": 1,
    "near_misses_logged": 2,
    "adoption_status": "Review",
    "review_decision": "Review wording controls before producing further report drafts",
    "evidence_note": "Sensitive-case boundary checks need tightening.",
}

# Stop or pause: adoption_status Stop
STOP_OR_PAUSE_RECORD = {
    "organisation_id": "ORG002",
    "organisation_name": "Northside Community Advice",
    "workflow_id": "WF008",
    "workflow_name": "AI acceptable use policy review",
    "related_build": "Build 6",
    "baseline_minutes_per_task": 70,
    "ai_supported_minutes_per_task": 55,
    "weekly_task_volume": 2,
    "staff_group": "Governance trustee",
    "confidence_before": 2.0,
    "confidence_after": 2.8,
    "training_completion_rate": 0.55,
    "pilot_status": "Paused",
    "quality_issues_logged": 2,
    "risk_incidents_logged": 1,
    "near_misses_logged": 1,
    "adoption_status": "Stop",
    "review_decision": "Stop this workflow until advice-sector boundaries are approved",
    "evidence_note": "Unclear boundaries around advice-specific client information.",
}

EXPECTED_IMPACT_FIELDS = {
    "organisation_id",
    "organisation_name",
    "workflow_id",
    "workflow_name",
    "related_build",
    "staff_group",
    "weekly_task_volume",
    "efficiency_gain_percent",
    "weekly_hours_saved",
    "confidence_change",
    "training_completion_rate",
    "quality_issues_logged",
    "quality_issue_rate_per_10_tasks",
    "risk_incidents_logged",
    "near_misses_logged",
    "risk_signal_count",
    "training_bottleneck",
    "quality_bottleneck",
    "risk_bottleneck",
    "efficiency_bottleneck",
    "primary_bottleneck",
    "workflow_impact_status",
    "adoption_status",
    "pilot_status",
    "review_decision",
}

# ---------------------------------------------------------------------------
# Test 1: calculate_quality_issue_rate_per_10_tasks basic calculation
# ---------------------------------------------------------------------------


def test_quality_issue_rate_basic():
    record = {"quality_issues_logged": 3, "weekly_task_volume": 5}
    # 3 / 5 * 10 = 6.0
    assert calculate_quality_issue_rate_per_10_tasks(record) == 6.0


# ---------------------------------------------------------------------------
# Test 2: zero weekly volume returns 0.0
# ---------------------------------------------------------------------------


def test_quality_issue_rate_zero_volume():
    record = {"quality_issues_logged": 4, "weekly_task_volume": 0}
    assert calculate_quality_issue_rate_per_10_tasks(record) == 0.0


def test_quality_issue_rate_negative_volume():
    record = {"quality_issues_logged": 2, "weekly_task_volume": -1}
    assert calculate_quality_issue_rate_per_10_tasks(record) == 0.0


# ---------------------------------------------------------------------------
# Test 3: calculate_risk_signal_count basic
# ---------------------------------------------------------------------------


def test_risk_signal_count_basic():
    record = {"risk_incidents_logged": 2, "near_misses_logged": 3}
    assert calculate_risk_signal_count(record) == 5


def test_risk_signal_count_zero():
    record = {"risk_incidents_logged": 0, "near_misses_logged": 0}
    assert calculate_risk_signal_count(record) == 0


# ---------------------------------------------------------------------------
# Test 4: negative risk values are clamped to zero
# ---------------------------------------------------------------------------


def test_risk_signal_count_negative_clamped():
    record = {"risk_incidents_logged": -3, "near_misses_logged": -1}
    assert calculate_risk_signal_count(record) == 0


def test_risk_signal_count_mixed_negative():
    record = {"risk_incidents_logged": -1, "near_misses_logged": 2}
    assert calculate_risk_signal_count(record) == 2


# ---------------------------------------------------------------------------
# Test 5: classify_training_bottleneck
# ---------------------------------------------------------------------------


def test_training_bottleneck_clear():
    # Low training rate AND low confidence change → clear
    record = {
        "training_completion_rate": 0.4,
        "confidence_before": 2.0,
        "confidence_after": 2.3,  # change = 0.3, below 0.5
    }
    assert classify_training_bottleneck(record) == "Clear training bottleneck"


def test_training_bottleneck_possible_low_rate_only():
    # Low training rate but good confidence change → possible
    record = {
        "training_completion_rate": 0.5,
        "confidence_before": 2.0,
        "confidence_after": 2.6,  # change = 0.6, above 0.5
    }
    assert classify_training_bottleneck(record) == "Possible training bottleneck"


def test_training_bottleneck_possible_low_confidence_only():
    # Good training rate but low confidence change → possible
    record = {
        "training_completion_rate": 0.8,
        "confidence_before": 3.0,
        "confidence_after": 3.2,  # change = 0.2, below 0.5
    }
    assert classify_training_bottleneck(record) == "Possible training bottleneck"


def test_training_bottleneck_none():
    # Good training rate and good confidence change → no bottleneck
    record = {
        "training_completion_rate": 0.75,
        "confidence_before": 2.4,
        "confidence_after": 3.7,  # change = 1.3
    }
    assert classify_training_bottleneck(record) == "No training bottleneck"


# ---------------------------------------------------------------------------
# Test 6: classify_quality_bottleneck
# ---------------------------------------------------------------------------


def test_quality_bottleneck_clear_high_issues():
    # More than 3 quality issues → clear
    record = {"quality_issues_logged": 5, "weekly_task_volume": 10}
    assert classify_quality_bottleneck(record) == "Clear quality bottleneck"


def test_quality_bottleneck_clear_high_rate():
    # Rate >= 4.0 → clear
    record = {"quality_issues_logged": 2, "weekly_task_volume": 4}
    # rate = 2/4*10 = 5.0
    assert classify_quality_bottleneck(record) == "Clear quality bottleneck"


def test_quality_bottleneck_possible_by_issues():
    # 1–3 quality issues → possible
    record = {"quality_issues_logged": 2, "weekly_task_volume": 20}
    # rate = 2/20*10 = 1.0, below 2.0 but issues are between 1 and 3
    assert classify_quality_bottleneck(record) == "Possible quality bottleneck"


def test_quality_bottleneck_possible_by_rate():
    # Rate between 2.0 and 4.0 → possible
    record = {"quality_issues_logged": 0, "weekly_task_volume": 10}
    # Manually force rate via a different record; use issues=2, volume=8 → rate=2.5
    record2 = {"quality_issues_logged": 2, "weekly_task_volume": 8}
    assert classify_quality_bottleneck(record2) == "Possible quality bottleneck"


def test_quality_bottleneck_none():
    record = {"quality_issues_logged": 0, "weekly_task_volume": 10}
    assert classify_quality_bottleneck(record) == "No quality bottleneck"


# ---------------------------------------------------------------------------
# Test 7: classify_risk_bottleneck
# ---------------------------------------------------------------------------


def test_risk_bottleneck_clear_incident():
    record = {"risk_incidents_logged": 1, "near_misses_logged": 0}
    assert classify_risk_bottleneck(record) == "Clear risk bottleneck"


def test_risk_bottleneck_clear_near_misses():
    # More than 2 near misses → clear
    record = {"risk_incidents_logged": 0, "near_misses_logged": 3}
    assert classify_risk_bottleneck(record) == "Clear risk bottleneck"


def test_risk_bottleneck_possible():
    # 1 or 2 near misses → possible
    record = {"risk_incidents_logged": 0, "near_misses_logged": 2}
    assert classify_risk_bottleneck(record) == "Possible risk bottleneck"


def test_risk_bottleneck_none():
    record = {"risk_incidents_logged": 0, "near_misses_logged": 0}
    assert classify_risk_bottleneck(record) == "No risk bottleneck"


# ---------------------------------------------------------------------------
# Test 8: classify_efficiency_bottleneck
# ---------------------------------------------------------------------------


def test_efficiency_bottleneck_clear():
    # Gain < 10% → clear
    record = {
        "baseline_minutes_per_task": 100,
        "ai_supported_minutes_per_task": 95,
        "weekly_task_volume": 5,
    }
    # gain = 5/100*100 = 5%
    assert classify_efficiency_bottleneck(record) == "Clear efficiency bottleneck"


def test_efficiency_bottleneck_possible():
    # Gain between 10% and 30% → possible
    record = {
        "baseline_minutes_per_task": 100,
        "ai_supported_minutes_per_task": 80,
        "weekly_task_volume": 5,
    }
    # gain = 20%
    assert classify_efficiency_bottleneck(record) == "Possible efficiency bottleneck"


def test_efficiency_bottleneck_none():
    # Gain >= 30% → no bottleneck
    record = {
        "baseline_minutes_per_task": 100,
        "ai_supported_minutes_per_task": 60,
        "weekly_task_volume": 5,
    }
    # gain = 40%
    assert classify_efficiency_bottleneck(record) == "No efficiency bottleneck"


# ---------------------------------------------------------------------------
# Test 9: identify_primary_bottleneck prioritises risk before quality/training/efficiency
# ---------------------------------------------------------------------------


def test_primary_bottleneck_risk_takes_priority():
    # Risk and quality signals both present — risk should win
    record = {
        "risk_incidents_logged": 1,
        "near_misses_logged": 0,
        "quality_issues_logged": 5,
        "weekly_task_volume": 2,
        "baseline_minutes_per_task": 100,
        "ai_supported_minutes_per_task": 98,
        "training_completion_rate": 0.3,
        "confidence_before": 2.0,
        "confidence_after": 2.1,
    }
    assert identify_primary_bottleneck(record) == "Risk"


def test_primary_bottleneck_quality_over_training():
    # Quality signals present, no risk — quality wins over training
    record = {
        "risk_incidents_logged": 0,
        "near_misses_logged": 0,
        "quality_issues_logged": 5,
        "weekly_task_volume": 5,
        "baseline_minutes_per_task": 100,
        "ai_supported_minutes_per_task": 98,
        "training_completion_rate": 0.3,
        "confidence_before": 2.0,
        "confidence_after": 2.1,
    }
    assert identify_primary_bottleneck(record) == "Quality"


def test_primary_bottleneck_no_major():
    # All thresholds met — no major bottleneck
    record = {
        "risk_incidents_logged": 0,
        "near_misses_logged": 0,
        "quality_issues_logged": 0,
        "weekly_task_volume": 5,
        "baseline_minutes_per_task": 100,
        "ai_supported_minutes_per_task": 60,
        "training_completion_rate": 0.85,
        "confidence_before": 2.0,
        "confidence_after": 3.0,
    }
    assert identify_primary_bottleneck(record) == "No major bottleneck"


# ---------------------------------------------------------------------------
# Test 10: classify_workflow_impact_status returns "Ready to scale"
# ---------------------------------------------------------------------------


def test_workflow_impact_status_ready_to_scale():
    assert classify_workflow_impact_status(SCALE_READY_RECORD) == "Ready to scale"


# ---------------------------------------------------------------------------
# Test 11: classify_workflow_impact_status returns "Needs governance review"
# ---------------------------------------------------------------------------


def test_workflow_impact_status_needs_governance_review():
    assert classify_workflow_impact_status(GOVERNANCE_REVIEW_RECORD) == "Needs governance review"


def test_workflow_impact_status_needs_governance_review_adoption_review():
    # adoption_status "Review" alone triggers governance review
    record = {
        **WF001_RECORD,
        "adoption_status": "Review",
        "risk_incidents_logged": 0,
        "near_misses_logged": 1,
        "pilot_status": "In progress",
    }
    assert classify_workflow_impact_status(record) == "Needs governance review"


# ---------------------------------------------------------------------------
# Test 12: classify_workflow_impact_status returns "Stop or pause"
# ---------------------------------------------------------------------------


def test_workflow_impact_status_stop_or_pause_stop():
    assert classify_workflow_impact_status(STOP_OR_PAUSE_RECORD) == "Stop or pause"


def test_workflow_impact_status_stop_or_pause_paused_pilot():
    record = {**WF001_RECORD, "adoption_status": "Continue", "pilot_status": "Paused"}
    assert classify_workflow_impact_status(record) == "Stop or pause"


# ---------------------------------------------------------------------------
# Test 13: build_workflow_impact_summary returns all expected fields
# ---------------------------------------------------------------------------


def test_workflow_impact_summary_has_all_fields():
    summary = build_workflow_impact_summary(WF001_RECORD)
    assert set(summary.keys()) == EXPECTED_IMPACT_FIELDS


def test_workflow_impact_summary_wf001_values():
    summary = build_workflow_impact_summary(WF001_RECORD)
    assert summary["efficiency_gain_percent"] == 40.0
    assert summary["weekly_hours_saved"] == 3.0
    assert summary["confidence_change"] == 1.3
    assert summary["quality_issue_rate_per_10_tasks"] == 3.33
    assert summary["risk_signal_count"] == 1
    assert summary["training_bottleneck"] == "No training bottleneck"
    assert summary["quality_bottleneck"] == "Possible quality bottleneck"
    assert summary["risk_bottleneck"] == "Possible risk bottleneck"
    assert summary["efficiency_bottleneck"] == "No efficiency bottleneck"
    assert summary["primary_bottleneck"] == "Risk"
    assert summary["workflow_impact_status"] == "Positive but monitor"


def test_workflow_impact_summary_identifiers():
    summary = build_workflow_impact_summary(WF001_RECORD)
    assert summary["organisation_id"] == "ORG001"
    assert summary["workflow_id"] == "WF001"
    assert summary["related_build"] == "Build 4"
    assert summary["staff_group"] == "Tutors"


# ---------------------------------------------------------------------------
# Test 14: build_all_workflow_impact_summaries returns one summary per record
# ---------------------------------------------------------------------------


def test_build_all_workflow_impact_summaries_count():
    records = [WF001_RECORD, SCALE_READY_RECORD, GOVERNANCE_REVIEW_RECORD]
    summaries = build_all_workflow_impact_summaries(records)
    assert len(summaries) == 3


def test_build_all_workflow_impact_summaries_empty():
    assert build_all_workflow_impact_summaries([]) == []


# ---------------------------------------------------------------------------
# Test 15: summarise_workflow_impact_by_organisation groups correctly
# ---------------------------------------------------------------------------


def test_summarise_by_organisation_count():
    records = [WF001_RECORD, SCALE_READY_RECORD, GOVERNANCE_REVIEW_RECORD]
    summaries = build_all_workflow_impact_summaries(records)
    org_summaries = summarise_workflow_impact_by_organisation(summaries)
    # Three different orgs → three org entries
    assert len(org_summaries) == 3


def test_summarise_by_organisation_keys():
    summaries = build_all_workflow_impact_summaries([WF001_RECORD])
    org_summaries = summarise_workflow_impact_by_organisation(summaries)
    expected_keys = {
        "organisation_id",
        "organisation_name",
        "workflow_count",
        "ready_to_scale_count",
        "positive_but_monitor_count",
        "needs_improvement_count",
        "needs_governance_review_count",
        "stop_or_pause_count",
        "risk_bottleneck_count",
        "quality_bottleneck_count",
        "training_bottleneck_count",
        "efficiency_bottleneck_count",
        "average_efficiency_gain_percent",
        "average_confidence_change",
    }
    assert set(org_summaries[0].keys()) == expected_keys


def test_summarise_by_organisation_wf001_status():
    summaries = build_all_workflow_impact_summaries([WF001_RECORD])
    org_summaries = summarise_workflow_impact_by_organisation(summaries)
    org = org_summaries[0]
    assert org["workflow_count"] == 1
    assert org["positive_but_monitor_count"] == 1
    assert org["ready_to_scale_count"] == 0


# ---------------------------------------------------------------------------
# Test 16: summarise_workflow_impact_by_related_build groups correctly
# ---------------------------------------------------------------------------


def test_summarise_by_related_build_count():
    records = [WF001_RECORD, SCALE_READY_RECORD]
    summaries = build_all_workflow_impact_summaries(records)
    build_summaries = summarise_workflow_impact_by_related_build(summaries)
    # WF001 is Build 4, SCALE_READY is Build 1 → two build entries
    assert len(build_summaries) == 2


def test_summarise_by_related_build_keys():
    summaries = build_all_workflow_impact_summaries([WF001_RECORD])
    build_summaries = summarise_workflow_impact_by_related_build(summaries)
    expected_keys = {
        "related_build",
        "workflow_count",
        "ready_to_scale_count",
        "positive_but_monitor_count",
        "needs_improvement_count",
        "needs_governance_review_count",
        "stop_or_pause_count",
        "average_efficiency_gain_percent",
        "average_confidence_change",
        "dominant_bottleneck",
    }
    assert set(build_summaries[0].keys()) == expected_keys


def test_summarise_by_related_build_dominant_bottleneck():
    # Two workflows, both with risk bottleneck → Risk should dominate
    summaries = build_all_workflow_impact_summaries([WF001_RECORD, GOVERNANCE_REVIEW_RECORD])
    # WF001 → Risk, GOVERNANCE_REVIEW → Risk
    build_summaries = summarise_workflow_impact_by_related_build(summaries)
    # WF001 and GOVERNANCE_REVIEW are different builds (Build 4 vs Build 5)
    build4 = next(b for b in build_summaries if b["related_build"] == "Build 4")
    assert build4["dominant_bottleneck"] == "Risk"


# ---------------------------------------------------------------------------
# Test 17: prioritise_workflows_for_action puts high-risk/problem workflows first
# ---------------------------------------------------------------------------


def test_prioritise_workflows_stop_first():
    records = [SCALE_READY_RECORD, WF001_RECORD, STOP_OR_PAUSE_RECORD]
    summaries = build_all_workflow_impact_summaries(records)
    prioritised = prioritise_workflows_for_action(summaries)
    assert prioritised[0]["workflow_impact_status"] == "Stop or pause"


def test_prioritise_workflows_governance_before_monitor():
    records = [WF001_RECORD, GOVERNANCE_REVIEW_RECORD]
    summaries = build_all_workflow_impact_summaries(records)
    prioritised = prioritise_workflows_for_action(summaries)
    assert prioritised[0]["workflow_impact_status"] == "Needs governance review"


def test_prioritise_workflows_ready_to_scale_last():
    records = [SCALE_READY_RECORD, WF001_RECORD, STOP_OR_PAUSE_RECORD]
    summaries = build_all_workflow_impact_summaries(records)
    prioritised = prioritise_workflows_for_action(summaries)
    assert prioritised[-1]["workflow_impact_status"] == "Ready to scale"


# ---------------------------------------------------------------------------
# Test 18: generate_workflow_action_recommendation returns practical text
# ---------------------------------------------------------------------------


def test_recommendation_stop_or_pause():
    summary = build_workflow_impact_summary(STOP_OR_PAUSE_RECORD)
    rec = generate_workflow_action_recommendation(summary)
    assert "governance" in rec.lower()


def test_recommendation_ready_to_scale():
    summary = build_workflow_impact_summary(SCALE_READY_RECORD)
    rec = generate_workflow_action_recommendation(summary)
    assert "scaling" in rec.lower()


def test_recommendation_risk_bottleneck():
    summary = build_workflow_impact_summary(WF001_RECORD)
    # WF001 primary_bottleneck = "Risk"
    rec = generate_workflow_action_recommendation(summary)
    assert "governance" in rec.lower()


def test_recommendation_quality_bottleneck():
    summary = {
        "workflow_impact_status": "Positive but monitor",
        "primary_bottleneck": "Quality",
    }
    rec = generate_workflow_action_recommendation(summary)
    assert "output" in rec.lower() or "quality" in rec.lower() or "review" in rec.lower()


def test_recommendation_training_bottleneck():
    summary = {
        "workflow_impact_status": "Needs improvement",
        "primary_bottleneck": "Training",
    }
    rec = generate_workflow_action_recommendation(summary)
    assert "training" in rec.lower()


def test_recommendation_efficiency_bottleneck():
    summary = {
        "workflow_impact_status": "Needs improvement",
        "primary_bottleneck": "Efficiency",
    }
    rec = generate_workflow_action_recommendation(summary)
    assert "workflow" in rec.lower() or "time" in rec.lower()


def test_recommendation_positive_but_monitor():
    summary = {
        "workflow_impact_status": "Positive but monitor",
        "primary_bottleneck": "No major bottleneck",
    }
    rec = generate_workflow_action_recommendation(summary)
    assert "pilot" in rec.lower() or "monitor" in rec.lower()


# ---------------------------------------------------------------------------
# Test 19: add_recommendations_to_impact_summaries adds fields without mutating
# ---------------------------------------------------------------------------


def test_add_recommendations_adds_field():
    summaries = build_all_workflow_impact_summaries([WF001_RECORD])
    enriched = add_recommendations_to_impact_summaries(summaries)
    assert "recommended_action" in enriched[0]
    assert isinstance(enriched[0]["recommended_action"], str)
    assert len(enriched[0]["recommended_action"]) > 0


def test_add_recommendations_does_not_mutate_original():
    summaries = build_all_workflow_impact_summaries([WF001_RECORD])
    original_keys = set(summaries[0].keys())
    _ = add_recommendations_to_impact_summaries(summaries)
    assert set(summaries[0].keys()) == original_keys
    assert "recommended_action" not in summaries[0]


def test_add_recommendations_count():
    records = [WF001_RECORD, SCALE_READY_RECORD, STOP_OR_PAUSE_RECORD]
    summaries = build_all_workflow_impact_summaries(records)
    enriched = add_recommendations_to_impact_summaries(summaries)
    assert len(enriched) == 3


# ---------------------------------------------------------------------------
# Test 20: all 12 synthetic Phase 1 adoption records process without errors
# ---------------------------------------------------------------------------


def test_all_synthetic_records_process_without_error():
    records = get_synthetic_adoption_metrics()
    assert len(records) == 12
    summaries = build_all_workflow_impact_summaries(records)
    assert len(summaries) == 12
    for summary in summaries:
        assert set(summary.keys()) == EXPECTED_IMPACT_FIELDS
        assert summary["workflow_impact_status"] in (
            "Ready to scale",
            "Positive but monitor",
            "Needs improvement",
            "Needs governance review",
            "Stop or pause",
        )
        assert summary["primary_bottleneck"] in (
            "Risk",
            "Quality",
            "Training",
            "Efficiency",
            "No major bottleneck",
        )


def test_all_synthetic_records_org_summaries():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_workflow_impact_summaries(records)
    org_summaries = summarise_workflow_impact_by_organisation(summaries)
    assert len(org_summaries) == 3
    total_workflows = sum(o["workflow_count"] for o in org_summaries)
    assert total_workflows == 12


def test_all_synthetic_records_build_summaries():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_workflow_impact_summaries(records)
    build_summaries = summarise_workflow_impact_by_related_build(summaries)
    # Synthetic data uses Build 1, Build 4, Build 5, Build 6
    assert len(build_summaries) == 4
    total_workflows = sum(b["workflow_count"] for b in build_summaries)
    assert total_workflows == 12


def test_prioritise_all_synthetic_records():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_workflow_impact_summaries(records)
    prioritised = prioritise_workflows_for_action(summaries)
    assert len(prioritised) == 12
    # First entry should be Stop or pause or Needs governance review
    assert prioritised[0]["workflow_impact_status"] in ("Stop or pause", "Needs governance review")
    # Last entry should be Ready to scale
    assert prioritised[-1]["workflow_impact_status"] == "Ready to scale"


def test_add_recommendations_all_synthetic_records():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_workflow_impact_summaries(records)
    enriched = add_recommendations_to_impact_summaries(summaries)
    assert len(enriched) == 12
    for item in enriched:
        assert "recommended_action" in item
        assert len(item["recommended_action"]) > 0
