# Build 11 — Client Demo Script

> For live demos of the application to a client, stakeholder, or interviewer.
> Assumes the app is running locally at http://localhost:8501.
> Total time: 10–15 minutes for the full flow; 5 minutes for the three-page quick demo.

---

## Recommended demo scenario

A training provider wants to know what their policy documents say about staff using AI tools with learner data. They are also worried about whether their existing policies cover governance risks adequately.

---

## Setup before the demo

```bash
cd 10-builds/production_ai_document_intelligence_governance_agent
pip install -r requirements.txt
streamlit run app.py
```

On first run, navigate to **Embedding Index** and click **Load model** ahead of time. The model download (~90MB) takes 30–60 seconds and should not happen during the demo.

Build the index on **Embedding Index** before the demo as well. Once built, it persists in memory for the session.

---

## Demo flow

### 1. Home (1 minute)

Open with: "What this shows is a working prototype of what an internal AI document intelligence tool looks like in practice."

Point to the workflow steps. Explain:
- "It loads your documents, builds a semantic index, and lets you ask questions in plain language."
- "The answers are drawn directly from the documents — nothing is made up."
- "It also checks for governance risks and can generate a report you could share with a QA team or board."

### 2. Document Library (1–2 minutes)

Show the eight documents. Explain:
- "These are synthetic policy documents I created for a fictional training provider — BrightPath Skills Training."
- "In a real system, these would be your AI acceptable use policy, your safeguarding guidance, your data protection notices, and so on."
- "The system works with any Markdown or plain text document. PDF and DOCX support would be the next step."

Click into one or two expanders to show the content. Point to the word counts in the table.

### 3. Document Processing (optional — 30 seconds)

You can skip this if the index is already built. If showing it:
- "This is where you configure how the documents are split into chunks. Smaller chunks give more precise retrieval; larger chunks give more context per result."
- "The default is 200 words with a 40-word overlap at boundaries."

### 4. Embedding Index (1 minute)

Show the model name and dimension:
- "The model is all-MiniLM-L6-v2 from the sentence-transformers library. It converts every chunk of text into a 384-dimensional vector that captures semantic meaning."
- "The index is built locally — no data leaves the machine, no API call is made."
- Show the metrics: total vectors, dimension, index type.
- "FAISS IndexFlatIP gives us exact cosine similarity. On 500 chunks it returns results in under 100 milliseconds."

### 5. Semantic Search (1–2 minutes)

Type the query: **Can staff use ChatGPT with learner data?**

Show the results. Point to:
- The score (cosine similarity, 0–1)
- The score label (Strong / Good / Moderate / Weak)
- The source document and chunk ID
- The coverage metrics row

Explain: "Notice that the top result is from the AI acceptable use policy, and it matches a section about entering learner names into AI tools — even though I didn't use those words in my query. That's semantic matching, not keyword search."

### 6. RAG Q&A (2–3 minutes)

This is the centrepiece of the demo.

Type the same query: **Can staff use ChatGPT with learner data?**

Click **Generate answer**. Walk through:
- The confidence indicator (Strong / Moderate / Weak)
- The grounded answer — point out that it is assembled from the source text, not invented
- The citations table — rank, source document, chunk ID, score
- The expandable source excerpts — "You can always trace the answer back to the exact sentence in the original document"
- The governance alert at the top (if risk flags are detected): "The system also flagged that this query touches on learner data and personal data — which are governance-sensitive categories"

End with: "There is no hallucination risk here because the system is not generating new text. It is selecting and presenting the most relevant passages from your documents."

### 7. Governance Review (1–2 minutes)

Navigate to **Governance Review**.

The risk flags from the last Q&A query are shown automatically at the bottom of the page. You can also click **Scan retrieved chunks** to run a fresh risk scan across the retrieved evidence chunks.

Walk through the risk flags:
- "High-risk flags — things like learner data, safeguarding references, assessment decisions — need immediate human review before any AI output is shared."
- "Medium-risk flags — personal data, confidential information, funding eligibility — need sign-off from an appropriate person."
- "Each flag includes the matched terms and a recommended action. This is not a legal opinion — it is a structured prompt for human judgement."

### 8. Report Builder (1 minute)

Click **Generate report**.

Show the preview briefly, then click **Download report (.md)**.

Say: "This is a leave-behind. A QA manager or compliance lead could read this report, check the citations, and make a decision. The report includes an executive summary, all the evidence, the governance flags, a next-steps section, and a human review checklist."

### 9. Evaluation Dashboard (1 minute)

Show the system configuration metrics and retrieval coverage metrics.

Point to the groundedness checklist: "This tells me that the answer is grounded, citations are present, and multiple sources were consulted."

Mention the manual evaluation form: "In a real deployment, you'd have staff rating responses and logging what was missing. That data feeds into improving the document library and the chunking strategy."

---

## Key talking points

**On accuracy:** "The system is honest about confidence. If it retrieves weak evidence, it says so. If it cannot answer, it says 'Insufficient evidence' rather than guessing."

**On data privacy:** "Nothing leaves the machine. No document content is sent to an API. The embedding model runs locally. This matters a great deal for documents that contain policy guidance about staff, learners, or safeguarding."

**On governance:** "Every page includes a responsible-use notice. The governance check is built into the pipeline, not bolted on afterwards. Human review is mandatory — the system is a tool to support decision-making, not replace it."

**On scalability:** "This runs on a laptop. A production version with a persistent vector store, document upload, and an LLM for prose generation could serve a team of fifty people querying hundreds of documents."

---

## What to avoid saying

**Do not say it is production-ready.** It is a production-style local prototype. It is not deployed, not authenticated, not connected to real documents, and not validated against real organisational risk.

**Do not claim the governance checks are exhaustive.** They cover eight categories relevant to FE training. A real compliance assessment requires qualified professional review.

**Do not demo with real documents.** The tool has not been assessed for use with real personal data, learner records, or safeguarding material. Use only the synthetic documents provided.

**Do not claim the answers are always correct.** The system retrieves and presents the most relevant text it can find. If the answer is not in the documents, the system will say so. If the documents are wrong, the answers will be wrong.

**Do not promise specific features in a production version** unless you have scoped that work separately. Keep the demo grounded in what is shown.

---

## Closing line

"What I've shown you is what responsible AI document intelligence looks like in practice — semantic retrieval, grounded answers, governance checks, and a structured report. All running locally, no external API, no data leaving the building. The next conversation is about what a production version of this would look like for your organisation and your documents."
