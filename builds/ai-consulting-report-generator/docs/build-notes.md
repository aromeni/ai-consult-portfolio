# Build Notes — AI Consulting Report Generator

**Build 5 · BrightPath ChatGPT Mastery Project**

---

## Phase 1: Scaffold and Sample Audit Data Setup

### What was created

**App scaffold (`app.py`)**

Multi-page Streamlit app with eight pages:
- Home — project intro, consulting workflow, Build 1–4 connections, responsible-use warning, prototype notice
- Audit Data — load BrightPath demo audit, display summary metrics, readiness scores, workflow findings, risk findings, pilot recommendations, training needs, governance gaps, Markdown preview
- Readiness Summary — score interpretation, category breakdown, immediate priorities, Markdown preview
- Report Sections, Risk Register, Roadmap, Client Report, Export Centre — clean placeholders explaining what each page will deliver in later phases

Dark navy sidebar with completion badges. Matches Build 4's professional styling.

**Synthetic demo data (`src/sample_data.py`)**

`get_brightpath_audit_data()` returns a fully structured synthetic audit for BrightPath Skills Training — a fictional small UK training provider used throughout the ChatGPT Mastery portfolio. Includes:
- Organisation profile (24 staff, 5 departments, Education and Training sector)
- Readiness scores across 6 dimensions (overall: 42/100 — Developing readiness)
- 4 workflow findings with pain points, AI opportunities, and recommended actions
- 5 risk findings including one Critical (Learner Data in Unapproved AI Tools)
- 3 pilot recommendations with timelines, success measures, and complexity ratings
- 6 training needs with audience, priority, and recommended formats
- 5 governance gaps including two Critical (No AI Use Policy, No Approved Tools List)

**Audit data layer (`src/audit_data_manager.py`)**

- `validate_audit_data()` — checks required fields, types, and constraints
- `summarise_audit_data()` — returns aggregated summary dict with counts and key metrics
- `format_audit_data_as_markdown()` — full Markdown representation of the audit
- `create_audit_data_from_form_data()` — builds audit data from UI form inputs

**Readiness scoring (`src/scoring_summary.py`)**

- `calculate_average_readiness_score()` — mean of 6 category scores
- `classify_readiness_level()` — bands: Low (0–39), Developing (40–59), Moderate (60–79), Strong (80–100)
- `generate_readiness_summary()` — structured summary with strongest/weakest categories, immediate priorities, and interpretation
- `format_readiness_summary_as_markdown()` — Markdown export

**Report section placeholders (`src/report_sections.py`)**

Five placeholder functions returning deterministic text:
- `generate_executive_summary_placeholder()`
- `generate_context_section_placeholder()`
- `generate_risk_section_placeholder()`
- `generate_opportunity_section_placeholder()`
- `generate_recommendations_section_placeholder()`

All handle missing/None fields safely without crashing.

**Scaffold modules**

- `src/risk_register.py` — sorts risk findings by severity; Markdown table formatter
- `src/roadmap_generator.py` — empty 30/60/90 structure placeholder
- `src/report_builder.py` — stub report builder
- `src/pdf_exporter.py` — `create_pdf_placeholder()` (basic reportlab scaffold) + `create_safe_pdf_filename()`
- `src/ui_components.py` — `apply_global_styles()`, `render_page_header()`, `render_responsible_use_warning()`, `render_prototype_notice()`, `render_info_card()`, `render_status_box()`, `render_metric_row()`, `render_completion_badge()`
- `src/utils.py` — `slugify()`, `create_safe_filename()`, `truncate_text()`, `risk_level_sort_key()`, `format_score_bar()`

**Tests**

Four test files, all passing:
- `tests/test_sample_data.py` — 17 tests
- `tests/test_audit_data_manager.py` — 20 tests
- `tests/test_scoring_summary.py` — 18 tests
- `tests/test_report_sections.py` — 20 tests

**Documentation**

- `README.md` — presentation-ready project overview
- `docs/build-notes.md` — this file
- `docs/architecture.md` — layer-by-layer architecture description
- `docs/safety-boundaries.md` — responsible-use constraints
- `docs/demo-script.md` — Phase 1 demo walkthrough
- `docs/future-improvements.md` — planned phases and future work

---

## Phase 2: Readiness Summary and Score Interpretation

The Readiness Summary page now interprets synthetic audit scores into a full client-facing readiness assessment.

**`src/scoring_summary.py` — expanded**

New functions added:

- `get_readiness_level_description(level)` — returns band description text for each of the four readiness levels
- `get_readiness_band_colour(level)` — returns hex colour for UI display
- `rank_readiness_categories(scores)` — returns all six category score dicts sorted highest to lowest
- `identify_readiness_strengths(scores, threshold=70)` — returns categories at or above the threshold with reason text
- `identify_readiness_gaps(scores, threshold=60)` — returns categories below threshold with risk and recommended action
- `generate_category_interpretation(category, score)` — returns band-specific consulting narrative for each category
- `generate_readiness_recommendations(summary)` — returns practical improvement actions derived from gaps and strengths

