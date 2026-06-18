# Build Notes — Semantic RAG Policy Assistant

**Build:** 3 of the ChatGPT Mastery / GPT Master Project
**Status:** UI polish complete. Production-style portfolio-ready RAG prototype.
**Version:** Prototype v0.9 (UI polish pass)
**Date:** June 2026

---

## Phase Log

| Phase | Name | Status | Notes |
|---|---|---|---|
| 1 | Scaffold and Architecture | Complete | Document loading, chunking, keyword search, app scaffold, tests |
| 2 | Improved Chunking and Chunking Explorer | Complete | Validation, summary, section strategy, session state, 60 tests |
| 3 | Local Embeddings | Complete | sentence-transformers/all-MiniLM-L6-v2, embed_chunks, session state, 51 tests |
| 4 | FAISS Vector Index | Complete | IndexFlatIP (cosine) + IndexFlatL2, save/load, 35 tests |
| 5 | Semantic Search | Complete | Query embedding, FAISS retrieval, ranked results, session state |
| 6 | RAG Q&A | Complete | Deterministic grounded answers, intent detection, evidence summary, Markdown download |
| 7 | Retrieval Comparison | Complete | Keyword vs semantic side-by-side, overlap detection, comparison insight, Markdown download |
| 8 | Mini Answer Report | Complete | Full 10-section Markdown report, RAG Q&A output, retrieved evidence, comparison section, download |
| 9 | Completion Review and Portfolio Notes | Complete | Completion review, portfolio case study, demo script, screenshots checklist, build reflection, deployment notes |
| — | UI Polish Pass | Complete | `/frontend-design` skill applied — expanded CSS, new helper functions, polished cards, phase grid, answer cards, result cards, index status bars, pipeline step indicators, comparison column headers |
| — | Polish Step 2 — Screenshot Structure | Complete | `assets/screenshots/` created; `assets/screenshots/README.md` with safety requirements and expected filenames; `docs/screenshots-checklist.md` rewritten with practical table; `README.md` Screenshots section added |

---

## Phase 1 Notes

**What was built:**
- Full folder structure and Python package layout
- `src/document_loader.py` — list, load, load all, metadata
- `src/chunker.py` — word-based chunking with overlap across single or all documents
- `src/keyword_search.py` — tokenise query, stop-word filter, score chunks by matched term count
- `src/report_generator.py` — Markdown report scaffold with question/answer/sources/limitations
- `src/ui_components.py` — inject_css, render_page_header, render_safety_warning, render_prototype_notice, render_placeholder, render_chunk_card, render_search_result, render_workflow_diagram, render_boundary_notice
- `src/sample_data.py` — DOCS_DIR, DEMO_QUERIES, PLANNED_PHASES
- Placeholder stubs with NotImplementedError for: embedding_engine, vector_store, semantic_search, rag_engine, comparison
- `app.py` — 8-page Streamlit app with full navigation
- `tests/` — 5 test files (test_document_loader, test_chunker, test_keyword_search, test_report_generator, test_rag_engine)
- 4 synthetic policy documents copied from Build 2
- Full documentation (README, architecture, safety-boundaries, demo-script, future-improvements)

**What is functional in Phase 1:**
- Home page: workflow diagram, phase status, live metrics (documents, words, chunks)
- Document Library: metadata table, full document preview
- Chunking Explorer: fully functional — select document/all, set chunk_size and overlap, view as cards or table
- Semantic Search: keyword search preview (Phase 4 placeholder for semantic)
- RAG Q&A: keyword search preview with suggested questions (Phase 5 placeholder for grounded answers)
- Mini Answer Report: sample report scaffold with download (Phase 5 placeholder for grounded reports)

**What is intentionally placeholder:**
- Embedding Index Builder (Phase 3)
- Semantic Search — semantic retrieval layer (Phase 4)
- RAG Q&A — grounded answer generation (Phase 5)
- Retrieval Comparison — keyword vs semantic (Phase 5)
- Mini Answer Report — post-RAG grounded report (Phase 5)

**Tests:** All passing. See `pytest` output.

---

## Phase 2 Notes

**What was improved:**

