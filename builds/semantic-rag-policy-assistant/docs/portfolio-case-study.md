# Semantic RAG Policy Assistant — Portfolio Case Study

**Build 3 · BrightPath ChatGPT Mastery Project**

---

## One-Line Summary

A locally-run semantic RAG prototype that chunks synthetic policy documents, generates embeddings, builds a FAISS vector index, retrieves evidence by meaning rather than exact keywords, generates grounded answers, and produces a downloadable Markdown report — without external AI API calls.

---

## Problem

Organisations considering semantic AI search for their internal policy documents face a practical evaluation gap:

- They cannot trial a full RAG system without significant vendor commitment or technical investment
- They need to understand the chunking, embedding, retrieval, and answer generation pipeline before choosing an architecture
- They need grounded, auditable answers — not black-box generation with no visible evidence trail
- They need to compare keyword retrieval against semantic retrieval to decide whether the cost of semantic search is justified
- They need to understand the responsible-use boundaries before scaling up to sensitive real documents

This build provides a transparent, locally-run prototype that demonstrates the full RAG pipeline safely and clearly.

---

## Target User

**Primary:** Rashid (AI consultant) — demonstrating semantic RAG concepts, architecture, and responsible-use principles to clients and prospective collaborators.

**Secondary:** Developers learning local RAG architecture phase by phase, with a clear test suite and documented design decisions.

**Tertiary:** Governance leads, managers, and clients who want to understand what semantic RAG is before committing to a vendor or production implementation.

---

## Workflow Context

This build sits in the AI consulting workflow after initial diagnostic (Build 1) and keyword-based document intelligence (Build 2). It demonstrates the next step: upgrading from deterministic keyword retrieval to neural similarity-based retrieval, while keeping the same responsible-use controls.

Workflow position:

> Client AI Audit → Document Intelligence → **Semantic RAG Prototype** → Staff Training → (Future: production deployment)

---

## Goals

1. Demonstrate the complete RAG pipeline in a locally-run, auditable prototype
2. Show that semantic retrieval finds relevant policy chunks that keyword search misses
3. Show grounded answer generation with visible evidence sources
4. Compare keyword and semantic retrieval side-by-side for client demonstrations
5. Generate a structured, reviewable Markdown report that a client can download and review
6. Build responsibly: no external AI APIs, no real sensitive data, human review required

---

## Success Criteria

- All 8 app pages are functional end-to-end
- Query → semantic search → grounded answer pipeline works locally without internet connection after initial model download
- Side-by-side retrieval comparison shows keyword and semantic differences clearly
- Downloadable Mini Answer Report includes question, answer, evidence, comparison, and limitations
- 429 tests pass
- No external LLM API calls at any point in the pipeline
- Safety boundaries are visible on every retrieval and generation page

---

## Solution Overview

Eight-phase Streamlit prototype:

1. Load synthetic policy documents
2. Explore configurable word-based chunking
3. Generate local embeddings using sentence-transformers/all-MiniLM-L6-v2
4. Build a FAISS cosine similarity vector index
5. Perform semantic search — retrieve most similar chunks for any query
6. Generate a deterministic grounded answer from retrieved evidence
7. Compare keyword and semantic retrieval for the same query
8. Download a full 10-section Markdown answer report

---

## Key Features

- **Chunking Explorer** — configurable chunk size and overlap; visual chunk cards; per-chunk word count and source range
- **Local embedding generation** — sentence-transformers; no API key; cached model; 384-dimensional vectors
- **FAISS vector index** — IndexFlatIP (cosine) and IndexFlatL2; in-memory; save/load support
- **Semantic search** — query embedding + FAISS nearest-neighbour search; ranked results with source labels
- **Deterministic RAG Q&A** — 13 policy topic categories; 8 question types; template-based answers; caution flag for sensitive topics; evidence cards
- **Retrieval comparison** — side-by-side keyword and semantic results; overlap detection; deterministic comparison insight
- **Mini Answer Report** — 10 sections; reviewer notes; caution notes; responsible-use limitations; download as Markdown

---

## Architecture

```
Documents (Markdown) →
  Chunker (word-based, configurable overlap) →
  Embedding Engine (sentence-transformers, local) →
  FAISS Vector Store (IndexFlatIP, in-memory) →
  Semantic Search (query embed + FAISS search) →
  RAG Engine (intent detection + template answer) →
  Retrieval Comparison (keyword vs semantic, overlap) →
  Report Generator (10-section Markdown)
```

Session state carries pipeline outputs forward so each page can consume results from previous pages.

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Language | Python 3.11 |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Index | FAISS (faiss-cpu) |
| Keyword Search | Custom token matching, stop-word filtered |
| RAG Logic | Deterministic template-based (no LLM) |
| Testing | pytest (429 tests) |
| Document Format | Markdown (.md) |
| External APIs | None |
| Database | None |

---

## Data / Documents / Inputs

All documents used in this prototype are synthetic Markdown policy documents. They are fictional, clearly labelled "Synthetic — for demonstration purposes only," and contain no real learner, safeguarding, confidential, staff HR, personal, or regulated data.

The four synthetic documents cover:

- AI acceptable use policy
- Data protection guidance for AI
- Safeguarding and AI boundaries
- Staff AI training notes

No real organisational data was used at any stage of this build.

---

## AI / Model / API Approach

This prototype uses local embeddings with `sentence-transformers/all-MiniLM-L6-v2` and FAISS vector search for retrieval. It does not use external LLM APIs, OpenAI, Anthropic, Google, or any cloud AI service. RAG answers are generated using deterministic intent-detection and template-based logic over retrieved evidence — not LLM-generated prose.

