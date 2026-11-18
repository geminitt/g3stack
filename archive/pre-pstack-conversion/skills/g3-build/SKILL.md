---
name: g3-build
description: Implement an accepted feature or execute a multi-task plan, using project tools and task-level evidence. Use for code changes with defined behavior; not unresolved product decisions.
license: See ../PROVENANCE.md and retained upstream notices.
---

Apply [shared execution boundaries](../compatibility.md). This is the selected
work procedure, not a new project controller. Return evidence and unresolved
questions to the existing project record.

# Build

Adapted from DevFlow's focused implementation and Superpowers execution methods.

1. Read the accepted requirements/plan and relevant code. Identify the complete
   change boundary: callers, configuration, exports, fixtures and user paths.
2. Reuse existing modules, project conventions and dependencies. Choose the
   simplest complete change. A small specified task needs no new plan, skill,
   worktree, dependency or delegation merely to follow a workflow.
3. For a multi-task plan, execute dependency-ready tasks and record actual
   progress in the existing project record. Use sequential execution unless
   delegation is both useful and authorized. Do not create a parallel ledger.
4. At each task, implement a testable slice and compare actual behavior with its
   accepted outcome. Meaningful regression checking follows [Debug](../g3-debug/SKILL.md);
   do not impose TDD on trivial wording edits or mirror implementation in tests.
5. If code is wrong, diagnose the mechanism. If a plan detail conflicts with the
   accepted requirement, make the smallest authorized correction and record why.
   If evidence invalidates a premise, use [Recovery](../g3-recover/SKILL.md).
6. Run focused and required project checks. Inspect the actual diff and complete
   connected changes. Unavailable target checks remain open; self-review is not
   an independent reviewer. Use [Review](../g3-review/SKILL.md) when appropriate.

Continue routine authorized work. Ask only for an actual unresolved owner decision.
Retain evidence and report delivered behavior, checks and limits. Do not add
commits, external updates, workspace deletion or branch-finishing actions from
an upstream checklist. Existing approved requirements remain the acceptance boundary.

[Source attribution and adaptations](../PROVENANCE.md).
