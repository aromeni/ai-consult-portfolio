"""Semantic RAG Policy Assistant — main Streamlit app.

Phase 8: Mini Answer Report — full Markdown report from RAG Q&A output.
"""

import os
import streamlit as st
import pandas as pd

from src import ui_components as ui
from src.document_loader import load_all_documents, list_documents, get_document_metadata
from src.chunker import (
    chunk_documents,
    chunk_text,
    validate_chunk_settings,
    estimate_chunk_count,
    get_chunking_summary,
    split_text_into_words,
)
from src.keyword_search import keyword_search_chunks
from src.sample_data import DOCS_DIR, DEMO_QUERIES, PLANNED_PHASES
from src.embedding_engine import (
    get_default_embedding_model_name,
    validate_chunks_for_embedding,
    embed_chunks as _do_embed_chunks,
    get_embedding_summary,
    load_embedding_model,
)
from src.vector_store import (
    create_vector_store as _do_build_index,
    get_vector_store_summary as _get_vs_summary,
)
from src.semantic_search import semantic_search as _do_semantic_search
from src.rag_engine import (
    generate_rag_response as _do_rag_response,
    generate_rag_markdown as _generate_rag_md,
)


@st.cache_resource(show_spinner="Loading embedding model — this may take a moment on first run...")
def _load_model_cached(model_name: str):
    return load_embedding_model(model_name)

st.set_page_config(
    page_title="Semantic RAG Policy Assistant",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)
