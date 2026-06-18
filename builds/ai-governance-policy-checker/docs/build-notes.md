# Build Notes — AI Governance Policy Checker

**Build 6 · BrightPath ChatGPT Mastery Project**

---

## Phase 8: Completion Review and Portfolio Notes

### What Was Added

#### Completion Review (`src/completion_review.py`)

- `get_build6_phase_checklist()` — returns all 8 Build 6 phases with name, purpose, status, and evidence
- `get_expected_build6_outputs()` — returns 28 expected session state outputs across all phases (Required / Recommended / Advisory)
- `check_session_state_outputs()` — inspects session state, returns available count, missing count, completion percentage, required missing list, and recommended next actions
- `check_documentation_files()` — checks 11 expected documentation files under base_path; returns existing, missing, and completion percentage
- `generate_completion_score()` — derives overall status (Complete / Mostly complete / In progress), phase/output/documentation percentages, final readiness label, and recommended final actions
- `generate_build6_completion_review()` — assembles the full completion review dict including portfolio value, commercial value, technical value, responsible-use position, prototype note, and human review note
- `generate_portfolio_summary()` — returns portfolio summary with one-line summary, problem solved, target users, core workflow, key features, technical stack, responsible AI features, portfolio positioning, and what-this-demonstrates list
- `generate_case_study_summary()` — returns BrightPath case study with client context, challenge, solution, outputs generated, consulting value, responsible-use controls, limitations, and next-step recommendation
- `format_completion_review_as_markdown()` — full Markdown document with 12 sections
- `format_portfolio_notes_as_markdown()` — portfolio notes document with LinkedIn/GitHub description, case study, and demo instructions

#### Completion Review Page (`app.py`)

- Replaces the Phase 8 placeholder
- Generates completion review from session state (works with partial or no prior outputs)
- Displays phase completion checklist (8 phases, ✅/❌)
- Displays output completion metrics and list (28 outputs, available vs missing)
- Displays documentation checklist (11 docs, present vs missing)
- Shows portfolio value, commercial value, technical value, and responsible-use position
- Shows recommended final actions
- Download button: Completion Review Markdown
- Download button: Portfolio Notes Markdown

#### Documentation Added

- `docs/completion-review.md` — final build overview, phases, outputs, tests, safety boundaries, final review checklist
- `docs/portfolio-notes.md` — one-line summary, problem, target users, workflow, features, stack, responsible AI features, case study, LinkedIn/GitHub description
- `docs/testing-checklist.md` — full manual testing checklist across all 10 pages plus responsible-use and error-handling checks
- `docs/case-study-summary.md` — BrightPath Skills Training synthetic case study with client context, challenge, solution, outputs, consulting value, limitations, next steps

#### Tests Added

- `tests/test_completion_review.py` — 78 tests across 10 test classes

### Test Count

Cumulative test count after Phase 8: **783 tests** (78 new tests added in Phase 8)

---

## Phase 7: Export Centre with PDF/Charts

### What Was Added

#### Export Centre (`src/export_centre.py`)

- `get_export_formats()` — returns `["Markdown", "PDF"]`
- `check_export_readiness()` — inspects session state, returns readiness dict with `is_ready`, `can_export_markdown`, `can_export_pdf`, `available_outputs`, `missing_outputs`, `recommended_next_steps`
- `build_export_data_from_session_state()` — assembles all available Build 6 outputs into a single export data dict; missing outputs are `None`
- `generate_export_quality_checklist()` — 12-item checklist (Required / Recommended / Advisory) checking policy pack, framework, coverage, gaps, recommendations, maturity, report, responsible-use boundaries, prototype limitations, human review note, and export availability
- `summarise_export_package()` — surface-level summary for metric display
- `create_export_filename_base()` — safe, lowercased, date-stamped filename base
- `prepare_markdown_export()` — returns `(markdown_text, filename)`
- `prepare_pdf_export()` — delegates to `pdf_exporter`; returns `(pdf_bytes, filename)`
- `prepare_all_exports()` — prepares both formats; errors are captured per-format, not raised globally

#### Report Analytics (`src/report_analytics.py`)

