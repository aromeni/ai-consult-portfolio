# Screenshots Checklist — AI Staff Training and Workshop Generator

**Build 4 · BrightPath ChatGPT Mastery Project**

---

## Purpose

This checklist tracks screenshots needed for portfolio use. All screenshots must use the synthetic BrightPath demo scenario only.

Store completed screenshots in `assets/screenshots/`.

---

## Screenshot Guidance

- Use the synthetic BrightPath demo scenario only — do not capture real learner, safeguarding, HR, personal, client, or regulated data
- Do not expose local secrets, API keys, environment files, or private file paths in the frame
- Use `streamlit run app.py` from the project directory with the BrightPath scenario loaded
- Crop screenshots cleanly — remove browser chrome where it adds no value
- Use consistent browser window width (1280px or 1440px recommended)
- Label screenshots clearly for portfolio use — use the filenames below

---

## Screenshots Required

| # | Filename | Page | What to show | Status |
|---|---|---|---|---|
| 1 | `01-home-page.png` | Home | Consulting workflow diagram, Build 1–3 connections, responsible-use warning | ☐ |
| 2 | `02-organisation-scenario.png` | Organisation Scenario | BrightPath scenario loaded — metric cards (8 staff, 8 topics, 4 roles, 9 concerns), Markdown preview | ☐ |
| 3 | `03-training-needs-assessment.png` | Training Needs Assessment | Generated needs assessment — topic priority table, learning outcomes, role-specific needs, metric cards | ☐ |
| 4 | `04-workshop-planner.png` | Workshop Planner | 90-minute in-person workshop — timed agenda table, one section expanded, trainer notes | ☐ |
| 5 | `05-activity-generator.png` | Activity Generator | Default activities selected — metric cards, one activity expanded (e.g. Safe vs Unsafe Prompt Sorting) | ☐ |
| 6 | `06-facilitator-guide.png` | Facilitator Guide | Generated guide — metric cards, opening script expanded, one section delivery note expanded | ☐ |
| 7 | `07-staff-handout.png` | Staff Handout | Generated handout — metric cards, safe prompt example expanded, escalation guidance expanded | ☐ |
| 8 | `08-knowledge-check.png` | Knowledge Check | 10 questions — metric cards, MCQ 001 expanded, answer key in expander | ☐ |
| 9 | `09-training-pack-export.png` | Training Pack Export | Readiness overview (all ✓), section selector (all 12 ticked), metric cards after generation | ☐ |
| 10 | `10-training-pack-analytics.png` | Training Pack Export | Analytics charts visible — section completion, topic coverage, activity mix | ☐ |
| 11 | `11-training-pack-preview.png` | Training Pack Export | Markdown preview expanded — cover page and table of contents visible | ☐ |
| 12 | `12-pdf-export.png` | Training Pack Export | PDF download button visible in the export panel | ☐ |
| 13 | `13-pptx-export.png` | Training Pack Export | "Download PowerPoint Training Deck" button visible (auto-generated) | ☐ |
| 14 | `14-test-results-terminal.png` | Terminal | `pytest` output showing 953 passed | ☐ |
| 15 | `15-report-export-panel.png` | Any report page | "Download This Report" panel showing Markdown + PDF buttons side by side | ☐ |
| 16 | `16-report-pdf-preview.png` | PDF viewer | An open report PDF (e.g. Staff Handout) — cover page with prototype notice | ☐ |
| 17 | `17-training-pack-pdf-preview.png` | PDF viewer | The full Training Pack PDF — executive summary or analytics chart page | ☐ |
| 18 | `18-pptx-title-slide.png` | PowerPoint viewer | Slide 1 — full navy title slide with org name and prototype footer | ☐ |
| 19 | `19-pptx-responsible-use-slide.png` | PowerPoint viewer | Slide 14 — Responsible-Use Boundaries with red left accent bar | ☐ |

---

## How to Capture

```bash
# Navigate to the project
cd 10-builds/ai-staff-training-workshop-generator

# Activate virtual environment
source .venv/bin/activate

# Start the app
streamlit run app.py

# In browser: http://localhost:8501
# 1. Organisation Scenario → Load BrightPath Demo Scenario
# 2. Run each page in order, generating outputs
# 3. Capture screenshots as listed above

# For test results terminal screenshot:
pytest
# Capture the terminal output showing "910 passed"
```

---

## Screenshot Tips by Page

**Home page**
- Scroll to show the full consulting workflow diagram
- Make sure the responsible-use warning is visible

**Organisation Scenario**
- Load BrightPath demo scenario — do not use the form with any real data
- Show metric cards and the Markdown preview (partially expanded)

**Training Needs Assessment**
- Show the topic priority table — HIGH topics should be visible
- Expand the learning outcomes section
- Show the role-specific needs cards

**Workshop Planner**
- Use 90-minute in-person — the recommended demo setting
- Show the full timed agenda table
- Expand one agenda section (e.g. "Safe Prompting Practice")

**Activity Generator**
- Leave default activities selected (6 types)
- Show metric cards
- Expand "Safe vs Unsafe Prompt Sorting" — show cards A–F

**Facilitator Guide**
- Show the facilitator principles section
- Expand the opening script — show the synthetic-data ground rules

**Staff Handout**
- Expand one safe prompt example — show the explicit "Do not include names..." instruction
- Expand the escalation guidance for Safeguarding

**Knowledge Check**
- Select 10 questions with answer key included
- Expand MCQ 001 — show question, options, and correct answer
- Show the pass guidance at the bottom

**Training Pack Export**
- Show the readiness overview with all sections marked ✓
- Show the section selector with all 12 checkboxes ticked
- After generating: show metric cards and the facilitator review checklist

**Training Pack Preview**
- Expand the Markdown preview
- Scroll to show the cover page and the start of the table of contents

**Report Export Panels**
- On any report page after generating, capture the "Download This Report" panel with the Markdown and PDF buttons side by side

**PDF Previews**
- Open a downloaded report PDF and capture the cover page (organisation name, generated date, prototype notice)
- Open the Training Pack PDF and capture the executive summary or an analytics chart page

**Test Results Terminal**
- Run `pytest` from the project directory
- Capture the "910 passed" summary line

---

## After Screenshots

- Place files in `assets/screenshots/` using the filenames above
- Update `assets/screenshots/README.md` to confirm each screenshot is complete
- Consider a `docs/demo-assets/` folder for any exported Markdown training pack samples

---

*Build 4 · AI Staff Training and Workshop Generator · BrightPath ChatGPT Mastery Project*
*All screenshots must use synthetic scenarios only. No real data.*
