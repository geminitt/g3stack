---
name: g3-review
description: Review an actual diff and affected behavior against requirements, source and meaningful checks. Use for a scoped review or consequential impact analysis; not automatic provider or audit execution.
license: See ../PROVENANCE.md and retained upstream notices.
---

Apply [shared execution boundaries](../compatibility.md). This is the selected
work procedure, not a new project controller. Return evidence and unresolved
questions to the existing project record.

# Review

Adapted from DevFlow's scoped review coordination and pstack's evidence-first impact analysis.

1. Pin the requested revision/range or working-tree state. Account for staged,
   unstaged and relevant untracked files when those are in scope; never review
   only committed HEAD while claiming coverage of all current work.
2. Read complete relevant diff chunks, accepted requirements and affected callers,
   contracts, data/wire formats and behavior outside the immediate diff.
3. Check candidates against source and real expected behavior. Prefer findings
   with a concrete failure path, location, consequence and reproducer/check.
   Distinguish actionable defects from style preferences and speculative concerns.
4. For a consequential change, identify the facts safety depends on and verify
   them at the strongest feasible level: actual code/library behavior or the
   running app. Record uncertainty; a plausible writeup is not proof.
5. Report reviewed identity, coverage/exclusions, findings and limits. A clean
   self-review is not independent verification or a complete security audit.
   Review-only scope does not authorize product fixes or external comments.

Ordinary review uses host/project tools directly. Use the source reference
`../../vendor/pstack/skills/blast-radius/SKILL.md` only for needed impact technique;
its Arena/model and delivery instructions do not become defaults.

For explicitly requested OCR integration, read
`../../vendor/devflow/plugin/skills/open-code-review/SKILL.md` and compatibility,
check the existing CLI/version and authorized provider/data movement. If absent,
continue host-native review and label the missing OCR capability; do not install it.
For a requested adversarial panel, use native authorized independent agents and
reproduce their counterexamples, not an assumed multi-model service. Security
claims go through [Security](../g3-security/SKILL.md) with its actual boundaries.

[Source attribution and adaptations](../PROVENANCE.md).
