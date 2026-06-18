# AI Staff Training and Workshop Generator

**A locally-run prototype that helps consultants and trainers turn AI adoption concerns into practical, responsible staff training materials.**

Build 4 of the BrightPath ChatGPT Mastery Project.
Nine phases + two polish releases. Zero external AI API calls.

---

## One-Line Summary

A Streamlit prototype that takes a synthetic organisation scenario and generates a complete AI staff training pack — workshop agenda, activities, facilitator guide, staff handout, knowledge check, and downloadable Markdown training pack — using deterministic, locally-run logic.

---

## Problem

Organisations that have completed an AI readiness audit face a practical next step: they need to train their staff. But:

- Staff training materials take significant time to write from scratch
- Generic AI training is not tailored to the organisation's specific concerns, sector, or staff roles
- Training materials for regulated contexts (education, healthcare, public sector) require careful responsible-use framing
- Small organisations typically don't have a dedicated L&D team to commission custom materials
- Consultants who deliver AI audits need a demonstrable answer to "what do we do now?"

Build 4 addresses this by showing what a consulting-grade AI training material generator looks like — starting from an organisation scenario and producing a structured, downloadable training pack.

---

## Target Users

| User | Why they use this |
|---|---|
| AI consultants (primary: Rashid) | Demonstrating AI training material generation to clients after an AI readiness audit |
| Trainers and L&D practitioners | Generating scenario-tailored training drafts as a starting point for review and delivery |
| Governance leads and managers | Understanding what responsible AI staff training looks like in practice |
| Developers | Learning deterministic content generation patterns for AI-adjacent tools |

---

## Why This Matters

Build 4 demonstrates that:

- AI training material generation does not require a live LLM call — deterministic templates produce consistent, testable, auditable outputs
- Responsible-use boundaries can be embedded into the product design, not just the documentation
- A consultant can go from an organisation scenario to a complete draft training pack in under 10 minutes
- Training materials that embed human-review requirements and synthetic-data notices are safer for regulated contexts

---

## Consulting Workflow

```
Organisation Scenario
  → Training Needs Assessment
  → Workshop Planner
  → Activity Generator
  → Facilitator Guide
  → Staff Handout
  → Knowledge Check
  → Training Pack Export
```

Each step builds on the previous. The final output is a complete, downloadable Markdown training pack.

---

## Core Features

- **Synthetic BrightPath scenario** — load a fictional small UK training provider in one click
- **Editable scenario form** — enter your own organisation details (synthetic/approved data only)
- **Training Needs Assessment** — 13-topic responsible AI catalogue; HIGH / MEDIUM / LOW priority scoring; role-specific training needs; learning outcomes
- **Workshop Planner** — 60 / 90 / 120-minute timed agendas; in-person, online, or hybrid; trainer notes; discussion prompts; responsible-use messages
- **Activity Generator** — 8 activity types: safe/unsafe prompt sorting, risky prompt rewrite, spot the hallucination, learner data boundaries, safeguarding escalation, human review checklist, approved tools decision, bias and fairness review
- **Facilitator Guide** — opening and closing scripts; section delivery notes; activity facilitation notes; common misconceptions; debrief guidance; preparation checklist
- **Staff Handout** — safe-use principles; allowed and prohibited uses; safe / unsafe / rewritten prompt examples; human review checklist; escalation guidance
- **Knowledge Check** — 5 / 10 / 15 MCQs; scenario questions; reflection prompts; answer key; staff and trainer copies; pass guidance
- **Training Pack Export** — readiness check; section selector; full Markdown assembly; facilitator review checklist; responsible-use and limitations sections; download button

---

## Professional UI and Export Options

The app uses a modern, professional dashboard presentation — clean off-white canvas, navy and slate accents, card-style metrics, status badges, and a sidebar workflow tracker — built with Streamlit-native components plus light CSS (`src/ui_components.py`).

**Every generated report supports both Markdown and PDF download:**

| Report | Markdown | PDF |
|---|---|---|
| Training Needs Assessment | ✓ | ✓ |
| Workshop Plan | ✓ | ✓ |
| Training Activities | ✓ | ✓ |
| Facilitator Guide | ✓ | ✓ |
| Staff Handout | ✓ | ✓ |
| Knowledge Check | ✓ | ✓ |
| Full Training Pack | ✓ | ✓ (+ PowerPoint) |

