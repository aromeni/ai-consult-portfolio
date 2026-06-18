# Architecture — AI Consulting Report Generator

**Build 5 · BrightPath ChatGPT Mastery Project**

---

## Overview

Build 5 is a locally-run, multi-page Streamlit application. It follows the same responsible-use and prototype principles as Builds 1–4: deterministic logic, synthetic data, no external AI API calls, and human review required for all outputs.

---

## Layer Overview

```
App Layer (Streamlit)
  app.py — multi-page navigation, session state management

Synthetic Audit Data Layer
  src/sample_data.py        — BrightPath demo audit data and helper functions

Audit Data Management Layer
  src/audit_data_manager.py — validation, summarisation, formatting, form integration

Readiness Scoring Layer
  src/scoring_summary.py    — score averaging, readiness classification, summary generation

Report Section Generation Layer (Phase 1: placeholders)
  src/report_sections.py    — deterministic placeholder section generators

Risk Register Layer (scaffold)
  src/risk_register.py      — risk sorting and Markdown table

Opportunity and Pilot Recommendation Layer (Phase 4)
  src/opportunity_generator.py — opportunity scoring, pilot sequencing, success measures, responsible-use controls

Roadmap Generation Layer (Phase 5)
  src/roadmap_generator.py  — staged 30/60/90-day roadmap with adaptive actions, owners, and responsible-use controls

Report Assembly Layer (scaffold)
  src/report_builder.py     — full report assembly (Phase 3)

Export Layer (scaffold)
  src/pdf_exporter.py       — basic reportlab PDF helper (Phase 3 full implementation)

UI Helpers
  src/ui_components.py      — reusable Streamlit presentation components

Utilities
  src/utils.py              — slugify, filename generation, text truncation, sort keys

Tests
  tests/                    — pytest suite for all src modules

Outputs
  outputs/reports/          — saved Markdown/PDF reports
  outputs/charts/           — chart images (Phase 2+)
```

---

## Session State

`st.session_state` carries audit data and derived summaries across pages:

| Key | Type | Set by |
|---|---|---|
| `audit_data` | dict | Audit Data page (on load) |
| `audit_summary` | dict | Audit Data page (on load) |
| `readiness_summary` | dict | Audit Data page (on load) |

Phase 3 adds: `risk_register`, `risk_register_summary`, `risk_register_markdown`.
Phase 4 adds: `opportunity_portfolio`, `opportunity_summary`, `opportunity_portfolio_markdown`.
Phase 5 adds: `implementation_roadmap`, `implementation_roadmap_summary`, `implementation_roadmap_markdown`.
Phase 6 adds: `report_sections`, `report_sections_summary`, `report_sections_markdown`.
Phase 7 adds: `client_report_data`, `client_report_markdown`, `client_report_filename`, `client_report_readiness`.
Phase 8 adds: `export_data`, `export_readiness`, `client_report_analytics`, `client_report_chart_paths`, `client_report_pdf_bytes`, `client_report_pdf_filename`, `client_report_pptx_bytes`, `client_report_pptx_filename`.
Phase 9 adds: `completion_review`, `completion_review_markdown`, `portfolio_notes`, `portfolio_notes_markdown`.

---

## Synthetic Audit Data Layer

`src/sample_data.py` — Phase 1.

`get_brightpath_audit_data()` returns a fully structured synthetic audit dict representing outputs from a Build 1-style AI readiness assessment. It includes organisation profile, six-dimension readiness scores, workflow findings, risk findings, pilot recommendations, training needs, and governance gaps.

All data is fictional. The BrightPath scenario (a small UK training provider) is used consistently across Builds 1–5 in the ChatGPT Mastery portfolio.

---

## Audit Data Management Layer

`src/audit_data_manager.py` — Phase 1.

- `validate_audit_data()` checks that required fields are present, have correct types, and pass simple constraints (positive staff count, non-empty name, etc.)
- `summarise_audit_data()` returns an aggregated summary dict: counts of workflows, risks, pilots, training needs, governance gaps; critical and high risk counts; high-priority training count
- `format_audit_data_as_markdown()` converts the full audit dict to a Markdown document for preview and export
- `create_audit_data_from_form_data()` builds a minimal audit dict from UI form inputs, using demo workflow/risk/pilot data as defaults in Phase 1

