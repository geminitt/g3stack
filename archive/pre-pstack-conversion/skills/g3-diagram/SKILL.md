---
name: g3-diagram
description: Create or revise an editable technical diagram grounded in source evidence. Use for architecture, sequence, data flow or workflow visuals; not a formal correctness proof.
license: See ../PROVENANCE.md and retained upstream notices.
---

Apply [shared execution boundaries](../compatibility.md). This is the selected
work procedure, not a new project controller. Return evidence and unresolved
questions to the existing project record.

# Diagram

Adapted from DevFlow's Diagram Design integration.

Identify the question, audience, current/proposed status and editable output format.
Ground entities, boundaries and relationships in the relevant source/accepted design;
label unknowns instead of inventing system behavior. Reuse project styling.
Choose the smallest view that explains the question, then check structure,
labels, geometry and the rendered result. Keep editable source and requested export.

For diagram-specific templates or helpers, read
`../../vendor/devflow/plugin/skills/diagram-design/SKILL.md`, its `GUIDE.md` and
only needed assets. Resolve resources from the real source directory, and keep
outputs outside vendor. Inspect a helper before execution and use available
runtimes; missing export/render tooling leaves that check open, not passed.

A Mermaid/state diagram explains behavior; it does not prove an invariant.
Use [Formal Verification](../g3-formal/SKILL.md) only for a justified formal target.
Report evidence sources, proposed elements, editable/export paths and visual checks.

[Source attribution and adaptations](../PROVENANCE.md).
