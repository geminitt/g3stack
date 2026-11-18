---
name: g3-prototype
description: Build a small disposable artifact to resolve a design, behavior or feasibility decision. Use when an observation can settle a fork before production implementation.
license: See ../PROVENANCE.md and retained upstream notices.
---

Apply [shared execution boundaries](../compatibility.md). This is the selected
work procedure, not a new project controller. Return evidence and unresolved
questions to the existing project record.

# Prototype

Adapted from pstack's decision-focused Prototype playbook.

1. Name the decision and the observation that can change it. Without a decision,
   use ordinary implementation or answer the question directly.
2. Inspect prior art only when the design space is open. Reuse an accepted
   direction rather than restarting discovery or asking again.
3. Build the smallest instrument in isolated project scratch space. A script
   can answer timing/behavior questions; a lightweight interactive artifact can
   answer UI questions. Label simulations and excluded behavior.
4. Compare alternatives only when alternatives are decision-relevant. Keep
   variants identifiable and conditions comparable. An arbitrary prototype
   count or new framework does not earn its cost.
5. Observe the matching surface: actual command output/timing, or rendered
   interaction and screenshots for UI. Follow [Experiment](../g3-experiment/SKILL.md)
   when making a comparative research claim. Prototype shortcuts do not remove
   correctness, authorization, data or measurement constraints.
6. Report the artifact path, observations, tradeoffs, recommendation and what
   remains unverified. The output is a decision instrument, not shippable code.

Do not require production-grade abstractions or broad test infrastructure for a
throwaway sketch. Keep checks needed to trust the observation. Hand an accepted
build direction to [Design](../g3-design/SKILL.md) or [Build](../g3-build/SKILL.md)
only within the authorized scope. Preserve useful evidence before scratch cleanup.

[Source attribution and adaptations](../PROVENANCE.md).
