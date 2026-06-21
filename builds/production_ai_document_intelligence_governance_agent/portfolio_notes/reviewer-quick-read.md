# Build 11 — Reviewer Quick-Read

> For a technical reviewer or hiring manager who wants to understand this build in under five minutes.
> Complete — all 9 phases implemented and QA verified.

---

## How to run in three commands

```bash
cd 10-builds/production_ai_document_intelligence_governance_agent
pip install -r requirements.txt
streamlit run app.py
```

On first run, go to **Embedding Index** and click **Load model** to download the sentence-transformer (~90MB, cached after first run).

## How to run tests

```bash
pytest
```

386 tests. Runs in under 1 second. No internet access, no model download.

---

## What to look at first

1. [logic/embeddings.py](../logic/embeddings.py) and [logic/vector_index.py](../logic/vector_index.py) — the semantic retrieval core: lazy model loading, unit-normalised embeddings, FAISS IndexFlatIP.
2. [logic/governance_checks.py](../logic/governance_checks.py) — rule-based risk detection: 8 categories, term matching, deduplication across chunks.
3. [logic/answer_generation.py](../logic/answer_generation.py) — extractive answer assembly: confidence labelling, citations, insufficient-evidence handling.
4. [app.py](../app.py) — ten-page Streamlit app: session state architecture, page routing, prerequisite gating.
5. [tests/](../tests/) — all 386 tests are deterministic and offline; the `FakeModel` pattern (16-dim, no download) enables fast isolated unit testing of the embedding and index layers.

---

## What this build demonstrates

**Semantic RAG architecture.** The pipeline is standard but solidly implemented: document loading → text cleaning → overlapping word-window chunking → dense embeddings (all-MiniLM-L6-v2, 384-dim) → FAISS IndexFlatIP → query retrieval → extractive answer generation. Each step is a single-responsibility module with its own test file.

**Responsible AI practice by design.** The governance check layer is not cosmetic. `check_text` and `check_chunks` in `governance_checks.py` scan for 8 risk categories (learner data, safeguarding, assessment decisions, disciplinary/complaints, personal data, confidential data, funding eligibility, human approval missing) with matched-term deduplication and recommended actions. Every page in the app includes a responsible-use notice. Human review is hardcoded into the report's checklist — not optional.

**Test-driven development across a multi-module logic layer.** 386 tests across 9 test files, all deterministic and fast. The `FakeModel` pattern and lazy imports mean the full suite runs without downloading any model. Tests validate structure, content, edge cases, and constants — not just happy paths.

**Production-quality Streamlit architecture.** Session state is used correctly: documents, chunks, model, embeddings, index, last results, and last answer all persist across page navigations. Prerequisite gating prevents downstream pages from running before their dependencies are ready. The report builder stores the generated report in session state so the download button survives a Streamlit rerun.

**Consulting communication.** The portfolio notes cover architecture decisions (why FAISS IndexFlatIP, why extractive answers, why lazy imports), a client demo script with talking points and what-to-avoid guidance, a limitations statement, and a build-over-build comparison with Build 3 and Build 10.

---

## Test breakdown

| Test file | Module tested | Tests |
|-----------|--------------|-------|
| test_document_loader.py | document_loader | 27 |
| test_text_cleaning.py | text_cleaning | 25 |
| test_chunking.py | chunking | 31 |
| test_embeddings.py | embeddings | 19 |
| test_retrieval.py | retrieval | 34 |
| test_answer_generation.py | answer_generation | 68 |
| test_governance_checks.py | governance_checks | 60 |
| test_report_builder.py | report_builder | 48 |
| test_evaluation.py | evaluation | 74 |
| **Total** | | **386** |

---

## What it does not claim to be

- Not a deployed enterprise product.
- Not a replacement for professional, legal, HR, safeguarding, or compliance expertise.
- Not connected to any external AI API by default (optional OpenAI path is documented in `.env.example`).
- Not tested on real personal or regulated data — all documents are synthetic.
- Not production-hardened — no authentication, no persistent storage, no scalability testing.

---

## Where to go next

- `portfolio_notes/architecture-notes.md` — key design decisions explained
- `portfolio_notes/limitations.md` — honest limitations and future improvements
- `portfolio_notes/client-demo-script.md` — scripted demo walkthrough with talking points
- `portfolio_notes/build-summary.md` — positioning relative to Build 3 and Build 10
