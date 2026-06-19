"""
Completion Review — AI Governance Policy Checker (Build 6, Phase 8)
BrightPath ChatGPT Mastery Project

Generates a completion review, portfolio summary, and case study summary for Build 6.
All logic is deterministic and template-based. No external AI, LLM, or API calls.
Synthetic/demo data only. Human review required before any real-world use.
"""

import os
from datetime import date


def get_build6_phase_checklist() -> list[dict]:
    return [
        {
            "phase": "Phase 1",
            "name": "Scaffold and synthetic policy data setup",
            "purpose": "Establish the app skeleton, synthetic policy pack, and governance framework data.",
            "status": "Complete",
            "evidence": "src/sample_policies.py, src/governance_framework.py, app.py, Policy Library page, Governance Framework page",
        },
        {
            "phase": "Phase 2",
            "name": "Governance framework coverage checker",
            "purpose": "Compare synthetic policy text against 12 responsible AI governance domains using keyword-based evidence matching.",
            "status": "Complete",
            "evidence": "src/policy_checker.py, Policy Checker page, coverage_results session state, Markdown export",
        },
        {
            "phase": "Phase 3",
            "name": "Policy gap analysis",
            "purpose": "Turn coverage results into prioritised policy gaps with severity levels, risk statements, and action hints.",
            "status": "Complete",
            "evidence": "src/gap_analysis.py, Gap Analysis page, gap_analysis session state, Markdown export",
        },
        {
            "phase": "Phase 4",
            "name": "Policy improvement recommendation engine",
            "purpose": "Convert identified gaps into prioritised recommendations with wording directions, implementation steps, and success criteria.",
            "status": "Complete",
            "evidence": "src/recommendation_engine.py, Recommendations page, policy_recommendations session state, Markdown export",
        },
        {
            "phase": "Phase 5",
            "name": "Governance score and maturity summary",
            "purpose": "Calculate an overall governance maturity level and domain-level maturity scores from coverage, gap, and recommendation data.",
            "status": "Complete",
            "evidence": "src/governance_maturity.py, Governance Maturity page, governance_maturity session state, Markdown export",
        },
        {
            "phase": "Phase 6",
            "name": "Governance report builder",
            "purpose": "Assemble a full client-facing Markdown governance review report from all available Build 6 outputs.",
            "status": "Complete",
            "evidence": "src/report_builder.py, Governance Report page, governance_report_markdown session state, Markdown export",
        },
        {
            "phase": "Phase 7",
            "name": "Export Centre with PDF/charts",
            "purpose": "Generate Markdown and PDF exports with analytics tables and matplotlib chart visualisations.",
            "status": "Complete",
            "evidence": "src/export_centre.py, src/report_analytics.py, src/chart_utils.py, src/pdf_exporter.py, Export Centre page, PDF and Markdown download buttons",
        },
        {
            "phase": "Phase 8",
            "name": "Completion review and portfolio notes",
            "purpose": "Close Build 6 as a portfolio-ready prototype with a completion review, portfolio notes, case study summary, and testing checklist.",
            "status": "Complete",
            "evidence": "src/completion_review.py, Completion Review page, docs/completion-review.md, docs/portfolio-notes.md, docs/testing-checklist.md, docs/case-study-summary.md",
        },
    ]


