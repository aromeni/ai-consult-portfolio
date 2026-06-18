# Demo Script — Phase 1

**AI Consulting Report Generator · Build 5 · BrightPath ChatGPT Mastery Project**

---

## Purpose

This script walks through Phases 1–8. Pages covered: Home, Audit Data, Readiness Summary, Risk Register, Opportunity and Pilot Recommendations, Roadmap, Report Sections, Client Report, and Export Centre (PDF, PPTX, and analytics charts).

**Demo time:** 30–40 minutes for a full Phases 1–8 walkthrough (25–30 minutes for Phases 1–7 only).

**Demo scenario:** BrightPath Skills Training — a fictional small UK training provider with 24 staff using ChatGPT informally without a policy.

---

## Setup

```bash
cd 10-builds/ai-consulting-report-generator
streamlit run app.py
```

Opens at `http://localhost:8501`.

---

## Step 1 — Home Page

Point out:

- **Project title and one-line summary**
- **Consulting workflow diagram**: seven steps from Audit Data to Export
- **Connection to Builds 1–4**: how this closes the consulting loop
  - Build 1 audited readiness → identified risks and workflows
  - Build 2 extracted policy evidence → grounds governance analysis
  - Build 3 answered policy questions semantically → grounds recommendations
  - Build 4 generated training materials → linked from training needs section
- **Responsible-use warning**: synthetic data only, human review required
- **Prototype status notice**: production-style prototype, not a compliance system

Key talking point:

> "This is the final step in the consulting workflow. After the readiness audit, the policy
> analysis, and the training pack, the consultant needs to hand the client a professional
> report. This prototype automates that report assembly from structured audit data."

---

## Step 2 — Audit Data Page

Navigate to **Audit Data**.

Click **Load BrightPath Demo Audit Data**.

Point out the **metric cards**:

- Staff: 24
- Workflows: 4
- Risks: 5
- Critical Risks: 1
- Pilots: 3
- Training Needs: 6
- Governance Gaps: 5

Point out the **readiness scores**:

- Strategy: 32/100 (Low)
- Data Governance: 28/100 (Low)
- Staff Capability: 45/100 (Developing)
- Workflow Opportunity: 68/100 (Moderate)
- Risk Management: 25/100 (Low)
- Leadership Alignment: 52/100 (Developing)
- Overall: 42/100 — Developing readiness

Key talking point:

> "The Workflow Opportunity score is the strongest — this organisation has real AI opportunity
> but weak governance to support it safely. That gap is exactly what the consulting report
> needs to address. The risk management score at 25 is the biggest concern."

Expand one **Workflow Finding** (e.g. Course Material Development):

> "The workflow analysis shows where AI can save time — but each finding also comes with
> a risk level and a recommended action. The report will turn these into prioritised
> recommendations."

Expand one **Risk Finding** (e.g. Learner Data in Unapproved AI Tools):

> "This is Critical. Staff are already using AI without a policy, which creates an
> immediate GDPR risk. The report will highlight this as an immediate action item."

Expand one **Pilot Recommendation** (e.g. AI-Assisted Lesson Plan Drafts):

> "Each pilot has a proposed solution, expected benefits, and measurable success criteria.
> These become the opportunity section of the client report."

Point out the **Governance Gaps**:

> "No AI Use Policy and no Approved Tools List — both Critical. These are the first two
> recommended actions in the report."

Click **View Audit Data as Markdown** and show the structured output:

> "This becomes Section 1 of the client report in Phase 3."

---

## Step 3 — Readiness Summary (Phase 2)

Navigate to **Readiness Summary**.

Point out the **metric cards**:

- Overall Score: 42/100
- Readiness Level: Developing readiness
- Strongest Area: Workflow opportunity (68/100)
- Weakest Area: Risk management (25/100)
- Priority Gaps: 5

Point out the **overall readiness band** (amber left border, developing readiness description).

Point out the **category scores with progress bars**:

- Show that Workflow opportunity (68) stands out visually as the longest bar
- Show that Risk management (25) and Data governance (28) are the shortest
- Expand one interpretation, e.g. Data governance:

> "Data governance appears to be a key constraint. The organisation should clarify
> what data can and cannot be used with AI tools, define approval routes, and avoid
> using sensitive or personal data in uncontrolled systems."

Point out **Priority Gaps** — expand Risk management:

> "Risk: Inadequate risk controls could lead to misuse, harm, or compliance breaches.
> Recommended action: Complete a risk register, assign owners, and define acceptable-use
> and incident-reporting processes."

Point out the **Strategic Interpretation**:

> "BrightPath Skills Training shows developing AI readiness. Some foundations are in
> place, but governance, staff guidance, and risk controls need strengthening before
> structured AI pilots begin. Workflow opportunity is a relative strength that can
> support early pilots. Risk management is the most significant gap."

Point out the **Recommendations** — highlight item 1 (data governance) and item 5 (staff training).

Click **Download Readiness Summary (Markdown)** and show the file structure.

Key talking point:

> "This is a client-ready one-pager. They can see exactly where they stand, what their
> strongest area is, what the biggest gaps are, and what to do about each one. The
> strategic interpretation paragraph is exactly what you'd say in the room — and now
> it's in the document too."

---

## Step 4 — Risk Register (Phase 3)

Navigate to **Risk Register**.

Point out the **summary metric cards**:

- Total Risks: 5
- Critical: 0
- High: 4
- Medium: 1
- Low: 0

Point out the **warning banner**:

> "4 high-priority risks should be addressed before scaling AI adoption or running wider pilots."

Point out the **Highest Risk** card:

> "RISK-001 — Learner Data in Unapproved AI Tools. Level: High, Score: 16/25. Likelihood: High, Impact: High."

Point out the **Overall Risk Position**:

> "The organisation should address priority AI governance, data, safeguarding, and human-review controls before scaling AI use."

Point out the **Recommended Focus Areas**:

- "Resolve 4 high risk(s) before scaling AI pilots."
- "Establish data protection controls and an approved AI use policy."
- "Brief all staff on safeguarding and AI boundaries."

Expand one **Risk Register card**, e.g. RISK-001 — Learner Data in Unapproved AI Tools:

> "Category: Data Protection. Likelihood: High (4/5). Impact: High (4/5). Score: 16/25. Risk level: High."

> "Recommended control: Define what data can and cannot be used with AI tools. Require only approved systems. Minimise data entry, remove identifiers where possible, and escalate any uncertainty to the data protection lead."

> "Owner: Quality and Compliance Lead. Priority action: Address before scaling AI adoption or running wider pilots. Review: Monthly."

Expand RISK-004 — Safeguarding Decisions Delegated to AI:

> "Likelihood: Low (2/5). Impact: Critical → treated as 5/5. Score: 10/25. Level: High."

> "Even a low likelihood of AI being used for safeguarding decisions is a high risk due to impact. The control is explicit prohibition in the AI policy."

Point out the **responsible-use warning** at the bottom of the page.

Click **Download Risk Register (Markdown)** and show the full document structure.

Key talking point:

> "This gives the client a complete AI risk picture: every risk scored, prioritised, assigned, and with a specific recommended control. The highest risk is data protection — learner data entering uncontrolled AI tools. The safeguarding risk has a low likelihood but such high impact that it still scores High. The download is a client-ready risk register they can take into governance conversations."

---

## Step 5 — Opportunity and Pilot Recommendations (Phase 4)

Navigate to **Opportunity and Pilot Recommendations**.

Point out the **summary metric cards**:

- AI Opportunities: 4
- Pilots: 3
- Strategic / High: 0
- Recommended First Pilot: AI-Assisted Lesson Plan Drafts

Point out the **Overall Opportunity Position**:

> "The organisation should start with one or two narrow pilots in low-risk workflows before wider adoption."

Point out the **Recommended Focus Areas**:

- "Plan 4 medium-priority opportunities for structured pilots."
- "Start with a controlled pilot: AI-Assisted Lesson Plan Drafts and Email Response Templates."
- "Establish responsible-use controls and success measures before any pilot begins."

Point out the **Recommended First Pilot** card:

> "PILOT-001 — AI-Assisted Lesson Plan Drafts. Medium priority. Complexity: Low. Risk: Low. Timeline: Month 1–2."

Point out the **Recommended Pilot Sequence** — three visual cards showing the order:

> "The safest pilot — lesson plan drafts — goes first. Email templates second. Quality reporting templates third, which has slightly higher complexity."

Expand one **AI Opportunity card**, e.g. OPP-001 — Course Material Development:

> "Value: High (4/5). Complexity: Medium (3/5). Risk: Medium (3/5). Score: 12/20. Priority: Medium."

> "AI opportunity: AI-assisted first-draft generation for lesson plans and handouts using approved synthetic templates, followed by tutor review and customisation."

> "Recommended action: [existing recommended_action from audit data]."

Open **Success measures** — show the 5 measures including time tracking and quality review.

Open **Responsible-use controls** — show the standard 8 controls.

Expand one **Pilot card**, e.g. PILOT-001 — AI-Assisted Lesson Plan Drafts:

> "Business problem: Tutors spend 8–12 hours creating course units from scratch."

> "Expected benefits: Reduce drafting time by 40–60%. Improve consistency. Build a curriculum template library."

Open **Success measures** — show existing measures plus generated extras (incident tracking, whether to continue or stop).

Open **Human review requirements**:

> "All AI-generated outputs must be reviewed and approved by a named reviewer before use."

Point out the **responsible-use warning** at the bottom of the page.

Click **Download Opportunity Portfolio (Markdown)** and show the full document structure.

Key talking point:

> "This gives the client a complete picture of where AI can add value, which pilot to start with, in what order to run the pilots, what success looks like, and exactly what safeguards to put in place before they start. The recommended first pilot is lesson plan drafts — Low complexity, Low risk, real time savings. That's the easiest win to build confidence and demonstrate responsible use before moving to higher-complexity workflows."

---

## Step 6 — Roadmap (Phase 5)

Navigate to **Roadmap**.

Point out the **summary metric cards**:

- Organisation: BrightPath Skills Training
- Total Actions: 24
- High Priority: 15+ actions
- Phases: 3
- Recommended First Pilot: AI-Assisted Lesson Plan Drafts

Point out the **Overall Roadmap Position**:

> "The roadmap should prioritise governance, data boundaries, safeguarding escalation, and human-review controls before wider AI scaling."

Point out the **Recommended First Pilot** highlight card:

> "AI-Assisted Lesson Plan Drafts — Complexity: Low, Risk: Low, Timeline: Month 1–2."

Point out the **First 30 Days — Foundation and Risk Control** section:

> "10 actions covering governance owners, data boundaries, safeguarding routes, acceptable-use guidance, pilot selection, staff training plan, and success measures. BrightPath gets two extra adaptive actions: draft AI use policy (critical governance gap) and address top priority risks (4 high risks)."

Expand one action, e.g. **DAY30-003 — Clarify data boundaries for all AI tools**:

> "Owner: Data Protection Lead / DPO. Priority: High. Success measure: Data boundary guidelines distributed and confirmed by all staff before any pilot begins. Risk reduction: Reduces GDPR, data protection, and learner privacy risk."

Point out the **Days 31–60 — Pilot Preparation and Controlled Delivery** section:

> "7 actions: deliver training, prepare pilot materials, brief participants, launch the pilot, require human review, track weekly data, and review incidents."

Point out the **Days 61–90 — Review, Refine, and Scale Decision** section:

> "7 actions: review evidence, make stop/continue/scale decision, update policy, strengthen controls, scope second pilot if positive, report to leadership, and address outstanding risk items."

Point out the **Cross-Cutting Controls** list:

> "10 always-on controls including approved tools only, no real data in AI tools, human review before use, escalation routes, use log, manager oversight, training before scaling, monthly review, no scaling before evidence, and stop the pilot if safeguarding concerns arise."

Point out the **Dependencies** and **Risks to Manage** sections.

Click **Download Implementation Roadmap (Markdown)** and show the full document structure.

Key talking point:

> "This gives the client a complete 90-day AI adoption plan — what to do in the first month to get governance in place, how to run the first pilot safely, and how to make an evidence-based decision at the end. It's not just a list of tasks — every action has an owner, a success measure, and a dependency. The safeguarding and data protection controls are built into every phase, not bolted on at the end."

---

## Step 7 — Report Sections (Phase 6)

Navigate to **Report Sections**.

Point out the **summary metric cards**:

- Organisation: BrightPath Skills Training
- Total Sections: 11
- Source Outputs Used: 5+ (all prior outputs available)
- Missing Source Outputs: 0
- Review Required: Yes

Point out the **Source Output Availability checklist**:

> "Five checkmarks — Audit Data, Readiness Summary, Risk Register, Opportunity Portfolio, Implementation Roadmap. All available because we generated them in earlier steps."

Point out the **Overall Report Readiness** statement:

> "The report sections are ready to be assembled into the full client report, subject to human review and responsible-owner approval."

Point out the **Report Sections list** — expand the **Executive Summary**:

> "BrightPath Skills Training is beginning to explore informal AI use across lesson planning, emails, and report drafting... The overall AI readiness score is 42/100 (Developing readiness)... The audit identified 5 AI risks, including 4 high-priority risks that should be addressed before scaling AI adoption... The recommended first pilot is AI-Assisted Lesson Plan Drafts."

Point out the **Key Points** and **Recommendations** inside the Executive Summary expander.

Expand the **AI Readiness Interpretation**:

> "Shows the full category score breakdown — Workflow opportunity 68/100, Risk management 25/100 — with the strategic interpretation paragraph."

