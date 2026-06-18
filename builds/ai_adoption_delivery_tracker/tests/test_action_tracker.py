"""Tests for the Build 8 Phase 2 action tracker engine."""

from data.synthetic_implementation_data import (
    get_synthetic_implementation_actions,
)
from logic.action_tracker import (
    add_action_recommendations,
    build_action_tracker_summary,
    build_all_action_tracker_summaries,
    calculate_action_score,
    classify_action_attention_level,
    classify_delivery_state,
    classify_due_window,
    generate_action_tracker_recommendation,
    is_action_blocked,
    is_action_complete,
    prioritise_actions,
    summarise_actions_by_organisation,
    summarise_actions_by_related_build,
)


BASE_ACTION = {
    "action_id": "ACT999",
    "organisation_id": "ORG999",
    "organisation_name": "Synthetic Test Organisation",
    "workflow_id": "WF999",
    "workflow_name": "Synthetic workflow",
    "related_build": "Build 7",
    "action_title": "Review implementation action",
    "owner_role": "Delivery Lead",
    "priority": "Medium",
    "status": "In progress",
    "due_in_days": 20,
    "blocker": "",
    "governance_signoff_required": False,
    "training_followup_required": True,
    "client_checkin_required": True,
}


def test_due_window_classification():
    assert classify_due_window(dict(BASE_ACTION, due_in_days=7)) == "Due now"
    assert classify_due_window(dict(BASE_ACTION, due_in_days=14)) == "Due soon"
    assert classify_due_window(dict(BASE_ACTION, due_in_days=30)) == "Due later"
    assert (
        classify_due_window(dict(BASE_ACTION, due_in_days=31))
        == "No immediate pressure"
    )


def test_attention_level_classification():
    assert (
        classify_action_attention_level(
            dict(BASE_ACTION, status="Blocked", priority="Low")
        )
        == "Critical attention"
    )
    assert (
        classify_action_attention_level(
            dict(BASE_ACTION, status="Deferred", priority="High")
        )
        == "High attention"
    )
    assert (
        classify_action_attention_level(
            dict(BASE_ACTION, status="Not started", priority="Low")
        )
        == "Medium attention"
    )
    assert (
        classify_action_attention_level(
            dict(
                BASE_ACTION,
                status="Deferred",
                priority="Low",
                due_in_days=40,
            )
        )
        == "Low attention"
    )


def test_blocked_action_detection():
    assert is_action_blocked(dict(BASE_ACTION, status="Blocked")) is True
    assert is_action_blocked(dict(BASE_ACTION, blocker="Approval pending")) is True
    assert is_action_blocked(BASE_ACTION) is False


def test_completed_action_detection():
    assert is_action_complete(dict(BASE_ACTION, status="Completed")) is True
    assert is_action_complete(BASE_ACTION) is False


def test_delivery_state_classification():
    assert (
        classify_delivery_state(dict(BASE_ACTION, status="Completed"))
        == "Completed"
    )
    assert (
        classify_delivery_state(dict(BASE_ACTION, blocker="Approval pending"))
        == "Blocked"
    )
    assert classify_delivery_state(BASE_ACTION) == "Active"
    assert (
        classify_delivery_state(dict(BASE_ACTION, status="Not started"))
        == "Waiting"
    )
    assert (
        classify_delivery_state(dict(BASE_ACTION, status="Deferred"))
        == "Deferred"
    )


def test_action_score_calculation():
    action = dict(
        BASE_ACTION,
        priority="Critical",
        status="Blocked",
        due_in_days=5,
        blocker="Approval pending",
    )

    assert calculate_action_score(action) == 75


def test_action_score_never_below_zero():
    action = dict(
        BASE_ACTION,
        priority="Unknown",
        status="Completed",
        due_in_days=40,
    )

    assert calculate_action_score(action) == 0


def test_action_tracker_summary_has_expected_keys():
    summary = build_action_tracker_summary(BASE_ACTION)
    expected_keys = {
        "action_id",
        "organisation_id",
        "organisation_name",
        "workflow_id",
        "workflow_name",
        "related_build",
        "action_title",
        "owner_role",
        "priority",
        "status",
        "due_in_days",
        "due_window",
        "delivery_state",
        "attention_level",
        "action_score",
        "blocker",
        "governance_signoff_required",
        "training_followup_required",
        "client_checkin_required",
    }

    assert summary.keys() == expected_keys


