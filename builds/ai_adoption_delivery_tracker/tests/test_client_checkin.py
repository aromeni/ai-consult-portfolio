"""Tests for the Build 8 Phase 6 client check-in summary builder."""

from data.synthetic_implementation_data import (
    get_synthetic_client_checkins,
    get_synthetic_delivery_organisations,
    get_synthetic_implementation_actions,
)
from logic.client_checkin import (
    add_checkin_recommendations,
    build_all_client_checkin_summaries,
    build_checkin_progress_snapshot,
    build_client_checkin_markdown,
    build_client_checkin_summary,
    build_next_review_focus,
    classify_checkin_health,
    generate_checkin_recommendation,
    get_actions_for_organisation,
    get_checkins_for_organisation,
    identify_checkin_attention_items,
    identify_client_decision_needs,
)


BASE_ACTION = {
    "action_id": "ACT999",
    "organisation_id": "ORG999",
    "organisation_name": "Synthetic Test Organisation",
    "workflow_id": "WF999",
    "workflow_name": "Synthetic workflow",
    "related_build": "Build 7",
    "action_title": "Complete synthetic delivery action",
    "owner_role": "Delivery Lead",
    "priority": "Medium",
    "status": "In progress",
    "due_in_days": 20,
    "blocker": "",
    "governance_signoff_required": False,
    "training_followup_required": False,
    "client_checkin_required": False,
}

BASE_ORGANISATION = {
    "organisation_id": "ORG999",
    "organisation_name": "Synthetic Test Organisation",
    "sector": "Synthetic services",
    "implementation_stage": "Controlled pilot",
}

BASE_CHECKIN = {
    "checkin_id": "CHK999",
    "organisation_id": "ORG999",
    "checkin_period": "Week 4",
    "checkin_focus": "Delivery review",
    "summary": "Synthetic delivery progress was reviewed.",
    "next_review_focus": "Confirm the next implementation action.",
}


def test_organisation_action_filtering_works():
    actions = [
        BASE_ACTION,
        dict(BASE_ACTION, action_id="OTHER", organisation_id="ORG888"),
    ]

    filtered = get_actions_for_organisation(actions, "ORG999")

    assert len(filtered) == 1
    assert filtered[0]["action_id"] == "ACT999"


def test_organisation_checkin_filtering_works():
    checkins = [
        BASE_CHECKIN,
        dict(BASE_CHECKIN, checkin_id="OTHER", organisation_id="ORG888"),
    ]

    filtered = get_checkins_for_organisation(checkins, "ORG999")

    assert len(filtered) == 1
    assert filtered[0]["checkin_id"] == "CHK999"


def test_progress_snapshot_returns_expected_keys():
    actions = [
        BASE_ACTION,
        dict(BASE_ACTION, action_id="DONE", status="Completed", priority="High"),
        dict(BASE_ACTION, action_id="BLOCKED", status="Blocked"),
    ]

    snapshot = build_checkin_progress_snapshot(actions)

    assert snapshot.keys() == {
        "total_actions",
        "completed_count",
        "in_progress_count",
        "not_started_count",
        "blocked_count",
        "deferred_count",
        "critical_or_high_priority_count",
    }
    assert snapshot["total_actions"] == 3
    assert snapshot["completed_count"] == 1
    assert snapshot["blocked_count"] == 1


def test_attention_item_identification_works():
    actions = [
        BASE_ACTION,
        dict(
            BASE_ACTION,
            action_id="BLOCKED",
            status="Blocked",
            priority="Low",
        ),
        dict(
            BASE_ACTION,
            action_id="CRITICAL",
            priority="Critical",
            due_in_days=10,
        ),
    ]

    attention_items = identify_checkin_attention_items(actions)

    assert [item["action_id"] for item in attention_items] == [
        "BLOCKED",
        "CRITICAL",
    ]


def test_checkin_health_classification_works():
    assert (
        classify_checkin_health(
            [
                dict(
                    BASE_ACTION,
                    status="Blocked",
                    priority="Critical",
                )
            ]
        )
        == "Blocked"
    )
    assert (
        classify_checkin_health(
            [dict(BASE_ACTION, status="Blocked", priority="High")]
        )
        == "At risk"
    )
    assert (
        classify_checkin_health(
            [
                dict(
                    BASE_ACTION,
                    client_checkin_required=True,
                    status="In progress",
                )
            ]
        )
        == "Needs attention"
    )
    assert (
        classify_checkin_health(
            [dict(BASE_ACTION, status="Completed")]
        )
        == "On track"
    )


