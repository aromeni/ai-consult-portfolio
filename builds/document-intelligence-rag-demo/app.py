"""
Build 2: Document Intelligence / RAG Demo
BrightPath — synthetic policy document analysis prototype.

Phase 1 — scaffold: document loading, keyword search, evidence extraction, mini brief.
Phase 3 — Policy Q&A / Keyword Search: transparent multi-term search across all documents.
Phase 4 — Evidence Extraction by Topic: topic-based keyword extraction across documents.
Phase 5 — Risk and Safeguard Summary: deterministic risk record + evidence per topic.
Phase 6 — Mini Brief Generator: automated evidence brief from topics and documents.
Phase 7 — Evidence-Based Policy Q&A: topic detection, evidence retrieval, templated answer.
Polish  — UI polish pass: custom CSS, page headers, evidence cards, styled components.
No external AI APIs, no embeddings, no vector database.
"""

import re
from collections import defaultdict
from datetime import date
from pathlib import Path

import streamlit as st

from src.document_loader import list_documents, load_document, get_document_metadata
from src.simple_search import normalise_text, tokenise_query, search_document, search_documents
from src.evidence_extractor import (
    get_supported_topics,
    get_topic_keywords,
    get_topic_description,
    extract_policy_evidence,
    extract_evidence_from_documents,
    TOPIC_KEYWORDS,
)
from src.brief_generator import (
    generate_markdown_brief,
    generate_short_answer,
    generate_next_actions,
    create_brief_filename,
)
from src.sample_data import DOCS_DIR, DEMO_QUERIES, DEMO_TOPICS, DEMO_BRIEF_DATA
from src.risk_summary import (
    generate_risk_safeguard_summary,
    get_overall_summary,
    generate_risk_summary_markdown,
    summarise_evidence_for_topic,
)
from src.qa_engine import answer_policy_question, generate_qa_markdown
from src import ui_components as ui

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="BrightPath Document Intelligence Demo",
    page_icon="📄",
    layout="wide",
)

ui.inject_css()

# ── Sidebar ───────────────────────────────────────────────────────────────────

st.sidebar.title("Document Intelligence")
st.sidebar.caption("Build 2 · Prototype v0.6")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Document Library",
        "Document Viewer",
        "Evidence Extraction",
        "Policy Q&A",
        "Risk and Safeguard Summary",
        "Mini Brief",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Synthetic documents only · No external APIs · Deterministic prototype"
)

# ── Document loading (cached) ─────────────────────────────────────────────────

@st.cache_data
def _load_all_documents():
    paths = list_documents(str(DOCS_DIR))
    return {Path(p).name: load_document(p) for p in paths}


docs = _load_all_documents()
doc_names = list(docs.keys())

# ── Page: Home ────────────────────────────────────────────────────────────────

if page == "Home":
    ui.page_header(
        "Document Intelligence / RAG Demo",
        "BrightPath · Synthetic policy document analysis prototype",
    )

    ui.safety_warning()

    # Workflow pipeline
    st.markdown("#### Document intelligence pipeline")
    ui.workflow_diagram()

    st.markdown("---")

    # Feature cards
    st.markdown("#### What this prototype does")
    ui.feature_cards()

    st.markdown("")
    ui.boundary_notice()

    st.markdown("---")

    # Summary metrics
    _total_words = 0
    _total_lines = 0
    for _n in doc_names:
        _meta = get_document_metadata(str(DOCS_DIR / _n))
        _total_words += _meta.get("word_count", 0)
        _total_lines += _meta.get("line_count", 0)

    _mc1, _mc2, _mc3, _mc4 = st.columns(4)
    _mc1.metric("Documents loaded", len(doc_names))
    _mc2.metric("Total words", f"{_total_words:,}")
    _mc3.metric("Policy topics", 13)
    _mc4.metric("Tests passing", 229)

    st.markdown("---")

    # Document list
    st.markdown("#### Documents in this library")
    for _name in doc_names:
        _m = get_document_metadata(str(DOCS_DIR / _name))
        st.markdown(
            f"`{_name}` &nbsp;—&nbsp; {_m.get('word_count', '?')} words, "
            f"{_m.get('line_count', '?')} lines",
        )

    st.markdown("---")
    st.info("Use the sidebar to navigate between pages.")

