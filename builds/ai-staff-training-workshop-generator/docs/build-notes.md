# Build Notes — AI Staff Training and Workshop Generator

**Build 4 · BrightPath ChatGPT Mastery Project**

---

## Phase 1: Scaffold and Training Scenario Setup

**Date:** 2026-06-12
**Status:** Complete
**Tests:** 52 passed

### What Was Created

**App scaffold:**
- `app.py` — 9-page Streamlit app with wide layout and sidebar navigation
- Session state wiring: `training_scenario` and `scenario_summary`
- Home page with consulting workflow, Build 1–3 connections, responsible-use warning, and prototype notice
- Organisation Scenario page: demo load button, editable form, validation, summary cards, Markdown preview
- 7 placeholder pages for Phases 2–8

**Source modules:**
- `src/sample_data.py` — `get_brightpath_training_scenario()`, `get_default_priority_topics()`, `get_default_staff_roles()`, `get_responsible_ai_topic_descriptions()`
- `src/scenario_manager.py` — `validate_training_scenario()`, `summarise_training_scenario()`, `format_scenario_as_markdown()`, `create_scenario_from_form_data()`
- `src/ui_components.py` — `render_page_header()`, `render_responsible_use_warning()`, `render_prototype_notice()`, `render_info_card()`, `render_status_box()`
- Phase 2–8 placeholder stubs: `needs_assessment.py`, `workshop_planner.py`, `activity_generator.py`, `facilitator_guide.py`, `handout_generator.py`, `knowledge_check.py`, `training_pack.py`

**Tests:**
- `tests/test_sample_data.py` — 25 tests covering scenario data, topic lists, roles, and descriptions
- `tests/test_scenario_manager.py` — 34 tests covering validation, summarisation, formatting, and form data
- `tests/test_training_pack.py` — 13 tests covering placeholder module import and basic function contracts

**Documentation:**
- `README.md` — presentation-ready project documentation
- `docs/architecture.md` — layered architecture overview and data flow
- `docs/safety-boundaries.md` — full responsible-use statement
- `docs/demo-script.md` — Phase 1 demo walkthrough
- `docs/future-improvements.md` — full phase roadmap

### Responsible-Use Controls in Phase 1

- All scenario data is synthetic (BrightPath is fictional)
- No external AI API calls — dependencies are `streamlit`, `pandas`, `pytest` only
- Responsible-use warning rendered on every page
- Prototype notice rendered on Home page
- `safety-boundaries.md` documents prohibited uses clearly

### Design Decisions

- 9-page structure maps one-to-one to the consulting workflow — makes the prototype self-documenting
- `sample_data.py` separates data from logic — easy to extend with new synthetic scenarios in later phases
- `scenario_manager.py` is pure Python with no Streamlit imports — makes it fully testable without mocking
- `ui_components.py` wraps Streamlit calls — consistent UI behaviour across all pages
- Placeholder stubs for Phases 2–8 confirm the module structure and allow placeholder tests to verify import contracts

### Next Steps

Phase 3: Workshop Planner — structured agenda and learning outcomes.

---

## Phase 2: Training Needs Assessment

**Date:** 2026-06-12
**Status:** Complete
**Tests:** 144 passed (79 from Phase 1 + 65 new)

### What Was Implemented

**`src/needs_assessment.py`** — full implementation replacing the Phase 1 placeholder:
- `get_training_topic_catalogue()` — 13-topic catalogue with title, description, risk_level, why_it_matters, example_staff_behaviour, and recommended_training_angle
- `assess_topic_priority(scenario, topic)` — deterministic priority scoring (high / medium / low) based on scenario priority_topics list and concern keywords
- `generate_training_needs_assessment(scenario)` — full assessment dict covering topic assessments, role-specific needs, learning outcomes, risk summary, session type, and responsible-use note
- `generate_learning_outcomes(scenario, priority_topics)` — 5–8 outcome strings from a template bank keyed to priority topics
- `generate_role_specific_needs(scenario)` — role-specific training needs for tutors, administrators, team leaders, quality lead, curriculum leads, assessors, and a generic fallback
- `summarise_training_needs(assessment)` — compact summary dict for metric cards
- `format_needs_assessment_as_markdown(assessment)` — full Markdown export with all required sections

**`app.py`** — Training Needs Assessment page made functional:
- Setup guide shown when no scenario is loaded (4-step instructions)
- Scenario context bar (organisation, staff count, delivery mode)
- Generate button with spinner
- Summary metric cards (priority topics, high priority count, staff roles, learning outcomes)
- Topic priorities table (Pandas DataFrame)
- Learning outcomes list
- Role-specific needs expandable sections
- Risk summary info box
- Responsible-use warning
- Markdown download button

**`tests/test_needs_assessment.py`** — 65 new tests across 7 test classes

### Design Decisions

- Priority logic is transparent and deterministic: a topic is high priority if it appears in the scenario's priority_topics list OR if it's in the hard-coded high-risk set and matches a concern keyword
- Role needs library (`_ROLE_NEEDS`) is a static dict — easy to extend in later phases with scenario-specific content
- Learning outcomes are template-matched to priority topics — ensures outcomes are specific and actionable, not generic
- `assess_topic_priority` also surfaces catalogue topics not in priority_topics if they score high — prevents gaps in the assessment
- Topic assessments are sorted high → medium → low for clean display

