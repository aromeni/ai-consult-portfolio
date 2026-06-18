# Build 9 — Phase 7 Notes

## What Phase 7 Adds

Phase 7 adds the Export Centre and Portfolio Evidence Pack. It introduces `logic/export_centre.py`, which provides functions to export the capstone dashboard and report outputs into reusable formats: Markdown, CSV, JSON, optional PDF via reportlab, and an optional PNG bar chart via matplotlib.

The Streamlit Export Centre page gives the user download buttons for all formats, a report scope selector for portfolio-level or client-level exports, a portfolio evidence summary metrics view, and a text preview of the evidence summary narrative.

---

## Why the Export Centre Matters

Phases 1–6 build the analytical infrastructure and convert it into an interactive dashboard and rendered report. Phase 7 moves that output outside the Streamlit UI into formats that can be shared, submitted, and reviewed independently.

A downloadable file serves a different purpose from a Streamlit preview. The Streamlit preview is for navigation and internal review. The downloaded file is for sending to a portfolio evaluator, attaching to a business development proposal, including in a GitHub portfolio, or submitting as structured consulting evidence.

Without Phase 7, the capstone output remains locked inside the running app. With it, the full consulting story becomes a portable artefact.

---

## How the Evidence Pack Supports Portfolio Review

The JSON evidence pack is the most complete format: it includes the raw synthetic data, all phase summaries, all client journey summaries, all cross-build summaries, all consulting recommendations, and the dashboard snapshot in one structured file. A technical reviewer can inspect it directly.

The CSV evidence table gives a flat view of every client/build-stage combination, useful for a reviewer who wants to verify evidence strength and consulting value at the stage level without navigating the Streamlit UI.

The Markdown report is the most readable format for a non-technical reviewer. The PDF wraps the same content in a layout-friendly document.

Together, these formats demonstrate that the consulting practice can produce structured, shareable evidence quickly from a consistent analytical foundation.

---

## How This Connects Builds 1–8

The CSV evidence table has one row per client/build stage. Each row links the stage back to its build number and domain. The seven build areas — AI Readiness, Document Intelligence, Staff Training, Consulting Report, Governance, ROI/Impact, and Delivery Tracking — each appear as rows in the table, showing exactly how the evidence was built up across the full consulting journey.

The JSON evidence pack includes `cross_build_summaries`, `client_journey_summaries`, and `consulting_recommendations`, which are the Phase 3, Phase 2, and Phase 4 outputs respectively. A reviewer can trace from the phase output back to the original stage-level evidence via `cross_build_stages`.

---

## How a Consultant Could Use It

A consultant preparing for a portfolio review or business development conversation could use the Phase 7 Export Centre to:

- Download the Markdown capstone report and share it with a technical portfolio reviewer.
- Export the JSON evidence pack and attach it to a GitHub portfolio or portfolio submission.
- Download the CSV evidence table and reference it during a client demonstration to show stage-by-stage evidence.
- Generate a scoped PDF for a specific client (BrightPath, Northside, or Greenacre) and use it as a client-facing summary document.
- Export the PNG readiness chart and include it in a slide deck or proposal.

---

## What Phase 8 Should Add Next

Phase 8 should be the final sweep, commercial positioning, and README polish. This will:

- Review all eight phases for consistency of language, British English, and consulting framing.
- Strengthen the README commercial narrative to describe Build 9 as a portfolio-ready product.
- Add a final consulting interpretation to the capstone dashboard that positions the seven build areas as a coherent AI adoption service.
- Review tests across all phases and confirm all 161+ tests continue to pass.
- Confirm the Streamlit app runs end-to-end without errors on all eight navigation items.

Phase 8 is where the capstone moves from technically complete to presentation-ready.

---

*Build 9 Phase 7 Notes · AI Adoption Consulting Capstone Dashboard · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
