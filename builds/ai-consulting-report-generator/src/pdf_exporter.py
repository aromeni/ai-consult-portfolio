"""PDF exporter — Build 5 Phase 8.

Generates a professional PDF consulting report from generated Build 5 outputs.
Uses reportlab only. No external AI calls. No real client data.
"""

import io
import os
import re
from datetime import date

_RESPONSIBLE_USE_TEXT = (
    "This report is generated from synthetic/demo audit data only. "
    "It must not be used with real client records, learner data, safeguarding case details, "
    "staff HR data, personal data, confidential data, or regulated information without "
    "appropriate governance, approvals, and responsible owners.\n\n"
    "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
    "financial, academic-integrity, or professional advice.\n\n"
    "Human review remains required before any real-world use.\n\n"
    "This report is a consulting support artefact, not a final approved organisational policy, "
    "legal opinion, compliance judgement, safeguarding assessment, HR decision, "
    "financial recommendation, or certified professional advice."
)

_PROTOTYPE_LIMITATIONS = [
    "Synthetic/demo audit data only — no real client data is used.",
    "Deterministic and template-based generation — no external AI or LLM API calls.",
    "No real client validation — outputs are based on the BrightPath demo scenario.",
    "No legal, compliance, safeguarding, HR, or financial approval.",
    "Not production-deployed — local prototype only.",
    "No authentication or audit logging.",
    "No persistent storage — outputs are lost on app restart.",
    "Outputs require responsible human review before any real-world use.",
]


# ── Filename ───────────────────────────────────────────────────────────────────


def create_safe_pdf_filename(title: str) -> str:
    """Return a safe dated PDF filename."""
    slug = re.sub(r"[^\w\s-]", "", (title or "report").lower()).strip()
    slug = re.sub(r"[\s_-]+", "-", slug)[:60]
    return f"{date.today()}-{slug}.pdf"


# ── Text helpers ───────────────────────────────────────────────────────────────


def format_pdf_text(text: str) -> str:
    """Strip Markdown syntax and escape XML special characters for reportlab."""
    if not text:
        return ""
    # Remove heading markers
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Remove horizontal rules
    text = re.sub(r"^---+\s*$", "", text, flags=re.MULTILINE)
    # Escape XML special chars
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Convert **bold** to <b>
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # Convert *italic* to <i>
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    return text.strip()


def _plain(text: str) -> str:
    """Strip all Markdown and XML for plain text use."""
    t = re.sub(r"^#{1,6}\s+", "", (text or ""), flags=re.MULTILINE)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"\*(.+?)\*", r"\1", t)
    t = re.sub(r"---+", "", t)
    t = re.sub(r"[<>]", "", t)
    return t.strip()


# ── Style builder ──────────────────────────────────────────────────────────────


def build_pdf_styles() -> dict:
    """Return a dict of named reportlab ParagraphStyle objects."""
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.lib.enums import TA_LEFT, TA_CENTER

    base = getSampleStyleSheet()
    navy = colors.HexColor("#1a2744")
    dark = colors.HexColor("#1e293b")
    muted = colors.HexColor("#64748b")
    white = colors.HexColor("#ffffff")

    styles = {
        "CoverTitle": ParagraphStyle(
            "CoverTitle",
            fontName="Helvetica-Bold",
            fontSize=28,
            textColor=white,
            spaceAfter=10,
            alignment=TA_LEFT,
            leading=34,
        ),
        "CoverSubtitle": ParagraphStyle(
            "CoverSubtitle",
            fontName="Helvetica",
            fontSize=14,
            textColor=colors.HexColor("#cbd5e1"),
            spaceAfter=6,
            alignment=TA_LEFT,
            leading=18,
        ),
        "CoverMeta": ParagraphStyle(
            "CoverMeta",
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#94a3b8"),
            spaceAfter=4,
            alignment=TA_LEFT,
        ),
        "CoverProto": ParagraphStyle(
            "CoverProto",
            fontName="Helvetica-Oblique",
            fontSize=9,
            textColor=colors.HexColor("#94a3b8"),
            spaceAfter=4,
            alignment=TA_LEFT,
        ),
        "H1": ParagraphStyle(
            "H1",
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=navy,
            spaceBefore=18,
            spaceAfter=8,
            leading=22,
        ),
        "H2": ParagraphStyle(
            "H2",
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=navy,
            spaceBefore=14,
            spaceAfter=6,
            leading=18,
        ),
        "H3": ParagraphStyle(
            "H3",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=dark,
            spaceBefore=10,
            spaceAfter=4,
            leading=14,
        ),
        "Body": ParagraphStyle(
            "Body",
            fontName="Helvetica",
            fontSize=10,
            textColor=dark,
            spaceAfter=6,
            leading=14,
        ),
        "Bullet": ParagraphStyle(
            "Bullet",
            fontName="Helvetica",
            fontSize=10,
            textColor=dark,
            spaceAfter=3,
            leading=14,
            leftIndent=16,
            firstLineIndent=0,
        ),
        "Caption": ParagraphStyle(
            "Caption",
            fontName="Helvetica-Oblique",
            fontSize=9,
            textColor=muted,
            spaceAfter=4,
            alignment=TA_CENTER,
        ),
        "Warning": ParagraphStyle(
            "Warning",
            fontName="Helvetica",
            fontSize=9,
            textColor=colors.HexColor("#92400e"),
            spaceAfter=6,
            leading=13,
            backColor=colors.HexColor("#fef3c7"),
            leftIndent=8,
            rightIndent=8,
            borderPadding=6,
        ),
    }
    return styles


