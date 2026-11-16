---
name: task-router
description: Route a Research or Engineering request to direct execution or a minimal workflow. Use when the user invokes $task-router or asks to select an approach for a task.
---

# Task Router

Select the smallest suitable procedure, then perform only the work the user
requested. A routing or planning request alone does not authorize execution.

## Governing instructions

Apply [Shared Core](../../../instructions/core.md) and the applicable project
instructions. Resolve this link relative to this skill's directory, not the
target project's working directory. Read Core if its complete, current content
is not already available. If this required source is unavailable, report the
limitation and stop dependent execution. Routing does not grant permissions
or override Core, owner decisions, or project requirements.

## Understand the task

Identify the user's goal, expected result, scope, relevant project context,
and existing acceptance criteria. Inspect only what is needed to resolve
material uncertainty. Ask about missing owner decisions when they affect
the next action; continue independent authorized work.

For a clear, bounded task with an obvious procedure and suitable checks,
proceed directly. Do not require a workflow label, elaborate plan, or planning
file. The direct path still follows Core and project safeguards.

## Select a workflow when needed

Prefer one workflow based on the requested result. These are routing categories,
not claims that separate playbooks or skills are installed.

| Workflow | Select when | Minimal procedure and evidence |
|---|---|---|
| Investigation | The user needs an explanation of unclear behavior, a cause, or a constraint. | Inspect relevant artifacts, test a hypothesis where possible, and report supported findings and unknowns. Do not infer repair authorization. |
| Research Exploration | The user needs to explore a question, literature, methods, or competing approaches. | Bound the search, compare relevant primary sources, and identify evidence gaps and the next decision. Do not infer experiment authorization. |
| Research Experiment | The user needs an empirical comparison or hypothesis test. | Define the hypothesis, baseline, protocol, and metric; run the authorized measurement; retain input identities, results, and limitations, including negative or unreliable results. |
| Prototype | The user needs a small proof of feasibility under uncertain assumptions. | Build and exercise the smallest representative slice; report observed feasibility and limitations without claiming production readiness. |
| Feature Development | The user needs new or changed behavior with observable acceptance criteria. | Establish acceptance, implement the behavior, and verify affected behavior and relevant regressions under project requirements. |
| Bug Fix | Existing behavior violates an intended contract and repair is requested. | Reproduce the failure, establish its cause, make a focused repair, and show the regression check failing before the repair and passing afterward. |
| Refactoring | The user needs structural improvement while preserving the behavior contract. | Identify invariants, change the structure, and verify those invariants and relevant regressions. |

When Investigation is selected, resolve this `SKILL.md` to its real
filesystem path, then resolve the
[shared investigation playbook](../../../playbooks/investigation.md)
relative to that file's parent directory. Read the complete playbook before
applying the workflow. Do not resolve it from the global symlink location or
working directory. If it is unavailable, report the limitation and stop
dependent investigation. Do not load it for direct answers or unrelated
workflows.

When Research Exploration is selected, resolve this `SKILL.md` to its real
filesystem path, then resolve the
[shared playbook](../../../playbooks/research-exploration.md) relative to that
file's parent directory. Read the complete playbook before applying the
workflow. Do not resolve it from the global symlink location or working
directory. If it is unavailable, report the limitation and stop dependent
exploration. Do not load it for direct answers or unrelated workflows.

When Research Experiment is selected, resolve this `SKILL.md` to its real
filesystem path, then resolve the
[shared experiment playbook](../../../playbooks/research-experiment.md)
relative to that file's parent directory. Read the complete playbook before
applying the workflow. Do not resolve it from the global symlink location or
working directory. If it is unavailable, report the limitation and stop
dependent experimental work. Do not load it for direct answers or unrelated
workflows.

When Bug Fix is selected, resolve this `SKILL.md` to its real filesystem
path, then resolve the
[shared bug-fix playbook](../../../playbooks/bug-fix.md) relative to that
file's parent directory. Read the complete playbook before applying the
workflow. Do not resolve it from the global symlink location or working
directory. If it is unavailable, report the limitation and stop dependent
bug-fix work. Do not load it for direct answers or unrelated workflows.

Combine workflows only when the task requires distinct stages with separate
results or dependencies. State their order, handoff evidence, and checks
required before dependent work. Do not add a separate stage merely because
a workflow includes some investigation or implementation.

If no category fits, construct a minimal task-specific procedure: the intended
result, necessary actions, suitable verification, and a completion or stop
condition. Use relevant existing guidance when available; missing optional
workflows do not block ordinary work. Do not create or assume additional
playbooks, skills, or agents merely to route the task.

## Verify and report

Select verification from the expected result, actual effects, risk, and project
requirements. Use the least costly check that can challenge each material claim,
plus all mandatory project checks. The workflow table suggests evidence types;
it does not replace project acceptance or Core's failed-check rules.

For non-trivial work, briefly explain the selected workflow or custom procedure
and its verification before proceeding. Continue within existing authorization;
if only routing or planning was requested, stop after the proposed procedure.

Report the result, checks actually performed, evidence locations, failed or
unavailable checks, and remaining limits. Distinguish a selected procedure from
an executed task, execution from goal achievement, and static review from
verified behavior. Follow Core's communication requirements.
