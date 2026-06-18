"""Export Centre for Build 7 Phase 8.

Packages synthetic adoption evidence from Phases 1–7 into downloadable formats.

All content is based on synthetic demo data only. No real client data.
"""

import csv
import io
import json

from logic.follow_up_report import build_full_follow_up_report
from logic.roi_summary import build_all_workflow_roi_summaries, summarise_portfolio_roi
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
from logic.decision_tracker import build_all_decision_summaries


# ---------------------------------------------------------------------------
# Markdown export
# ---------------------------------------------------------------------------


def export_markdown_report(
    records: list[dict],
    organisation_id: str | None = None,
) -> str:
    """Return Markdown follow-up report text."""
    return build_full_follow_up_report(records, organisation_id=organisation_id)


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------


def build_csv_export_rows(records: list[dict]) -> list[dict]:
    """Return flat rows combining ROI, workflow impact, training, risk, and decision fields."""
    roi_summaries = build_all_workflow_roi_summaries(records)
    impact_summaries = build_all_workflow_impact_summaries(records)
    impact_enriched = add_recommendations_to_impact_summaries(impact_summaries)
    tr_summaries = build_all_training_readiness_summaries(records)
    tr_enriched = add_training_recommendations_to_summaries(tr_summaries)
    rq_summaries = build_all_risk_quality_summaries(records)
    rq_enriched = add_risk_quality_recommendations(rq_summaries)
    decision_summaries = build_all_decision_summaries(records)

    roi_map = {s["workflow_id"]: s for s in roi_summaries}
    impact_map = {s["workflow_id"]: s for s in impact_enriched}
    tr_map = {s["workflow_id"]: s for s in tr_enriched}
    rq_map = {s["workflow_id"]: s for s in rq_enriched}
    decision_map = {s["workflow_id"]: s for s in decision_summaries}

    rows = []
    for record in records:
        wf_id = record.get("workflow_id", "")
        roi = roi_map.get(wf_id, {})
        impact = impact_map.get(wf_id, {})
        tr = tr_map.get(wf_id, {})
        rq = rq_map.get(wf_id, {})
        dec = decision_map.get(wf_id, {})

        rows.append({
            "organisation_id": record.get("organisation_id", ""),
            "organisation_name": record.get("organisation_name", ""),
            "workflow_id": wf_id,
            "workflow_name": record.get("workflow_name", ""),
            "related_build": record.get("related_build", ""),
            "staff_group": record.get("staff_group", ""),
            "pilot_status": record.get("pilot_status", ""),
            "adoption_status": record.get("adoption_status", ""),
            "weekly_hours_saved": roi.get("weekly_hours_saved", ""),
            "annual_hours_saved": roi.get("annual_hours_saved", ""),
            "efficiency_gain_percent": roi.get("efficiency_gain_percent", ""),
            "annual_value_equivalent": roi.get("annual_value_equivalent", ""),
            "time_saving_band": roi.get("time_saving_band", ""),
            "adoption_value_indicator": roi.get("adoption_value_indicator", ""),
            "workflow_impact_status": impact.get("workflow_impact_status", ""),
            "primary_bottleneck": impact.get("primary_bottleneck", ""),
            "recommended_action": impact.get("recommended_action", ""),
            "training_completion_rate": tr.get("training_completion_rate", ""),
            "confidence_before": tr.get("confidence_before", ""),
            "confidence_after": tr.get("confidence_after", ""),
            "training_readiness_band": tr.get("training_readiness_band", ""),
            "staff_adoption_readiness": tr.get("staff_adoption_readiness", ""),
            "training_support_need": tr.get("training_support_need", ""),
            "quality_level": rq.get("quality_level", ""),
            "risk_level": rq.get("risk_level", ""),
            "responsible_adoption_status": rq.get("responsible_adoption_status", ""),
            "control_need": rq.get("control_need", ""),
            "scaling_permission": rq.get("scaling_permission", ""),
            "decision_outcome": dec.get("decision_outcome", ""),
            "decision_confidence": dec.get("decision_confidence", ""),
            "decision_reason": dec.get("decision_reason", ""),
            "next_action": dec.get("next_action", ""),
        })

    return rows


def export_csv_text(records: list[dict]) -> str:
    """Return CSV text of all adoption evidence fields."""
    rows = build_csv_export_rows(records)
    if not rows:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


# ---------------------------------------------------------------------------
# JSON export
# ---------------------------------------------------------------------------


