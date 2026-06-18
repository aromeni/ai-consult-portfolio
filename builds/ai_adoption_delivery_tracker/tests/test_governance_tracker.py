"""Tests for the Build 8 Phase 4 governance tracker."""

from data.synthetic_implementation_data import (
    get_synthetic_implementation_actions,
)
from logic.governance_tracker import (
    add_governance_recommendations,
    build_all_governance_summaries,
    build_governance_summary,
    classify_control_area,
    classify_control_readiness,
    classify_governance_delivery_risk,
    classify_signoff_urgency,
    generate_governance_recommendation,
    identify_governance_owner_need,
    prioritise_governance_actions,
    requires_governance_signoff,
    summarise_governance_by_organisation,
    summarise_governance_by_related_build,
)


BASE_ACTION = {
    "action_id": "ACT999",
    "organisation_id": "ORG999",
    "organisation_name": "Synthetic Test Organisation",
    "workflow_id": "WF999",
    "workflow_name": "Synthetic workflow",
    "related_build": "Build 7",
    "action_title": "Complete synthetic delivery action",
    "action_description": "Complete a fictional implementation task.",
    "owner_role": "Delivery Lead",
    "priority": "Medium",
    "status": "In progress",
    "due_in_days": 20,
    "blocker": "",
    "governance_signoff_required": False,
}


def test_governance_signoff_detection_works():
    assert (
        requires_governance_signoff(
            dict(BASE_ACTION, governance_signoff_required=True)
        )
        is True
    )
    assert requires_governance_signoff(BASE_ACTION) is False


def test_signoff_urgency_classification_works():
    assert (
        classify_signoff_urgency(
            dict(
                BASE_ACTION,
                governance_signoff_required=True,
                due_in_days=7,
            )
        )
        == "Urgent sign-off"
    )
    assert (
        classify_signoff_urgency(
            dict(
                BASE_ACTION,
                governance_signoff_required=True,
                due_in_days=14,
            )
        )
        == "Sign-off due soon"
    )
    assert (
        classify_signoff_urgency(
            dict(
                BASE_ACTION,
                governance_signoff_required=True,
                due_in_days=15,
            )
        )
        == "Routine sign-off"
    )
    assert classify_signoff_urgency(BASE_ACTION) == "No sign-off required"


def test_control_area_classification_works():
    cases = [
        ("Review the responsible AI policy", "Policy control"),
        ("Secure formal authorisation", "Approval control"),
        ("Agree the output quality standard", "Quality control"),
        ("Assess the incident escalation route", "Risk control"),
        ("Confirm confidential data boundaries", "Data control"),
    ]

    for description, expected in cases:
        action = dict(BASE_ACTION, action_description=description)
        assert classify_control_area(action) == expected

    assert (
        classify_control_area(
            dict(
                BASE_ACTION,
                governance_signoff_required=True,
                action_title="Confirm delivery arrangement",
            )
        )
        == "General control"
    )
    assert classify_control_area(BASE_ACTION) == "No governance control"


def test_control_readiness_classification_works():
    assert (
        classify_control_readiness(
            dict(
                BASE_ACTION,
                governance_signoff_required=True,
                status="Blocked",
            )
        )
        == "Control blocked"
    )
    assert (
        classify_control_readiness(
            dict(BASE_ACTION, governance_signoff_required=True)
        )
        == "Control needs review"
    )
    assert classify_control_readiness(BASE_ACTION) == "Control ready"
    assert (
        classify_control_readiness(
            dict(BASE_ACTION, status="Deferred")
        )
        == "No control required"
    )


def test_governance_owner_need_classification_works():
    assert (
        identify_governance_owner_need(
            dict(
                BASE_ACTION,
                priority="Critical",
                governance_signoff_required=True,
            )
        )
        == "Senior approval needed"
    )
    assert (
        identify_governance_owner_need(
            dict(BASE_ACTION, governance_signoff_required=True)
        )
        == "Governance lead review needed"
    )
    assert (
        identify_governance_owner_need(BASE_ACTION)
        == "Operational owner can proceed"
    )
    assert (
        identify_governance_owner_need(
            dict(BASE_ACTION, status="Completed")
        )
        == "No governance owner needed"
    )


def test_governance_delivery_risk_classification_works():
    assert (
        classify_governance_delivery_risk(
            dict(
                BASE_ACTION,
                governance_signoff_required=True,
                status="Blocked",
            )
        )
        == "High governance delivery risk"
    )
    assert (
        classify_governance_delivery_risk(
            dict(
                BASE_ACTION,
                governance_signoff_required=True,
                priority="High",
                due_in_days=7,
            )
        )
        == "High governance delivery risk"
    )
    assert (
        classify_governance_delivery_risk(
            dict(BASE_ACTION, governance_signoff_required=True)
        )
        == "Moderate governance delivery risk"
    )
    assert (
        classify_governance_delivery_risk(BASE_ACTION)
        == "Low governance delivery risk"
    )


