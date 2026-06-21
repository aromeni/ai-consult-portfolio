# Build 11 — Known Limitations

> Portfolio note — complete. Written in Phase 8 after all implementation was finished.

This document is intentional and honest. It is part of the portfolio because responsible AI consulting requires clear communication of what a tool does not do.

---

## Current limitations

**Synthetic documents only.** The document library contains eight fictional policy documents for a fictional organisation (BrightPath Skills Training). This demonstrates methodology and architecture — it does not reflect any real organisation's policies. A real deployment would require real documents and would surface real governance gaps.

**Extractive answers, not fluent prose.** Answers are assembled by concatenating retrieved chunk text. This means answers are grounded and auditable, but they may be longer than necessary, may have some repetition across chunks, and are not rewritten for fluency. An LLM integration (optional, via `.env`) would address this at the cost of hallucination risk and data privacy considerations.

**In-memory FAISS index.** The vector index is built in session memory each time the app starts. It is not persisted between sessions. For a library of 8 documents (~500 chunks) this takes a few seconds. For thousands of documents, a persistent on-disk or cloud-hosted vector store would be needed.

**Rule-based governance checks only.** The eight governance categories in `RISK_CATEGORIES` cover the highest-priority signals for a UK FE training organisation. They do not cover every possible governance risk. Governance checks are a starting point for human review, not a complete compliance assessment.

**No authentication or access controls.** The Streamlit app has no login, no role separation, and no audit trail. It is not suitable for use with real sensitive data — personal, learner, safeguarding, or financial — without adding authentication and access control layers.

**First-run model download requires internet.** The sentence-transformers model (~90MB) is downloaded on first use and cached locally. Subsequent runs are fully offline. Air-gapped environments would need the model pre-loaded.

**Markdown and plain text files only.** The document loader reads `.md` and `.txt` files. PDF and DOCX support is documented as future work.

**No multi-tenancy.** The app serves a single document library per session. A shared deployment serving multiple teams or clients would need multi-tenant architecture.

---

## What a production version would additionally require

| Requirement | Why |
|------------|-----|
| User authentication | Real documents may contain sensitive data — access must be controlled |
| Role-based permissions | Read, write, and admin roles are needed for team use |
| Persistent vector store | Index must survive restarts; incremental document adds must be supported |
| Document upload UI | Real users need to upload their own documents, not use synthetic fixtures |
| PDF and DOCX parsing | Policy documents are commonly distributed as PDFs and Word files |
| Audit logging | Governance use cases require a record of who queried what and when |
| Proper data residency | Where embeddings and documents are stored matters for GDPR compliance |
| LLM integration governance | If adding an LLM, a data processing agreement with the provider is required |
| Retrieval evaluation baseline | A labelled test set of queries and expected source documents is needed to measure retrieval quality objectively |
| Scalability testing | Performance at 10,000+ chunks and 50+ concurrent users needs to be validated |

---

## Future improvements (within the Streamlit prototype)

**PDF and DOCX support.** Add `pypdf` or `pdfminer` for PDF parsing and `python-docx` for Word file support. The document loader is the only module that would need to change.

**Optional LLM-assisted prose.** Wire the optional OpenAI key in `.env.example` to a generation step that rephrases the extractive answer into fluent prose while keeping citations. The `answer_generation.py` module is designed with this extension point in mind.

**Persistent index.** Add FAISS index serialisation (`faiss.write_index` / `faiss.read_index`) so the index survives app restarts. The embedding matrix should be stored alongside it.

**Section-aware chunking.** For Markdown documents, chunk at heading boundaries rather than using a fixed word window. This keeps logically related content together and may improve retrieval precision.

**Retrieval hit-rate evaluation.** Add a test question set with expected source documents, and compute hit@1 and hit@5 metrics to give an objective measure of retrieval quality — rather than relying solely on manual evaluation.

**Reranking.** Add a cross-encoder reranker (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) as a post-retrieval step to improve precision on ambiguous queries.