`generate_readiness_summary()` now returns a richer structure with: `overall_score`, `overall_level`, `overall_description`, `category_scores`, `ranked_categories`, `strengths`, `gaps`, `strategic_interpretation`, `recommendations`, `responsible_use_note`, `prototype_note`.

Category labels updated to human-readable form (e.g. "Strategy and leadership", "Data governance").

If `overall_readiness_score` is missing, it is calculated from the category average. Missing or invalid category scores are safely skipped.

**Readiness Summary page (`app.py`) — functional**

Page now:
- Checks for `audit_data` in session state (not pre-computed summary); shows setup steps if missing
- Generates the readiness summary fresh on page visit and stores in `readiness_summary` and `readiness_summary_markdown`
- Shows 5 metric cards: overall score, readiness level, strongest category, weakest category, priority gap count
- Shows overall readiness band with colour-coded left border
- Shows category scores with progress bars and expandable interpretation for each
- Shows ranked categories table
- Shows strengths panel (info cards) or informational message if no areas above threshold
- Shows priority gaps as expandable cards with risk and recommended action
- Shows strategic interpretation paragraph
- Shows numbered recommendations
- Shows responsible-use and prototype notices
- Provides a Markdown download button

**Tests** — `tests/test_scoring_summary.py` updated: 57 tests across 9 test classes covering all new functions.

---

## Phase 3: Risk Register Generator

The Risk Register page now converts synthetic audit risk findings into a structured AI risk register with risk scoring, risk levels, owner suggestions, recommended controls, priority actions, and Markdown export.

**`src/risk_register.py` — full implementation**

New functions:

- `normalise_risk_score(value)` — converts string labels (Very low/Low/Medium/High/Very high/Critical) or numeric values to an integer 1–5; defaults to 3 (Medium) for missing or invalid values
- `calculate_risk_score(likelihood, impact)` — returns `likelihood_score * impact_score` (range 1–25)
- `classify_risk_level(risk_score)` — 1–4: Low, 5–9: Medium, 10–16: High, 17–25: Critical
- `get_risk_level_description(risk_level)` — returns client-facing description of the risk level
- `get_risk_level_colour(risk_level)` — returns hex colour for UI display
- `generate_risk_id(index)` — formats as RISK-001, RISK-002, etc.
- `generate_risk_control_recommendation(risk)` — returns deterministic recommended control based on risk category from a lookup table
- `generate_risk_owner_suggestion(risk)` — returns suggested owner based on risk category
- `generate_risk_register(audit_data)` — builds complete risk register from audit risk findings; each item includes risk_id, risk_title, risk_category, description, likelihood, impact, likelihood_score, impact_score, risk_score, risk_level, risk_level_description, recommended_control, owner, priority_action, review_frequency, status, source
- `summarise_risk_register(risk_register)` — returns total/critical/high/medium/low counts, highest_risk, top_risk_categories, overall_risk_position, recommended_focus
- `prioritise_risks(risk_register)` — returns list sorted by risk_score descending
- `format_risk_register_as_markdown(risk_register, summary)` — full Markdown document with Risk Summary, Overall Risk Position, Recommended Focus Areas, Risk Register Table, Detailed Risk Notes, and Responsible-Use Boundaries sections

**Risk Register page (`app.py`) — functional**

Page now:
- Checks for `audit_data` in session state; shows setup steps if missing
- Generates risk register, summary, and prioritised list fresh on page visit
- Stores in `risk_register`, `risk_register_summary`, `risk_register_markdown` session state keys
- Shows 5 metric cards: total risks, critical, high, medium, low
- Shows a warning banner if critical or high risks are present
- Shows the highest-risk item with colour-coded left border
- Shows overall risk position paragraph
- Shows recommended focus areas as a bullet list
- Shows each risk as an expander with risk level badge, scores, owner, priority action, review frequency, and recommended control
- Shows responsible-use warning
- Provides a Markdown download button

**BrightPath demo results:**

| Risk | Likelihood | Impact | Score | Level |
|---|---|---|---|---|
| Learner Data in Unapproved AI Tools | High (4) | High (4) | 16 | High |
| No Approved AI Tools List | High (4) | Medium (3) | 12 | High |
| AI Hallucination in Training Materials | Medium (3) | High (4) | 12 | High |
| Safeguarding Decisions Delegated to AI | Low (2) | Critical→5 | 10 | High |
| Inconsistent AI Use Across Departments | High (4) | Low (2) | 8 | Medium |

**Tests** — `tests/test_risk_register.py` created: 110 tests across 11 test classes covering all new functions.

---

## Phase 4: Opportunity and Pilot Recommendation Generator

