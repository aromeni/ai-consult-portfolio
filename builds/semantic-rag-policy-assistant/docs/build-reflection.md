# Build Reflection — Semantic RAG Policy Assistant

**Build 3 · BrightPath ChatGPT Mastery Project**

---

## What Was Built

A complete, locally-run semantic RAG pipeline built across eight phases:

- Synthetic policy document loading and metadata display
- Configurable word-based chunking with overlap
- Local embedding generation using sentence-transformers/all-MiniLM-L6-v2
- FAISS vector index (IndexFlatIP cosine + IndexFlatL2)
- Semantic search with query embedding and ranked FAISS retrieval
- Deterministic grounded RAG Q&A with intent detection and evidence grounding
- Retrieval comparison: keyword vs semantic side-by-side with overlap detection
- Mini Answer Report: 10-section downloadable Markdown report

429 tests. 8 pages. Zero external AI API calls. All runs locally.

---

## Why It Was Built

Three reasons:

1. **Portfolio evidence.** To demonstrate that I can build a complete semantic RAG pipeline — not describe it, not link to a tutorial, but build it, test it, and document it responsibly.

2. **Client conversation tool.** Clients and organisations often ask "should we use semantic search for our policy documents?" This prototype lets me show them the full pipeline, explain the trade-offs, and demonstrate the responsible-use boundaries — before any vendor commitment.

3. **Learning through building.** Reading about FAISS, sentence-transformers, and RAG is different from debugging `search_vector_store`, writing 429 tests, and figuring out why the session state loses the embedding matrix on rerun.

---

## What Worked Well

**Phased building.** Each phase had a clear, testable goal. Testing each layer before building the next meant that when Phase 7 (retrieval comparison) ran for the first time, it worked — because the semantic search and keyword search layers were already solid.

**Fake models in tests.** Using `FakeModel` and `monkeypatch` patterns meant all 429 tests run offline and fast, with no model downloads. Tests verify contracts and logic, not model quality.

**Session state as a data bus.** Treating `st.session_state` as a shared pipeline state — chunks flow to embeddings, embeddings flow to the vector store, the vector store flows to semantic search, and so on — made the multi-page app feel natural and the pipeline feel real.

**Deterministic RAG before generative.** Starting with template-based answers kept the pipeline honest and auditable. Every answer cites retrieved evidence directly. There is no hallucination risk — you can see exactly what the system retrieved and exactly how it generated the answer.

**Responsible-use controls as code.** Writing validation functions (`validate_rag_inputs`, `validate_semantic_search_inputs`), limitation strings included in every output, and caution flags for sensitive topics meant the safety boundaries were enforced by the code, not just stated in documentation.

---

## What Was Difficult

**Two-environment Python setup.** Streamlit runs from the Anaconda Python environment (`/Applications/anaconda3/bin/python`), not from the project `.venv`. Installing sentence-transformers and faiss-cpu into the wrong environment caused confusing import errors that looked like package problems but were actually environment problems. Solution: install into the Anaconda environment.

**FAISS cosine similarity with normalised embeddings.** FAISS IndexFlatIP computes inner product, not cosine similarity directly. Cosine similarity only equals inner product when vectors are unit-normalised. The sentence-transformers model normalises by default, so the results are correct — but this is a subtle point that requires understanding or it produces scores above 1.0 for unnormalised vectors.

**Deterministic RAG answers that feel genuinely grounded.** Template-based answers are easy to write but hard to write well. The challenge was making them feel evidenced (they reference the detected policy topic and remind the user to review the source) without overclaiming precision they don't have.

**Keeping the Streamlit page code readable.** By Phase 8, `app.py` was over 1,300 lines. The pattern of prefixing all local page variables with `_` helped reduce namespace collisions, but the file became dense. A future build should split pages into modules.

---

## Design Decisions

**No external LLM API.** Keeps costs at zero, removes external dependencies, makes the architecture fully inspectable. The trade-off is that answers use deterministic templates rather than generated prose. Accepted — for a prototype, honest templates are more trustworthy than opaque generation.

**FAISS over Chroma, LangChain, or LlamaIndex.** FAISS is explicit and minimal. Every step is visible: index type, search function, result format. This makes the prototype easier to explain and the architecture easier to audit. Higher-level libraries abstract away the details this build is trying to demonstrate.

**sentence-transformers/all-MiniLM-L6-v2.** Widely used, well-documented, 384 dimensions, ~90 MB, no API key, runs on CPU. A pragmatic default that keeps the demo accessible.

