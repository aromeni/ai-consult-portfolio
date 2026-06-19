"""Build 9 — AI Adoption Consulting Capstone Dashboard."""

import streamlit as st

from data.synthetic_capstone_data import (
    get_synthetic_capstone_clients,
    get_synthetic_capstone_indicators,
    get_synthetic_cross_build_stages,
)
from logic.capstone_overview import (
    summarise_phase_1_capstone,
    validate_all_capstone_data,
)
from logic.capstone_report import build_full_capstone_report
from logic.export_centre import (
    build_export_filename,
    build_portfolio_evidence_summary,
    build_portfolio_evidence_summary_text,
    export_csv_text,
    export_json_evidence_pack,
    export_markdown_capstone_report,
    export_pdf_bytes,
    export_summary_chart_png_bytes,
)
from logic.capstone_dashboard import (
    build_capstone_snapshot,
    build_client_dashboard_context,
    build_client_selector_options,
    build_dashboard_metric_summary,
    build_dashboard_table_rows,
    build_portfolio_dashboard_context,
    get_client_by_selector_label,
)
from logic.client_journey import (
    add_journey_recommendations,
    build_all_client_journey_summaries,
    prioritise_clients_for_review,
    summarise_journey_health,
)
from logic.cross_build_insights import (
    add_cross_build_recommendations,
    build_all_cross_build_summaries,
    build_client_build_matrix,
    prioritise_build_areas_for_improvement,
    summarise_cross_build_insights,
)
from logic.recommendation_pathway import (
    add_consulting_recommendation_text,
    build_all_consulting_recommendations,
    build_recommendation_pathway_matrix,
    prioritise_recommendations,
    summarise_recommendation_pathways,
)

PHASE_NAVIGATION = [
    "1. Capstone Client Setup",
    "2. Client Journey Overview",
    "3. Cross-Build Insight Aggregator",
    "4. Consulting Recommendation Pathway",
    "5. Capstone Dashboard",
    "6. Capstone Report Builder",
    "7. Export Centre",
    "8. Final Review",
]

ACTIVE_PHASES = PHASE_NAVIGATION[:8]

_PORTFOLIO_CSS = """
<style>
/* ─── Rashid AI Consult — Portfolio Theme ──────────────────────────────────── */
.main .block-container { padding-top: 1.5rem; padding-bottom: 3rem; }
section[data-testid="stSidebar"] { background: #1a2744 !important; }
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div { color: #cbd5e1 !important; }
section[data-testid="stSidebar"] strong,
section[data-testid="stSidebar"] b { color: #f1f5f9 !important; }
section[data-testid="stSidebar"] hr { border-color: #334155 !important; }
section[data-testid="stSidebar"] .stRadio label { color: #e2e8f0 !important; font-size: 0.88rem !important; }
section[data-testid="stSidebar"] [data-testid="stCaption"] { color: #94a3b8 !important; font-size: 0.75rem !important; }
h1 { color: #0f172a !important; font-weight: 800 !important; letter-spacing: -0.02em; }
h2 { color: #1a2744 !important; font-weight: 700 !important; border-left: 4px solid #2563eb; padding-left: 0.65rem; }
h3 { color: #1e3a5f !important; font-weight: 600 !important; }
[data-testid="stMetric"] { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 0.7rem 1rem; box-shadow: 0 1px 2px rgba(15,23,42,0.05); }
[data-testid="stMetricValue"] { color: #2563eb !important; font-weight: 800 !important; font-size: 1.5rem !important; }
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600 !important; }
.stButton > button { border-radius: 8px !important; font-weight: 600 !important; font-size: 0.85rem !important; transition: all 0.15s ease-out !important; }
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 2px 6px rgba(15,23,42,0.12); }
.stDownloadButton > button { border-radius: 8px !important; font-weight: 600 !important; }
.stTextInput > div > div > input { border-radius: 8px !important; border-color: #cbd5e1 !important; }
.stSelectbox > div > div { border-radius: 8px !important; border-color: #cbd5e1 !important; }
hr { border-color: #e2e8f0 !important; margin: 1.25rem 0 !important; }
.stTabs [data-baseweb="tab"] { font-weight: 600 !important; }
[data-testid="stExpander"] { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; }
.streamlit-expanderHeader { font-weight: 600 !important; color: #1e3a5f !important; }
[data-testid="stDataFrame"] { border: 1px solid #e2e8f0; border-radius: 10px; }
</style>
"""