The Opportunity and Pilot Recommendation page now converts synthetic audit workflow findings and pilot recommendations into a structured AI opportunity portfolio with opportunity scoring, pilot sequencing, success measures, responsible-use controls, and Markdown export.

**`src/opportunity_generator.py` — full implementation**

New functions:

- `normalise_priority_value(value)` — converts string labels (Very low/Low/Medium/High/Very high) or numeric values to an integer 1–5; defaults to 3 (Medium) for missing or invalid values; strips descriptive text after em-dashes ("High — could save hours" → 4)
- `classify_complexity(value)` — returns a text label (Very low → Very high) for a complexity value
- `classify_potential_value(value)` — returns a text label for a potential value
- `classify_pilot_risk(value)` — returns a text label for a risk level
- `calculate_opportunity_score(potential_value, complexity, risk_level)` — returns `value*2 - complexity - risk + 10`, clamped 0–20
- `classify_opportunity_priority(score)` — 0–6: Low priority, 7–12: Medium priority, 13–16: High priority, 17–20: Strategic priority
- `generate_opportunity_id(index)` — formats as OPP-001, OPP-002, etc.
- `get_opportunity_priority_colour(priority)` — returns hex colour for UI display
- `generate_responsible_pilot_controls(pilot)` — returns standard responsible-use controls with pilot-specific extras for learner, quality, and safeguarding workflows
- `generate_pilot_success_measures(pilot)` — returns combined success measures (existing from pilot data + standard extras without duplication)
- `generate_opportunity_from_workflow_finding(finding, index)` — builds scored opportunity from a workflow finding; uses existing recommended_action when present
- `generate_pilot_from_recommendation(pilot, index)` — builds structured pilot from a pilot recommendation; uses "Medium" default for potential_value (not in raw pilot data)
- `prioritise_opportunities(opportunities)` — returns list sorted by opportunity_score descending
- `prioritise_pilots(pilots)` — returns list sorted by combined complexity + risk ascending (safest pilot first)
- `generate_ai_opportunity_portfolio(audit_data)` — builds full portfolio with opportunities, pilots, recommended first pilot, pilot sequence, and summary
- `summarise_opportunity_portfolio(portfolio)` — returns total/strategic/high/medium/low counts, recommended first pilot name, overall opportunity position, and recommended focus areas
- `format_opportunity_portfolio_as_markdown(portfolio, summary)` — full Markdown document with all required sections and responsible-use boundaries

**Opportunity and Pilot Recommendations page (`app.py`) — functional**

Page now:
- Checks for `audit_data` in session state; shows setup steps if missing
- Generates opportunity portfolio, summary, and Markdown fresh on page visit
- Stores in `opportunity_portfolio`, `opportunity_summary`, `opportunity_portfolio_markdown` session state keys
- Shows 4 metric cards: AI Opportunities, Pilots, Strategic/High count, Recommended First Pilot name
- Shows overall opportunity position paragraph
- Shows recommended focus areas as bullet list
- Shows recommended first pilot with colour-coded left border
- Shows recommended pilot sequence as visual cards with priority colour top border
- Shows each opportunity as an expander with priority badge, score, value/complexity/risk metrics, recommended action, success measures, and responsible-use controls
- Shows each pilot as an expander with priority badge, expected benefits, scope, success measures, responsible-use controls, and human review requirements
- Shows responsible-use warning
- Provides a Markdown download button

**BrightPath demo results:**

| Opportunity | Value | Complexity | Risk | Score | Priority |
|---|---|---|---|---|---|
| OPP-001 Course Material Development | High (4) | Medium (3) | Medium (3) | 12 | Medium priority |
| OPP-002 Quality and Compliance Reporting | High (4) | Medium (3) | Medium (3) | 12 | Medium priority |
| OPP-003 Enquiry and Enrolment Administration | Medium (3) | Medium (3) | Low (2) | 11 | Medium priority |
| OPP-004 Learner Progress Report Writing | Medium (3) | Medium (3) | High (4) | 9 | Medium priority |

| Pilot | Complexity | Risk | Priority |
|---|---|---|---|
| PILOT-001 AI-Assisted Lesson Plan Drafts | Low | Low | Medium priority |
| PILOT-002 Email Response Templates | Low | Low | Medium priority |
| PILOT-003 Quality Report Structure Templates | Medium | Medium | Medium priority |

Recommended first pilot: AI-Assisted Lesson Plan Drafts (lowest complexity + risk)

**Tests** — `tests/test_opportunity_generator.py` created: 160 tests across 13 test classes covering all new functions.

---

## Phase 5: 30/60/90-Day Roadmap Generator

The Roadmap page now generates a staged AI implementation roadmap covering First 30 days, Days 31–60, and Days 61–90. It includes actions, owners, success measures, cross-cutting controls, dependencies, risks to manage, and Markdown export.

