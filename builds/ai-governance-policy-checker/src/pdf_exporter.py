"""
PDF Exporter — AI Governance Policy Checker
Build 6 · BrightPath ChatGPT Mastery Project

Exports the governance report as a professional PDF using reportlab.
No external AI, LLM, or API calls. Synthetic/demo data only.
"""

import io
import os
import re

try:
    from reportlab.lib import colors as rl_colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        PageBreak,
        Table,
        TableStyle,
        HRFlowable,
        Image as RLImage,
    )
    _REPORTLAB_AVAILABLE = True
    _NAVY = rl_colors.HexColor("#1a2744")
    _TEAL = rl_colors.HexColor("#2d7d6e")
    _LIGHT_GREY = rl_colors.HexColor("#f5f5f5")
    _MID_GREY = rl_colors.HexColor("#cccccc")
    _AMBER = rl_colors.HexColor("#b87a2d")
    _WARN_BG = rl_colors.HexColor("#fff8e1")
    _DARK_TEXT = rl_colors.HexColor("#222222")
    _MID_TEXT = rl_colors.HexColor("#555555")
    _CAPTION_TEXT = rl_colors.HexColor("#888888")
except ImportError:
    _REPORTLAB_AVAILABLE = False
    _NAVY = _TEAL = _LIGHT_GREY = _MID_GREY = _AMBER = None
    _WARN_BG = _DARK_TEXT = _MID_TEXT = _CAPTION_TEXT = None

_RESPONSIBLE_USE_TEXT = (
    "This governance report is generated from synthetic/demo policy text only. "
    "It must not be used with real client policies, learner data, safeguarding case details, "
    "staff HR data, personal data, confidential data, or regulated information without "
    "appropriate governance, approvals, and responsible owners.\n\n"
    "This prototype does not provide legal, safeguarding, HR, compliance, data-protection, "
    "financial, medical, academic-integrity, or professional governance advice. "
    "Suggested wording directions are not legally approved policy text. They require review by "
    "appropriate responsible owners before real-world use. This is a deterministic governance "
    "review support tool, not a compliance certification system. "
    "Human review remains required before any real-world use."
)


def create_safe_pdf_filename(title: str) -> str:
    safe = re.sub(r"[^\w\s-]", "", str(title))
    safe = re.sub(r"[\s]+", "-", safe).strip("-").lower()
    return f"{safe}.pdf"


