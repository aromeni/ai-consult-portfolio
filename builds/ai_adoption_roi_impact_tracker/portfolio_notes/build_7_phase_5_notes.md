# Build 7 Phase 5 — Portfolio Notes

**AI Adoption ROI and Impact Tracker — Risk, Quality, and Responsible Adoption Review**

---

## 1. What Phase 5 Adds

Phase 5 adds a deterministic risk and quality review engine to the Build 7 adoption tracker. It checks whether AI-supported workflows are safe enough to continue, pause, or scale, based on evidence from quality issues, risk incidents, near misses, governance review decisions, and staff readiness signals.

The engine provides:

- Quality concern classification — Low / Moderate / High concern bands based on the number of quality issues logged during the pilot.
- Risk concern classification — Low / Moderate / High concern bands based on logged risk incidents and near misses.
- Responsible adoption status — Pause adoption / Requires governance review / Continue with controls / Responsible to continue / Responsible to scale.
- Control need identification — Governance review / Quality assurance checklist / Incident logging review / Training reinforcement / Standard monitoring.
- Scaling permission — Pause or stop / Do not scale yet / Scale with controls / Scale permitted.
- Organisation-level risk and quality summaries — counts of concerns, governance review needs, and scaling permissions per organisation.
- Related-build risk and quality summaries — groups the same counts by Build 1, Build 4, Build 5, and Build 6.
- Prioritised risk and quality action list — ranks all workflows from most urgent (Pause adoption) to least urgent (Responsible to scale).
- Deterministic consultant recommendations — one practical recommendation per workflow based on the primary control need.

All classifications are deterministic and template-based. No external LLM or API is called.

---

## 2. Why Responsible Adoption Matters

The concept of responsible AI adoption is distinct from effective AI adoption. A workflow can save time, improve output speed, and increase staff confidence while still being conducted irresponsibly — if quality outputs are not being reviewed, if incidents are not being logged, or if the boundaries of safe AI use are unclear to the staff doing the work.

In small organisations, the risks of irresponsible adoption are amplified by limited governance infrastructure. There is often no dedicated AI risk lead, no formal incident logging process, and no systematic quality checking of AI-generated outputs. This means that quality problems or safety concerns can accumulate quietly before they become visible.

Phase 5 makes these risks measurable. It converts quality issues, near misses, and risk incidents into structured evidence that a consultant can use to have a clear, specific conversation with a client about where adoption is safe, where controls are needed, and where a pause or governance review is appropriate.

---

## 3. Why Time Saved Is Not Enough

Phases 2 and 3 focused on whether AI adoption is producing measurable operational value. Phase 4 checked whether staff are confident and trained enough to sustain that adoption. Phase 5 asks a different and necessary question: even if time savings are real and staff are confident, is the adoption itself being conducted responsibly?

A workflow that saves three hours per week but produces frequent quality issues is not a successful adoption — it is a risk. A workflow where near misses are regularly occurring but not being escalated is creating unreported safety exposure. A governance review workflow where staff have not received training on escalation wording may produce documentation that gives false assurance.

Time saved is the most visible signal of AI adoption value, but it is not a sufficient measure of adoption quality. Phase 5 closes this gap by reviewing the conditions under which adoption is happening, not just the outcomes it is producing.

---

## 4. How Quality and Risk Are Reviewed

Quality concerns are classified in three bands:

- **Low quality concern** — fewer than three quality issues logged. Adoption may proceed under standard monitoring.
- **Moderate quality concern** — three or four quality issues logged. Quality checking controls and sample-review routines should be added before wider rollout.
- **High quality concern** — five or more quality issues logged. This level of quality signal suggests the workflow is not yet reliable enough for wider use without significant review intervention.

Risk concerns are classified separately:

- **Low risk concern** — no incidents logged and fewer than two near misses. Risk exposure is within a manageable range.
- **Moderate risk concern** — two or more near misses but no logged incidents. The pattern suggests that staff are approaching the boundary of safe use but have not yet caused a recordable incident.
- **High risk concern** — one or more logged risk incidents. Any logged incident indicates a breakdown in safe adoption that requires a formal governance review.

The two classifications — quality and risk — are kept separate because they represent different types of concern. Quality problems tend to be operational; risk incidents tend to have governance and accountability implications.

---

## 5. How Scaling Permission Is Assigned

Scaling permission represents the consultant's view of whether a workflow is ready to be extended to more staff, more sites, or more use cases.

