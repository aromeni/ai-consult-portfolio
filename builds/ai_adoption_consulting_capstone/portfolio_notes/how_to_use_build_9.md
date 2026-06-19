# How to Use the AI Adoption Consulting Capstone Dashboard
### A Complete Beginner's Guide — From Launching the App to Running a Client Session

*Written for Rashid. Assumes no prior knowledge of the application.*

---

## Before You Read Anything Else — Understand This One Thing

This application is not a piece of software you passively observe.

It is **your consulting methodology, made visible**.

Every page, every table, every score, every export exists to answer one question that every client organisation will eventually ask you:

> *"We've heard a lot about AI. Should we be using it, and if so — where do we start, and what would it actually cost us to get there?"*

This dashboard is how you answer that question — systematically, credibly, and with evidence.

When you sit in front of a prospect, a hiring panel, or a potential client, this tool is what separates you from someone who talks about AI consulting and someone who **demonstrates** it.

---

## Part 1 — What Is This Application?

### The Problem It Solves

Imagine you are an AI consultant. You have assessed a client's readiness, audited their workflows, checked their governance policy, and tracked their early AI pilots. You now have findings from eight different tools across eight different areas of their organisation.

But right now, those findings are scattered. They live in separate reports, separate conversations, separate tabs. You cannot show the client a single coherent picture. You cannot say: *"Here is where you are, here is where the gaps are, and here is exactly what I recommend you do next."*

That is the problem Build 9 solves.

It takes everything you have gathered — all eight areas of your consulting engagement — and assembles it into:

- One unified dashboard showing the client's AI adoption position
- A scored journey health assessment across all build areas
- A formal consulting recommendation with a commercial next step
- A professional report the client can take away
- Evidence in five downloadable formats

### What It Is Not

Be clear on this — especially when presenting to clients:

- It is **not** a magic AI tool that analyses your client's data automatically
- It is **not** connected to the internet or to any live data source
- It is **not** giving financial, legal, HR, or compliance advice
- It currently runs on **synthetic (fictional) demonstration data** — three fictional client organisations

The synthetic data exists so you can demonstrate the *methodology* in full, without needing a real client in the room. Once you are in a paid engagement, the methodology stays exactly the same — only the data changes.

---

## Part 2 — Getting the Application Running

### What You Need

- A computer with Python installed (version 3.11 or above)
- A terminal (on Mac, this is called Terminal; on Windows, use Command Prompt or PowerShell)
- The project folder — located at `10-builds/ai_adoption_consulting_capstone/`

### Step-by-Step: Launching the App

**Step 1 — Open your terminal.**

On a Mac: press `Cmd + Space`, type `Terminal`, press Enter.

**Step 2 — Navigate to the project folder.**

Type the following and press Enter:

```bash
cd /Users/abdulrashidomeni/chatGPT-Mastery/10-builds/ai_adoption_consulting_capstone
```

*Why this step matters:* The terminal needs to be inside the correct folder before it can find and run the application files. Think of it like making sure you are in the right room before you turn on the lights.

**Step 3 — Install the required libraries (first time only).**

```bash
pip install -r requirements.txt
```

*Why this step matters:* The application is built using a set of tools written by other developers — things like Streamlit (which creates the visual interface), ReportLab (which creates the PDF), and Matplotlib (which draws the charts). This command downloads and installs all of them in one go. You only need to do this once.

**Step 4 — Launch the application.**

```bash
streamlit run app.py
```

*Why this step matters:* This is the command that starts the dashboard. Streamlit is the framework that turns your Python code into a visual, clickable web interface. When you run this command, Streamlit starts a small local web server on your computer.

**What you will see in the terminal:**

