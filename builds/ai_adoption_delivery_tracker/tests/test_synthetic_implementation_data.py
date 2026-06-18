"""Tests for the Build 8 synthetic implementation data."""

from data.synthetic_implementation_data import (
    get_synthetic_client_checkins,
    get_synthetic_delivery_organisations,
    get_synthetic_implementation_actions,
)
from logic.implementation_actions import validate_implementation_action


def test_delivery_organisations_returns_at_least_three_organisations():
    organisations = get_synthetic_delivery_organisations()

    assert len(organisations) >= 3


def test_organisation_ids_are_unique():
    organisations = get_synthetic_delivery_organisations()
    organisation_ids = [
        organisation["organisation_id"] for organisation in organisations
    ]

    assert len(organisation_ids) == len(set(organisation_ids))


def test_implementation_actions_returns_at_least_fifteen_actions():
    actions = get_synthetic_implementation_actions()

    assert len(actions) >= 15


def test_action_ids_are_unique():
    actions = get_synthetic_implementation_actions()
    action_ids = [action["action_id"] for action in actions]

    assert len(action_ids) == len(set(action_ids))


def test_all_implementation_actions_pass_validation():
    actions = get_synthetic_implementation_actions()

    for action in actions:
        assert validate_implementation_action(action) == []


def test_action_organisation_ids_match_synthetic_organisations():
    organisations = get_synthetic_delivery_organisations()
    actions = get_synthetic_implementation_actions()
    valid_organisation_ids = {
        organisation["organisation_id"] for organisation in organisations
    }

    assert all(
        action["organisation_id"] in valid_organisation_ids for action in actions
    )


def test_action_followup_flags_are_actual_booleans():
    actions = get_synthetic_implementation_actions()
    boolean_fields = {
        "governance_signoff_required",
        "training_followup_required",
        "client_checkin_required",
    }

    for action in actions:
        assert all(isinstance(action[field], bool) for field in boolean_fields)


def test_client_checkins_returns_at_least_six_checkins():
    checkins = get_synthetic_client_checkins()

    assert len(checkins) >= 6


def test_every_checkin_has_required_link_and_review_fields():
    checkins = get_synthetic_client_checkins()
    required_fields = {
        "organisation_id",
        "checkin_period",
        "summary",
        "next_review_focus",
    }

    for checkin in checkins:
        assert required_fields <= checkin.keys()
        assert all(checkin[field] for field in required_fields)