---

## Readiness Summary Layer

`src/scoring_summary.py` — Phase 2.

The Readiness Summary page reads synthetic audit readiness scores from `st.session_state["audit_data"]` and passes them to `generate_readiness_summary()`.

The scoring layer classifies AI readiness and generates a full client-facing interpretation without external AI calls through five mechanisms:

1. **Band classification** — `classify_readiness_level()` maps 0–39 → Low, 40–59 → Developing, 60–79 → Moderate, 80–100 → Strong
2. **Category interpretation** — `generate_category_interpretation()` returns band-specific consulting narrative from a lookup table keyed to category and score range
3. **Strength/gap identification** — `identify_readiness_strengths()` and `identify_readiness_gaps()` compare each category against configurable thresholds and return risk and recommended-action text from lookup tables
4. **Strategic interpretation** — `_build_strategic_interpretation()` builds a short deterministic narrative from the organisation's overall level, top strength, and top gap
5. **Recommendations** — `generate_readiness_recommendations()` produces practical actions by checking which gap categories are present and whether workflow opportunity is a strength

The output is stored in `st.session_state["readiness_summary"]` and `st.session_state["readiness_summary_markdown"]` for use in later client report generation.

All content is deterministic and template-based — no external AI calls.

---

## Risk Register Layer

`src/risk_register.py` — Phase 3.

The Risk Register page reads synthetic audit risk findings from `st.session_state["audit_data"]` and passes them to `generate_risk_register()`.

The risk register layer builds a structured client-facing register through four deterministic mechanisms:

1. **Score normalisation** — `normalise_risk_score()` converts string labels (Very low/Low/Medium/High/Very high/Critical) or numeric values to a 1–5 integer; defaults to 3 (Medium) for missing or invalid inputs
2. **Risk scoring** — `calculate_risk_score()` multiplies likelihood and impact scores to produce a 1–25 risk score; `classify_risk_level()` maps that score to Low (1–4), Medium (5–9), High (10–16), or Critical (17–25)
3. **Control and owner lookup** — `generate_risk_control_recommendation()` and `generate_risk_owner_suggestion()` use category-keyed lookup tables to return deterministic recommended controls and suggested owners for each risk
4. **Priority and review** — priority actions and review frequencies are determined from the risk level and appended to each register item

The output is stored in `st.session_state["risk_register"]`, `st.session_state["risk_register_summary"]`, and `st.session_state["risk_register_markdown"]` for later use in client report generation.

All content is deterministic and template-based — no external AI calls.

---

## Opportunity and Pilot Recommendation Layer

`src/opportunity_generator.py` — Phase 4.

The Opportunity and Pilot Recommendations page reads synthetic workflow findings and pilot recommendations from `st.session_state["audit_data"]` and passes them to `generate_ai_opportunity_portfolio()`.

The opportunity layer builds a client-facing portfolio through four deterministic mechanisms:

1. **Score normalisation** — `normalise_priority_value()` converts string labels (Very low/Low/Medium/High/Very high) or numeric values to a 1–5 integer; strips descriptive text after em-dashes; defaults to 3 (Medium) for missing or invalid inputs
2. **Opportunity scoring** — `calculate_opportunity_score()` applies `value*2 - complexity - risk + 10` (clamped 0–20); `classify_opportunity_priority()` maps that score to Low priority (0–6), Medium priority (7–12), High priority (13–16), or Strategic priority (17–20)
3. **Pilot sequencing** — `prioritise_pilots()` sorts pilots by combined complexity + risk ascending, placing the safest and simplest pilot first as the recommended starting point
4. **Controls and success measures** — `generate_responsible_pilot_controls()` and `generate_pilot_success_measures()` return deterministic controls and measures keyed to pilot name; standard controls are supplemented with pilot-specific extras for learner data, quality/compliance, and safeguarding contexts

The output is stored in `st.session_state["opportunity_portfolio"]`, `st.session_state["opportunity_summary"]`, and `st.session_state["opportunity_portfolio_markdown"]` for later use in client report generation.

