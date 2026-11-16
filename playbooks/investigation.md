# Investigation

Use this playbook to understand an unfamiliar codebase or existing system,
explain technical behavior or an incident, or investigate an uncertain cause.
Apply [Shared Core](../instructions/core.md) and applicable project instructions.
For a bounded factual question with a directly supported answer, answer and
verify it directly rather than expanding it into an investigation.

Scale the work to the question. Skip irrelevant parts with a short reason.
Do not require diagrams, documentation or state files, or an exhaustive
architecture review. Reuse relevant evidence; do not reread or search the
whole repository when a focused search or existing observation is sufficient.

## 1. Bound the question

Identify the question, scope, expected explanation, and evidence needed to
answer it. Establish available artifacts and access, relevant versions or
environments, known symptoms, assumptions, and important unknowns. For an
incident, identify the affected behavior and time range before following leads.

Choose the smallest useful investigation boundary. Follow leads only when they
could change the answer. Finish when the question is answered or further
inspection is unlikely to resolve the remaining uncertainty. If a required
source or check is unavailable, stop only dependent work and report the limit;
continue independent authorized work. Do not guess or widen scope without
justification.

## 2. Map the relevant system slice

Inspect relevant repository structure, entry points, manifests, dependencies,
configuration, and execution paths as applicable. Start from the user's example,
affected interface, or observable output, then follow the components it reaches.
Inspect history only when it can explain a relevant decision or change.

Describe the actors, inputs, outputs, state, and boundaries needed to explain
the behavior. Distinguish configuration defaults and documented intent from
values or behavior actually observed. Missing code, logs, or runtime access
limits the model; it does not justify inventing components or behavior.

## 3. Trace concrete evidence

Trace calls, data flow, state changes, and error handling along the relevant
path. Tie material claims to source locations, configuration evidence, logs,
traces, or reproducible observations, with relevant versions and input identities.
Treat names and documentation as navigation aids rather than proof of behavior.
Static code establishes possible paths, not that a path ran in a given incident.

For incidents, correlate events and changes within the affected time range;
temporal proximity alone does not establish causation. Identify competing
explanations and evidence that supports or challenges each material hypothesis.

## 4. Check the uncertain links

When useful and authorized, choose a targeted, low-cost check that can
distinguish explanations. State its predicted observation and inspect the actual
result. Prefer existing observations or safe, bounded checks to broad test runs.
Inspect a command's effects before running it; a test or diagnostic can mutate
state or contact a live service.

Preserve existing project behavior. Do not edit files, change configuration,
restart services, or replay requests with side effects merely to investigate.
If a useful reproduction requires changes or consequential execution outside
the authorized scope, describe the proposed check and leave it unperformed.
Report failed or unavailable checks and the questions they leave unresolved.

## 5. Explain and hand off

Report the relevant system model and evidence-backed answer. Label observations
(what was seen), confirmed findings (supported conclusions), hypotheses
(unverified explanations), and unknowns. State checks performed, evidence
locations, conflicting evidence, and limits on the conclusion.

Claim a root cause only when evidence supports the causal chain; identify
material alternatives tested or still open. Otherwise report a suspected cause
and the smallest next check or decision needed. Recommend changes only after
explaining the supporting evidence and remaining uncertainty.

For suspected defects, provide the failing behavior, reproduction evidence or
limitations, and relevant paths as a handoff to a separately authorized Bug Fix
stage. An investigation request does not authorize that stage. Finish with the
recommended next action; do not automatically continue into implementation.
