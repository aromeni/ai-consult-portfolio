# Portfolio Case Study — AI Staff Training and Workshop Generator

**Build 4 · BrightPath ChatGPT Mastery Project**

---

## One-Line Summary

A locally-run Streamlit prototype that turns an AI adoption scenario into a complete, downloadable responsible AI staff training pack — using deterministic logic, synthetic scenarios, and no external AI APIs.

---

## Problem

Organisations completing an AI readiness audit face an immediate, practical next step: they need to train their staff. But:

- Writing training materials from scratch is time-consuming and requires specialist knowledge
- Generic AI awareness training does not address the organisation's specific concerns, sector risks, or staff roles
- Training materials for regulated contexts (education, healthcare, public sector) require careful responsible-use framing
- Small organisations typically do not have a dedicated L&D team to commission custom materials
- Consultants who deliver AI audits are often asked "what do we do now?" — and need a practical, demonstrable answer

---

## Target User

| User | Role |
|---|---|
| AI consultants | Demonstrating a training material generation workflow to clients after an AI readiness audit |
| Trainers and L&D practitioners | Generating scenario-tailored training drafts as a starting point for review and delivery |
| Governance leads and managers | Understanding what responsible AI staff training looks like in practice |
| Developers / researchers | Studying deterministic content generation patterns for AI-adjacent tools |

Primary user: **Rashid** — AI consultant using this to demonstrate a consulting-grade training workflow to prospective clients.

---

## Workflow Context

Build 4 sits at the end of a four-build AI consulting chain:

| Build | What it does | How it feeds Build 4 |
|---|---|---|
| Build 1 — AI Readiness Audit | Diagnoses AI readiness, workflow gaps, staff concerns, risk themes | Identifies training priorities that inform the needs assessment |
| Build 2 — Document Intelligence | Extracts evidence from policy documents, builds topic summaries | Policy themes that could ground training content |
| Build 3 — Semantic RAG Policy Assistant | Retrieves semantically relevant policy evidence, generates grounded answers | Policy-grounded evidence that could enrich training activities |
| **Build 4 — AI Staff Training Generator** | Turns audit findings and policy context into a complete training pack | — |

> **Audit → Document Intelligence → Semantic RAG → Staff Training**

---

## Goals

1. Demonstrate how an AI consultant can take a synthetic organisation scenario and generate a structured, responsible AI staff training pack
2. Prove that training material generation can be deterministic and locally-run — no LLM API calls required
3. Embed responsible-use controls at every stage: synthetic data, human review requirement, clear limitations
4. Produce a portfolio-ready, testable, runnable prototype across eight functional phases

---

## Success Criteria

- All 9 app pages functional
- Markdown training pack downloadable from the Training Pack Export page
- Responsible-use boundaries visible on every generated output
- pytest test suite passing (target: 700+ tests)
- Demo runnable in under 5 minutes using BrightPath synthetic scenario
- No external LLM API calls, no real sensitive data

**Result:** 9 functional pages, 758 passing tests, full Markdown training pack export, responsible-use controls at every layer.

---

## Solution Overview

A nine-phase Streamlit application implementing the full consulting workflow from organisation scenario to downloadable training pack. Each phase is a functional Streamlit page backed by a tested Python source module. All generation is deterministic and locally-run.

---

## Key Features

- Synthetic BrightPath Skills Training organisation scenario (loadable in one click)
- Editable scenario form — organisation type, sector, staff count, roles, AI concerns, priority topics
- Training Needs Assessment — topic priority scoring, role-specific needs, learning outcomes
- Workshop Planner — 60/90/120-minute timed agendas with trainer notes and discussion prompts
- 8 activity types — safe/unsafe prompt sorting, risky prompt rewrite, hallucination review, learner data boundaries, safeguarding escalation, human review, approved tools, bias and fairness
- Facilitator Guide — opening/closing scripts, delivery notes, misconceptions, debrief guidance
- Staff Handout — safe-use principles, allowed/prohibited uses, prompt examples, escalation guidance
- Knowledge Check — MCQs, scenario questions, reflection prompts, answer key
- Training Pack Export — section selector, full Markdown assembly, download button
- Responsible-use boundaries visible on every output page
- 758 pytest tests across all source modules