**`src/roadmap_generator.py` — full implementation (replaces Phase 1 scaffold)**

New functions:

- `get_roadmap_phase_definitions()` — returns the three phase definitions (label, focus, ID prefix, colour)
- `generate_roadmap_action_id(phase_label, index)` — formats as DAY30-001, DAY60-001, DAY90-001, etc.
- `generate_roadmap_action(...)` — builds a single roadmap action dict with 10 fields: action_id, phase, title, description, owner, priority, success_measure, dependency, risk_reduction, related_output
- `get_priority_colour(priority)` — returns hex colour for High/Medium/Low priority
- `get_phase_colour(phase_label)` — returns hex colour for each phase
- `generate_foundation_actions(audit_data, readiness_summary, risk_summary)` — returns First 30 days actions (8 base + up to 2 adaptive based on governance gaps and high/critical risks)
- `generate_pilot_preparation_actions(audit_data, opportunity_portfolio)` — returns Days 31–60 preparation actions (training, materials, briefing)
- `generate_pilot_delivery_actions(audit_data, opportunity_portfolio)` — returns Days 31–60 delivery actions (launch, review, tracking, incidents); references recommended first pilot name when available
- `generate_review_and_scale_actions(audit_data, opportunity_portfolio, risk_summary)` — returns Days 61–90 actions (6 base + 1 adaptive for unresolved high risks)
- `generate_implementation_roadmap(audit_data, readiness_summary, risk_register, risk_summary, opportunity_portfolio)` — builds the full roadmap; renumbers combined Day 60 actions sequentially; determines recommended first pilot from opportunity portfolio or audit data; derives overall_roadmap_position from risk and readiness summaries
- `summarise_implementation_roadmap(roadmap)` — returns total/Day30/Day60/Day90/high-priority action counts, first pilot name, dependencies, risks, and overall position
- `format_implementation_roadmap_as_markdown(roadmap, summary)` — full Markdown document with all required sections and responsible-use boundaries

**Adaptive roadmap logic for BrightPath:**

- BrightPath has "No AI Use Policy" (Critical governance gap) → foundation adds a "Draft and approve a formal AI use policy" action
- BrightPath has 4 high-priority risks → foundation adds "Address top priority AI governance and data risks" action
- BrightPath has 4 high-priority risks → review phase adds "Address outstanding risk register items before scaling" action
- Recommended first pilot: AI-Assisted Lesson Plan Drafts (from opportunity portfolio)

**BrightPath demo results:**

| Phase | Actions |
|---|---|
| First 30 days (foundation) | 10 |
| Days 31–60 (pilot prep + delivery) | 7 |
| Days 61–90 (review and scale) | 7 |
| **Total** | **24** |

High-priority actions: 15+. Overall position: governance and data boundary priority before scaling.

**Roadmap page (`app.py`) — functional**

Page now:
- Checks for `audit_data` in session state; shows setup steps if missing
- Shows a helpful tip if readiness summary, risk register, or opportunity portfolio are not yet generated
- Optionally uses `readiness_summary`, `risk_register`, `risk_register_summary`, and `opportunity_portfolio` from session state
- Generates roadmap, summary, and Markdown fresh on page visit
- Stores in `implementation_roadmap`, `implementation_roadmap_summary`, `implementation_roadmap_markdown` session state keys
- Shows 5 metric cards: Organisation, Total Actions, High Priority, Phases (3), Recommended First Pilot
- Shows overall roadmap position
- Shows recommended first pilot with green highlight card
- Shows each of the 3 phases with colour-coded headers and action expanders; each action shows description, priority badge, owner, success measure, dependency, risk reduction, and related output
- Shows cross-cutting controls, success measures, dependencies, and risks to manage as bullet lists
- Shows responsible-use warning
- Provides Markdown download button

**Tests** — `tests/test_roadmap_generator.py` created: 111 tests across 10 test classes covering all new functions.

---

---

## Phase 6: Report Section Generator

The Report Sections page now generates deterministic consulting-style report sections from synthetic audit data and optional enrichment outputs (readiness summary, risk register, opportunity portfolio, implementation roadmap).

**`src/report_sections.py` — full Phase 6 implementation**

New functions (Phase 1 placeholder functions kept for backward compatibility):