ui.inject_css()

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🔎 Semantic RAG\n**Policy Assistant**")
    st.caption("Build 3 · Local embeddings · FAISS · No external APIs")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        [
            "🏠  Home",
            "📚  Document Library",
            "✂️  Chunking Explorer",
            "🧠  Embedding Index Builder",
            "🔍  Semantic Search",
            "💬  RAG Q&A",
            "⚖️  Retrieval Comparison",
            "📄  Mini Answer Report",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("v0.9 · All 8 phases complete")


# ── Page routing ──────────────────────────────────────────────────────────────

# ── Home ───────────────────────────────────────────────────────────────────────
if page == "🏠  Home":
    ui.render_page_header(
        "Semantic RAG Policy Assistant",
        "Local semantic retrieval-augmented generation using synthetic policy documents",
    )
    ui.render_safety_warning()

    st.markdown("### RAG Pipeline")
    ui.render_workflow_diagram()

    ui.render_prototype_notice(
        "This prototype demonstrates a <strong>local semantic RAG architecture</strong> "
        "using synthetic policy documents. It is designed to show the full RAG workflow — "
        "from documents through chunks and embeddings to vector search and grounded answers — "
        "without external AI APIs, cloud services, or real personal data."
    )

    st.markdown("### Completed Phases")
    ui.render_phase_completion_row(PLANNED_PHASES)

    docs = load_all_documents(DOCS_DIR)
    all_chunks = chunk_documents(docs, chunk_size=500, overlap=100)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        ui.render_metric_card("Documents", str(len(docs)), "Synthetic policy documents loaded")
    with c2:
        total_words = sum(len(t.split()) for t in docs.values())
        ui.render_metric_card("Total Words", f"{total_words:,}", "Across all documents")
    with c3:
        ui.render_metric_card("Chunks (500w)", str(len(all_chunks)), "With 100-word overlap")
    with c4:
        ui.render_metric_card("Phase", "8", "Current build phase")

    ui.render_boundary_notice()


# ── Document Library ───────────────────────────────────────────────────────────
elif page == "📚  Document Library":
    ui.render_page_header(
        "Document Library",
        "Synthetic policy documents — metadata and preview",
    )
    ui.render_safety_warning()

    doc_paths = list_documents(DOCS_DIR)
    if not doc_paths:
        st.warning("No documents found. Check that data/synthetic_documents/ contains .md files.")
    else:
        metadata_rows = [get_document_metadata(p) for p in doc_paths]
        df = pd.DataFrame(metadata_rows)[["filename", "title", "word_count", "line_count", "character_count"]]
        df.columns = ["Filename", "Title", "Words", "Lines", "Characters"]
        st.dataframe(df, use_container_width=True)

        ui.render_prototype_notice(
            "Documents must be <strong>chunked</strong> before embeddings and semantic search "
            "can work. Use the Chunking Explorer page to inspect how these documents are split."
        )

        st.markdown("---")
        st.markdown("### Document Preview")
        selected = st.selectbox(
            "Select a document to preview",
            options=[m["filename"] for m in metadata_rows],
        )
        if selected:
            docs = load_all_documents(DOCS_DIR)
            with st.expander(f"📄 {selected}", expanded=True):
                st.markdown(docs[selected])


# ── Chunking Explorer ──────────────────────────────────────────────────────────
elif page == "✂️  Chunking Explorer":
    ui.render_page_header(
        "Chunking Explorer",
        "Configure and inspect how policy documents are split before embedding",
    )
    ui.render_safety_warning()

    # ── Why chunking matters ─────────────────────────────────────────────────
    with st.expander("📖 Why chunking matters in RAG", expanded=False):
        st.markdown(
            """
**RAG systems retrieve chunks, not whole documents.**

Before a document can be searched semantically, it must be split into smaller units called chunks.
Each chunk is embedded into a vector — a numerical representation of its meaning.
When a user asks a question, the query is also embedded, and the nearest chunks are retrieved.

**Chunk size affects retrieval quality:**

| Setting | Effect |
|---|---|
| Smaller chunks | More precise retrieval, but may lose surrounding context |
| Larger chunks | More context per result, but may retrieve irrelevant material |
| Overlap | Preserves context at chunk boundaries — the same sentence may appear in two adjacent chunks |

**Good chunking improves answer grounding.** If the right evidence isn't in a retrieved chunk,
the RAG system cannot produce a well-grounded answer — no matter how good the model is.

> These synthetic documents are short (~700–1,000 words). A chunk size of 120 words and
> overlap of 30 words is recommended for exploring them clearly.
            """
        )

    docs = load_all_documents(DOCS_DIR)

    # ── Settings ─────────────────────────────────────────────────────────────
    st.markdown("### Settings")
    col_a, col_b, col_c, col_d = st.columns([2, 1, 1, 1])
    with col_a:
        doc_scope = st.selectbox(
            "Document scope",
            options=["All documents"] + sorted(docs.keys()),
        )
    with col_b:
        chunk_size = st.number_input(
            "Chunk size (words)", min_value=10, max_value=2000, value=120, step=10
        )
    with col_c:
        overlap = st.number_input(
            "Overlap (words)", min_value=0, max_value=500, value=30, step=10
        )
    with col_d:
        strategy = st.selectbox(
            "Strategy",
            options=["word", "section (experimental)"],
        )
    strategy_key = "section" if strategy.startswith("section") else "word"

    # ── Validation ───────────────────────────────────────────────────────────
    is_valid, val_msg = validate_chunk_settings(int(chunk_size), int(overlap))
    if not is_valid:
        st.error(f"⚠ {val_msg}")
        st.stop()

    # Word count for estimation
    if doc_scope == "All documents":
        total_words_for_estimate = sum(len(t.split()) for t in docs.values())
    else:
        total_words_for_estimate = len(docs[doc_scope].split())
    estimated = estimate_chunk_count(total_words_for_estimate, int(chunk_size), int(overlap))

    st.caption(
        f"Estimated chunks: **{estimated}** · "
        f"Step: {int(chunk_size) - int(overlap)} words · "
        f"Strategy: {strategy_key}"
    )

    # ── Generate button ───────────────────────────────────────────────────────
    if st.button("✂️ Generate Chunks", type="primary"):
        if doc_scope == "All documents":
            chunks = chunk_documents(
                docs, chunk_size=int(chunk_size), overlap=int(overlap), strategy=strategy_key
            )
        else:
            chunks = chunk_text(
                docs[doc_scope],
                chunk_size=int(chunk_size),
                overlap=int(overlap),
                document_name=doc_scope,
                strategy=strategy_key,
            )
        summary = get_chunking_summary(chunks)
        st.session_state["chunks"] = chunks
        st.session_state["chunking_summary"] = summary
        st.session_state["chunking_settings"] = {
            "chunk_size": int(chunk_size),
            "overlap": int(overlap),
            "strategy": strategy_key,
            "document_scope": doc_scope,
        }

    # ── Results ───────────────────────────────────────────────────────────────
    if "chunks" in st.session_state and st.session_state["chunks"]:
        chunks = st.session_state["chunks"]
        summary = st.session_state["chunking_summary"]
        settings = st.session_state["chunking_settings"]

        st.markdown("---")
        st.markdown("### Results")

        # Metric cards
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            ui.render_metric_card("Documents", str(summary["total_documents"]), "Documents processed")
        with m2:
            ui.render_metric_card("Total Chunks", str(summary["total_chunks"]), "Chunks generated")
        with m3:
            ui.render_metric_card(
                "Avg Chunk Size",
                f"{summary['average_chunk_words']}w",
                "Average words per chunk",
            )
        with m4:
            ui.render_metric_card("Overlap", f"{settings['overlap']}w", "Words shared between adjacent chunks")
        with m5:
            ui.render_metric_card("Strategy", settings["strategy"], "Chunking strategy used")

        st.markdown("---")

        # Table view
        st.markdown("### Chunk Table")
        table_rows = [
            {
                "Chunk ID": c["chunk_id"],
                "Document": c["document_name"],
                "Index": c["chunk_index"],
                "Words": c["word_count"],
                "Chars": c["character_count"],
                "Start Word": c["start_word"],
                "End Word": c["end_word"],
            }
            for c in chunks
        ]
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

        # Expandable chunk inspector
        st.markdown("### Inspect Chunks")
        max_display = min(50, len(chunks))
        show_n = st.slider(
            "Chunks to inspect",
            min_value=1,
            max_value=max_display,
            value=min(10, max_display),
        )
        for chunk in chunks[:show_n]:
            with st.expander(
                f"Chunk {chunk['chunk_index']} — {chunk['document_name']} "
                f"· words {chunk['start_word']}–{chunk['end_word']} "
                f"· {chunk['word_count']} words",
                expanded=False,
            ):
                st.caption(
                    f"**Chunk ID:** `{chunk['chunk_id']}`  "
                    f"**Strategy:** {chunk['strategy']}  "
                    f"**Chunk size setting:** {chunk['chunk_size']}  "
                    f"**Overlap setting:** {chunk['overlap']}"
                )
                st.markdown(chunk["text"])
    else:
        st.info("Configure settings above and click **Generate Chunks** to inspect the chunks.")


# ── Embedding Index Builder ────────────────────────────────────────────────────
elif page == "🧠  Embedding Index Builder":
    ui.render_page_header(
        "Embedding Index Builder",
        "Generate local embeddings and build a FAISS vector index — Phase 4 (functional)",
    )
    ui.render_safety_warning()
    ui.render_prototype_notice(
        "This page runs two steps: generate local embeddings using sentence-transformers, "
        "then build a FAISS vector index for fast similarity search. "
        "No external AI API, no cloud service."
    )

    # ── What are embeddings? ──────────────────────────────────────────────────
    with st.expander("🔢 What are embeddings?", expanded=False):
        st.markdown(
            """
**Embeddings are numeric vector representations of text.**

Each chunk is converted into a list of numbers (a vector) that encodes its meaning.
Chunks with similar meanings will have vectors that point in similar directions.

In a RAG system, both document chunks and user queries are embedded into the same vector space.
Retrieval works by finding which chunk vectors are most similar to the query vector.

| Step | What happens |
|---|---|
| Step 1 (this page) | Each chunk → embedding vector (384 numbers) |
| Step 2 (this page) | Vectors stored in a FAISS index for fast similarity search |
| Phase 5 | Query embedded → nearest chunks retrieved → grounded answer |
            """
        )

    # ── What is a FAISS vector index? ────────────────────────────────────────
    with st.expander("📦 What is a FAISS vector index?", expanded=False):
        st.markdown(
            """
**FAISS (Facebook AI Similarity Search) is a library for efficient vector similarity search.**

- FAISS stores numeric vectors so similar vectors can be searched efficiently.
- In RAG, document chunks are embedded and stored in a vector index.
- A user question is embedded using the same model.
- The index retrieves chunks that are semantically close to the question.
- This phase builds the index; Phase 5 will use it for semantic search.

**Index types used in this build:**

| Type | Metric | When similar | Used when |
|---|---|---|---|
| IndexFlatIP | Inner product (cosine) | Higher score | Embeddings are normalised (default) |
| IndexFlatL2 | Euclidean distance | Lower distance | When normalisation is not applied |

> This prototype keeps the index in memory. Saving the index to disk is supported
> by FAISS but not required in this phase.
            """
        )

    # ── Check for chunks ──────────────────────────────────────────────────────
    if "chunks" not in st.session_state or not st.session_state["chunks"]:
        ui.render_placeholder(
            "No chunks found",
            "Go to the Chunking Explorer page first, configure your settings, "
            "and click Generate Chunks. Then return here to embed them.",
        )
        st.stop()

    chunks = st.session_state["chunks"]
    chunking_settings = st.session_state.get("chunking_settings", {})

    st.markdown(
        f"**Chunks ready:** {len(chunks)} chunks from "
        f"**{st.session_state.get('chunking_summary', {}).get('total_documents', '?')}** documents"
        f" · chunk size {chunking_settings.get('chunk_size', '?')}w"
        f" · overlap {chunking_settings.get('overlap', '?')}w"
        f" · strategy: {chunking_settings.get('strategy', '?')}"
    )

    st.markdown("---")

    # ── Step 1: Generate Embeddings ───────────────────────────────────────────
    st.markdown("### Step 1: Generate Embeddings")

    if "embedding_summary" in st.session_state:
        emb_summary = st.session_state["embedding_summary"]
        st.success(
            f"Embeddings ready — {emb_summary['chunk_count']} chunks · "
            f"{emb_summary['embedding_dimension']}d vectors · "
            f"model: {emb_summary['model_name'].split('/')[-1]} · "
            f"normalised: {emb_summary['normalised']}"
        )

        with st.expander("Embedding details", expanded=False):
            m1, m2, m3, m4, m5 = st.columns(5)
            with m1:
                ui.render_metric_card(
                    "Model", emb_summary["model_name"].split("/")[-1], emb_summary["model_name"]
                )
            with m2:
                ui.render_metric_card("Chunks", str(emb_summary["chunk_count"]), "Chunks embedded")
            with m3:
                ui.render_metric_card(
                    "Dimensions", str(emb_summary["embedding_dimension"]), "Vector length"
                )
            with m4:
                ui.render_metric_card(
                    "Documents", str(emb_summary["documents_embedded"]), "Source documents"
                )
            with m5:
                ui.render_metric_card(
                    "Normalised",
                    "Yes" if emb_summary["normalised"] else "No",
                    "Unit-length normalisation",
                )

            stats_df = pd.DataFrame([
                {"Stat": "Average chunk words", "Value": emb_summary["average_chunk_words"]},
                {"Stat": "Min chunk words", "Value": emb_summary["min_chunk_words"]},
                {"Stat": "Max chunk words", "Value": emb_summary["max_chunk_words"]},
            ])
            st.table(stats_df)

            embedded_chunks_preview = st.session_state.get("embedded_chunks", [])
            if embedded_chunks_preview:
                st.markdown("**Embedding Preview** — first 8 vector values per chunk (4 d.p.)")
                preview_rows = []
                for ec in embedded_chunks_preview:
                    vec_preview = [round(v, 4) for v in ec["embedding_vector"][:8]]
                    preview_rows.append({
                        "Idx": ec["embedding_index"],
                        "Chunk ID": ec["chunk_id"],
                        "Document": ec["document_name"],
                        "Words": ec["word_count"],
                        "Vector (first 8)": str(vec_preview),
                    })
                st.dataframe(pd.DataFrame(preview_rows), use_container_width=True)

        if st.button("Re-generate Embeddings"):
            for key in ("embedding_model_name", "embedded_chunks", "embedding_matrix",
                        "embedding_summary", "vector_store", "vector_store_summary", "vector_metric"):
                st.session_state.pop(key, None)
            st.rerun()
    else:
        st.markdown("#### Embedding model")
        model_name = st.text_input(
            "Model name (sentence-transformers)",
            value=get_default_embedding_model_name(),
            help="A local sentence-transformers model. No API key required.",
        )
        st.caption(
            "This model generates dense vector representations of each chunk. "
            "The first run may download model weights (~90 MB). "
            "Later runs use the cached model."
        )
        st.info(
            "**Performance note:** On first run the model may take a minute or two to download. "
            "Later runs are much faster because the model is cached for the session."
        )

        if st.button("🧠 Generate Embeddings", type="primary"):
            valid, val_msg = validate_chunks_for_embedding(chunks)
            if not valid:
                st.error(f"Cannot embed: {val_msg}")
            else:
                try:
                    with st.spinner("Loading model and generating embeddings..."):
                        model = _load_model_cached(model_name)
                        result = _do_embed_chunks(chunks, model=model, model_name=model_name)
                        summary = get_embedding_summary(
                            result["embedded_chunks"],
                            result["model_name"],
                            embedding_dimension=result["embedding_dimension"],
                            normalised=result["normalised"],
                        )
                    st.session_state["embedding_model_name"] = model_name
                    st.session_state["embedded_chunks"] = result["embedded_chunks"]
                    st.session_state["embedding_matrix"] = result["embedding_matrix"]
                    st.session_state["embedding_summary"] = summary
                    st.success(
                        f"Embeddings generated — {result['chunk_count']} chunks · "
                        f"{result['embedding_dimension']}d vectors · "
                        f"normalised: {result['normalised']}"
                    )
                    st.rerun()
                except Exception as e:
                    st.error(
                        f"Embedding failed: {e}\n\n"
                        "Check that sentence-transformers is installed "
                        "(`pip install sentence-transformers`) and that the model name is correct."
                    )

    st.markdown("---")

    # ── Step 2: Build FAISS Index ─────────────────────────────────────────────
    st.markdown("### Step 2: Build FAISS Vector Index")

    if "embedding_matrix" not in st.session_state or "embedded_chunks" not in st.session_state:
        st.info(
            "Generate chunks in the Chunking Explorer first, "
            "then generate embeddings before building the vector index."
        )
        st.stop()

    col_metric, _spacer = st.columns([1, 3])
    with col_metric:
        metric = st.selectbox(
            "Similarity metric",
            options=["cosine", "l2"],
            index=0,
            help=(
                "cosine: IndexFlatIP — higher score means more similar. "
                "Best with normalised embeddings (default). "
                "l2: IndexFlatL2 — lower distance means more similar."
            ),
        )
    st.caption(
        "**cosine** uses IndexFlatIP (inner product) — best with normalised embeddings (Phase 3 default). "
        "**l2** uses IndexFlatL2 (Euclidean distance)."
    )

    if st.button("📦 Build FAISS Index", type="primary"):
        try:
            with st.spinner("Building FAISS vector index..."):
                vs = _do_build_index(
                    st.session_state["embedded_chunks"],
                    st.session_state["embedding_matrix"],
                    metric=metric,
                )
                vs_summary = _get_vs_summary(vs)
            st.session_state["vector_store"] = vs
            st.session_state["vector_store_summary"] = vs_summary
            st.session_state["vector_metric"] = metric
            st.success(
                f"FAISS index built — {vs['chunk_count']} vectors · "
                f"{vs['dimension']}d · "
                f"{vs['index_type']} · "
                f"metric: {vs['metric']}"
            )
            st.rerun()
        except ImportError as e:
            st.error(str(e))
            st.info("Install dependencies with: pip install -r requirements.txt")
        except Exception as e:
            st.error(f"Index build failed: {e}")

    # ── Index results ─────────────────────────────────────────────────────────
    if "vector_store_summary" in st.session_state:
        vs_summary = st.session_state["vector_store_summary"]

        st.markdown("---")
        st.markdown("### Index Summary")

        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            ui.render_metric_card("Index Type", vs_summary["index_type"], "FAISS index type")
        with m2:
            ui.render_metric_card("Metric", vs_summary["metric"], "Similarity metric")
        with m3:
            ui.render_metric_card(
                "Vectors", str(vs_summary["total_vectors"]), "Vectors indexed"
            )
        with m4:
            ui.render_metric_card(
                "Dimensions", str(vs_summary["dimension"]), "Embedding dimension"
            )
        with m5:
            ui.render_metric_card(
                "Documents", str(vs_summary["document_count"]), "Documents indexed"
            )

        st.markdown("### Vector Store Summary")
        summary_rows = [
            {"Property": "Index Type", "Value": vs_summary["index_type"]},
            {"Property": "Similarity Metric", "Value": vs_summary["metric"]},
            {"Property": "Total Vectors", "Value": str(vs_summary["total_vectors"])},
            {"Property": "Chunk Count", "Value": str(vs_summary["chunk_count"])},
            {"Property": "Embedding Dimension", "Value": str(vs_summary["dimension"])},
            {"Property": "Document Count", "Value": str(vs_summary["document_count"])},
            {"Property": "Index Trained", "Value": "Yes" if vs_summary["is_trained"] else "No"},
        ]
        st.table(pd.DataFrame(summary_rows))

        if vs_summary.get("documents_indexed"):
            st.caption("Documents indexed: " + " · ".join(vs_summary["documents_indexed"]))

        ui.render_prototype_notice(
            "The FAISS vector index is stored in session state and ready for Phase 5 "
            "(semantic search). Semantic search, RAG Q&A, and retrieval comparison "
            "are not yet available."
        )


# ── Semantic Search ────────────────────────────────────────────────────────────
elif page == "🔍  Semantic Search":
    ui.render_page_header(
        "Semantic Search",
        "Vector similarity search over embedded policy chunks — Phase 5 (functional)",
    )
    ui.render_safety_warning()

    with st.expander("🔍 What does semantic search do?", expanded=False):
        st.markdown(
            """
**Semantic search finds relevant content by meaning, not just matching words.**

| Step | What happens |
|---|---|
| 1 | Your query is converted into an embedding vector using the same model used for document chunks |
| 2 | FAISS compares the query vector against every chunk vector in the index |
| 3 | The chunks most similar to your query are returned, ranked by similarity score |
| 4 | Results are evidence candidates — human review is required before acting on any output |

**Why this matters:**
- A keyword search for "learner privacy" might miss a chunk about "student data protection"
- Semantic search retrieves both, because the meanings are similar
- This enables better retrieval even when exact words differ

> Scores indicate semantic similarity, not certainty. Results still require human review.
            """
        )

    # ── Pipeline check ────────────────────────────────────────────────────────
    if "vector_store" not in st.session_state or not st.session_state.get("vector_store"):
        st.markdown("**Complete these steps first:**")
        ui.render_pipeline_steps([
            "Go to Chunking Explorer and click Generate Chunks.",
            "Go to Embedding Index Builder and click Generate Embeddings.",
            "On the same page, click Build FAISS Index.",
            "Return here to run semantic search.",
        ])
        st.stop()

    vector_store = st.session_state["vector_store"]
    model_name = st.session_state.get("embedding_model_name", get_default_embedding_model_name())
    vs_summary = st.session_state.get("vector_store_summary", {})

    ui.render_index_ready_bar(
        vs_summary.get("total_vectors", "?"),
        vs_summary.get("dimension", "?"),
        vs_summary.get("index_type", "?"),
        model_name,
    )

    st.markdown("---")

    # ── Suggested queries ─────────────────────────────────────────────────────
    _SEMANTIC_DEMO_QUERIES = [
        "Can staff put learner names into ChatGPT?",
        "What should staff do with safeguarding information?",
        "How should AI-generated lesson plans be checked?",
        "Which tools are staff allowed to use?",
        "What happens if AI gives false or biased information?",
        "Who is responsible for AI-assisted outputs?",
        "What should happen after a data incident?",
    ]

    if "semantic_query_input" not in st.session_state:
        st.session_state["semantic_query_input"] = ""

    st.markdown("### Suggested queries")
    sq_cols = st.columns(4)
    for i, sq in enumerate(_SEMANTIC_DEMO_QUERIES):
        with sq_cols[i % 4]:
            if st.button(sq, key=f"sem_q_{i}"):
                st.session_state["semantic_query_input"] = sq

    st.markdown("---")

    # ── Search input ──────────────────────────────────────────────────────────
    st.markdown("### Search")
    query = st.text_input(
        "Enter a natural language query",
        key="semantic_query_input",
        placeholder="e.g. What should staff do with safeguarding information?",
    )
    top_k = st.slider("Number of results", min_value=1, max_value=10, value=5)

    if st.button("🔍 Search", type="primary"):
        if not query or not query.strip():
            st.warning("Enter a search query above.")
        else:
            try:
                with st.spinner("Embedding query and searching index..."):
                    model = _load_model_cached(model_name)
                    search_result = _do_semantic_search(
                        query,
                        vector_store,
                        model=model,
                        model_name=model_name,
                        top_k=top_k,
                    )
                st.session_state["last_semantic_query"] = query
                st.session_state["last_semantic_results"] = search_result["results"]
                st.session_state["last_semantic_search_summary"] = {
                    "query": query,
                    "result_count": search_result["result_count"],
                    "top_k": search_result["top_k"],
                    "metric": search_result["metric"],
                    "model_name": search_result["model_name"],
                    "query_embedding_dimension": search_result["query_embedding_dimension"],
                    "limitations": search_result["limitations"],
                }
                st.rerun()
            except Exception as e:
                st.error(f"Search failed: {e}")

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.get("last_semantic_results") is not None:
        last_query = st.session_state.get("last_semantic_query", "")
        results = st.session_state["last_semantic_results"]
        search_summary = st.session_state.get("last_semantic_search_summary", {})

        st.markdown("---")
        st.markdown(f"### Results for: _{last_query}_")
        st.caption(
            f"{len(results)} result(s) · "
            f"metric: {search_summary.get('metric', '?')} · "
            f"model: {search_summary.get('model_name', '?').split('/')[-1]}"
        )

        if not results:
            st.info(
                "No results found. Try a different query or rebuild the index "
                "with more chunks from the Embedding Index Builder."
            )
        else:
            st.caption(
                "Higher scores indicate stronger semantic similarity. "
                "Scores are ranking signals, not confidence percentages."
            )
            for r in results:
                ui.render_semantic_result_card(r)

        with st.expander("Responsible-use limitations", expanded=False):
            for lim in search_summary.get("limitations", []):
                st.markdown(f"- {lim}")

        ui.render_prototype_notice(
            "Results are retrieved evidence candidates, not verified answers. "
            "Human review is required before acting on any output from this prototype."
        )


# ── RAG Q&A ────────────────────────────────────────────────────────────────────
elif page == "💬  RAG Q&A":
    ui.render_page_header(
        "RAG Q&A",
        "Grounded question answering with deterministic evidence-based answers — Phase 6 (functional)",
    )
    ui.render_safety_warning()

    with st.expander("💬 What is RAG Q&A?", expanded=False):
        st.markdown(
            """
**RAG Q&A (Retrieval-Augmented Generation) answers questions from retrieved document evidence.**

| Step | What happens |
|---|---|
| 1 | Your question is embedded using the same model used for document chunks |
| 2 | FAISS retrieves the most semantically similar chunks |
| 3 | A deterministic, template-based answer is generated from the detected question intent |
| 4 | Retrieved evidence is shown alongside the answer |

**Important constraints in this prototype:**
- Answers are template-based — no external LLM is used
- Answers are only as good as the retrieved chunks
- Human review is required before acting on any answer
- Answers do not constitute professional, legal, or safeguarding advice
            """
        )

    # ── Pipeline check ────────────────────────────────────────────────────────
    if "vector_store" not in st.session_state or not st.session_state.get("vector_store"):
        st.markdown("**Complete these steps first:**")
        ui.render_pipeline_steps([
            "Go to Chunking Explorer and click Generate Chunks.",
            "Go to Embedding Index Builder and click Generate Embeddings.",
            "On the same page, click Build FAISS Index.",
            "Return here to run RAG Q&A.",
        ])
        st.stop()

    vector_store = st.session_state["vector_store"]
    model_name = st.session_state.get("embedding_model_name", get_default_embedding_model_name())
    vs_summary = st.session_state.get("vector_store_summary", {})

    ui.render_index_ready_bar(
        vs_summary.get("total_vectors", "?"),
        vs_summary.get("dimension", "?"),
        vs_summary.get("index_type", "?"),
        model_name,
    )

    st.markdown("---")

    # ── Suggested questions ───────────────────────────────────────────────────
    _RAG_DEMO_QUESTIONS = [
        "Can staff put learner names into ChatGPT?",
        "What should staff do with safeguarding information?",
        "How should AI-generated lesson plans be checked?",
        "Which AI tools are staff allowed to use?",
        "What happens if AI gives false or biased information?",
        "Who is responsible for AI-assisted outputs?",
        "What should happen after a data incident?",
        "Can AI make safeguarding decisions?",
    ]

    if "rag_question_input" not in st.session_state:
        st.session_state["rag_question_input"] = ""

    st.markdown("### Suggested questions")
    rq_cols = st.columns(4)
    for i, rq in enumerate(_RAG_DEMO_QUESTIONS):
        with rq_cols[i % 4]:
            if st.button(rq, key=f"rag_q_{i}"):
                st.session_state["rag_question_input"] = rq

    st.markdown("---")

    # ── Question input ────────────────────────────────────────────────────────
    st.markdown("### Your question")
    question = st.text_input(
        "Enter a policy question",
        key="rag_question_input",
        placeholder="e.g. Can staff put learner names into ChatGPT?",
    )
    top_k = st.slider("Chunks to retrieve", min_value=1, max_value=10, value=5)

    if st.button("💬 Generate Answer", type="primary"):
        if not question or not question.strip():
            st.warning("Enter a question above.")
        else:
            try:
                with st.spinner("Retrieving evidence and generating answer..."):
                    model = _load_model_cached(model_name)
                    rag_result = _do_rag_response(
                        question,
                        vector_store,
                        model=model,
                        model_name=model_name,
                        top_k=top_k,
                    )
                st.session_state["last_rag_question"] = question
                st.session_state["last_rag_response"] = rag_result
                st.session_state["last_rag_answer"] = rag_result["answer"]
                st.session_state["last_rag_evidence"] = rag_result["evidence_summary"]
                st.rerun()
            except Exception as e:
                st.error(f"RAG Q&A failed: {e}")

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.get("last_rag_response") is not None:
        rag = st.session_state["last_rag_response"]

        st.markdown("---")
        st.markdown(f"### Answer for: _{rag['question']}_")

        # Answer card (with optional caution banner)
        _caution = rag["caution_reason"] if rag.get("needs_caution") else ""
        ui.render_answer_card(rag["answer"], _caution)

        # Metadata
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            ui.render_metric_card(
                "Question Type", rag["question_type"].replace("_", " ").title(), ""
            )
        with m2:
            topics_display = ", ".join(rag["detected_topics"]) or "none detected"
            ui.render_metric_card("Detected Topics", str(len(rag["detected_topics"])), topics_display)
        with m3:
            ui.render_metric_card("Chunks Retrieved", str(len(rag["retrieved_chunks"])), "From FAISS index")
        with m4:
            ui.render_metric_card("Metric", rag["metric"], f"model: {rag['model_name'].split('/')[-1]}")

        if rag["detected_topics"]:
            st.caption("Topics detected: " + " · ".join(rag["detected_topics"]))

        # Evidence
        if rag["evidence_summary"]:
            st.markdown("---")
            st.markdown("### Retrieved Evidence")
            st.caption(
                "Chunks are ranked by semantic similarity. "
                "Higher scores indicate stronger similarity."
            )
            for item in rag["evidence_summary"]:
                ui.render_evidence_card(item)
        else:
            st.info(
                "No evidence retrieved. Try a different question or rebuild the index "
                "with more chunks."
            )

        # Limitations
        with st.expander("Responsible-use limitations", expanded=False):
            for lim in rag["limitations"]:
                st.markdown(f"- {lim}")

        # Download
        st.markdown("---")
        st.markdown("### Download")
        md_content = _generate_rag_md(rag)
        safe_name = "".join(c if c.isalnum() else "_" for c in rag["question"][:40]).lower()
        st.download_button(
            "⬇️ Download Q&A response (.md)",
            data=md_content,
            file_name=f"rag_response_{safe_name}.md",
            mime="text/markdown",
        )

        ui.render_prototype_notice(
            "This answer was generated using deterministic template logic from retrieved evidence. "
            "It is not legal, safeguarding, HR, or professional advice. "
            "Human review is required before acting on any output."
        )


# ── Retrieval Comparison ───────────────────────────────────────────────────────
elif page == "⚖️  Retrieval Comparison":
    from src.comparison import (
        compare_retrieval_methods as _do_comparison,
        generate_retrieval_comparison_markdown as _generate_comparison_md,
    )

    ui.render_page_header(
        "Retrieval Comparison",
        "Keyword vs semantic retrieval side by side — Phase 7",
    )
    ui.render_safety_warning()

    _chunks = st.session_state.get("chunks")
    _vs = st.session_state.get("vector_store")

    if not _chunks or not _vs:
        st.markdown("**Complete these steps first:**")
        ui.render_pipeline_steps([
            "Go to Chunking Explorer and generate chunks.",
            "Go to Embedding Index Builder and generate embeddings.",
            "Build the FAISS vector index.",
            "Return to Retrieval Comparison.",
        ])
        st.stop()

    with st.expander("What is retrieval comparison?", expanded=False):
        st.markdown(
            "Retrieval comparison runs both keyword search and semantic search for the same "
            "query and shows results side by side.\n\n"
            "- **Keyword search** finds chunks containing the exact (or near-exact) words in your query.\n"
            "- **Semantic search** finds chunks whose meaning is most similar to your query, "
            "even when the wording is different.\n"
            "- **Overlap** shows which chunks both methods agree on — often the strongest evidence candidates.\n"
            "- **Differences** reveal where semantic search adds value beyond exact keyword matching."
        )

    _COMPARISON_QUERIES = [
        "Can staff put learner names into ChatGPT?",
        "What should staff do with safeguarding information?",
        "How should AI-generated lesson plans be checked?",
        "What happens if AI gives false or biased information?",
        "Who is responsible for AI-assisted outputs?",
        "What should happen after a data incident?",
        "Can AI make safeguarding decisions?",
    ]

    st.markdown("#### Suggested comparison queries")
    _cq_cols = st.columns(3)
    for _i, _cq in enumerate(_COMPARISON_QUERIES):
        if _cq_cols[_i % 3].button(_cq, key=f"comp_q_{_i}"):
            st.session_state["comparison_query_input"] = _cq

    _comp_query = st.text_input(
        "Enter a query to compare",
        key="comparison_query_input",
        placeholder="e.g. Can staff use ChatGPT for marking?",
    )
    _comp_top_k = st.slider("Chunks to retrieve per method", 1, 10, 5, key="comparison_top_k")

    if st.button("⚖️ Compare Retrieval Methods"):
        if not _comp_query or not _comp_query.strip():
            st.warning("Enter a query before running the comparison.")
        else:
            _comp_model_name = st.session_state.get(
                "embedding_model_name", get_default_embedding_model_name()
            )
            _comp_model = _load_model_cached(_comp_model_name)
            with st.spinner("Running keyword and semantic retrieval..."):
                try:
                    _comp_result = _do_comparison(
                        query=_comp_query,
                        chunks=_chunks,
                        vector_store=_vs,
                        model=_comp_model,
                        model_name=_comp_model_name,
                        top_k=_comp_top_k,
                    )
                    st.session_state["last_comparison_query"] = _comp_query
                    st.session_state["last_retrieval_comparison"] = _comp_result
                    st.session_state["last_keyword_results"] = _comp_result["keyword_results"]
                    st.session_state["last_semantic_results"] = _comp_result["semantic_results"]
                    st.rerun()
                except Exception as _comp_err:
                    st.error(f"Comparison error: {_comp_err}")

    _comp = st.session_state.get("last_retrieval_comparison")
    if _comp:
        _ks = _comp["keyword_summary"]
        _ss = _comp["semantic_summary"]
        _ov = _comp["overlap"]

        _mc1, _mc2, _mc3, _mc4, _mc5 = st.columns(5)
        with _mc1:
            ui.render_metric_card("Keyword Results", str(_ks["result_count"]), "chunks found")
        with _mc2:
            ui.render_metric_card("Semantic Results", str(_ss["result_count"]), "chunks found")
        with _mc3:
            ui.render_metric_card("Overlapping", str(len(_ov)), "found by both")
        with _mc4:
            ui.render_metric_card("Keyword Docs", str(_ks["unique_documents"]), "unique documents")
        with _mc5:
            ui.render_metric_card("Semantic Docs", str(_ss["unique_documents"]), "unique documents")

        st.markdown("#### Comparison Insight")
        ui.render_comparison_insight_card(_comp["comparison_insight"])

        _kw_col, _sem_col = st.columns(2)

        with _kw_col:
            ui.render_comparison_col_header("Keyword Results", "keyword")
            st.caption(_ks["method_note"])
            _kw_res = _comp["keyword_results"]
            if _kw_res:
                for _rank, _r in enumerate(_kw_res, 1):
                    ui.render_keyword_result_card(_r, _rank)
            else:
                st.info("No keyword results for this query.")

        with _sem_col:
            ui.render_comparison_col_header("Semantic Results", "semantic")
            st.caption(_ss["method_note"])
            _sem_res = _comp["semantic_results"]
            if _sem_res:
                for _r in _sem_res:
                    ui.render_semantic_result_card(_r)
            else:
                st.info("No semantic results for this query.")

        st.markdown("#### Overlapping Results")
        if _ov:
            _ov_data = [
                {
                    "Chunk ID": _item["chunk_id"],
                    "Document": _item["document_name"],
                    "Keyword Rank": _item["keyword_rank"],
                    "Semantic Rank": _item["semantic_rank"],
                }
                for _item in _ov
            ]
            st.table(pd.DataFrame(_ov_data))
        else:
            st.info(
                "No overlapping chunks found. "
                "This may indicate that the two methods are retrieving different kinds of evidence."
            )

        with st.expander("How to interpret retrieval comparison"):
            st.markdown(
                "- **Keyword search** is useful when the query uses the same terms as the document.\n"
                "- **Semantic search** is useful when the query uses different wording but similar meaning.\n"
                "- **Overlap** between methods can strengthen confidence that a chunk is relevant.\n"
                "- **Differences** between methods are useful for review, not automatically errors.\n"
                "- Retrieval comparison helps diagnose whether chunking, query wording, "
                "or embedding quality needs improvement."
            )

        with st.expander("Limitations and responsible use"):
            for _lim in _comp["limitations"]:
                st.markdown(f"- {_lim}")

        _safe_q = (
            "".join(c if c.isalnum() or c == " " else "-" for c in _comp["query"])[:40]
            .strip()
            .replace(" ", "-")
            .lower()
        )
        st.download_button(
            "⬇️ Download comparison report (.md)",
            data=_generate_comparison_md(_comp),
            file_name=f"retrieval-comparison-{_safe_q}.md",
            mime="text/markdown",
        )

        ui.render_prototype_notice(
            "This comparison is a <strong>prototype</strong> using synthetic documents. "
            "Results are starting points for human review, not final authority."
        )


# ── Mini Answer Report ─────────────────────────────────────────────────────────
elif page == "📄  Mini Answer Report":
    from src.report_generator import (
        generate_markdown_answer_report as _gen_report,
        create_report_filename as _safe_filename,
        build_report_data_from_session_state as _build_report_data,
        get_default_report_limitations as _default_limitations,
    )

    _DEFAULT_REVIEWER_NOTES_TEXT = (
        "Check whether the retrieved chunks directly support the answer.\n"
        "Review surrounding source-document sections.\n"
        "Confirm whether the answer misses important policy context.\n"
        "Check whether human review, escalation, or governance controls are needed.\n"
        "Treat this as evidence support, not final authority."
    )

    ui.render_page_header(
        "Mini Answer Report",
        "Downloadable Markdown report from RAG Q&A output — Phase 8",
    )

    st.warning(
        "Use synthetic or approved documents only. Do not upload, paste, or process "
        "real learner data, safeguarding case details, confidential client records, "
        "staff HR data, personal data, or regulated information."
    )

    _rag_response = st.session_state.get("last_rag_response")

    if not _rag_response:
        st.markdown("**Complete these steps first:**")
        ui.render_pipeline_steps([
            "Go to Chunking Explorer and generate chunks.",
            "Go to Embedding Index Builder and generate embeddings, then build the FAISS index.",
            "Go to RAG Q&A and ask a policy question.",
            "Optional: go to Retrieval Comparison to include comparison data in the report.",
            "Return here to generate and download the Mini Answer Report.",
        ])
        st.stop()

    _rpt_question = st.session_state.get("last_rag_question", "")
    _rpt_answer = st.session_state.get("last_rag_answer", "")
    _rpt_evidence = st.session_state.get("last_rag_evidence", []) or []
    _rpt_topics = (_rag_response or {}).get("detected_topics", [])
    _rpt_comparison = st.session_state.get("last_retrieval_comparison")

    _rmc1, _rmc2, _rmc3, _rmc4 = st.columns(4)
    with _rmc1:
        _q_preview = (_rpt_question[:30] + "...") if len(_rpt_question) > 30 else _rpt_question
        ui.render_metric_card("Question", "Ready", _q_preview or "—")
    with _rmc2:
        ui.render_metric_card("Evidence items", str(len(_rpt_evidence)), "retrieved chunks")
    with _rmc3:
        ui.render_metric_card("Topics", str(len(_rpt_topics)), "detected")
    with _rmc4:
        ui.render_metric_card(
            "Comparison",
            "Yes" if _rpt_comparison else "No",
            "retrieval comparison available",
        )

    st.markdown("#### Current RAG Q&A result")
    with st.expander("Question and answer preview", expanded=True):
        st.markdown(f"**Question:** {_rpt_question or '—'}")
        st.markdown(f"**Answer:** {_rpt_answer or '—'}")
        if _rpt_topics:
            st.caption(f"Topics: {', '.join(_rpt_topics)}")

    st.markdown("#### Report settings")

    _default_title = "Semantic RAG Policy Answer Report"
    if _rpt_question:
        _title_words = _rpt_question.split()[:5]
        _default_title = "RAG Answer Report — " + " ".join(_title_words)

    _rpt_title = st.text_input("Report title", value=_default_title)
    _include_comparison = st.checkbox(
        "Include retrieval comparison section",
        value=bool(_rpt_comparison),
    )
    _max_evidence = st.slider("Maximum evidence items in report", 1, 10, 8)
    _reviewer_notes_input = st.text_area(
        "Reviewer notes (one per line)",
        value=_DEFAULT_REVIEWER_NOTES_TEXT,
        height=120,
    )

    if st.button("📄 Generate Report"):
        _report_data = _build_report_data(dict(st.session_state))
        _report_data["report_title"] = _rpt_title.strip() or "Semantic RAG Policy Answer Report"
        _report_data["reviewer_notes"] = [
            line.strip()
            for line in _reviewer_notes_input.split("\n")
            if line.strip()
        ]
        if not _include_comparison:
            _report_data["comparison_result"] = None
        _report_data["evidence_items"] = _report_data["evidence_items"][:_max_evidence]

        _rpt_md = _gen_report(_report_data)
        _rpt_filename = _safe_filename(_report_data["report_title"])

        st.session_state["last_answer_report_markdown"] = _rpt_md
        st.session_state["last_answer_report_data"] = _report_data
        st.session_state["last_answer_report_filename"] = _rpt_filename
        st.rerun()

    _rpt_md_out = st.session_state.get("last_answer_report_markdown")
    if _rpt_md_out:
        st.markdown("#### Report preview")
        with st.expander("Preview full report", expanded=False):
            st.markdown(_rpt_md_out)

        _rpt_fn_out = st.session_state.get("last_answer_report_filename", "semantic-rag-answer-report.md")
        st.download_button(
            "⬇️ Download report (.md)",
            data=_rpt_md_out,
            file_name=_rpt_fn_out,
            mime="text/markdown",
        )

        with st.expander("Limitations and responsible use"):
            for _lim in _default_limitations():
                st.markdown(f"- {_lim}")

    ui.render_prototype_notice(
        "This report is a <strong>prototype output</strong> using synthetic documents. "
        "It is intended for review, learning, and demonstration — not production use."
    )