### Responsible-Use Controls in Phase 2

- All assessment logic operates on synthetic scenario data only
- `responsible_use_note` is included in every generated assessment and Markdown export
- Responsible-use warning rendered on the page
- No external API calls — all logic is deterministic Python

---

## Phase 3: Workshop Planner

**Date:** 2026-06-12
**Status:** Complete
**Tests:** 235 passed (144 from Phases 1–2 + 91 new)

### What Was Implemented

**`src/workshop_planner.py`** — full implementation replacing the Phase 1 placeholder:
- `normalise_duration_to_minutes(duration)` — converts strings ("90 minutes", "1 hour 30 minutes", "1.5 hours") and integers to int minutes, defaults to 90
- `create_workshop_title(scenario, assessment)` — sector and goal-aware title generation
- `get_default_workshop_resources(delivery_mode)` — mode-specific resource list (in-person, online, hybrid)
- `get_default_workshop_ground_rules()` — 6 standard workshop ground rules
- `generate_learning_outcome_section(scenario, assessment)` — uses assessment outcomes if available, falls back to role-sensitive defaults
- `generate_timed_agenda(scenario, assessment, duration_minutes)` — 7 proportionally-weighted blocks that scale for 60, 90, or 120 minutes; each item includes time_range, section_title, purpose, trainer_activity, participant_activity, key_message, materials
- `generate_trainer_notes(scenario, assessment)` — scenario-aware and assessment-aware practical trainer notes
- `generate_discussion_prompts(scenario, assessment)` — 8 facilitated discussion prompts with sector variation
- `generate_follow_up_actions(scenario, assessment)` — 8 post-workshop organisation actions
- `generate_workshop_plan(scenario, assessment, duration_minutes, delivery_mode)` — assembles complete plan dict
- `summarise_workshop_plan(workshop_plan)` — compact summary for metric cards
- `format_workshop_plan_as_markdown(workshop_plan)` — full Markdown export with all required sections
- `create_workshop_plan_filename(title)` — safe kebab-case filename

**`app.py`** — Workshop Planner page made functional:
- Setup guide if scenario is missing
- Info note if training needs assessment not yet run (plan still generates from scenario)
- Duration selector (60 / 90 / 120 minutes)
- Delivery mode selector (In-person / Online / Hybrid)
- Generate button with spinner
- Summary metric cards (duration, agenda sections, learning outcomes, follow-up actions)
- Compact agenda table (Pandas DataFrame)
- Expandable detailed agenda sections
- Resources, trainer notes, discussion prompts, responsible-use messages
- Follow-up actions
- Markdown download

**`tests/test_workshop_planner.py`** — 91 new tests across 9 test classes

### Design Decisions

- Agenda blocks use a `weight` system so they scale proportionally to any duration — no hard-coded minute values per block
- Last block absorbs timing remainder to ensure the agenda sums cleanly to the chosen duration
- `normalise_duration_to_minutes` handles all common human-entered formats — robust to inconsistent user input
- Delivery mode drives resource list — online workshops get different tools than in-person ones
- Workshop plan stores `prototype_note` — included in every Markdown export as a non-negotiable responsible-use statement

### Next Steps

Phase 4: Activity Generator — safe/unsafe prompt sorting, risky prompt rewrite, hallucination review, learner data boundary, safeguarding escalation, human review checklist.

---

## Phase 4: Activity Generator

**Date:** 2026-06-12
**Status:** Complete
**Tests:** 337 passed (235 from Phases 1–3 + 102 new)

### What Was Implemented

**`src/activity_generator.py`** — full implementation replacing the Phase 1 placeholder:
- `get_activity_type_catalogue()` — 8-type catalogue with title, type, recommended_duration, description
- `get_default_activity_types()` — 6 default activities for BrightPath demo
- `create_safe_unsafe_prompt_sorting_activity()` — 6 scenario cards (SAFE/RISKY/PROHIBITED) with expected classifications and reasons
- `create_risky_prompt_rewrite_activity()` — 2 risky prompt cards with original prompt, problem, safe rewrite, and what changed
- `create_hallucination_review_activity()` — 2 AI output cards with hallucination flags and remediation steps
- `create_learner_data_boundary_activity()` — 3 scenario cards with boundary rules and correct actions
- `create_safeguarding_escalation_activity()` — 2 scenario cards with DSL escalation guidance
- `create_human_review_checklist_activity()` — 8-item checklist with scenario application card
- `create_approved_tools_decision_activity()` — 4 cards with APPROVED/ESCALATE/STOP decisions
- `create_bias_fairness_review_activity()` — 2 AI output cards with bias flags and fair rewrites
- `generate_training_activities()` — assembles list from selected activity types; handles None scenario/assessment/plan
- `summarise_training_activities()` — compact summary for metric cards
- `format_activity_as_markdown()` — single activity as Markdown
- `format_activities_as_markdown()` — full document with summary, all activities, and responsible-use boundaries
- `create_activities_filename()` — kebab-case filename

**`app.py`** — Activity Generator page made functional:
- Setup guide if scenario missing
- Info note if Training Needs Assessment or Workshop Plan not yet run
- Multiselect for activity types (default BrightPath selection pre-loaded)
- Generate button with spinner
- Summary metric cards (activities, est. time, activity types, target roles)
- Expandable activity sections with all fields
- Markdown download button
- Session state keys: `training_activities`, `training_activities_markdown`, `training_activities_filename`

