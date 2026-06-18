# Demo Script

**AI Staff Training and Workshop Generator · Build 4**

---

## Purpose

This script walks through the complete Build 4 prototype with a client, collaborator, or reviewer. It covers all nine pages: Home, Organisation Scenario, Training Needs Assessment, Workshop Planner, Activity Generator, Facilitator Guide, Staff Handout, Knowledge Check, and Training Pack Export.

**Demo time:** 10–15 minutes for a full walkthrough; 5 minutes for a focused highlights demo.

**Demo scenario:** BrightPath Skills Training — a fictional small UK training provider with 8 staff using ChatGPT informally for lesson planning, emails, and reports.

**Training theme:** Using AI Safely for Lesson Planning and Admin

## Audience

- Prospective clients who have completed (or are considering) an AI readiness audit
- L&D practitioners exploring AI training material generation
- Governance leads wanting to understand responsible AI training design
- Technical reviewers evaluating the portfolio project

---

## Setup

```bash
cd 10-builds/ai-staff-training-workshop-generator
streamlit run app.py
```

Opens at `http://localhost:8501`.

---

## Step 1 — Open the Home Page

Point out:

- The **consulting workflow diagram**: eight steps from Organisation Scenario to Training Pack Export
- How Build 4 **connects to Builds 1, 2, and 3**:
  - Build 1 diagnosed AI readiness → identified training needs
  - Build 2 extracted policy document evidence → grounded training content
  - Build 3 performed semantic RAG over policy documents → policy-grounded answers
  - Build 4 turns those inputs into structured training materials
- The **responsible-use warning** and **prototype status notice**

Key talking point:

> "This closes the consulting loop. After the audit and document intelligence work,
> the organisation needs a way to actually train their staff. This prototype shows
> what that training generation pipeline looks like."

---

## Step 2 — Load the BrightPath Demo Scenario

Navigate to **Organisation Scenario**.

Click **Load BrightPath Demo Scenario**.

Point out:

- **Organisation:** BrightPath Skills Training — a fictional small UK training provider
- **Staff count:** 8 — the target audience for the workshop
- **Current AI use:** informal ChatGPT use for lesson planning, emails, and reports
- **Main concerns:** 9 concerns including learner data, safeguarding, hallucination, bias
- **Priority topics:** 8 specific training topics selected for the workshop

Key talking point:

> "The scenario captures everything a trainer needs to know before designing the
> workshop. In a real engagement, this would come from the Build 1 audit findings
> and an initial conversation with the organisation's lead."

---

## Step 3 — Review the Scenario Summary

Point out the **metric cards**:

- Staff count: 8
- Priority topics: 8
- Staff roles: 4
- Concerns: 9

And the **Markdown preview** (expand it):

> "This scenario can be exported as part of the full training pack in Phase 8.
> It becomes the context section at the top of the facilitator guide."

---

## Step 4 — Training Needs Assessment (Phase 2)

Navigate to **Training Needs Assessment**.

Click **Generate Training Needs Assessment**.

Point out:

- **Summary metrics:** priority topics, high-priority count, staff roles, learning outcomes
- **Topic priorities table:** each topic with its priority level (HIGH / MEDIUM / LOW), risk level, and training need
- **Recommended learning outcomes:** 5–8 specific, role-relevant outcomes
- **Role-specific needs:** expand each role (Tutors, Administrators, Team Leaders, Quality Lead) to see key risks and practical guidance
- **Risk summary:** how the scenario's concern profile translates into a training emphasis
- **Responsible-use note:** visible on every generated assessment

Key talking point:

> "This is what separates a generic AI awareness session from a tailored one.
> The assessment is driven by the organisation's specific concerns — learner data,
> safeguarding, hallucination — not a one-size-fits-all topic list."

Download the Markdown output and show the structure:

> "The consultant can share this with the client before the workshop.
> It confirms what topics will be covered and why — no surprises on the day."

---

## Step 5 — Workshop Planner (Phase 3)

Navigate to **Workshop Planner**.

Select **90 minutes** and **In-person workshop**. Click **Generate Workshop Plan**.

Point out:

- **Summary metrics:** duration, agenda sections, learning outcomes, follow-up actions
- **Workshop title:** automatically derived from the sector and training goal
- **Timed agenda table:** 7 sections spanning 90 minutes — show that times are proportional, not arbitrary
- **Agenda detail:** expand one section (e.g. Safe Prompting) to show trainer activity, participant activity, key message, and materials
- **Resources needed:** tailored to in-person delivery
- **Trainer notes:** scenario-aware — references the specific concerns BrightPath staff flagged
- **Discussion prompts:** 8 facilitated questions for the session
- **Responsible-use messages:** the 6 core rules the trainer must cover explicitly

