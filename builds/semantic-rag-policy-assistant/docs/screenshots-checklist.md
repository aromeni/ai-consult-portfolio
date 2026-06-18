# Screenshots Checklist — Semantic RAG Policy Assistant

**Build 3 · BrightPath ChatGPT Mastery Project**

---

## Purpose

Use this checklist to capture screenshots for portfolio use — GitHub project, LinkedIn post,
case study, client demo pack, or presentation slides.

Screenshots are saved to: `assets/screenshots/`

---

## Safety Reminder

> **Use synthetic documents only.**
> Do not capture, display, or include any real learner data, safeguarding case details,
> confidential client records, staff HR data, personal data, or regulated information.
>
> Do not expose local secrets, API keys, environment files, or private file paths.
>
> Crop screenshots cleanly. Remove browser address bars, system notifications, and
> unrelated content where possible.
>
> If you are unsure whether a screenshot is safe to share, do not share it.

See `assets/screenshots/README.md` for the full safety checklist.

---

## Demo Scenario

**Demo question used throughout the pipeline:**

> Can staff put learner names into ChatGPT?

This question:
- Produces clear keyword and semantic results
- Triggers the learner data caution flag in RAG Q&A
- Generates a well-grounded answer with responsible-use notes
- Is safe to demonstrate to clients and use in public portfolio materials

**Recommended pipeline flow for screenshots:**

Home → Document Library → Chunking Explorer → Embedding Index Builder → FAISS Index →
Semantic Search → RAG Q&A → Retrieval Comparison → Mini Answer Report → pytest terminal

---

## Screenshot Table

| # | Filename | App Page / Feature | What to Show | Suggested Demo Input | Expected Result | Safety Reminder |
|---|---|---|---|---|---|---|
| 1 | `01-home-page.png` | Home | RAG pipeline workflow diagram, completed phases grid, live metric cards (documents, words, chunks, phase), sidebar navigation | — | All 8 phases shown as green completion items; metric cards populated | No personal data visible; synthetic-only notice visible |
| 2 | `02-document-library.png` | Document Library | Metadata table with all 4 synthetic documents (filename, title, word count, line count); one document preview expanded | Select `synthetic-ai-acceptable-use-policy.md` for preview | Metadata table visible; document preview shows synthetic policy content | Confirm document content is synthetic only; no real names or personal data |
| 3 | `03-chunking-explorer.png` | Chunking Explorer | Chunk settings, estimated chunk count, generated chunk summary metrics (total chunks, avg size), chunk table | Chunk size: 120, overlap: 30, All documents | 5 metric cards; chunk table with chunk IDs and document names | No personal data in chunk text; synthetic documents only |
| 4 | `04-embedding-index-builder.png` | Embedding Index Builder — Step 1 | Embeddings generated success state; model name (all-MiniLM-L6-v2), chunk count, embedding dimensions (384), normalised status; embedding preview table | Use default model name; click Generate Embeddings | Green index-ready bar; embedding preview table showing first 8 vector values | No real document content needed; embedding values are numerical |
| 5 | `05-faiss-index-summary.png` | Embedding Index Builder — Step 2 | FAISS index built success state; index type (IndexFlatIP), metric (cosine), vectors indexed, dimension (384), document count; vector store summary table | Select cosine metric; click Build FAISS Index | Green index-ready bar; 5 metric cards; vector store summary table | No personal data; numerical values only |
| 6 | `06-semantic-search-learner-data.png` | Semantic Search | Query input with demo question; top 5 result cards showing rank pill, score pill, document pill, word-count pill, chunk ID, text preview | `Can staff put learner names into ChatGPT?` | 5 ranked result cards with blue left-border styling | Confirm chunk text is from synthetic documents only |
| 7 | `07-rag-qa-learner-data.png` | RAG Q&A | Grounded answer card (blue); caution banner (if triggered); metric cards (question type, detected topics, chunks retrieved); evidence cards below | `Can staff put learner names into ChatGPT?` | Red caution banner for learner data; blue answer card; green evidence cards | Confirm answer is template-based; no real learner names visible |
| 8 | `08-retrieval-comparison.png` | Retrieval Comparison | Side-by-side columns: keyword results (navy header) and semantic results (green header); comparison insight card (amber); metric summary cards; overlap table | `Can staff put learner names into ChatGPT?` | Both columns populated; amber insight card visible; overlap table or "no overlap" message | Confirm results are from synthetic documents only |
| 9 | `09-mini-answer-report-preview.png` | Mini Answer Report | Report settings (title input, reviewer notes, comparison checkbox, max evidence slider); metric cards (question, evidence count, topics, comparison); report preview expander showing first few report sections; download button | Run after RAG Q&A and Retrieval Comparison; click Generate Report | Report preview showing `# Semantic RAG Mini Answer Report`, section headings, evidence items; download button visible | Confirm no real learner data in report content |
| 10 | `10-downloaded-markdown-report.png` | Downloaded .md report | The downloaded `.md` file open in a text editor or Markdown viewer (e.g. VS Code, Typora, GitHub preview); at least 3–4 section headings visible | Open the downloaded file from `semantic-rag-answer-report.md` | Section headings: `# Semantic RAG Mini Answer Report`, `## 1. Question`, `## 2. Short Grounded Answer`, `## 5. Retrieved Evidence`, `## 8. Limitations` | Confirm no personal data in the report file before sharing |
| 11 | `11-test-results-terminal.png` | Terminal (pytest) | Terminal window showing `pytest` run output: `429 passed` (or current count); no errors; fast run time | Run: `pytest` from `semantic-rag-policy-assistant/` directory | `429 passed in X.XXs` — all green | No personal data in test output; no private paths in visible terminal text |

