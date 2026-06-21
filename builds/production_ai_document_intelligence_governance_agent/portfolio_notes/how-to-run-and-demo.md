# Build 10 Run and Demo Guide

# Production AI Document Intelligence & Governance Agent

## 1. What This Programme Is

This programme is a production-style AI document intelligence and governance application.

It allows an organisation to load documents, break them into searchable sections, build a semantic search index, ask questions over the documents, receive evidence-based answers with citations, detect governance risks, and generate a structured report.

In simple terms, this app helps answer questions such as:

* What do our documents say?
* Where is the evidence?
* What risks are hidden in the content?
* Which AI use cases are safe to pilot?
* What should humans review before taking action?
* How can this information be turned into a useful report?

This is not just a chatbot. It is a full document intelligence workflow.

The programme demonstrates how AI can support professional work in organisations such as:

* training providers,
* universities,
* councils,
* charities,
* HR teams,
* compliance teams,
* operations teams,
* professional service firms.

The app is designed as a local, portfolio-ready prototype. It shows production-style thinking, but it is not claiming to be a fully deployed enterprise SaaS product.

---

## 2. Why This Build Matters

Many organisations want to use AI, but they face three major problems.

First, they have too many documents. Staff waste time reading policies, reports, guidance notes, workflows, and templates manually.

Second, they do not fully trust AI outputs. A normal chatbot can sound confident even when it is wrong. That is risky in education, public services, compliance, HR, safeguarding, and governance.

Third, they need safe AI adoption. It is not enough to say "use ChatGPT". Organisations need boundaries, review steps, risk flags, and human approval.

This build solves those problems by combining:

* semantic document search,
* evidence-based answering,
* source citations,
* governance risk checks,
* human review guidance,
* report generation,
* evaluation metrics,
* synthetic safe sample documents,
* and a tested modular codebase.

A potential client should be impressed because this app shows that the developer understands both sides of AI delivery:

1. the technical side: embeddings, retrieval, chunking, search, Streamlit, testing;
2. the consulting side: risk, governance, human review, data protection, client reporting.

That combination is valuable.

---

## 3. How This Build Fits the Portfolio

The public portfolio now has 10 builds.

Earlier builds show different parts of the AI consulting journey. Build 10 is the flagship technical build.

The important progression is:

| Build    | Role                                                        |
| -------- | ----------------------------------------------------------- |
| Build 2  | Basic keyword document search foundation                    |
| Build 3  | Semantic retrieval using sentence-transformers and FAISS    |
| Build 10 | Production-style document intelligence and governance agent |

Build 10 is stronger than its predecessor baseline because it is not just retrieval. It combines retrieval with governance, reporting, evaluation, screenshots, documentation, and 386 passing tests.

It is also stronger than a basic chatbot because it does not simply generate answers from nowhere. It retrieves evidence from documents and shows where the answer came from.

---

## 4. What the App Does from Start to Finish

The complete workflow is:

```text
Load documents
→ clean text
→ split text into chunks
→ create semantic embeddings
→ build vector index
→ search relevant evidence
→ answer questions with citations
→ detect governance risks
→ generate report
→ review evaluation metrics
```

Each stage has a purpose.

The app does not jump straight from document to answer. It shows the internal pipeline so that the user can understand, inspect, and trust the process.

---

## 5. How to Run the Programme

### Step 1: Open the project folder

In your terminal, go to the public portfolio repository:

```bash
cd path/to/rashid-ai-consult-portfolio
```

Then go into the Build 10 folder:

```bash
cd builds/production_ai_document_intelligence_governance_agent
```

### Step 2: Create a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install the requirements

```bash
pip install -r requirements.txt
```

This installs the Python packages needed for the app, including Streamlit, sentence-transformers, FAISS, pandas, numpy, and pytest.

### Step 4: Run the tests

Before running the app, prove the code works:

```bash
pytest
```

Expected result:

```text
386 passed
```

This matters because a serious technical reviewer wants to see that the project is tested, not just visually impressive.

### Step 5: Compile-check the app

```bash
python -m py_compile app.py
```

If there is no output, the app has no Python syntax errors.

### Step 6: Run the Streamlit app

```bash
streamlit run app.py
```

Streamlit will open the app in your browser.

If it does not open automatically, the terminal will show a local URL, usually something like:

```text
http://localhost:8501
```

If running through the full portfolio launcher or Docker setup, Build 10 may be available on:

```text
http://localhost:8510
```

---

## 6. How to Run the Full Portfolio

If the public portfolio has a launch script, you can run all builds using:

```bash
./launch_all.sh
```

If Docker Compose is configured, you can run:

```bash
docker compose up --build
```

Then open the Build 10 service on its assigned port:

```text
http://localhost:8510
```

The exact port is also listed in the public portfolio README.

---

## 7. The Folder Structure and Why It Matters

The Build 10 folder is structured like a professional software project.

```text
production_ai_document_intelligence_governance_agent/
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── data/
├── logic/
├── tests/
├── screenshots/
└── portfolio_notes/
```

### `app.py`

This is the main Streamlit application. It controls the user interface, page navigation, session state, and how the logic modules are called.

### `data/`

This contains synthetic sample documents. These are fictional documents created for safe demonstration. They avoid real learner data, real staff data, real safeguarding records, or private client information.

This is important because public AI demos should not contain sensitive data.

### `logic/`

This contains the actual application logic. The logic is separated into modules rather than being placed inside one giant file. This is a sign of better software engineering.

Logic modules include:

* document loading,
* text cleaning,
* chunking,
* embeddings,
* vector indexing,
* retrieval,
* answer generation,
* governance checks,
* report building,
* evaluation,
* UI components.

This modular structure makes the project easier to test, debug, extend, and explain.

### `tests/`

This contains the pytest test suite. The project has 386 passing tests.

The tests matter because they prove the internal functions behave as expected. They also show that the developer can build reliable software, not just a nice-looking demo.

### `screenshots/`

This contains visual evidence of the app. Screenshots help portfolio reviewers quickly understand what the app does without having to run it immediately.

### `portfolio_notes/`

This contains explanation documents for reviewers and potential clients. These notes explain the architecture, limitations, demo script, build summary, and what to inspect first.

This is important because a portfolio should not only contain code. It should help the reader understand the business value and technical choices.

---

## 8. The Logic Explained in Plain English

### 8.1 Document Loading

The first step is loading documents.

The app reads synthetic sample files from the `data/` folder. These include AI policy notes, staff guidance, workflow descriptions, safeguarding boundary notes, and pilot evaluation documents.

The loader turns each file into a structured document object with:

* document ID,
* source name,
* text content,
* metadata.

Why this matters:

A document intelligence system needs to know where every piece of text came from. Without source tracking, citations and governance review become unreliable.

---

### 8.2 Text Cleaning

Raw text is often messy. It may contain extra spaces, repeated blank lines, strange formatting, or inconsistent line breaks.

The text cleaning stage improves readability while preserving meaning.

It handles:

* repeated whitespace,
* unnecessary blank lines,
* leading/trailing spaces,
* formatting consistency.

Why this matters:

Clean text improves chunking, search quality, and answer quality. If the text is messy, the AI system may retrieve poor evidence.

---

### 8.3 Chunking

Large documents are too big to search or answer from directly. The app splits them into smaller sections called chunks.

Each chunk has:

* chunk ID,
* source document,
* chunk index,
* text,
* word count,
* metadata.

Example:

```text
Document: staff_ai_guidance.md
Chunk ID: staff_ai_guidance_chunk_003
Text: Staff must not enter learner names, safeguarding notes...
```

Why this matters:

AI retrieval works better when the system searches smaller, focused pieces of evidence rather than entire documents. Chunking also makes citations possible.

---

### 8.4 Embeddings

An embedding is a numerical representation of text. It converts a sentence, paragraph, or document chunk into a vector of numbers.

The idea is that similar meanings should have similar vectors.

For example:

```text
"Do not enter learner data into ChatGPT"
```

and

```text
"Staff must avoid putting personal learner information into AI tools"
```

may use different words, but they mean similar things. A semantic embedding model recognises that similarity better than simple keyword search.

Why this matters:

Keyword search only finds matching words. Semantic search finds related meaning. That is why Build 10 is stronger than a simple keyword tool.

---

### 8.5 Vector Index

Once chunks have embeddings, the app stores them in a vector index.

A vector index allows fast similarity search. When the user asks a question, the app embeds the question and compares it to the stored document chunk embeddings, returning a ranked list of the most relevant chunks.

Why this matters:

Without an index, searching through many embeddings would be slow and inefficient. A vector index makes semantic document search practical.

---

### 8.6 Semantic Search

Semantic search allows the user to type a query such as:

```text
What should staff avoid putting into ChatGPT?
```

The app retrieves evidence chunks that are semantically related, even if the documents do not use exactly the same wording.

The app shows:

* ranked results,
* similarity scores,
* source document,
* chunk ID,
* evidence preview.

Why this matters:

A potential client can see that the app is not simply guessing. It is retrieving evidence from documents. This creates trust.

---

### 8.7 Evidence-Based Q&A

The user asks a question, such as:

```text
What low-risk AI workflows should we pilot first?
```

The app then:

1. embeds the question,
2. retrieves relevant document chunks,
3. generates an evidence-based answer,
4. includes citations,
5. explains limitations.

If the evidence is weak, the app says so rather than inventing an answer.

Why this matters:

This is a safer alternative to a normal chatbot. It is grounded in the documents and shows its evidence. A client will be impressed because the app behaves like a careful analyst, not a reckless text generator.

---

### 8.8 Citations

Citations show where the answer came from. A citation includes:

* source document,
* chunk ID,
* evidence snippet.

Why this matters:

In professional settings, people do not just want an answer. They want to know where it came from and whether they can check the source. Citations make the system transparent and auditable.

---

### 8.9 Governance and Risk Review

The app does not only answer questions. It also checks for risk.

The governance review layer flags categories such as:

* learner or personal data,
* safeguarding or vulnerable users,
* assessment or grading decisions,
* disciplinary issues,
* complaints,
* funding eligibility,
* confidential business information,
* missing human approval.

The checks are rule-based. This means they are transparent and explainable. The app does not pretend the risk detection is perfect.

Why this matters:

Many AI demos focus only on productivity. This build also focuses on responsibility. That is important for education, public services, charities, HR, and compliance-heavy organisations. A potential client may be impressed because this shows you understand the real barriers to AI adoption.

---

### 8.10 Report Builder

The report builder turns the analysis into a structured consulting-style report including:

* executive summary,
* documents analysed,
* evidence retrieved,
* grounded answer,
* citations,
* governance risk flags,
* recommended next steps,
* human review checklist,
* limitations and responsible use.

Why this matters:

Clients do not only want a tool. They want outputs they can use in meetings, planning, and decision-making. The report builder connects technical AI capability with consulting delivery.

---

### 8.11 Evaluation Dashboard

The evaluation dashboard helps users inspect how well the system is performing. It shows:

* number of documents and chunks,
* embedding dimension,
* retrieval scores,
* coverage grade,
* groundedness checklist,
* risk flag summary,
* manual evaluation form.

Why this matters:

A serious AI system should be evaluated. The evaluation dashboard shows maturity. It proves you are thinking about quality, not just functionality.

---

## 9. The 10 App Pages Explained

### Page 1: Home

Sets expectations. Explains the purpose, pipeline, and boundaries before the user presses anything. A client should immediately see this is about document intelligence, evidence, governance, and human review.

### Page 2: Document Library

Loads and displays the documents. Warns users not to upload real personal, learner, safeguarding, or confidential data. Safe data handling is built into the workflow from the beginning.

### Page 3: Document Processing

Shows what was loaded and configures chunking parameters. Gives transparency — users can see the app has actually processed the documents.

### Page 4: Chunk Explorer

Lets users inspect individual chunks. Helps build trust by making the retrieval inputs visible before any search is run.

### Page 5: Embedding Index

Builds the semantic vector index. Makes the hidden AI process visible — shows that semantic vectors are being used rather than simple keyword matching.

### Page 6: Semantic Search

Searches documents by meaning, returning ranked evidence with similarity scores. Demonstrates the core technical capability.

### Page 7: RAG Q&A

Answers natural language questions with grounded evidence and citations. The page most clients will immediately understand.

### Page 8: Governance Review

Detects governance risks across 8 categories and recommends human action. Where the app becomes more than a document chatbot — it becomes a responsible AI adoption tool.

### Page 9: Report Builder

Generates a structured 10-section Markdown report. Turns technical analysis into a usable business deliverable.

### Page 10: Evaluation Dashboard

Shows retrieval coverage, groundedness checklist, risk summary, and a manual evaluation form. Demonstrates that quality is being measured, not assumed.

---

## 10. Why a Potential Client Would Be Impressed

### It solves a real problem

Organisations have too many documents and not enough time. This app helps them find answers faster.

### It shows evidence

The app does not just answer. It shows where the answer came from. That is important for trust.

### It includes governance

Many AI tools ignore risk. This app directly addresses personal data, safeguarding, assessment decisions, complaints, funding eligibility, and human review — highly relevant in education, public sector, HR, and compliance environments.

### It is tested

386 passing tests show engineering discipline. A client or technical reviewer can see this is not just a one-page prototype thrown together quickly.

### It is modular

The code is separated into logical modules. This means the system can be extended later — authentication, database storage, audit logs, OpenAI API, FastAPI backend, Next.js frontend.

### It is honest about limits

The app clearly explains that risk detection is rule-based, answers need human review, this is not legal advice, and this is not a deployed enterprise SaaS platform. This honesty makes the demo more credible, not less.

### It connects technical AI to consulting value

The app supports a real consulting offer: AI workflow audits, safe-use rules, pilot planning, document intelligence, governance review, and management reports.

