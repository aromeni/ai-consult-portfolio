# Build 8 — AI Adoption Delivery and Implementation Tracker

## Purpose

Build 8 helps an AI consultant manage the work that follows an audit, governance review, training programme, consulting report, and adoption impact review. It turns findings and decisions into implementation actions with owners, priorities, deadlines, blockers, and follow-up requirements.

## How Build 8 fits the portfolio

Build 7 measures whether AI adoption is producing practical value. Build 8 takes the next step by tracking what must be delivered to implement, continue, control, pause, or scale adoption.

- Build 1 supplies readiness findings and candidate workflows.
- Build 4 supplies training and confidence-building needs.
- Build 5 supplies consulting recommendations and follow-up actions.
- Build 6 supplies governance gaps, controls, and sign-off needs.
- Build 7 supplies adoption evidence and stop, continue, review, or scale decisions.
- Build 8 converts those outputs into an owned delivery plan.

## Phase 1 — Scaffold and Synthetic Implementation Action Data

Phase 1 creates the Streamlit scaffold, deterministic synthetic data, validation logic, calculated action summaries, organisation filtering, tests, and portfolio notes.

## Phase 2 — Action Tracker and Status Engine

Phase 2 adds a deterministic action tracker that helps a consultant identify urgent, blocked, active, waiting, deferred, and completed delivery work.

Phase 2 provides:

- Due-window classification: Due now, Due soon, Due later, or No immediate pressure.
- Attention-level classification: Critical, High, Medium, or Low attention.
- Delivery-state classification: Completed, Blocked, Active, Waiting, or Deferred.
- Deterministic action scoring using priority, blockers, due pressure, and completion.
- A prioritised action list sorted by action score, status priority, and due days.
- Organisation-level action summaries showing delivery load and average scores.
- Related-build action summaries showing which earlier builds generate the most follow-up work.
- Deterministic delivery recommendations for every action.

## Phase 3 — Blocker, Risk, and Dependency Review

Phase 3 adds a deterministic review layer for blocked actions, blocker severity, implementation dependencies, delivery risk, and escalation needs.

Phase 3 provides:

- Blocker detection from recorded status and blocker text.
- Blocker type classification covering governance, training, client decisions, quality, ownership, and general delivery blockers.
- Blocker severity classification from Critical blocker to No blocker.
- Dependency classification for governance sign-off, training follow-up, client check-ins, and multiple dependencies.
- Delivery risk classification using blocker severity, dependencies, priority, due pressure, and completion status.
- Escalation detection for severe blockers, high delivery risk, and blocked actions due within fourteen days.
- Organisation-level and related-build blocker exposure summaries.
- A prioritised blocker resolution list.
- Deterministic blocker resolution recommendations.

## Phase 4 — Governance Sign-off and Control Tracker

Phase 4 adds a deterministic governance tracking layer for explicit sign-offs, control readiness, approval ownership, and governance delivery risk.

Phase 4 provides:

- Governance sign-off detection.
- Sign-off urgency classification: Urgent, Due soon, Routine, or Not required.
- Control area classification covering policy, approval, quality, risk, data, general, and no governance control.
- Control readiness classification: Control ready, Needs review, Blocked, or Not required.
- Governance owner need classification.
- Governance delivery risk classification.
- Organisation-level and related-build governance workload summaries.
- A prioritised governance action list.
- Deterministic governance recommendations.

## Phase 5 — Training Follow-up and Support Plan

Phase 5 adds a deterministic support-planning layer for training follow-up, coaching, workflow demonstrations, quality-review practice, and responsible-use reinforcement.

Phase 5 provides:

- Training follow-up detection.
- Follow-up urgency classification.
- Training support type classification covering foundation, workflow, quality, responsible-use, practical coaching, general, and no support.
- Support intensity classification.
- Training delivery need classification.
- Training delivery risk classification.
- Organisation-level and related-build training workload summaries.
- Owner-role support summaries.
- A prioritised training follow-up list.
- Deterministic training recommendations.

## Phase 6 — Client Check-in Summary Builder

Phase 6 adds a deterministic organisation-level check-in builder that combines action progress, blockers, governance needs, training follow-up, client decisions, and the latest synthetic check-in context.

Phase 6 provides:

- Organisation-level client check-in summaries.
- Delivery progress snapshots.
- Check-in health classification: On track, Needs attention, At risk, or Blocked.
- Prioritised attention item identification.
- Concise client decision needs.
- Deterministic next-review focus.
- Markdown client check-in summary preview.
- Deterministic check-in recommendations.

## Phase 7 — Implementation Progress Report Builder

Phase 7 adds a deterministic Markdown report builder that turns Build 8 delivery evidence into a structured implementation progress report.

Phase 7 provides:

- **Portfolio-level progress report** — covers all synthetic organisations and implementation actions.
- **Organisation-level progress report** — filtered to a single organisation's actions, blockers, governance, training, and check-ins.
- **Executive summary** — total, completed, blocked, high-priority, governance, training, and check-in action counts.
- **Delivery progress section** — prioritised action list with delivery state, attention level, and recommendation.
- **Blocker and dependency section** — blocker type, severity, dependency need, delivery risk, escalation flag, and recommendation.
- **Governance sign-off section** — sign-off urgency, control area, control readiness, governance delivery risk, and recommendation.
- **Training follow-up section** — follow-up urgency, support type, support intensity, delivery need, and recommendation.
- **Client check-in section** — check-in health, attention item count, client decision needs, and next review focus per organisation.
- **Priority next actions** — top ten actions by delivery score.
- **Deterministic consulting interpretation** — fixed guidance on how to use the report.
- **Next review section** — fixed checklist for the next client checkpoint.

Charts, exports, uploads, databases, authentication, cloud deployment, and external AI services are not included.

## Phase 8 — Export Centre, Completion Review, and Final Sweep

Phase 8 completes Build 8 by adding a full export centre that packages delivery evidence into downloadable formats, a completion review that summarises all eight phases, and a portfolio summary for external use.

Phase 8 provides:

- **Markdown report export** — downloads the full Phase 7 implementation progress report as a `.md` file.
- **CSV evidence export** — downloads a flat evidence table combining action, tracker, blocker, governance, and training fields for all fifteen synthetic actions.
- **JSON evidence pack** — downloads a structured JSON file containing all organisations, actions, check-ins, and all analytical summaries from Phases 2–5.
- **Optional PDF export** — downloads a basic PDF version of the progress report using reportlab (if installed).
- **Optional PNG chart export** — downloads a delivery state summary bar chart using matplotlib (if installed).
- **Completion summary metrics** — headline figures across all phases in one dashboard view.
- **Completion review document** — Markdown review covering what Build 8 does, completed phases, consulting use case, limitations, and recommended future extensions.
- **Portfolio summary** — portfolio-ready summary for external use.
- **Final test sweep** — 47 Phase 8 tests, 203 total.

## Synthetic data only

Every organisation, workflow, implementation action, owner role, blocker, evidence note, and client check-in is fictional. Do not add real client data, personal data, learner data, safeguarding data, HR data, confidential data, or regulated information.

The build uses deterministic Python logic only. It does not use OpenAI, Claude, LangChain, LlamaIndex, or any external LLM API.

## Current features

- Three synthetic delivery organisations.
- Fifteen synthetic implementation actions across Builds 1, 4, 5, 6, and 7.
- Six synthetic client check-ins.
- Action ownership, priority, status, due days, blockers, and workflow links.
- Governance sign-off, training follow-up, and client check-in flags.
- Validation for required fields, allowed values, due days, booleans, titles, and owners.
- Calculated status and priority counts.
- Phase 1 delivery summary.
- Organisation-level action filtering.
- Due-window, attention-level, and delivery-state classifications.
- Deterministic action scoring and prioritised delivery list.
- Organisation-level and related-build action tracker summaries.
- Deterministic delivery recommendations.
- Blocker type, severity, dependency, delivery risk, and escalation classifications.
- Organisation-level and related-build blocker exposure summaries.
- Prioritised blocker resolution list with deterministic recommendations.
- Governance sign-off, urgency, control area, control readiness, owner need, and delivery risk classifications.
- Organisation-level and related-build governance workload summaries.
- Prioritised governance action list with deterministic recommendations.
- Training follow-up urgency, support type, support intensity, delivery need, and risk classifications.
- Organisation-level, related-build, and owner-role training workload summaries.
- Prioritised training follow-up list with deterministic recommendations.
- Organisation-level progress snapshots and check-in health.
- Attention items, client decision needs, next-review focus, and Markdown check-in previews.
- Improved Streamlit delivery dashboard with Phases 1–7 active.
- Portfolio-level and organisation-level Markdown implementation progress reports.
- Executive summary with total, completed, blocked, governance, training, and check-in counts.
- Delivery progress section with prioritised action tracker output.
- Blocker and dependency section with escalation flags and blocker recommendations.
- Governance sign-off section with sign-off urgency and control readiness per action.
- Training follow-up section with support type, intensity, and delivery need per action.
- Client check-in section with health, attention items, decisions, and next review focus.
- Priority next actions list (top 10 by delivery score).
- Deterministic consulting interpretation and next review guidance.

## Planned phases

1. Phase 1 — Scaffold and Synthetic Implementation Action Data — Complete
2. Phase 2 — Action Tracker and Status Engine — Complete
3. Phase 3 — Blocker, Risk, and Dependency Review — Complete
4. Phase 4 — Governance Sign-off and Control Tracker — Complete
5. Phase 5 — Training Follow-up and Support Plan — Complete
6. Phase 6 — Client Check-in Summary Builder — Complete
7. Phase 7 — Implementation Progress Report Builder — Complete
8. Phase 8 — Export Centre, Completion Review, and Final Sweep — Complete

## Build 8 Completion Status

Build 8 is complete and portfolio-ready. It now includes all eight phases:

1. Synthetic implementation action data with validation
2. Action tracker and status engine
3. Blocker, risk, and dependency review
4. Governance sign-off and control tracker
5. Training follow-up and support plan
6. Client check-in summary builder
7. Implementation progress report builder
8. Export centre and completion review

## How to run the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How to run tests

```bash
pytest
```
