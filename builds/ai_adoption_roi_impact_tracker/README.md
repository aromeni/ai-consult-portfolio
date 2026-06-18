# Build 7 — AI Adoption ROI and Impact Tracker

## Purpose

Build 7 tracks whether AI adoption is producing practical value after audit, governance, training, and pilot work. It gives a consultant a structured place to record early adoption metrics and convert them into directional ROI evidence before moving into deeper analysis.

## How Build 7 fits the overall portfolio

This build connects the earlier portfolio tools into a follow-up measurement workflow:

- Build 1 identifies candidate workflows and readiness gaps.
- Build 4 supports staff training and confidence-building.
- Build 5 turns findings into consulting reports.
- Build 6 checks governance and responsible-use controls.
- Build 7 tracks whether adoption is creating measurable operational value and whether risks are being managed.

## Phase 1 — Adoption Metrics Setup

Phase 1 scaffolds the app, synthetic data, validation logic, basic calculations, tests, and portfolio notes. It prepares the foundation for later phases without building money-based ROI scoring, charts, exports, or advanced recommendations.

## Phase 2 — ROI Summary Engine

Phase 2 adds a deterministic ROI summary engine that converts synthetic adoption metrics into practical consulting indicators.

Phase 2 provides:

- **Workflow-level ROI summaries** — minutes saved per task, weekly/monthly/annual hours saved, efficiency gain percentage, synthetic value-equivalent estimates, time-saving bands, confidence improvement bands, and adoption value indicators.
- **Organisation-level ROI summaries** — totals and averages across all workflows for each synthetic organisation.
- **Portfolio-level ROI summary** — totals and averages across all organisations and workflows, with a breakdown of adoption value indicators.

The value-equivalent figures are synthetic consulting estimates for demonstration. They should not be treated as audited financial ROI.

## Phase 3 — Workflow Impact and Bottleneck Analysis

Phase 3 adds a deterministic workflow impact and bottleneck analysis engine that helps a consultant understand why certain workflows are performing well and where adoption is being held back.

Phase 3 provides:

- **Workflow impact status classification** — each workflow is classified as Ready to scale, Positive but monitor, Needs improvement, Needs governance review, or Stop or pause.
- **Training bottleneck detection** — identifies workflows where low training completion rates or poor confidence change signal a training gap.
- **Quality bottleneck detection** — identifies workflows with high quality issue counts or rates per 10 tasks.
- **Risk bottleneck detection** — identifies workflows with logged incidents or near-miss patterns above safe thresholds.
- **Efficiency bottleneck detection** — identifies workflows where the AI-supported process is not yet saving enough time to justify wider rollout.
- **Primary bottleneck identification** — surfaces the highest-priority concern per workflow, in order: Risk > Quality > Training > Efficiency.
- **Organisation-level workflow impact summaries** — groups all bottleneck and status counts by organisation.
- **Build-level workflow impact summaries** — groups outcomes by related build area, including dominant bottleneck per build.
- **Prioritised workflow action list** — ranks all workflows from most urgent (Stop or pause) to least urgent (Ready to scale), with secondary sorting by risk signal count and quality issues.
- **Deterministic action recommendations** — each workflow receives a plain-language consulting recommendation based on its impact status and primary bottleneck.

## Phase 4 — Training, Confidence, and Adoption Readiness Review

Phase 4 adds a deterministic training readiness engine that analyses whether staff are becoming sufficiently trained, confident, and adoption-ready to use AI-supported workflows safely and practically.

Phase 4 provides:

- **Training completion classification** — Low / Moderate / Good / Strong completion bands.
- **Confidence level classification** — Low / Developing / Good / Strong confidence bands for before and after scores.
- **Confidence growth classification** — No growth / Small / Moderate / Strong growth bands.
- **Training readiness scoring** — a composite 0–100 score combining training completion, confidence after, and confidence growth.
- **Staff adoption readiness classification** — Blocked / Needs support / Developing / Adoption ready / Scale ready.
- **Staff group readiness summaries** — groups all adoption readiness and support need counts by staff group.
- **Organisation-level readiness summaries** — groups all training and confidence indicators by organisation.
- **Related-build readiness summaries** — shows how Build 1, Build 4, Build 5, and Build 6 are contributing to training and readiness outcomes.
- **Prioritised training support actions** — ranks workflows from most urgent (Blocked) to least urgent (Scale ready).
- **Deterministic training support recommendations** — Foundation training / Workflow-specific coaching / Confidence reinforcement / Light-touch support / Scale enablement.

