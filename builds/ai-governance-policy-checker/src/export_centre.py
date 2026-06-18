"""
Export Centre — AI Governance Policy Checker
Build 6 · BrightPath ChatGPT Mastery Project

Prepares Markdown and PDF export packages from all available Build 6 outputs.
Deterministic only. No external AI, LLM, or API calls.
Synthetic/demo data only.
"""

import datetime


_REQUIRED_FOR_EXPORT = ["policy_pack", "governance_report_markdown"]

_RECOMMENDED_FOR_EXPORT = [
    "policy_pack",
    "governance_framework",
    "coverage_results",
    "coverage_summary",
    "gap_analysis",
    "gap_summary",
    "policy_recommendations",
    "recommendation_summary",
    "governance_maturity",
    "governance_maturity_summary",
    "governance_report_data",
    "governance_report_markdown",
]

_RESPONSIBLE_USE_NOTE = (
    "This governance report is generated from synthetic/demo policy text only. "
    "It must not be used with real client policies, learner data, safeguarding "
    "case details, staff HR data, personal data, confidential data, or regulated "
    "information without appropriate governance, approvals, and responsible owners."
)

_PROTOTYPE_NOTE = (
    "This prototype does not provide legal, safeguarding, HR, compliance, "
    "data-protection, financial, medical, academic-integrity, or professional "
    "governance advice. Suggested wording directions are not legally approved "
    "policy text. They require review by appropriate responsible owners before "
    "real-world use. This is a deterministic governance review support tool, "
    "not a compliance certification system. Human review remains required before "
    "any real-world use."
)

_STEP_MAP = {
    "policy_pack": "Go to Policy Library and load the BrightPath synthetic policy pack.",
    "governance_framework": "Go to Governance Framework and load the governance framework.",
    "coverage_results": "Go to Policy Checker and run the policy coverage check.",
    "coverage_summary": "Go to Policy Checker and run the policy coverage check.",
    "gap_analysis": "Go to Gap Analysis to generate the gap analysis.",
    "gap_summary": "Go to Gap Analysis to generate the gap analysis.",
    "policy_recommendations": "Go to Recommendations to generate policy improvement recommendations.",
    "recommendation_summary": "Go to Recommendations to generate policy improvement recommendations.",
    "governance_maturity": "Go to Governance Maturity to generate the maturity summary.",
    "governance_maturity_summary": "Go to Governance Maturity to generate the maturity summary.",
    "governance_report_data": "Go to Governance Report and generate the governance report.",
    "governance_report_markdown": "Go to Governance Report and generate the governance report.",
}


def get_export_formats() -> list[str]:
    """Return the list of supported export formats."""
    return ["Markdown", "PDF"]


def check_export_readiness(session_state: dict) -> dict:
    """
    Inspect session state and return export readiness status.

    Returns:
        is_ready: True if minimum required data is present (policy pack + report).
        available_outputs: list of keys confirmed in session state.
        missing_outputs: list of recommended keys not yet in session state.
        recommended_next_steps: deduplicated guidance on what to run first.
        can_export_markdown: True if Markdown export is possible.
        can_export_pdf: True if PDF export is possible.
    """
    available = [k for k in _RECOMMENDED_FOR_EXPORT if k in session_state]
    missing = [k for k in _RECOMMENDED_FOR_EXPORT if k not in session_state]

    can_export_markdown = (
        "policy_pack" in session_state
        and "governance_report_markdown" in session_state
    )
    can_export_pdf = can_export_markdown

    seen: set[str] = set()
    recommended_next_steps = []
    for key in missing:
        step = _STEP_MAP.get(key, "")
        if step and step not in seen:
            seen.add(step)
            recommended_next_steps.append(step)

    return {
        "is_ready": can_export_markdown,
        "available_outputs": available,
        "missing_outputs": missing,
        "recommended_next_steps": recommended_next_steps,
        "can_export_markdown": can_export_markdown,
        "can_export_pdf": can_export_pdf,
    }


