# Architecture — AI Governance Policy Checker

**Build 6 · BrightPath ChatGPT Mastery Project**

---

## Overview

The AI Governance Policy Checker is a Streamlit multi-page application. Phases 1–8 provide synthetic policy data, a responsible AI governance framework, a functional policy coverage checker, policy gap analysis, a policy improvement recommendation engine, a governance maturity summary, a governance report builder, an Export Centre with Markdown/PDF export, analytics, and charts, and a Completion Review with portfolio notes.

---

## App Layer

`app.py` — Streamlit entry point. Manages:

- Page navigation via `st.sidebar.radio`
- Session state as the shared data bus
- Page rendering for all 10 pages: Home, Policy Library, Governance Framework, Policy Checker, Gap Analysis, Recommendations, Governance Maturity, Governance Report, Export Centre, and Completion Review (all functional as of Phase 8)

Navigation order follows the governance review workflow:

```
Home → Policy Library → Governance Framework → Policy Checker
→ Gap Analysis → Recommendations → Governance Report → Export Centre → Completion Review
```

---

## Synthetic Policy Data Layer

`src/sample_policies.py` — Provides the BrightPath synthetic policy pack:

- `get_brightpath_policy_pack()` — full policy pack dictionary
- `get_demo_policy_list()` — list of 6 synthetic policy documents
- Individual policy getters for each of the 6 policies
- `get_default_policy_types()` — reference list of policy types
- `get_default_risk_areas()` — reference list of risk areas

All policy content is synthetic and created for portfolio demonstration only.

---

## Governance Framework Layer

`src/governance_framework.py` — Provides the responsible AI governance framework:

- `get_responsible_ai_governance_framework()` — 12 governance domains
- `get_framework_domain_ids()` and `get_framework_domain_names()` — domain lookups
- `get_high_priority_domains()` — filters to High priority domains
- `summarise_governance_framework()` — summary statistics
- `format_governance_framework_as_markdown()` — Markdown export

Framework domains cover: Strategy and Ownership, Approved AI Tools, Prohibited AI Uses, Data Protection and Confidentiality, Learner and Client Data Boundaries, Safeguarding Boundaries, Human Review and Accountability, Accuracy and Hallucination Control, Bias/Fairness/Inclusion, Staff Training and Capability, Escalation and Incident Reporting, Monitoring/Review/Continuous Improvement.

---

## Policy Data Manager Layer

`src/policy_data_manager.py` — Policy pack utilities:

- `validate_policy_pack()` — checks required fields and structure
- `summarise_policy_pack()` — extracts statistics and metadata
- `format_policy_pack_as_markdown()` — Markdown export with responsible-use boundaries
- `get_policy_by_id()` — lookup by policy ID
- `search_policies_by_risk_area()` — filter policies by risk area keyword
- `extract_policy_titles()` — list of policy titles

---

## Policy Checker Layer (Phase 2)

`src/policy_checker.py` — Performs deterministic keyword-based coverage checking:

- `normalise_text()` — lowercases and cleans input text for consistent matching
- `count_keyword_matches()` — counts total keyword occurrences across policy text
- `extract_matching_policy_snippets()` — extracts lines containing keyword matches as evidence snippets
- `get_domain_keyword_map()` — maps each of the 12 governance domain names to a keyword list
- `check_domain_coverage()` — checks one domain across all policies; returns score, level, matched policies, keywords, and snippets
- `check_policy_pack_coverage()` — runs coverage check across all 12 domains; returns full results dict
- `calculate_coverage_score()` — averages domain scores into an overall score
- `classify_coverage_level()` — maps score to Not covered / Weak / Partial / Strong coverage
- `summarise_policy_coverage()` — extracts summary stats, gaps, best/weakest domains, focus areas
- `format_policy_coverage_as_markdown()` — produces a full Markdown coverage review report

**It does not use LLMs, embeddings, semantic search, or external APIs.** All matching is deterministic substring search. Coverage results are stored in session state for later gap analysis and reporting.

