"""Build 7 Streamlit app for synthetic AI adoption impact tracking."""

import streamlit as st

from data.synthetic_adoption_data import (
    get_synthetic_adoption_metrics,
    get_synthetic_organisations,
    get_synthetic_review_decisions,
)
from logic.adoption_metrics import (
    calculate_confidence_change,
    calculate_minutes_saved_per_task,
    calculate_weekly_minutes_saved,
    summarise_phase_1_metrics,
    validate_all_adoption_records,
)
from logic.roi_summary import (
    build_all_workflow_roi_summaries,
    summarise_portfolio_roi,
    summarise_roi_by_organisation,
)
from logic.workflow_impact import (
    add_recommendations_to_impact_summaries,
    build_all_workflow_impact_summaries,
    prioritise_workflows_for_action,
    summarise_workflow_impact_by_organisation,
    summarise_workflow_impact_by_related_build,
)
from logic.training_readiness import (
    add_training_recommendations_to_summaries,
    build_all_training_readiness_summaries,
    prioritise_training_support_actions,
    summarise_training_readiness_by_organisation,
    summarise_training_readiness_by_related_build,
    summarise_training_readiness_by_staff_group,
)
from logic.risk_quality_review import (
    add_risk_quality_recommendations,
    build_all_risk_quality_summaries,
    prioritise_risk_quality_actions,
    summarise_risk_quality_by_organisation,
    summarise_risk_quality_by_related_build,
)
from logic.decision_tracker import (
    add_follow_up_evidence_notes,
    build_all_decision_summaries,
    prioritise_decisions_for_follow_up,
    summarise_decisions_by_organisation,
    summarise_decisions_by_related_build,
)
from logic.follow_up_report import (
    build_full_follow_up_report,
    get_organisation_records,
)
from logic.export_centre import (
    build_completion_review_text,
    build_completion_summary,
    export_csv_text,
    export_json_text,
    export_markdown_report,
    build_export_filename,
)


PAGE_TITLE = "Build 7 — AI Adoption ROI and Impact Tracker"

PHASE_NAVIGATION = [
    "1. Adoption Metrics Setup",
    "2. ROI Summary",
    "3. Workflow Impact",
    "4. Training and Confidence",
    "5. Risk and Quality Review",
    "6. Decision Tracker",
    "7. Client Follow-up Report",
    "8. Export Centre",
]

ACTIVE_PHASES = PHASE_NAVIGATION[:8]


