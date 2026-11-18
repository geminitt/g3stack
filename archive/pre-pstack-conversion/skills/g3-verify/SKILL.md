---
name: g3-verify
description: Run meaningful checks or create and maintain a missing real-app verification recipe. Use for observable CLI, API, library or UI behavior; reuse an adequate existing harness.
license: See ../PROVENANCE.md and retained upstream notices.
---

Apply [shared execution boundaries](../compatibility.md). This is the selected
work procedure, not a new project controller. Return evidence and unresolved
questions to the existing project record.

# Verify

Adapted from pstack's create/maintain verification-skill family.

Choose the smallest route:

- **Run**: use the project's adequate existing harness and accepted criteria.
  Record actual inputs, commands, outcomes and uncovered behavior. Do not create
  a verification skill merely because this entry was selected.
- **Create/extend**: when a repeated real-app check is missing, inspect startup,
  user surface, existing automation, observations, seed data and instance isolation.
  Write only the missing recipe/helpers in the approved project location.
- **Maintain**: inspect the existing recipe/map against source and real behavior;
  distinguish documentation drift, a harness gap and a product defect.

A reusable recipe contains exact launch/readiness, doctor, drive, evidence and
cleanup steps grounded in this app. Prefer stable selectors and project scripts.
A noninteractive CLI can use a bounded subprocess; PTY/tmux is conditional.
A Codex project skill uses `.agents/skills/verify-<app>/`; prepare an undiscoverable
draft when native activation has not been authorized.

Reuse the project's authoritative journey/feature map. If none exists and a
reusable recipe needs one, seed a concise index of actual user-facing paths,
their preconditions, drive steps, expected end states and known limits. Prefer
stable ARIA/data handles, routes or command contracts to coordinates and tab order.
Do not invent a second map beside an adequate existing acceptance suite.

Before handing over a created recipe, follow its instructions to exercise at
least one mapped journey, verify resulting state/side effects and confirm that
evidence survives cleanup. Report all untested journeys. A stand-in environment
does not prove the actual target setup.

Maintenance checks every mapped feature against source and the matching live
surface. Merge overlapping recipes for efficient driving. Doctor after surprising
behavior; reset a wedged session rather than assuming health. Re-drive any repaired
harness path. Product defects are reported, not hidden by rewriting expected behavior.
Keep required unreachable paths incomplete with the exact prerequisite and route tried.

Retain evidence after cleanup and stop only owned processes. Source-reading may
be sequential; self-review is not independent verification. A failed startup
permits only repairs within the approved task, not automatic dependency installs.
Report the route, coverage, actual checks, artifacts, product gaps and next action.

[Source attribution and adaptations](../PROVENANCE.md).