def test_all_summaries_match_input_length():
    actions = get_synthetic_implementation_actions()

    summaries = build_all_action_tracker_summaries(actions)

    assert len(summaries) == len(actions)


def test_prioritisation_puts_high_score_actions_first():
    actions = [
        dict(BASE_ACTION, action_id="LOW", priority="Low", due_in_days=40),
        dict(
            BASE_ACTION,
            action_id="HIGH",
            priority="Critical",
            status="Blocked",
            blocker="Approval pending",
            due_in_days=2,
        ),
    ]

    prioritised = prioritise_actions(actions)

    assert prioritised[0]["action_id"] == "HIGH"
    assert prioritised[0]["action_score"] > prioritised[1]["action_score"]


def test_organisation_summary_groups_correctly():
    actions = get_synthetic_implementation_actions()

    summaries = summarise_actions_by_organisation(actions)
    summary_by_id = {
        summary["organisation_id"]: summary for summary in summaries
    }

    assert len(summaries) == 3
    assert summary_by_id["ORG001"]["total_actions"] == 5
    assert summary_by_id["ORG002"]["total_actions"] == 5
    assert summary_by_id["ORG003"]["total_actions"] == 5
    assert summary_by_id["ORG001"]["completed_count"] == 2


def test_related_build_summary_groups_correctly():
    actions = get_synthetic_implementation_actions()

    summaries = summarise_actions_by_related_build(actions)
    summary_by_build = {
        summary["related_build"]: summary for summary in summaries
    }

    assert set(summary_by_build) == {
        "Build 1",
        "Build 4",
        "Build 5",
        "Build 6",
        "Build 7",
    }
    assert summary_by_build["Build 4"]["total_actions"] == 4
    assert summary_by_build["Build 7"]["total_actions"] == 3


def test_recommendation_generation():
    completed = build_action_tracker_summary(
        dict(BASE_ACTION, status="Completed")
    )
    critical = build_action_tracker_summary(
        dict(BASE_ACTION, status="Blocked")
    )
    high = build_action_tracker_summary(
        dict(BASE_ACTION, priority="High", status="Deferred")
    )
    medium = build_action_tracker_summary(
        dict(BASE_ACTION, status="Not started")
    )
    low = build_action_tracker_summary(
        dict(
            BASE_ACTION,
            priority="Low",
            status="Deferred",
            due_in_days=40,
        )
    )

    assert generate_action_tracker_recommendation(completed).startswith(
        "No further delivery action"
    )
    assert generate_action_tracker_recommendation(critical).startswith(
        "Escalate this action"
    )
    assert generate_action_tracker_recommendation(high).startswith(
        "Prioritise this action"
    )
    assert generate_action_tracker_recommendation(medium).startswith(
        "Keep this action moving"
    )
    assert generate_action_tracker_recommendation(low).startswith(
        "Monitor this action"
    )


def test_recommendations_are_added_without_mutation():
    summaries = [build_action_tracker_summary(BASE_ACTION)]
    original = dict(summaries[0])

    enriched = add_action_recommendations(summaries)

    assert summaries[0] == original
    assert "action_recommendation" not in summaries[0]
    assert "action_recommendation" in enriched[0]
    assert enriched[0] is not summaries[0]


def test_all_synthetic_implementation_actions_process_without_errors():
    actions = get_synthetic_implementation_actions()

    summaries = build_all_action_tracker_summaries(actions)
    prioritised = prioritise_actions(actions)
    organisation_summaries = summarise_actions_by_organisation(actions)
    build_summaries = summarise_actions_by_related_build(actions)
    enriched = add_action_recommendations(prioritised)

    assert len(summaries) == 15
    assert len(prioritised) == 15
    assert len(enriched) == 15
    assert len(organisation_summaries) == 3
    assert len(build_summaries) == 5
    assert all(summary["action_score"] >= 0 for summary in summaries)
