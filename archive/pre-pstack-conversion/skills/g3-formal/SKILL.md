---
name: g3-formal
description: Create or maintain formal verification for a justified high-risk invariant or state machine. Use when tests leave a material concurrency, protocol, parser or safety question unresolved.
license: See ../PROVENANCE.md and retained upstream notices.
---

Apply [shared execution boundaries](../compatibility.md). This is the selected
work procedure, not a new project controller. Return evidence and unresolved
questions to the existing project record.

# Formal Verification

Adapted from pstack's formal-verification family and Statechart method.

Name the invariant, actual code boundary, defect cost and why tests alone leave
this decision unresolved. Identify the suitable formal tool, model assumptions,
bounds and available approved runtime. A source guide supplies no installed prover.

Choose only the relevant guide under `../../vendor/pstack/skills/`:
`create-formal-verification-skill/SKILL.md` for a missing recipe,
`maintain-formal-verification-skill/SKILL.md` for code/model drift, or
`statechart/SKILL.md` for an existing checked TLA+ model and explanatory statechart.
Read the selected guide in full and required resources. Apply native project paths,
configured models, authorized sequential/delegated work and the shared boundaries.

Keep code/model synchronization and properties explicit. Check that a deliberate
property violation is detected where feasible, retain counterexamples and distinguish
model drift, harness defects and product defects. A bounded model is not a proof
of unmodeled code or all possible inputs. A rendered diagram is not a model-check run.

Retain tool/version, model/code identity, assumptions, bounds, commands and results.
Report proved properties, counterexamples, unresolved checks and coverage limits;
leave unavailable target/toolchain claims open. Do not install a tool or activate a
generated verification skill merely because an upstream guide requests it.

[Source attribution and adaptations](../PROVENANCE.md).
