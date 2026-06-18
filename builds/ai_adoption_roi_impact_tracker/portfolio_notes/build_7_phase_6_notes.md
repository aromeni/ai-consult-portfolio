# Build 7 Phase 6 — Portfolio Notes

**AI Adoption ROI and Impact Tracker — Decision Tracker and Client Follow-up Evidence**

---

## 1. What Phase 6 Adds

Phase 6 adds a deterministic decision-tracking layer that converts the adoption evidence gathered in Phases 1–5 into clear consulting decisions and synthetic client follow-up evidence notes.

The layer provides:

- Decision outcome classification — Stop / Pause / Continue with controls / Scale / Scale with monitoring / Continue / Review later.
- Decision confidence classification — High / Moderate / Low confidence based on training completion, confidence after training, and pilot status.
- Decision reason generation — a short deterministic reason explaining why each decision was reached.
- Next action generation — one practical follow-up action per workflow, matched to the decision outcome.
- Organisation-level and build-level decision summaries — counts of each outcome grouped by organisation and by related build area.
- Prioritised follow-up decision list — all workflows ranked from Stop at the top to Scale at the bottom, with secondary sort by risk, near misses, and quality signals.
- Synthetic client follow-up evidence notes — one note per workflow explaining what the adoption evidence supports and what the follow-up step should be.

All outputs are deterministic and template-based. No external LLM or API is called.

---

## 2. Why Decision Tracking Matters

Phase 5 identifies where controls are needed and where adoption is safe. Phase 6 takes the next step: it converts that analysis into decisions. The distinction matters because a consultant's job is not just to identify risks but to make a clear recommendation about what should happen next.

Without decision tracking, an adoption review can produce findings without conclusions. A client may know that near misses have occurred, that quality checks are missing, or that training is incomplete — but without a structured decision on what to do about it, this evidence remains unactioned. Phase 6 closes that gap.

The prioritised follow-up list means a consultant arriving at a client review can immediately see which workflows need urgent attention and which can continue under standard monitoring. The evidence note gives a concise, evidence-grounded statement that can be shared in a client update meeting without requiring the full adoption report.

---

## 3. Why Adoption Evidence Must Lead to Action

The fundamental risk of adoption tracking is that evidence accumulates without being acted upon. A pilot may have run for three months, with quality issues logged, near misses recorded, and governance decisions noted — but if no clear decision has been made about whether to stop, continue, or scale, the evidence has not produced value.

Phase 6 makes decisions unavoidable. Every workflow in the synthetic portfolio receives a classified decision outcome. There is no ambiguous middle ground: each workflow is placed in a named decision category, given a reason, given a next action, and given a follow-up evidence note. This structure forces the consultant and client to move from observation to commitment.

In small organisations in particular, the absence of a structured decision process means that informal adoption can continue indefinitely, even when signals suggest it should be paused or reviewed. Phase 6 provides the structure to prevent this.

---

## 4. How Decisions Are Classified

Decision outcomes are assigned using a deterministic priority order:

1. **Stop** — the adoption_status is formally Stop. No further use is appropriate.
2. **Pause** — the pilot_status is Paused. Rollout is suspended pending further review.
3. **Continue with controls** — one or more of the following: a logged risk incident, more than one near miss, or three or more quality issues. Adoption may continue but requires stronger controls.
4. **Scale** — the adoption decision is Scale, training completion is at least 90%, confidence after training is at least 4.0, and there are no quality issues, incidents, or near misses.
5. **Scale with monitoring** — the adoption decision is Scale, training is at least 75%, confidence after is at least 3.5, and no incidents have been logged. Less demanding than Scale but still requires monitoring.
6. **Continue** — the adoption_status is Continue and no blocking signals are present.
7. **Review later** — all other cases. Typically a Scale decision that does not yet meet confidence or training thresholds, or a Review adoption status without a blocking signal.

Decision confidence is assessed separately using training completion, confidence after, and pilot status. High confidence requires all three to be above threshold. Low confidence results from weak training and confidence data, regardless of the decision outcome.

---

## 5. How This Connects to Build 1

Build 1 is the AI Readiness and Workflow Audit Tool. It assesses whether an organisation's AI readiness foundations are in place before adoption begins.

