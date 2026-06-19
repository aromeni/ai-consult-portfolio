# Build 9 — AI Adoption Consulting Capstone Dashboard

Build 9 is the capstone wrapper for the AI adoption consulting portfolio. It connects the previous builds into one end-to-end consulting journey and packages the result as a dashboard, report, and evidence pack.

---

## Overview

Build 9 is a Streamlit dashboard that aggregates synthetic evidence from Builds 1–8 — the seven AI adoption consulting tools built throughout this portfolio — into one structured client-facing view. It produces a consulting report, a recommendation pathway, and downloadable evidence in five formats.

Everything is built with deterministic Python logic and synthetic data. No external AI APIs, no real client data, no database, no authentication.

**172 automated tests, all passing.**

---

## Why This Build Exists

Most AI consulting portfolios demonstrate individual capabilities: a readiness tool here, a governance checker there. What they rarely show is how those tools connect into one coherent consulting story — how a consultant actually moves a client organisation from initial diagnosis to governed implementation to commercial outcome.

Build 9 answers that question. It shows:

- How evidence from eight different consulting tools becomes one picture of a client's AI adoption position.
- How that picture translates into a consulting recommendation and a commercial next step.
- How the result is packaged as a report, a dashboard, and an evidence pack — the actual deliverables of a consulting engagement.

---

## How It Connects Builds 1–8

| Build | Tool | What Build 9 Draws On |
|---|---|---|
| Build 1 | AI Readiness + Workflow Audit Tool | Readiness findings and workflow priority identification |
| Build 2/3 | Document Intelligence / Semantic RAG | Document handling capability and retrieval demonstration |
| Build 4 | AI Staff Training + Workshop Generator | Training delivery, workshop design, and staff confidence |
| Build 5 | AI Consulting Report Generator | Structured consulting report and client-facing recommendations |
| Build 6 | AI Governance Policy Checker | Governance maturity, policy gaps, and control readiness |
| Build 7 | AI Adoption ROI and Impact Tracker | ROI evidence, workflow impact, and adoption decisions |
| Build 8 | AI Adoption Delivery and Implementation Tracker | Implementation actions, blockers, and delivery progress |

Each build appears in Build 9 as a journey stage, a cross-build evidence row, a column in the CSV export, and a section of the JSON evidence pack.

---

## Key Features

| Feature | Page |
|---|---|
| Three synthetic client organisations with 21 cross-build journey stages | 1 — Capstone Client Setup |
| Deterministic journey health engine (Strong / Healthy / Developing / Needs Review / Blocked) | 2 — Client Journey Overview |
| Cross-build evidence aggregator with client-build status matrix | 3 — Cross-Build Insight Aggregator |
| Capstone readiness classification and commercial next step selection | 4 — Consulting Recommendation Pathway |
| Unified dashboard with Client Spotlight and three summary tables | 5 — Capstone Dashboard |
| Structured Markdown capstone report at portfolio or client scope | 6 — Capstone Report Builder |
| Five export formats: Markdown, CSV, JSON, PDF, PNG | 7 — Export Centre |
| Completion summary, limitations, and commercial positioning | 8 — Final Review |

---

## Demo Flow

The recommended demo order follows the Streamlit sidebar navigation:

1. **Capstone Client Setup** — show the three synthetic clients, 21 journey stages, and portfolio indicators
2. **Client Journey Overview** — show journey health, completion rate, evidence score, and prioritised client review
3. **Cross-Build Insight Aggregator** — show build-area evidence health and the client-build status matrix
4. **Consulting Recommendation Pathway** — show capstone readiness classification and commercial next step
5. **Capstone Dashboard** — show the unified view with Client Spotlight and summary tables
6. **Capstone Report Builder** — generate a portfolio-level or client-scoped consulting report
7. **Export Centre** — download Markdown, CSV, JSON, PDF, and PNG evidence
8. **Final Review** — close with completion status and limitations

Allow 8–12 minutes for a business audience. See `portfolio_notes/build_9_demo_walkthrough.md` for a full presenter script, talking points, and suggested audience adaptation.

---

## Screenshots

