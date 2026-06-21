# Build 11 — Build Summary

> Portfolio note — complete. Written in Phase 8 and QA-verified in Phase 9.

---

## What problem does Build 11 solve?

Organisations that handle policy documents, guidance notes, staff handbooks, and operational procedures need a safe way to make those documents searchable and queryable. Staff currently lose time hunting for relevant policy sections, and there is no systematic way to identify governance risks across a document set.

Build 11 addresses this with a semantic document intelligence tool that allows an organisation to load their documents, ask questions in natural language, receive source-cited answers, see a structured governance review of what their documents do and do not cover, and export a structured Markdown report.

---

## What does it demonstrate?

**Semantic retrieval using neural embeddings.** Queries are matched by meaning, not keyword frequency. A question like "What happens if staff share AI output without approval?" retrieves the relevant policy section even when none of those exact words appear in the text. This is the core technical differentiator from a keyword search or a TF-IDF baseline (Build 10).

**Governance integration.** A document intelligence tool used in an FE or skills training context will surface sensitive content — learner data, safeguarding references, assessment decisions. Build 11 includes a rule-based governance check layer that scans queries and retrieved chunks for high-risk signals and surfaces recommended actions. This demonstrates that responsible AI is an engineering concern, not an afterthought.

**End-to-end product thinking.** The application covers the complete journey: document loading → text cleaning → chunking → embedding → index building → retrieval → answer generation → governance review → report export → evaluation. Each step is a distinct page with appropriate UI and controls. The output is a structured Markdown report that could serve as a leave-behind in a real client conversation.

**Production-style architecture.** Ten single-responsibility modules, 386 deterministic tests, lazy imports to keep CI fast, no hardcoded API keys, modular data flow. The code is written as if it will be handed to a team — not just run once.

**Consulting communication.** The portfolio notes (this directory) include a client demo script, a reviewer quick-read, an architecture decision record, and a limitations statement. The README is written for multiple audiences: a hiring manager, a technical reviewer, and a client.

---

## How does it relate to Build 10 and Build 3?

| Dimension | Build 10 | Build 3 | Build 11 |
|-----------|----------|---------|---------|
| Retrieval method | TF-IDF + cosine | sentence-transformers + FAISS | sentence-transformers + FAISS |
| Primary purpose | Teach the pipeline step-by-step | Demonstrate semantic RAG phases | Client-facing consulting product |
| Governance | None | None | Rule-based risk flags (8 categories) |
| Report builder | Markdown / CSV / JSON | Structured answer | Full 10-section consulting report |
| Evaluation | Basic retrieval metrics | Coverage and groundedness | Dashboard + manual evaluation form |
| Test suite | Functional | 429 tests (8 logic modules) | 386 tests (10 logic modules) |
| Portfolio position | Local baseline (private) | Technical teaching build | Flagship product demo |

Build 10 (TF-IDF) provides the explainable keyword-matching baseline. Build 3 teaches the semantic pipeline phase by phase. Build 11 packages the same semantic core as a complete consulting product with governance, a report, and an evaluation layer.

---

## Who is the target user for a demo?

**FE training organisation stakeholders:** a director of quality or operations who needs to know whether their policies cover AI usage by staff; a compliance manager worried about GDPR exposure in their current document set; a head of curriculum wanting to understand what their lesson planning guidance says.

**Technology-aware clients:** a business owner or operations lead who has heard of ChatGPT and wants to understand what a responsible internal AI tool looks like — one that cites sources, flags risks, and always recommends human review.

**Employers and collaborators:** a hiring manager or technical lead who wants to see how the builder thinks about AI product architecture, responsible use, and consulting communication.

---

## What is the recommended demo flow?

See `client-demo-script.md` for the full scripted walkthrough.

The shortest possible demo is three pages: **RAG Q&A** (ask a policy question, see a grounded answer with citations), **Governance Review** (show the risk flags for the same query), **Report Builder** (generate and download the report). This can be done in under five minutes.

The full demo takes 10–15 minutes and covers all 10 pages. It is most effective when the person watching has a real policy question in mind — ideally about AI use, data sharing, or safeguarding boundaries.
