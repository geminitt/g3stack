---
name: g3-debug
description: Reproduce and diagnose a bug or integration failure, then verify a scoped fix with meaningful regression evidence. Use when observed behavior contradicts an accepted contract.
license: See ../PROVENANCE.md and retained upstream notices.
---

Apply [shared execution boundaries](../compatibility.md). This is the selected
work procedure, not a new project controller. Return evidence and unresolved
questions to the existing project record.

# Debug

Adapted from DevFlow's systematic-debugging and pstack's practical TDD method.

1. Identify intended behavior, actual symptom and affected surface. Read errors,
   source, callers, recent relevant changes and environment differences.
2. Establish failing behavior before editing when feasible. Select the cheapest
   meaningful test or executable reproduction already close to the path. Confirm
   it fails for the reported reason. If direct reproduction is impossible,
   record the limitation and use an appropriate alternative observation.
3. Trace data and component boundaries; compare a working path with the failing
   path. State competing hypotheses and choose one discriminating check at a time.
   Add targeted instrumentation only where its result can change the diagnosis.
4. Confirm the mechanism before fixing. A count of failed attempts does not prove
   an architectural defect. A first counterexample to a load-bearing premise
   warrants [Recovery](../g3-recover/SKILL.md), even without repeated failures.
5. Make the smallest complete fix preserving neighboring contracts. Do not mix
   speculative improvements or unrelated refactors into it.
6. Rerun the original reproduction, the regression check and required nearby
   checks. Retain failing-before/passing-after output when feasible. Remove only
   task-created instrumentation and keep failure evidence.

Prefer a focused unit/component/integration test where it naturally fits. When
new harness setup would be disproportionate, use a repeatable CLI, HTTP, browser,
trace or log check and explain the limitation. Do not weaken assertions to match
wrong code. For a captured or live performance artifact, use the relevant
measurement branch; do not claim unit tests prove unexercised target behavior.

A diagnosis-only request ends with evidence and a proposed repair boundary.
Report the symptom, supported cause, change, regression proof and remaining limits.

[Source attribution and adaptations](../PROVENANCE.md).