def render_phase_1(clients, stages, indicators):
    st.caption("Capstone setup / Phase 1")
    st.subheader("Capstone Client Setup")

    st.info(
        "This dashboard uses synthetic portfolio data only. "
        "All organisations, stages, and evidence records are fictional. "
        "Human review is required before any real-world consulting use."
    )

    # 1. Capstone client overview
    st.markdown("### Capstone Clients")
    client_rows = [
        {
            "Client ID": c["client_id"],
            "Organisation": c["organisation_name"],
            "Sector": c["sector"],
            "Staff": c["staff_count"],
            "Stage": c["capstone_stage"],
            "Primary AI Goal": c["primary_ai_goal"],
        }
        for c in clients
    ]
    st.dataframe(client_rows, use_container_width=True)

    # 2. Cross-build journey stage table
    st.markdown("### Cross-Build Journey Stages")
    stage_rows = [
        {
            "Stage ID": s["stage_id"],
            "Client": s["organisation_name"],
            "Build": s["build_number"],
            "Journey Stage": s["journey_stage"],
            "Status": s["stage_status"],
            "Evidence": s["evidence_strength"],
            "Summary": s["stage_summary"],
        }
        for s in stages
    ]
    st.dataframe(stage_rows, use_container_width=True)

    # 3. Capstone indicator table
    st.markdown("### Capstone Portfolio Indicators")
    indicator_rows = [
        {
            "Client": i["organisation_name"],
            "Readiness": i["readiness_position"],
            "Governance": i["governance_position"],
            "Training": i["training_position"],
            "ROI": i["roi_position"],
            "Delivery": i["delivery_position"],
            "Overall Status": i["overall_capstone_status"],
            "Recommended Next Step": i["recommended_next_step"],
        }
        for i in indicators
    ]
    st.dataframe(indicator_rows, use_container_width=True)

    # 4. Phase 1 capstone summary
    st.markdown("### Phase 1 Summary")
    summary = summarise_phase_1_capstone(clients, stages, indicators)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Clients", summary["total_clients"])
    col2.metric("Journey Stages", summary["total_cross_build_stages"])
    col3.metric("Completed Stages", summary["completed_stage_count"])
    col4.metric("In Progress", summary["in_progress_stage_count"])

    col5, col6, col7 = st.columns(3)
    col5.metric("Needs Review", summary["needs_review_stage_count"])
    col6.metric("Strong / Very Strong Evidence", summary["strong_or_very_strong_evidence_count"])
    col7.metric("Portfolio-Ready Clients", summary["portfolio_ready_or_strong_asset_count"])

    # 5. Validation summary
    st.markdown("### Validation Summary")
    validation = validate_all_capstone_data(clients, stages, indicators)
    if validation["warnings"]:
        for warning in validation["warnings"]:
            st.warning(warning)
    else:
        st.success(
            f"All {validation['total_clients']} clients, "
            f"{validation['total_stages']} stages, and "
            f"{validation['total_indicators']} indicators passed validation."
        )

    # 6. How Build 9 connects Builds 1–8
    st.markdown("### How Build 9 Connects Builds 1–8")
    st.markdown(
        """
Build 9 is the AI adoption consulting capstone dashboard. It aggregates evidence and insights
from the seven previous builds into a single client-facing portfolio view.

| Build | Tool | What Build 9 Draws On |
| --- | --- | --- |
| Build 1 | AI Readiness / Workflow Audit Tool | Readiness findings and workflow priority identification |
| Build 2/3 | Document Intelligence / Semantic RAG | Document handling capability and retrieval demonstration |
| Build 4 | AI Staff Training and Workshop Generator | Training delivery, workshop design, and staff confidence |
| Build 5 | AI Consulting Report Generator | Structured consulting report and client-facing recommendations |
| Build 6 | AI Governance Policy Checker | Governance maturity, policy gaps, and control readiness |
| Build 7 | AI Adoption ROI and Impact Tracker | ROI evidence, workflow impact, and adoption decisions |
| Build 8 | AI Adoption Delivery and Implementation Tracker | Implementation actions, blockers, and delivery progress |

Each of these tools has already been built and tested as a standalone portfolio demonstration.
Build 9 connects their outputs into one coherent consulting journey, showing how a consultant
moves a client from initial readiness diagnosis through to tracked implementation delivery.
        """
    )