Expand the **Risk Summary**:

> "5 risks: 0 critical, 4 high, 1 medium. Top 3 risks listed with recommended controls."

Expand the **Opportunity and Pilot Summary**:

> "4 opportunities, 3 pilots. Recommended first pilot: AI-Assisted Lesson Plan Drafts. Pilot sequence: Lesson Plans → Email Templates → Quality Reports."

Expand the **30/60/90-Day Roadmap Summary**:

> "24 actions across three phases — 10 in Day 30, 7 in Day 60, 7 in Day 90. 15 high-priority actions. Key dependencies and risks listed."

Expand the **Training and Capability Needs**:

> "6 training topics. Connect to Build 4: 'Training recommendations can later be turned into workshop materials using Build 4: AI Staff Training and Workshop Generator.'"

Expand the **Governance Recommendations**:

> "5 governance gaps from the audit + 10 standard recommendations including policy, data boundaries, safeguarding routes, approved tools, human review."

Expand the **Immediate Next Steps**:

> "8 practical actions from confirming governance owners through to reviewing pilot outcomes. The first pilot name is woven into step 7."

Expand the **Responsible-Use Boundaries**:

> "Full responsible-use text: synthetic data only, no legal/safeguarding/HR advice, human review required, not an organisational policy or compliance judgement."

Point out the **responsible-use warning** at the bottom of the page.

Click **Download Report Sections (Markdown)** and show the full document structure:

> "`# AI Consulting Report Sections` → Report Overview → Source Outputs Used → all 11 sections in order with purpose, content, key points, recommendations, and review note."

Key talking point:

> "This gives the consultant a complete set of client-facing report sections in a single click — after five minutes of generating analysis outputs. Every section has a key points list, a recommendations list, and a review note. The sections are ready to paste into a final client document, or to feed into the Client Report Builder in the next phase. The responsible-use boundaries are always the last section — not an afterthought, but a structural part of every deliverable."

---

## Step 8 — Client Report (Phase 7)

Navigate to **Client Report**.

Point out the **Report Readiness Checklist**:

> "Eight source outputs are checked — Readiness Summary, Risk Register, Risk Register Summary, Opportunity Portfolio, Opportunity Summary, Implementation Roadmap, Roadmap Summary, and Report Sections. All checkmarks are green because we generated them in the earlier steps."

Point out the **recommended next steps** if any source outputs are missing.

Point out the **Section Selection controls**:

> "The consultant can choose exactly which sections to include — executive summary and organisation context are always included, but the client can request a shorter report by deselecting optional sections."

Leave all recommended sections selected.

Point out the **Summary Metric Cards**:

- Organisation: BrightPath Skills Training
- Sections Included: 13
- Missing Recommended: 0
- Risks Included: 5
- Pilots Included: 3

Point out the **Report Readiness** statement:

> "The client report is ready for export, subject to human review and responsible-owner approval."

Expand the **View Full Client Report (Markdown)** preview:

> "Scroll through: Cover Page → Table of Contents → Executive Summary → Organisation Context → AI Readiness Summary → Key Findings → Risk Register Summary → Opportunity and Pilot Recommendations → 30/60/90-Day Implementation Roadmap → Training and Capability Needs → Governance Recommendations → Immediate Next Steps → Responsible-Use Boundaries → Prototype Limitations → Appendices."

Point out the **Executive Summary** section in the preview:

> "The executive summary draws from the Report Sections we generated in Step 7 — it has the key points and recommendations baked in."

Point out the **Responsible-Use Boundaries** section in the preview:

> "This is always the last active section before Prototype Limitations. Responsible-use is structural, not an afterthought — it appears in every single deliverable."

Point out the **Appendices**:

> "The appendices include the audit data summary, category score table, risk register table, pilot sequence table, roadmap action summary, and source outputs availability. Everything a client or reviewer needs to verify the report's basis."

Click **Download Client Report (Markdown)** and show the complete document:

> "One file, one click, after five minutes of generating analysis. This is a complete first-draft client report — 13 sections covering readiness, risks, opportunities, roadmap, governance, and responsible-use, all assembled from the synthetic audit data."

Key talking point:

> "This closes the consulting loop. Build 1 ran the audit. Build 2 extracted policy evidence. Build 3 answered policy questions. Build 4 generated training materials. Build 5 now turns all of that into a complete client report. The consultant's job is to review, refine, and present — not to spend hours formatting."

---

## Step 9 — Export Centre (Phase 8)

Navigate to **Export Centre**.

The Export Centre is now fully functional. **Note:** The Export Centre requires `audit_data` and `client_report_markdown` in session state — run steps 1–8 in order before demoing this page.

