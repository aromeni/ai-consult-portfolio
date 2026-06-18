# Deployment Notes — Document Intelligence / RAG Demo

**Build 2 · Prototype v0.6**

---

## Purpose

This document describes simple ways to run or share the Build 2 document intelligence prototype locally and via Streamlit Community Cloud.

---

## Prototype Status

**This is a prototype, not a production system.**

It uses:

- Synthetic Markdown documents (four fictional policy documents)
- Deterministic keyword search
- Deterministic topic detection
- Deterministic evidence extraction
- Deterministic risk and safeguard mapping
- Templated Markdown outputs

It does **not** use:

- External AI APIs
- Embeddings
- Vector databases
- Production document upload
- Authentication or access control
- Secure document storage
- Real client, learner, safeguarding, staff HR, personal, or regulated data

---

## Local Run

**Requirements:** Python 3.10 or later.

```bash
# Navigate to the project
cd 10-builds/document-intelligence-rag-demo

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Opens at `http://localhost:8501`.

---

## Run Tests

```bash
pytest
```

Run from `10-builds/document-intelligence-rag-demo/`. No external services, API keys, or model calls required.

Expected output: **229 tests, all passing.**

---

## Streamlit Community Cloud Option

The app can be shared for demo or portfolio review via Streamlit Community Cloud at no cost.

**High-level steps:**

1. Push the repository to a GitHub account (public or private)
2. Log in at [share.streamlit.io](https://share.streamlit.io) and connect the repository
3. Set the entry point to `app.py` (path: `10-builds/document-intelligence-rag-demo/app.py`)
4. Confirm `requirements.txt` is present at the same path
5. Deploy — Streamlit installs dependencies and starts the app automatically

**Before deploying:**

- Use synthetic demo documents only — do not push real learner data, safeguarding case information, confidential client records, staff HR data, personal data, or regulated information to the repository
- Do not add secrets, API keys, or `.env` files to the repository — use Streamlit's Secrets management if needed in a future phase
- Review what is visible in the public URL before sharing

No database, external API credentials, or environment variables are required for the current build.

---

## What Not To Deploy Yet

Do not deploy this prototype in any context involving:

- Real learner data
- Safeguarding case documents or case notes
- Confidential client records or contracts
- Staff HR or disciplinary files
- Personal data of any kind
- Regulated information (financial, medical, legal, etc.)
- Production client use or operational decision-making
- Claims of legal, compliance, or safeguarding authority
- Unsupervised or automated decision-making without human review

This prototype is suitable for portfolio demonstration, learning, internal experimentation with synthetic documents, and early consulting conversation support only.

---

## Environment Variables

No real API keys, model credentials, or database connection strings are required in the current version. The build is entirely local and deterministic.

- `.env.example` exists in the project root as a template for future extension
- Copy it to `.env` during local setup if needed: `cp .env.example .env`
- The `.env` file is listed in `.gitignore` — never commit it
- Never show `.env` contents, secrets, or API keys in screenshots, demos, or shared recordings

---

## Demo Safety Checklist

Before any demo or recorded walkthrough:

- [ ] Confirm all documents loaded are synthetic
- [ ] Clear any typed inputs from a previous session if reusing the browser tab
- [ ] Close or crop out any unrelated browser tabs, secrets, or system notifications
- [ ] Confirm no real client names, learner names, or personal identifiers appear in search fields
- [ ] Confirm no real data, API keys, or environment files are visible on screen
- [ ] Be ready to explain that all matching is keyword-based (not AI-generated)
- [ ] Be ready to explain that human review of all outputs is required before acting
- [ ] Be ready to state that this tool does not provide legal, safeguarding, HR, compliance, medical, financial, academic-integrity, or professional advice

---

## Future Production Considerations

If this prototype is extended toward production use, the following should be addressed:

**Access and security:**
- User authentication and role-based access control
- Secure document upload with file type validation and virus scanning
- Secure document storage (encrypted at rest and in transit)
- Audit logging of all queries and document access
- Session isolation for concurrent users

**Data governance:**
- Document retention policy
- DPIA (Data Protection Impact Assessment) where personal or regulated data is involved
- Privacy review and legal sign-off before processing real documents
- Role-based review workflow (so outputs require a named approver before use)

**AI and model governance (if LLMs are added):**
- Citation verification — every AI-generated claim must reference a source document
- Model governance documentation
- Hallucination and bias testing
- Human review requirement before any output is acted on
- Clear disclaimer on all AI-generated outputs

**Infrastructure:**
- Proper hosting with security review
- Monitoring and alerting
- Dependency and security updates

**Professional review:**
- Legal, safeguarding, compliance, and domain expert review before any live use case

---

## Recommended Current Use

Use this version for:

- Portfolio demonstration
- Learning and experimentation with synthetic documents
- Internal capability showcases
- Early consulting conversations to illustrate what document intelligence looks like before embeddings and LLMs are added

Do not use this version for operational decision-making, processing real organisational data, or any regulated use case.

---

*Build 2 · Document Intelligence / RAG Demo · BrightPath ChatGPT Mastery Project*
