"""Tests for the Build 8 Phase 3 blocker review engine."""

from data.synthetic_implementation_data import (
    get_synthetic_implementation_actions,
)
from logic.blocker_review import (
    add_blocker_recommendations,
    build_all_blocker_review_summaries,
    build_blocker_review_summary,
    calculate_dependency_count,
    classify_blocker_severity,
    classify_blocker_type,
    classify_delivery_risk_level,
    classify_dependency_need,
    generate_blocker_resolution_recommendation,
    has_blocker,
    prioritise_blockers_for_resolution,
    requires_escalation,
    summarise_blockers_by_organisation,
    summarise_blockers_by_related_build,
)


BASE_ACTION = {
    "action_id": "ACT999",
    "organisation_id": "ORG999",
    "organisation_name": "Synthetic Test Organisation",
    "workflow_id": "WF999",
    "workflow_name": "Synthetic workflow",
    "related_build": "Build 7",
    "action_title": "Resolve synthetic delivery blocker",
    "owner_role": "Delivery Lead",
    "priority": "Medium",
    "status": "In progress",
    "due_in_days": 20,
    "blocker": "",
    "governance_signoff_required": False,
    "training_followup_required": False,
    "client_checkin_required": False,
}


def test_blocker_detection_works():
    assert has_blocker(dict(BASE_ACTION, status="Blocked")) is True
    assert has_blocker(dict(BASE_ACTION, blocker="Approval pending")) is True
    assert has_blocker(BASE_ACTION) is False


def test_blocker_type_classification_works():
    assert (
        classify_blocker_type(
            dict(BASE_ACTION, blocker="Governance approval is pending")
        )
        == "Governance blocker"
    )
    assert (
        classify_blocker_type(
            dict(BASE_ACTION, blocker="Staff training guidance is incomplete")
        )
        == "Training blocker"
    )
    assert (
        classify_blocker_type(
            dict(BASE_ACTION, blocker="Client feedback is required")
        )
        == "Client decision blocker"
    )
    assert (
        classify_blocker_type(
            dict(BASE_ACTION, blocker="Quality criteria are unclear")
        )
        == "Quality blocker"
    )
    assert (
        classify_blocker_type(
            dict(BASE_ACTION, blocker="Action owner is not confirmed")
        )
        == "Ownership blocker"
    )
    assert (
        classify_blocker_type(
            dict(BASE_ACTION, blocker="External timetable is delayed")
        )
        == "General delivery blocker"
    )
    assert classify_blocker_type(BASE_ACTION) == "No blocker"


def test_status_blocked_with_empty_blocker_returns_general_blocker():
    action = dict(BASE_ACTION, status="Blocked", blocker="")

    assert classify_blocker_type(action) == "General delivery blocker"


def test_blocker_severity_classification_works():
    assert (
        classify_blocker_severity(
            dict(BASE_ACTION, status="Blocked", priority="Critical")
        )
        == "Critical blocker"
    )
    assert (
        classify_blocker_severity(
            dict(BASE_ACTION, status="Blocked", priority="Low")
        )
        == "High blocker"
    )
    assert (
        classify_blocker_severity(
            dict(BASE_ACTION, priority="High", blocker="Owner pending")
        )
        == "Moderate blocker"
    )
    assert (
        classify_blocker_severity(
            dict(BASE_ACTION, priority="Low", blocker="Timetable delayed")
        )
        == "Low blocker"
    )
    assert classify_blocker_severity(BASE_ACTION) == "No blocker"


def test_dependency_count_works():
    action = dict(
        BASE_ACTION,
        governance_signoff_required=True,
        training_followup_required=True,
        client_checkin_required=False,
    )

    assert calculate_dependency_count(action) == 2


def test_dependency_need_classification_works():
    assert (
        classify_dependency_need(
            dict(BASE_ACTION, governance_signoff_required=True)
        )
        == "Governance dependency"
    )
    assert (
        classify_dependency_need(
            dict(BASE_ACTION, training_followup_required=True)
        )
        == "Training dependency"
    )
    assert (
        classify_dependency_need(
            dict(BASE_ACTION, client_checkin_required=True)
        )
        == "Client check-in dependency"
    )
    assert (
        classify_dependency_need(
            dict(
                BASE_ACTION,
                governance_signoff_required=True,
                client_checkin_required=True,
            )
        )
        == "Multiple dependencies"
    )
    assert classify_dependency_need(BASE_ACTION) == "No major dependency"