def test_summary_has_expected_keys():
    summary = build_governance_summary(BASE_ACTION)
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
        "governance_signoff_required",
        "signoff_urgency",
        "control_area",
        "control_readiness",
        "governance_owner_need",
        "governance_delivery_risk",
        "blocker",
    }

    assert summary.keys() == expected_keys


def test_all_summaries_match_input_length():
    actions = get_synthetic_implementation_actions()

    summaries = build_all_governance_summaries(actions)

    assert len(summaries) == len(actions)


def test_organisation_summary_groups_correctly():
    actions = get_synthetic_implementation_actions()

    summaries = summarise_governance_by_organisation(actions)
    summary_by_id = {
        summary["organisation_id"]: summary for summary in summaries
    }

    assert len(summaries) == 3
    assert summary_by_id["ORG001"]["total_actions"] == 5
    assert summary_by_id["ORG002"]["signoff_required_count"] == 3
    assert summary_by_id["ORG003"]["signoff_required_count"] == 1


def test_related_build_summary_groups_correctly():
    actions = get_synthetic_implementation_actions()

    summaries = summarise_governance_by_related_build(actions)
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
    assert summary_by_build["Build 6"]["signoff_required_count"] == 3
    assert summary_by_build["Build 4"]["signoff_required_count"] == 0


def test_prioritisation_puts_high_risk_governance_items_first():
    actions = [
        dict(BASE_ACTION, action_id="LOW", due_in_days=1),
        dict(
            BASE_ACTION,
            action_id="HIGH",
            priority="Critical",
            status="Blocked",
            due_in_days=20,
            governance_signoff_required=True,
        ),
    ]

    prioritised = prioritise_governance_actions(actions)

    assert prioritised[0]["action_id"] == "HIGH"
    assert (
        prioritised[0]["governance_delivery_risk"]
        == "High governance delivery risk"
    )


def test_recommendation_generation_works():
    summaries = [
        (
            {
                "governance_delivery_risk": "High governance delivery risk",
                "signoff_urgency": "Routine sign-off",
                "control_readiness": "Control needs review",
                "governance_signoff_required": True,
            },
            "Escalate governance review",
        ),
        (
            {
                "governance_delivery_risk": "Moderate governance delivery risk",
                "signoff_urgency": "Urgent sign-off",
                "control_readiness": "Control needs review",
                "governance_signoff_required": True,
            },
            "Secure sign-off",
        ),
        (
            {
                "governance_delivery_risk": "Moderate governance delivery risk",
                "signoff_urgency": "Routine sign-off",
                "control_readiness": "Control blocked",
                "governance_signoff_required": True,
            },
            "Resolve the governance blocker",
        ),
        (
            {
                "governance_delivery_risk": "Moderate governance delivery risk",
                "signoff_urgency": "Routine sign-off",
                "control_readiness": "Control needs review",
                "governance_signoff_required": True,
            },
            "Review the relevant control",
        ),
        (
            {
                "governance_delivery_risk": "Low governance delivery risk",
                "signoff_urgency": "No sign-off required",
                "control_readiness": "Control ready",
                "governance_signoff_required": False,
            },
            "No governance sign-off",
        ),
    ]

    for summary, expected_start in summaries:
        assert generate_governance_recommendation(summary).startswith(
            expected_start
        )


def test_recommendations_are_added_without_mutation():
    summaries = [build_governance_summary(BASE_ACTION)]
    original = dict(summaries[0])

    enriched = add_governance_recommendations(summaries)

    assert summaries[0] == original
    assert "governance_recommendation" not in summaries[0]
    assert "governance_recommendation" in enriched[0]
    assert enriched[0] is not summaries[0]


def test_all_synthetic_implementation_actions_process_without_errors():
    actions = get_synthetic_implementation_actions()

    summaries = build_all_governance_summaries(actions)
    prioritised = prioritise_governance_actions(actions)
    organisation_summaries = summarise_governance_by_organisation(actions)
    build_summaries = summarise_governance_by_related_build(actions)
    enriched = add_governance_recommendations(prioritised)

    assert len(summaries) == 15
    assert len(prioritised) == 15
    assert len(enriched) == 15
    assert len(organisation_summaries) == 3
    assert len(build_summaries) == 5
    assert all(
        summary["governance_delivery_risk"]
        in {
            "High governance delivery risk",
            "Moderate governance delivery risk",
            "Low governance delivery risk",
        }
        for summary in summaries
    )