All content is deterministic and template-based — no external AI calls.

---

## Readiness Scoring Layer

`src/scoring_summary.py` — Phase 1 (extended in Phase 2).

The scoring layer classifies AI readiness into four bands:

| Score Range | Band |
|---|---|
| 0–39 | Low readiness |
| 40–59 | Developing readiness |
| 60–79 | Moderate readiness |
| 80–100 | Strong readiness |

`generate_readiness_summary()` returns the overall band, per-category scores and bands, the strongest and weakest category, a plain-English interpretation, and a list of the three lowest-scoring immediate priorities.

---

## Roadmap Generator Layer

`src/roadmap_generator.py` — Phase 5.

The Roadmap page reads synthetic audit data and optionally the readiness summary, risk register, and opportunity portfolio from `st.session_state`, then passes them to `generate_implementation_roadmap()`.

The roadmap layer builds a staged 30/60/90-day implementation plan through three mechanisms:

1. **Phase action generation** — `generate_foundation_actions()`, `generate_pilot_preparation_actions()`, `generate_pilot_delivery_actions()`, and `generate_review_and_scale_actions()` each return deterministic action lists for their phase; Day 60 actions are combined and renumbered sequentially so IDs are unique
2. **Adaptive actions** — foundation actions detect critical governance gaps in the audit data (e.g. No AI Use Policy) and add targeted actions; both foundation and review phases detect high/critical risks from `risk_summary` and add risk-specific actions
3. **Overall position derivation** — `_derive_roadmap_position()` derives a client-facing roadmap position statement from readiness level and risk counts; if high/critical risks exist, governance and data controls are prioritised before scaling

The roadmap also includes deterministic cross-cutting controls, success measures, dependencies, and risks-to-manage — all template-based with no external AI calls.

The output is stored in `st.session_state["implementation_roadmap"]`, `st.session_state["implementation_roadmap_summary"]`, and `st.session_state["implementation_roadmap_markdown"]` for later use in client report generation.

---

## Client Report Builder Layer

`src/report_builder.py` — Phase 7.

The Client Report page reads all generated Build 5 outputs from session state, then calls `build_client_report_data_from_session_state()` and `generate_markdown_client_report()` to assemble a complete client-facing consulting report.

The client report builder works through three mechanisms:

1. **Readiness check** — `check_client_report_readiness()` inspects session state for available outputs, identifies missing sections, and returns recommended next steps. If only audit data is available, the page generates a partial report with graceful "not yet generated" messages rather than crashing.
2. **Section assembly** — thirteen section generators (`generate_report_cover_section()`, `generate_report_executive_summary_section()`, etc.) each pull from report_sections data when available, falling back to direct audit data parsing when enrichment outputs are missing. `generate_markdown_client_report()` assembles them into a single ordered Markdown document.
3. **Section selection** — `include_sections` dict allows the user to choose which optional sections to include; required sections (executive summary, organisation context, responsible-use boundaries, prototype limitations) are always included.

Generated Markdown is stored in `st.session_state["client_report_markdown"]` for later use in the Export Centre.

No external AI calls are used in any section generator.

---

## Report Section Generator Layer

`src/report_sections.py` — Phase 6.

The Report Sections page reads synthetic audit data and all optional generated analysis outputs from `st.session_state`, then passes them to `generate_all_report_sections()`.

The report section layer generates eleven polished client-facing consulting sections through three mechanisms:

1. **Section generation** — each of the eleven section functions (`generate_executive_summary()`, `generate_organisation_context_section()`, `generate_readiness_interpretation_section()`, etc.) returns a structured dict containing `section_id`, `section_title`, `section_purpose`, `content`, `key_points`, `recommendations`, `source_outputs_used`, and `review_note`
2. **Graceful degradation** — sections that depend on enrichment outputs (readiness summary, risk register, opportunity portfolio, implementation roadmap) display an appropriate "not yet generated" message when the data is absent, so the page always renders without crashing
3. **Source output tracking** — each section records which outputs it drew from; `summarise_report_sections()` aggregates these across all sections and identifies which source outputs are still missing