Phase 6 connects to Build 1 through the decision evidence for Build 1-related workflows — specifically workflows designed to review and improve readiness, such as the workflow readiness review and the appointment admin workflow audit. If these workflows receive a Continue or Scale with monitoring decision, it suggests that the readiness infrastructure is supporting adoption. If they receive a Pause or Continue with controls decision, it suggests that the readiness foundations themselves need attention before additional workflows are introduced.

---

## 6. How This Connects to Build 4

Build 4 is the AI Staff Training and Workshop Generator. It creates training materials to help staff use AI safely and confidently.

Phase 6 connects to Build 4 through decision confidence. Workflows with high decision confidence tend to be those where training completion and staff confidence are strong — which is precisely what Build 4 is designed to produce. A Build 4-related workflow that receives a Low confidence decision suggests that the training materials or delivery have not yet moved staff to the confidence level needed for adoption. This feedback closes the loop between training delivery and adoption readiness evidence.

---

## 7. How This Connects to Build 5

Build 5 is the AI Consulting Report Generator. It produces structured client-facing reports summarising audit findings and recommendations.

Phase 6 produces exactly the content that belongs in the follow-up evidence section of a Build 5 report. The decision outcomes, confidence levels, reasons, next actions, and follow-up evidence notes for each workflow translate directly into structured report findings. A consultant preparing a quarterly review report could pull the prioritised follow-up list from Phase 6 and use it as the basis for the recommendations section, without needing to re-derive decisions from raw adoption data.

---

## 8. How This Connects to Build 6

Build 6 is the AI Governance Policy Checker. It reviews whether governance policies cover the responsible-use controls required for AI adoption.

Phase 6 connects to Build 6 through the decision outcomes for governance-related workflows. Workflows linked to Build 6 — such as governance checklist reviews, incident log reviews, and acceptable use policy reviews — should, in principle, have the lowest risk signal density of any workflow group, because they are designed to strengthen governance. In the synthetic data, two of the three Build 6 workflows receive Stop or Pause decisions, which reflects the fact that governance process workflows are often among the most sensitive to pilot conditions. This is a realistic and useful signal: a governance workflow that itself requires a Stop or Pause decision is a strong indicator that the organisation's governance infrastructure has not yet been brought to a safe standard.

---

## 9. How a Consultant Could Use This with a Small Organisation

A consultant working with a small organisation could use Build 7 Phase 6 as follows:

1. **After the Phase 5 risk and quality review**, run the Phase 6 decision tracker to convert risk and quality evidence into named decisions for each workflow.
2. **Use the decision overview metrics** to give leadership a clear view of how many workflows are stopped, paused, continuing, or scaling across the portfolio.
3. **Use the organisation-level decision summary** to identify which organisations have the highest concentration of Stop or Pause decisions, and whether any organisation is ready to scale.
4. **Use the build-level summary** to identify whether governance-related workflows (Build 6) are creating disproportionate risk signals, and whether training-related workflows (Build 4) are producing the scale-ready outcomes they should.
5. **Use the prioritised follow-up list** to structure the client review conversation: Start with Stop and Pause decisions, address Continue with controls workflows next, and confirm Continue and Scale decisions last.
6. **Use the follow-up evidence notes** as a concise client-facing summary of what the evidence shows and what the next step should be, without requiring the client to read the full adoption data.

The key consulting discipline is to move from evidence to decision without introducing personal judgement that is not grounded in the adoption data. Phase 6 provides that structure: every decision is traceable to a specific signal in the adoption record, and every follow-up note reflects the decision outcome rather than a general assessment.

---

## 10. What Phase 7 Should Add Next

Phase 7 should add a Client Follow-up Report Builder. This would:

- Generate a structured, client-ready follow-up document for a selected organisation, summarising the decision outcomes, evidence, and next actions from Phase 6.
- Include a decision timeline showing when each stop, pause, continue, or scale decision was reached and what evidence supported it.
- Connect directly to Build 5 report generation, so that Phase 7 output can be incorporated into a formal consulting report without additional reformatting.
- Provide a checklist of outstanding follow-up actions drawn from the Phase 6 next action recommendations, organised by urgency and workflow.

Phase 7 would close the reporting loop: Phase 6 converts evidence into decisions, Phase 7 converts decisions into client-ready communication that demonstrates the consulting process and its governance rationale.

---

*Build 7 Phase 6 · AI Adoption ROI and Impact Tracker · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
