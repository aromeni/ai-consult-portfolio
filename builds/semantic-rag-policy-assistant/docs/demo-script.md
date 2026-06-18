# Demo Script — Semantic RAG Policy Assistant

**Build 3 · Phase 8 · BrightPath ChatGPT Mastery Project**

---

## Demo Purpose

Walk an audience through the full semantic RAG pipeline — from loading synthetic policy documents through grounded Q&A, retrieval comparison, and a downloadable Markdown report — in a clear, practical, 15–20 minute demonstration.

---

## Audience

- AI consultant clients (training providers, schools, SMEs considering semantic AI search)
- Governance leads and managers evaluating RAG before vendor commitment
- Developers learning the RAG pipeline
- Portfolio reviewers (LinkedIn, GitHub, prospective employers)

---

## Demo Setup

Before you start:

1. Run: `streamlit run app.py` from `semantic-rag-policy-assistant/`
2. Confirm: app opens at `http://localhost:8501`
3. Confirm: sidebar shows all 8 pages
4. The first run of the Embedding Index Builder will download the sentence-transformers model. Do this before the demo to avoid waiting.
5. Use the synthetic documents already in `data/synthetic_documents/` — do not use real documents

---

## Demo Scenario

> **A UK training provider wants to review their AI policy documents.**
> A member of staff asks: **"Can we put learner names into ChatGPT?"**
> The question is common, practical, and policy-relevant — a good test for any RAG system.

---

## Demo Flow

---

### Step 1 — Home Page

**What to show:**
- The RAG pipeline diagram at the top: `Documents → Chunks → Embeddings → Vector Index → Semantic Search → Grounded Answer → Report`
- The phase status cards showing all phases complete
- The live metrics: 4 documents, total word count, chunk count, phase 8

**What to say:**
> "This is the home page of the Semantic RAG Policy Assistant. It's a prototype that shows every step of a RAG pipeline — from loading policy documents through to a grounded answer and a downloadable report. Everything runs locally. No OpenAI API. No LangChain. No cloud services. Just Python, Streamlit, sentence-transformers, and FAISS."

**Key message:** This is a complete, locally-run RAG pipeline built from scratch.

---

### Step 2 — Document Library

**What to show:**
- The document metadata table: four synthetic documents, word counts
- Click one document to preview it — show the "Synthetic — for demonstration purposes only" header

**What to say:**
> "We're working with four synthetic policy documents — an AI acceptable use policy, data protection guidance, safeguarding and AI boundaries, and staff training notes. They're fictional. They contain no real learner names, no real staff data, no confidential information. This is how you prototype safely."

**Key message:** Synthetic documents enable safe, full-pipeline demonstrations.

---

### Step 3 — Chunking Explorer

**What to show:**
- Select All Documents
- Set chunk size 120, overlap 30
- Click Generate Chunks
- Show the summary metrics row: total chunks, documents, average chunk size
- Open one chunk card to show chunk ID, document name, word range, text

**What to say:**
> "Before we can embed these documents, we need to split them into chunks — overlapping segments that can be matched against a query. Overlap is important: it means content near a chunk boundary appears in two adjacent chunks, so we don't miss evidence that spans a boundary."
>
> "The chunk size matters a lot in RAG. Smaller chunks are more precise — you get tighter evidence. Larger chunks give more context but may retrieve irrelevant material. This explorer lets you see the effect directly."

**Key message:** Chunking is a design decision, not a detail. The explorer makes it visible.

---

### Step 4 — Embedding Index Builder

**What to show:**
- Step 1: Generate Embeddings — model name, click button, show summary (384 dimensions, normalised)
- Step 2: Build FAISS Index — select Cosine (IndexFlatIP), click button, show index summary (vectors indexed, dimension, index type)

**What to say:**
> "Now we convert each chunk into a 384-dimensional vector using a sentence-transformers model running locally. This model has learned to represent sentence meaning — similar meanings produce similar vectors, even when the wording is different."
>
> "We then load those vectors into a FAISS index. FAISS is a library for fast vector similarity search. When a user submits a query, we embed that query using the same model and find the most similar chunk vectors in the index."

**Key message:** Local embeddings and FAISS give us semantic retrieval without any external dependency.

---

### Step 5 — Semantic Search

**What to show:**
- Click the suggested query: **"Can staff put learner names into ChatGPT?"**
- Show the ranked result cards: rank, similarity score, document name, chunk text
- Open a result card to show the full chunk text

