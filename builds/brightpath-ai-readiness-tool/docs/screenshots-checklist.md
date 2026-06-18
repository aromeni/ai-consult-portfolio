# Screenshots Checklist — BrightPath AI Readiness + Workflow Audit Tool

Use this checklist when capturing screenshots for the portfolio, GitHub README, or LinkedIn case study.

---

## Safety Rules (Read Before Capturing)

**All screenshots must use synthetic BrightPath-style data only.**

- Load BrightPath demo data from the Home page before capturing any screenshot
- Do not show real personal data, learner records, client data, staff information, safeguarding details, or confidential documents
- Do not expose local file paths, API keys, environment variables, credentials, or terminal history containing sensitive information
- Crop screenshots cleanly — remove browser toolbars, unrelated tabs, and desktop notifications
- Do not commit screenshots containing real client data to any repository

---

## Core Screenshots

| Done | Filename | Page / Feature | What to Show | Data to Use | Safety Reminder |
|---|---|---|---|---|---|
| ☐ | `01-home-page.png` | Home | Title, welcome text, metrics (7 pages / 10 dimensions / 8 workflows), Load BrightPath demo data button, responsible-use notice | Click Load BrightPath demo data before any other page | No personal data visible on screen |
| ☐ | `02-organisation-profile.png` | Organisation Profile | BrightPath profile loaded — org type, sector, tools in use, policy flags, notes | BrightPath demo data pre-loaded from Home | Confirm profile shows synthetic org details only |
| ☐ | `03-ai-readiness-assessment.png` | AI Readiness Assessment | All 10 sliders populated, score 35 / 100, category "Early awareness", coloured alert, bar chart visible | BrightPath demo data loaded from Home | No real staff or individual scores |
| ☐ | `04-workflow-audit.png` | Workflow Audit | Sample workflow loaded, form populated, suitability score 42 / 50, "Good pilot candidate", bar chart | Click Load BrightPath sample workflow on the Workflow Audit page | No real workflow names, staff roles, or org-specific details |
| ☐ | `05-risk-assessment-matrix.png` | Risk Assessment | Sample risk profile loaded, risk summary table, High risk warning for safeguarding, overall summary metrics | Click Load BrightPath sample risk profile on the Risk Assessment page | No real risk data, client context, or case information |
| ☐ | `06-pilot-recommendation.png` | Pilot Recommendation | "Governance-first before pilot" recommendation, explanation, next actions, safeguards, summary table | Auto-computed from BrightPath data loaded on earlier pages | No real client name, engagement details, or confidential information |
| ☐ | `07-mini-report-preview.png` | Mini Report | BrightPath sample report data loaded, preview expander open, Section 1 and Section 8 visible | Click Load BrightPath sample report data on the Mini Report page | Confirm no personal data appears in the preview before capturing |
| ☐ | `08-downloaded-markdown-report.png` | Downloaded report | `.md` file open in VS Code or a Markdown viewer, all 9 section headers visible | File downloaded from Mini Report page using BrightPath sample data only | Open only the downloaded synthetic file — not personal folders, desktops, or client files |

---

## Additional Screenshots (Optional)

These are useful for a deeper portfolio presentation but not required for the core demo.

| Filename | Page / Feature | What to Show | Safety Reminder |
|---|---|---|---|
| `03b-readiness-score-detail.png` | AI Readiness Assessment | Close-up of the coloured alert and "Suggested next action" text | No real scores |
| `05b-risk-safeguarding-detail.png` | Risk Assessment | Close-up of the High risk warning box for safeguarding, including the required safeguard text | No real case details |
| `08b-report-section-8.png` | Downloaded report | Section 8 — Responsible Use and Limitations | Synthetic data only |
| `09-terminal-running.png` | Terminal | `streamlit run app.py` command and `http://localhost:8501` URL visible | Crop terminal history; no file paths or credentials visible |
| `10-requirements-txt.png` | `requirements.txt` | Only `streamlit` and `pandas` — shows minimal dependency footprint | No sensitive config visible |

---

## Portfolio Use

**GitHub README:** Use `03-ai-readiness-assessment.png`, `06-pilot-recommendation.png`, and `07-mini-report-preview.png` — these show the scoring, recommendation, and output in one pass.

**LinkedIn case study:** Lead with `06-pilot-recommendation.png` — it shows the most value in one view. Add `07-mini-report-preview.png` to show the deliverable.

**Portfolio document / slide deck:** Use `04-workflow-audit.png` (scoring approach), `05-risk-assessment-matrix.png` (governance methodology), and `08-downloaded-markdown-report.png` (client-facing output).

---

## File Storage

Save all screenshots to `assets/screenshots/` using the exact filenames listed above. See [`assets/screenshots/README.md`](../assets/screenshots/README.md) for the naming convention and folder guidance.