def get_expected_build6_outputs() -> list[dict]:
    return [
        {"key": "policy_pack", "label": "Synthetic policy pack", "importance": "Required"},
        {"key": "policy_pack_summary", "label": "Policy pack summary", "importance": "Recommended"},
        {"key": "policy_pack_markdown", "label": "Policy pack Markdown", "importance": "Advisory"},
        {"key": "governance_framework", "label": "Responsible AI governance framework", "importance": "Required"},
        {"key": "governance_framework_summary", "label": "Governance framework summary", "importance": "Recommended"},
        {"key": "governance_framework_markdown", "label": "Governance framework Markdown", "importance": "Advisory"},
        {"key": "coverage_results", "label": "Policy coverage results", "importance": "Required"},
        {"key": "coverage_summary", "label": "Coverage summary", "importance": "Recommended"},
        {"key": "coverage_markdown", "label": "Coverage review Markdown", "importance": "Advisory"},
        {"key": "gap_analysis", "label": "Gap analysis", "importance": "Required"},
        {"key": "gap_summary", "label": "Gap analysis summary", "importance": "Recommended"},
        {"key": "gap_analysis_markdown", "label": "Gap analysis Markdown", "importance": "Advisory"},
        {"key": "policy_recommendations", "label": "Policy recommendations", "importance": "Required"},
        {"key": "recommendation_summary", "label": "Recommendation summary", "importance": "Recommended"},
        {"key": "policy_recommendations_markdown", "label": "Recommendations Markdown", "importance": "Advisory"},
        {"key": "governance_maturity", "label": "Governance maturity summary", "importance": "Required"},
        {"key": "governance_maturity_summary", "label": "Maturity summary dict", "importance": "Recommended"},
        {"key": "governance_maturity_markdown", "label": "Maturity summary Markdown", "importance": "Advisory"},
        {"key": "governance_report_data", "label": "Governance report data", "importance": "Required"},
        {"key": "governance_report_summary", "label": "Governance report summary", "importance": "Recommended"},
        {"key": "governance_report_markdown", "label": "Governance report Markdown", "importance": "Required"},
        {"key": "governance_report_filename", "label": "Governance report filename", "importance": "Advisory"},
        {"key": "export_data", "label": "Export data package", "importance": "Recommended"},
        {"key": "export_readiness", "label": "Export readiness check", "importance": "Advisory"},
        {"key": "governance_report_analytics", "label": "Governance analytics", "importance": "Recommended"},
        {"key": "governance_report_chart_paths", "label": "Chart image paths", "importance": "Advisory"},
        {"key": "governance_report_pdf_bytes", "label": "PDF report bytes", "importance": "Recommended"},
        {"key": "governance_report_pdf_filename", "label": "PDF report filename", "importance": "Advisory"},
    ]


def check_session_state_outputs(session_state: dict) -> dict:
    expected = get_expected_build6_outputs()
    available = []
    missing = []

    for item in expected:
        key = item["key"]
        if key in session_state and session_state[key] is not None:
            available.append(item)
        else:
            missing.append(item)

    total = len(expected)
    available_count = len(available)
    completion_pct = round((available_count / total) * 100) if total > 0 else 0

    required_missing = [i for i in missing if i["importance"] == "Required"]

    next_actions = []
    key_steps = [
        ("policy_pack", "Load the BrightPath synthetic policy pack (Policy Library page)."),
        ("governance_framework", "Load the responsible AI governance framework (Governance Framework page)."),
        ("coverage_results", "Run the policy coverage check (Policy Checker page)."),
        ("gap_analysis", "Generate the gap analysis (Gap Analysis page)."),
        ("policy_recommendations", "Generate policy recommendations (Recommendations page)."),
        ("governance_maturity", "Generate the governance maturity summary (Governance Maturity page)."),
        ("governance_report_markdown", "Generate the governance report (Governance Report page)."),
        ("export_data", "Open Export Centre to generate analytics, charts, and export files."),
    ]
    for key, action in key_steps:
        if key not in session_state or session_state[key] is None:
            next_actions.append(action)

    return {
        "available_outputs": available,
        "missing_outputs": missing,
        "available_count": available_count,
        "missing_count": len(missing),
        "total_outputs": total,
        "completion_percentage": completion_pct,
        "required_missing": required_missing,
        "recommended_next_actions": next_actions[:3],
    }


def check_documentation_files(base_path: str = ".") -> dict:
    expected_docs = [
        {"path": "README.md", "label": "Project README"},
        {"path": "docs/build-notes.md", "label": "Build notes"},
        {"path": "docs/architecture.md", "label": "Architecture overview"},
        {"path": "docs/safety-boundaries.md", "label": "Safety boundaries"},
        {"path": "docs/demo-script.md", "label": "Demo script"},
        {"path": "docs/screenshots-checklist.md", "label": "Screenshots checklist"},
        {"path": "docs/future-improvements.md", "label": "Future improvements"},
        {"path": "docs/completion-review.md", "label": "Completion review document"},
        {"path": "docs/portfolio-notes.md", "label": "Portfolio notes"},
        {"path": "docs/testing-checklist.md", "label": "Manual testing checklist"},
        {"path": "docs/case-study-summary.md", "label": "Case study summary"},
    ]

    existing = []
    missing = []

    for doc in expected_docs:
        full_path = os.path.join(base_path, doc["path"])
        if os.path.isfile(full_path):
            existing.append(doc)
        else:
            missing.append(doc)

    total = len(expected_docs)
    existing_count = len(existing)
    pct = round((existing_count / total) * 100) if total > 0 else 0

    return {
        "existing_files": existing,
        "missing_files": missing,
        "existing_count": existing_count,
        "missing_count": len(missing),
        "total_docs": total,
        "documentation_completion_percentage": pct,
    }