- `src/chunker.py` — fully rewritten with:
  - `split_text_into_words(text)` — explicit word splitter
  - `validate_chunk_settings(chunk_size, overlap)` — returns `(bool, message)` with clear error messages
  - `estimate_chunk_count(word_count, chunk_size, overlap)` — exact estimate using the same sliding-window logic as `chunk_text`
  - `chunk_text(text, chunk_size, overlap, document_name, strategy)` — extended signature; each chunk now includes `start_word`, `end_word`, `chunk_size`, `overlap`, `strategy`
  - `chunk_documents(documents, chunk_size, overlap, strategy)` — passes all settings through to `chunk_text`
  - `get_chunking_summary(chunks)` — returns `total_chunks`, `total_documents`, `total_words`, `average_chunk_words`, `min_chunk_words`, `max_chunk_words`, `average_chunk_characters`
  - `_word_chunks` — internal sliding-window implementation
  - `_section_chunks` — experimental: splits on `## ` Markdown headings, word-chunks each section, falls back to word chunking if < 2 headings found

- `tests/test_chunker.py` — 60 tests covering all new functions

- `app.py` — Chunking Explorer page redesigned:
  - Default chunk size: 120 words, overlap: 30 words (appropriate for short synthetic docs)
  - Strategy selector: word / section (experimental)
  - Inline validation message
  - Estimated chunk count shown before generating
  - "Generate Chunks" button stores result in `st.session_state["chunks"]`, `["chunking_summary"]`, `["chunking_settings"]`
  - Metric cards: documents processed, total chunks, average chunk size, overlap, strategy
  - Full chunk table: chunk_id, document_name, chunk_index, word_count, character_count, start_word, end_word
  - Expandable chunk inspector: full text, chunk_id, word range, strategy, settings
  - "Why chunking matters in RAG" explanation panel

- `app.py` — Document Library now includes a notice about chunking being required before embeddings

- Sidebar caption updated to Phase 2
- Home page metric updated to Phase 2 / 5

**What is intentionally placeholder:**
- Embedding Index Builder (Phase 3)
- Semantic Search (Phase 4)
- RAG Q&A (Phase 5)
- Retrieval Comparison (Phase 5)
- Full Mini Answer Report (Phase 5)

**Tests:** 60/60 chunker tests passing. Full suite: run `pytest`.

---

## Phase 3 Notes

**What was implemented:**

- `requirements.txt` — added `sentence-transformers`
- `src/embedding_engine.py` — full implementation replacing the Phase 1 stub:
  - `get_default_embedding_model_name()` → `"sentence-transformers/all-MiniLM-L6-v2"`
  - `load_embedding_model(model_name)` — lazy-imports `SentenceTransformer` to avoid import errors if not installed; gives clear message if missing
  - `validate_chunks_for_embedding(chunks)` → `(bool, message)` — checks non-empty chunks and non-empty text
  - `embed_texts(texts, model, model_name, normalise)` → dict with `model_name`, `embedding_dimension`, `embeddings` (ndarray), `text_count`, `normalised`; handles empty list safely
  - `embed_chunks(chunks, model, model_name, normalise)` → dict with `model_name`, `embedding_dimension`, `embedded_chunks`, `embedding_matrix`, `chunk_count`, `normalised`; each embedded chunk preserves all metadata and adds `embedding_index` and `embedding_vector` (list for serialisability)
  - `get_embedding_summary(embedded_chunks, model_name, embedding_dimension, normalised)` → aggregate stats dict

- `tests/test_embedding_engine.py` — 51 tests, all using `FakeEmbeddingModel` (no internet access needed)

- `app.py` — Embedding Index Builder page fully implemented:
  - "What are embeddings?" explainer (collapsible)
  - Chunk availability check — redirects to Chunking Explorer if no chunks in session state
  - Model name input (default: all-MiniLM-L6-v2)
  - Performance note about first-run model download
  - "Generate Embeddings" button with error handling
  - `@st.cache_resource` caches the model across Streamlit reruns
  - Stores `embedding_model_name`, `embedded_chunks`, `embedding_matrix`, `embedding_summary` in session state
  - Shows 5 metric cards: model, chunks, dimensions, documents, normalised
  - Word stats table
  - Embedding preview table: first 8 vector values rounded to 4 d.p.

**What is intentionally placeholder:**
- Semantic Search (Phase 5)
- Retrieval Comparison (Phase 5)
- RAG Q&A (Phase 5)
- Full Mini Answer Report (Phase 5)

**Tests:** 51/51 embedding tests passing. Full suite: run `pytest`.

---

## Phase 4 Notes

**What was implemented:**

