"""
Report generation for the BrightPath AI Readiness + Workflow Audit Tool.

Phase 1 — plain-text report (generate_text_report, kept for backwards compatibility)
Phase 6 — Markdown mini report (generate_markdown_report and helpers)
Phase 7 (Polish 5) — PDF mini report (generate_pdf_report_bytes)
"""

import re
from io import BytesIO
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
    KeepTogether,
)


def generate_text_report(profile: dict, responses: dict, band: dict,
                         workflow_summary: dict, candidates: list) -> str:
    today = date.today().strftime("%d %B %Y")
    lines = []

    lines.append("=" * 60)
    lines.append("BRIGHTPATH AI READINESS + WORKFLOW AUDIT REPORT")
    lines.append(f"Generated: {today}")
    lines.append("=" * 60)
    lines.append("")

    lines.append("ORGANISATION PROFILE")
    lines.append("-" * 40)
    lines.append(f"Name:         {profile.get('org_name', 'Not provided')}")
    lines.append(f"Type:         {profile.get('org_type', 'Not provided')}")
    lines.append(f"Sector:       {profile.get('sector', 'Not provided')}")
    lines.append(f"Staff count:  {profile.get('staff_count', 'Not provided')}")
    tools = profile.get("current_ai_tools", [])
    lines.append(f"Current tools: {', '.join(tools) if tools else 'None reported'}")
    lines.append(f"AI policy:    {'Yes' if profile.get('has_ai_policy') else 'No'}")
    lines.append(f"Approved tools defined: {'Yes' if profile.get('has_approved_tools') else 'No'}")
    lines.append("")

    lines.append("AI READINESS SCORE")
    lines.append("-" * 40)
    lines.append(f"Total score:  {band['score']} / {band['max']}")
    lines.append(f"Band:         {band['label']}")
    lines.append("")
    lines.append("Dimension scores:")
    dimension_labels = {
        "data_awareness": "Data Awareness",
        "prompt_skill": "Prompt Skill",
        "output_review": "Output Review",
        "governance": "Governance",
        "manager_oversight": "Manager Oversight",
    }
    for key, label in dimension_labels.items():
        score = responses.get(key, "-")
        lines.append(f"  {label:<22} {score} / 5")
    lines.append("")

    lines.append("RECOMMENDATION")
    lines.append("-" * 40)
    lines.append(band["recommendation"])
    lines.append("")

    lines.append("WORKFLOW AUDIT SUMMARY")
    lines.append("-" * 40)
    lines.append(f"AI-suitable workflows:   {workflow_summary['suitable_count']}")
    lines.append(f"Borderline workflows:    {workflow_summary['borderline_count']}")
    lines.append(f"Unsuitable workflows:    {workflow_summary['unsuitable_count']}")
    lines.append(f"High / critical risk:    {workflow_summary['high_risk_count']}")
    lines.append("")

    if candidates:
        lines.append("PILOT WORKFLOW CANDIDATES")
        lines.append("-" * 40)
        for i, w in enumerate(candidates, 1):
            lines.append(f"{i}. {w['workflow']} ({w['role']}) — Risk: {w['risk_level']}")
            if w.get("notes"):
                lines.append(f"   Note: {w['notes']}")
        lines.append("")

    if workflow_summary["high_risk"]:
        lines.append("HIGH / CRITICAL RISK WORKFLOWS — DO NOT PILOT")
        lines.append("-" * 40)
        for w in workflow_summary["high_risk"]:
            lines.append(f"  {w['workflow']} — {w['risk_level']}")
            if w.get("notes"):
                lines.append(f"  Note: {w['notes']}")
        lines.append("")

    lines.append("RESPONSIBLE USE NOTICE")
    lines.append("-" * 40)
    lines.append(
        "This report is for indicative assessment and pilot planning purposes only.\n"
        "It does not constitute legal, compliance, safeguarding, HR, or financial advice.\n"
        "All sample data used in this prototype is synthetic and anonymised.\n"
        "No real learner, client, staff, or confidential data should be entered.\n"
        "Organisations should seek qualified advice for governance and compliance decisions."
    )
    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)


# ── Phase 6: Markdown mini report ─────────────────────────────────────────────

