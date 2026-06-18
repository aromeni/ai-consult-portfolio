"""Client Follow-up Report Builder for Build 7 Phase 7.

Converts synthetic adoption evidence from Phases 1–6 into a structured
Markdown report suitable for a consultant to review with a client.

All content is based on synthetic demo data only. No real client data.
"""

from logic.roi_summary import (
    build_all_workflow_roi_summaries,
    summarise_portfolio_roi,
)
from logic.workflow_impact import (
    add_recommendations_to_impact_summaries,
    build_all_workflow_impact_summaries,
)
from logic.training_readiness import (
    add_training_recommendations_to_summaries,
    build_all_training_readiness_summaries,
)
from logic.risk_quality_review import (
    add_risk_quality_recommendations,
    build_all_risk_quality_summaries,
)
from logic.decision_tracker import (
    add_follow_up_evidence_notes,
    build_all_decision_summaries,
)


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------


def get_organisation_records(records: list[dict], organisation_id: str) -> list[dict]:
    """Return all records for one organisation."""
    return [r for r in records if r.get("organisation_id") == organisation_id]


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------


def build_markdown_table(rows: list[dict], columns: list[str]) -> str:
    """Return a simple Markdown table from a list of row dicts.

    Preserves column order. Converts all values to strings.
    Returns an empty string if rows is empty.
    """
    if not rows:
        return ""

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"

    body_lines = []
    for row in rows:
        cells = [str(row.get(col, "")) for col in columns]
        body_lines.append("| " + " | ".join(cells) + " |")

    return "\n".join([header, separator] + body_lines)


# ---------------------------------------------------------------------------
# Report sections
# ---------------------------------------------------------------------------


def build_report_title(organisation_name: str) -> str:
    """Return a Markdown report title."""
    return f"# AI Adoption Follow-up Report — {organisation_name}"


def build_report_disclaimer() -> str:
    """Return the synthetic-data disclaimer section."""
    return (
        "> **Disclaimer:** This report uses synthetic portfolio data only. "
        "It is for demonstration purposes and does not contain real client, staff, "
        "learner, safeguarding, HR, personal, confidential, or regulated data."
    )


def build_executive_summary(records: list[dict]) -> str:
    """Return a short Markdown executive summary."""
    roi_summaries = build_all_workflow_roi_summaries(records)
    portfolio = summarise_portfolio_roi(roi_summaries)
    decision_summaries = build_all_decision_summaries(records)

    workflow_count = portfolio["workflow_count"]
    weekly_hours = portfolio["total_weekly_hours_saved"]
    annual_hours = portfolio["total_annual_hours_saved"]
    annual_value = portfolio["total_annual_value_equivalent"]

    scale_count = sum(
        1 for s in decision_summaries
        if s["decision_outcome"] in ("Scale", "Scale with monitoring")
    )
    concern_count = sum(
        1 for s in decision_summaries
        if s["decision_outcome"] in ("Stop", "Pause", "Continue with controls")
    )

    lines = [
        "## Executive Summary",
        "",
        f"This report covers **{workflow_count} workflow(s)** tracked during the AI adoption pilot. "
        f"Across these workflows, the pilot is saving approximately "
        f"**{weekly_hours:.1f} hours per week** and **{annual_hours:.1f} hours per year**, "
        f"with an estimated value equivalent of **£{annual_value:,.0f} per year**.",
        "",
        f"**{scale_count}** workflow(s) are ready to scale or scale with monitoring. "
        f"**{concern_count}** workflow(s) require a stop, pause, or continue-with-controls "
        "decision based on risk, quality, or governance signals.",
        "",
        "> Estimated value equivalents use synthetic hourly-rate assumptions. "
        "They are directional consulting indicators, not audited financial ROI.",
    ]
    return "\n".join(lines)