def render_phase_2(clients, stages, indicators):
    st.caption("Client journey / Phase 2")
    st.subheader("Client Journey Overview Engine")

    st.info(
        "This section uses synthetic portfolio data only. It demonstrates how a consultant "
        "could review each client's end-to-end AI adoption journey across Builds 1–8."
    )

    summaries = build_all_client_journey_summaries(clients, stages, indicators)
    summaries_with_rec = add_journey_recommendations(summaries)
    health = summarise_journey_health(summaries)
    prioritised = prioritise_clients_for_review(summaries_with_rec)

    # 1. Overview metrics
    st.markdown("### Journey Health Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clients", health["total_clients"])
    col2.metric("Strong Journey", health["strong_journey_count"])
    col3.metric("Healthy Journey", health["healthy_journey_count"])

    col4, col5, col6 = st.columns(3)
    col4.metric("Developing Journey", health["developing_journey_count"])
    col5.metric("Needs Review", health["needs_review_count"])
    col6.metric("Blocked Journey", health["blocked_journey_count"])

    # 2. Client journey summary table
    st.markdown("### Client Journey Summaries")
    summary_rows = [
        {
            "Organisation": s["organisation_name"],
            "Sector": s["sector"],
            "Capstone Stage": s["capstone_stage"],
            "Total Stages": s["total_stages"],
            "Completed": s["completed_stage_count"],
            "In Progress": s["in_progress_stage_count"],
            "Needs Review": s["needs_review_stage_count"],
            "Completion %": s["stage_completion_rate"],
            "Avg Evidence Score": s["average_evidence_score"],
            "Journey Health": s["journey_health"],
            "Weakest Stage": s["weakest_stage"],
            "Next Journey Step": s["next_journey_step"],
            "Overall Status": s["overall_capstone_status"],
            "Recommendation": s["journey_recommendation"],
        }
        for s in summaries_with_rec
    ]
    st.dataframe(summary_rows, use_container_width=True)

    # 3. Prioritised client review table
    st.markdown("### Prioritised Client Review")
    st.caption("Clients sorted by review urgency — blocked and needs-review clients appear first.")
    priority_rows = [
        {
            "Priority": rank + 1,
            "Organisation": s["organisation_name"],
            "Journey Health": s["journey_health"],
            "Completion %": s["stage_completion_rate"],
            "Avg Evidence Score": s["average_evidence_score"],
            "Weakest Stage": s["weakest_stage"],
            "Next Step": s["next_journey_step"],
            "Recommendation": s["journey_recommendation"],
        }
        for rank, s in enumerate(prioritised)
    ]
    st.dataframe(priority_rows, use_container_width=True)

    # 4. Consulting interpretation
    st.markdown("### Consulting Interpretation")
    st.markdown(
        "The client journey overview turns the individual build outputs into a single "
        "consulting pathway. It helps identify which client stories are strong enough for "
        "portfolio presentation, which ones need more evidence, and which stages should be "
        "improved before the capstone is presented as complete."
    )