def generate_completion_score(
    phase_status: list[dict],
    output_status: dict,
    documentation_status: dict,
) -> dict:
    total_phases = len(phase_status)
    complete_phases = sum(1 for p in phase_status if p.get("status") == "Complete")
    phase_pct = round((complete_phases / total_phases) * 100) if total_phases > 0 else 0

    output_pct = output_status.get("completion_percentage", 0)
    doc_pct = documentation_status.get("documentation_completion_percentage", 0)

    overall_pct = round((phase_pct + output_pct + doc_pct) / 3)

    if overall_pct >= 80:
        overall_status = "Complete"
        readiness_label = (
            "Build 6 is ready for portfolio review and demonstration, "
            "subject to final screenshots and manual export checks."
        )
    elif overall_pct >= 50:
        overall_status = "Mostly complete"
        readiness_label = (
            "Build 6 is mostly complete but should be manually tested across "
            "the full workflow before portfolio presentation."
        )
    else:
        overall_status = "In progress"
        readiness_label = (
            "Build 6 needs further implementation or testing before being "
            "presented as a portfolio asset."
        )

    actions = []
    if output_status.get("recommended_next_actions"):
        actions.extend(output_status["recommended_next_actions"])
    if documentation_status.get("missing_count", 0) > 0:
        missing_docs = [d["label"] for d in documentation_status.get("missing_files", [])]
        if missing_docs:
            actions.append(f"Create missing documentation: {', '.join(missing_docs[:3])}.")
    actions.append("Run pytest to confirm all tests pass.")
    actions.append("Follow the manual testing checklist in docs/testing-checklist.md.")
    actions.append("Capture portfolio screenshots following docs/screenshots-checklist.md.")

    return {
        "overall_status": overall_status,
        "phase_completion_percentage": phase_pct,
        "output_completion_percentage": output_pct,
        "documentation_completion_percentage": doc_pct,
        "overall_completion_percentage": overall_pct,
        "final_readiness_label": readiness_label,
        "recommended_final_actions": actions[:6],
    }


