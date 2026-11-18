---
name: g3-plan
description: Turn an accepted design into bounded implementation tasks with explicit interfaces and verification. Use for multi-step work; skip for a small specified edit.
license: See ../PROVENANCE.md and retained upstream notices.
---

Apply [shared execution boundaries](../compatibility.md). This is the selected
work procedure, not a new project controller. Return evidence and unresolved
questions to the existing project record.

# Plan

Adapted from DevFlow's scoped Superpowers writing-plans procedure.

Read the accepted design, existing code and project constraints before decomposing.
A plan carries decisions an implementer cannot infer, rather than code they can write.

For each independently testable task record:

- The user-visible result and requirement it satisfies.
- Exact files/areas affected, dependencies and accepted constraints.
- Interfaces consumed and produced: names, inputs, outputs and error behavior.
- A meaningful verification command/scenario, independent expected outcome,
  relevant failure cases and recovery when changes are consequential.

Choose task boundaries where one result could be accepted independently of another.
Fold setup and documentation into the task that needs them. Do not manufacture
separate scaffolding tasks, fixed review-case counts, a new worktree or a full plan
for an obvious edit. Use the existing plan location and task record.

Check requirement coverage, cross-task interface consistency, untested failure
classes and proportion. Describe unresolved assumptions explicitly. Use
[Design](../g3-design/SKILL.md) or [Research](../g3-research/SKILL.md) for a material
unknown rather than silently freezing it into implementation.

Deliver the plan when planning is the requested outcome. When execution is already
authorized, continue through [Build](../g3-build/SKILL.md); do not ask for the same
scope or execution decision again. A plan cannot grant commit, push or deployment permission.

[Source attribution and adaptations](../PROVENANCE.md).
