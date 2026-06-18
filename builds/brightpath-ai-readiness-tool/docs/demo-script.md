# Demo Script — BrightPath AI Readiness + Workflow Audit Tool

## Demo Purpose

Show a prospective client, hiring manager, or collaborator how the tool works — from opening the app to downloading a recommendation report — in under 15 minutes.

---

## Audience

- Managers of small training providers considering AI adoption
- Hiring managers evaluating AI consulting capability
- Potential collaborators or project partners
- Portfolio reviewers (LinkedIn, GitHub)

---

## Demo Setup

Before the demo:

1. Open a terminal and run `streamlit run app.py` from the project directory
2. Open `http://localhost:8501` in a browser
3. Ensure the Home page is visible with no previous data loaded
4. Have this script open in a second window or on paper

The demo uses only the BrightPath synthetic data. No real client data is needed.

---

## Demo Scenario

**Organisation:** BrightPath Skills Training

- Small UK training provider, 8 staff
- Staff are using personal ChatGPT accounts informally for lesson planning, email drafting, and report writing
- No AI policy exists, no approved tools list, no data controls
- The manager wants to know: is this safe, and where should we start?

**Consultant role:** Rashid is running an AI readiness diagnostic with the manager and two tutors.

---

## Demo Flow

---

### Step 1 — Home Page

**What to show:**
- The title, welcome text, and tool description
- The three metrics (7 pages, 10 readiness dimensions, 8 sample workflows)
- The "Load BrightPath demo data" button

**What to say:**
> "This is the BrightPath AI Readiness and Workflow Audit Tool. It's designed to run in a 60 to 90 minute session with a client. We start with some context about the organisation, then work through readiness, workflow, risk, and recommendation. At the end we download a report."

> "I've pre-loaded a fictional training provider called BrightPath to show you how it works. Let me click Load BrightPath demo data."

**Action:** Click **Load BrightPath demo data**.

**Key message:** The tool is pre-loaded with a realistic scenario. No real data needed.

**Expected output:** Success message confirming demo data is loaded.

---

### Step 2 — Organisation Profile

**What to show:**
- The profile panel showing BrightPath's details
- The note about staff using personal ChatGPT accounts
- The flags: no AI policy, no approved tools

**What to say:**
> "This is the organisation profile. We can see BrightPath has 11 to 50 staff, uses ChatGPT and Grammarly on personal accounts, and has no AI policy or approved tools list — but they do have a data protection lead. That's a useful baseline."

> "The profile shapes the rest of the assessment. You can see immediately that governance is the biggest gap."

**Key message:** The profile surfaces governance gaps at a glance.

---

### Step 3 — AI Readiness Assessment

**What to show:**
- The ten readiness sliders
- The live score updating as sliders move
- The category, explanation, and suggested next action

**What to say:**
> "This is the readiness assessment — ten dimensions scored 0 to 10. Each one corresponds to a real question I'd ask in the room: how well do staff understand what AI can and can't do? How mature is the governance? How clear are the business goals?"

> "The sliders are already pre-populated with BrightPath's profile. Their total is 35 out of 100, which puts them in the Early Awareness band. That's honest — they're interested but not ready to pilot yet."

**Point to:** The bar chart showing governance_maturity (1) and risk_awareness (2) as the lowest dimensions.

**What to say:**
> "You can see governance and risk awareness are almost zero. That's not a criticism — it's the starting point. It tells us exactly what needs to happen before we go near a live workflow."

**Key message:** 35/100 is a realistic baseline for a small provider at this stage. The gaps are specific and actionable.

**Expected output:** Score 35 / 100 — "Early awareness."

---

### Step 4 — Workflow Audit

**What to show:**
- The workflow information form
- Click "Load BrightPath sample workflow (Generic lesson planning support)"
- The ten suitability sliders
- The score, category, bar chart

**What to say:**
> "Now we look at a specific workflow. I've picked generic lesson planning support — tutors spend 45 minutes a week on this, it's repetitive, topic-based, and doesn't require any learner data. That makes it structurally a good candidate."