---

## Gap Analysis Layer (Phase 3)

`src/gap_analysis.py` — Reads coverage results from the Policy Checker and identifies governance gaps based on coverage level and domain priority.

- `classify_gap_severity()` — maps coverage level + priority to Critical / High / Medium / Low / No significant gap
- `calculate_gap_priority_score()` — integer urgency score 0–100 weighting gap size and domain priority
- `generate_domain_gap()` — builds a structured gap dict with severity, type, risk statement, missing evidence, and action hint
- `generate_policy_gap_analysis()` — runs gap analysis across all domains; separates gaps by severity; builds covered_domains list
- `summarise_gap_analysis()` — summary stats, overall gap position statement, top gap domains, recommended focus
- `prioritise_gaps()` — sorts gaps by priority score descending
- `format_gap_analysis_as_markdown()` — full Markdown gap analysis report

The output is stored in session state (`gap_analysis`, `gap_summary`, `gap_analysis_markdown`) for use in later recommendation and reporting phases. No external AI calls are used.

---

## Recommendation Engine Layer (Phase 4)

`src/recommendation_engine.py` — Reads gap analysis outputs and generates deterministic policy improvement recommendations.

- `classify_recommendation_priority()` — maps gap severity + priority score to Urgent / High / Medium / Low
- `suggest_policy_action_type()` — determines Create / Strengthen / Add checklist / Add escalation / Review action
- `suggest_policy_owner()` — domain-matched suggested responsible owner role
- `suggest_target_policy()` — suggests which policy to update; matches against available policy pack titles
- `generate_policy_wording_direction()` — domain-matched suggested wording direction (indicative, not approved text)
- `generate_implementation_steps()` — 4–7 practical steps per recommendation
- `generate_review_questions()` and `generate_success_criteria()` — domain-tailored checklists
- `generate_policy_recommendations()` — full package: priority groups, quick wins, themes, owner summary, recommended sequence
- `summarise_policy_recommendations()` — summary stats, position statement, top themes, top owners, recommended focus
- `prioritise_recommendations()` — sorts by priority then score descending
- `format_policy_recommendations_as_markdown()` — full Markdown report

Outputs are stored in session state (`policy_recommendations`, `recommendation_summary`, `policy_recommendations_markdown`) for use in governance report generation. No external AI calls are used.

---

## Governance Maturity Layer (Phase 5)

`src/governance_maturity.py` — Reads policy coverage results and optionally gap analysis and
recommendation outputs to calculate a governance maturity picture.

- `classify_governance_maturity_level()` — maps a 0–100 score to Initial / Developing / Defined / Managed / Optimised
- `calculate_domain_maturity_score()` — starts from coverage_score, applies gap penalties (-3 to -25), recommendation penalties (-2 to -15), and an extra -10 for High-priority domains below 50
- `calculate_overall_governance_score()` — weighted average (High 1.5×, Medium 1.0×, Low 0.75×)
- `identify_maturity_strengths()` / `identify_maturity_weaknesses()` — domain lists above/below thresholds
- `identify_maturity_blockers()` — surfaces critical/high gaps and urgent/high-priority recommendations as blockers
- `generate_maturity_improvement_priorities()` — derives ordered action list from blockers and weaknesses
- `generate_adoption_readiness_position()` — practical consulting guidance on AI adoption readiness
- `generate_governance_maturity_summary()` — full package including all of the above
- `summarise_governance_maturity()` — compact stats dict for UI display
- `format_governance_maturity_as_markdown()` — full Markdown report

The maturity summary is stored in session state (`governance_maturity`, `governance_maturity_summary`,
`governance_maturity_markdown`) for use in governance report generation. No external AI calls are used.

---

## Governance Report Builder Layer (Phase 6)

`src/report_builder.py` — Reads all generated Build 6 outputs from session state and assembles
a complete client-facing governance report.

