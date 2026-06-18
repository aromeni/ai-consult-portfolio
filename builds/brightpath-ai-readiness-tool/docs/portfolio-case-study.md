# BrightPath AI Readiness + Workflow Audit Tool

## One-line Summary

A Streamlit prototype that gives AI consultants a structured, repeatable process for diagnosing a small organisation's AI readiness, auditing workflows, scoring risks, and generating a pilot recommendation — without requiring any external APIs, databases, or personal data.

---

## Problem

Small UK training providers want to explore AI tools but lack the structure to do it safely. Common patterns:

- Staff using personal ChatGPT accounts without policy, approved tools, or data controls
- Managers unsure which workflows are safe to pilot and which carry significant risk
- No governance baseline — no AI acceptable use policy, no escalation routes, no data boundaries defined
- Consultants delivering workshops without a diagnostic tool to anchor the conversation

An AI consultant needs something more than a slide deck. They need a tool that asks the right questions, scores the answers consistently, and produces a written recommendation the client can keep.

---

## Target User

**Primary:** An AI consultant (Rashid) delivering AI readiness diagnostics to small UK organisations.

**Secondary:** Managers of small training providers, FE colleges, adult education organisations, and document-heavy SMEs wanting a baseline assessment before committing to AI adoption.

---

## Workflow Context

A typical engagement looks like this:

1. Consultant meets with the manager and two or three staff members
2. They work through the tool together — 60 to 90 minutes
3. The consultant uses the scoring dimensions to structure a conversation, not just tick boxes
4. At the end, the Mini Report is downloaded and shared with the manager
5. The recommendation drives the next session: governance workshop, pilot design, or training programme

---

## Goals

1. Give a consultant a structured, repeatable diagnostic process
2. Surface AI readiness gaps before any pilot begins
3. Identify the lowest-risk workflow to pilot first
4. Generate a written recommendation the client can act on
5. Demonstrate that Layer 3–7 methodology works as a real-world deliverable

---

## Success Criteria

- A consultant can complete a full session in under 90 minutes
- The readiness, workflow, risk, and recommendation scores are consistent and defensible
- The Mini Report is good enough to share with the client manager as a first draft
- The tool does not require a developer to set up or run
- No personal or sensitive data needs to be entered at any point

---

## Solution Overview

A seven-page Streamlit app with modular scoring logic, synthetic sample data, and a Markdown report generator. The app guides the consultant through five assessment stages, then produces a downloadable report.

All state is held in `st.session_state`. No database, no API, no authentication. Runs locally with two dependencies: Streamlit and Pandas.

---

## Key Features

| Feature | Description |
|---|---|
| AI Readiness Assessment | 10 dimensions scored 0–10; total 0–100; five readiness bands |
| Workflow Audit | 10 suitability dimensions scored 0–5; total 0–50; five suitability bands |
| Risk Assessment | 10 risk categories; likelihood × impact (1–5 each); four risk levels |
| Pilot Recommendation | Combines all three scores; six outcome categories from "Not ready" to "Ready for controlled implementation" |
| Markdown Mini Report | 9-section structured report; editable before download; safe filename generation |
| BrightPath sample data | Realistic synthetic example pre-loaded for demonstration |
| Safety boundaries | Responsible-use notice, data safety reminders, and limitations on every page |

---

## Architecture

```
app.py
├── sidebar navigation (7 pages)
├── session state initialisation
├── page routing (if/elif chain)
└── imports from src/

src/scoring.py          — all scoring logic, dimension definitions, band thresholds
src/sample_data.py      — all synthetic sample data (BrightPath profile, scores, workflows)
src/report_generator.py — plain-text (Phase 1) and Markdown (Phase 6) report generators
src/utils.py            — session state init, responsible_use_notice(), score_bar()
```

All scoring logic is separated from the UI. `app.py` calls functions and renders results — it contains no scoring logic, band thresholds, or recommendation rules inline.

---

## Tech Stack

| Component | Choice | Reason |
|---|---|---|
| UI | Streamlit | Lowest friction for form-based, data-driven prototypes; no frontend build tooling |
| Data | Pandas | DataFrames for bar charts and tables |
| Language | Python 3.11 | Standard choice; matches most UK developer environments |
| State | `st.session_state` | Keeps the prototype self-contained and portable |
| Export | Standard library `re`, `datetime` | No additional dependencies for report generation |
| Deployment | Local only (MVP) | No infrastructure needed to demonstrate the tool |

---

## Data / Documents / Inputs

All data in this prototype is synthetic, anonymised, or fictional.

- `BRIGHTPATH_PROFILE` — fictional organisation profile
- `BRIGHTPATH_READINESS_SCORES` — synthetic readiness dimension scores
- `BRIGHTPATH_WORKFLOWS` — eight fictional workflows with risk levels
- `BRIGHTPATH_SAMPLE_WORKFLOW` — one workflow described in detail (lesson planning)
- `BRIGHTPATH_SAMPLE_WORKFLOW_SCORES` — suitability scores for the sample workflow
- `BRIGHTPATH_RISK_PROFILE` — synthetic risk scores for the lesson planning use case
- `BRIGHTPATH_PILOT_EXAMPLE` — illustrative recommendation example
- `BRIGHTPATH_MINI_REPORT_SAMPLE` — full sample report field values

No real learner data, client data, staff data, safeguarding information, or regulated data is used anywhere in the codebase.

---

## AI / Model / API Approach

**This version does not use external AI APIs or model calls. It is a deterministic Streamlit prototype using structured scoring logic and synthetic examples.**

All scoring, categorisation, recommendation logic, and report generation is implemented as pure Python functions in `src/scoring.py` and `src/report_generator.py`. There are no calls to ChatGPT, Claude, or any other model.