---

## Architecture

```
App Layer (Streamlit)
  app.py — 9-page multi-page app, st.session_state as shared data bus

Scenario Layer
  src/sample_data.py         — synthetic BrightPath scenario, topic lists, descriptions
  src/scenario_manager.py    — validation, summarisation, Markdown formatting

Generation Modules (Phases 2–8)
  src/needs_assessment.py    — topic priority scoring, role-specific needs, learning outcomes
  src/workshop_planner.py    — timed agenda, trainer notes, resources, delivery notes
  src/activity_generator.py  — 8 activity types with fully-populated dicts
  src/facilitator_guide.py   — scripts, delivery notes, activity notes, misconceptions
  src/handout_generator.py   — safe-use guide, prompt examples, escalation guidance
  src/knowledge_check.py     — MCQ bank, scenario bank, reflection bank, answer key
  src/training_pack.py       — readiness check, Markdown assembly, section selector

UI Helpers
  src/ui_components.py       — reusable Streamlit rendering helpers

Tests
  tests/                     — 758 pytest tests, no external dependencies
```

---

## Tech Stack

| Component | Technology |
|---|---|
| UI framework | Streamlit |
| Data handling | Pandas |
| Language | Python 3.11 |
| State management | `st.session_state` |
| Content generation | Deterministic template-based logic |
| Testing | pytest |
| External APIs | None |
| Database | None |
| Authentication | None |

---

## Data / Scenarios / Inputs

**All scenarios are synthetic.**

No real learner data, safeguarding information, staff HR data, confidential client records, personal data, or regulated information is used in this prototype at any stage. The BrightPath Skills Training scenario is fictional and clearly labelled. All example prompts, scenario cards, and AI outputs shown in activities and handouts are invented for demonstration purposes only.

---

## AI / Model / API Approach

**This version uses deterministic/template-based generation.**

It does not use external LLM APIs or cloud model calls. No OpenAI, Anthropic, Cohere, Google AI, Azure AI, or other external model API is called at any point. All content generation runs locally using Python logic. The same inputs produce the same outputs every time.

This mirrors the responsible-use principle applied in Build 3 — being honest about what the system knows and how it generates its outputs, with no hallucination risk from probabilistic generation.

---

## Implementation Process

| Phase | What was implemented |
|---|---|
| 1 | App scaffold, BrightPath synthetic scenario, scenario validation, session state wiring, 7 placeholder pages, test infrastructure (52 tests) |
| 2 | Training Needs Assessment — 13-topic catalogue, priority scoring, role-specific needs, learning outcomes, Markdown export (144 tests) |
| 3 | Workshop Planner — timed agenda, delivery mode, trainer notes, discussion prompts, responsible-use messages, Markdown export (235 tests) |
| 4 | Activity Generator — 8 activity types, fully-populated dicts, scenario cards, debrief questions, risk warnings, Markdown export (337 tests) |
| 5 | Facilitator Guide — opening/closing scripts, delivery notes, activity notes, misconceptions, debrief, preparation checklist, Markdown export (456 tests) |
| 6 | Staff Handout — safe-use principles, allowed/prohibited uses, prompt examples with activity-based enrichment, escalation guidance, Markdown export (573 tests) |
| 7 | Knowledge Check — 15-item MCQ bank, 4 scenario questions, 5 reflection questions, answer key, pass threshold, staff/trainer copies, Markdown export (674 tests) |
| 8 | Training Pack Export — readiness check, section selector, Markdown assembly with pre-rendered session state strings, responsible-use and limitations sections, download button (758 tests) |
| 9 | Completion review, portfolio documentation, demo script, screenshots checklist, safety boundaries update, build reflection |

---

## Testing and Validation

- **758 pytest tests** across 10 source modules
- All tests use synthetic data — no API keys, no external services, no real data
- Tests verify: function return types, required keys in output dicts, content rules (no real data, responsible-use notes, prototype notices), edge cases (None inputs, empty lists, invalid counts), and Markdown format contracts
- No end-to-end UI testing (Streamlit rendering not tested at unit level — tested manually via app)

