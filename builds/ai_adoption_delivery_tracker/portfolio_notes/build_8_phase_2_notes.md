# Build 8 Phase 2 Notes

## What Phase 2 adds

Phase 2 adds a deterministic action tracker and status engine. It converts the synthetic implementation action register into due windows, attention levels, delivery states, priority scores, grouped workload summaries, and recommended next steps.

## Why action tracking matters after adoption review

An AI adoption review can recommend that a workflow should stop, continue, improve controls, or scale. Those decisions only become useful when the related work is prioritised and followed through.

The Phase 2 tracker helps distinguish routine actions from blocked, critical, or time-sensitive work. It also makes the delivery burden visible across organisations and across the earlier portfolio builds.

## How the tracker uses delivery evidence

- Priority sets the base delivery weight.
- Status shows whether work is complete, active, waiting, blocked, or deferred.
- Due days classify actions as due now, due soon, due later, or under no immediate pressure.
- Blocker text is treated as a delivery constraint even when the recorded status has not yet been changed to Blocked.
- The action score combines priority, blockers, due pressure, and completion into a simple deterministic ranking.

## Connection to Builds 1, 4, 5, 6, and 7

- Build 1 readiness actions can be compared with follow-up work from other builds.
- Build 4 training actions can be prioritised when confidence or support gaps remain.
- Build 5 report recommendations can be tracked as assigned delivery work.
- Build 6 governance actions can be escalated when sign-off or control dependencies block progress.
- Build 7 adoption decisions can be converted into prioritised implementation actions.

## Consulting use

A consultant could use the Action Tracker during weekly implementation meetings or client check-ins. The prioritised list identifies which actions need escalation first, while organisation and related-build summaries show where delivery capacity is under the greatest pressure.

The recommendation text provides consistent prompts for the next conversation without using an external AI model.

## What Phase 3 should add

Phase 3 should add a blocker, risk, and dependency review. It should classify blocker type and severity, identify dependency chains, highlight governance and training constraints, and produce a prioritised intervention list.

Phase 3 should continue to use synthetic data and deterministic Python logic only.