def format_pdf_text(text: str) -> str:
    """Strip Markdown formatting for plain PDF paragraphs."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*>]\s*", "", text, flags=re.MULTILINE)
    return text.strip()


def build_pdf_styles() -> dict:
    """Build reportlab paragraph styles for the governance report PDF."""
    if not _REPORTLAB_AVAILABLE:
        return {}

    base = getSampleStyleSheet()

    return {
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Heading1"],
            fontSize=22,
            textColor=_NAVY,
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            parent=base["Normal"],
            fontSize=13,
            textColor=_TEAL,
            spaceAfter=8,
            alignment=TA_CENTER,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta",
            parent=base["Normal"],
            fontSize=10,
            textColor=_MID_TEXT,
            spaceAfter=6,
            alignment=TA_CENTER,
        ),
        "cover_note": ParagraphStyle(
            "cover_note",
            parent=base["Normal"],
            fontSize=9,
            textColor=_CAPTION_TEXT,
            spaceAfter=4,
            alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontSize=15,
            textColor=_NAVY,
            spaceBefore=14,
            spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontSize=12,
            textColor=_TEAL,
            spaceBefore=10,
            spaceAfter=5,
            fontName="Helvetica-Bold",
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontSize=10,
            textColor=_NAVY,
            spaceBefore=7,
            spaceAfter=3,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontSize=9,
            textColor=_DARK_TEXT,
            spaceAfter=5,
            leading=14,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["Normal"],
            fontSize=9,
            leftIndent=14,
            spaceAfter=3,
            leading=13,
        ),
        "note": ParagraphStyle(
            "note",
            parent=base["Normal"],
            fontSize=8,
            textColor=_MID_TEXT,
            spaceAfter=4,
            leftIndent=10,
            leading=12,
        ),
        "responsible_use": ParagraphStyle(
            "responsible_use",
            parent=base["Normal"],
            fontSize=9,
            textColor=rl_colors.HexColor("#333333"),
            backColor=_WARN_BG,
            spaceAfter=6,
            leading=14,
            borderPad=6,
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base["Normal"],
            fontSize=8,
            textColor=_CAPTION_TEXT,
            spaceAfter=4,
            alignment=TA_CENTER,
        ),
    }


def add_cover_page(
    story: list,
    styles: dict,
    title: str,
    organisation_name: str = "",
    subtitle: str = "",
    generated_date: str = "",
    prototype_note: str = "",
) -> None:
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph(title, styles["cover_title"]))
    story.append(Spacer(1, 0.5 * cm))
    if organisation_name:
        story.append(Paragraph(f"Organisation: {organisation_name}", styles["cover_subtitle"]))
    if subtitle:
        story.append(Paragraph(subtitle, styles["cover_subtitle"]))
    story.append(Spacer(1, 0.5 * cm))
    if generated_date:
        story.append(Paragraph(f"Date: {generated_date}", styles["cover_meta"]))
    story.append(Spacer(1, 1.5 * cm))
    if prototype_note:
        story.append(Paragraph(prototype_note, styles["cover_note"]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "Synthetic scenarios only. Human review required before any real-world use.",
        styles["cover_note"],
    ))
    story.append(PageBreak())


def add_section_heading(story: list, styles: dict, heading: str) -> None:
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(heading, styles["h1"]))
    story.append(HRFlowable(
        width="100%", thickness=1, color=_TEAL, spaceAfter=6
    ))


def add_paragraphs_from_markdown(story: list, styles: dict, markdown_text: str) -> None:
    """Convert Markdown text to PDF story elements (headings, bullets, body)."""
    if not markdown_text:
        return

    for line in markdown_text.split("\n"):
        line = line.rstrip()

        if re.match(r"^---+$", line):
            story.append(HRFlowable(
                width="100%", thickness=0.5, color=_MID_GREY, spaceAfter=3
            ))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], styles["h2"]))
        elif line.startswith("### "):
            story.append(Paragraph(line[4:], styles["h3"]))
        elif line.startswith("# "):
            story.append(Paragraph(line[2:], styles["h1"]))
        elif line.startswith("|"):
            pass  # Tables handled separately
        elif line.startswith("> "):
            text = format_pdf_text(line[2:])
            if text:
                story.append(Paragraph(f"<i>{text}</i>", styles["note"]))
        elif re.match(r"^\s*[-*]\s+", line):
            text = format_pdf_text(re.sub(r"^\s*[-*]\s+", "", line))
            if text:
                story.append(Paragraph(f"• {text}", styles["bullet"]))
        elif re.match(r"^\d+\.\s+", line):
            m = re.match(r"^(\d+)\.\s+(.*)", line)
            if m:
                text = format_pdf_text(m.group(2))
                if text:
                    story.append(Paragraph(f"{m.group(1)}. {text}", styles["bullet"]))
        elif not line.strip():
            story.append(Spacer(1, 0.12 * cm))
        else:
            clean = format_pdf_text(line)
            if clean:
                story.append(Paragraph(clean, styles["body"]))


def add_bullet_list(story: list, styles: dict, items: list[str]) -> None:
    for item in items:
        story.append(Paragraph(f"• {item}", styles["bullet"]))
    story.append(Spacer(1, 0.2 * cm))


def add_simple_table(story: list, styles: dict, data: list[list[str]]) -> None:
    if not data:
        return

    col_count = max(len(row) for row in data)
    page_width = A4[0] - 4 * cm
    col_width = page_width / col_count

    table = Table(data, colWidths=[col_width] * col_count, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), _NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), rl_colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("BACKGROUND", (0, 1), (-1, -1), rl_colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [rl_colors.white, _LIGHT_GREY]),
        ("GRID", (0, 0), (-1, -1), 0.4, _MID_GREY),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.25 * cm))


def add_chart_image(story: list, image_path: str, title: str = "") -> None:
    """Add a chart image to the PDF story if the file exists and is readable."""
    if not image_path or not os.path.exists(image_path):
        return
    try:
        styles = build_pdf_styles()
        page_width = A4[0] - 4 * cm
        img = RLImage(image_path, width=page_width, height=page_width * 0.42)
        story.append(img)
        if title:
            story.append(Paragraph(title, styles["caption"]))
        story.append(Spacer(1, 0.3 * cm))
    except Exception:
        pass


def add_responsible_use_section(story: list, styles: dict) -> None:
    story.append(Spacer(1, 0.3 * cm))
    add_section_heading(story, styles, "Responsible-Use Boundaries")
    story.append(Paragraph(_RESPONSIBLE_USE_TEXT, styles["responsible_use"]))
    story.append(Spacer(1, 0.3 * cm))


def _extract_markdown_tables(markdown_text: str) -> list[tuple[int, int, list[list[str]]]]:
    """
    Extract Markdown tables from text.
    Returns list of (start_line_index, end_line_index, table_data).
    """
    lines = markdown_text.split("\n")
    tables: list[tuple[int, int, list[list[str]]]] = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("|"):
            start = i
            table_lines = []
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1
            data: list[list[str]] = []
            for tl in table_lines:
                stripped = tl.strip()
                if re.match(r"^\|[-| :]+\|$", stripped):
                    continue
                cells = [c.strip() for c in stripped.strip("|").split("|")]
                if cells:
                    data.append(cells)
            if len(data) > 0:
                tables.append((start, i - 1, data))
        else:
            i += 1
    return tables


def _build_analytics_summary_section(
    story: list,
    styles: dict,
    analytics: dict,
) -> None:
    """Add tabular analytics summary to the PDF before the main report content."""
    add_section_heading(story, styles, "Report Analytics Summary")

    completion = analytics.get("export_completion", {})
    if completion.get("items"):
        story.append(Paragraph("Export Completion Status", styles["h2"]))
        data = [["Output", "Status"]]
        for label, available in completion["items"].items():
            data.append([label, "Available" if available else "Not available"])
        pct = completion.get("completion_percentage", 0)
        data.append(["Completion", f"{pct}%"])
        add_simple_table(story, styles, data)

    cov = analytics.get("coverage_levels", {})
    if cov.get("counts") and cov.get("total", 0) > 0:
        story.append(Paragraph("Policy Coverage Level Distribution", styles["h2"]))
        data = [["Coverage Level", "Domains"]]
        for level, count in cov["counts"].items():
            data.append([level, str(count)])
        add_simple_table(story, styles, data)

    gaps = analytics.get("gap_severities", {})
    if gaps.get("counts") and gaps.get("total", 0) > 0:
        story.append(Paragraph("Policy Gap Severity Distribution", styles["h2"]))
        data = [["Gap Severity", "Count"]]
        for sev, count in gaps["counts"].items():
            data.append([sev, str(count)])
        add_simple_table(story, styles, data)

    recs = analytics.get("recommendation_priorities", {})
    if recs.get("counts") and recs.get("total", 0) > 0:
        story.append(Paragraph("Recommendation Priority Distribution", styles["h2"]))
        data = [["Priority", "Count"]]
        for pri, count in recs["counts"].items():
            data.append([pri, str(count)])
        add_simple_table(story, styles, data)

    scores = analytics.get("governance_scores", {})
    if scores.get("overall_governance_score") or scores.get("overall_coverage_score"):
        story.append(Paragraph("Governance Score Overview", styles["h2"]))
        data = [["Metric", "Value"]]
        if scores.get("overall_coverage_score"):
            data.append(["Coverage Score", f"{scores['overall_coverage_score']}/100"])
        if scores.get("overall_governance_score"):
            data.append(["Governance Score", f"{scores['overall_governance_score']}/100"])
        if scores.get("overall_maturity_level"):
            data.append(["Maturity Level", scores["overall_maturity_level"]])
        add_simple_table(story, styles, data)

    quality = analytics.get("report_quality", {})
    if quality.get("sections_total", 0) > 0:
        story.append(Paragraph(
            f"Report Quality: {quality.get('sections_present', 0)} of "
            f"{quality.get('sections_total', 0)} sections present "
            f"({quality.get('quality_percentage', 0)}%)",
            styles["body"],
        ))

    story.append(PageBreak())


def export_governance_report_to_pdf_bytes(
    export_data: dict,
    analytics: dict | None = None,
    chart_paths: dict | None = None,
) -> bytes:
    """
    Export the governance report to PDF as bytes.

    Handles missing analytics, missing chart paths, and partial export data gracefully.
    Returns a bytes object containing the PDF.
    """
    if not _REPORTLAB_AVAILABLE:
        return b"%PDF-1.4 (reportlab not available)"

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="AI Governance Policy Review Report",
        author="AI Governance Policy Checker — Build 6",
    )

    styles = build_pdf_styles()
    story: list = []

    org = export_data.get("organisation_name", "Unnamed organisation")
    date = export_data.get("generated_date", "")

    # Cover page
    add_cover_page(
        story,
        styles,
        title="AI Governance Policy Review Report",
        organisation_name=org,
        subtitle="Build 6 · BrightPath ChatGPT Mastery Project",
        generated_date=date,
        prototype_note=(
            "Prototype status: production-style AI governance review prototype — "
            "not a production compliance, legal, safeguarding, HR, data-protection, "
            "or professional advisory system."
        ),
    )

    # Analytics summary tables
    if analytics:
        try:
            _build_analytics_summary_section(story, styles, analytics)
        except Exception:
            pass

    # Charts
    if chart_paths:
        chart_titles = {
            "completion_status": "Export Completion Status",
            "coverage_levels": "Policy Coverage Level Distribution",
            "gap_severities": "Policy Gap Severity Distribution",
            "recommendation_priorities": "Recommendation Priority Distribution",
            "maturity_levels": "Domain Maturity Level Distribution",
            "governance_scores": "Governance Scores by Domain",
        }
        has_charts = any(p and os.path.exists(p) for p in chart_paths.values())
        if has_charts:
            add_section_heading(story, styles, "Governance Analytics Charts")
            for key, path in chart_paths.items():
                if path and os.path.exists(path):
                    add_chart_image(story, path, chart_titles.get(key, ""))
            story.append(PageBreak())

    # Main report content
    markdown = export_data.get("governance_report_markdown") or ""
    if markdown:
        add_section_heading(story, styles, "Full Governance Report")

        table_positions = _extract_markdown_tables(markdown)
        lines = markdown.split("\n")
        i = 0

        while i < len(lines):
            table_match = next(
                ((s, e, d) for s, e, d in table_positions if s <= i <= e), None
            )
            if table_match:
                start, end, data = table_match
                if i == start:
                    add_simple_table(story, styles, data)
                i = end + 1
            else:
                line = lines[i].rstrip()

                if re.match(r"^---+$", line):
                    story.append(HRFlowable(
                        width="100%", thickness=0.5, color=_MID_GREY, spaceAfter=3
                    ))
                elif line.startswith("## "):
                    story.append(Paragraph(line[3:], styles["h2"]))
                elif line.startswith("### "):
                    story.append(Paragraph(line[4:], styles["h3"]))
                elif line.startswith("# "):
                    story.append(Paragraph(line[2:], styles["h1"]))
                elif line.startswith("> "):
                    text = format_pdf_text(line[2:])
                    if text:
                        story.append(Paragraph(f"<i>{text}</i>", styles["note"]))
                elif re.match(r"^\s*[-*]\s+", line):
                    text = format_pdf_text(re.sub(r"^\s*[-*]\s+", "", line))
                    if text:
                        story.append(Paragraph(f"• {text}", styles["bullet"]))
                elif re.match(r"^\d+\.\s+", line):
                    m = re.match(r"^(\d+)\.\s+(.*)", line)
                    if m:
                        text = format_pdf_text(m.group(2))
                        if text:
                            story.append(Paragraph(f"{m.group(1)}. {text}", styles["bullet"]))
                elif not line.strip():
                    story.append(Spacer(1, 0.1 * cm))
                else:
                    clean = format_pdf_text(line)
                    if clean:
                        story.append(Paragraph(clean, styles["body"]))
                i += 1
    else:
        story.append(Paragraph(
            "No governance report content is available. "
            "Generate the governance report from the Governance Report page first.",
            styles["body"],
        ))

    # Responsible-use section
    story.append(PageBreak())
    add_responsible_use_section(story, styles)

    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "Build 6 · AI Governance Policy Checker · BrightPath ChatGPT Mastery Project",
        styles["caption"],
    ))
    story.append(Paragraph(
        "Synthetic scenarios only. Human review required before any real-world use.",
        styles["caption"],
    ))

    doc.build(story)
    return buffer.getvalue()
