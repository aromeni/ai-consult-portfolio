# Build Notes — BrightPath AI Readiness + Workflow Audit Tool

**Build start:** 2026-06-08  
**Status:** Polish Step 6 — PDF report design polish complete (Prototype v0.9)

---

## Build Objective

Create a working Streamlit prototype that a consultant (Rashid) can use with a small UK training provider to:

1. Baseline the organisation's current AI use and readiness
2. Audit its workflows for AI suitability and risk
3. Score readiness across five dimensions
4. Generate a simple, evidence-based pilot recommendation
5. Produce a concise summary report the manager can keep

This is the first practical build in the ChatGPT Mastery / GPT Master project. It is the proof point that Layers 3–7 work together as a client-facing deliverable.

---

## MVP Scope

The MVP (Phases 1–5) will include:

- [ ] Streamlit app with seven-page sidebar navigation
- [ ] Organisation profile form (org type, size, sector, current AI tool use)
- [ ] AI readiness questionnaire (five dimensions, scored 1–5 each)
- [ ] Workflow audit table (list of common workflows with AI suitability flag and risk level)
- [ ] Risk scoring display (aggregated from readiness and workflow inputs)
- [ ] Pilot recommendation output (based on total readiness score band)
- [ ] Mini report page (summary of all inputs and scores, text export)
- [ ] BrightPath synthetic sample data pre-loaded for demo use

---

## Non-Features (MVP)

These are explicitly out of scope for the MVP:

- No external API calls
- No AI model calls (ChatGPT, Claude, etc.)
- No real data storage or database
- No user authentication
- No multi-user sessions
- No PDF export (text export only in MVP)
- No benchmarking against other organisations
- No automated email or report delivery
- No live workflow integration

These may be added in a future phase — they are not gaps in the MVP.

---

## Safety Boundaries

- All sample data is synthetic, anonymised, or fictional
- No real learner, client, staff, safeguarding, or personal data should be entered
- The tool provides indicative assessment guidance — not legal, compliance, or HR advice
- Outputs are a structured starting point for conversation, not a certified audit result
- The responsible use notice is displayed on the Home page and in the mini report

---

## Planned Build Phases

| Phase | Scope | Status |
|---|---|---|
| 1 | Scaffold — folder structure, app.py navigation, placeholder pages | Complete |
| 2 | AI Readiness Assessment — 10-dimension questionnaire, 0–100 scoring, live category, bar chart, next action | Complete |
| 3 | Workflow Audit — 10-dimension suitability scoring (0–50), workflow info form, category, next action, bar chart, BrightPath sample loader | Complete |
| 4 | Risk Assessment — 10 risk categories, likelihood × impact scoring (1–25), level classification, safeguards, overall recommendation | Complete |
| 5 | Pilot Recommendation — combines readiness, workflow, and risk scores into a recommendation with explanation, safeguards, and next actions | Complete |
| 6 | Mini Report — 9-section Markdown report generator, editable form, live preview, `.md` download, BrightPath sample loader | Complete |
| 7 | Portfolio documentation — case study, demo script, screenshots checklist, build reflection, future improvements, README rewrite | Complete |

### Phase 2 notes (2026-06-08)

- Added `READINESS_DIMENSIONS` (10 entries) to `scoring.py` — each with key, label, question, and hint
- Added `READINESS_LEVELS` to `scoring.py` — five bands (0–25, 26–50, 51–70, 71–85, 86–100) each with category, alert type, explanation, and next action
- Added `calculate_readiness_score()`, `get_readiness_level()`, `get_readiness_category()`, `get_readiness_explanation()`, `get_next_action()` to `scoring.py`
- Added `BRIGHTPATH_READINESS_SCORES` to `sample_data.py` — 10 synthetic dimension scores totalling 35 ("Early awareness")
- Replaced assessment page placeholder in `app.py` with: 10 sliders (0–10, keyed to session state), live total metric, readiness category metric, colour-coded explanation, quoted next action, bar chart, and expandable score table
- Demo data button on Home page now pre-populates all 10 slider values from `BRIGHTPATH_READINESS_SCORES`
- All sliders use `help=` tooltip for the hint text — questions are the slider labels; no personal or sensitive data requested at any point

### Phase 3 notes (2026-06-08)