> "Let me load the sample data. You can see the suitability score is 42 out of 50, which puts it in the Good Pilot Candidate band. The data sensitivity and human review scores are both 5 out of 5 — because no learner data is needed and a tutor can check the output easily."

**Key message:** The workflow audit separates the structural question (is this workflow suitable for AI?) from the governance question (is the organisation ready?). They can give different answers.

**Expected output:** Score 42 / 50 — "Good pilot candidate."

---

### Step 5 — Risk Assessment

**What to show:**
- The ten risk categories with likelihood and impact sliders
- Click "Load BrightPath sample risk profile"
- Point to safeguarding (likelihood 2, impact 5, score 10 = High)
- The overall summary and recommendation

**What to say:**
> "The risk assessment uses a likelihood-times-impact matrix. Most categories are Low for lesson planning — no learner data, no credentials, no confidential content. But look at safeguarding."

> "Likelihood is 2 — it's unlikely a tutor would add case context to a lesson plan prompt. But the impact is 5 — if they did, it would be critical. That gives us a High risk score. And that changes everything."

**Point to:** The red warning box for safeguarding.

**What to say:**
> "The safeguarding safeguard here is simple: do not enter safeguarding case information into AI tools. But we have to name it explicitly, train on it, and confirm it before any pilot begins."

**Key message:** Even a low-risk workflow can carry a high-risk category if the consequences of misuse are severe.

**Expected output:** Highest risk level — High. Overall recommendation — "Pilot only with safeguards, staff guidance, and human review."

---

### Step 6 — Pilot Recommendation

**What to show:**
- The auto-computed recommendation
- The summary table (readiness, workflow, risk inputs)
- The next actions and safeguards

**What to say:**
> "The pilot recommendation pulls together everything: readiness score 35, workflow score 42, highest risk High. The recommendation comes back as 'Governance-first before pilot'."

> "This is the right answer for BrightPath right now. The workflow is ready. The organisation is not. The high safeguarding risk means we need to get governance controls in place before anyone uses AI on this workflow — even for lesson planning."

> "Here's what that looks like in practice." *[Read through the next actions list.]*

**Key message:** A good workflow score is not enough. Governance readiness and risk profile both gate the recommendation.

**Expected output:** "Governance-first before pilot." Next actions: confirm approved tools, define human review, escalate safeguarding training, select low-risk workflows.

---

### Step 7 — Mini Report Download

**What to show:**
- Navigate to Mini Report
- Click "Load BrightPath sample report data"
- Open the preview expander to show the 9-section report
- Click the Download button

**What to say:**
> "This is the final output — a structured Markdown report covering everything we've covered in the session. Organisation profile, readiness summary, workflow audit, risk assessment, recommendation, safeguards, next actions, responsible use statement, and consultant notes."

> "I download this and share it with the manager. They have a written record, a clear recommendation, and specific next steps. This is the deliverable."

**Show the filename:** `brightpath-skills-training-ai-readiness-mini-report.md`

**What to say:**
> "The filename is generated from the organisation name automatically. No manual renaming needed."

**Key message:** The report is structured, professional, and specific. It's not a generic summary — it reflects the actual session and gives the client something to act on.

**Expected output:** Downloaded `.md` file with all nine sections populated.

---

## Responsible Use Message

Include this in any live demonstration:

> "This tool uses only synthetic, anonymised data. No real learner records, safeguarding information, client data, or staff personal information is used at any point. The tool is a prototype — its outputs are indicative and designed to support a structured conversation, not replace professional judgement or compliance review. Organisations should always work with qualified advisors for governance, legal, and data protection decisions."

---

## Closing Pitch

> "What you've just seen is a working AI consulting diagnostic tool — built in Python using Streamlit, modular scoring logic, and a Markdown report generator. No external APIs, no database, no authentication required."

> "It combines structured readiness assessment, workflow diagnosis, risk scoring, governance-aware recommendation, and a client-ready written output — in a single 60 to 90 minute session."

> "This is how I think about AI consulting. Not just training people to use ChatGPT, but helping organisations understand where they are, what the risks are, which workflows are actually ready, and what they need to do before they start."

> "This is the prototype. The next version adds richer workflows, PDF export, and a governance checklist generator. But this version already works — and it produces something a client can take away and act on."
