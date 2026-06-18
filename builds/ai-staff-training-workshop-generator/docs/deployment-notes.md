# Deployment Notes — AI Staff Training and Workshop Generator

**Build 4 · BrightPath ChatGPT Mastery Project**

---

## Prototype Status

> **This is a production-style prototype, not a production training compliance system.**

Build 4 is designed for local demonstration use with synthetic scenarios only. It has not been reviewed for production deployment, real client use, or regulated data handling.

---

## Local Run

**Requirements:** Python 3.10 or later.

```bash
# 1. Navigate to the project
cd 10-builds/ai-staff-training-workshop-generator

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Opens at `http://localhost:8501` by default.

**Quick start:** navigate to Organisation Scenario → **Load BrightPath Demo Scenario**.

---

## Dependencies

`requirements.txt` contains:

```
streamlit
pandas
pytest
```

No external LLM SDK, no HTTP client for model calls, no vector database, no authentication library.

---

## Running Tests

```bash
pytest
```

Run from `10-builds/ai-staff-training-workshop-generator/`. No API keys or external services required. All 758 tests use synthetic data.

---

## Streamlit Community Cloud — Optional Public Demo

Streamlit Community Cloud allows free public hosting for open-source Streamlit apps. The steps below are for reference only — **review the responsible-use constraints before making any deployment public.**

1. Push the repository to GitHub (ensure no secrets, real client data, or sensitive files are included)
2. Visit [share.streamlit.io](https://share.streamlit.io) and connect to the GitHub repository
3. Set the entry point to `10-builds/ai-staff-training-workshop-generator/app.py`
4. Ensure `requirements.txt` is present in the project directory
5. Use synthetic scenarios only — do not upload or hard-code real client, learner, safeguarding, HR, or personal data

Limitations of Community Cloud deployment for this prototype:
- Session state resets on page refresh — in-memory only, no persistence
- No authentication — public URL is accessible by anyone
- No access control — all session state visible to the session user only, but no user separation
- Not suitable for real organisational data of any kind

---

## What Not to Deploy (Now or Without Governance)

Do not deploy any version of this tool that:

- Handles real learner data, safeguarding case information, or confidential client records
- Handles staff HR data, personal data, or regulated information of any kind
- Makes or supports real safeguarding, HR, compliance, clinical, or legal decisions
- Claims to be a certified or accredited training system
- Operates without a qualified human reviewing all outputs before use

---

## Future Production Considerations

If a future version is extended for real organisational use, the following are required before any production deployment:

| Area | Requirement |
|---|---|
| Authentication | Login system with role-based access control |
| Access control | Per-organisation data isolation |
| Secure data handling | Encrypted storage, secure input, no data leakage |
| Audit logging | Record of who generated what, when |
| Data retention | Policy for how long generated content is stored and when it is deleted |
| Privacy / DPIA | Full Data Protection Impact Assessment before processing personal or sensitive data |
| Safeguarding review | Review by a qualified safeguarding officer before deployment in an education/care setting |
| HR review | Review by HR professional before any content referencing staff behaviour is used |
| Legal / compliance review | Review of all training content claims, disclaimers, and responsible-use statements |
| Incident response | Breach notification and incident reporting procedures |
| Model governance (if LLMs added) | Evidence grounding, output review, human-in-the-loop controls |
| Monitoring | App health, error rates, usage tracking |
| Responsible owner | Named individual accountable for the tool's use in the organisation |

No production deployment should proceed without governance sign-off across all relevant domains.

---

*Build 4 · AI Staff Training and Workshop Generator · BrightPath ChatGPT Mastery Project*
*All scenarios are synthetic. Outputs require human review before use.*