- `requirements.txt` — added `faiss-cpu`
- `src/vector_store.py` — full implementation replacing the Phase 1 stub:
  - `validate_embedding_matrix(embedding_matrix, embedded_chunks)` → `(bool, message)` — 6 validation checks including shape, dimension, dtype, and count mismatch
  - `build_faiss_index(embedding_matrix, metric)` — builds IndexFlatIP (cosine) or IndexFlatL2; lazy-imports FAISS with readable error if not installed
  - `create_vector_store(embedded_chunks, embedding_matrix, metric)` → dict with `index`, `embedded_chunks`, `embedding_matrix`, `metric`, `dimension`, `chunk_count`, `document_count`, `index_type`
  - `search_vector_store(vector_store, query_embedding, top_k)` → list of ranked result dicts; handles top_k > chunk_count safely; does not mutate original chunks
  - `get_vector_store_summary(vector_store)` → aggregate stats dict; safe defaults for empty input
  - `save_faiss_index(index, path)` and `load_faiss_index(path)` — disk persistence via `faiss.write_index` / `faiss.read_index`

- `tests/test_vector_store.py` — 35 tests, all using fake numpy arrays (no model downloads):
  - `TestValidateEmbeddingMatrix` — 10 tests
  - `TestBuildFaissIndex` — 8 tests
  - `TestCreateVectorStore` — 11 tests (includes `TestGetVectorStoreSummary` and index assertions)
  - `TestSearchVectorStore` — 14 tests
  - `TestSaveLoadFaissIndex` — 3 tests

- `app.py` — Embedding Index Builder page redesigned as a two-step flow:
  - Step 1: Generate Embeddings — same as Phase 3 but collapsed into a success summary with "Embedding details" expander once done; "Re-generate" button clears downstream state
  - Step 2: Build FAISS Index — metric selector (cosine / l2, default cosine), "Build FAISS Index" button, error handling for ImportError and general exceptions
  - Stores `vector_store`, `vector_store_summary`, `vector_metric` in session state
  - Shows 5 metric cards: index type, metric, vectors indexed, embedding dimension, documents indexed
  - Shows vector store summary table and documents-indexed caption
  - Added "What is a FAISS vector index?" expander
  - Added visible responsible-use warning

- Home page updated: Phase 3 and 4 shown as `st.success` (live); Phase 5 placeholder remains; metric card updated to "4 / 5"
- Sidebar caption updated to "Phase 4 — Chunking · Embeddings · FAISS Index"

**What is intentionally placeholder:**
- Semantic Search (Phase 5)
- Retrieval Comparison (Phase 5)
- RAG Q&A (Phase 5)
- Full Mini Answer Report (Phase 5)

**Tests:** 35/35 vector store tests passing. Full suite: run `pytest`.

---

## Phase 5 Notes

**What was implemented:**

- `src/semantic_search.py` — full implementation replacing the Phase 1 stub:
  - `validate_semantic_search_inputs(query, vector_store)` → `(bool, message)` — checks empty query, missing/unready vector store
  - `embed_query(query, model, model_name, normalise)` → dict with `query`, `model_name`, `embedding` (shape 1×dim), `embedding_dimension`, `normalised`; raises `ValueError` on empty query
  - `format_semantic_search_results(results)` → adds `source_label` and `preview_text` to each result dict; does not mutate originals
  - `semantic_search(query, vector_store, model, model_name, top_k, normalise)` → dict with `query`, `model_name`, `top_k`, `results`, `result_count`, `query_embedding_dimension`, `metric`, `limitations`

- `tests/test_semantic_search.py` — new file with 50 tests across 4 classes, all using FakeModel and fake numpy arrays:
  - `TestValidateSemanticSearchInputs` — 10 tests
  - `TestEmbedQuery` — 15 tests
  - `TestFormatSemanticSearchResults` — 11 tests
  - `TestSemanticSearch` — 14 tests

- `app.py` — Semantic Search page made fully functional:
  - Pipeline check: clear 4-step instructions if vector store is not built
  - Index status summary: vectors, dimensions, index type, model
  - 7 suggested demo queries (clickable buttons)
  - Natural language query input with `st.session_state` key for two-way binding
  - Top-k slider (1–10, default 5)
  - Search button embeds query and searches FAISS index
  - Result cards: rank, score, document, chunk index, word count, chunk text, source label
  - Responsible-use limitations expander
  - Prototype notice
  - Session state: `last_semantic_query`, `last_semantic_results`, `last_semantic_search_summary`
  - "What does semantic search do?" explainer expander
  - Responsible-use warning banner

