# Build 9 — Phase 2 Notes

## What Phase 2 Adds

Phase 2 adds the client journey overview engine. For each synthetic capstone client, it analyses all seven cross-build journey stages and produces a structured summary: completion rate, average evidence score, journey health classification, weakest stage, and deterministic next step.

It also produces a journey health summary across all clients, a prioritised client review list sorted by urgency, and individual consulting recommendations for each client journey.

The Streamlit Phase 2 page displays overview metrics, a full client journey summary table, and a prioritised review table with recommendations.

---

## Why Client Journey Overview Matters

A capstone dashboard without analysis is just a collection of tables. The client journey overview engine converts raw stage data into consulting insight: it tells a consultant which clients are ready to be presented as portfolio evidence, which are developing, which need governance or evidence gaps resolved, and which cannot be presented until missing stages are completed.

This is the difference between a data dump and a consulting tool. The journey health classification and prioritised review list make the capstone useful for an active consulting engagement, not just a portfolio presentation.

---

## How Journey Health Is Classified

Journey health is classified using a four-level priority check:

1. **Blocked journey** — any stage has a status of "Not started". A blocked client cannot be presented as a complete capstone example because the consulting journey is incomplete.
2. **Needs review** — two or more stages are classified as "Needs review". The evidence or status is uncertain enough that further work is needed before converting this into a client story.
3. **Strong journey** — stage completion rate is 85% or above, and average evidence score is 3.5 or above. This client's journey is comprehensive and well-evidenced.
4. **Healthy journey** — completion rate is 70% or above, and average evidence score is 3.0 or above. The journey is progressing well with good evidence.
5. **Developing journey** — anything that does not meet the above criteria. The journey has started but needs more progress before it can be presented as a strong capstone asset.

---

## Why Evidence Strength Matters

Completing a journey stage is necessary but not sufficient. A "Completed" stage with "Weak" evidence is less valuable than a "Completed" stage with "Very strong" evidence. The average evidence score ensures that a client whose stages were technically completed but poorly evidenced does not rank as highly as a client whose stages produced strong, reusable portfolio material.

This mirrors real consulting practice: a governance review that produced a signed policy, a data boundary checklist, and an approved incident response guide is more valuable than one that produced a verbal confirmation.

---

## How This Connects Builds 1–8

Each journey stage in the Phase 2 analysis maps directly to a completed build:

- **Readiness diagnosis** → Build 1 outputs (readiness score, workflow priorities, pilot recommendation)
- **Document intelligence** → Build 2/3 outputs (retrieval demonstration, policy search capability)
- **Staff training** → Build 4 outputs (workshop design, training delivery, confidence building)
- **Consulting report** → Build 5 outputs (structured client-facing report and recommendations)
- **Governance review** → Build 6 outputs (maturity score, policy gaps, control readiness)
- **ROI and impact review** → Build 7 outputs (ROI evidence, workflow impact, adoption decisions)
- **Delivery tracking** → Build 8 outputs (implementation actions, blockers, delivery progress)

Phase 2 scores each of these stages by status and evidence strength, giving a compound view of how well each consulting engagement was executed across all seven builds.

---

## How a Consultant Could Use It

A consultant preparing for a portfolio review could use the Phase 2 client journey overview to:

- Identify which client (BrightPath, Northside, Greenacre) makes the strongest capstone story and lead with that one.
- Understand exactly which stages are weak and what would need to improve before presenting a client journey as complete.
- Prepare specific talking points for each client: "We're at 57% completion for BrightPath — governance and ROI tracking are in progress."
- Use the prioritised review list to structure a weekly or monthly work review: address blocked clients first, then those needing review, then developing journeys.
- Show the journey health classification to a potential client as evidence that the consulting methodology includes structured completion criteria, not just activity tracking.

---

## What Phase 3 Should Add Next

Phase 3 should build the cross-build insight aggregator. This will:

- Pull headline figures from each individual build's logic layer (e.g. readiness score from Build 1, governance maturity score from Build 6, ROI evidence from Build 7, delivery completion from Build 8).
- Aggregate these figures into a single cross-build insight record per client.
- Identify where the strongest evidence sits across the journey and where the weakest gaps are.
- Generate a cross-build consulting observation for each client that a consultant could use directly in a client meeting.

Phase 3 is where Build 9 moves from analysing its own synthetic data to drawing on the analytical outputs of the earlier builds.

---

*Build 9 Phase 2 Notes · AI Adoption Consulting Capstone Dashboard · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
