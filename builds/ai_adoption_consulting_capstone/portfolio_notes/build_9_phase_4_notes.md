# Build 9 — Phase 4 Notes

## What Phase 4 Adds

Phase 4 adds the consulting recommendation pathway. For each synthetic client, it converts the journey health, completion rate, and evidence score from Phase 2 into a structured consulting decision: whether the client is ready for capstone presentation, which consulting pathway applies, what the commercial next step should be, and which improvement area to focus on first.

It also produces a recommendation priority classification, a pathway summary across all clients, a prioritised client list sorted by urgency, deterministic consulting recommendation text per client, and a simplified pathway matrix for dashboard display.

The Streamlit Phase 4 page displays pathway overview metrics, a full recommendation summary table, the pathway matrix, and a prioritised client list.

---

## Why Recommendation Pathways Matter

Phases 1–3 aggregate and classify evidence. Phase 4 turns that classification into a consulting direction. Without a recommendation pathway, the dashboard tells a consultant what the data says but not what to do next.

The pathway answers a practical question: given what we know about BrightPath, Northside, and Greenacre, which one should be presented first, which one needs more work, and what would a follow-up engagement look like? These are the decisions a consultant makes before a portfolio review or new business conversation.

---

## How Capstone Readiness Is Classified

Capstone readiness is derived directly from Phase 2 journey health and the underlying evidence metrics:

- **Capstone ready** — Strong journey health with completion rate above 85% and average evidence score above 3.5. The client story is complete and well-evidenced.
- **Nearly ready** — Strong or Healthy journey health with completion rate above 70% and average evidence score above 3.0. One more round of evidence strengthening would make this capstone-quality.
- **Needs strengthening** — Developing journey or Needs review health. The journey has started but the evidence is not yet strong enough to use as a standalone capstone demonstration.
- **Not ready** — Blocked journey. Missing stages mean the consulting journey is incomplete and should not be presented as end-to-end evidence.

In the synthetic data, all three clients are classified as "Needs strengthening" (BrightPath and Greenacre — Developing journey) or "Not ready" (Northside — Blocked journey). This represents a realistic early-stage consulting portfolio where no client has yet reached the highest readiness level.

---

## How Commercial Next Steps Are Selected

Each commercial next step is matched to journey health rather than capstone readiness, so it reflects the most appropriate commercial offer for the client's current position:

- **Strong journey** → Portfolio demonstration: this client can anchor a new business conversation.
- **Healthy journey** → Paid implementation review: the client is progressing and can be engaged for structured follow-up.
- **Needs review** → Governance improvement sprint: the most valuable intervention is resolving governance uncertainty.
- **Developing journey** → Training and adoption support package: the client needs more structured enablement before progressing further.
- **Blocked journey** → Document intelligence upgrade: the client needs to resolve foundational gaps before any other intervention.

These options give a consultant a ready-made commercial anchor for each client interaction, framed in terms of value to the client rather than consultant activity.

---

## How This Connects Builds 1–8

The recommendation pathway draws on outputs from all previous phases:

- **Build 1** → Readiness diagnosis stages inform journey health and completion rate.
- **Build 2/3** → Document intelligence stages contribute to evidence scoring.
- **Build 4** → Staff training stages contribute to completion rate and evidence strength.
- **Build 5** → Consulting report stages anchor the "consulting pathway" classification.
- **Build 6** → Governance stages often drive "Needs review" and "Blocked" health states.
- **Build 7** → ROI stages that are "Not started" trigger "Blocked journey" and "Not ready" readiness.
- **Build 8** → Delivery tracking stages affect completion rate and determine whether a client can be presented as having a complete end-to-end engagement.

The recommendation pathway is the first phase where the full analytical output of Builds 1–8 is converted into a decision a consultant could use directly in a client conversation.

---

## How a Consultant Could Use It

A consultant preparing for a portfolio review or business development conversation could use the Phase 4 recommendation pathway to:

- Identify immediately that Northside Community Advice is "Not ready" and should not be the lead capstone example. It instead becomes a "Document intelligence upgrade" commercial opportunity.
- Lead with Greenacre Dental Group as the strongest capstone story currently available, while being clear that the journey is "Needs strengthening" rather than complete.
- Use the prioritised client list to structure a fortnightly consulting review: address the high-priority blocked client first, then the two developing clients.
- Show a prospective client the "Consulting Recommendation Pathway" section as evidence that the consulting practice uses structured decision frameworks, not gut feel, to prioritise client work.
- Prepare a clear commercial proposal for each client based on the "Commercial next step" classification.

---

## What Phase 5 Should Add Next

Phase 5 should build the Capstone Dashboard UI. This will:

- Present the headline capstone story for the full portfolio in a single well-structured page, rather than across separate analysis pages.
- Show the strongest client and build areas prominently at the top.
- Include a narrative summary of the AI adoption consulting journey so far.
- Provide a structured consulting story that moves from readiness through governance, training, reporting, ROI, and delivery to capstone presentation.
- Use the Phase 4 recommendation pathway outputs as the basis for the capstone narrative.

Phase 5 is where Build 9 moves from structured data analysis to a client-facing consulting story.

---

*Build 9 Phase 4 Notes · AI Adoption Consulting Capstone Dashboard · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