- **Pause or stop** — the workflow has been formally stopped or paused. No further expansion is appropriate.
- **Do not scale yet** — one or more blocking signals are present: a logged risk incident, more than two near misses, training completion below 75%, or confidence after training below 3.5 on a 5-point scale.
- **Scale with controls** — no blocking signals, but there are some quality issues or a small number of near misses. Scaling may proceed with additional quality assurance or incident logging controls in place.
- **Scale permitted** — no quality issues, no risk incidents, no near misses, and staff are sufficiently trained and confident. Scaling may proceed under continued monitoring.

The thresholds are designed to be practically useful rather than technically precise. They reflect common-sense consulting judgements: any logged incident is serious enough to pause scaling; low training or confidence is a meaningful signal that staff are not yet ready for wider deployment.

---

## 6. How This Connects to Build 1

Build 1 is the AI Readiness and Workflow Audit Tool. It identifies candidate workflows and assesses whether the organisation's readiness foundations are in place before adoption begins.

Phase 5 provides the follow-up evidence. If Build 1 flagged a particular workflow as having weak governance controls or unclear escalation procedures, Phase 5 shows whether those concerns materialised as near misses, quality issues, or formal governance review decisions during the pilot. This closes the loop between pre-adoption risk assessment and post-pilot risk evidence.

---

## 7. How This Connects to Build 4

Build 4 is the AI Staff Training and Workshop Generator. It creates practical training materials to help staff use AI tools safely.

Phase 5 connects to Build 4 through the training reinforcement control need. When a workflow has low training completion or weak staff confidence, Phase 5 identifies training reinforcement as the primary control — not additional governance checks. This means the Phase 5 recommendation points the consultant back to a Build 4 intervention as the appropriate next step.

---

## 8. How This Connects to Build 5

Build 5 is the AI Consulting Report Generator. It produces structured client-facing reports summarising audit findings and recommendations.

Phase 5 produces exactly the kind of responsible adoption evidence that belongs in the risk and governance section of a Build 5 consulting report. The responsible adoption status, scaling permission, and control need for each workflow translate directly into structured findings that a report can document and communicate to a client's leadership or governance team.

---

## 9. How This Connects to Build 6

Build 6 is the AI Governance Policy Checker. It reviews whether an organisation's governance policies cover the key responsible-use controls required for AI adoption.

Phase 5 is directly connected to Build 6 through the governance review control need. Workflows linked to Build 6 — such as governance checklist reviews, acceptable use policy reviews, and incident log management — should have the lowest risk signal density of any workflow group, because these are the workflows designed to strengthen governance. If a Build 6-related workflow itself shows high risk concern or requires a governance review, it suggests that the governance process itself has not been adequately controlled during the pilot.

---

## 10. How a Consultant Could Use This with a Small Organisation

A consultant working with a small organisation could use Build 7 Phase 5 as follows:

1. **After the pilot period**, review the Phase 1 adoption records for all active workflows, noting quality issues, risk incidents, near misses, and adoption decisions.
2. **Run the Phase 5 risk and quality review** to classify each workflow's responsible adoption status and identify the primary control need.
3. **Use the organisation-level summary** to give leadership a clear view of where quality concerns and risk signals are concentrated across the portfolio.
4. **Use the build-level summary** to identify whether particular practice areas — such as governance workflows or report-generation workflows — are carrying more risk than others.
5. **Use the prioritised action list** to open a structured conversation with the client about which workflows need immediate governance review, which need quality assurance controls, and which are already demonstrating responsible adoption.
6. **Use the control need recommendations** to move from diagnosis to action: governance review, quality assurance checklist, incident logging review, training reinforcement, or standard monitoring.

The key consulting discipline is to maintain the distinction between adoption that is happening and adoption that is happening responsibly. Phase 5 helps a consultant make that distinction clearly, and communicate it in a way that leads to concrete control decisions rather than general reassurances.

---

## 11. What Should Come Next in Phase 6

Phase 6 should add a Decision Tracker and Client Follow-up Evidence layer. This would:

- Provide a structured record of stop, continue, review, and scale decisions across the portfolio, linked to the quality and risk evidence from Phase 5.
- Allow a consultant to build a timeline of decision points that can be shared with a client as evidence of responsible governance.
- Generate follow-up prompts for each decision, identifying what evidence would be needed to change a stop or review decision to a continue or scale decision.
- Connect directly to Build 5 report generation, so that decision evidence can be exported as a client-ready follow-up document.

Phase 6 would close the responsible adoption loop: Phase 5 identifies where controls are needed, Phase 6 tracks whether those controls were acted upon and whether the decisions taken are defensible on the basis of the available evidence.

---

*Build 7 Phase 5 · AI Adoption ROI and Impact Tracker · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
