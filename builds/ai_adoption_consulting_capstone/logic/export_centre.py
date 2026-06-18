"""Export centre and portfolio evidence pack for Build 9 Phase 7."""

import csv
import io
import json
import re

from logic.capstone_dashboard import (
    build_capstone_snapshot,
    build_portfolio_dashboard_context,
)
from logic.capstone_overview import summarise_phase_1_capstone
from logic.capstone_report import build_full_capstone_report
from logic.client_journey import (
    add_journey_recommendations,
    build_all_client_journey_summaries,
)
from logic.cross_build_insights import (
    add_cross_build_recommendations,
    build_all_cross_build_summaries,
    summarise_cross_build_insights,
)
from logic.recommendation_pathway import (
    add_consulting_recommendation_text,
    build_all_consulting_recommendations,
    summarise_recommendation_pathways,
)


def export_markdown_capstone_report(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
    client_id: str | None = None,
) -> str:
    """Return Markdown capstone report text."""
    return build_full_capstone_report(clients, stages, indicators, client_id)


def build_csv_evidence_rows(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
) -> list[dict]:
    """Return flat capstone evidence rows, one per client/build stage combination."""
    journey_summaries = build_all_client_journey_summaries(clients, stages, indicators)
    recommendations = add_consulting_recommendation_text(
        build_all_consulting_recommendations(journey_summaries)
    )
    rec_by_client = {r["client_id"]: r for r in recommendations}

    indicators_by_client = {i["client_id"]: i for i in indicators}
    clients_by_id = {c["client_id"]: c for c in clients}

    rows = []
    for stage in stages:
        client_id = stage.get("client_id", "")
        client = clients_by_id.get(client_id, {})
        rec = rec_by_client.get(client_id, {})
        indicator = indicators_by_client.get(client_id, {})

        rows.append(
            {
                "client_id": client_id,
                "organisation_name": stage.get("organisation_name", ""),
                "sector": client.get("sector", ""),
                "staff_count": client.get("staff_count", ""),
                "capstone_stage": client.get("capstone_stage", ""),
                "build_number": stage.get("build_number", ""),
                "build_name": stage.get("build_name", ""),
                "journey_stage": stage.get("journey_stage", ""),
                "stage_status": stage.get("stage_status", ""),
                "evidence_strength": stage.get("evidence_strength", ""),
                "consulting_value": stage.get("consulting_value", ""),
                "readiness_position": indicator.get("readiness_position", ""),
                "governance_position": indicator.get("governance_position", ""),
                "training_position": indicator.get("training_position", ""),
                "roi_position": indicator.get("roi_position", ""),
                "delivery_position": indicator.get("delivery_position", ""),
                "commercial_position": indicator.get("commercial_position", ""),
                "overall_capstone_status": indicator.get("overall_capstone_status", ""),
                "recommended_next_step": rec.get("consulting_recommendation", ""),
            }
        )
    return rows


def export_csv_text(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
) -> str:
    """Return CSV evidence text with headers."""
    rows = build_csv_evidence_rows(clients, stages, indicators)
    if not rows:
        return ""

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def export_json_evidence_pack(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
) -> str:
    """Return pretty JSON evidence pack."""
    phase_1 = summarise_phase_1_capstone(clients, stages, indicators)
    journey_summaries = add_journey_recommendations(
        build_all_client_journey_summaries(clients, stages, indicators)
    )
    cross_build_summaries = add_cross_build_recommendations(
        build_all_cross_build_summaries(stages)
    )
    recommendations = add_consulting_recommendation_text(
        build_all_consulting_recommendations(journey_summaries)
    )
    context = build_portfolio_dashboard_context(clients, stages, indicators)
    snapshot = build_capstone_snapshot(context)
    evidence_summary = build_portfolio_evidence_summary(clients, stages, indicators)

    pack = {
        "clients": clients,
        "cross_build_stages": stages,
        "capstone_indicators": indicators,
        "phase_1_summary": phase_1,
        "client_journey_summaries": journey_summaries,
        "cross_build_summaries": cross_build_summaries,
        "consulting_recommendations": recommendations,
        "dashboard_snapshot": snapshot,
        "portfolio_evidence_summary": evidence_summary,
    }
    return json.dumps(pack, indent=2)


def build_export_filename(base_name: str, extension: str) -> str:
    """Return safe lowercase filename with extension."""
    ext = extension.lstrip(".")
    name = base_name.lower()
    name = name.replace(" ", "_")
    name = re.sub(r"[^a-z0-9_\-]", "", name)
    if name.endswith(f".{ext}"):
        return name
    return f"{name}.{ext}"