def build_export_data_from_session_state(session_state: dict) -> dict:
    """
    Build the export data dict from all available session state outputs.
    Missing outputs are represented as None.
    """
    policy_pack = session_state.get("policy_pack") or {}
    org_name = policy_pack.get("organisation_name", "Unnamed organisation")

    source_outputs_available = {
        key: key in session_state for key in _RECOMMENDED_FOR_EXPORT
    }

    return {
        "organisation_name": org_name,
        "generated_date": datetime.date.today().isoformat(),
        "policy_pack": session_state.get("policy_pack"),
        "policy_pack_summary": session_state.get("policy_pack_summary"),
        "governance_framework": session_state.get("governance_framework"),
        "governance_framework_summary": session_state.get("governance_framework_summary"),
        "coverage_results": session_state.get("coverage_results"),
        "coverage_summary": session_state.get("coverage_summary"),
        "gap_analysis": session_state.get("gap_analysis"),
        "gap_summary": session_state.get("gap_summary"),
        "policy_recommendations": session_state.get("policy_recommendations"),
        "recommendation_summary": session_state.get("recommendation_summary"),
        "governance_maturity": session_state.get("governance_maturity"),
        "governance_maturity_summary": session_state.get("governance_maturity_summary"),
        "governance_report_data": session_state.get("governance_report_data"),
        "governance_report_markdown": session_state.get("governance_report_markdown", ""),
        "source_outputs_available": source_outputs_available,
        "responsible_use_note": _RESPONSIBLE_USE_NOTE,
        "prototype_note": _PROTOTYPE_NOTE,
    }


def generate_export_quality_checklist(export_data: dict) -> list[dict]:
    """
    Generate a quality checklist for the export package.

    Each item has:
        label: str
        is_complete: bool
        importance: "Required" | "Recommended" | "Advisory"
        note: str
    """
    available = export_data.get("source_outputs_available", {})
    markdown = export_data.get("governance_report_markdown", "") or ""

    def has(key: str) -> bool:
        return bool(available.get(key)) or bool(export_data.get(key))

    def in_markdown(phrase: str) -> bool:
        return phrase.lower() in markdown.lower()

    return [
        {
            "label": "Synthetic policy pack loaded",
            "is_complete": has("policy_pack"),
            "importance": "Required",
            "note": "The policy pack is the source input for the entire governance review.",
        },
        {
            "label": "Governance framework loaded",
            "is_complete": has("governance_framework"),
            "importance": "Recommended",
            "note": "The framework defines the 12 governance domains assessed in the review.",
        },
        {
            "label": "Coverage review generated",
            "is_complete": has("coverage_results"),
            "importance": "Recommended",
            "note": "Policy coverage scores form the foundation of the governance report.",
        },
        {
            "label": "Gap analysis generated",
            "is_complete": has("gap_analysis"),
            "importance": "Recommended",
            "note": "Gap analysis identifies where policy coverage is absent, weak, or insufficient.",
        },
        {
            "label": "Recommendations generated",
            "is_complete": has("policy_recommendations"),
            "importance": "Recommended",
            "note": "Recommendations give the organisation actionable policy improvement steps.",
        },
        {
            "label": "Governance maturity summary generated",
            "is_complete": has("governance_maturity"),
            "importance": "Recommended",
            "note": "The maturity score gives a calibrated picture of overall governance readiness.",
        },
        {
            "label": "Governance report generated",
            "is_complete": has("governance_report_markdown"),
            "importance": "Required",
            "note": "The governance report assembles all outputs into a single client-facing document.",
        },
        {
            "label": "Responsible-use boundaries included",
            "is_complete": in_markdown("responsible-use") or in_markdown("synthetic/demo"),
            "importance": "Required",
            "note": "Responsible-use boundaries must be included in all exported governance reports.",
        },
        {
            "label": "Prototype limitations included",
            "is_complete": in_markdown("prototype limitations"),
            "importance": "Required",
            "note": "Prototype limitations must be included so readers understand the scope of the review.",
        },
        {
            "label": "Human review note included",
            "is_complete": in_markdown("human review"),
            "importance": "Required",
            "note": "Human review is required before any real-world use of the report.",
        },
        {
            "label": "Markdown export available",
            "is_complete": bool(markdown),
            "importance": "Advisory",
            "note": "Markdown export is available when the governance report has been generated.",
        },
        {
            "label": "PDF export available",
            "is_complete": bool(markdown),
            "importance": "Advisory",
            "note": "PDF export is available when the governance report has been generated.",
        },
    ]


