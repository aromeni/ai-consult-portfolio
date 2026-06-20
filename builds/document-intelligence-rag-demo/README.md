# Build 2 — Document Intelligence: Keyword Search and Evidence Extraction

**A Streamlit prototype for transparent, keyword-based document intelligence using synthetic policy documents.**

Build 2 of the ChatGPT Mastery / GPT Master project.

> **Note on naming:** This build was originally titled "RAG Demo." It is not a RAG system. It uses deterministic keyword matching and topic detection — no chunking, no embeddings, no vector retrieval. It is the **pre-RAG foundation layer**: the transparent, auditable starting point before vector search is added. For the full RAG pipeline implementation, see [Build 10 — Production-Style Document Intelligence RAG Agent](../production_document_intelligence_rag_agent/).

---

## One-Line Summary

A working document intelligence tool that searches, extracts evidence from, and generates risk summaries and Q&A answers from synthetic policy documents — using deterministic keyword matching only, with no external AI APIs, no embeddings, and no vector database.

---

## Problem

Organisations that want to apply AI to their policy documents face a practical gap before adding embeddings or a language model:

- They need to understand what their documents actually say before automating anything
- They need to extract and review evidence safely, without exposing sensitive data to external APIs
- They need a transparent, auditable foundation — not a black box
- They need to know where the safe boundaries are before scaling up

This prototype provides that foundation: a fully functional, transparent, and safe document intelligence scaffold — ready for synthetic documents, demonstrable to clients, and extensible into a true RAG system.

---

## Target Users

| User | Why they would use this |
|---|---|
| AI consultants (primary: Rashid) | Demonstrating document intelligence to training providers and governance leads |
| Managers and governance leads | Understanding how AI document analysis works before adopting it |
| Developers | Learning to build AI-adjacent tools safely before adding external APIs |
| Clients evaluating AI policy tools | Seeing a safe, transparent, auditable starting point |

---

## Why This Matters

Before any organisation connects a language model to their policy documents, they need to:

1. Understand what their documents say
2. Extract evidence transparently and safely
3. Identify risks and safeguards from the evidence
4. Produce reviewable outputs with source references

This build demonstrates all four steps using only deterministic keyword matching — so every result is explainable, every match is traceable, and there are no hidden model calls.

---

## Core Features

| Feature | Status |
|---|---|
| Load synthetic policy documents from a local folder | Live |
| Browse document library with metadata (word count, size, line count) | Live |
| View full document with inline keyword search | Live |
| Policy Q&A: multi-term keyword search across all documents | Live |
| Policy Q&A: evidence-based Q&A with topic detection and templated answers | Live |
| Evidence extraction by topic across 13 policy topics | Live |
| Cross-document risk and safeguard summary with evidence | Live |
| 9-section automated Markdown mini brief generator | Live |
| Downloadable Markdown outputs for briefs, risk summaries, and Q&A | Live |
| Responsible-use warnings on every page | Live |

---

## App Pages

| Page | What it does |
|---|---|
| Home | Document library summary, responsible-use notice |
| Document Library | Metadata table with expandable cards for each document |
| Document Viewer | Full document display with inline keyword search |
| Policy Q&A | Tab 1: keyword search. Tab 2: evidence-based Q&A with topic detection |
| Evidence Extraction | Select a topic, extract all matching snippets across documents |
| Risk and Safeguard Summary | Select topics, generate cross-document risk and safeguard summary |
| Mini Brief | Select topics, generate a 9-section downloadable policy evidence brief |

---

## Responsible-Use Boundaries

This prototype is safe for demonstration and planning with synthetic documents.

- All documents are synthetic, anonymised, and fictional
- Do not enter real learner data, safeguarding case details, confidential client records, staff HR data, personal data, or regulated information
- No external AI API calls — all matching is keyword-based and auditable
- Human review of all evidence, summaries, and briefs is required before acting on any output
- This tool does not provide legal, safeguarding, HR, compliance, medical, financial, academic-integrity, or professional advice

See [docs/safety-boundaries.md](docs/safety-boundaries.md) for the full safety statement.

---

## Technical Stack

| Component | Technology |
|---|---|
| UI framework | Streamlit |
| Data tables | Pandas |
| Language | Python 3.11 |
| State management | `st.session_state` |
| Document format | Markdown (.md) |
| Search | Keyword matching (no embeddings, no AI) |
| Topic detection | Keyword + co-detection mapping |
| Evidence extraction | Deterministic keyword/topic matching |
| Risk mapping | Deterministic topic → risk record mapping |
| Brief generation | Templated Markdown generation |
| External APIs | None |
| Embeddings | None |
| Vector database | None |
| Database | None |
| Authentication | None |

