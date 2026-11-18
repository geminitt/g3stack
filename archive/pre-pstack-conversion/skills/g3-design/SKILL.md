---
name: g3-design
description: Choose data ownership, types, interfaces or a reference-led product design. Use for consequential architecture and unresolved design decisions; reuse accepted decisions for ordinary edits.
license: See ../PROVENANCE.md and retained upstream notices.
---

Apply [shared execution boundaries](../compatibility.md). This is the selected
work procedure, not a new project controller. Return evidence and unresolved
questions to the existing project record.

# Design

Adapted from pstack Architect/domain methods and DevFlow's reference-led design.

For a code structure decision, trace the touched systems and compare meaningful
shapes for types, signatures and module boundaries. Prefer one owner per state,
explicit invariants and a small caller-facing surface. Model stateful behavior
with a structure appropriate to the domain rather than scattered shape assumptions.
Do not force multiple designs or an Arena panel for a settled or mechanical change.

For reference-led product work:

1. Establish the actual user outcome, constraints and observable acceptance.
   Separate confirmed requirements, assumptions and owner decisions.
2. Compare official options, relevant licensed components and observed reference
   behavior. Check feasibility before expensive design. Distinguish discovered
   behavior from a proposed contract; screenshots do not reveal backend facts.
3. Define only the applicable data, permission, API/CLI/module and failure-state
   contracts. Use the existing project format; no mandatory web mock for a CLI.
4. Use [Prototype](../g3-prototype/SKILL.md) when feedback can settle a decision.
   Update affected contracts when evidence changes the accepted direction.
5. Hand an authorized accepted design to [Plan](../g3-plan/SKILL.md) or
   [Build](../g3-build/SKILL.md), with constraints and acceptance evidence intact.

For an explicitly requested full reference-led product lifecycle, read
`../../vendor/devflow/plugin/skills/devflow/references/system-workflow.md` and
its selected supporting resources. Treat it as the bounded product procedure;
its release/staging gates do not apply to unrelated research or local-only work.
Reverse analysis requires its actual authorized source and clean-room boundary;
prefer official documentation or licensed reuse when adequate.

[Source attribution and adaptations](../PROVENANCE.md).
