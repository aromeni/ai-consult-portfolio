# Architecture — AI Staff Training and Workshop Generator

**Build 4 · BrightPath ChatGPT Mastery Project**

---

## Overview

Build 4 is a locally-run, multi-page Streamlit application. It follows the same
responsible-use and prototype principles as Builds 1, 2, and 3 — deterministic
logic, synthetic data, no external AI API calls, and human review required for all outputs.

---

## Layer Overview

```
App Layer (Streamlit)
  app.py — multi-page navigation, session state management

Scenario Layer
  src/sample_data.py       — synthetic scenario data and topic descriptions
  src/scenario_manager.py  — validation, summarisation, formatting

Generation Modules (Phases 2–8)
  src/needs_assessment.py   — training needs scoring (Phase 2)
  src/workshop_planner.py   — agenda generation (Phase 3)
  src/activity_generator.py — activity generation (Phase 4)
  src/facilitator_guide.py  — trainer guide generation (Phase 5)
  src/handout_generator.py  — staff handout generation (Phase 6)
  src/knowledge_check.py    — quiz and check generation (Phase 7)
  src/training_pack.py      — pack assembly and export (Phase 8)

UI Helpers
  src/ui_components.py      — reusable Streamlit rendering helpers

Workshop Planner Layer (Phase 3)
  src/workshop_planner.py   — title, agenda, resources, trainer notes, prompts, export

Export Layer
  outputs/training_packs/   — saved Markdown training packs (Phase 8+)

Tests
  tests/                    — pytest test suite for all src modules
```

---

## Session State

`st.session_state` carries scenario data forward so each page can consume it:

| Key | Type | Set by |
|---|---|---|
| `training_scenario` | dict | Organisation Scenario page |
| `scenario_summary` | dict | Organisation Scenario page |

Phase 2 added: `training_needs_assessment`, `training_needs_markdown`.
Phase 3 added: `workshop_plan`, `workshop_plan_markdown`, `workshop_plan_filename`.
Phase 4 added: `training_activities`, `training_activities_markdown`, `training_activities_filename`.
Phase 5 added: `facilitator_guide`, `facilitator_guide_markdown`, `facilitator_guide_filename`.
Phase 6 added: `staff_handout`, `staff_handout_markdown`, `staff_handout_filename`.
Phase 7 added: `knowledge_check`, `knowledge_check_markdown`, `knowledge_check_filename`.
Phase 8 added: `training_pack_data`, `training_pack_markdown`, `training_pack_filename`, `training_pack_readiness`.

---

## Training Needs Assessment Layer

`src/needs_assessment.py` — implemented in Phase 2.

The app reads the saved synthetic organisation scenario from `st.session_state["training_scenario"]`
and passes it to `generate_training_needs_assessment()`.

Priority topics are mapped to deterministic training needs using two mechanisms:
1. A 13-topic catalogue with risk levels, training angles, and example staff behaviours
2. A priority scoring function that marks topics as high / medium / low based on the scenario's priority_topics list and concern keywords

Role-specific needs and learning outcomes are generated from template libraries —
no external AI calls, no LLM inference. The output is a structured Python dict
that feeds the UI, populates the Markdown export, and is stored in
`st.session_state["training_needs_assessment"]` for use in later phases
(workshop planning, activities, facilitator guide, handout, knowledge check, training pack export).

---

## Training Pack Export Layer

`src/training_pack.py` — implemented in Phase 8.

The app reads all saved outputs from session state via `build_training_pack_data_from_session_state()`,
which collects both the raw dicts and the pre-rendered markdown strings from each prior phase.

The training pack is assembled without external AI calls through four mechanisms:
1. A readiness check that identifies available and missing sections before generation
2. A section selector that pre-ticks available sections and allows the trainer to choose which to include
3. A `generate_markdown_training_pack()` function that assembles sections in order, preferring pre-rendered markdown from session state and falling back to local dict formatting for any section
4. Fixed sections for cover page, responsible-use boundaries, prototype limitations, facilitator review checklist, and recommended next steps

The `include_sections` parameter allows partial pack generation — for example, a staff copy without the facilitator guide or answer key.

Missing sections display a clear "No X available yet. Run the X page to include this section." note — the pack never crashes on missing data.

Markdown export is supported in Phase 8. PDF export remains a future improvement.

The output is stored in `st.session_state["training_pack_markdown"]` for download.

---

## Knowledge Check Layer

`src/knowledge_check.py` — implemented in Phase 7.

