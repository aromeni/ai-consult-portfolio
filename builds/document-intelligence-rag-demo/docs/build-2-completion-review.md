# Build 2 Completion Review

**Document Intelligence / RAG Demo**
**Date:** 10 June 2026
**Version:** Prototype v0.6

---

## Purpose of this Review

This document records the completion of Build 2: Document Intelligence / RAG Demo. It summarises what was built, how, why, and what it proves — for portfolio review, future reference, and handover to the next build.

---

## Build Goal

Create a working prototype that demonstrates safe document intelligence using synthetic policy documents. The tool allows a consultant, manager, or governance lead to:

1. Browse a library of synthetic policy documents
2. Search documents by keyword across one or all documents
3. Extract evidence for a chosen policy topic
4. Generate a cross-document risk and safeguard summary
5. Produce a downloadable Markdown evidence brief
6. Ask evidence-based policy questions and receive a structured templated answer

All without using external AI APIs, embeddings, or a vector database.

---

## What Was Built

A 7-page Streamlit application for deterministic document intelligence, supported by 6 source modules and a test suite of 229 tests. The app uses synthetic policy documents and produces evidence-grounded outputs including keyword search results, topic-based evidence snippets, risk summaries, and policy Q&A answers.

---

## Completed Phases

### Phase 1: Scaffold

Folder structure, Streamlit navigation, four synthetic policy documents, three source modules (`document_loader.py`, `simple_search.py`, `evidence_extractor.py`), initial test suite.

### Phase 2: Document Library and Viewer

Document library page with metadata (word count, line count, size). Document Viewer page with full document display and inline keyword search.

> Note: Phase 2 was completed inline as part of Phase 1. The Document Library and Viewer pages were live from the initial scaffold.

### Phase 3: Keyword Search Across Documents

Rewrote `simple_search.py` with `normalise_text`, `tokenise_query` (stop-word filtering), `search_document` (deduplication, relevance count, matched terms), and `search_documents` (cross-document). Policy Q&A page made fully functional with suggested searches, scope selector, and results display.

### Phase 4: Evidence Extraction by Topic

Expanded `evidence_extractor.py` from 9 to 13 topics. Added `get_supported_topics()`, `get_topic_keywords()`, `get_topic_description()`, `extract_evidence_from_documents()`. Updated `extract_policy_evidence()` with `document_name`, `relevance_count`, deduplication, and sorting. Evidence Extraction page fully functional.

### Phase 5: Risk and Safeguard Summary

Created `risk_summary.py` from scratch with deterministic risk mapping for all 13 topics. Functions: `get_risk_summary_for_topic`, `summarise_evidence_for_topic`, `generate_risk_safeguard_summary`, `get_overall_summary`, `generate_risk_summary_markdown`. Risk and Safeguard Summary page fully functional with topic set presets, per-topic expanders, and Markdown download.

### Phase 6: Mini Brief Generator

Rewrote `brief_generator.py` with `generate_short_answer`, `deduplicate_list`, `generate_next_actions`, `generate_markdown_brief` (9-section structure), and `create_brief_filename`. Mini Brief page fully functional with 4 presets, 6 suggested questions, topic multiselect, generate button, and Markdown download.

### Phase 7: Evidence-Based Policy Q&A

Created `qa_engine.py` with `detect_topics_from_question` (keyword + co-detection), `generate_policy_answer` (templated, deterministic), `get_question_limitations`, `answer_policy_question` (full pipeline), and `generate_qa_markdown`. Policy Q&A page restructured with two tabs: Keyword Search (preserved) and Evidence-Based Q&A (new).

### Phase 8: Completion Review and Portfolio Notes

Created this completion review, portfolio case study, updated demo script, screenshots checklist, build reflection, and future improvements. README overhauled for portfolio presentation. Build-notes updated to v0.6.

---

## Key Features

- **Synthetic policy document library** — four Markdown documents covering acceptable use, data protection, safeguarding boundaries, and staff training
- **Document metadata and viewer** — word count, line count, file size, full document display with inline search
- **Multi-term keyword search** — cross-document, ranked by relevance count, with matched terms displayed
- **Topic-based evidence extraction** — 13 policy topics, keyword matching, deduplication, sorted by relevance
- **Deterministic risk and safeguard summary** — one risk record per topic, coverage notes, overall summary, Markdown download
- **Automated Markdown mini brief** — 9-section brief from topics, evidence, and risk data; downloadable
- **Evidence-based policy Q&A** — topic detection from question text, co-detection expansion, templated answer, evidence snippets, safeguards, owners, limitations, download
- **Source snippets and line references** — all results show document name and line number
- **Responsible-use warnings** — on every page, on every generated output
- **Tests for all core logic** — 229 passing tests across 6 test files

---

## Methodologies Reused

- **Layer 4 software build methodology** — iterative phases, testable logic, clean source modules
- **Layer 5 document intelligence and evidence extraction methodology** — keyword-to-evidence pipeline, topic mapping, source grounding before generative AI
- **Layer 6 governance and responsible AI controls** — risk mapping, safeguard recommendations, responsible-owner assignment, limitations disclosure
- **Build 1 lessons** — Streamlit session-state pre-fill pattern, downloadable outputs, responsible-use warnings, pytest test structure

---

## Technical Implementation