- `calculate_export_completion_status()` — which of the 7 logical outputs are present
- `calculate_coverage_level_counts()` — Strong/Partial/Weak/Not covered from coverage summary
- `calculate_gap_severity_counts()` — Critical/High/Medium/Low from gap summary
- `calculate_recommendation_priority_counts()` — Urgent/High/Medium/Low from recommendation summary
- `calculate_maturity_level_counts()` — Initial/Developing/Defined/Managed/Optimised from maturity summary
- `calculate_governance_score_breakdown()` — overall scores and domain-level maturity scores
- `calculate_report_quality_summary()` — checks for 10 sections in the generated Markdown
- `build_governance_report_analytics()` — assembles all analytics into one dict

#### Chart Utilities (`src/chart_utils.py`)

- Uses `matplotlib` with `Agg` backend only (no seaborn, no display)
- Charts: completion status (horizontal bar), coverage levels, gap severities, recommendation priorities, maturity levels (all vertical bar), governance scores by domain (horizontal bar)
- `generate_all_export_charts()` — generates all charts into `outputs/charts/`; graceful failure per chart
- Professional style: navy/teal/amber colour scheme, clean spines, readable labels
- Falls back to overall scores if domain scores are not available

#### PDF Exporter (`src/pdf_exporter.py`) — Replaced stub

- `export_governance_report_to_pdf_bytes()` — full professional PDF using reportlab
- Cover page with organisation, date, subtitle, prototype note
- Analytics summary tables (completion status, coverage levels, gap severities, recommendation priorities, governance scores)
- Charts section with embedded PNG images (if generated)
- Full report content parsed from Markdown: headings, bullets, numbered lists, blockquotes, body text, Markdown tables → reportlab `Table` objects
- Responsible-use section on final page
- Handles missing analytics, missing chart paths, partial Markdown, and empty export data gracefully
- Navy headings, teal rule lines, light grey table alternating rows

#### Export Centre Page (`app.py`)

- Replaces the Phase 7 placeholder
- Setup guidance if policy pack or report is missing (no crash)
- Readiness checklist: 7 logical outputs with ✅/❌
- Missing output guidance in expander
- Package summary metrics: organisation, domains, gaps, recommendations, maturity level, governance score
- Export quality checklist: Required/Recommended/Advisory split into columns
- Analytics inline display: coverage levels, gap severities, recommendation priorities, governance scores
- Chart previews displayed in a 2-column grid using `st.image()`
- Markdown download button
- PDF download button (PDF generated on-page with a spinner)
- Responsible-use caption

### Tests Added

- `tests/test_export_centre.py` — 62 tests across 8 test classes
- `tests/test_report_analytics.py` — 47 tests across 9 test classes
- `tests/test_chart_utils.py` — 31 tests across 7 test classes
- `tests/test_pdf_exporter.py` — 32 tests across 4 test classes

**Cumulative total: 705 tests passing**

---

## Phase 1: Scaffold and Synthetic Policy Data Setup

### What Was Created

#### Streamlit App Scaffold (`app.py`)

- Wide layout Streamlit app with dark navy (`#1a2744`) sidebar
- 9-page navigation: Home, Policy Library, Governance Framework, Policy Checker, Gap Analysis, Recommendations, Governance Report, Export Centre, Completion Review
- Navigation order follows the governance review consulting workflow
- Session state used as the shared data bus across pages
- Sidebar completion badges for each workflow step
- Home page: project overview, workflow diagram, connections to Builds 1–5, responsible-use boundaries
- Policy Library page: functional — loads synthetic policy pack, validates, stores in session state, displays with expanders and metric row
- Governance Framework page: functional — loads governance framework, stores in session state, displays 12 domains with expanders
- All remaining pages: clean placeholders with purpose explanation and required prior step

#### Synthetic Policy Pack (`src/sample_policies.py`)

Six synthetic policies for BrightPath Skills Training:

| Policy ID | Title | Type | Owner |
|---|---|---|---|
| POL-001 | AI Acceptable Use Policy | Acceptable Use | Chief Executive Officer |
| POL-002 | Data Protection and AI Use Guidance | Data Protection | Data Protection Lead |
| POL-003 | Safeguarding and AI Boundary Policy | Safeguarding | Designated Safeguarding Lead |
| POL-004 | Staff AI Tool Use Procedure | Procedure | Head of Operations |
| POL-005 | AI Output Review Checklist | Checklist | Quality and Standards Lead |
| POL-006 | AI Incident and Escalation Procedure | Incident Procedure | Head of Operations |