The app reads the saved synthetic organisation scenario and optionally the Training Needs Assessment,
Workshop Plan, Training Activities, Facilitator Guide, and Staff Handout, then passes them to `generate_knowledge_check()`.

The knowledge check is generated without external AI calls through three mechanisms:
1. A deterministic bank of 15 multiple-choice questions covering 10 responsible-AI topic areas — questions are selected by count (5, 10, or 15)
2. A fixed bank of 4 scenario questions covering safeguarding, learner data, hallucination, and bias — each with expected answer points, risk flags, and a model answer
3. A bank of 5 reflection questions (optionally enriched for high-priority assessment topics)

The `format_knowledge_check_as_markdown` function accepts an `include_answer_key` flag — allowing a staff copy (questions only) and a trainer copy (full answer key) to be generated from the same dict.

The output is stored in `st.session_state["knowledge_check"]` and `st.session_state["knowledge_check_markdown"]`
for use in Phase 8 (training pack export).

---

## Staff Handout Layer

`src/handout_generator.py` — implemented in Phase 6.

The app reads the saved synthetic organisation scenario and optionally the Training Needs Assessment,
Workshop Plan, Training Activities, and Facilitator Guide, then passes them to `generate_staff_handout()`.

The staff handout is generated without external AI calls through three mechanisms:
1. Fixed safe-use principles, prohibited-use rules, and human review checklist — consistent across all scenarios
2. Scenario-parameterised allowed uses, escalation guidance, and key takeaways — personalised to the organisation, sector, and staff roles
3. Optional activity-based enrichment — safe prompt examples, unsafe prompt examples, and safer rewrites are augmented with real cards from Phase 4 activity dicts (if available)

All prompt examples are synthetic and fictional — no real learner, safeguarding, HR, or personal data.

The output is stored in `st.session_state["staff_handout"]` and `st.session_state["staff_handout_markdown"]`
for use in later phases (knowledge check, training pack export).

---

## Facilitator Guide Layer

`src/facilitator_guide.py` — implemented in Phase 5.

The app reads the saved synthetic organisation scenario and optionally the Training Needs Assessment,
Workshop Plan, and Training Activities, then passes them to `generate_facilitator_guide()`.

The facilitator guide is generated without external AI calls through four mechanisms:
1. Fixed facilitator principles and preparation checklist — consistent across all scenarios
2. Scenario-parameterised scripts (opening and closing) with synthetic-data ground rules built in
3. Section delivery notes that mirror the 6 workshop agenda blocks — each with what to say, what to ask, expected responses, and watch-out-for
4. Activity facilitation notes mapped directly from the generated activity dicts

The output is stored in `st.session_state["facilitator_guide"]` and
`st.session_state["facilitator_guide_markdown"]` for use in later phases
(staff handout, knowledge check, training pack export).

---

## Activity Generator Layer

`src/activity_generator.py` — implemented in Phase 4.

The app reads the saved synthetic organisation scenario and optionally the Training Needs Assessment
and Workshop Plan, then passes them to `generate_training_activities()`.

Activities are generated without external AI calls through two mechanisms:
1. An 8-type activity catalogue with fixed type, duration, and description metadata
2. Individual activity creator functions that produce fully-populated activity dicts with trainer instructions, participant instructions, scenario cards, expected answers, debrief questions, key takeaways, and risk warnings

All scenario cards, example prompts, and AI outputs are synthetic and fictional — no real learner,
safeguarding, or HR data. Every activity includes `risk_warnings` and `responsible_use_note`.

The output is stored in `st.session_state["training_activities"]` and
`st.session_state["training_activities_markdown"]` for use in later phases
(facilitator guide, staff handout, knowledge check, training pack export).

---

## Workshop Planner Layer

`src/workshop_planner.py` — implemented in Phase 3.

The app reads the saved synthetic organisation scenario and the optional Training Needs Assessment
and passes them to `generate_workshop_plan()`.

The workshop plan is generated without external AI calls through four mechanisms:
1. A 7-block agenda template weighted proportionally to the chosen duration (60 / 90 / 120 min)
2. Learning outcomes sourced from the Training Needs Assessment if available, otherwise role-sensitive defaults
3. Trainer notes, discussion prompts, and follow-up actions derived from scenario concern and role data
4. Resource lists tailored to the delivery mode (in-person / online / hybrid)

The output is stored in `st.session_state["workshop_plan"]` and `st.session_state["workshop_plan_markdown"]`
for use in later phases (activities, facilitator guide, handout, knowledge check, training pack export).

---