Key talking point:

> "The trainer doesn't need to design the session from scratch. They get a complete plan:
> timing, activities, what to say, what to ask, what materials to prepare.
> They still need to review it and make it their own — but the heavy lifting is done."

Download the Markdown workshop plan and show the structure:

> "This goes to the trainer the week before the session.
> The training pack export in Phase 8 will bundle this with the handout, quiz, and facilitator guide."

---

## Step 6 — Activity Generator (Phase 4)

Navigate to **Activity Generator**.

The default BrightPath activity types are already selected:
- Safe vs Unsafe Prompt Sorting
- Rewrite a Risky Prompt Safely
- Spot the Hallucination
- Learner Data Boundary Scenario
- Safeguarding Escalation Scenario
- Human Review Checklist

Click **Generate Activities**.

Point out:

- **Summary metrics:** total activities, estimated time, activity types, target roles
- **Safe vs Unsafe Prompt Sorting:** expand and walk through cards A–F — show that Card E (safeguarding decision) and Card F (HR data) are PROHIBITED, not just risky
- **Rewrite a Risky Prompt Safely:** show card R1 — the original prompt contains a learner name and ID; show the safe rewrite
- **Spot the Hallucination:** show card H1 — point out the invented 40% statistic and the unverified Education Act reference
- **Safeguarding Escalation:** show card S1 — tutor wants to use ChatGPT for a safeguarding concern; show the correct escalation path to the DSL
- **Human Review Checklist:** walk through the 8 review checks; show scenario C1

Key talking point:

> "These aren't abstract policies — they're things staff can practise in the room.
> The sorting activity, the rewrite activity, the hallucination review — these all
> give staff direct, hands-on experience with the boundaries before they're
> working with real learner data."

Download the Markdown activity pack and show the structure:

> "This goes to the trainer alongside the workshop plan.
> Phase 8 will bundle activities, the facilitator guide, staff handout, and quiz
> into a single downloadable training pack."

---

## Step 7 — Facilitator Guide (Phase 5)

Navigate to **Facilitator Guide**.

Click **Generate Facilitator Guide**.

Point out:

- **Summary metrics:** duration, sections, activities covered, misconceptions
- **Session purpose:** derived from the scenario — specific to BrightPath's training goal
- **Facilitator principles:** 8 non-negotiable rules for responsible facilitation — synthetic examples, human-led decisions, safe escalation
- **Preparation checklist:** 11-item checklist covering approved tools, DPO contact, safeguarding lead, parking-lot process
- **Opening script (expand):** includes the synthetic-only ground rules verbatim — a trainer can read this aloud
- **Section delivery notes:** expand "Data and Safeguarding Boundaries" — show the what-to-say, what-to-ask, expected responses, and watch-out-for
- **Activity facilitation notes:** expand one activity (e.g. Safe vs Unsafe Prompt Sorting) — show how facilitator notes mirror the activity cards
- **Common misconceptions:** expand "AI can decide safeguarding actions" — show the facilitator response with a reference back to the activity cards
- **Debrief guidance:** step-by-step close including parking lot, three commitments, escalation contacts
- **Closing script (expand):** three-point summary recap — trainer-ready

Key talking point:

> "The facilitator guide turns the workshop plan into something a trainer can
> actually run on the day. The opening script sets the synthetic-only ground
> rules before any AI discussion starts. The misconception cards are the most
> useful thing for new facilitators — they tell you exactly what to say when
> someone pushes back."

Download the Markdown facilitator guide and show the structure:

> "This is what goes to the trainer alongside the workshop plan and activity pack.
> Phase 8 bundles everything into one downloadable training pack."

---

## Step 8 — Staff Handout (Phase 6)

Navigate to **Staff Handout**.

Click **Generate Staff Handout**.

Point out:

- **Summary metrics:** organisation, audience roles, safe prompt examples, unsafe prompt examples, escalation items
- **Handout title and purpose:** derived from the scenario — references BrightPath and labels all examples as synthetic
- **Safe-Use Principles:** 8 core rules — expand and highlight "Keep learner data, safeguarding information, HR data, confidential records, personal data, and regulated information out of AI tools"
- **What Staff Can Use AI For:** practical examples — generic lesson planning, rewriting correspondence, generating checklists
- **What Staff Must Not Use AI For:** prohibited uses including learner data, safeguarding decisions, HR records, assessment decisions
- **Safe Prompt Examples (expand one):** show the explicit instruction embedded in the prompt: "Do not include learner names, personal details, or case-specific information"
- **Unsafe Prompt Examples (expand one):** show the learner personal data or safeguarding decision risk
- **Safer Rewritten Prompt Examples (expand one):** show the unsafe → safer rewrite with what_changed list
- **Human Review Checklist:** checkbox-format list — suitable for a printed handout
- **Escalation Guidance (expand Safeguarding):** show "Do not enter any details into an AI tool. Follow safeguarding procedure. Contact DSL."
- **Key Takeaways:** 7 summary reminders — highlight "AI is a drafting and support tool — not a decision-maker"

Key talking point:

> "This is what gets handed to every staff member before the session — or immediately after.
> It's a reference card, not a policy document. It tells them exactly what they can do,
> what they must not do, and who to call if something goes wrong. The prompt examples
> are the most valuable part: staff can see the difference between a safe and an unsafe
> prompt side by side."

Download the Markdown staff handout and show the structure:

> "This goes to every attendee alongside the workshop materials.
> Phase 8 will bundle the handout, facilitator guide, activity pack, and knowledge check
> into a single downloadable training pack."

---

## Step 9 — Knowledge Check (Phase 7)

Navigate to **Knowledge Check**.

Select **10 questions**. Leave all sections checked (MCQs, scenarios, reflections, answer key).

Click **Generate Knowledge Check**.

Point out:

- **Summary metrics:** organisation, MCQ count, scenario question count, reflection question count, answer key included
- **MCQ 001 (expand):** "Which prompt is safest?" — walk through options A–D, point out why B is correct (generic topic, no personal data) and why A, C, D are prohibited
- **MCQ 003 (expand):** Learner data — "Which of the following must NOT be entered into an AI tool?" — confirm B (learner names and attendance) is the answer
- **MCQ 006 (expand):** Hallucination — "85% statistic" question — confirm C is correct (verify independently)
- **Scenario 001 (expand):** Safeguarding — tutor wants to paste a safeguarding concern into ChatGPT — walk through expected answer points
- **Scenario 002 (expand):** Learner data — administrator using personal AI account with learner names — walk through risk flags
- **Reflection 002:** "What is one type of information you must never enter into an AI tool?" — note guidance points, not a single model answer
- **Answer Key (expand):** confirm it includes correct answers and explanations for all MCQs, model answers for scenarios, and guidance for reflections
- **Pass and review guidance:** point out the threshold (8/10) and the qualitative review guidance for scenarios and reflections

Key talking point:

> "The knowledge check closes the learning loop. After the activities and the handout,
> staff can use this to check what they've actually understood. The trainer copy
> has a full answer key — the staff copy is just questions. Both download from the same page."

Download the Markdown knowledge check and show the structure:

> "Phase 8 will bundle this with the facilitator guide, handout, activity pack, and workshop plan
> into a single downloadable training pack."

---

## Step 10 — Training Pack Export (Phase 8)

Navigate to **Training Pack Export**.

Point out the **Training Pack Readiness** overview:

- Available sections: ✓ Organisation Scenario, Training Needs Assessment, Workshop Plan, Training Activities, Facilitator Guide, Staff Handout, Knowledge Check
- Missing sections: none (if all previous pages have been run)

Point out the **Section Selector**:

- 12 checkboxes in 3 columns, all pre-ticked
- Uncheck "Answer Key" to demonstrate a staff-copy export (questions without answers)
- Re-tick it to generate the full trainer copy

Click **Generate Training Pack**.

Point out:

- **Summary metrics:** organisation, sections available (7/7), activity count, MCQ count, answer key included
- **Facilitator Review Checklist:** 10 pre-delivery checks with ☐ formatting — highlight "Confirm safeguarding escalation route" and "Confirm this pack is treated as training support, not legal advice"
- **Recommended Next Steps:** 9 action items — highlight "Run a pilot workshop with a small group before full delivery"
- **Markdown Preview (expand):** first 4,000 characters of the pack — show the cover page, table of contents, organisation scenario summary, and section headers
- Scroll the preview to show section headings 1–12

Key talking point:

> "This is the complete deliverable. Everything generated across the eight pages —
> the scenario, the needs assessment, the workshop plan, activities, facilitator guide,
> handout, knowledge check, and answer key — combined into one Markdown file.
> The facilitator gets the full trainer copy. Staff get a copy without the answer key.
> Both download from this page with one click."

Point out the **Training Pack Analytics**: pack completeness, section completion chart, priority topic coverage, activity mix, workshop time allocation, and knowledge check topic charts.