def build_roi_section(records: list[dict]) -> str:
    """Return a Markdown ROI and value summary section."""
    roi_summaries = build_all_workflow_roi_summaries(records)
    portfolio = summarise_portfolio_roi(roi_summaries)

    lines = [
        "## ROI and Value Summary",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| Total weekly hours saved | {portfolio['total_weekly_hours_saved']:.1f} hrs |",
        f"| Total monthly hours saved | {portfolio['total_monthly_hours_saved']:.1f} hrs |",
        f"| Total annual hours saved | {portfolio['total_annual_hours_saved']:.1f} hrs |",
        f"| Weekly estimated value equivalent | £{portfolio['total_weekly_value_equivalent']:,.2f} |",
        f"| Monthly estimated value equivalent | £{portfolio['total_monthly_value_equivalent']:,.2f} |",
        f"| Annual estimated value equivalent | £{portfolio['total_annual_value_equivalent']:,.2f} |",
        f"| Average efficiency gain | {portfolio['average_efficiency_gain_percent']:.1f}% |",
        f"| Average confidence change | {portfolio['average_confidence_change']:.2f} |",
        "",
        "> All value figures are synthetic consulting estimates only.",
    ]
    return "\n".join(lines)


def build_workflow_impact_section(records: list[dict]) -> str:
    """Return a Markdown workflow impact section."""
    impact_summaries = build_all_workflow_impact_summaries(records)
    enriched = add_recommendations_to_impact_summaries(impact_summaries)

    rows = [
        {
            "Workflow": s["workflow_name"],
            "Related build": s["related_build"],
            "Impact status": s["workflow_impact_status"],
            "Primary bottleneck": s["primary_bottleneck"],
            "Efficiency gain %": f"{s['efficiency_gain_percent']:.1f}%",
            "Weekly hrs saved": f"{s['weekly_hours_saved']:.1f}",
        }
        for s in enriched
    ]

    columns = [
        "Workflow", "Related build", "Impact status",
        "Primary bottleneck", "Efficiency gain %", "Weekly hrs saved",
    ]

    lines = [
        "## Workflow Impact",
        "",
        build_markdown_table(rows, columns),
    ]
    return "\n".join(lines)


def build_training_readiness_section(records: list[dict]) -> str:
    """Return a Markdown training readiness section."""
    tr_summaries = build_all_training_readiness_summaries(records)
    enriched = add_training_recommendations_to_summaries(tr_summaries)

    rows = [
        {
            "Workflow": s["workflow_name"],
            "Staff group": s["staff_group"],
            "Training %": f"{s['training_completion_rate']:.0%}",
            "Confidence after": s["confidence_after"],
            "Readiness band": s["training_readiness_band"],
            "Support need": s["training_support_need"],
            "Adoption readiness": s["staff_adoption_readiness"],
        }
        for s in enriched
    ]

    columns = [
        "Workflow", "Staff group", "Training %",
        "Confidence after", "Readiness band", "Support need", "Adoption readiness",
    ]

    lines = [
        "## Training Readiness",
        "",
        build_markdown_table(rows, columns),
    ]
    return "\n".join(lines)


def build_risk_quality_section(records: list[dict]) -> str:
    """Return a Markdown risk and quality section."""
    rq_summaries = build_all_risk_quality_summaries(records)
    enriched = add_risk_quality_recommendations(rq_summaries)

    rows = [
        {
            "Workflow": s["workflow_name"],
            "Quality level": s["quality_level"],
            "Risk level": s["risk_level"],
            "Responsible adoption status": s["responsible_adoption_status"],
            "Control need": s["control_need"],
            "Scaling permission": s["scaling_permission"],
        }
        for s in enriched
    ]

    columns = [
        "Workflow", "Quality level", "Risk level",
        "Responsible adoption status", "Control need", "Scaling permission",
    ]

    lines = [
        "## Risk and Quality Review",
        "",
        build_markdown_table(rows, columns),
    ]
    return "\n".join(lines)


def build_decision_section(records: list[dict]) -> str:
    """Return a Markdown decision and follow-up section."""
    decision_summaries = build_all_decision_summaries(records)

    rows = [
        {
            "Workflow": s["workflow_name"],
            "Decision outcome": s["decision_outcome"],
            "Confidence": s["decision_confidence"],
            "Reason": s["decision_reason"],
            "Next action": s["next_action"],
        }
        for s in decision_summaries
    ]

    columns = ["Workflow", "Decision outcome", "Confidence", "Reason", "Next action"]

    lines = [
        "## Decision and Follow-up Evidence",
        "",
        build_markdown_table(rows, columns),
    ]
    return "\n".join(lines)


