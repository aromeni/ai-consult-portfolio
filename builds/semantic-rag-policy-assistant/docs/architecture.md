# Architecture — Semantic RAG Policy Assistant

**Build 3 · BrightPath ChatGPT Mastery Project**

---

## Overview

This document describes the architecture of the Semantic RAG Policy Assistant across all nine phases. All core components (Phases 1–8) are fully implemented.

The architecture follows a standard RAG (Retrieval-Augmented Generation) pipeline:

```
Documents → Chunks → Embeddings → Vector Index → Semantic Search → Grounded Answer → Report
```

---

## 1. Document Loading (`src/document_loader.py`)

**Status: Phase 1 — implemented**

Loads synthetic Markdown policy documents from `data/synthetic_documents/`.

- `list_documents(directory)` — returns sorted list of `.md` file paths
- `load_document(path)` — returns full text content of one file
- `load_all_documents(directory)` — returns `{filename: text}` dict
- `get_document_metadata(path)` — returns filename, path, title, word_count, line_count, character_count

No external calls. All documents are local and synthetic.

---

## 2. Chunking Layer (`src/chunker.py`)

**Status: Phase 2 — implemented**

Splits document text into overlapping word-count chunks before embedding.
Documents must be chunked before they can be embedded or indexed.

**Functions:**
- `split_text_into_words(text)` — explicit whitespace tokeniser
- `validate_chunk_settings(chunk_size, overlap)` — returns `(bool, message)` before chunking starts
- `estimate_chunk_count(word_count, chunk_size, overlap)` — exact estimate using the same sliding-window logic
- `chunk_text(text, chunk_size, overlap, document_name, strategy)` — splits one document
- `chunk_documents(documents, chunk_size, overlap, strategy)` — splits all documents in a `{filename: text}` dict
- `get_chunking_summary(chunks)` — returns aggregate statistics for a chunk list

**Each chunk contains:**
`chunk_id`, `document_name`, `chunk_index`, `text`, `word_count`, `character_count`,
`start_word`, `end_word`, `chunk_size`, `overlap`, `strategy`.

**Chunk ID format:** `{doc-slug}__chunk_{index:03d}` (e.g. `synthetic-ai-acceptable-use-policy__chunk_003`).
Chunk IDs are globally unique because each document's slug is derived from its unique filename.

**Strategies:**
- `word` (default) — sliding window over whitespace-split words with configurable overlap
- `section` (experimental) — splits on `## ` Markdown level-2 headings, then word-chunks each section;
  falls back to word chunking if fewer than 2 headings are found

**Session state:** Generated chunks are stored in `st.session_state["chunks"]`,
`["chunking_summary"]`, and `["chunking_settings"]` so they can be passed forward to the
embedding phase (Phase 3) without re-chunking.

**Chunk settings guidance:**
- Chunk size affects retrieval precision and context quality
- Smaller chunks are more precise but may lose surrounding context
- Larger chunks keep more context but may retrieve irrelevant material
- Overlap preserves context at chunk boundaries
- Recommended defaults for these short synthetic docs: chunk_size=120, overlap=30

---

## 3. Embedding Layer (`src/embedding_engine.py`)

**Status: Phase 3 — implemented**

Converts document chunks into dense vector embeddings using a local sentence-transformers model.
All processing is local — no external AI API calls, no cloud services.

**Functions:**
- `get_default_embedding_model_name()` → `"sentence-transformers/all-MiniLM-L6-v2"`
- `load_embedding_model(model_name)` — lazy-imports `SentenceTransformer`; gives a clear error if the library is not installed
- `validate_chunks_for_embedding(chunks)` → `(bool, message)` — checked before embedding starts
- `embed_texts(texts, model, model_name, normalise)` → result dict with `model_name`, `embedding_dimension`, `embeddings` (numpy ndarray), `text_count`, `normalised`
- `embed_chunks(chunks, model, model_name, normalise)` → result dict with `model_name`, `embedding_dimension`, `embedded_chunks`, `embedding_matrix`, `chunk_count`, `normalised`
- `get_embedding_summary(embedded_chunks, model_name, embedding_dimension, normalised)` → aggregate statistics dict

**Default model:** `sentence-transformers/all-MiniLM-L6-v2`
- 384-dimensional embeddings
- ~90 MB model download on first use
- No API key required
- Runs locally on CPU or GPU

**Embedded chunk format:** Each chunk dict from the chunker gains two new keys:
- `embedding_index` (int): row position in the embedding matrix
- `embedding_vector` (list[float]): serialisable list form of the embedding

