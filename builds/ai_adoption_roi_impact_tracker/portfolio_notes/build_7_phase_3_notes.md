# Build 7 Phase 3 — Portfolio Notes

**AI Adoption ROI and Impact Tracker — Workflow Impact and Bottleneck Analysis**

---

## 1. What Phase 3 Adds

Phase 3 adds a deterministic workflow impact and bottleneck analysis engine to the Build 7 adoption tracker. It converts the ROI estimates and adoption metrics from Phases 1 and 2 into operational diagnostic evidence that a consultant can discuss directly with a client.

The engine provides:

- Workflow impact status classification (Ready to scale / Positive but monitor / Needs improvement / Needs governance review / Stop or pause).
- Training bottleneck detection — identifying where low completion rates or weak confidence change indicate that training investment has not yet landed.
- Quality bottleneck detection — identifying where output quality concerns could undermine the value of AI adoption.
- Risk bottleneck detection — identifying where logged incidents or near-miss patterns require governance attention before adoption continues.
- Efficiency bottleneck detection — identifying where the AI-supported process is not yet producing enough time saving to justify wider use.
- Primary bottleneck identification — returning the highest-priority concern per workflow, in the order Risk > Quality > Training > Efficiency.
- Organisation-level and build-level groupings of bottleneck evidence.
- A prioritised workflow action list, ranking workflows by consulting urgency.
- Deterministic action recommendations — plain-language consulting guidance for each workflow.

All calculations are deterministic and template-based. No external LLM or API is called.

---

## 2. Why Workflow Impact Analysis Matters After an AI Pilot

After an AI pilot, a small organisation typically has a collection of loosely structured observations: time saving estimates, staff feedback, quality concerns, and incident reports. Without a structured framework, these observations are difficult to act on.

Workflow impact analysis gives a consultant a systematic way to review that evidence across all workflows at once, identify which are ready to scale and which require further attention, and produce a prioritised action list that the leadership team can act on quickly.

This matters because small organisations rarely have time for extended analysis. They need clear positions, not long-winded reviews. Phase 3 provides that clarity in a format that supports a confident consulting conversation.

---

## 3. Why Time Saved Alone Is Not Enough

Phase 2 estimated the financial value equivalent of time saving. Phase 3 goes further by asking whether the time saving was achieved safely, confidently, and consistently.

A workflow that saves five hours per week but generates multiple quality issues is not ready to scale. A workflow that shows strong time saving but has low training completion may not be sustainable. A workflow that triggered a risk incident should not be expanded until the underlying governance concern is resolved.

Phase 3 makes these distinctions explicit by treating time saving as one input into a multi-signal diagnostic picture, rather than the final measure of adoption success.

---

## 4. How Bottlenecks Are Classified

Phase 3 uses four bottleneck types, each with three levels: Clear, Possible, and No bottleneck.

**Training bottleneck** — based on training completion rate and confidence change. A clear bottleneck requires both signals to be weak. A possible bottleneck requires either one.

**Quality bottleneck** — based on the number of quality issues logged and the quality issue rate per 10 weekly tasks. A high absolute count or a high rate relative to task volume triggers the classification.

**Risk bottleneck** — based on logged risk incidents and near misses. Any logged incident triggers a clear bottleneck immediately, because risk incidents should not be normalised during a pilot.

**Efficiency bottleneck** — based on the efficiency gain percentage against the baseline task time. A clear bottleneck is fewer than 10 percentage points of gain. A possible bottleneck is 10–30 percentage points.

The primary bottleneck then identifies the highest-priority concern, in the order Risk > Quality > Training > Efficiency. Risk and quality problems take priority because they directly affect whether adoption is safe and whether output is fit for use.

---

## 5. Why Risk and Quality Are Prioritised Before Scaling

In a small organisation adopting AI for the first time, risk incidents and quality failures carry disproportionate consequences. A single safeguarding concern, data boundary breach, or misleading report output can undermine trust in AI adoption for months.

For this reason, Phase 3 applies a hard prioritisation: any workflow with a clear or possible risk bottleneck is classified first, regardless of how strong the time saving or confidence gains may be. Quality bottlenecks come second, because poor output quality can compound over time and create operational problems that are expensive to reverse.

This mirrors the approach a responsible AI adoption consultant would take: celebrate the efficiency wins, but do not scale anything that has unresolved governance or quality concerns.

---

## 6. How This Connects to Build 1

Build 1 is the AI Readiness and Workflow Audit Tool. It identifies candidate workflows and assesses whether the organisation's governance, training, and process foundations are ready for AI adoption.