| Component | Approach |
|---|---|
| UI | Streamlit 7-page app with `st.session_state` for cross-page state |
| Document loading | `document_loader.py` with `@st.cache_data` |
| Keyword search | `simple_search.py` — tokenise, stop-word filter, match, deduplicate, sort |
| Evidence extraction | `evidence_extractor.py` — topic keyword lists, line-level matching |
| Risk/safeguard mapping | `risk_summary.py` — deterministic dict, 13 topics |
| Brief generation | `brief_generator.py` — templates + `collections.defaultdict` grouping |
| Q&A engine | `qa_engine.py` — keyword co-detection + templated answers |
| Testing | `pytest` — 229 tests, 0 failures |
| External AI APIs | None |
| Embeddings | None |
| Vector database | None |
| Database | None |
| Authentication | None |

---

## Responsible Use Boundaries

The following boundaries are enforced throughout Build 2 and must not be relaxed without governance approval:

- **Synthetic documents only** — all four policy documents are fictional and clearly labelled
- **No real learner data** — names, records, grades, attendance, or any learner-identifying information
- **No safeguarding case data** — disclosures, concerns, referrals, or child protection records
- **No confidential client records** — contracts, pricing, commercial strategy, or client-specific information
- **No staff HR data** — performance reviews, appraisals, disciplinary records, or HR files
- **No personal data** — nothing that could identify a living individual
- **No regulated information** — health, financial, legal, or data-protection-regulated content
- **Human review required** — all outputs are evidence starting points, not final authority
- **Not professional advice** — not legal, safeguarding, HR, compliance, medical, financial, or academic-integrity advice
- **Prototype output is supportive evidence review** — not a decision-making system

---

## Evidence That Build 2 Is Complete

The following verifiable references confirm build completion:

- `app.py` contains all seven navigation pages: Home, Document Library, Document Viewer, Policy Q&A, Evidence Extraction, Risk and Safeguard Summary, Mini Brief
- `data/synthetic_documents/` contains four synthetic policy Markdown documents
- `src/document_loader.py` exists with `list_documents`, `load_document`, `get_document_metadata`
- `src/simple_search.py` exists with `normalise_text`, `tokenise_query`, `search_document`, `search_documents`
- `src/evidence_extractor.py` exists with 13-topic `TOPIC_KEYWORDS`, `extract_policy_evidence`, `extract_evidence_from_documents`
- `src/risk_summary.py` exists with `_RISK_MAPPING` (13 topics), `generate_risk_safeguard_summary`, `get_overall_summary`
- `src/brief_generator.py` exists with `generate_markdown_brief`, `generate_short_answer`, `deduplicate_list`
- `src/qa_engine.py` exists with `detect_topics_from_question`, `answer_policy_question`, `generate_qa_markdown`
- `tests/` contains 6 test files covering all source modules
- `pytest` runs and reports 229 tests passing, 0 failures
- Streamlit app runs locally with `streamlit run app.py`

---

## What This Build Proves

- Rashid can build a document intelligence prototype from scratch in Python and Streamlit
- Rashid can design and implement safe synthetic document workflows with appropriate boundaries
- Rashid can implement evidence extraction before adding generative AI
- Rashid understands RAG foundations: documents, retrieval, evidence, source grounding, and limitations
- Rashid can connect AI governance topics (safeguarding, data minimisation, accountability) with policy evidence
- Rashid can create explainable deterministic logic that is transparent, auditable, and extensible
- Rashid can maintain responsible-use controls across a multi-phase build
- Rashid can produce portfolio-ready Streamlit apps with tests, documentation, and download outputs
- Rashid can think about the progression from keyword matching to embeddings to LLM-assisted Q&A

---

## What This Build Does Not Prove

- Real RAG with embeddings and a vector database
- Semantic search or natural language understanding
- Production document ingestion (OCR, PDF parsing, secure upload handling)
- Client validation or real-world organisational accuracy
- Production deployment or infrastructure configuration
- Legal or compliance approval for any output
- Accuracy on real organisational documents
- Suitability for live sensitive data of any kind
- Commercial traction or contract-ready delivery

---

## Remaining Optional Improvements

The build is complete as a prototype. Optional improvements for future polish:

- Capture portfolio screenshots using [screenshots-checklist.md](screenshots-checklist.md) — `assets/screenshots/` folder is in place
- Add PDF export for mini briefs
- Add semantic search and local embeddings in a later phase
- Add LLM-assisted answers with strict evidence grounding and safeguards
- Add richer test coverage for edge cases and empty-document scenarios
- Add a portfolio walkthrough video

See [future-improvements.md](future-improvements.md) for the complete list by priority.

---

## Readiness for Portfolio / Demo Use

**Build 2 is ready for portfolio and demo use with synthetic documents**, subject to:
- Adding screenshots for visual portfolio materials
- Light presentation polish (headings, spacing) if needed

No further code changes are required for portfolio or demo readiness.

---

## Recommended Next Actions

1. **Capture screenshots** for the app pages listed in [screenshots-checklist.md](screenshots-checklist.md)
2. **Add simple deployment notes** (Streamlit Cloud or local Docker) if not already present
3. **Start Build 3** or upgrade Build 2 into a true RAG version by adding local embeddings, a vector store, and optionally an LLM-assisted answer layer with strict evidence grounding

---

## Final Verdict

**Build 2 is complete as a deterministic, portfolio-ready document intelligence prototype using synthetic policy documents.**

It demonstrates the full evidence extraction pipeline — from document loading through keyword search, topic-based extraction, risk mapping, brief generation, and evidence-based Q&A — without external AI APIs, embeddings, or a vector database. All logic is transparent, testable, and auditable.

---

*Build 2 · Document Intelligence / RAG Demo · BrightPath ChatGPT Mastery Project*
