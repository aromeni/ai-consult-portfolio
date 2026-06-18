# Build Notes — Document Intelligence / RAG Demo

**Build start:** 2026-06-10
**Build number:** 2
**Status:** Polish Step 3 — UI polish pass complete (Prototype v0.6)

---

## Build Objective

Create a working prototype that demonstrates safe document intelligence using synthetic
policy documents. The tool allows a consultant or manager to:

1. Browse a library of synthetic policy documents
2. Search documents by keyword
3. Extract evidence for a chosen topic (safeguarding, learner data, human review, etc.)
4. Generate a cross-document risk and safeguard summary
5. Produce a downloadable Markdown evidence brief

This is the first phase. No external AI APIs, embeddings, or vector databases are used.
All logic is keyword-based, making it fully transparent and auditable.

---

## Relationship to Build 1

Build 1 ([`brightpath-ai-readiness-tool/`](../../brightpath-ai-readiness-tool/)) assessed
AI readiness using a questionnaire. Build 2 applies document intelligence to the policies
that govern AI use — demonstrating the next practical layer of a real AI consultancy workflow.

---

## Planned Build Phases

| Phase | Scope | Status |
|---|---|---|
| 1 | Scaffold — folder structure, app.py navigation, src modules, synthetic docs, tests | Complete |
| 3 | Keyword Search — Policy Q&A page functional with multi-term transparent search | Complete |
| 4 | Evidence Extraction — topic-based keyword extraction across 13 topics, full UI | Complete |
| 5 | Risk and Safeguard Summary — deterministic risk record + evidence, Markdown download | Complete |
| 6 | Mini Brief Generator — 9-section automated brief, presets, download | Complete |
| 7 | Evidence-Based Policy Q&A — topic detection, evidence retrieval, templated answer, download | Complete |
| 8 | Completion Review and Portfolio Notes — README overhaul, case study, demo script, reflection, improvements | Complete |
| Polish 1 | Screenshot structure and guidance — assets/screenshots/, checklist, README section | Complete |
| Polish 2 | Deployment notes — local run, Streamlit Cloud option, demo safety checklist, production considerations | Complete |
| Polish 3 | UI polish pass — custom CSS, page headers, evidence cards, answer cards, safeguard lists, dark sidebar, workflow diagram, feature cards | Complete |
| 2 | Document upload UI — allow users to load their own synthetic/approved documents | Planned |
| 3 | Embeddings and vector store — chunk documents, embed with a local model, store in FAISS/Chroma | Planned |
| 4 | Policy Q&A — free-text question, retrieve top-k chunks, generate grounded answer | Planned |
| 5 | Source citation and evidence trail — show which document + section answered each question | Planned |
| 6 | Portfolio documentation — case study, demo script update, screenshots | Planned |

---

## Polish Step 3 Notes (2026-06-11)

**Polish Step 3: UI Polish Pass**

- Created `src/ui_components.py` (new module, no tests required — presentation only):
  - `inject_css()` — single `<style>` block injected once at startup; covers app background,
    dark navy sidebar, heading colours, native metric/button tweaks, tab styling, and all
    custom `.dp-*` component classes
  - `page_header(title, subtitle)` — navy-underlined page header replacing bare `st.title()`
  - `safety_warning()` — amber border-left card replacing bare `st.warning()` safety notice
  - `prototype_notice(text)` — blue border-left info card for prototype/topic context
  - `info_card(title, body)` — generic white card with shadow
  - `workflow_diagram()` — dark navy pipeline steps (Documents → Search → Evidence → ...)
  - `feature_cards()` — 4-column feature summary cards for Home page
  - `boundary_notice()` — concise prototype-limits strip for Home page
  - `badge_html(label, style)` / `render_badges(labels, style)` — inline coloured chips
  - `kw_badges_html(keywords)` — keyword badges for use inside card HTML
  - `evidence_card(result)` — styled card for evidence/search results with doc name,
    line number, relevance count, snippet, and keyword badges; handles both
    `evidence_text` (evidence_extractor) and `snippet` (simple_search) keys
  - `answer_card(text)` — blue-tinted answer card replacing `st.info()` for Q&A answers
  - `safeguard_list(items)` — green-check checklist inside a white card
