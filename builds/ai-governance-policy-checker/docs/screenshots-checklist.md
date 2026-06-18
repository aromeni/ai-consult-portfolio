# Screenshots Checklist — AI Governance Policy Checker

**Build 6 · Phases 1–8 · BrightPath ChatGPT Mastery Project**

Capture screenshots after running the Phases 1–8 demo workflow. Use synthetic demo data only.

---

## Recommended Screenshots for Phases 1–8

| Filename | Page / Feature | What to Show | Suggested State |
|---|---|---|---|
| `01-home-page.png` | Home | Project title, workflow steps, connections to builds | Home page loaded |
| `02-policy-library.png` | Policy Library | Load button visible, metric row, at least one policy expander open | Policy pack loaded |
| `03-policy-pack-loaded.png` | Policy Library | After loading: metrics, policy list, risk areas, Markdown download button | Policy pack loaded, expander open |
| `04-governance-framework.png` | Governance Framework | Framework loaded: metric row, at least one domain expander open | GOV-006 Safeguarding expander open |
| `05-policy-checker.png` | Policy Checker | Overall score, coverage level, domain detail expanders | Coverage check complete |
| `06-gap-analysis.png` | Gap Analysis | Gap summary metrics, overall gap position, at least one gap expander open | Gap analysis complete |
| `07-recommendations.png` | Recommendations | Summary metrics, highest priority recommendation, at least one expander open | Recommendations generated |
| `08-governance-maturity.png` | Governance Maturity | Overall score, maturity level, domain maturity table, at least one domain expander | Maturity summary generated |
| `09-governance-report.png` | Governance Report | Report generated: summary metrics, Markdown preview | Full report generated |
| `10-export-centre.png` | Export Centre | Readiness checklist, analytics, chart previews, download buttons | All outputs available, charts visible |
| `11-pdf-report-preview.png` | PDF | Opened PDF showing cover page and analytics section | PDF downloaded and opened |
| `12-completion-review.png` | Completion Review | Phase checklist, output status, portfolio value, download buttons | All phases complete |
| `13-test-results-terminal.png` | Terminal | pytest output showing 783+ tests passing | `pytest` run from the project directory |

---

## Safety Reminder

- Use BrightPath synthetic demo data only
- Do not include real client records, learner data, safeguarding case information, personal data, confidential data, or regulated information in any screenshot
- Avoid browser tabs, personal folders, or personal information visible in the frame
- Confirm responsible-use warnings are visible where possible

---

## Capture Instructions

1. Run the app:
   ```bash
   cd 10-builds/ai-governance-policy-checker
   source .venv/bin/activate
   streamlit run app.py
   ```
2. Open at `http://localhost:8501`
3. Follow the demo workflow in `docs/demo-script.md` — work through all 10 steps before capturing screenshots
4. Capture each screenshot and save to `assets/screenshots/`

---

## Run Tests Before Capturing Terminal Screenshot

```bash
cd 10-builds/ai-governance-policy-checker
source .venv/bin/activate
pytest
```

Confirm all tests pass before capturing the terminal screenshot.

---

## PDF Preview Capture

To capture the PDF report preview screenshot:

1. Go to Export Centre
2. Complete the full workflow (all outputs must be available)
3. Click **Download PDF Governance Report**
4. Open the downloaded PDF in a PDF reader (Preview on Mac, Adobe Reader on Windows)
5. Scroll to the cover page and capture that view

---

*Build 6 · AI Governance Policy Checker · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
