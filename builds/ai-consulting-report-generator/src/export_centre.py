"""Export Centre — Build 5 Phase 8.

Coordinates export readiness, data assembly, and all export format generation.
No external AI calls. No real client data. Deterministic and template-based.
"""

from datetime import date

_RESPONSIBLE_USE_NOTE = (
    "This export package is generated from synthetic/demo audit data only. "
    "It must not be used with real client records, learner data, safeguarding case details, "
    "staff HR data, personal data, confidential data, or regulated information without "
    "appropriate governance, approvals, and responsible owners. "
    "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
    "financial, academic-integrity, or professional advice. "
    "Human review remains required before any real-world use."
)

_PROTOTYPE_NOTE = (
    "This export is produced by a deterministic prototype. All outputs must be reviewed, "
    "validated, and approved by a qualified consultant before client delivery."
)

_REQUIRED_KEYS = ["audit_data", "client_report_markdown"]

_RECOMMENDED_KEYS = [
    "readiness_summary",
    "risk_register",
    "risk_register_summary",
    "opportunity_portfolio",
    "opportunity_summary",
    "implementation_roadmap",
    "implementation_roadmap_summary",
    "report_sections",
    "client_report_data",
    "client_report_markdown",
]


# ── Format list ────────────────────────────────────────────────────────────────


def get_export_formats() -> list:
    """Return the list of available export formats."""
    return ["Markdown", "PDF", "PowerPoint (PPTX)"]


# ── Readiness check ────────────────────────────────────────────────────────────


def check_export_readiness(session_state: dict) -> dict:
    """Inspect session state and return an export readiness report."""
    ss = session_state or {}
    has_audit = bool(ss.get("audit_data"))
    has_report = bool(ss.get("client_report_markdown"))

    available = [k for k in _RECOMMENDED_KEYS if ss.get(k) is not None]
    missing = [k for k in _RECOMMENDED_KEYS if ss.get(k) is None]

    steps = []
    if not has_audit:
        steps = [
            "Go to Audit Data.",
            "Load the BrightPath demo audit data.",
            "Generate the earlier outputs (Readiness, Risk, Opportunities, Roadmap, Report Sections).",
            "Generate the Client Report.",
            "Return to Export Centre.",
        ]
    elif not has_report:
        steps = [
            "Go to Client Report.",
            "Generate the client report.",
            "Return to Export Centre.",
        ]
    else:
        for key in _RECOMMENDED_KEYS:
            if key not in available and key not in ("client_report_data", "client_report_markdown"):
                steps.append(f"Run the {key.replace('_', ' ').title()} page to enrich the export.")

    return {
        "is_ready": has_audit and has_report,
        "available_outputs": available,
        "missing_outputs": missing,
        "recommended_next_steps": steps,
        "can_export_markdown": has_audit,
        "can_export_pdf": has_audit,
        "can_export_pptx": has_audit,
    }


# ── Export data assembly ───────────────────────────────────────────────────────


def build_export_data_from_session_state(session_state: dict) -> dict:
    """Collect all session state data into a single export data dict."""
    ss = session_state or {}
    audit = ss.get("audit_data") or {}
    org_name = (
        audit.get("organisation_profile", {}).get("organisation_name")
        or "Unnamed organisation"
    )
    source = ss.get("client_report_data", {}) or {}
    source_outputs = source.get("source_outputs_available") or {
        "audit_data": bool(audit),
        "readiness_summary": ss.get("readiness_summary") is not None,
        "risk_register": ss.get("risk_register") is not None,
        "opportunity_portfolio": ss.get("opportunity_portfolio") is not None,
        "implementation_roadmap": ss.get("implementation_roadmap") is not None,
        "report_sections": ss.get("report_sections") is not None,
    }

    return {
        "organisation_name": org_name,
        "generated_date": date.today().isoformat(),
        "audit_data": audit,
        "readiness_summary": ss.get("readiness_summary"),
        "risk_register": ss.get("risk_register"),
        "risk_register_summary": ss.get("risk_register_summary"),
        "opportunity_portfolio": ss.get("opportunity_portfolio"),
        "opportunity_summary": ss.get("opportunity_summary"),
        "implementation_roadmap": ss.get("implementation_roadmap"),
        "implementation_roadmap_summary": ss.get("implementation_roadmap_summary"),
        "report_sections": ss.get("report_sections"),
        "client_report_data": ss.get("client_report_data"),
        "client_report_markdown": ss.get("client_report_markdown") or "",
        "source_outputs_available": source_outputs,
        "responsible_use_note": _RESPONSIBLE_USE_NOTE,
        "prototype_note": _PROTOTYPE_NOTE,
    }


# ── Quality checklist ──────────────────────────────────────────────────────────