Then show the **Export Options** panel — Markdown, PDF, and PowerPoint side by side:

- Click **Download Markdown Training Pack**
- Click **Download PDF Training Pack** (generated automatically when the pack is assembled)
- Click **Download PowerPoint Training Deck** (also auto-generated — appears immediately without a separate button click)

Open the PDF and point out: cover page, executive summary, analytics charts, all generated sections, facilitator review checklist, responsible-use boundaries, prototype limitations, and the per-page footer "Synthetic scenario prototype. Human review required."

Open the PowerPoint and point out: 15 slides covering organisation context, training needs, workshop agenda, activities, safe-use rules, human review checklist, escalation guidance, knowledge check, pack completion, responsible-use boundaries (slide 14 has a red accent bar), and recommended next steps. Speaker notes are included on key slides. Every slide footer carries the prototype notice.

> "The PowerPoint is a reviewer-ready training deck — something a consultant can hand to a client or trainer before the session. Like every other output, every slide is marked as a prototype requiring human review."

> "The PDF is a draft consulting/training deliverable. It looks client-ready,
> but it is explicitly marked as a prototype output that requires human review —
> the boundary is part of the document itself."

Click **Download Training Pack (Markdown)**.

Open the downloaded file and point out:

- The cover page with prototype status and synthetic-data notice
- Section 1: Organisation Scenario Summary
- Section 6: Staff Handout (embedded from the handout page's output)
- Section 10: Responsible-Use Boundaries (the non-negotiable responsible-use statement)
- Section 11: Prototype Limitations (prevents misuse as a formal compliance system)
- Section 12: Recommended Next Steps

> "This closes the Build 4 loop. The consultant can share this pack with the trainer
> the week before the session. Everything they need is in one file."

Key talking point:

> "Each page in the final build will generate a specific section of the training
> pack. The goal is that a trainer can go from scenario to a complete, downloadable
> workshop in under 5 minutes — without writing it from scratch."

---

## Showing the Polished UI and PDF Exports

Throughout the demo:

- Point out the **polished dashboard presentation** — page headers, metric cards, status badges, and the numbered sidebar workflow tracker filling in with ✓ as each step completes
- On **every report page** (Steps 4–9), show the **Download This Report** panel: each report downloads as both **Markdown** (editable) and **PDF** (formatted, client-presentable)
- Open one report PDF (e.g. the Staff Handout) and show: cover page with organisation name and prototype status, styled sections, and the responsible-use boundaries at the end

> "Every deliverable in this workflow exports as a professional PDF — but every
> page of every PDF carries the same footer: synthetic scenario prototype,
> human review required."

---

## Responsible-Use Points to Cover

- All scenarios are synthetic — no real learner, safeguarding, HR, or personal data
- No external AI API calls — all generation is deterministic and local
- All outputs require human review before use in a real training session
- This is a production-style prototype, not a training compliance system
- Production use would require DPIA, governance, security, legal, safeguarding, and HR review

---

## Closing Pitch

> "Build 4 shows the end-to-end consulting workflow from an AI adoption concern to a practical, downloadable training pack. The scenario captures the organisation's specific risks. The needs assessment prioritises what to train on. The workshop plan structures the session. The activities give staff hands-on practice. The facilitator guide tells the trainer what to say. The handout stays with staff after the session. The knowledge check closes the learning loop. And the training pack bundles everything into one deliverable.
>
> What's important is that none of this required a live AI model call. Everything is deterministic, local, and human-reviewable. That means it's auditable, consistent, and safe to use in contexts where responsible AI governance matters — like education, healthcare, and the public sector.
>
> This is what a consulting-grade responsible AI training workflow looks like."

---

## Expected Outputs (Full Demo Run)

| Output | Generated by | Formats |
|---|---|---|
| Training Needs Assessment | Phase 2 page | Markdown + PDF |
| 90-minute in-person workshop plan | Phase 3 page | Markdown + PDF |
| 6 responsible AI activities | Phase 4 page | Markdown + PDF |
| Facilitator guide with scripts | Phase 5 page | Markdown + PDF |
| Staff handout with prompt examples | Phase 6 page | Markdown + PDF |
| 10-question knowledge check with answer key | Phase 7 page | Markdown + PDF |
| Complete training pack | Phase 8 page | Markdown + PDF + PowerPoint (15 slides) |

---

*Build 4 · AI Staff Training and Workshop Generator · BrightPath ChatGPT Mastery Project*
*All scenarios are synthetic. Outputs require human review before use.*