def export_json_text(records: list[dict]) -> str:
    """Return pretty-printed JSON of all adoption evidence rows."""
    rows = build_csv_export_rows(records)
    return json.dumps(rows, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Filename helper
# ---------------------------------------------------------------------------


def build_export_filename(base_name: str, extension: str) -> str:
    """Return a safe lowercase filename with extension.

    Example: build_export_filename("Build 7 AI Adoption Export", "csv")
    → "build_7_ai_adoption_export.csv"
    """
    safe = base_name.lower().replace(" ", "_")
    safe = "".join(c for c in safe if c.isalnum() or c == "_")
    return f"{safe}.{extension}"


# ---------------------------------------------------------------------------
# Completion summary and review
# ---------------------------------------------------------------------------


def build_completion_summary(records: list[dict]) -> dict:
    """Return final Build 7 completion metrics."""
    roi_summaries = build_all_workflow_roi_summaries(records)
    portfolio = summarise_portfolio_roi(roi_summaries)
    decision_summaries = build_all_decision_summaries(records)
    rq_summaries = build_all_risk_quality_summaries(records)

    org_ids = {r.get("organisation_id") for r in records if r.get("organisation_id")}

    scale_or_scale_with_monitoring = sum(
        1 for s in decision_summaries
        if s["decision_outcome"] in ("Scale", "Scale with monitoring")
    )
    continue_or_continue_with_controls = sum(
        1 for s in decision_summaries
        if s["decision_outcome"] in ("Continue", "Continue with controls")
    )
    stop_or_pause = sum(
        1 for s in decision_summaries
        if s["decision_outcome"] in ("Stop", "Pause")
    )
    governance_review_count = sum(
        1 for s in rq_summaries
        if s.get("responsible_adoption_status") == "Requires governance review"
    )

    return {
        "total_organisations": len(org_ids),
        "total_workflows": portfolio["workflow_count"],
        "total_weekly_hours_saved": portfolio["total_weekly_hours_saved"],
        "total_annual_hours_saved": portfolio["total_annual_hours_saved"],
        "scale_or_scale_with_monitoring_count": scale_or_scale_with_monitoring,
        "continue_or_continue_with_controls_count": continue_or_continue_with_controls,
        "stop_or_pause_count": stop_or_pause,
        "governance_review_count": governance_review_count,
    }


def build_completion_review_text(records: list[dict]) -> str:
    """Return a concise Markdown completion review for Build 7."""
    summary = build_completion_summary(records)

    lines = [
        "# Build 7 — Completion Review",
        "",
        "## What Build 7 Does",
        "",
        "Build 7 is a deterministic AI adoption ROI and impact tracker built in Python and Streamlit. "
        "It uses synthetic portfolio data to demonstrate how a consultant could record, review, and "
        "report on AI adoption metrics after an initial pilot period. It is not connected to any "
        "external API, database, or real client dataset.",
        "",
        "## Phases Completed",
        "",
        "| Phase | Title |",
        "| --- | --- |",
        "| Phase 1 | Adoption Metrics Setup |",
        "| Phase 2 | ROI Summary Engine |",
        "| Phase 3 | Workflow Impact and Bottleneck Analysis |",
        "| Phase 4 | Training, Confidence, and Adoption Readiness Review |",
        "| Phase 5 | Risk, Quality, and Responsible Adoption Review |",
        "| Phase 6 | Decision Tracker and Client Follow-up Evidence |",
        "| Phase 7 | Client Follow-up Report Builder |",
        "| Phase 8 | Export Centre and Completion Review |",
        "",
        "## Portfolio Metrics (Synthetic)",
        "",
        f"- Organisations tracked: {summary['total_organisations']}",
        f"- Workflows tracked: {summary['total_workflows']}",
        f"- Total weekly hours saved (synthetic): {summary['total_weekly_hours_saved']:.1f}",
        f"- Total annual hours saved (synthetic): {summary['total_annual_hours_saved']:.1f}",
        f"- Scale or scale with monitoring: {summary['scale_or_scale_with_monitoring_count']}",
        f"- Continue or continue with controls: {summary['continue_or_continue_with_controls_count']}",
        f"- Stop or pause: {summary['stop_or_pause_count']}",
        f"- Workflows requiring governance review: {summary['governance_review_count']}",
        "",
        "## Synthetic Data Disclaimer",
        "",
        "> All organisations, workflows, staff groups, metrics, and decisions in Build 7 are "
        "fictional synthetic examples created for portfolio demonstration. No real client data, "
        "learner data, safeguarding data, HR data, personal data, confidential data, or regulated "
        "information is used anywhere in this build.",
        "",
        "## Consulting Use Case",
        "",
        "Build 7 demonstrates how a consultant supporting small and medium organisations "
        "through AI adoption could collect structured evidence, generate ROI estimates, "
        "analyse workflow impact and training readiness, check responsible adoption signals, "
        "reach explicit decisions, and produce a client-facing follow-up report — all without "
        "manual formatting or spreadsheet work.",
        "",
        "## Limitations",
        "",
        "- All metrics are synthetic and template-based. Figures are directional indicators only.",
        "- No external APIs, LLMs, or machine-learning models are used.",
        "- The ROI value equivalents are based on synthetic hourly-rate assumptions and "
        "should not be presented as audited financial savings.",
        "- The export centre provides basic file formats only. Advanced formatting, "
        "branded templates, and presentation exports are not included.",
        "",
        "## Recommended Future Extensions",
        "",
        "- Real data input through validated CSV or form-based entry.",
        "- Trend analysis across multiple adoption periods.",
        "- Integration with a Build 1 readiness audit to provide end-to-end traceability.",
        "- Branded PDF report templates for specific client sectors.",
        "- A governance checklist linking Build 6 policy outputs to Build 7 adoption decisions.",
        "",
        "---",
        "",
        "*Build 7 Phase 8 · AI Adoption ROI and Impact Tracker · BrightPath ChatGPT Mastery Project*",
        "*Synthetic scenarios only. Human review required before any real-world use.*",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Optional PDF export
# ---------------------------------------------------------------------------


def export_pdf_bytes(markdown_text: str) -> bytes:
    """Return basic PDF bytes from Markdown-like text.

    Requires reportlab. Strips Markdown formatting and renders as plain paragraphs.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.enums import TA_LEFT
    except ImportError as exc:
        raise ImportError(
            "reportlab is required for PDF export. Install it with: pip install reportlab"
        ) from exc

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    h1_style = ParagraphStyle(
        "H1", parent=styles["Heading1"], fontSize=16, spaceAfter=12
    )
    h2_style = ParagraphStyle(
        "H2", parent=styles["Heading2"], fontSize=13, spaceAfter=8, spaceBefore=12
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"], fontSize=10, spaceAfter=6, leading=14
    )
    note_style = ParagraphStyle(
        "Note", parent=styles["Normal"], fontSize=9, spaceAfter=6, leading=13,
        leftIndent=12, textColor="grey",
    )

    story = []

    for line in markdown_text.splitlines():
        stripped = line.strip()

        if stripped.startswith("# "):
            text = stripped[2:].strip()
            story.append(Paragraph(_escape_xml(text), h1_style))
            story.append(Spacer(1, 4))

        elif stripped.startswith("## "):
            text = stripped[3:].strip()
            story.append(Paragraph(_escape_xml(text), h2_style))

        elif stripped.startswith("> "):
            text = stripped[2:].strip().lstrip("*").rstrip("*").strip()
            story.append(Paragraph(_escape_xml(text), note_style))

        elif stripped.startswith("- "):
            text = "• " + stripped[2:].strip()
            story.append(Paragraph(_escape_xml(text), body_style))

        elif stripped.startswith("| ") and "---" not in stripped:
            cells = [c.strip() for c in stripped.split("|") if c.strip()]
            text = "  |  ".join(cells)
            story.append(Paragraph(_escape_xml(text), body_style))

        elif stripped.startswith("**") and stripped.endswith("**"):
            text = stripped.strip("*")
            story.append(Paragraph(f"<b>{_escape_xml(text)}</b>", body_style))

        elif stripped == "---":
            story.append(Spacer(1, 8))

        elif stripped == "":
            story.append(Spacer(1, 4))

        else:
            text = stripped.replace("**", "")
            story.append(Paragraph(_escape_xml(text), body_style))

    doc.build(story)
    return buffer.getvalue()


def _escape_xml(text: str) -> str:
    """Escape characters that would break reportlab XML parsing."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# ---------------------------------------------------------------------------
# Optional PNG chart export
# ---------------------------------------------------------------------------


def export_summary_chart_png_bytes(records: list[dict]) -> bytes:
    """Return simple PNG bytes for a decision outcome count bar chart.

    Requires matplotlib.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(
            "matplotlib is required for chart export. Install it with: pip install matplotlib"
        ) from exc

    decision_summaries = build_all_decision_summaries(records)

    outcome_order = [
        "Stop", "Pause", "Continue with controls",
        "Review later", "Continue", "Scale with monitoring", "Scale",
    ]
    counts = {outcome: 0 for outcome in outcome_order}
    for s in decision_summaries:
        outcome = s.get("decision_outcome", "")
        if outcome in counts:
            counts[outcome] += 1

    labels = list(counts.keys())
    values = list(counts.values())

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(labels, values, color="#4472C4")
    ax.set_title("Decision Outcome Counts — Synthetic Portfolio", fontsize=12, pad=12)
    ax.set_xlabel("Decision Outcome", fontsize=10)
    ax.set_ylabel("Number of Workflows", fontsize=10)
    ax.set_ylim(0, max(values) + 1 if values else 1)
    ax.tick_params(axis="x", labelrotation=30)
    fig.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=120)
    plt.close(fig)
    buffer.seek(0)
    return buffer.getvalue()