**`tests/test_activity_generator.py`** — 102 new tests across 11 test classes

### Design Decisions

- Each activity function is independent — any combination of activities can be generated
- All scenario cards use synthetic, fictional content — no real learner, safeguarding, or HR examples
- `risk_warnings` and `responsible_use_note` are included in every activity — cannot be omitted
- Activity catalogue maps directly to creator functions via dict — easy to extend in later phases
- `generate_training_activities` falls back to default types if selected_activity_types is empty
- None scenario handled gracefully — activity functions use empty dicts and return sensible defaults

### Responsible-Use Controls in Phase 4

- All activity scenario cards are synthetic and fictional
- Safeguarding escalation activity explicitly includes safeguarding-specific risk warnings
- Markdown export includes a Prototype and Responsible-Use Boundaries section as a non-negotiable statement
- No external API calls — all generation is deterministic Python

### Next Steps

Phase 5: Facilitator Guide — opening/closing scripts, section delivery notes, activity facilitation notes, misconceptions, debrief guidance.

---

## Phase 5: Facilitator Guide Generator

**Date:** 2026-06-12
**Status:** Complete
**Tests:** 456 passed (337 from Phases 1–4 + 119 new)

### What Was Implemented

**`src/facilitator_guide.py`** — full implementation replacing the Phase 1 placeholder:
- `get_default_facilitator_principles()` — 8 core principles for responsible AI facilitation
- `get_facilitator_preparation_checklist()` — 11-item pre-session preparation checklist
- `generate_opening_script(scenario, workshop_plan)` — scenario-aware opening with ground rules
- `generate_closing_script(scenario, workshop_plan)` — recap-and-commitments closing
- `generate_section_delivery_notes(scenario, assessment, workshop_plan)` — 6 section-by-section notes with facilitator goal, what to say, what to ask, expected responses, watch-out-for, and transition
- `generate_activity_facilitation_notes(activities)` — maps activity dicts to facilitator notes; falls back to default Safe vs Unsafe prompt sorting note if no activities provided
- `generate_common_misconceptions(scenario, assessment)` — 7 misconceptions with why-it-is-risky and facilitator-response
- `generate_debrief_guidance(scenario, activities)` — 8 step-by-step debrief instructions
- `generate_facilitator_risk_warnings(scenario, assessment)` — 10 facilitator-specific warnings (including assessment-driven high-priority warning)
- `generate_facilitator_discussion_prompts(scenario, assessment, workshop_plan)` — 8–10 prompts, deduped against workshop plan
- `generate_facilitator_guide()` — assembles complete guide dict
- `summarise_facilitator_guide()` — compact summary for metric cards
- `format_facilitator_guide_as_markdown()` — full document with all required sections
- `create_facilitator_guide_filename()` — kebab-case filename

**`app.py`** — Facilitator Guide page made functional:
- Setup guide if scenario missing
- Info note listing which of assessment/workshop plan/activities are not yet run
- Generate button with spinner
- Summary metric cards (duration, sections, activities, misconceptions)
- Session purpose, principles, preparation checklist
- Opening/closing scripts in expandable sections
- Section delivery notes, activity facilitation notes, misconceptions in expandable sections
- Debrief guidance, risk warnings, Markdown download
- Session state keys: `facilitator_guide`, `facilitator_guide_markdown`, `facilitator_guide_filename`

**`tests/test_facilitator_guide.py`** — 119 new tests across 11 test classes

### Design Decisions

- `generate_section_delivery_notes` uses a fixed 6-section template that mirrors the workshop agenda blocks — consistent mapping from plan to guide
- `generate_activity_facilitation_notes` mirrors the activity structure exactly — facilitator notes and activities stay in sync
- Misconceptions include a `facilitator_response` that cross-references the activity cards — actionable, not just advisory
- Opening and closing scripts are parameterised by scenario and workshop_plan duration — can be read aloud without editing
- `generate_debrief_guidance` appends activity-aware guidance if activities are present — richer debrief when full session is run

### Responsible-Use Controls in Phase 5

- Opening script explicitly sets synthetic-only ground rules at the start of the session
- Preparation checklist requires confirming DPO, safeguarding lead, and approved tools before the session
- Risk warnings include a real-time safeguarding event protocol (redirect immediately if real concern raised)
- `prototype_note` is included in every generated guide and Markdown export as a non-negotiable statement

### Next Steps

Phase 6: Staff Handout — AI safe-use reference for workshop attendees.

---

## Phase 6: Staff Handout Generator

**Date:** 2026-06-12
**Status:** Complete
**Tests:** 573 passed (456 from Phases 1–5 + 117 new)

### What Was Implemented

