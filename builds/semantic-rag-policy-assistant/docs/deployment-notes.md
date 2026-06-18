# Deployment Notes — Semantic RAG Policy Assistant

**Build 3 · BrightPath ChatGPT Mastery Project**

---

## Prototype Status

> **This is a production-style prototype, not a production system.**

It is designed for local demonstration, portfolio use, and client walkthroughs using synthetic documents. It has no authentication, no access control, no audit logging, and no persistent storage. It must not be used with real learner data, safeguarding information, confidential client records, staff HR data, personal data, or regulated information without appropriate governance and security controls in place.

---

## Local Run (Recommended for Demo and Development)

### Step 1 — Clone or navigate to the project

```bash
cd 10-builds/semantic-rag-policy-assistant
```

### Step 2 — Create and activate a virtual environment

```bash
# macOS / Linux
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run the app

```bash
streamlit run app.py
```

Opens at `http://localhost:8501` by default.

### Step 5 — Run tests

```bash
pytest
```

All 429 tests run without internet access, model downloads, or external services.

---

## Model Download Note

The first time the **Embedding Index Builder** page is used, it will download the `sentence-transformers/all-MiniLM-L6-v2` model from Hugging Face (~90 MB). This requires internet access on the first load only. The model is then cached locally.

If you are demoing in an environment with unreliable internet:

1. Run the Embedding Index Builder once before the demo while connected to the internet
2. The model will be cached in `~/.cache/huggingface/` (macOS/Linux) or `%USERPROFILE%\.cache\huggingface\` (Windows)
3. Subsequent runs will use the cached model without internet access

---

## Streamlit Community Cloud (Public Demo Option)

For a public portfolio link or client access, the app can be deployed to Streamlit Community Cloud at no cost.

### Prerequisites

- A GitHub account
- The repository pushed to GitHub (public or private)
- `requirements.txt` present at the root of the deployed folder
- `app.py` present at the root of the deployed folder

### Steps

1. Push the `semantic-rag-policy-assistant/` folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in
3. Create a new app:
   - Repository: your GitHub repo
   - Branch: `main`
   - Main file path: `app.py` (or the path relative to the repo root)
4. Click Deploy
5. The app will be publicly accessible at a `*.streamlit.app` URL

### Notes for Streamlit Community Cloud

- The sentence-transformers model will be downloaded on first deploy — allow a few minutes for cold start
- Synthetic documents in `data/synthetic_documents/` will be included if committed to the repository
- Do not commit real documents, API keys, `.env` files, or credentials to the repository
- Community Cloud apps are public by default — only use with synthetic documents
- Session state resets when the browser is closed or the app restarts

---

## Environment Variables

This prototype does not require any API keys or environment variables for its core functionality.

If you have a `.env.example` file, copy it to `.env`:

```bash
cp .env.example .env
```

No values need to be filled in for local use. The `.env` file is included in `.gitignore`.

---

## Requirements

Key dependencies from `requirements.txt`:

| Package | Purpose |
|---|---|
| `streamlit` | Web UI |
| `pandas` | Data tables |
| `numpy` | Numerical operations |
| `sentence-transformers` | Local embedding model |
| `faiss-cpu` | FAISS vector index |
| `pytest` | Test runner |

All processing runs locally. No OpenAI, Anthropic, or external AI service is required.

---

## What Not To Deploy Yet

Before deploying with any documents other than the included synthetic files:

- Do not upload real learner data, safeguarding case details, confidential client records, staff HR data, personal data, or regulated information
- Do not claim production readiness without a full governance review
- Do not deploy to a shared or public environment without authentication and access control
- Do not skip the DPIA and legal review required before processing real personal or sensitive data

---

## Future Production Considerations

If this architecture is adapted for real organisational use, the following must be in place before any production deployment:

| Requirement | Notes |
|---|---|
| Authentication | User login and session management |
| Access control | Role-based access to document sets and query logs |
| Secure document upload | Validated upload with file-type checking, size limits, content scanning |
| Secure storage | Encrypted document and index storage |
| Audit logging | Record all queries, retrieved chunks, and generated answers |
| Data retention policy | Define how long documents and session data are retained and deleted |
| Privacy / DPIA review | Data Protection Impact Assessment before processing personal data |
| Responsible owner | Named individual accountable for the system and its outputs |
| Legal/safeguarding/compliance review | Where the tool will be used in regulated contexts |
| Model governance | Record which models are used, when updated, and how quality is monitored |
| Monitoring and evaluation | Track retrieval quality and system behaviour over time |
| Incident reporting | Procedure for data incidents or unexpected outputs |

No production deployment should proceed without all relevant items from the above list reviewed and addressed.

---

*Build 3 · Semantic RAG Policy Assistant · BrightPath ChatGPT Mastery Project*
*All documents used in this prototype are synthetic and for demonstration purposes only.*