# ── Story builders ─────────────────────────────────────────────────────────────


def add_cover_page(
    story: list,
    styles: dict,
    title: str,
    organisation_name: str = "",
    subtitle: str = "",
    generated_date: str = "",
    prototype_note: str = "",
) -> None:
    """Add a styled cover page to the story."""
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import Spacer, Paragraph, Table, TableStyle

    navy = colors.HexColor("#1a2744")
    # Navy header block via a single-cell table
    header_data = [[Paragraph(title or "AI Consulting Report", styles["CoverTitle"])]]
    header_table = Table(header_data, colWidths=[160 * mm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), navy),
        ("TOPPADDING", (0, 0), (-1, -1), 24),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 24),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 16))

    if organisation_name:
        story.append(Paragraph(f"Prepared for: <b>{organisation_name}</b>", styles["H2"]))
    if subtitle:
        story.append(Paragraph(subtitle, styles["Body"]))
    story.append(Spacer(1, 10))
    if generated_date:
        story.append(Paragraph(f"Generated: {generated_date}", styles["CoverMeta"]))
    story.append(Spacer(1, 6))
    proto = prototype_note or (
        "Production-style AI consulting report prototype. "
        "Not a production consulting, legal, safeguarding, HR, compliance, "
        "financial, or professional advisory system."
    )
    story.append(Paragraph(proto, styles["CoverProto"]))


def add_section_heading(story: list, styles: dict, heading: str) -> None:
    """Add a section heading paragraph."""
    from reportlab.platypus import Paragraph
    story.append(Paragraph(_plain(heading), styles["H1"]))


def add_paragraphs_from_markdown(
    story: list,
    styles: dict,
    markdown_text: str,
) -> None:
    """Convert Markdown text to reportlab story elements."""
    from reportlab.platypus import Paragraph, Spacer

    if not markdown_text:
        return

    table_rows = []

    def _flush_table():
        if table_rows:
            _add_table_from_rows(story, styles, table_rows)
            table_rows.clear()

    for line in markdown_text.splitlines():
        stripped = line.strip()

        if not stripped:
            _flush_table()
            story.append(Spacer(1, 4))
            continue

        # Heading levels
        if stripped.startswith("### "):
            _flush_table()
            story.append(Paragraph(format_pdf_text(stripped[4:]), styles["H3"]))
        elif stripped.startswith("## "):
            _flush_table()
            story.append(Paragraph(format_pdf_text(stripped[3:]), styles["H2"]))
        elif stripped.startswith("# "):
            _flush_table()
            story.append(Paragraph(format_pdf_text(stripped[2:]), styles["H1"]))
        # Bullet
        elif stripped.startswith("- ") or stripped.startswith("* "):
            _flush_table()
            story.append(Paragraph("• " + format_pdf_text(stripped[2:]), styles["Bullet"]))
        # Numbered list
        elif re.match(r"^\d+\.\s+", stripped):
            _flush_table()
            story.append(Paragraph(format_pdf_text(stripped), styles["Bullet"]))
        # Markdown table row
        elif stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if not all(re.match(r"^-+$", c.replace(":", "")) for c in cells):
                table_rows.append(cells)
        # Horizontal rule
        elif stripped.startswith("---"):
            _flush_table()
            story.append(Spacer(1, 8))
        # Plain paragraph
        else:
            _flush_table()
            story.append(Paragraph(format_pdf_text(stripped), styles["Body"]))

    _flush_table()


