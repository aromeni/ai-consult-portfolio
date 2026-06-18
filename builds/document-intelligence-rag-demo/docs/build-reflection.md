# Build Reflection — Document Intelligence / RAG Demo

**Build 2 · Prototype v0.6**
**Date:** June 2026

---

## What Was Built

A 7-page Streamlit prototype for deterministic document intelligence using synthetic policy documents. The build covers the full document intelligence pipeline: loading, keyword search, topic-based evidence extraction, risk and safeguard mapping, brief generation, and evidence-based Q&A — without external AI APIs, embeddings, or a vector database.

---

## Why It Was Built

Build 2 was the practical demonstration layer for Layer 5 (Document Intelligence Agent) of the ChatGPT Mastery project. The goal was to show what document intelligence looks like in practice — before adding a language model — and to produce a portfolio-ready prototype that demonstrates:

- Evidence extraction methodology
- Responsible AI implementation
- Transparent, auditable logic
- Policy governance thinking applied to real workflow context

It also built on Build 1 (AI Readiness Tool), which assessed readiness through a questionnaire. Build 2 applies that readiness assessment to the actual documents governing AI use.

---

## What Worked Well

**1. The keyword pipeline scales cleanly.**
Starting with a simple keyword list per topic produced immediately useful results. Expanding from 9 to 13 topics in Phase 4 required adding entries to a single dict, and all tests continued passing. The abstraction held up well through 8 phases.

**2. Deterministic logic is easy to test.**
Because every function produces predictable output from known inputs, pytest tests were fast to write and highly reliable. 229 tests across 6 files with 0 flaky tests. This would be significantly harder with LLM-generated outputs.

**3. The session-state pre-fill pattern works well in Streamlit.**
Setting session state from a button and calling `st.rerun()` made suggested queries, topic presets, and brief presets feel immediate and seamless. This pattern, carried over from Build 1, worked well across every page.

**4. The risk mapping and template approach made Phase 5, 6, and 7 faster.**
Once a solid risk record structure was established in Phase 5, Phases 6 and 7 could reuse it directly. The brief generator and Q&A engine both draw on the same risk data, so consistent outputs appeared automatically without re-implementing logic.

**5. Responsible-use design was easier to maintain than expected.**
Putting the safety notice on every page and including limitations in every generated output normalised the boundary rather than making it feel like a disclaimer. No separate enforcement layer was needed — it was just part of the output structure.

---

## What Was Difficult

**1. Balancing topic coverage vs. false positives in keyword lists.**
Some keywords, like "report" (used in both "incident reporting" and general administrative contexts), can match unrelated lines. The solution was to use multi-word phrases where possible and accept some false positives as a known limitation of keyword-based matching — clearly documented.

**2. The co-detection map required careful thought.**
Designing `_CO_DETECTION_MAP` in Phase 7 required working through the expected examples manually and verifying that each expansion felt logical rather than mechanical. The rule "when learner data is detected, also add data minimisation, anonymisation, approved tools, human review" is defensible because those topics are genuinely related in practice — but it required deliberate design, not just coding.

**3. Streamlit tab state isolation.**
When the Policy Q&A page was restructured from a single view to two tabs in Phase 7, managing session state across tabs required care to avoid stale results appearing after switching modes. The solution was separate session state keys per tab.

**4. Keeping the evidence results structure consistent across phases.**
Phases 4, 5, 6, and 7 all use evidence dicts with the same keys (`topic`, `document_name`, `line_number`, `evidence_text`, `matched_keywords`, `relevance_count`). Renaming `text` to `evidence_text` in Phase 4 required updating all downstream callers simultaneously — a good lesson in keeping data contracts visible.

---

## Design Decisions

**Flat evidence result list, sorted by relevance.**
Rather than returning a nested dict by document or by topic, evidence results are a flat list sorted by `relevance_count` descending. This makes it easy to take the top N results globally or filter by topic, without needing separate extraction calls.

**Co-detection over strict keyword-only detection.**
For the Q&A engine, topic detection from a question uses a two-pass approach: direct keyword matching first, then expansion via a co-detection map. This produces better results for natural policy questions than keyword-only matching, without requiring NLP or intent inference.

**Separate `generate_markdown_brief` and `generate_qa_markdown` functions.**
Even though briefs and Q&A outputs share some sections, they have different structures and purposes. Keeping them separate avoids entangled logic and makes each function independently testable.