**`src/handout_generator.py`** — full implementation replacing the Phase 1 placeholder:
- `get_default_safe_use_principles()` — 8 core safe-use rules for all staff
- `generate_allowed_ai_uses(scenario, assessment)` — practical allowed uses; scenario- and sector-parameterised with optional assessment enrichment
- `generate_prohibited_ai_uses(scenario, assessment)` — prohibited uses including learner data, safeguarding, HR, personal data, unapproved tools, AI decision-making; assessment-enriched for hallucination and bias priority topics
- `generate_safe_prompt_examples(scenario, activities)` — 4 base safe examples; optionally augmented with activity card examples from Phase 4 Safe vs Unsafe activity
- `generate_unsafe_prompt_examples(scenario, activities)` — 4 base unsafe examples including learner PII, safeguarding decision, HR, assessment; optionally augmented from activity PROHIBITED cards
- `generate_safer_rewritten_prompt_examples(scenario, activities)` — 3 base safer rewrites with what_changed lists; optionally augmented from Phase 4 risky_prompt_rewrite activity cards
- `generate_human_review_checklist(scenario, assessment)` — 10-item checklist; assessment-enriched for high-priority hallucination and bias topics
- `generate_escalation_guidance(scenario, assessment)` — 5 escalation items covering safeguarding, data protection, inaccurate output, unapproved tools, and AI-decision risks
- `generate_key_takeaways(scenario, assessment)` — 7 base takeaways; assessment-enriched for hallucination and bias topics
- `generate_staff_handout()` — assembles complete 15-key handout dict
- `summarise_staff_handout()` — compact summary for metric cards
- `format_staff_handout_as_markdown()` — full Markdown export with all required sections and `- [ ]` checklist formatting
- `create_staff_handout_filename()` — kebab-case filename with regex sanitisation

**`app.py`** — Staff Handout page made functional:
- Setup guide if scenario missing
- Info note listing which of assessment/workshop plan/activities/facilitator guide are not yet run
- Generate button with spinner
- Summary metric cards (organisation, audience roles, safe prompts, unsafe prompts, escalation items)
- Handout title, audience, purpose
- Safe-use principles
- Allowed and prohibited AI uses
- Safe, unsafe, and safer-rewritten prompt examples in expandable sections
- Human review checklist with ☐ formatting
- Escalation guidance in expandable sections
- Key takeaways
- Responsible-use warning
- Markdown download button
- Session state keys: `staff_handout`, `staff_handout_markdown`, `staff_handout_filename`

**`tests/test_handout_generator.py`** — 117 new tests across 9 test classes

### Design Decisions

- All activity-based enrichment is optional and additive — handout functions accept `None` for activities and still return sensible defaults
- Safe prompt examples use explicit "Do not include names, personal details, or case-specific information" wording in the prompt text itself — modelling safe behaviour, not just describing it
- Unsafe prompt examples use plausible staff-behaviour scenarios (not contrived) so they are recognisable in real use
- Safer rewrites follow a three-field structure (unsafe_prompt, safer_prompt, what_changed list) matching the Phase 4 risky_prompt_rewrite activity structure — consistent across the training pack
- Human review checklist uses `- [ ]` Markdown checkbox format — suitable for a printed or digital handout
- Escalation guidance uses the organisation's name in who_to_contact — personalises the handout to the scenario

### Responsible-Use Controls in Phase 6

- All prompt examples are synthetic — no real learner, safeguarding, HR, or personal data
- Prototype note is included in every generated handout and Markdown export
- Handout purpose statement explicitly labels examples as synthetic
- `responsible_use_warning` is included at the end of the displayed handout and the Markdown export

### Next Steps

Phase 7: Knowledge Check — quiz questions, scenario questions, answer key.

---

## Phase 7: Knowledge Check Generator

**Date:** 2026-06-12
**Status:** Complete
**Tests:** 674 passed (573 from Phases 1–6 + 101 new)

### What Was Implemented

**`src/knowledge_check.py`** — full implementation replacing the Phase 1 placeholder:
- `get_default_question_topics()` — 10 topic strings covering safe prompting, learner data, safeguarding, approved tools, human review, hallucination, bias, accountability, escalation, prohibited uses
- `generate_multiple_choice_questions(scenario, assessment, handout, question_count)` — draws from a deterministic bank of 15 MCQs; `question_count` controls how many are returned (validated, defaults to 10); each question has question_id, topic, question, options (A/B/C/D), correct_answer, explanation
- `generate_scenario_questions(scenario, assessment, activities)` — returns 4 deterministic scenario questions covering safeguarding, learner data, hallucination, and bias/fairness; each has expected_answer_points, risk_flags, and model_answer
- `generate_short_reflection_questions(scenario, assessment)` — returns 5 base reflection questions; optionally enriched with a bias/fairness reflection question if bias is a high-priority topic in the assessment
- `generate_answer_key(mcqs, scenario_qs, reflection_qs)` — assembles answer key dict from all question types plus `marking_note`
- `generate_knowledge_check()` — assembles complete 13-key knowledge check dict
- `summarise_knowledge_check()` — compact summary for metric cards
- `format_knowledge_check_as_markdown(knowledge_check, include_answer_key)` — full Markdown export with `include_answer_key` flag to generate staff-only vs trainer versions
- `create_knowledge_check_filename()` — kebab-case filename with regex sanitisation

**`app.py`** — Knowledge Check page made functional:
- Setup guide if scenario missing
- Info note listing which upstream pages haven't run yet
- Question count selector (5 / 10 / 15 MCQs)
- Section include checkboxes (MCQs, scenarios, reflection, answer key)
- Generate button with spinner
- Summary metric cards (organisation, MCQs, scenario questions, reflection questions, answer key included)
- Knowledge check title, audience, purpose, instructions
- Multiple-choice questions in expandable sections
- Scenario questions in expandable sections
- Reflection questions listed
- Answer key in a single expander (trainer/facilitator only)
- Pass and review guidance
- Responsible-use warning
- Markdown download button
- Session state keys: `knowledge_check`, `knowledge_check_markdown`, `knowledge_check_filename`