- **PDF reports** (`src/pdf_exporter.py`) — reportlab-generated with cover page, organisation name, generated date, prototype status, styled headings, bullet lists, tables, responsible-use boundaries, and a "Synthetic scenario prototype. Human review required." footer on every page
- **Premium Training Pack PDF** (`src/export_utils.py`) — cover page, executive summary, analytics charts, all generated sections, facilitator review checklist, responsible-use boundaries, prototype limitations, and recommended next steps — a draft consulting deliverable for human review
- **PowerPoint Training Deck export** (`src/pptx_exporter.py`) — 15-slide professional deck auto-generated when the training pack is assembled; covers organisation context, training needs, workshop agenda, activities, safe-use rules, human review checklist, escalation guidance, knowledge check, pack completion, and responsible-use boundaries; suitable for demo and portfolio review
- **Analytics charts** (`src/report_analytics.py`, `src/chart_utils.py`) — deterministic section completion, activity mix, workshop time allocation, and knowledge check topic coverage charts; computed only from generated content, never invented performance data

All exports use synthetic scenario content only and require human review before real-world use.

---

## App Pages

| Page | Status | Phase |
|---|---|---|
| Home | Functional — workflow overview, Build 1–3 connections, responsible-use warning | 1 |
| Organisation Scenario | Functional — load demo scenario, editable form, validation, summary cards, Markdown preview | 1 |
| Training Needs Assessment | Functional — topic priorities, learning outcomes, role needs, Markdown download | 2 |
| Workshop Planner | Functional — timed agenda, trainer notes, resources, responsible-use messages, Markdown download | 3 |
| Activity Generator | Functional — 8 activity types, scenario cards, debrief questions, risk warnings, Markdown download | 4 |
| Facilitator Guide | Functional — opening/closing scripts, delivery notes, activity notes, misconceptions, debrief, Markdown download | 5 |
| Staff Handout | Functional — safe-use principles, allowed/prohibited uses, prompt examples, escalation guidance, Markdown download | 6 |
| Knowledge Check | Functional — MCQs, scenario questions, reflections, answer key, pass guidance, Markdown download | 7 |
| Training Pack Export | Functional — readiness check, section selector, Markdown pack assembly, download | 8 |

---

## Responsible-Use Boundaries

> **Use synthetic or approved scenarios only. Do not enter real learner data, safeguarding case details, confidential client records, staff HR data, personal data, or regulated information.**

- All scenarios in this prototype are synthetic, fictional, and clearly labelled
- No external AI API calls — all processing runs locally; no OpenAI, Anthropic, Google, Azure AI, or other model API
- No LangChain, LlamaIndex, or agent frameworks
- No vector database
- No document upload, no authentication, no production database
- Human review is required before using any output in a real training session
- This tool does not provide legal, safeguarding, HR, compliance, medical, financial, or professional advice
- Training materials are support materials, not official organisational policy unless reviewed and approved by responsible owners
- Production use requires governance, DPIA, security review, privacy review, safeguarding review, HR review, legal review, and responsible-owner approval

See [docs/safety-boundaries.md](docs/safety-boundaries.md) for the full safety statement.

---

## Technical Stack

| Component | Technology |
|---|---|
| UI framework | Streamlit |
| Data handling | Pandas |
| Language | Python 3.11 |
| State management | `st.session_state` |
| Content generation | Deterministic template-based logic (no LLM API calls) |
| Analytics | matplotlib — deterministic chart generation from generated content |
| PDF export | reportlab — per-report PDFs plus premium training pack PDF with charts |
| PPTX export | python-pptx — 15-slide professional training deck |
| Testing | pytest — 953 tests |
| External APIs | None |
| Database | None |
| Authentication | None |

---

## Setup Instructions

**Requirements:** Python 3.10 or later.

```bash
# 1. Navigate to the project
cd 10-builds/ai-staff-training-workshop-generator

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## How to Run

```bash
streamlit run app.py
```

Opens at `http://localhost:8501` by default.