Functions:
- `get_brightpath_policy_pack()` — full policy pack
- `get_demo_policy_list()` — list of 6 policies
- `get_ai_acceptable_use_policy()` through `get_ai_incident_escalation_procedure()` — individual policies
- `get_default_policy_types()` — 10 standard policy types
- `get_default_risk_areas()` — 16 standard risk areas

Each policy includes: `policy_id`, `policy_title`, `policy_type`, `owner`, `version`, `status`, `last_reviewed`, `summary`, `policy_text`, `related_risk_areas`.

All policy text is synthetic and does not include real law, real organisations, real names, real cases, or real data.

#### Responsible AI Governance Framework (`src/governance_framework.py`)

12 governance domains:

| Domain ID | Domain Name | Priority |
|---|---|---|
| GOV-001 | Strategy and Ownership | High |
| GOV-002 | Approved AI Tools | High |
| GOV-003 | Prohibited AI Uses | Medium |
| GOV-004 | Data Protection and Confidentiality | High |
| GOV-005 | Learner and Client Data Boundaries | High |
| GOV-006 | Safeguarding Boundaries | High |
| GOV-007 | Human Review and Accountability | High |
| GOV-008 | Accuracy and Hallucination Control | Medium |
| GOV-009 | Bias, Fairness, and Inclusion | Medium |
| GOV-010 | Staff Training and Capability | Medium |
| GOV-011 | Escalation and Incident Reporting | High |
| GOV-012 | Monitoring, Review, and Continuous Improvement | Medium |

High-priority domains: 7 (GOV-001, 002, 004, 005, 006, 007, 011)

Functions:
- `get_responsible_ai_governance_framework()` — full list of 12 domain dicts
- `get_framework_domain_ids()` — list of domain IDs
- `get_framework_domain_names()` — list of domain names
- `get_high_priority_domains()` — filtered list of High priority domains
- `summarise_governance_framework()` — summary statistics dict
- `format_governance_framework_as_markdown()` — Markdown string with all domains

#### Policy Data Manager (`src/policy_data_manager.py`)

Functions:
- `validate_policy_pack()` — checks required top-level fields and each policy's required fields; returns `(bool, str)` tuple
- `summarise_policy_pack()` — returns statistics including total_policies, policy_types, risk_areas, owners, synthetic_demo_only flag
- `format_policy_pack_as_markdown()` — returns full Markdown including Organisation, Policy Pack Summary, Policies, and Responsible-Use Boundaries sections
- `get_policy_by_id()` — returns policy dict or None
- `search_policies_by_risk_area()` — case-insensitive substring search across related_risk_areas
- `extract_policy_titles()` — returns list of policy title strings

#### UI Components (`src/ui_components.py`)

Reusable helpers:
- `apply_global_styles()` — dark navy sidebar, info card styles
- `render_page_header()` — title + optional subtitle + divider
- `render_responsible_use_warning()` — `st.warning` with full responsible-use text
- `render_prototype_notice()` — `st.info` with prototype status text
- `render_info_card()` — HTML card with navy left border
- `render_status_box()` — dispatches to st.info/warning/success/error
- `render_metric_row()` — creates equal-width columns with `st.metric`
- `render_completion_badge()` — ✅ or ⬜ + label in sidebar
- `render_workflow_steps()` — numbered step list with current step highlighted

#### Utilities (`src/utils.py`)

- `safe_get()` — safe dict access with default
- `safe_list()` — coerces None/scalar to list
- `clean_text()` — strips and stringifies
- `create_safe_filename()` — regex-based filename sanitiser
- `get_current_date_label()` — returns today's ISO date string

#### Stub Modules

- `src/policy_checker.py` — `check_policy_coverage_placeholder()` returns status dict
- `src/gap_analysis.py` — `generate_gap_analysis_placeholder()` returns status dict
- `src/recommendation_engine.py` — `generate_recommendations_placeholder()` returns status dict
- `src/report_builder.py` — `generate_governance_report_placeholder()` returns Markdown string
- `src/pdf_exporter.py` — `create_safe_pdf_filename()` returns safe `.pdf` filename

#### Safety Boundaries