The `embedding_matrix` (numpy ndarray, shape: `[n_chunks, 384]`) is also stored for fast vector operations in Phase 4.

**Session state:** After embedding, the app stores:
- `st.session_state["embedding_model_name"]`
- `st.session_state["embedded_chunks"]`
- `st.session_state["embedding_matrix"]`
- `st.session_state["embedding_summary"]`

These will be consumed by the vector index builder in Phase 4.

**Model caching:** The loaded model is cached with `@st.cache_resource` so it stays in memory across Streamlit reruns without reloading from disk.

**No external API calls.** All embedding will run locally using the `sentence-transformers` library.
`sentence-transformers` will be added to `requirements.txt` in Phase 3 only.

---

## 4. Vector Index Layer (`src/vector_store.py`)

**Status: Phase 4 — implemented**

Builds an in-memory FAISS vector index from the Phase 3 embedding matrices.
Embedded chunks are stored in the index and can be searched by cosine similarity or Euclidean distance.
All processing is local — no external API calls, no cloud services.

**Functions:**
- `validate_embedding_matrix(embedding_matrix, embedded_chunks)` — returns `(bool, message)` before indexing; checks shape, dimension, dtype, and count alignment
- `build_faiss_index(embedding_matrix, metric)` — builds IndexFlatIP (cosine) or IndexFlatL2 (L2); lazy-imports FAISS with a readable error if not installed
- `create_vector_store(embedded_chunks, embedding_matrix, metric)` — validates, builds index, returns a vector store dict
- `search_vector_store(vector_store, query_embedding, top_k)` — returns ranked result dicts; safe if top_k exceeds chunk count; does not mutate original chunks
- `get_vector_store_summary(vector_store)` — aggregate stats dict with safe defaults for empty input
- `save_faiss_index(index, path)` — writes index to disk via `faiss.write_index`
- `load_faiss_index(path)` — reloads index from disk via `faiss.read_index`

**Index types:**
- `IndexFlatIP` — cosine similarity via inner product. Used when `metric="cosine"` (default). Requires unit-normalised embeddings — Phase 3 normalises by default. Higher score means more similar.
- `IndexFlatL2` — Euclidean distance. Used when `metric="l2"`. Lower distance means more similar.

**`create_vector_store` output dict:**
```
{
    index, embedded_chunks, embedding_matrix, metric,
    dimension, chunk_count, document_count, index_type
}
```

**`search_vector_store` result fields:**
`rank`, `score`, `chunk_id`, `document_name`, `chunk_index`, `text`, `word_count`, `character_count`, `embedding_index`.

**Session state:** After building the index, the app stores:
- `st.session_state["vector_store"]`
- `st.session_state["vector_store_summary"]`
- `st.session_state["vector_metric"]`

These will be consumed by the semantic search function in Phase 5.

**Design decisions:**
- The index is in-memory for this prototype — no persistent storage is required.
- Flat indexes (IndexFlatIP, IndexFlatL2) perform exact search — no approximation. Correct for this scale.
- `faiss-cpu` was added to `requirements.txt` in Phase 4 only, as planned.
- No Chroma, no LangChain, no LlamaIndex — FAISS only, installed locally.

---

## 5. Semantic Search Layer (`src/semantic_search.py`)

**Status: Phase 5 — implemented**

Embeds a user query using the same sentence-transformers model used for document chunks,
then searches the FAISS vector index for the most semantically similar chunks.
All processing is local — no external AI API calls.

**Functions:**
- `validate_semantic_search_inputs(query, vector_store)` → `(bool, message)` — checks that query is non-empty and vector store has a built index
- `embed_query(query, model, model_name, normalise)` → dict with `query`, `model_name`, `embedding` (np.ndarray shape 1×dim), `embedding_dimension`, `normalised`
- `format_semantic_search_results(results)` → adds `source_label` and `preview_text` to each result dict; does not mutate originals
- `semantic_search(query, vector_store, model, model_name, top_k, normalise)` → full search result dict

**`semantic_search` output dict:**
```
{
    query, model_name, top_k, results, result_count,
    query_embedding_dimension, metric, limitations
}
```

**Each result includes:**
`rank`, `score`, `chunk_id`, `document_name`, `chunk_index`, `text`,
`word_count`, `character_count`, `embedding_index`, `source_label`, `preview_text`.

**Session state:** After search, the app stores:
- `st.session_state["last_semantic_query"]`
- `st.session_state["last_semantic_results"]`
- `st.session_state["last_semantic_search_summary"]`

These prepare the session for RAG Q&A and Mini Answer Report in the next phase.