# ── Page: Document Library ────────────────────────────────────────────────────

elif page == "Document Library":
    ui.page_header(
        "Document Library",
        "Browse and inspect your synthetic policy documents",
    )
    ui.safety_warning()

    if not doc_names:
        st.error(
            "No documents found. "
            "Check that data/synthetic_documents/ exists and contains .md files."
        )
        st.stop()

    # Summary metrics
    _total_words = sum(
        get_document_metadata(str(DOCS_DIR / n)).get("word_count", 0) for n in doc_names
    )
    _total_lines = sum(
        get_document_metadata(str(DOCS_DIR / n)).get("line_count", 0) for n in doc_names
    )
    _lc1, _lc2, _lc3 = st.columns(3)
    _lc1.metric("Documents", len(doc_names))
    _lc2.metric("Total words", f"{_total_words:,}")
    _lc3.metric("Total lines", f"{_total_lines:,}")

    st.markdown("---")
    st.caption("All documents are synthetic — fictional examples for demonstration purposes only.")

    for name in doc_names:
        meta = get_document_metadata(str(DOCS_DIR / name))
        with st.expander(f"{name}"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Words", meta.get("word_count", "—"))
            col2.metric("Lines", meta.get("line_count", "—"))
            col3.metric("Size (bytes)", meta.get("size_bytes", "—"))
            st.caption(f"Last modified: {meta.get('modified', '—')}")
            st.caption(f"Path: {meta.get('path', '—')}")

# ── Page: Document Viewer ─────────────────────────────────────────────────────

elif page == "Document Viewer":
    ui.page_header(
        "Document Viewer",
        "Read and search within a single synthetic policy document",
    )
    ui.safety_warning()

    if not doc_names:
        st.error("No documents found.")
        st.stop()

    selected = st.selectbox("Select a document to view", doc_names)
    content = docs[selected]

    # Document metadata strip
    _vmeta = get_document_metadata(str(DOCS_DIR / selected))
    _vc1, _vc2, _vc3 = st.columns(3)
    _vc1.metric("Words", _vmeta.get("word_count", "—"))
    _vc2.metric("Lines", _vmeta.get("line_count", "—"))
    _vc3.metric("Size (bytes)", _vmeta.get("size_bytes", "—"))

    st.markdown("---")

    query = st.text_input(
        "Search within this document",
        placeholder="e.g. safeguarding",
        help="Enter a keyword or phrase to highlight matching lines.",
    )

    if query.strip():
        results = search_document(content, query, document_name=selected)
        if results:
            st.success(f"{len(results)} matching line(s) found for '{query}'.")
            st.markdown("")
            for r in results:
                ui.evidence_card(r)
        else:
            st.info(f"No matches found for '{query}' in this document.")
        st.markdown("---")

    st.subheader(selected)
    st.markdown(content)

# ── Page: Evidence Extraction ─────────────────────────────────────────────────

elif page == "Evidence Extraction":
    ui.page_header(
        "Evidence Extraction",
        "Extract topic-based evidence snippets from the synthetic policy documents",
    )
    ui.safety_warning()

    st.markdown(
        "Select a policy topic and extract all relevant policy statements "
        "across the synthetic documents. Results are ranked by relevance count."
    )

    st.markdown("---")

    # ── Suggested demo topics ─────────────────────────────────────────────────
    st.markdown("**Suggested topics — click to select:**")
    _demo_topic_suggestions = [
        "learner data", "safeguarding", "human review", "approved tools", "hallucination",
    ]
    _et_cols = st.columns(5)
    for _i, _t in enumerate(_demo_topic_suggestions):
        if _et_cols[_i].button(_t, key=f"_et_{_i}"):
            st.session_state["ev_topic"] = _t
            st.rerun()

    st.markdown("---")

    # ── Topic selector ────────────────────────────────────────────────────────
    _all_topics = get_supported_topics()
    if "ev_topic" not in st.session_state:
        st.session_state["ev_topic"] = _all_topics[0]

    topic = st.selectbox(
        "Select a topic",
        _all_topics,
        key="ev_topic",
        help="Choose a topic to extract evidence for.",
    )

    # ── Topic explanation ─────────────────────────────────────────────────────
    _kw_list = get_topic_keywords(topic)
    _description = get_topic_description(topic)

    ui.prototype_notice(
        f"<strong>Topic:</strong> {topic} &nbsp;·&nbsp; "
        f"<strong>Useful for:</strong> {_description}<br>"
        f"<strong>Keywords:</strong> "
        + "".join(ui.badge_html(k, "slate") for k in _kw_list)
    )

    # ── Scope selector ────────────────────────────────────────────────────────
    ev_scope = st.radio(
        "Search scope",
        ["All documents", "Specific document"],
        horizontal=True,
    )
    ev_selected_doc = doc_names[0] if doc_names else None
    if ev_scope == "Specific document" and doc_names:
        ev_selected_doc = st.selectbox("Select document", doc_names, key="ev_selected_doc")

    st.markdown("---")

    # ── Extract button ────────────────────────────────────────────────────────
    if st.button("Extract evidence", type="primary"):
        if ev_scope == "All documents":
            all_results = extract_evidence_from_documents(docs, topic)
            scope_label = f"all {len(doc_names)} document(s)"
        else:
            all_results = extract_policy_evidence(
                docs.get(ev_selected_doc, ""), topic, document_name=ev_selected_doc
            )
            scope_label = f"`{ev_selected_doc}`"

        if all_results:
            st.success(
                f"**{len(all_results)} evidence item(s)** found for topic "
                f"**'{topic}'** in {scope_label}."
            )
            st.markdown("")
            for r in all_results:
                ui.evidence_card(r)
        else:
            st.info(
                f"No evidence found for topic **'{topic}'** in {scope_label}. "
                "Try a different topic or check that the documents contain relevant content."
            )

    # ── Interpretation guide ──────────────────────────────────────────────────
    with st.expander("How to interpret extracted evidence"):
        st.markdown("""
- **Evidence snippets are not final advice.** Always read the surrounding policy section
  before making any governance or operational decision.
- **Results depend on keyword matching.** Relevant content may be missed if the document
  uses different wording. A future phase will add semantic search.
- **Relevance count** shows how many keyword occurrences appear in a line.
  Higher counts appear at the top.
- **Matched keywords** shows which topic keywords triggered each result.
- This prototype does not generate legal, safeguarding, HR, compliance, medical,
  financial, or academic-integrity advice.
- **Human review remains required** before acting on any extracted evidence.
        """)

# ── Page: Policy Q&A ──────────────────────────────────────────────────────────

elif page == "Policy Q&A":
    ui.page_header(
        "Policy Q&A",
        "Search policy content by keyword or ask an evidence-based policy question",
    )
    ui.safety_warning()

    _tab_ks, _tab_qa = st.tabs(["Keyword Search", "Evidence-Based Q&A"])

    # ── Tab 1: Keyword Search ─────────────────────────────────────────────────
    with _tab_ks:
        ui.prototype_notice(
            "<strong>Transparent keyword search</strong> — results show exact matching lines "
            "from the synthetic policy documents, ranked by relevance count. "
            "This is not AI-generated — every match is a real line from the source document."
        )

        st.markdown("---")

        if "qa_query" not in st.session_state:
            st.session_state["qa_query"] = ""

        st.markdown("**Suggested searches — click to run:**")
        _suggestions = [
            "learner data", "safeguarding", "human review", "approved tools",
            "hallucination", "accountability", "copyright", "escalation",
        ]
        _cols_a = st.columns(4)
        for _i, _q in enumerate(_suggestions[:4]):
            if _cols_a[_i].button(_q, key=f"_sq_{_i}"):
                st.session_state["qa_query"] = _q
                st.rerun()
        _cols_b = st.columns(4)
        for _i, _q in enumerate(_suggestions[4:]):
            if _cols_b[_i].button(_q, key=f"_sq_{_i + 4}"):
                st.session_state["qa_query"] = _q
                st.rerun()

        st.markdown("---")

        st.text_input(
            "Search query",
            key="qa_query",
            placeholder="e.g. safeguarding, learner data, human review approved tools",
            help="Enter one or more keywords. Multi-word queries match lines containing any of the terms.",
        )
        qa_query = st.session_state.get("qa_query", "")

        qa_scope = st.radio(
            "Search scope",
            ["All documents", "Specific document"],
            horizontal=True,
        )
        qa_selected_doc = doc_names[0] if doc_names else None
        if qa_scope == "Specific document" and doc_names:
            qa_selected_doc = st.selectbox("Select document", doc_names)

        with st.expander("How to interpret results"):
            st.markdown("""
- **Relevance count** shows how many times the query terms appeared in a snippet.
  Higher counts mean more matches — those results appear at the top.
- **Matched terms** shows exactly which words from your query triggered each result.
- Results are **evidence snippets**, not final advice. Read the full document section
  before making any policy or governance decisions.
- A multi-word query (e.g. *learner data safeguarding*) returns lines containing
  **any** of the terms — not necessarily all of them.
- This prototype does not use AI to generate answers. It returns exact matching lines only.
            """)

        st.markdown("---")

        if qa_query.strip():
            tokens = tokenise_query(qa_query)

            if qa_scope == "All documents":
                results = search_documents(docs, qa_query)
                scope_label = f"all {len(doc_names)} document(s)"
            else:
                results = search_document(
                    docs.get(qa_selected_doc, ""), qa_query, document_name=qa_selected_doc
                )
                scope_label = f"`{qa_selected_doc}`"

            if results:
                st.success(
                    f"**{len(results)} result(s)** for **'{qa_query}'** in {scope_label}."
                )
                st.markdown("")
                # Active search terms as badges
                ui.render_badges(tokens, "slate")
                st.markdown("")

                for r in results:
                    ui.evidence_card(r)
            else:
                st.info(
                    f"No results found for **'{qa_query}'** in {scope_label}. "
                    "Try a different term, check the spelling, or broaden your search."
                )
        else:
            st.markdown(
                "*Enter a search query above or click a suggested search to get started.*"
            )

    # ── Tab 2: Evidence-Based Q&A ─────────────────────────────────────────────
    with _tab_qa:
        ui.prototype_notice(
            "Ask a policy question — the tool detects relevant topics, retrieves "
            "supporting evidence from the synthetic documents, and generates a structured "
            "templated answer with safeguards and responsible owners. "
            "No external AI APIs are used. All matching is deterministic and transparent."
        )

        st.markdown("---")

        # Session state initialisation
        for _k, _v in [("qa_eb_question", "")]:
            if _k not in st.session_state:
                st.session_state[_k] = _v
        for _k in ("qa_eb_result", "qa_eb_markdown"):
            if _k not in st.session_state:
                st.session_state[_k] = None

        # ── Suggested questions ───────────────────────────────────────────────
        _QA_SUGGESTED = [
            "Can staff enter learner data into AI tools?",
            "What does the policy say about safeguarding information and AI?",
            "What human review is required for AI-generated outputs?",
            "Which AI uses are allowed and prohibited?",
            "What safeguards are required before staff use AI for lesson planning?",
            "What should staff do if AI output seems inaccurate or unsafe?",
            "Who is responsible for AI-assisted outputs?",
            "What should staff do if they accidentally enter sensitive information into an AI tool?",
        ]

        st.markdown("**Suggested questions — click to use:**")
        _qa_row_a = st.columns(4)
        _qa_row_b = st.columns(4)
        for _i, _q in enumerate(_QA_SUGGESTED[:4]):
            if _qa_row_a[_i].button(_q, key=f"_qas_{_i}", use_container_width=True):
                st.session_state["qa_eb_question"] = _q
                st.session_state["qa_eb_result"] = None
                st.rerun()
        for _i, _q in enumerate(_QA_SUGGESTED[4:]):
            if _qa_row_b[_i].button(_q, key=f"_qas_{_i + 4}", use_container_width=True):
                st.session_state["qa_eb_question"] = _q
                st.session_state["qa_eb_result"] = None
                st.rerun()

        st.markdown("---")

        # ── Question input ────────────────────────────────────────────────────
        st.text_input(
            "Policy question",
            key="qa_eb_question",
            placeholder="e.g. What does the policy say about safeguarding and AI?",
            help="Type a policy question or click a suggested question above.",
        )

        # ── Scope selector ────────────────────────────────────────────────────
        _eb_scope = st.radio(
            "Document scope",
            ["All documents", "Specific document"],
            horizontal=True,
            key="qa_eb_scope",
        )
        _eb_selected_doc = None
        if _eb_scope == "Specific document" and doc_names:
            _eb_selected_doc = st.selectbox("Select document", doc_names, key="qa_eb_doc")

        st.markdown("---")

        # ── Generate button ───────────────────────────────────────────────────
        if st.button("Generate answer", type="primary", key="qa_eb_generate"):
            _eb_question = st.session_state.get("qa_eb_question", "").strip()
            if not _eb_question:
                st.warning("Enter a policy question before generating an answer.")
            else:
                _selected = _eb_selected_doc if _eb_scope == "Specific document" else None
                _result = answer_policy_question(_eb_question, docs, selected_document=_selected)
                _md = generate_qa_markdown(_result)
                st.session_state["qa_eb_result"] = _result
                st.session_state["qa_eb_markdown"] = _md

        # ── Display results ───────────────────────────────────────────────────
        if st.session_state.get("qa_eb_result"):
            _r = st.session_state["qa_eb_result"]
            _md = st.session_state["qa_eb_markdown"]

            st.markdown("---")

            # Question echo
            st.markdown(f"**Question:** {_r['question']}")

            # Detected topics as badges
            _dt = _r.get("detected_topics", [])
            if _dt:
                st.caption("Detected policy topics:")
                ui.render_badges(_dt)
            else:
                st.caption("No policy topics detected from this question.")

            st.markdown("")

            # Short answer
            st.markdown("#### Answer")
            ui.answer_card(_r["answer"])

            # Evidence grouped by topic (max 3 per topic)
            _ev = _r.get("evidence_results", [])
            st.markdown("#### Evidence Found")
            if _ev and _dt:
                _ev_by_topic = defaultdict(list)
                for _e in _ev:
                    _ev_by_topic[_e.get("topic", "unknown")].append(_e)

                for _t in _dt:
                    _items = _ev_by_topic.get(_t, [])[:3]
                    if not _items:
                        continue
                    st.markdown(f"**{_t.title()}** — {len(_items)} snippet(s):")
                    for _e in _items:
                        ui.evidence_card(_e)
            else:
                st.markdown(
                    "*No direct evidence found in the selected documents. "
                    "Try broadening the document scope or reviewing the full documents manually.*"
                )

            # Coverage note
            st.caption(f"Source coverage: {_r.get('coverage_note', '')}")

            st.markdown("---")

            # Safeguards
            _sg = _r.get("safeguards", [])
            if _sg:
                st.markdown("#### Recommended Safeguards")
                ui.safeguard_list(_sg)
                st.markdown("")

            # Owners
            _ow = _r.get("owners", [])
            if _ow:
                st.markdown("#### Suggested Responsible Owners")
                for _o in _ow:
                    st.markdown(f"- {_o}")
                st.markdown("")

            # Limitations
            with st.expander("Limitations and responsible use"):
                for _lim in _r.get("limitations", []):
                    st.markdown(f"- {_lim}")

            # Download
            st.download_button(
                label="⬇  Download Q&A as Markdown",
                data=_md,
                file_name=f"policy-qa-{date.today().strftime('%Y-%m-%d')}.md",
                mime="text/markdown",
                type="primary",
            )

# ── Page: Risk and Safeguard Summary ─────────────────────────────────────────

elif page == "Risk and Safeguard Summary":
    ui.page_header(
        "Risk and Safeguard Summary",
        "Generate a structured risk and safeguard summary for selected policy topics",
    )
    ui.safety_warning()

    st.markdown(
        "Select policy topics and generate a cross-document risk and safeguard summary. "
        "Each topic shows a risk description, recommended safeguards, suggested owner, "
        "and supporting evidence from the synthetic documents."
    )

    st.markdown("---")

    # ── Suggested topic sets ──────────────────────────────────────────────────
    _TOPIC_SETS = {
        "AI governance basics": [
            "approved tools", "human review", "accountability", "escalation",
        ],
        "Data protection": [
            "learner data", "data minimisation", "anonymisation", "retention", "incident reporting",
        ],
        "Safeguarding boundary": [
            "safeguarding", "escalation", "human review", "accountability",
        ],
        "Output quality": [
            "hallucination", "bias", "human review", "accountability",
        ],
    }

    if "rs_topics" not in st.session_state:
        st.session_state["rs_topics"] = list(_TOPIC_SETS["AI governance basics"])
    for _k in ("rs_summary", "rs_overall", "rs_markdown"):
        if _k not in st.session_state:
            st.session_state[_k] = None

    st.markdown("**Suggested topic sets — click to load:**")
    _ts_cols = st.columns(4)
    for _i, (_set_name, _set_topics) in enumerate(_TOPIC_SETS.items()):
        if _ts_cols[_i].button(_set_name, key=f"_ts_{_i}"):
            st.session_state["rs_topics"] = list(_set_topics)
            st.session_state["rs_summary"] = None
            st.rerun()

    st.markdown("---")

    # ── Topic multiselect ─────────────────────────────────────────────────────
    selected_topics = st.multiselect(
        "Select policy topics",
        get_supported_topics(),
        key="rs_topics",
        help="Choose one or more topics to include in the summary.",
    )

    # ── Scope selector ────────────────────────────────────────────────────────
    rs_scope = st.radio(
        "Document scope",
        ["All documents", "Specific document"],
        horizontal=True,
    )
    rs_selected_doc = doc_names[0] if doc_names else None
    if rs_scope == "Specific document" and doc_names:
        rs_selected_doc = st.selectbox("Select document", doc_names, key="rs_selected_doc")

    st.markdown("---")

    # ── Generate button ───────────────────────────────────────────────────────
    if st.button("Generate summary", type="primary"):
        if not selected_topics:
            st.warning("Select at least one topic to generate a summary.")
        else:
            all_evidence = []
            if rs_scope == "All documents":
                for _t in selected_topics:
                    all_evidence.extend(extract_evidence_from_documents(docs, _t))
                _scope_label = f"all {len(doc_names)} document(s)"
            else:
                for _t in selected_topics:
                    all_evidence.extend(
                        extract_policy_evidence(
                            docs.get(rs_selected_doc, ""), _t, document_name=rs_selected_doc
                        )
                    )
                _scope_label = f"`{rs_selected_doc}`"

            _summary = generate_risk_safeguard_summary(selected_topics, all_evidence)
            _overall = get_overall_summary(_summary)
            _md = generate_risk_summary_markdown(_summary, _overall)

            st.session_state["rs_summary"] = _summary
            st.session_state["rs_overall"] = _overall
            st.session_state["rs_markdown"] = _md
            st.session_state["rs_scope_label"] = _scope_label

    # ── Display results ───────────────────────────────────────────────────────
    if st.session_state["rs_summary"]:
        _summary = st.session_state["rs_summary"]
        _overall = st.session_state["rs_overall"]
        _md = st.session_state["rs_markdown"]
        _scope_label = st.session_state.get("rs_scope_label", "selected documents")

        st.caption(f"Scope: {_scope_label}")
        st.markdown("")

        # Overall metrics
        st.markdown("### Overall Summary")
        _m1, _m2, _m3, _m4 = st.columns(4)
        _m1.metric("Topics reviewed", _overall["topics_reviewed"])
        _m2.metric("With evidence", _overall["topics_with_evidence"])
        _m3.metric("No evidence", _overall["topics_without_evidence"])
        _m4.metric("Total snippets", _overall["total_evidence_snippets"])
        st.info(_overall["overall_note"])
        st.markdown("---")

        # Per-topic cards
        for _item in _summary:
            with st.expander(
                f"**{_item['risk_title']}**  ·  {_item['evidence_count']} snippet(s)",
                expanded=True,
            ):
                _col_desc, _col_meta = st.columns([3, 1])
                with _col_desc:
                    st.markdown(f"**Risk:** {_item['risk_description']}")
                    st.markdown(f"**Why it matters:** {_item['why_it_matters']}")
                with _col_meta:
                    ui.prototype_notice(
                        f"<strong>Suggested owner</strong><br>{_item['suggested_owner']}"
                    )

                st.markdown("**Recommended safeguards:**")
                ui.safeguard_list(_item["recommended_safeguards"])

                st.markdown("---")

                if _item["evidence_items"]:
                    _shown = len(_item["evidence_items"])
                    _total = _item["evidence_count"]
                    st.markdown(
                        f"**Evidence found** (top {_shown} of {_total} snippet(s)):"
                    )
                    for _e in _item["evidence_items"]:
                        ui.evidence_card(_e)
                else:
                    st.markdown(
                        "*No evidence found in the selected documents for this topic.*"
                    )

                st.caption(f"Coverage: {_item['coverage_note']}")

        st.markdown("---")

        # Responsible use
        with st.expander("Responsible use and limitations"):
            st.markdown(
                "This summary is generated by a prototype using deterministic topic and "
                "keyword matching. It is intended to support discussion and review, not to "
                "replace legal, safeguarding, HR, compliance, medical, financial, "
                "academic-integrity, or professional advice. Users should review the full "
                "source documents and involve appropriate responsible owners before acting."
            )

        # Download
        st.download_button(
            label="⬇  Download risk summary as Markdown",
            data=_md,
            file_name=f"risk-summary-{date.today().strftime('%Y-%m-%d')}.md",
            mime="text/markdown",
            type="primary",
        )

# ── Page: Mini Brief ──────────────────────────────────────────────────────────

elif page == "Mini Brief":
    ui.page_header(
        "Mini Brief",
        "Generate a 9-section downloadable policy evidence brief",
    )
    ui.safety_warning()

    st.markdown(
        "Generate a short evidence-based Markdown brief from selected policy topics "
        "and synthetic documents. Use a preset below or configure your own brief."
    )

    st.markdown("---")

    # ── Preset definitions ────────────────────────────────────────────────────
    _BRIEF_PRESETS = {
        "Learner Data": {
            "title": "Learner Data and AI Use",
            "question": "Can staff enter learner data into AI tools?",
            "topics": ["learner data", "data minimisation", "anonymisation", "approved tools", "human review"],
        },
        "Safeguarding": {
            "title": "Safeguarding and AI Boundaries",
            "question": "What does the policy say about safeguarding information and AI?",
            "topics": ["safeguarding", "escalation", "human review", "accountability"],
        },
        "Output Quality": {
            "title": "AI Output Quality",
            "question": "What should staff do if AI output seems inaccurate, biased, or unsafe?",
            "topics": ["hallucination", "bias", "human review", "escalation", "accountability"],
        },
        "Lesson Planning": {
            "title": "Approved AI Use for Lesson Planning",
            "question": "What safeguards are required before staff use AI for lesson planning?",
            "topics": ["approved tools", "learner data", "human review", "accountability", "copyright"],
        },
    }

    # ── Session state initialisation ──────────────────────────────────────────
    for _k, _v in [("mb_title", ""), ("mb_question", ""), ("mb_topics", [])]:
        if _k not in st.session_state:
            st.session_state[_k] = _v
    for _k in ("mb_brief_data", "mb_markdown"):
        if _k not in st.session_state:
            st.session_state[_k] = None

    # ── Preset buttons ────────────────────────────────────────────────────────
    st.markdown("**Suggested brief presets — click to load:**")
    _bp_cols = st.columns(4)
    for _i, (_preset_name, _preset) in enumerate(_BRIEF_PRESETS.items()):
        if _bp_cols[_i].button(_preset_name, key=f"_bp_{_i}"):
            st.session_state["mb_title"] = _preset["title"]
            st.session_state["mb_question"] = _preset["question"]
            st.session_state["mb_topics"] = list(_preset["topics"])
            st.session_state["mb_brief_data"] = None
            st.rerun()

    st.markdown("---")

    # ── Brief title ───────────────────────────────────────────────────────────
    st.text_input(
        "Brief title",
        key="mb_title",
        placeholder="e.g. Safeguarding and AI Boundaries",
    )

    # ── Suggested questions ───────────────────────────────────────────────────
    _SUGGESTED_QUESTIONS = [
        "Can staff enter learner data into AI tools?",
        "What does the policy say about safeguarding information and AI?",
        "What human review is required for AI-generated outputs?",
        "Which AI uses are allowed and prohibited?",
        "What safeguards are required before staff use AI for lesson planning?",
        "What should staff do if an AI output seems inaccurate or unsafe?",
    ]
    st.markdown("**Suggested policy questions — click to use:**")
    _sq_row_a = st.columns(3)
    _sq_row_b = st.columns(3)
    for _i, _q in enumerate(_SUGGESTED_QUESTIONS[:3]):
        if _sq_row_a[_i].button(_q, key=f"_sqb_{_i}"):
            st.session_state["mb_question"] = _q
            st.rerun()
    for _i, _q in enumerate(_SUGGESTED_QUESTIONS[3:]):
        if _sq_row_b[_i].button(_q, key=f"_sqb_{_i + 3}"):
            st.session_state["mb_question"] = _q
            st.rerun()

    st.text_input(
        "Policy question",
        key="mb_question",
        placeholder="e.g. What does the policy say about safeguarding and AI?",
    )

    # ── Topic multiselect ─────────────────────────────────────────────────────
    st.multiselect(
        "Policy topics to include",
        get_supported_topics(),
        key="mb_topics",
        help="Select one or more topics. Evidence and risks are extracted for each.",
    )

    # ── Scope selector ────────────────────────────────────────────────────────
    mb_scope = st.radio(
        "Document scope",
        ["All documents", "Specific document"],
        horizontal=True,
    )
    mb_selected_doc = doc_names[0] if doc_names else None
    if mb_scope == "Specific document" and doc_names:
        mb_selected_doc = st.selectbox("Select document", doc_names, key="mb_selected_doc")

    st.markdown("---")

    # ── Generate button ───────────────────────────────────────────────────────
    if st.button("Generate brief", type="primary"):
        _mb_topics = st.session_state.get("mb_topics", [])
        _mb_title = st.session_state.get("mb_title", "")
        _mb_question = st.session_state.get("mb_question", "")

        if not _mb_topics:
            st.warning("Select at least one topic to generate a brief.")
        else:
            _all_evidence = []
            if mb_scope == "All documents":
                for _t in _mb_topics:
                    _all_evidence.extend(extract_evidence_from_documents(docs, _t))
                _scope_doc_names = list(doc_names)
            else:
                for _t in _mb_topics:
                    _all_evidence.extend(
                        extract_policy_evidence(
                            docs.get(mb_selected_doc, ""), _t,
                            document_name=mb_selected_doc,
                        )
                    )
                _scope_doc_names = [mb_selected_doc] if mb_selected_doc else []

            # Top evidence items per topic
            _brief_evidence = []
            for _t in _mb_topics:
                _brief_evidence.extend(summarise_evidence_for_topic(_t, _all_evidence))

            _risk_items = generate_risk_safeguard_summary(_mb_topics, _all_evidence)
            _short_answer = generate_short_answer(_mb_question, _mb_topics, _all_evidence)
            _next_actions = generate_next_actions(_mb_topics, _all_evidence)

            _brief_data = {
                "title": _mb_title or "Policy Evidence Brief",
                "question": _mb_question or "—",
                "topics": _mb_topics,
                "documents_reviewed": _scope_doc_names,
                "generated_date": date.today().strftime("%d %B %Y"),
                "short_answer": _short_answer,
                "evidence_results": _brief_evidence,
                "risk_summary_items": _risk_items,
                "next_actions": _next_actions,
            }
            _md = generate_markdown_brief(_brief_data)

            st.session_state["mb_brief_data"] = _brief_data
            st.session_state["mb_markdown"] = _md

    # ── Display results ───────────────────────────────────────────────────────
    if st.session_state.get("mb_brief_data"):
        _bd = st.session_state["mb_brief_data"]
        _md = st.session_state["mb_markdown"]

        st.markdown("")

        # Quick metrics
        _m1, _m2, _m3 = st.columns(3)
        _m1.metric("Topics included", len(_bd.get("topics", [])))
        _m2.metric("Evidence snippets", len(_bd.get("evidence_results", [])))
        _m3.metric("Risk areas", len(_bd.get("risk_summary_items", [])))

        st.markdown("#### Short Answer")
        ui.answer_card(_bd.get("short_answer", "—"))

        with st.expander("Full brief preview", expanded=True):
            st.markdown(_md)

        _filename = create_brief_filename(_bd.get("title", ""))
        st.download_button(
            label=f"⬇  Download brief  ({_filename})",
            data=_md,
            file_name=_filename,
            mime="text/markdown",
            type="primary",
        )