- All policy text is synthetic/demo only
- No real client policies, learner data, safeguarding case data, staff HR data, personal data, confidential data, or regulated information
- No external LLM or AI API calls
- Responsible-use warning rendered on every page

#### Tests

| File | Classes | Tests |
|---|---|---|
| `tests/test_sample_policies.py` | 5 | 18 |
| `tests/test_governance_framework.py` | 6 | 22 |
| `tests/test_policy_data_manager.py` | 6 | 29 |

Total Phase 1 tests: **69**

---

## Phase 2: Governance Framework Coverage Checker

The Policy Checker page now compares synthetic policy text against all 12 responsible AI governance domains using deterministic keyword-based evidence matching.

### What Was Created

#### `src/policy_checker.py` (full implementation)

Functions:

| Function | Purpose |
|---|---|
| `normalise_text(text)` | Lowercase, strip, collapse whitespace |
| `count_keyword_matches(text, keywords)` | Count total keyword occurrences in text |
| `extract_matching_policy_snippets(policy_text, keywords, max_snippets)` | Return up to N matching lines as snippets |
| `get_domain_keyword_map()` | Return keyword list per governance domain name |
| `check_domain_coverage(domain, policies)` | Run keyword check for one domain across all policies |
| `check_policy_pack_coverage(policy_pack, framework)` | Run coverage check across all domains |
| `calculate_coverage_score(domain_results)` | Average domain scores to overall score |
| `classify_coverage_level(coverage_score)` | Score → "Not covered / Weak / Partial / Strong coverage" |
| `summarise_policy_coverage(coverage_results)` | Summary stats, gaps, best/weakest, focus areas |
| `format_policy_coverage_as_markdown(coverage_results, summary)` | Full Markdown coverage report |

**Coverage scoring logic:**
- 0 matches → score 0 → Not covered (0–24)
- 1–2 matches → score 25–49 → Weak coverage
- 3–6 matches → score 50–74 → Partial coverage
- 7+ matches → score 72–100 → Strong coverage
- Policy breadth bonus: more policies contributing → higher score
- All scores clamped to 0–100

**Keyword map:** 12 keys matching governance domain names exactly. Keywords cover approved tools, prohibited uses, data protection, learner/client boundaries, safeguarding, human review, accuracy/hallucination, bias/fairness, training, incidents, and monitoring.

#### Policy Checker page in `app.py`

- Checks prerequisites: policy pack and governance framework must be loaded
- Shows clear setup instructions if either is missing
- "Run Policy Coverage Check" button triggers coverage generation and caches in session state
- Displays: overall score (with progress bar), coverage level, counts (strong/partial/weak/not covered), high-priority gaps, recommended focus areas, best/weakest domains side by side, domain expander table with scores, matched policies, matched keywords, evidence snippets, coverage explanation, Markdown download

#### Session state keys added (Phase 2)

| Key | Content |
|---|---|
| `coverage_results` | Full coverage results dict (all domain results, overall score, categorised lists) |
| `coverage_summary` | Summary statistics dict (counts, gaps, best/weakest, focus areas) |
| `coverage_markdown` | Markdown string of full coverage review |

#### Tests — `tests/test_policy_checker.py`

| Class | Tests |
|---|---|
| `TestNormaliseText` | 6 |
| `TestCountKeywordMatches` | 7 |
| `TestExtractMatchingPolicySnippets` | 7 |
| `TestGetDomainKeywordMap` | 5 |
| `TestClassifyCoverageLevel` | 8 |
| `TestCalculateCoverageScore` | 4 |
| `TestCheckDomainCoverage` | 12 |
| `TestCheckPolicyPackCoverage` | 11 |
| `TestSummarisePolicyCoverage` | 13 |
| `TestFormatPolicyCoverageAsMarkdown` | 9 |

Total Phase 2 tests: **82** (cumulative total: **159**)

---

## Phase 3: Policy Gap Analysis

The Gap Analysis page now identifies missing, weak, and partially covered governance domains from the coverage review. It classifies gap severity, calculates priority scores, explains missing evidence, describes the risk created by each gap, and provides action hints.

### What Was Created

#### `src/gap_analysis.py` (full implementation)

Functions:

| Function | Purpose |
|---|---|
| `classify_gap_severity(coverage_level, priority_level)` | Map coverage level + domain priority to Critical / High / Medium / Low / No significant gap |
| `calculate_gap_priority_score(coverage_score, priority_level)` | Integer urgency score 0–100 based on gap size and domain priority |
| `generate_gap_id(index)` | Format GAP-001, GAP-002, etc. |
| `identify_gap_type(domain_result)` | Missing / Weak / Partial / Covered sufficiently / Unknown |
| `generate_gap_risk_statement(domain_result)` | Deterministic consulting-style risk statement per domain |
| `generate_missing_evidence_statement(domain_result)` | What evidence the policy pack is missing |
| `generate_gap_action_hint(domain_result)` | Short first-step guidance for resolving the gap |
| `generate_domain_gap(domain_result, index)` | Full structured gap dict for one domain |
| `generate_policy_gap_analysis(coverage_results)` | Full gap analysis across all domains |
| `summarise_gap_analysis(gap_analysis)` | Summary stats, counts, gap position, focus areas |
| `prioritise_gaps(gaps)` | Sort gaps by priority score descending |
| `format_gap_analysis_as_markdown(gap_analysis, summary)` | Full Markdown gap analysis report |

**Gap severity logic:**

| Coverage Level | High Priority | Medium Priority | Low Priority |
|---|---|---|---|
| Not covered | Critical gap | High gap | Medium gap |
| Weak coverage | High gap | Medium gap | Low gap |
| Partial coverage | Medium gap | Low gap | Low gap |
| Strong coverage | No significant gap | No significant gap | No significant gap |

**Priority score logic:**
- Start with `100 - coverage_score`
- Add: High priority +20, Medium priority +10, Low priority +0
- Clamp to 0–100

**Output structure per gap:**
`gap_id`, `domain_id`, `domain_name`, `priority_level`, `coverage_score`, `coverage_level`, `gap_type`, `gap_severity`, `gap_priority_score`, `matched_policies`, `matched_keywords`, `evidence_snippets`, `expected_policy_evidence`, `missing_evidence`, `risk_statement`, `action_hint`, `review_note`

#### Gap Analysis page in `app.py`

- Auto-runs gap analysis when coverage_results is present in session state
- Shows setup instructions if coverage_results is missing
- Displays: summary metrics (total/critical/high/medium/low/covered), overall gap position (error/warning/success), highest priority gap, recommended focus areas, gap themes, prioritised gap table with expanders (missing evidence, risk statement, action hint, evidence snippets), covered domains list, Markdown download
- Stores: `gap_analysis`, `gap_summary`, `gap_analysis_markdown` in session state

#### Session state keys added (Phase 3)

| Key | Content |
|---|---|
| `gap_analysis` | Full gap analysis dict (all gaps by severity, covered domains, themes, focus areas) |
| `gap_summary` | Summary statistics dict (counts, gap position, top gaps, recommended focus) |
| `gap_analysis_markdown` | Markdown string of full gap analysis report |

#### Tests — `tests/test_gap_analysis.py`

| Class | Tests |
|---|---|
| `TestClassifyGapSeverity` | 10 |
| `TestCalculateGapPriorityScore` | 6 |
| `TestGenerateGapId` | 3 |
| `TestIdentifyGapType` | 6 |
| `TestGenerateGapRiskStatement` | 7 |
| `TestGenerateMissingEvidenceStatement` | 4 |
| `TestGenerateGapActionHint` | 6 |
| `TestGenerateDomainGap` | 8 |
| `TestGeneratePolicyGapAnalysis` | 10 |
| `TestSummariseGapAnalysis` | 10 |
| `TestPrioritiseGaps` | 5 |
| `TestFormatGapAnalysisAsMarkdown` | 9 |

Total Phase 3 tests: **84** (cumulative total: **243**)

---

## Phase 4: Policy Improvement Recommendation Engine

The Recommendations page now converts policy gaps into practical improvement recommendations. It prioritises recommendations, suggests target policies and owners, provides wording directions, implementation steps, review questions, success criteria, quick wins, and recommended sequencing.

### What Was Created

#### `src/recommendation_engine.py` (full implementation)

Functions:

| Function | Purpose |
|---|---|
| `generate_recommendation_id(index)` | Format REC-001, REC-002, etc. |
| `classify_recommendation_priority(gap_severity, gap_priority_score)` | Urgent / High priority / Medium priority / Low priority (takes higher of severity or score) |
| `suggest_policy_action_type(gap)` | Create / Strengthen / Add checklist / Add escalation / Add training / Add monitoring / Review and clarify |
| `suggest_policy_owner(gap)` | Domain-matched suggested owner role |
| `suggest_target_policy(gap, policy_pack)` | Suggested target policy title (matched from policy pack if available) |
| `generate_recommendation_rationale(gap)` | Consulting-style rationale using gap risk statement + severity framing |
| `generate_policy_wording_direction(gap)` | Domain-matched suggested wording direction (prefixed "Suggested wording direction:") |
| `generate_implementation_steps(gap)` | 4–7 practical steps; adds pre-rollout note for Urgent/High |
| `generate_review_questions(gap)` | 7+ review questions including domain-specific additions |
| `generate_success_criteria(gap)` | 7+ measurable criteria including domain-specific additions |
| `generate_recommendation_from_gap(gap, index, policy_pack)` | Full 18-key recommendation dict |
| `generate_policy_recommendations(gap_analysis, policy_pack, coverage_results)` | Full recommendation package: priority groups, quick wins, themes, owner summary, sequence |
| `summarise_policy_recommendations(recommendations)` | Summary stats, position statement, top themes, top owners, focus areas |
| `prioritise_recommendations(recommendation_items)` | Sort by priority then gap_priority_score descending |
| `format_policy_recommendations_as_markdown(recommendations, summary)` | Full Markdown report |

**Priority classification logic:**
- Critical gap OR score ≥ 85 → Urgent
- High gap OR score ≥ 70 → High priority
- Medium gap OR score ≥ 45 → Medium priority
- Low gap OR score < 45 → Low priority
- Takes the higher priority of severity-based and score-based results

**Recommended sequence grouping:**
1. Immediate policy controls (Urgent + High recommendations)
2. Clarify operational procedures (Medium recommendations, non-training)
3. Staff communication and training (training/capability domain recommendations)
4. Monitoring and review (monitoring/improvement domain recommendations)

#### Recommendations page in `app.py`

- Auto-generates recommendations when gap_analysis is present in session state
- Shows setup instructions (5-step) if gap_analysis is missing
- Uses policy_pack from session state if available for better target policy matching
- Displays: summary metrics, overall recommendation position banner, highest priority recommendation, recommended focus areas, recommended sequence (expanders), quick wins, policy update themes, owner summary, prioritised recommendation table with full expanders (rationale, wording direction, implementation steps, review Q&A in nested expander), Markdown download
- Stores: `policy_recommendations`, `recommendation_summary`, `policy_recommendations_markdown` in session state

#### Session state keys added (Phase 4)

| Key | Content |
|---|---|
| `policy_recommendations` | Full recommendation package dict |
| `recommendation_summary` | Summary statistics dict |
| `policy_recommendations_markdown` | Markdown string of full recommendations report |

#### Tests — `tests/test_recommendation_engine.py`

| Class | Tests |
|---|---|
| `TestGenerateRecommendationId` | 3 |
| `TestClassifyRecommendationPriority` | 9 |
| `TestSuggestPolicyActionType` | 7 |
| `TestSuggestPolicyOwner` | 5 |
| `TestSuggestTargetPolicy` | 6 |
| `TestGenerateRecommendationRationale` | 5 |
| `TestGeneratePolicyWordingDirection` | 5 |
| `TestGenerateImplementationSteps` | 6 |
| `TestGenerateReviewQuestions` | 4 |
| `TestGenerateSuccessCriteria` | 4 |
| `TestGenerateRecommendationFromGap` | 10 |
| `TestGeneratePolicyRecommendations` | 11 |
| `TestSummarisePolicyRecommendations` | 8 |
| `TestPrioritiseRecommendations` | 6 |
| `TestFormatPolicyRecommendationsAsMarkdown` | 10 |

Total Phase 4 tests: **99** (cumulative total: **342**)

---

## Phase 5: Governance Score and Maturity Summary

The Governance Maturity page calculates an overall AI governance maturity score from policy
coverage results, gap analysis, and policy recommendations. It produces domain-level maturity
scores, strengths, weaknesses, blockers, improvement priorities, and adoption-readiness guidance.

### Functions Implemented (`src/governance_maturity.py`)