def build_portfolio_evidence_summary(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
) -> dict:
    """Return final portfolio evidence summary."""
    phase_1 = summarise_phase_1_capstone(clients, stages, indicators)
    journey_summaries = build_all_client_journey_summaries(clients, stages, indicators)
    recommendations = add_consulting_recommendation_text(
        build_all_consulting_recommendations(journey_summaries)
    )
    pathway_summary = summarise_recommendation_pathways(recommendations)
    cross_build_summaries = build_all_cross_build_summaries(stages)
    insight_summary = summarise_cross_build_insights(cross_build_summaries)
    context = build_portfolio_dashboard_context(clients, stages, indicators)
    snapshot = build_capstone_snapshot(context)

    strong_or_very_strong = sum(
        1
        for s in stages
        if s.get("evidence_strength") in ("Strong", "Very strong")
    )

    return {
        "total_clients": phase_1["total_clients"],
        "total_cross_build_stages": phase_1["total_cross_build_stages"],
        "total_build_areas": insight_summary["total_build_areas"],
        "completed_stage_count": phase_1["completed_stage_count"],
        "in_progress_stage_count": phase_1["in_progress_stage_count"],
        "needs_review_stage_count": phase_1["needs_review_stage_count"],
        "strong_or_very_strong_evidence_count": strong_or_very_strong,
        "capstone_ready_count": pathway_summary["capstone_ready_count"],
        "nearly_ready_count": pathway_summary["nearly_ready_count"],
        "needs_strengthening_count": pathway_summary["needs_strengthening_count"],
        "not_ready_count": pathway_summary["not_ready_count"],
        "strongest_build_area": insight_summary["strongest_build_area"],
        "weakest_build_area": insight_summary["weakest_build_area"],
        "dashboard_status": snapshot["dashboard_status"],
    }


def build_portfolio_evidence_summary_text(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
) -> str:
    """Return concise Markdown portfolio evidence summary."""
    summary = build_portfolio_evidence_summary(clients, stages, indicators)

    lines = [
        "## Portfolio Evidence Summary\n",
        "**What Build 9 does:** Build 9 is the AI adoption consulting capstone dashboard. "
        "It connects the outputs of Builds 1–8 into one coherent client-facing portfolio view, "
        "showing how a consultant moves an organisation from initial readiness diagnosis "
        "through to tracked implementation delivery.\n",
        "> **Synthetic data disclaimer:** This summary uses synthetic portfolio data only. "
        "All organisations, stages, and evidence records are fictional. "
        "Human review is required before any real-world consulting use.\n",
        "**Builds 1–8 evidence summary:**",
        f"- Journey stages across all clients: {summary['total_cross_build_stages']}",
        f"- Completed stages: {summary['completed_stage_count']}",
        f"- In progress: {summary['in_progress_stage_count']}",
        f"- Needs review: {summary['needs_review_stage_count']}",
        f"- Strong or very strong evidence: {summary['strong_or_very_strong_evidence_count']} stages\n",
        "**Capstone readiness position:**",
        f"- Capstone ready: {summary['capstone_ready_count']}",
        f"- Nearly ready: {summary['nearly_ready_count']}",
        f"- Needs strengthening: {summary['needs_strengthening_count']}",
        f"- Not ready: {summary['not_ready_count']}\n",
        f"**Strongest build area:** {summary['strongest_build_area']}",
        f"**Weakest build area:** {summary['weakest_build_area']}\n",
        "**Consulting and product value:** The Export Centre packages the full capstone "
        "output into formats suitable for portfolio review, business development conversations, "
        "and prospective client demonstrations. It shows that the consulting practice can "
        "produce structured evidence-backed documents quickly, using deterministic logic "
        "applied to collected consulting evidence.\n",
        f"**Dashboard status:** {summary['dashboard_status']}",
        "**Recommended next step:** Use the downloaded evidence pack to support a portfolio "
        "review, client demonstration, or commercial follow-up conversation.",
    ]
    return "\n".join(lines) + "\n"


def export_pdf_bytes(markdown_text: str) -> bytes:
    """Return basic PDF bytes from Markdown-like text."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    except ImportError as exc:
        raise ImportError(
            "reportlab is required for PDF export. Install it with: pip install reportlab"
        ) from exc

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm)
    styles = getSampleStyleSheet()
    story = []

    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 4 * mm))
            continue

        if stripped.startswith("# "):
            para = Paragraph(stripped[2:], styles["Title"])
        elif stripped.startswith("## "):
            para = Paragraph(stripped[3:], styles["Heading2"])
        elif stripped.startswith("### "):
            para = Paragraph(stripped[4:], styles["Heading3"])
        elif stripped.startswith("> "):
            para = Paragraph(stripped[2:], styles["Italic"])
        elif stripped.startswith("- "):
            para = Paragraph(f"• {stripped[2:]}", styles["Normal"])
        elif stripped.startswith("| ") and stripped.endswith(" |"):
            para = Paragraph(stripped.replace("|", " | "), styles["Code"])
        else:
            para = Paragraph(stripped, styles["Normal"])

        story.append(para)
        story.append(Spacer(1, 2 * mm))

    doc.build(story)
    return buffer.getvalue()


def export_summary_chart_png_bytes(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
) -> bytes:
    """Return simple PNG bytes showing capstone readiness counts."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(
            "matplotlib is required for chart export. Install it with: pip install matplotlib"
        ) from exc

    summary = build_portfolio_evidence_summary(clients, stages, indicators)

    labels = ["Capstone ready", "Nearly ready", "Needs strengthening", "Not ready"]
    values = [
        summary["capstone_ready_count"],
        summary["nearly_ready_count"],
        summary["needs_strengthening_count"],
        summary["not_ready_count"],
    ]
    colours = ["#2ecc71", "#f39c12", "#e67e22", "#e74c3c"]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(labels, values, color=colours, edgecolor="white")
    ax.set_title("Capstone Readiness — Client Portfolio", fontsize=13, pad=12)
    ax.set_ylabel("Number of clients")
    ax.set_ylim(0, max(values) + 1 if any(v > 0 for v in values) else 3)
    ax.bar_label(bars, padding=3)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=120)
    plt.close(fig)
    return buffer.getvalue()