---

## 11. Demo Script: How to Present It to a Client

```text
This is a production-style document intelligence and governance prototype.

The idea is simple: many organisations want to use AI, but they do not just need a chatbot. They need evidence, governance, and human review.

Here, we load a set of synthetic organisation documents. The system cleans the text, chunks the content, creates semantic embeddings, and builds a searchable vector index.

Then we can ask natural language questions, such as: "What should staff avoid putting into ChatGPT?" or "Which AI workflows are safest to pilot first?"

The app retrieves evidence from the documents and shows citations, so the answer is grounded rather than invented.

The governance review page then flags possible risks, such as learner data, safeguarding, assessment decisions, or missing human approval.

Finally, the report builder turns the findings into a structured mini-report that a manager could use for an AI adoption discussion.

This is not positioned as a finished enterprise platform. It is a local production-style prototype showing how a safer document intelligence workflow could be designed for an organisation.
```

---

## 12. Best Demo Questions to Ask in the App

```text
What should staff avoid entering into ChatGPT?
```

```text
Which low-risk workflows should BrightPath pilot first?
```

```text
What human approval steps are recommended before using AI-generated content?
```

```text
What are the main risks of informal ChatGPT use?
```

```text
How should safeguarding concerns be handled?
```

```text
What should be included in a safe AI pilot plan?
```

```text
What evidence supports using AI for lesson planning?
```

These questions naturally trigger retrieval, citations, governance boundaries, and practical recommendations.

---

## 13. What Not to Claim

Do not say:

```text
This is a fully deployed enterprise AI system.
```

Do not say:

```text
This guarantees safe AI use.
```

Do not say:

```text
This replaces compliance staff or safeguarding leads.
```

Do not say:

```text
This gives legal advice.
```

Better wording:

```text
This is a production-style local prototype showing how document intelligence, semantic retrieval, citations, governance checks, and human review can work together.
```

Or:

```text
This demonstrates the architecture and workflow I would use as the foundation for a more customised organisation-specific system.
```

---

## 14. How This Could Become a Real Client Product

A real client version could add:

* secure login and role-based access control,
* organisation-specific document storage,
* PostgreSQL database,
* persistent vector database,
* audit logs,
* cloud deployment,
* OpenAI API or approved enterprise LLM,
* document permission controls,
* export to PDF or Word,
* monitoring and evaluation dashboard.

The technical upgrade path:

```text
Streamlit prototype
→ FastAPI backend
→ Next.js frontend
→ PostgreSQL database
→ vector database
→ authentication
→ audit logs
→ cloud deployment
```

---

## 15. How to Explain the Business Value

The value is:

```text
faster document understanding
+ better evidence visibility
+ safer AI adoption
+ clearer human review
+ structured reporting
+ reduced uncertainty around AI use
```

For a training provider: AI policy review, staff guidance, lesson planning workflow improvement, report structuring, safe-use training, audit preparation.

For a council or public-sector team: policy search, report summarisation, governance review, internal AI adoption planning.

For HR: handbook Q&A, onboarding document search, policy comparison, risk-aware staff guidance.

---

## 16. How to Explain the Technical Value

The technical value is that the app demonstrates:

* semantic search and vector retrieval,
* modular Python architecture,
* test-driven development,
* Streamlit product design,
* synthetic data handling,
* governance rules engine,
* report generation,
* evaluation thinking,
* safe AI system design.

The strongest technical proof: **386 passing tests.**

---

## 17. Recommended Short Portfolio Summary

```text
Build 10 is a production-style AI document intelligence and governance agent. It uses semantic retrieval to search synthetic organisational documents, answer questions with source citations, flag governance risks, and generate a structured report. The build includes a 10-page Streamlit app, modular Python architecture, 8 synthetic documents, 10 screenshots, portfolio notes, and 386 passing tests.
```

---

## 18. Recommended Client-Friendly Summary

```text
This prototype shows how an organisation could use AI to understand internal documents more safely. Instead of giving unsupported chatbot answers, the system retrieves relevant evidence, shows source references, highlights governance risks, and produces a structured report for human review. It is designed to demonstrate how AI can support document-heavy teams without removing human responsibility.
```

---

## 19. Final Explanation

This programme is impressive because it joins together several things that are usually separate:

* AI search,
* document processing,
* governance,
* human review,
* report writing,
* testing,
* portfolio documentation.

That is exactly what organisations need.

A simple chatbot demo is easy to build. A risk-aware document intelligence workflow is much more valuable.

Build 10 shows that the developer can think like:

* a software engineer,
* an AI consultant,
* a governance-aware practitioner,
* a product builder,
* and a business problem solver.

That is why it is the flagship build.
