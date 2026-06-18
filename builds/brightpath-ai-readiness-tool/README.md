# BrightPath AI Readiness + Workflow Audit Tool

**A Streamlit prototype that helps small UK training providers assess their AI readiness, audit workflows for safe AI adoption, score risks, and generate a pilot recommendation — all without entering any personal or sensitive data.**

---

## Problem

Small UK training providers want to explore AI tools but face a practical gap: they lack the structure to know where to start, which workflows are safe to pilot, what the risks are, and what governance needs to be in place first.

A consultant walking into one of these organisations needs a fast, credible diagnostic tool — something that asks the right questions, produces evidence-based recommendations, and gives the manager something tangible to take away.

This prototype is that tool.

---

## Target Users

- AI consultants (primary: Rashid) delivering AI readiness diagnostics to small training providers
- Managers of small UK training providers (8–50 staff) considering AI adoption
- Skills training providers, FE colleges, adult education organisations, third-sector organisations
- Document-heavy SMEs wanting a structured AI baseline

---

## Why This Matters

Most small organisations approach AI adoption informally — staff start using tools before governance exists. This creates real risks: learner data entering unapproved tools, safeguarding information being processed without controls, AI outputs being used without verification.

This tool gives a consultant a structured, repeatable process for:
- diagnosing where an organisation actually is on AI readiness
- identifying the lowest-risk workflows to pilot first
- surfacing governance gaps before any pilot begins
- producing a written recommendation the manager can keep

---

## Core Features

| Feature | Phase | Status |
|---|---|---|
| Organisation profile capture | 1 | Live |
| AI Readiness Assessment (10 dimensions, 0–100) | 2 | Live |
| Workflow Audit (10 dimensions, 0–50) | 3 | Live |
| Risk Assessment (10 categories, likelihood × impact) | 4 | Live |
| Pilot Recommendation (combined logic, 6 outcomes) | 5 | Live |
| Markdown + PDF Mini Report generator + download | 6 | Live |
| Portfolio and demo documentation | 7 | Live |

---

## App Pages

| Page | Description |
|---|---|
| Home | Welcome, demo data loader, responsible-use notice |
| Organisation Profile | Shows loaded profile (form in a future phase) |
| AI Readiness Assessment | 10 sliders (0–10 each), live total, category, chart |
| Workflow Audit | Workflow info form + 10 suitability sliders (0–5 each), live score |
| Risk Assessment | 10 risk categories, likelihood × impact (1–5 each), safeguards |
| Pilot Recommendation | Combines readiness, workflow, and risk → 6-category recommendation |
| Mini Report | Editable form, live preview, downloadable `.md` and `.pdf` report. The Mini Report page supports Markdown and PDF downloads. |

---

## Responsible Use Boundaries

This tool is a prototype for indicative assessment only.

- All sample data is synthetic, anonymised, or fictional
- No real learner, client, staff, safeguarding, or confidential data should be entered
- The tool does not provide legal, safeguarding, HR, compliance, medical, financial, or academic-integrity advice
- Outputs are a structured starting point for conversation — not a certified audit result
- Organisations should seek qualified advice for compliance, governance, and legal decisions

---

## Technical Stack

| Component | Technology |
|---|---|
| UI framework | Streamlit |
| Data tables and charts | Pandas |
| Language | Python 3.11 |
| State management | `st.session_state` |
| Deployment | Local (`streamlit run app.py`) |
| External APIs | None |
| Database | None |
| Authentication | None |

---

## Folder Structure

```
brightpath-ai-readiness-tool/
├── app.py                    # Main Streamlit app (7-page navigation)
├── requirements.txt          # streamlit, pandas, reportlab
├── .env.example              # Environment variable template
├── README.md
│
├── src/
│   ├── scoring.py            # All scoring logic — Phases 1–5
│   ├── sample_data.py        # All synthetic sample data
│   ├── report_generator.py   # Report generation — Phase 1 text + Phase 6 Markdown
│   └── utils.py              # Shared helpers, session state init
│
├── data/
│   └── samples/              # Placeholder for future sample documents
│
├── outputs/
│   └── reports/              # Placeholder for locally saved reports
│
├── assets/
│   └── screenshots/          # Portfolio and demo screenshots (synthetic data only)
│
├── docs/
│   ├── build-notes.md        # Phase-by-phase build log
│   ├── portfolio-case-study.md
│   ├── demo-script.md
│   ├── screenshots-checklist.md
│   ├── build-reflection.md
│   └── future-improvements.md
│
└── tests/                    # Placeholder — unit tests planned
```

