---
name: g3-measure
description: Diagnose performance, validate a benchmark, optimize a fixed metric or compare agent configurations. Use when measured behavior can change a decision, not to benchmark an unrelated task.
license: See ../PROVENANCE.md and retained upstream notices.
---

Apply [shared execution boundaries](../compatibility.md). This is the selected
work procedure, not a new project controller. Return evidence and unresolved
questions to the existing project record.

# Measure

Adapted from pstack Benchmark Checklist, Perf Issue, Hillclimb, Eval and forensics.
Apply [Experiment](../g3-experiment/SKILL.md) for the domain protocol and independent
assessment. Select one branch; measurement is not a second project controller.

## Performance and optimization

Name the realistic workload, correctness gate, metric, baseline, limiter and stop
condition. Read what the harness times/counts/ignores. Confirm actual work occurs
inside the timed region and outputs/errors are counted. Use production-relevant
settings, representative data and comparable resource conditions.

Sample enough to distinguish variation from an effect; alternate conditions where
noise/drift matter. Report run count, units and variation. A requested single-run
ballpark is not a basis for adoption. Check physical/resource bounds and end-to-end
relevance before reporting a speedup. Unknown limiter or invalid comparison leaves
the conclusion inconclusive rather than a narrower unsupported win.

For sustained improvement, freeze a sensitive harness, change one hypothesis at a
time and retain only gains beyond noise with the correctness gate green. Keep
negative attempts in the existing record. Follow the owner's budget and stop
boundary, not an upstream minimum-attempt count or automatic commit schedule.

## Agent comparison

Hold tasks, model, tools, permissions, input snapshot and scoring conditions
controlled. Use realistic task prompts, sanitized labels and independent scoring
when possible. Inspect actual execution traces; neither a naming blacklist nor
self-reported skill usage establishes evaluation independence or quality.

## Forensics

For live symptoms capture the relevant profile/trace with authorized tools and
prove the suspected mechanism. For an existing capture, inspect the fixed artifact
with the appropriate parser and map hotspots/retainers to source; do not rerun just
to recreate it. A paired capture can confirm a change; a single artifact may only
support a hypothesis. Instrumentation and live mutation still require scope.

Optional detailed references, read only for the selected branch:
`../../vendor/pstack/skills/poteto-mode/playbooks/{perf-issue,hillclimb,eval,runtime-forensics,trace-forensics}.md`
and `../../vendor/pstack/skills/benchmark-checklist/SKILL.md`.
Configured models, native tools and this skill's boundaries replace vendor defaults.

[Source attribution and adaptations](../PROVENANCE.md).