def _add_table_from_rows(story: list, styles: dict, rows: list) -> None:
    """Add a simple styled table from a list of row-lists."""
    if not rows:
        return
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import Table, TableStyle, Spacer

    navy = colors.HexColor("#1a2744")
    light = colors.HexColor("#f8fafc")
    border = colors.HexColor("#e2e8f0")

    col_count = max(len(r) for r in rows)
    col_width = 150 * mm / col_count

    table = Table(rows, colWidths=[col_width] * col_count)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), navy),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BACKGROUND", (0, 1), (-1, -1), light),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [light, colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, border),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(table)
    story.append(Spacer(1, 8))


def add_bullet_list(story: list, styles: dict, items: list) -> None:
    """Add a bullet list to the story."""
    from reportlab.platypus import Paragraph
    for item in (items or []):
        story.append(Paragraph("• " + format_pdf_text(str(item)), styles["Bullet"]))


def add_simple_table(
    story: list,
    styles: dict,
    data: list,
) -> None:
    """Add a simple table from a list of row-lists."""
    _add_table_from_rows(story, styles, data)


def add_chart_image(
    story: list,
    image_path: str,
    title: str = "",
) -> None:
    """Embed a chart image in the story if the file exists."""
    if not image_path or not os.path.exists(image_path):
        return
    try:
        from reportlab.lib.units import mm
        from reportlab.platypus import Image as RLImage, Spacer, Paragraph

        # We need styles — build them on the fly for caption
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        caption_style = ParagraphStyle(
            "CaptionInline",
            fontName="Helvetica-Oblique",
            fontSize=9,
            textColor=colors.HexColor("#64748b"),
            alignment=TA_CENTER,
            spaceAfter=4,
        )
        if title:
            story.append(Paragraph(title, caption_style))
        img = RLImage(image_path, width=150 * mm, height=80 * mm, kind="proportional")
        story.append(img)
        story.append(Spacer(1, 12))
    except Exception:
        pass


def add_responsible_use_section(story: list, styles: dict) -> None:
    """Add the responsible-use boundaries section."""
    from reportlab.platypus import Paragraph, Spacer
    story.append(Paragraph("Responsible-Use Boundaries", styles["H1"]))
    for para in _RESPONSIBLE_USE_TEXT.split("\n\n"):
        if para.strip():
            story.append(Paragraph(format_pdf_text(para.strip()), styles["Body"]))
    story.append(Spacer(1, 8))


# ── Full PDF export ────────────────────────────────────────────────────────────


