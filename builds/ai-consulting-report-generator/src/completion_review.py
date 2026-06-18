"""Completion review helpers for Build 5 Phase 9.

This module checks portfolio readiness for the AI Consulting Report Generator.
It uses deterministic local checks only: session-state keys, expected docs, and
fixed portfolio/case-study notes. No external AI calls are used.
"""

from pathlib import Path


_PHASES = [
    {
        "phase": "Phase 1",
        "name": "Scaffold and sample audit data setup",
        "purpose": "Create the app structure, synthetic BrightPath audit data, and baseline readiness scoring.",
        "status": "Complete",
        "evidence": "Streamlit scaffold, sample_data, audit data manager, utilities, tests, and docs.",
    },
    {
        "phase": "Phase 2",
        "name": "Readiness summary and score interpretation",
        "purpose": "Turn readiness scores into category-level interpretation, strengths, gaps, and recommendations.",
        "status": "Complete",
        "evidence": "Readiness Summary page, scoring_summary helpers, Markdown export, and tests.",
    },
    {
        "phase": "Phase 3",
        "name": "Risk register generator",
        "purpose": "Convert synthetic audit risks into scored risks with controls, owners, and priority actions.",
        "status": "Complete",
        "evidence": "Risk Register page, risk_register module, Markdown export, and tests.",
    },
    {
        "phase": "Phase 4",
        "name": "Opportunity and pilot recommendation generator",
        "purpose": "Score AI workflow opportunities and sequence responsible pilot recommendations.",
        "status": "Complete",
        "evidence": "Opportunity page, opportunity_generator module, pilot sequence, Markdown export, and tests.",
    },
    {
        "phase": "Phase 5",
        "name": "30/60/90-day roadmap generator",
        "purpose": "Create an implementation roadmap from audit findings, risks, pilots, and governance gaps.",
        "status": "Complete",
        "evidence": "Roadmap page, roadmap_generator module, action plan summaries, Markdown export, and tests.",
    },
    {
        "phase": "Phase 6",
        "name": "Report section generator",
        "purpose": "Generate polished client-facing report sections from the available Build 5 outputs.",
        "status": "Complete",
        "evidence": "Report Sections page, eleven deterministic sections, source-output tracking, and tests.",
    },
    {
        "phase": "Phase 7",
        "name": "Client report builder",
        "purpose": "Assemble all outputs into a complete Markdown consulting report with section selection.",
        "status": "Complete",
        "evidence": "Client Report page, report_builder module, full report Markdown export, and tests.",
    },
    {
        "phase": "Phase 8",
        "name": "Export Centre with PDF/PPTX/charts",
        "purpose": "Prepare Markdown, PDF, and PowerPoint exports with deterministic analytics charts.",
        "status": "Complete",
        "evidence": "Export Centre page, export_centre, report_analytics, chart_utils, PDF/PPTX exporters, and tests.",
    },
    {
        "phase": "Phase 9",
        "name": "Completion review and portfolio notes",
        "purpose": "Close the build with final readiness checks, portfolio notes, case study notes, and demo guidance.",
        "status": "Complete",
        "evidence": "Completion Review page, completion_review module, portfolio docs, and final test checklist.",
    },
]


