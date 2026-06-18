"""Tests for Build 7 adoption metric helpers."""

from logic.adoption_metrics import (
    calculate_confidence_change,
    calculate_minutes_saved_per_task,
    calculate_weekly_minutes_saved,
    summarise_phase_1_metrics,
    validate_adoption_record,
    validate_all_adoption_records,
)


VALID_RECORD = {
    "organisation_id": "ORG999",
    "organisation_name": "Synthetic Test Organisation",
    "workflow_id": "WF999",
    "workflow_name": "Synthetic workflow",
    "related_build": "Build 1",
    "baseline_minutes_per_task": 60,
    "ai_supported_minutes_per_task": 35,
    "weekly_task_volume": 4,
    "staff_group": "Operations",
    "confidence_before": 2.25,
    "confidence_after": 3.5,
    "training_completion_rate": 0.75,
    "pilot_status": "In progress",
    "quality_issues_logged": 1,
    "risk_incidents_logged": 0,
    "near_misses_logged": 2,
    "adoption_status": "Continue",
    "review_decision": "Continue with weekly review",
    "evidence_note": "Synthetic evidence note.",
}


def test_calculate_minutes_saved_per_task():
    assert calculate_minutes_saved_per_task(VALID_RECORD) == 25


def test_negative_savings_are_clamped_to_zero():
    record = dict(
        VALID_RECORD,
        baseline_minutes_per_task=20,
        ai_supported_minutes_per_task=35,
    )

    assert calculate_minutes_saved_per_task(record) == 0


def test_calculate_weekly_minutes_saved():
    assert calculate_weekly_minutes_saved(VALID_RECORD) == 100


def test_calculate_confidence_change():
    assert calculate_confidence_change(VALID_RECORD) == 1.25


def test_validation_catches_invalid_confidence_values():
    record = dict(VALID_RECORD, confidence_before=0.5, confidence_after=5.5)

    warnings = validate_adoption_record(record)

    assert any("confidence_before" in warning for warning in warnings)
    assert any("confidence_after" in warning for warning in warnings)


def test_validation_catches_invalid_training_completion_rates():
    record = dict(VALID_RECORD, training_completion_rate=1.25)

    warnings = validate_adoption_record(record)

    assert any("training_completion_rate" in warning for warning in warnings)


def test_validation_catches_negative_incident_counts():
    record = dict(VALID_RECORD, risk_incidents_logged=-1)

    warnings = validate_adoption_record(record)

    assert any("risk_incidents_logged" in warning for warning in warnings)


def test_validation_catches_invalid_adoption_status():
    record = dict(VALID_RECORD, adoption_status="Maybe")

    warnings = validate_adoption_record(record)

    assert any("adoption_status" in warning for warning in warnings)


def test_validate_all_adoption_records():
    invalid_record = dict(VALID_RECORD, workflow_id="WF998", pilot_status="Delayed")

    summary = validate_all_adoption_records([VALID_RECORD, invalid_record])

    assert summary["total_records"] == 2
    assert summary["valid_records"] == 1
    assert summary["records_with_warnings"] == 1
    assert any("WF998" in warning for warning in summary["warnings"])


def test_summarise_phase_1_metrics():
    second_record = dict(
        VALID_RECORD,
        workflow_id="WF998",
        baseline_minutes_per_task=50,
        ai_supported_minutes_per_task=30,
        weekly_task_volume=3,
        confidence_before=3.0,
        confidence_after=4.0,
        training_completion_rate=0.85,
        quality_issues_logged=2,
        risk_incidents_logged=1,
        near_misses_logged=0,
    )

    summary = summarise_phase_1_metrics([VALID_RECORD, second_record])

    assert summary["total_workflows"] == 2
    assert summary["total_weekly_minutes_saved"] == 160
    assert summary["average_confidence_change"] == 1.12
    assert summary["average_training_completion_rate"] == 0.80
    assert summary["total_quality_issues"] == 3
    assert summary["total_risk_incidents"] == 1
    assert summary["total_near_misses"] == 2