- Home page updated: Phase 5 Semantic Search shown as `st.success`; "RAG Q&A — Coming Next" placeholder; metric card updated to "5 / 5"
- Sidebar caption updated to "Phase 5 — Chunking · Embeddings · FAISS · Semantic Search"

**What is intentionally placeholder:**
- RAG Q&A — grounded answers with source citations (coming next)
- Retrieval Comparison — keyword vs semantic side by side (coming next)
- Full Mini Answer Report — post-RAG grounded report (coming next)

**Tests:** 50/50 semantic search tests passing. Full suite: run `pytest`.

---

## Phase 6 Notes

**What was implemented:**

- `src/rag_engine.py` — full implementation replacing the Phase 1 stub:
  - `validate_rag_inputs(question, vector_store)` → `(bool, message)` — 4 checks including empty question, missing index, no embedded chunks
  - `detect_question_intent(question)` → dict with `detected_topics`, `question_type`, `needs_caution`, `caution_reason`; deterministic keyword matching over 13 policy topic categories
  - `generate_grounded_answer(question, retrieved_chunks, intent)` → template-selected answer string; `_NO_CHUNKS_ANSWER` when no chunks retrieved
  - `generate_evidence_summary(retrieved_chunks, max_items)` → list of evidence dicts with rank, score, document_name, chunk_id, chunk_index, evidence_text, source_label
  - `get_rag_limitations()` → 7 responsible-use limitation strings
  - `generate_rag_response(question, vector_store, model, model_name, top_k)` → full RAG pipeline dict
  - `generate_rag_markdown(rag_response)` → Markdown string with Question, Short Answer, Detected Topics, Question Type, Retrieved Evidence, Caution Notes, Limitations sections

- `tests/test_rag_engine.py` — fully rewritten with 66 tests across 7 classes:
  - `TestValidateRagInputs` — 8 tests
  - `TestDetectQuestionIntent` — 18 tests
  - `TestGenerateGroundedAnswer` — 8 tests
  - `TestGenerateEvidenceSummary` — 7 tests
  - `TestGetRagLimitations` — 5 tests
  - `TestGenerateRagMarkdown` — 11 tests
  - `TestGenerateRagResponse` — 9 tests (using `monkeypatch` to avoid model downloads)

- `app.py` — RAG Q&A page made fully functional:
  - Pipeline check: 4-step instructions if vector store not built
  - "What is RAG Q&A?" expander
  - Responsible-use warning
  - 8 suggested demo questions
  - Question input with session state key for two-way button binding
  - Top-k slider (1–10, default 5)
  - "Generate Answer" button runs full RAG pipeline
  - Answer card in `st.info` block
  - Caution box shown if `needs_caution` is True
  - 4 metric cards: question type, detected topics, chunks retrieved, metric/model
  - Evidence cards: rank, score, document, chunk ID, evidence text
  - Responsible-use limitations expander
  - Markdown download button
  - Session state: `last_rag_question`, `last_rag_response`, `last_rag_answer`, `last_rag_evidence`
  - Prototype notice

- Home page updated: Phase 6 RAG Q&A shown as `st.success`; "Retrieval Comparison and Mini Answer Report — Coming Next" placeholder; metric updated to "6"
- Sidebar caption updated to "Phase 6 — Chunking · Embeddings · FAISS · Semantic Search · RAG Q&A"

**Intent detection topic categories:**
learner data, safeguarding, human review, approved tools, accountability,
bias, hallucination, copyright, escalation, data minimisation, anonymisation,
retention, incident reporting.

**Question types (priority order):**
safeguarding, data_protection, output_quality, approved_use, accountability,
incident_response, general_policy, unknown.

**What is intentionally placeholder:**
- Full Mini Answer Report — grounded post-RAG report with full download (coming next)

**Tests:** 66/66 RAG engine tests passing. Full suite: `348 passed`.

---

## Phase 7 Notes

**What was implemented:**

