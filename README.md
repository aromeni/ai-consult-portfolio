# Rashid AI Consult — AI Adoption Consulting Portfolio

A ten-build software portfolio demonstrating a complete, structured AI adoption consulting methodology — from initial readiness diagnosis through to tracked implementation delivery and client-facing reporting.

Built by **Rashid Omeni**, AI adoption consultant at **Rashid AI Consult**.

---

## What This Portfolio Demonstrates

Each build maps to a distinct phase of an AI adoption consulting engagement. Together they cover the full journey a client organisation goes through when adopting AI responsibly:

| Build | Tool | Consulting Phase |
|---|---|---|
| [Build 1](builds/brightpath-ai-readiness-tool/) | AI Readiness + Workflow Audit Tool | Discovery — identify safe AI opportunities and hard exclusions |
| [Build 2](builds/document-intelligence-rag-demo/) | Document Intelligence / RAG Demo | Document capability — index and retrieve over client document collections |
| [Build 3](builds/semantic-rag-policy-assistant/) | Semantic RAG Policy Assistant | Knowledge retrieval — semantic search over policy and guidance documents |
| [Build 4](builds/ai-staff-training-workshop-generator/) | AI Staff Training + Workshop Generator | Training — design and deliver sector-specific staff AI training sessions |
| [Build 5](builds/ai-consulting-report-generator/) | AI Consulting Report Generator | Reporting — produce structured client-facing consulting reports |
| [Build 6](builds/ai-governance-policy-checker/) | AI Governance Policy Checker | Governance — review policy maturity and close responsible AI gaps |
| [Build 7](builds/ai_adoption_roi_impact_tracker/) | AI Adoption ROI and Impact Tracker | Impact — measure time savings, adoption decisions, and workflow evidence |
| [Build 8](builds/ai_adoption_delivery_tracker/) | AI Adoption Delivery and Implementation Tracker | Delivery — track implementation actions, blockers, and governance sign-off |
| [Build 9](builds/ai_adoption_consulting_capstone/) | AI Adoption Consulting Capstone Dashboard | Capstone — connect all eight phases into one portfolio evidence view |
| [Build 10](builds/production_ai_document_intelligence_governance_agent/) | AI Document Intelligence & Governance Agent | Flagship technical build — semantic RAG, governance checks, report generation, 386-test suite |

---

## Quick Start

### Option A — Docker (recommended, no Python setup required)

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
git clone https://github.com/aromeni/ai-consult-portfolio
cd ai-consult-portfolio
docker compose up
```

First run builds all ten images — allow 5–10 minutes. Subsequent starts are instant.

Open **http://localhost:8509** — the capstone dashboard — as the entry point.

Stop everything:

```bash
docker compose down
```

---

### Option B — Run without Docker

Requires Python 3.11+ and pip.

```bash
git clone https://github.com/aromeni/ai-consult-portfolio
cd ai-consult-portfolio
for req in builds/*/requirements.txt; do pip install -r "$req" -q; done
bash launch_all.sh
```

Stop everything:

```bash
bash launch_all.sh stop
```

---

### Run a single build (no Docker)

```bash
cd builds/<build-folder>
pip install -r requirements.txt
streamlit run app.py
```

---

## Port Reference

| Port | Build |
|---|---|
| 8501 | Build 1 — AI Readiness + Workflow Audit Tool |
| 8502 | Build 2 — Document Intelligence / RAG Demo |
| 8503 | Build 3 — Semantic RAG Policy Assistant |
| 8504 | Build 4 — AI Staff Training + Workshop Generator |
| 8505 | Build 5 — AI Consulting Report Generator |
| 8506 | Build 6 — AI Governance Policy Checker |
| 8507 | Build 7 — AI Adoption ROI and Impact Tracker |
| 8508 | Build 8 — AI Adoption Delivery and Implementation Tracker |
| 8509 | Build 9 — AI Adoption Consulting Capstone Dashboard |
| 8510 | Build 10 — AI Document Intelligence & Governance Agent |

---

## Run the Tests

Each build has its own pytest suite. From any build directory:

```bash
pytest
```

Build 9 alone has 172 tests, all passing. Build 10 has 386 tests, all passing.

---

## Who This Is For

The consulting service works with any UK organisation using or considering AI tools where responsible adoption matters:

- Training providers and adult education colleges
- Universities and further education
- Charities and non-profit organisations
- NHS teams and healthcare organisations
- Housing associations
- Professional services — accountants, solicitors, consultancies

---

## Technical Notes

**Stack:** Python · Streamlit · sentence-transformers · FAISS · pandas · numpy · pytest · reportlab · matplotlib

**Data:** All ten builds use synthetic demonstration data only. No real client data, personal data, or learner records are used anywhere in this portfolio.

**Architecture:** Each build is an independent Streamlit application with its own `requirements.txt`, `logic/` module layer, `data/` layer, and `tests/` suite. No shared dependencies between builds.

**External APIs:** None by default. Builds 1–9 are fully offline. Build 10 uses sentence-transformers (all-MiniLM-L6-v2, ~90MB, downloaded once and cached locally on first run) and FAISS for local semantic retrieval — no API key required. An optional OpenAI integration path is documented in Build 10's `.env.example` but is not called in the default mode.

**Build 10 note:** Build 10 is a production-style local Streamlit prototype demonstrating semantic document retrieval, evidence-based Q&A with citations, governance risk checks, structured report generation, and a 386-test suite. It is not a deployed SaaS product.

**Language:** British English throughout.

---

## Suggested Demo Flow

Start at **http://localhost:8509** (Build 9 — Capstone Dashboard) and follow the eight-phase navigation. Dip into individual builds on the other ports to show the underlying tools in detail.

For a deep technical walkthrough, go to **http://localhost:8510** (Build 10 — AI Document Intelligence & Governance Agent). Load the embedding model, build the FAISS index, run a policy query, review the governance risk flags, and export a structured Markdown report.

For a guided walkthrough, timing guide, and audience-specific talking points, see the demo script in the full consulting portfolio.

---

## About Rashid AI Consult

Rashid AI Consult provides structured AI adoption consulting for UK organisations. The service covers every phase of responsible AI adoption — from initial workflow diagnosis and governance review through to staff training, impact measurement, and tracked implementation delivery.

**Contact:** aromeni@gmail.com

---

## Licence

This portfolio is shared for demonstration purposes. The consulting methodology, templates, and software builds are the work of Rashid Omeni. Not for redistribution or commercial use without permission.
