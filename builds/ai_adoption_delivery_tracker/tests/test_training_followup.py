"""Tests for the Build 8 Phase 5 training follow-up engine."""

from data.synthetic_implementation_data import (
    get_synthetic_implementation_actions,
)
from logic.training_followup import (
    add_training_followup_recommendations,
    build_all_training_followup_summaries,
    build_training_followup_summary,
    classify_training_delivery_risk,
    classify_training_followup_urgency,
    classify_training_support_intensity,
    classify_training_support_type,
    generate_training_followup_recommendation,
    identify_training_delivery_need,
    prioritise_training_followup_actions,
    requires_training_followup,
    summarise_training_followup_by_organisation,
    summarise_training_followup_by_owner_role,
    summarise_training_followup_by_related_build,
)


BASE_ACTION = {
    "action_id": "ACT999",
    "organisation_id": "ORG999",
    "organisation_name": "Synthetic Test Organisation",
    "workflow_id": "WF999",
    "workflow_name": "Synthetic workflow",
    "related_build": "Build 4",
    "action_title": "Complete synthetic implementation action",
    "action_description": "Complete a fictional delivery activity.",
    "owner_role": "Training Lead",
    "priority": "Medium",
    "status": "In progress",
    "due_in_days": 20,
    "blocker": "",
    "training_followup_required": False,
}


def test_training_followup_detection_works():
    assert (
        requires_training_followup(
            dict(BASE_ACTION, training_followup_required=True)
        )
        is True
    )
    assert requires_training_followup(BASE_ACTION) is False


def test_training_followup_urgency_classification_works():
    assert (
        classify_training_followup_urgency(
            dict(
                BASE_ACTION,
                training_followup_required=True,
                due_in_days=7,
            )
        )
        == "Urgent training follow-up"
    )
    assert (
        classify_training_followup_urgency(
            dict(
                BASE_ACTION,
                training_followup_required=True,
                due_in_days=14,
            )
        )
        == "Training follow-up due soon"
    )
    assert (
        classify_training_followup_urgency(
            dict(
                BASE_ACTION,
                training_followup_required=True,
                due_in_days=15,
            )
        )
        == "Routine training follow-up"
    )
    assert (
        classify_training_followup_urgency(BASE_ACTION)
        == "No training follow-up required"
    )


def test_training_support_type_classification_works():
    cases = [
        ("Build confidence with safe prompting", "Foundation AI training"),
        ("Demonstrate the workflow template", "Workflow-specific coaching"),
        ("Agree a quality review standard", "Quality review training"),
        ("Explain responsible AI policy", "Responsible AI guidance"),
        ("Provide a coaching demonstration", "Practical coaching"),
    ]

    for description, expected in cases:
        action = dict(BASE_ACTION, action_description=description)
        assert classify_training_support_type(action) == expected

    assert (
        classify_training_support_type(
            dict(
                BASE_ACTION,
                training_followup_required=True,
                action_title="Discuss delivery questions",
            )
        )
        == "General support"
    )
    assert (
        classify_training_support_type(BASE_ACTION) == "No training support"
    )


def test_training_support_intensity_classification_works():
    assert (
        classify_training_support_intensity(
            dict(
                BASE_ACTION,
                training_followup_required=True,
                status="Blocked",
            )
        )
        == "High support"
    )
    assert (
        classify_training_support_intensity(
            dict(
                BASE_ACTION,
                training_followup_required=True,
                due_in_days=14,
            )
        )
        == "Moderate support"
    )
    assert (
        classify_training_support_intensity(
            dict(
                BASE_ACTION,
                training_followup_required=True,
                due_in_days=30,
            )
        )
        == "Light support"
    )
    assert (
        classify_training_support_intensity(BASE_ACTION)
        == "No support required"
    )


def test_training_delivery_need_classification_works():
    assert (
        identify_training_delivery_need(
            dict(
                BASE_ACTION,
                training_followup_required=True,
                status="Blocked",
            )
        )
        == "Immediate coaching session"
    )
    assert (
        identify_training_delivery_need(
            dict(
                BASE_ACTION,
                training_followup_required=True,
                action_description="Demonstrate the workflow template",
            )
        )
        == "Practical workflow demonstration"
    )
    assert (
        identify_training_delivery_need(
            dict(
                BASE_ACTION,
                training_followup_required=True,
                action_description="Practise the quality standard",
            )
        )
        == "Quality review practice"
    )
    assert (
        identify_training_delivery_need(
            dict(
                BASE_ACTION,
                training_followup_required=True,
                action_description="Explain responsible AI policy",
            )
        )
        == "Responsible-use refresher"
    )
    assert (
        identify_training_delivery_need(
            dict(
                BASE_ACTION,
                training_followup_required=True,
                action_title="Discuss delivery questions",
            )
        )
        == "Peer support or office hours"
    )
    assert (
        identify_training_delivery_need(BASE_ACTION)
        == "No training delivery needed"
    )


