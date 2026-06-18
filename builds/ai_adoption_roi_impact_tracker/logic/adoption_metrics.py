"""Validation and basic Phase 1 metric helpers for Build 7."""


REQUIRED_FIELDS = [
    "organisation_id",
    "organisation_name",
    "workflow_id",
    "workflow_name",
    "related_build",
    "baseline_minutes_per_task",
    "ai_supported_minutes_per_task",
    "weekly_task_volume",
    "staff_group",
    "confidence_before",
    "confidence_after",
    "training_completion_rate",
    "pilot_status",
    "quality_issues_logged",
    "risk_incidents_logged",
    "near_misses_logged",
    "adoption_status",
    "review_decision",
    "evidence_note",
]

VALID_ADOPTION_STATUSES = {"Stop", "Continue", "Scale", "Review"}
VALID_PILOT_STATUSES = {"Not started", "In progress", "Completed", "Paused"}
COUNT_FIELDS = [
    "quality_issues_logged",
    "risk_incidents_logged",
    "near_misses_logged",
]


def calculate_minutes_saved_per_task(record: dict) -> int:
    """Calculate minutes saved per task, clamped to zero."""
    saved = record.get("baseline_minutes_per_task", 0) - record.get(
        "ai_supported_minutes_per_task",
        0,
    )
    return max(int(saved), 0)


def calculate_weekly_minutes_saved(record: dict) -> int:
    """Calculate weekly minutes saved for a workflow."""
    return calculate_minutes_saved_per_task(record) * int(record.get("weekly_task_volume", 0))


def calculate_confidence_change(record: dict) -> float:
    """Calculate confidence change rounded to two decimal places."""
    return round(record.get("confidence_after", 0.0) - record.get("confidence_before", 0.0), 2)


def validate_adoption_record(record: dict) -> list[str]:
    """Return validation warnings for one adoption metric record."""
    warnings = []

    for field in REQUIRED_FIELDS:
        if field not in record:
            warnings.append(f"Missing required field: {field}")

    if "baseline_minutes_per_task" in record and record["baseline_minutes_per_task"] < 0:
        warnings.append("baseline_minutes_per_task is below zero")

    if "ai_supported_minutes_per_task" in record and record["ai_supported_minutes_per_task"] < 0:
        warnings.append("ai_supported_minutes_per_task is below zero")

    if (
        "baseline_minutes_per_task" in record
        and "ai_supported_minutes_per_task" in record
        and record["ai_supported_minutes_per_task"] > record["baseline_minutes_per_task"]
    ):
        warnings.append("ai_supported_minutes_per_task is greater than baseline_minutes_per_task")

    if "weekly_task_volume" in record and record["weekly_task_volume"] < 0:
        warnings.append("weekly_task_volume is below zero")

    if "confidence_before" in record and not 1.0 <= record["confidence_before"] <= 5.0:
        warnings.append("confidence_before is outside 1.0 to 5.0")

    if "confidence_after" in record and not 1.0 <= record["confidence_after"] <= 5.0:
        warnings.append("confidence_after is outside 1.0 to 5.0")

    if (
        "training_completion_rate" in record
        and not 0.0 <= record["training_completion_rate"] <= 1.0
    ):
        warnings.append("training_completion_rate is outside 0.0 to 1.0")

    for field in COUNT_FIELDS:
        if field in record and record[field] < 0:
            warnings.append(f"{field} cannot be negative")
        if field in record and not isinstance(record[field], int):
            warnings.append(f"{field} must be an integer")

    if "adoption_status" in record and record["adoption_status"] not in VALID_ADOPTION_STATUSES:
        valid_values = ", ".join(sorted(VALID_ADOPTION_STATUSES))
        warnings.append(f"adoption_status must be one of: {valid_values}")

    if "pilot_status" in record and record["pilot_status"] not in VALID_PILOT_STATUSES:
        valid_values = ", ".join(sorted(VALID_PILOT_STATUSES))
        warnings.append(f"pilot_status must be one of: {valid_values}")

    return warnings


def validate_all_adoption_records(records: list[dict]) -> dict:
    """Validate all adoption records and return a compact summary."""
    warnings = []
    records_with_warnings = 0

    for record in records:
        record_warnings = validate_adoption_record(record)
        if record_warnings:
            records_with_warnings += 1
            workflow_id = record.get("workflow_id", "Unknown workflow")
            warnings.extend(f"{workflow_id}: {warning}" for warning in record_warnings)

    total_records = len(records)
    return {
        "total_records": total_records,
        "valid_records": total_records - records_with_warnings,
        "records_with_warnings": records_with_warnings,
        "warnings": warnings,
    }


def summarise_phase_1_metrics(records: list[dict]) -> dict:
    """Return a non-financial Phase 1 summary for the adoption metrics."""
    total_workflows = len(records)

    if total_workflows == 0:
        return {
            "total_workflows": 0,
            "total_weekly_minutes_saved": 0,
            "average_confidence_change": 0.0,
            "average_training_completion_rate": 0.0,
            "total_quality_issues": 0,
            "total_risk_incidents": 0,
            "total_near_misses": 0,
        }

    return {
        "total_workflows": total_workflows,
        "total_weekly_minutes_saved": sum(calculate_weekly_minutes_saved(record) for record in records),
        "average_confidence_change": round(
            sum(calculate_confidence_change(record) for record in records) / total_workflows,
            2,
        ),
        "average_training_completion_rate": round(
            sum(record["training_completion_rate"] for record in records) / total_workflows,
            2,
        ),
        "total_quality_issues": sum(record["quality_issues_logged"] for record in records),
        "total_risk_incidents": sum(record["risk_incidents_logged"] for record in records),
        "total_near_misses": sum(record["near_misses_logged"] for record in records),
    }