- Updated `app.py`:
  - Added `from src import ui_components as ui` import
  - Added `ui.inject_css()` after `st.set_page_config()`
  - Removed `_SAFETY_NOTICE` constant (safety text is now centralised in `ui_components.py`)
  - Removed unused `from collections import defaultdict as _dd` inline import (moved to
    top-level `from collections import defaultdict`)
  - Removed unused `import re` (was in original but unused in display code)
  - All pages: replaced `st.title()` + `st.warning()` with `page_header()` + `safety_warning()`
  - Home page: complete restructure — workflow diagram, 4 feature cards, boundary notice,
    4-metric row (documents / total words / topics / tests), document list
  - Document Library: added 3-metric summary row (documents / total words / total lines)
  - Document Viewer: added metadata strip (words / lines / size); results via `evidence_card()`
  - Evidence Extraction: topic info via `prototype_notice()` with inline keyword badges;
    results via `evidence_card()`
  - Policy Q&A Tab 1: mode description via `prototype_notice()`; active search terms as
    badge row; results via `evidence_card()`
  - Policy Q&A Tab 2: mode description via `prototype_notice()`; detected topics as badge
    row; answer via `answer_card()`; evidence via `evidence_card()`; safeguards via
    `safeguard_list()`; tab labels updated to include emoji icons
  - Risk and Safeguard Summary: suggested owner via `prototype_notice()` inside expanders;
    safeguards via `safeguard_list()`; evidence via `evidence_card()`
  - Mini Brief: short answer via `answer_card()`
- Updated `README.md`: added `ui_components.py` to folder structure
- Updated `docs/build-notes.md`: status to Polish Step 3 complete; row added to phases table

No logic changes — all retrieval, extraction, generation, and session-state code is unchanged.
No new dependencies — only Streamlit (already in requirements.txt).
229/229 tests still pass.

---

## Polish Step 2 Notes (2026-06-11)

**Polish Step 2: Deployment Notes**

- Created `docs/deployment-notes.md`:
  - Prototype status — what it is and is not (no APIs, no auth, no production data)
  - Local run instructions (venv, pip install, streamlit run app.py)
  - Run tests instructions (pytest, expected 229 passing)
  - Streamlit Community Cloud option (high-level steps, safety rules before deploying)
  - What not to deploy yet (real data, safeguarding docs, HR files, production use)
  - Environment variables (no keys required, .env.example exists, never commit .env)
  - Demo safety checklist (7-item checklist before any demo or recording)
  - Future production considerations (auth, access control, secure storage, audit logs, DPIA, model governance, hosting, legal review)
  - Recommended current use (portfolio, learning, early consulting conversations, synthetic documents only)
- Updated `README.md`:
  - Added Deployment section (after Running Tests) linking to `docs/deployment-notes.md`, with local and Streamlit Cloud one-liners and a clear "not production-ready" statement
  - Added `deployment-notes.md` to Folder Structure
- Updated `docs/build-notes.md`: status to Polish Step 2 complete; Polish Step 2 row added to planned phases table

No app functionality, tests, or dependencies changed.

---

## Polish Step 1 Notes (2026-06-10)

**Polish Step 1: Screenshot Structure and Guidance**

- Created `assets/screenshots/` folder with `.gitkeep` to track the folder in git
- Created `assets/screenshots/README.md`:
  - Safety rules (no real data, no API keys, no private paths, crop browser clutter)
  - Table of 10 expected filenames mapped to app pages
  - Instructions for capturing and saving screenshots
- Replaced `docs/screenshots-checklist.md` with a full practical table:
  - Columns: filename, app page, what to show, demo input, expected result, safety note
  - All 10 screenshot scenarios including the two Policy Q&A evidence-based Q&A questions
  - Capture instructions, storage path reference, portfolio use guidance
- Updated `README.md`:
  - Added Screenshots section (after Demo Scenario) linking to `assets/screenshots/` and `docs/screenshots-checklist.md`
  - Added `assets/screenshots/` entry to Folder Structure
- Updated `docs/build-notes.md`: status updated to Polish Step 1 complete; Polish Step 1 row added to planned phases table

No app functionality, tests, or dependencies changed.

---

## Phase 8 Notes (2026-06-10)

**Phase 8: Completion Review and Portfolio Notes**

- Overhauled `README.md` for portfolio presentation:
  - One-line summary, why this matters section, app pages table, updated feature table,
    updated folder structure (all 6 src modules, all 6 test files), updated test count to 229,
    phase history table, cleaner demo scenario, updated future improvements section