- `src/comparison.py` — full implementation replacing the Phase 1 stub:
  - `summarise_keyword_results(keyword_results)` → aggregate dict with result_count, documents_found, unique_documents, top_score, matched_terms, method_note
  - `summarise_semantic_results(semantic_results)` → aggregate dict with result_count, documents_found, unique_documents, top_score, method_note
  - `find_overlap_between_results(keyword_results, semantic_results)` → list of overlap dicts matched by chunk_id; each item includes chunk_id, document_name, keyword_rank, semantic_rank
  - `generate_retrieval_comparison_insight(query, keyword_summary, semantic_summary, overlap)` → deterministic one-paragraph explanation covering 5 cases
  - `generate_retrieval_comparison_markdown(comparison_result)` → Markdown download string with 8 sections
  - `compare_retrieval_methods(query, chunks, vector_store, model, model_name, top_k)` → full pipeline dict

- `tests/test_comparison.py` — new file with 44 tests across 6 classes:
  - `TestSummariseKeywordResults` — 8 tests
  - `TestSummariseSemanticResults` — 8 tests
  - `TestFindOverlapBetweenResults` — 6 tests
  - `TestGenerateRetrievalComparisonInsight` — 5 tests
  - `TestGenerateRetrievalComparisonMarkdown` — 10 tests
  - `TestCompareRetrievalMethods` — 9 tests (using `monkeypatch` to avoid model downloads)

- `app.py` — Retrieval Comparison page made fully functional:
  - Pipeline check: 4-step instructions if chunks or vector store not built
  - "What is retrieval comparison?" expander
  - Responsible-use warning
  - 7 suggested comparison queries
  - Query input with session state key for two-way button binding
  - Top-k slider (1–10, default 5)
  - "Compare Retrieval Methods" button runs full comparison pipeline
  - 5 metric cards: keyword results, semantic results, overlapping, keyword docs, semantic docs
  - Comparison insight in `st.info` block
  - Side-by-side keyword and semantic result expanders
  - Overlap table (or info message if no overlap)
  - Interpretation expander
  - Limitations expander
  - Markdown download button
  - Session state: `last_comparison_query`, `last_retrieval_comparison`, `last_keyword_results`, `last_semantic_results`
  - Prototype notice

- Home page updated: Phase 7 Retrieval Comparison shown as `st.success`; "Mini Answer Report — Coming Next" placeholder; metric updated to "7"
- Sidebar caption updated to "Phase 7 — ... · Retrieval Comparison"

**Comparison insight cases:**
1. Semantic only (keyword=0, semantic>0) → semantic found what keyword missed
2. Both with overlap → both methods agree on evidence
3. Both without overlap → different evidence; review both sets
4. Neither returns results → try rephrasing
5. Keyword only (keyword>0, semantic=0) → keyword found matches; consider rebuilding index

**Tests:** 44/44 comparison tests passing. Full suite: `392 passed`.

---

## Phase 8 Notes

**What was implemented:**

- `src/report_generator.py` — fully rewritten:
  - `create_report_filename(title)` — unchanged from Phase 1; safe lowercase slug
  - `get_default_report_limitations()` → 4 responsible-use limitation strings
  - `format_detected_topics(topics)` → comma-separated string; fallback for empty list
  - `format_evidence_items(evidence_items, max_items)` → Markdown evidence block with document, chunk ID, score, text
  - `format_limitations(limitations)` → Markdown bullet list; falls back to defaults if empty
  - `format_retrieval_comparison_section(comparison_result)` → comparison summary Markdown; placeholder if missing
  - `build_report_data_from_session_state(session_state)` → assembles all report fields from session state with safe defaults
  - `generate_markdown_answer_report(report_data)` → full 10-section Markdown report
  - Backward compatible: accepts old `sources` and `retrieval_method` keys from Phase 1

- `tests/test_report_generator.py` — fully rewritten with 55 tests:
  - `create_report_filename` — 9 tests (unchanged)
  - `get_default_report_limitations` — 3 tests
  - `format_detected_topics` — 4 tests
  - `format_evidence_items` — 5 tests
  - `format_limitations` — 4 tests
  - `format_retrieval_comparison_section` — 5 tests
  - `build_report_data_from_session_state` — 6 tests
  - `generate_markdown_answer_report` — 19 tests

- `app.py` — Mini Answer Report page made fully functional:
  - Pipeline check: 5-step setup instructions if no RAG response in session state
  - Summary metrics: question ready, evidence count, topics, comparison available
  - Question/answer preview expander
  - Report settings: title input, include comparison checkbox, max evidence slider, reviewer notes text area
  - "Generate Report" button builds and renders the full 10-section report
  - Report preview expander
  - Download button (.md)
  - Limitations expander
  - Session state: `last_answer_report_markdown`, `last_answer_report_data`, `last_answer_report_filename`
  - Prototype notice