_EXPECTED_OUTPUTS = [
    {"key": "audit_data", "label": "Audit data", "page": "Audit Data"},
    {"key": "audit_summary", "label": "Audit summary", "page": "Audit Data"},
    {"key": "readiness_summary", "label": "Readiness summary", "page": "Readiness Summary"},
    {"key": "readiness_summary_markdown", "label": "Readiness summary Markdown", "page": "Readiness Summary"},
    {"key": "risk_register", "label": "Risk register", "page": "Risk Register"},
    {"key": "risk_register_summary", "label": "Risk register summary", "page": "Risk Register"},
    {"key": "risk_register_markdown", "label": "Risk register Markdown", "page": "Risk Register"},
    {"key": "opportunity_portfolio", "label": "Opportunity portfolio", "page": "Opportunity and Pilot Recommendations"},
    {"key": "opportunity_summary", "label": "Opportunity summary", "page": "Opportunity and Pilot Recommendations"},
    {"key": "opportunity_portfolio_markdown", "label": "Opportunity portfolio Markdown", "page": "Opportunity and Pilot Recommendations"},
    {"key": "implementation_roadmap", "label": "Implementation roadmap", "page": "Roadmap"},
    {"key": "implementation_roadmap_summary", "label": "Implementation roadmap summary", "page": "Roadmap"},
    {"key": "implementation_roadmap_markdown", "label": "Implementation roadmap Markdown", "page": "Roadmap"},
    {"key": "report_sections", "label": "Report sections", "page": "Report Sections"},
    {"key": "report_sections_summary", "label": "Report sections summary", "page": "Report Sections"},
    {"key": "report_sections_markdown", "label": "Report sections Markdown", "page": "Report Sections"},
    {"key": "client_report_data", "label": "Client report data", "page": "Client Report"},
    {"key": "client_report_markdown", "label": "Client report Markdown", "page": "Client Report"},
    {"key": "client_report_filename", "label": "Client report filename", "page": "Client Report"},
    {"key": "export_data", "label": "Export data", "page": "Export Centre"},
    {"key": "client_report_analytics", "label": "Client report analytics", "page": "Export Centre"},
    {"key": "client_report_chart_paths", "label": "Client report chart paths", "page": "Export Centre"},
    {"key": "client_report_pdf_bytes", "label": "Client report PDF bytes", "page": "Export Centre"},
    {"key": "client_report_pptx_bytes", "label": "Client report PPTX bytes", "page": "Export Centre"},
]


_DOCUMENTATION_FILES = [
    "README.md",
    "docs/build-notes.md",
    "docs/architecture.md",
    "docs/safety-boundaries.md",
    "docs/demo-script.md",
    "docs/screenshots-checklist.md",
    "docs/future-improvements.md",
    "docs/completion-review.md",
    "docs/portfolio-notes.md",
    "docs/testing-checklist.md",
    "docs/case-study-summary.md",
]


def _percentage(done: int, total: int) -> int:
    if total <= 0:
        return 0
    return int(round((done / total) * 100))


def _is_available(value) -> bool:
    if value is None:
        return False
    if isinstance(value, (str, bytes, list, tuple, dict, set)):
        return len(value) > 0
    return bool(value)


def get_build5_phase_checklist() -> list[dict]:
    """Return the completed Build 5 phase checklist."""
    return [dict(item) for item in _PHASES]


def get_expected_build5_outputs() -> list[dict]:
    """Return expected session-state outputs for a full Build 5 demo run."""
    return [dict(item) for item in _EXPECTED_OUTPUTS]


def check_session_state_outputs(session_state: dict) -> dict:
    """Report which expected Build 5 outputs are currently present."""
    ss = session_state or {}
    available = []
    missing = []

    for expected in get_expected_build5_outputs():
        key = expected["key"]
        item = dict(expected)
        item["available"] = _is_available(ss.get(key))
        if item["available"]:
            available.append(item)
        else:
            missing.append(item)

    total = len(_EXPECTED_OUTPUTS)
    available_count = len(available)
    pct = _percentage(available_count, total)

    return {
        "expected_outputs": get_expected_build5_outputs(),
        "available_outputs": available,
        "missing_outputs": missing,
        "available_count": available_count,
        "missing_count": len(missing),
        "total_expected": total,
        "completion_percentage": pct,
        "output_completion_percentage": pct,
        "recommended_next_actions": _recommended_output_actions(missing),
    }