def test_training_delivery_risk_classification_works():
    assert (
        classify_training_delivery_risk(
            dict(
                BASE_ACTION,
                training_followup_required=True,
                status="Blocked",
            )
        )
        == "High training delivery risk"
    )
    assert (
        classify_training_delivery_risk(
            dict(
                BASE_ACTION,
                training_followup_required=True,
                due_in_days=14,
            )
        )
        == "Moderate training delivery risk"
    )
    assert (
        classify_training_delivery_risk(BASE_ACTION)
        == "Low training delivery risk"
    )


def test_summary_has_expected_keys():
    summary = build_training_followup_summary(BASE_ACTION)
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
        "training_followup_required",
        "training_followup_urgency",
        "training_support_type",
        "training_support_intensity",
        "training_delivery_need",
        "training_delivery_risk",
        "blocker",
    }

    assert summary.keys() == expected_keys


def test_all_summaries_match_input_length():
    actions = get_synthetic_implementation_actions()

    summaries = build_all_training_followup_summaries(actions)

    assert len(summaries) == len(actions)


def test_organisation_summary_groups_correctly():
    actions = get_synthetic_implementation_actions()

    summaries = summarise_training_followup_by_organisation(actions)
    summary_by_id = {
        summary["organisation_id"]: summary for summary in summaries
    }

    assert len(summaries) == 3
    assert summary_by_id["ORG001"]["training_followup_required_count"] == 3
    assert summary_by_id["ORG002"]["training_followup_required_count"] == 2
    assert summary_by_id["ORG003"]["training_followup_required_count"] == 2


def test_related_build_summary_groups_correctly():
    actions = get_synthetic_implementation_actions()

    summaries = summarise_training_followup_by_related_build(actions)
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
    assert summary_by_build["Build 4"]["training_followup_required_count"] == 4
    assert summary_by_build["Build 6"]["training_followup_required_count"] == 0


def test_owner_role_summary_groups_correctly():
    actions = get_synthetic_implementation_actions()

    summaries = summarise_training_followup_by_owner_role(actions)
    summary_by_owner = {
        summary["owner_role"]: summary for summary in summaries
    }

    assert summary_by_owner["Training Lead"]["total_actions"] == 2
    assert (
        summary_by_owner["Training Lead"]["training_followup_required_count"]
        == 2
    )
    assert summary_by_owner["Practice Manager"]["total_actions"] == 2


def test_prioritisation_puts_high_risk_training_items_first():
    actions = [
        dict(BASE_ACTION, action_id="LOW", due_in_days=1),
        dict(
            BASE_ACTION,
            action_id="HIGH",
            priority="Critical",
            status="Blocked",
            due_in_days=20,
            training_followup_required=True,
        ),
    ]

    prioritised = prioritise_training_followup_actions(actions)

    assert prioritised[0]["action_id"] == "HIGH"
    assert (
        prioritised[0]["training_delivery_risk"]
        == "High training delivery risk"
    )


def test_recommendation_generation_works():
    expected_starts = {
        "Immediate coaching session": "Book an immediate coaching session",
        "Practical workflow demonstration": "Run a practical workflow demonstration",
        "Quality review practice": "Provide quality review practice",
        "Responsible-use refresher": "Run a short responsible-use refresher",
        "Peer support or office hours": "Use peer support or office hours",
        "No training delivery needed": "No specific training follow-up",
    }

    for delivery_need, expected_start in expected_starts.items():
        recommendation = generate_training_followup_recommendation(
            {"training_delivery_need": delivery_need}
        )
        assert recommendation.startswith(expected_start)


def test_recommendations_are_added_without_mutation():
    summaries = [build_training_followup_summary(BASE_ACTION)]
    original = dict(summaries[0])

    enriched = add_training_followup_recommendations(summaries)

    assert summaries[0] == original
    assert "training_followup_recommendation" not in summaries[0]
    assert "training_followup_recommendation" in enriched[0]
    assert enriched[0] is not summaries[0]


def test_all_synthetic_implementation_actions_process_without_errors():
    actions = get_synthetic_implementation_actions()

    summaries = build_all_training_followup_summaries(actions)
    prioritised = prioritise_training_followup_actions(actions)
    organisation_summaries = summarise_training_followup_by_organisation(
        actions
    )
    build_summaries = summarise_training_followup_by_related_build(actions)
    owner_summaries = summarise_training_followup_by_owner_role(actions)
    enriched = add_training_followup_recommendations(prioritised)

    assert len(summaries) == 15
    assert len(prioritised) == 15
    assert len(enriched) == 15
    assert len(organisation_summaries) == 3
    assert len(build_summaries) == 5
    assert len(owner_summaries) > 0
    assert all(
        summary["training_delivery_risk"]
        in {
            "High training delivery risk",
            "Moderate training delivery risk",
            "Low training delivery risk",
        }
        for summary in summaries
    )