- Home page updated: Phase 8 Mini Answer Report shown as `st.success`; metric updated to "8"
- Sidebar caption updated to include "· Report"

**Report sections (10 sections):**
1. Question
2. Short Grounded Answer
3. Detected Topics and Question Type
4. Retrieval Setup
5. Retrieved Evidence
6. Retrieval Comparison Summary
7. Caution Notes
8. Limitations and Responsible Use
9. Reviewer Notes
10. Prototype Status

**What is intentionally not included:**
- PDF export — planned as a future improvement
- Real document upload — not added per safety constraints
- Authentication or persistent storage

**Tests:** 55/55 report generator tests passing. Full suite: 429 passed.

---

## Phase 9 Notes

**What was created:**

- `README.md` — fully rewritten as a presentation-ready project page covering all 8 phases, all app pages, demo scenario, technical stack, safety boundaries, setup, testing, planned phases, limitations, and portfolio positioning
- `docs/build-3-completion-review.md` — formal completion review: build goal, completed phases, key features, technical implementation, responsible-use boundaries, evidence of completion, what this proves, what it does not prove, readiness verdict, and recommended next actions
- `docs/portfolio-case-study.md` — portfolio case study covering problem, target user, workflow context, goals, solution, architecture, tech stack, data approach, AI/model approach, implementation process, testing, demo notes, results, business value, risks, limitations, lessons learned, and portfolio summary
- `docs/demo-script.md` — full rewrite: 8-step demo flow with what to show, what to say, and key message for each step; demo scenario, setup instructions, responsible-use message, and closing pitch
- `docs/screenshots-checklist.md` — 14-item screenshot checklist with labels, guidance, and portfolio usage notes
- `docs/build-reflection.md` — honest reflection covering what worked, what was difficult, design decisions, safety decisions, technical decisions, what this proves, what it does not prove, lessons learned, and next build improvements
- `docs/future-improvements.md` — full rewrite with completed phases, short-term, medium-term, long-term, and avoid-for-now sections
- `docs/deployment-notes.md` — local run instructions, model download note, Streamlit Community Cloud option, environment variable guidance, what not to deploy, and future production considerations
- `docs/build-notes.md` — Phase 9 row added; this notes section added; version updated to v0.9

**No code changes in Phase 9.** All app functionality and tests remain from Phases 1–8.

**Final test count:** 429 passed.

**Docs created or updated in Phase 9:**
| File | Action |
|---|---|
| `README.md` | Full rewrite — presentation-ready |
| `docs/build-3-completion-review.md` | Created |
| `docs/portfolio-case-study.md` | Created |
| `docs/demo-script.md` | Full rewrite (was Phase 1 scaffold) |
| `docs/screenshots-checklist.md` | Created |
| `docs/build-reflection.md` | Created |
| `docs/future-improvements.md` | Updated with Phase 9 completion and full future roadmap |
| `docs/deployment-notes.md` | Created |
| `docs/build-notes.md` | Phase 9 row and notes added; status updated to v0.9 |

---

## UI Polish Notes

**What was changed:**

UI polish pass applied using the `/frontend-design` skill. All semantic RAG logic, session state, downloads, and safety boundaries were preserved. 429/429 tests continue to pass. No new dependencies were added.

**Files changed:**

| File | Change |
|---|---|
| `src/ui_components.py` | Full rewrite — expanded CSS (result cards, answer card, pipeline steps, phase grid, index bar, comparison headers, pill badges), new helper functions |
| `src/sample_data.py` | `PLANNED_PHASES` updated to reflect all 8 actual completed phases |
| `app.py` | Targeted edits across all 8 pages — see below |
| `docs/build-notes.md` | This entry added |

**app.py changes:**