Phase 3 of Build 7 provides the feedback loop for Build 1 work. The workflow impact classifications directly reflect the readiness factors Build 1 identified: governance readiness connects to the risk bottleneck, training readiness connects to the training bottleneck, and process efficiency connects to the efficiency bottleneck.

A consultant using both Build 1 and Build 7 Phase 3 can now complete the audit-to-impact cycle: identify what should be adopted, measure what was adopted, and assess whether the adoption produced the expected results.

---

## 7. How This Connects to Build 4

Build 4 is the AI Staff Training and Workshop Generator. It creates training materials to build staff confidence and safe AI practice.

Phase 3 directly measures the impact of Build 4 activity through training bottleneck detection. Workflows with high training completion rates and strong confidence improvement have no training bottleneck. Workflows where Build 4 training has not yet been applied or completed show either a possible or clear training bottleneck.

The build-level workflow impact summary in Phase 3 makes this connection explicit: it shows how workflows related to Build 4 are performing across the portfolio, including the dominant bottleneck type. This gives the consultant a clear view of whether training investment has translated into adoption quality.

---

## 8. How This Connects to Build 5

Build 5 is the AI Consulting Report Generator. It produces structured client-facing reports summarising audit findings and recommendations.

Phase 3 produces the kind of structured consulting evidence that a Build 5 report would present to a client leadership team. The workflow impact status classifications, prioritised action list, and deterministic recommendations translate directly into a report structure: here is what is working, here is what needs attention, and here is what we recommend you do next.

A consultant could use the Phase 3 prioritised action list as the basis for the recommendations section of a Build 5 consulting report, with workflow impact evidence backing each recommendation.

---

## 9. How This Connects to Build 6

Build 6 is the AI Governance Policy Checker. It reviews whether an organisation's policies cover the key governance areas required for responsible AI adoption.

Phase 3 tracks the adoption quality of governance-related workflows — including incident log reviews, acceptable use policy reviews, and governance checklist work — through risk bottleneck detection. Workflows that have triggered incidents, logged near misses, or been paused for governance reasons appear clearly in the prioritised action list.

The connection between Build 6 and Build 7 Phase 3 demonstrates that governance policy quality has a direct effect on adoption quality. Organisations with stronger governance foundations tend to show fewer risk bottlenecks in the Phase 3 analysis.

---

## 10. How a Consultant Could Use This with a Small Organisation

A consultant working with a small organisation could use Build 7 Phase 3 as follows:

1. **After the pilot period**, collect the Phase 1 adoption metric records for all active workflows.
2. **Run the Phase 3 impact engine** to classify each workflow's status and identify primary bottlenecks.
3. **Use the prioritised action list** to open a structured review conversation, starting with Stop or pause and Needs governance review workflows.
4. **Share the organisation-level summary** with the client's leadership team to give a clear picture of which departments or teams are seeing the strongest adoption outcomes.
5. **Share the build-level summary** to show how different types of AI support activity — audit work, training, report generation, governance checking — are contributing to adoption quality across the portfolio.
6. **Use the deterministic recommendations** as conversation starters: the text is intentionally plain and direct, designed to anchor a practical discussion rather than to read as a final verdict.
7. **Feed the Phase 3 analysis into a consulting report** (Build 5) to create a structured client-facing document that the organisation can share with trustees, funders, or senior staff.

The key consulting discipline here is to separate the good-news story from the areas of concern. Phase 3 makes both explicit: it celebrates what is working, identifies what needs attention, and provides a prioritised path forward.

---

## 11. What Should Come Next in Phase 4

Phase 4 should add a Training, Confidence, and Adoption Readiness Review. This would:

- Analyse staff confidence change patterns across all workflows in more depth, identifying whether confidence gains are consistent or uneven.
- Track training completion rates across organisations and builds, flagging where investment in Build 4 activity is needed.
- Compare pre-adoption and post-adoption confidence profiles to identify whether AI adoption is building capability or creating dependency.
- Produce a structured readiness position for each organisation: is the organisation ready to move from pilot to early adoption, or does training and confidence-building need to continue first?

Phase 4 would build directly on the bottleneck detection in Phase 3, adding a deeper layer of training and confidence analysis to support more targeted consulting advice.

---

*Build 7 Phase 3 · AI Adoption ROI and Impact Tracker · BrightPath ChatGPT Mastery Project*
*Synthetic scenarios only. Human review required before any real-world use.*
