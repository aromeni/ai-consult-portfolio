# Demo Script — Document Intelligence / RAG Demo

**Build 2 · Prototype v0.6**
**Updated:** June 2026

---

## Demo Purpose

To show how a document intelligence prototype can search, extract evidence from, and generate structured outputs from synthetic policy documents — transparently, safely, and without external AI APIs.

---

## Audience

- Training provider managers or governance leads evaluating AI policy tools
- Consultants or developers reviewing the build
- Portfolio reviewers

---

## Demo Setup

```bash
cd 10-builds/document-intelligence-rag-demo
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

**All data shown is synthetic. Do not use real learner data, safeguarding information, confidential client records, staff HR data, personal data, or regulated information at any point.**

---

## Demo Scenario

**Organisation:** BrightPath Skills Training (synthetic)
**Context:** An AI consultant is helping a small training provider review their AI governance policies before deploying AI tools. The provider has four synthetic policy documents and wants to identify risks, extract evidence, and produce a brief for the board.

**Duration:** 10–15 minutes for the full flow. 5 minutes for a focused Q&A demonstration.

---

## Demo Flow

---

### Step 1: Home Page

**What to show:**
Navigate to the Home page. Point to the responsible-use notice and the document list.

**What to say:**
> "This prototype loads four synthetic policy documents and lets a consultant search, extract evidence, and generate governance briefs — all without external AI APIs. Every result is keyword-based, so you can see exactly why each line was returned."

**Key message:** Transparent, auditable, safe foundation. No black-box model calls.

---

### Step 2: Document Library

**What to show:**
Navigate to Document Library. Expand the expander for one document.

**What to say:**
> "Here you can see all four documents with their metadata — word count, line count, file size. These are synthetic policy documents covering acceptable use, data protection, safeguarding boundaries, and staff training notes. In a real deployment this could point to an organisation's live policy folder."

**Key message:** Document metadata is extracted automatically. All four documents are loadable and browsable.

---

### Step 3: Document Viewer

**What to show:**
Navigate to Document Viewer. Select `synthetic-ai-acceptable-use-policy.md`. Type `safeguarding` in the inline search box.

**What to say:**
> "I can search within any document instantly. Here you can see every line in the Acceptable Use Policy that mentions safeguarding — with the line number shown, so you can find the context in the full document below."

**Key message:** Fast, transparent, in-document keyword search with line references.

---

### Step 4: Policy Q&A — Keyword Search Tab

**What to show:**
Navigate to Policy Q&A. Make sure the Keyword Search tab is selected. Click the suggested search `learner data`.

**What to say:**
> "The keyword search runs across all four documents at once. Each result shows the document name, line number, relevance count, and which terms matched. Notice that a higher relevance count means the term appeared more times in that line."

**Expected output:** 10–20 matching lines from multiple documents, ranked by relevance.

**Key message:** Multi-document search in one step, with transparent relevance ranking.

---

### Step 5: Policy Q&A — Evidence-Based Q&A Tab

**What to show:**
Click the Evidence-Based Q&A tab. Click the suggested question "Can staff enter learner data into AI tools?". Click **Generate answer**.

**What to say:**
> "This is the evidence-based Q&A mode. When you ask a policy question, the tool detects the relevant policy topics — here it detected learner data, data minimisation, anonymisation, approved tools, and human review. It then retrieves supporting evidence snippets from the documents, generates a structured answer, and shows the recommended safeguards and responsible owners."

**Expected output:**
- Detected topics: learner data, approved tools, data minimisation, anonymisation, human review
- Short answer: staff should not enter identifiable learner data into AI tools
- Evidence snippets from the documents with source and line references
- Recommended safeguards list
- Responsible owners
- Limitations expander

**What to say about limitations:**
> "Notice the limitations section — it tells you this is keyword-based matching, not a legal or safeguarding expert. Human review is still required. This transparency is the point."

**Key message:** Evidence-based Q&A without any AI model call. Every match is traceable, every limitation is explicit.

---

### Step 6: Evidence Extraction

**What to show:**
Navigate to Evidence Extraction. Click the suggested topic `safeguarding`. Select All documents. Click **Extract evidence**.

**What to say:**
> "Evidence Extraction lets you run a single topic across all four documents and see every relevant line ranked by relevance. Notice each result shows the document name, line number, relevance count, and which keywords triggered the match."

**Expected output:** 10–20 evidence items across the four documents.

Then change to `human review`. Click Extract again.

**What to say:**
> "Different topic, same four documents. 13 topics are supported in total — everything from learner data and safeguarding to copyright and incident reporting."

**Key message:** Cross-document, topic-based evidence extraction in one click.

---

### Step 7: Risk and Safeguard Summary

**What to show:**
Navigate to Risk and Safeguard Summary. Click the **Data protection** topic set button. Click **Generate summary**.

**What to say:**
> "This page generates a structured risk and safeguard summary for selected topics — showing the risk title, why it matters, recommended safeguards, suggested owner, and supporting evidence snippets. A governance lead can use this to check whether their policy library covers the key risk areas."

**Expected output:** Summary for learner data, data minimisation, anonymisation, retention, and incident reporting — each with evidence coverage notes and safeguards.

**What to say:**
> "Notice the coverage note on each topic — it tells you whether multiple snippets were found, limited evidence, or no direct evidence. That tells you where the policy gaps might be."

**Key message:** Cross-document, cross-topic governance overview. Downloadable as Markdown.

---

### Step 8: Mini Brief

**What to show:**
Navigate to Mini Brief. Click the **Learner Data** preset. Click **Generate brief**. Show the short answer, the full brief preview, then click Download.

**What to say:**
> "The Mini Brief pulls everything together — the question, documents reviewed, short answer, evidence found, key risks, recommended safeguards, next actions, limitations, and reviewer notes — into a single downloadable Markdown document. The consultant can edit it, send it to the governance lead, or use it as the starting point for a board discussion."

**Expected output:**
- 3-column metrics (topics, evidence snippets, risk areas)
- Short answer in an info box
- Full 9-section brief in a preview expander
- Download button producing a timestamped `.md` file

**Key message:** Evidence extracted → brief generated → downloadable in one session.

---

## Responsible Use Message

At each stage where it is relevant, return to this message:

> "Everything in this demo uses synthetic documents. The same tool with real documents would require appropriate data handling controls, governance approval, and human review of every output before acting. This prototype shows the capability — not a ready-to-deploy product."

---

## Closing Pitch

> "What you've seen is the foundation for document intelligence. We've gone from document loading through keyword search, topic-based evidence extraction, risk and safeguard mapping, mini brief generation, and evidence-based Q&A — all without a single external API call.

> This is the right way to start before adding embeddings and a language model. You know what your documents say. You know what evidence exists for each risk topic. You know what the gaps are. Now you're ready to add AI on top of a solid, auditable foundation.

> The next phase adds local embeddings and semantic search. After that, LLM-assisted answers with strict evidence grounding and source citation. But the hard governance work — knowing your documents, knowing your risks, knowing what human review is required — is already done."

---

## What NOT to Show

- Do not demonstrate with any real learner names, attendance records, or assessment data
- Do not demonstrate with any real safeguarding concerns or case details
- Do not enter real client names, contractual information, or HR data
- Do not use real staff names, addresses, or personal identifiers
- Keep all searches, questions, and demonstrations within the synthetic documents provided

---

*Demo script for Build 2 · Document Intelligence / RAG Demo*
*All data used in this demo is synthetic and fictional.*