## Data Flow (Phase 1)
```
Scenario → Needs Assessment → Workshop Plan → Activities
  → Facilitator Guide → Staff Handout → Knowledge Check
  → Training Pack (assembled + Markdown export)
```

---

## Polish and Export Layer

`src/report_analytics.py` and `src/export_utils.py` — added in Polish Phase A.

**Report analytics** calculates deterministic summaries from content already in pack_data — section completion flags, topic counts, activity type counts, workshop time allocation, knowledge check topic distribution, and overall pack completeness. No external data. No invented statistics.

**Export utilities** generates three output formats from the same pack_data:
- Markdown (Phase 8, unchanged)
- PDF — reportlab with cover page, 9 content sections, embedded charts, responsible-use and limitations pages
- PPTX — 11-slide python-pptx presentation with navy title slide and professional layout

Charts (section completion, topic coverage, activity mix, time allocation, knowledge check topics) are generated as matplotlib PNG bytes and embedded in the PDF and displayed in the Streamlit app. All export functions return bytes suitable for `st.download_button`.

All exports carry the synthetic-data notice and human-review requirement. PDF and PPTX are presentation aids — not certified training documents.

---

## PPTX Export Layer

`src/pptx_exporter.py` — added in Polish Phase A, rebuilt as standalone in Polish Phase A5.

A self-contained 15-slide PowerPoint training deck builder. Converts the generated training pack data into a professional PPTX presentation for demo and portfolio review.

- Uses `python-pptx` only — no external AI API calls
- All content comes from synthetic generated data already in `pack_data` and `analytics`
- Utility functions (`format_slide_text`, `extract_slide_bullets`) handle varied input shapes gracefully
- Public slide builders (`add_title_slide`, `add_bullet_slide`, `add_two_column_slide`, `add_responsible_use_slide`) can be composed independently for future deck variants
- `export_training_pack_to_pptx_bytes` returns bytes suitable for `st.download_button`
- Missing sections produce placeholder text — the export never crashes on incomplete data
- Every slide carries a footer: "Synthetic scenario prototype. Human review required before use."

---

## Professional UI and Export Layer

Added in Polish Phase B.

```
src/ui_components.py    — reusable presentation components and apply_global_styles()
src/pdf_exporter.py     — reusable professional PDF generation for every report
src/chart_utils.py      — matplotlib chart files (outputs/charts/)
src/pptx_exporter.py    — stable PPTX interface for the full training pack
src/report_analytics.py — deterministic content analytics
```

- **`ui_components.py`** provides page headers, responsible-use warnings, info cards, status boxes, metric rows, workflow steps, completion badges, report preview cards, export panels, and quality checklists — modern SaaS dashboard presentation with Streamlit-native components plus light CSS.
- **`pdf_exporter.py`** converts each report's generated Markdown into a professional PDF: cover page (title, organisation, date, prototype status), styled headings, bullet lists, tables, responsible-use boundaries, and a per-page prototype footer. Used by all six report pages.
- **`report_analytics.py`** computes deterministic coverage analytics from generated content only — section completion, priority topics, activity mix, workshop time allocation, knowledge check topics, and pack quality.
- **`chart_utils.py`** renders those analytics as clean matplotlib bar charts written to `outputs/charts/`; chart failures never block PDF export.
- All outputs remain based on synthetic scenario content. **PDF reports require human review before real-world use.**

---

## Generation Approach

All content generation is **deterministic and template-based** — no external LLM APIs.

- Phase 2: scores and ranks topics based on scenario concerns and sector
- Phase 3: generates agenda segments from topic list and training duration
- Phase 4: selects activities from a deterministic activity bank keyed to topics
- Phase 5: generates trainer notes from activity and topic templates
- Phase 6: generates handout sections from topic description library
- Phase 7: generates quiz questions from a question bank keyed to topics
- Phase 8: assembles all outputs into a Markdown training pack
- Polish A: analytics computed from generated content; PDF/PPTX assembled from pack_data dicts

This approach mirrors Build 3's deterministic RAG — honest about what the system
knows, grounded in templates and evidence, no hallucination risk.

---

## External AI API Usage

**None in any phase of Build 4.**

Future optional extension: Ollama-assisted generation with strict grounding controls
(noted in `docs/future-improvements.md`). This would require explicit user consent
and would not be enabled by default.

---

## No Database, No Authentication

This is a single-session, local prototype. All state lives in `st.session_state`
and is lost on app restart. No database, no authentication, no cloud storage.

---

*Build 4 · AI Staff Training and Workshop Generator · BrightPath ChatGPT Mastery Project*