Screenshots should be captured manually from the Streamlit app and saved in the `screenshots/` folder using the filenames listed below.

| File | Page | What It Shows |
|---|---|---|
| `01-capstone-client-setup.png` | 1 — Capstone Client Setup | Synthetic client table, journey stages, and portfolio indicators |
| `02-client-journey-overview.png` | 2 — Client Journey Overview | Journey health classification and prioritised review table |
| `03-cross-build-insight-aggregator.png` | 3 — Cross-Build Insight Aggregator | Build-area evidence health and client-build status matrix |
| `04-consulting-recommendation-pathway.png` | 4 — Consulting Recommendation Pathway | Capstone readiness and commercial next step per client |
| `05-capstone-dashboard.png` | 5 — Capstone Dashboard | Unified dashboard with Client Spotlight |
| `06-capstone-report-builder.png` | 6 — Capstone Report Builder | Rendered Markdown consulting report |
| `07-export-centre.png` | 7 — Export Centre | Download buttons for all five export formats |
| `08-final-review-commercial-positioning.png` | 8 — Final Review | Completion status and limitations |

See `screenshots/README.md` for detailed capture instructions per screenshot.

---

## Export Formats

The Export Centre (page 7) provides all of the following:

| Format | Content | Use Case |
|---|---|---|
| Markdown (`.md`) | Full capstone report at portfolio or client scope | Copy into a proposal, client document, or portfolio |
| CSV (`.csv`) | Flat evidence table, one row per client/build stage | Review in spreadsheet, share with stakeholders |
| JSON (`.json`) | Structured evidence pack with all capstone data | Structured record, future integration |
| PDF (`.pdf`) | Formatted consulting report ready for email | Client leave-behind after a discovery meeting |
| PNG (`.png`) | Capstone readiness bar chart | Slide deck, presentation, LinkedIn post |

All exports are generated from synthetic demonstration data.

---

## Commercial Positioning

Build 9 is suitable for:

- **Portfolio demonstration** — walk a prospect, recruiter, or evaluator through the full AI adoption consulting methodology in one session (8–12 minutes).
- **Business development** — use the PDF capstone report and PNG chart as a leave-behind after a discovery conversation.
- **Consulting methodology proof** — demonstrate a structured, repeatable, evidence-backed approach to AI adoption consulting across six UK sectors: training providers, universities, charities, NHS teams, housing associations, professional services.
- **Future productisation** — the methodology, logic, and export structure are ready to accept real client data and live integrations without redesign.

This is not a production system. See `portfolio_notes/build_9_commercial_case_study.md` for the full commercial case study including future productisation path.

---

## Technical Architecture

```
app.py                          ← Streamlit presentation layer only
│
├── data/
│   └── synthetic_capstone_data.py   ← All synthetic clients, stages, indicators
│
├── logic/
│   ├── capstone_overview.py         ← Phase 1 summary and validation
│   ├── client_journey.py            ← Journey health engine
│   ├── cross_build_insights.py      ← Build-area evidence aggregation
│   ├── recommendation_pathway.py    ← Capstone readiness and commercial next step
│   ├── capstone_dashboard.py        ← Dashboard context assembly
│   ├── capstone_report.py           ← Markdown report builder
│   └── export_centre.py             ← All export format generators
│
└── tests/
    ├── test_synthetic_capstone_data.py
    ├── test_capstone_overview.py
    ├── test_client_journey.py
    ├── test_cross_build_insights.py
    ├── test_recommendation_pathway.py
    ├── test_capstone_dashboard.py
    ├── test_capstone_report.py
    └── test_export_centre.py
```

**Design principles:**
- All logic is in pure functions in `logic/` — no side effects, fully testable.
- `app.py` only handles data loading and rendering — no business logic.
- All data comes from `data/synthetic_capstone_data.py` — one source of truth.
- No shared mutable state between Streamlit pages.
- British English throughout — consulting vocabulary, labels, and report text.

---

## Project Structure