def generate_build6_completion_review(
    session_state: dict,
    base_path: str = ".",
) -> dict:
    phase_checklist = get_build6_phase_checklist()
    output_status = check_session_state_outputs(session_state)
    documentation_status = check_documentation_files(base_path)
    completion_score = generate_completion_score(
        phase_checklist, output_status, documentation_status
    )

    return {
        "build_title": "AI Governance Policy Checker",
        "build_number": "Build 6",
        "generated_date": str(date.today()),
        "completion_status": completion_score,
        "phase_checklist": phase_checklist,
        "output_status": output_status,
        "documentation_status": documentation_status,
        "portfolio_value": (
            "Build 6 demonstrates the ability to turn AI governance concerns into a practical "
            "policy review workflow. Starting from a synthetic policy pack, it systematically "
            "checks coverage against a responsible AI governance framework, identifies gaps, "
            "generates improvement recommendations, calculates governance maturity, assembles "
            "a client-facing report, and exports it as Markdown and PDF. This end-to-end "
            "workflow demonstrates consulting product thinking: structuring an audit input, "
            "applying a governance framework, surfacing actionable findings, and delivering "
            "a polished client artefact."
        ),
        "commercial_value": (
            "This prototype could support AI consulting services including: AI policy reviews "
            "for organisations adopting AI tools; AI governance readiness assessments ahead of "
            "external audits; staff AI-use policy improvement programmes; responsible AI "
            "adoption support for training providers, charities, and SMEs; and governance "
            "gap analysis as a structured starting point for regulatory alignment work. "
            "With appropriate governance controls, data protection measures, and qualified "
            "human review, a production version could be offered as a billable consulting "
            "service or SaaS tool."
        ),
        "technical_value": (
            "Build 6 demonstrates: deterministic keyword-based analysis across 12 governance "
            "domains; multi-step coverage scoring, gap classification, and recommendation "
            "generation; governance maturity calculation with penalty weighting; Markdown "
            "report assembly from session state; reportlab PDF generation with cover page, "
            "analytics tables, and embedded chart images; matplotlib chart generation with "
            "graceful fallback; modular Streamlit multi-page architecture using session state "
            "as a shared data bus; 705+ tests with pytest; and responsible-use boundaries "
            "enforced throughout the codebase and UI."
        ),
        "responsible_use_position": (
            "Build 6 is deliberately synthetic, deterministic, and evidence-based throughout. "
            "It does not use real client policies, learner data, safeguarding information, "
            "HR data, personal data, confidential data, or regulated information. "
            "It does not call external AI, LLM, or third-party services. "
            "It does not claim compliance certification, legal authority, or professional "
            "governance judgement. Every page carries a responsible-use warning. "
            "Human review is required before any real-world use of the outputs."
        ),
        "prototype_note": (
            "This is a portfolio prototype. It is not deployed to production infrastructure, "
            "has no authentication or access controls, uses no persistent storage, "
            "and is not a production-ready compliance or governance system."
        ),
        "human_review_note": (
            "All outputs — coverage results, gap analysis, recommendations, maturity scores, "
            "governance reports, and exports — must be reviewed by a qualified human "
            "before any real-world governance, compliance, or policy decision is made."
        ),
        "recommended_final_actions": completion_score.get("recommended_final_actions", []),
    }


def generate_portfolio_summary() -> dict:
    return {
        "project_name": "AI Governance Policy Checker",
        "one_line_summary": (
            "A Streamlit-based AI governance prototype that reviews synthetic AI policy text "
            "against a responsible AI governance framework, identifies coverage gaps, generates "
            "policy improvement recommendations, calculates maturity, and exports a governance "
            "report."
        ),
        "problem_solved": (
            "After an AI readiness audit, an AI consultant needs to check whether the "
            "organisation's AI policies adequately address responsible AI governance. "
            "This tool demonstrates a structured workflow for converting a synthetic policy pack "
            "into a governance coverage review, gap identification, improvement recommendations, "
            "and a client-facing governance review report."
        ),
        "target_users": [
            "AI consultants reviewing client governance readiness",
            "Small organisations exploring AI adoption and needing policy review support",
            "Training providers and educational organisations with AI usage policies",
            "Compliance and governance teams assessing AI policy coverage",
            "Operational managers responsible for staff AI-use policies",
            "Responsible AI programme leads building governance frameworks",
        ],
        "core_workflow": [
            "Synthetic Policy Pack",
            "Governance Framework",
            "Coverage Review",
            "Gap Analysis",
            "Recommendations",
            "Maturity Summary",
            "Governance Report",
            "Export",
        ],
        "key_features": [
            "Synthetic BrightPath Skills Training policy pack (6 policies, 12 risk areas)",
            "12-domain responsible AI governance framework",
            "Keyword-based coverage checker (deterministic, no LLM)",
            "Policy gap analysis with severity classification",
            "Policy improvement recommendation engine with wording directions",
            "Governance maturity scoring with domain-level breakdown",
            "Markdown governance report builder",
            "PDF export with cover page, analytics tables, and chart images",
            "Matplotlib chart analytics (6 chart types)",
            "Completion review and portfolio notes",
        ],
        "technical_stack": [
            "Python 3 — language",
            "Streamlit — multi-page app framework",
            "st.session_state — shared data bus across pages",
            "reportlab — professional PDF generation",
            "matplotlib — chart visualisation (Agg backend)",
            "pytest — 705+ automated tests",
            "No external AI, LLM, or third-party API calls",
        ],
        "responsible_ai_features": [
            "Synthetic/demo data only — no real client data used",
            "Deterministic keyword-based analysis — no LLM hallucination risk",
            "Responsible-use warning on every page",
            "Human review requirement stated throughout",
            "Safety boundaries document (docs/safety-boundaries.md)",
            "Prototype limitations disclosed in every report and export",
            "No production deployment claim",
            "No compliance certification claim",
        ],
        "portfolio_positioning": (
            "This build demonstrates how AI governance concerns can be turned into a structured "
            "review workflow: synthetic policies are checked against a responsible AI framework, "
            "gaps are identified, recommendations are generated, maturity is scored, and a "
            "governance review report is exported. It is a strong complement to Build 5 "
            "(Consulting Report Generator) and shows how AI consulting moves from readiness "
            "diagnosis to governance assurance."
        ),
        "what_this_demonstrates": [
            "AI governance consulting product thinking",
            "Structured audit input design (policy pack and governance framework)",
            "Deterministic analysis workflow without LLM dependency",
            "Coverage scoring and gap prioritisation logic",
            "Report generation and Markdown/PDF export pipeline",
            "Responsible-use boundary enforcement in a prototype",
            "Modular Streamlit app architecture with session state",
            "End-to-end testing with pytest (705+ tests)",
        ],
    }


