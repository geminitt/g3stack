# Research Experiment

Use this playbook for an experiment design, hypothesis test, or empirical
comparison that can inform a decision. Apply
[Shared Core](../instructions/core.md) and applicable project instructions.

For a design-only request, provide an actionable protocol and stop before
running measurements. Execute only within the authorized task scope, subject
to Core's environment, paid-job, and consequential-execution requirements.
Do not assume GPU, cloud, paid services, or external data are available.

Scale the protocol to the question and risk. Skip irrelevant parts with a
short reason without relaxing Core. Do not require fixed numbers of trials,
methods, or metrics, new infrastructure, or planning and state files.

## 1. Define the question and decision

Inspect relevant existing context and evidence. State the research question,
testable hypothesis, plausible competing explanations, and measurable outcome.
Identify the decision that the experiment could change and what result would
support, challenge, or leave the hypothesis unresolved.

## 2. Select inputs and comparisons

Define a relevant baseline or reference condition; add a control when useful
to distinguish competing explanations. Identify representative data or cases,
their provenance, sampling method, coverage, and possible selection bias.
Identify the unit being measured and important confounders. Reuse suitable
available inputs rather than requiring a new dataset or project structure.

If the available inputs cannot support the intended claim, narrow the question
or stop dependent execution and state what is missing. Do not substitute
convenient cases without explaining how that limits the conclusion.

## 3. Specify the smallest useful protocol

Choose the smallest experiment that can resolve the decision-relevant unknown.
Before execution, define the procedure, metrics, acceptance criteria, and
meaningful uncertainty: what variation or measurement error could change the
decision? Use repetitions or statistical analysis only when the conclusion
requires them; explain what the chosen design cannot establish.

Prevent leakage between tuning and evaluation. When applicable, separate
exploratory tuning inputs from held-out evaluation inputs, and fix the method
and evaluation protocol before examining held-out results. Evaluate comparisons
under comparable conditions. If results guide further tuning, treat them as
exploratory and obtain independent evaluation before making held-out claims.
Report any limitation that prevents a reliable comparison.

## 4. Set bounds and check readiness

Define the execution venue, required resources, time and cost bounds, completion
criteria, and stopping conditions before running. Confirm authorization covers
the intended execution and that required data, environment, checks, and output
locations are available. Apply Core's execution and recovery safeguards.

Stop dependent execution if a prerequisite is missing, an approved limit is
reached, or the protocol cannot yield valid evidence. Report the blocker and
smallest next action; do not silently expand the run or replace the protocol.
For design-only work, report unperformed readiness checks as open; do not run
measurements merely to verify the plan.

## 5. Execute only when authorized and retain evidence

Run the agreed protocol within its bounds. Record relevant versions, exact
input identities, parameters, commands, environment details, and seeds when
randomness matters. Retain raw outputs, logs, failures, and deviations needed
to reproduce and interpret the measurements. Use existing artifacts or a
compact record appropriate to the task, not a mandatory new documentation
system. If reproduction is limited, explain why.

Check required outputs and artifacts for completeness before analysis. Do not
accept an incomplete or uncertain run as successful evidence. After a partial
run, identify completed measurements, missing work, and whether any subset
still supports a narrower conclusion.

## 6. Analyze and report

Compare observed results with the baseline and predefined criteria. Assess
competing explanations, uncertainty, bias, and protocol deviations; distinguish
observations from interpretations. Report negative, failed, inconclusive, and
partial results without changing the success criteria after seeing them.

For design-only work, deliver the protocol, rationale, resource and authorization
needs, readiness checks still open, and stopping conditions; report no measured
outcome. For executed work, report the protocol actually used, evidence
locations, measurements, checks, limitations, and resulting decision or remaining
uncertainty. Separate run completion from hypothesis support. Do not generalize
beyond the exercised data and conditions or continue into implementation unless
that stage is also authorized.