def format_safeguards(safeguards: list) -> str:
    return "\n".join(f"- {s}" for s in safeguards)


def format_next_actions(next_actions: list) -> str:
    return "\n".join(f"{i}. {action}" for i, action in enumerate(next_actions, 1))


def create_report_filename(organisation_name: str) -> str:
    if not organisation_name or not organisation_name.strip():
        return "ai-readiness-mini-report.md"
    name = organisation_name.lower().strip()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    name = name.strip("-")
    return f"{name}-ai-readiness-mini-report.md"


def _cell(value) -> str:
    """Escape pipe characters so long values do not break Markdown table cells."""
    return str(value).replace("|", "&#124;") if value else "—"


def generate_markdown_report(report_data: dict) -> str:
    org_name = report_data.get("org_name") or "Not provided"
    generated_date = report_data.get("generated_date") or date.today().strftime("%d %B %Y")

    lines = []

    lines += [
        "# AI Readiness and Workflow Audit Mini Report",
        "",
        f"**Organisation:** {org_name}  ",
        f"**Generated:** {generated_date}",
        "",
        "---",
        "",
    ]

    # 1. Organisation Profile
    lines += [
        "## 1. Organisation Profile",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Organisation name | {_cell(report_data.get('org_name'))} |",
        f"| Organisation type | {_cell(report_data.get('org_type'))} |",
        f"| Number of staff | {_cell(report_data.get('staff_count'))} |",
        f"| Current AI use | {_cell(report_data.get('ai_use_summary'))} |",
        f"| Main concerns | {_cell(report_data.get('main_concerns'))} |",
        "",
        "---",
        "",
    ]

    # 2. AI Readiness Summary
    readiness_score = report_data.get("readiness_score", "—")
    readiness_cat = report_data.get("readiness_category") or "—"
    lines += [
        "## 2. AI Readiness Summary",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Readiness score | {readiness_score} / 100 |",
        f"| Category | {_cell(readiness_cat)} |",
        "",
        "---",
        "",
    ]

    # 3. Workflow Audit Summary
    workflow_score = report_data.get("workflow_score", "—")
    workflow_cat = report_data.get("workflow_category") or "—"
    lines += [
        "## 3. Workflow Audit Summary",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Workflow name | {_cell(report_data.get('workflow_name'))} |",
        f"| Owner / team | {_cell(report_data.get('workflow_owner'))} |",
        f"| Proposed AI support | {_cell(report_data.get('ai_support_idea'))} |",
        f"| Suitability score | {workflow_score} / 50 |",
        f"| Suitability category | {_cell(workflow_cat)} |",
        "",
        "---",
        "",
    ]

    # 4. Risk Assessment Summary
    has_critical = report_data.get("has_critical", False)
    has_high = report_data.get("has_high", False)
    lines += [
        "## 4. Risk Assessment Summary",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Highest risk level | {_cell(report_data.get('highest_risk'))} |",
        f"| Critical risk present | {'Yes' if has_critical else 'No'} |",
        f"| High risk present | {'Yes' if has_high else 'No'} |",
        f"| Key risk notes | {_cell(report_data.get('key_risk_notes'))} |",
        "",
        "---",
        "",
    ]

    # 5. Pilot Recommendation
    recommendation = report_data.get("recommendation") or "—"
    explanation = report_data.get("recommendation_explanation") or ""
    lines += ["## 5. Pilot Recommendation", ""]
    lines.append(f"**Recommendation:** {recommendation}")
    lines.append("")
    if explanation:
        lines.append(explanation)
        lines.append("")
    lines += ["---", ""]

    # 6. Recommended Safeguards
    safeguards_text = (report_data.get("safeguards_text") or "").strip()
    lines += ["## 6. Recommended Safeguards", ""]
    lines.append(safeguards_text if safeguards_text else "*No safeguards recorded.*")
    lines += ["", "---", ""]

    # 7. Suggested Next Actions
    next_actions_text = (report_data.get("next_actions_text") or "").strip()
    lines += ["## 7. Suggested Next Actions", ""]
    lines.append(next_actions_text if next_actions_text else "*No next actions recorded.*")
    lines += ["", "---", ""]

    # 8. Responsible Use and Limitations
    lines += [
        "## 8. Responsible Use and Limitations",
        "",
        "This report is generated by a prototype tool and is intended to support discussion, "
        "planning, and early-stage AI adoption decisions. It is not legal, safeguarding, HR, "
        "compliance, medical, financial, or academic-integrity advice. Organisations should "
        "review all recommendations with appropriate responsible owners before acting.",
        "",
        "The tool should not be used with identifiable learner data, safeguarding case "
        "information, confidential client records, staff HR/disciplinary information, "
        "regulated information, or sensitive personal data unless appropriate governance, "
        "approvals, and controls are in place.",
        "",
        "AI recommendations should be treated as draft support. Human review, data protection "
        "checks, risk assessment, and organisational judgement remain required.",
        "",
        "---",
        "",
    ]

    # 9. Consultant Notes
    consultant_notes = (report_data.get("consultant_notes") or "").strip()
    lines += ["## 9. Consultant Notes", ""]
    lines.append(consultant_notes if consultant_notes else "*No consultant notes recorded.*")
    lines += [
        "",
        "---",
        "",
        "*Generated by BrightPath AI Readiness + Workflow Audit Tool (prototype)*  ",
        "*All sample data is synthetic. This report provides indicative assessment guidance only.*",
    ]

    return "\n".join(lines)