st.set_page_config(
    page_title=PAGE_TITLE,
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_sidebar() -> str:
    """Render the phase navigation sidebar and return the selected phase label."""
    with st.sidebar:
        st.title("Build 7")
        st.caption("AI Adoption ROI and Impact Tracker")
        st.divider()
        st.markdown("### Phase Navigation")
        selected = st.radio(
            "Active phase",
            ACTIVE_PHASES,
            index=0,
            label_visibility="collapsed",
        )
        for phase in PHASE_NAVIGATION[len(ACTIVE_PHASES):]:
            st.button(phase, disabled=True, use_container_width=True)
        st.divider()
        st.caption(
            "Phases 1–8 use synthetic/demo data only. No real client, learner, "
            "HR, safeguarding, personal, confidential, or regulated data."
        )
    return selected


# ---------------------------------------------------------------------------
# Phase 1 helpers
# ---------------------------------------------------------------------------


def build_metrics_table(records: list[dict]) -> list[dict]:
    """Prepare a compact table for the Phase 1 Streamlit view."""
    return [
        {
            "Organisation": r["organisation_name"],
            "Workflow": r["workflow_name"],
            "Related build": r["related_build"],
            "Staff group": r["staff_group"],
            "Minutes saved per task": calculate_minutes_saved_per_task(r),
            "Weekly minutes saved": calculate_weekly_minutes_saved(r),
            "Confidence change": calculate_confidence_change(r),
            "Training completion": f"{r['training_completion_rate']:.0%}",
            "Pilot status": r["pilot_status"],
            "Adoption status": r["adoption_status"],
            "Quality issues": r["quality_issues_logged"],
            "Risk incidents": r["risk_incidents_logged"],
            "Near misses": r["near_misses_logged"],
            "Review decision": r["review_decision"],
        }
        for r in records
    ]


def render_validation_summary(validation_summary: dict) -> None:
    """Render a simple validation summary for the synthetic records."""
    col1, col2, col3 = st.columns(3)
    col1.metric("Total records", validation_summary["total_records"])
    col2.metric("Valid records", validation_summary["valid_records"])
    col3.metric("Records with warnings", validation_summary["records_with_warnings"])

    if validation_summary["warnings"]:
        st.warning("Validation warnings were found in the synthetic data.")
        st.write(validation_summary["warnings"])
    else:
        st.success("All synthetic adoption metric records passed the Phase 1 validation checks.")


def render_phase_1_metrics(summary: dict) -> None:
    """Render non-financial Phase 1 metric signals."""
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Workflows tracked", summary["total_workflows"])
    col2.metric("Weekly minutes saved", summary["total_weekly_minutes_saved"])
    col3.metric("Avg confidence change", summary["average_confidence_change"])
    col4.metric("Avg training completion", f"{summary['average_training_completion_rate']:.0%}")

    col5, col6, col7 = st.columns(3)
    col5.metric("Quality issues", summary["total_quality_issues"])
    col6.metric("Risk incidents", summary["total_risk_incidents"])
    col7.metric("Near misses", summary["total_near_misses"])


def render_phase_1(
    adoption_records: list[dict],
    organisations: list[dict],
    review_decisions: list[dict],
) -> None:
    """Render Phase 1: Adoption Metrics Setup."""
    validation_summary = validate_all_adoption_records(adoption_records)
    phase_1_summary = summarise_phase_1_metrics(adoption_records)

    st.title(PAGE_TITLE)
    st.write(
        "This tool tracks whether AI adoption is producing practical value after audit, "
        "governance, training, and pilot work."
    )
    st.info(
        "Phase 1 establishes the synthetic adoption metrics foundation. "
        "Use the sidebar to explore the completed ROI, impact, training, risk, "
        "decision, reporting, and export phases."
    )

    st.subheader("Synthetic Organisation Overview")
    st.dataframe(organisations, hide_index=True, use_container_width=True)

    st.subheader("Synthetic Adoption Metrics")
    st.dataframe(build_metrics_table(adoption_records), hide_index=True, use_container_width=True)

    st.subheader("Basic Validation Summary")
    render_validation_summary(validation_summary)

    st.subheader("Phase 1 Metric Signals")
    render_phase_1_metrics(phase_1_summary)

    st.subheader("Synthetic Review Decision Examples")
    st.dataframe(review_decisions, hide_index=True, use_container_width=True)

    st.subheader("Portfolio Connection")
    st.markdown(
        """
Build 7 closes the loop after earlier consulting outputs have been produced:

- **Build 1** identifies workflows, readiness gaps, and adoption opportunities that can be tracked here.
- **Build 4** creates staff training materials; Build 7 tracks confidence change and completion.
- **Build 5** produces consulting reports; Build 7 adds follow-up evidence for later client updates.
- **Build 6** checks governance policies; Build 7 tracks quality issues, incidents, near misses, and review decisions.
        """
    )


# ---------------------------------------------------------------------------
# Phase 2 helpers
# ---------------------------------------------------------------------------


def build_roi_workflow_table(roi_summaries: list[dict]) -> list[dict]:
    """Prepare a compact workflow ROI table for Streamlit display."""
    return [
        {
            "Organisation": s["organisation_name"],
            "Workflow": s["workflow_name"],
            "Staff group": s["staff_group"],
            "Weekly hrs saved": s["weekly_hours_saved"],
            "Annual hrs saved": s["annual_hours_saved"],
            "Efficiency gain %": s["efficiency_gain_percent"],
            "Annual value equiv. (£)": s["annual_value_equivalent"],
            "Time saving band": s["time_saving_band"],
            "Confidence improvement": s["confidence_improvement_band"],
            "Adoption value": s["adoption_value_indicator"],
            "Status": s["adoption_status"],
        }
        for s in roi_summaries
    ]


def build_roi_org_table(org_summaries: list[dict]) -> list[dict]:
    """Prepare a compact organisation ROI table for Streamlit display."""
    return [
        {
            "Organisation": s["organisation_name"],
            "Workflows": s["workflow_count"],
            "Weekly hrs saved": s["total_weekly_hours_saved"],
            "Annual hrs saved": s["total_annual_hours_saved"],
            "Annual value equiv. (£)": s["total_annual_value_equivalent"],
            "Avg efficiency gain %": s["average_efficiency_gain_percent"],
            "Avg confidence change": s["average_confidence_change"],
            "Strong / Clear value": s["strong_or_clear_value_workflows"],
            "Needs review": s["needs_review_workflows"],
        }
        for s in org_summaries
    ]


def render_phase_2(adoption_records: list[dict]) -> None:
    """Render Phase 2: ROI Summary."""
    roi_summaries = build_all_workflow_roi_summaries(adoption_records)
    org_summaries = summarise_roi_by_organisation(roi_summaries)
    portfolio = summarise_portfolio_roi(roi_summaries)

    st.title(PAGE_TITLE)
    st.subheader("Phase 2 — ROI Summary")
    st.write(
        "This section estimates adoption value using synthetic time-saving, efficiency, "
        "and value-equivalent assumptions."
    )
    st.info(
        "These figures are synthetic consulting estimates for portfolio demonstration only. "
        "They are not audited financial ROI and do not use real client data."
    )

    st.subheader("Portfolio-Level ROI Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Organisations", portfolio["organisation_count"])
    col2.metric("Workflows tracked", portfolio["workflow_count"])
    col3.metric("Avg efficiency gain", f"{portfolio['average_efficiency_gain_percent']}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("Total weekly hrs saved", portfolio["total_weekly_hours_saved"])
    col5.metric("Total monthly hrs saved", portfolio["total_monthly_hours_saved"])
    col6.metric("Total annual hrs saved", portfolio["total_annual_hours_saved"])

    col7, col8, col9 = st.columns(3)
    col7.metric("Weekly value equiv.", f"£{portfolio['total_weekly_value_equivalent']:,.2f}")
    col8.metric("Monthly value equiv.", f"£{portfolio['total_monthly_value_equivalent']:,.2f}")
    col9.metric("Annual value equiv.", f"£{portfolio['total_annual_value_equivalent']:,.2f}")

    col10, col11, _ = st.columns(3)
    col10.metric("Avg confidence change", portfolio["average_confidence_change"])
    col11.metric("Workflows needing review", portfolio["needs_review_workflows"])

    st.subheader("Organisation-Level ROI Summary")
    st.dataframe(build_roi_org_table(org_summaries), hide_index=True, use_container_width=True)

    st.subheader("Workflow-Level ROI Summary")
    st.dataframe(build_roi_workflow_table(roi_summaries), hide_index=True, use_container_width=True)

    st.subheader("Consulting Interpretation")
    st.markdown(
        """
The ROI summary helps a consultant identify which AI-supported workflows are showing measurable
operational benefit, which pilots need review, and which workflows may be ready to scale.
The figures should be treated as directional evidence rather than audited financial return.

- **Time-saving bands** (Low / Moderate / High / Very high) give a quick view of where AI is
  having operational impact.
- **Confidence improvement bands** reflect whether staff are more confident using AI safely
  after training.
- **Adoption value indicators** combine time saved, confidence, training completion, and quality
  signals into a single summary position per workflow.
- **Workflows marked "Needs review"** have either an active risk incident, a Stop or Review
  decision, or more than two near misses — these should be prioritised in the next client
  follow-up conversation.

> Estimated value equivalents use synthetic hourly-rate assumptions and should not be presented
> to clients as audited financial savings. They are directional indicators for consulting
> conversations only.
        """
    )


# ---------------------------------------------------------------------------
# Phase 3 helpers
# ---------------------------------------------------------------------------


def build_impact_action_table(prioritised: list[dict]) -> list[dict]:
    """Prepare a compact prioritised action table for Streamlit display."""
    return [
        {
            "Organisation": s["organisation_name"],
            "Workflow": s["workflow_name"],
            "Related build": s["related_build"],
            "Impact status": s["workflow_impact_status"],
            "Primary bottleneck": s["primary_bottleneck"],
            "Efficiency gain %": s["efficiency_gain_percent"],
            "Confidence change": s["confidence_change"],
            "Quality issues": s["quality_issues_logged"],
            "Risk signals": s["risk_signal_count"],
            "Recommended action": s["recommended_action"],
        }
        for s in prioritised
    ]


def build_impact_org_table(org_summaries: list[dict]) -> list[dict]:
    """Prepare a compact organisation impact table for Streamlit display."""
    return [
        {
            "Organisation": s["organisation_name"],
            "Workflows": s["workflow_count"],
            "Ready to scale": s["ready_to_scale_count"],
            "Positive / monitor": s["positive_but_monitor_count"],
            "Needs improvement": s["needs_improvement_count"],
            "Governance review": s["needs_governance_review_count"],
            "Stop or pause": s["stop_or_pause_count"],
            "Risk bottleneck": s["risk_bottleneck_count"],
            "Quality bottleneck": s["quality_bottleneck_count"],
            "Avg efficiency %": s["average_efficiency_gain_percent"],
            "Avg confidence change": s["average_confidence_change"],
        }
        for s in org_summaries
    ]


def build_impact_build_table(build_summaries: list[dict]) -> list[dict]:
    """Prepare a compact related-build impact table for Streamlit display."""
    return [
        {
            "Related build": s["related_build"],
            "Workflows": s["workflow_count"],
            "Ready to scale": s["ready_to_scale_count"],
            "Positive / monitor": s["positive_but_monitor_count"],
            "Governance review": s["needs_governance_review_count"],
            "Stop or pause": s["stop_or_pause_count"],
            "Avg efficiency %": s["average_efficiency_gain_percent"],
            "Avg confidence change": s["average_confidence_change"],
            "Dominant bottleneck": s["dominant_bottleneck"],
        }
        for s in build_summaries
    ]


def render_phase_3(adoption_records: list[dict]) -> None:
    """Render Phase 3: Workflow Impact and Bottleneck Analysis."""
    impact_summaries = build_all_workflow_impact_summaries(adoption_records)
    enriched = add_recommendations_to_impact_summaries(impact_summaries)
    org_summaries = summarise_workflow_impact_by_organisation(impact_summaries)
    build_summaries = summarise_workflow_impact_by_related_build(impact_summaries)
    prioritised = prioritise_workflows_for_action(enriched)

    st.title(PAGE_TITLE)
    st.subheader("Phase 3 — Workflow Impact and Bottleneck Analysis")
    st.write(
        "This section identifies which AI-supported workflows are working well, "
        "which ones need improvement, and which ones may require governance review "
        "before scaling."
    )
    st.info(
        "This analysis uses synthetic portfolio data only. It is designed to demonstrate "
        "how a consultant could review adoption evidence after an AI pilot."
    )

    st.subheader("Workflow Impact Overview")

    total = len(impact_summaries)
    ready = sum(1 for s in impact_summaries if s["workflow_impact_status"] == "Ready to scale")
    positive = sum(
        1 for s in impact_summaries if s["workflow_impact_status"] == "Positive but monitor"
    )
    improvement = sum(
        1 for s in impact_summaries if s["workflow_impact_status"] == "Needs improvement"
    )
    governance = sum(
        1 for s in impact_summaries if s["workflow_impact_status"] == "Needs governance review"
    )
    stopped = sum(
        1 for s in impact_summaries if s["workflow_impact_status"] == "Stop or pause"
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total workflows", total)
    col2.metric("Ready to scale", ready)
    col3.metric("Positive but monitor", positive)

    col4, col5, col6 = st.columns(3)
    col4.metric("Needs improvement", improvement)
    col5.metric("Needs governance review", governance)
    col6.metric("Stop or pause", stopped)

    st.subheader("Organisation-Level Workflow Impact")
    st.dataframe(build_impact_org_table(org_summaries), hide_index=True, use_container_width=True)

    st.subheader("Build-Level Workflow Impact")
    st.write(
        "This shows how workflows related to Build 1, Build 4, Build 5, and Build 6 "
        "are contributing to adoption outcomes across the portfolio."
    )
    st.dataframe(
        build_impact_build_table(build_summaries), hide_index=True, use_container_width=True
    )

    st.subheader("Prioritised Workflow Action List")
    st.write(
        "Workflows are listed from most to least urgent, based on impact status, "
        "risk signals, and quality issues."
    )
    st.dataframe(
        build_impact_action_table(prioritised), hide_index=True, use_container_width=True
    )

    st.subheader("Consulting Interpretation")
    st.markdown(
        """
This analysis helps a consultant move beyond simple ROI figures. A workflow may save time
but still require review if quality issues, staff confidence gaps, or governance signals are
present. The prioritised action list helps decide where to intervene first, where to continue
monitoring, and where cautious scaling may be appropriate.

- **Ready to scale** — strong adoption evidence with positive signals across efficiency,
  confidence, training, quality, and risk.
- **Positive but monitor** — time saving is visible and risk is low, but the pilot is not
  yet complete enough to recommend scaling.
- **Needs improvement** — adoption is proceeding but one or more bottlenecks need attention
  before the workflow can show its full value.
- **Needs governance review** — active risk incidents, near-miss patterns, or a Review
  decision require follow-up before the workflow continues.
- **Stop or pause** — the workflow has been stopped or paused and should not be expanded
  until outstanding concerns are resolved.

> Bottleneck classifications are based on synthetic pilot evidence. They should be used
> as a starting point for consulting conversations, not as final assessments.
        """
    )


# ---------------------------------------------------------------------------
# Phase 4 helpers
# ---------------------------------------------------------------------------


def build_training_support_table(prioritised: list[dict]) -> list[dict]:
    """Prepare a compact prioritised training support table for Streamlit display."""
    return [
        {
            "Organisation": s["organisation_name"],
            "Workflow": s["workflow_name"],
            "Related build": s["related_build"],
            "Staff group": s["staff_group"],
            "Training %": f"{s['training_completion_rate']:.0%}",
            "Confidence before": s["confidence_before"],
            "Confidence after": s["confidence_after"],
            "Confidence change": s["confidence_change"],
            "Readiness score": s["training_readiness_score"],
            "Readiness band": s["training_readiness_band"],
            "Support need": s["training_support_need"],
            "Adoption readiness": s["staff_adoption_readiness"],
            "Recommendation": s["training_recommendation"],
        }
        for s in prioritised
    ]


def build_training_staff_group_table(group_summaries: list[dict]) -> list[dict]:
    """Prepare a compact staff group readiness table for Streamlit display."""
    return [
        {
            "Staff group": s["staff_group"],
            "Workflows": s["workflow_count"],
            "Avg training %": f"{s['average_training_completion_rate']:.0%}",
            "Avg confidence before": s["average_confidence_before"],
            "Avg confidence after": s["average_confidence_after"],
            "Avg confidence change": s["average_confidence_change"],
            "Avg readiness score": s["average_training_readiness_score"],
            "Blocked": s["blocked_count"],
            "Needs support": s["needs_support_count"],
            "Developing": s["developing_count"],
            "Adoption ready": s["adoption_ready_count"],
            "Scale ready": s["scale_ready_count"],
            "Dominant support need": s["dominant_support_need"],
        }
        for s in group_summaries
    ]


def build_training_org_table(org_summaries: list[dict]) -> list[dict]:
    """Prepare a compact organisation readiness table for Streamlit display."""
    return [
        {
            "Organisation": s["organisation_name"],
            "Workflows": s["workflow_count"],
            "Avg training %": f"{s['average_training_completion_rate']:.0%}",
            "Avg confidence change": s["average_confidence_change"],
            "Avg readiness score": s["average_training_readiness_score"],
            "Blocked": s["blocked_count"],
            "Needs support": s["needs_support_count"],
            "Developing": s["developing_count"],
            "Adoption ready": s["adoption_ready_count"],
            "Scale ready": s["scale_ready_count"],
            "Dominant support need": s["dominant_support_need"],
        }
        for s in org_summaries
    ]


def build_training_build_table(build_summaries: list[dict]) -> list[dict]:
    """Prepare a compact related-build readiness table for Streamlit display."""
    return [
        {
            "Related build": s["related_build"],
            "Workflows": s["workflow_count"],
            "Avg training %": f"{s['average_training_completion_rate']:.0%}",
            "Avg confidence change": s["average_confidence_change"],
            "Avg readiness score": s["average_training_readiness_score"],
            "Blocked": s["blocked_count"],
            "Developing": s["developing_count"],
            "Adoption ready": s["adoption_ready_count"],
            "Scale ready": s["scale_ready_count"],
            "Dominant support need": s["dominant_support_need"],
        }
        for s in build_summaries
    ]


def render_phase_4(adoption_records: list[dict]) -> None:
    """Render Phase 4: Training, Confidence, and Adoption Readiness Review."""
    tr_summaries = build_all_training_readiness_summaries(adoption_records)
    enriched = add_training_recommendations_to_summaries(tr_summaries)
    staff_group_summaries = summarise_training_readiness_by_staff_group(tr_summaries)
    org_summaries = summarise_training_readiness_by_organisation(tr_summaries)
    build_summaries = summarise_training_readiness_by_related_build(tr_summaries)
    prioritised = prioritise_training_support_actions(enriched)

    st.title(PAGE_TITLE)
    st.subheader("Phase 4 — Training, Confidence, and Adoption Readiness Review")
    st.write(
        "This section reviews whether staff groups are becoming confident enough to use "
        "AI-supported workflows safely, consistently, and independently."
    )
    st.info(
        "This review uses synthetic portfolio data only. It demonstrates how a consultant "
        "could assess training impact and adoption readiness after an AI pilot."
    )

    st.subheader("Training Readiness Overview")

    total = len(tr_summaries)
    blocked = sum(1 for s in tr_summaries if s["staff_adoption_readiness"] == "Blocked")
    needs_support = sum(1 for s in tr_summaries if s["staff_adoption_readiness"] == "Needs support")
    developing = sum(1 for s in tr_summaries if s["staff_adoption_readiness"] == "Developing")
    adoption_ready = sum(1 for s in tr_summaries if s["staff_adoption_readiness"] == "Adoption ready")
    scale_ready = sum(1 for s in tr_summaries if s["staff_adoption_readiness"] == "Scale ready")
    avg_training = round(sum(s["training_completion_rate"] for s in tr_summaries) / total, 2) if total else 0.0
    avg_change = round(sum(s["confidence_change"] for s in tr_summaries) / total, 2) if total else 0.0
    avg_score = round(sum(s["training_readiness_score"] for s in tr_summaries) / total, 2) if total else 0.0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total workflows", total)
    col2.metric("Blocked", blocked)
    col3.metric("Needs support", needs_support)

    col4, col5, col6 = st.columns(3)
    col4.metric("Developing", developing)
    col5.metric("Adoption ready", adoption_ready)
    col6.metric("Scale ready", scale_ready)

    col7, col8, col9 = st.columns(3)
    col7.metric("Avg training completion", f"{avg_training:.0%}")
    col8.metric("Avg confidence change", avg_change)
    col9.metric("Avg readiness score", avg_score)

    st.subheader("Staff Group Readiness")
    st.dataframe(
        build_training_staff_group_table(staff_group_summaries),
        hide_index=True,
        use_container_width=True,
    )

    st.subheader("Organisation-Level Readiness")
    st.dataframe(
        build_training_org_table(org_summaries), hide_index=True, use_container_width=True
    )

    st.subheader("Build-Level Readiness")
    st.write(
        "This shows how workflows related to Build 1, Build 4, Build 5, and Build 6 are "
        "contributing to training and adoption readiness across the portfolio."
    )
    st.dataframe(
        build_training_build_table(build_summaries), hide_index=True, use_container_width=True
    )

    st.subheader("Prioritised Training Support Actions")
    st.write(
        "Workflows are listed from most to least urgent, based on adoption readiness, "
        "training completion, and confidence levels."
    )
    st.dataframe(
        build_training_support_table(prioritised), hide_index=True, use_container_width=True
    )

    st.subheader("Consulting Interpretation")
    st.markdown(
        """
This review helps a consultant understand whether adoption is being limited by people-side
factors rather than technology alone. A workflow may show time savings, but it should not
be scaled if staff confidence is weak, training completion is low, or users still need
guided support. The prioritised action list helps decide where further training, coaching,
reinforcement, or scale enablement is needed.

- **Blocked** — the workflow has been stopped or paused. No further training investment
  is appropriate until the underlying adoption decision is resolved.
- **Needs support** — staff confidence or training completion is too low for independent
  adoption. Structured support is required before continuing.
- **Developing** — staff are making progress but are not yet consistently confident or
  trained enough to adopt without ongoing guidance.
- **Adoption ready** — staff show sufficient training and confidence for continued
  independent adoption under monitoring.
- **Scale ready** — staff have strong training completion, high confidence, and meaningful
  confidence growth, and the workflow is approved for scaling.

> Readiness scores are synthetic consulting estimates based on training completion,
> confidence after, and confidence growth. They are not formal capability assessments.
        """
    )


# ---------------------------------------------------------------------------
# Phase 5 helpers
# ---------------------------------------------------------------------------


def build_risk_quality_action_table(prioritised: list[dict]) -> list[dict]:
    """Prepare a compact prioritised risk and quality action table for Streamlit display."""
    return [
        {
            "Organisation": s["organisation_name"],
            "Workflow": s["workflow_name"],
            "Related build": s["related_build"],
            "Adoption status": s["responsible_adoption_status"],
            "Control need": s["control_need"],
            "Scaling permission": s["scaling_permission"],
            "Quality issues": s["quality_issues_logged"],
            "Risk incidents": s["risk_incidents_logged"],
            "Near misses": s["near_misses_logged"],
            "Recommendation": s["risk_quality_recommendation"],
        }
        for s in prioritised
    ]


def build_risk_quality_org_table(org_summaries: list[dict]) -> list[dict]:
    """Prepare a compact organisation risk and quality table for Streamlit display."""
    return [
        {
            "Organisation": s["organisation_name"],
            "Workflows": s["workflow_count"],
            "High quality concern": s["high_quality_concern_count"],
            "High risk concern": s["high_risk_concern_count"],
            "Governance review": s["requires_governance_review_count"],
            "Pause adoption": s["pause_adoption_count"],
            "Scale permitted": s["scale_permitted_count"],
            "Scale with controls": s["scale_with_controls_count"],
            "Do not scale yet": s["do_not_scale_yet_count"],
        }
        for s in org_summaries
    ]


def build_risk_quality_build_table(build_summaries: list[dict]) -> list[dict]:
    """Prepare a compact related-build risk and quality table for Streamlit display."""
    return [
        {
            "Related build": s["related_build"],
            "Workflows": s["workflow_count"],
            "High quality concern": s["high_quality_concern_count"],
            "High risk concern": s["high_risk_concern_count"],
            "Governance review": s["requires_governance_review_count"],
            "Pause adoption": s["pause_adoption_count"],
            "Scale permitted": s["scale_permitted_count"],
            "Scale with controls": s["scale_with_controls_count"],
            "Do not scale yet": s["do_not_scale_yet_count"],
        }
        for s in build_summaries
    ]


def render_phase_5(adoption_records: list[dict]) -> None:
    """Render Phase 5: Risk, Quality, and Responsible Adoption Review."""
    rq_summaries = build_all_risk_quality_summaries(adoption_records)
    enriched = add_risk_quality_recommendations(rq_summaries)
    org_summaries = summarise_risk_quality_by_organisation(rq_summaries)
    build_summaries = summarise_risk_quality_by_related_build(rq_summaries)
    prioritised = prioritise_risk_quality_actions(enriched)

    st.title(PAGE_TITLE)
    st.subheader("Phase 5 — Risk, Quality, and Responsible Adoption Review")
    st.write(
        "This review checks whether AI-supported workflows are safe enough to continue, "
        "pause, or scale, based on quality issues, risk incidents, near misses, and "
        "governance review needs."
    )
    st.info(
        "This review uses synthetic portfolio data only. It demonstrates how a consultant "
        "could check whether AI-supported workflows are safe enough to continue, pause, or scale."
    )

    st.subheader("Risk and Quality Overview")

    total = len(rq_summaries)
    governance_review = sum(
        1 for s in rq_summaries if s["responsible_adoption_status"] == "Requires governance review"
    )
    pause_count = sum(
        1 for s in rq_summaries if s["responsible_adoption_status"] == "Pause adoption"
    )
    scale_permitted = sum(
        1 for s in rq_summaries if s["scaling_permission"] == "Scale permitted"
    )
    scale_with_controls = sum(
        1 for s in rq_summaries if s["scaling_permission"] == "Scale with controls"
    )
    do_not_scale = sum(
        1 for s in rq_summaries if s["scaling_permission"] == "Do not scale yet"
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total workflows", total)
    col2.metric("Requires governance review", governance_review)
    col3.metric("Pause adoption", pause_count)

    col4, col5, col6 = st.columns(3)
    col4.metric("Scale permitted", scale_permitted)
    col5.metric("Scale with controls", scale_with_controls)
    col6.metric("Do not scale yet", do_not_scale)

    st.subheader("Organisation-Level Risk and Quality")
    st.dataframe(
        build_risk_quality_org_table(org_summaries), hide_index=True, use_container_width=True
    )

    st.subheader("Build-Level Risk and Quality")
    st.write(
        "This shows how workflows related to Build 1, Build 4, Build 5, and Build 6 "
        "are performing on quality and risk indicators across the portfolio."
    )
    st.dataframe(
        build_risk_quality_build_table(build_summaries), hide_index=True, use_container_width=True
    )

    st.subheader("Prioritised Risk and Quality Action List")
    st.write(
        "Workflows are listed from most to least urgent, based on responsible adoption "
        "status, risk signals, and quality issues."
    )
    st.dataframe(
        build_risk_quality_action_table(prioritised), hide_index=True, use_container_width=True
    )

    st.subheader("Consulting Interpretation")
    st.markdown(
        """
This review prevents AI adoption from being judged by time saved alone. A workflow should
not be scaled if quality issues, near misses, risk incidents, or weak controls suggest that
adoption is not yet responsible.

- **Responsible to scale** — the workflow has a Scale decision, sufficient training, good
  staff confidence, and no significant quality or risk signals. Scaling may proceed with
  continued monitoring.
- **Responsible to continue** — the workflow is running without major concerns, but no
  scaling decision has been made. Continue monitoring.
- **Continue with controls** — quality issues or near misses are present. Additional
  controls, review checklists, or incident logging clarity are needed before scaling.
- **Requires governance review** — a logged risk incident or a pattern of near misses above
  safe thresholds requires a formal review before the workflow continues or scales.
- **Pause adoption** — the workflow has been stopped or paused. No further scaling or
  expansion is appropriate until the adoption decision is resolved.

> Scaling permissions are based on synthetic quality, risk, training, and confidence
> evidence. They are consulting indicators, not formal governance decisions.
        """
    )


# ---------------------------------------------------------------------------
# Phase 6 helpers
# ---------------------------------------------------------------------------


def build_decision_follow_up_table(prioritised: list[dict]) -> list[dict]:
    """Prepare a compact prioritised follow-up decision table for Streamlit display."""
    return [
        {
            "Organisation": s["organisation_name"],
            "Workflow": s["workflow_name"],
            "Related build": s["related_build"],
            "Decision outcome": s["decision_outcome"],
            "Decision confidence": s["decision_confidence"],
            "Decision reason": s["decision_reason"],
            "Next action": s["next_action"],
            "Follow-up evidence note": s["follow_up_evidence_note"],
        }
        for s in prioritised
    ]


def build_decision_org_table(org_summaries: list[dict]) -> list[dict]:
    """Prepare a compact organisation decision table for Streamlit display."""
    return [
        {
            "Organisation": s["organisation_name"],
            "Workflows": s["workflow_count"],
            "Stop": s["stop_count"],
            "Pause": s["pause_count"],
            "Continue": s["continue_count"],
            "Continue with controls": s["continue_with_controls_count"],
            "Scale": s["scale_count"],
            "Scale with monitoring": s["scale_with_monitoring_count"],
            "Review later": s["review_later_count"],
        }
        for s in org_summaries
    ]


def build_decision_build_table(build_summaries: list[dict]) -> list[dict]:
    """Prepare a compact related-build decision table for Streamlit display."""
    return [
        {
            "Related build": s["related_build"],
            "Workflows": s["workflow_count"],
            "Stop": s["stop_count"],
            "Pause": s["pause_count"],
            "Continue": s["continue_count"],
            "Continue with controls": s["continue_with_controls_count"],
            "Scale": s["scale_count"],
            "Scale with monitoring": s["scale_with_monitoring_count"],
            "Review later": s["review_later_count"],
        }
        for s in build_summaries
    ]


def render_phase_6(adoption_records: list[dict]) -> None:
    """Render Phase 6: Decision Tracker and Client Follow-up Evidence."""
    decision_summaries = build_all_decision_summaries(adoption_records)
    enriched = add_follow_up_evidence_notes(decision_summaries)
    org_summaries = summarise_decisions_by_organisation(decision_summaries)
    build_summaries = summarise_decisions_by_related_build(decision_summaries)
    prioritised = prioritise_decisions_for_follow_up(enriched)

    st.title(PAGE_TITLE)
    st.subheader("Phase 6 — Decision Tracker and Client Follow-up Evidence")
    st.write(
        "This section converts adoption evidence into clear consulting decisions and "
        "generates deterministic follow-up evidence notes for each workflow."
    )
    st.info(
        "This section uses synthetic portfolio data only. It demonstrates how a consultant "
        "could convert adoption evidence into stop, continue, review, or scale decisions."
    )

    st.subheader("Decision Overview")

    total = len(decision_summaries)
    stop_count = sum(1 for s in decision_summaries if s["decision_outcome"] == "Stop")
    pause_count = sum(1 for s in decision_summaries if s["decision_outcome"] == "Pause")
    continue_count = sum(1 for s in decision_summaries if s["decision_outcome"] == "Continue")
    continue_controls_count = sum(
        1 for s in decision_summaries if s["decision_outcome"] == "Continue with controls"
    )
    scale_count = sum(1 for s in decision_summaries if s["decision_outcome"] == "Scale")
    scale_monitoring_count = sum(
        1 for s in decision_summaries if s["decision_outcome"] == "Scale with monitoring"
    )
    review_later_count = sum(
        1 for s in decision_summaries if s["decision_outcome"] == "Review later"
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total workflows", total)
    col2.metric("Stop", stop_count)
    col3.metric("Pause", pause_count)
    col4.metric("Continue", continue_count)

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Continue with controls", continue_controls_count)
    col6.metric("Scale", scale_count)
    col7.metric("Scale with monitoring", scale_monitoring_count)
    col8.metric("Review later", review_later_count)

    st.subheader("Organisation-Level Decision Summary")
    st.dataframe(
        build_decision_org_table(org_summaries), hide_index=True, use_container_width=True
    )

    st.subheader("Build-Level Decision Summary")
    st.write(
        "This shows how workflows related to Build 1, Build 4, Build 5, and Build 6 "
        "are performing on decision outcomes across the portfolio."
    )
    st.dataframe(
        build_decision_build_table(build_summaries), hide_index=True, use_container_width=True
    )

    st.subheader("Prioritised Follow-up Decision List")
    st.write(
        "Workflows are listed from most to least urgent, based on decision outcome, "
        "risk incidents, near misses, and quality issues."
    )
    st.dataframe(
        build_decision_follow_up_table(prioritised), hide_index=True, use_container_width=True
    )

    st.subheader("Consulting Interpretation")
    st.markdown(
        """
This tracker turns adoption evidence into practical consulting decisions. It helps avoid vague
recommendations by showing which workflows should stop, pause, continue, continue with controls,
or scale based on training, confidence, quality, and risk signals.

- **Stop** — the workflow has been formally stopped. No further expansion is appropriate
  until the adoption decision has been revisited and revised boundaries are in place.
- **Pause** — the pilot has been paused. A structured review of governance and workflow
  controls is needed before rollout can resume.
- **Continue with controls** — risk incidents, multiple near misses, or significant quality
  issues are present. The workflow may continue, but stronger quality assurance, incident
  logging, or governance review controls are required.
- **Scale with monitoring** — positive training, confidence, and risk evidence supports
  cautious scaling, with continued monitoring to confirm that quality and safety hold.
- **Scale** — all adoption indicators are strong. The workflow may scale under continued
  periodic monitoring.
- **Continue** — the pilot is proceeding within its agreed scope. Continue monitoring and
  review at the next adoption period.
- **Review later** — evidence is not yet strong enough for a clear scale or stop decision.
  Collect more data before making a wider rollout recommendation.

> Decision outcomes are synthetic consulting indicators based on training, confidence,
> quality, and risk signals. They should support, not replace, direct client judgement.
        """
    )


# ---------------------------------------------------------------------------
# Phase 7 helpers
# ---------------------------------------------------------------------------

_ORG_SELECTOR_OPTIONS = {
    "Portfolio — All Organisations": None,
    "BrightPath Skills Training": "ORG001",
    "Northside Community Advice": "ORG002",
    "Greenacre Dental Group": "ORG003",
}


def render_phase_7(adoption_records: list[dict]) -> None:
    """Render Phase 7: Client Follow-up Report Builder."""
    st.title(PAGE_TITLE)
    st.subheader("Phase 7 — Client Follow-up Report Builder")
    st.write(
        "This report builder converts synthetic adoption evidence from Phases 1–6 "
        "into a structured Markdown follow-up report."
    )
    st.info(
        "This report builder uses synthetic portfolio data only. It demonstrates how a "
        "consultant could turn adoption evidence into a structured follow-up report."
    )

    selected_label = st.selectbox(
        "Select report scope",
        list(_ORG_SELECTOR_OPTIONS.keys()),
        index=0,
    )
    organisation_id = _ORG_SELECTOR_OPTIONS[selected_label]

    report_markdown = build_full_follow_up_report(adoption_records, organisation_id=organisation_id)

    st.subheader("Generated Report Preview")
    st.markdown(report_markdown)

    st.divider()
    st.download_button(
        label="Download Markdown Report",
        data=report_markdown,
        file_name="ai_adoption_follow_up_report.md",
        mime="text/markdown",
    )


# ---------------------------------------------------------------------------
# Phase 8 helpers
# ---------------------------------------------------------------------------


def render_phase_8(adoption_records: list[dict]) -> None:
    """Render Phase 8: Export Centre and Completion Review."""
    st.title(PAGE_TITLE)
    st.subheader("Phase 8 — Export Centre and Completion Review")
    st.write(
        "This export centre packages all synthetic adoption evidence from Phases 1–7 "
        "into downloadable formats for consulting review and portfolio demonstration."
    )
    st.info(
        "This export centre uses synthetic portfolio data only. It demonstrates how a consultant "
        "could package adoption evidence for review and follow-up."
    )

    completion = build_completion_summary(adoption_records)

    st.subheader("Completion Summary")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Organisations", completion["total_organisations"])
    col2.metric("Workflows tracked", completion["total_workflows"])
    col3.metric("Scale / Scale with monitoring", completion["scale_or_scale_with_monitoring_count"])
    col4.metric("Stop / Pause", completion["stop_or_pause_count"])

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Continue / Continue with controls", completion["continue_or_continue_with_controls_count"])
    col6.metric("Governance review required", completion["governance_review_count"])
    col7.metric("Weekly hrs saved (synthetic)", f"{completion['total_weekly_hours_saved']:.1f}")
    col8.metric("Annual hrs saved (synthetic)", f"{completion['total_annual_hours_saved']:.1f}")

    st.subheader("Export Options")

    markdown_text = export_markdown_report(adoption_records)
    csv_text = export_csv_text(adoption_records)
    json_text = export_json_text(adoption_records)

    col_md, col_csv, col_json = st.columns(3)

    with col_md:
        st.download_button(
            label="Download Markdown Report",
            data=markdown_text,
            file_name=build_export_filename("build_7_ai_adoption_report", "md"),
            mime="text/markdown",
        )

    with col_csv:
        st.download_button(
            label="Download CSV Evidence Table",
            data=csv_text,
            file_name=build_export_filename("build_7_ai_adoption_export", "csv"),
            mime="text/csv",
        )

    with col_json:
        st.download_button(
            label="Download JSON Evidence Pack",
            data=json_text,
            file_name=build_export_filename("build_7_ai_adoption_export", "json"),
            mime="application/json",
        )

    col_pdf, col_png, _ = st.columns(3)

    with col_pdf:
        try:
            from logic.export_centre import export_pdf_bytes
            pdf_bytes = export_pdf_bytes(markdown_text)
            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name=build_export_filename("build_7_ai_adoption_report", "pdf"),
                mime="application/pdf",
            )
        except ImportError:
            st.caption("PDF export requires reportlab (not installed).")

    with col_png:
        try:
            from logic.export_centre import export_summary_chart_png_bytes
            png_bytes = export_summary_chart_png_bytes(adoption_records)
            st.download_button(
                label="Download PNG Summary Chart",
                data=png_bytes,
                file_name=build_export_filename("build_7_decision_summary_chart", "png"),
                mime="image/png",
            )
        except ImportError:
            st.caption("Chart export requires matplotlib (not installed).")

    st.subheader("Completion Review")

    review_text = build_completion_review_text(adoption_records)
    st.markdown(review_text)

    st.subheader("Consulting Interpretation")
    st.markdown(
        """
The export centre turns Build 7 from an analysis dashboard into a reusable consulting asset.
It packages adoption evidence, decisions, and follow-up material into formats that could support
a client review, internal portfolio demonstration, or future productised workflow.

- **Markdown** — a structured consultant-facing follow-up report ready to share with a client.
- **CSV** — a flat evidence table combining all analytical engines for review or further analysis.
- **JSON** — a machine-readable evidence pack suitable for integration with other tools.
- **PDF** — a basic PDF version of the Markdown report for distribution without formatting tools.
- **PNG chart** — a simple decision outcome summary chart for use in presentations or notes.

> All exports use synthetic demo data only. No real client, learner, HR, safeguarding,
> personal, confidential, or regulated data is included in any export.
        """
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Run the Build 7 Streamlit app."""
    selected_phase = render_sidebar()

    adoption_records = get_synthetic_adoption_metrics()
    organisations = get_synthetic_organisations()
    review_decisions = get_synthetic_review_decisions()

    if selected_phase == PHASE_NAVIGATION[7]:
        render_phase_8(adoption_records)
    elif selected_phase == PHASE_NAVIGATION[6]:
        render_phase_7(adoption_records)
    elif selected_phase == PHASE_NAVIGATION[5]:
        render_phase_6(adoption_records)
    elif selected_phase == PHASE_NAVIGATION[4]:
        render_phase_5(adoption_records)
    elif selected_phase == PHASE_NAVIGATION[3]:
        render_phase_4(adoption_records)
    elif selected_phase == PHASE_NAVIGATION[2]:
        render_phase_3(adoption_records)
    elif selected_phase == PHASE_NAVIGATION[1]:
        render_phase_2(adoption_records)
    else:
        render_phase_1(adoption_records, organisations, review_decisions)


if __name__ == "__main__":
    main()
