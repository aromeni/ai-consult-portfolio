"""Tests for Build 7 Phase 6 — Decision Tracker and Client Follow-up Evidence.

All test records are deterministic synthetic fixtures. No real client data.
"""

from data.synthetic_adoption_data import get_synthetic_adoption_metrics
from logic.decision_tracker import (
    add_follow_up_evidence_notes,
    build_all_decision_summaries,
    build_decision_summary,
    classify_decision_confidence,
    classify_decision_outcome,
    generate_follow_up_evidence_note,
    identify_decision_reason,
    identify_next_action,
    prioritise_decisions_for_follow_up,
    summarise_decisions_by_organisation,
    summarise_decisions_by_related_build,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

# WF001 — Continue, In progress, quality=2, near_misses=1 (not >1), incidents=0
CONTINUE_RECORD = {
    "organisation_id": "ORG001",
    "organisation_name": "BrightPath Skills Training",
    "workflow_id": "WF001",
    "workflow_name": "Lesson plan drafting",
    "related_build": "Build 4",
    "staff_group": "Tutors",
    "confidence_before": 2.4,
    "confidence_after": 3.7,
    "training_completion_rate": 0.75,
    "pilot_status": "In progress",
    "quality_issues_logged": 2,
    "risk_incidents_logged": 0,
    "near_misses_logged": 1,
    "adoption_status": "Continue",
    "review_decision": "Continue with stronger review checklist",
    "evidence_note": "Tutors report faster first drafts but still need human review.",
}

# WF002 — Scale adoption but confidence_after=3.4 falls below 3.5 threshold → Review later
REVIEW_LATER_RECORD = {
    "organisation_id": "ORG001",
    "organisation_name": "BrightPath Skills Training",
    "workflow_id": "WF002",
    "workflow_name": "Staff AI confidence check-in",
    "related_build": "Build 4",
    "staff_group": "Tutors and administrators",
    "confidence_before": 2.0,
    "confidence_after": 3.4,
    "training_completion_rate": 0.88,
    "pilot_status": "Completed",
    "quality_issues_logged": 1,
    "risk_incidents_logged": 0,
    "near_misses_logged": 0,
    "adoption_status": "Scale",
    "review_decision": "Scale the check-in template across all weekly team reviews",
    "evidence_note": "Staff are more confident naming safe and unsafe AI uses.",
}

# WF004 — Paused pilot, quality=3, incidents=1, near_misses=2 → Pause
PAUSE_RECORD = {
    "organisation_id": "ORG001",
    "organisation_name": "BrightPath Skills Training",
    "workflow_id": "WF004",
    "workflow_name": "Governance policy checklist review",
    "related_build": "Build 6",
    "staff_group": "Quality lead",
    "confidence_before": 2.1,
    "confidence_after": 3.2,
    "training_completion_rate": 0.80,
    "pilot_status": "Paused",
    "quality_issues_logged": 3,
    "risk_incidents_logged": 1,
    "near_misses_logged": 2,
    "adoption_status": "Review",
    "review_decision": "Review governance evidence before widening use",
    "evidence_note": "The checklist saved time, but reviewers want clearer escalation wording.",
}

# WF006 — incidents=1, quality=4, near_misses=2 → Continue with controls
CONTINUE_WITH_CONTROLS_RECORD = {
    "organisation_id": "ORG002",
    "organisation_name": "Northside Community Advice",
    "workflow_id": "WF006",
    "workflow_name": "Draft service improvement report",
    "related_build": "Build 5",
    "staff_group": "Service managers",
    "confidence_before": 2.3,
    "confidence_after": 3.0,
    "training_completion_rate": 0.60,
    "pilot_status": "In progress",
    "quality_issues_logged": 4,
    "risk_incidents_logged": 1,
    "near_misses_logged": 2,
    "adoption_status": "Review",
    "review_decision": "Review wording controls before producing further report drafts",
    "evidence_note": "Draft reports are faster, but sensitive-case boundary checks need tightening.",
}

# WF008 — adoption_status=Stop, pilot_status=Paused → Stop (Stop takes priority over Pause)
STOP_RECORD = {
    "organisation_id": "ORG002",
    "organisation_name": "Northside Community Advice",
    "workflow_id": "WF008",
    "workflow_name": "AI acceptable use policy review",
    "related_build": "Build 6",
    "staff_group": "Governance trustee",
    "confidence_before": 2.0,
    "confidence_after": 2.8,
    "training_completion_rate": 0.55,
    "pilot_status": "Paused",
    "quality_issues_logged": 2,
    "risk_incidents_logged": 1,
    "near_misses_logged": 1,
    "adoption_status": "Stop",
    "review_decision": "Stop this workflow until advice-sector boundaries are approved",
    "evidence_note": "The review found unclear boundaries around advice-specific client information.",
}

# WF009 — Scale, training=0.83, confidence_after=3.9, incidents=0 → Scale with monitoring
SCALE_WITH_MONITORING_RECORD = {
    "organisation_id": "ORG003",
    "organisation_name": "Greenacre Dental Group",
    "workflow_id": "WF009",
    "workflow_name": "Appointment admin workflow audit",
    "related_build": "Build 1",
    "staff_group": "Reception team",
    "confidence_before": 2.7,
    "confidence_after": 3.9,
    "training_completion_rate": 0.83,
    "pilot_status": "Completed",
    "quality_issues_logged": 1,
    "risk_incidents_logged": 0,
    "near_misses_logged": 0,
    "adoption_status": "Scale",
    "review_decision": "Scale the workflow audit template to other admin processes",
    "evidence_note": "Reception staff identified repeatable admin bottlenecks more quickly.",
}

# Custom fixture — all Scale thresholds met (training>=0.9, confidence>=4.0, no issues) → Scale
SCALE_RECORD = {
    "organisation_id": "ORG_TEST",
    "organisation_name": "Greenacre Dental Group",
    "workflow_id": "WF_SCALE",
    "workflow_name": "Clinical admin boundary training — extended",
    "related_build": "Build 4",
    "staff_group": "All clinical admin",
    "confidence_before": 2.5,
    "confidence_after": 4.1,
    "training_completion_rate": 0.95,
    "pilot_status": "Completed",
    "quality_issues_logged": 0,
    "risk_incidents_logged": 0,
    "near_misses_logged": 0,
    "adoption_status": "Scale",
    "review_decision": "Scale across all sites",
    "evidence_note": "All adoption indicators are strong across both sites.",
}

EXPECTED_DECISION_SUMMARY_FIELDS = {
    "organisation_id",
    "organisation_name",
    "workflow_id",
    "workflow_name",
    "related_build",
    "staff_group",
    "decision_outcome",
    "decision_confidence",
    "decision_reason",
    "next_action",
    "adoption_status",
    "pilot_status",
    "training_completion_rate",
    "confidence_after",
    "quality_issues_logged",
    "risk_incidents_logged",
    "near_misses_logged",
    "review_decision",
    "evidence_note",
}


# ---------------------------------------------------------------------------
# 1. Decision outcome — Stop
# ---------------------------------------------------------------------------


class TestDecisionOutcomeStop:
    def test_stop_when_adoption_status_is_stop(self):
        assert classify_decision_outcome(STOP_RECORD) == "Stop"

    def test_stop_takes_priority_over_paused_pilot(self):
        record = {**STOP_RECORD, "pilot_status": "Paused"}
        assert classify_decision_outcome(record) == "Stop"

    def test_stop_takes_priority_over_continue_with_controls_conditions(self):
        record = {
            **STOP_RECORD,
            "adoption_status": "Stop",
            "risk_incidents_logged": 2,
            "quality_issues_logged": 5,
        }
        assert classify_decision_outcome(record) == "Stop"


# ---------------------------------------------------------------------------
# 2. Decision outcome — Pause
# ---------------------------------------------------------------------------


class TestDecisionOutcomePause:
    def test_pause_when_pilot_is_paused(self):
        assert classify_decision_outcome(PAUSE_RECORD) == "Pause"

    def test_pause_even_when_incidents_present(self):
        record = {**PAUSE_RECORD, "adoption_status": "Review", "risk_incidents_logged": 1}
        assert classify_decision_outcome(record) == "Pause"

    def test_pause_even_when_quality_high(self):
        record = {**PAUSE_RECORD, "adoption_status": "Continue", "quality_issues_logged": 5}
        assert classify_decision_outcome(record) == "Pause"


# ---------------------------------------------------------------------------
# 3. Decision outcome — Continue with controls
# ---------------------------------------------------------------------------


class TestDecisionOutcomeContinueWithControls:
    def test_continue_with_controls_when_incident_logged(self):
        assert classify_decision_outcome(CONTINUE_WITH_CONTROLS_RECORD) == "Continue with controls"

    def test_continue_with_controls_when_near_misses_above_threshold(self):
        record = {
            **CONTINUE_RECORD,
            "near_misses_logged": 2,
            "risk_incidents_logged": 0,
            "quality_issues_logged": 1,
        }
        assert classify_decision_outcome(record) == "Continue with controls"

    def test_continue_with_controls_when_quality_at_threshold(self):
        record = {
            **CONTINUE_RECORD,
            "quality_issues_logged": 3,
            "risk_incidents_logged": 0,
            "near_misses_logged": 0,
        }
        assert classify_decision_outcome(record) == "Continue with controls"

    def test_one_near_miss_does_not_trigger_continue_with_controls(self):
        record = {
            **CONTINUE_RECORD,
            "near_misses_logged": 1,
            "risk_incidents_logged": 0,
            "quality_issues_logged": 2,
        }
        assert classify_decision_outcome(record) == "Continue"


# ---------------------------------------------------------------------------
# 4. Decision outcome — Scale
# ---------------------------------------------------------------------------


class TestDecisionOutcomeScale:
    def test_scale_when_all_high_thresholds_met(self):
        assert classify_decision_outcome(SCALE_RECORD) == "Scale"

    def test_scale_requires_training_above_high_threshold(self):
        record = {**SCALE_RECORD, "training_completion_rate": 0.88}
        assert classify_decision_outcome(record) != "Scale"

    def test_scale_requires_confidence_above_high_threshold(self):
        record = {**SCALE_RECORD, "confidence_after": 3.9}
        assert classify_decision_outcome(record) != "Scale"

    def test_scale_requires_zero_quality_issues(self):
        record = {**SCALE_RECORD, "quality_issues_logged": 1}
        assert classify_decision_outcome(record) != "Scale"


# ---------------------------------------------------------------------------
# 5. Decision outcome — Scale with monitoring
# ---------------------------------------------------------------------------


class TestDecisionOutcomeScaleWithMonitoring:
    def test_scale_with_monitoring_when_moderate_evidence(self):
        assert classify_decision_outcome(SCALE_WITH_MONITORING_RECORD) == "Scale with monitoring"

    def test_scale_with_monitoring_requires_no_incidents(self):
        record = {**SCALE_WITH_MONITORING_RECORD, "risk_incidents_logged": 1}
        assert classify_decision_outcome(record) != "Scale with monitoring"

    def test_scale_with_monitoring_requires_confidence_at_threshold(self):
        record = {**SCALE_WITH_MONITORING_RECORD, "confidence_after": 3.4}
        assert classify_decision_outcome(record) != "Scale with monitoring"


# ---------------------------------------------------------------------------
# 6. Decision outcome — Continue
# ---------------------------------------------------------------------------


class TestDecisionOutcomeContinue:
    def test_continue_when_adoption_status_is_continue(self):
        assert classify_decision_outcome(CONTINUE_RECORD) == "Continue"

    def test_review_later_when_scale_evidence_incomplete(self):
        assert classify_decision_outcome(REVIEW_LATER_RECORD) == "Review later"

    def test_review_later_when_adoption_status_is_review(self):
        record = {
            "adoption_status": "Review",
            "pilot_status": "In progress",
            "quality_issues_logged": 0,
            "risk_incidents_logged": 0,
            "near_misses_logged": 0,
            "training_completion_rate": 0.60,
            "confidence_after": 3.2,
        }
        assert classify_decision_outcome(record) == "Review later"


# ---------------------------------------------------------------------------
# 7. Decision confidence classification
# ---------------------------------------------------------------------------


class TestClassifyDecisionConfidence:
    def test_high_confidence_when_all_thresholds_met(self):
        assert classify_decision_confidence(CONTINUE_RECORD) == "High confidence decision"

    def test_high_confidence_requires_pilot_status_active_or_complete(self):
        record = {**SCALE_WITH_MONITORING_RECORD}
        assert classify_decision_confidence(record) == "High confidence decision"

    def test_moderate_confidence_when_below_scale_threshold(self):
        assert classify_decision_confidence(PAUSE_RECORD) == "Moderate confidence decision"

    def test_moderate_confidence_for_review_later_record(self):
        assert classify_decision_confidence(REVIEW_LATER_RECORD) == "Moderate confidence decision"

    def test_low_confidence_when_training_and_confidence_weak(self):
        assert classify_decision_confidence(STOP_RECORD) == "Low confidence decision"

    def test_low_confidence_below_training_threshold(self):
        record = {**CONTINUE_RECORD, "training_completion_rate": 0.55, "confidence_after": 2.9}
        assert classify_decision_confidence(record) == "Low confidence decision"


# ---------------------------------------------------------------------------
# 8. Decision reason priority
# ---------------------------------------------------------------------------


class TestIdentifyDecisionReason:
    def test_reason_references_stopped_adoption(self):
        reason = identify_decision_reason(STOP_RECORD)
        assert "stopped" in reason.lower()

    def test_reason_references_paused_pilot(self):
        reason = identify_decision_reason(PAUSE_RECORD)
        assert "paused" in reason.lower()

    def test_reason_references_risk_incident(self):
        record = {
            **CONTINUE_RECORD,
            "adoption_status": "Continue",
            "pilot_status": "In progress",
            "risk_incidents_logged": 1,
        }
        reason = identify_decision_reason(record)
        assert "incident" in reason.lower()

    def test_reason_references_near_misses(self):
        record = {
            **CONTINUE_RECORD,
            "adoption_status": "Continue",
            "pilot_status": "In progress",
            "risk_incidents_logged": 0,
            "near_misses_logged": 2,
        }
        reason = identify_decision_reason(record)
        assert "near miss" in reason.lower()

    def test_reason_references_quality_issues(self):
        record = {
            **CONTINUE_RECORD,
            "adoption_status": "Continue",
            "pilot_status": "In progress",
            "risk_incidents_logged": 0,
            "near_misses_logged": 0,
            "quality_issues_logged": 3,
        }
        reason = identify_decision_reason(record)
        assert "quality" in reason.lower()

    def test_reason_references_scale_evidence_for_scale_record(self):
        reason = identify_decision_reason(SCALE_RECORD)
        assert "scal" in reason.lower()

    def test_reason_references_pilot_scope_for_continue(self):
        reason = identify_decision_reason(CONTINUE_RECORD)
        assert "pilot" in reason.lower() or "adoption" in reason.lower()

    def test_stop_reason_takes_priority_over_incident_reason(self):
        record = {**STOP_RECORD, "risk_incidents_logged": 2}
        reason = identify_decision_reason(record)
        assert "stopped" in reason.lower()


# ---------------------------------------------------------------------------
# 9. Next action generation
# ---------------------------------------------------------------------------


class TestIdentifyNextAction:
    def test_next_action_for_stop(self):
        action = identify_next_action(STOP_RECORD)
        assert "stop" in action.lower()

    def test_next_action_for_pause(self):
        action = identify_next_action(PAUSE_RECORD)
        assert "pause" in action.lower()

    def test_next_action_for_continue_with_controls(self):
        action = identify_next_action(CONTINUE_WITH_CONTROLS_RECORD)
        assert "quality assurance" in action.lower() or "incident" in action.lower() or "controls" in action.lower()

    def test_next_action_for_scale(self):
        action = identify_next_action(SCALE_RECORD)
        assert "scale" in action.lower()

    def test_next_action_for_scale_with_monitoring(self):
        action = identify_next_action(SCALE_WITH_MONITORING_RECORD)
        assert "scale" in action.lower() or "monitor" in action.lower()

    def test_next_action_for_continue(self):
        action = identify_next_action(CONTINUE_RECORD)
        assert "continue" in action.lower() or "review" in action.lower()

    def test_next_action_for_review_later(self):
        action = identify_next_action(REVIEW_LATER_RECORD)
        assert "evidence" in action.lower() or "collect" in action.lower()


# ---------------------------------------------------------------------------
# 10. Workflow summary has expected keys
# ---------------------------------------------------------------------------


class TestBuildDecisionSummary:
    def test_summary_has_all_expected_fields(self):
        summary = build_decision_summary(CONTINUE_RECORD)
        assert EXPECTED_DECISION_SUMMARY_FIELDS.issubset(set(summary.keys()))

    def test_summary_decision_outcome_matches_classifier(self):
        summary = build_decision_summary(CONTINUE_RECORD)
        assert summary["decision_outcome"] == classify_decision_outcome(CONTINUE_RECORD)

    def test_summary_decision_confidence_matches_classifier(self):
        summary = build_decision_summary(CONTINUE_RECORD)
        assert summary["decision_confidence"] == classify_decision_confidence(CONTINUE_RECORD)

    def test_summary_passes_through_evidence_note(self):
        summary = build_decision_summary(CONTINUE_RECORD)
        assert summary["evidence_note"] == CONTINUE_RECORD["evidence_note"]

    def test_summary_clamps_negative_quality_issues(self):
        record = {**CONTINUE_RECORD, "quality_issues_logged": -1}
        summary = build_decision_summary(record)
        assert summary["quality_issues_logged"] == 0

    def test_summary_clamps_negative_risk_incidents(self):
        record = {**CONTINUE_RECORD, "risk_incidents_logged": -2}
        summary = build_decision_summary(record)
        assert summary["risk_incidents_logged"] == 0


# ---------------------------------------------------------------------------
# 11. All summaries match input length
# ---------------------------------------------------------------------------


class TestBuildAllDecisionSummaries:
    def test_all_summaries_length_matches_input(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        assert len(summaries) == len(records)

    def test_all_summaries_have_expected_fields(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        for summary in summaries:
            assert EXPECTED_DECISION_SUMMARY_FIELDS.issubset(set(summary.keys()))

    def test_all_summaries_have_non_empty_decision_outcome(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        for summary in summaries:
            assert summary["decision_outcome"] != ""

    def test_all_summaries_have_non_empty_decision_confidence(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        for summary in summaries:
            assert summary["decision_confidence"] != ""


# ---------------------------------------------------------------------------
# 12. Organisation summary groups correctly
# ---------------------------------------------------------------------------


class TestSummariseDecisionsByOrganisation:
    def test_org_summary_count_matches_three_organisations(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        org_summaries = summarise_decisions_by_organisation(summaries)
        assert len(org_summaries) == 3

    def test_org001_has_correct_workflow_count(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        org_summaries = summarise_decisions_by_organisation(summaries)
        org001 = next(o for o in org_summaries if o["organisation_id"] == "ORG001")
        assert org001["workflow_count"] == 4

    def test_org001_has_one_pause(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        org_summaries = summarise_decisions_by_organisation(summaries)
        org001 = next(o for o in org_summaries if o["organisation_id"] == "ORG001")
        assert org001["pause_count"] == 1

    def test_org001_has_one_review_later(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        org_summaries = summarise_decisions_by_organisation(summaries)
        org001 = next(o for o in org_summaries if o["organisation_id"] == "ORG001")
        assert org001["review_later_count"] == 1

    def test_org002_has_one_stop(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        org_summaries = summarise_decisions_by_organisation(summaries)
        org002 = next(o for o in org_summaries if o["organisation_id"] == "ORG002")
        assert org002["stop_count"] == 1

    def test_org002_has_one_continue_with_controls(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        org_summaries = summarise_decisions_by_organisation(summaries)
        org002 = next(o for o in org_summaries if o["organisation_id"] == "ORG002")
        assert org002["continue_with_controls_count"] == 1

    def test_org003_has_two_scale_with_monitoring(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        org_summaries = summarise_decisions_by_organisation(summaries)
        org003 = next(o for o in org_summaries if o["organisation_id"] == "ORG003")
        assert org003["scale_with_monitoring_count"] == 2

    def test_org003_has_two_continue_with_controls(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        org_summaries = summarise_decisions_by_organisation(summaries)
        org003 = next(o for o in org_summaries if o["organisation_id"] == "ORG003")
        assert org003["continue_with_controls_count"] == 2

    def test_org_summary_has_expected_keys(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        org_summaries = summarise_decisions_by_organisation(summaries)
        expected_keys = {
            "organisation_id", "organisation_name", "workflow_count",
            "stop_count", "pause_count", "continue_count",
            "continue_with_controls_count", "scale_count",
            "scale_with_monitoring_count", "review_later_count",
        }
        for org in org_summaries:
            assert expected_keys.issubset(set(org.keys()))


# ---------------------------------------------------------------------------
# 13. Related-build summary groups correctly
# ---------------------------------------------------------------------------


class TestSummariseDecisionsByRelatedBuild:
    def test_build_summary_count_matches_four_builds(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        build_summaries = summarise_decisions_by_related_build(summaries)
        assert len(build_summaries) == 4

    def test_build_5_has_two_continue_with_controls(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        build_summaries = summarise_decisions_by_related_build(summaries)
        build5 = next(b for b in build_summaries if b["related_build"] == "Build 5")
        assert build5["continue_with_controls_count"] == 2

    def test_build_6_has_one_stop_and_one_pause(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        build_summaries = summarise_decisions_by_related_build(summaries)
        build6 = next(b for b in build_summaries if b["related_build"] == "Build 6")
        assert build6["stop_count"] == 1
        assert build6["pause_count"] == 1

    def test_build_1_has_one_scale_with_monitoring(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        build_summaries = summarise_decisions_by_related_build(summaries)
        build1 = next(b for b in build_summaries if b["related_build"] == "Build 1")
        assert build1["scale_with_monitoring_count"] == 1

    def test_build_summary_has_expected_keys(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        build_summaries = summarise_decisions_by_related_build(summaries)
        expected_keys = {
            "related_build", "workflow_count", "stop_count", "pause_count",
            "continue_count", "continue_with_controls_count", "scale_count",
            "scale_with_monitoring_count", "review_later_count",
        }
        for build in build_summaries:
            assert expected_keys.issubset(set(build.keys()))


# ---------------------------------------------------------------------------
# 14. Prioritisation puts Stop/Pause/control workflows first
# ---------------------------------------------------------------------------


class TestPrioritiseDecisionsForFollowUp:
    def test_stop_workflow_is_first(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        prioritised = prioritise_decisions_for_follow_up(summaries)
        assert prioritised[0]["decision_outcome"] == "Stop"

    def test_pause_workflow_is_second(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        prioritised = prioritise_decisions_for_follow_up(summaries)
        assert prioritised[1]["decision_outcome"] == "Pause"

    def test_continue_with_controls_comes_before_continue(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        prioritised = prioritise_decisions_for_follow_up(summaries)
        outcomes = [s["decision_outcome"] for s in prioritised]
        last_control = max(i for i, o in enumerate(outcomes) if o == "Continue with controls")
        first_continue = min(i for i, o in enumerate(outcomes) if o == "Continue")
        assert last_control < first_continue

    def test_scale_with_monitoring_comes_after_continue(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        prioritised = prioritise_decisions_for_follow_up(summaries)
        outcomes = [s["decision_outcome"] for s in prioritised]
        last_continue = max(i for i, o in enumerate(outcomes) if o == "Continue")
        first_scale_monitoring = min(
            i for i, o in enumerate(outcomes) if o == "Scale with monitoring"
        )
        assert last_continue < first_scale_monitoring

    def test_within_continue_with_controls_incidents_sort_first(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        prioritised = prioritise_decisions_for_follow_up(summaries)
        control_workflows = [s for s in prioritised if s["decision_outcome"] == "Continue with controls"]
        assert control_workflows[0]["risk_incidents_logged"] >= control_workflows[-1]["risk_incidents_logged"]


# ---------------------------------------------------------------------------
# 15. Follow-up evidence notes are added without mutation
# ---------------------------------------------------------------------------


class TestAddFollowUpEvidenceNotes:
    def test_follow_up_note_is_added(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        enriched = add_follow_up_evidence_notes(summaries)
        for summary in enriched:
            assert "follow_up_evidence_note" in summary

    def test_original_summaries_are_not_mutated(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        _ = add_follow_up_evidence_notes(summaries)
        for summary in summaries:
            assert "follow_up_evidence_note" not in summary

    def test_stop_follow_up_note_content(self):
        summary = build_decision_summary(STOP_RECORD)
        note = generate_follow_up_evidence_note(summary)
        assert "redesign" in note.lower() or "should not continue" in note.lower()

    def test_pause_follow_up_note_content(self):
        summary = build_decision_summary(PAUSE_RECORD)
        note = generate_follow_up_evidence_note(summary)
        assert "pause" in note.lower()

    def test_continue_with_controls_follow_up_note_content(self):
        summary = build_decision_summary(CONTINUE_WITH_CONTROLS_RECORD)
        note = generate_follow_up_evidence_note(summary)
        assert "controls" in note.lower() or "monitoring" in note.lower()

    def test_scale_follow_up_note_content(self):
        summary = build_decision_summary(SCALE_RECORD)
        note = generate_follow_up_evidence_note(summary)
        assert "scal" in note.lower()

    def test_scale_with_monitoring_follow_up_note_content(self):
        summary = build_decision_summary(SCALE_WITH_MONITORING_RECORD)
        note = generate_follow_up_evidence_note(summary)
        assert "monitor" in note.lower() or "scal" in note.lower()

    def test_continue_follow_up_note_content(self):
        summary = build_decision_summary(CONTINUE_RECORD)
        note = generate_follow_up_evidence_note(summary)
        assert "continu" in note.lower() or "pilot" in note.lower()

    def test_enriched_count_matches_input(self):
        records = get_synthetic_adoption_metrics()
        summaries = build_all_decision_summaries(records)
        enriched = add_follow_up_evidence_notes(summaries)
        assert len(enriched) == len(summaries)


# ---------------------------------------------------------------------------
# 16. All synthetic adoption records process without errors
# ---------------------------------------------------------------------------


class TestAllSyntheticRecords:
    def test_all_records_produce_valid_decision_outcome(self):
        valid_outcomes = {
            "Stop", "Pause", "Continue with controls",
            "Scale", "Scale with monitoring", "Continue", "Review later",
        }
        records = get_synthetic_adoption_metrics()
        for record in records:
            outcome = classify_decision_outcome(record)
            assert outcome in valid_outcomes, f"Unexpected outcome for {record['workflow_id']}: {outcome}"

    def test_all_records_produce_valid_confidence(self):
        valid_confidence = {
            "High confidence decision", "Moderate confidence decision", "Low confidence decision"
        }
        records = get_synthetic_adoption_metrics()
        for record in records:
            confidence = classify_decision_confidence(record)
            assert confidence in valid_confidence

    def test_all_records_produce_non_empty_reason(self):
        records = get_synthetic_adoption_metrics()
        for record in records:
            reason = identify_decision_reason(record)
            assert isinstance(reason, str) and len(reason) > 0

    def test_all_records_produce_non_empty_next_action(self):
        records = get_synthetic_adoption_metrics()
        for record in records:
            action = identify_next_action(record)
            assert isinstance(action, str) and len(action) > 0

    def test_wf008_is_stop(self):
        records = get_synthetic_adoption_metrics()
        wf008 = next(r for r in records if r["workflow_id"] == "WF008")
        assert classify_decision_outcome(wf008) == "Stop"

    def test_wf004_is_pause(self):
        records = get_synthetic_adoption_metrics()
        wf004 = next(r for r in records if r["workflow_id"] == "WF004")
        assert classify_decision_outcome(wf004) == "Pause"

    def test_wf006_is_continue_with_controls(self):
        records = get_synthetic_adoption_metrics()
        wf006 = next(r for r in records if r["workflow_id"] == "WF006")
        assert classify_decision_outcome(wf006) == "Continue with controls"

    def test_wf009_is_scale_with_monitoring(self):
        records = get_synthetic_adoption_metrics()
        wf009 = next(r for r in records if r["workflow_id"] == "WF009")
        assert classify_decision_outcome(wf009) == "Scale with monitoring"

    def test_wf011_is_scale_with_monitoring(self):
        records = get_synthetic_adoption_metrics()
        wf011 = next(r for r in records if r["workflow_id"] == "WF011")
        assert classify_decision_outcome(wf011) == "Scale with monitoring"

    def test_wf001_is_continue(self):
        records = get_synthetic_adoption_metrics()
        wf001 = next(r for r in records if r["workflow_id"] == "WF001")
        assert classify_decision_outcome(wf001) == "Continue"

    def test_wf002_is_review_later(self):
        records = get_synthetic_adoption_metrics()
        wf002 = next(r for r in records if r["workflow_id"] == "WF002")
        assert classify_decision_outcome(wf002) == "Review later"

    def test_wf010_is_continue_with_controls(self):
        records = get_synthetic_adoption_metrics()
        wf010 = next(r for r in records if r["workflow_id"] == "WF010")
        assert classify_decision_outcome(wf010) == "Continue with controls"

    def test_wf012_is_continue_with_controls(self):
        records = get_synthetic_adoption_metrics()
        wf012 = next(r for r in records if r["workflow_id"] == "WF012")
        assert classify_decision_outcome(wf012) == "Continue with controls"