- `check_governance_report_readiness()` — inspects session state for available and missing outputs
- `build_governance_report_data_from_session_state()` — builds a full report data dict; missing outputs stored as None
- Per-section generators for: Cover, TOC, Executive Summary, Policy Pack, Framework, Coverage, Gap Analysis, Recommendations, Maturity, Next Steps, Responsible Use, Prototype Limitations, Appendices
- `generate_markdown_governance_report()` — assembles the full Markdown report; respects user-selected include_sections
- `summarise_governance_report()` — compact stats dict including readiness position
- `create_governance_report_filename()` — safe snake-case `.md` filename

The report can be generated as a complete or partial draft depending on available sections.
Generated Markdown is stored in session state (`governance_report_markdown`, `governance_report_data`,
`governance_report_filename`, `governance_report_readiness`, `governance_report_summary`) for the
Export Centre. No external AI calls are used.

---

## UI and Utilities

`src/ui_components.py` — Reusable Streamlit UI helpers: page headers, responsible-use warnings, prototype notices, metric rows, completion badges, workflow steps display.

`src/utils.py` — General utilities: safe dict access, text cleaning, filename generation, date label.

---

## Session State

| Key | Set by | Content |
|---|---|---|
| `policy_pack` | Policy Library | Full synthetic policy pack dict |
| `policy_pack_summary` | Policy Library | Summary statistics dict |
| `policy_pack_markdown` | Policy Library | Markdown string of policy pack |
| `governance_framework` | Governance Framework | List of governance domain dicts |
| `governance_framework_summary` | Governance Framework | Summary statistics dict |
| `governance_framework_markdown` | Governance Framework | Markdown string of framework |

Phase 2 adds: `coverage_results`, `coverage_summary`, `coverage_markdown`.
Phase 3 adds: `gap_analysis`, `gap_summary`, `gap_analysis_markdown`.
Phase 4 adds: `policy_recommendations`, `recommendation_summary`, `policy_recommendations_markdown`.
Phase 5 adds: `governance_maturity`, `governance_maturity_summary`, `governance_maturity_markdown`.
Phase 6 adds: `governance_report_data`, `governance_report_markdown`, `governance_report_filename`, `governance_report_readiness`, `governance_report_summary`.
Phase 7 adds: `export_data`, `export_readiness`, `governance_report_analytics`, `governance_report_chart_paths`, `governance_report_pdf_bytes`, `governance_report_pdf_filename`.
Phase 8 adds: `completion_review`, `completion_review_markdown`, `portfolio_notes`, `portfolio_notes_markdown`.

---

## Tests

`tests/test_sample_policies.py` — Tests for the synthetic policy pack and individual policy getters.

`tests/test_governance_framework.py` — Tests for the governance framework functions.

`tests/test_policy_data_manager.py` — Tests for policy data manager functions including validation, summarisation, Markdown export, lookup, and search.

---

`tests/test_policy_checker.py` — Tests for policy coverage checking functions.

`tests/test_gap_analysis.py` — Tests for gap analysis functions.

`tests/test_recommendation_engine.py` — Tests for recommendation engine functions.

`tests/test_governance_maturity.py` — Tests for governance maturity functions including scoring, penalty logic, blocker identification, improvement priorities, adoption readiness, and Markdown export.

`tests/test_report_builder.py` — Tests for the governance report builder including readiness checks, section generators, full report assembly, section exclusion, summary, and filename generation.

`tests/test_export_centre.py` — Tests for export readiness checks, export data building, quality checklist, package summary, filename generation, and export preparation.

`tests/test_report_analytics.py` — Tests for all analytics functions: completion status, coverage levels, gap severities, recommendation priorities, maturity levels, governance score breakdown, report quality summary, and full analytics assembly.

`tests/test_chart_utils.py` — Tests for all chart generation functions including graceful failure on empty data and missing files.