```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

**Step 5 — Open your browser.**

Go to: **http://localhost:8501**

The application will open. You will see a dark navy sidebar on the left and the first page on the right.

*You are now inside the Capstone Dashboard.*

---

## Part 3 — Understanding the Layout Before You Click Anything

Take thirty seconds to look at the screen before you touch anything. Here is what you are looking at:

### The Sidebar (Left Panel)

The dark navy panel on the left is your **navigation menu**. It lists all eight pages of the dashboard:

```
1. Capstone Client Setup
2. Client Journey Overview
3. Cross-Build Insight Aggregator
4. Consulting Recommendation Pathway
5. Capstone Dashboard
6. Capstone Report Builder
7. Export Centre
8. Final Review
```

These eight pages represent the eight stages of your consulting engagement — in order. You move through them from top to bottom, just as you would move through a real consulting project.

**The logic:** A consultant does not jump straight to recommendations. They first establish context (who is the client, what are we measuring), then gather and aggregate evidence, then produce a recommendation, then package the deliverable. The page order reflects that exact discipline.

### The Main Area (Right Panel)

Everything to the right of the sidebar is the working area — tables, charts, metrics, reports, and download buttons. This is where the content lives.

### The Three Synthetic Clients

Everywhere in this application, you will see references to three organisations:

| Client | Sector | What They Represent |
|---|---|---|
| **BrightPath Digital Services** | Professional services / EdTech | A client who is progressing well — good evidence, clear direction |
| **Northside Housing Association** | Housing / public sector | A client with a mixed picture — some areas strong, others need work |
| **Greenacre Professional Services** | Professional services | A client with gaps — earlier in their journey, needs more groundwork |

*Why three different clients?* Because in a real consulting practice, not every client is at the same stage. You need to be able to show a prospect what "strong progress", "developing", and "needs review" look like — and what you would recommend in each case. These three clients give you that range.

---

## Part 4 — Page-by-Page Guide

Work through these pages in order. Do not skip ahead.

---

### Page 1 — Capstone Client Setup

**What it is:**

This is your starting point. It shows you the full picture of all three synthetic client organisations — who they are, what journey stages have been recorded for them, and how their portfolio indicators currently sit.

**What you will see:**

- A table listing all three client organisations with their sector and overall stage count
- A breakdown of the 21 journey stages across all builds
- Portfolio-level indicators (e.g., how many clients have completed governance review, how many have a pilot in progress)

**The logic behind it:**

Before a consultant can produce any analysis, they need to establish *what data exists*. This page answers: "Who are we looking at, and what have we collected so far?" It is the equivalent of opening a client file at the start of a meeting and checking it is complete before you begin your assessment.

In a real engagement, this is where you would load or confirm the client's recorded data — their readiness score, their governance gaps, their training completion. For now, the synthetic data does this automatically.

**What to do on this page:**

- Read through the client table and the journey stage breakdown
- Take note of which clients have the most complete journey records and which have gaps
- These gaps will matter when you reach the recommendation page

**What to say to a client if they are watching:**

> *"This first screen is where we establish the evidence baseline. Before I make any recommendation, I need to confirm what we have actually measured across your organisation. Every row in this table represents a specific area of your AI adoption journey that we have assessed — readiness, governance, training, implementation. Nothing here is an assumption. It is a record of what we found."*

---

### Page 2 — Client Journey Overview

**What it is:**

This is the health assessment. The application takes every journey stage recorded for every client and runs it through a scoring engine to produce a health classification: Strong, Healthy, Developing, Needs Review, or Blocked.

**What you will see:**

- A summary of each client's overall journey health score
- A completion rate (how many of the possible journey stages have evidence)
- An evidence quality score
- A prioritised review table — which client most urgently needs your attention

**The logic behind it:**

Think of this as your triage page. When you have multiple clients, you need to know: who is thriving, who is progressing, and who is at risk? The health engine scores each client deterministically — meaning it applies the same rules every time, without bias or guesswork.

The five health classifications work like this:

| Classification | What It Means |
|---|---|
| **Strong** | Evidence is complete, scores are high, no blockers — this client is ready to scale |
| **Healthy** | Good progress, minor gaps — this client needs light-touch support to maintain momentum |
| **Developing** | Mixed evidence — some areas are progressing, others are lagging. Focused intervention needed |
| **Needs Review** | Significant gaps or low scores — this client needs a structured reassessment before moving forward |
| **Blocked** | Critical gap or unresolved blocker — this client cannot progress until a specific issue is resolved |

**What to do on this page:**

- Note the health classification for each client
- Look at the prioritised review table — the client at the top needs your attention most urgently
- Make a mental note of the completion rate — a low completion rate means you need more evidence before you can make a solid recommendation

**What to say to a client if they are watching:**

> *"This is where I give you an honest picture of where you sit. These classifications are not opinions — they come directly from the evidence we collected. A 'Developing' classification does not mean you are failing. It means you have made a start and there are specific areas where we need to focus our next phase of work. The important thing is that we can now see exactly which areas those are."*

---

### Page 3 — Cross-Build Insight Aggregator

**What it is:**

This page zooms in on the evidence by **build area** rather than by client. It asks: across all eight consulting tools we applied, where is the evidence strongest and where are the gaps?

**What you will see:**

- Build-area evidence health scores — a rating for each of the eight build areas (Readiness, Document Intelligence, Training, Governance, ROI, Delivery, etc.)
- A client-build status matrix — a grid showing which client has evidence in which build area, and how strong that evidence is

**The logic behind it:**

This is the cross-cutting view. Imagine you have assessed three clients across eight areas. You now want to know: *"Is Governance consistently weak across all clients? Is Training consistently strong?"* If a particular area is weak across multiple clients, that tells you something important — either the methodology for that area needs more time, or there is a sector-wide pattern that you can speak to with authority.

The matrix is the most powerful tool on this page. Each cell represents one client's evidence in one build area. A full matrix means comprehensive evidence. A patchy matrix means there are areas you still need to work on before you can make a complete recommendation.

**What to do on this page:**

- Scan the matrix for patterns — are there entire rows (clients) or entire columns (build areas) that are weak?
- Use the build-area health scores to identify which consulting tools produced the strongest evidence
- If you were in a real engagement, this is where you would go back to the client and say: *"We have not completed your governance assessment yet — we need to do that before I can give you a final recommendation"*

**What to say to a client if they are watching:**

> *"This matrix gives us both a single view of the entire engagement. Every column is one of the eight areas we assessed. Every row is your organisation. A strong score in a cell means we have solid evidence and you are progressing well in that area. A gap means we have more work to do there before I can give you a confident recommendation. Transparency is the point — I am not going to recommend a full AI rollout if your governance column is empty."*

---

### Page 4 — Consulting Recommendation Pathway

**What it is:**

This is the output of the diagnostic phase. Based on the journey health, the evidence completeness, and the build-area scores, the application produces a formal capstone readiness classification and a commercial next step for each client.

**What you will see:**

- A **Capstone Readiness Classification** per client (Not Ready / Foundation Phase / Pilot Ready / Scale Ready / Optimisation Ready)
- A **Commercial Next Step** — the specific action you should recommend to the client
- The reasoning behind each recommendation

**The logic behind it:**

This is the page that answers the client's fundamental question: *"What should we do next?"*

The five readiness classifications work like this:

| Classification | What It Means | Recommended Next Step |
|---|---|---|
| **Not Ready** | Critical foundations are missing — governance, policy, or basic readiness have not been established | Foundation work first — governance review, policy drafting, awareness training |
| **Foundation Phase** | Early-stage evidence exists but is incomplete — some areas assessed, others not | Complete the diagnostic — return to unfinished build areas before moving forward |
| **Pilot Ready** | Solid foundation evidence with a clear use case identified | Run a structured AI pilot in one workflow — measure and report back in 90 days |
| **Scale Ready** | Pilot evidence exists and governance is in place | Plan a phased rollout across additional workflows or departments |
| **Optimisation Ready** | Mature adoption with strong evidence across all areas | Focus on continuous improvement, ROI measurement, and staff capability development |

*Why this matters so much:* Many AI consultants give the same recommendation to every client — "run a pilot." That is not consulting. That is a default. The recommendation pathway forces you to be specific, to match the recommendation to the actual evidence. A client who is "Not Ready" should not be running a pilot yet. A client who is "Scale Ready" does not need another readiness assessment.

**What to do on this page:**

- Read each client's classification and the reasoning attached to it
- Check whether the commercial next step aligns with what you would have recommended based on what you saw in Pages 2 and 3 — if it does, that is your evidence that the methodology is working
- Note the exact language used — this is the language you will use in the formal report and in your client conversation

**What to say to a client if they are watching:**

> *"This is the moment the evidence turns into a recommendation. I am not telling you what to do based on intuition or what I did for another client. I am telling you what the evidence says about your specific situation. Your classification today is [X]. That means [explanation]. The specific next step I am recommending is [Y], and here is why that is the right move at this stage rather than jumping straight to [Z]."*

---

### Page 5 — Capstone Dashboard

**What it is:**

This is the executive summary view — the page you would show at the beginning of a board presentation or senior leadership meeting. It brings together the most important information from all previous pages into one screen.

**What you will see:**

- A **Client Spotlight** — a focused summary of the selected client's position
- **Portfolio-level metrics** — totals and averages across all three clients
- **Three summary tables** — journey health, recommendation pathway, and evidence completeness side by side

**The logic behind it:**

Senior stakeholders and board-level decision-makers do not have time for detail when they first walk into a room. They need to see the headline picture immediately — then they can drill down. The Capstone Dashboard is designed for exactly that moment: the first thirty seconds of a senior-level conversation.

The Client Spotlight is particularly important. It allows you to switch focus from the portfolio view to one specific client — useful when you are in a meeting with that client and do not want to show them information about other organisations.

**What to do on this page:**

- Select each client in turn using the dropdown or selector and read the Client Spotlight
- Use the portfolio metrics to prepare your opening statement for a broader presentation
- This is the page you would have on screen when you first sit down with a client — before you start walking through the detail

**What to say to a client if they are watching:**

> *"Before we go into the detail, let me show you the headline picture. This is where your organisation sits today relative to your AI adoption journey. [Point to the health classification and readiness score.] What I want you to take away from this screen is [one or two key points]. In the next few minutes I am going to show you exactly how we got here and what it means for your next steps."*

---

### Page 6 — Capstone Report Builder

**What it is:**

This page generates a full, structured consulting report in plain text format (Markdown). You can generate it at portfolio level (covering all three clients) or at individual client level (focused on one organisation).

**What you will see:**

- A scope selector (Portfolio or individual client)
- A button to generate the report
- The rendered report appearing on screen — with sections for context, findings, recommendation, and next steps

**The logic behind it:**

Everything you have done across the first five pages needs to end in a document the client can take away. Verbal recommendations are forgotten. A written report is a record. It demonstrates rigour. It shows the client that what you delivered was structured and professional, not an informal conversation.

The report follows a standard consulting report structure:

1. **Executive Summary** — the headline finding in two or three sentences
2. **Context** — who the client is, what was assessed, and when
3. **Findings** — the evidence from each build area
4. **Health Assessment** — the journey health classification and what drove it
5. **Recommendation** — the readiness classification and the specific next step
6. **Limitations** — what the assessment did not cover and what caveats apply
7. **Next Steps** — the concrete actions recommended for the next 30, 60, or 90 days

*Why the limitations section matters:* A professional consultant always states what their assessment cannot tell you. It builds trust. It shows the client you are not over-claiming. It also protects you — if a client acts on your recommendation and something goes wrong in an area you explicitly said was outside the scope of your assessment, you have a clear record.

**What to do on this page:**

- First, generate the portfolio-level report and read through it — get familiar with the structure
- Then switch to individual client view and generate a report for each of the three clients — notice how the report changes in tone and emphasis based on the client's specific situation
- Read the limitations section carefully — this is the language you will use when a client asks "what can't this tell me?"

**What to say to a client if they are watching:**

> *"What I am generating now is your formal report. This is not a template I have filled in — it is built directly from the evidence we collected during our engagement. Every finding in this report is referenced back to something we actually measured. I will send this to you in PDF format after today's session, but I want to walk you through the key sections now so nothing in the document surprises you."*

---

### Page 7 — Export Centre

**What it is:**

This page gives you one-click downloads for five different formats of the consulting output. Each format is designed for a different use case.

**What you will see:**

Five download buttons, each producing a different file:

| Format | What It Contains | When to Use It |
|---|---|---|
| **Markdown (.md)** | The full consulting report as plain text | Paste directly into a proposal, email, or client portal |
| **CSV (.csv)** | A flat data table — one row per client per build area | Share with a client's data or operations team for their own records |
| **JSON (.json)** | All capstone data in structured format | Technical handover — for a client's IT team or for future integration |
| **PDF (.pdf)** | Formatted consulting report, ready to print or email | The professional leave-behind — the document you hand to the client at the end of the meeting |
| **PNG (.png)** | A capstone readiness bar chart | Drop into a slide deck, a LinkedIn post, or a proposal document |

**The logic behind it:**

Different stakeholders need different things. The CEO wants a PDF they can read on a plane. The operations director wants a CSV they can load into their own systems. The IT lead wants a JSON file they can pipe into their infrastructure. The consultant wants a chart they can drop into a slide deck for the board presentation.

By offering all five formats from one screen, you are demonstrating that your consulting practice is structured enough to package deliverables for any audience — not just the person who commissioned the work.

**What to do on this page:**

- Download all five formats and open each one so you understand exactly what each contains
- The PDF is the one you will use most often — open it and read it as a client would. Does it look professional? Does the structure make sense? Is the recommendation clear?
- The PNG chart is the one you will use in presentations — check that the labels are readable and the chart tells a clear story at a glance

**What to say to a client if they are watching:**

> *"At the end of every engagement, I provide the full evidence pack in the format that works best for your team. The PDF is for you and your leadership team — it is the formal record of our engagement. The CSV is for your operations or data team if they want to build on this work internally. The JSON is for your IT team if they want to integrate this evidence into your own systems. Everything is exportable and everything is yours."*

---

### Page 8 — Final Review and Commercial Positioning

**What it is:**

This is the closing page of the dashboard. It shows a completion summary across all eight phases, states the limitations of the assessment clearly, and positions the commercial opportunity — what a continued or expanded engagement would look like.

**What you will see:**

- A phase completion table — all eight phases marked as complete
- A limitations statement — what this assessment does and does not cover
- A responsible use notice — the ethical guardrails on how this output should be used
- A commercial positioning section — what the natural next conversation with the client looks like

**The logic behind it:**

Closing a consulting engagement well is as important as opening it. The final review does three things:

1. **It demonstrates completeness.** You have not left anything unfinished. Every phase has been addressed.
2. **It manages expectations honestly.** The limitations section makes clear what you assessed and what falls outside the scope. This builds trust — a consultant who tells you what they *cannot* tell you is more credible than one who pretends to have all the answers.
3. **It opens the commercial conversation.** The methodology you have just demonstrated is the foundation of a real engagement. The final page positions what that looks like — and invites the client to take the next step.

**What to do on this page:**

- Read the limitations section out loud to yourself — practise saying it naturally. When a client asks "what does this not cover?", you need a clear, confident answer.
- Read the commercial positioning section and think about how it applies to the specific client in front of you. Which of the next steps is most relevant to where they are?
- This is the page you leave on screen as the meeting closes — it is a professional, measured ending to the session.

**What to say to a client if they are watching:**

> *"Before we close, I want to be clear about what today's assessment covers and what it does not. [Read or paraphrase the limitations.] The recommendation I have given you is based on the evidence we have gathered. Where we have gaps, I have said so. What I would like to propose as a next step is [specific action from the commercial positioning section]. I can have a proposal in front of you within [timeframe]. Does that work?"*

---

## Part 5 — Using the Exports in a Real Client Context

### The PDF Report — Your Most Important Export

The PDF is the primary deliverable of every consulting session using this tool. Here is how to use it:

1. **Before the meeting:** Generate it so you know exactly what it contains.
2. **During the meeting:** Use it to guide the conversation — you do not need to share your screen if you have already sent the PDF.
3. **After the meeting:** Email it within 24 hours as the formal record of the session.
4. **In a proposal:** Include key sections as quoted evidence in your commercial proposal.

### The PNG Chart — Your LinkedIn and Presentation Asset

The readiness bar chart is designed to be dropped into slides and social content. Use it to:

- Open a board presentation with the headline picture before the detail
- Include in a LinkedIn post showing your consulting methodology in action (remember: synthetic data — do not present it as a real client case study)
- Drop into a proposal document to make the recommendation visually immediate

### The CSV and JSON — For the Client's Technical Team

These formats are not for the senior stakeholder — they are for the people who will actually implement what you recommend. Hand these over to the client's operations lead or IT manager with a brief note explaining what each column or field represents.

---

## Part 6 — Running a Complete Client Session

Here is how to structure a full 60-minute client session using this dashboard.

### Before the Meeting (15 minutes)

- Launch the application (`streamlit run app.py`)
- Read through all eight pages once — know what you are going to show before you show it
- Generate and read the PDF report for the relevant client
- Open the Export Centre and pre-download the files you will need
- Decide which pages you will show and which you will reference verbally — you do not need to click through every screen in every meeting

### Opening (5 minutes)

- Open on the **Capstone Dashboard** (Page 5) — not Page 1
- The dashboard gives the client an immediate visual picture of where they stand
- Use this as your opening: *"Before we go through the detail, here is the headline view of where you are today"*

### The Diagnostic Walkthrough (20 minutes)

- Move to **Page 1 — Capstone Client Setup** and walk through the evidence baseline
- Move to **Page 2 — Client Journey Overview** and present the health classification — invite questions here
- Move to **Page 3 — Cross-Build Insight Aggregator** and show the matrix — this is usually where the most important conversation happens, because clients can see exactly where their gaps are
- Move to **Page 4 — Consulting Recommendation Pathway** and present the recommendation — this is your professional opinion backed by the evidence you have just shown

### The Deliverable (10 minutes)

- Move to **Page 6 — Capstone Report Builder** and generate the report on screen
- Walk through the key sections — Executive Summary, Findings, Recommendation, Next Steps
- Tell the client you will send the PDF version after the meeting

### The Export (5 minutes)

- Move to **Page 7 — Export Centre** and demonstrate the five formats
- Ask the client which formats their team needs — this shows you understand that different people in their organisation have different requirements
- Download the formats they need now; send the rest via email

### Closing (10 minutes)

- Move to **Page 8 — Final Review**
- State the limitations clearly — do not skip this
- Make your commercial proposal — the specific next step you are recommending
- Agree on a follow-up date before you leave the room

---

## Part 7 — The Most Common Mistakes (And How to Avoid Them)

**Mistake 1: Jumping straight to the recommendation.**

The recommendation only means something if the client has seen the evidence that supports it. Always walk through Pages 2 and 3 before you present Page 4. The recommendation is the conclusion — it needs the argument to come first.

**Mistake 2: Skipping the limitations section.**

Every credible consultant states what their work does not cover. If you skip the limitations and something goes wrong later in an area you did not assess, you have no record that you flagged it. The limitations section protects both you and the client.

**Mistake 3: Presenting the synthetic data as if it is real.**

This dashboard runs on fictional data. When you are demonstrating the methodology to a prospect, say so clearly: *"The clients you are seeing here are fictional — they are here so I can show you the methodology in full. When we work together, the data will be yours."* Never imply the three synthetic clients are real case studies.

**Mistake 4: Using the PNG chart without explaining what it shows.**

The chart shows capstone readiness scores. Before you put it in a slide or send it to a client, add a brief explanation of what the scores mean and how they were derived. A chart without context creates confusion, not clarity.

**Mistake 5: Ending the session without a clear next step.**

The closing page is called Final Review for a reason. Every session should end with one specific, agreed next action — not "I'll be in touch." The commercial positioning section gives you the language for that conversation.

---

## Quick Reference Card

| Page | Purpose | Key Question It Answers |
|---|---|---|
| 1 — Capstone Client Setup | Establish the evidence baseline | Who are we looking at and what have we measured? |
| 2 — Client Journey Overview | Health classification | How is each client progressing overall? |
| 3 — Cross-Build Insight Aggregator | Evidence by build area | Where are the strengths and gaps across all eight areas? |
| 4 — Consulting Recommendation Pathway | Formal recommendation | What should each client do next, and why? |
| 5 — Capstone Dashboard | Executive summary | What is the headline picture for leadership? |
| 6 — Capstone Report Builder | Generate the written deliverable | What does the formal consulting report say? |
| 7 — Export Centre | Package the outputs | In what format does each stakeholder need the evidence? |
| 8 — Final Review | Close the session | What are the limitations and what is the commercial next step? |

---

## The One Thing to Remember

This tool demonstrates a structured, repeatable methodology. The value you bring to a client is not the software — it is the thinking the software makes visible. You are the consultant. The dashboard is the evidence of your process.

Every time you open this application, you are showing a client or prospect that your approach to AI adoption consulting is:

- **Systematic** — you cover all eight areas, not just the ones that are easy
- **Evidence-based** — every recommendation is traceable back to what you actually measured
- **Honest** — you state the limitations, you do not over-claim
- **Actionable** — you close every session with a specific next step, not a vague direction

That combination is what distinguishes a credible AI consultant from someone who simply talks about AI.

---

*Rashid AI Consult · AI Adoption Consulting Capstone Dashboard · Build 9*
*Synthetic data only. Not professional consulting, legal, financial, or HR advice.*