def test_client_decision_needs_are_generated():
    actions = [
        dict(
            BASE_ACTION,
            status="Blocked",
            governance_signoff_required=True,
            client_checkin_required=True,
            training_followup_required=True,
        )
    ]

    decisions = identify_client_decision_needs(actions)

    assert len(decisions) == 4
    assert any("governance sign-off" in decision for decision in decisions)
    assert any("unblock" in decision for decision in decisions)
    assert any("client direction" in decision for decision in decisions)
    assert any("training follow-up" in decision for decision in decisions)


def test_next_review_focus_is_generated():
    focus = build_next_review_focus(
        [
            dict(
                BASE_ACTION,
                status="Blocked",
                priority="High",
            )
        ]
    )

    assert focus.startswith("Resolve blocked Critical or High-priority")


def test_client_checkin_summary_has_expected_keys():
    summary = build_client_checkin_summary(
        BASE_ORGANISATION,
        [BASE_ACTION],
        [BASE_CHECKIN],
    )
    expected_keys = {
        "organisation_id",
        "organisation_name",
        "sector",
        "implementation_stage",
        "checkin_health",
        "progress_snapshot",
        "attention_item_count",
        "client_decision_needs",
        "latest_checkin_period",
        "latest_checkin_focus",
        "latest_checkin_summary",
        "next_review_focus",
    }

    assert summary.keys() == expected_keys
    assert summary["latest_checkin_period"] == "Week 4"


def test_all_organisation_summaries_match_organisation_count():
    organisations = get_synthetic_delivery_organisations()
    actions = get_synthetic_implementation_actions()
    checkins = get_synthetic_client_checkins()

    summaries = build_all_client_checkin_summaries(
        organisations,
        actions,
        checkins,
    )

    assert len(summaries) == len(organisations)


def test_markdown_checkin_summary_contains_expected_headings():
    summary = build_client_checkin_summary(
        BASE_ORGANISATION,
        [BASE_ACTION],
        [BASE_CHECKIN],
    )
    attention_items = identify_checkin_attention_items([BASE_ACTION])

    markdown = build_client_checkin_markdown(summary, attention_items)

    assert "# Client Check-in Summary" in markdown
    assert "## Current Health" in markdown
    assert "## Progress Snapshot" in markdown
    assert "## Key Attention Items" in markdown
    assert "## Client Decisions Needed" in markdown
    assert "## Next Review Focus" in markdown


def test_recommendation_generation_works():
    expected_starts = {
        "Blocked": "Use the next check-in to unblock delivery",
        "At risk": "Focus the next check-in on reducing delivery risk",
        "Needs attention": "Use the next check-in to confirm decisions",
        "On track": "Use the next check-in to confirm progress evidence",
    }

    for health, expected_start in expected_starts.items():
        assert generate_checkin_recommendation(
            {"checkin_health": health}
        ).startswith(expected_start)


def test_recommendations_are_added_without_mutation():
    summaries = [
        build_client_checkin_summary(
            BASE_ORGANISATION,
            [BASE_ACTION],
            [BASE_CHECKIN],
        )
    ]
    original = dict(summaries[0])

    enriched = add_checkin_recommendations(summaries)

    assert summaries[0] == original
    assert "checkin_recommendation" not in summaries[0]
    assert "checkin_recommendation" in enriched[0]
    assert enriched[0] is not summaries[0]


def test_all_synthetic_data_processes_without_errors():
    organisations = get_synthetic_delivery_organisations()
    actions = get_synthetic_implementation_actions()
    checkins = get_synthetic_client_checkins()

    summaries = build_all_client_checkin_summaries(
        organisations,
        actions,
        checkins,
    )
    enriched = add_checkin_recommendations(summaries)

    assert len(summaries) == 3
    assert len(enriched) == 3
    assert all(summary["progress_snapshot"]["total_actions"] == 5 for summary in summaries)
    assert all(summary["latest_checkin_period"] == "Week 4" for summary in summaries)
    assert all(
        summary["checkin_health"]
        in {"On track", "Needs attention", "At risk", "Blocked"}
        for summary in summaries
    )