- Added `WORKFLOW_SCORING_DIMENSIONS` (10 entries) to `scoring.py` — each with key, label, question, and hint
- Added `WORKFLOW_SUITABILITY_LEVELS` to `scoring.py` — five bands (0–15, 16–25, 26–35, 36–42, 43–50) each with category, alert type, explanation, and next action
- Added `calculate_workflow_suitability_score()`, `get_workflow_suitability_level()`, `get_workflow_suitability_category()`, `get_workflow_suitability_explanation()`, `get_workflow_next_action()` to `scoring.py`
- Added `BRIGHTPATH_SAMPLE_WORKFLOW` (9-field dict) and `BRIGHTPATH_SAMPLE_WORKFLOW_SCORES` (10 scores totalling 42 → "Good pilot candidate") to `sample_data.py`
- Replaced Workflow Audit page placeholder in `app.py` with: safety notice, sample loader button (pre-populates all fields + sliders via session state + `st.rerun()`), two-column workflow info form (name, owner, tools, frequency, time, data sensitivity), three text areas (description, pain points, AI idea), 10 scoring sliders (0–5), live results (score/50 metric, category metric, colour-coded explanation, quoted next action), bar chart, and expandable score table
- Sample loader button positioned above all form widgets so session state is set before widgets render — no widget-after-instantiation errors
- All form fields use role/process-level placeholders; no personal data fields at any point

### Phase 4 notes (2026-06-08)

- Added `RISK_CATEGORIES` (10 entries) to `scoring.py` — each with key, label, and description
- Added `RISK_SAFEGUARDS` dict to `scoring.py` — one safeguard per category
- Added `_RISK_LEVEL_MAP` to `scoring.py` — four bands (1–4 Low, 5–9 Moderate, 10–15 High, 16–25 Critical)
- Added `calculate_risk_score(likelihood, impact)`, `get_risk_level()`, `get_risk_level_explanation()`, `get_risk_safeguard()`, `calculate_overall_risk_summary()` to `scoring.py`
- Added `BRIGHTPATH_RISK_PROFILE` to `sample_data.py` — lesson planning use case with 10 synthetic risk scores (total profile: 4 Low, 3 Moderate, 1 High, 0 Critical → overall "Pilot only with safeguards")
- Replaced Risk Assessment page placeholder in `app.py` with: prototype disclaimer warning, data safety notice, sample loader button, 10 risk category rating sections (each with likelihood slider + impact slider), live risk summary table, High/Critical alerts with safeguards, overall summary metrics (counts by level + highest level), colour-coded overall recommendation, and expandable BrightPath example with worked table and observations
- Sample loader button positioned above all keyed widgets — uses `st.rerun()` to prevent widget-after-instantiation errors (same pattern as Phase 3)
- Safety warning displayed prominently at the top: "This tool is a prototype and does not provide legal, safeguarding, HR, compliance, medical, financial, or academic-integrity advice."
- No personal data fields at any point — all inputs are organisation-level and process-level observations

### Phase 5 notes (2026-06-08)

- Added `_PILOT_ALERT_TYPES`, `_PILOT_EXPLANATIONS`, `_PILOT_NEXT_ACTIONS`, `PILOT_SAFEGUARDS` to `scoring.py`
- Added `get_pilot_recommendation()`, `get_pilot_recommendation_explanation()`, `get_pilot_next_actions()`, `get_pilot_safeguards()` to `scoring.py`
- Recommendation logic checks restrictive conditions first: critical risk → "Not ready"; high risk → "Governance-first"; readiness < 51 → "Not ready"; workflow < 26 → "Process redesign"; then positive conditions in descending strength order
- Safeguards are universal (10 items applicable to all recommendations) — next actions differ by recommendation category
- Added `BRIGHTPATH_PILOT_EXAMPLE` to `sample_data.py` — illustrative values (readiness 62, workflow 40, risk Moderate) giving "Low-risk pilot candidate"
- Replaced Pilot Recommendation page placeholder in `app.py` with: data safety notice, auto/manual hybrid inputs (pulls from session state for readiness, workflow, risk, workflow name, AI support idea; falls back to number inputs / text fields if not set), recommendation alert with explanation, two-column next actions + safeguards, summary table (Metric/Value/Interpretation), expandable BrightPath example with worked table and explanation
- Risk defaults to Low for all categories if Risk Assessment page not completed — visible caption warns user

### Phase 6 notes (2026-06-08)

- Added `format_safeguards()`, `format_next_actions()`, `create_report_filename()`, `generate_markdown_report()` to `report_generator.py`; kept `generate_text_report()` for backwards compatibility
- `create_report_filename()` lowercases the org name, strips non-alphanumeric characters to hyphens, and appends `-ai-readiness-mini-report.md`
- `generate_markdown_report()` produces a 9-section Markdown string: Organisation Profile, AI Readiness Summary, Workflow Audit Summary, Risk Assessment Summary, Pilot Recommendation, Recommended Safeguards, Suggested Next Actions, Responsible Use and Limitations (verbatim from spec), Consultant Notes
- `_cell()` helper escapes pipe characters in long field values to prevent breaking Markdown table rows
- Added `BRIGHTPATH_MINI_REPORT_SAMPLE` to `sample_data.py` — 13-field dict with BrightPath sample values for all Mini Report form fields
- Replaced Mini Report placeholder in `app.py` with: safety notice, sample loader button (pre-populates all `report_*` keys + `st.rerun()`), 6-section form (organisation, readiness, workflow, risk, pilot recommendation, consultant notes), live recommendation alert computed from form inputs, editable safeguards and next actions text areas pre-populated from `get_pilot_safeguards()` / `get_pilot_next_actions()`, report preview expander, Markdown download button showing filename
- Form defaults are computed from existing session state (previous-page slider values, `wf_*` keys, `risk_*` keys, profile) — each widget uses its computed default on first render only; after that, session state or sample loader controls the value
- Sample loader button positioned above all keyed widgets + calls `st.rerun()` — consistent with Phases 3/4/5 pattern
- No personal data fields at any point — all inputs are org/role/process level with appropriate placeholder text