def _recommended_output_actions(missing_outputs: list[dict]) -> list[str]:
    if not missing_outputs:
        return ["Run a final manual walkthrough, capture screenshots, and confirm PDF/PPTX downloads open correctly."]

    missing_keys = {item["key"] for item in missing_outputs}
    actions = []

    if {"audit_data", "audit_summary"} & missing_keys:
        actions.append("Load the BrightPath demo audit data on the Audit Data page.")
    if {"readiness_summary", "readiness_summary_markdown"} & missing_keys:
        actions.append("Open Readiness Summary and generate the readiness interpretation.")
    if {"risk_register", "risk_register_summary", "risk_register_markdown"} & missing_keys:
        actions.append("Open Risk Register and generate the risk register outputs.")
    if {"opportunity_portfolio", "opportunity_summary", "opportunity_portfolio_markdown"} & missing_keys:
        actions.append("Open Opportunity and Pilot Recommendations and generate the portfolio.")
    if {"implementation_roadmap", "implementation_roadmap_summary", "implementation_roadmap_markdown"} & missing_keys:
        actions.append("Open Roadmap and generate the 30/60/90-day implementation plan.")
    if {"report_sections", "report_sections_summary", "report_sections_markdown"} & missing_keys:
        actions.append("Open Report Sections and generate the client-facing sections.")
    if {"client_report_data", "client_report_markdown", "client_report_filename"} & missing_keys:
        actions.append("Open Client Report and generate the assembled Markdown report.")
    if {"export_data", "client_report_analytics", "client_report_chart_paths", "client_report_pdf_bytes", "client_report_pptx_bytes"} & missing_keys:
        actions.append("Open Export Centre and generate the Markdown, PDF, PPTX, analytics, and chart outputs.")

    return actions


def check_documentation_files(base_path: str = ".") -> dict:
    """Check whether expected Build 5 documentation files exist."""
    root = Path(base_path or ".")
    existing = []
    missing = []

    for rel_path in _DOCUMENTATION_FILES:
        if (root / rel_path).is_file():
            existing.append(rel_path)
        else:
            missing.append(rel_path)

    total = len(_DOCUMENTATION_FILES)
    existing_count = len(existing)
    pct = _percentage(existing_count, total)
    return {
        "expected_files": list(_DOCUMENTATION_FILES),
        "existing_files": existing,
        "missing_files": missing,
        "existing_count": existing_count,
        "missing_count": len(missing),
        "total_expected": total,
        "documentation_completion_percentage": pct,
        "completion_percentage": pct,
    }


def generate_completion_score(
    phase_status: list[dict],
    output_status: dict,
    documentation_status: dict,
) -> dict:
    """Generate the overall Build 5 completion score."""
    phases = phase_status or []
    complete_phases = sum(1 for item in phases if item.get("status") == "Complete")
    phase_pct = _percentage(complete_phases, len(phases))
    output_pct = int(output_status.get("output_completion_percentage", output_status.get("completion_percentage", 0)) or 0)
    doc_pct = int(documentation_status.get("documentation_completion_percentage", documentation_status.get("completion_percentage", 0)) or 0)

    if phase_pct == 100 and output_pct >= 90 and doc_pct >= 90:
        overall_status = "Complete"
        final_label = (
            "Build 5 is ready for portfolio review and demonstration, subject to final "
            "screenshots and manual export checks."
        )
    elif phase_pct >= 90 and output_pct >= 50 and doc_pct >= 70:
        overall_status = "Mostly complete"
        final_label = (
            "Build 5 is mostly complete but should be manually tested across the full "
            "workflow before portfolio presentation."
        )
    else:
        overall_status = "In progress"
        final_label = (
            "Build 5 needs further implementation or testing before being presented as a "
            "portfolio asset."
        )

    actions = []
    if output_pct < 100:
        actions.extend(output_status.get("recommended_next_actions") or [])
    if doc_pct < 100:
        missing = documentation_status.get("missing_files") or []
        actions.append("Add or update missing documentation files: " + ", ".join(missing) + ".")
    if not actions:
        actions = [
            "Capture final screenshots using docs/screenshots-checklist.md.",
            "Run the full manual workflow in docs/testing-checklist.md.",
            "Open the generated PDF and PowerPoint deck to confirm formatting.",
        ]

    return {
        "overall_status": overall_status,
        "phase_completion_percentage": phase_pct,
        "output_completion_percentage": output_pct,
        "documentation_completion_percentage": doc_pct,
        "final_readiness_label": final_label,
        "recommended_final_actions": actions,
    }


