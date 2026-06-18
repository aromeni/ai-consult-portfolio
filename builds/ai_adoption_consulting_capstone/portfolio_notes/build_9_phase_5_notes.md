# Build 9 — Phase 5 Notes

## What Phase 5 Adds

Phase 5 adds the capstone dashboard UI. It assembles all Phase 1–4 outputs into a single Streamlit experience: a portfolio-level snapshot, headline metrics, a client spotlight with a selectbox, three summary tables, and a consulting interpretation section.

It also introduces `logic/capstone_dashboard.py`, which provides the context-building functions that aggregate all previous logic modules into one unified view.

---

## Why the Dashboard UI Matters

Phases 1–4 build progressively deeper analytical layers: capstone data → journey analysis → cross-build insights → recommendation pathways. Phase 5 is the first phase where all of those layers appear together in a single view.

Without a unified dashboard, the app feels like four separate modules. With it, the full consulting story becomes visible: which clients are ready, which build areas need work, and what a consultant should do next. This is the phase that makes Build 9 feel like a client-facing portfolio tool rather than a set of technical demonstrations.

---

## How It Connects Builds 1–8

The dashboard brings all seven build areas into one place:

- **Build 1** → Journey health and completion rate from readiness diagnosis stages.
- **Build 2/3** → Document intelligence evidence shown in the cross-build table.
- **Build 4** → Staff training stages contribute to completion rate and evidence score.
- **Build 5** → Consulting report stages influence weakest-stage identification.
- **Build 6** → Governance stages often drive "Needs review" or "Blocked" health.
- **Build 7** → ROI stages not yet started contribute to blocked journeys and "Not ready" readiness.
- **Build 8** → Delivery tracking stages affect whether a client journey is complete end-to-end.

The dashboard status, client spotlight, and table sections reflect the cumulative state of all seven builds simultaneously.

---

## How It Presents the Capstone as One Consulting Journey

The dashboard snapshot is the first time the full portfolio is condensed into one line: a status (e.g. "Needs review"), a focus statement, the strongest and weakest build areas, and a recommended next step.

The client spotlight gives a consultant a way to present one client in detail without switching between analysis tabs. The three tables — client journeys, cross-build evidence, recommendation pathways — provide the evidence base, the build-level position, and the commercial direction in one scrollable view.

Together, these sections frame the full consulting engagement: from initial readiness through governance and training to delivery and capstone presentation.

---

## How a Consultant Could Use It

A consultant preparing for a portfolio review could use the Phase 5 dashboard to:

- Open with the Dashboard Snapshot to confirm the portfolio's current readiness position before a conversation.
- Use the Headline Metrics to quickly answer "how many clients are ready?" and "are there any blocked journeys?" without scrolling through data tables.
- Select a client in the Client Spotlight to show exactly what the consulting journey looks like for that organisation, including what to improve and what to offer commercially.
- Share the Cross-Build Evidence Table as a visual summary of which areas of the consulting practice are well-evidenced and which need more work.
- Use the Recommendation Pathway Table as the basis for a structured commercial conversation about next steps with each client.

---

## What Phase 6 Should Add Next

Phase 6 should build the Capstone Report Builder. This will:

- Generate a structured plain-text consulting narrative for one or all clients, using the Phase 4 recommendation pathway and Phase 2 journey summary as inputs.
- Produce a section for each build area covering what was done, what evidence exists, and what the next step is.
- Include a headline consulting summary paragraph that presents the portfolio as a coherent end-to-end service.
- Provide a pathway from the dashboard into a document that could be shown to a client or used as a portfolio asset.

Phase 6 is where Build 9 moves from an interactive dashboard into a concrete consulting output.

---

*Build 9 Phase 5 Notes · AI Adoption Consulting Capstone Dashboard · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