**`tests/test_knowledge_check.py`** — 101 new tests across 8 test classes

### Design Decisions

- MCQ bank holds 15 questions — enough for 5/10/15 selection without repeating; extending the bank requires only adding to `_MCQ_BANK`
- All questions are deterministic and static — no randomisation, no shuffling; consistent output simplifies testing and facilitator preparation
- `include_answer_key` flag on `format_knowledge_check_as_markdown` allows generating two versions: a staff copy (no answers) and a trainer copy (full answers)
- Answer key uses a `marking_note` clarifying this is a learning tool, not a certification system — prevents misuse as formal assessment
- Pass guidance is dynamically calculated from `question_count` (threshold = max(count - 2, 80% of count)) — scales across 5/10/15 options
- Reflection questions have `guidance_points` rather than a single model answer — correct for qualitative, open-ended responses

### Responsible-Use Controls in Phase 7

- All scenario questions use synthetic, fictional examples — no real learner, safeguarding, or HR data
- `prototype_note` included in every generated check and Markdown export
- `marking_note` explicitly states this is not formal certification
- Responsible-use warning at end of displayed check and Markdown export

### Next Steps

Phase 8: Training Pack Export — combine all outputs into a downloadable Markdown training pack.

---

## Phase 8: Training Pack Export

**Date:** 2026-06-12
**Status:** Complete
**Tests:** 758 passed (674 from Phases 1–7 + 84 new, 13 Phase 1 placeholder tests replaced = 99 total in test_training_pack.py, net +86)

### What Was Implemented

**`src/training_pack.py`** — full Phase 8 implementation replacing the Phase 1 placeholder:
- `get_training_pack_required_sections()` — returns `["scenario"]` as the single required section
- `get_training_pack_optional_sections()` — returns all 11 optional/recommended section keys
- `check_training_pack_readiness(session_state)` — inspects session state for all 7 recommended data keys; returns `is_ready`, `available_sections`, `missing_sections`, `recommended_next_steps`
- `build_training_pack_data_from_session_state(session_state)` — collects all session state dicts and pre-rendered markdown strings into a single pack data dict; handles missing keys gracefully
- `generate_training_pack_cover_section(pack_data)` — cover page with org name, type, sector, staff roles, duration, delivery mode, generated date, prototype status, and synthetic-data notice
- `generate_training_pack_table_of_contents(include_sections)` — numbered TOC based on which sections are included
- `generate_training_pack_responsible_use_section()` — static responsible-use statement covering learner data, safeguarding, HR, personal data, and human review requirements
- `generate_training_pack_limitations_section()` — static prototype limitations list with 6 bullet points
- `generate_facilitator_review_checklist()` — 10-item pre-delivery facilitator checklist
- `generate_training_pack_next_steps(pack_data)` — 9 recommended next steps parameterised with org name
- `generate_markdown_training_pack(pack_data, include_sections)` — full Markdown assembly; uses pre-rendered markdown from session state where available, falling back to local formatting from dict; strips top-level headings before embedding; shows "No X available yet" notes for missing sections; knowledge check section strips the Answer Key sub-section (it gets its own numbered section)
- `summarise_training_pack(pack_data)` — 8-key compact summary for metric cards
- `create_training_pack_filename(organisation_name)` — kebab-case filename with regex sanitisation
- Backwards-compatible shims for `get_placeholder_message`, `assemble_training_pack`, `generate_pack_markdown` (these delegate to Phase 8 functions)

**`app.py`** — Training Pack Export page made functional:
- Readiness check via `check_training_pack_readiness` at page load (no scenario → setup steps shown)
- Readiness overview: available sections (✓) and missing sections (○) in two columns
- Section selector: 12 checkboxes in 3 columns, pre-ticked if the data is available
- Generate button with spinner
- Summary metric cards (organisation, sections available, activity count, MCQs, answer key)
- Facilitator review checklist with ☐ formatting
- Recommended next steps
- Markdown preview (first 4,000 characters) in expander
- Markdown download button
- Session state keys: `training_pack_data`, `training_pack_markdown`, `training_pack_filename`, `training_pack_readiness`

**`tests/test_training_pack.py`** — replaced Phase 1 placeholder tests with 99 Phase 8 tests across 11 test classes

### Design Decisions

- `build_training_pack_data_from_session_state` stores both the raw dicts and the pre-rendered markdown strings — `generate_markdown_training_pack` prefers the pre-rendered strings (from session state) and falls back to local formatting from the raw dicts, so the pack output matches what each individual page's download button would produce
- `_strip_top_heading` removes the first `# Heading` line from each embedded section — avoids h1 headings nested inside h2 section blocks in the combined document
- The Knowledge Check section strips the embedded Answer Key sub-section — the answer key gets its own numbered section in the training pack, avoiding duplication
- `include_sections` flag with 12 keys allows a partial pack export (e.g. staff-only copy without facilitator guide or answer key)
- Section selector pre-ticks only available data — unavailable sections are still shown but unchecked by default
- `check_training_pack_readiness` passes a `dict(st.session_state)` copy — avoids Streamlit session state type dependency in the module

