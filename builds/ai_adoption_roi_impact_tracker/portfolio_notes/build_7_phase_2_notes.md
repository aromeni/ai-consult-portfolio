# Build 7 Phase 2 — Portfolio Notes

**AI Adoption ROI and Impact Tracker — ROI Summary Engine**

---

## 1. What Phase 2 Adds

Phase 2 adds a deterministic ROI summary engine to the Build 7 adoption tracker. It converts the synthetic workflow-level adoption metrics from Phase 1 into practical consulting indicators that a consultant could use in a follow-up conversation with a small organisation.

The engine calculates:

- Minutes saved per task and weekly minutes saved (reused from Phase 1).
- Weekly, monthly, and annual hours saved.
- Efficiency gain percentage against the baseline task time.
- Synthetic value-equivalent estimates (weekly, monthly, annual) based on staff group assumptions.
- Time-saving bands (Low / Moderate / High / Very high).
- Confidence improvement bands (No improvement / Small / Moderate / Strong).
- Adoption value indicators (Strong value / Clear value / Emerging value / Low value / Needs review).
- Organisation-level ROI summaries grouping all workflows for each client.
- Portfolio-level ROI summary across all organisations and workflows.

All calculations are deterministic and template-based. No external LLM or API is called.

---

## 2. Why ROI Summaries Matter in AI Adoption Consulting

When a small organisation completes an AI pilot, they typically ask: was it worth it? In most cases, they do not have the infrastructure to measure this rigorously. They need a consultant to help them convert rough operational observations into a structured position they can share with leadership, trustees, or funders.

ROI summaries give that position. They translate "we saved some time" into "we estimate 156 hours per year across lesson plan drafting, at a synthetic value equivalent of approximately £4,368 annually" — framed explicitly as a directional estimate, not an audited figure.

This matters because:

- It makes adoption visible and decisions easier to justify.
- It creates a baseline for the next review conversation.
- It identifies which workflows are creating value and which need more support.
- It helps prioritise where to invest limited consulting or training time.

---

## 3. Why Time Saved Is Not Enough on Its Own

Time saving is an important signal, but it can mislead if taken in isolation. A workflow that saves 5 hours per week but generates 3 risk incidents is not a success. A workflow that saves very little time but dramatically improves staff confidence in safe AI use may be exactly what a cautious organisation needs.

Phase 2 deliberately combines time saving with other signals:

- **Confidence change** — are staff more confident using AI safely?
- **Training completion rate** — has the adoption been supported by training?
- **Quality issues logged** — are there signs of output quality problems?
- **Risk incidents and near misses** — are boundaries being maintained?

This multi-signal approach produces a more honest adoption value indicator than time saving alone.

---

## 4. Why Confidence, Training Completion, Risk Incidents, and Quality Issues Are Included

These four signals come directly from the Phase 1 adoption metric records. They were chosen because they reflect the dimensions a responsible consultant would want to review before recommending that a pilot be continued, scaled, or stopped.

- **Confidence** measures whether AI adoption is building capability or just creating dependency on a tool people do not understand.
- **Training completion** signals whether the governance infrastructure is in place. Low completion rates with high time saving is a warning sign.
- **Risk incidents** are a hard gate. Any logged incident should trigger review regardless of other signals.
- **Quality issues** are a softer signal. A few quality issues during a pilot are normal. Many quality issues suggest the workflow is not yet stable enough to scale.

Together, these signals form the basis of the adoption value indicator — a single summary position that a consultant can discuss with a client in plain language.

---

## 5. How This Connects to Build 1

Build 1 is the AI Readiness and Workflow Audit Tool. It identifies which workflows in a small organisation are candidates for AI support, what barriers exist, and what governance controls are needed before starting.

Build 7 Phase 2 picks up where Build 1 leaves off. The workflows tracked in Phase 2 are exactly the kind of workflows that Build 1 would have surfaced. The ROI summary gives a consultant the evidence to answer: did the workflows Build 1 recommended actually produce measurable value in practice?

---

## 6. How This Connects to Build 4

Build 4 is the AI Staff Training and Workshop Generator. It creates training materials to help staff use AI safely and confidently.

Build 7 Phase 2 tracks two direct outputs of Build 4 activity: confidence change (before vs. after training) and training completion rate. Workflows supported by strong Build 4 training show higher confidence improvement bands. Workflows with low training completion rates show weaker adoption value indicators.

This connection demonstrates how training investment translates into adoption quality — a consulting insight that is hard to show without a measurement tool like Build 7.

---

## 7. How This Connects to Build 5

Build 5 is the AI Consulting Report Generator. It produces structured client-facing reports summarising audit findings and recommendations.

Build 7 Phase 2 produces organisation-level and portfolio-level ROI summaries that could feed directly into a Build 5 consulting report. The estimated value equivalents, adoption value indicators, and needs-review flags are exactly the kind of evidence a consulting report needs to justify continued investment or a decision to scale.

---

## 8. How This Connects to Build 6

Build 6 is the AI Governance Policy Checker. It reviews whether an organisation's existing policies cover responsible AI governance.

Build 7 Phase 2 tracks the adoption quality of governance-related workflows — such as governance checklist reviews and policy boundary training — including risk incidents and near misses. Workflows that were paused or stopped due to unclear governance boundaries appear clearly in the adoption value indicator as "Needs review."

This demonstrates the feedback loop between governance policy (Build 6) and live adoption evidence (Build 7): good governance foundations correlate with stronger adoption value indicators.

---

## 9. How a Consultant Could Use This with a Small Organisation

A consultant working with a small organisation could use Build 7 Phase 2 as follows:

1. **After the pilot period** (typically 4–8 weeks), collect workflow-level adoption data: time before and after, confidence scores, training completion, incidents, quality issues.
2. **Run the ROI summary engine** to produce weekly, monthly, and annual time-saving estimates and value-equivalent figures.
3. **Share the portfolio-level summary** with the client's leadership team — framing it explicitly as synthetic directional evidence, not audited financial return.
4. **Use adoption value indicators** to identify which workflows to continue, which to scale, and which to pause for review.
5. **Flag "Needs review" workflows** for immediate follow-up — these have incidents or stop/review decisions and should not be left without a clear next action.
6. **Feed the summary into a consulting report** (Build 5) to create a structured follow-up document the client can share with trustees, funders, or senior staff.

The key consulting discipline here is to be honest about what the figures represent: directional evidence from a structured estimate, not a business case with audited financial data.

---

## 10. What Should Come Next in Phase 3

Phase 3 should add workflow impact and bottleneck analysis. This would:

- Identify which workflow steps are taking the most time before and after AI support.
- Surface patterns across multiple workflows — for example, whether AI support consistently reduces drafting time but not review time.
- Compare workflows across organisations to identify cross-sector patterns.
- Generate a structured workflow impact report that a consultant could include in a follow-up presentation.

Phase 3 would build directly on the Phase 2 ROI summaries, adding a layer of structured diagnostic insight to complement the high-level value indicators.

---

*Build 7 Phase 2 · AI Adoption ROI and Impact Tracker · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
