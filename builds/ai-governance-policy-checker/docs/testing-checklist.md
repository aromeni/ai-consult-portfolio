# Manual Testing Checklist — AI Governance Policy Checker

**Build 6 · Phases 1–8 · BrightPath ChatGPT Mastery Project**

Run these manual tests after `pytest` passes to confirm the full workflow works end-to-end.

---

## Setup

```bash
cd 10-builds/ai-governance-policy-checker
source .venv/bin/activate
streamlit run app.py
```

Open at `http://localhost:8501`.

---

## Full Workflow Test

### Step 1: Home Page

- [ ] Home page loads without errors
- [ ] Project title visible: AI Governance Policy Checker
- [ ] Governance review workflow steps visible
- [ ] Connections to Builds 1–5 visible
- [ ] Responsible-use warning displayed
- [ ] Prototype notice displayed

### Step 2: Policy Library

- [ ] Policy Library page loads without errors
- [ ] "Load BrightPath Synthetic Policy Pack" button visible
- [ ] Click the button — policy pack loads successfully
- [ ] Metric row shows: 6 policies
- [ ] At least one policy expander can be opened
- [ ] Policy content (summary, risk areas, owner) is visible inside expander
- [ ] "Download Policy Pack Markdown" button appears
- [ ] Synthetic data warning visible at bottom

### Step 3: Governance Framework

- [ ] Governance Framework page loads without errors
- [ ] "Load Responsible AI Governance Framework" button visible
- [ ] Click the button — framework loads successfully
- [ ] Metric row shows: 12 domains, 7 high priority, 5 medium priority
- [ ] At least one domain expander can be opened (e.g. GOV-006 Safeguarding)
- [ ] Expected policy evidence and example controls visible inside expander
- [ ] "Download Framework Markdown" button appears

### Step 4: Policy Checker

- [ ] Policy Checker page loads without errors (assuming policy pack and framework loaded)
- [ ] "Run Policy Coverage Check" button visible
- [ ] Click the button — coverage check runs
- [ ] Overall score and coverage level displayed
- [ ] Progress bar visible
- [ ] Coverage counts shown (Strong / Partial / Weak / Not covered)
- [ ] Domain coverage expanders open correctly
- [ ] Evidence snippets visible in at least one domain
- [ ] "Download Coverage Review Markdown" button appears

### Step 5: Gap Analysis

- [ ] Gap Analysis page loads and auto-generates from coverage results
- [ ] Gap summary metrics displayed (total gaps, critical/high/medium/low counts)
- [ ] Overall gap position message displayed (error/warning/success)
- [ ] At least one gap expander opens correctly
- [ ] Missing evidence, risk statement, and action hint visible inside expander
- [ ] "Download Gap Analysis Markdown" button appears

### Step 6: Recommendations

- [ ] Recommendations page loads and auto-generates from gap analysis
- [ ] Recommendation summary metrics displayed
- [ ] Highest priority recommendation visible
- [ ] At least one recommendation expander opens correctly
- [ ] Wording direction, implementation steps, review questions, success criteria visible inside
- [ ] "Download Recommendations Markdown" button appears

### Step 7: Governance Maturity

- [ ] Governance Maturity page loads and auto-generates from coverage + gaps + recommendations
- [ ] Overall governance score and maturity level displayed
- [ ] Progress bar visible
- [ ] Adoption readiness position displayed
- [ ] Maturity blockers section visible (or "No blockers" message)
- [ ] Domain maturity scores table populated
- [ ] "Download Governance Maturity Markdown" button appears

### Step 8: Governance Report

- [ ] Governance Report page loads without errors
- [ ] Readiness checklist shows available and missing outputs
- [ ] Section selection checkboxes visible and pre-selected
- [ ] "Generate Governance Report" button visible
- [ ] Click the button — report generates successfully
- [ ] Report summary metrics displayed
- [ ] Markdown preview loads (first 10,000 characters visible)
- [ ] "Download Governance Report Markdown" button appears and downloads a file

### Step 9: Export Centre

- [ ] Export Centre page loads without errors
- [ ] Readiness checklist shows available outputs
- [ ] Package summary metrics displayed
- [ ] Export quality checklist visible (Required / Recommended / Advisory)
- [ ] Analytics section populates (coverage levels, gap severities, etc.)
- [ ] Charts section shows 6 chart previews (or graceful info message if charts fail)
- [ ] "Download Markdown Governance Report" button visible and downloads a file
- [ ] "Download PDF Governance Report" button visible
- [ ] PDF download generates a valid PDF (opens in PDF reader, shows cover page)

### Step 10: Completion Review

- [ ] Completion Review page loads without errors (even if some outputs are missing)
- [ ] Phase completion checklist shows 8 phases (all ✅)
- [ ] Output completion metrics displayed
- [ ] Documentation checklist shows existing and missing files
- [ ] Portfolio value, commercial value, technical value sections visible
- [ ] Responsible-use position displayed in success box
- [ ] Recommended final actions listed
- [ ] "Download Completion Review Markdown" button visible and downloads a file
- [ ] "Download Portfolio Notes Markdown" button visible and downloads a file

---

## Responsible-Use Checks

- [ ] Responsible-use warning visible on every page
- [ ] Prototype notice visible on Home page
- [ ] No real client policies used anywhere
- [ ] No real learner data used anywhere
- [ ] No real safeguarding case information used anywhere
- [ ] No real staff HR data used anywhere
- [ ] No personal data visible in any output
- [ ] Human review requirement stated in all downloaded files

---

## Error Handling Checks

- [ ] Policy Checker shows setup guidance if policy pack is missing (navigate directly to it)
- [ ] Governance Report shows setup guidance if policy pack is missing
- [ ] Export Centre shows setup guidance if governance report is missing
- [ ] Completion Review loads without errors even if no previous outputs are present
- [ ] Charts section shows info message if charts cannot be generated

---

## Automated Tests

```bash
cd 10-builds/ai-governance-policy-checker
source .venv/bin/activate
pytest
```

- [ ] All tests pass (target: 783+)
- [ ] No test failures
- [ ] No import errors

---

## Screenshot Capture

After completing the manual tests, capture screenshots following `docs/screenshots-checklist.md`.

---

*Build 6 · AI Governance Policy Checker · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