**Design decisions:**
- User queries are embedded with the same model and normalisation settings as document chunks.
  When Phase 3 normalises embeddings (`normalise=True`, the default), IndexFlatIP inner product
  equals cosine similarity — so the query must also be normalised for consistent scoring.
- `embed_query` always returns a 2D numpy array (shape 1×dim) ready for `faiss.index.search`.
- `format_semantic_search_results` adds display fields without mutating the original result dicts.
- Limitations are always included in the output to surface responsible-use context alongside results.

**Semantic search enables retrieval without exact keyword matching** — capturing relevant chunks
even when the query uses different words than the document text.

---

## 6. Keyword Search (`src/keyword_search.py`)

**Status: Phase 1 — implemented**

Deterministic keyword search over chunk text. Used as a retrieval baseline for comparison with semantic search.

- `tokenise_query(query)` — lowercase tokens, stop-word filtered
- `keyword_search_chunks(chunks, query, top_k)` — returns scored results with matched_terms

Used in Phase 1 as the only retrieval method. Will be compared against semantic search in Phase 5.

---

## 7. RAG Q&A Layer (`src/rag_engine.py`)

**Status: Phase 6 — implemented**

Generates grounded, evidence-based answers from retrieved FAISS chunks using deterministic
template logic. No external LLM API. No hallucination beyond retrieved evidence.

**Functions:**
- `validate_rag_inputs(question, vector_store)` → `(bool, message)` — 4-check validation before pipeline runs
- `detect_question_intent(question)` → dict with `detected_topics`, `question_type`, `needs_caution`, `caution_reason`; deterministic keyword matching
- `generate_grounded_answer(question, retrieved_chunks, intent)` → template-based answer selected by question_type; cautious no-results message when no chunks retrieved
- `generate_evidence_summary(retrieved_chunks, max_items)` → list of evidence dicts for display and export
- `get_rag_limitations()` → 7 responsible-use limitation strings
- `generate_rag_response(question, vector_store, model, model_name, top_k)` → full pipeline: validate → intent → retrieve → answer → evidence → return dict
- `generate_rag_markdown(rag_response)` → Markdown string for download

**`generate_rag_response` output dict:**
```
{
    question, answer, detected_topics, question_type,
    needs_caution, caution_reason, retrieved_chunks,
    evidence_summary, top_k, model_name, metric, limitations
}
```

**Intent detection — 13 topic categories:**
learner data, safeguarding, human review, approved tools, accountability,
bias, hallucination, copyright, escalation, data minimisation, anonymisation,
retention, incident reporting.

**Question types (priority order):**
safeguarding, data_protection, output_quality, approved_use, accountability,
incident_response, general_policy, unknown.

**Answer templates:**
Each question_type maps to a fixed answer template grounded in retrieved evidence.
Templates reference the policy position, required staff action, and review reminder.
No evidence is invented — templates acknowledge what was retrieved, not what should exist.

**Session state:** After generating a response, the app stores:
- `st.session_state["last_rag_question"]`
- `st.session_state["last_rag_response"]`
- `st.session_state["last_rag_answer"]`
- `st.session_state["last_rag_evidence"]`

These will be consumed by Retrieval Comparison and Mini Answer Report in the next phase.

**Safety constraint:** All answers cite retrieved evidence. No answer is generated without retrieved chunks unless displaying the no-results fallback. Limitations are always included. Answers must not claim to be professional advice.

**No external LLM API.** Answer generation uses deterministic templates only.
Optional LLM-assisted answers remain a long-term improvement.

---

## 8. Retrieval Comparison (`src/comparison.py`)

**Status: Phase 7 — implemented**

Runs both keyword and semantic retrieval for the same query and returns a structured comparison
including result summaries, overlap detection, and a deterministic insight.
All processing is local — no external AI API calls.

**Functions:**
- `summarise_keyword_results(keyword_results)` → dict with result_count, unique_documents, top_score, matched_terms, method_note
- `summarise_semantic_results(semantic_results)` → dict with result_count, unique_documents, top_score, method_note
- `find_overlap_between_results(keyword_results, semantic_results)` → list of overlap dicts; matched by chunk_id; each item has chunk_id, document_name, keyword_rank, semantic_rank
- `generate_retrieval_comparison_insight(query, keyword_summary, semantic_summary, overlap)` → deterministic explanation string covering 5 retrieval outcome cases
- `generate_retrieval_comparison_markdown(comparison_result)` → Markdown string for download
- `compare_retrieval_methods(query, chunks, vector_store, model, model_name, top_k)` → full pipeline dict

**`compare_retrieval_methods` output dict:**
```
{
    query, top_k,
    keyword_results, semantic_results,
    keyword_summary, semantic_summary,
    overlap, comparison_insight, limitations
}
```