# ── Polish Step 5: PDF mini report ────────────────────────────────────────────

def create_pdf_report_filename(organisation_name: str) -> str:
    if not organisation_name or not organisation_name.strip():
        return "ai-readiness-mini-report.pdf"
    name = organisation_name.lower().strip()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    name = name.strip("-")
    return f"{name}-ai-readiness-mini-report.pdf"


def generate_pdf_report_bytes(report_data: dict) -> bytes:
    """Generate a styled PDF mini report and return the content as bytes."""

    buffer = BytesIO()

    PAGE_W, PAGE_H = A4
    L_MARGIN = R_MARGIN = 2.5 * cm
    T_MARGIN = 2.5 * cm
    B_MARGIN = 3.0 * cm          # extra room for per-page footer
    USABLE_W = PAGE_W - L_MARGIN - R_MARGIN   # ~16.2 cm

    # Colour palette
    C_DARK_BLUE  = HexColor("#1a3a5c")
    C_LIGHT_BLUE = HexColor("#e8f0f7")  # section heading background
    C_HDR_BG     = HexColor("#d4e4f4")  # KV table label-column background
    C_ROW_ALT    = HexColor("#f5f8fc")  # alternating value-column rows
    C_BORDER     = HexColor("#c0d4e8")  # table borders
    C_BODY_TEXT  = HexColor("#333333")
    C_MUTED      = HexColor("#999999")

    styles = getSampleStyleSheet()

    _title = ParagraphStyle(
        "BPTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        spaceAfter=2,
        textColor=HexColor("#ffffff"),
        alignment=TA_LEFT,
    )
    _subtitle = ParagraphStyle(
        "BPSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        textColor=HexColor("#aaccee"),
        spaceAfter=0,
    )
    _heading = ParagraphStyle(
        "BPHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        spaceBefore=0,
        spaceAfter=0,
        textColor=C_DARK_BLUE,
    )
    _body = ParagraphStyle(
        "BPBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=14,
        spaceAfter=6,
        textColor=C_BODY_TEXT,
    )
    _label = ParagraphStyle(
        "BPLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=13,
        textColor=C_DARK_BLUE,
    )
    _value = ParagraphStyle(
        "BPValue",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=13,
        textColor=C_BODY_TEXT,
    )
    _bullet = ParagraphStyle(
        "BPBullet",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=14,
        leftIndent=14,
        spaceAfter=4,
        textColor=C_BODY_TEXT,
    )

    # ── Per-page footer drawn directly on the canvas ──────────────────────────

    _footer_line1 = (
        "Generated by BrightPath AI Readiness + Workflow Audit Tool (prototype)"
    )
    _footer_line2 = (
        "All sample data is synthetic. This report provides indicative assessment guidance only."
    )

    def _draw_footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(HexColor("#cccccc"))
        canvas.setLineWidth(0.5)
        canvas.line(L_MARGIN, 1.85 * cm, PAGE_W - R_MARGIN, 1.85 * cm)
        canvas.setFont("Helvetica-Oblique", 6.5)
        canvas.setFillColor(C_MUTED)
        canvas.drawCentredString(PAGE_W / 2, 1.35 * cm, _footer_line1)
        canvas.drawCentredString(PAGE_W / 2, 0.85 * cm, _footer_line2)
        canvas.setFont("Helvetica", 6.5)
        canvas.drawRightString(PAGE_W - R_MARGIN, 1.35 * cm, f"Page {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=L_MARGIN,
        rightMargin=R_MARGIN,
        topMargin=T_MARGIN,
        bottomMargin=B_MARGIN,
    )

    # ── Helper: dark-blue title banner ────────────────────────────────────────

    def _title_banner(org_name, generated_date):
        t = Table(
            [
                [Paragraph("AI Readiness and Workflow Audit Mini Report", _title)],
                [Paragraph(f"{org_name}  ·  {generated_date}", _subtitle)],
            ],
            colWidths=[USABLE_W],
        )
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), C_DARK_BLUE),
            ("TOPPADDING",    (0, 0), (-1, 0),  12),
            ("BOTTOMPADDING", (0, 0), (-1, 0),  2),
            ("TOPPADDING",    (0, 1), (-1, 1),  0),
            ("BOTTOMPADDING", (0, 1), (-1, 1),  12),
            ("LEFTPADDING",   (0, 0), (-1, -1), 14),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
        ]))
        return t

    # ── Helper: light-blue section heading with left accent ───────────────────

    def _section_heading(text):
        t = Table([[Paragraph(text, _heading)]], colWidths=[USABLE_W])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), C_LIGHT_BLUE),
            ("LINEBEFORE",    (0, 0), (0, -1),  4, C_DARK_BLUE),
            ("TOPPADDING",    (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ]))
        return t

    # ── Helper: two-column key-value table ────────────────────────────────────

    def _kv_table(rows):
        data = [
            [Paragraph(k, _label), Paragraph(str(v) if v else "—", _value)]
            for k, v in rows
        ]
        n = len(data)
        style_cmds = [
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING",   (0, 0), (-1, -1), 7),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
            ("BACKGROUND",    (0, 0), (0, -1),  C_HDR_BG),   # label column
            ("BOX",           (0, 0), (-1, -1), 0.5, C_BORDER),
            ("LINEAFTER",     (0, 0), (0, -1),  0.5, C_BORDER),
            ("LINEBELOW",     (0, 0), (-1, n - 2), 0.5, C_BORDER),
        ]
        for i in range(1, n, 2):
            style_cmds.append(("BACKGROUND", (1, i), (1, i), C_ROW_ALT))
        t = Table(data, colWidths=[4.5 * cm, USABLE_W - 4.5 * cm])
        t.setStyle(TableStyle(style_cmds))
        return t

    # ── Helper: bullet / numbered list ────────────────────────────────────────

    def _render_list(text, numbered=False):
        paras = []
        for line in (text or "").splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("- "):
                content = "• " + line[2:]
            elif numbered and len(line) >= 3 and line[1] in ".)" and line[0].isdigit():
                content = line
            else:
                content = line
            paras.append(Paragraph(content, _bullet))
        return paras or [Paragraph("—", _body)]

    # ── Story ─────────────────────────────────────────────────────────────────

    story = []

    org_name       = report_data.get("org_name")       or "Not provided"
    generated_date = report_data.get("generated_date") or date.today().strftime("%d %B %Y")

    story.append(_title_banner(org_name, generated_date))
    story.append(Spacer(1, 0.45 * cm))

    # 1. Organisation Profile
    story.append(KeepTogether([
        _section_heading("1. Organisation Profile"),
        Spacer(1, 0.15 * cm),
        _kv_table([
            ("Organisation",   report_data.get("org_name")),
            ("Type",           report_data.get("org_type")),
            ("Staff",          report_data.get("staff_count")),
            ("Current AI use", report_data.get("ai_use_summary")),
            ("Main concerns",  report_data.get("main_concerns")),
        ]),
    ]))
    story.append(Spacer(1, 0.3 * cm))

    # 2. AI Readiness Summary
    r_score = report_data.get("readiness_score", "—")
    r_cat   = report_data.get("readiness_category") or "—"
    story.append(KeepTogether([
        _section_heading("2. AI Readiness Summary"),
        Spacer(1, 0.15 * cm),
        _kv_table([
            ("Readiness score", f"{r_score} / 100"),
            ("Category",        r_cat),
        ]),
    ]))
    story.append(Spacer(1, 0.3 * cm))

    # 3. Workflow Audit Summary
    w_score = report_data.get("workflow_score", "—")
    w_cat   = report_data.get("workflow_category") or "—"
    story.append(KeepTogether([
        _section_heading("3. Workflow Audit Summary"),
        Spacer(1, 0.15 * cm),
        _kv_table([
            ("Workflow name",        report_data.get("workflow_name")),
            ("Owner / team",         report_data.get("workflow_owner")),
            ("Proposed AI support",  report_data.get("ai_support_idea")),
            ("Suitability score",    f"{w_score} / 50"),
            ("Suitability category", w_cat),
        ]),
    ]))
    story.append(Spacer(1, 0.3 * cm))

    # 4. Risk Assessment Summary
    has_critical = report_data.get("has_critical", False)
    has_high     = report_data.get("has_high",     False)
    story.append(KeepTogether([
        _section_heading("4. Risk Assessment Summary"),
        Spacer(1, 0.15 * cm),
        _kv_table([
            ("Highest risk level",    report_data.get("highest_risk")),
            ("Critical risk present", "Yes" if has_critical else "No"),
            ("High risk present",     "Yes" if has_high     else "No"),
            ("Key risk notes",        report_data.get("key_risk_notes")),
        ]),
    ]))
    story.append(Spacer(1, 0.3 * cm))

    # 5. Pilot Recommendation
    recommendation = report_data.get("recommendation")             or "—"
    explanation    = report_data.get("recommendation_explanation") or ""
    rec_block = [
        _section_heading("5. Pilot Recommendation"),
        Spacer(1, 0.15 * cm),
        Paragraph(f"<b>Recommendation:</b> {recommendation}", _body),
    ]
    if explanation:
        rec_block.append(Paragraph(explanation, _body))
    story.append(KeepTogether(rec_block))
    story.append(Spacer(1, 0.3 * cm))

    # 6. Recommended Safeguards
    story.append(_section_heading("6. Recommended Safeguards"))
    story.append(Spacer(1, 0.15 * cm))
    story.extend(_render_list((report_data.get("safeguards_text") or "").strip()))
    story.append(Spacer(1, 0.3 * cm))

    # 7. Suggested Next Actions
    story.append(_section_heading("7. Suggested Next Actions"))
    story.append(Spacer(1, 0.15 * cm))
    story.extend(_render_list((report_data.get("next_actions_text") or "").strip(), numbered=True))
    story.append(Spacer(1, 0.3 * cm))

    # 8. Responsible Use and Limitations
    story.append(KeepTogether([
        _section_heading("8. Responsible Use and Limitations"),
        Spacer(1, 0.15 * cm),
        Paragraph(
            "This report is generated by a prototype tool and is intended to support discussion, "
            "planning, and early-stage AI adoption decisions. It is not legal, safeguarding, HR, "
            "compliance, medical, financial, or academic-integrity advice. Organisations should "
            "review all recommendations with appropriate responsible owners before acting.",
            _body,
        ),
    ]))
    story.append(Paragraph(
        "The tool should not be used with identifiable learner data, safeguarding case "
        "information, confidential client records, staff HR/disciplinary information, "
        "regulated information, or sensitive personal data unless appropriate governance, "
        "approvals, and controls are in place.",
        _body,
    ))
    story.append(Paragraph(
        "AI recommendations should be treated as draft support. Human review, data protection "
        "checks, risk assessment, and organisational judgement remain required.",
        _body,
    ))
    story.append(Spacer(1, 0.3 * cm))

    # 9. Consultant Notes
    consultant_notes = (report_data.get("consultant_notes") or "").strip()
    story.append(KeepTogether([
        _section_heading("9. Consultant Notes"),
        Spacer(1, 0.15 * cm),
        Paragraph(
            consultant_notes if consultant_notes else "No consultant notes recorded.",
            _body,
        ),
    ]))

    doc.build(story, onFirstPage=_draw_footer, onLaterPages=_draw_footer)
    return buffer.getvalue()