def build_follow_up_evidence_section(records: list[dict]) -> str:
    """Return a Markdown follow-up evidence section."""
    decision_summaries = build_all_decision_summaries(records)
    enriched = add_follow_up_evidence_notes(decision_summaries)

    lines = ["## Follow-up Evidence Notes", ""]

    for s in enriched:
        workflow_name = s["workflow_name"]
        evidence_note = s.get("evidence_note", "")
        follow_up_note = s.get("follow_up_evidence_note", "")

        lines.append(f"**{workflow_name}**")
        if evidence_note:
            lines.append(f"- Adoption evidence: {evidence_note}")
        if follow_up_note:
            lines.append(f"- Follow-up note: {follow_up_note}")
        lines.append("")

    return "\n".join(lines)


def build_recommendations_section(records: list[dict]) -> str:
    """Return a Markdown recommendations section."""
    impact_summaries = build_all_workflow_impact_summaries(records)
    impact_enriched = add_recommendations_to_impact_summaries(impact_summaries)

    tr_summaries = build_all_training_readiness_summaries(records)
    tr_enriched = add_training_recommendations_to_summaries(tr_summaries)

    rq_summaries = build_all_risk_quality_summaries(records)
    rq_enriched = add_risk_quality_recommendations(rq_summaries)

    decision_summaries = build_all_decision_summaries(records)

    impact_map = {s["workflow_id"]: s["recommended_action"] for s in impact_enriched}
    tr_map = {s["workflow_id"]: s["training_recommendation"] for s in tr_enriched}
    rq_map = {s["workflow_id"]: s["risk_quality_recommendation"] for s in rq_enriched}
    decision_map = {s["workflow_id"]: s["next_action"] for s in decision_summaries}

    lines = ["## Recommendations", ""]

    for record in records:
        wf_id = record.get("workflow_id", "")
        wf_name = record.get("workflow_name", "")

        lines.append(f"**{wf_name}**")
        if wf_id in decision_map:
            lines.append(f"- Decision: {decision_map[wf_id]}")
        if wf_id in rq_map:
            lines.append(f"- Risk and quality: {rq_map[wf_id]}")
        if wf_id in tr_map:
            lines.append(f"- Training: {tr_map[wf_id]}")
        if wf_id in impact_map:
            lines.append(f"- Workflow impact: {impact_map[wf_id]}")
        lines.append("")

    return "\n".join(lines)


def build_next_review_section() -> str:
    """Return a short deterministic next-review section."""
    lines = [
        "## Next Review",
        "",
        "Review these adoption decisions again after the next pilot period. "
        "Focus on whether controls have improved, staff confidence has increased, "
        "and workflows marked for monitoring have remained safe and useful.",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Full report
# ---------------------------------------------------------------------------


def build_full_follow_up_report(
    records: list[dict],
    organisation_id: str | None = None,
) -> str:
    """Build a complete Markdown follow-up report.

    If organisation_id is provided, reports only on that organisation's records.
    If None, builds a portfolio-level report across all records.
    """
    if organisation_id is not None:
        filtered = get_organisation_records(records, organisation_id)
        if not filtered:
            return f"# AI Adoption Follow-up Report\n\nNo records found for organisation ID: {organisation_id}"
        org_name = filtered[0].get("organisation_name", organisation_id)
        report_records = filtered
    else:
        report_records = records
        org_name = "Portfolio — All Organisations"

    sections = [
        build_report_title(org_name),
        "",
        build_report_disclaimer(),
        "",
        build_executive_summary(report_records),
        "",
        build_roi_section(report_records),
        "",
        build_workflow_impact_section(report_records),
        "",
        build_training_readiness_section(report_records),
        "",
        build_risk_quality_section(report_records),
        "",
        build_decision_section(report_records),
        "",
        build_follow_up_evidence_section(report_records),
        "",
        build_recommendations_section(report_records),
        "",
        build_next_review_section(),
    ]

    return "\n".join(sections)