**Quick start:** navigate to Organisation Scenario and click **Load BrightPath Demo Scenario**.

---

## Running Tests

```bash
pytest
```

Run from the `ai-staff-training-workshop-generator/` directory. No API keys or external services required. All 910 tests use synthetic data and run in under 10 seconds.

---

## Demo Scenario

**BrightPath Skills Training** — a fictional small UK training provider:

- **Staff count:** 8
- **Current AI use:** informal ChatGPT use for lesson planning, emails, and reports
- **Main concerns:** learner data, safeguarding, staff misuse, output accuracy, hallucination, bias, approved tools, accountability, time saving (9 concerns)
- **Priority topics:** 8 responsible AI training topics selected for the workshop
- **Staff roles:** Tutors, Administrators, Team Leaders, Quality Lead

Click **Load BrightPath Demo Scenario** on the Organisation Scenario page to populate the full scenario in one click.

---

## Phase Roadmap

| Phase | Feature | Status |
|---|---|---|
| 1 | Scaffold, synthetic scenario setup, app navigation, test infrastructure | Complete |
| 2 | Training needs assessment — topic priorities, learning outcomes, role-specific needs, Markdown export | Complete |
| 3 | Workshop planner — timed agenda, trainer notes, resources, responsible-use messages, Markdown export | Complete |
| 4 | Activity generator — safe/unsafe prompts, risky prompt rewrite, hallucination review, learner data boundaries, safeguarding escalation, human review checklist, approved tools decision, bias and fairness review | Complete |
| 5 | Facilitator guide — opening/closing scripts, delivery notes, activity notes, misconceptions, debrief | Complete |
| 6 | Staff handout — safe-use principles, allowed/prohibited uses, prompt examples, human review checklist, escalation guidance | Complete |
| 7 | Knowledge check — MCQs, scenario questions, reflections, answer key, pass/review guidance | Complete |
| 8 | Training pack export — readiness check, section selector, full Markdown pack assembly and download | Complete |
| 9 | Completion review and portfolio documentation | Complete |

---

## Relationship to Builds 1, 2, and 3

**Build 1 — AI Readiness and Workflow Audit** diagnosed where an organisation stands with AI: workflow gaps, risk areas, and staff readiness. Its audit report identifies the training needs that Build 4 turns into actionable materials.

**Build 2 — Document Intelligence and RAG Demo** extracted evidence from policy documents using keyword search. Build 4 can be extended to use that document evidence to ground training activities in the organisation's actual policies.

**Build 3 — Semantic RAG Policy Assistant** retrieved semantically relevant policy chunks and generated grounded answers. Build 4 can pull from Build 3's RAG pipeline to support training content generation in later phases.

**Build 4 — AI Staff Training Generator** *(this build)* closes the consulting loop:

> Audit → Document Intelligence → Semantic RAG → **Staff Training**

---

## Current Limitations

- In-memory session state — resets on app restart; no persistent storage
- Single synthetic scenario template — additional scenario templates are a future improvement
- No document upload — scenarios must be defined in the form or loaded as the demo
- No authentication — single-session, local use only
- No staff completion tracking, LMS integration, or audit logging
- All outputs require human review before use in a real training session

---

## Future Improvements

**Polish Phase A (complete):** professional UI, sidebar workflow status, analytics charts, training pack PDF export, PowerPoint/PPTX export.

**Polish Phase B (complete):** modern dashboard styling, per-report PDF export on every report page, reusable PDF exporter, chart utilities, premium training pack PDF with executive summary and facilitator review checklist.

**Short-term:** screenshots and demo assets, branded PDF/PPTX themes, additional scenario templates.

**Medium-term:** editable templates, richer knowledge-check scoring, Build 3 RAG integration, organisation-specific policy references.

**Long-term:** optional local LLM-assisted generation (Ollama, strict controls), PDF/PPTX export, LMS/SCORM export, secure deployment with authentication and audit logging.

See [docs/future-improvements.md](docs/future-improvements.md) for the full roadmap.

---

## Folder Structure