### Responsible-Use Controls in Phase 8

- Cover page includes synthetic-data notice
- Dedicated Responsible-Use Boundaries section with full statement
- Facilitator review checklist explicitly confirms synthetic examples and no real data
- `prototype_note` and `responsible_use_note` included in every pack data dict and Markdown output
- Prototype Limitations section prevents misuse as a formal compliance or legal training system

### Next Steps

Phase 9: Completion review and portfolio documentation.

---

## Phase 9: Completion Review and Portfolio Notes

**Date:** 2026-06-12
**Status:** Complete
**Tests:** 758 passed (unchanged — no new source modules in this phase)

### What Was Created

**Documentation:**
- `docs/build-4-completion-review.md` — full build completion review covering all 9 phases, key features, methodologies reused, technical implementation, responsible-use boundaries, evidence of completion, what this build proves and does not prove, remaining improvements, readiness verdict, and recommended next action
- `docs/portfolio-case-study.md` — portfolio-ready case study covering problem, target user, workflow context, solution overview, architecture, tech stack, implementation process (phases 1–9), testing, results, business value, risk and governance considerations, limitations, lessons learned, future improvements, and portfolio summary
- `docs/build-reflection.md` — honest build reflection covering what worked, what was difficult, design decisions, safety and governance decisions, technical decisions, what this proves, what it does not prove, lessons learned, and next build improvements
- `docs/screenshots-checklist.md` — 11-item screenshot checklist with capture instructions, per-page guidance, and expected filenames
- `docs/deployment-notes.md` — local run instructions, dependencies, Streamlit Community Cloud notes, what not to deploy, and future production considerations
- `assets/screenshots/README.md` — screenshots index with expected filenames and capture status

**Updated files:**
- `docs/future-improvements.md` — Phase 9 marked complete in planned phases table; improvements reorganised into Short-Term, Medium-Term, Long-Term, and Not Yet / Avoid For Now sections
- `docs/safety-boundaries.md` — added "Training Materials Are Support Materials" section; expanded data protection guidance for future phases to 10 items including safeguarding review, HR review, and responsible owner
- `README.md` — full presentation-ready update: project title, one-line summary, problem statement, target users, consulting workflow, core features, app pages, responsible-use boundaries, technical stack, setup instructions, run instructions, test instructions, demo scenario, limitations, future improvements, folder structure, relationship to Builds 1–3, and portfolio positioning

### Design Decisions

- Phase 9 creates no new source modules and no new app pages — documentation only
- `docs/build-4-completion-review.md` is the canonical completion record for the build; `docs/portfolio-case-study.md` is the version optimised for LinkedIn / GitHub / client sharing
- Screenshots are not generated automatically — they are captured manually from the running app using synthetic BrightPath scenario only
- Safety boundaries update adds the "Training Materials Are Support Materials" section to make explicit that generated outputs are not official policy — this was implicit in earlier phases but needed to be stated clearly

### Responsible-Use Controls in Phase 9

- All documentation states clearly that Build 4 uses synthetic scenarios only
- All documentation explicitly requires human review before any output is used in a real training session
- Portfolio case study and completion review both include what this build does not prove (production readiness, real client validation, legal/safeguarding/HR/compliance approval)
- Safety boundaries update strengthens the responsible-owner requirement

### Build 4 Final Status

Build 4 is complete across all nine phases. 758 tests pass. All 9 app pages are functional. Full Markdown training pack export is available. Documentation is portfolio-ready.

**Recommended next action:** Add screenshots → light presentation polish → then decide between Build 5 (AI Training Delivery Tracker) or Build 4 enhancement (PDF/PPTX export).

---

## Polish Phase A: Professional UI, Analytics Charts, PDF/PPTX Export

**Date:** 2026-06-13
**Status:** Complete
**Tests:** 851 passed (758 from Phases 1–9 + 93 new — 51 in test_report_analytics.py, 42 in test_export_utils.py)

### What Was Implemented

**`src/report_analytics.py`** — new deterministic analytics module:
- `calculate_section_completion_status(session_state)` — {section_name: bool} from session state keys
- `calculate_training_topic_counts(pack_data)` — {topic: 1} for each priority topic
- `calculate_activity_type_counts(activities)` — {activity_type: count} from activity list
- `calculate_workshop_time_allocation(workshop_plan)` — [{section, minutes}] for agenda items
- `calculate_knowledge_check_topic_counts(knowledge_check)` — {topic: count} across MCQs and scenario questions
- `calculate_report_quality_summary(pack_data)` — completeness percentage, section count, activity count, MCQ count, answer key flag
- `build_training_pack_analytics(pack_data)` — full analytics dict combining all the above

