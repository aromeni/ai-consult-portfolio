# Screenshots — Semantic RAG Policy Assistant

**Build 3 · BrightPath ChatGPT Mastery Project**

---

## Purpose

This folder stores portfolio and demo screenshots of the Semantic RAG Policy Assistant app.

Screenshots are intended for use in:
- GitHub project pages
- LinkedIn posts and case studies
- Client demo packs
- Portfolio presentations

---

## Safety Requirements Before Taking Screenshots

> **Use synthetic documents only.**
> All screenshots must be taken using the synthetic policy documents included in
> `data/synthetic_documents/`. These documents are for demonstration purposes only
> and do not contain real personal, sensitive, or regulated information.

The following must **never** appear in any screenshot stored in this folder or shared publicly:

- Real learner data of any kind (names, IDs, progress, attendance, grades)
- Safeguarding case information, welfare referrals, or disclosure records
- Confidential client records, contracts, or commercial information
- Staff HR data, disciplinary records, or personal performance information
- Personal data that could identify any living individual
- Regulated information subject to GDPR, DPA 2018, or any other data protection law
- API keys, access tokens, or credentials of any kind
- `.env` files, secrets files, or configuration files containing private values
- Private local file paths that reveal system usernames, home directories, or folder structures
- Browser session data, saved passwords, or autofill suggestions

If you are unsure whether a screenshot is safe to share, **do not share it** until you have reviewed it carefully.

---

## Recommended Screenshot Preparation

1. **Crop carefully.** Remove browser address bars, OS taskbars, system notifications, and any background windows.
2. **Check the full frame.** Scroll the content area and check all visible text before capturing.
3. **Use private or incognito mode** when taking screenshots for public use, to reduce accidental autofill or saved-session exposure.
4. **Label files clearly** using the naming convention below.

---

## Expected Screenshot Files

The following 11 screenshots are part of the recommended Build 3 portfolio set.
See `docs/screenshots-checklist.md` for the full guidance table.

| Filename | Page / Feature |
|---|---|
| `01-home-page.png` | Home page — RAG pipeline diagram and completed phases |
| `02-document-library.png` | Document Library — synthetic document metadata table |
| `03-chunking-explorer.png` | Chunking Explorer — generated chunks and summary metrics |
| `04-embedding-index-builder.png` | Embedding Index Builder — embeddings generated (Step 1) |
| `05-faiss-index-summary.png` | Embedding Index Builder — FAISS index built (Step 2) |
| `06-semantic-search-learner-data.png` | Semantic Search — results for demo query |
| `07-rag-qa-learner-data.png` | RAG Q&A — grounded answer for demo query |
| `08-retrieval-comparison.png` | Retrieval Comparison — keyword vs semantic side by side |
| `09-mini-answer-report-preview.png` | Mini Answer Report — report preview and download button |
| `10-downloaded-markdown-report.png` | Downloaded Markdown report open in editor or viewer |
| `11-test-results-terminal.png` | Terminal — pytest passing (429 passed) |

---

## Demo Query Used in Screenshots

```
Can staff put learner names into ChatGPT?
```

This question is the recommended demo input throughout the pipeline because it:
- Triggers the learner data caution flag in RAG Q&A
- Produces clear keyword and semantic results in Retrieval Comparison
- Generates a complete, evidence-grounded answer with a responsible-use note

---

## Format and Resolution

| Setting | Recommendation |
|---|---|
| Format | PNG (preferred) — lossless, renders cleanly on GitHub and in documents |
| Resolution | At least 1280 × 800 |
| Zoom | 100% browser zoom — avoid zoomed-in captures that cut off content |
| Window width | Full-width Streamlit layout — use `layout="wide"` (already configured) |

---

*Build 3 · Semantic RAG Policy Assistant · BrightPath ChatGPT Mastery Project*
*All documents used in this prototype are synthetic and for demonstration purposes only.*
