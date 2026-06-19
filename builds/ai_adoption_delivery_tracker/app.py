"""Build 8 Streamlit scaffold for synthetic AI adoption delivery tracking."""

import streamlit as st

from data.synthetic_implementation_data import (
    get_synthetic_client_checkins,
    get_synthetic_delivery_organisations,
    get_synthetic_implementation_actions,
)
from logic.implementation_actions import (
    calculate_action_counts_by_priority,
    calculate_action_counts_by_status,
    get_actions_by_organisation,
    summarise_phase_1_delivery_actions,
    validate_all_implementation_actions,
)
from logic.action_tracker import (
    add_action_recommendations,
    build_all_action_tracker_summaries,
    prioritise_actions,
    summarise_actions_by_organisation,
    summarise_actions_by_related_build,
)
from logic.blocker_review import (
    add_blocker_recommendations,
    build_all_blocker_review_summaries,
    prioritise_blockers_for_resolution,
    summarise_blockers_by_organisation,
    summarise_blockers_by_related_build,
)
from logic.governance_tracker import (
    add_governance_recommendations,
    build_all_governance_summaries,
    prioritise_governance_actions,
    summarise_governance_by_organisation,
    summarise_governance_by_related_build,
)
from logic.training_followup import (
    add_training_followup_recommendations,
    build_all_training_followup_summaries,
    prioritise_training_followup_actions,
    summarise_training_followup_by_organisation,
    summarise_training_followup_by_owner_role,
    summarise_training_followup_by_related_build,
)
from logic.client_checkin import (
    build_client_checkin_markdown,
    build_client_checkin_summary,
    generate_checkin_recommendation,
    get_actions_for_organisation,
    identify_checkin_attention_items,
)
from logic.export_centre import (
    build_completion_review_text,
    build_completion_summary,
    build_export_filename,
    export_csv_text,
    export_json_text,
    export_markdown_report,
    export_pdf_bytes,
    export_summary_chart_png_bytes,
)
from logic.progress_report import build_full_progress_report


PAGE_TITLE = "Build 8 — AI Adoption Delivery and Implementation Tracker"

PHASE_NAVIGATION = [
    "1. Implementation Action Setup",
    "2. Action Tracker",
    "3. Blocker and Dependency Review",
    "4. Governance Sign-off Tracker",
    "5. Training Follow-up Plan",
    "6. Client Check-in Summary",
    "7. Implementation Progress Report",
    "8. Export Centre",
]

ACTIVE_PHASES = PHASE_NAVIGATION[:8]

STATUS_ORDER = [
    "Not started",
    "In progress",
    "Blocked",
    "Completed",
    "Deferred",
]

PRIORITY_ORDER = ["Critical", "High", "Medium", "Low"]