- `generate_executive_summary(audit_data, readiness_summary, risk_summary, opportunity_summary, roadmap_summary)` — polished two-to-three paragraph executive summary using all available outputs; references org name, overall score, level, strongest/weakest areas, risk count, and recommended first pilot
- `generate_organisation_context_section(audit_data)` — structured description of organisation, sector, staff count, departments, current AI use, and main business goals
- `generate_readiness_interpretation_section(readiness_summary)` — full score interpretation if readiness summary is available; falls back to a "not yet generated" message
- `generate_key_findings_section(audit_data, readiness_summary, risk_summary, opportunity_summary)` — 5–10 deterministic key findings derived from all available outputs; adapts to include risk counts, readiness level, and governance gaps
- `generate_risk_summary_section(risk_register, risk_summary)` — risk count, top risks, overall position, and focus areas; falls back to "not yet generated" if no data
- `generate_opportunity_summary_section(opportunity_portfolio, opportunity_summary)` — opportunity and pilot counts, first pilot, pilot sequence; falls back to "not yet generated" if no data
- `generate_roadmap_summary_section(implementation_roadmap, roadmap_summary)` — phase action counts, high-priority count, first pilot, key dependencies, overall position; falls back to "not yet generated" if no data
- `generate_training_needs_section(audit_data)` — structured listing of training topics with audience, priority, reason, and format; includes link to Build 4
- `generate_governance_recommendations_section(audit_data, risk_summary, readiness_summary)` — governance gaps from audit + 10 standard recommendations
- `generate_immediate_next_steps_section(audit_data, readiness_summary, risk_summary, opportunity_summary, roadmap_summary)` — 8 practical next steps with first pilot name adapted from available outputs
- `generate_responsible_use_section()` — fixed responsible-use text with no real data, no advice claims, and human review required
- `generate_all_report_sections(...)` — generates all eleven sections and returns full report dict with section_order, source_outputs_available, prototype_note
- `summarise_report_sections(report_sections)` — returns total/with-content counts, source outputs used, missing source outputs, review_required, overall readiness message
- `format_report_sections_as_markdown(report_sections)` — full Markdown document starting with `# AI Consulting Report Sections`, Report Overview, Source Outputs Used, then all eleven sections in order with purpose, content, key points, recommendations, and review notes

Each section function returns a dict with: `section_id`, `section_title`, `section_purpose`, `content`, `key_points`, `recommendations`, `source_outputs_used`, `review_note`.

All functions handle missing or None inputs without crashing. If enrichment outputs are missing, sections display an appropriate message and recommend running the relevant page.

**Report Sections page (`app.py`) — functional**

Page now:
- Checks for `audit_data` in session state; shows setup steps if missing
- Shows a tip if readiness summary, risk register, opportunity portfolio, or roadmap are not yet generated
- Collects all optional enrichment data from session state
- Generates report sections, summary, and Markdown fresh on page visit
- Stores in `report_sections`, `report_sections_summary`, `report_sections_markdown` session state keys
- Shows 5 metric cards: Organisation, Total Sections, Source Outputs Used, Missing Source Outputs, Review Required
- Shows source output availability checklist (5 cards: audit data, readiness summary, risk register, opportunity portfolio, implementation roadmap)
- Shows overall report readiness statement
- Shows each of the 11 sections in expanders: purpose, content, key points, recommendations, review note
- Shows responsible-use warning
- Provides a Markdown download button

Sidebar badge updated: Report Sections completion badge now reflects whether `report_sections` is in session state.

**BrightPath demo results (with all enrichment outputs generated):**

| Section | Status |
|---|---|
| Executive Summary | Generated — score 42/100, 4 high risks, Lesson Plan Drafts as first pilot |
| Organisation Context | Generated — 24 staff, 5 departments, informal AI use |
| AI Readiness Interpretation | Generated — 6 category scores, 1 gap, strategic interpretation |
| Key Findings | Generated — 9 findings including governance, risk, and training constraints |
| Risk Summary | Generated — 5 risks (4 high), top 3 risks with controls |
| Opportunity and Pilot Summary | Generated — 4 opportunities, 3 pilots, pilot sequence |
| 30/60/90-Day Roadmap Summary | Generated — 24 actions, 15 high priority, dependencies and risks |
| Training and Capability Needs | Generated — 6 training topics with Build 4 reference |
| Governance Recommendations | Generated — 5 gaps + 10 standard recommendations |
| Immediate Next Steps | Generated — 8 practical actions |
| Responsible-Use Boundaries | Generated — fixed responsible-use boundaries text |

**Tests** — `tests/test_report_sections.py` updated: 5 backward-compatibility classes (25 tests) + 14 new Phase 6 test classes (120+ tests) covering all new functions. 538+ total suite tests pass.

---

## Phase 7: Client Report Builder

The Client Report page now assembles all generated Build 5 outputs into a complete client-facing Markdown consulting report. It includes report readiness checks, section selection, missing-output guidance, responsible-use boundaries, prototype limitations, and Markdown export.

### Functions added to `src/report_builder.py` (full rewrite)