---

## Folder Structure

```
document-intelligence-rag-demo/
├── app.py                      # Main Streamlit app (7-page navigation)
├── requirements.txt            # streamlit, pandas, pytest
├── pytest.ini                  # pythonpath = .
├── .env.example                # API key template (no values required yet)
│
├── src/
│   ├── document_loader.py      # list_documents, load_document, get_document_metadata
│   ├── simple_search.py        # normalise_text, tokenise_query, search_document, search_documents
│   ├── evidence_extractor.py   # TOPIC_KEYWORDS, get_supported_topics, extract_policy_evidence, extract_evidence_from_documents
│   ├── risk_summary.py         # get_risk_summary_for_topic, generate_risk_safeguard_summary, get_overall_summary
│   ├── brief_generator.py      # generate_markdown_brief, generate_short_answer, deduplicate_list
│   ├── qa_engine.py            # detect_topics_from_question, answer_policy_question, generate_qa_markdown
│   ├── ui_components.py        # inject_css, page_header, safety_warning, evidence_card, answer_card, safeguard_list
│   └── sample_data.py          # DOCS_DIR, DEMO_TOPICS, DEMO_QUERIES, DEMO_BRIEF_DATA
│
├── data/
│   └── synthetic_documents/    # Four synthetic policy .md files
│
├── assets/
│   └── screenshots/            # Portfolio screenshots (synthetic documents only)
│
├── outputs/
│   └── briefs/                 # Placeholder for saved briefs
│
├── docs/
│   ├── build-notes.md          # Build log and phase notes
│   ├── deployment-notes.md     # Local run, Streamlit Cloud, demo safety checklist
│   ├── build-2-completion-review.md  # Phase completion review
│   ├── portfolio-case-study.md # Portfolio write-up
│   ├── demo-script.md          # Step-by-step demo walkthrough
│   ├── screenshots-checklist.md# Screenshots to capture for portfolio
│   ├── build-reflection.md     # Lessons learned and design decisions
│   ├── future-improvements.md  # Planned improvements by priority
│   └── safety-boundaries.md   # Full safety statement
│
└── tests/
    ├── test_document_loader.py   # 15 tests
    ├── test_simple_search.py     # 36 tests
    ├── test_evidence_extractor.py# 44 tests
    ├── test_risk_summary.py      # 40 tests
    ├── test_brief_generator.py   # 41 tests
    └── test_qa_engine.py         # 53 tests
```

**229 tests total. All passing.**

---

## Synthetic Documents

Four synthetic Markdown policy documents stored in `data/synthetic_documents/`:

| Document | Topics covered |
|---|---|
| `synthetic-ai-acceptable-use-policy.md` | Approved/prohibited use, learner data, safeguarding, human review, accountability, escalation |
| `synthetic-data-protection-guidance.md` | Data minimisation, anonymisation, approved tools, access control, retention, incident reporting |
| `synthetic-safeguarding-and-ai-boundaries.md` | Safeguarding/AI boundary, escalation, AI decision-making limits, safe/unsafe prompts |
| `synthetic-staff-ai-training-notes.md` | Safe prompting, checking outputs, hallucination risk, bias, copyright, escalation |

All documents are fictional. All contain "Synthetic — for demonstration purposes only" in the header.

---

## Setup Instructions

**Requirements:** Python 3.10 or later.

```bash
# 1. Navigate to the project
cd 10-builds/document-intelligence-rag-demo

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy the environment template (no values needed for this build)
cp .env.example .env
```

---

## How to Run

```bash
streamlit run app.py
```

Opens at `http://localhost:8501` by default.

---

## Running Tests

```bash
pytest
```

Run from the `document-intelligence-rag-demo/` directory. No external services, API keys, or model calls required.

Expected output: **229 tests, all passing.**

---

## Deployment

See [docs/deployment-notes.md](docs/deployment-notes.md) for full details.

**Local:** `streamlit run app.py` from the project directory — no API keys or external services required.

**Streamlit Community Cloud:** push the repo to GitHub, set the entry point to `app.py`, confirm `requirements.txt` is present. Use synthetic documents only — do not deploy with real learner data, safeguarding documents, confidential client records, staff HR data, personal data, or regulated information.

**This prototype is not production-ready.** It is suitable for portfolio demonstration, learning, and early consulting conversations using synthetic documents only.

---

## Demo Scenario

