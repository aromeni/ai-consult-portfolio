# Build 8 Phase 3 Notes

## What Phase 3 adds

Phase 3 adds a deterministic blocker, risk, and dependency review. It analyses blocker text, action status, delivery priority, due pressure, and required governance, training, or client follow-up dependencies.

The phase produces action-level blocker summaries, organisation and related-build exposure summaries, escalation flags, a prioritised resolution list, and deterministic recommendations.

## Why blocker and dependency review matters

An implementation action can appear active while still being unable to progress. A pending approval, unclear quality standard, missing owner, training gap, or unresolved client decision can quietly delay adoption.

This review separates ordinary action tracking from deeper delivery risk. It makes constraints visible before they affect rollout quality, confidence, or governance.

## How blocker severity works

- Critical blocker: a blocked action with Critical priority.
- High blocker: a blocked action, a Critical-priority action with a blocker, or a blocked action due within seven days.
- Moderate blocker: a High-priority blocked action or a blocked action due within fourteen days.
- Low blocker: any other action with a recorded blocker.
- No blocker: no blocked status and no blocker text.

## How dependencies are classified

The engine checks whether an action requires governance sign-off, training follow-up, or a client check-in. One active requirement is labelled as its specific dependency. Two or more active requirements are labelled Multiple dependencies.

Delivery risk increases when high-priority work has multiple dependencies, when blocker severity is high, or when an incomplete action is due within seven days.

## Connection to Builds 1, 4, 5, 6, and 7

- Build 1 workflow actions may depend on leadership decisions or named implementation owners.
- Build 4 actions may be delayed by training, confidence, coaching, or staff guidance gaps.
- Build 5 follow-up actions may depend on quality criteria or client agreement.
- Build 6 governance actions may require policy, control, approval, or sign-off decisions.
- Build 7 evidence actions may depend on agreed review thresholds and client check-ins.

## Consulting use

A consultant could use the Phase 3 review during an implementation meeting to identify which blockers need escalation, who must resolve them, and which organisations or portfolio builds carry the greatest dependency exposure.

The prioritised table supports focused follow-up rather than reviewing every open action with equal urgency.

## What Phase 4 should add

Phase 4 should add a governance sign-off and control tracker. It should classify approval readiness, control implementation status, responsible governance owners, evidence requirements, and actions that cannot proceed until sign-off is complete.

Phase 4 should continue using synthetic data and deterministic Python logic only.