### Polish Step 6 notes (2026-06-10)

- Polish Step 6 redesigned the PDF report visually without changing content, sections, or scoring logic.
- **Title banner**: replaced plain title text with a full-width dark-blue (`#1a3a5c`) table cell; white title (18pt bold), light-blue subtitle (`#aaccee`, 9pt) showing org name and date.
- **Section headings**: replaced plain `Paragraph` headings with a 1-column Table; light-blue background (`#e8f0f7`), 4pt dark-blue left border accent via `LINEBEFORE`, 10pt left padding.
- **KV tables**: added shaded label column (`#d4e4f4`), full box border, column divider, row-separator lines, and alternating value-column row shading (`#f5f8fc`) on odd rows.
- **Per-page footer**: removed the flowable footer; added `_draw_footer` canvas callback passed to `doc.build(onFirstPage=, onLaterPages=)`. Draws a rule at 1.85 cm, two centred italic lines at 1.35 cm and 0.85 cm, and a right-aligned page number.
- **Section flow**: wrapped compact sections (1–5, 8, 9) in `KeepTogether` to prevent orphaned headings.
- **Spacing**: consistent `Spacer(1, 0.3*cm)` between sections; `Spacer(1, 0.15*cm)` between heading and table.
- Added `KeepTogether` import from `reportlab.platypus`; no other imports changed.
- Markdown export unchanged. All 71 tests pass.

### Polish Step 5 notes (2026-06-10)

- Polish Step 5 added PDF report export while keeping Markdown export.
- Added `reportlab` to `requirements.txt`.
- Added `create_pdf_report_filename()` and `generate_pdf_report_bytes()` to `src/report_generator.py` — both functions mirror the same `report_data` dict accepted by `generate_markdown_report()`.
- PDF uses `reportlab.platypus.SimpleDocTemplate` with A4 page size, 2.5 cm margins, custom `ParagraphStyle` objects for title, headings, body, bullet lists, and footer; includes all 9 report sections plus responsible-use text verbatim.
- Updated `app.py` Mini Report page: replaced the single Markdown download button with two side-by-side download buttons (Markdown `type="primary"`, PDF default style) plus a caption note: "Markdown is useful for editing and version control. PDF is better for sharing a polished report."
- Added `generate_pdf_report_bytes` and `create_pdf_report_filename` to `src/report_generator` imports in `app.py`.
- Added 4 new tests to `tests/test_report_generator.py`: `test_pdf_returns_bytes`, `test_pdf_is_not_empty`, `test_pdf_starts_with_pdf_magic`, `test_pdf_handles_missing_optional_fields` — all pass.
- Total test count: 71 (was 67). All 71 pass.

### Polish Step 4 notes (2026-06-08)

- Rewrote `src/utils.py` with full custom CSS (`_CSS` string) and 11 new helper functions: `inject_custom_css()`, `render_page_header()`, `render_safety_notice()`, `render_responsible_use()`, `get_risk_badge()`, `render_risk_table()`, `render_score_hero()`, `render_recommendation_card()`, `render_next_actions()`, `render_safeguards()`, `render_section_heading()`
- CSS targets: `.bp-header`, `.bp-feature-grid / .bp-feature-card`, `.bp-step-row / .bp-step-num`, `.risk-badge` with four level classes, `.bp-risk-table`, `.score-hero`, `.bp-safety`, `.bp-ru-notice`, `.bp-profile-card / .bp-profile-item / .flag-yes / .flag-no`, `.scale-legend`, `.bp-section`, `.rec-banner` with four type classes, `.actions-box / .action-item`, `.safeguards-box / .safeguard-item`, sidebar and metric container via `[data-testid]` selectors
- Rewrote `app.py` (~450 lines → clean, structured) using all new helpers — no logic changes, only UI orchestration layer updated
- Home page: feature grid (6 cards), numbered step guide (7 steps), branded sidebar header; version caption updated to "Prototype v0.7 · Polish Step 4"
- Organisation Profile page: HTML profile card with `.flag-yes` / `.flag-no` badges for policy/governance fields
- AI Readiness and Workflow Audit pages: scale legend chip strip, `render_score_hero()` for score display, `render_section_heading()` throughout
- Risk Assessment page: `render_risk_table()` with coloured `.risk-badge` pills replacing `st.dataframe`; High/Critical safeguard alerts preserved
- Pilot Recommendation page: `render_recommendation_card()` for recommendation banner, `render_next_actions()` and `render_safeguards()` for two-column lists
- Mini Report page: consistent section headings, `render_recommendation_card()` live preview, all form widgets and download button preserved exactly
- All scoring logic, session state keys, sample loaders, `st.rerun()` calls, and test compatibility preserved — 67/67 tests still pass after rewrite

