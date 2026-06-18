# Deployment Notes — BrightPath AI Readiness + Workflow Audit Tool

---

## Purpose

This document describes simple, safe ways to run or share the prototype — locally or via Streamlit Community Cloud. It is not a production deployment guide.

---

## Prototype Status

**This is a prototype, not a production system.**

It has no authentication, no persistent storage, no audit logging, and no access controls. It is safe for portfolio demonstration, learning, and early consulting conversation support. It is not safe for production use with real client data.

---

## Local Run

Run the app on your own machine. No internet connection or cloud account required.

```bash
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate it
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Opens at `http://localhost:8501` by default.

If port 8501 is already in use:

```bash
streamlit run app.py --server.port 8502
```

---

## Streamlit Community Cloud Option

Streamlit Community Cloud lets you share a running version of the app via a public URL at no cost. This is suitable for portfolio use with synthetic demo data only.

**Steps at a high level:**

1. Push the repository to a public or private GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub account
3. Select `app.py` as the entry point
4. Confirm `requirements.txt` is present at the project root
5. Deploy

No account-specific steps are included here — follow the Streamlit Community Cloud documentation for current setup instructions.

**Before deploying:**

- Use synthetic BrightPath demo data only
- Do not upload `.env` files, API keys, secrets, or credentials
- Do not deploy a version that prompts for or accepts real client data
- Add a clear prototype/demo notice to the Home page if sharing publicly

---

## What Not to Deploy Yet

Do not use this version in any context involving:

- Real learner data — no identifiable learner records, attendance data, or assessment outcomes
- Safeguarding case data — never. Any safeguarding information must remain entirely outside this tool
- Confidential client records — no commercially sensitive, contractual, or restricted client information
- Personal data — no names, contact details, or identifiable information about individuals
- Regulated data — no data subject to UK GDPR special category protections
- Production client use — this prototype has not been reviewed for production use
- Unsupported compliance claims — do not present this tool as compliant with any regulatory standard

---

## Environment Variables

The current version requires no API keys or external credentials.

- `.env.example` is included at the project root as a template for future extension
- Never commit a real `.env` file to version control — add it to `.gitignore`
- No secrets are required to run the MVP locally or on Streamlit Community Cloud

---

## Demo Safety Checklist

Before running a demo or sharing a deployed version:

- [ ] Use synthetic BrightPath-style data only — load via the Home page demo data button
- [ ] Clear browser session/cache beforehand if a previous real-data session was active
- [ ] Do not show local file paths, environment files, or terminal history containing credentials
- [ ] Do not show real client data, learner records, or safeguarding information at any point
- [ ] Explain the prototype limitations to any audience before the demo begins
- [ ] Explain that all outputs require human review before informing real decisions
- [ ] Confirm the responsible-use notice is visible on the Home page

---

## Future Production Considerations

If this tool is ever developed beyond a prototype, the following would be required before real client use:

- **Authentication** — user login and session management
- **Access control** — role-based permissions for consultants, reviewers, and admins
- **Secure storage** — encrypted storage for any session data or reports
- **Audit logging** — records of who ran assessments and when
- **Data retention policy** — clear rules for how long session data is kept and how it is deleted
- **DPIA / privacy review** — data protection impact assessment where personal or regulated data is involved
- **Role-based review process** — safeguarding lead and data protection officer sign-off before use with real data
- **Proper hosting and security review** — penetration testing, secure configuration, and HTTPS enforcement
- **Testing and monitoring** — automated tests, error monitoring, and usage analytics
- **Legal, safeguarding, and compliance review** — qualified review before any client-facing deployment

---

## Recommended Current Use

Use this version for **portfolio demonstration, learning, and early consulting conversation support only.**

Do not use it with real client data, in a regulated context, or as a substitute for professional advice.
