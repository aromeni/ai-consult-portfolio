"""Tests for Build 7 Phase 4 Training, Confidence, and Adoption Readiness.

All test data is deterministic and uses synthetic demo records only.
No real client data, personal data, or regulated information is used.
"""

from data.synthetic_adoption_data import get_synthetic_adoption_metrics
from logic.training_readiness import (
    add_training_recommendations_to_summaries,
    build_all_training_readiness_summaries,
    build_training_readiness_summary,
    calculate_training_readiness_score,
    classify_confidence_growth,
    classify_confidence_level,
    classify_staff_adoption_readiness,
    classify_training_completion_band,
    classify_training_readiness_band,
    generate_training_support_recommendation,
    identify_training_support_need,
    prioritise_training_support_actions,
    summarise_training_readiness_by_organisation,
    summarise_training_readiness_by_related_build,
    summarise_training_readiness_by_staff_group,
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

# Blocked: adoption stopped
BLOCKED_RECORD = {
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
    "review_decision": "Stop this workflow",
    "evidence_note": "Unclear boundaries.",
}

# Needs support: low training completion
NEEDS_SUPPORT_RECORD = {
    "organisation_id": "TESTORG",
    "organisation_name": "Test Organisation",
    "workflow_id": "WFTEST1",
    "workflow_name": "Low training workflow",
    "related_build": "Build 4",
    "baseline_minutes_per_task": 60,
    "ai_supported_minutes_per_task": 45,
    "weekly_task_volume": 5,
    "staff_group": "Test staff",
    "confidence_before": 2.0,
    "confidence_after": 2.5,  # below 3.0 → needs support
    "training_completion_rate": 0.4,  # below 0.6 → needs support
    "pilot_status": "In progress",
    "quality_issues_logged": 0,
    "risk_incidents_logged": 0,
    "near_misses_logged": 0,
    "adoption_status": "Continue",
    "review_decision": "Continue with more training",
    "evidence_note": "Low training completion.",
}

# Scale ready: very strong training and confidence
SCALE_READY_RECORD = {
    "organisation_id": "TESTORG",
    "organisation_name": "Test Organisation",
    "workflow_id": "WFTEST2",
    "workflow_name": "Scale ready workflow",
    "related_build": "Build 4",
    "baseline_minutes_per_task": 60,
    "ai_supported_minutes_per_task": 30,
    "weekly_task_volume": 10,
    "staff_group": "Test staff",
    "confidence_before": 2.5,
    "confidence_after": 4.5,
    "training_completion_rate": 1.0,
    "pilot_status": "Completed",
    "quality_issues_logged": 0,
    "risk_incidents_logged": 0,
    "near_misses_logged": 0,
    "adoption_status": "Scale",
    "review_decision": "Scale to all teams",
    "evidence_note": "Excellent training and confidence outcomes.",
}

EXPECTED_TRAINING_READINESS_FIELDS = {
    "organisation_id",
    "organisation_name",
    "workflow_id",
    "workflow_name",
    "related_build",
    "staff_group",
    "training_completion_rate",
    "training_completion_band",
    "confidence_before",
    "confidence_after",
    "confidence_before_band",
    "confidence_after_band",
    "confidence_change",
    "confidence_growth_band",
    "training_readiness_score",
    "training_readiness_band",
    "training_support_need",
    "staff_adoption_readiness",
    "adoption_status",
    "pilot_status",
    "review_decision",
}

# ---------------------------------------------------------------------------
# Test 1: classify_training_completion_band returns correct bands
# ---------------------------------------------------------------------------


def test_training_completion_band_low():
    assert classify_training_completion_band(0.0) == "Low completion"
    assert classify_training_completion_band(0.59) == "Low completion"


def test_training_completion_band_moderate():
    assert classify_training_completion_band(0.6) == "Moderate completion"
    assert classify_training_completion_band(0.74) == "Moderate completion"


def test_training_completion_band_good():
    assert classify_training_completion_band(0.75) == "Good completion"
    assert classify_training_completion_band(0.89) == "Good completion"


def test_training_completion_band_strong():
    assert classify_training_completion_band(0.9) == "Strong completion"
    assert classify_training_completion_band(1.0) == "Strong completion"


# ---------------------------------------------------------------------------
# Test 2: invalid completion rates are clamped sensibly
# ---------------------------------------------------------------------------


def test_training_completion_band_below_zero():
    # Should be clamped to 0.0 → Low completion
    assert classify_training_completion_band(-0.5) == "Low completion"


def test_training_completion_band_above_one():
    # Should be clamped to 1.0 → Strong completion
    assert classify_training_completion_band(1.5) == "Strong completion"


# ---------------------------------------------------------------------------
# Test 3: classify_confidence_level returns correct bands
# ---------------------------------------------------------------------------


def test_confidence_level_low():
    assert classify_confidence_level(1.0) == "Low confidence"
    assert classify_confidence_level(2.9) == "Low confidence"


def test_confidence_level_developing():
    assert classify_confidence_level(3.0) == "Developing confidence"
    assert classify_confidence_level(3.4) == "Developing confidence"


def test_confidence_level_good():
    assert classify_confidence_level(3.5) == "Good confidence"
    assert classify_confidence_level(3.9) == "Good confidence"


def test_confidence_level_strong():
    assert classify_confidence_level(4.0) == "Strong confidence"
    assert classify_confidence_level(5.0) == "Strong confidence"


# ---------------------------------------------------------------------------
# Test 4: invalid confidence scores are clamped sensibly
# ---------------------------------------------------------------------------


def test_confidence_level_clamp_below_one():
    # Clamped to 1.0 → Low confidence
    assert classify_confidence_level(0.0) == "Low confidence"


def test_confidence_level_clamp_above_five():
    # Clamped to 5.0 → Strong confidence
    assert classify_confidence_level(6.0) == "Strong confidence"


# ---------------------------------------------------------------------------
# Test 5: classify_confidence_growth returns correct bands
# ---------------------------------------------------------------------------


def test_confidence_growth_no_growth():
    record = {"confidence_before": 3.0, "confidence_after": 2.5}  # negative change
    assert classify_confidence_growth(record) == "No growth"


def test_confidence_growth_no_growth_zero():
    record = {"confidence_before": 3.0, "confidence_after": 3.0}
    assert classify_confidence_growth(record) == "No growth"


def test_confidence_growth_small():
    record = {"confidence_before": 3.0, "confidence_after": 3.3}  # 0.3 change
    assert classify_confidence_growth(record) == "Small growth"


def test_confidence_growth_moderate():
    record = {"confidence_before": 2.5, "confidence_after": 3.1}  # 0.6 change
    assert classify_confidence_growth(record) == "Moderate growth"


def test_confidence_growth_strong():
    record = {"confidence_before": 2.4, "confidence_after": 3.7}  # 1.3 change
    assert classify_confidence_growth(record) == "Strong growth"


# ---------------------------------------------------------------------------
# Test 6: calculate_training_readiness_score works correctly
# ---------------------------------------------------------------------------


def test_training_readiness_score_wf001():
    # training=0.75, confidence_after=3.7, change=1.3
    # training_score = 0.75 * 40 = 30.0
    # after_score = (2.7 / 4.0) * 35 = 23.625
    # growth_score = min(1.3 / 2.0 * 25, 25) = 16.25
    # total = 30 + 23.625 + 16.25 = 69.875 → 69.88
    score = calculate_training_readiness_score(WF001_RECORD)
    assert score == 69.88


def test_training_readiness_score_scale_ready():
    # training=1.0, confidence_after=4.5, change=2.0
    # 40 + (3.5/4)*35 + min(2.0/2*25, 25) = 40 + 30.625 + 25 = 95.625
    score = calculate_training_readiness_score(SCALE_READY_RECORD)
    assert score == 95.62


def test_training_readiness_score_needs_support():
    # Low training and low confidence
    score = calculate_training_readiness_score(NEEDS_SUPPORT_RECORD)
    assert score < 60  # Should be low


# ---------------------------------------------------------------------------
# Test 7: score never returns below 0 or above 100
# ---------------------------------------------------------------------------


def test_training_readiness_score_never_negative():
    # Zero training, minimum confidence, negative change
    record = {
        "training_completion_rate": 0.0,
        "confidence_before": 3.0,
        "confidence_after": 1.0,  # change = -2.0 (negative)
    }
    score = calculate_training_readiness_score(record)
    assert score >= 0.0


def test_training_readiness_score_never_above_100():
    # Perfect record
    record = {
        "training_completion_rate": 1.0,
        "confidence_before": 1.0,
        "confidence_after": 5.0,
    }
    score = calculate_training_readiness_score(record)
    assert score <= 100.0


# ---------------------------------------------------------------------------
# Test 8: classify_training_readiness_band returns correct bands
# ---------------------------------------------------------------------------


def test_readiness_band_not_ready():
    assert classify_training_readiness_band(0.0) == "Not ready"
    assert classify_training_readiness_band(39.9) == "Not ready"


def test_readiness_band_partly_ready():
    assert classify_training_readiness_band(40.0) == "Partly ready"
    assert classify_training_readiness_band(59.9) == "Partly ready"


def test_readiness_band_ready_with_support():
    assert classify_training_readiness_band(60.0) == "Ready with support"
    assert classify_training_readiness_band(79.9) == "Ready with support"


def test_readiness_band_ready_to_scale():
    assert classify_training_readiness_band(80.0) == "Ready to scale"
    assert classify_training_readiness_band(100.0) == "Ready to scale"


# ---------------------------------------------------------------------------
# Test 9: identify_training_support_need returns Foundation training for low completion
# ---------------------------------------------------------------------------


def test_support_need_foundation_training():
    record = {**WF001_RECORD, "training_completion_rate": 0.45}
    assert identify_training_support_need(record) == "Foundation training"


def test_support_need_foundation_training_boundary():
    record = {**WF001_RECORD, "training_completion_rate": 0.59}
    assert identify_training_support_need(record) == "Foundation training"


# ---------------------------------------------------------------------------
# Test 10: identify_training_support_need returns Workflow-specific coaching
# ---------------------------------------------------------------------------


def test_support_need_workflow_specific_coaching():
    # training >= 0.6 but confidence_after < 3.5
    record = {**WF001_RECORD, "training_completion_rate": 0.72, "confidence_after": 3.2}
    assert identify_training_support_need(record) == "Workflow-specific coaching"


# ---------------------------------------------------------------------------
# Test 11: identify_training_support_need returns Scale enablement for strong records
# ---------------------------------------------------------------------------


def test_support_need_scale_enablement():
    # training >= 0.9, confidence_after >= 4.0, change >= 1.0
    record = {
        **WF001_RECORD,
        "training_completion_rate": 0.95,
        "confidence_before": 2.5,
        "confidence_after": 4.2,
    }
    assert identify_training_support_need(record) == "Scale enablement"


def test_support_need_light_touch_for_wf001():
    # WF001: training=0.75, after=3.7, change=1.3 — good but not scale-ready
    assert identify_training_support_need(WF001_RECORD) == "Light-touch support"


# ---------------------------------------------------------------------------
# Test 12: classify_staff_adoption_readiness returns Blocked for stopped/paused
# ---------------------------------------------------------------------------


def test_adoption_readiness_blocked_stop():
    record = {**WF001_RECORD, "adoption_status": "Stop", "pilot_status": "Completed"}
    assert classify_staff_adoption_readiness(record) == "Blocked"


def test_adoption_readiness_blocked_paused():
    record = {**WF001_RECORD, "adoption_status": "Continue", "pilot_status": "Paused"}
    assert classify_staff_adoption_readiness(record) == "Blocked"


def test_adoption_readiness_blocked_from_fixture():
    assert classify_staff_adoption_readiness(BLOCKED_RECORD) == "Blocked"


# ---------------------------------------------------------------------------
# Test 13: classify_staff_adoption_readiness returns Needs support for weak records
# ---------------------------------------------------------------------------


def test_adoption_readiness_needs_support_low_training():
    record = {**WF001_RECORD, "training_completion_rate": 0.45, "pilot_status": "In progress"}
    assert classify_staff_adoption_readiness(record) == "Needs support"


def test_adoption_readiness_needs_support_low_confidence():
    record = {
        **WF001_RECORD,
        "confidence_after": 2.8,  # below 3.0
        "pilot_status": "In progress",
        "adoption_status": "Continue",
    }
    assert classify_staff_adoption_readiness(record) == "Needs support"


def test_adoption_readiness_needs_support_from_fixture():
    assert classify_staff_adoption_readiness(NEEDS_SUPPORT_RECORD) == "Needs support"


# ---------------------------------------------------------------------------
# Test 14: classify_staff_adoption_readiness returns Scale ready for strong records
# ---------------------------------------------------------------------------


def test_adoption_readiness_scale_ready():
    # training=1.0, after=4.5, change=2.0, score=95.62, adoption=Scale
    assert classify_staff_adoption_readiness(SCALE_READY_RECORD) == "Scale ready"


def test_adoption_readiness_scale_ready_requires_all_conditions():
    # Same as scale_ready but adoption_status != Scale → not scale ready
    record = {**SCALE_READY_RECORD, "adoption_status": "Continue"}
    result = classify_staff_adoption_readiness(record)
    assert result != "Scale ready"


# ---------------------------------------------------------------------------
# Test 15: build_training_readiness_summary returns all expected fields
# ---------------------------------------------------------------------------


def test_training_readiness_summary_has_all_fields():
    summary = build_training_readiness_summary(WF001_RECORD)
    assert set(summary.keys()) == EXPECTED_TRAINING_READINESS_FIELDS


def test_training_readiness_summary_wf001_values():
    summary = build_training_readiness_summary(WF001_RECORD)
    assert summary["training_completion_rate"] == 0.75
    assert summary["training_completion_band"] == "Good completion"
    assert summary["confidence_before"] == 2.4
    assert summary["confidence_after"] == 3.7
    assert summary["confidence_before_band"] == "Low confidence"
    assert summary["confidence_after_band"] == "Good confidence"
    assert summary["confidence_change"] == 1.3
    assert summary["confidence_growth_band"] == "Strong growth"
    assert summary["training_readiness_score"] == 69.88
    assert summary["training_readiness_band"] == "Ready with support"
    assert summary["training_support_need"] == "Light-touch support"
    assert summary["staff_adoption_readiness"] == "Developing"


def test_training_readiness_summary_identifiers():
    summary = build_training_readiness_summary(WF001_RECORD)
    assert summary["organisation_id"] == "ORG001"
    assert summary["workflow_id"] == "WF001"
    assert summary["related_build"] == "Build 4"
    assert summary["staff_group"] == "Tutors"


# ---------------------------------------------------------------------------
# Test 16: build_all_training_readiness_summaries returns one per record
# ---------------------------------------------------------------------------


def test_build_all_training_readiness_summaries_count():
    records = [WF001_RECORD, BLOCKED_RECORD, SCALE_READY_RECORD]
    summaries = build_all_training_readiness_summaries(records)
    assert len(summaries) == 3


def test_build_all_training_readiness_summaries_empty():
    assert build_all_training_readiness_summaries([]) == []


# ---------------------------------------------------------------------------
# Test 17: summarise_training_readiness_by_staff_group groups correctly
# ---------------------------------------------------------------------------


def test_summarise_by_staff_group_count():
    # WF001 is "Tutors", BLOCKED is "Governance trustee" → 2 staff groups
    records = [WF001_RECORD, BLOCKED_RECORD]
    summaries = build_all_training_readiness_summaries(records)
    group_summaries = summarise_training_readiness_by_staff_group(summaries)
    assert len(group_summaries) == 2


def test_summarise_by_staff_group_keys():
    summaries = build_all_training_readiness_summaries([WF001_RECORD])
    group_summaries = summarise_training_readiness_by_staff_group(summaries)
    expected_keys = {
        "staff_group",
        "workflow_count",
        "average_training_completion_rate",
        "average_confidence_before",
        "average_confidence_after",
        "average_confidence_change",
        "average_training_readiness_score",
        "blocked_count",
        "needs_support_count",
        "developing_count",
        "adoption_ready_count",
        "scale_ready_count",
        "dominant_support_need",
    }
    assert set(group_summaries[0].keys()) == expected_keys


def test_summarise_by_staff_group_wf001():
    summaries = build_all_training_readiness_summaries([WF001_RECORD])
    group_summaries = summarise_training_readiness_by_staff_group(summaries)
    tutors = group_summaries[0]
    assert tutors["staff_group"] == "Tutors"
    assert tutors["workflow_count"] == 1
    assert tutors["developing_count"] == 1
    assert tutors["blocked_count"] == 0


# ---------------------------------------------------------------------------
# Test 18: summarise_training_readiness_by_organisation groups correctly
# ---------------------------------------------------------------------------


def test_summarise_by_organisation_three_orgs():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_training_readiness_summaries(records)
    org_summaries = summarise_training_readiness_by_organisation(summaries)
    assert len(org_summaries) == 3


def test_summarise_by_organisation_total_workflows():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_training_readiness_summaries(records)
    org_summaries = summarise_training_readiness_by_organisation(summaries)
    total = sum(o["workflow_count"] for o in org_summaries)
    assert total == 12


def test_summarise_by_organisation_keys():
    summaries = build_all_training_readiness_summaries([WF001_RECORD])
    org_summaries = summarise_training_readiness_by_organisation(summaries)
    expected_keys = {
        "organisation_id",
        "organisation_name",
        "workflow_count",
        "average_training_completion_rate",
        "average_confidence_before",
        "average_confidence_after",
        "average_confidence_change",
        "average_training_readiness_score",
        "blocked_count",
        "needs_support_count",
        "developing_count",
        "adoption_ready_count",
        "scale_ready_count",
        "dominant_support_need",
    }
    assert set(org_summaries[0].keys()) == expected_keys


# ---------------------------------------------------------------------------
# Test 19: summarise_training_readiness_by_related_build groups correctly
# ---------------------------------------------------------------------------


def test_summarise_by_related_build_count():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_training_readiness_summaries(records)
    build_summaries = summarise_training_readiness_by_related_build(summaries)
    # Synthetic data has Build 1, Build 4, Build 5, Build 6
    assert len(build_summaries) == 4


def test_summarise_by_related_build_total_workflows():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_training_readiness_summaries(records)
    build_summaries = summarise_training_readiness_by_related_build(summaries)
    total = sum(b["workflow_count"] for b in build_summaries)
    assert total == 12


def test_summarise_by_related_build_keys():
    summaries = build_all_training_readiness_summaries([WF001_RECORD])
    build_summaries = summarise_training_readiness_by_related_build(summaries)
    expected_keys = {
        "related_build",
        "workflow_count",
        "average_training_completion_rate",
        "average_confidence_change",
        "average_training_readiness_score",
        "blocked_count",
        "needs_support_count",
        "developing_count",
        "adoption_ready_count",
        "scale_ready_count",
        "dominant_support_need",
    }
    assert set(build_summaries[0].keys()) == expected_keys


# ---------------------------------------------------------------------------
# Test 20: prioritise_training_support_actions puts blocked/support-needed first
# ---------------------------------------------------------------------------


def test_prioritise_blocked_first():
    records = [WF001_RECORD, SCALE_READY_RECORD, BLOCKED_RECORD]
    summaries = build_all_training_readiness_summaries(records)
    prioritised = prioritise_training_support_actions(summaries)
    assert prioritised[0]["staff_adoption_readiness"] == "Blocked"


def test_prioritise_scale_ready_last():
    records = [WF001_RECORD, SCALE_READY_RECORD, BLOCKED_RECORD]
    summaries = build_all_training_readiness_summaries(records)
    prioritised = prioritise_training_support_actions(summaries)
    assert prioritised[-1]["staff_adoption_readiness"] == "Scale ready"


def test_prioritise_needs_support_before_developing():
    records = [WF001_RECORD, NEEDS_SUPPORT_RECORD]
    summaries = build_all_training_readiness_summaries(records)
    prioritised = prioritise_training_support_actions(summaries)
    assert prioritised[0]["staff_adoption_readiness"] == "Needs support"


# ---------------------------------------------------------------------------
# Test 21: generate_training_support_recommendation returns practical text
# ---------------------------------------------------------------------------


def test_recommendation_blocked():
    summary = build_training_readiness_summary(BLOCKED_RECORD)
    rec = generate_training_support_recommendation(summary)
    assert "paused or stopped" in rec.lower() or "resolve" in rec.lower()


def test_recommendation_foundation_training():
    summary = {
        "staff_adoption_readiness": "Needs support",
        "training_support_need": "Foundation training",
    }
    rec = generate_training_support_recommendation(summary)
    assert "foundation" in rec.lower()


def test_recommendation_workflow_specific():
    summary = {
        "staff_adoption_readiness": "Developing",
        "training_support_need": "Workflow-specific coaching",
    }
    rec = generate_training_support_recommendation(summary)
    assert "coaching" in rec.lower() or "workflow" in rec.lower()


def test_recommendation_confidence_reinforcement():
    summary = {
        "staff_adoption_readiness": "Developing",
        "training_support_need": "Confidence reinforcement",
    }
    rec = generate_training_support_recommendation(summary)
    assert "confidence" in rec.lower() or "reinforcement" in rec.lower()


def test_recommendation_scale_enablement():
    summary = {
        "staff_adoption_readiness": "Scale ready",
        "training_support_need": "Scale enablement",
    }
    rec = generate_training_support_recommendation(summary)
    assert "scale" in rec.lower()


def test_recommendation_light_touch():
    summary = build_training_readiness_summary(WF001_RECORD)
    rec = generate_training_support_recommendation(summary)
    assert "light" in rec.lower() or "monitor" in rec.lower() or "continue" in rec.lower()


# ---------------------------------------------------------------------------
# Test 22: add_training_recommendations_to_summaries adds field without mutating
# ---------------------------------------------------------------------------


def test_add_recommendations_adds_field():
    summaries = build_all_training_readiness_summaries([WF001_RECORD])
    enriched = add_training_recommendations_to_summaries(summaries)
    assert "training_recommendation" in enriched[0]
    assert isinstance(enriched[0]["training_recommendation"], str)
    assert len(enriched[0]["training_recommendation"]) > 0


def test_add_recommendations_does_not_mutate_original():
    summaries = build_all_training_readiness_summaries([WF001_RECORD])
    original_keys = set(summaries[0].keys())
    _ = add_training_recommendations_to_summaries(summaries)
    assert "training_recommendation" not in summaries[0]
    assert set(summaries[0].keys()) == original_keys


def test_add_recommendations_count():
    records = [WF001_RECORD, BLOCKED_RECORD, SCALE_READY_RECORD]
    summaries = build_all_training_readiness_summaries(records)
    enriched = add_training_recommendations_to_summaries(summaries)
    assert len(enriched) == 3


# ---------------------------------------------------------------------------
# Test 23: all 12 synthetic records process without errors
# ---------------------------------------------------------------------------


def test_all_synthetic_records_process():
    records = get_synthetic_adoption_metrics()
    assert len(records) == 12
    summaries = build_all_training_readiness_summaries(records)
    assert len(summaries) == 12
    for summary in summaries:
        assert set(summary.keys()) == EXPECTED_TRAINING_READINESS_FIELDS
        assert summary["staff_adoption_readiness"] in (
            "Blocked",
            "Needs support",
            "Developing",
            "Adoption ready",
            "Scale ready",
        )
        assert summary["training_support_need"] in (
            "Foundation training",
            "Workflow-specific coaching",
            "Confidence reinforcement",
            "Scale enablement",
            "Light-touch support",
        )


def test_all_synthetic_records_org_summaries():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_training_readiness_summaries(records)
    org_summaries = summarise_training_readiness_by_organisation(summaries)
    assert len(org_summaries) == 3
    total = sum(o["workflow_count"] for o in org_summaries)
    assert total == 12


def test_all_synthetic_records_blocked_count():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_training_readiness_summaries(records)
    # WF004 (Paused) and WF008 (Stop and Paused) are blocked
    blocked = [s for s in summaries if s["staff_adoption_readiness"] == "Blocked"]
    assert len(blocked) == 2


def test_all_synthetic_records_prioritised_first_is_blocked():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_training_readiness_summaries(records)
    prioritised = prioritise_training_support_actions(summaries)
    assert prioritised[0]["staff_adoption_readiness"] == "Blocked"


def test_all_synthetic_records_recommendations():
    records = get_synthetic_adoption_metrics()
    summaries = build_all_training_readiness_summaries(records)
    enriched = add_training_recommendations_to_summaries(summaries)
    assert len(enriched) == 12
    for item in enriched:
        assert "training_recommendation" in item
        assert len(item["training_recommendation"]) > 0
