# Build 7 Phase 4 — Portfolio Notes

**AI Adoption ROI and Impact Tracker — Training, Confidence, and Adoption Readiness Review**

---

## 1. What Phase 4 Adds

Phase 4 adds a deterministic training readiness engine to the Build 7 adoption tracker. It analyses whether staff groups are becoming sufficiently trained, confident, and adoption-ready to use AI-supported workflows safely and practically.

The engine provides:

- Training completion classification — Low / Moderate / Good / Strong completion bands.
- Confidence level classification — Low / Developing / Good / Strong bands for confidence scores before and after the pilot.
- Confidence growth classification — No growth / Small / Moderate / Strong growth based on the change between before and after scores.
- Training readiness scoring — a composite 0–100 score combining training completion, confidence after, and confidence growth.
- Training readiness band classification — Not ready / Partly ready / Ready with support / Ready to scale.
- Training support need identification — Foundation training / Workflow-specific coaching / Confidence reinforcement / Light-touch support / Scale enablement.
- Staff adoption readiness classification — Blocked / Needs support / Developing / Adoption ready / Scale ready.
- Staff group readiness summaries — aggregates all readiness counts and averages by staff group.
- Organisation-level readiness summaries — aggregates by organisation.
- Related-build readiness summaries — shows how Build 1, Build 4, Build 5, and Build 6 are contributing to training and confidence outcomes.
- Prioritised training support actions — ranks workflows from most urgent to least urgent.
- Deterministic training support recommendations — one practical recommendation per workflow.

All calculations are deterministic and template-based. No external LLM or API is called.

---

## 2. Why Training and Confidence Matter in AI Adoption

Introducing AI to a small organisation is not primarily a technology challenge. The technology can usually be set up in hours. The harder challenge is whether staff trust it, understand its limits, and feel confident enough to use it well.

In practice, AI adoption fails or stalls for human reasons: staff who were not involved in the decision feel anxious about new tools; managers who were not trained cannot support their teams; confident early adopters push ahead while cautious colleagues stay behind. These dynamics do not show up in efficiency statistics. They show up in inconsistent use, quality problems, governance gaps, and a quiet reluctance to engage with the next phase of adoption.

Phase 4 makes the human layer of adoption measurable. It converts training completion rates and confidence scores into structured evidence that a consultant can use to identify where staff are ready, where they need support, and where adoption is at risk of stalling.

---

## 3. Why Time Saved Does Not Prove Readiness

Phases 2 and 3 focused on whether AI adoption is saving time and producing operational value. Phase 4 asks a different question: even if the time saving is real, are staff in a position to sustain and expand that adoption independently?

A workflow that saves five hours per week but is driven by one confident user who has not shared their practice with colleagues is fragile. Remove that user, and the time saving disappears. Scale the workflow to three more teams, and quality problems emerge because other staff have not received the same training.

Training readiness analysis identifies whether the adoption is person-dependent or team-embedded. A workflow with strong time saving but low training completion and weak confidence growth should not be scaled — it should be supported first.

---

## 4. How Readiness Is Scored

The training readiness score combines three signals into a composite 0–100 estimate:

- **Training completion** contributes up to 40 points, weighted as the single largest factor because it reflects the organisation's investment in preparing staff for adoption.
- **Confidence after** contributes up to 35 points, based on how confident staff feel using AI after the pilot. This captures the current state of capability, not just the change.
- **Confidence growth** contributes up to 25 points, based on how much confidence improved during the pilot period. Growth is capped to avoid rewarding starting from a very low baseline.

The resulting score is then classified into readiness bands: Not ready (below 40), Partly ready (40–60), Ready with support (60–80), and Ready to scale (80 and above).

The score is a synthetic consulting estimate. It is designed to give a consultant a single directional indicator to use in a conversation, not a validated psychometric measure.

---

## 5. Why Staff Groups Are Analysed Separately

Different staff groups within the same organisation often have very different relationships with AI adoption. Managers may be confident in using AI for reporting workflows but anxious about using it in client-facing communications. Administrators may have high training completion rates but low confidence in assessing the quality of AI-generated output. Frontline workers may be enthusiastic but not yet sure when it is safe to act on AI suggestions without human review.

Analysing readiness by staff group allows a consultant to:

- Identify which groups are ready to expand adoption and which need more structured support.
- Design targeted training interventions rather than generic all-staff sessions.
- Prioritise the groups whose readiness is most critical to the next phase of adoption.
- Avoid the common mistake of assuming that one confident team represents the organisation as a whole.