**Organisation:** BrightPath Skills Training (synthetic)
**Context:** A consultant wants to review four synthetic AI policy documents, identify safeguarding and data protection risks, and generate a brief for a governance discussion.

**Recommended demo path:**

1. **Home** — see the document library and responsible-use notice
2. **Document Library** — browse the four documents and their metadata
3. **Document Viewer** — open the AI Acceptable Use Policy, search for `safeguarding`
4. **Policy Q&A (Keyword Search tab)** — search for `learner data` across all documents
5. **Policy Q&A (Evidence-Based Q&A tab)** — ask "Can staff enter learner data into AI tools?"
6. **Evidence Extraction** — select all documents, topic `safeguarding`, click Extract
7. **Risk and Safeguard Summary** — load "Data protection" preset, click Generate
8. **Mini Brief** — click Learner Data preset, click Generate brief, download the `.md` file

See [docs/demo-script.md](docs/demo-script.md) for the full scripted walkthrough.

---

## Screenshots

Portfolio and demo screenshots are stored in [`assets/screenshots/`](assets/screenshots/).

Capture scenarios are listed in [`docs/screenshots-checklist.md`](docs/screenshots-checklist.md).

**All screenshots must use synthetic documents only.** Do not capture real learner data, safeguarding case information, confidential client records, staff HR data, personal data, API keys, or regulated information.

---

## Phase History

| Phase | What was built |
|---|---|
| 1 | Scaffold — document loading, navigation, synthetic documents, initial tests |
| 3 | Keyword Search — multi-term transparent search across all documents |
| 4 | Evidence Extraction — topic-based keyword extraction across 13 topics |
| 5 | Risk and Safeguard Summary — deterministic risk record + evidence per topic |
| 6 | Mini Brief Generator — 9-section automated Markdown brief |
| 7 | Evidence-Based Policy Q&A — topic detection, evidence retrieval, templated answers |
| 8 | Completion Review and Portfolio Notes |

---

## Current Limitations

- Document search is keyword-based — no semantic understanding
- No document upload — documents must be placed in `data/synthetic_documents/` manually
- No chunking, no embeddings, no vector store — this is the pre-RAG foundation layer
- Topic detection uses keyword/co-detection matching — not NLP or intent inference
- Session data is lost when the app restarts — no persistent storage
- Single-session use — designed for one user at a time

The RAG pipeline (chunking, TF-IDF embeddings, cosine similarity retrieval, hit-rate evaluation) is implemented in [Build 10](../production_document_intelligence_rag_agent/).

---

## Future Improvements

**Short-term:** Screenshots, UI polish, PDF export for mini briefs.

**Medium-term:** Document upload UI for synthetic/approved files, section-level references.

**The RAG upgrade path** (chunking → embeddings → vector retrieval → LLM generation) has been implemented as a separate, standalone build. See [Build 10 — Production-Style Document Intelligence RAG Agent](../production_document_intelligence_rag_agent/).

See [docs/future-improvements.md](docs/future-improvements.md) for the full list.

---

## Relationship to Other Builds

**Build 1** ([`brightpath-ai-readiness-tool/`](../brightpath-ai-readiness-tool/)) assessed an organisation's AI readiness through a questionnaire. Build 2 applies document intelligence to the policies that govern AI use — showing what keyword-based document analysis looks like in practice.

**Build 10** ([`production_document_intelligence_rag_agent/`](../production_document_intelligence_rag_agent/)) is the direct technical progression from this build. It implements the full RAG pipeline — chunking, TF-IDF embeddings, cosine similarity retrieval, hit-rate evaluation, and exportable reports — using the same consulting context and synthetic document approach.

| | Build 2 (this build) | Build 10 |
|---|---|---|
| Search method | Keyword matching | TF-IDF cosine similarity |
| Chunking | No | Yes — 200-word overlapping chunks |
| Embeddings | No | Yes — TF-IDF index |
| Similarity scores | No | Yes — per-chunk scores |
| Evaluation | No | Yes — hit-rate against 10 questions |
| Risk and brief outputs | Yes | No |
| Teaching focus | Evidence extraction workflow | RAG pipeline mechanics |

Build 2 is the foundation. Build 10 is what the foundation enables.

**Layer 5 — Document Intelligence Agent** of the ChatGPT Mastery project covers:
- Document classification and RAG-readiness concepts
- Keyword-to-embedding progression
- Safe use boundaries for document AI

Build 2 demonstrates the keyword layer of this progression. Build 10 demonstrates the embedding and retrieval layer.

---

*Part of: ChatGPT Mastery / GPT Master Project*
*All sample data and documents are synthetic. This tool provides indicative evidence only.*