def test_delivery_risk_classification_works():
    critical_blocker = dict(
        BASE_ACTION,
        status="Blocked",
        priority="Critical",
    )
    multiple_high_dependencies = dict(
        BASE_ACTION,
        priority="High",
        governance_signoff_required=True,
        client_checkin_required=True,
    )
    moderate_dependency = dict(
        BASE_ACTION,
        training_followup_required=True,
    )

    assert (
        classify_delivery_risk_level(critical_blocker)
        == "High delivery risk"
    )
    assert (
        classify_delivery_risk_level(multiple_high_dependencies)
        == "High delivery risk"
    )
    assert (
        classify_delivery_risk_level(moderate_dependency)
        == "Moderate delivery risk"
    )
    assert classify_delivery_risk_level(BASE_ACTION) == "Low delivery risk"


def test_escalation_detection_works():
    high_blocker = dict(
        BASE_ACTION,
        status="Blocked",
        due_in_days=20,
    )
    high_risk = dict(
        BASE_ACTION,
        priority="High",
        governance_signoff_required=True,
        client_checkin_required=True,
    )

    assert requires_escalation(high_blocker) is True
    assert requires_escalation(high_risk) is True
    assert requires_escalation(BASE_ACTION) is False


def test_summary_has_expected_keys():
    summary = build_blocker_review_summary(BASE_ACTION)
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
        "blocker",
        "has_blocker",
        "blocker_type",
        "blocker_severity",
        "dependency_need",
        "dependency_count",
        "delivery_risk_level",
        "requires_escalation",
        "governance_signoff_required",
        "training_followup_required",
        "client_checkin_required",
    }

    assert summary.keys() == expected_keys


def test_all_summaries_match_input_length():
    actions = get_synthetic_implementation_actions()

    summaries = build_all_blocker_review_summaries(actions)

    assert len(summaries) == len(actions)


def test_organisation_summary_groups_correctly():
    actions = get_synthetic_implementation_actions()

    summaries = summarise_blockers_by_organisation(actions)
    summary_by_id = {
        summary["organisation_id"]: summary for summary in summaries
    }

    assert len(summaries) == 3
    assert summary_by_id["ORG001"]["total_actions"] == 5
    assert summary_by_id["ORG002"]["total_actions"] == 5
    assert summary_by_id["ORG003"]["total_actions"] == 5
    assert summary_by_id["ORG001"]["governance_dependency_count"] == 1


def test_related_build_summary_groups_correctly():
    actions = get_synthetic_implementation_actions()

    summaries = summarise_blockers_by_related_build(actions)
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
    assert summary_by_build["Build 6"]["total_actions"] == 3
    assert summary_by_build["Build 6"]["governance_dependency_count"] == 3


def test_prioritisation_puts_escalation_items_first():
    actions = [
        dict(BASE_ACTION, action_id="NORMAL", due_in_days=1),
        dict(
            BASE_ACTION,
            action_id="ESCALATE",
            status="Blocked",
            priority="Critical",
            due_in_days=20,
        ),
    ]

    prioritised = prioritise_blockers_for_resolution(actions)

    assert prioritised[0]["action_id"] == "ESCALATE"
    assert prioritised[0]["requires_escalation"] is True


def test_recommendation_generation_works():
    expected_starts = {
        "Governance blocker": "Escalate governance approval",
        "Training blocker": "Resolve the training gap",
        "Client decision blocker": "Use the next client check-in",
        "Quality blocker": "Clarify quality criteria",
        "Ownership blocker": "Confirm ownership",
        "General delivery blocker": "Review the blocker",
        "No blocker": "No blocker-specific action required",
    }

    for blocker_type, expected_start in expected_starts.items():
        recommendation = generate_blocker_resolution_recommendation(
            {"blocker_type": blocker_type}
        )
        assert recommendation.startswith(expected_start)


def test_recommendations_are_added_without_mutation():
    summaries = [build_blocker_review_summary(BASE_ACTION)]
    original = dict(summaries[0])

    enriched = add_blocker_recommendations(summaries)

    assert summaries[0] == original
    assert "blocker_recommendation" not in summaries[0]
    assert "blocker_recommendation" in enriched[0]
    assert enriched[0] is not summaries[0]


def test_all_synthetic_implementation_actions_process_without_errors():
    actions = get_synthetic_implementation_actions()

    summaries = build_all_blocker_review_summaries(actions)
    prioritised = prioritise_blockers_for_resolution(actions)
    organisation_summaries = summarise_blockers_by_organisation(actions)
    build_summaries = summarise_blockers_by_related_build(actions)
    enriched = add_blocker_recommendations(prioritised)

    assert len(summaries) == 15
    assert len(prioritised) == 15
    assert len(enriched) == 15
    assert len(organisation_summaries) == 3
    assert len(build_summaries) == 5
    assert all(summary["dependency_count"] >= 0 for summary in summaries)