This is an intentional design decision for the MVP:
- The tool can be demonstrated without API keys or costs
- The scoring logic is transparent and auditable
- Clients can see exactly how each recommendation is derived

Future phases may add LLM-assisted report drafting with strict safeguards (see [future-improvements.md](future-improvements.md)).

---

## Implementation Process

| Phase | Scope | Status |
|---|---|---|
| 1 | Scaffold — folder structure, 7-page navigation, placeholder pages | Complete |
| 2 | AI Readiness Assessment — 10-dimension questionnaire, 0–100 scoring, live category and chart | Complete |
| 3 | Workflow Audit — 10-dimension suitability scoring (0–50), workflow info form, category, next action, chart | Complete |
| 4 | Risk Assessment — 10 risk categories, likelihood × impact, level classification, safeguards | Complete |
| 5 | Pilot Recommendation — combines readiness, workflow, and risk scores; 6 outcome categories | Complete |
| 6 | Mini Report — 9-section Markdown report generator, editable form, live preview, `.md` download | Complete |
| 7 | Portfolio documentation — case study, demo script, reflection, future improvements | Complete |

**Build approach:** Each phase had a defined scope, was implemented in a single session, reviewed against a checklist of criteria, and marked complete before the next phase began. Phase 7 is documentation only.

---

## Testing and Validation

Functional verification was carried out at the end of each phase using Python assertion scripts:

- **Scoring logic:** Boundary conditions tested for all band thresholds (readiness, workflow suitability, risk, recommendation)
- **Recommendation logic:** Nine test cases covering all restrictive and positive conditions in order
- **Report generator:** Nine section headers verified; responsible-use text verified; key content verified; filename generation tested with edge cases
- **Syntax:** `ast.parse()` used after every code change to verify no syntax errors before running the app

No automated test suite exists yet. A pytest-based suite is planned in a future phase.

---

## Screenshots / Demo Notes

See [docs/screenshots-checklist.md](screenshots-checklist.md) for the full screenshots list and guidance.

Key demo points:
- Load BrightPath demo data from the Home page to pre-populate all pages
- The lesson planning workflow scores well on suitability (42/50) but the safeguarding risk is High
- This drives the recommendation to "Governance-first before pilot" — a realistic and defensible result
- The Mini Report downloads as a `.md` file with a clean, safe filename

---

## Results

**As a prototype demonstrating capability:**

- Seven pages implemented across seven phases in a single build session
- Six scoring dimensions (readiness, workflow, risk, recommendation, safeguards, next actions) all working correctly
- Markdown report generation producing a client-ready 9-section document
- Synthetic BrightPath scenario consistently producing realistic, defensible outputs
- All safety boundaries maintained throughout — no personal data required at any point

**As a client tool (not yet validated in the field):**

The tool has not been tested with real clients. Commercial validation — whether it saves time, improves recommendation quality, or produces better pilot outcomes — remains to be demonstrated.

---

## Business or User Value

| User | Value |
|---|---|
| AI consultant | A structured diagnostic process that replaces ad hoc conversations; a client-facing report to leave behind; a repeatable tool that can be used across multiple clients |
| Organisation manager | A scored baseline they can share internally; a specific workflow recommendation with safeguards; a starting point for governance conversations |
| Project (ChatGPT Mastery) | Proof that Layers 3–7 work as a real-world deliverable; a portfolio asset demonstrating consulting, governance, and software build capability |

---

## Risk and Governance Considerations

This prototype handles governance carefully by design:

- Safeguarding risk category flags prominently in the Risk Assessment — even for seemingly low-risk workflows like lesson planning
- The recommendation logic checks critical and high risks first — a Critical risk always returns "Not ready", regardless of readiness or workflow scores
- Responsible-use notices appear on every page and in the generated report
- No personal data is required at any point; all inputs are organisation-level or process-level
- The Markdown report's Section 8 includes a verbatim limitations statement

These decisions were made to ensure the tool can be used in front of a safeguarding-conscious client without causing concern.

---

## Limitations

- Indicative only — scores are estimates, not measured data
- Single assessor bias — if only the consultant scores the dimensions, the result reflects their interpretation
- No persistent storage — session data lost on app restart
- No multi-user support
- No PDF export in this version
- Not tested with real clients — commercial value is hypothetical
- Organisation Profile is read-only — no input form yet

---

## Lessons Learned

1. **Separating scoring logic from UI is essential.** Keeping all logic in `scoring.py` made testing easy and kept `app.py` readable.
2. **Sample data is as important as the scoring logic.** A realistic synthetic example makes the tool demonstrable without a real client.
3. **Safety boundaries should be designed in, not added on.** Building the responsible-use notices into every page from Phase 1 meant they never felt bolted on.
4. **The `st.rerun()` pattern is necessary for sample loaders.** Setting session state keys before widget instantiation requires a rerun; this was the most technically subtle part of the build.
5. **Recommendation logic order matters.** Checking restrictive conditions first (critical risk → high risk → low readiness) prevents false positive recommendations.

---

## Future Improvements

See [docs/future-improvements.md](future-improvements.md) for the full prioritised list.

---

## Portfolio Summary

This project demonstrates:

- **AI consulting capability** — structured readiness assessment, workflow diagnosis, risk scoring, governance-aware recommendation
- **Software build capability** — Streamlit app built in phases, modular architecture, clean separation of logic and UI
- **Governance and safety awareness** — safeguarding risk flagged, data boundaries enforced, responsible-use language throughout
- **Training and workshop knowledge** — dimensions and recommendations draw directly from Layer 7 training methodology
- **Practical delivery** — the tool can be demonstrated to a client in under 90 minutes and produces a downloadable report

**What this does not prove:** Real-world commercial validation, client results, or production readiness. This is a portfolio prototype — a proof of concept and a foundation for a real product.
