# Screenshots Checklist — Document Intelligence / RAG Demo

**Build 2 · Prototype v0.6**

Use these scenarios for portfolio, GitHub, and LinkedIn screenshots.
Screenshots are stored in [`assets/screenshots/`](../assets/screenshots/).

---

## Safety Reminder

**Before taking any screenshot:**

- Use synthetic documents only — do not show real learner data, safeguarding case information, confidential client records, staff HR data, personal data, or regulated information
- Do not expose API keys, `.env` file contents, secrets, or private local paths
- Crop browser clutter (bookmarks bar, unrelated tabs, notifications) out of the frame
- These screenshots are intended for public portfolio use — review before publishing

---

## Screenshot Scenarios

| # | Filename | App page | What to show | Demo input | Expected result | Safety note |
|---|---|---|---|---|---|---|
| 1 | `01-home-page.png` | Home | Responsible-use warning, document list | None | Welcome text + four synthetic doc names + warning banner | No real data visible |
| 2 | `02-document-library.png` | Document Library | All four synthetic documents with metadata | Open one expander | Document card showing word count, line count, file size | No real doc names or data |
| 3 | `03-document-viewer.png` | Document Viewer | Inline search with results | Select `synthetic-ai-acceptable-use-policy.md`, search `safeguarding` | Matched lines at top with line numbers and matched terms; full doc below | Synthetic doc only |
| 4 | `04-keyword-search-learner-data.png` | Policy Q&A → Keyword Search tab | Multi-document results with relevance | Click suggested search `learner data` | 10–20 result cards showing document name, line number, relevance count, matched terms | Synthetic results only |
| 5 | `05-evidence-extraction-safeguarding.png` | Evidence Extraction | Topic-based evidence across all docs | Topic: `safeguarding`, scope: All documents, click Extract | 10–20 evidence items ranked by relevance, with document name, line number, matched keywords | Synthetic results only |
| 6 | `06-risk-safeguard-summary.png` | Risk and Safeguard Summary | Five-topic risk and safeguard summary | Select topics: learner data, safeguarding, human review, approved tools, hallucination — click Generate summary | Metrics row (4 cols), at least one expanded topic card showing risk, safeguards, owner, evidence snippets | Synthetic results only |
| 7 | `07-mini-brief-preview.png` | Mini Brief | Brief preview with metrics and short answer | Click preset `Learner Data and AI Use`, click Generate brief, open preview | 3-col metrics, short answer info box, 9-section brief in expander, download button | Synthetic content only |
| 8 | `08-policy-qa-learner-data.png` | Policy Q&A → Evidence-Based Q&A tab | Detected topics, short answer, evidence snippets | Click suggested question "Can staff enter learner data into AI tools?", click Generate answer | Detected topics caption, short answer info box, at least one evidence snippet card, safeguards section | Synthetic results only |
| 9 | `09-policy-qa-safeguarding.png` | Policy Q&A → Evidence-Based Q&A tab | Q&A result for a safeguarding question | Type "What does the policy say about safeguarding information and AI?", click Generate answer | Detected topics (safeguarding, escalation, human review, accountability), short answer, evidence snippets | Synthetic results only |
| 10 | `10-test-results-terminal.png` | Terminal | Full pytest pass | Run `pytest` in `10-builds/document-intelligence-rag-demo/` | `229 passed in X.XXs` line visible | No sensitive paths visible |

---

## How to Capture

```bash
# Start the app
cd 10-builds/document-intelligence-rag-demo
source .venv/bin/activate
streamlit run app.py
```

Open `http://localhost:8501` and follow each scenario above.

Save screenshots to:

```
10-builds/document-intelligence-rag-demo/assets/screenshots/
```

See [`assets/screenshots/README.md`](../assets/screenshots/README.md) for the full file list and safety rules.

---

## Portfolio Use

Once captured, screenshots can be used in:

- **GitHub README.md** — embed in the Features or Demo Scenario section using `![alt text](assets/screenshots/01-home-page.png)`
- **LinkedIn case study** — attach to the article or post
- **Portfolio site** — include in the Build 2 project page
- **Client demonstration pack** — include alongside [docs/demo-script.md](demo-script.md)

---

*Build 2 · Document Intelligence / RAG Demo · All screenshots must use synthetic documents only.*
