# Screenshots — Document Intelligence / RAG Demo

**Build 2 · Prototype v0.6**

This folder stores screenshots captured for portfolio, GitHub, and LinkedIn use.

---

## Safety Rules

**Before taking any screenshot, verify:**

- All data shown is synthetic — no real learner data, safeguarding case information, confidential client records, staff HR data, personal data, or regulated information
- No API keys, `.env` file contents, or secrets are visible
- No private local filesystem paths are visible where avoidable
- Browser clutter (bookmarks, notifications, unrelated tabs) is cropped out
- Screenshot is labelled clearly using the filename conventions below

If in doubt, do not take the screenshot. These images are intended for public portfolio use.

---

## Expected Files

| Filename | App page / feature |
|---|---|
| `01-home-page.png` | Home page — document list and responsible-use notice |
| `02-document-library.png` | Document Library — all four synthetic documents visible |
| `03-document-viewer.png` | Document Viewer — synthetic-ai-acceptable-use-policy.md open |
| `04-keyword-search-learner-data.png` | Policy Q&A → Keyword Search tab — results for "learner data" |
| `05-evidence-extraction-safeguarding.png` | Evidence Extraction — topic "safeguarding", all documents |
| `06-risk-safeguard-summary.png` | Risk and Safeguard Summary — five-topic set generated |
| `07-mini-brief-preview.png` | Mini Brief — Learner Data preset, preview expanded |
| `08-policy-qa-learner-data.png` | Policy Q&A → Evidence-Based Q&A — "Can staff enter learner data into AI tools?" |
| `09-policy-qa-safeguarding.png` | Policy Q&A → Evidence-Based Q&A — "What does the policy say about safeguarding information and AI?" |
| `10-test-results-terminal.png` | Terminal — pytest showing 229 tests passing |

---

## How to Capture

1. Run the app: `streamlit run app.py` from `10-builds/document-intelligence-rag-demo/`
2. Follow the scenarios in [../../docs/screenshots-checklist.md](../../docs/screenshots-checklist.md)
3. Crop to the app window only — no browser chrome needed
4. Save each file using the exact filename above

---

*Build 2 · Document Intelligence / RAG Demo · All screenshots must use synthetic documents only.*