---

## Demo Notes

- Run `streamlit run app.py` from `10-builds/ai-staff-training-workshop-generator/`
- Click **Load BrightPath Demo Scenario** on the Organisation Scenario page
- Run each page in order to populate session state
- Full training pack downloadable from Training Pack Export in under 5 minutes
- See [docs/demo-script.md](demo-script.md) for a step-by-step walkthrough

---

## Results

- 9 functional app pages
- 758 passing tests
- Complete Markdown training pack export covering: scenario, needs assessment, workshop plan, activities, facilitator guide, staff handout, knowledge check, answer key, responsible-use boundaries, limitations, and next steps
- Responsible-use controls embedded at every layer of the application

---

## Business / User Value

Build 4 helps organisations convert responsible AI adoption concerns into practical staff behaviour through structured training materials. Concretely:

- A consultant running this tool after an AI readiness audit can produce a draft training pack for client review in under 10 minutes
- A trainer receiving the output has a ready-made workshop agenda, activity pack, facilitator guide, staff handout, and knowledge check — reducing preparation time from days to hours
- A governance lead reviewing the output can see that every section carries responsible-use framing, clear limitations, and a human review requirement — reducing the risk of the tool being misused as a compliance authority

---

## Risk and Governance Considerations

- All generation is local and deterministic — no data is sent to external services
- Responsible-use warnings are visible on every generated output
- The training pack includes a dedicated Responsible-Use Boundaries section and a Prototype Limitations section
- Human review is explicitly required before using any output in a real training session
- Production deployment would require: DPIA, authentication, access control, audit logging, data retention policy, safeguarding review, HR review, legal review, and responsible-owner approval

---

## Limitations

- Markdown export only — no PDF or PPTX
- In-memory session state — resets on app restart
- Single synthetic scenario template — BrightPath only (additional templates are a future improvement)
- No document upload — scenarios must be defined in the form or loaded as the demo
- No LMS / SCORM integration
- No staff completion tracking
- Prototype outputs require qualified human review before real delivery

---

## Lessons Learned

- Deterministic generation is underrated for responsible AI tools — no hallucination, predictable outputs, fully testable
- Embedding responsible-use constraints into the product design (not just the documentation) produces a stronger portfolio artefact than a technical demo alone
- Session state as the shared data bus works well for linear consulting workflows — each page reads from and writes to a known set of keys
- Pre-rendering Markdown strings at generation time (rather than reformatting in the pack assembler) keeps the Training Pack Export module clean and avoids duplicating formatting logic
- Testing at 758 tests is achievable in a prototype if you design modules to be pure Python with no Streamlit dependencies

---

## Future Improvements

See [docs/future-improvements.md](future-improvements.md) for the full list. Key priorities:

1. PDF / PPTX export — significantly increases commercial usefulness
2. Additional scenario templates — education, healthcare, professional services, retail, public sector
3. Build 3 RAG integration — ground training activities in the organisation's actual policies
4. LLM-assisted generation (optional, local Ollama only) — richer content with strict evidence grounding
5. Secure deployment with authentication, access control, and audit logging

---

## Portfolio Summary

Build 4 demonstrates that Rashid can:

- Design a multi-phase, end-to-end AI training material generation pipeline
- Build clean, deterministic content generation logic without external AI dependencies
- Apply responsible AI controls consistently across a complete consulting product chain
- Create testable, modular Streamlit prototypes with a real pytest test suite (758 tests)
- Connect AI tools — audit → document intelligence → semantic RAG → training — into a coherent consulting offer
- Produce portfolio-grade documentation: architecture notes, safety boundaries, demo scripts, case studies, and completion reviews

This is a production-style portfolio prototype demonstrating architecture, methodology, and responsible AI practice. It is not a production training compliance system.

---

*Build 4 · AI Staff Training and Workshop Generator · BrightPath ChatGPT Mastery Project*
*All scenarios are synthetic. Outputs require human review before use.*