**How the two methods differ:**
- Keyword search retrieves chunks containing exact or near-exact query terms.
  It is fast and deterministic but misses synonyms and paraphrased content.
- Semantic search retrieves chunks whose embedding is most similar to the query embedding.
  It captures meaning-based relevance but may return conceptually related yet imprecise chunks.

**Why comparison helps:**
- Overlap between methods can indicate strong evidence candidates — both approaches converge.
- Differences reveal where semantic retrieval adds value over keyword matching.
- Gaps (neither method returns results) surface where chunking, query wording,
  or embedding quality may need review.

**Session state:** After comparison, the app stores:
- `st.session_state["last_comparison_query"]`
- `st.session_state["last_retrieval_comparison"]`
- `st.session_state["last_keyword_results"]`
- `st.session_state["last_semantic_results"]`

These will be consumed by Mini Answer Report in the next phase.

---

## 9. Mini Answer Report Layer (`src/report_generator.py`)

**Status: Phase 8 — implemented**

Generates a full 10-section Markdown report from RAG Q&A output, retrieved evidence,
and optional retrieval comparison results.
All processing is local — no external AI API calls.

**Functions:**
- `create_report_filename(title)` → safe lowercase `.md` filename
- `get_default_report_limitations()` → 4 responsible-use limitation strings
- `format_detected_topics(topics)` → comma-separated string or fallback message
- `format_evidence_items(evidence_items, max_items)` → Markdown evidence block; placeholder if empty
- `format_limitations(limitations)` → Markdown bullet list; defaults if empty
- `format_retrieval_comparison_section(comparison_result)` → comparison summary Markdown; placeholder if missing
- `build_report_data_from_session_state(session_state)` → assembles all report fields from session state with safe defaults
- `generate_markdown_answer_report(report_data)` → full 10-section Markdown report

**Report sections:**
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

**`report_data` dict keys:**
`report_title`, `generated_date`, `question`, `answer`, `detected_topics`, `question_type`,
`needs_caution`, `caution_reason`, `model_name`, `retrieval_metric`, `top_k`,
`evidence_items`, `comparison_result`, `limitations`, `reviewer_notes`.

**Backward compatible:** accepts old keys `sources` and `retrieval_method` from Phase 1.

**Session state:** After report generation, the app stores:
- `st.session_state["last_answer_report_markdown"]`
- `st.session_state["last_answer_report_data"]`
- `st.session_state["last_answer_report_filename"]`

**Report role:**
- The report collects the latest RAG response, retrieved evidence, and source chunks.
- The retrieval comparison section is included when available.
- The Markdown format is designed for easy editing and portfolio/demo use.
- Outputs are evidence support for discussion and review, not final advice.

**No external dependencies.** The report generator uses only the Python standard library.

---

## 10. UI Layer (`src/ui_components.py`)

**Status: Phase 1 — implemented**

Streamlit-native helper functions for consistent, portfolio-quality presentation.

- CSS injection (dark navy sidebar, clean app background, card components)
- `render_page_header`, `render_safety_warning`, `render_prototype_notice`
- `render_placeholder` — dashed-border coming-soon cards for future phases
- `render_chunk_card`, `render_search_result` — result display cards
- `render_workflow_diagram`, `render_boundary_notice`

No external CSS frameworks or additional dependencies.

---

## Safety Boundaries

This architecture is designed with the following constraints that must not be relaxed without governance approval:

- **Synthetic documents only** — all documents are fictional and clearly labelled
- **No real personal data** — no learner data, safeguarding information, HR records, or regulated information
- **No external AI API calls** — all processing (embedding, search, generation) runs locally
- **No production deployment** — this is a prototype for learning and portfolio use
- **Human review required** — all outputs are starting points, not final authority
- **No professional advice** — outputs are not legal, safeguarding, HR, compliance, or clinical advice

See [safety-boundaries.md](safety-boundaries.md) for the full safety statement.

---

## Why Synthetic Documents?

Synthetic documents allow the full RAG pipeline to be built, tested, and demonstrated safely:

1. No data protection risk — no real personal data can be exposed
2. No safeguarding risk — no real welfare or case information involved
3. Full portfolio demonstrability — clients and learners can see the tool without sensitive exposure
4. Reproducible tests — documents are stable and versioned

When this architecture is adapted for real organisational use, it must go through a Data Protection Impact Assessment (DPIA) and legal review before processing real documents.

---

*Build 3 · Semantic RAG Policy Assistant · BrightPath ChatGPT Mastery Project*
