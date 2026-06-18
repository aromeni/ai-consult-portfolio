# Demo Script — AI Governance Policy Checker

**Build 6 · Phases 1–8 · BrightPath ChatGPT Mastery Project**

Demo time: 40–45 minutes for Phases 1–8 walkthrough.

---

## Before You Start

```bash
cd 10-builds/ai-governance-policy-checker
source .venv/bin/activate
streamlit run app.py
```

Open at `http://localhost:8501`.

---

## Step 1: Home Page

Open the Home page.

**What to show:**
- Project title: AI Governance Policy Checker
- Summary: this tool helps an AI consultant review whether an organisation's AI policies contain sufficient responsible-use governance coverage
- Governance review workflow steps: Synthetic Policies → Governance Framework → Policy Coverage Review → Gap Analysis → Recommendations → Governance Report → Export
- Connections to Builds 1–5: explain how readiness findings (Build 1), evidence retrieval (Build 3), training needs (Build 4), and consulting reports (Build 5) all connect to governance policy review
- Prototype notice and responsible-use warning

**Key talking point:**
> "This is the final step in turning an AI readiness audit into actionable client deliverables — checking whether the organisation's policies actually reflect responsible AI governance."

---

## Step 2: Policy Library

Open the Policy Library page.

Click **Load BrightPath Synthetic Policy Pack**.

**What to show:**
- Organisation summary: BrightPath Skills Training, small UK training provider
- Metric row: 6 policies, policy types, risk areas covered
- Policy list with expanders — open one or two policies:
  - POL-001: AI Acceptable Use Policy — approved uses, prohibited uses, human review requirement
  - POL-003: Safeguarding and AI Boundary Policy — absolute safeguarding boundaries
- Risk areas list
- Policy pack Markdown preview (open the expander briefly)

**Key talking point:**
> "The policy pack represents what the organisation has in place. In a real engagement, you'd be reviewing the client's actual policies — this prototype uses synthetic demo content only."

---

## Step 3: Governance Framework

Open the Governance Framework page.

Click **Load Responsible AI Governance Framework**.

**What to show:**
- Metric row: 12 domains, 7 high priority, 5 medium priority
- Governance domain list — open two or three expanders:
  - GOV-006 Safeguarding Boundaries (High priority) — expected evidence, example controls
  - GOV-007 Human Review and Accountability (High priority)
  - GOV-011 Escalation and Incident Reporting (High priority)
- Explain the expected policy evidence and example controls structure

**Key talking point:**
> "This framework defines what good looks like. The Policy Checker on the next page compares the organisation's policy text against each of these 12 domains to identify what's covered and what's missing."

---

## Step 4: Policy Checker

Open the Policy Checker page.

Click **Run Policy Coverage Check**.

**What to show:**
- Overall coverage score and level (e.g. "Partial coverage")
- Progress bar
- Coverage counts: strong / partial / weak / not covered
- High-priority gaps (if any)
- Recommended focus areas
- Best-covered domains and weakest domains side by side
- Domain coverage expanders — open two or three:
  - GOV-006 Safeguarding Boundaries — score, matched policies, evidence snippets
  - GOV-007 Human Review and Accountability — strong evidence across multiple policies
  - GOV-001 Strategy and Ownership — compare with a domain that has less coverage
- Markdown download

**Key talking point:**
> "This is a deterministic keyword-based check — no AI, no LLM, no external API. It searches the synthetic policy text for evidence keywords that relate to each governance domain. In a real engagement, this helps frame the conversation about where the policy pack is strong and where gaps need attention — with a qualified consultant reviewing the outputs."

---

## Step 5: Gap Analysis

Open the Gap Analysis page. The gap analysis runs automatically from the coverage results.

**What to show:**
- Summary metrics: total gaps, critical/high/medium/low counts, domains covered
- Overall gap position (error banner if critical/high gaps exist)
- Highest priority gap — domain, severity, priority score
- Recommended focus areas
- Gap themes (e.g. "Safeguarding governance", "Human review and accountability")
- Prioritised gap table — open two or three expanders:
  - A critical or high gap — show missing evidence, risk statement, action hint
  - A lower severity gap — compare how the detail differs
- Covered domains list
- Markdown download

**Key talking point:**
> "The gap analysis turns the coverage scores into prioritised, actionable gaps. Each gap includes what evidence is missing from the policy pack, what risk the gap creates, and a first-step action hint. The highest-priority gaps are surfaced first so a consultant can focus the client conversation on what matters most — with human review required before any of this is acted on."

---

## Step 6: Recommendations

Open the Recommendations page. Recommendations generate automatically from the gap analysis.

**What to show:**
- Summary metrics: total recommendations, urgent/high/medium/low counts, quick wins
- Overall recommendation position (error banner if urgent/high exist)
- Highest priority recommendation — title, priority, action type, target policy, owner
- Recommended focus areas
- Recommended sequence — open the expanders to show the logical order of steps
- Quick wins — show which recommendations are most straightforward to action
- Owner summary — who needs to act on which recommendations
- Prioritised recommendation table — open two or three expanders:
  - An urgent or high-priority recommendation — show rationale, wording direction, implementation steps
  - Open the nested review questions and success criteria expander
  - A medium-priority recommendation — compare action type and wording direction
