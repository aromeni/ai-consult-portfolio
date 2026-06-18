# Build 8 Phase 6 Notes

## What Phase 6 adds

Phase 6 adds a deterministic client check-in summary builder. It combines synthetic organisation details, implementation actions, and the latest check-in record into a structured view of delivery health, progress, attention items, decisions needed, and the next review focus.

The phase also produces a concise Markdown summary that can be previewed during a client conversation.

## Why client check-ins matter during implementation

Implementation work can become fragmented across actions, owners, approvals, training needs, and blockers. A regular check-in gives the consultant and client a shared point to confirm what has moved, what is stuck, and what decisions are required.

The summary builder keeps that conversation focused on current delivery evidence rather than reviewing every record equally.

## How delivery progress is summarised

The progress snapshot counts completed, in-progress, not-started, blocked, and deferred actions for the selected organisation. Check-in health then classifies delivery as On track, Needs attention, At risk, or Blocked using action status, priority, client decisions, governance sign-offs, and training dependencies.

## How attention items and decision needs are identified

Attention items include blocked actions, Critical or High-priority work, client check-in actions, governance sign-offs, and training follow-up due within fourteen days.

Decision needs are generated for open governance approvals, blocked actions, client direction, and training follow-up. The next review focus follows a fixed priority from blocked Critical or High-priority work through to standard delivery progress.

## Connection to Builds 1, 4, 5, 6, and 7

- Build 1 workflow actions can be reviewed as pilot-readiness decisions.
- Build 4 training actions become coaching and support discussion points.
- Build 5 report follow-ups become client-facing quality and delivery decisions.
- Build 6 governance actions become approval and control agenda items.
- Build 7 adoption evidence informs whether the next step is to continue, review, or scale.

## Consulting use

A consultant could select an organisation before a weekly or monthly check-in, review its health and attention list, and use the Markdown preview as a concise meeting structure.

## What Phase 7 should add

Phase 7 should add an implementation progress report builder. It should combine action, blocker, governance, training, and check-in evidence into a fuller consultant-facing progress report with organisation and portfolio views.

Phase 7 should continue using synthetic data and deterministic Python logic only.