def summarise_export_package(export_data: dict) -> dict:
    """Summarise the export package for display."""
    available = export_data.get("source_outputs_available", {})

    total_outputs = len(available)
    outputs_available = sum(1 for v in available.values() if v)
    outputs_missing = total_outputs - outputs_available

    coverage = export_data.get("coverage_results") or {}
    gap_analysis = export_data.get("gap_analysis") or {}
    recs = export_data.get("policy_recommendations") or {}
    maturity = export_data.get("governance_maturity") or {}
    markdown = export_data.get("governance_report_markdown", "") or ""

    return {
        "organisation_name": export_data.get("organisation_name", "Unnamed organisation"),
        "generated_date": export_data.get("generated_date", ""),
        "total_outputs": total_outputs,
        "outputs_available": outputs_available,
        "outputs_missing": outputs_missing,
        "export_formats": get_export_formats(),
        "domains_reviewed": coverage.get("total_domains_checked", 0),
        "gaps_included": gap_analysis.get("total_gaps", 0),
        "recommendations_included": recs.get("total_recommendations", 0),
        "maturity_level": maturity.get("overall_maturity_level", ""),
        "governance_score": maturity.get("overall_governance_score", 0),
        "markdown_available": bool(markdown),
        "pdf_available": bool(markdown),
    }


def create_export_filename_base(organisation_name: str) -> str:
    """Create a safe base filename (no extension) for exports."""
    safe = str(organisation_name).lower()
    safe = "".join(c if c.isalnum() or c in (" ", "-") else "" for c in safe)
    safe = safe.strip().replace(" ", "-")
    safe = "-".join(p for p in safe.split("-") if p)
    if not safe:
        safe = "unnamed-organisation"
    date = datetime.date.today().isoformat()
    return f"{safe}-ai-governance-report-{date}"


def prepare_markdown_export(export_data: dict) -> tuple[str, str]:
    """
    Prepare the Markdown export.
    Returns (markdown_text, filename).
    """
    markdown = export_data.get("governance_report_markdown", "") or ""
    org = export_data.get("organisation_name", "Unnamed organisation")
    filename = create_export_filename_base(org) + ".md"
    return markdown, filename


def prepare_pdf_export(
    export_data: dict,
    analytics: dict | None = None,
    chart_paths: dict | None = None,
) -> tuple[bytes, str]:
    """
    Prepare the PDF export.
    Returns (pdf_bytes, filename).
    """
    from src.pdf_exporter import export_governance_report_to_pdf_bytes

    pdf_bytes = export_governance_report_to_pdf_bytes(export_data, analytics, chart_paths)
    org = export_data.get("organisation_name", "Unnamed organisation")
    filename = create_export_filename_base(org) + ".pdf"
    return pdf_bytes, filename


def prepare_all_exports(
    export_data: dict,
    analytics: dict | None = None,
    chart_paths: dict | None = None,
) -> dict:
    """
    Prepare all exports. Returns dict of format -> {content, filename, error}.
    Handles errors gracefully — missing data will not crash.
    """
    result: dict = {}

    try:
        md_text, md_filename = prepare_markdown_export(export_data)
        result["markdown"] = {"content": md_text, "filename": md_filename, "error": None}
    except Exception as e:
        result["markdown"] = {"content": "", "filename": "", "error": str(e)}

    try:
        pdf_bytes, pdf_filename = prepare_pdf_export(export_data, analytics, chart_paths)
        result["pdf"] = {"content": pdf_bytes, "filename": pdf_filename, "error": None}
    except Exception as e:
        result["pdf"] = {"content": b"", "filename": "", "error": str(e)}

    return result