def render_phase_3(clients, stages, indicators):
    st.caption("Cross-build insights / Phase 3")
    st.subheader("Cross-Build Insight Aggregator")

    st.info(
        "This section uses synthetic portfolio data only. It demonstrates how a consultant "
        "could aggregate evidence across Builds 1–8 into one capstone-level view."
    )

    summaries = build_all_cross_build_summaries(stages)
    summaries_with_rec = add_cross_build_recommendations(summaries)
    insight_summary = summarise_cross_build_insights(summaries)
    prioritised = prioritise_build_areas_for_improvement(summaries_with_rec)
    matrix = build_client_build_matrix(clients, stages)

    # 1. Overview metrics
    st.markdown("### Build Evidence Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Build Areas", insight_summary["total_build_areas"])
    col2.metric("Very Strong Evidence", insight_summary["very_strong_evidence_count"])
    col3.metric("Strong Evidence", insight_summary["strong_evidence_count"])
    col4.metric("Developing Evidence", insight_summary["developing_evidence_count"])

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Weak Evidence", insight_summary["weak_evidence_count"])
    col6.metric("No Evidence", insight_summary["no_evidence_count"])
    col7.metric("Strongest Build Area", insight_summary["strongest_build_area"])
    col8.metric("Weakest Build Area", insight_summary["weakest_build_area"])

    # 2. Cross-build summary table
    st.markdown("### Cross-Build Summary")
    summary_rows = [
        {
            "Build": s["build_number"],
            "Domain": s["build_domain"],
            "Clients": s["client_stage_count"],
            "Completed": s["completed_count"],
            "In Progress": s["in_progress_count"],
            "Needs Review": s["needs_review_count"],
            "Not Started": s["not_started_count"],
            "Completion %": s["completion_rate"],
            "Avg Evidence Score": s["average_evidence_score"],
            "Evidence Health": s["evidence_health"],
            "Build Gap": s["build_gap"],
            "Recommendation": s["cross_build_recommendation"],
        }
        for s in summaries_with_rec
    ]
    st.dataframe(summary_rows, use_container_width=True)

    # 3. Client-build matrix table
    st.markdown("### Client-Build Status Matrix")
    st.caption("Stage status for each client across all seven build areas.")
    matrix_rows = [
        {
            "Organisation": row["organisation_name"],
            "Build 1": row["Build 1"],
            "Build 2/3": row["Build 2/3"],
            "Build 4": row["Build 4"],
            "Build 5": row["Build 5"],
            "Build 6": row["Build 6"],
            "Build 7": row["Build 7"],
            "Build 8": row["Build 8"],
        }
        for row in matrix
    ]
    st.dataframe(matrix_rows, use_container_width=True)

    # 4. Prioritised build improvement table
    st.markdown("### Prioritised Build Improvement")
    st.caption("Build areas sorted by improvement priority — weakest and missing evidence first.")
    priority_rows = [
        {
            "Priority": rank + 1,
            "Build": s["build_number"],
            "Domain": s["build_domain"],
            "Evidence Health": s["evidence_health"],
            "Completion %": s["completion_rate"],
            "Avg Evidence Score": s["average_evidence_score"],
            "Build Gap": s["build_gap"],
            "Recommendation": s["cross_build_recommendation"],
        }
        for rank, s in enumerate(prioritised)
    ]
    st.dataframe(priority_rows, use_container_width=True)

    # 5. Consulting interpretation
    st.markdown("### Consulting Interpretation")
    st.markdown(
        "The cross-build insight aggregator shows how the individual portfolio builds combine "
        "into one end-to-end consulting story. It helps identify which build areas are strong "
        "enough to lead the capstone narrative and which areas need more evidence before final "
        "presentation."
    )