Point out the **Export Readiness Checklist**:

> "Nine quality checks — executive summary included, responsible-use section present, prototype limitations noted, all source outputs available, organisation name set, generation date set. All checks should be green after a full session."

Point out the **Analytics Summary cards**:

- Completion Status: 7 outputs tracked
- Readiness Scores: 6 categories + Overall
- Risk Levels: Critical / High / Medium / Low counts
- Opportunity Priorities: Strategic / High / Medium / Low
- Roadmap Actions: across 3 phases
- Report Quality: 8 boolean quality checks

Point out the **Chart Previews** (3-column grid):

> "Five matplotlib charts generated from the session data — Completion Status, Readiness Scores, Risk Levels, Opportunity Priorities, and Roadmap Actions. All charts are generated locally from the synthetic audit data — no external services involved."

Point out the **three download buttons**:

- **Download Markdown** — complete client report `.md` file (same as Client Report page download)
- **Download PDF** — professional PDF with cover page, analytics section, charts, styled report sections, and responsible-use boundaries
- **Download PowerPoint** — 15-slide PPTX executive deck with navy theme, chart slides, and an amber Responsible-Use Boundaries slide

Click **Download PDF** and show the structure:

> "Cover page with navy header and white BrightPath title. Analytics page. Five chart pages. Full report sections in styled reportlab paragraphs. Responsible-use section. Prototype limitations. One click from the assembled report to a complete client-ready PDF."

Click **Download PowerPoint** and open the PPTX:

> "Slide 1 — title slide with navy background. Slides 2–3 — organisation context and readiness summary. Slide 4 — readiness score chart. Slides 5–7 — key findings, risk summary, risk chart. Slides 8–9 — opportunities, opportunity chart. Slides 10–11 — roadmap, roadmap chart. Slides 12–13 — governance and immediate next steps. Slide 14 — Responsible-Use Boundaries with amber title bar. Slide 15 — recommended direction. This is the deck the consultant hands the client at the end of the engagement."

Key talking point:

> "Phase 8 closes the full loop. The consultant runs the AI Consulting Report Generator for a 90-minute session, generates the readiness summary, risk register, opportunity portfolio, roadmap, report sections, and client report — and then exports a PDF and a PowerPoint deck in one click. No formatting, no copy-paste, no manual chart building. The human's job is to review, refine, and present."

Point out the **responsible-use warning** at the bottom of the page:

> "All outputs are generated from synthetic demo audit data only. No real client, learner, or personal data is used. Human review is required before any output is presented to a real client."

---

## Step 10 — Completion Review (Phase 9)

Navigate to **Completion Review** after generating the full workflow.

Point out the **completion score metrics**:

- Overall status
- Phase completion percentage
- Output completion percentage
- Documentation completion percentage
- Final readiness label

Point out the **Phase Completion Checklist**:

> "All nine phases are listed here with purpose and evidence. This turns the build from a set of features into a clear portfolio story."

Point out the **Output Completion Status**:

> "The page checks the Streamlit session state and shows which generated outputs exist right now. If a reviewer opens this page too early, it does not crash — it tells them what to generate next."

Point out the **Documentation Checklist**:

> "The build checks for the README, architecture notes, safety boundaries, demo script, screenshot checklist, completion review, portfolio notes, testing checklist, and case study summary."

Point out the **portfolio, commercial, and technical value cards**:

> "This section explains why the build matters: it demonstrates an end-to-end consulting workflow, export automation, responsible-use design, and practical Python/Streamlit engineering."

Point out the **Responsible-Use Position**:

> "The boundary is still explicit at the end: synthetic data only, no learner or safeguarding data, no HR or personal data, no regulated information, no professional advice, and human review required."

Download the **Completion Review** and **Portfolio Notes** Markdown files:

> "These are the handoff artefacts for portfolio review: what was built, why it matters, how to demo it, what the BrightPath case study shows, and what still requires manual review."

Key talking point:

> "Phase 9 closes Build 5. It does not add a major product feature — it makes the build reviewable, explainable, safe to demo, and ready for screenshots."

---

## Responsible-Use Points to Cover

- All scenarios are synthetic — no real learner, client, HR, or personal data
- No external AI API calls — all generation is deterministic
- All outputs require human review before client delivery
- This is a prototype, not a certified consulting or compliance system
- Production use would require DPIA, governance, security, and responsible-owner approval

---

*Build 5 · AI Consulting Report Generator · BrightPath ChatGPT Mastery Project*
*All scenarios are synthetic. Outputs require human review before real-world use.*