def generate_build5_completion_review(
    session_state: dict,
    base_path: str = ".",
) -> dict:
    """Build a complete Phase 9 completion review dictionary."""
    phases = get_build5_phase_checklist()
    outputs = check_session_state_outputs(session_state)
    docs = check_documentation_files(base_path)
    score = generate_completion_score(phases, outputs, docs)

    return {
        "build_title": "AI Consulting Report Generator",
        "build_number": "Build 5",
        "completion_status": score,
        "phase_checklist": phases,
        "output_status": outputs,
        "documentation_status": docs,
        "portfolio_value": (
            "A portfolio-ready demonstration of an end-to-end AI consulting workflow: "
            "audit findings become a readiness interpretation, risk register, opportunity "
            "portfolio, roadmap, client report, PDF, and executive deck."
        ),
        "commercial_value": (
            "Shows how a consultant could reduce report-production time after an AI readiness "
            "engagement while keeping human review, responsible-use boundaries, and evidence "
            "of source outputs visible."
        ),
        "technical_value": (
            "Demonstrates Streamlit state orchestration, deterministic scoring, structured "
            "data assembly, report generation, reportlab PDF export, python-pptx deck export, "
            "matplotlib charting, and broad pytest coverage."
        ),
        "responsible_use_position": (
            "Synthetic/demo organisation data only. No real learner data, safeguarding case "
            "information, confidential client records, staff HR data, personal data, or "
            "regulated information. Outputs are not legal, safeguarding, HR, compliance, "
            "financial, medical, or professional advice. Human review and responsible owners "
            "are required before any real-world use."
        ),
        "recommended_final_actions": score["recommended_final_actions"],
        "prototype_note": (
            "Build 5 is a local deterministic prototype. It is not production deployed and "
            "does not include authentication, persistent storage, cloud hosting, or real-data ingestion."
        ),
        "human_review_note": (
            "A qualified human consultant must review, validate, and approve every output "
            "before it is shared or used in a real engagement."
        ),
    }


def generate_portfolio_summary() -> dict:
    """Return portfolio positioning notes for Build 5."""
    return {
        "project_name": "AI Consulting Report Generator",
        "one_line_summary": (
            "A Streamlit-based AI consulting prototype that turns synthetic AI readiness "
            "audit findings into a structured client-facing report, risk register, "
            "opportunity portfolio, 30/60/90-day roadmap, PDF report, and PowerPoint "
            "executive deck."
        ),
        "problem_solved": (
            "Consultants often spend hours turning audit notes into client-ready reports. "
            "This build shows how structured synthetic audit findings can be transformed "
            "into a complete first-draft consulting pack."
        ),
        "target_users": [
            "AI consultants",
            "AI governance leads",
            "L&D teams planning responsible AI adoption",
            "Portfolio reviewers evaluating the ChatGPT Mastery build sequence",
        ],
        "core_workflow": [
            "Load the BrightPath synthetic audit data.",
            "Generate readiness interpretation, risks, opportunities, and roadmap.",
            "Generate report sections and assemble the client report.",
            "Export Markdown, PDF, and PowerPoint deliverables.",
            "Run the Completion Review for final portfolio/demo readiness.",
        ],
        "key_features": [
            "Six-dimension AI readiness interpretation",
            "AI risk register with controls and owners",
            "Opportunity and pilot recommendation portfolio",
            "30/60/90-day implementation roadmap",
            "Full Markdown client report builder",
            "PDF and PPTX export with analytics charts",
            "Completion review and portfolio notes",
        ],
        "technical_stack": [
            "Python",
            "Streamlit",
            "pytest",
            "reportlab",
            "python-pptx",
            "matplotlib",
            "st.session_state",
        ],
        "responsible_ai_features": [
            "Synthetic/demo data only",
            "No external LLM or AI API calls",
            "No real learner, HR, safeguarding, personal, confidential, or regulated data",
            "Prototype notices and responsible-use boundaries in app and exports",
            "Human review required before any real-world use",
        ],
        "portfolio_positioning": (
            "Build 5 is the portfolio capstone for the consulting workflow: it turns "
            "diagnosis into deliverables while showing responsible AI governance, export "
            "automation, and practical product thinking."
        ),
        "what_this_demonstrates": [
            "Ability to design an end-to-end consulting product workflow",
            "Ability to translate AI readiness findings into structured deliverables",
            "Responsible-use thinking embedded in UI, docs, tests, and exports",
            "Practical Python app engineering with broad test coverage",
            "Clear handoff material for demos, screenshots, and portfolio review",
        ],
    }