def render_phase_4(clients, stages, indicators):
    st.caption("Consulting recommendations / Phase 4")
    st.subheader("Consulting Recommendation Pathway")

    st.info(
        "This section uses synthetic portfolio data only. It demonstrates how a consultant "
        "could convert capstone evidence into practical client recommendations and commercial "
        "next steps."
    )

    client_summaries = build_all_client_journey_summaries(clients, stages, indicators)
    recommendations = build_all_consulting_recommendations(client_summaries)
    recommendations_with_text = add_consulting_recommendation_text(recommendations)
    pathway_summary = summarise_recommendation_pathways(recommendations)
    prioritised = prioritise_recommendations(recommendations_with_text)
    matrix = build_recommendation_pathway_matrix(recommendations_with_text)

    # 1. Overview metrics
    st.markdown("### Recommendation Pathway Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Clients", pathway_summary["total_clients"])
    col2.metric("Capstone Ready", pathway_summary["capstone_ready_count"])
    col3.metric("Nearly Ready", pathway_summary["nearly_ready_count"])
    col4.metric("Needs Strengthening", pathway_summary["needs_strengthening_count"])

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Not Ready", pathway_summary["not_ready_count"])
    col6.metric("High Priority", pathway_summary["high_priority_count"])
    col7.metric("Medium Priority", pathway_summary["medium_priority_count"])
    col8.metric("Low Priority", pathway_summary["low_priority_count"])

    # 2. Recommendation pathway table
    st.markdown("### Client Recommendation Summaries")
    recommendation_rows = [
        {
            "Organisation": r["organisation_name"],
            "Sector": r["sector"],
            "Journey Health": r["journey_health"],
            "Completion %": r["stage_completion_rate"],
            "Avg Evidence Score": r["average_evidence_score"],
            "Weakest Stage": r["weakest_stage"],
            "Capstone Readiness": r["capstone_readiness"],
            "Consulting Pathway": r["consulting_pathway"],
            "Commercial Next Step": r["commercial_next_step"],
            "Improvement Area": r["primary_improvement_area"],
            "Priority": r["recommendation_priority"],
            "Consulting Recommendation": r["consulting_recommendation"],
        }
        for r in recommendations_with_text
    ]
    st.dataframe(recommendation_rows, use_container_width=True)

    # 3. Recommendation pathway matrix
    st.markdown("### Recommendation Pathway Matrix")
    st.caption("Simplified view of consulting pathway decisions across all clients.")
    matrix_rows = [
        {
            "Organisation": row["organisation_name"],
            "Capstone Readiness": row["capstone_readiness"],
            "Consulting Pathway": row["consulting_pathway"],
            "Commercial Next Step": row["commercial_next_step"],
            "Improvement Area": row["primary_improvement_area"],
            "Priority": row["recommendation_priority"],
        }
        for row in matrix
    ]
    st.dataframe(matrix_rows, use_container_width=True)

    # 4. Prioritised recommendations table
    st.markdown("### Prioritised Recommendations")
    st.caption("Clients sorted by recommendation priority — high-priority clients appear first.")
    priority_rows = [
        {
            "Priority": rank + 1,
            "Organisation": r["organisation_name"],
            "Journey Health": r["journey_health"],
            "Capstone Readiness": r["capstone_readiness"],
            "Priority Level": r["recommendation_priority"],
            "Consulting Pathway": r["consulting_pathway"],
            "Commercial Next Step": r["commercial_next_step"],
            "Consulting Recommendation": r["consulting_recommendation"],
        }
        for rank, r in enumerate(prioritised)
    ]
    st.dataframe(priority_rows, use_container_width=True)

    # 5. Consulting interpretation
    st.markdown("### Consulting Interpretation")
    st.markdown(
        "The recommendation pathway turns cross-build evidence into a practical consulting "
        "direction. It helps decide whether a client journey is ready for capstone presentation, "
        "needs more evidence, or should become a focused improvement or commercial follow-up "
        "opportunity."
    )