- Markdown download

**Key talking point:**
> "Each recommendation tells the consultant what to do, who should own it, which policy to update, how to frame the wording, what steps to take, and how to know it's done. The wording direction is indicative only — it's a starting point for the policy owner to review, not approved text. Human review is required before any policy is actually changed."

---

## Step 7: Governance Maturity

Open the Governance Maturity page. The maturity summary generates automatically from coverage results, gap analysis, and recommendations.

**What to show:**
- Overall governance score (0–100) and progress bar
- Maturity level (Initial / Developing / Defined / Managed / Optimised)
- Maturity description — what this level means in consulting terms
- Adoption readiness position — practical guidance on whether pilots or scaling are appropriate
- Recommended next step — the single most important action
- Governance strengths (domains scoring 75+) and weaknesses (domains below 50) side by side
- Maturity blockers — expand one to show reason and recommended action
- Improvement priorities list
- Domain maturity table — open two or three expanders:
  - A weak domain (Initial or Developing) — show coverage score, maturity score, gap severity, recommended focus
  - A strong domain (Managed or Optimised) — compare the detail
- Markdown download

**Key talking point:**
> "The maturity score combines coverage scores with gap severity and recommendation priority penalties to give a calibrated picture of governance readiness. A high coverage score doesn't automatically mean high maturity — if there's a critical gap in a high-priority domain, the maturity score reflects that. The adoption-readiness position gives the consultant a clear anchor point for the governance conversation."

---

## Step 8: Governance Report

Open the Governance Report page after generating coverage review, gap analysis, recommendations, and maturity summary.

**What to show:**
- Readiness checklist — available outputs (✅) and missing outputs (❌)
- Recommended steps if any outputs are missing
- Section selection checkboxes — show which are preselected (data available) and which are optional
- Click **Generate Governance Report**
- Summary metric cards: organisation, sections available, domains reviewed, gaps included, recommendations, maturity level
- Report readiness position (success if all recommended outputs available)
- Markdown preview expander — scroll through the report structure briefly
- Click through the TOC to show what's included: Cover, Executive Summary, Policy Pack Overview, Coverage Review, Gap Analysis, Recommendations, Maturity Summary, Next Steps, Responsible-Use Boundaries, Prototype Limitations, Appendices
- Download button for the Markdown report

**Key talking point:**
> "This is the assembled governance report — a single Markdown document that combines everything generated in Phases 2 through 5. A consultant could hand this to a client, adapt it for a formal report template, or use Build 5 to embed the key findings into a wider consulting report. Phase 7 will add PDF export and charts."

---

## Step 9: Export Centre

Open Export Centre after generating the governance report.

**What to show:**
- Readiness checklist — available (✅) and missing (❌) outputs
- Missing output guidance (collapsed in expander)
- Package summary metric row: organisation, domains reviewed, gaps, recommendations, maturity level
- Export quality checklist split into Required / Recommended / Advisory columns
- Analytics summary: coverage levels, gap severities, recommendation priorities, governance scores
- Chart previews in 2-column grid: completion status, coverage levels, gap severities, recommendation priorities, maturity levels, domain governance scores
- Download Markdown Governance Report button
- Download PDF Governance Report button (PDF generated with a spinner)
- Responsible-use caption

**Key talking point:**
> "The Export Centre turns everything generated in Phases 2 through 6 into a downloadable governance report package. The Markdown download is a portable, editable governance review document. The PDF is a consulting-style report with analytics tables and chart visualisations embedded — ready to adapt for a client briefing. Phase 8 will complete the portfolio review."

---

## Step 10: Completion Review

Open Completion Review after generating the full workflow.

**What to show:**
- Phase completion checklist — 8 phases, all ✅
- Output completion metrics and available/missing output lists
- Documentation checklist — present and missing files
- Portfolio value section
- Commercial value section
- Technical value section
- Responsible-use position (success box)
- Recommended final actions
- Download Completion Review Markdown button
- Download Portfolio Notes Markdown button

**Key talking point:**
> "The Completion Review gives a structured summary of what Build 6 has achieved — all 8 phases complete, the output status, the portfolio value, and downloadable portfolio notes. This is the final step before portfolio presentation."

---

## Step 11: Wrap-Up

Return to Home.

**Key talking points:**
- Phases 1–8 complete: synthetic policy data, governance framework, policy library, framework viewer, policy coverage checker, policy gap analysis, policy improvement recommendations, governance maturity summary, governance report builder, Export Centre with Markdown/PDF/charts, and Completion Review with portfolio notes
- 783 tests passing
- All phases are fully deterministic — no LLM, no external API, no embeddings
- The Export Centre generates a downloadable Markdown report and a professional PDF governance review report with analytics tables and chart visualisations
- The Completion Review page confirms build status and provides downloadable portfolio notes

---

## Safety Reminders During Demo

- All data shown is synthetic — BrightPath Skills Training is a fictional demo organisation
- No real client policies, learner data, safeguarding case information, or personal data is used
- This is a portfolio prototype, not a production compliance or legal system
- Human review is required before any real-world governance assessment

---

*Build 6 · AI Governance Policy Checker · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
