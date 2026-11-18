---
name: g3-security
description: Inspect a concrete security question or perform an explicitly scoped audit with source evidence, isolation and honest coverage. Does not authorize probing or target-code execution.
license: See ../PROVENANCE.md and retained upstream notices.
---

Apply [shared execution boundaries](../compatibility.md). This is the selected
work procedure, not a new project controller. Return evidence and unresolved
questions to the existing project record.

# Security

Adapted from DevFlow's Cloudflare Security Audit integration. Keep focused review
and a full audit distinct. Integration or installation is not an audit request.

For a specific question or suspicious change, define the actual trust boundary,
read the affected source, trace a concrete attack/failure path and distinguish
confirmed findings, needs-validation candidates and rejected hypotheses. An
unresolved decisive fact remains needs-validation; do not manufacture severity.

Before full-audit or target-controlled execution, read
`../../vendor/devflow/plugin/skills/security-audit/SKILL.md`, `GUIDE.md` and only
selected companions. Preserve its OS-enforced isolation: no external network,
allowlisted clean environment, read-only target/toolchain, scratch-only writes
and bounded time/resources. Source access does not authorize live probing.
If controls are unavailable, continue useful source inspection and report the
execution blocker; do not substitute ordinary target builds/tests for isolation.

Full confirmation needs the specified independent verification and applicable
phases. Sequential author self-review does not satisfy that requirement. Read
`VALIDATION-AND-REPORTING.md` and `report-schema.json` in the same source folder
before emitting full-audit records; use supported protected-file or trusted-parent
stdin validators as specified. They validate records, not exploit truth, isolation
or independence. Preserve race-safe promotion and retained artifacts.

Report source revision, scope, findings, coverage, actual verification and blockers.
Keep the full audit incomplete while a required control/check/reviewer is missing.
Fixes, production probing, publication and external messages remain separately scoped.

[Source attribution and adaptations](../PROVENANCE.md).
