# g3stack goal ownership

Use this contract when the owner delegates a project outcome, rather than a
single bounded task. The active agent owns the accepted goal across all selected
skills and playbooks. The owner supplies goals, constraints and consequential
decisions; the agent chooses routine steps. No second controller is required.

1. Establish the accepted outcome, scope, constraints and success evidence from
   owner decisions and observed project state. An empty project needs no scaffold.
2. Choose the most consequential unresolved question or implementation gap.
   Select the matching full playbook or skill. Use Investigation, `g3-how` or
   `g3-why` for source questions; Prototype for a decision-changing observation;
   Feature/Bug fix/Refactoring for accepted engineering work; Eval/Hillclimb for
   an authorized experiment. Use `g3-figure-it-out` when no narrower workflow fits.
3. Execute the selected work and verify its actual artifact. Research and
   Engineering are modes, not compulsory sequential phases. Research may itself
   produce the accepted answer. An implementation can expose a research question.
4. Return the result, input identity, evidence, limitations and rejected
   assumptions to the project decision. A completed skill or passing unit check
   is not automatically completion of the project. Continue the next authorized
   action while the accepted goal remains open.
5. Before reporting completion, compare every accepted criterion with current
   evidence. Stop when the outcome is supported, or a concrete owner decision,
   required safeguard, resource or authorization boundary blocks further work.
   State the exact gap and next action; continue independent authorized work.

## A contradicted premise

A clear counterexample to an important premise is enough to reopen it. Do not
wait for the source principle's “two failed fixes” threshold. State the premise,
its falsifying observation and the decisions/artifacts that depend on it. Use
`g3-principle-attack-the-premise` to test it directly, then reopen only affected
work. Preserve valid unrelated results and negative evidence. Resume the goal
loop with the corrected premise rather than starting another blind patch cycle.

## Cross-skill continuation

For a delegated project goal, the Investigation playbook's “hand back to the
user” means return evidence to this loop and continue an already authorized
implementation. Ask only for a consequential unresolved decision. For a research-
only or plan-only request, honor that bounded deliverable and do not implement.
Likewise a PR, commit, merge, shipping step or unattended wake is not an implied
project completion criterion or permission.

Reuse the existing project record. At a consequential handoff retain the goal,
acceptance criteria, source/artifact identity, checked results and limitations,
rejected premises, open decisions, permitted next action and restrictions. A
transcript or prior success summary is a lead to revalidate, not current proof.
