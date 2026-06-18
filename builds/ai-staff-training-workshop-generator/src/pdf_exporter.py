"""Reusable professional PDF export for the AI Staff Training and Workshop Generator.

Converts generated Markdown reports and structured report dicts into clean,
client-presentable PDF documents using reportlab platypus.

All content is deterministic and based on synthetic scenario data only.
No external API calls. No real data. Human review required before use.
"""

import io
import re
from datetime import date

PROTOTYPE_FOOTER = "Synthetic scenario prototype. Human review required."

REPORT_TITLES = {
    "needs_assessment": "Training Needs Assessment",
    "workshop_plan": "Workshop Plan",
    "activities": "Training Activity Pack",
    "facilitator_guide": "Facilitator Guide",
    "staff_handout": "Staff Handout",
    "knowledge_check": "Knowledge Check",
    "training_pack": "Responsible AI Staff Training Pack",
}

RESPONSIBLE_USE_ITEMS = [
    "Use synthetic or approved scenarios only — no real learner, safeguarding, "
    "HR, personal, or regulated data.",
    "No external AI API calls — all generation runs locally and deterministically.",
    "Human review is required before using any output in a real training session.",
    "This report does not constitute legal, safeguarding, HR, compliance, "
    "medical, or professional advice.",
    "Training materials are support materials, not official organisational policy.",
    "Production use requires governance, DPIA, security, privacy, and "
    "responsible-owner approval.",
]


# ── Filename and text helpers ───────────────────────────────────────────────────

def create_safe_filename(title: str, extension: str = "pdf") -> str:
    """Return a lowercase kebab-case filename safe for download."""
    if not isinstance(title, str):
        title = "report"
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower().strip()).strip("-")
    slug = slug[:60] or "report"
    ext = str(extension).lstrip(".") or "pdf"
    return f"{slug}.{ext}"