```
ai-staff-training-workshop-generator/
├── app.py                          # 9-page Streamlit app
├── requirements.txt                # streamlit, pandas, pytest
├── pytest.ini                      # pythonpath = .
│
├── src/
│   ├── __init__.py
│   ├── sample_data.py              # BrightPath scenario, topic lists, descriptions
│   ├── scenario_manager.py         # validate, summarise, format, create
│   ├── needs_assessment.py         # Phase 2 — training needs assessment
│   ├── workshop_planner.py         # Phase 3 — workshop plan generation
│   ├── activity_generator.py       # Phase 4 — activity generation
│   ├── facilitator_guide.py        # Phase 5 — facilitator guide generation
│   ├── handout_generator.py        # Phase 6 — staff handout generation
│   ├── knowledge_check.py          # Phase 7 — knowledge check generation
│   ├── training_pack.py            # Phase 8 — training pack assembly and export
│   ├── report_analytics.py         # Polish A — deterministic pack analytics
│   ├── export_utils.py             # Polish A — training pack PDF and PPTX export
│   ├── pdf_exporter.py             # Polish B — reusable per-report PDF export
│   ├── chart_utils.py              # Polish B — matplotlib chart files
│   ├── pptx_exporter.py            # Polish B — training pack PPTX interface
│   └── ui_components.py            # Streamlit UI helpers and global styles
│
├── assets/
│   └── screenshots/                # App screenshots (add using screenshots-checklist.md)
│
├── outputs/
│   ├── reports/                    # Generated report PDFs (gitignored)
│   ├── charts/                     # Generated chart PNGs (gitignored)
│   └── training_packs/             # Saved training packs (generated files gitignored)
│
├── docs/
│   ├── build-notes.md              # Phase-by-phase implementation notes
│   ├── architecture.md             # Layered architecture overview and data flow
│   ├── safety-boundaries.md        # Full responsible-use statement
│   ├── demo-script.md              # Step-by-step demo walkthrough
│   ├── future-improvements.md      # Full improvement roadmap
│   ├── build-4-completion-review.md # Build 4 completion record
│   ├── portfolio-case-study.md     # Portfolio and LinkedIn case study
│   ├── build-reflection.md         # Build reflection and lessons learned
│   ├── screenshots-checklist.md    # Screenshot capture checklist
│   └── deployment-notes.md         # Local run and deployment guidance
│
└── tests/
    ├── test_sample_data.py          # 25 tests
    ├── test_scenario_manager.py     # 34 tests
    ├── test_needs_assessment.py     # 65 tests
    ├── test_workshop_planner.py     # 91 tests
    ├── test_activity_generator.py   # 102 tests
    ├── test_facilitator_guide.py    # 119 tests
    ├── test_handout_generator.py    # 117 tests
    ├── test_knowledge_check.py      # 101 tests
    ├── test_training_pack.py        # 99 tests
    ├── test_report_analytics.py     # 55 tests (Polish A + B)
    ├── test_export_utils.py         # 42 tests (Polish A)
    ├── test_pdf_exporter.py         # 34 tests (Polish B)
    ├── test_chart_utils.py          # 15 tests (Polish B)
    └── test_pptx_exporter.py        # 6 tests (Polish B)
                                     # Total: 910 tests
```

---

## Portfolio Positioning

Build 4 demonstrates that Rashid can:

- Design a multi-phase, end-to-end responsible AI training material generation pipeline
- Build clean, deterministic content generation logic without external AI dependencies
- Apply responsible AI controls consistently across a complete consulting product chain
- Create testable, modular Streamlit prototypes with a real pytest test suite (910 tests)
- Connect AI tools — audit, document intelligence, semantic RAG, training — into a coherent consulting offer
- Produce portfolio-grade documentation: architecture notes, safety boundaries, demo scripts, case studies, and completion reviews

**This is not a production system.** It is a production-style prototype built to demonstrate architecture, methodology, and responsible AI practice.

See [docs/portfolio-case-study.md](docs/portfolio-case-study.md) for the full case study.

---

*Build 4 · AI Staff Training and Workshop Generator · BrightPath ChatGPT Mastery Project*
*All scenarios are synthetic. Outputs require human review before use.*