| Function | Purpose |
|---|---|
| `classify_governance_maturity_level` | Maps 0–100 score to Initial / Developing / Defined / Managed / Optimised |
| `get_maturity_level_description` | Returns the consulting description for a maturity level |
| `get_maturity_level_colour` | Returns a colour label (red/orange/blue/green) for UI display |
| `calculate_domain_maturity_score` | Calculates maturity score per domain; applies gap and recommendation penalties |
| `calculate_overall_governance_score` | Weighted average across all domain maturity scores |
| `identify_maturity_strengths` | Returns domains at or above a score threshold |
| `identify_maturity_weaknesses` | Returns domains below a score threshold |
| `identify_maturity_blockers` | Identifies critical/high gaps and urgent/high-priority recommendations as blockers |
| `generate_maturity_improvement_priorities` | Derives ordered improvement priorities from blockers and weaknesses |
| `generate_adoption_readiness_position` | Generates practical adoption-readiness consulting guidance |
| `generate_governance_maturity_summary` | Full maturity summary: scores, strengths, weaknesses, blockers, priorities, readiness |
| `summarise_governance_maturity` | Summary statistics: counts, position statement, recommended focus |
| `format_governance_maturity_as_markdown` | Full Markdown report with all sections and responsible-use footer |

### Maturity Level Thresholds

| Score | Maturity Level |
|---|---|
| 0–24 | Initial governance |
| 25–49 | Developing governance |
| 50–74 | Defined governance |
| 75–89 | Managed governance |
| 90–100 | Optimised governance |

### Penalty Logic

| Penalty Source | Penalty Applied |
|---|---|
| Critical gap | -25 |
| High gap | -15 |
| Medium gap | -8 |
| Low gap | -3 |
| Urgent recommendation | -15 |
| High priority recommendation | -10 |
| Medium priority recommendation | -5 |
| Low priority recommendation | -2 |
| High-priority domain, coverage < 50 | -10 extra |

### Session State Keys Added (Phase 5)

| Key | Content |
|---|---|
| `governance_maturity` | Full maturity summary dict |
| `governance_maturity_summary` | Summary statistics dict |
| `governance_maturity_markdown` | Markdown string for download |

### App Page Added

`page_governance_maturity()` in `app.py`:

- Checks for `coverage_results` in session state; shows setup instructions if missing
- Optionally uses `gap_analysis` and `policy_recommendations` for richer scoring
- Generates maturity summary automatically on first load; stores in session state
- Displays: 2 metric rows, maturity level banner, adoption-readiness position, recommended next step,
  strengths/weaknesses side by side, maturity blockers with expanders, improvement priorities,
  domain maturity table sorted by score ascending, responsible-use caption, Markdown download

### Tests (`tests/test_governance_maturity.py`)

| Class | Tests |
|---|---|
| `TestClassifyGovernanceMaturityLevel` | 10 |
| `TestGetMaturityLevelDescription` | 6 |
| `TestGetMaturityLevelColour` | 4 |
| `TestCalculateDomainMaturityScore` | 9 |
| `TestCalculateOverallGovernanceScore` | 5 |
| `TestIdentifyMaturityStrengths` | 4 |
| `TestIdentifyMaturityWeaknesses` | 4 |
| `TestIdentifyMaturityBlockers` | 6 |
| `TestGenerateMaturityImprovementPriorities` | 4 |
| `TestGenerateAdoptionReadinessPosition` | 5 |
| `TestGenerateGovernanceMaturitySummary` | 10 |
| `TestSummariseGovernanceMaturity` | 5 |
| `TestFormatGovernanceMaturityAsMarkdown` | 15 |

Total Phase 5 tests: **87** (cumulative total: **429**)

---

## Phase 6: Governance Report Builder

The Governance Report page now assembles all generated Build 6 outputs into a complete
client-facing AI governance policy review report. It includes a readiness check, section
selection, missing-output guidance, Markdown export, responsible-use boundaries, prototype
limitations, and appendices.

### Functions Implemented (`src/report_builder.py`)

