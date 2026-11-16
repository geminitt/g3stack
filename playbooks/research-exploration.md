# Research Exploration

Use this playbook to understand an unfamiliar problem, assess methods or
literature, or choose an approach when important uncertainty remains. It also
applies to an empty project with no requirements, architecture, code, or docs.
Apply [Shared Core](../instructions/core.md) and applicable project
instructions.

For a bounded factual question with a direct, adequately supported answer,
answer directly with appropriate verification. Do not expand it into this
workflow merely because the subject is unfamiliar.

## How to use

Scale the work to the decision and its risk. Skip irrelevant steps or parts
with a short reason; do not skip applicable Core safeguards. There is no fixed
number of alternatives, searches, or iterations, and no required planning,
state, or project documentation file. Report findings in the response unless
the task calls for another deliverable.

Exploration assesses evidence and proposes a decision. Experimental execution
generates new empirical evidence; implementation changes the project. Treat
either as a distinct stage only when it is within the authorized task scope.

## 1. Frame the decision

Identify the user's goal, expected result, constraints, known facts,
assumptions, and important unknowns. Separate owner decisions from tentative
ideas. Define useful evidence and criteria for choosing an approach. Ask only
about missing decisions that affect the next action; continue independent
work.

## 2. Inspect existing context

Inspect relevant existing instructions, decisions, documentation, code, and
observations before proposing a project structure. Reuse what is applicable.
If the project is empty, state that and continue from the user's question;
do not invent requirements or create scaffolding merely to begin exploration.

## 3. Gather and assess evidence

Investigate the unknowns that could change the decision. Prefer primary sources
and reproducible observations. For each material finding, keep a source or
observation reference and enough input, version, or date context to assess it.
Check relevance, source quality, freshness, and conflicting evidence.
Distinguish documented claims from observed behavior; identify what has not
been exercised.

Bound the search by the decision criteria and any agreed resource limits.
Revisit the question when new evidence changes its premises. Stop searching
when evidence is sufficient, further search is unlikely to change the decision,
or a material access, authorization, or resource limit prevents progress.
Do not treat a search limit as proof.

## 4. Compare and recommend

Compare plausible approaches against explicit, task-relevant criteria, such as
fitness for the goal, evidence strength, complexity, cost, and reversibility.
Include reuse or no change when plausible. Do not invent alternatives to fill
a quota; explain when only one approach merits consideration.

Recommend the simplest approach justified by the evidence. State the tradeoffs,
assumptions, and what evidence could change the recommendation. If evidence
is insufficient, narrow the conclusion and identify the unresolved decision
instead of forcing a recommendation.

## 5. Propose a test only if needed

Skip the experiment proposal when existing evidence supports the decision.
If a consequential unknown requires empirical testing, propose the smallest
useful experiment: the question, representative inputs, comparison,
measurable decision rule, resource bounds, and stopping condition. Explain
how each possible outcome would affect the decision. Do not propose a test
that cannot resolve the gap.

Keep the proposal distinct from execution. Hand off to Research Experiment
or Prototype as appropriate; do not assume a separate playbook exists or start
an experiment or implementation merely because it was recommended.

## 6. Verify and close

Check that material conclusions are supported by the cited evidence, comparison
criteria address the user's goal, and unresolved assumptions do not invalidate
the recommendation. Report any failed or unavailable checks and their effect.
Finish when the requested answer is supported or the evidence limit is clear;
stop dependent work when a required source, safeguard, or owner decision is
unavailable. State what would permit progress.

Provide a concise answer with the goal and scope, relevant context, key findings
and sources, approach comparison when applicable, recommendation or evidence
gap, checks performed, limitations, and next decision. Include a test proposal
only when needed. State skipped parts briefly; a direct answer does not require
an exploration report. Do not claim experimental or implementation success
from exploration alone.