def normalise_report_text(text: str) -> str:
    """Strip Markdown markers and normalise whitespace; always returns a string."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def _escape_xml(text: str) -> str:
    """Escape characters that break reportlab Paragraph markup."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _inline_markup(text: str) -> str:
    """Convert inline Markdown (**bold**, *italic*, `code`) to reportlab markup."""
    text = _escape_xml(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`", r"<font face='Courier' size='9'>\1</font>", text)
    return text


# ── Style sheet ─────────────────────────────────────────────────────────────────

def build_pdf_styles() -> dict:
    """Return the named ParagraphStyle dict used by all report PDFs."""
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    base = getSampleStyleSheet()

    navy = colors.HexColor("#16243d")
    slate = colors.HexColor("#334155")
    grey = colors.HexColor("#64748b")
    amber = colors.HexColor("#b45309")

    return {
        "title": ParagraphStyle(
            "ReportTitle", parent=base["Title"], fontSize=24, leading=29,
            textColor=navy, spaceAfter=10, alignment=0,
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle", parent=base["Normal"], fontSize=12, leading=16,
            textColor=slate, spaceAfter=6,
        ),
        "h1": ParagraphStyle(
            "ReportH1", parent=base["Heading1"], fontSize=17, leading=21,
            textColor=navy, spaceBefore=16, spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "ReportH2", parent=base["Heading2"], fontSize=13.5, leading=17,
            textColor=slate, spaceBefore=12, spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "ReportH3", parent=base["Heading3"], fontSize=11.5, leading=15,
            textColor=slate, spaceBefore=10, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "ReportBody", parent=base["Normal"], fontSize=10, leading=14.5,
            textColor=colors.HexColor("#1f2937"), spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "ReportBullet", parent=base["Normal"], fontSize=10, leading=14,
            textColor=colors.HexColor("#1f2937"), leftIndent=14, spaceAfter=3,
        ),
        "small": ParagraphStyle(
            "ReportSmall", parent=base["Normal"], fontSize=8.5, leading=11.5,
            textColor=grey, spaceAfter=4,
        ),
        "notice": ParagraphStyle(
            "ReportNotice", parent=base["Normal"], fontSize=9.5, leading=13,
            textColor=amber, spaceBefore=4, spaceAfter=8, leftIndent=8,
        ),
        "cover_meta": ParagraphStyle(
            "CoverMeta", parent=base["Normal"], fontSize=11, leading=16,
            textColor=slate, spaceAfter=4,
        ),
        "table_header": ParagraphStyle(
            "TableHeader", parent=base["Normal"], fontSize=9, leading=12,
            textColor=colors.white, fontName="Helvetica-Bold",
        ),
        "table_body": ParagraphStyle(
            "TableBody", parent=base["Normal"], fontSize=9, leading=12,
            textColor=colors.HexColor("#1f2937"),
        ),
    }


# ── Story builders ──────────────────────────────────────────────────────────────

def add_pdf_cover_page(
    story,
    styles,
    report_title: str,
    organisation_name: str = "",
    subtitle: str = "",
    generated_date: str = "",
    prototype_note: str = "",
) -> None:
    """Append a clean cover page (title, organisation, date, prototype note)."""
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import HRFlowable, PageBreak, Paragraph, Spacer

    story.append(Spacer(1, 4.5 * cm))
    story.append(Paragraph(_escape_xml(report_title), styles["title"]))
    story.append(HRFlowable(width="100%", thickness=2.5, color=colors.HexColor("#2563eb")))
    story.append(Spacer(1, 0.6 * cm))
    if organisation_name:
        story.append(Paragraph(f"<b>{_escape_xml(organisation_name)}</b>", styles["subtitle"]))
    if subtitle:
        story.append(Paragraph(_escape_xml(subtitle), styles["cover_meta"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(
        f"Generated: {_escape_xml(generated_date or str(date.today()))}",
        styles["cover_meta"],
    ))
    story.append(Paragraph(
        "Status: Production-style prototype — draft for human review",
        styles["cover_meta"],
    ))
    story.append(Spacer(1, 1.4 * cm))
    story.append(Paragraph(
        _escape_xml(
            prototype_note
            or "All scenarios are synthetic. This document is a draft training "
               "deliverable and requires qualified human review before use in a "
               "real training session. It is not legal, safeguarding, HR, "
               "compliance, medical, or professional advice."
        ),
        styles["notice"],
    ))
    story.append(PageBreak())


def add_pdf_section(story, styles, heading: str, content) -> None:
    """Append a section heading and its content (string, list, or dict)."""
    from reportlab.lib import colors
    from reportlab.platypus import HRFlowable, Paragraph

    story.append(Paragraph(_inline_markup(heading), styles["h2"]))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#cbd5e1")))
    if content is None:
        return
    if isinstance(content, dict):
        for key, value in content.items():
            label = str(key).replace("_", " ").title()
            story.append(Paragraph(
                f"<b>{_escape_xml(label)}:</b> {_inline_markup(str(value))}",
                styles["body"],
            ))
    elif isinstance(content, (list, tuple)):
        add_pdf_bullet_list(story, styles, list(content))
    else:
        for line in str(content).split("\n"):
            line = line.strip()
            if line:
                story.append(Paragraph(_inline_markup(line), styles["body"]))


def add_pdf_bullet_list(story, styles, items: list) -> None:
    """Append a bullet list of items."""
    from reportlab.platypus import Paragraph

    for item in items or []:
        story.append(Paragraph(f"•  {_inline_markup(str(item))}", styles["bullet"]))


def add_pdf_table(story, styles, data: list, column_widths: list | None = None) -> None:
    """Append a styled table. First row is treated as the header row."""
    from reportlab.lib import colors
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

    if not data:
        return

    wrapped = []
    for r, row in enumerate(data):
        style = styles["table_header"] if r == 0 else styles["table_body"]
        wrapped.append([Paragraph(_inline_markup(str(cell)), style) for cell in row])

    table = Table(wrapped, colWidths=column_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16243d")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(Spacer(1, 4))
    story.append(table)
    story.append(Spacer(1, 6))


def add_responsible_use_footer_section(story, styles) -> None:
    """Append the standard responsible-use boundaries and limitations section."""
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import HRFlowable, Paragraph, Spacer

    story.append(Spacer(1, 0.6 * cm))
    story.append(Paragraph("Responsible-Use Boundaries", styles["h2"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#b91c1c")))
    add_pdf_bullet_list(story, styles, RESPONSIBLE_USE_ITEMS)
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(PROTOTYPE_FOOTER, styles["small"]))


# ── Page furniture ──────────────────────────────────────────────────────────────

def _draw_page_footer(canvas, doc) -> None:
    """Draw the prototype footer and page number on every page."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm

    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#94a3b8"))
    canvas.drawString(2 * cm, 1.2 * cm, PROTOTYPE_FOOTER)
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def _is_table_separator_row(cells: list) -> bool:
    """True for Markdown table separator rows like | --- | :---: |."""
    return all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in cells if c.strip()) if cells else False


# ── Markdown report export ──────────────────────────────────────────────────────

def export_markdown_report_to_pdf_bytes(
    markdown_text: str,
    report_title: str,
    organisation_name: str = "",
    subtitle: str = "",
    include_cover_page: bool = True,
) -> bytes:
    """Convert a generated Markdown report into professional PDF bytes.

    Headings, bullets, numbered lists, tables, blockquotes, and dividers are
    converted into styled report elements — not raw Markdown text.
    """
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

    if not isinstance(markdown_text, str):
        markdown_text = ""

    styles = build_pdf_styles()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2.2 * cm,
        title=str(report_title),
    )

    story = []
    if include_cover_page:
        add_pdf_cover_page(
            story, styles,
            report_title=str(report_title),
            organisation_name=organisation_name,
            subtitle=subtitle,
        )
    else:
        story.append(Paragraph(_escape_xml(str(report_title)), styles["h1"]))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb")))

    table_rows: list = []

    def flush_table():
        if table_rows:
            add_pdf_table(story, styles, list(table_rows))
            table_rows.clear()

    for raw_line in markdown_text.split("\n"):
        line = raw_line.strip()

        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not _is_table_separator_row(cells):
                table_rows.append(cells)
            continue
        flush_table()

        if not line:
            story.append(Spacer(1, 3))
        elif re.fullmatch(r"[-*_]{3,}", line):
            story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#cbd5e1")))
        elif line.startswith("# "):
            story.append(Paragraph(_inline_markup(line[2:]), styles["h1"]))
        elif line.startswith("## "):
            story.append(Paragraph(_inline_markup(line[3:]), styles["h2"]))
        elif re.match(r"^#{3,6}\s+", line):
            story.append(Paragraph(_inline_markup(re.sub(r"^#{3,6}\s+", "", line)), styles["h3"]))
        elif line.startswith("> "):
            story.append(Paragraph(_inline_markup(line[2:]), styles["notice"]))
        elif re.match(r"^[-*+]\s+", line):
            bullet_text = re.sub(r"^[-*+]\s+", "", line)
            story.append(Paragraph(f"•  {_inline_markup(bullet_text)}", styles["bullet"]))
        elif re.match(r"^\d+[.)]\s+", line):
            story.append(Paragraph(_inline_markup(line), styles["bullet"]))
        else:
            story.append(Paragraph(_inline_markup(line), styles["body"]))

    flush_table()
    add_responsible_use_footer_section(story, styles)

    doc.build(story, onFirstPage=_draw_page_footer, onLaterPages=_draw_page_footer)
    buf.seek(0)
    return buf.read()


# ── Structured report export ────────────────────────────────────────────────────

def export_structured_report_to_pdf_bytes(
    report_data: dict,
    report_type: str,
    markdown_text: str | None = None,
) -> bytes:
    """Export a structured report dict to PDF bytes.

    Prefers the pre-rendered Markdown when supplied (richest formatting);
    otherwise renders the dict's top-level fields as titled sections so
    minimal or partial report data never crashes generation.
    """
    if not isinstance(report_data, dict):
        report_data = {}

    report_title = REPORT_TITLES.get(report_type, str(report_type).replace("_", " ").title() or "Report")
    scenario = report_data.get("scenario") or {}
    organisation_name = (
        report_data.get("organisation_name")
        or scenario.get("organisation_name")
        or ""
    )

    if markdown_text:
        return export_markdown_report_to_pdf_bytes(
            markdown_text,
            report_title=report_title,
            organisation_name=organisation_name,
            subtitle="Responsible AI staff training — synthetic scenario prototype",
        )

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate

    styles = build_pdf_styles()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2.2 * cm,
        title=report_title,
    )

    story: list = []
    add_pdf_cover_page(
        story, styles,
        report_title=report_title,
        organisation_name=organisation_name,
        subtitle="Responsible AI staff training — synthetic scenario prototype",
    )

    for key, value in report_data.items():
        if value is None or value == "" or value == [] or value == {}:
            continue
        heading = str(key).replace("_", " ").title()
        if isinstance(value, (str, int, float)):
            add_pdf_section(story, styles, heading, str(value))
        elif isinstance(value, list) and all(isinstance(i, (str, int, float)) for i in value):
            add_pdf_section(story, styles, heading, value)
        elif isinstance(value, dict):
            flat = {k: v for k, v in value.items() if isinstance(v, (str, int, float))}
            if flat:
                add_pdf_section(story, styles, heading, flat)
        # Nested lists of dicts are summarised by count to stay readable
        elif isinstance(value, list):
            add_pdf_section(story, styles, heading, f"{len(value)} item(s) — see Markdown export for full detail.")

    if not report_data:
        add_pdf_section(story, styles, "Report", "No report data available.")

    add_responsible_use_footer_section(story, styles)
    doc.build(story, onFirstPage=_draw_page_footer, onLaterPages=_draw_page_footer)
    buf.seek(0)
    return buf.read()
