# Build 11 — Architecture Notes

> Portfolio note — complete. Written in Phase 8 after all logic and UI were implemented.

---

## Stack

| Component | Library / Tool | Purpose |
|-----------|----------------|---------|
| UI | Streamlit ≥1.32 | Ten-page multi-page app with session state |
| Embeddings | sentence-transformers ≥2.2.2 | Dense vector embeddings, all-MiniLM-L6-v2 |
| Vector index | faiss-cpu ≥1.7.4 | Exact cosine similarity search |
| Data | pandas ≥2.0 | Tabular display and evaluation DataFrames |
| Numerics | numpy ≥1.24 | Embedding arrays and normalisation |
| Future baseline | scikit-learn ≥1.3 | Included for optional TF-IDF comparison work |
| Tests | pytest ≥7.4 | 386 deterministic tests across all logic modules |
| Config | python-dotenv ≥1.0 | Optional OpenAI API key via .env |

No external API is required for the default pipeline. All processing runs locally.

---

## Module responsibilities

Each module in `logic/` has a single responsibility and is independently testable.

| Module | Responsibility |
|--------|---------------|
| `document_loader.py` | Read .md and .txt files from the sample_documents directory; return structured dicts with metadata |
| `text_cleaning.py` | Remove Markdown syntax, normalise whitespace, return cleaned text with updated word and character counts |
| `chunking.py` | Split cleaned text into overlapping word-window chunks; attach source metadata to each chunk |
| `embeddings.py` | Load the sentence-transformer model (lazy import); embed chunk lists and single queries |
| `vector_index.py` | Build a FAISS IndexFlatIP from an embedding matrix; run nearest-neighbour search |
| `retrieval.py` | Orchestrate query embedding → index search → ranked result assembly; expose weak-retrieval detection |
| `answer_generation.py` | Assemble a grounded extractive answer from retrieved chunks; attach citations and confidence labels |
| `governance_checks.py` | Scan text and chunk lists for governance risk signals using rule-based substring matching |
| `report_builder.py` | Assemble a ten-section structured Markdown report from Q&A output, evidence, and risk flags |
| `evaluation.py` | Compute retrieval coverage metrics, groundedness checklist, risk summary, and manual evaluation records |

The app layer (`app.py`) imports from logic only. There are no cross-module dependencies in the reverse direction.

---

## Key design decisions

### Why FAISS IndexFlatIP?

`IndexFlatIP` performs an exact (brute-force) inner product search. When embeddings are unit-normalised, inner product equals cosine similarity, so this gives exact cosine similarity without approximation.

For the document counts in scope — typically 50–500 chunks — exact search is fast enough (well under 100ms per query on a laptop CPU). Approximate nearest-neighbour indices (e.g., `IndexIVFFlat`, `IndexHNSW`) trade accuracy for speed, which is only beneficial at hundreds of thousands of vectors. Using the exact index keeps retrieval results deterministic and avoids approximation artefacts that would complicate evaluation.

### Why sentence-transformers/all-MiniLM-L6-v2?

- 384-dimensional output — compact, fast to embed, and fast to search
- Good semantic performance on English prose across general domains
- ~90MB download, cached locally after first run — no recurring API cost
- MIT licence, widely used, well-maintained
- Runs on CPU without GPU; no hardware requirements beyond a standard laptop

The model maps semantically similar sentences to nearby vectors regardless of keyword overlap. This allows "Can staff put learner names into ChatGPT?" to retrieve the policy section that says "Staff must not enter learner names or reference numbers into AI tools" even though no keyword matches exist.

### Why extractive answers rather than LLM-generated prose?

An external LLM (OpenAI, Claude) can produce fluent, synthesised prose. For a governance and policy Q&A context, that fluency comes with costs:

- **Hallucination risk** — LLMs can add details not present in the source documents
- **Data privacy** — submitting policy and guidance text to an external API raises data governance questions
- **Cost and dependency** — requires a paid API key and an internet connection
- **Auditability** — a cited extract is easier to verify than a paraphrased answer

