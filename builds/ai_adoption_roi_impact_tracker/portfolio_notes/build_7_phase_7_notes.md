# Build 7 Phase 7 — Portfolio Notes

**AI Adoption ROI and Impact Tracker — Client Follow-up Report Builder**

---

## 1. What Phase 7 Adds

Phase 7 adds a deterministic Markdown report builder that converts the adoption evidence produced in Phases 1–6 into a single structured consultant-facing document. The report is designed to be shared with a client as a follow-up to an AI pilot review meeting.

The builder provides:

- A complete portfolio-level report covering all synthetic workflows and organisations.
- Organisation-level reports filtered to a single client's workflows.
- An executive summary with workflow count, time-saving estimates, value equivalents, and decision outcome counts.
- An ROI and value summary section with total and average figures.
- A workflow impact section with impact status, primary bottleneck, efficiency gain, and weekly hours saved per workflow.
- A training readiness section with completion rates, confidence after, readiness bands, and adoption readiness per workflow.
- A risk and quality section with quality level, risk level, responsible adoption status, control need, and scaling permission.
- A decision and follow-up evidence section with decision outcomes, confidence levels, reasons, and next actions.
- A consolidated recommendations section drawing from all four analytical engines.
- A Markdown download button so the report can be distributed without any further formatting or export step.

All report content is deterministic and template-based. No external LLM or API is called.

---

## 2. Why Client Follow-up Reports Matter

The phases before Phase 7 produce structured evidence and decisions, but they do so inside the Streamlit application. A client cannot take a Streamlit dashboard into a governance meeting or board presentation. The follow-up report addresses this gap by converting the dashboard evidence into a document format that can be shared, stored, and referenced outside the tool.

In consulting practice, the ability to produce a follow-up document is often what distinguishes a credible AI adoption review from an informal check-in. A follow-up report demonstrates that the consultant has structured the evidence, reached a specific set of decisions, and proposed concrete next actions. It creates a formal record that the client can use to demonstrate responsible governance to their board, trustees, or regulators.

Phase 7 makes this step deterministic. The consultant does not need to write the report from scratch: the structure, the evidence, the decisions, and the recommendations are all generated automatically from the adoption data already collected in Phases 1–6.

---

## 3. How This Connects ROI, Workflow, Training, Risk, and Decisions

The Phase 7 report is the first place in Build 7 where all five analytical engines are brought together in a single output. Each section of the report draws from a different phase:

- The executive summary uses Phase 2 (ROI) and Phase 6 (Decision Tracker) to give a concise opening position.
- The ROI and value section uses Phase 2 portfolio-level figures.
- The workflow impact section uses Phase 3 (Workflow Impact and Bottleneck Analysis).
- The training readiness section uses Phase 4 (Training, Confidence, and Adoption Readiness Review).
- The risk and quality section uses Phase 5 (Risk, Quality, and Responsible Adoption Review).
- The decision and follow-up evidence section uses Phase 6 (Decision Tracker and Client Follow-up Evidence).
- The recommendations section consolidates recommendations from Phases 3, 4, 5, and 6.

This integration means that the consultant does not need to consult five separate sections of the dashboard to produce a coherent client update. The Phase 7 report does that synthesis automatically.

---

## 4. How This Connects to Build 1

Build 1 is the AI Readiness and Workflow Audit Tool. It identifies candidate workflows and assesses whether the organisation's readiness foundations are in place before adoption begins.

Phase 7 connects to Build 1 because the follow-up report is the natural document to produce after a Build 1-informed pilot has run for one or two adoption periods. The workflow impact section of the Phase 7 report will include the same workflows that Build 1 flagged as candidates — and the report will show whether those workflows have delivered the expected efficiency and confidence gains, or whether the readiness gaps Build 1 identified have materialised as quality issues, near misses, or governance concerns.

A consultant using both Build 1 and Build 7 together can present a client with a narrative that spans from the initial readiness audit to a structured follow-up review of how the pilot actually performed.

---

## 5. How This Connects to Build 4

Build 4 is the AI Staff Training and Workshop Generator. It creates training materials to help staff use AI tools safely.

Phase 7 connects to Build 4 through the training readiness section of the follow-up report. The training completion rates, confidence after figures, readiness bands, and support need classifications in the report directly reflect whether Build 4 training materials are producing measurable improvements in staff readiness. If multiple workflows show low confidence after training or a need for further support, the Phase 7 report provides an evidence base for revisiting the Build 4 training content or delivery.

---

## 6. How This Connects to Build 5

Build 5 is the AI Consulting Report Generator. It produces structured client-facing reports summarising audit findings and recommendations.

Phase 7 is closely related to Build 5, but it serves a different purpose. Build 5 produces a report at the beginning of an engagement — after the audit, during the governance and readiness assessment phase. Phase 7 produces a report at the follow-up stage — after a pilot has run, adoption data has been collected, and decisions have been reached. The two reports are complementary: Build 5 documents the consulting entry point, and Phase 7 documents what happened after the advice was followed.

A consultant could combine a Build 5 report with a Phase 7 follow-up report to give a client a complete picture of the engagement from first audit to post-pilot review.

---

## 7. How This Connects to Build 6

Build 6 is the AI Governance Policy Checker. It reviews whether governance policies cover the responsible-use controls required for AI adoption.

Phase 7 connects to Build 6 through the risk and quality section and the decision section of the follow-up report. If Build 6-related workflows appear in the report with high risk concern, governance review status, or Stop or Pause decisions, this is an important governance signal that belongs in the client-facing record. The Phase 7 report makes this visible in a way that can be shared with governance leads or trustees who may not have access to the full Build 7 dashboard.

---

## 8. How a Consultant Could Use This with a Small Organisation

A consultant working with a small organisation could use Build 7 Phase 7 as follows:

1. **After completing Phase 6**, select the client's organisation from the report scope selector in Phase 7.
2. **Review the generated report preview** to confirm that the evidence, decisions, and recommendations are an accurate reflection of the adoption data collected during the pilot.
3. **Download the Markdown report** and share it with the client in advance of a follow-up review meeting.
4. **Use the report as the agenda for the meeting** — working through each section: executive summary, ROI, workflow impact, training readiness, risk and quality, decisions, and recommendations.
5. **Use the recommendations section** to open a structured conversation about which actions the client will take in the next pilot period.
6. **Store the report** as part of the client's governance record, demonstrating that a structured evidence-based review was conducted after the AI pilot.

The key consulting value of Phase 7 is that it removes the friction between analysis and communication. The consultant does not need to translate dashboard findings into a document: the translation is done automatically, and the consultant can focus on the conversation rather than the formatting.

---

## 9. What Phase 8 Should Add Next

Phase 8 should add an Export Centre, a Completion Review, and a Final Sweep of the Build 7 portfolio. This would include:

- A structured export centre allowing download of individual sections as separate files, or the full report as a single document.
- A completion review checklist confirming that all eight phases of Build 7 have been implemented, tested, and documented correctly.
- A final sweep reviewing the consistency of terminology, British English usage, synthetic data labelling, and responsible-use disclaimers across all phases.
- A portfolio summary page bringing together headline figures from all phases into a single overview view.
- A CLAUDE.md or project notes file summarising the Build 7 architecture for future reference.

Phase 8 would close Build 7 as a complete, portfolio-ready demonstration of an AI adoption tracking and reporting system built without real client data, external APIs, or cloud deployment.

---

*Build 7 Phase 7 · AI Adoption ROI and Impact Tracker · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