def generate_export_quality_checklist(export_data: dict) -> list:
    """Return a list of quality check dicts for the export package."""
    ed = export_data or {}
    cr_md = ed.get("client_report_markdown") or ""
    source = ed.get("source_outputs_available") or {}

    def _in(text: str) -> bool:
        return text.lower() in cr_md.lower()

    checks = [
        {
            "item": "Client report Markdown generated",
            "passed": bool(cr_md),
        },
        {
            "item": "Audit data loaded",
            "passed": source.get("audit_data", bool(ed.get("audit_data"))),
        },
        {
            "item": "Readiness summary included",
            "passed": source.get("readiness_summary", False),
        },
        {
            "item": "Risk register included",
            "passed": source.get("risk_register", False),
        },
        {
            "item": "Opportunity portfolio included",
            "passed": source.get("opportunity_portfolio", False),
        },
        {
            "item": "Implementation roadmap included",
            "passed": source.get("implementation_roadmap", False),
        },
        {
            "item": "Responsible-use boundaries present",
            "passed": _in("responsible-use") or _in("responsible use"),
        },
        {
            "item": "Prototype limitations present",
            "passed": _in("prototype limitations"),
        },
        {
            "item": "Human review note present",
            "passed": _in("human review"),
        },
    ]
    return checks


# ── Summary ────────────────────────────────────────────────────────────────────


def summarise_export_package(export_data: dict) -> dict:
    """Return a summary dict for the export package."""
    ed = export_data or {}
    source = ed.get("source_outputs_available") or {}

    sections_available = sum(1 for v in source.values() if v)
    sections_missing = sum(1 for v in source.values() if not v)

    risk_register = ed.get("risk_register") or []
    opp_portfolio = ed.get("opportunity_portfolio") or {}
    pilots = opp_portfolio.get("pilots") or []
    opps = opp_portfolio.get("opportunities") or []
    rm_summary = ed.get("implementation_roadmap_summary") or {}
    roadmap_actions = rm_summary.get("total_actions", 0)

    return {
        "organisation_name": ed.get("organisation_name") or "Unnamed organisation",
        "sections_available": sections_available,
        "sections_missing": sections_missing,
        "risks_included": len(risk_register),
        "opportunities_included": len(opps),
        "pilots_included": len(pilots),
        "roadmap_actions_included": roadmap_actions,
        "export_formats": get_export_formats(),
        "human_review_required": True,
    }


# ── Filename base ──────────────────────────────────────────────────────────────


def create_export_filename_base(organisation_name: str) -> str:
    """Return a safe base name for export files."""
    from src.utils import slugify
    slug = slugify(organisation_name or "client")[:50]
    return f"{date.today()}-ai-report-{slug}"


# ── Prepare individual exports ─────────────────────────────────────────────────


def prepare_markdown_export(export_data: dict) -> tuple:
    """Return (markdown_text, filename)."""
    from src.utils import create_safe_filename
    ed = export_data or {}
    org = ed.get("organisation_name") or "client"
    md = ed.get("client_report_markdown") or "No client report generated yet."
    filename = create_safe_filename(f"ai-consulting-report-{org}", "md")
    return md, filename


def prepare_pdf_export(
    export_data: dict,
    analytics: dict | None = None,
    chart_paths: dict | None = None,
) -> tuple:
    """Return (pdf_bytes, filename). Returns (b'', filename) on failure."""
    from src.pdf_exporter import export_client_report_to_pdf_bytes, create_safe_pdf_filename
    ed = export_data or {}
    org = ed.get("organisation_name") or "client"
    pdf_bytes = export_client_report_to_pdf_bytes(ed, analytics, chart_paths)
    filename = create_safe_pdf_filename(f"ai-consulting-report-{org}")
    return pdf_bytes, filename


def prepare_pptx_export(
    export_data: dict,
    analytics: dict | None = None,
    chart_paths: dict | None = None,
) -> tuple:
    """Return (pptx_bytes, filename). Returns (b'', filename) on failure."""
    from src.pptx_exporter import export_client_report_to_pptx_bytes, create_safe_pptx_filename
    ed = export_data or {}
    org = ed.get("organisation_name") or "client"
    pptx_bytes = export_client_report_to_pptx_bytes(ed, analytics, chart_paths)
    filename = create_safe_pptx_filename(f"ai-executive-deck-{org}")
    return pptx_bytes, filename


def prepare_all_exports(
    export_data: dict,
    analytics: dict | None = None,
    chart_paths: dict | None = None,
) -> dict:
    """Prepare Markdown, PDF, and PPTX exports. Returns dict with all results."""
    md, md_fname = prepare_markdown_export(export_data)
    pdf_bytes, pdf_fname = prepare_pdf_export(export_data, analytics, chart_paths)
    pptx_bytes, pptx_fname = prepare_pptx_export(export_data, analytics, chart_paths)
    return {
        "markdown": md,
        "markdown_filename": md_fname,
        "pdf_bytes": pdf_bytes,
        "pdf_filename": pdf_fname,
        "pptx_bytes": pptx_bytes,
        "pptx_filename": pptx_fname,
    }