def generate_case_study_summary() -> dict:
    """Return the BrightPath case-study summary used by portfolio notes."""
    return {
        "case_study_title": "BrightPath Skills Training AI Readiness Report",
        "client_context": (
            "BrightPath Skills Training is a synthetic UK training provider with 24 staff "
            "across delivery, learner support, operations, compliance, and leadership functions."
        ),
        "challenge": (
            "BrightPath has informal AI use, weak governance, limited data boundaries, "
            "and several high-priority risks that must be addressed before AI adoption scales."
        ),
        "solution": (
            "Build 5 converts the synthetic audit findings into readiness interpretation, "
            "risk controls, pilot recommendations, a 30/60/90-day roadmap, and client-ready exports."
        ),
        "outputs_generated": [
            "AI readiness summary",
            "AI risk register",
            "Opportunity and pilot portfolio",
            "30/60/90-day implementation roadmap",
            "Client report Markdown",
            "PDF consulting report",
            "PowerPoint executive deck",
            "Completion review and portfolio notes",
        ],
        "responsible_use_controls": [
            "Synthetic data only",
            "No real learner, HR, safeguarding, client, personal, or regulated data",
            "No external LLM calls",
            "Explicit prototype limitations",
            "Human review required before real-world use",
        ],
        "consulting_value": (
            "The case study shows how a consultant can move from audit findings to a "
            "structured report pack, helping a client prioritise governance, risk controls, "
            "safe pilots, and staff capability building."
        ),
        "limitations": [
            "Synthetic scenario only",
            "Not production deployed",
            "No authentication or persistent storage",
            "No legal, safeguarding, HR, compliance, financial, medical, or professional advice",
            "Requires consultant review before any real-world use",
        ],
    }


def format_completion_review_as_markdown(review: dict) -> str:
    """Format a completion review dict as Markdown."""
    rv = review or {}
    status = rv.get("completion_status") or {}
    outputs = rv.get("output_status") or {}
    docs = rv.get("documentation_status") or {}

    lines = [
        "# Build 5 Completion Review",
        "",
        "## Build Overview",
        "",
        f"**Build:** {rv.get('build_number', 'Build 5')} - {rv.get('build_title', 'AI Consulting Report Generator')}",
        f"**Overall status:** {status.get('overall_status', 'In progress')}",
        f"**Final readiness:** {status.get('final_readiness_label', '')}",
        "",
        "## Phase Completion Checklist",
        "",
        "| Phase | Name | Status | Evidence |",
        "|---|---|---|---|",
    ]
    for item in rv.get("phase_checklist") or []:
        lines.append(
            f"| {item.get('phase', '')} | {item.get('name', '')} | "
            f"{item.get('status', '')} | {item.get('evidence', '')} |"
        )

    lines.extend([
        "",
        "## Output Completion Checklist",
        "",
        f"Output completion: **{outputs.get('completion_percentage', 0)}%** "
        f"({outputs.get('available_count', 0)} of {outputs.get('total_expected', 0)} outputs available)",
        "",
        "| Output | Page | Status |",
        "|---|---|---|",
    ])
    for item in outputs.get("expected_outputs") or []:
        status_text = "Available" if item["key"] in {o["key"] for o in outputs.get("available_outputs", [])} else "Missing"
        lines.append(f"| {item.get('label', '')} | {item.get('page', '')} | {status_text} |")

    lines.extend([
        "",
        "## Documentation Checklist",
        "",
        f"Documentation completion: **{docs.get('documentation_completion_percentage', 0)}%** "
        f"({docs.get('existing_count', 0)} of {docs.get('total_expected', 0)} files available)",
        "",
        "| File | Status |",
        "|---|---|",
    ])
    existing_docs = set(docs.get("existing_files") or [])
    for file_path in docs.get("expected_files") or []:
        lines.append(f"| {file_path} | {'Available' if file_path in existing_docs else 'Missing'} |")

    lines.extend([
        "",
        "## Portfolio Value",
        "",
        rv.get("portfolio_value", ""),
        "",
        "## Commercial Value",
        "",
        rv.get("commercial_value", ""),
        "",
        "## Technical Value",
        "",
        rv.get("technical_value", ""),
        "",
        "## Responsible-Use Position",
        "",
        rv.get("responsible_use_position", ""),
        "",
        "## Recommended Final Actions",
        "",
    ])
    for action in rv.get("recommended_final_actions") or []:
        lines.append(f"- {action}")

    lines.extend([
        "",
        "## Prototype Limitations",
        "",
        rv.get("prototype_note", ""),
        "",
        "## Human Review Requirement",
        "",
        rv.get("human_review_note", ""),
        "",
    ])
    return "\n".join(lines)