| Function | Description |
|---|---|
| `get_client_report_required_sections()` | Returns always-included section IDs |
| `get_client_report_optional_sections()` | Returns optional section IDs |
| `check_client_report_readiness(session_state)` | Checks which outputs are available; returns readiness report with missing sections and recommended next steps |
| `build_client_report_data_from_session_state(session_state)` | Assembles all session state data into a single report data dict |
| `generate_report_cover_section(report_data)` | Generates cover page Markdown with org details and prototype status |
| `generate_report_table_of_contents(report_data, include_sections)` | Generates TOC respecting section selection |
| `generate_report_executive_summary_section(report_data)` | Uses report_sections data when available; falls back to audit data |
| `generate_report_context_section(report_data)` | Organisation profile from audit data |
| `generate_report_readiness_section(report_data)` | Category scores and strategic interpretation; graceful missing-data message |
| `generate_report_risk_section(report_data)` | Risk summary with top risks table; graceful missing-data message |
| `generate_report_opportunity_section(report_data)` | Opportunities and pilot sequence; graceful missing-data message |
| `generate_report_roadmap_section(report_data)` | 30/60/90-day plan summary; graceful missing-data message |
| `generate_report_training_needs_section(report_data)` | Training topics with Build 4 reference |
| `generate_report_governance_section(report_data)` | Governance gaps from audit + 10 standard recommendations |
| `generate_report_next_steps_section(report_data)` | 8 immediate next steps; weaves in first pilot name |
| `generate_report_key_findings_section(report_data)` | 5–7 deterministic key findings from audit data |
| `generate_report_appendices_section(report_data)` | Audit summary, category scores, risk table, pilot table, roadmap summary, source outputs |
| `generate_report_responsible_use_section()` | Verbatim responsible-use boundaries |
| `generate_markdown_client_report(report_data, include_sections)` | Assembles full 13-section Markdown report |
| `summarise_client_report(report_data)` | Returns summary dict: organisation, sections, risks, pilots, roadmap actions, readiness |
| `create_client_report_filename(organisation_name)` | Safe dated Markdown filename |
| `build_report_placeholder(audit_data)` | Retained for backward compatibility |

### BrightPath demo report (full session)

| Metric | Value |
|---|---|
| Organisation | BrightPath Skills Training |
| Sections available | 6 of 6 source outputs |
| Risks included | 5 |
| Opportunities | 4 |
| Pilots | 3 |
| Roadmap actions | 24 |
| Report readiness | Ready for export, subject to human review |

### Session state keys added (Phase 7)

| Key | Type | Set by |
|---|---|---|
| `client_report_data` | dict | Client Report page |
| `client_report_markdown` | str | Client Report page |
| `client_report_filename` | str | Client Report page |
| `client_report_readiness` | dict | Client Report page |

**Tests** — `tests/test_report_builder.py` created: 122 tests across 10 test classes covering all Phase 7 functions. 807 total suite tests pass.

---

## Phase 8: Export Centre — PDF, PPTX, and Analytics Charts

The Export Centre page is now fully functional. It generates PDF and PowerPoint exports of the AI consulting client report, with deterministic analytics, matplotlib charts, and professional formatting. All exports use synthetic demo data only.

### New source modules

**`src/report_analytics.py`**

Deterministic analytics calculated from generated Build 5 outputs only.

- `calculate_export_completion_status(export_data)` — returns dict of output name → bool (Audit Data, Readiness Summary, Risk Register, Opportunity Portfolio, Implementation Roadmap, Report Sections, Client Report)
- `calculate_readiness_score_breakdown(export_data)` — returns `{label: int_score}` from audit_data readiness_scores with Overall key
- `calculate_risk_level_counts(export_data)` — prefers `risk_register_summary`; falls back to counting risk_register list; returns `{Critical: n, High: n, Medium: n, Low: n}`
- `calculate_opportunity_priority_counts(export_data)` — prefers opportunity_summary keys; returns `{Strategic: n, High: n, Medium: n, Low: n}`
- `calculate_roadmap_action_counts(export_data)` — prefers implementation_roadmap_summary; returns `{"First 30 Days": n, "Days 31–60": n, "Days 61–90": n}`
- `calculate_report_quality_summary(export_data)` — returns 8-key boolean dict checking client_report_markdown content
- `build_client_report_analytics(export_data)` — returns all 6 analytics dicts under their respective keys

**`src/chart_utils.py`**

matplotlib bar charts with Agg backend (server-safe). All functions return path or `""` on any failure.

- `create_completion_status_chart(completion_status, output_path)` — horizontal bar, green=done, light=not done
- `create_readiness_score_chart(score_breakdown, output_path)` — horizontal bar, green ≥70, amber ≥40, red <40; dashed lines at 40 and 70
- `create_risk_level_chart(risk_counts, output_path)` — returns `""` if all counts are zero
- `create_opportunity_priority_chart(opportunity_counts, output_path)` — horizontal bar by priority tier
- `create_roadmap_action_chart(roadmap_counts, output_path)` — navy/blue/amber for 3 phases
- `generate_all_export_charts(analytics, output_dir)` — returns dict of `chart_name → file_path` for all successfully generated charts; chart files written to `outputs/charts/`

