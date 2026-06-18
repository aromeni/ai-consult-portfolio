# Build 9 — Phase 3 Notes

## What Phase 3 Adds

Phase 3 adds the cross-build insight aggregator. For each of the seven build areas (Builds 1 through 8), it analyses all client stages associated with that build and produces a structured insight summary: completion rate, average evidence score, evidence health classification, and a deterministic build gap statement.

It also identifies the strongest and weakest build areas across the portfolio, produces a client-build status matrix showing each client's stage status across all builds at a glance, a prioritised build improvement list sorted by evidence weakness, and individual recommendations per build area.

The Streamlit Phase 3 page displays overview metrics, the full cross-build summary table, the client-build matrix, and the prioritised improvement list.

---

## Why Cross-Build Insights Matter

Phases 1 and 2 analyse the capstone journey from the client's perspective — which clients are ready, blocked, or developing. Phase 3 switches to the build perspective: which of the seven portfolio builds is generating strong evidence, and which is still weak across the client base?

This is important for two reasons. First, it reveals portfolio gaps: if Build 6 (Governance) is consistently weak across all three clients, that points to a systemic gap in the consulting practice, not just one client issue. Second, it gives a consultant a clear prioritisation signal: where should effort be directed before the capstone is presented as a complete end-to-end demonstration?

---

## How Build Evidence Health Is Classified

Build evidence health uses a four-level classification applied to all client stages for that build:

1. **Very strong evidence** — completion rate is 85% or above and average evidence score is 3.5 or above. This build is well-executed and well-evidenced across the client base.
2. **Strong evidence** — completion rate is 70% or above and average evidence score is 3.0 or above. Good coverage with solid evidence.
3. **Developing evidence** — completion rate is 40% or above and average evidence score is 2.0 or above. The build has started across clients but still needs improvement.
4. **Weak evidence** — anything below the developing thresholds. The build has low completion or poor evidence across clients and needs attention.
5. **No evidence** — no stages exist for this build area.

---

## How Strongest and Weakest Build Areas Are Identified

The strongest build area is determined by sorting all build summaries by average evidence score descending, then completion rate descending, then BUILD_ORDER position ascending as a tiebreaker. The top result is the strongest.

The weakest build area applies the same logic in ascending order: lowest average evidence score first, then lowest completion rate, then BUILD_ORDER position. This ensures deterministic results even if two builds score identically.

In the synthetic data, Build 4 (Staff training and enablement) emerges as the strongest because it includes a "Very strong" evidence stage from Greenacre Dental Group's signed acceptable-use agreements. Build 8 (Delivery and implementation tracking) is the weakest because two of three clients have not yet started delivery tracking.

---

## How This Supports the Capstone Story

The client-build matrix provides an immediate snapshot: which clients have completed which builds, and where the gaps are. A consultant preparing for a portfolio review can scan the matrix and see that Greenacre Dental Group has the most complete picture, while Northside Community Advice has two "Not started" build areas that need to be addressed before the engagement can be presented as end-to-end.

The prioritised build improvement list complements this: it surfaces Build 8 and Build 7 as the highest-priority areas for improvement, since both have clients that have not started these stages and both carry low average evidence scores.

---

## How a Consultant Could Use It

A consultant preparing the capstone for a portfolio review could use the Phase 3 cross-build insight aggregator to:

- Identify Build 4 (Staff training) as the strongest proof point and lead with it when explaining the consulting methodology to a prospective client.
- Flag Build 8 (Delivery tracking) as the area needing most improvement, and plan what evidence would need to be created before the capstone is presented as fully complete.
- Use the client-build matrix to explain the current state of each engagement and show which clients are further along.
- Use the prioritised improvement list to structure a one-page action plan for completing the capstone.
- Demonstrate to a prospective client that the consulting practice uses structured evidence scoring — not just activity tracking — to assess the quality of each engagement.

---

## What Phase 4 Should Add Next

Phase 4 should build the consulting recommendation pathway. This will:

- Draw on Phase 2 journey health and Phase 3 build evidence health together to generate a structured consulting recommendation for each client.
- Produce a narrative recommendation explaining where the client is in the AI adoption journey, what the strongest evidence says, and what the recommended next consulting step is.
- Connect the journey health classification, the weakest journey stage, and the weakest build area into one coherent client-level recommendation.
- Generate a portfolio-level recommendation for the consultant showing which clients are ready for a capstone presentation, which need more work, and what that work should be.

Phase 4 is where Build 9 moves from aggregating and classifying evidence to producing consulting output — turning data into a recommendation a consultant could present in a client meeting.

---

*Build 9 Phase 3 Notes · AI Adoption Consulting Capstone Dashboard · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