def generate_case_study_summary() -> dict:
    return {
        "case_study_title": "BrightPath Skills Training AI Governance Policy Review",
        "client_context": (
            "BrightPath Skills Training is a synthetic small UK training provider using AI tools "
            "informally across their operations. Staff use AI tools for lesson planning, "
            "communication drafting, and administrative tasks, but the organisation does not have "
            "a clear AI governance framework or comprehensive policy coverage. This case study is "
            "entirely synthetic and uses demo data only — BrightPath is not a real organisation."
        ),
        "challenge": (
            "The organisation needed clearer policy guidance around: approved AI tools and their "
            "acceptable use; data boundaries when processing learner and client information; "
            "safeguarding boundaries to prevent AI tools from being used in high-stakes welfare "
            "decisions; human review requirements for AI-generated outputs; escalation procedures "
            "for AI-related incidents; accuracy and hallucination controls; bias and fairness "
            "considerations; staff training and AI capability development; and ongoing monitoring "
            "and continuous improvement of AI governance."
        ),
        "solution": (
            "The AI Governance Policy Checker reviewed BrightPath's synthetic 6-policy pack "
            "against a 12-domain responsible AI governance framework. Coverage gaps were "
            "identified and prioritised, policy improvement recommendations were generated with "
            "wording directions and implementation steps, and a governance maturity score was "
            "calculated. A full governance review report was assembled and exported as Markdown "
            "and PDF, providing the organisation with a structured starting point for policy "
            "improvement — with human review required before any real-world changes."
        ),
        "outputs_generated": [
            "Policy pack overview (6 synthetic policies reviewed)",
            "12-domain governance framework coverage check",
            "Prioritised policy gap analysis with risk statements",
            "Policy improvement recommendations with wording directions",
            "Governance maturity score and domain-level maturity breakdown",
            "Client-facing Markdown governance review report",
            "PDF governance report with cover page, analytics, and charts",
            "Markdown and PDF download exports",
        ],
        "responsible_use_controls": [
            "Synthetic/demo policy text only — no real BrightPath data",
            "Deterministic keyword-based analysis — no LLM or AI API calls",
            "All outputs carry responsible-use disclaimers",
            "Human review required before any policy change",
            "Maturity score is indicative, not a compliance certification",
            "Recommended wording directions are starting points, not approved policy text",
        ],
        "consulting_value": (
            "This prototype demonstrates how an AI consultant could structure a governance policy "
            "review engagement: load the client's policy pack, apply a governance framework, "
            "identify coverage gaps, generate improvement recommendations, score governance "
            "maturity, and deliver a written governance review report. In a real engagement, "
            "the same workflow would apply to actual client policies, with qualified human "
            "review, appropriate governance approvals, and responsible owners throughout."
        ),
        "limitations": [
            "Synthetic/demo data only — not based on real BrightPath policies",
            "Keyword-based analysis — does not understand policy intent or legal adequacy",
            "Coverage scores are indicative, not compliance ratings",
            "Gap analysis does not represent legal or regulatory risk findings",
            "Maturity score is a relative guide, not a certification",
            "Wording directions require qualified review before use",
            "No production deployment — prototype only",
        ],
        "next_step_recommendation": (
            "Before undertaking a real governance policy review engagement, obtain appropriate "
            "governance sign-off, implement data protection controls for real policy handling, "
            "engage qualified legal or governance professionals for review, and confirm "
            "responsible owners and accountability structures with the client."
        ),
    }


