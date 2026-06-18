# Build 8 Phase 4 Notes

## What Phase 4 adds

Phase 4 adds a deterministic governance sign-off and control tracker. It identifies explicit approval requirements, sign-off urgency, control areas, control readiness, governance owner needs, and governance delivery risk.

The phase produces action-level governance summaries, organisation and related-build workload summaries, a prioritised governance action list, and deterministic recommendations.

## Why governance sign-off matters during implementation

AI implementation can move faster than the organisation's approval and control processes. A workflow may be operationally ready while policy wording, quality standards, data boundaries, or senior approval remain unresolved.

The tracker makes those approval dependencies visible so delivery does not proceed without the necessary governance checks.

## How control readiness is reviewed

- Control blocked: explicit sign-off is required and the action status is Blocked.
- Control needs review: explicit sign-off is required or blocker text names a governance, approval, quality, risk, or data concern.
- Control ready: no sign-off is required, work is completed or in progress, and no blocker is recorded.
- No control required: no other control readiness condition applies.

Control areas are classified from action titles, descriptions, and blocker text using deterministic keyword matching.

## How governance risk is classified

High governance delivery risk applies when required sign-off is blocked or when a Critical or High-priority action needs urgent sign-off. Moderate risk applies when sign-off is required, due soon, or control review is needed. Other actions are classified as low governance delivery risk.

## Connection to Builds 1, 4, 5, 6, and 7

- Build 1 workflow actions may require approval before a controlled pilot begins.
- Build 4 training actions may depend on approved guidance and review standards.
- Build 5 report follow-ups may require quality, data, or client-facing approval controls.
- Build 6 governance actions create the strongest direct sign-off and policy workload.
- Build 7 scale or continuation actions may require evidence thresholds and governance approval.

## Consulting use

A consultant could use Phase 4 during implementation governance meetings to identify urgent approvals, blocked controls, responsible owner needs, and the organisations or build areas carrying the greatest governance workload.

The prioritised table supports a clear discussion about what can proceed operationally and what must wait for approval or control review.

## What Phase 5 should add

Phase 5 should add a training follow-up and support plan. It should identify staff groups needing support, classify training urgency and support type, connect training needs to implementation actions, and prioritise coaching or reinforcement activity.

Phase 5 should continue using synthetic data and deterministic Python logic only.