**What to say:**
> "This is semantic search in action. We've embedded the query using the same model we used for chunks, and FAISS has found the most semantically similar chunks. Notice that the top results come from the AI acceptable use policy and the data protection guidance — the documents most relevant to learner data and AI tool use."
>
> "The scores are cosine similarities. Higher is more similar. They're ranking signals, not confidence scores — a 0.85 doesn't mean 85% accurate. It means this chunk is more similar to the query than those scored lower."

**Key message:** Semantic search finds relevant evidence by meaning, not just by word match.

---

### Step 6 — RAG Q&A

**What to show:**
- Click the suggested question: **"Can staff put learner names into ChatGPT?"**
- Click Generate Answer
- Show the caution box (learner data topic flagged)
- Show the grounded answer in the answer card
- Show the metric cards: question type, detected topics, chunks retrieved
- Expand one or two evidence cards to show chunk text and source
- Show the Limitations expander
- Click the download button

**What to say:**
> "The RAG Q&A page takes the same query, retrieves the top chunks from the FAISS index, and generates a grounded answer based on what was retrieved. The answer references the policy position, the required staff action, and the review reminder."
>
> "Notice the caution flag — the system detected that this question involves learner data, which is a flagged topic requiring extra human care."
>
> "Every evidence card shows exactly which document and chunk the answer is grounded in. There's no black box here. You can see the evidence, read the source, and decide whether the answer is well-supported."
>
> "The limitations section is always shown. This prototype does not provide legal advice. It provides evidence support for human review."

**Key message:** Grounded answers with visible evidence are more trustworthy than black-box generation.

---

### Step 7 — Retrieval Comparison

**What to show:**
- Click the suggested query: **"Can staff put learner names into ChatGPT?"**
- Click Compare Retrieval Methods
- Show the metric cards: keyword results, semantic results, overlapping
- Show the side-by-side columns
- Point to overlap (or lack of it)
- Show the comparison insight box

**What to say:**
> "This page runs both keyword search and semantic search for the same query and shows results side by side. Keyword search finds chunks that contain the exact words — learner, names, ChatGPT. Semantic search finds chunks that are conceptually related, even if the wording differs."
>
> "Overlap between the two methods is a strong signal — if both approaches agree on a chunk, it's likely to be relevant. Differences are equally useful: they show where semantic search adds value that keyword search misses."
>
> "When I'm talking to a client about whether to invest in semantic search, I show them this comparison. It makes the case better than any slide."

**Key message:** Retrieval comparison makes the value of semantic search concrete and visible.

---

### Step 8 — Mini Answer Report

**What to show:**
- Point out the summary metrics: question ready, evidence items, topics, comparison available
- Set a report title
- Click Generate Report
- Expand the report preview — scroll through the 10 sections
- Click Download to save as `.md`

**What to say:**
> "Finally, the Mini Answer Report pulls everything together into a structured, downloadable Markdown document. Ten sections: the question, the answer, detected topics, retrieval setup, retrieved evidence, retrieval comparison summary, caution notes, limitations, reviewer notes, and prototype status."
>
> "A reviewer can open this file, read the evidence, check whether the answer is well-supported, and add their own notes. It's designed for the human-in-the-loop — evidence support for a qualified reviewer, not a replacement for one."

**Key message:** The report makes the full pipeline output reviewable, portable, and auditable.

---

## Responsible Use Message

At the end of every demo, always close with this:

> "Everything you've seen runs entirely locally. No data left this machine. No external AI service was called. The documents are synthetic — no real learner data, no real safeguarding information, no real confidential records were used at any point.
>
> If you want to use something like this with real documents — real policy files, real organisational data — that's a production conversation. It needs a DPIA, legal review, authentication, access control, audit logging, and a responsible owner who understands what the system can and cannot do.
>
> What I've shown you is the architecture and the approach. The prototype proves the concept. Production deployment is a separate, governed process."

---

## Closing Pitch

> "Build 3 is a working demonstration of a full semantic RAG pipeline — documents, chunks, embeddings, vector search, grounded answers, retrieval comparison, and a structured report — built in eight phases, tested with 429 tests, and running locally without any external AI API.
>
> What it proves is that semantic RAG is not magic. It's a pipeline with understandable components, explainable trade-offs, and measurable behaviour. And the responsible-use boundaries are built in at every layer — not added as an afterthought.
>
> This is what a production-style RAG prototype looks like before it becomes a production system."

---

*Build 3 · Semantic RAG Policy Assistant · BrightPath ChatGPT Mastery Project*
*All documents are synthetic. Outputs are indicative only and require human review.*
