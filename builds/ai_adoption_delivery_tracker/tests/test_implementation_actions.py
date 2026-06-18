"""Tests for Build 8 implementation action helpers."""

from data.synthetic_implementation_data import (
    get_synthetic_implementation_actions,
)
from logic.implementation_actions import (
    calculate_action_counts_by_priority,
    calculate_action_counts_by_status,
    get_actions_by_organisation,
    summarise_phase_1_delivery_actions,
    validate_all_implementation_actions,
    validate_implementation_action,
)


VALID_ACTION = {
    "action_id": "ACT999",
    "organisation_id": "ORG999",
    "organisation_name": "Synthetic Test Organisation",
    "workflow_id": "WF999",
    "workflow_name": "Synthetic delivery workflow",
    "related_build": "Build 7",
    "action_title": "Review synthetic implementation evidence",
    "action_description": "Review the fictional evidence and agree the next action.",
    "owner_role": "Delivery Lead",
    "priority": "High",
    "status": "In progress",
    "due_in_days": 10,
    "blocker": "",
    "governance_signoff_required": False,
    "training_followup_required": True,
    "client_checkin_required": True,
    "evidence_note": "Synthetic evidence only.",
}


def test_valid_action_returns_no_warnings():
    assert validate_implementation_action(VALID_ACTION) == []


def test_missing_required_fields_are_caught():
    action = dict(VALID_ACTION)
    del action["workflow_id"]

    warnings = validate_implementation_action(action)

    assert any("workflow_id" in warning for warning in warnings)


def test_invalid_priority_is_caught():
    action = dict(VALID_ACTION, priority="Urgent")

    warnings = validate_implementation_action(action)

    assert any("priority" in warning for warning in warnings)


def test_invalid_status_is_caught():
    action = dict(VALID_ACTION, status="Waiting")

    warnings = validate_implementation_action(action)

    assert any("status" in warning for warning in warnings)


def test_negative_due_in_days_is_caught():
    action = dict(VALID_ACTION, due_in_days=-1)

    warnings = validate_implementation_action(action)

    assert any("due_in_days" in warning for warning in warnings)


def test_non_boolean_governance_signoff_is_caught():
    action = dict(VALID_ACTION, governance_signoff_required="Yes")

    warnings = validate_implementation_action(action)

    assert any(
        "governance_signoff_required" in warning for warning in warnings
    )


def test_non_boolean_training_followup_is_caught():
    action = dict(VALID_ACTION, training_followup_required=1)

    warnings = validate_implementation_action(action)

    assert any(
        "training_followup_required" in warning for warning in warnings
    )


def test_non_boolean_client_checkin_is_caught():
    action = dict(VALID_ACTION, client_checkin_required=None)

    warnings = validate_implementation_action(action)

    assert any("client_checkin_required" in warning for warning in warnings)


def test_empty_action_title_is_caught():
    action = dict(VALID_ACTION, action_title="   ")

    warnings = validate_implementation_action(action)

    assert any("action_title" in warning for warning in warnings)


def test_empty_owner_role_is_caught():
    action = dict(VALID_ACTION, owner_role="")

    warnings = validate_implementation_action(action)

    assert any("owner_role" in warning for warning in warnings)


def test_status_counts_work():
    actions = get_synthetic_implementation_actions()

    assert calculate_action_counts_by_status(actions) == {
        "Not started": 3,
        "In progress": 4,
        "Blocked": 2,
        "Completed": 4,
        "Deferred": 2,
    }


def test_priority_counts_work():
    actions = get_synthetic_implementation_actions()

    assert calculate_action_counts_by_priority(actions) == {
        "Low": 3,
        "Medium": 6,
        "High": 5,
        "Critical": 1,
    }


def test_phase_1_summary_returns_expected_keys():
    actions = get_synthetic_implementation_actions()
    summary = summarise_phase_1_delivery_actions(actions)
    expected_keys = {
        "total_actions",
        "not_started_count",
        "in_progress_count",
        "blocked_count",
        "completed_count",
        "deferred_count",
        "critical_count",
        "high_count",
        "medium_count",
        "low_count",
        "governance_signoff_required_count",
        "training_followup_required_count",
        "client_checkin_required_count",
    }

    assert expected_keys == summary.keys()
    assert summary["total_actions"] == 15
    assert summary["governance_signoff_required_count"] == 5
    assert summary["training_followup_required_count"] == 7
    assert summary["client_checkin_required_count"] == 8


def test_organisation_filtering_works():
    actions = get_synthetic_implementation_actions()

    filtered = get_actions_by_organisation(actions, "ORG002")

    assert len(filtered) == 5
    assert all(action["organisation_id"] == "ORG002" for action in filtered)


def test_all_synthetic_actions_process_without_errors():
    actions = get_synthetic_implementation_actions()

    validation = validate_all_implementation_actions(actions)
    summary = summarise_phase_1_delivery_actions(actions)

    assert validation == {
        "total_actions": 15,
        "valid_actions": 15,
        "actions_with_warnings": 0,
        "warnings": [],
    }
    assert sum(calculate_action_counts_by_status(actions).values()) == 15
    assert sum(calculate_action_counts_by_priority(actions).values()) == 15
    assert summary["total_actions"] == 15
