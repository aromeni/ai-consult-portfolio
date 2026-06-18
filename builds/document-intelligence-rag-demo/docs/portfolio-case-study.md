# Document Intelligence / RAG Demo — Portfolio Case Study

**Build 2 of the ChatGPT Mastery / GPT Master Project**
**Role:** Lead developer — Rashid
**Date:** June 2026

---

## One-Line Summary

A deterministic document intelligence prototype that searches, extracts evidence from, and generates risk summaries and Q&A answers from synthetic policy documents — without external AI APIs, embeddings, or a vector database.

---

## Problem

Training providers and organisations implementing AI face a consistent early challenge: they have policy documents, governance guidance, and acceptable-use policies — but no structured way to extract, review, and act on what those documents actually say.

Before adding embeddings or a language model, they need:

- A way to find and extract relevant policy statements across multiple documents
- A risk and safeguard framework mapped to real policy evidence
- A way to answer governance questions and generate briefing notes from that evidence
- Confidence that no sensitive data has been exposed to external systems

This prototype addresses all four needs as a safe, transparent, auditable scaffold.

---

## Target User

- AI consultants demonstrating document intelligence to training providers and governance leads
- Managers and compliance leads reviewing AI governance policy coverage
- Developers learning to build document intelligence tools safely before adding AI model calls

---

## Workflow Context

This tool fits into an AI implementation workflow at the "evidence review" stage — before an organisation adopts AI tools, a consultant or governance lead reviews the existing policies, identifies gaps, and generates a brief for discussion. Build 2 makes that review structured, fast, and traceable.

---

## Goals

1. Load and browse synthetic policy documents
2. Search documents by keyword across one or all documents
3. Extract policy evidence by topic with source references
4. Generate a cross-document risk and safeguard summary
5. Produce a downloadable Markdown evidence brief
6. Answer evidence-based policy questions deterministically
7. Maintain visible responsible-use boundaries throughout

---

## Success Criteria

| Criterion | Met? |
|---|---|
| 7-page Streamlit app running locally | Yes |
| Four synthetic policy documents loaded | Yes |
| Keyword search with relevance ranking | Yes |
| Evidence extraction for 13 policy topics | Yes |
| Risk and safeguard summary for all 13 topics | Yes |
| Downloadable Markdown brief | Yes |
| Evidence-based Q&A with topic detection | Yes |
| 229 tests passing | Yes |
| Responsible-use warnings on all pages | Yes |
| No external AI API calls | Yes |

---

## Solution Overview

A Streamlit multi-page application built in Python, using four synthetic Markdown policy documents as its document library. All processing is deterministic: keyword matching identifies relevant lines, topic keyword lists map lines to policy topics, risk records map topics to known risks and safeguards, and template-based generation produces structured outputs.

The application demonstrates the complete document intelligence pipeline — from document loading through evidence extraction, risk mapping, brief generation, and Q&A — as a safe, explainable, auditable foundation for future AI augmentation.

---

## Key Features

- **Document library** — metadata-rich browsable document list
- **Inline document search** — keyword search within a selected document
- **Multi-term keyword search** — cross-document, ranked by relevance, with matched terms
- **Topic-based evidence extraction** — 13 policy topics, keyword matching, sorted by relevance
- **Risk and safeguard summary** — one deterministic risk record per topic, with evidence coverage note
- **9-section Markdown mini brief** — title, question, evidence, risks, safeguards, next actions, limitations, reviewer notes
- **Evidence-based Q&A** — topic detection from question text, co-detection expansion, templated answer, safeguards, owners, limitations
- **Downloadable Markdown outputs** — briefs, risk summaries, Q&A answers

---

## Architecture

```
User question / keyword
        ↓
detect_topics_from_question / tokenise_query
        ↓
extract_policy_evidence / extract_evidence_from_documents
(keyword matching against document lines)
        ↓
generate_risk_safeguard_summary / get_risk_summary_for_topic
(deterministic risk record lookup)
        ↓
generate_policy_answer / generate_markdown_brief / generate_qa_markdown
(template-based output generation)
        ↓
Streamlit display + Markdown download
```

All logic is synchronous, deterministic, and auditable. No model calls, no embeddings, no external services.

---

## Tech Stack

| Component | Technology |
|---|---|
| UI | Streamlit |
| Language | Python 3.11 |
| State management | `st.session_state` |
| Document format | Markdown (.md) |
| Data tables | Pandas |
| Search | Deterministic keyword matching |
| Topic detection | Keyword + co-detection mapping |
| Risk mapping | Dict-based lookup |
| Output generation | Template strings + `collections.defaultdict` |
| Testing | pytest — 229 tests |
| External APIs | None |
| Embeddings | None |
| Vector database | None |
| Authentication | None |

---

## Data / Documents / Inputs

**All documents are synthetic Markdown policy documents. No real learner, safeguarding, confidential, staff HR, personal, or regulated data is used at any point.**

The four synthetic documents cover:

| Document | Coverage |
|---|---|
| `synthetic-ai-acceptable-use-policy.md` | Approved/prohibited use, learner data, safeguarding, human review, accountability, escalation |
| `synthetic-data-protection-guidance.md` | Data minimisation, anonymisation, approved tools, retention, incident reporting |
| `synthetic-safeguarding-and-ai-boundaries.md` | Safeguarding/AI boundary, escalation, AI decision limits, safe/unsafe prompt examples |
| `synthetic-staff-ai-training-notes.md` | Hallucination risk, bias, copyright, verification, escalation, safe use |

Each document is 400–700 words. Each contains "Synthetic — for demonstration purposes only" in the header.

---

## AI / Model / API Approach

**This version does not use external AI APIs, embeddings, vector databases, or generative model calls.**