def render_phase_5(clients, stages, indicators):
    st.caption("Capstone dashboard / Phase 5")
    st.subheader("Capstone Dashboard")

    st.info(
        "This dashboard uses synthetic portfolio data only. It demonstrates how the full "
        "AI adoption consulting journey can be presented as one coherent client-facing capstone."
    )

    context = build_portfolio_dashboard_context(clients, stages, indicators)
    snapshot = build_capstone_snapshot(context)
    metrics = build_dashboard_metric_summary(context)
    table_rows = build_dashboard_table_rows(context)

    # 1. Dashboard snapshot
    st.markdown("### Dashboard Snapshot")
    col1, col2, col3 = st.columns(3)
    col1.metric("Dashboard Status", snapshot["dashboard_status"])
    col2.metric("Strongest Build Area", snapshot["strongest_build_area"])
    col3.metric("Weakest Build Area", snapshot["weakest_build_area"])

    st.markdown(f"**Dashboard Focus:** {snapshot['dashboard_focus']}")
    st.markdown(f"**Recommended Next Step:** {snapshot['recommended_dashboard_next_step']}")

    # 2. Headline metrics
    st.markdown("### Headline Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Clients", metrics["total_clients"])
    col2.metric("Total Build Areas", metrics["total_build_areas"])
    col3.metric("Capstone Ready", metrics["capstone_ready_count"])
    col4.metric("Nearly Ready", metrics["nearly_ready_count"])

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Needs Strengthening", metrics["needs_strengthening_count"])
    col6.metric("Strong Journey", metrics["strong_journey_count"])
    col7.metric("Blocked Journey", metrics["blocked_journey_count"])
    col8.metric("Weak Evidence", metrics["weak_evidence_count"])

    # 3. Client spotlight
    st.markdown("### Client Spotlight")
    selector_options = build_client_selector_options(clients)
    selected_label = st.selectbox(
        "Select client",
        options=selector_options,
        label_visibility="collapsed",
    )
    selected_client = get_client_by_selector_label(clients, selected_label)

    if selected_client:
        client_ctx = build_client_dashboard_context(selected_client, stages, indicators)
        rec = client_ctx["recommendation_summary"]
        journey = client_ctx["journey_summary"]

        col1, col2, col3 = st.columns(3)
        col1.metric("Organisation", selected_client.get("organisation_name", ""))
        col2.metric("Sector", selected_client.get("sector", ""))
        col3.metric("Staff Count", selected_client.get("staff_count", ""))

        col4, col5, col6 = st.columns(3)
        col4.metric("Capstone Stage", selected_client.get("capstone_stage", ""))
        col5.metric("Journey Health", journey.get("journey_health", ""))
        col6.metric("Capstone Readiness", rec.get("capstone_readiness", ""))

        st.markdown(
            f"**Primary AI Goal:** {selected_client.get('primary_ai_goal', 'Not available')}"
        )
        st.markdown(
            f"**Consulting Priority:** {selected_client.get('consulting_priority', 'Not available')}"
        )
        st.markdown(
            f"**Commercial Next Step:** {rec.get('commercial_next_step', 'Not available')}"
        )
        st.markdown(
            f"**Primary Improvement Area:** {rec.get('primary_improvement_area', 'Not available')}"
        )
        st.markdown(
            f"**Recommendation Priority:** {rec.get('recommendation_priority', 'Not available')}"
        )

    # 4. Client journey table
    st.markdown("### Client Journey Table")
    st.caption("Journey health and evidence position for each client.")
    st.dataframe(table_rows["client_journey_rows"], use_container_width=True)

    # 5. Cross-build evidence table
    st.markdown("### Cross-Build Evidence Table")
    st.caption("Evidence health position across all seven build areas.")
    st.dataframe(table_rows["cross_build_rows"], use_container_width=True)

    # 6. Recommendation pathway table
    st.markdown("### Recommendation Pathway Table")
    st.caption("Consulting pathway and commercial next step for each client.")
    st.dataframe(table_rows["recommendation_rows"], use_container_width=True)

    # 7. Consulting interpretation
    st.markdown("### Consulting Interpretation")
    st.markdown(
        "The capstone dashboard brings the portfolio together as one consulting journey. "
        "It helps a prospect or evaluator understand how readiness, document intelligence, "
        "training, reporting, governance, ROI, and delivery tracking connect into a practical "
        "AI adoption service."
    )


def render_phase_6(clients, stages, indicators):
    st.caption("Capstone report builder / Phase 6")
    st.subheader("Capstone Report Builder")

    st.info(
        "This report builder uses synthetic portfolio data only. It demonstrates how the full "
        "AI adoption consulting journey can be converted into a structured capstone report."
    )

    # 1. Report scope selector
    st.markdown("### Report Scope")
    scope_options = ["Portfolio-level report"] + build_client_selector_options(clients)
    selected_scope = st.selectbox(
        "Select report scope",
        options=scope_options,
        label_visibility="collapsed",
    )

    if selected_scope == "Portfolio-level report":
        report_client_id = None
    else:
        matched = get_client_by_selector_label(clients, selected_scope)
        report_client_id = matched["client_id"] if matched else None

    # 2. Generated Markdown report preview
    st.markdown("### Report Preview")
    report_content = build_full_capstone_report(clients, stages, indicators, report_client_id)
    st.markdown(report_content)

    # 3. Short explanation
    st.divider()
    st.markdown(
        "The capstone report combines client journey evidence, cross-build insight, "
        "recommendation pathways, and dashboard-level interpretation into one consulting narrative."
    )