All functions wrapped in `try/except Exception`; return `""` on failure.

**`src/pdf_exporter.py` — complete rewrite**

Full professional PDF: cover page, analytics section, embedded charts, full client report Markdown, responsible-use section, and prototype limitations.

- `create_safe_pdf_filename(title)` — safe dated filename
- `format_pdf_text(text)` — strips `#` headings, converts `**bold**` → `<b>bold</b>`, escapes XML characters
- `build_pdf_styles()` — returns 12-key style dict (CoverTitle, CoverSubtitle, CoverMeta, CoverProto, H1, H2, H3, Body, Bullet, Caption, Warning); all use Helvetica; navy headings
- `add_cover_page(story, styles, title, organisation_name, subtitle, generated_date, prototype_note)` — navy table header block with white title
- `add_section_heading(story, styles, heading)` — H1-level section divider
- `add_paragraphs_from_markdown(story, styles, markdown_text)` — line-by-line parser: `##` → H2, `###` → H3, `-` → Bullet, `|` → table, plain → Body
- `add_bullet_list(story, styles, items)` — formatted bullet list
- `add_simple_table(story, styles, data)` — striped table from list of lists
- `add_chart_image(story, image_path, title)` — skips if file missing; 150mm×80mm embedded image
- `add_responsible_use_section(story, styles)` — fixed responsible-use boundaries
- `export_client_report_to_pdf_bytes(export_data, analytics, chart_paths)` — returns full PDF bytes; returns `b""` on failure
- `create_pdf_placeholder(title, body_text)` — retained for backward compatibility

**`src/pptx_exporter.py` — new file**

15-slide executive PPTX deck using python-pptx with blank layouts and manual shape placement. Widescreen (13.33" × 7.5"). All slides use blank layout for full control.