def format_portfolio_notes_as_markdown(
    portfolio_summary: dict,
    case_study_summary: dict,
) -> str:
    """Format portfolio and case-study notes as Markdown."""
    ps = portfolio_summary or {}
    cs = case_study_summary or {}

    lines = [
        "# Build 5 Portfolio Notes",
        "",
        "## One-Line Summary",
        "",
        ps.get("one_line_summary", ""),
        "",
        "## Problem Solved",
        "",
        ps.get("problem_solved", ""),
        "",
        "## Target Users",
        "",
    ]
    lines.extend([f"- {item}" for item in ps.get("target_users") or []])
    lines.extend(["", "## Core Workflow", ""])
    lines.extend([f"{i}. {item}" for i, item in enumerate(ps.get("core_workflow") or [], start=1)])
    lines.extend(["", "## Key Features", ""])
    lines.extend([f"- {item}" for item in ps.get("key_features") or []])
    lines.extend(["", "## Technical Stack", ""])
    lines.extend([f"- {item}" for item in ps.get("technical_stack") or []])
    lines.extend(["", "## Responsible AI Features", ""])
    lines.extend([f"- {item}" for item in ps.get("responsible_ai_features") or []])
    lines.extend(["", "## What This Demonstrates", ""])
    lines.extend([f"- {item}" for item in ps.get("what_this_demonstrates") or []])

    lines.extend([
        "",
        "## Case Study: BrightPath Skills Training",
        "",
        f"**Title:** {cs.get('case_study_title', '')}",
        "",
        f"**Client context:** {cs.get('client_context', '')}",
        "",
        f"**Challenge:** {cs.get('challenge', '')}",
        "",
        f"**Solution:** {cs.get('solution', '')}",
        "",
        "**Outputs generated:**",
        "",
    ])
    lines.extend([f"- {item}" for item in cs.get("outputs_generated") or []])

    lines.extend([
        "",
        "## Consulting Value",
        "",
        cs.get("consulting_value", ""),
        "",
        "## Limitations",
        "",
    ])
    lines.extend([f"- {item}" for item in cs.get("limitations") or []])

    lines.extend([
        "",
        "## How To Demo This Build",
        "",
        "1. Load the BrightPath demo audit data.",
        "2. Generate the Readiness Summary, Risk Register, Opportunity Portfolio, Roadmap, and Report Sections.",
        "3. Generate the Client Report.",
        "4. Open Export Centre and generate Markdown, PDF, PPTX, analytics, and chart outputs.",
        "5. Open Completion Review and show phase completion, output completion, documentation status, and portfolio notes.",
        "6. Close by restating the synthetic-data boundary and human-review requirement.",
        "",
    ])
    return "\n".join(lines)
