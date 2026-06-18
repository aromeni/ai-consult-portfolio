# Build 9 — AI Adoption Consulting Capstone Dashboard

## Purpose

Build 9 is the AI adoption consulting capstone dashboard. It connects the outputs of Builds 1–8 into a single client-facing portfolio view, showing how a consultant moves an organisation from initial readiness diagnosis through to tracked implementation delivery.

Build 9 does not rebuild the previous tools. It summarises and connects them into one coherent consulting journey:

```text
Readiness → Document Intelligence → Staff Training → Consulting Report → Governance → ROI/Impact → Delivery Tracking → Capstone Summary
```

It exists to show a reviewer, prospective client, or collaborator how the separate portfolio builds work as one commercially coherent AI adoption consulting service rather than as isolated demonstrations.

## Repository Location and Naming

Build 9 is stored at `10-builds/ai_adoption_consulting_capstone`. The folder name follows the repository's numbered-build structure and uses underscores for a safe Python project path. The product name remains **Build 9 — AI Adoption Consulting Capstone Dashboard**.

## How Build 9 Fits the Portfolio

| Build | Tool | What Build 9 Draws On |
| --- | --- | --- |
| Build 1 | AI Readiness / Workflow Audit Tool | Readiness findings and workflow priority identification |
| Build 2/3 | Document Intelligence / Semantic RAG | Document handling capability and retrieval demonstration |
| Build 4 | AI Staff Training and Workshop Generator | Training delivery, workshop design, and staff confidence |
| Build 5 | AI Consulting Report Generator | Structured consulting report and client-facing recommendations |
| Build 6 | AI Governance Policy Checker | Governance maturity, policy gaps, and control readiness |
| Build 7 | AI Adoption ROI and Impact Tracker | ROI evidence, workflow impact, and adoption decisions |
| Build 8 | AI Adoption Delivery and Implementation Tracker | Implementation actions, blockers, and delivery progress |

## Phase 1 Scope

Phase 1 creates the Streamlit scaffold and synthetic capstone client data. It prepares:

- Three synthetic capstone client organisations.
- Twenty-one cross-build journey stages connecting each client to Builds 1–8.
- Three capstone portfolio indicators summarising each client's position.
- Validation logic for all capstone data.
- Phase 1 summary metrics.
- A Streamlit Phase 1 page displaying all data with a validation summary.

Phase 1 does not include advanced scoring, aggregated build outputs, charts, exports, or a consulting recommendation pathway. These are added in Phases 2–8.

## Phase 2 — Client Journey Overview Engine

Phase 2 adds a deterministic client journey overview engine that analyses each synthetic client across the full AI adoption pathway.

Phase 2 provides:

- **Stage completion rate** — percentage of journey stages with a status of Completed.
- **Average evidence score** — numeric average of evidence strength across all stages using a four-level scale (Weak → Very strong).
- **Journey health classification** — Blocked journey, Needs review, Developing journey, Healthy journey, or Strong journey.
- **Weakest-stage identification** — the journey stage with the lowest combined status and evidence score.
- **Next journey step** — deterministic guidance on what to address first across each client's journey.
- **Client-level journey summaries** — one structured summary per client combining all journey metrics.
- **Journey health summary** — counts of clients by journey health across the portfolio.
- **Prioritised client review list** — clients sorted by review urgency, with blocked and needs-review clients appearing first.
- **Deterministic journey recommendations** — one recommendation per client based on journey health.

## Phase 3 — Cross-Build Insight Aggregator

Phase 3 adds a cross-build insight aggregator that analyses the seven build areas across all synthetic clients and produces a portfolio-level view of where the consulting evidence is strongest and where gaps remain.

Phase 3 provides:

- **Build-level evidence summaries** — one structured summary per build area covering stage counts, completion rate, average evidence score, evidence health, and build gap.
- **Build completion rate** — percentage of client journey stages marked Completed for each build area.
- **Average evidence scoring** — numeric average of evidence strength across all client stages for a build, using a four-level scale (Weak → Very strong).
- **Build evidence health classification** — Very strong evidence, Strong evidence, Developing evidence, Weak evidence, or No evidence.
- **Build gap identification** — deterministic text explaining the current gap status for each build area.
- **Strongest and weakest build areas** — identifies which build is producing the strongest portfolio evidence and which needs most attention.
- **Prioritised build improvement list** — build areas sorted by improvement priority, with weakest and missing evidence areas appearing first.
- **Client-build status matrix** — one row per client showing stage status across all seven build areas at a glance.
- **Deterministic cross-build recommendations** — one recommendation per build area based on evidence health.

## Phase 4 — Consulting Recommendation Pathway

Phase 4 adds a consulting recommendation pathway that converts each client's capstone journey evidence into a structured consulting decision and commercial next step.

Phase 4 provides:

- **Capstone readiness classification** — Capstone ready, Nearly ready, Needs strengthening, or Not ready, based on journey health, completion rate, and evidence score.
- **Consulting pathway selection** — deterministic pathway assignment per client: Ready for capstone presentation, Prepare client-facing follow-up, Strengthen weak evidence, Complete missing journey stages, or Run focused improvement sprint.
- **Commercial next-step selection** — one commercial option per client based on journey health, including Portfolio demonstration, Paid implementation review, Governance improvement sprint, Training and adoption support package, Document intelligence upgrade, or Delivery tracking retainer.
- **Primary improvement area** — identifies the weakest journey stage as the immediate focus for consulting effort.
- **Recommendation priority** — High, Medium, or Low based on journey health, for triage across the client portfolio.
- **Recommendation pathway summary** — counts of clients by readiness and priority across the portfolio.
- **Prioritised recommendations** — clients sorted by recommendation priority, then completion rate, then evidence score.
- **Deterministic consulting recommendation text** — one plain-English recommendation per client based on capstone readiness.
- **Recommendation pathway matrix** — simplified one-row-per-client view of pathway decisions for dashboard display.

## Synthetic Data Only

Every organisation, stage, indicator, and evidence record is fictional. Do not add real client data, personal data, learner data, safeguarding data, HR data, confidential data, or regulated information.

The build uses deterministic Python logic only. It does not use OpenAI, Claude, LangChain, LlamaIndex, or any external LLM API.

## Core Features

- Three synthetic capstone client organisations.
- Twenty-one cross-build journey stages across Builds 1–8.
- Three capstone portfolio indicators.
- Positive, mixed, and review-needed demonstration states.
- Client journey health, completion, evidence, and weakest-stage analysis.
- Cross-build evidence aggregation and prioritised improvement areas.
- Consulting pathways, commercial next steps, and capstone readiness.
- Portfolio and selected-client dashboards.
- Portfolio-level and correctly scoped client-level reports.
- Markdown, CSV, JSON, PDF, and PNG exports.
- Eight-page Streamlit reviewer journey and a complete automated test suite.

## Phase 5 — Capstone Dashboard UI

Phase 5 adds a unified capstone dashboard that brings together the outputs of Phases 1–4 into one coherent Streamlit experience.

Phase 5 provides:

- **Portfolio dashboard context** — a single combined context object that assembles all Phase 1–4 outputs for the portfolio-level dashboard.
- **Client dashboard context** — a per-client context combining stages, indicator, journey summary, and recommendation summary in one place.
- **Dashboard status classification** — Strong capstone dashboard, Portfolio-ready dashboard, Developing dashboard, or Needs review, based on capstone readiness, journey health, and evidence strength.
- **Dashboard focus** — deterministic text directing consulting attention to the most important action, based on evidence and journey health.
- **Headline metrics** — eight dashboard metrics covering client count, build area count, capstone readiness counts, journey health counts, and evidence health counts.
- **Client spotlight** — a Streamlit selectbox for choosing a client and displaying their full consulting profile: organisation, sector, stage, journey health, capstone readiness, commercial next step, improvement area, and recommendation priority.
- **Client journey table** — one row per client showing journey health, completion rate, average evidence score, weakest stage, and next journey step.
- **Cross-build evidence table** — one row per build area showing evidence health, completion rate, and build gap.
- **Recommendation pathway table** — one row per client showing capstone readiness, consulting pathway, commercial next step, and priority.

## Phase 6 — Capstone Report Builder

Phase 6 adds a deterministic Markdown capstone report builder that converts all Phase 1–5 outputs into a structured consulting report.

Phase 6 provides:

- **Portfolio-level capstone report** — one complete Markdown report covering all three synthetic clients and all seven build areas.
- **Client-level capstone report** — a scoped report covering one client's journey, evidence, and recommendation pathway.
- **Executive summary** — concise bullet-point summary: client count, total stages, completed stages, strongest and weakest build areas, portfolio readiness, and recommended next step.
- **Client overview section** — table of organisation name, sector, staff count, capstone stage, primary AI goal, and consulting priority.
- **Capstone snapshot section** — dashboard status, dashboard focus, strongest and weakest build areas, and recommended next step.
- **AI adoption journey section** — table of journey health, completion rate, average evidence score, weakest stage, and next journey step per client.
- **Cross-build evidence section** — table of all seven build areas with evidence health, completion rate, build gap, and cross-build recommendation.
- **Consulting recommendation pathway section** — table of capstone readiness, consulting pathway, commercial next step, improvement area, priority, and consulting recommendation per client.
- **Consulting interpretation** — deterministic narrative connecting Builds 1–8 into one consulting story.
- **Next steps section** — one deterministic bullet per client based on capstone readiness classification.

## Phase 7 — Export Centre and Portfolio Evidence Pack

Phase 7 adds an Export Centre that packages the capstone dashboard and report outputs into reusable portfolio evidence formats.

Phase 7 provides:

- **Markdown capstone report export** — full capstone report as a downloadable plain-text Markdown file, scoped to portfolio-level or one client.
- **CSV capstone evidence export** — flat evidence table with one row per client/build stage combination, including journey stage, status, evidence strength, readiness indicators, and consulting recommendation.
- **JSON portfolio evidence pack** — structured JSON file containing all capstone data, phase summaries, journey summaries, cross-build summaries, consulting recommendations, and dashboard snapshot.
- **Portfolio evidence summary** — structured summary dict covering client count, stage count, evidence counts, capstone readiness breakdown, strongest and weakest build areas, and dashboard status.
- **Portfolio evidence summary text** — concise Markdown narrative covering what Build 9 does, synthetic data disclaimer, Builds 1–8 evidence summary, capstone readiness position, and recommended next step.
- **PDF export** — basic PDF generated from the Markdown report using reportlab, declared in `requirements.txt`.
- **PNG chart export** — simple capstone readiness bar chart generated using matplotlib, declared in `requirements.txt`.
- **Streamlit Export Centre page** — download buttons for all formats, portfolio evidence metrics, report scope selector, evidence summary text preview, and consulting interpretation.

## Phase 8 — Final Sweep, Commercial Positioning, and README Polish

Phase 8 completes Build 9 with a final quality sweep, commercial positioning pass, and portfolio notes.

Phase 8 provides:

- **Final Review page** — Streamlit page summarising completion status, commercial positioning, portfolio value, limitations, and recommended next steps.
- **Completion review notes** — detailed review of all phases, consulting value, connections to Builds 1–8, limitations, and future upgrade path.
- **Portfolio summary notes** — portfolio-ready summary covering the problem it solves, target users, key features, consulting use cases, and what it demonstrates commercially.
- **Commercial positioning notes** — one-sentence offer, ideal customer, core pain points, practical outcomes, consulting delivery use case, productisation potential, and suggested demo narrative.

## Build 9 Completion Status

Build 9 is complete. It includes:

1. Synthetic capstone client data — three organisations, 21 journey stages, three indicators
2. Client journey overview engine — health classification, completion rate, evidence scoring
3. Cross-build insight aggregator — evidence health for all seven build areas
4. Consulting recommendation pathway — readiness, consulting pathway, commercial next step
5. Capstone dashboard UI — metrics, client spotlight, journey table, evidence table, recommendation table
6. Capstone report builder — Markdown capstone report at portfolio or client scope
7. Export centre and portfolio evidence pack — Markdown, CSV, JSON, PDF, and PNG exports
8. Final review and commercial positioning — completion summary and commercial narrative

**All phases: Complete**

## Commercial Positioning

Build 9 is the capstone wrapper for Builds 1–8. It demonstrates the full AI adoption consulting journey from readiness diagnosis through to tracked implementation delivery and client-facing reporting.

It is suitable for:

- **Portfolio demonstration** — walk a recruiter, evaluator, or prospective client through the full consulting methodology in one session.
- **Business development** — use the capstone report and evidence pack as a leave-behind after a discovery conversation.
- **Consulting methodology demonstration** — show how client evidence could move through a structured engagement while keeping this build synthetic-only.
- **Future productisation** — the methodology, logic, and export structure are designed to support a subscription consulting toolkit or client-facing portal.

This is not a production system. It uses synthetic data only, has no authentication, database, cloud deployment, or external LLM APIs, and requires human review before any real-world consulting use.

## How Build 9 Connects Builds 1–8

```text
Build 1   — Readiness and workflow diagnosis
Build 2/3 — Document intelligence and RAG evidence
Build 4   — Staff training and enablement
Build 5   — Consulting report generation
Build 6   — Governance and responsible AI controls
Build 7   — ROI, adoption, and impact tracking
Build 8   — Delivery and implementation tracking
Build 9   — Capstone dashboard, report, and evidence pack
```

Each build appears in the capstone as a journey stage, a cross-build evidence row, a column in the CSV export, and a section of the JSON evidence pack.

## Completed Phases

1. Phase 1 — Scaffold and Synthetic Capstone Client Data — Complete
2. Phase 2 — Client Journey Overview Engine — Complete
3. Phase 3 — Cross-Build Insight Aggregator — Complete
4. Phase 4 — Consulting Recommendation Pathway — Complete
5. Phase 5 — Capstone Dashboard UI — Complete
6. Phase 6 — Capstone Report Builder — Complete
7. Phase 7 — Export Centre and Portfolio Evidence Pack — Complete
8. Phase 8 — Final Sweep, Commercial Positioning, and README Polish — Complete

## How to Run the App

From this directory:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## How to Run Tests

```bash
pytest
```

## Export Formats

The Export Centre provides:

- Markdown capstone reports at portfolio or selected-client scope
- CSV cross-build evidence
- JSON portfolio evidence packs
- PDF reports via reportlab
- PNG readiness charts via matplotlib

All exports are generated from synthetic demonstration data.

## Suggested Demo Flow

1. Start with Capstone Client Setup
2. Review Client Journey Overview
3. Open Cross-Build Insight Aggregator
4. Review Consulting Recommendation Pathway
5. Open Capstone Dashboard
6. Generate a Capstone Report
7. Use Export Centre to download evidence
8. Finish with Final Review