## Synthetic data only

All organisations, workflows, review decisions, and adoption metrics are fictional synthetic examples. Do not add real client data, learner data, safeguarding data, HR data, personal data, confidential data, or regulated information.

This build does not use OpenAI, Claude, LangChain, LlamaIndex, cloud deployment, authentication, databases, real file upload, or external APIs.

## Current features

- Synthetic organisation overview for three small organisations.
- Twelve synthetic workflow-level adoption metric records.
- Six synthetic review decision records.
- Minutes-saved, confidence-change, and non-financial summary helpers.
- Validation checks for missing fields, invalid ranges, negative counts, pilot status, and adoption status.
- Workflow-level ROI summaries with hours saved, efficiency gain, and synthetic value-equivalent estimates.
- Organisation-level ROI summaries with totals and averages.
- Portfolio-level ROI summary with adoption value indicator breakdown.
- Time-saving bands (Low / Moderate / High / Very high).
- Confidence improvement bands (No improvement / Small / Moderate / Strong).
- Adoption value indicators (Strong value / Clear value / Emerging value / Low value / Needs review).
- Streamlit app with all eight phases active.
- Workflow impact status classification (Ready to scale / Positive but monitor / Needs improvement / Needs governance review / Stop or pause).
- Training, quality, risk, and efficiency bottleneck detection per workflow.
- Primary bottleneck identification prioritising Risk > Quality > Training > Efficiency.
- Organisation-level and build-level workflow impact summaries.
- Prioritised workflow action list sorted by consulting urgency.
- Deterministic action recommendations for each workflow.
- Training completion, confidence level, confidence growth, and readiness scoring per workflow.
- Staff adoption readiness classification (Blocked / Needs support / Developing / Adoption ready / Scale ready).
- Staff group, organisation-level, and build-level training readiness summaries.
- Prioritised training support actions with deterministic recommendations.
- Quality concern and risk concern classification per workflow (Low / Moderate / High).
- Responsible adoption status (Pause adoption / Requires governance review / Continue with controls / Responsible to continue / Responsible to scale).
- Control need identification (Governance review / Quality assurance checklist / Incident logging review / Training reinforcement / Standard monitoring).
- Scaling permission per workflow (Pause or stop / Do not scale yet / Scale with controls / Scale permitted).
- Organisation-level and build-level risk and quality summaries with concern and scaling counts.
- Prioritised risk and quality action list with deterministic recommendations.
- Pytest coverage for synthetic data, metric helpers, ROI summary engine, workflow impact engine, training readiness engine, risk quality review engine, decision tracker engine, client follow-up report builder, and export centre.

## Phase 5 — Risk, Quality, and Responsible Adoption Review

Phase 5 adds a deterministic risk and quality review engine that checks whether AI-supported workflows are safe enough to continue, pause, or scale.

Phase 5 provides:

- **Quality concern classification** — Low / Moderate / High concern bands based on quality issues logged.
- **Risk concern classification** — Low / Moderate / High concern bands based on risk incidents and near misses.
- **Responsible adoption status** — Pause adoption / Requires governance review / Continue with controls / Responsible to continue / Responsible to scale.
- **Control need identification** — Governance review / Quality assurance checklist / Incident logging review / Training reinforcement / Standard monitoring.
- **Scaling permission** — Pause or stop / Do not scale yet / Scale with controls / Scale permitted.
- **Organisation-level risk and quality summaries** — counts of concerns, governance reviews, and scaling permissions per organisation.
- **Related-build risk and quality summaries** — shows how Build 1, Build 4, Build 5, and Build 6 are performing on quality and risk indicators.
- **Prioritised risk and quality action list** — ranks workflows from most urgent (Pause adoption) to least urgent (Responsible to scale).
- **Deterministic consultant recommendations** — one practical recommendation per workflow based on the primary control need.

