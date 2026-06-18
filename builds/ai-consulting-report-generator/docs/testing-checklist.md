# Build 5 Testing Checklist

Use this checklist before portfolio review, recording screenshots, or presenting the demo.

---

## Automated Tests

```bash
cd 10-builds/ai-consulting-report-generator
source .venv/bin/activate
pytest
```

Expected result: all tests pass.

---

## Manual Full Workflow

1. Open the app.
2. Load BrightPath demo audit data.
3. Generate Readiness Summary.
4. Generate Risk Register.
5. Generate Opportunity Portfolio.
6. Generate Roadmap.
7. Generate Report Sections.
8. Generate Client Report.
9. Generate Export Centre outputs.
10. Generate Completion Review.
11. Download Markdown report.
12. Download PDF report.
13. Download PowerPoint deck.
14. Confirm charts appear in the Export Centre, or confirm graceful failure message if charts are unavailable.
15. Confirm responsible-use boundaries appear on every page.
16. Confirm no real data is used anywhere in the app or outputs.
17. Run pytest.

---

## Completion Review Checks

- Phase checklist appears
- Output completion status appears
- Documentation checklist appears
- Portfolio value appears
- Commercial value appears
- Technical value appears
- Responsible-use position appears
- Recommended final actions appear
- Completion review Markdown download works
- Portfolio notes Markdown download works

---

## Export Checks

- Markdown report downloads and opens
- PDF report downloads and opens
- PowerPoint deck downloads and opens
- PDF includes responsible-use section
- PowerPoint includes Responsible-Use Boundaries slide
- Charts render or fail gracefully without crashing exports

---

## Safety Checks

- Synthetic BrightPath data only
- No real client records
- No learner data
- No safeguarding case data
- No staff HR data
- No personal data
- No confidential data
- No regulated information
- No production-readiness claims
- Human review requirement visible

---

*Build 5 - Testing Checklist*
