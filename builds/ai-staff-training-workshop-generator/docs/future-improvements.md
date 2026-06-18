# Future Improvements — AI Staff Training and Workshop Generator

**Build 4 · BrightPath ChatGPT Mastery Project**

---

## Planned Phases (Build 4 Roadmap)

| Phase | Feature |
|---|---|
| 1 | Scaffold, synthetic scenario setup, app navigation *(complete)* |
| 2 | Training needs assessment — topic scoring, risk theme identification *(complete)* |
| 3 | Workshop planner — agenda, learning outcomes, timed segments *(complete)* |
| 4 | Activity generator — safe/unsafe prompts, risky prompt rewrite, hallucination review, learner data boundaries, safeguarding escalation, human review checklist, approved tools decision, bias and fairness review *(complete)* |
| 5 | Facilitator guide — opening/closing scripts, section delivery notes, activity facilitation notes, misconceptions, debrief guidance *(complete)* |
| 6 | Staff handout — AI safe-use reference for workshop attendees *(complete)* |
| 7 | Knowledge check — multiple-choice questions, scenario questions, reflection prompts, answer key, pass/review guidance *(complete)* |
| 8 | Training pack export — readiness check, section selector, full Markdown pack assembly and download *(complete)* |
| 9 | Completion review and portfolio documentation *(complete)* |
| Polish A | Professional UI, analytics charts, training pack PDF export, PowerPoint/PPTX export *(complete)* |
| Polish A5 | Standalone 15-slide PowerPoint training deck with utility functions, auto-generation on pack assembly *(complete)* |
| Polish B | Modern dashboard styling, per-report PDF export on every report page, reusable PDF exporter, chart utilities, premium training pack PDF *(complete)* |

---

## Short-Term Improvements

- **Screenshots and demo assets** — capture app screenshots using the BrightPath demo scenario; see [docs/screenshots-checklist.md](screenshots-checklist.md)
- **Advanced branded PDF themes** — PDF with organisation logo, colour scheme, and custom cover page (per-report PDF export is complete in Polish B)
- **Advanced branded PPTX templates** — custom slide master with organisation logo, brand colours, and editable slide themes (15-slide deck is complete in Polish A5)
- **Clearer demo presets** — one-click demo flow that pre-fills all pages for a faster walkthrough
- **Better Markdown preview** — syntax-highlighted or rendered preview of the training pack before download
- **Richer tests for generated content** — additional assertions on content quality, not just structure
- **More scenario templates** — additional pre-built synthetic scenarios (education, healthcare, professional services, retail, public sector)
- **Custom scenario input** — allow trainers to enter their own organisation details via the form (form exists in Phase 1; content enrichment for new scenarios is the next step)

---

## Medium-Term Improvements

- **Editable training templates** — allow trainers to customise section headings, activity descriptions, and escalation contacts before export
- **Multiple organisation profiles** — save and switch between multiple synthetic scenario profiles within a session
- **Configurable workshop duration** — more granular duration control (e.g. 45 minutes, 2 hours) beyond the current 60/90/120 options
- **Richer knowledge-check scoring** — weighted scoring by topic priority; rubric-based feedback rather than pass/review threshold only
- **Editable Word export** — DOCX export so trainers can edit reports in Word before delivery
- **Facilitator notes in printable format** — one-click printable facilitator card format (A5, printer-friendly)
- **Staff feedback form generator** — post-workshop feedback template tied to the training topics
- **Training attendance log template** — blank attendance record for the session
- **Build 3 RAG integration** — pull semantically relevant policy evidence from Build 3's RAG pipeline to ground training activities in the organisation's actual approved policies (synthetic/approved data only)
- **Organisation-specific policy references** — link training activities to specific policy clauses (synthetic/approved data only)

---

## Long-Term Improvements

- **LLM-assisted generation (optional, local only)** — optional Ollama integration for richer training content generation, with strict evidence grounding, human review requirements, and synthetic-data-only constraints; disabled by default
- **RAG-grounded training packs** — ground training pack content in approved policy documents retrieved via Build 3's semantic RAG pipeline
- **Secure deployment** — authentication, access control, encrypted storage, audit logging, DPIA, and responsible-owner sign-off before handling any real data
- **LMS / SCORM export** — package training content for delivery via a Learning Management System
- **Staff completion tracking** — record which staff have completed training, passed the knowledge check, and committed to responsible-use behaviours
- **Training effectiveness dashboard** — follow-up survey and behaviour-change tracking after workshop delivery
- **Client-specific governance configuration** — allow governance leads to configure escalation contacts, approved tools list, and responsible-use boundaries per organisation
- **Human approval workflow** — route generated training materials through a named reviewer before they are marked as ready to deliver
- **Build 1 audit integration** — import audit recommendations directly as training priority inputs
- **Scenario library** — multiple pre-built synthetic scenarios covering education, healthcare, professional services, retail, and public sector

---

## Not Yet / Avoid For Now

The following are explicitly excluded from all current and near-term phases:

- Real learner data, safeguarding case documents, HR/disciplinary files, personal data, or regulated information — strictly prohibited
- Production claims — this is a prototype; no output should be used as official training policy without qualified human review and organisational approval
- Unsupervised legal, compliance, safeguarding, clinical, or HR interpretation — all outputs require human review
- Model-generated training advice without evidence, citations, and human review — deterministic templates only until strict evidence grounding controls are in place
- Deployment for real client data without full DPIA, governance, security, and responsible-owner review

---

*Build 4 · AI Staff Training and Workshop Generator · BrightPath ChatGPT Mastery Project*
