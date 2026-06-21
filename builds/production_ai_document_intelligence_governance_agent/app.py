"""
Build 10 — Production AI Document Intelligence & Governance Agent
Streamlit multi-page application.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from logic import ui_components as ui
from logic.answer_generation import generate_answer
from logic.chunking import chunk_all_documents, chunking_summary
from logic.document_loader import document_summary, load_all_documents
from logic.embeddings import embed_chunks, embedding_dimension, load_model
from logic.evaluation import (
    evaluation_summary,
    groundedness_checklist,
    record_manual_evaluation,
    retrieval_coverage,
    risk_summary,
)
from logic.governance_checks import (
    check_chunks,
    check_query,
    check_text,
    highest_risk_level,
    summarise_risk_flags,
)
from logic.report_builder import build_report
from logic.retrieval import format_results_for_display, is_retrieval_weak, retrieve
from logic.text_cleaning import clean_document
from logic.vector_index import build_index, index_summary

st.set_page_config(
    page_title="Build 10 — AI Document Intelligence & Governance Agent",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)
ui.inject_css()

PAGES = [
    "Home",
    "Document Library",
    "Document Processing",
    "Chunk Explorer",
    "Embedding Index",
    "Semantic Search",
    "RAG Q&A",
    "Governance Review",
    "Report Builder",
    "Evaluation Dashboard",
]

DEFAULT_CHUNK_SIZE = 200
DEFAULT_OVERLAP = 40
DEFAULT_TOP_K = 5
ORG_NAME = "BrightPath Skills Training"


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

def _init_session_state() -> None:
    defaults: dict = {
        "documents": None,
        "chunks": None,
        "chunk_size": DEFAULT_CHUNK_SIZE,
        "overlap": DEFAULT_OVERLAP,
        "model": None,
        "embeddings": None,
        "index": None,
        "last_query": "",
        "last_results": [],
        "last_answer": None,
        "last_risk_flags": [],
        "last_report": None,
        "text_scan_flags": None,
        "full_scan_flags": None,
        "manual_evals": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("### Build 10\n**AI Document Intelligence**\n**& Governance Agent**")
        st.caption(f"{ORG_NAME}")
        st.markdown("---")
        page = st.radio("Navigate", PAGES, label_visibility="collapsed")
        st.markdown("---")

        docs_ok = st.session_state.get("documents") is not None
        chunks_ok = bool(st.session_state.get("chunks"))
        model_ok = st.session_state.get("model") is not None
        index_ok = st.session_state.get("index") is not None

        st.markdown("**System status**")
        st.markdown(
            f"{'&#9679;' if docs_ok else '&#9675;'} Documents: {'Ready' if docs_ok else 'Not ready'}  \n"
            f"{'&#9679;' if chunks_ok else '&#9675;'} Chunks: {'Ready' if chunks_ok else 'Not ready'}  \n"
            f"{'&#9679;' if model_ok else '&#9675;'} Model: {'Ready' if model_ok else 'Not ready'}  \n"
            f"{'&#9679;' if index_ok else '&#9675;'} Index: {'Ready' if index_ok else 'Not ready'}"
        )

        st.markdown("---")
        st.caption("v1.0 · 9 phases complete · 386 tests")
    return page


# ---------------------------------------------------------------------------
# Page 1: Home
# ---------------------------------------------------------------------------

def page_home() -> None:
    ui.render_page_header(
        "AI Document Intelligence & Governance Agent",
        f"Build 10 · {ORG_NAME} · Local embeddings · FAISS · No external APIs",
    )
    ui.render_safety_warning()

    st.markdown("### Pipeline")
    ui.render_workflow_diagram()

    ui.render_prototype_notice(
        "This prototype demonstrates a <strong>production-grade document intelligence "
        "pipeline</strong> for a further education training organisation. It provides "
        "semantic document retrieval, evidence-based Q&amp;A with citations, governance "
        "risk review, and structured report generation — all running locally without "
        "external APIs."
    )

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Document intelligence")
        st.markdown(
            "- Load and clean policy and guidance documents\n"
            "- Overlapping word-window chunking\n"
            "- 384-dimensional dense embeddings (all-MiniLM-L6-v2)\n"
            "- FAISS IndexFlatIP semantic vector search"
        )
    with col2:
        st.subheader("Governance and assurance")
        st.markdown(
            "- Rule-based risk flag detection across 8 categories\n"
            "- High and Medium risk classification\n"
            "- Grounded, cited extractive answers only\n"
            "- Structured Markdown report export"
        )

    st.markdown("---")
    st.subheader("Suggested workflow")
    st.markdown(
        "1. **Document Library** — review the 8 synthetic policy documents\n"
        "2. **Document Processing** — configure chunking and process documents\n"
        "3. **Embedding Index** — load the model and build the FAISS index\n"
        "4. **Semantic Search** — test retrieval quality with example queries\n"
        "5. **RAG Q&A** — generate grounded answers with citations\n"
        "6. **Governance Review** — scan for risk signals in queries and evidence\n"
        "7. **Report Builder** — export a structured Markdown intelligence report\n"
        "8. **Evaluation Dashboard** — review system and answer quality metrics"
    )

    st.markdown("---")
    ui.render_boundary_notice()


# ---------------------------------------------------------------------------
# Page 2: Document Library
# ---------------------------------------------------------------------------

def page_document_library() -> None:
    ui.render_page_header(
        "Document Library",
        "Review the synthetic policy documents loaded into the analysis library.",
    )
    ui.render_safety_warning()

    if st.session_state["documents"] is None:
        with st.spinner("Loading and cleaning documents..."):
            raw_docs = load_all_documents()
            st.session_state["documents"] = [clean_document(d) for d in raw_docs]

    documents = st.session_state["documents"]
    if not documents:
        st.error("No documents found. Check that data/sample_documents/ contains .md or .txt files.")
        return

    summary = document_summary(documents)
    col1, col2, col3 = st.columns(3)
    col1.metric("Documents loaded", summary["total_documents"])
    col2.metric("Total words", f"{summary['total_word_count']:,}")
    col3.metric("Total characters", f"{summary['total_char_count']:,}")

    st.markdown("---")
    st.subheader("Document index")
    rows = [
        {
            "File": doc["source_name"],
            "Words": doc["word_count"],
            "Characters": doc["char_count"],
        }
        for doc in documents
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.markdown("---")
    st.subheader("Document previews")
    for doc in documents:
        with st.expander(doc["source_name"]):
            col1, col2 = st.columns(2)
            col1.markdown(f"**Words:** {doc['word_count']}")
            col2.markdown(f"**Characters:** {doc['char_count']}")
            st.markdown("---")
            preview = doc["text"][:1500]
            if len(doc["text"]) > 1500:
                preview += "\n\n_[Preview truncated — full document available for processing]_"
            st.text(preview)


# ---------------------------------------------------------------------------
# Page 3: Document Processing
# ---------------------------------------------------------------------------

def page_document_processing() -> None:
    ui.render_page_header(
        "Document Processing",
        "Configure chunking parameters and split documents into searchable units.",
    )

    if st.session_state["documents"] is None:
        st.warning("No documents loaded. Visit Document Library first.")
        return

    documents = st.session_state["documents"]

    col1, col2 = st.columns(2)
    with col1:
        chunk_size = st.slider(
            "Chunk size (words)", min_value=50, max_value=500,
            value=DEFAULT_CHUNK_SIZE, step=10,
            help="Number of words per chunk. Larger chunks provide more context; smaller chunks improve precision.",
        )
    with col2:
        overlap = st.slider(
            "Overlap (words)", min_value=0, max_value=150,
            value=DEFAULT_OVERLAP, step=5,
            help="Number of words shared between consecutive chunks to preserve context at boundaries.",
        )

    if overlap >= chunk_size:
        st.error("Overlap must be less than chunk size.")
        return

    if st.button("Process documents", type="primary"):
        with st.spinner(f"Chunking {len(documents)} documents..."):
            chunks = chunk_all_documents(documents, chunk_size, overlap)
            st.session_state["chunks"] = chunks
            st.session_state["chunk_size"] = chunk_size
            st.session_state["overlap"] = overlap
            st.session_state["embeddings"] = None
            st.session_state["index"] = None
        st.success(f"Processed {len(documents)} document(s) into {len(chunks)} chunks.")

    chunks = st.session_state.get("chunks")
    if not chunks:
        ui.render_prototype_notice(
            "Configure the parameters above and click <strong>Process documents</strong> to begin."
        )
        return

    summary = chunking_summary(chunks)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total chunks", summary["total_chunks"])
    col2.metric("Avg words/chunk", f"{summary['avg_word_count']:.0f}")
    col3.metric("Min words", summary["min_word_count"])
    col4.metric("Max words", summary["max_word_count"])

    st.markdown("---")
    st.subheader("Chunk preview")
    preview_df = pd.DataFrame([
        {
            "Chunk ID": c["chunk_id"],
            "Source": c["source_name"],
            "Words": c["word_count"],
            "Text (first 120 chars)": c["text"][:120],
        }
        for c in chunks[:25]
    ])
    st.dataframe(preview_df, use_container_width=True)
    if len(chunks) > 25:
        st.caption(f"Showing first 25 of {len(chunks)} chunks.")


# ---------------------------------------------------------------------------
# Page 4: Chunk Explorer
# ---------------------------------------------------------------------------

def page_chunk_explorer() -> None:
    ui.render_page_header(
        "Chunk Explorer",
        "Browse and inspect individual chunks across all documents.",
    )

    chunks = st.session_state.get("chunks")
    if not chunks:
        st.warning("No chunks available. Visit Document Processing first.")
        return

    sources = sorted({c["source_name"] for c in chunks})
    selected_source = st.selectbox("Filter by document", ["All documents"] + sources)

    filtered = (
        chunks if selected_source == "All documents"
        else [c for c in chunks if c["source_name"] == selected_source]
    )

    st.markdown(f"**{len(filtered)} chunk(s) shown** &nbsp;&middot;&nbsp; Source: {selected_source}")

    st.subheader("Word count distribution")
    chart_df = pd.DataFrame({"Word count": [c["word_count"] for c in filtered]})
    st.bar_chart(chart_df["Word count"])

    st.markdown("---")
    st.subheader("Chunk inspector")

    if not filtered:
        st.info("No chunks to display for the selected source.")
        return

    chunk_labels = [f"{c['chunk_id']}  ({c['word_count']} words)" for c in filtered]
    selected_label = st.selectbox("Select chunk", chunk_labels)
    selected_idx = chunk_labels.index(selected_label)
    chunk = filtered[selected_idx]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Chunk index", chunk["chunk_index"])
    col2.metric("Word count", chunk["word_count"])
    col3.metric("Start word", chunk["start_word"])
    col4.metric("End word", chunk["end_word"])

    st.markdown("---")
    ui.render_chunk_card(chunk)


# ---------------------------------------------------------------------------
# Page 5: Embedding Index
# ---------------------------------------------------------------------------

def page_embedding_index() -> None:
    ui.render_page_header(
        "Embedding Index",
        "Load the sentence-transformer model and build the FAISS vector index.",
    )

    chunks = st.session_state.get("chunks")
    if not chunks:
        st.warning("No chunks available. Visit Document Processing first.")
        return

    st.subheader("Embedding model")
    st.markdown(
        "**Model:** `sentence-transformers/all-MiniLM-L6-v2`  \n"
        "**Output dimension:** 384  \n"
        "**Normalisation:** unit-normalised embeddings (cosine similarity via inner product)  \n"
        "The model is approximately 90MB and is cached locally after the first download."
    )

    model = st.session_state.get("model")
    if model is None:
        if st.button("Load model", type="primary"):
            with st.spinner("Loading embedding model — this may take a moment on first run..."):
                try:
                    st.session_state["model"] = load_model()
                    st.rerun()
                except Exception as exc:
                    st.error(f"Failed to load model: {exc}")
        return

    dim = embedding_dimension(model)
    st.success(f"Model loaded — embedding dimension: {dim}")

    st.markdown("---")
    st.subheader("FAISS vector index")
    st.markdown(
        "Index type: `IndexFlatIP` (exact inner product search on unit-normalised vectors).  \n"
        "This provides exact cosine similarity — no approximation."
    )

    index = st.session_state.get("index")
    embeddings = st.session_state.get("embeddings")

    if index is None:
        ui.render_prototype_notice(
            f"Ready to embed <strong>{len(chunks)} chunks</strong> and build the FAISS index."
        )
        if st.button("Build index", type="primary"):
            with st.spinner(f"Embedding {len(chunks)} chunks and building FAISS index..."):
                try:
                    emb = embed_chunks(chunks, model)
                    idx = build_index(emb)
                    st.session_state["embeddings"] = emb
                    st.session_state["index"] = idx
                    st.rerun()
                except Exception as exc:
                    st.error(f"Failed to build index: {exc}")
        return

    summary = index_summary(index, embeddings)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total vectors", summary["total_vectors"])
    col2.metric("Embedding dimension", summary["embedding_dimension"])
    col3.metric("Index type", summary["index_type"])

    ui.render_index_ready_bar(
        total_vectors=summary["total_vectors"],
        dimension=summary["embedding_dimension"],
        index_type=summary["index_type"],
    )

    st.caption("FAISS index is ready. You may now use Semantic Search and RAG Q&A.")

    if st.button("Rebuild index"):
        st.session_state["embeddings"] = None
        st.session_state["index"] = None
        st.rerun()


# ---------------------------------------------------------------------------
# Page 6: Semantic Search
# ---------------------------------------------------------------------------

def page_semantic_search() -> None:
    ui.render_page_header(
        "Semantic Search",
        "Search the document library using natural language queries.",
    )

    model = st.session_state.get("model")
    index = st.session_state.get("index")
    chunks = st.session_state.get("chunks")

    if not all([model, index, chunks]):
        st.warning("The embedding index is not ready. Visit Embedding Index first.")
        return

    query = st.text_input(
        "Search query",
        placeholder="e.g. Can staff use ChatGPT with learner data?",
    )
    top_k = st.slider("Results to return", min_value=1, max_value=10, value=DEFAULT_TOP_K)

    if st.button("Search", type="primary"):
        if not query.strip():
            st.warning("Please enter a search query.")
        else:
            with st.spinner("Searching..."):
                results = retrieve(query.strip(), model, index, chunks, top_k=top_k)
                st.session_state["last_query"] = query.strip()
                st.session_state["last_results"] = results

    results = st.session_state.get("last_results", [])
    last_query = st.session_state.get("last_query", "")

    if not results:
        if last_query:
            st.info("No results above the minimum retrieval threshold for this query.")
        return

    coverage = retrieval_coverage(results, top_k=top_k)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Results", coverage["result_count"])
    col2.metric("Top score", f"{coverage['top_score']:.3f}")
    col3.metric("Avg score", f"{coverage['avg_score']:.3f}")
    col4.metric("Coverage grade", coverage["coverage_grade"])

    if is_retrieval_weak(results):
        st.warning(
            "Top retrieval score is below 0.25. Results may not be relevant to the query. "
            "Consider rephrasing."
        )

    st.markdown("---")
    st.subheader(f"Results for: _{last_query}_")

    formatted = format_results_for_display(results)
    for r in formatted:
        ui.render_semantic_result_card(r)
        with st.expander("View full excerpt"):
            st.markdown(f"> {r['text']}")


# ---------------------------------------------------------------------------
# Page 7: RAG Q&A
# ---------------------------------------------------------------------------

def page_rag_qa() -> None:
    ui.render_page_header(
        "RAG Q&A",
        "Ask a question and receive a grounded answer drawn exclusively from the document library.",
    )
    ui.render_safety_warning()

    model = st.session_state.get("model")
    index = st.session_state.get("index")
    chunks = st.session_state.get("chunks")

    if not all([model, index, chunks]):
        st.warning("The embedding index is not ready. Visit Embedding Index first.")
        return

    query = st.text_input(
        "Your question",
        placeholder="e.g. What must staff do before sharing AI-generated content?",
    )
    top_k = st.slider("Evidence chunks to retrieve", min_value=1, max_value=10, value=DEFAULT_TOP_K)

    if st.button("Generate answer", type="primary"):
        if not query.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Retrieving evidence and generating grounded answer..."):
                results = retrieve(query.strip(), model, index, chunks, top_k=top_k)
                answer_dict = generate_answer(query.strip(), results)
                risk_flags = check_query(query.strip())
                st.session_state["last_query"] = query.strip()
                st.session_state["last_results"] = results
                st.session_state["last_answer"] = answer_dict
                st.session_state["last_risk_flags"] = risk_flags

    answer_dict = st.session_state.get("last_answer")
    last_query = st.session_state.get("last_query", "")

    if not answer_dict:
        return

    # Governance alert from query check
    risk_flags = st.session_state.get("last_risk_flags", [])
    if risk_flags:
        highest = highest_risk_level(risk_flags)
        flag_msg = (
            f"Governance alert — {len(risk_flags)} risk flag(s) detected in this query. "
            f"Highest risk level: {highest}. See Governance Review for details."
        )
        if highest == "High":
            st.error(flag_msg)
        else:
            st.warning(flag_msg)

    confidence = answer_dict.get("confidence", "insufficient")
    has_evidence = answer_dict.get("has_evidence", False)

    st.markdown(f"**Query:** _{last_query}_")
    st.markdown("---")

    if not has_evidence:
        st.error(
            "Insufficient evidence — the document library does not contain sufficient "
            "information to answer this question confidently."
        )
        st.markdown(answer_dict.get("answer", ""))
    else:
        confidence_labels = {"strong": "Strong", "moderate": "Moderate", "weak": "Weak"}
        conf_label = confidence_labels.get(confidence, confidence.capitalize())

        if confidence == "strong":
            st.success(f"Confidence: {conf_label}")
        elif confidence == "moderate":
            st.info(f"Confidence: {conf_label}")
        else:
            st.warning(f"Confidence: {conf_label}")

        st.markdown("**Grounded answer**")
        ui.render_answer_card(answer_dict.get("answer", ""))

        citations = answer_dict.get("citations", [])
        if citations:
            st.markdown("---")
            st.subheader("Citations")
            cit_rows = [
                {
                    "Rank": c.get("rank", "—"),
                    "Source": c.get("source_name", "Unknown"),
                    "Chunk ID": c.get("chunk_id", ""),
                    "Score": f"{c.get('score', 0.0):.3f}",
                }
                for c in citations
            ]
            st.dataframe(pd.DataFrame(cit_rows), use_container_width=True)

            st.markdown("**Source excerpts**")
            for c in citations:
                label = f"{c.get('source_name', 'Unknown')} — chunk `{c.get('chunk_id', '')}`"
                with st.expander(label):
                    st.markdown(f"> {c.get('excerpt', '')}")

    st.markdown("---")
    st.caption(answer_dict.get("limitations", ""))


# ---------------------------------------------------------------------------
# Page 8: Governance Review
# ---------------------------------------------------------------------------

def _render_risk_flags(flags: list[dict], context: str = "") -> None:
    suffix = f" in {context}" if context else ""
    if not flags:
        st.success(f"No governance risks detected{suffix}.")
        return

    summary = summarise_risk_flags(flags)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total flags", summary["total_flags"])
    col2.metric("High risk", summary["high_count"])
    col3.metric("Medium risk", summary["medium_count"])

    st.markdown("---")
    for flag in flags:
        ui.render_risk_flag_card(flag)


def page_governance_review() -> None:
    ui.render_page_header(
        "Governance Review",
        "Scan queries and document chunks for governance risk signals across 8 rule-based categories.",
    )
    ui.render_prototype_notice(
        "Governance checks are <strong>rule-based</strong> and cover 8 risk categories relevant "
        "to UK FE training. They are a structured prompt for human judgement — not a complete "
        "compliance assessment. High-risk flags require immediate human review before any AI "
        "output is shared or acted upon."
    )

    st.subheader("Scan a query or text")
    query_input = st.text_input(
        "Enter text to scan",
        placeholder="e.g. Can we use AI to review safeguarding disclosures?",
    )
    if st.button("Scan text", type="primary"):
        if query_input.strip():
            st.session_state["text_scan_flags"] = check_text(query_input.strip())
        else:
            st.warning("Please enter some text to scan.")

    text_flags = st.session_state.get("text_scan_flags")
    if text_flags is not None:
        _render_risk_flags(text_flags, context="query text")

    # Scan last retrieved chunks
    last_results = st.session_state.get("last_results", [])
    if last_results:
        st.markdown("---")
        st.subheader("Scan last retrieved evidence")
        st.caption(
            f"{len(last_results)} chunk(s) from the most recent retrieval. "
            "Query: _{}_".format(st.session_state.get("last_query", ""))
        )
        if st.button("Scan retrieved chunks"):
            flags = check_chunks(last_results)
            st.session_state["last_risk_flags"] = flags

        cached_retrieved = st.session_state.get("last_risk_flags", [])
        if cached_retrieved:
            _render_risk_flags(cached_retrieved, context="retrieved evidence")

    # Scan full library
    chunks = st.session_state.get("chunks")
    if chunks:
        st.markdown("---")
        st.subheader("Scan full document library")
        st.caption(f"Scan all {len(chunks)} chunks across the loaded document library.")
        if st.button("Scan all chunks"):
            with st.spinner("Scanning all document chunks..."):
                st.session_state["full_scan_flags"] = check_chunks(chunks)

        full_flags = st.session_state.get("full_scan_flags")
        if full_flags is not None:
            _render_risk_flags(full_flags, context="full document library")

    # Show flags cached from last Q&A
    last_query = st.session_state.get("last_query", "")
    qa_flags = st.session_state.get("last_risk_flags", [])
    if qa_flags and last_query:
        st.markdown("---")
        st.subheader("Risk flags from last Q&A")
        st.caption(f"Query: _{last_query}_")
        _render_risk_flags(qa_flags, context="last Q&A query")


# ---------------------------------------------------------------------------
# Page 9: Report Builder
# ---------------------------------------------------------------------------

def page_report_builder() -> None:
    ui.render_page_header(
        "Report Builder",
        "Generate a structured Markdown intelligence report from the current Q&A session.",
    )

    last_answer = st.session_state.get("last_answer")
    last_query = st.session_state.get("last_query", "")

    if not last_answer:
        st.warning(
            "No Q&A session found. Visit RAG Q&A, generate an answer, then return here."
        )
        return

    documents = st.session_state.get("documents") or []
    last_results = st.session_state.get("last_results", [])
    last_risk_flags = st.session_state.get("last_risk_flags", [])

    st.subheader("Session summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Documents", len(documents))
    col2.metric("Evidence chunks", len(last_results))
    col3.metric("Risk flags", len(last_risk_flags))
    col4.metric("Confidence", last_answer.get("confidence", "—").capitalize())
    st.markdown(f"**Query:** _{last_query}_")

    st.markdown("---")
    org_name = st.text_input("Organisation name for report", value=ORG_NAME)

    if st.button("Generate report", type="primary"):
        with st.spinner("Assembling report..."):
            st.session_state["last_report"] = build_report(
                documents=documents,
                query=last_query,
                answer_dict=last_answer,
                results=last_results,
                risk_flags=last_risk_flags,
                organisation_name=org_name,
            )

    last_report = st.session_state.get("last_report")
    if last_report:
        st.markdown("---")
        st.subheader("Report preview")
        st.markdown(last_report)

        st.markdown("---")
        st.download_button(
            label="Download report (.md)",
            data=last_report,
            file_name="document_intelligence_report.md",
            mime="text/markdown",
        )


# ---------------------------------------------------------------------------
# Page 10: Evaluation Dashboard
# ---------------------------------------------------------------------------

def page_evaluation_dashboard() -> None:
    ui.render_page_header(
        "Evaluation Dashboard",
        "Review system configuration, retrieval quality, and answer groundedness metrics.",
    )

    documents = st.session_state.get("documents") or []
    chunks = st.session_state.get("chunks") or []
    model = st.session_state.get("model")
    last_results = st.session_state.get("last_results") or []
    last_answer = st.session_state.get("last_answer")
    last_risk_flags = st.session_state.get("last_risk_flags") or []
    last_query = st.session_state.get("last_query", "")

    index_dim = embedding_dimension(model) if model else 0
    eval_sum = evaluation_summary(documents, chunks, index_dim, last_risk_flags)

    st.subheader("System configuration")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Documents", eval_sum["doc_count"])
    col2.metric("Chunks", eval_sum["chunk_count"])
    col3.metric("Embedding dim", eval_sum["embedding_dim"])
    col4.metric("Risk flags", eval_sum["risk_flag_count"])

    if last_results:
        st.markdown("---")
        st.subheader("Retrieval coverage")
        st.caption(f"Query: _{last_query}_")
        coverage = retrieval_coverage(last_results)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Results returned", coverage["result_count"])
        col2.metric("Top score", f"{coverage['top_score']:.3f}")
        col3.metric("Avg score", f"{coverage['avg_score']:.3f}")
        col4.metric("Coverage grade", coverage["coverage_grade"])

        scores_df = pd.DataFrame({
            "Rank": [r.get("rank", i + 1) for i, r in enumerate(last_results)],
            "Score": [r["score"] for r in last_results],
            "Source": [r.get("source_name", "Unknown") for r in last_results],
        })
        st.dataframe(scores_df, use_container_width=True)
    else:
        st.info("No retrieval results yet. Run a search or Q&A to see coverage metrics.")

    if last_answer:
        st.markdown("---")
        st.subheader("Answer groundedness checklist")
        st.caption(f"Query: _{last_query}_")
        checklist = groundedness_checklist(last_answer, last_results)
        for item in checklist:
            label = f"{'Pass' if item['passed'] else 'Fail'} — {item['criterion']}: {item['note']}"
            if item["passed"]:
                st.success(label)
            else:
                st.warning(label)
    else:
        st.info("No Q&A answer yet. Run RAG Q&A to see groundedness metrics.")

    if last_risk_flags:
        st.markdown("---")
        st.subheader("Governance risk summary")
        rs = risk_summary(last_risk_flags)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total flags", rs["total_flags"])
        col2.metric("High", rs["high_count"])
        col3.metric("Medium", rs["medium_count"])
        col4.metric("Highest level", rs["highest_risk_level"])

    st.markdown("---")
    st.subheader("Manual evaluation")
    st.caption("Record your assessment of the most recent Q&A response.")

    if not last_query:
        st.info("No Q&A session to evaluate. Visit RAG Q&A first.")
    else:
        st.markdown(f"**Evaluating response for:** _{last_query}_")

        with st.form("manual_eval_form"):
            relevance = st.slider(
                "Relevance of retrieved results (1 = not relevant, 5 = highly relevant)",
                min_value=1, max_value=5, value=3,
            )
            grounded = st.checkbox("The answer is grounded in the retrieved text")
            useful_cits = st.checkbox("The citations are useful and accurate")
            missing = st.text_area(
                "Missing content or improvement notes",
                placeholder="Describe any missing information or areas for improvement.",
            )
            submitted = st.form_submit_button("Submit evaluation")

        if submitted:
            record = record_manual_evaluation(
                query=last_query,
                relevance_rating=relevance,
                answer_grounded=grounded,
                citations_useful=useful_cits,
                missing_content=missing,
            )
            st.session_state["manual_evals"].append(record)
            st.success("Evaluation recorded.")

    manual_evals = st.session_state.get("manual_evals", [])
    if manual_evals:
        st.markdown(f"**Evaluations recorded this session:** {len(manual_evals)}")
        evals_df = pd.DataFrame(manual_evals)
        display_cols = [
            c for c in
            ["query", "relevance_rating", "answer_grounded", "citations_useful", "timestamp"]
            if c in evals_df.columns
        ]
        st.dataframe(evals_df[display_cols], use_container_width=True)


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

def main() -> None:
    _init_session_state()
    page = render_sidebar()

    if page == "Home":
        page_home()
    elif page == "Document Library":
        page_document_library()
    elif page == "Document Processing":
        page_document_processing()
    elif page == "Chunk Explorer":
        page_chunk_explorer()
    elif page == "Embedding Index":
        page_embedding_index()
    elif page == "Semantic Search":
        page_semantic_search()
    elif page == "RAG Q&A":
        page_rag_qa()
    elif page == "Governance Review":
        page_governance_review()
    elif page == "Report Builder":
        page_report_builder()
    elif page == "Evaluation Dashboard":
        page_evaluation_dashboard()


if __name__ == "__main__":
    main()
