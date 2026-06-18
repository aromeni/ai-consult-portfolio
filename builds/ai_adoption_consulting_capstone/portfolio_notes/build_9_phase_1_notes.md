# Build 9 — Phase 1 Notes

## What Phase 1 Adds

Phase 1 creates the scaffold and synthetic data layer for the AI Adoption Consulting Capstone Dashboard. It establishes three synthetic client organisations, twenty-one cross-build journey stages, three portfolio indicator records, and all validation logic needed to confirm that the data is structurally sound.

The Streamlit page for Phase 1 displays this data as tables with a headline summary and a validation check. It also explains how Build 9 connects to each of the previous seven builds.

Phase 1 does not aggregate outputs from the individual builds. That work begins in Phases 2 and 3.

---

## Why a Capstone Dashboard Matters

Most consulting portfolios show individual tools in isolation. A capstone dashboard demonstrates something more commercially significant: that the consultant can connect a journey across multiple tools, explain how they relate to each other, and present a coherent client-facing picture.

Build 9 answers the question that a serious buyer always asks: "If I engaged you for a full AI adoption programme, what would the whole thing look like?" The capstone gives a concrete, evidence-based answer — shown through the same three fictional organisations that appear throughout the portfolio.

---

## How This Connects Build 1

Build 1 is the AI Readiness and Workflow Audit Tool. It assesses an organisation's readiness for AI adoption, scores candidate workflows, and produces a pilot recommendation.

Build 9 uses the readiness findings from Build 1 as the starting point of each client's journey. The capstone journey stage for Build 1 captures whether the readiness diagnosis was completed, how strong the evidence is, and what consulting value it provided. In later phases, Build 9 will surface the readiness score and workflow priority directly from Build 1's logic.

---

## How This Connects Builds 2/3

Builds 2 and 3 are document intelligence tools: a semantic RAG policy assistant and a document intelligence RAG demo. They demonstrate AI-assisted document retrieval, semantic search, and policy question-answering.

Build 9 treats Builds 2/3 as a single journey stage — document intelligence review — because they address the same consulting need: showing how an organisation's existing documents can be made searchable and retrievable using AI. The capstone represents this stage as a capability description and evidence note rather than a live data feed, which is appropriate given that RAG tools produce outputs through interactive queries rather than pre-computed summaries.

---

## How This Connects Build 4

Build 4 is the AI Staff Training and Workshop Generator. It produces structured workshop plans, training packs, facilitator guides, and knowledge checks.

Build 9 draws on Build 4 as the staff training stage of the consulting journey. The journey stage captures whether training was delivered, how strong the evidence is, and what the training achieved for the client. In later phases, Build 9 may surface training summary details such as workshop duration, delivery mode, and follow-up obligations.

---

## How This Connects Build 5

Build 5 is the AI Consulting Report Generator. It produces structured client-facing reports covering readiness findings, workflow priorities, risk assessments, and recommendations.

Build 9 treats the Build 5 consulting report as a formal milestone in the journey — the point at which all prior work is synthesised into a professional document that a client receives. The journey stage captures the report's completion status and the consulting value it provided.

---

## How This Connects Build 6

Build 6 is the AI Governance Policy Checker. It assesses governance maturity, identifies policy gaps, generates improvement priorities, and produces a structured governance maturity summary.

Build 9 draws on Build 6 as the governance review stage. This is often the most critical stage for small and medium organisations: without adequate governance controls, broader adoption cannot safely proceed. The capstone captures governance position, control readiness, and sign-off status as key indicators.

---

## How This Connects Build 7

Build 7 is the AI Adoption ROI and Impact Tracker. It tracks workflow impact, records adoption evidence, measures time savings, assesses training readiness, and produces stop, continue, review, or scale decisions.

Build 9 draws on Build 7 as the impact measurement stage. This is where adoption value is quantified and the business case for continued investment is built. The capstone captures ROI position and adoption decision as portfolio indicators.

---

## How This Connects Build 8

Build 8 is the AI Adoption Delivery and Implementation Tracker. It converts consulting recommendations into owned implementation actions with priorities, deadlines, blockers, governance sign-offs, training follow-up, and client check-in summaries.

Build 9 draws on Build 8 as the delivery tracking stage — the operational layer that ensures recommendations are actually implemented. The delivery position indicator captures whether implementation is active, what blockers exist, and how far along the client is in their implementation plan.

---

## What a Consultant Could Use It For

A consultant presenting their AI adoption methodology to a potential client or employer could use Build 9 to:

- Walk through the full consulting journey from readiness to delivery.
- Show how different tools are used at different stages of an engagement.
- Compare client progress across three different organisations at different stages.
- Explain why some clients are portfolio-ready and others are still developing.
- Demonstrate that consulting value is tracked, evidenced, and connected — not just described.

The capstone dashboard replaces a ten-page portfolio document with a live, interactive demonstration that a reviewer can explore.

---

## What Phase 2 Should Add Next

Phase 2 should build the Client Journey Overview Engine. This will:

- Display a single-client view showing all seven journey stages for one selected organisation.
- Provide a stage-by-stage status and evidence breakdown.
- Summarise the client's overall journey position.
- Flag which stages are blocking progress and which stages are portfolio-strong.
- Generate a brief Markdown journey summary for the selected client.

Phase 2 will make the data in Phase 1 navigable and client-specific rather than shown as flat tables across all organisations.

---

*Build 9 Phase 1 Notes · AI Adoption Consulting Capstone Dashboard · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