def export_client_report_to_pdf_bytes(
    export_data: dict,
    analytics: dict | None = None,
    chart_paths: dict | None = None,
) -> bytes:
    """Generate the full client report PDF. Returns bytes or b'' on failure."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            SimpleDocTemplate, Spacer, PageBreak, Paragraph,
        )

        ed = export_data or {}
        an = analytics or {}
        cp = chart_paths or {}

        org = ed.get("organisation_name") or "Unnamed organisation"
        generated = ed.get("generated_date") or str(date.today())
        cr_md = ed.get("client_report_markdown") or ""
        proto_note = ed.get("prototype_note") or (
            "Production-style prototype. Not a production consulting, legal, "
            "safeguarding, HR, compliance, or professional advisory system."
        )

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=22 * mm,
            rightMargin=22 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
            title="AI Readiness and Responsible AI Adoption Report",
            author="Build 5 — AI Consulting Report Generator",
        )
        styles = build_pdf_styles()
        story = []

        # ── Cover page ─────────────────────────────────────────────────────────
        add_cover_page(
            story, styles,
            title="AI Readiness and\nResponsible AI Adoption Report",
            organisation_name=org,
            generated_date=generated,
            prototype_note=proto_note,
        )
        story.append(PageBreak())

        # ── Analytics summary ──────────────────────────────────────────────────
        if an:
            story.append(Paragraph("Report Analytics Summary", styles["H1"]))
            story.append(Spacer(1, 6))

            quality = an.get("report_quality_summary") or {}
            if quality:
                story.append(Paragraph("Report Quality Checklist", styles["H2"]))
                for key, val in quality.items():
                    label = key.replace("_", " ").replace(" included", "").title()
                    icon = "✓" if val else "✗"
                    story.append(
                        Paragraph(f"{icon}  {label}", styles["Bullet"])
                    )
                story.append(Spacer(1, 8))

            completion = an.get("completion_status") or {}
            if completion:
                story.append(Paragraph("Output Completion Status", styles["H2"]))
                for output, done in completion.items():
                    icon = "✓" if done else "○"
                    story.append(Paragraph(f"{icon}  {output}", styles["Bullet"]))
                story.append(Spacer(1, 8))

            # Completion chart
            add_chart_image(
                story, cp.get("completion_status", ""), "Output Completion"
            )

            story.append(PageBreak())

        # ── Readiness score chart ──────────────────────────────────────────────
        readiness_chart = cp.get("readiness_scores", "")
        if readiness_chart:
            story.append(Paragraph("AI Readiness Scores", styles["H1"]))
            add_chart_image(story, readiness_chart, "Readiness Score by Category")
            story.append(PageBreak())

        # ── Risk chart ─────────────────────────────────────────────────────────
        risk_chart = cp.get("risk_levels", "")
        if risk_chart:
            story.append(Paragraph("Risk Distribution", styles["H1"]))
            add_chart_image(story, risk_chart, "AI Risk Distribution by Level")
            story.append(PageBreak())

        # ── Opportunity chart ──────────────────────────────────────────────────
        opp_chart = cp.get("opportunity_priorities", "")
        if opp_chart:
            story.append(Paragraph("Opportunity Priorities", styles["H1"]))
            add_chart_image(story, opp_chart, "AI Opportunity Priority Distribution")
            story.append(PageBreak())

        # ── Roadmap chart ──────────────────────────────────────────────────────
        roadmap_chart = cp.get("roadmap_actions", "")
        if roadmap_chart:
            story.append(Paragraph("Roadmap Actions", styles["H1"]))
            add_chart_image(story, roadmap_chart, "Roadmap Actions by Phase")
            story.append(PageBreak())

        # ── Full client report content ─────────────────────────────────────────
        if cr_md:
            story.append(Paragraph("Full Client Report", styles["H1"]))
            story.append(Spacer(1, 8))
            add_paragraphs_from_markdown(story, styles, cr_md)
            story.append(PageBreak())
        else:
            story.append(Paragraph("Full Client Report", styles["H1"]))
            story.append(Paragraph(
                "The client report has not been generated yet. "
                "Go to the Client Report page and generate the report first.",
                styles["Body"],
            ))
            story.append(PageBreak())

        # ── Responsible use ────────────────────────────────────────────────────
        add_responsible_use_section(story, styles)
        story.append(Spacer(1, 8))

        # ── Prototype limitations ──────────────────────────────────────────────
        story.append(Paragraph("Prototype Limitations", styles["H1"]))
        add_bullet_list(story, styles, _PROTOTYPE_LIMITATIONS)

        doc.build(story)
        return buffer.getvalue()

    except Exception:
        return b""


# ── Backward-compatible stub ───────────────────────────────────────────────────


def create_pdf_placeholder(title: str, body_text: str) -> bytes:
    """Return a minimal PDF stub. Retained for backward compatibility."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=25 * mm,
            rightMargin=25 * mm,
            topMargin=25 * mm,
            bottomMargin=25 * mm,
        )
        styles = getSampleStyleSheet()
        story = [
            Paragraph(title, styles["Title"]),
            Spacer(1, 12),
            Paragraph(f"Generated: {date.today()}", styles["Normal"]),
            Spacer(1, 8),
            Paragraph(
                "Synthetic scenario prototype. Human review required before use.",
                styles["Italic"],
            ),
            Spacer(1, 24),
        ]
        for line in body_text.split("\n"):
            stripped = line.strip()
            if stripped:
                story.append(Paragraph(stripped, styles["Normal"]))
                story.append(Spacer(1, 6))
        doc.build(story)
        return buffer.getvalue()
    except Exception:
        return b""