The generated sections are stored in `st.session_state["report_sections"]`, `st.session_state["report_sections_summary"]`, and `st.session_state["report_sections_markdown"]` for later use in the Client Report Builder.

Phase 1 placeholder functions (`generate_executive_summary_placeholder()` etc.) are retained for backward compatibility.

---

## Export Centre Layer

`src/export_centre.py` — Phase 8.

The Export Centre page coordinates all export operations from a single entry point. It checks readiness, builds export data, generates analytics and charts, then prepares Markdown, PDF, and PPTX outputs.

**Export Centre (`src/export_centre.py`)** — Phase 8.

Provides: `check_export_readiness()`, `build_export_data_from_session_state()`, `generate_export_quality_checklist()`, `summarise_export_package()`, `prepare_markdown_export()`, `prepare_pdf_export()`, `prepare_pptx_export()`, and `prepare_all_exports()`.

**Report Analytics (`src/report_analytics.py`)** — Phase 8.

Deterministic analytics from Build 5 outputs only. Provides completion status, readiness score breakdown, risk level counts, opportunity priority counts, roadmap action counts, and report quality summary. No external data or AI calls.

**Chart Utilities (`src/chart_utils.py`)** — Phase 8.

matplotlib bar charts with Agg backend (no display context needed — server-safe). All chart functions return the file path on success or `""` on failure. Chart PNG files are written to `outputs/charts/`.

**PDF Exporter (`src/pdf_exporter.py`)** — Phase 1 scaffold; full rewrite in Phase 8.

`export_client_report_to_pdf_bytes()` builds a professional reportlab PDF: navy cover page, analytics section, embedded matplotlib charts, full Markdown client report converted line-by-line to styled reportlab paragraphs, responsible-use section, and prototype limitations. Returns `b""` on any failure.

`create_pdf_placeholder()` retained for backward compatibility.

**PPTX Exporter (`src/pptx_exporter.py`)** — Phase 8.

python-pptx 15-slide executive deck. All slides use blank layout with manual shape placement (rectangles for title bars, textboxes for content) for full control and portability. `export_client_report_to_pptx_bytes()` returns ZIP-format PPTX bytes (`b"PK..."`) or `b""` on failure. Slide 14 uses an amber title bar to signal responsible-use importance.

---

## Completion Review Layer

`src/completion_review.py` — Phase 9.

The Completion Review layer closes Build 5 as a portfolio-ready prototype. It does not add a new product workflow; it reviews the outputs and documentation already produced by earlier phases.

It provides deterministic helpers for:

- Checking the completed phase checklist
- Checking expected session-state outputs
- Checking expected documentation files
- Generating a completion score
- Generating portfolio notes
- Generating the BrightPath case-study summary
- Formatting completion review and portfolio notes as Markdown

The Completion Review page summarises final build status in Streamlit. It shows phase completion, session-output completion, documentation completion, portfolio value, commercial value, technical value, responsible-use position, recommended final actions, Markdown previews, and two Markdown downloads.

No external AI calls are used. The layer only reads local code/docs state and `st.session_state`.

---

## Generation Approach

All content is **deterministic and template-based** — no external LLM APIs in any phase.

- Phase 1: audit data loaded from synthetic dict; scores classified by fixed bands
- Phase 2: report sections generated from template libraries keyed to audit findings
- Phase 3–7: sections assembled into full client report; PDF generated from Markdown
- Phase 8: analytics calculated from generated outputs; charts rendered by matplotlib; PDF/PPTX assembled by reportlab/python-pptx
- Phase 9: completion review generated from local phase metadata, session-state outputs, and documentation file checks

This approach is consistent with Builds 1–4 and mirrors Build 3's deterministic RAG philosophy: honest about what the system knows, no hallucination risk, human review required for all outputs.

---

## External AI API Usage

**None in Phase 1 or any planned phase of Build 5.**

Optional future extension: Ollama-assisted report drafting with strict evidence grounding (noted in `docs/future-improvements.md`). Disabled by default.

---

## No Database, No Authentication

Single-session local prototype. All state lives in `st.session_state` and is lost on app restart. No database, no authentication, no cloud storage.

---

*Build 5 · AI Consulting Report Generator · BrightPath ChatGPT Mastery Project*