- Created `docs/build-2-completion-review.md`:
  - Build goal, completed phases 1–8, key features, methodologies reused, technical
    implementation, responsible-use boundaries, evidence of completion, what this build
    proves, what it does not prove, remaining optional improvements, readiness verdict,
    recommended next actions, final verdict
- Created `docs/portfolio-case-study.md`:
  - One-line summary, problem, target user, workflow context, goals, success criteria,
    solution overview, architecture, tech stack, data/documents, AI approach, implementation
    phases, testing table, demo notes, results, business value, risk/governance, limitations,
    lessons learned, future improvements, portfolio summary
- Updated `docs/demo-script.md` to v0.6:
  - Added Step 5 (Evidence-Based Q&A tab) with suggested question, expected output, and
    key message; updated Step 4 to be Keyword Search tab specifically; updated Step 6–8
    numbering; updated closing pitch to reference Phase 7 capability; version bumped to v0.6
- Created `docs/screenshots-checklist.md`:
  - 11 screenshot items (home, library, viewer, keyword search, Q&A answer, Q&A safeguards,
    evidence extraction, risk summary, mini brief, downloaded brief, pytest results);
    safety reminder, storage path, portfolio use guidance
- Created `docs/build-reflection.md`:
  - What was built, why, what worked well (5 items), what was difficult (4 items), design
    decisions, safety/governance decisions, technical decisions, what this proves, what it
    does not prove, lessons learned (5 items), next build improvements
- Created `docs/future-improvements.md`:
  - Short-term (screenshots, deployment, UI, PDF export, stronger tests),
    medium-term (multi-doc sets, upload UI, semantic search, local embeddings),
    long-term (LLM-assisted Q&A, RAG, citation verification, policy gap analysis,
    governance checklist, secure deployment),
    not-yet/avoid (real sensitive data, safeguarding cases, HR files, production claims)
- Updated `docs/build-notes.md`: status to Phase 8 complete; Phase 8 row in table

## Phase 7 Notes (2026-06-10)

**Phase 7: Evidence-Based Policy Q&A**

- Created `src/qa_engine.py` from scratch:
  - `_QUESTION_TOPIC_KEYWORDS` — dict mapping each of the 13 topics to a list of
    question-level keywords matched case-insensitively against user questions
  - `_CO_DETECTION_MAP` — when a topic is detected directly, automatically add
    related topics (e.g. "learner data" adds data minimisation, anonymisation,
    approved tools, human review)
  - `_ANSWER_TEMPLATES` — 13 deterministic answer templates, one per topic
  - `_NO_TOPICS_ANSWER` — cautious fallback if no topic detected
  - `_NO_EVIDENCE_ANSWER` — cautious fallback if topics detected but no evidence
  - `detect_topics_from_question(question)` — two-pass: direct keyword matches
    then co-detection expansion; returns deduplicated list
  - `generate_policy_answer(question, detected_topics, evidence_results, risk_summary_items)`
    — returns template-based answer, or cautious fallback if no topics/evidence
  - `get_question_limitations(detected_topics, evidence_results)` — returns 5 standard
    limitation notes; appends extra note if no evidence found
  - `answer_policy_question(question, documents, selected_document=None)` — full
    pipeline: detect topics → extract evidence → build risk summary → generate answer
    → collect safeguards/owners → derive coverage note → return qa_result dict
  - `generate_qa_markdown(qa_result)` — 7-section Markdown: Question, Short Answer,
    Detected Topics, Evidence Found (capped at 8), Recommended Safeguards, Suggested
    Responsible Owners, Limitations
- Restructured Policy Q&A page in `app.py` using `st.tabs`:
  - Tab 1 "Keyword Search": existing multi-term keyword search (unchanged)
  - Tab 2 "Evidence-Based Q&A":
    - 8 suggested question buttons (2 rows of 4) with session-state pre-fill pattern
    - Policy question text_input with `key="qa_eb_question"`
    - Scope radio (all documents / specific document)
    - "Generate answer" button: calls `answer_policy_question`, stores result in
      session state so it persists after reruns
    - Results: question echo, detected topics caption, short answer info box,
      evidence by topic (max 3 per topic), source coverage note, safeguards list,
      owners list, limitations expander, Markdown download button