**`src/export_utils.py`** — new PDF and PPTX export module:
- `create_safe_filename(title, extension)` — kebab-case filename sanitisation
- `format_text_for_pdf(text)` — strips Markdown formatting for PDF paragraph use
- `format_slide_text(text, max_chars)` — truncates and strips Markdown for slide bodies
- `generate_chart_images_for_training_pack(pack_data, analytics)` — generates 5 matplotlib chart types (section completion, topic coverage, activity mix, time allocation, knowledge check topics) as PNG bytes dicts
- `export_training_pack_to_pdf(pack_data, markdown_text, analytics, output_path)` — full reportlab PDF with cover page, 9 content sections, embedded chart images, responsible-use and limitations pages; returns bytes
- `export_training_pack_to_pptx(pack_data, analytics, output_path)` — 11-slide python-pptx PowerPoint with navy title slide, training context, needs, workshop plan, agenda, activities, safe-use rules, human review/escalation, knowledge check, responsible-use boundaries, next steps; returns bytes

**`src/ui_components.py`** — extended with:
- `inject_global_css()` — minimal CSS for spacing, metric label sizing, expander headers, divider colour
- `render_metric_row(metrics)` — dynamic column metric row from list of dicts
- `render_workflow_steps(steps, current_step)` — horizontal step display with active step bolded
- `render_section_card(title, body)` — titled section card
- `render_completion_badge(label, is_complete)` — inline ✓ / ○ badge with colour
- `render_download_panel(title, description)` — download section header
- `render_report_quality_notice()` — standard report quality info box
- `render_export_options_panel()` — 3-column export format description (Markdown / PDF / PowerPoint)

**`app.py`** — updated:
- Added `report_analytics as ra` and `export_utils as eu` imports
- `inject_global_css()` called at startup
- Sidebar: workflow status indicators (✓ complete / ○ pending) for all 8 pipeline steps; safety note
- Training Pack Export page: analytics section with pack completeness, 5-chart display; 3-format export panel (Markdown / PDF / PowerPoint); session state keys `training_pack_analytics`, `training_pack_pdf_bytes`, `training_pack_pptx_bytes`

**`requirements.txt`** — added `matplotlib`, `reportlab`, `python-pptx`

**`tests/test_report_analytics.py`** — 51 tests across 7 test classes
**`tests/test_export_utils.py`** — 42 tests across 6 test classes

### Design Decisions

- Charts generated on-demand in the app and reused in PDF export — no permanent chart files stored in the project
- PDF uses reportlab platypus for flow-based layout; PPTX uses python-pptx with blank slide layout and manual positioning for maximum control
- `add_notice` helper inside `export_training_pack_to_pptx` defaults `text` to a standard synthetic-data notice — slides without custom notices still get the footer
- `use_container_width=True` on download buttons gives a consistent full-width panel appearance
- Charts wrapped in `try/except` in the app — if matplotlib fails for any reason, a caption is shown rather than crashing

### Responsible-Use Controls in Polish Phase A

- PDF cover page includes synthetic-data notice in amber text
- PDF dedicated Responsible-Use Boundaries page and Prototype Limitations page preserved
- PPTX slide 10 is Responsible-Use Boundaries; slide 1 footer repeats the synthetic prototype notice
- `generate_chart_images_for_training_pack` uses only data already in pack_data — no invented statistics
- All chart labels derived from generated content keys, not from hardcoded assumptions about real organisations

### New Dependencies

| Package | Purpose |
|---|---|
| `matplotlib` | Chart image generation (PNG bytes) |
| `reportlab` | PDF generation |
| `python-pptx` | PowerPoint generation |

---

## Polish Phase B: Professional UI and PDF Reports

The app UI was polished for portfolio/client-demo use. Every generated report now supports PDF export alongside Markdown. The Training Pack Export page includes professional report presentation, report quality indicators, and analytics charts where possible.

### What Was Built

**`src/pdf_exporter.py` (new)** — reusable professional PDF export module:
- `create_safe_filename` / `normalise_report_text` — filename and text helpers
- `build_pdf_styles` — shared navy/slate ParagraphStyle sheet
- `add_pdf_cover_page`, `add_pdf_section`, `add_pdf_bullet_list`, `add_pdf_table`, `add_responsible_use_footer_section` — composable story builders
- `export_markdown_report_to_pdf_bytes` — converts generated Markdown (headings, bullets, numbered lists, tables, blockquotes, dividers) into a styled report PDF with cover page and per-page "Synthetic scenario prototype. Human review required." footer
- `export_structured_report_to_pdf_bytes` — renders report dicts directly; prefers Markdown when supplied; missing fields never crash generation

**`src/chart_utils.py` (new)** — matplotlib chart files for analytics:
- `create_section_completion_chart`, `create_activity_mix_chart`, `create_workshop_time_chart`, `create_knowledge_topic_chart` — write clean PNG bar charts to disk, return the path ("" on empty data)
- `generate_all_report_charts` — generates every available chart into `outputs/charts/`, skipping failures safely

**`src/pptx_exporter.py` (new)** — stable `export_training_pack_to_pptx_bytes` interface over the 11-slide python-pptx builder in `export_utils.py`

**`src/ui_components.py`** — `apply_global_styles()` global stylesheet (off-white canvas, navy headings, card-style metrics, polished buttons/expanders); new `render_report_preview_card`, `render_export_panel`, `render_quality_checklist`; `render_info_card` upgraded to a bordered card

**`src/report_analytics.py`** — added `calculate_priority_topic_counts` public name; fixed `calculate_workshop_time_allocation` to derive minutes from agenda `time_range` values (e.g. "00:10-00:25" → 15) so the workshop time chart now renders