def format_completion_review_as_markdown(review: dict) -> str:
    today = review.get("generated_date", str(date.today()))
    status = review.get("completion_status", {})
    phases = review.get("phase_checklist", [])
    outputs = review.get("output_status", {})
    docs = review.get("documentation_status", {})

    lines = [
        "# Build 6 Completion Review",
        "",
        "**AI Governance Policy Checker · BrightPath ChatGPT Mastery Project**",
        "",
        f"*Generated: {today}*",
        "",
        "---",
        "",
        "## Build Overview",
        "",
        f"- **Build:** {review.get('build_number', 'Build 6')}",
        f"- **Title:** {review.get('build_title', 'AI Governance Policy Checker')}",
        f"- **Overall status:** {status.get('overall_status', '—')}",
        f"- **Phase completion:** {status.get('phase_completion_percentage', 0)}%",
        f"- **Output completion:** {status.get('output_completion_percentage', 0)}%",
        f"- **Documentation completion:** {status.get('documentation_completion_percentage', 0)}%",
        "",
        f"**Final readiness:** {status.get('final_readiness_label', '')}",
        "",
        "---",
        "",
        "## Phase Completion Checklist",
        "",
    ]

    for phase in phases:
        mark = "Done" if phase.get("status") == "Complete" else "Pending"
        lines.append(f"### {mark} {phase['phase']}: {phase['name']}")
        lines.append("")
        lines.append(f"**Purpose:** {phase['purpose']}")
        lines.append("")
        lines.append(f"**Status:** {phase['status']}")
        lines.append("")
        lines.append(f"**Evidence:** {phase['evidence']}")
        lines.append("")

    lines += [
        "---",
        "",
        "## Output Completion Checklist",
        "",
        f"**{outputs.get('available_count', 0)}/{outputs.get('total_outputs', 0)} outputs available "
        f"({outputs.get('completion_percentage', 0)}%)**",
        "",
        "**Available outputs:**",
        "",
    ]
    for item in outputs.get("available_outputs", []):
        lines.append(f"- [Done] {item['label']} ({item['importance']})")
    lines.append("")
    lines.append("**Missing outputs:**")
    lines.append("")
    for item in outputs.get("missing_outputs", []):
        lines.append(f"- [Pending] {item['label']} ({item['importance']})")
    lines.append("")

    lines += [
        "---",
        "",
        "## Documentation Checklist",
        "",
        f"**{docs.get('existing_count', 0)}/{docs.get('total_docs', 0)} documentation files present "
        f"({docs.get('documentation_completion_percentage', 0)}%)**",
        "",
        "**Present:**",
        "",
    ]
    for doc in docs.get("existing_files", []):
        lines.append(f"- [Present] {doc['label']} ({doc['path']})")
    lines.append("")
    lines.append("**Missing:**")
    lines.append("")
    for doc in docs.get("missing_files", []):
        lines.append(f"- [Missing] {doc['label']} ({doc['path']})")
    lines.append("")

    lines += [
        "---",
        "",
        "## Portfolio Value",
        "",
        review.get("portfolio_value", ""),
        "",
        "---",
        "",
        "## Commercial Value",
        "",
        review.get("commercial_value", ""),
        "",
        "---",
        "",
        "## Technical Value",
        "",
        review.get("technical_value", ""),
        "",
        "---",
        "",
        "## Responsible-Use Position",
        "",
        review.get("responsible_use_position", ""),
        "",
        "---",
        "",
        "## Recommended Final Actions",
        "",
    ]
    for action in review.get("recommended_final_actions", []):
        lines.append(f"- {action}")
    lines.append("")

    lines += [
        "---",
        "",
        "## Prototype Limitations",
        "",
        review.get("prototype_note", ""),
        "",
        "---",
        "",
        "## Human Review Requirement",
        "",
        review.get("human_review_note", ""),
        "",
        "---",
        "",
        "*Build 6 · AI Governance Policy Checker · BrightPath ChatGPT Mastery Project*",
        "*Synthetic scenarios only. Human review required before any real-world use.*",
        "",
    ]

    return "\n".join(lines)