## Phase 6 — Decision Tracker and Client Follow-up Evidence

Phase 6 adds a deterministic decision-tracking layer that converts adoption evidence into structured consulting decisions and generates synthetic client follow-up evidence notes.

Phase 6 provides:

- **Decision outcome classification** — Stop / Pause / Continue with controls / Scale / Scale with monitoring / Continue / Review later, based on adoption status, pilot status, training, confidence, quality, and risk signals.
- **Decision confidence classification** — High / Moderate / Low confidence, based on training completion, confidence after training, and pilot status.
- **Decision reason generation** — a deterministic short reason for each decision, following a priority order from stopped adoption to insufficient evidence.
- **Next action generation** — one practical consulting next action per workflow, matched to the decision outcome.
- **Workflow-level decision summaries** — all decision fields combined with adoption evidence fields in a single summary per workflow.
- **Organisation-level decision summaries** — counts of each decision outcome grouped by organisation.
- **Related-build decision summaries** — counts of each decision outcome grouped by Build 1, Build 4, Build 5, and Build 6.
- **Prioritised follow-up decision list** — workflows ranked from most urgent (Stop) to least urgent (Scale), with secondary sort by risk incidents, near misses, and quality issues.
- **Synthetic client follow-up evidence notes** — one deterministic evidence note per workflow, explaining what the evidence supports and what the next step should be.

## Phase 7 — Client Follow-up Report Builder

Phase 7 adds a deterministic Markdown report builder that converts adoption evidence from Phases 1–6 into a structured consultant-facing follow-up report.

Phase 7 provides:

- **Markdown report generation** — a complete structured report covering adoption evidence, ROI, workflow impact, training readiness, risk and quality review, decision outcomes, and recommendations.
- **Portfolio-level report** — a single report summarising all synthetic workflows and organisations.
- **Organisation-level report** — a filtered report for each individual synthetic organisation.
- **Executive summary** — workflow count, hours saved, estimated value equivalent, and decision outcome counts.
- **ROI and value section** — total and average time-saving, efficiency gain, and value-equivalent figures.
- **Workflow impact section** — impact status, primary bottleneck, efficiency gain, and weekly hours saved per workflow.
- **Training readiness section** — training completion, confidence after, readiness band, support need, and adoption readiness per workflow.
- **Risk and quality section** — quality level, risk level, responsible adoption status, control need, and scaling permission per workflow.
- **Decision and follow-up evidence section** — decision outcome, confidence, reason, and next action per workflow, plus follow-up evidence notes.
- **Deterministic recommendations** — consolidated decision, risk/quality, training, and workflow impact recommendations per workflow.
- **Markdown download button** — allows the generated report to be downloaded as a plain Markdown file.

## Phase 8 — Export Centre, Completion Review, and Final Sweep

Phase 8 completes Build 7 by adding an export centre, a completion review, and portfolio documentation.

Phase 8 provides:

- **Markdown export** — the full follow-up report from Phase 7 as a downloadable Markdown file.
- **CSV export** — a flat evidence table combining ROI, workflow impact, training, risk, and decision fields for all workflows.
- **JSON export** — a machine-readable evidence pack with all analytical fields per workflow.
- **PDF export** — a basic PDF version of the Markdown report generated using reportlab.
- **PNG chart export** — a simple bar chart of decision outcome counts generated using matplotlib.
- **Completion summary** — headline figures from all phases in a single overview.
- **Completion review** — a structured Markdown review of what Build 7 does, what was completed, limitations, and recommended future extensions.
- **Portfolio summary** — a portfolio-ready summary covering the problem, target users, key features, consulting use cases, and commercial demonstration value.

## Build 7 Completion Status

Build 7 is complete and portfolio-ready. It includes:

1. Synthetic adoption metrics (Phase 1)
2. ROI summary engine (Phase 2)
3. Workflow impact and bottleneck analysis (Phase 3)
4. Training, confidence, and adoption readiness review (Phase 4)
5. Risk, quality, and responsible adoption review (Phase 5)
6. Decision tracker and client follow-up evidence (Phase 6)
7. Client follow-up report builder (Phase 7)
8. Export centre and completion review (Phase 8)

## How to run the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How to run tests

```bash
pytest
```