**`src/export_utils.py`** — premium Training Pack PDF extended with an Executive Summary page, a Facilitator Guide section, and a Facilitator Review Checklist section (now 11 numbered sections)

**`app.py`** — every report page (Needs Assessment, Workshop Plan, Activities, Facilitator Guide, Staff Handout, Knowledge Check) now generates PDF bytes at generation time and offers a side-by-side Markdown + PDF download panel; the Training Pack PDF is generated automatically when the pack is assembled; the sidebar workflow is numbered 1–8

### Session State Keys Added

`training_needs_pdf_bytes/_filename`, `workshop_plan_pdf_bytes/_filename`, `training_activities_pdf_bytes/_filename`, `facilitator_guide_pdf_bytes/_filename`, `staff_handout_pdf_bytes/_filename`, `knowledge_check_pdf_bytes/_filename`, `training_pack_pdf_filename`

### Tests

- `tests/test_pdf_exporter.py` — 34 tests (filenames, text normalisation, styles, Markdown→PDF, structured→PDF, missing-field safety)
- `tests/test_chart_utils.py` — 15 tests (file creation, PNG magic bytes, empty-data safety)
- `tests/test_pptx_exporter.py` — 6 tests (bytes, PK magic, missing analytics safety)
- `tests/test_report_analytics.py` — +4 tests for `calculate_priority_topic_counts`
- **Total: 910 passed**

---

## Polish Phase A5: PowerPoint Training Deck Export

**Date:** 2026-06-16
**Status:** Complete
**Tests:** 953 passed (+43)

### What Was Added

A self-contained, professional 15-slide PowerPoint training deck export was implemented in `src/pptx_exporter.py`. The module replaces the previous thin wrapper with a full standalone builder.

**`src/pptx_exporter.py`** (rebuilt — standalone module):
- `create_safe_pptx_filename(title)` — kebab-case `.pptx` filename from a title string
- `format_slide_text(text, max_chars=700)` — strips Markdown formatting and truncates for slide use
- `extract_slide_bullets(items, max_items=6)` — extracts clean bullet strings from lists, dicts, or newline-delimited strings
- `add_title_slide(prs, title, subtitle, footer)` — full navy title slide
- `add_bullet_slide(prs, title, bullets, speaker_notes)` — navy title bar + up to 6 bullets + optional speaker notes
- `add_two_column_slide(prs, title, left_title, left_bullets, right_title, right_bullets)` — two-column layout with vertical divider
- `add_responsible_use_slide(prs)` — responsible-use boundaries slide with red left accent
- `export_training_pack_to_pptx_bytes(pack_data, analytics)` — 15-slide deck builder; returns bytes for `st.download_button`

**Deck structure (15 slides):**
1. Title (org name, date, prototype notice)
2. Organisation Context (overview + main concerns)
3. Training Need (learning outcomes)
4. Priority Topics (HIGH and MEDIUM priority)
5. Workshop Plan (details + responsible-use messages)
6. Workshop Agenda (timed session)
7. Training Activities (list + activity mix)
8. What Staff CAN Use AI For
9. What Staff Must NOT Do
10. Human Review Checklist
11. Escalation Guidance
12. Knowledge Check (overview + topics)
13. Pack Completion (section status + quality reminders)
14. Responsible-Use Boundaries (red accent)
15. Recommended Next Steps

**Design:** Dark navy title bars, off-white slide body, muted blue text accents, maximum 6 bullets per slide, speaker notes on key slides, per-slide prototype footer.

**`app.py`** changes:
- PPTX is now auto-generated when "Generate Training Pack" is clicked (stored in `training_pack_pptx_bytes` and `training_pack_pptx_filename`)
- Analytics generation split into its own try/except block so PPTX and PDF failures are independent
- Export panel shows "Download PowerPoint Training Deck" directly when auto-generated; "Generate PowerPoint" button appears only as a retry if auto-generation failed
- Filename uses `ppt.create_safe_pptx_filename` instead of `eu.create_safe_filename`

### Tests

`tests/test_pptx_exporter.py` (rebuilt — 49 tests across 5 classes):
- `TestCreateSafePptxFilename` (6 tests) — extension, slugification, edge cases
- `TestFormatSlideText` (10 tests) — Markdown stripping, truncation, ellipsis, None/non-string
- `TestExtractSlideBullets` (9 tests) — lists, strings, dicts, max_items, empty/None
- `TestSlideBuilders` (10 tests) — each helper adds one slide, empty inputs, speaker notes, accumulation
- `TestExportTrainingPackToPptxBytes` (14 tests) — bytes, PK magic, 15 slides, missing sections, None input, analytics variants

**Total: 953 passed**

### Responsible-Use Controls

- Every slide carries the per-slide footer: "Synthetic scenario prototype. Human review required before use."
- Slides 8 and 9 explicitly separate allowed and prohibited AI uses
- Slide 14 (Responsible-Use Boundaries) has a red accent bar to visually distinguish it
- No external AI API calls; no real data anywhere in the pipeline

### Responsible-Use Controls

- Every PDF carries a cover-page prototype notice, a Responsible-Use Boundaries section, and a per-page footer: "Synthetic scenario prototype. Human review required."
- Analytics remain deterministic content-coverage indicators — no invented performance data, no training-effectiveness claims
- No external AI API calls; no real data anywhere in the pipeline
