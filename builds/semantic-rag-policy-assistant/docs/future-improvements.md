# Future Improvements — Semantic RAG Policy Assistant

**Build 3 · BrightPath ChatGPT Mastery Project**

---

## Completed

- **Phase 1:** Scaffold — document loading, chunking, keyword search, app scaffold, tests
- **Phase 2:** Improved chunking — validation, summary, section strategy, Chunking Explorer
- **Phase 3:** Local embeddings — `sentence-transformers/all-MiniLM-L6-v2`, `embed_chunks`, session state storage
- **Phase 4:** FAISS vector index — IndexFlatIP (cosine) and IndexFlatL2, `create_vector_store`, `search_vector_store`, save/load, 35 tests
- **Phase 5:** Semantic search — `embed_query`, `semantic_search`, `format_semantic_search_results`, 7 demo queries, ranked result cards, session state storage, 50 tests
- **Phase 6:** RAG Q&A — `detect_question_intent`, `generate_grounded_answer`, `generate_rag_response`, `generate_rag_markdown`, 8 demo questions, evidence cards, Markdown download, 66 tests
- **Phase 7:** Retrieval Comparison — `compare_retrieval_methods`, `summarise_keyword_results`, `summarise_semantic_results`, `find_overlap_between_results`, `generate_retrieval_comparison_insight`, `generate_retrieval_comparison_markdown`, 7 demo queries, side-by-side result cards, overlap table, Markdown download, 44 tests
- **Phase 8:** Mini Answer Report — `generate_markdown_answer_report`, `build_report_data_from_session_state`, `format_evidence_items`, `format_retrieval_comparison_section`, 10-section report, reviewer notes, download, 55 tests
- **Phase 9:** Completion review and portfolio documentation

---

## Short-Term Improvements

*High value, low-to-medium effort. Suitable for Build 3 polish before client demos.*

- **Screenshots and portfolio assets** — capture all 8 app pages; label for LinkedIn, GitHub, and case study
- **Deployment notes** — document how to deploy to Streamlit Community Cloud for public demo access
- **PDF export for Mini Answer Report** — allow the 10-section report to be downloaded as a PDF as well as Markdown
- **Demo presets** — one-click pipeline setup with pre-selected documents, chunk size, and demo query
- **UI polish** — improve visual hierarchy in result cards; consistent spacing; better mobile layout
- **Better error handling for model downloads** — show a clear progress message and retry option if the sentence-transformers model download is slow or interrupted
- **Clearer pipeline status in the sidebar** — show which pipeline steps are complete (chunks ✓, embeddings ✓, index ✓) so users always know where they are

---

## Medium-Term Improvements

*Higher effort. Suitable for Build 3 extension or start of Build 4.*

- **Document upload for synthetic/approved files** — allow `.md` files to be uploaded via the UI, with safety validation (filename check, content flag, size limit)
- **Support for multiple document sets** — allow switching between named document collections without re-chunking
- **Section-aware chunking** — split documents on Markdown headings before word-chunking each section; improves precision for well-structured documents
- **Metadata filters for retrieval** — filter retrieved chunks by document name, section, or topic before ranking
- **Retrieval evaluation metrics** — add precision and recall measurement for a small set of known test questions with known correct retrievals
- **Citation verification** — confirm that each retrieved chunk contains content that directly supports the generated answer
- **Persistent local FAISS indexes** — save the index to disk and reload on app start, so re-embedding is not required on every session
- **Chunking strategy comparison** — allow the user to compare word-based, section-based, and paragraph-based chunking side by side
- **Richer test coverage** — integration tests that test the full pipeline end-to-end with a known small document set

---

## Long-Term Improvements

*Significant complexity. For a future build or production architecture planning.*

- **LLM-assisted grounded answers** — replace template answers with LLM-generated prose, grounded strictly in retrieved evidence, with mandatory citation checking and safeguards
- **Optional Ollama integration** — local LLM inference for generated answers; no external API required; model governance documented
- **Hybrid retrieval** — combine keyword (BM25-style) and semantic scores for a single unified ranked result list
- **Reranking retrieved chunks** — add a cross-encoder reranker to improve result order before answer generation
- **Multi-document synthesis** — generate answers that draw evidence from multiple documents simultaneously, with cross-document citation
- **Secure deployment** — authentication, user management, HTTPS, secure document upload, environment variable management
- **Access control** — role-based access to document sets and retrieval logs
- **Audit logging** — record all queries, retrieved chunks, and generated answers for governance and review
- **Data retention controls** — define, enforce, and document how long document chunks and session data are retained
- **Model monitoring and retrieval quality dashboards** — track retrieval quality over time as documents change
- **Privacy and DPIA workflow** — structured checklist for document intake, data protection assessment, and responsible-owner sign-off
- **Client-specific governance configuration** — allow different organisations to set their own responsible-use rules, topic categories, and escalation paths

---

## Not Yet / Avoid For Now

The following should not be added to this prototype without appropriate governance, approval, and technical safeguards:

- Real sensitive learner data of any kind
- Safeguarding case documents, welfare referrals, or disclosure records
- HR or disciplinary files
- Confidential client contracts, pricing, or commercial strategy
- Personal data that could identify any living individual
- Regulated information of any kind
- Production claims without validation
- Unsupervised legal, compliance, safeguarding, clinical, or HR interpretation
- Model-generated answers without evidence grounding, citation, and human review
- Cloud deployment without DPIA, legal review, and responsible-owner sign-off

---

*Build 3 · Semantic RAG Policy Assistant · BrightPath ChatGPT Mastery Project*
