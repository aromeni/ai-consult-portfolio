# Future Improvements

Improvements are grouped by effort and priority. Short-term items can be added without a major rearchitecture. Long-term items require significant design work.

---

## Short-Term Improvements

These are achievable in one or two focused sessions without changing the core architecture.

- **Organisation Profile input form** — replace the read-only display with a properly keyed form so consultants can enter (anonymised) org details in the session
- **Persistent session state** — save all session state to a local JSON file so a session can be resumed or shared without losing data
- **Multiple workflow audits** — allow the consultant to audit two or three workflows in a single session and compare suitability scores side by side
- **Automated test suite** — replace manual `ast.parse()` and assertion scripts with a proper `pytest` test suite covering all scoring functions, band thresholds, and report generator helpers
- **Portfolio screenshots** — capture and add screenshots to the `screenshots/` folder and reference them in the README
- **Deployment instructions** — add a section to README covering how to deploy to Streamlit Community Cloud for a public demo URL

---

## Medium-Term Improvements

These require more substantial changes but do not change the core concept.

- **Charts and dashboard summary** — add a Home page dashboard showing all scores at a glance once assessments are complete: readiness score, workflow score, risk level, and recommendation in a single view
- **Richer risk register** — expand the risk assessment to allow notes per risk category; export the risk register as a separate table in the report
- **Governance checklist generator** — based on the risk profile, generate a governance checklist the organisation needs to complete before piloting; items should be specific and actionable
- **Staff training recommendation generator** — based on the readiness score and staff capability dimensions, recommend a training programme format from the Layer 7 training library (60-minute briefing, half-day workshop, full-day programme, or four-week pilot)
- **Save assessment history locally** — allow the consultant to save multiple assessment sessions to a local file and retrieve them later; useful for tracking progress across visits
- **Add richer BrightPath scenario variants** — create three or four synthetic organisations with different profiles (highly ready, partially ready, governance-only blocker, workflow-only blocker) for demo and training use

---

## Long-Term Improvements

These require significant design work and should be treated as separate project phases.

- **Document upload using synthetic documents** — allow the consultant to upload a sample policy, template, or workflow document (anonymised) and use it to populate part of the assessment; keep strictly within the data safety boundaries
- **RAG / document intelligence module** — connect to a local or managed vector store to allow retrieval-augmented generation against a library of synthetic policy documents and workflow templates; requires careful governance design
- **LLM-assisted report drafting with strict safeguards** — use a managed LLM API (Claude, GPT-4) to draft or improve report sections, with strict prompting constraints preventing the model from requesting or inferring personal data; requires governance approval process before enabling
- **Benchmarking across organisations** — anonymised aggregate scoring allowing a consultant to compare a client's profile against similar organisations; requires careful anonymisation and aggregate-only display
- **Automated email or report delivery** — send the Mini Report directly to the manager's email after the session; requires SMTP configuration and data handling review

---

## Not Yet / Avoid For Now

These are explicitly out of scope for the foreseeable future.

- **Real learner data** — the tool must never handle identifiable learner records, attendance data, assessment outcomes, or progress reports
- **Safeguarding case information** — never. Any feature that could allow safeguarding case details to enter the tool must be blocked at the design stage
- **Multi-user / SaaS version** — building a multi-tenant product requires a full authentication system, database, data isolation, GDPR compliance review, and commercial/legal infrastructure; this is a separate business decision
- **Automated scoring (AI-driven)** — replacing human-scored sliders with AI-inferred scores would introduce bias, opacity, and accountability problems; the human-in-the-loop scoring is a feature, not a limitation
- **Integration with MIS or student records systems** — connecting to SIMS, ProSolution, or similar systems would introduce regulated data; this requires a full data processing agreement and governance review before any design work begins