- Added import: `answer_policy_question`, `generate_qa_markdown` from `qa_engine`
- Created `tests/test_qa_engine.py` — 53 tests covering all 5 public functions:
  detect_topics_from_question, generate_policy_answer, get_question_limitations,
  answer_policy_question, generate_qa_markdown
- Version bumped to v0.6

## Phase 6 Notes (2026-06-10)

**Phase 6: Mini Brief Generator**

- Rewrote `src/brief_generator.py` completely:
  - `_SHORT_ANSWER_TEMPLATES` — 13 topic templates for deterministic short answers
  - `_NEXT_ACTIONS_UNIVERSAL` — 7 universal next-action strings
  - `_NEXT_ACTIONS_BY_TOPIC` — 13 topic-specific next-action strings
  - `_REVIEWER_NOTES` — 4 default reviewer note strings
  - `_LIMITATIONS_TEXT` — full responsible-use limitations statement
  - `generate_short_answer(question, topics, evidence_results)` — combines relevant
    topic templates; returns cautious fallback for empty/unknown topics
  - `deduplicate_list(items)` — removes duplicates preserving original order
  - `generate_next_actions(topics, evidence_results)` — starts with universal actions,
    appends topic-specific actions, deduplicates; works for any combination of topics
  - `generate_markdown_brief(brief_data)` — 9-section Markdown document: Question/Topic,
    Documents Reviewed, Short Answer, Evidence Found (grouped by topic with source/line),
    Key Risks, Recommended Safeguards (deduplicated across topics), Suggested Next Actions,
    Limitations and Responsible Use, Notes for Reviewer; falls back to generating
    short_answer if not provided in brief_data
  - `create_brief_filename(title)` — lowercase slug with hyphens + `.md`; returns
    `document-intelligence-mini-brief.md` for empty titles
- Replaced Mini Brief page in `app.py` entirely:
  - 4 preset buttons (Learner Data / Safeguarding / Output Quality / Lesson Planning)
    using session-state pre-fill pattern; each preset sets title, question, and topics
  - Brief title text_input with `key="mb_title"`
  - 6 suggested question buttons (2 rows of 3) using session-state pre-fill pattern
  - Policy question text_input with `key="mb_question"`
  - Topic multiselect with `key="mb_topics"` and `get_supported_topics()` options
  - Scope radio (all documents / specific document)
  - "Generate brief" button: extracts evidence per topic, takes top 3 per topic,
    builds risk summary, generates short answer + next actions, assembles brief_data,
    calls `generate_markdown_brief`, stores result in session state
  - Results: 3-column metrics (topics / evidence snippets / risk areas), short answer
    info box, full brief preview in expander, Markdown download button
- Updated imports in `app.py`: added `generate_short_answer`, `generate_next_actions`,
  `create_brief_filename` from brief_generator; added `summarise_evidence_for_topic`
  from risk_summary
- Created `tests/test_brief_generator.py` — 41 tests covering all 5 public functions:
  generate_short_answer, deduplicate_list, generate_next_actions,
  generate_markdown_brief, create_brief_filename
- Version bumped to v0.5

## Phase 5 Notes (2026-06-10)

**Phase 5: Risk and Safeguard Summary**

- Created `src/risk_summary.py` from scratch:
  - `_RISK_MAPPING` — deterministic dict mapping 13 topics to risk record
    (risk_title, risk_description, why_it_matters, recommended_safeguards, suggested_owner)
  - `_RESPONSIBLE_USE_TEXT` — shared disclaimer string used in Markdown output
  - `get_risk_mapping()` — returns the full mapping dict
  - `get_risk_summary_for_topic(topic)` — returns the risk record for one topic, or `{}`
    for unknown topics; case-insensitive lookup
  - `summarise_evidence_for_topic(topic, evidence_results, max_items=3)` — filters evidence
    by topic, sorts by `relevance_count` descending, returns up to `max_items`
  - `_coverage_note(count)` — returns a short note based on evidence count
    (0 → no direct evidence; 1 → limited; ≥2 → multiple)
  - `generate_risk_safeguard_summary(topics, evidence_results)` — builds a summary item
    per supported topic; unsupported topics are silently skipped; `evidence_count` is the
    total (not capped to 3), `evidence_items` is the top-3 by relevance
  - `get_overall_summary(summary_items)` — counts topics reviewed/with/without evidence,
    sums total snippets, derives overall_note based on coverage
  - `generate_risk_summary_markdown(summary_items, overall_summary)` — Markdown document
    with Overall Summary, Topic Summaries, Responsible Use and Limitations sections