It is a deterministic document intelligence prototype using:
- Keyword search and tokenisation
- Topic keyword lists
- Keyword co-detection for related topics
- Deterministic risk and safeguard mapping
- Template-based output generation

This is the correct foundation before adding AI model calls. It allows transparent review, safe demonstration, and a clear baseline for comparing keyword-only vs embedding vs LLM-assisted results.

---

## Implementation Process

| Phase | What was built |
|---|---|
| Phase 1 | Scaffold — document loading, navigation, 4 synthetic docs, initial tests |
| Phase 2 | Document Library page and Document Viewer page |
| Phase 3 | Keyword search — `simple_search.py`, Policy Q&A page |
| Phase 4 | Evidence extraction — 13 topics, `evidence_extractor.py`, Evidence Extraction page |
| Phase 5 | Risk summary — `risk_summary.py`, Risk and Safeguard Summary page |
| Phase 6 | Mini brief — `brief_generator.py`, Mini Brief page |
| Phase 7 | Evidence Q&A — `qa_engine.py`, Policy Q&A page (two tabs) |
| Phase 8 | Completion review and portfolio documentation |

---

## Testing and Validation

| Test file | Tests | Coverage |
|---|---|---|
| `test_document_loader.py` | 15 | list, load, metadata |
| `test_simple_search.py` | 36 | normalise, tokenise, search, multi-doc |
| `test_evidence_extractor.py` | 44 | topics, keywords, extraction, cross-doc |
| `test_risk_summary.py` | 40 | mapping, evidence summary, overall summary, Markdown |
| `test_brief_generator.py` | 41 | short answer, deduplication, next actions, brief, filename |
| `test_qa_engine.py` | 53 | topic detection, co-detection, answer generation, Q&A result, Markdown |

All 229 tests pass. No mocking of document loading — tests use real synthetic documents or minimal inline fixtures.

---

## Demo Notes

- Best shown live in Streamlit running locally
- Full demo takes 10–15 minutes following the demo script
- Focused demo (Q&A only) takes 5 minutes
- All page outputs are immediately visible — no loading delays
- Markdown downloads are ready immediately after generation
- See [demo-script.md](demo-script.md) for the step-by-step walkthrough

---

## Results

- A working 7-page Streamlit application with 229 passing tests
- Complete document intelligence pipeline from load → extract → summarise → brief → Q&A
- Downloadable Markdown outputs for three page types (brief, risk summary, Q&A)
- Transparent, auditable deterministic logic throughout
- Responsible-use warnings, limitations disclosures, and owner suggestions on all generated outputs
- Ready for portfolio presentation, client demonstration, and LinkedIn case study

---

## Business or User Value

- A consultant can review four policy documents in under 5 minutes and download a structured brief
- A governance lead can see at a glance which topics have policy evidence and which have gaps
- A developer can see a working document intelligence foundation before adding embeddings or AI
- A client can see that document AI can be implemented transparently and safely before any model is called

---

## Risk and Governance Considerations

| Risk | Mitigation |
|---|---|
| Real sensitive data entered into the tool | Responsible-use warnings on every page; safety-boundaries.md |
| Outputs treated as authoritative without review | Limitations and caveats included in all generated outputs |
| Reliance on incomplete keyword coverage | "How to interpret" expanders explaining keyword-based limitations |
| Tool used for live safeguarding decisions | Explicit warning that tool is not safeguarding or legal advice |

---

## Limitations

- Keyword-based matching only — no semantic search
- 13 supported topics — documents using different terminology may not match
- No document upload — documents placed manually in `data/synthetic_documents/`
- No embeddings or vector store
- No session persistence — data lost on app restart
- Designed for synthetic documents only
- Not validated against real organisational policy documents

---

## Lessons Learned

1. **Build the pipeline before adding AI.** A deterministic keyword pipeline is faster to build, easier to test, and easier to explain to clients than a generative AI pipeline. It also provides a baseline for comparing AI-augmented results.

2. **Session state pre-fill pattern is powerful in Streamlit.** Setting session state from a button and calling `st.rerun()` makes suggested queries and presets feel seamless without complex widget state management.

3. **`@st.cache_data` on document loading is essential.** Without it, documents reload on every page interaction, making the app slow.

4. **Deterministic outputs are easier to test.** Template-based answers and keyword mapping are fully testable with pytest. LLM-generated answers would require different test strategies.

5. **Responsible-use boundaries need to be visible, not hidden.** Every page has the safety notice. Every generated output includes limitations text. This normalises responsible use rather than treating it as a disclaimer to bury.

---

## Future Improvements

See [future-improvements.md](future-improvements.md) for the full list. Key next steps:

- Add screenshots for portfolio materials
- Add local embeddings for semantic search
- Add LLM-assisted Q&A with strict evidence grounding and source citation

---

## Portfolio Summary

Build 2 demonstrates:

| Capability | Evidence |
|---|---|
| Python and Streamlit app development | 7-page app, 6 source modules, 229 tests |
| Document intelligence foundations | Load → extract → summarise → brief → Q&A pipeline |
| RAG principles without a vector database | Evidence retrieval, source grounding, limitations disclosure |
| Responsible AI implementation | Safety boundaries, warnings, human review emphasis |
| Testable, auditable logic | pytest, deterministic matching, no black-box outputs |
| Portfolio-ready deliverables | Markdown downloads, demo script, case study, reflection |

This build is suitable for:
- Portfolio inclusion
- GitHub project
- LinkedIn case study
- Client demonstration of document intelligence foundations
- Evidence of AI consulting capability

---

*Build 2 · Document Intelligence / RAG Demo · BrightPath ChatGPT Mastery Project*
*All sample data and documents are synthetic. No real personal, learner, safeguarding, or regulated data is used.*