```
ai_adoption_consulting_capstone/
├── app.py
├── requirements.txt
├── pytest.ini
├── README.md
├── data/
│   └── synthetic_capstone_data.py
├── logic/
│   ├── capstone_overview.py
│   ├── client_journey.py
│   ├── cross_build_insights.py
│   ├── recommendation_pathway.py
│   ├── capstone_dashboard.py
│   ├── capstone_report.py
│   └── export_centre.py
├── tests/
│   ├── test_synthetic_capstone_data.py
│   ├── test_capstone_overview.py
│   ├── test_client_journey.py
│   ├── test_cross_build_insights.py
│   ├── test_recommendation_pathway.py
│   ├── test_capstone_dashboard.py
│   ├── test_capstone_report.py
│   └── test_export_centre.py
├── screenshots/
│   └── README.md
└── portfolio_notes/
    ├── README.md
    ├── build_9_phase_1_notes.md
    ├── build_9_phase_2_notes.md
    ├── build_9_phase_3_notes.md
    ├── build_9_phase_4_notes.md
    ├── build_9_phase_5_notes.md
    ├── build_9_phase_6_notes.md
    ├── build_9_phase_7_notes.md
    ├── build_9_completion_review.md
    ├── build_9_portfolio_summary.md
    ├── build_9_commercial_positioning.md
    ├── build_9_demo_walkthrough.md
    └── build_9_commercial_case_study.md
```

---

## How to Run

From this directory:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

Start with **1. Capstone Client Setup** in the sidebar and follow the navigation through all eight pages.

---

## How to Run Tests

From this directory:

```bash
pytest
```

Expected output: **172 passed**

To run a specific test file:

```bash
pytest tests/test_client_journey.py
pytest tests/test_export_centre.py
```

---

## Synthetic Data and Safety

All data in this build is synthetic:

- Three fictional client organisations: BrightPath Digital Services, Northside Housing Association, Greenacre Professional Services.
- 21 cross-build journey stages, designed to produce a range of positive, mixed, and review-needed consulting outcomes.
- Three capstone portfolio indicators.

No real client data, personal data, learner records, safeguarding data, HR data, or regulated information is used anywhere in this build.

No external AI APIs are used. The build contains no calls to OpenAI, Claude, LangChain, LlamaIndex, or any language model. All outputs are deterministic Python logic.

---

## Limitations

- **Synthetic data only.** This build uses fictional client organisations and fictional evidence records. It is a demonstration of the methodology, not a record of real consulting outcomes.
- **No authentication.** There is no user login. This is not suitable for storing real client data.
- **No database.** All data is in-process. Nothing persists between sessions.
- **No production deployment.** This is a local Streamlit app, not a cloud-hosted service.
- **No external integrations.** Builds 1–8 are not live-connected to Build 9. Evidence flows through synthetic data, not real tool outputs.
- **Human review required.** Any real-world consulting use of this methodology requires human judgement and review before delivery to a client.

---

## Future Improvements

A production version of this consulting tool would add:

1. Real client data input — form or file upload replacing the synthetic data module.
2. Authentication — per-consultant login for private client portfolios.
3. Persistent database — client data, journey stages, and evidence records stored across sessions.
4. Multi-tenant architecture — one dashboard instance per consulting firm.
5. Cloud deployment — hosted access without a local install.
6. Live integrations — evidence flowing directly from Builds 1–8 into the capstone layer.

The methodology, logic, report structure, and export formats are already production-ready. The infrastructure is the remaining gap.

---

## Portfolio Status

| Phase | Title | Status |
|---|---|---|
| 1 | Scaffold and Synthetic Capstone Client Data | Complete |
| 2 | Client Journey Overview Engine | Complete |
| 3 | Cross-Build Insight Aggregator | Complete |
| 4 | Consulting Recommendation Pathway | Complete |
| 5 | Capstone Dashboard UI | Complete |
| 6 | Capstone Report Builder | Complete |
| 7 | Export Centre and Portfolio Evidence Pack | Complete |
| 8 | Final Sweep and Commercial Positioning | Complete |

**All 8 phases complete. 172 tests passing. Ready for portfolio presentation.**

---

*Build 9 — AI Adoption Consulting Capstone Dashboard · Rashid AI Consult*  
*Synthetic data only. Not professional consulting, legal, financial, or HR advice.*