- `create_safe_pptx_filename(title)` — safe dated filename ending in `.pptx`
- `format_slide_text(text, max_chars)` — strips Markdown, truncates to max_chars with ellipsis
- `extract_slide_bullets(items, max_items)` — handles list or string input; strips `- •` prefixes; returns up to max_items
- `add_title_slide(prs, title, subtitle, footer)` — navy background, blue top accent bar, white title 36pt bold
- `add_bullet_slide(prs, title, bullets, speaker_notes)` — navy title bar (1.1"), white content area, bullet points 13pt
- `add_two_column_slide(prs, title, left_title, left_bullets, right_title, right_bullets)` — two equal-width content panels below title bar
- `add_chart_slide(prs, title, image_path, bullets)` — chart left + bullets right if image exists; graceful text-only fallback
- `add_responsible_use_slide(prs)` — amber title bar to signal importance
- `export_client_report_to_pptx_bytes(export_data, analytics, chart_paths)` — returns PPTX bytes; returns `b""` on failure

15-slide deck structure:
1. Title slide (navy background)
2. Organisation Context
3. AI Readiness Summary
4. Readiness Score Chart
5. Key Findings
6. Risk Summary
7. Risk Chart
8. Opportunity and Pilot Recommendations
9. Opportunity Chart
10. 30/60/90-Day Roadmap
11. Roadmap Chart
12. Governance Recommendations
13. Immediate Next Steps
14. Responsible-Use Boundaries (amber title bar)
15. Recommended Direction

**`src/export_centre.py` — new file**

Central coordinator for export readiness, data assembly, quality checking, and format preparation.

- `get_export_formats()` — returns `["Markdown", "PDF", "PowerPoint (PPTX)"]`
- `check_export_readiness(session_state)` — returns `is_ready`, `available_outputs`, `missing_outputs`, `recommended_next_steps`, `can_export_markdown`, `can_export_pdf`, `can_export_pptx`
- `build_export_data_from_session_state(session_state)` — returns all session outputs + org_name, generated_date, responsible_use_note, prototype_note
- `generate_export_quality_checklist(export_data)` — returns list of `{item: str, passed: bool}` (9 checks)
- `summarise_export_package(export_data)` — returns organisation_name, sections_available/missing, counts, export_formats, human_review_required
- `create_export_filename_base(organisation_name)` — safe text base for filenames
- `prepare_markdown_export(export_data)` — returns `(markdown_text, filename)`
- `prepare_pdf_export(export_data, analytics, chart_paths)` — returns `(pdf_bytes, filename)`; `(b"", filename)` on failure
- `prepare_pptx_export(export_data, analytics, chart_paths)` — returns `(pptx_bytes, filename)`
- `prepare_all_exports(export_data, analytics, chart_paths)` — returns dict with markdown, markdown_filename, pdf_bytes, pdf_filename, pptx_bytes, pptx_filename

### Export Centre page (`app.py`) — functional

Page now:
- Guard: `audit_data` missing → shows setup steps and stops
- Guard: `client_report_markdown` missing → prompts to run Client Report page first
- Builds export_data and export_readiness from session state
- Generates analytics via `ra.build_client_report_analytics()`
- Generates chart_paths via `cu.generate_all_export_charts()` with graceful failure
- Stores `export_data`, `export_readiness`, `client_report_analytics`, `client_report_chart_paths` in session state
- Shows 6 summary metric cards
- Shows export readiness quality checklist in 3-column grid
- Shows analytics summary (2-col + 3-col layout)
- Shows chart previews (3 columns, reading PNG bytes from file)
- Prepares PDF and PPTX bytes in try/except blocks
- Stores all export outputs in session state
- Shows 3 download buttons: Markdown | PDF | PPTX
- Shows responsible-use warning at bottom

### Session state keys added (Phase 8)

| Key | Type | Set by |
|---|---|---|
| `export_data` | dict | Export Centre page |
| `export_readiness` | dict | Export Centre page |
| `client_report_analytics` | dict | Export Centre page |
| `client_report_chart_paths` | dict | Export Centre page |
| `client_report_pdf_bytes` | bytes | Export Centre page |
| `client_report_pdf_filename` | str | Export Centre page |
| `client_report_pptx_bytes` | bytes | Export Centre page |
| `client_report_pptx_filename` | str | Export Centre page |

### Supporting files

- `outputs/charts/.gitkeep` — tracks `outputs/charts/` directory in git without committing generated PNG files

### New dependencies

- `matplotlib>=3.8.0` — chart generation (Agg backend)
- `python-pptx>=0.6.21` — PPTX export

### Tests

Five new test files:

| File | Classes | Tests |
|---|---|---|
| `tests/test_report_analytics.py` | 7 | 33 |
| `tests/test_chart_utils.py` | 6 | 24 |
| `tests/test_pdf_exporter.py` | 5 | 23 |
| `tests/test_pptx_exporter.py` | 4 | 22 |
| `tests/test_export_centre.py` | 8 | 43 |

Total test suite: 807 existing + Phase 8 tests.

---

## Phase 9: Completion Review and Portfolio Notes

The Completion Review page and supporting documentation were added to close Build 5 as a portfolio-ready AI consulting prototype. The build now includes phase tracking, output completion checks, documentation checks, portfolio notes, case study summary, testing checklist, screenshot guidance, and final review guidance.

### New source module

**`src/completion_review.py`**

Deterministic completion-review helpers:

- `get_build5_phase_checklist()` — returns all 9 completed phases with purpose, status, and evidence
- `get_expected_build5_outputs()` — returns the full expected session-state output checklist
- `check_session_state_outputs(session_state)` — checks available/missing outputs and recommends next actions
- `check_documentation_files(base_path)` — checks expected README/docs files
- `generate_completion_score(phase_status, output_status, documentation_status)` — returns overall completion status and final readiness label
- `generate_build5_completion_review(session_state, base_path)` — assembles the full completion review dict
- `generate_portfolio_summary()` — returns portfolio positioning notes
- `generate_case_study_summary()` — returns the BrightPath case-study summary
- `format_completion_review_as_markdown(review)` — exports completion review Markdown
- `format_portfolio_notes_as_markdown(portfolio_summary, case_study_summary)` — exports portfolio notes Markdown

### Completion Review page (`app.py`)

The new page:

- Generates the Build 5 completion review
- Shows phase checklist
- Shows output completion status
- Shows documentation checklist
- Shows completion score and final readiness label
- Shows portfolio value, commercial value, technical value, and responsible-use position
- Shows recommended final actions
- Shows Markdown previews
- Provides Markdown downloads for the completion review and portfolio notes
- Handles missing workflow outputs safely by showing what still needs to be generated

### Session state keys added (Phase 9)

| Key | Type | Set by |
|---|---|---|
| `completion_review` | dict | Completion Review page |
| `completion_review_markdown` | str | Completion Review page |
| `portfolio_notes` | dict | Completion Review page |
| `portfolio_notes_markdown` | str | Completion Review page |

### Documentation added

- `docs/completion-review.md`
- `docs/portfolio-notes.md`
- `docs/testing-checklist.md`
- `docs/case-study-summary.md`
- `docs/screenshots-checklist.md`

### Documentation updated

- `README.md`
- `docs/build-notes.md`
- `docs/architecture.md`
- `docs/safety-boundaries.md`
- `docs/demo-script.md`
- `docs/future-improvements.md`

### Tests

New test file:

| File | Tests |
|---|---|
| `tests/test_completion_review.py` | Completion-review functions, score generation, portfolio/case-study summaries, Markdown formatting, missing-output handling |

Responsible-use boundaries remain unchanged: synthetic/demo data only, no real client/learner/HR/safeguarding/personal/confidential/regulated data, no external LLM calls, no production-readiness claim, and human review required before any real-world use.

---

*Build 5 · AI Consulting Report Generator · BrightPath ChatGPT Mastery Project*