---

## Capture Status

Track your progress here:

- [ ] `01-home-page.png`
- [ ] `02-document-library.png`
- [ ] `03-chunking-explorer.png`
- [ ] `04-embedding-index-builder.png`
- [ ] `05-faiss-index-summary.png`
- [ ] `06-semantic-search-learner-data.png`
- [ ] `07-rag-qa-learner-data.png`
- [ ] `08-retrieval-comparison.png`
- [ ] `09-mini-answer-report-preview.png`
- [ ] `10-downloaded-markdown-report.png`
- [ ] `11-test-results-terminal.png`

---

## Before the Demo / Screenshot Session

1. Launch the app: `streamlit run app.py`
2. Navigate to Chunking Explorer → generate chunks (chunk size 120, overlap 30)
3. Navigate to Embedding Index Builder → generate embeddings → build FAISS index
4. Confirm the index-ready bar is green on Semantic Search and RAG Q&A pages
5. Use the demo question `Can staff put learner names into ChatGPT?` throughout
6. Optional: run Retrieval Comparison before Mini Answer Report to include it in the report

---

## Screenshot Guidance

| Setting | Recommendation |
|---|---|
| Format | PNG — lossless, renders cleanly on GitHub and in presentations |
| Resolution | At least 1280 × 800 |
| Browser zoom | 100% — avoid partial captures from zoomed views |
| Window width | Full width — Streamlit is configured with `layout="wide"` |
| Cropping | Remove OS taskbar, browser tabs, and unrelated windows |
| Filename | Use exact filenames above for consistency with README references |
| Storage | Save to `assets/screenshots/` |

---

## Portfolio Usage

These 11 screenshots support:

| Use | Recommended screenshots |
|---|---|
| GitHub README banner / pipeline image | 1, 6, 7 |
| LinkedIn post (3–5 screenshots) | 1, 6, 7, 8, 11 |
| Case study document | All 11 in order |
| Client demo slideshow | 1, 3, 6, 7, 8, 9, 11 |
| CV / portfolio website | 1, 7, 9 |

---

*Build 3 · Semantic RAG Policy Assistant · BrightPath ChatGPT Mastery Project*
*All documents used in this prototype are synthetic and for demonstration purposes only.*
