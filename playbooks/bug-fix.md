# Bug Fix

Use this playbook to diagnose a defect or make an authorized correction to
behavior that violates an intended contract. Apply
[Shared Core](../instructions/core.md) and applicable project instructions.
A bounded factual question can use a direct answer with suitable verification.

For diagnosis-only requests, perform the relevant diagnosis and report findings;
do not edit project files, add tests, or proceed into implementation. Run checks
only within the authorized scope. Repair steps below apply only when a fix is
authorized. Skip irrelevant parts with a short reason, without relaxing Core.

## 1. Establish the behavior and scope

Identify expected behavior and its source, the observed failure, affected
inputs, environment, versions, and interfaces. Resolve material uncertainty
about the intended contract before selecting a correction. Inspect relevant
project checks and current changes; preserve existing user edits.

Define the requested outcome, permitted changes and execution, and evidence
needed to demonstrate it. Do not infer repair authorization from a bug report.
Use existing project tests and tools; no mandatory plan or state file is needed.

## 2. Establish fail-before evidence

Reproduce the failure with the smallest useful test or observation when feasible,
before modifying code. Record the command or observation method, inputs, relevant
environment and source identity, expected result, actual result, and evidence
location. A setup error or unrelated test failure is not reproduction evidence.

For authorized repair, add or update focused regression coverage when appropriate
and verify that it fails for the defect before implementing the correction when
feasible. Test observable behavior rather than mirroring the proposed patch.

If direct reproduction is unavailable, state why and what would enable it.
Use appropriate alternative evidence, such as a recorded failure, an isolated
check, or analysis of a violated invariant. Distinguish that evidence from a
reproduced failure. Proceed with repair only when authorization and evidence
justify the cause and correction; otherwise stop dependent repair and report
the next useful observation. Do not treat failure to reproduce as a fix.

## 3. Establish the cause

Trace the relevant execution path from the failing input through state changes,
boundaries, and error handling. Explain how the proposed cause produces the
observed failure and what supports or challenges competing explanations.
Separate confirmed causes from hypotheses; names and documentation alone do
not establish runtime behavior.

Use [Investigation](investigation.md) when a distinct deeper investigation is
needed, carrying existing evidence forward. Do not require a separate workflow
for routine diagnosis of a simple defect.

## 4. Make the justified correction

For an authorized repair, change the smallest scope that addresses the supported
root cause and preserves the intended contract. Avoid speculative fixes,
unrelated refactoring, and unnecessary dependencies. Keep user changes intact.
If appropriate regression coverage is omitted or cannot be added, explain the
reason, remaining risk, and alternative check.

## 5. Verify the affected behavior

Run the same targeted verification with the failing inputs after the correction,
under comparable conditions. Inspect the runtime result against the original
expectation. Explain relevant differences in inputs, environment, or checks;
do not present different checks as an equivalent fail-before/pass-after pair.

Check relevant edge cases, affected interfaces, and regression risks, plus all
mandatory project checks. Prefer the smallest reliable verification path over
unrelated broad suites. A patch, compilation, or unrelated passing test alone
does not demonstrate that the defect is fixed.

Apply Core's failed and unavailable check rules. If verification fails, revisit
the causal explanation instead of stacking speculative changes. If required
verification cannot run, stop dependent work and limit the conclusion to the
evidence available. Do not impose fixed retry counts. Use independent review
or additional agents only when risk justifies their cost and they are available
and authorized.

## 6. Report the outcome and limits

Report the expected and observed behavior, supported cause or remaining
hypotheses, and changes made, if any. Give exact fail-before and pass-after
commands or observation methods, input and version identities, relevant outputs
or statuses, and evidence locations. State explicitly when either half of that
comparison was not obtained.

List checks actually run, failed or unavailable checks, unresolved risks, and
the next action. Distinguish diagnosis, an applied correction, and verified
resolution in the exercised environment. For diagnosis-only work, finish with
findings and a proposed next step; do not automatically implement it.