### Polish Step 3 notes (2026-06-08)

- Created `docs/deployment-notes.md` — 8 sections: purpose, prototype status, local run (with Windows note), Streamlit Community Cloud option, what not to deploy, environment variables, demo safety checklist, future production considerations, recommended current use
- Added Deployment section to `README.md` linking to `docs/deployment-notes.md` with a one-line safety reminder
- No code changes, no authentication added, no external services added

### Polish Step 2 notes (2026-06-08)

- Added `pytest` to `requirements.txt`
- Created `tests/test_scoring.py` — 38 tests covering all band boundaries for readiness (5 bands), workflow suitability (5 bands), risk level (4 bands), plus `calculate_readiness_score`, `calculate_workflow_suitability_score`, `calculate_risk_score`, and 8 `get_pilot_recommendation` cases including all specified boundary inputs
- Created `tests/test_report_generator.py` — 19 tests covering return type, all 6 section headings, data values in output, minimal-data edge case, and 8 `create_report_filename` cases including empty/whitespace/special-character inputs
- Added Running Tests section to `README.md` with `pytest` command and description
- No changes to app functionality or scoring logic

### Polish Step 1 notes (2026-06-08)

- Created `assets/screenshots/` folder with `README.md` — lists 8 expected screenshots with filename, page, what to show, data to use, and safety rules
- Rewrote `docs/screenshots-checklist.md` as a structured table with columns: done, filename, page/feature, what to show, data to use, safety reminder
- Added optional additional screenshots table (5 items) and portfolio use guidance by platform
- Added Screenshots section to `README.md` pointing to `assets/screenshots/` and `docs/screenshots-checklist.md`
- Updated folder structure in `README.md` to include `assets/screenshots/`
- No code changes, no browser automation, no app functionality changed

### Phase 7 notes (2026-06-08)

- Rewrote README.md to be presentation-ready: problem statement, why it matters, feature table, app pages table, tech stack table, folder structure, demo scenario, limitations, future improvements, Layer connections table
- Created `docs/portfolio-case-study.md` — 18-section case study including problem, target user, solution overview, architecture, tech stack, AI/API approach (explicitly: no external APIs), phase table, testing, results, business value, governance considerations, limitations, lessons learned, future improvements, portfolio summary
- Created `docs/demo-script.md` — 7-step demo walkthrough with what to show, what to say, key message, and expected output for each step; includes setup instructions, responsible-use message, and closing pitch
- Created `docs/screenshots-checklist.md` — 18-item screenshot checklist covering all pages, downloaded report, and terminal; includes safety rules, portfolio guidance, and naming convention
- Created `docs/build-reflection.md` — 12-section reflection covering what was built, what worked, what was difficult, design/safety/technical decisions, what this proves and does not prove, lessons learned, next build improvements
- Created `docs/future-improvements.md` — 4-category improvements list: short-term (8 items), medium-term (7 items), long-term (5 items), not-yet/avoid (6 items with explicit exclusions for learner data, safeguarding, and MIS integration)
- Updated build-notes.md status to "Phase 7 — complete"
- No code changes in Phase 7 — documentation only

---

## Layer Connections

| Layer | Contribution to this build |
|---|---|
| Layer 3 — Consulting methodology | Audit structure, client engagement process, recommendation framework |
| Layer 4 — Software build methodology | Technical build approach, prototype design, demo delivery |
| Layer 5 — Document intelligence | Document classification, RAG-readiness assessment |
| Layer 6 — AI Governance Lab | Risk assessment template, acceptable use policy, human review framework, staff capability scoring |
| Layer 7 — Teaching and Workshop Lab | Training needs assessment questions, programme recommendations, materials package output |

---

## Design Decisions (Phase 1)

- **Streamlit chosen** — lowest friction for a data-driven, form-based prototype; no frontend build tooling required; runs locally or deploys easily
- **No database in MVP** — all state held in `st.session_state`; keeps the prototype self-contained and portable
- **Modular `src/` layout** — scoring, report generation, sample data, and utilities separated from the main app file; easier to extend without touching `app.py`
- **Synthetic sample data** — a pre-loaded BrightPath profile allows the tool to be demonstrated without requiring a client to fill in every field first
