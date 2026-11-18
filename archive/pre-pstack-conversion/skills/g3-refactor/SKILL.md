---
name: g3-refactor
description: Restructure code while preserving its accepted observable behavior. Use for a scoped refactor, API reshape or module cleanup; not an unapproved feature or behavior change.
license: See ../PROVENANCE.md and retained upstream notices.
---

Apply [shared execution boundaries](../compatibility.md). This is the selected
work procedure, not a new project controller. Return evidence and unresolved
questions to the existing project record.

# Refactor

Adapted from pstack's Refactoring playbook.

1. Pin the behavior contract before moving structure. Reuse characterization
   tests, snapshots, recorded outputs or an equivalence harness that exercises
   the affected behavior; type checks and lint alone are not a behavior pin.
2. Name the target data shape, ownership and module structure. Use
   [Design](../g3-design/SKILL.md) when the move crosses a consequential boundary.
   Leave a clear local structure alone when it already fits.
3. Remove relevant dead paths and redundant wrappers before introducing another
   abstraction. Move in small steps that keep the pin green; check callers,
   strings, configuration and documentation references after renames.
4. Migrate internal callers together when safe. Preserve public compatibility
   required by the owner; upstream remove-all-shims preferences do not override it.
5. Verify equivalence on the real artifact: old/new output comparison, replay,
   the project's harness or matching-surface smoke checks. A passing build alone
   does not establish unchanged behavior.
6. Assess whether the result reduces reader burden or invalid states. Report
   the structure changed, behavior pin, equivalence evidence and remaining risks.

Separate a discovered feature request or behavior defect from a structural change.
Do not delete owner work, delegate automatically, rebase, commit or open a PR just
because an upstream refactor checklist ends there.

[Source attribution and adaptations](../PROVENANCE.md).