- Rewrote Risk and Safeguard Summary page in `app.py`:
  - 4 suggested topic set buttons (AI governance basics / Data protection /
    Safeguarding boundary / Output quality) using session-state pre-fill pattern
  - Topic multiselect with `key="rs_topics"` reads from session state
  - Scope radio (all documents / specific document)
  - "Generate summary" button → runs `extract_evidence_from_documents` or
    `extract_policy_evidence` per topic, then `generate_risk_safeguard_summary`
    and `get_overall_summary`; stores results in session state so they persist
  - Overall metrics row (4 columns: topics reviewed, with evidence, no evidence,
    total snippets) + overall note
  - Per-topic expander: risk + why-it-matters column, suggested owner info box,
    recommended safeguards list, top evidence snippets with doc/line, coverage note
  - "Responsible use and limitations" expander
  - "Download risk summary as Markdown" download button
- Updated `app.py` imports to include `generate_risk_safeguard_summary`,
  `get_overall_summary`, `generate_risk_summary_markdown`
- Created `tests/test_risk_summary.py` — 40 tests covering all 6 public functions:
  RISK_MAPPING, get_risk_summary_for_topic, summarise_evidence_for_topic,
  generate_risk_safeguard_summary, get_overall_summary, generate_risk_summary_markdown.
- Version bumped to v0.4.

## Phase 4 Notes (2026-06-10)

**Phase 4: Evidence Extraction by Topic**

- Expanded `TOPIC_KEYWORDS` in `src/evidence_extractor.py` from 9 to 13 topics:
  added `data minimisation`, `anonymisation`, `retention`, `incident reporting`.
  Each topic has a detailed keyword list matched case-insensitively against document lines.
- Added `_TOPIC_DESCRIPTIONS` dict — short explanation of what each topic is useful for,
  displayed in the Evidence Extraction page topic info box.
- Added four new public functions:
  - `get_supported_topics()` — returns all topic names from TOPIC_KEYWORDS
  - `get_topic_keywords(topic)` — returns keyword list for a topic; empty list for unknown topics
  - `get_topic_description(topic)` — returns the description string for a topic
  - `extract_evidence_from_documents(documents, topic)` — extracts across multiple docs,
    returns flat list sorted by `relevance_count` descending
- Updated `extract_policy_evidence(text, topic, document_name="")`:
  - Added `document_name=""` parameter
  - Result key `text` renamed to `evidence_text`
  - Added `relevance_count` (total keyword occurrences in matched line)
  - Added `document_name` to each result
  - Unsupported topics now return empty list (previously fell back to topic-as-keyword)
  - Added deduplication of identical snippets
  - Results sorted by `relevance_count` descending
- Rewrote Evidence Extraction page in `app.py`:
  - 5 suggested-topic buttons (learner data, safeguarding, human review, approved tools, hallucination)
  - Session-state pre-fill pattern: buttons set `st.session_state["ev_topic"]` then `st.rerun()`
  - Topic selectbox with `key="ev_topic"` reads from session state
  - Topic explanation box: selected topic, keyword list, useful-for description
  - Scope radio (all documents / specific document)
  - "Extract evidence" button triggers `extract_evidence_from_documents` or `extract_policy_evidence`
  - Results: document name, line number, relevance count, evidence snippet, matched keywords
  - "How to interpret extracted evidence" expander with responsible-use caveats
- Updated Risk and Safeguard Summary page to use `get_supported_topics()` (all 13 topics)
  and `r['evidence_text']` (renamed from `r['text']`).
- Updated `src/sample_data.py` `DEMO_TOPICS` to include all 13 topics.
- Rewrote `tests/test_evidence_extractor.py` — 44 tests (was 16), covering all functions:
  `TOPIC_KEYWORDS`, `get_supported_topics`, `get_topic_keywords`,
  `extract_sentences_with_keywords`, `extract_policy_evidence`, `extract_evidence_from_documents`.
- Version bumped to v0.3.

## Phase 3 Notes (2026-06-10)

**Phase 3: Keyword Search Across Documents**

