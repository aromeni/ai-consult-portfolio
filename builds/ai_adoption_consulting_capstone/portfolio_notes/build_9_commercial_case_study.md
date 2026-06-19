# Case Study: AI Adoption Consulting Capstone Dashboard

**Rashid AI Consult — Build 9**  
**Portfolio — Synthetic Demonstration — June 2026**

---

## Summary

Build 9 is a synthetic but realistic AI adoption consulting capstone dashboard that brings readiness diagnosis, document intelligence, staff training, governance policy review, ROI tracking, delivery tracking, structured reporting, and exportable evidence into one coherent client-facing journey. It is built with Python, Streamlit, and deterministic consulting logic, using synthetic data only, with no external AI APIs.

It demonstrates the methodology, architecture, and commercial product thinking behind a structured AI adoption consulting practice — without using real client data.

---

## The Problem

Small organisations adopting AI — charities, housing associations, NHS teams, training providers, universities, accountancy firms, and professional services businesses — typically face the same challenge: they get isolated, disconnected advice.

A readiness tool says they are partially ready. A governance checklist says they have gaps. A training provider runs a workshop. A consultant writes a report. None of these connect. There is no single place where the evidence from each stage is collected, analysed, and presented as one coherent picture of where the organisation is in its AI adoption journey.

As a result:

- Consultants cannot easily show clients what has been done across all phases.
- Clients cannot easily understand how much progress they have made or what to do next.
- Evidence that justifies continued investment or a commercial next step is scattered or absent.
- Portfolio reviewers cannot tell whether the consultant thinks structurally or just delivers isolated tools.

---

## The Target User

**Primary:** AI adoption consultants and freelancers working with UK small organisations who need a structured, evidence-backed way to manage and present a client's AI adoption journey.

**Secondary:** Prospective clients — small organisation decision-makers — who want to understand what a structured consulting engagement would look like before committing.

**Portfolio:** Technical reviewers, recruiters, and evaluators assessing whether the consultant can build, position, and present a coherent AI consulting product.

---

## The Solution

Build 9 is the capstone layer for the AI adoption consulting portfolio. It connects the outputs of Builds 1–8 — each of which represents a distinct phase of an AI adoption engagement — into one structured dashboard, consulting report, and exportable evidence pack.

It does not rebuild the previous tools. Instead, it models the evidence those tools would produce, aggregates it across clients and build areas, applies deterministic consulting logic, and presents the result as a client-facing consulting view.

---

## What I Built

| Component | Description |
|---|---|
| Synthetic capstone data | Three client organisations, 21 cross-build journey stages, three portfolio indicators — designed to produce a range of positive, mixed, and review-needed consulting outcomes |
| Client journey overview engine | Deterministic health classification (Strong / Healthy / Developing / Needs Review / Blocked) with completion rate, evidence scoring, weakest-stage identification, and prioritised review list |
| Cross-build insight aggregator | Evidence health across all seven build areas, client-build status matrix, and prioritised improvement list |
| Consulting recommendation pathway | Capstone readiness classification, consulting pathway assignment, commercial next step selection, and recommendation priority triage |
| Capstone dashboard UI | Portfolio-level and client-level metrics, Client Spotlight, and three summary tables |
| Capstone report builder | Structured Markdown report at portfolio or client scope, covering executive summary, journey analysis, cross-build evidence, recommendation pathway, and next steps |
| Export centre | Markdown, CSV, JSON, PDF (reportlab), and PNG (matplotlib) exports |
| Final review page | Completion status, commercial positioning, limitations, and recommended next steps |
| Automated test suite | 172 tests covering all logic modules |

---

## How It Works

1. **Synthetic data layer** — `data/synthetic_capstone_data.py` defines three client organisations (BrightPath Digital Services, Northside Housing Association, Greenacre Professional Services), 21 journey stages linking each client to each build area with a status and evidence strength, and three portfolio indicators.

2. **Logic layer** — Six logic modules in `logic/` handle the analytical pipeline:
   - `capstone_overview.py` — Phase 1 summary and validation
   - `client_journey.py` — journey health classification and prioritisation
   - `cross_build_insights.py` — build-area evidence aggregation
   - `recommendation_pathway.py` — capstone readiness and commercial next step
   - `capstone_dashboard.py` — dashboard context assembly
   - `capstone_report.py` — Markdown report builder
   - `export_centre.py` — all export format generators

3. **Presentation layer** — `app.py` renders eight Streamlit pages using the logic layer outputs. No logic lives in the app file — it only handles data loading and rendering.

4. **Test suite** — `tests/` contains one test file per logic module, covering 172 individual assertions across all functions.

---

## Consulting Journey

| Build 9 Phase | Consulting Phase | Purpose |
|---|---|---|
| 1 — Capstone Client Setup | Client intake and scoping | Establish the starting evidence position across all phases |
| 2 — Client Journey Overview | Discovery review and journey mapping | Analyse progress and health across the full adoption pathway |
| 3 — Cross-Build Insight Aggregator | Evidence aggregation and gap analysis | Identify which consulting areas are strong and where gaps remain |
| 4 — Consulting Recommendation Pathway | Consulting advice and commercial proposal | Convert evidence into a practical consulting direction and next step |
| 5 — Capstone Dashboard | Client-facing review session | Present the full picture in one place with headline metrics |
| 6 — Capstone Report Builder | Consulting report and follow-up document | Produce a structured, readable client-facing report |
| 7 — Export Centre | Evidence submission and portfolio packaging | Package evidence in reusable formats for client delivery |
| 8 — Final Review | Engagement review and commercial positioning | Summarise completion, acknowledge limitations, set next steps |

---

## Outputs

The dashboard produces the following outputs, all generated from synthetic data:

- **Structured consulting report** — Markdown, scoped to portfolio or individual client
- **CSV evidence table** — flat file with one row per client/build stage, suitable for spreadsheet review
- **JSON evidence pack** — structured export of all capstone data, phase summaries, and recommendations
- **PDF report** — consulting report formatted for client delivery (via reportlab)
- **PNG readiness chart** — capstone readiness bar chart for presentations (via matplotlib)
- **Dashboard metrics** — eight headline metrics for the portfolio-level view
- **Client Spotlight** — full consulting profile for any selected client

---

## Commercial Value

Build 9 is designed to support the following commercial use cases:

**Portfolio demonstration** — A prospective client or recruiter can be walked through the full AI adoption consulting methodology in 8–12 minutes. The dashboard provides a structured narrative from diagnosis to evidence pack without requiring a live client engagement.

**Business development leave-behind** — After a discovery conversation, the Markdown or PDF capstone report can be sent as a structured evidence document. It looks and reads like a consulting report, not a prototype screenshot.

**Consulting methodology proof** — The commercial next steps generated by the recommendation pathway — Portfolio demonstration, Paid implementation review, Governance improvement sprint, Training and adoption support package, Document intelligence upgrade, Delivery tracking retainer — show that the methodology is wired to produce commercial directions, not just analytical outputs.

**Future client onboarding** — The data layer and logic are structured to accept real client evidence with minimal modification. The synthetic clients would be replaced by real client organisations; the logic, report structure, and export formats would remain unchanged.

---

## Responsible AI and Data Handling

- All data in this build is synthetic. Three fictional organisations — BrightPath Digital Services, Northside Housing Association, and Greenacre Professional Services — were designed to produce a range of consulting outcomes across the dashboard.
- No real client data, personal data, learner records, safeguarding data, or regulated information is used anywhere in this build.
- No external AI APIs are used. The build contains no calls to OpenAI, Claude, LangChain, LlamaIndex, or any language model. All outputs are deterministic Python logic.
- The Final Review page includes an explicit limitations declaration: this is a synthetic demonstration that requires human review before any real-world consulting use.
- The sidebar in every page of the Streamlit app carries a disclaimer: "Synthetic data only. Not professional consulting, legal, financial, or HR advice."

---

## Technical Implementation

**Stack:** Python 3.11 · Streamlit · pytest · reportlab · matplotlib

**Architecture:**
- `data/` — synthetic data module (one file, one source of truth)
- `logic/` — seven pure-function modules with no side effects (testable, modular)
- `tests/` — one test file per logic module (172 tests, all passing)
- `app.py` — presentation only, no logic (renders phase functions using logic layer outputs)
- `requirements.txt` — four dependencies: streamlit, pytest, reportlab, matplotlib

**Design decisions:**
- No database — all data is in-process Python dictionaries.
- No authentication — this is a demonstration build, not a production system.
- No shared state between pages — each Streamlit page loads data and renders independently.
- British English throughout — consulting vocabulary, UI labels, and report text.
- No external API calls — the build is safe to run in any environment without API keys.

**Test philosophy:** All logic functions are pure — they take inputs and return outputs with no side effects. This makes the test suite fast, reliable, and free of mocking. 172 assertions cover all functions across all six logic modules, including edge cases for missing data, boundary evidence scores, and all classification branches.

---

## What This Demonstrates

| Skill | Evidence |
|---|---|
| Streamlit product design | Eight-page structured consulting application with metrics, tables, selectbox, download buttons |
| Deterministic consulting logic | Journey health, evidence aggregation, readiness classification, commercial next step — all deterministic Python |
| Synthetic data modelling | Three clients, 21 stages, three indicators — designed to produce a range of consulting outcomes |
| Test-driven implementation | 172 tests across all logic modules, written before or alongside implementation |
| Exportable portfolio evidence | Five export formats: Markdown, CSV, JSON, PDF, PNG |
| Responsible AI awareness | Explicit limitations, synthetic-only disclaimer, no external AI APIs, human review required |
| AI consulting product thinking | Commercial next steps, recommendation pathway, client spotlight, consulting report structure |
| Commercial positioning | The build positions itself as a consulting offer — not just an engineering exercise |

---

## Future Productisation

Build 9 as a production consulting tool would require:

1. **Client data input** — a form or file upload for real client evidence, replacing the synthetic data module.
2. **Authentication** — per-consultant login so each consultant's client portfolio is private.
3. **Database** — persistent storage for client data, journey stages, and evidence records.
4. **Multi-tenant architecture** — one dashboard instance per consultant or consulting firm.
5. **Cloud deployment** — hosted on a cloud provider so the dashboard is accessible without a local install.
6. **Live integrations** — connections to Builds 1–8 so that client evidence flows directly from the source tool into the capstone layer.

The methodology, logic, report structure, and export formats are already production-ready. The infrastructure required to turn this into a live product is a matter of engineering time and commercial commitment, not a rethink of the approach.

---

## Final Positioning Statement

Build 9 is evidence that a structured, repeatable, evidence-backed AI adoption consulting methodology can be designed, built, tested, and packaged as a software product. It does not claim to be a production system. It claims to demonstrate the thinking, the architecture, the consulting vocabulary, and the commercial product instincts behind a practice that is ready to take on its first real engagement.

> A synthetic but realistic AI adoption consulting capstone dashboard that brings readiness, document intelligence, staff training, governance, ROI tracking, delivery tracking, reporting, and exportable evidence into one structured client-facing journey — built with deterministic Python, tested to 172 assertions, and ready to demonstrate to a prospective client or portfolio reviewer.

---

*Build 9 Commercial Case Study · AI Adoption Consulting Capstone Dashboard · Rashid AI Consult*  
*Synthetic data only. No real client data. No external AI APIs. Human review required before any real-world consulting use.*