---

## Setup Instructions

**Requirements:** Python 3.10 or later.

```bash
# 1. Clone or download the project
git clone <repo-url>
cd brightpath-ai-readiness-tool

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment template (no values required for MVP)
cp .env.example .env
```

---

## How to Run

```bash
streamlit run app.py
```

Opens at `http://localhost:8501` by default. The server must be running each time you use the tool.

---

## Running Tests

```bash
pytest
```

Run from the `brightpath-ai-readiness-tool/` directory. Tests cover scoring functions (readiness, workflow suitability, risk, pilot recommendation) and report generation (section headings, filename generation). No external services or API calls required.

---

## Demo Scenario

**Organisation:** BrightPath Skills Training — a small UK training provider with 8 staff  
**Context:** Staff are using ChatGPT informally for lesson planning and emails. No AI policy exists.  
**Goal:** Identify whether they can safely pilot AI for generic lesson planning.

**Quick demo path:**

1. Go to **Home** and click **Load BrightPath demo data**
2. Navigate to **AI Readiness Assessment** — see score 35 / 100, category "Early awareness"
3. Navigate to **Workflow Audit** — click **Load BrightPath sample workflow** — score 42 / 50, "Good pilot candidate"
4. Navigate to **Risk Assessment** — click **Load BrightPath sample risk profile** — see Safeguarding as High
5. Navigate to **Pilot Recommendation** — see "Governance-first before pilot" (driven by the High safeguarding risk)
6. Navigate to **Mini Report** — click **Load BrightPath sample report data** — preview and download the `.md` or `.pdf` report

**Key message:** The lesson planning workflow is structurally ready, but the risk profile requires governance controls before any pilot begins.

---

## Limitations

- This is a prototype — outputs are indicative, not certified
- Scores are based on practitioner estimates, not measured data
- The tool does not connect to any external systems, data sources, or AI models
- Organisation Profile page is read-only in this version (form input planned in Phase 8)
- No persistent storage — session data is lost when the app restarts
- No multi-user support — designed for single-session consultant use

---

## Future Improvements

See [docs/future-improvements.md](docs/future-improvements.md) for the full list. Short-term priorities:

- Persistent session state across pages (browser storage or local file)
- Multiple workflow audits in one session
- Organisation Profile input form

---

## Deployment

For instructions on running the app locally or sharing it via Streamlit Community Cloud, see [`docs/deployment-notes.md`](docs/deployment-notes.md).

This is a prototype. Use synthetic BrightPath demo data only. Do not deploy with real learner data, safeguarding information, or confidential client records.

---

## Screenshots

Portfolio and demo screenshots are stored in [`assets/screenshots/`](assets/screenshots/).

For a full checklist of what to capture, what to show on each page, what data to use, and safety rules, see [`docs/screenshots-checklist.md`](docs/screenshots-checklist.md).

All screenshots must use synthetic BrightPath-style data only. Do not capture real personal data, learner records, client information, or safeguarding details.

---

## Connection to the ChatGPT Mastery / GPT Master Project

This tool is the first practical build in the ChatGPT Mastery / GPT Master project (Layer 10 — Practical Builds). It applies the methodology developed across Layers 3–7:

| Layer | Contribution |
|---|---|
| Layer 3 — Consulting methodology | Audit structure, client engagement, recommendation framework |
| Layer 4 — Software build methodology | Prototype design, build phases, demo delivery |
| Layer 5 — Document intelligence | Document classification, RAG-readiness concepts |
| Layer 6 — AI Governance Lab | Risk assessment, acceptable use, human review framework |
| Layer 7 — Teaching and Workshop Lab | Training needs assessment, staff capability, programme design |

---

*Part of: ChatGPT Mastery / GPT Master Project*  
*All sample data is synthetic. This tool provides indicative assessment guidance only.*
