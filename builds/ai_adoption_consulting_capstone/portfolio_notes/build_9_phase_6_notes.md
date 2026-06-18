# Build 9 — Phase 6 Notes

## What Phase 6 Adds

Phase 6 adds the capstone report builder. It introduces `logic/capstone_report.py`, which provides functions to generate a structured Markdown consulting report from the Phase 1–5 capstone data and logic outputs.

The report can be generated at portfolio level (all three synthetic clients, all seven build areas) or at client level (one selected client scoped to their journey, evidence, and recommendations). The Streamlit Capstone Report Builder page renders the report directly as Markdown.

---

## Why a Capstone Report Matters

Phases 1–5 build the analytical infrastructure: data, journey analysis, cross-build insights, recommendation pathways, and a unified dashboard. Phase 6 converts that infrastructure into a document.

A report serves a different purpose from a dashboard. A dashboard is for navigation and quick decisions. A report is for presenting, sharing, and archiving the consulting story. It can be shown to a prospective client, included in a portfolio submission, or used to walk a stakeholder through the AI adoption journey from start to finish.

Without Phase 6, the capstone story lives only in interactive widgets. With it, the full consulting narrative becomes a structured, readable document.

---

## How the Report Connects Builds 1–8

The report sections are directly mapped to the seven build areas:

- **Executive summary** → headline outputs from all phases combined.
- **Client overview** → captures the client profile that Build 1 readiness work would establish.
- **AI adoption journey section** → reflects the stage-by-stage consulting progression across Builds 1–8.
- **Cross-build evidence section** → shows the evidence position for each of the seven build areas.
- **Consulting recommendation pathway section** → derived from the Phase 4 recommendation logic, itself built on all eight stages.
- **Consulting interpretation** → narrative that ties readiness, document intelligence, training, reporting, governance, ROI, and delivery tracking into one coherent service.
- **Next steps** → deterministic bullets per client based on capstone readiness, giving a consultant a ready-made action list.

---

## How It Supports Consulting and Product Positioning

The capstone report demonstrates several things simultaneously:

1. That the consulting practice works from structured evidence, not opinion — each section is backed by the analytical outputs from Phases 1–5.
2. That the practice can produce client-facing documents quickly, using deterministic logic applied to collected evidence.
3. That the seven build areas form a coherent end-to-end service offering, not a disconnected set of tools.

The `build_full_capstone_report` function can take a `client_id` argument, meaning a consultant can generate a tailored report for each client in minutes by switching the scope selector.

---

## How a Consultant Could Use It

A consultant preparing for a portfolio review or business development conversation could use the Phase 6 report builder to:

- Generate a portfolio-level report to walk a prospective client through the full AI adoption consulting methodology.
- Generate a client-level report for BrightPath, Northside, or Greenacre to show what the consulting journey looks like for a specific organisation and sector.
- Use the Next Steps section as a client-facing action plan based on the capstone readiness classification.
- Share the Markdown output with a technical reviewer or portfolio evaluator who wants to see the structure of the consulting approach.
- Extend Phase 7 export capabilities by using the Phase 6 Markdown content as the input for a downloadable file.

---

## What Phase 7 Should Add Next

Phase 7 should build the Export Centre. This will:

- Provide a Streamlit download button for the full capstone report as a plain-text Markdown file.
- Optionally provide a plain-text version of the same report for copy-paste use.
- Allow the user to select which client or scope to export.
- Package the portfolio evidence into a structured downloadable format for portfolio submission.

Phase 7 is where the capstone output moves from the Streamlit UI into a format that can be shared outside the app.

---

*Build 9 Phase 6 Notes · AI Adoption Consulting Capstone Dashboard · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
