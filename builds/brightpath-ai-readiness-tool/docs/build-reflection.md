# Build Reflection

## What Was Built

A seven-phase Streamlit prototype that takes a consultant and a client through a structured AI readiness diagnostic — from organisation profile to downloadable Markdown report. Seven pages, five scoring systems, six recommendation categories, ten safeguard definitions, and a 9-section report generator. Built in Python with two dependencies: Streamlit and Pandas.

---

## Why It Was Built

The ChatGPT Mastery project needed a proof point — evidence that the methodology developed across Layers 3 to 7 actually works as a real-world client deliverable, not just as documentation.

Building this tool also addressed a practical need: a consultant without a structured diagnostic tool relies on experience and instinct to run a readiness session. That works once. It does not scale, it is not repeatable, and it does not leave the client with anything to act on. This tool changes that.

---

## What Worked Well

**Modular architecture.** Keeping scoring logic in `scoring.py`, sample data in `sample_data.py`, and report generation in `report_generator.py` made each phase feel independent. Adding Phase 4 did not require touching Phase 2 code. Testing one function did not require running the full app.

**The `st.session_state` pattern.** Using keyed widgets throughout meant that the sample loader buttons worked cleanly — set the keys, call `st.rerun()`, and every widget on the page re-renders with the new values. Once this pattern was understood, it was applied consistently across Phases 3, 4, 5, and 6.

**Synthetic sample data.** Having a realistic BrightPath scenario that consistently scores 35/100 readiness, 42/50 workflow, and generates a "Governance-first before pilot" recommendation made every page demonstrable from day one.

**Safety-first language.** Writing responsible-use notices, data safety reminders, and placeholder text that modelled safe use from Phase 1 meant the tool never felt like a compliance add-on. It looked like it was designed that way.

**Phase-by-phase scope control.** Each phase had a clear deliverable and a review checklist. This prevented scope creep and made the build log accurate.

---

## What Was Difficult

**Widget-after-instantiation errors.** Streamlit raises an error if you set `st.session_state[key]` after a widget with that key has already been rendered in the same script run. The fix — putting the load-sample button above all keyed widgets and calling `st.rerun()` — was not obvious from the docs and required reading the error carefully.

**Separator characters in Edit operations.** Some comment separators in `app.py` used Unicode box-drawing characters (`──`). When trying to edit those lines, the Edit tool failed because the literal bytes had to be matched exactly. Reading the file first and copying the exact string was the fix.

**Recommendation ordering.** The pilot recommendation function has six categories and checks six conditions. Getting the order right — critical risk first, then high risk, then low readiness, then low workflow score, then positive conditions in descending strength — required careful thought and test cases to verify.

**Initialising form defaults from session state.** For the Mini Report page, form fields needed sensible default values computed from previous pages, but could not override values the user had already entered or the sample loader had set. Using Streamlit's `value=` parameter (which is only used when the key is not yet in session state) solved this cleanly — but it took time to understand the behaviour.

---

## Design Decisions

**No database, no API, no authentication.** The prototype needed to be demonstrable without infrastructure. A consultant should be able to run this on a laptop in a client's office with no internet connection.

**Separate scoring module.** Putting all logic in `scoring.py` rather than inline in `app.py` was the right call from Phase 1. It made the code testable without Streamlit's rendering context.

**Universal safeguards for the pilot recommendation.** Rather than generating recommendation-specific safeguards (which would have been complex and potentially misleading), the ten universal safeguards were applied across all recommendation categories. The recommendation-specific variation comes from the next actions list instead.

**Markdown rather than plain text for the report.** Markdown is human-readable as raw text, renders well in any browser or note-taking app, and is close enough to plain text to paste into a Word document. It was a better choice than HTML for a tool aimed at non-technical managers.

**Synthetic data over form-based profile input.** The Organisation Profile page is read-only in this version. Getting the form input working would have been straightforward, but the effort was better spent on the scoring and recommendation pages. The profile is pre-loaded from sample data for demonstration purposes.

---

## Safety and Governance Decisions

**Safeguarding as a risk category.** Including safeguarding as an explicit risk category (not just "data sensitivity") was important. In UK training provider contexts, safeguarding data is special category under UK GDPR — it is categorically different from other confidential data and must be treated that way. The tool naming it explicitly, flagging it as High in the BrightPath scenario, and giving it a specific safeguard statement sends the right message.

**Critical risk overrides everything.** In the recommendation logic, a Critical risk returns "Not ready for AI pilot" regardless of how good the readiness and workflow scores are. This is the correct decision. No amount of organisational readiness justifies using AI on a workflow with unmanaged critical risk.

**Responsible-use notice on every page.** Not just on the Home page. Every page ends with `responsible_use_notice()`. This was a deliberate choice to ensure the limitations are visible regardless of where a reviewer or client is in the tool.

**Placeholder text models safe use.** Every text area and text input has placeholder text that describes what kind of information is appropriate. This reduces the chance of a user entering something they should not — not because the tool blocks it, but because the expected input is modelled clearly.

---

## Technical Decisions

**`ast.parse()` for syntax verification.** Running the app after every code change is slow. Using `ast.parse()` to check for syntax errors before running Streamlit was faster and caught errors earlier.

**`st.rerun()` after sample loaders.** Rather than trying to set widget values mid-render, calling `st.rerun()` after the sample button sets all session state keys ensures widgets render with the correct values from a clean script run.

**No `st.form()`.** Using regular widgets rather than `st.form()` means the report preview and recommendation update live as the user changes values. This makes the tool feel more interactive and easier to demonstrate.

**`_cell()` in the report generator.** Pipe characters in cell values would break Markdown table rows. A simple escape helper function prevented this without requiring an additional library.

---

## What This Proves

- Rashid can translate a consulting methodology (Layers 3–7) into a working software prototype
- He can design and implement modular Python code with clean separation of concerns
- He understands AI governance, safeguarding risk, and data protection well enough to encode it into a tool
- He can build something demonstrable, explainable, and safe to show to clients
- He can scope a build into phases, execute each phase cleanly, and document it accurately

---

## What It Does Not Prove

- Commercial validation — the tool has not been used with a real client
- Real-world effectiveness — we do not know whether it produces better outcomes than an experienced consultant working without a tool
- Scalability — it has not been tested with multiple users, large organisations, or complex scenarios
- Production readiness — there is no CI/CD, no deployment pipeline, no persistent storage, and no error handling for unexpected inputs

---

## Lessons Learned

1. **Start with the scoring logic before the UI.** If the scoring functions are tested independently, the Streamlit code becomes straightforward.
2. **Sample data is a first-class deliverable.** It deserves as much thought as the scoring logic.
3. **Read the Streamlit session state docs carefully.** The widget-key-value relationship is not immediately obvious and causes subtle bugs if misunderstood.
4. **Write the responsible-use language before the code.** Once it is in the safety spec, it becomes easy to add to every page. If left to the end, it often gets forgotten or feels tacked on.
5. **Phase scope matters.** "Phase 3: Workflow Audit" is clear. "Phase 3: Everything else" is not. Scoping each phase tightly prevented drift and made the build log accurate.

---

## Next Build Improvements

The next version of this tool should address:

1. **Organisation Profile input form** — so consultants can enter real (anonymised) data in the session rather than using pre-loaded sample data
2. **Persistent session state** — so a session can be saved, resumed, or shared
3. **Multiple workflow audits** — so the tool can compare two or three workflows in a single session
4. **PDF export** — so the report can be shared without requiring the recipient to render Markdown
5. **Automated test suite** — so changes can be verified without manual assertion scripts