This choice was deliberate: it demonstrates the architecture clearly, keeps costs at zero, removes external dependencies, and ensures the prototype can be inspected and audited at every step.

---

## Implementation Process

The build was implemented in nine phases:

| Phase | Deliverable |
|---|---|
| 1 | Project scaffold, document loader, chunker, keyword search, app scaffold, test infrastructure |
| 2 | Improved chunking with validation, summary, section strategy, and Chunking Explorer |
| 3 | Local embedding generation using sentence-transformers; embedding summary; session state |
| 4 | FAISS vector index (IndexFlatIP + IndexFlatL2); in-memory; save/load; 35 tests |
| 5 | Semantic search; query embedding; ranked results with source labels; 50 tests |
| 6 | Deterministic RAG Q&A; intent detection; template answers; evidence summary; 66 tests |
| 7 | Retrieval comparison; overlap detection; comparison insight; Markdown download; 47 tests |
| 8 | Mini Answer Report; 10-section Markdown; reviewer notes; build_report_data; 55 tests |
| 9 | Completion review and portfolio documentation |

Each phase was test-driven: tests were written alongside implementation. All 429 tests run offline using fake/mock data.

---

## Testing and Validation

- **429 tests** covering document loading, chunking, embedding, vector index, semantic search, RAG engine, retrieval comparison, and report generation
- All tests run without internet access, model downloads, or external services (FakeModel / monkeypatch patterns used throughout)
- Tests verify function contracts, edge cases, safety fallbacks, and output structure
- End-to-end pipeline tested manually using the Streamlit UI with synthetic documents

---

## Demo Notes

Run the app with:

```bash
streamlit run app.py
```

Navigate through all 8 pages in order. Use the suggested query:

> "Can staff put learner names into ChatGPT?"

Expected outputs:

- **Semantic Search:** top-ranked chunks from the AI acceptable use policy and data protection guidance
- **RAG Q&A:** grounded answer with caution flag (learner data topic); evidence cards; download button
- **Retrieval Comparison:** keyword and semantic results side-by-side; overlap; comparison insight
- **Mini Answer Report:** full 10-section Markdown report; download as `.md`

---

## Results

- Complete 8-phase RAG pipeline built and functional
- All 8 app pages operational end-to-end
- 429 tests passing
- Zero external AI API calls at any point
- Responsible-use controls visible at every page
- Downloadable Markdown report with structured evidence, comparison, and reviewer notes

---

## Business and User Value

| Stakeholder | Value |
|---|---|
| Clients (training providers, schools, SMEs) | See how semantic RAG could work for their policy documents before committing to a vendor |
| Governance leads | Understand what the pipeline does and where human review is needed |
| AI consultants | Demonstrate a full production-style RAG architecture without external dependencies |
| Developers | A clear, phase-by-phase codebase showing how each layer of a RAG system works |

---

## Risk and Governance Considerations

- This prototype uses synthetic documents only — zero data protection risk in its current form
- Production use with real documents would require DPIA, legal review, authentication, audit logging, secure storage, and responsible-owner approval
- All outputs include explicit limitations and responsible-use notices
- Human review is required before acting on any output — stated clearly at every relevant point

---

## Limitations

- Answers use deterministic templates, not LLM-generated prose
- Retrieval is cosine similarity only — no hybrid ranking, reranking, or BM25
- No document upload — documents must be added manually to `data/synthetic_documents/`
- No persistent session storage — state resets on app restart
- No authentication — single-user, local only
- Tested only on synthetic documents — accuracy on real organisational documents is unknown
- Not benchmarked against any retrieval evaluation dataset

---

## Lessons Learned

1. **Phased builds work well.** Testing each layer before building the next kept quality high and made debugging easy.
2. **Local-only constraints are liberating.** No API keys, no rate limits, no costs, no external dependencies — the prototype is fully self-contained and inspectable.
3. **Deterministic over generative for prototyping.** Template-based answers are honest about what the system knows — they cite retrieved evidence directly without the risk of hallucination.
4. **Responsible-use controls should be code, not comments.** Validation functions, limitation strings, and visible warnings are more reliable than policy statements in documentation.
5. **Session state is the RAG pipeline.** Treating `st.session_state` as a shared data bus across pages made the multi-phase pipeline feel natural.

---

## Future Improvements

Short-term: PDF export for reports, demo presets, persistent local FAISS index.

Medium-term: document upload for synthetic/approved files, section-aware chunking, metadata filtering, retrieval evaluation, persistent local indexes.

Long-term: LLM-assisted grounded answers (Ollama), hybrid retrieval, reranking, secure deployment, authentication, audit logging, DPIA-compliant production architecture.

See [future-improvements.md](future-improvements.md) for the full roadmap.

---

## Portfolio Summary

**What this demonstrates for clients and employers:**

- Rashid understands semantic RAG architecture end-to-end
- Rashid can build it from scratch, phase by phase, with tests
- Rashid can implement responsible AI controls as working software
- Rashid can explain the trade-offs between keyword and semantic retrieval clearly
- Rashid can deliver a production-style, portfolio-ready prototype without external dependencies
- Rashid positions outputs honestly — evidence support, not final authority

**This is a production-style prototype, not a production system.** It is designed to demonstrate architecture, methodology, and responsible AI practice — and to serve as a foundation for production builds when appropriate governance is in place.

---

*Build 3 · Semantic RAG Policy Assistant · BrightPath ChatGPT Mastery Project*
*All documents are synthetic. Outputs are indicative only and require human review.*