st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="✓",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_styles() -> None:
    """Apply a compact operational dashboard style."""
    st.markdown(
        """
        <style>
        :root {
            --ink: #18242b;
            --muted: #5d6a70;
            --line: #dce4e5;
            --surface: #f5f7f7;
            --teal: #0f6b64;
            --coral: #c95d44;
            --green: #357654;
            --amber: #9a651b;
        }

        .stApp {
            background: #ffffff;
            color: var(--ink);
        }

        [data-testid="stAppViewContainer"] > .main .block-container {
            max-width: 1480px;
            padding-top: 2.2rem;
            padding-bottom: 4rem;
        }

        [data-testid="stSidebar"] {
            background: #1a2744 !important;
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem;
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] div { color: #cbd5e1 !important; }
        section[data-testid="stSidebar"] strong,
        section[data-testid="stSidebar"] b { color: #f1f5f9 !important; }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; }
        section[data-testid="stSidebar"] hr { border-color: #334155 !important; }
        section[data-testid="stSidebar"] .stRadio label { color: #e2e8f0 !important; }
        section[data-testid="stSidebar"] [data-testid="stCaption"] { color: #94a3b8 !important; }

        h1, h2, h3 {
            color: var(--ink);
            letter-spacing: 0;
        }

        h1 {
            font-size: 2.15rem;
            line-height: 1.15;
            margin-bottom: 0.55rem;
        }

        h2 {
            font-size: 1.25rem;
            margin-top: 2.25rem;
        }

        h3 {
            font-size: 1rem;
        }

        .phase-kicker {
            color: var(--teal);
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }

        .page-intro {
            color: var(--muted);
            font-size: 1.04rem;
            line-height: 1.6;
            max-width: 900px;
            margin-bottom: 0.8rem;
        }

        .scope-note {
            border-left: 3px solid var(--teal);
            background: var(--surface);
            color: #405056;
            padding: 0.8rem 1rem;
            margin: 1.2rem 0 1.7rem;
        }

        [data-testid="stMetric"] {
            border: 1px solid var(--line);
            border-radius: 6px;
            background: #ffffff;
            padding: 0.85rem 1rem;
            min-height: 108px;
        }

        [data-testid="stMetricLabel"] {
            color: var(--muted);
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: var(--ink);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 6px;
            overflow: hidden;
        }

        div[data-baseweb="select"] > div {
            border-radius: 6px;
        }

        .validation-ok {
            border-left: 3px solid var(--green);
            background: #f3f8f5;
            color: #28563e;
            padding: 0.85rem 1rem;
        }

        .connection-note {
            color: var(--muted);
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }

        button[kind="secondary"][disabled] {
            border-color: var(--line);
            color: #798489;
            background: #f4f6f5;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> str:
    """Render active and future delivery phases and return the selected page."""
    with st.sidebar:
        st.markdown("## Build 8")
        st.caption("AI Adoption Delivery and Implementation Tracker")
        st.divider()
        st.markdown("**Delivery workflow**")
        selected_phase = st.radio(
            "Active phase",
            ACTIVE_PHASES,
            index=0,
            label_visibility="collapsed",
        )
        for phase in PHASE_NAVIGATION[len(ACTIVE_PHASES):]:
            st.button(phase, disabled=True, use_container_width=True)
        st.divider()
        st.markdown("**Phase status**")
        st.caption("Phases 1–8 active")
        st.progress(len(ACTIVE_PHASES) / len(PHASE_NAVIGATION))
        st.caption("8 of 8 phases")
        st.divider()
        st.caption(
            "Synthetic/demo data only. No real client, personal, learner, "
            "safeguarding, HR, confidential, or regulated data."
        )
    return selected_phase


def build_organisation_table(organisations: list[dict]) -> list[dict]:
    """Prepare organisation data for a concise display."""
    return [
        {
            "Organisation": organisation["organisation_name"],
            "Sector": organisation["sector"],
            "Staff": organisation["staff_count"],
            "Implementation stage": organisation["implementation_stage"],
        }
        for organisation in organisations
    ]


def build_action_table(actions: list[dict]) -> list[dict]:
    """Prepare implementation actions for the Phase 1 action register."""
    return [
        {
            "ID": action["action_id"],
            "Organisation": action["organisation_name"],
            "Action": action["action_title"],
            "Workflow": action["workflow_name"],
            "Build": action["related_build"],
            "Owner": action["owner_role"],
            "Priority": action["priority"],
            "Status": action["status"],
            "Due (days)": action["due_in_days"],
            "Blocker": action["blocker"] or "None logged",
            "Governance": action["governance_signoff_required"],
            "Training": action["training_followup_required"],
            "Check-in": action["client_checkin_required"],
            "Evidence": action["evidence_note"],
        }
        for action in actions
    ]


def build_checkin_table(
    checkins: list[dict],
    organisations: list[dict],
) -> list[dict]:
    """Prepare client check-ins with readable organisation names."""
    organisation_names = {
        organisation["organisation_id"]: organisation["organisation_name"]
        for organisation in organisations
    }
    return [
        {
            "Organisation": organisation_names.get(
                checkin["organisation_id"],
                checkin["organisation_id"],
            ),
            "Period": checkin["checkin_period"],
            "Focus": checkin["checkin_focus"],
            "Summary": checkin["summary"],
            "Next review focus": checkin["next_review_focus"],
        }
        for checkin in checkins
    ]


def render_headline_metrics(summary: dict) -> None:
    """Render the most useful delivery signals at a glance."""
    open_actions = (
        summary["not_started_count"]
        + summary["in_progress_count"]
        + summary["blocked_count"]
    )

    columns = st.columns(6)
    columns[0].metric("Total actions", summary["total_actions"])
    columns[1].metric("Open actions", open_actions)
    columns[2].metric("In progress", summary["in_progress_count"])
    columns[3].metric("Blocked", summary["blocked_count"])
    columns[4].metric("Completed", summary["completed_count"])
    columns[5].metric("Critical", summary["critical_count"])


def render_delivery_summary(summary: dict) -> None:
    """Render calculated status, priority, and follow-up counts."""
    status_counts = [
        {"Status": status, "Actions": summary[f"{status.lower().replace(' ', '_')}_count"]}
        for status in STATUS_ORDER
    ]
    priority_counts = [
        {"Priority": priority, "Actions": summary[f"{priority.lower()}_count"]}
        for priority in PRIORITY_ORDER
    ]

    status_col, priority_col = st.columns(2)
    with status_col:
        st.markdown("#### Status distribution")
        st.dataframe(
            status_counts,
            hide_index=True,
            use_container_width=True,
            height=212,
        )

    with priority_col:
        st.markdown("#### Priority distribution")
        st.dataframe(
            priority_counts,
            hide_index=True,
            use_container_width=True,
            height=212,
        )

    st.markdown("#### Required follow-up")
    followup_columns = st.columns(3)
    followup_columns[0].metric(
        "Governance sign-offs",
        summary["governance_signoff_required_count"],
    )
    followup_columns[1].metric(
        "Training follow-ups",
        summary["training_followup_required_count"],
    )
    followup_columns[2].metric(
        "Client check-ins",
        summary["client_checkin_required_count"],
    )


def render_validation_summary(validation: dict) -> None:
    """Render validation health for the synthetic action register."""
    columns = st.columns(3)
    columns[0].metric("Actions checked", validation["total_actions"])
    columns[1].metric("Valid actions", validation["valid_actions"])
    columns[2].metric(
        "Actions with warnings",
        validation["actions_with_warnings"],
    )

    if validation["warnings"]:
        st.warning("Validation warnings were found in the synthetic action data.")
        for warning in validation["warnings"]:
            st.write(f"- {warning}")
    else:
        st.markdown(
            '<div class="validation-ok">'
            "All synthetic implementation actions passed the Phase 1 validation checks."
            "</div>",
            unsafe_allow_html=True,
        )


def render_portfolio_connections() -> None:
    """Explain how Build 8 turns earlier build outputs into delivery work."""
    connections = [
        {
            "Build": "Build 1",
            "Earlier output": "Readiness findings and workflow opportunities",
            "Build 8 delivery use": "Assign owners and actions for approved pilot workflows",
        },
        {
            "Build": "Build 4",
            "Earlier output": "Training plans and confidence-building support",
            "Build 8 delivery use": "Track coaching, refresher, and adoption support actions",
        },
        {
            "Build": "Build 5",
            "Earlier output": "Consulting findings and client recommendations",
            "Build 8 delivery use": "Turn report recommendations into owned follow-up work",
        },
        {
            "Build": "Build 6",
            "Earlier output": "Governance gaps and control recommendations",
            "Build 8 delivery use": "Track sign-offs, controls, blockers, and approval dependencies",
        },
        {
            "Build": "Build 7",
            "Earlier output": "ROI evidence and stop, continue, review, or scale decisions",
            "Build 8 delivery use": "Convert adoption decisions into deadlines and implementation actions",
        },
    ]
    st.dataframe(connections, hide_index=True, use_container_width=True)
    st.markdown(
        '<p class="connection-note">'
        "Build 8 is the delivery layer: it turns evidence and recommendations into "
        "specific work with an owner, due date, status, blocker, and follow-up need."
        "</p>",
        unsafe_allow_html=True,
    )


def render_phase_1(
    organisations: list[dict],
    actions: list[dict],
    checkins: list[dict],
) -> None:
    """Render Phase 1: synthetic implementation action setup."""
    summary = summarise_phase_1_delivery_actions(actions)
    validation = validate_all_implementation_actions(actions)

    st.markdown('<div class="phase-kicker">Delivery control / Phase 1</div>', unsafe_allow_html=True)
    st.title(PAGE_TITLE)
    st.markdown(
        '<p class="page-intro">'
        "This tool helps track implementation actions after AI readiness, governance, "
        "training, reporting, and adoption review work."
        "</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="scope-note">'
        "<strong>Phase 1:</strong> synthetic implementation action setup. "
        "Advanced scoring, charts, reports, exports, uploads, and external APIs "
        "are intentionally not included."
        "</div>",
        unsafe_allow_html=True,
    )

    render_headline_metrics(summary)

    st.subheader("Synthetic Organisation Overview")
    st.dataframe(
        build_organisation_table(organisations),
        hide_index=True,
        use_container_width=True,
        height=144,
    )

    st.subheader("Implementation Action Register")
    organisation_options = {
        "All organisations": None,
        **{
            organisation["organisation_name"]: organisation["organisation_id"]
            for organisation in organisations
        },
    }
    selected_organisation = st.selectbox(
        "Organisation scope",
        list(organisation_options),
    )
    selected_id = organisation_options[selected_organisation]
    visible_actions = (
        actions
        if selected_id is None
        else get_actions_by_organisation(actions, selected_id)
    )
    st.caption(f"Showing {len(visible_actions)} of {len(actions)} synthetic actions.")
    st.dataframe(
        build_action_table(visible_actions),
        hide_index=True,
        use_container_width=True,
        height=510,
        column_config={
            "ID": st.column_config.TextColumn(width="small"),
            "Organisation": st.column_config.TextColumn(width="medium"),
            "Action": st.column_config.TextColumn(width="large"),
            "Workflow": st.column_config.TextColumn(width="medium"),
            "Build": st.column_config.TextColumn(width="small"),
            "Owner": st.column_config.TextColumn(width="medium"),
            "Priority": st.column_config.TextColumn(width="small"),
            "Status": st.column_config.TextColumn(width="small"),
            "Due (days)": st.column_config.NumberColumn(format="%d"),
            "Blocker": st.column_config.TextColumn(width="large"),
            "Governance": st.column_config.CheckboxColumn(width="small"),
            "Training": st.column_config.CheckboxColumn(width="small"),
            "Check-in": st.column_config.CheckboxColumn(width="small"),
            "Evidence": st.column_config.TextColumn(width="large"),
        },
    )

    st.subheader("Phase 1 Delivery Summary")
    render_delivery_summary(summary)

    st.subheader("Validation Summary")
    render_validation_summary(validation)

    st.subheader("Synthetic Client Check-ins")
    st.dataframe(
        build_checkin_table(checkins, organisations),
        hide_index=True,
        use_container_width=True,
        height=280,
        column_config={
            "Organisation": st.column_config.TextColumn(width="medium"),
            "Period": st.column_config.TextColumn(width="small"),
            "Focus": st.column_config.TextColumn(width="medium"),
            "Summary": st.column_config.TextColumn(width="large"),
            "Next review focus": st.column_config.TextColumn(width="large"),
        },
    )

    st.subheader("Portfolio Connection")
    render_portfolio_connections()


def build_tracker_organisation_table(summaries: list[dict]) -> list[dict]:
    """Prepare organisation-level action tracker summaries for display."""
    return [
        {
            "Organisation": summary["organisation_name"],
            "Total": summary["total_actions"],
            "Completed": summary["completed_count"],
            "Blocked": summary["blocked_count"],
            "Active": summary["active_count"],
            "Waiting": summary["waiting_count"],
            "Deferred": summary["deferred_count"],
            "Critical attention": summary["critical_attention_count"],
            "High attention": summary["high_attention_count"],
            "Average score": summary["average_action_score"],
        }
        for summary in summaries
    ]


def build_tracker_related_build_table(summaries: list[dict]) -> list[dict]:
    """Prepare related-build action tracker summaries for display."""
    return [
        {
            "Related build": summary["related_build"],
            "Total": summary["total_actions"],
            "Completed": summary["completed_count"],
            "Blocked": summary["blocked_count"],
            "Active": summary["active_count"],
            "Waiting": summary["waiting_count"],
            "Deferred": summary["deferred_count"],
            "Critical attention": summary["critical_attention_count"],
            "High attention": summary["high_attention_count"],
            "Average score": summary["average_action_score"],
        }
        for summary in summaries
    ]


def build_prioritised_action_table(summaries: list[dict]) -> list[dict]:
    """Prepare the scored and prioritised action list for Streamlit."""
    return [
        {
            "Organisation": summary["organisation_name"],
            "Workflow": summary["workflow_name"],
            "Related build": summary["related_build"],
            "Action": summary["action_title"],
            "Owner": summary["owner_role"],
            "Priority": summary["priority"],
            "Status": summary["status"],
            "Due (days)": summary["due_in_days"],
            "Due window": summary["due_window"],
            "Delivery state": summary["delivery_state"],
            "Attention level": summary["attention_level"],
            "Action score": summary["action_score"],
            "Recommendation": summary["action_recommendation"],
        }
        for summary in summaries
    ]


def render_action_tracker_metrics(summaries: list[dict]) -> None:
    """Render Phase 2 action tracker overview metrics."""
    total_actions = len(summaries)
    completed_count = sum(
        summary["delivery_state"] == "Completed" for summary in summaries
    )
    blocked_count = sum(
        summary["delivery_state"] == "Blocked" for summary in summaries
    )
    active_count = sum(
        summary["delivery_state"] == "Active" for summary in summaries
    )
    waiting_count = sum(
        summary["delivery_state"] == "Waiting" for summary in summaries
    )
    deferred_count = sum(
        summary["delivery_state"] == "Deferred" for summary in summaries
    )
    critical_attention_count = sum(
        summary["attention_level"] == "Critical attention"
        for summary in summaries
    )
    high_attention_count = sum(
        summary["attention_level"] == "High attention"
        for summary in summaries
    )

    first_row = st.columns(4)
    first_row[0].metric("Total actions", total_actions)
    first_row[1].metric("Completed", completed_count)
    first_row[2].metric("Blocked", blocked_count)
    first_row[3].metric("Active", active_count)

    second_row = st.columns(4)
    second_row[0].metric("Waiting", waiting_count)
    second_row[1].metric("Deferred", deferred_count)
    second_row[2].metric("Critical attention", critical_attention_count)
    second_row[3].metric("High attention", high_attention_count)


def render_phase_2(actions: list[dict]) -> None:
    """Render Phase 2: Action Tracker and Status Engine."""
    tracker_summaries = build_all_action_tracker_summaries(actions)
    organisation_summaries = summarise_actions_by_organisation(actions)
    related_build_summaries = summarise_actions_by_related_build(actions)
    prioritised_summaries = add_action_recommendations(
        prioritise_actions(actions)
    )

    st.markdown(
        '<div class="phase-kicker">Delivery control / Phase 2</div>',
        unsafe_allow_html=True,
    )
    st.title("Action Tracker and Status Engine")
    st.markdown(
        '<p class="page-intro">'
        "Prioritise implementation work by delivery pressure, blocker status, "
        "owner, due window, and portfolio source."
        "</p>",
        unsafe_allow_html=True,
    )
    st.info(
        "This section uses synthetic portfolio data only. It demonstrates how a "
        "consultant could prioritise AI adoption delivery actions after audit, "
        "governance, training, reporting, and adoption review work."
    )

    st.subheader("Action Tracker Overview")
    render_action_tracker_metrics(tracker_summaries)

    st.subheader("Organisation-Level Action Summary")
    st.dataframe(
        build_tracker_organisation_table(organisation_summaries),
        hide_index=True,
        use_container_width=True,
        height=145,
    )

    st.subheader("Related-Build Action Summary")
    st.dataframe(
        build_tracker_related_build_table(related_build_summaries),
        hide_index=True,
        use_container_width=True,
        height=213,
    )

    st.subheader("Prioritised Action List")
    st.caption(
        "Actions are ordered by score, recorded status priority, and due days."
    )
    st.dataframe(
        build_prioritised_action_table(prioritised_summaries),
        hide_index=True,
        use_container_width=True,
        height=560,
        column_config={
            "Organisation": st.column_config.TextColumn(width="medium"),
            "Workflow": st.column_config.TextColumn(width="medium"),
            "Related build": st.column_config.TextColumn(width="small"),
            "Action": st.column_config.TextColumn(width="large"),
            "Owner": st.column_config.TextColumn(width="medium"),
            "Priority": st.column_config.TextColumn(width="small"),
            "Status": st.column_config.TextColumn(width="small"),
            "Due (days)": st.column_config.NumberColumn(format="%d"),
            "Due window": st.column_config.TextColumn(width="small"),
            "Delivery state": st.column_config.TextColumn(width="small"),
            "Attention level": st.column_config.TextColumn(width="medium"),
            "Action score": st.column_config.NumberColumn(format="%d"),
            "Recommendation": st.column_config.TextColumn(width="large"),
        },
    )

    st.subheader("Consulting Interpretation")
    st.markdown(
        """
The action tracker turns AI adoption recommendations into delivery work. It helps a
consultant identify blocked actions, urgent tasks, ownership gaps, and follow-up items
that need attention before implementation can progress safely.
        """
    )


def build_blocker_organisation_table(summaries: list[dict]) -> list[dict]:
    """Prepare organisation-level blocker exposure summaries for display."""
    return [
        {
            "Organisation": summary["organisation_name"],
            "Total": summary["total_actions"],
            "Blocked actions": summary["blocked_action_count"],
            "Critical blockers": summary["critical_blocker_count"],
            "High blockers": summary["high_blocker_count"],
            "Escalations": summary["escalation_required_count"],
            "High delivery risk": summary["high_delivery_risk_count"],
            "Governance dependencies": summary["governance_dependency_count"],
            "Training dependencies": summary["training_dependency_count"],
            "Client dependencies": summary["client_checkin_dependency_count"],
        }
        for summary in summaries
    ]


def build_blocker_related_build_table(summaries: list[dict]) -> list[dict]:
    """Prepare related-build blocker exposure summaries for display."""
    return [
        {
            "Related build": summary["related_build"],
            "Total": summary["total_actions"],
            "Blocked actions": summary["blocked_action_count"],
            "Critical blockers": summary["critical_blocker_count"],
            "High blockers": summary["high_blocker_count"],
            "Escalations": summary["escalation_required_count"],
            "High delivery risk": summary["high_delivery_risk_count"],
            "Governance dependencies": summary["governance_dependency_count"],
            "Training dependencies": summary["training_dependency_count"],
            "Client dependencies": summary["client_checkin_dependency_count"],
        }
        for summary in summaries
    ]


def build_prioritised_blocker_table(summaries: list[dict]) -> list[dict]:
    """Prepare the prioritised blocker resolution list for Streamlit."""
    return [
        {
            "Organisation": summary["organisation_name"],
            "Workflow": summary["workflow_name"],
            "Related build": summary["related_build"],
            "Action": summary["action_title"],
            "Owner": summary["owner_role"],
            "Priority": summary["priority"],
            "Status": summary["status"],
            "Due (days)": summary["due_in_days"],
            "Blocker type": summary["blocker_type"],
            "Blocker severity": summary["blocker_severity"],
            "Dependency need": summary["dependency_need"],
            "Delivery risk": summary["delivery_risk_level"],
            "Escalation required": summary["requires_escalation"],
            "Recommendation": summary["blocker_recommendation"],
        }
        for summary in summaries
    ]


def render_blocker_review_metrics(summaries: list[dict]) -> None:
    """Render Phase 3 blocker and delivery risk overview metrics."""
    metrics = {
        "Total actions": len(summaries),
        "Blocked actions": sum(
            summary["has_blocker"] for summary in summaries
        ),
        "Critical blockers": sum(
            summary["blocker_severity"] == "Critical blocker"
            for summary in summaries
        ),
        "High blockers": sum(
            summary["blocker_severity"] == "High blocker"
            for summary in summaries
        ),
        "Escalation required": sum(
            summary["requires_escalation"] for summary in summaries
        ),
        "High delivery risk": sum(
            summary["delivery_risk_level"] == "High delivery risk"
            for summary in summaries
        ),
    }
    columns = st.columns(6)
    for column, (label, value) in zip(columns, metrics.items()):
        column.metric(label, value)


def render_phase_3(actions: list[dict]) -> None:
    """Render Phase 3: Blocker, Risk, and Dependency Review."""
    blocker_summaries = build_all_blocker_review_summaries(actions)
    organisation_summaries = summarise_blockers_by_organisation(actions)
    related_build_summaries = summarise_blockers_by_related_build(actions)
    prioritised_summaries = add_blocker_recommendations(
        prioritise_blockers_for_resolution(actions)
    )

    st.markdown(
        '<div class="phase-kicker">Delivery control / Phase 3</div>',
        unsafe_allow_html=True,
    )
    st.title("Blocker, Risk, and Dependency Review")
    st.markdown(
        '<p class="page-intro">'
        "Identify implementation constraints, dependency exposure, delivery risk, "
        "and actions that require escalation before rollout is affected."
        "</p>",
        unsafe_allow_html=True,
    )
    st.info(
        "This section uses synthetic portfolio data only. It demonstrates how a "
        "consultant could identify blocked implementation actions, delivery risks, "
        "and dependencies before rollout progress is affected."
    )

    st.subheader("Blocker and Risk Overview")
    render_blocker_review_metrics(blocker_summaries)

    st.subheader("Organisation-Level Blocker Exposure")
    st.dataframe(
        build_blocker_organisation_table(organisation_summaries),
        hide_index=True,
        use_container_width=True,
        height=145,
    )

    st.subheader("Related-Build Blocker Exposure")
    st.dataframe(
        build_blocker_related_build_table(related_build_summaries),
        hide_index=True,
        use_container_width=True,
        height=213,
    )

    st.subheader("Prioritised Blocker Resolution List")
    st.caption(
        "Escalation items appear first, followed by blocker severity, delivery "
        "risk, due pressure, and action priority."
    )
    st.dataframe(
        build_prioritised_blocker_table(prioritised_summaries),
        hide_index=True,
        use_container_width=True,
        height=560,
        column_config={
            "Organisation": st.column_config.TextColumn(width="medium"),
            "Workflow": st.column_config.TextColumn(width="medium"),
            "Related build": st.column_config.TextColumn(width="small"),
            "Action": st.column_config.TextColumn(width="large"),
            "Owner": st.column_config.TextColumn(width="medium"),
            "Priority": st.column_config.TextColumn(width="small"),
            "Status": st.column_config.TextColumn(width="small"),
            "Due (days)": st.column_config.NumberColumn(format="%d"),
            "Blocker type": st.column_config.TextColumn(width="medium"),
            "Blocker severity": st.column_config.TextColumn(width="medium"),
            "Dependency need": st.column_config.TextColumn(width="medium"),
            "Delivery risk": st.column_config.TextColumn(width="medium"),
            "Escalation required": st.column_config.CheckboxColumn(
                width="small"
            ),
            "Recommendation": st.column_config.TextColumn(width="large"),
        },
    )

    st.subheader("Consulting Interpretation")
    st.markdown(
        """
This review helps a consultant find the delivery actions most likely to slow down
or weaken AI adoption. It separates simple task tracking from deeper delivery risk
by highlighting blockers, dependencies, escalation needs, and ownership issues.
        """
    )


def build_governance_organisation_table(
    summaries: list[dict],
) -> list[dict]:
    """Prepare organisation-level governance workload for display."""
    return [
        {
            "Organisation": summary["organisation_name"],
            "Total": summary["total_actions"],
            "Sign-off required": summary["signoff_required_count"],
            "Urgent sign-off": summary["urgent_signoff_count"],
            "Control blocked": summary["control_blocked_count"],
            "Control needs review": summary["control_needs_review_count"],
            "High governance risk": summary["high_governance_risk_count"],
            "Senior approval": summary["senior_approval_needed_count"],
            "Governance lead review": (
                summary["governance_lead_review_needed_count"]
            ),
        }
        for summary in summaries
    ]


def build_governance_related_build_table(
    summaries: list[dict],
) -> list[dict]:
    """Prepare related-build governance workload for display."""
    return [
        {
            "Related build": summary["related_build"],
            "Total": summary["total_actions"],
            "Sign-off required": summary["signoff_required_count"],
            "Urgent sign-off": summary["urgent_signoff_count"],
            "Control blocked": summary["control_blocked_count"],
            "Control needs review": summary["control_needs_review_count"],
            "High governance risk": summary["high_governance_risk_count"],
            "Senior approval": summary["senior_approval_needed_count"],
            "Governance lead review": (
                summary["governance_lead_review_needed_count"]
            ),
        }
        for summary in summaries
    ]


def build_prioritised_governance_table(
    summaries: list[dict],
) -> list[dict]:
    """Prepare the prioritised governance action list for Streamlit."""
    return [
        {
            "Organisation": summary["organisation_name"],
            "Workflow": summary["workflow_name"],
            "Related build": summary["related_build"],
            "Action": summary["action_title"],
            "Owner": summary["owner_role"],
            "Priority": summary["priority"],
            "Status": summary["status"],
            "Due (days)": summary["due_in_days"],
            "Sign-off urgency": summary["signoff_urgency"],
            "Control area": summary["control_area"],
            "Control readiness": summary["control_readiness"],
            "Governance owner need": summary["governance_owner_need"],
            "Governance delivery risk": summary["governance_delivery_risk"],
            "Recommendation": summary["governance_recommendation"],
        }
        for summary in summaries
    ]


def render_governance_metrics(summaries: list[dict]) -> None:
    """Render Phase 4 governance overview metrics."""
    metrics = {
        "Total actions": len(summaries),
        "Sign-off required": sum(
            summary["governance_signoff_required"] for summary in summaries
        ),
        "Urgent sign-off": sum(
            summary["signoff_urgency"] == "Urgent sign-off"
            for summary in summaries
        ),
        "Control blocked": sum(
            summary["control_readiness"] == "Control blocked"
            for summary in summaries
        ),
        "Controls need review": sum(
            summary["control_readiness"] == "Control needs review"
            for summary in summaries
        ),
        "High governance risk": sum(
            summary["governance_delivery_risk"]
            == "High governance delivery risk"
            for summary in summaries
        ),
        "Senior approval needed": sum(
            summary["governance_owner_need"] == "Senior approval needed"
            for summary in summaries
        ),
    }
    columns = st.columns(7)
    for column, (label, value) in zip(columns, metrics.items()):
        column.metric(label, value)


def render_phase_4(actions: list[dict]) -> None:
    """Render Phase 4: Governance Sign-off and Control Tracker."""
    governance_summaries = build_all_governance_summaries(actions)
    organisation_summaries = summarise_governance_by_organisation(actions)
    related_build_summaries = summarise_governance_by_related_build(actions)
    prioritised_summaries = add_governance_recommendations(
        prioritise_governance_actions(actions)
    )

    st.markdown(
        '<div class="phase-kicker">Delivery control / Phase 4</div>',
        unsafe_allow_html=True,
    )
    st.title("Governance Sign-off and Control Tracker")
    st.markdown(
        '<p class="page-intro">'
        "Track approval urgency, control readiness, governance ownership, and "
        "delivery risks before implementation moves forward."
        "</p>",
        unsafe_allow_html=True,
    )
    st.info(
        "This section uses synthetic portfolio data only. It demonstrates how a "
        "consultant could track governance sign-offs, control readiness, and "
        "approval risks during AI implementation."
    )

    st.subheader("Governance and Control Overview")
    render_governance_metrics(governance_summaries)

    st.subheader("Organisation-Level Governance Workload")
    st.dataframe(
        build_governance_organisation_table(organisation_summaries),
        hide_index=True,
        use_container_width=True,
        height=145,
    )

    st.subheader("Related-Build Governance Workload")
    st.dataframe(
        build_governance_related_build_table(related_build_summaries),
        hide_index=True,
        use_container_width=True,
        height=213,
    )

    st.subheader("Prioritised Governance Action List")
    st.caption(
        "Actions are ordered by governance delivery risk, sign-off urgency, "
        "control readiness, due pressure, and priority."
    )
    st.dataframe(
        build_prioritised_governance_table(prioritised_summaries),
        hide_index=True,
        use_container_width=True,
        height=560,
        column_config={
            "Organisation": st.column_config.TextColumn(width="medium"),
            "Workflow": st.column_config.TextColumn(width="medium"),
            "Related build": st.column_config.TextColumn(width="small"),
            "Action": st.column_config.TextColumn(width="large"),
            "Owner": st.column_config.TextColumn(width="medium"),
            "Priority": st.column_config.TextColumn(width="small"),
            "Status": st.column_config.TextColumn(width="small"),
            "Due (days)": st.column_config.NumberColumn(format="%d"),
            "Sign-off urgency": st.column_config.TextColumn(width="medium"),
            "Control area": st.column_config.TextColumn(width="medium"),
            "Control readiness": st.column_config.TextColumn(width="medium"),
            "Governance owner need": st.column_config.TextColumn(
                width="medium"
            ),
            "Governance delivery risk": st.column_config.TextColumn(
                width="medium"
            ),
            "Recommendation": st.column_config.TextColumn(width="large"),
        },
    )

    st.subheader("Consulting Interpretation")
    st.markdown(
        """
This tracker helps prevent implementation from moving faster than governance. It
shows which actions need approval, which controls need review, and where sign-off
delays or weak controls could affect responsible AI adoption.
        """
    )


def build_training_organisation_table(
    summaries: list[dict],
) -> list[dict]:
    """Prepare organisation-level training support workload for display."""
    return [
        {
            "Organisation": summary["organisation_name"],
            "Total": summary["total_actions"],
            "Follow-up required": summary[
                "training_followup_required_count"
            ],
            "Urgent follow-up": summary["urgent_training_followup_count"],
            "High support": summary["high_support_count"],
            "Moderate support": summary["moderate_support_count"],
            "High training risk": summary[
                "high_training_delivery_risk_count"
            ],
            "Immediate coaching": summary["immediate_coaching_count"],
            "Workflow demonstrations": summary[
                "workflow_demonstration_count"
            ],
        }
        for summary in summaries
    ]


def build_training_related_build_table(
    summaries: list[dict],
) -> list[dict]:
    """Prepare related-build training support workload for display."""
    return [
        {
            "Related build": summary["related_build"],
            "Total": summary["total_actions"],
            "Follow-up required": summary[
                "training_followup_required_count"
            ],
            "Urgent follow-up": summary["urgent_training_followup_count"],
            "High support": summary["high_support_count"],
            "Moderate support": summary["moderate_support_count"],
            "High training risk": summary[
                "high_training_delivery_risk_count"
            ],
            "Immediate coaching": summary["immediate_coaching_count"],
            "Workflow demonstrations": summary[
                "workflow_demonstration_count"
            ],
        }
        for summary in summaries
    ]


def build_training_owner_table(summaries: list[dict]) -> list[dict]:
    """Prepare owner-role training support workload for display."""
    return [
        {
            "Owner role": summary["owner_role"],
            "Total": summary["total_actions"],
            "Follow-up required": summary[
                "training_followup_required_count"
            ],
            "High support": summary["high_support_count"],
            "Moderate support": summary["moderate_support_count"],
            "High training risk": summary[
                "high_training_delivery_risk_count"
            ],
        }
        for summary in summaries
    ]


def build_prioritised_training_table(
    summaries: list[dict],
) -> list[dict]:
    """Prepare the prioritised training follow-up list for Streamlit."""
    return [
        {
            "Organisation": summary["organisation_name"],
            "Workflow": summary["workflow_name"],
            "Related build": summary["related_build"],
            "Action": summary["action_title"],
            "Owner": summary["owner_role"],
            "Priority": summary["priority"],
            "Status": summary["status"],
            "Due (days)": summary["due_in_days"],
            "Follow-up urgency": summary["training_followup_urgency"],
            "Support type": summary["training_support_type"],
            "Support intensity": summary["training_support_intensity"],
            "Delivery need": summary["training_delivery_need"],
            "Training delivery risk": summary["training_delivery_risk"],
            "Recommendation": summary[
                "training_followup_recommendation"
            ],
        }
        for summary in summaries
    ]


def render_training_followup_metrics(summaries: list[dict]) -> None:
    """Render Phase 5 training support overview metrics."""
    metrics = {
        "Total actions": len(summaries),
        "Follow-up required": sum(
            summary["training_followup_required"] for summary in summaries
        ),
        "Urgent follow-up": sum(
            summary["training_followup_urgency"]
            == "Urgent training follow-up"
            for summary in summaries
        ),
        "High support": sum(
            summary["training_support_intensity"] == "High support"
            for summary in summaries
        ),
        "Moderate support": sum(
            summary["training_support_intensity"] == "Moderate support"
            for summary in summaries
        ),
        "High training risk": sum(
            summary["training_delivery_risk"]
            == "High training delivery risk"
            for summary in summaries
        ),
        "Immediate coaching": sum(
            summary["training_delivery_need"] == "Immediate coaching session"
            for summary in summaries
        ),
    }
    columns = st.columns(7)
    for column, (label, value) in zip(columns, metrics.items()):
        column.metric(label, value)


def render_phase_5(actions: list[dict]) -> None:
    """Render Phase 5: Training Follow-up and Support Plan."""
    training_summaries = build_all_training_followup_summaries(actions)
    organisation_summaries = summarise_training_followup_by_organisation(
        actions
    )
    related_build_summaries = summarise_training_followup_by_related_build(
        actions
    )
    owner_summaries = summarise_training_followup_by_owner_role(actions)
    prioritised_summaries = add_training_followup_recommendations(
        prioritise_training_followup_actions(actions)
    )

    st.markdown(
        '<div class="phase-kicker">Delivery control / Phase 5</div>',
        unsafe_allow_html=True,
    )
    st.title("Training Follow-up and Support Plan")
    st.markdown(
        '<p class="page-intro">'
        "Plan targeted coaching, workflow demonstrations, quality-review "
        "practice, and responsible-use support during implementation."
        "</p>",
        unsafe_allow_html=True,
    )
    st.info(
        "This section uses synthetic portfolio data only. It demonstrates how a "
        "consultant could plan training follow-up, coaching, and support actions "
        "during AI implementation."
    )

    st.subheader("Training Support Overview")
    render_training_followup_metrics(training_summaries)

    st.subheader("Organisation-Level Training Workload")
    st.dataframe(
        build_training_organisation_table(organisation_summaries),
        hide_index=True,
        use_container_width=True,
        height=145,
    )

    st.subheader("Related-Build Training Workload")
    st.dataframe(
        build_training_related_build_table(related_build_summaries),
        hide_index=True,
        use_container_width=True,
        height=213,
    )

    st.subheader("Owner-Role Training Support")
    st.dataframe(
        build_training_owner_table(owner_summaries),
        hide_index=True,
        use_container_width=True,
        height=360,
    )

    st.subheader("Prioritised Training Follow-up List")
    st.caption(
        "Actions are ordered by training delivery risk, follow-up urgency, "
        "support intensity, due pressure, and priority."
    )
    st.dataframe(
        build_prioritised_training_table(prioritised_summaries),
        hide_index=True,
        use_container_width=True,
        height=560,
        column_config={
            "Organisation": st.column_config.TextColumn(width="medium"),
            "Workflow": st.column_config.TextColumn(width="medium"),
            "Related build": st.column_config.TextColumn(width="small"),
            "Action": st.column_config.TextColumn(width="large"),
            "Owner": st.column_config.TextColumn(width="medium"),
            "Priority": st.column_config.TextColumn(width="small"),
            "Status": st.column_config.TextColumn(width="small"),
            "Due (days)": st.column_config.NumberColumn(format="%d"),
            "Follow-up urgency": st.column_config.TextColumn(width="medium"),
            "Support type": st.column_config.TextColumn(width="medium"),
            "Support intensity": st.column_config.TextColumn(width="medium"),
            "Delivery need": st.column_config.TextColumn(width="medium"),
            "Training delivery risk": st.column_config.TextColumn(
                width="medium"
            ),
            "Recommendation": st.column_config.TextColumn(width="large"),
        },
    )

    st.subheader("Consulting Interpretation")
    st.markdown(
        """
This plan helps a consultant move from generic training advice to targeted support
actions. It shows where staff need coaching, workflow demonstrations, responsible-use
refreshers, or quality review practice before implementation can progress safely.
        """
    )


def build_checkin_attention_table(items: list[dict]) -> list[dict]:
    """Prepare client check-in attention items for Streamlit."""
    return [
        {
            "Action": item["action_title"],
            "Owner": item["owner_role"],
            "Priority": item["priority"],
            "Status": item["status"],
            "Due (days)": item["due_in_days"],
            "Blocker": item["blocker"] or "None logged",
            "Governance sign-off": item["governance_signoff_required"],
            "Training follow-up": item["training_followup_required"],
            "Client check-in": item["client_checkin_required"],
        }
        for item in items
    ]


def render_checkin_overview_metrics(summary: dict) -> None:
    """Render Phase 6 organisation-level check-in metrics."""
    snapshot = summary["progress_snapshot"]
    metrics = [
        ("Total actions", snapshot["total_actions"]),
        ("Completed", snapshot["completed_count"]),
        ("In progress", snapshot["in_progress_count"]),
        ("Blocked", snapshot["blocked_count"]),
        ("Deferred", snapshot["deferred_count"]),
        ("Attention items", summary["attention_item_count"]),
        ("Check-in health", summary["checkin_health"]),
    ]
    columns = st.columns(7)
    for column, (label, value) in zip(columns, metrics):
        column.metric(label, value)


def render_phase_6(
    organisations: list[dict],
    actions: list[dict],
    checkins: list[dict],
) -> None:
    """Render Phase 6: Client Check-in Summary Builder."""
    st.markdown(
        '<div class="phase-kicker">Delivery control / Phase 6</div>',
        unsafe_allow_html=True,
    )
    st.title("Client Check-in Summary Builder")
    st.markdown(
        '<p class="page-intro">'
        "Prepare a focused implementation conversation using current progress, "
        "attention items, decisions needed, and the next review priority."
        "</p>",
        unsafe_allow_html=True,
    )
    st.info(
        "This section uses synthetic portfolio data only. It demonstrates how a "
        "consultant could prepare structured client check-in summaries during "
        "AI implementation."
    )

    organisation_lookup = {
        organisation["organisation_name"]: organisation
        for organisation in organisations
    }
    selected_name = st.selectbox(
        "Organisation",
        list(organisation_lookup),
        key="phase_6_organisation",
    )
    selected_organisation = organisation_lookup[selected_name]
    selected_actions = get_actions_for_organisation(
        actions,
        selected_organisation["organisation_id"],
    )
    summary = build_client_checkin_summary(
        selected_organisation,
        actions,
        checkins,
    )
    attention_items = identify_checkin_attention_items(selected_actions)
    markdown_summary = build_client_checkin_markdown(
        summary,
        attention_items,
    )

    st.subheader("Check-in Overview")
    render_checkin_overview_metrics(summary)
    st.caption(
        f"Latest synthetic check-in: {summary['latest_checkin_period']} · "
        f"{summary['latest_checkin_focus']}"
    )
    st.markdown(
        '<div class="scope-note">'
        f"<strong>Recommended approach:</strong> "
        f"{generate_checkin_recommendation(summary)}"
        "</div>",
        unsafe_allow_html=True,
    )

    st.subheader("Client Decisions Needed")
    if summary["client_decision_needs"]:
        for decision in summary["client_decision_needs"]:
            st.markdown(f"- {decision}")
    else:
        st.success("No specific client decisions are currently required.")

    st.subheader("Key Attention Items")
    st.dataframe(
        build_checkin_attention_table(attention_items),
        hide_index=True,
        use_container_width=True,
        height=360,
        column_config={
            "Action": st.column_config.TextColumn(width="large"),
            "Owner": st.column_config.TextColumn(width="medium"),
            "Priority": st.column_config.TextColumn(width="small"),
            "Status": st.column_config.TextColumn(width="small"),
            "Due (days)": st.column_config.NumberColumn(format="%d"),
            "Blocker": st.column_config.TextColumn(width="large"),
            "Governance sign-off": st.column_config.CheckboxColumn(
                width="small"
            ),
            "Training follow-up": st.column_config.CheckboxColumn(
                width="small"
            ),
            "Client check-in": st.column_config.CheckboxColumn(width="small"),
        },
    )

    st.subheader("Markdown Check-in Summary Preview")
    st.markdown(markdown_summary)

    st.subheader("Consulting Interpretation")
    st.markdown(
        """
The check-in summary builder turns delivery tracking into a practical client
conversation. It helps the consultant focus on blocked actions, decisions required,
training follow-up, governance sign-offs, and the next review focus.
        """
    )


def render_phase_7(
    organisations: list[dict],
    actions: list[dict],
    checkins: list[dict],
) -> None:
    """Render Phase 7: Implementation Progress Report Builder."""
    st.markdown(
        '<div class="phase-kicker">Delivery control / Phase 7</div>',
        unsafe_allow_html=True,
    )
    st.title("Implementation Progress Report Builder")
    st.markdown(
        '<p class="page-intro">'
        "Turn AI adoption delivery evidence into a structured implementation "
        "progress report covering actions, blockers, governance, training, "
        "and client check-ins."
        "</p>",
        unsafe_allow_html=True,
    )
    st.info(
        "This section uses synthetic portfolio data only. It demonstrates how a "
        "consultant could turn AI adoption delivery evidence into a structured "
        "implementation progress report."
    )

    organisation_options = {
        "Portfolio-level report": None,
        **{
            organisation["organisation_name"]: organisation["organisation_id"]
            for organisation in organisations
        },
    }
    selected_name = st.selectbox(
        "Report scope",
        list(organisation_options),
        key="phase_7_scope",
    )
    selected_id = organisation_options[selected_name]

    report_text = build_full_progress_report(
        organisations, actions, checkins, organisation_id=selected_id
    )

    st.subheader("Generated Markdown Report")
    st.markdown(report_text)

    st.subheader("About this Report")
    st.markdown(
        "The report combines action tracking, blocker review, governance sign-off, "
        "training follow-up, and client check-in evidence into one implementation "
        "progress view."
    )


def render_phase_8(
    organisations: list[dict],
    actions: list[dict],
    checkins: list[dict],
) -> None:
    """Render Phase 8: Export Centre and Completion Review."""
    st.markdown(
        '<div class="phase-kicker">Delivery control / Phase 8</div>',
        unsafe_allow_html=True,
    )
    st.title("Export Centre and Completion Review")
    st.markdown(
        '<p class="page-intro">'
        "Package Build 8 implementation delivery evidence into downloadable formats "
        "and review the final completion status of all eight phases."
        "</p>",
        unsafe_allow_html=True,
    )
    st.info(
        "This export centre uses synthetic portfolio data only. It demonstrates how a "
        "consultant could package AI implementation delivery evidence for review, "
        "follow-up, and portfolio presentation."
    )

    summary = build_completion_summary(organisations, actions, checkins)

    st.subheader("Completion Summary")
    first_row = st.columns(4)
    first_row[0].metric("Total organisations", summary["total_organisations"])
    first_row[1].metric("Total actions", summary["total_actions"])
    first_row[2].metric("Total check-ins", summary["total_checkins"])
    first_row[3].metric("Completed actions", summary["completed_actions"])

    second_row = st.columns(4)
    second_row[0].metric("Blocked actions", summary["blocked_actions"])
    second_row[1].metric("In-progress actions", summary["in_progress_actions"])
    second_row[2].metric(
        "Critical or high priority", summary["critical_or_high_priority_actions"]
    )
    second_row[3].metric(
        "Escalation required", summary["escalation_required_actions"]
    )

    third_row = st.columns(3)
    third_row[0].metric(
        "Governance sign-off required",
        summary["governance_signoff_required_actions"],
    )
    third_row[1].metric(
        "Training follow-up required",
        summary["training_followup_required_actions"],
    )
    third_row[2].metric(
        "Client check-in required",
        summary["client_checkin_required_actions"],
    )

    st.subheader("Report Scope")
    organisation_options = {
        "Portfolio-level report": None,
        **{
            organisation["organisation_name"]: organisation["organisation_id"]
            for organisation in organisations
        },
    }
    selected_name = st.selectbox(
        "Report scope",
        list(organisation_options),
        key="phase_8_scope",
    )
    selected_id = organisation_options[selected_name]

    st.subheader("Downloads")

    markdown_text = export_markdown_report(
        organisations, actions, checkins, organisation_id=selected_id
    )
    st.download_button(
        label="Download Markdown Progress Report",
        data=markdown_text,
        file_name=build_export_filename("build_8_ai_adoption_progress_report", "md"),
        mime="text/markdown",
    )

    csv_text = export_csv_text(actions)
    st.download_button(
        label="Download CSV Evidence Table",
        data=csv_text,
        file_name=build_export_filename("build_8_ai_adoption_evidence", "csv"),
        mime="text/csv",
    )

    json_text = export_json_text(organisations, actions, checkins)
    st.download_button(
        label="Download JSON Evidence Pack",
        data=json_text,
        file_name=build_export_filename("build_8_ai_adoption_evidence", "json"),
        mime="application/json",
    )

    try:
        pdf_bytes = export_pdf_bytes(markdown_text)
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=build_export_filename(
                "build_8_ai_adoption_progress_report", "pdf"
            ),
            mime="application/pdf",
        )
    except ImportError:
        st.caption(
            "PDF export is not available. Install reportlab to enable this option."
        )

    try:
        chart_bytes = export_summary_chart_png_bytes(actions)
        st.download_button(
            label="Download PNG Summary Chart",
            data=chart_bytes,
            file_name=build_export_filename(
                "build_8_ai_adoption_summary_chart", "png"
            ),
            mime="image/png",
        )
    except ImportError:
        st.caption(
            "Chart export is not available. Install matplotlib to enable this option."
        )

    st.subheader("Completion Review")
    review_text = build_completion_review_text(organisations, actions, checkins)
    st.markdown(review_text)

    st.subheader("Consulting Interpretation")
    st.markdown(
        "The export centre turns Build 8 from a delivery dashboard into a reusable "
        "consulting asset. It packages implementation actions, blockers, governance "
        "needs, training follow-up, check-in evidence, and progress reporting into "
        "formats that can support client reviews and portfolio demonstrations."
    )


def main() -> None:
    """Run the Build 8 Streamlit app."""
    apply_styles()
    selected_phase = render_sidebar()

    organisations = get_synthetic_delivery_organisations()
    actions = get_synthetic_implementation_actions()
    checkins = get_synthetic_client_checkins()

    if selected_phase == PHASE_NAVIGATION[7]:
        render_phase_8(organisations, actions, checkins)
    elif selected_phase == PHASE_NAVIGATION[6]:
        render_phase_7(organisations, actions, checkins)
    elif selected_phase == PHASE_NAVIGATION[5]:
        render_phase_6(organisations, actions, checkins)
    elif selected_phase == PHASE_NAVIGATION[4]:
        render_phase_5(actions)
    elif selected_phase == PHASE_NAVIGATION[3]:
        render_phase_4(actions)
    elif selected_phase == PHASE_NAVIGATION[2]:
        render_phase_3(actions)
    elif selected_phase == PHASE_NAVIGATION[1]:
        render_phase_2(actions)
    else:
        render_phase_1(organisations, actions, checkins)


if __name__ == "__main__":
    main()