def render_phase_7(clients, stages, indicators):
    st.caption("Export centre / Phase 7")
    st.subheader("Export Centre and Portfolio Evidence Pack")

    st.info(
        "This export centre uses synthetic portfolio data only. It demonstrates how the capstone "
        "dashboard and report can be packaged as reusable portfolio evidence."
    )

    evidence_summary = build_portfolio_evidence_summary(clients, stages, indicators)

    # 1. Portfolio evidence summary metrics
    st.markdown("### Portfolio Evidence Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clients", evidence_summary["total_clients"])
    col2.metric("Total Cross-Build Stages", evidence_summary["total_cross_build_stages"])
    col3.metric("Total Build Areas", evidence_summary["total_build_areas"])

    col4, col5, col6 = st.columns(3)
    col4.metric("Completed Stages", evidence_summary["completed_stage_count"])
    col5.metric("Strong / Very Strong Evidence", evidence_summary["strong_or_very_strong_evidence_count"])
    col6.metric("Capstone Ready", evidence_summary["capstone_ready_count"])

    col7, col8, col9 = st.columns(3)
    col7.metric("Nearly Ready", evidence_summary["nearly_ready_count"])
    col8.metric("Strongest Build Area", evidence_summary["strongest_build_area"])
    col9.metric("Weakest Build Area", evidence_summary["weakest_build_area"])

    st.metric("Dashboard Status", evidence_summary["dashboard_status"])

    # 2. Report scope selector
    st.markdown("### Report Scope")
    scope_options = ["Portfolio-level report"] + build_client_selector_options(clients)
    selected_scope = st.selectbox(
        "Select export scope",
        options=scope_options,
        label_visibility="collapsed",
    )

    if selected_scope == "Portfolio-level report":
        export_client_id = None
    else:
        export_client = get_client_by_selector_label(clients, selected_scope)
        export_client_id = export_client["client_id"] if export_client else None

    # 3. Export buttons
    st.markdown("### Export Formats")

    md_text = export_markdown_capstone_report(clients, stages, indicators, export_client_id)
    md_filename = build_export_filename(
        "build_9_capstone_report" if not export_client_id
        else f"build_9_capstone_report_{export_client_id.lower()}",
        "md",
    )
    st.download_button(
        label="Download Markdown Capstone Report",
        data=md_text,
        file_name=md_filename,
        mime="text/markdown",
    )

    csv_text = export_csv_text(clients, stages, indicators)
    st.download_button(
        label="Download CSV Evidence Table",
        data=csv_text,
        file_name=build_export_filename("build_9_capstone_evidence_table", "csv"),
        mime="text/csv",
    )

    json_text = export_json_evidence_pack(clients, stages, indicators)
    st.download_button(
        label="Download JSON Evidence Pack",
        data=json_text,
        file_name=build_export_filename("build_9_capstone_evidence_pack", "json"),
        mime="application/json",
    )

    try:
        pdf_bytes = export_pdf_bytes(md_text)
        pdf_filename = build_export_filename(
            "build_9_capstone_report" if not export_client_id
            else f"build_9_capstone_report_{export_client_id.lower()}",
            "pdf",
        )
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=pdf_filename,
            mime="application/pdf",
        )
    except ImportError:
        st.caption("PDF export unavailable — reportlab not installed.")

    try:
        chart_bytes = export_summary_chart_png_bytes(clients, stages, indicators)
        st.download_button(
            label="Download PNG Summary Chart",
            data=chart_bytes,
            file_name=build_export_filename("build_9_capstone_readiness_chart", "png"),
            mime="image/png",
        )
    except ImportError:
        st.caption("Chart export unavailable — matplotlib not installed.")

    # 4. Portfolio evidence summary text preview
    st.markdown("### Portfolio Evidence Summary Text")
    summary_text = build_portfolio_evidence_summary_text(clients, stages, indicators)
    st.markdown(summary_text)

    # 5. Consulting interpretation
    st.divider()
    st.markdown(
        "The export centre turns the capstone dashboard into reusable portfolio evidence. "
        "It packages the end-to-end AI adoption journey, cross-build evidence, client "
        "recommendations, and capstone readiness position into formats suitable for review, "
        "demonstration, and future commercial presentation."
    )