**`@st.cache_data` on document loading only.**
Only the document loading step is cached. Evidence extraction, risk summaries, and briefs are re-computed on demand, which keeps the output fresh when users change scope or topics.

---

## Safety and Governance Decisions

**Synthetic documents only.**
From Phase 1, the build was constrained to synthetic documents. This removed the risk of real data exposure during development and demonstration, and established the right habit for future phases.

**Responsible-use notice on every page.**
The safety notice appears as a `st.warning` at the top of every page, not just the home page. This was a deliberate decision to normalise the boundary rather than burying it.

**Limitations text in every generated output.**
Every Markdown output (brief, risk summary, Q&A answer) includes a limitations section that explicitly states: keyword-based matching, not professional advice, human review required. This is not a disclaimer to avoid — it is part of the output.

**No external API calls — not even for convenience.**
The constraint was maintained throughout all eight phases. Even where a simple external API call might have been faster (e.g., for summarisation), the build stayed deterministic. This was the right decision for a foundation-layer prototype.

---

## Technical Decisions

**Python 3.11 with no additional dependencies beyond Streamlit and Pandas.**
Keeping the dependency footprint minimal made the build easy to set up and explain. No LangChain, no vector database client, no model library. This was intentional — the point was to show what you can do before adding those layers.

**Markdown as the document format.**
Markdown is easy to read, write, and version-control. It loads cleanly into Streamlit. A future phase can add PDF parsing or other formats without changing the extraction logic.

**Templated output generation rather than f-strings inline.**
Keeping template strings as named constants (`_SHORT_ANSWER_TEMPLATES`, `_ANSWER_TEMPLATES`, `_LIMITATIONS_TEXT`) made them easy to read, update, and test independently of the generation logic.

---

## What This Proves

- Rashid can build a working document intelligence prototype from scratch
- Rashid can design safe synthetic document workflows with appropriate boundaries
- Rashid understands RAG foundations: document loading, retrieval, evidence grounding, source citation, limitations
- Rashid can think about document AI governance — risk mapping, safeguard recommendations, responsible owner assignment
- Rashid can maintain a consistent data contract across multiple modules through an 8-phase build
- Rashid can produce deterministic, testable, auditable logic as the foundation for future AI augmentation

---

## What It Does Not Prove

This build proves Rashid can turn document intelligence methodology into a working prototype, **but does not yet prove:**

- Real-world RAG performance with embeddings and a vector database
- Semantic search or natural language understanding
- Production readiness or deployment capability
- Accuracy on real organisational documents
- Client validation or acceptance
- Legal or compliance suitability for any live use case

These are the correct next steps, not gaps in this build. The point of a foundation is to be solid before building higher.

---

## Lessons Learned

1. **Design the data contract early.** The evidence result dict structure (`topic`, `document_name`, `evidence_text`, etc.) was established in Phase 4 and held through Phase 7 without changes. Getting this right early saved significant refactoring.

2. **Test at the function level, not the UI level.** Testing the source modules independently made it easy to catch bugs early and maintain confidence when adding new features. UI-level testing was not needed — the logic was already verified.

3. **Phase structure is worth maintaining even when it slows you down.** Each phase built cleanly on the previous one. Jumping ahead to later features without completing earlier ones would have created untested dependencies.

4. **Explainability is a feature, not a constraint.** The transparency of keyword matching — showing matched terms, relevance counts, and source line numbers — turned out to be one of the most useful parts of the demo. It builds trust in a way that a generative answer alone would not.

5. **Start with the boundaries, not the features.** Establishing the synthetic-documents-only constraint from Phase 1 made every subsequent decision easier. There was never a temptation to cut corners on data handling because the boundary was already set.

---

## Next Build Improvements

For the next phase of Build 2 or a Build 3:

- Add local embeddings (e.g., sentence-transformers) for semantic search
- Add a vector store (FAISS or Chroma) for retrieval
- Add LLM-assisted answer generation with strict evidence grounding and source citation
- Add document upload for synthetic/approved files from the UI
- Add section-level evidence references (paragraph context around matched lines)
- Add PDF or Word document parsing
- Add deployment notes for Streamlit Cloud or a simple container

---

*Build 2 · Document Intelligence / RAG Demo · BrightPath ChatGPT Mastery Project*