- **Sidebar:** updated captions to "Build 3 · Local embeddings · FAISS · No external APIs" and "v0.9 · All 8 phases complete"
- **Home page:** replaced 6× `st.success()` phase list + `st.table()` with `ui.render_phase_completion_row()` — clean green completion grid showing all 8 phases
- **Embedding Index Builder:** removed duplicate `st.warning()` (safety warning already shown via `ui.render_safety_warning()`)
- **Semantic Search:** removed duplicate `st.warning()`; replaced `st.success()` index status with `ui.render_index_ready_bar()`; replaced bare-markdown result loop with `ui.render_semantic_result_card()`; replaced bare markdown pipeline steps with `ui.render_pipeline_steps()`
- **RAG Q&A:** removed duplicate `st.warning()`; replaced `st.success()` index status with `ui.render_index_ready_bar()`; replaced `st.error()` caution + `st.info()` answer with `ui.render_answer_card()`; replaced evidence loop with `ui.render_evidence_card()`; replaced bare markdown pipeline steps with `ui.render_pipeline_steps()`
- **Retrieval Comparison:** replaced `st.warning()` with `ui.render_safety_warning()`; replaced `st.info()` insight with `ui.render_comparison_insight_card()`; replaced column section headers with `ui.render_comparison_col_header()`; replaced result expanders with `ui.render_keyword_result_card()` / `ui.render_semantic_result_card()`; replaced bare markdown pipeline steps with `ui.render_pipeline_steps()`
- **Mini Answer Report:** replaced bare markdown pipeline steps with `ui.render_pipeline_steps()`

**New ui_components.py functions:**

| Function | Purpose |
|---|---|
| `render_phase_completion_row(phases)` | Vertical green grid of completed phase items |
| `render_pipeline_steps(steps)` | Numbered dark-navy step indicator for pipeline prerequisites |
| `render_index_ready_bar(...)` | Green status bar showing index ready state |
| `render_answer_card(answer, caution_text)` | Styled blue answer card with optional red caution banner |
| `render_semantic_result_card(result)` | Navy-bordered result card with rank/score/doc/chunk-id/text-preview |
| `render_evidence_card(item)` | Green-bordered evidence card for RAG evidence items |
| `render_keyword_result_card(result, rank)` | Purple-bordered keyword result card with matched-term badges |
| `render_comparison_insight_card(insight)` | Amber insight card for retrieval comparison |
| `render_comparison_col_header(title, method)` | Styled column header (navy for keyword, dark green for semantic) |
| `_e(text)` | HTML escape helper used in all card functions |

**Visual improvements by page:**

| Page | Before | After |
|---|---|---|
| Home | 6× green success banners + table | Compact green phase completion grid |
| Semantic Search | Plain text rank/score/doc lines | Styled cards with pill badges (rank, score, doc, word count) |
| RAG Q&A | `st.info()` for answer, `st.error()` for caution | Styled answer card; caution shown as distinct red banner above |
| RAG Q&A evidence | Expander-per-item with plain markdown inside | Evidence cards with rank/score/doc/chunk badges and text preview |
| Retrieval Comparison | Expanders for results; `st.info()` for insight | Column-coloured result cards; amber insight card; styled column headers |
| All pipeline check pages | Bare numbered markdown list | Numbered step cards with dark navy circle indicators |
| Embedding/Search/RAG index status | `st.success()` green banner | Compact green index-ready bar with dot indicator |

---

## Polish Step 2 Notes — Screenshot Structure

**What was added:**

- `assets/screenshots/` folder created
- `assets/screenshots/README.md` — safety requirements, expected filenames, demo query guidance, format recommendations
- `docs/screenshots-checklist.md` — full rewrite with practical 11-row table (filename, page, what to show, suggested input, expected result, safety reminder), capture status checklist, demo flow, portfolio usage table
- `README.md` — Screenshots section added (after Running Tests); Folder Structure updated to include `assets/screenshots/`; short-term improvements line updated to remove already-completed items
- `docs/build-notes.md` — this entry added

**No code changes.** No tests added or removed. 429/429 tests continue to pass.

**Expected screenshot filenames (stored in `assets/screenshots/`):**

| Filename | Page |
|---|---|
| `01-home-page.png` | Home |
| `02-document-library.png` | Document Library |
| `03-chunking-explorer.png` | Chunking Explorer |
| `04-embedding-index-builder.png` | Embedding Index Builder — Step 1 |
| `05-faiss-index-summary.png` | Embedding Index Builder — Step 2 |
| `06-semantic-search-learner-data.png` | Semantic Search |
| `07-rag-qa-learner-data.png` | RAG Q&A |
| `08-retrieval-comparison.png` | Retrieval Comparison |
| `09-mini-answer-report-preview.png` | Mini Answer Report |
| `10-downloaded-markdown-report.png` | Downloaded .md report |
| `11-test-results-terminal.png` | pytest terminal |

**Demo question used throughout:** `Can staff put learner names into ChatGPT?`