- Rewrote `src/simple_search.py` with four functions:
  - `normalise_text(text)` — lowercase and strip whitespace
  - `tokenise_query(query)` — split on whitespace, filter stop words, return lowercase tokens;
    preserves policy-meaningful terms like "not", "must", "HR", "AI"
  - `search_document(text, query, document_name="")` — multi-term case-insensitive search;
    deduplicates identical snippets; returns `document_name`, `line_number`, `snippet`,
    `relevance_count` (total term occurrences), `matched_terms` (list of matching tokens)
  - `search_documents(documents, query)` — calls `search_document` across all docs,
    returns flat list sorted by `relevance_count` descending
- Updated `app.py` — Policy Q&A page fully functional: suggested searches (8 buttons),
  free-text query input with session state, scope selector (all docs / specific doc),
  results with document name + line number + relevance count + matched terms,
  "How to interpret results" expander, future-phase note. Document Viewer also shows
  matched terms. Version bumped to v0.2.
- Rewrote `tests/test_simple_search.py` — 36 tests covering all four functions including
  `normalise_text`, `tokenise_query` stop word filtering, deduplication, `matched_terms`,
  `relevance_count`, `document_name`, stop-word-only query returning empty list.

## Phase 1 Notes (2026-06-10)

### Folder structure

- `app.py` — 7-page Streamlit app with sidebar navigation
- `src/document_loader.py` — `list_documents`, `load_document`, `get_document_metadata`
- `src/simple_search.py` — `search_document`, `search_documents`
- `src/evidence_extractor.py` — `extract_sentences_with_keywords`, `extract_policy_evidence`,
  `TOPIC_KEYWORDS` (9 topics: learner data, safeguarding, human review, approved tools,
  accountability, bias, hallucination, copyright, escalation)
- `src/brief_generator.py` — `generate_markdown_brief`
- `src/sample_data.py` — `DOCS_DIR`, `DEMO_TOPICS`, `DEMO_QUERIES`, `DEMO_BRIEF_DATA`

### Synthetic documents created

Four synthetic Markdown policy documents, each 400–700 words, stored in
`data/synthetic_documents/`:

1. `synthetic-ai-acceptable-use-policy.md` — purpose, approved/prohibited use, learner data,
   safeguarding, human review, accountability, escalation
2. `synthetic-data-protection-guidance.md` — data minimisation, anonymisation, approved tools,
   access control, retention, DPIA placeholder, incident reporting
3. `synthetic-safeguarding-and-ai-boundaries.md` — safeguarding AI boundary, escalation,
   AI decision-making limits, safe/unsafe prompt examples, human-led decision-making
4. `synthetic-staff-ai-training-notes.md` — safe prompting, checking outputs, hallucination
   risk, bias and fairness, copyright awareness, when to ask a manager, safe use examples

All documents are fictional. All contain "Synthetic — for demonstration purposes only" in the header.

### Tests

Three test files covering:
- `tests/test_document_loader.py` — 15 tests (list, load, metadata)
- `tests/test_simple_search.py` — 16 tests (single-doc search, multi-doc search)
- `tests/test_evidence_extractor.py` — 16 tests (sentence extraction, policy evidence, topics dict)

All tests pass using `pytest` from the project root.

### App pages

| Page | Implementation |
|---|---|
| Home | Welcome, document list, responsible-use warning |
| Document Library | Metadata table with expanders |
| Document Viewer | Full document + inline keyword search |
| Evidence Extraction | Topic selector + multi-doc extraction |
| Policy Q&A | Placeholder with future-phase description |
| Risk and Safeguard Summary | Cross-document summary across all 9 topics |
| Mini Brief | Editable form, demo loader, preview, Markdown download |

### Design decisions

- **No external dependencies beyond streamlit, pandas, pytest** — keeps the prototype
  self-contained and easy to understand
- **Keyword lists in `TOPIC_KEYWORDS`** — explicit, auditable, easy to extend without
  changing function signatures
- **`@st.cache_data` on document loading** — documents are loaded once per session,
  not on every page render
- **Pre-fill pattern for Mini Brief** — same session state pattern as Build 1
- **All pages show the safety notice** — normalises the responsible-use message

### Safety boundaries preserved

- No real data used anywhere
- No external API calls
- No database or authentication
- Responsible-use warning on every page
- Synthetic documents explicitly labelled as fictional in their headers