`tests/test_pdf_exporter.py` — Tests for filename generation, text formatting, style building, and PDF export bytes including minimal data and missing analytics/chart paths.

`tests/test_completion_review.py` — Tests for all completion review functions: phase checklist, expected outputs, session state checking, documentation file checking, completion scoring, full review generation, portfolio summary, case study summary, and Markdown formatting.

---

## Completion Review Layer (Phase 8)

`src/completion_review.py` — Generates the Build 6 completion review, portfolio summary, and case study:

- `get_build6_phase_checklist()` — all 8 phases with name, purpose, status, and evidence
- `get_expected_build6_outputs()` — 28 expected session state outputs (Required / Recommended / Advisory)
- `check_session_state_outputs()` — inspects session state; returns available, missing, completion percentage, and recommended next actions
- `check_documentation_files()` — checks 11 documentation files; returns existing, missing, and completion percentage
- `generate_completion_score()` — overall status (Complete / Mostly complete / In progress), final readiness label, recommended final actions
- `generate_build6_completion_review()` — full completion review dict with portfolio value, commercial value, technical value, responsible-use position
- `generate_portfolio_summary()` — one-line summary, problem, target users, core workflow, key features, stack, responsible AI features, positioning
- `generate_case_study_summary()` — BrightPath case study with client context, challenge, solution, outputs, consulting value, limitations
- `format_completion_review_as_markdown()` — full Markdown completion review with 12 sections
- `format_portfolio_notes_as_markdown()` — portfolio notes Markdown with case study, LinkedIn/GitHub description, demo instructions

The Completion Review page in `app.py` generates the review automatically and works even if no previous outputs are available. Results are stored in session state for Markdown download.

---

## Export Centre Layer (Phase 7)

`src/export_centre.py` — Prepares export packages from all available Build 6 outputs:

- `check_export_readiness()` — inspects session state and returns readiness status with `can_export_markdown` and `can_export_pdf`
- `build_export_data_from_session_state()` — assembles all available outputs into a single export data dict
- `generate_export_quality_checklist()` — 12-item quality checklist (Required / Recommended / Advisory)
- `summarise_export_package()` — summary statistics for display
- `create_export_filename_base()` — safe, date-stamped filename base
- `prepare_markdown_export()` — returns `(text, filename)` for Markdown download
- `prepare_pdf_export()` — returns `(bytes, filename)` for PDF download
- `prepare_all_exports()` — both formats with per-format error capture

`src/report_analytics.py` — Generates deterministic analytics from generated outputs:

- `build_governance_report_analytics()` — assembles all analytics into one dict
- Sub-functions cover: export completion status, coverage level distribution, gap severity distribution, recommendation priority distribution, maturity level distribution, governance score breakdown, report quality summary

`src/chart_utils.py` — Generates matplotlib charts for the Export Centre:

- Six chart functions: completion status, coverage levels, gap severities, recommendation priorities, maturity levels, governance scores by domain
- `generate_all_export_charts()` — generates all charts into `outputs/charts/`; each chart fails gracefully if data is missing or generation errors occur
- Uses `Agg` backend (non-interactive); no seaborn; navy/teal/amber professional palette

`src/pdf_exporter.py` — Exports the governance report as a professional PDF using reportlab:

- `export_governance_report_to_pdf_bytes()` — full PDF with cover page, analytics tables, chart images, Markdown report content, and responsible-use section
- Markdown content parsed line-by-line: headings, bullets, numbered lists, blockquotes, tables → reportlab `Table` objects
- Handles missing analytics, missing chart paths, partial Markdown, and empty export data
- Navy headings, teal rule lines, alternating grey table rows

---

## No External AI API (All Phases)

All phases are deterministic and template-based throughout. No external LLM or AI API calls are made across any phase. No OpenAI, Claude, LangChain, LlamaIndex, vector databases, or similar services are used.

---

*Build 6 · AI Governance Policy Checker · BrightPath ChatGPT Mastery Project*