| Function | Purpose |
|---|---|
| `get_governance_report_required_sections` | List of required section keys (minimum: policy_pack) |
| `get_governance_report_optional_sections` | All available report section keys |
| `check_governance_report_readiness` | Inspects session state; returns available, missing, next steps |
| `build_governance_report_data_from_session_state` | Builds full report data dict from all session state outputs |
| `generate_report_cover_section` | Markdown cover page with org name, date, prototype status |
| `generate_report_table_of_contents` | Numbered section TOC |
| `generate_report_executive_summary_section` | Deterministic executive summary from all available outputs |
| `generate_report_policy_pack_section` | Policy pack overview with policy table and risk areas |
| `generate_report_framework_section` | Governance framework summary with domain table |
| `generate_report_coverage_section` | Coverage review with score, counts, and domain table |
| `generate_report_gap_analysis_section` | Gap analysis with counts, themes, and prioritised table |
| `generate_report_recommendations_section` | Recommendations with quick wins and prioritised table |
| `generate_report_maturity_section` | Maturity summary with score, level, strengths, weaknesses |
| `generate_report_next_steps_section` | Up to 8 practical next steps from available outputs |
| `generate_report_appendices_section` | Policy list, domain list, all tables, source outputs checklist |
| `generate_report_responsible_use_section` | Responsible-use boundaries text |
| `generate_report_prototype_limitations_section` | Prototype limitations text |
| `generate_markdown_governance_report` | Assembles full Markdown report from all sections |
| `summarise_governance_report` | Summary statistics: sections, domains, gaps, recs, maturity |
| `create_governance_report_filename` | Safe snake-case `.md` filename |

### Report Sections (11 sections)

| Section | Key |
|---|---|
| Executive Summary | executive_summary |
| Policy Pack Overview | policy_pack |
| Responsible AI Governance Framework | governance_framework |
| Policy Coverage Review | coverage_review |
| Policy Gap Analysis | gap_analysis |
| Policy Improvement Recommendations | recommendations |
| Governance Score and Maturity Summary | maturity_summary |
| Recommended Next Steps | next_steps |
| Responsible-Use Boundaries | responsible_use |
| Prototype Limitations | prototype_limitations |
| Appendices | appendices |

### Session State Keys Added (Phase 6)

| Key | Content |
|---|---|
| `governance_report_data` | Full assembled report data dict |
| `governance_report_markdown` | Full Markdown report string |
| `governance_report_filename` | Safe `.md` filename |
| `governance_report_readiness` | Readiness check dict |
| `governance_report_summary` | Summary statistics dict |

### App Page Updated

`page_governance_report()` in `app.py`:

- Checks for `policy_pack` in session state; shows setup instructions if missing
- Checks readiness for all 10 recommended outputs; shows available and missing
- Shows recommended steps to complete partial reports
- Section selection with checkboxes — preselected based on data availability
- Generates report on button click; stores all report outputs in session state
- Displays: summary metric cards, readiness position, Markdown preview (truncated to 8000 chars), download button

### Tests (`tests/test_report_builder.py`)

| Class | Tests |
|---|---|
| `TestGetGovernanceReportRequiredSections` | 2 |
| `TestGetGovernanceReportOptionalSections` | 3 |
| `TestCheckGovernanceReportReadiness` | 7 |
| `TestBuildGovernanceReportDataFromSessionState` | 6 |
| `TestGenerateReportCoverSection` | 5 |
| `TestGenerateReportTableOfContents` | 4 |
| `TestGenerateReportExecutiveSummarySections` | 5 |
| `TestGenerateReportPolicyPackSection` | 4 |
| `TestGenerateReportFrameworkSection` | 4 |
| `TestGenerateReportCoverageSection` | 4 |
| `TestGenerateReportGapAnalysisSection` | 4 |
| `TestGenerateReportRecommendationsSection` | 4 |
| `TestGenerateReportMaturitySection` | 4 |
| `TestGenerateReportNextStepsSection` | 4 |
| `TestGenerateReportAppendicesSection` | 6 |
| `TestGenerateReportResponsibleUseSection` | 4 |
| `TestGenerateReportPrototypeLimitationsSection` | 4 |
| `TestGenerateMarkdownGovernanceReport` | 15 |
| `TestSummariseGovernanceReport` | 9 |
| `TestCreateGovernanceReportFilename` | 6 |

Total Phase 6 tests: **104** (cumulative total: **533**)

---

*Build 6 · AI Governance Policy Checker · BrightPath ChatGPT Mastery Project*