Build 11 deliberately uses extractive answers: the answer is assembled directly from retrieved chunk text with no paraphrasing. This keeps every answer fully grounded and auditable. The `build_citation` function in `answer_generation.py` attaches a direct excerpt, score, and source reference to each citation. An optional OpenAI integration path is documented in `.env.example` but not implemented in MVP.

### Why overlapping word-window chunking?

Fixed-size chunks risk splitting a relevant sentence across a boundary, causing neither chunk to contain enough context for retrieval. Overlapping chunks preserve context at boundaries: a 200-word chunk with 40-word overlap means consecutive chunks share 40 words. The step size is `chunk_size − overlap = 160` words, so the overlap is 20% of the chunk.

The values 200 words / 40 overlap are defaults. The Document Processing page exposes sliders so a user can adjust both parameters before building the index.

### Why lazy imports for sentence_transformers and faiss?

Both libraries are large and slow to import. If they were imported at the module level in `embeddings.py` and `vector_index.py`, running `pytest` would trigger downloads and model loads that are irrelevant to unit-testing the logic.

Instead, `load_model()` imports `SentenceTransformer` inside its function body, and `build_index()` imports `faiss` inside its function body. Tests use a `FakeModel` (16-dimensional, deterministic, no download) and a synthetically-built FAISS index. The full test suite runs in under 1 second with no internet access.

### Why rule-based governance checks?

A machine-learning classifier for governance risk would require labelled training data, ongoing maintenance, and a calibrated confidence threshold. For the document counts and risk categories in scope, a rule-based substring matcher is:

- Deterministic — every flag can be explained by pointing to the matched term
- Auditable — the matched term appears verbatim in the flagged text
- Fast — no model inference required
- Maintainable — new risk categories are added by extending the `RISK_CATEGORIES` dict

The eight categories (learner data, safeguarding, assessment decisions, disciplinary/complaints, personal data, confidential data, funding eligibility, human approval missing) cover the highest-priority governance signals for an FE training organisation. The limitation is documented: rule-based checks do not cover every possible risk, and all flags require human review.

---

## Data flow

```
sample_documents/*.md
        |
        v
document_loader.py   ← load_all_documents()
        |
        v
text_cleaning.py     ← clean_document()
        |
        v
chunking.py          ← chunk_all_documents(chunk_size=200, overlap=40)
        |
        v
embeddings.py        ← embed_chunks(chunks, model)  [384-dim unit-normalised]
        |
        v
vector_index.py      ← build_index(embeddings)  [FAISS IndexFlatIP]
        |
        |
query ──┼──→ embeddings.py  ← embed_query(query, model)
        |
        v
vector_index.py      ← search_index(index, query_emb, chunks, top_k)
        |
        v
retrieval.py         ← retrieve()  →  ranked results
        |
        ├──→ answer_generation.py  ← generate_answer()  →  answer dict + citations
        |
        ├──→ governance_checks.py  ← check_query() / check_chunks()  →  risk flags
        |
        ├──→ report_builder.py     ← build_report()  →  Markdown report
        |
        └──→ evaluation.py         ← retrieval_coverage() / groundedness_checklist()
```

---

## Future full-stack path

The Streamlit MVP demonstrates the pipeline. A production system serving a real organisation would move to:

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js (React) — richer UX, authentication flows, role-based views |
| API | FastAPI — typed endpoints, dependency injection, background tasks |
| Database | PostgreSQL — document metadata, evaluation logs, audit trail |
| Vector store | Chroma or Pinecone — persistent index, multi-tenant, incremental updates |
| Generation | Claude API or OpenAI GPT-4 — optional LLM-assisted prose with citations |
| Auth | JWT + role-based access control — restrict access to sensitive documents |
| Deployment | AWS ECS / Azure App Service / GCP Cloud Run, or Vercel + Railway |
| Monitoring | Structured logging, retrieval quality tracking, governance flag alerting |

The modular logic layer in Build 11 is designed so that each module maps cleanly to a service boundary in the full-stack version.