This level of granularity is especially important in small organisations where staff roles are often hybrid and training resources are limited.

---

## 6. How This Connects to Build 1

Build 1 is the AI Readiness and Workflow Audit Tool. It identifies candidate workflows and assesses whether the organisation's readiness foundations — governance, training, and process clarity — are in place.

Phase 4 of Build 7 provides the evidence to answer whether those foundations were sufficient. The training readiness scores and support needs in Phase 4 directly reflect the readiness factors Build 1 assessed before the pilot began. If Build 1 flagged low training readiness as a risk factor, Phase 4 shows whether that risk materialised as a training bottleneck or was successfully addressed.

---

## 7. How This Connects to Build 4

Build 4 is the AI Staff Training and Workshop Generator. It creates practical training materials to help staff use AI tools safely, confidently, and within appropriate boundaries.

Phase 4 directly measures the outcome of Build 4 investment. The training completion rate measures how thoroughly Build 4 training was delivered. The confidence before and after scores measure whether that training improved staff capability. The training support need identifies what type of follow-on Build 4 activity — whether a foundational session, workflow-specific coaching, or confidence reinforcement — would be most valuable next.

The build-level readiness summary in Phase 4 makes this link explicit: it shows how workflows related to Build 4 are performing on training and confidence metrics across the portfolio.

---

## 8. How This Connects to Build 5

Build 5 is the AI Consulting Report Generator. It produces structured client-facing reports summarising audit findings and recommendations.

Phase 4 produces exactly the kind of training and readiness evidence that a Build 5 consulting report would include in its training and capability section. The staff adoption readiness classifications, prioritised support actions, and training recommendations translate directly into actionable report content: here is who is ready, here is who needs support, and here is what we recommend.

---

## 9. How This Connects to Build 6

Build 6 is the AI Governance Policy Checker. It reviews whether an organisation's governance policies cover the key responsible-use controls required for AI adoption.

Phase 4 tracks the training and confidence outcomes for governance-related workflows — including governance checklist reviews, acceptable use policy reviews, and incident log management. A workflow linked to Build 6 that shows low training completion or weak confidence growth suggests that governance training is not yet embedded, even if the policy documentation exists.

This demonstrates the distinction between governance on paper and governance in practice: Phase 6 checks the policy, Phase 4 checks whether the staff carrying out governance responsibilities feel trained and confident enough to apply it.

---

## 10. How a Consultant Could Use This with a Small Organisation

A consultant working with a small organisation could use Build 7 Phase 4 as follows:

1. **After the pilot period**, review the Phase 1 adoption records for all active workflows, noting training completion rates and confidence scores.
2. **Run the Phase 4 training readiness engine** to classify each workflow's readiness status and identify the dominant training support need across staff groups.
3. **Use the staff group summary** to open a structured conversation with the client about which teams are progressing well and which need more support before adoption is extended.
4. **Use the organisation-level summary** to give leadership a clear view of overall readiness across the portfolio.
5. **Use the prioritised training support list** to agree a concrete next-step training plan: which workflows need foundation training immediately, which need workflow-specific coaching, and which are ready to move to scale enablement.
6. **Feed the Phase 4 analysis into a consulting report** (Build 5) to document the training evidence behind any scaling or pausing decisions.

The key consulting discipline is to distinguish between adoption that is working and adoption that is ready to expand. Phase 4 helps a consultant make that distinction clearly, and communicate it to the client in a way that leads to a practical training investment decision.

---

## 11. What Should Come Next in Phase 5

Phase 5 should add a Risk, Quality, and Responsible Adoption Review. This would:

- Provide a dedicated review of quality issues and risk incidents across the portfolio, going deeper than the bottleneck detection in Phase 3.
- Calculate quality issue rates and risk signal densities across organisations and builds.
- Classify each workflow's responsible adoption status, identifying where governance controls are insufficient or where quality is not yet acceptable for wider use.
- Generate structured responsible adoption summaries that a consultant could share with a client's leadership or governance team.
- Connect directly to Build 6 governance evidence to show where policy gaps are affecting adoption quality.

Phase 5 would close the responsible adoption loop: Phase 4 ensures staff are ready, Phase 5 ensures the adoption itself is being conducted responsibly.

---

*Build 7 Phase 4 · AI Adoption ROI and Impact Tracker · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
