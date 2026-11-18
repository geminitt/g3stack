---
name: g3-research
description: Investigate a system, compare options or resolve feasibility from source evidence. Use for an unclear question or research-only outcome; not for implementing an already specified change.
license: See ../PROVENANCE.md and retained upstream notices.
---

Apply [shared execution boundaries](../compatibility.md). This is the selected
work procedure, not a new project controller. Return evidence and unresolved
questions to the existing project record.

# Research

1. Identify the question, the decision it can change, known constraints and
   consequential unknowns. Reuse project material; an empty project needs no scaffold.
2. For system investigation, trace entry points, data/state flow, configuration,
   callers and failure boundaries. Separate code possibilities from observed behavior.
3. For external claims, follow primary documentation, source, specifications or
   reproducible observations. Retain source identity, version/date and the exact
   assertion supported. Evaluate domain fit, sample coverage, incentives,
   contradictory evidence and omitted alternatives.
4. State plausible competing explanations. Choose the smallest safe observation
   that separates them. Research-only scope does not authorize a fix or a
   consequential experiment; report the necessary permission boundary.
5. Compare viable options against the actual goal, complexity, evidence strength,
   maintenance and cost. Include reuse or doing nothing when plausible; do not
   invent alternatives to meet a count.
6. Conclude when evidence answers the question or more searching is unlikely to
   change the decision. Report findings, uncertainty, sources and the next
   permitted action. Research can finish with an answer and no implementation.

A root-cause claim needs a supported causal chain. If observation cannot decide,
use [Experiment](../g3-experiment/SKILL.md) or [Prototype](../g3-prototype/SKILL.md)
for a bounded check. New contradictory evidence goes to
[Premise Recovery](../g3-recover/SKILL.md). Create a research note only when the
requested deliverable or continuity warrants one.

[Source attribution and adaptations](../PROVENANCE.md).