def render_phase_8(clients, stages, indicators):
    st.caption("Final review / Phase 8")
    st.subheader("Final Review and Commercial Positioning")

    st.info(
        "This final review uses synthetic portfolio data only. It summarises Build 9 as a "
        "portfolio-ready capstone connecting the full AI adoption consulting journey across Builds 1–8."
    )

    evidence_summary = build_portfolio_evidence_summary(clients, stages, indicators)

    # 1. Completion status metrics
    st.markdown("### Build 9 Completion Status")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Clients", evidence_summary["total_clients"])
    col2.metric("Total Cross-Build Stages", evidence_summary["total_cross_build_stages"])
    col3.metric("Total Build Areas", evidence_summary["total_build_areas"])
    col4.metric("Completed Stages", evidence_summary["completed_stage_count"])

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Strong / Very Strong Evidence", evidence_summary["strong_or_very_strong_evidence_count"])
    col6.metric("Capstone Ready", evidence_summary["capstone_ready_count"])
    col7.metric("Nearly Ready", evidence_summary["nearly_ready_count"])
    col8.metric("Dashboard Status", evidence_summary["dashboard_status"])

    # 2. Commercial positioning summary
    st.markdown("### Commercial Positioning")
    st.markdown(
        "Build 9 positions the portfolio as an end-to-end AI adoption consulting toolkit for "
        "small organisations. It shows how a consultant can move from readiness diagnosis to "
        "document intelligence, staff training, governance, ROI review, delivery tracking, and "
        "final capstone reporting."
    )

    # 3. Portfolio value summary
    st.markdown("### Portfolio Value")
    st.markdown(
        "The capstone demonstrates consulting thinking, software implementation, deterministic AI "
        "workflow design, synthetic data modelling, governance awareness, reporting, and commercial "
        "product packaging."
    )

    # 4. Limitations
    st.markdown("### Limitations")
    st.markdown(
        "This is a synthetic portfolio demonstration. It does not use real client data, live "
        "integrations, external LLM APIs, authentication, databases, or production deployment."
    )

    # 5. Recommended next steps
    st.markdown("### Recommended Next Steps")
    st.markdown(
        "Recommended next steps are to polish the wider portfolio README, record screenshots or "
        "demo walkthroughs, and prepare a short commercial case study explaining how Builds 1–9 "
        "form one consulting offer."
    )


def main():
    st.set_page_config(
        page_title="Build 9 — AI Adoption Consulting Capstone Dashboard",
        layout="wide",
    )
    st.markdown(_PORTFOLIO_CSS, unsafe_allow_html=True)

    clients = get_synthetic_capstone_clients()
    stages = get_synthetic_cross_build_stages()
    indicators = get_synthetic_capstone_indicators()

    st.title("Build 9 — AI Adoption Consulting Capstone Dashboard")
    st.markdown(
        "This dashboard connects the AI adoption consulting journey across readiness, "
        "document intelligence, training, reporting, governance, ROI, and delivery tracking."
    )

    with st.sidebar:
        st.markdown("**Build 9 — AI Adoption Consulting Capstone Dashboard**")
        st.caption("BrightPath ChatGPT Mastery · Build 9")
        st.divider()
        selected_phase = st.radio(
            "Select phase",
            options=ACTIVE_PHASES,
            label_visibility="collapsed",
        )
        st.divider()
        st.caption("All 8 phases active · Build 9 complete")
        st.divider()
        st.caption(
            "Synthetic data only. Not professional consulting, legal, financial, or HR advice."
        )

    if selected_phase == PHASE_NAVIGATION[7]:
        render_phase_8(clients, stages, indicators)
    elif selected_phase == PHASE_NAVIGATION[6]:
        render_phase_7(clients, stages, indicators)
    elif selected_phase == PHASE_NAVIGATION[5]:
        render_phase_6(clients, stages, indicators)
    elif selected_phase == PHASE_NAVIGATION[4]:
        render_phase_5(clients, stages, indicators)
    elif selected_phase == PHASE_NAVIGATION[3]:
        render_phase_4(clients, stages, indicators)
    elif selected_phase == PHASE_NAVIGATION[2]:
        render_phase_3(clients, stages, indicators)
    elif selected_phase == PHASE_NAVIGATION[1]:
        render_phase_2(clients, stages, indicators)
    elif selected_phase == PHASE_NAVIGATION[0]:
        render_phase_1(clients, stages, indicators)


if __name__ == "__main__":
    main()
