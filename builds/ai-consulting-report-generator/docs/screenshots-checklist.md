# Build 5 Screenshots Checklist

Capture screenshots after running the full BrightPath demo workflow. Do not include real client, learner, HR, safeguarding, personal, confidential, or regulated data.

---

## Current Screenshot Status

| Filename in `assets/screenshots/` | Page/Feature | Status |
|---|---|---|
| `01-home-page.png` | Home page | ✅ Captured |
| `02-Audit-Data.png` | Audit Data | ✅ Captured |
| `03-Readiness-Summary.png` | Readiness Summary | ✅ Captured |
| `04-Risk-Register.png` | Risk Register | ✅ Captured |
| `07-Opportunity-Portfolio.png` | Opportunity Portfolio | ✅ Captured |
| `08-RoadMap.png` | Roadmap | ✅ Captured |
| `06-Report-Section.png` | Report Sections | ✅ Captured |
| `09-Client-Report-Builder.png` | Client Report Builder | ✅ Captured |
| `10-ExportCentre.png` | Export Centre | ✅ Captured |
| `11-Completion-Review.png` | Completion Review | ✅ Captured |
| `12-Test-results-terminal.png` | Test Results Terminal | ✅ Captured |
| `10-pdf-report-preview.png` | PDF Report Preview | ⬜ Not yet captured |
| `11-powerpoint-deck-preview.png` | PowerPoint Deck Preview | ⬜ Not yet captured |

---

## To Capture: PDF Report Preview

1. Run the full workflow in the app (Audit Data → … → Export Centre).
2. Click **Download PDF Consulting Report**.
3. Open the PDF in Preview or Acrobat.
4. Capture the **cover page** (navy header, white title, BrightPath name, generated date).
5. Save as `assets/screenshots/10-pdf-report-preview.png`.

Safety reminder: The PDF is generated from synthetic demo data. Confirm no real information is in the frame.

---

## To Capture: PowerPoint Deck Preview

1. Run the full workflow and download the **Download PowerPoint Executive Deck** file.
2. Open the PPTX in PowerPoint or Keynote.
3. Capture **Slide 1** (title slide, navy background) or **Slide 14** (Responsible-Use Boundaries, amber title bar).
4. Save as `assets/screenshots/11-powerpoint-deck-preview.png`.

Safety reminder: The PPTX is generated from synthetic demo data. Confirm no real information is in the frame.

---

## Capture Notes

- Use the BrightPath demo dataset only.
- Do not include real client, learner, HR, safeguarding, personal, confidential, or regulated data in any screenshot.
- Avoid browser tabs, local folders, or personal information visible in the frame.
- Capture the responsible-use notices where possible.
- Run `pytest` and confirm all tests pass before capturing test results terminal screenshot.
- See `docs/testing-checklist.md` for the full manual workflow checklist.

---

*Build 5 · AI Consulting Report Generator · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required for all outputs.*
