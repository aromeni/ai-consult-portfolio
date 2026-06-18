# Build 6 Portfolio Notes

**AI Governance Policy Checker · BrightPath ChatGPT Mastery Project**

---

## One-Line Summary

A Streamlit-based AI governance prototype that reviews synthetic AI policy text against a responsible AI governance framework, identifies coverage gaps, generates policy improvement recommendations, calculates maturity, and exports a governance report.

---

## Problem Solved

After an AI readiness audit, an AI consultant needs to check whether the organisation's AI policies adequately address responsible AI governance. This tool demonstrates a structured workflow for converting a synthetic policy pack into a governance coverage review, gap identification, improvement recommendations, and a client-facing governance review report — with no LLM, no external API, and clear responsible-use boundaries throughout.

---

## Target Users

- AI consultants reviewing client governance readiness
- Small organisations exploring AI adoption and needing policy review support
- Training providers and educational organisations with AI usage policies
- Compliance and governance teams assessing AI policy coverage
- Operational managers responsible for staff AI-use policies
- Responsible AI programme leads building governance frameworks

---

## Core Workflow

Synthetic Policy Pack → Governance Framework → Coverage Review → Gap Analysis → Recommendations → Maturity Summary → Governance Report → Export

---

## Key Features

- Synthetic BrightPath Skills Training policy pack (6 policies, 12 risk areas)
- 12-domain responsible AI governance framework
- Keyword-based coverage checker (deterministic, no LLM)
- Policy gap analysis with severity classification (Critical / High / Medium / Low)
- Policy improvement recommendation engine with wording directions, implementation steps, review questions, and success criteria
- Governance maturity scoring with domain-level breakdown and maturity blocker identification
- Markdown governance report builder assembling all outputs into a client-facing document
- PDF export with cover page, analytics tables, and embedded chart images
- Matplotlib chart analytics: completion status, coverage levels, gap severities, recommendation priorities, maturity levels, domain governance scores
- Completion review page showing phase, output, and documentation completion status
- Portfolio notes and case study Markdown download

---

## Technical Stack

| Component | Technology |
|---|---|
| App framework | Streamlit |
| Language | Python 3 |
| State management | `st.session_state` |
| PDF export | reportlab |
| Charts | matplotlib (Agg backend) |
| Tests | pytest |
| External AI / LLM | None |

---

## Responsible AI Features

- Synthetic/demo data only — no real client data ever used
- Deterministic keyword-based analysis — no LLM hallucination risk
- Responsible-use warning on every page
- Human review requirement stated throughout all outputs and exports
- Safety boundaries documented in `docs/safety-boundaries.md`
- Prototype limitations disclosed in every report and export
- No production deployment claim
- No compliance certification claim
- No legal, safeguarding, HR, compliance, or professional governance advice

---

## What This Demonstrates

- AI governance consulting product thinking
- Structured audit input design (policy pack + governance framework)
- Deterministic analysis workflow without LLM dependency
- Coverage scoring and gap prioritisation logic
- Multi-step workflow building (coverage → gaps → recommendations → maturity → report → export)
- Report generation and Markdown/PDF export pipeline
- Responsible-use boundary enforcement in a prototype
- Modular Streamlit multi-page architecture with session state as data bus
- End-to-end testing with pytest (783+ tests)

---

## Portfolio Positioning

This build demonstrates how AI governance concerns can be turned into a structured review workflow: synthetic policies are checked against a responsible AI framework, gaps are identified, recommendations are generated, maturity is scored, and a governance review report is exported. It is a strong complement to Build 5 (Consulting Report Generator) and shows how AI consulting moves from readiness diagnosis to governance assurance.

Build 6 closes the governance loop by turning a synthetic policy pack review into structured governance findings, gap identification, improvement recommendations, and a client-ready report — all without external AI APIs and with responsible-use boundaries enforced throughout.

---

## Case Study: BrightPath Skills Training AI Governance Policy Review

**Client context:**
BrightPath Skills Training is a synthetic small UK training provider using AI tools informally across their operations. Staff use AI tools for lesson planning, communication drafting, and administrative tasks, but the organisation lacks a clear AI governance framework. This is a synthetic demo — BrightPath is not a real organisation.

**Challenge:**
The organisation needed clearer policy coverage across approved AI tools, data boundaries, safeguarding, human review, escalation, accuracy controls, bias and fairness, staff training, and monitoring.

**Solution:**
The AI Governance Policy Checker reviewed BrightPath's 6-policy synthetic pack against a 12-domain framework. Coverage gaps were identified and prioritised, recommendations were generated with wording directions, governance maturity was scored, and a full governance review report was exported.

**Consulting value:**
This prototype demonstrates how an AI consultant could structure a governance policy review: load the client's policy pack, apply a governance framework, identify coverage gaps, generate improvement recommendations, score governance maturity, and deliver a written governance review report. In a real engagement, the same workflow would apply to actual client policies with appropriate governance controls and qualified human review.

---

## Suggested LinkedIn / GitHub Description

Built an AI Governance Policy Checker that reviews synthetic organisational AI policy text against a responsible AI governance framework. The prototype identifies coverage gaps, generates policy improvement recommendations, calculates governance maturity, and exports a client-facing governance report with PDF and chart support. It uses deterministic logic, synthetic data only, and clear responsible-use boundaries.

**Skills demonstrated:** AI governance consulting, Streamlit app development, deterministic NLP analysis, PDF generation (reportlab), data visualisation (matplotlib), responsible AI design, software testing (pytest).

---

## How To Demo This Build

```bash
cd 10-builds/ai-governance-policy-checker
source .venv/bin/activate
streamlit run app.py
```

Open at `http://localhost:8501` and follow the demo script in `docs/demo-script.md`.

---

## Relationship to Other Builds

| Build | Relationship |
|---|---|
| Build 1 — AI Readiness Audit | Readiness findings identify governance gaps that Build 6 checks |
| Build 3 — Semantic RAG Policy Assistant | Future integration: retrieve evidence from real policy documents |
| Build 4 — AI Staff Training Generator | Training needs identified in Build 6 can feed Build 4 |
| Build 5 — AI Consulting Report Generator | Governance review outputs can be embedded in a consulting report |

---

*Build 6 · AI Governance Policy Checker · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
