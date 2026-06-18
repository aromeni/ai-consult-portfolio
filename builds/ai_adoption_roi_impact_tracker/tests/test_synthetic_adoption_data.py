"""Tests for Build 7 synthetic adoption data."""

from data.synthetic_adoption_data import (
    get_synthetic_adoption_metrics,
    get_synthetic_organisations,
    get_synthetic_review_decisions,
)
from logic.adoption_metrics import validate_adoption_record


def test_get_synthetic_organisations_returns_at_least_three_organisations():
    organisations = get_synthetic_organisations()

    assert len(organisations) >= 3


def test_organisation_ids_are_unique():
    organisations = get_synthetic_organisations()
    organisation_ids = [organisation["organisation_id"] for organisation in organisations]

    assert len(organisation_ids) == len(set(organisation_ids))


def test_get_synthetic_adoption_metrics_returns_at_least_twelve_records():
    records = get_synthetic_adoption_metrics()

    assert len(records) >= 12


def test_workflow_ids_are_unique():
    records = get_synthetic_adoption_metrics()
    workflow_ids = [record["workflow_id"] for record in records]

    assert len(workflow_ids) == len(set(workflow_ids))


def test_all_synthetic_records_pass_validation():
    records = get_synthetic_adoption_metrics()

    for record in records:
        assert validate_adoption_record(record) == []


def test_get_synthetic_review_decisions_returns_at_least_six_decisions():
    decisions = get_synthetic_review_decisions()

    assert len(decisions) >= 6


def test_every_review_decision_has_organisation_id_and_workflow_id():
    decisions = get_synthetic_review_decisions()

    for decision in decisions:
        assert decision["organisation_id"]
        assert decision["workflow_id"]