def format_portfolio_notes_as_markdown(
    portfolio_summary: dict,
    case_study_summary: dict,
) -> str:
    lines = [
        "# Build 6 Portfolio Notes",
        "",
        "**AI Governance Policy Checker · BrightPath ChatGPT Mastery Project**",
        "",
        "---",
        "",
        "## One-Line Summary",
        "",
        portfolio_summary.get("one_line_summary", ""),
        "",
        "---",
        "",
        "## Problem Solved",
        "",
        portfolio_summary.get("problem_solved", ""),
        "",
        "---",
        "",
        "## Target Users",
        "",
    ]
    for user in portfolio_summary.get("target_users", []):
        lines.append(f"- {user}")
    lines.append("")

    lines += [
        "---",
        "",
        "## Core Workflow",
        "",
    ]
    workflow = portfolio_summary.get("core_workflow", [])
    lines.append(" → ".join(workflow))
    lines.append("")

    lines += [
        "---",
        "",
        "## Key Features",
        "",
    ]
    for feature in portfolio_summary.get("key_features", []):
        lines.append(f"- {feature}")
    lines.append("")

    lines += [
        "---",
        "",
        "## Technical Stack",
        "",
    ]
    for tech in portfolio_summary.get("technical_stack", []):
        lines.append(f"- {tech}")
    lines.append("")

    lines += [
        "---",
        "",
        "## Responsible AI Features",
        "",
    ]
    for feature in portfolio_summary.get("responsible_ai_features", []):
        lines.append(f"- {feature}")
    lines.append("")

    lines += [
        "---",
        "",
        "## What This Demonstrates",
        "",
    ]
    for item in portfolio_summary.get("what_this_demonstrates", []):
        lines.append(f"- {item}")
    lines.append("")

    cs = case_study_summary
    lines += [
        "---",
        "",
        f"## Case Study: {cs.get('case_study_title', 'BrightPath Skills Training')}",
        "",
        "### Client Context",
        "",
        cs.get("client_context", ""),
        "",
        "### Challenge",
        "",
        cs.get("challenge", ""),
        "",
        "### Solution",
        "",
        cs.get("solution", ""),
        "",
        "### Outputs Generated",
        "",
    ]
    for output in cs.get("outputs_generated", []):
        lines.append(f"- {output}")
    lines.append("")

    lines += [
        "### Consulting Value",
        "",
        cs.get("consulting_value", ""),
        "",
        "---",
        "",
        "## Portfolio Positioning",
        "",
        portfolio_summary.get("portfolio_positioning", ""),
        "",
        "---",
        "",
        "## Limitations",
        "",
    ]
    for limitation in cs.get("limitations", []):
        lines.append(f"- {limitation}")
    lines.append("")

    lines += [
        "---",
        "",
        "## How To Demo This Build",
        "",
        "```bash",
        "cd 10-builds/ai-governance-policy-checker",
        "source .venv/bin/activate",
        "streamlit run app.py",
        "```",
        "",
        "Open at `http://localhost:8501` and follow the demo script in `docs/demo-script.md`.",
        "",
        "---",
        "",
        "## Suggested LinkedIn / GitHub Description",
        "",
        "Built an AI Governance Policy Checker that reviews synthetic organisational AI policy "
        "text against a responsible AI governance framework. The prototype identifies coverage gaps, "
        "generates policy improvement recommendations, calculates governance maturity, and exports "
        "a client-facing governance report with PDF and chart support. It uses deterministic logic, "
        "synthetic data only, and clear responsible-use boundaries.",
        "",
        "**Skills demonstrated:** AI governance consulting, Streamlit app development, "
        "deterministic NLP analysis, PDF generation (reportlab), data visualisation (matplotlib), "
        "responsible AI design, software testing (pytest).",
        "",
        "---",
        "",
        "*Build 6 · AI Governance Policy Checker · BrightPath ChatGPT Mastery Project*",
        "*Synthetic scenarios only. Human review required before any real-world use.*",
        "",
    ]

    return "\n".join(lines)