**Word-based chunking as default.** Simple, predictable, and easy to explain. Sentence-aware or paragraph-aware chunking would improve retrieval quality but adds complexity and is harder to demonstrate. Phase 2's section-based strategy was included as an experimental option.

**Markdown for all reports.** Markdown is portable, editable, readable in any text editor, and renderable on GitHub. A client can receive a `.md` report, open it in Notion, paste it into a Word document, or version-control it in their own repository. PDF export is on the future improvements list but not required for a prototype.

---

## Safety and Governance Decisions

**Synthetic documents only from the start.** The decision to use only synthetic documents was not a Phase 1 constraint that would be relaxed later — it was a permanent boundary for this prototype. This removed all data protection risk and meant the prototype could be shared, demoed, and open-sourced without concern.

**Visible responsible-use warnings on every generation page.** Each page that produces an output (semantic search, RAG Q&A, retrieval comparison, mini answer report) shows a `st.warning` banner with the responsible-use boundary. This is visible to any user who navigates to the page, not hidden in a footer.

**Limitations included in every output dict and every download.** Every function that produces a report or answer includes a `limitations` key in its output. Every downloadable file includes a Limitations section. There is no output that does not acknowledge what it cannot do.

**Caution flags for sensitive topics.** The RAG engine detects questions about learner data, safeguarding, and data incidents and flags them with an explicit caution note. This is a simple but important signal that some topics need extra human care.

---

## Technical Decisions

**All tests use fake/mock data.** `FakeModel` returns fake numpy arrays. `monkeypatch` replaces `semantic_search` in comparison tests. This means tests are fast, reproducible, and run offline. The trade-off is that integration quality (does the real model produce good results?) is assessed manually, not in CI.

**`pytest.importorskip("faiss")` in FAISS-dependent tests.** Allows test files to skip gracefully if faiss-cpu is not installed. This is important for environments where faiss may not be available (e.g. CI pipelines without C++ extensions).

**Session state variables use consistent naming conventions.** `last_rag_question`, `last_rag_response`, `last_rag_evidence`, `last_retrieval_comparison`, etc. Each stage of the pipeline writes to named session state keys that downstream pages consume. This makes the data flow explicit and debuggable.

---

## What This Proves

- I can design and implement a multi-phase RAG pipeline from scratch
- I understand each layer of the RAG architecture and can explain the trade-offs
- I can use local sentence-transformers and FAISS without external dependencies
- I can write a test suite that verifies contracts without requiring model downloads
- I can build responsible AI controls into code — not just documentation
- I can deliver a portfolio-ready prototype that is honest about what it does and does not do

---

## What It Does Not Prove

- **Production readiness.** This is a prototype. It has no authentication, no audit logging, no persistent storage, and no access control.
- **Accuracy on real documents.** The prototype was only evaluated on synthetic documents.
- **LLM-quality answers.** Template-based answers are grounded but not fluent prose.
- **Client validation.** No paying client has used or validated this tool.
- **Safe handling of real sensitive data.** It has not been tested with real learner data, safeguarding information, or confidential client records — and it must not be, until appropriate governance is in place.

---

## Lessons Learned

1. **Test the contracts, not the model.** Fake data in tests is not a shortcut — it's a correct separation of concerns. Unit tests verify logic. Manual evaluation assesses quality.
2. **Responsible AI controls should be enforced by code.** A warning in documentation is not a control. A validation function that returns `(False, "message")` is.
3. **Phased building produces better software than planning everything upfront.** The retrieval comparison and mini answer report emerged from what was built in earlier phases — their design was informed by what the pipeline actually produced.
4. **Local-only prototypes are easier to trust.** When everything runs locally, you can inspect every intermediate state, step through the pipeline, and understand what happened. Cloud abstractions make this harder.
5. **Honest limitations build more trust than vague capability claims.** Clients and colleagues respond better to "this is a prototype that does X but does not yet do Y" than to "this demonstrates AI-powered policy analysis."

---

## Next Build Improvements

- **Split `app.py` into page modules** — by Phase 9, `app.py` exceeded 1,300 lines. A next build should use Streamlit multi-page app structure or page modules.
- **Add integration tests** — test the full pipeline end-to-end with a small, known document set and known expected retrievals.
- **Add evaluation metrics** — measure retrieval precision and recall for a small set of known test questions.
- **Add PDF export** — the Markdown report is good; a PDF would be more portable for client handoffs.
- **Add document upload for synthetic/approved files** — the current manual file placement is a friction point in demos.

---

*Build 3 · Semantic RAG Policy Assistant · BrightPath ChatGPT Mastery Project*
