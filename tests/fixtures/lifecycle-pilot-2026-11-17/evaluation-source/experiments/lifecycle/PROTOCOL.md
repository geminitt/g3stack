# Lifecycle pilot protocol

## Decision

Can a fresh Codex session pursue one bounded project goal, challenge an
incorrect research premise, implement and verify the resulting artifact,
use a scoped imported technique, and stop without step-by-step user steering?

This is a synthetic development pilot. It is not a general benchmark of
research quality or evidence that all real projects can run unattended.

## Task and provenance

The fixture is authored for g3stack and uses synthetic batch counts. Its
legacy research note incorrectly treats a mean of batch pass rates as the
pooled pass rate, regardless of batch size. The agent may reject this premise
before implementation; avoiding a predictable failure earns the same credit
as detecting and repairing it after a failed check. Do not force a bad fix
merely to manufacture a Research/Engineering transition.

The goal, CLI contract, public checks, initial state, and output schema are
fixed before the live run. A separate parent-owned scorer tests additional
inputs through the actual CLI. The agent must not inspect the parent scorer.
The parent retains hashes of the workflow snapshot and protected fixtures.

## Conditions

- `baseline`: the existing g3stack router snapshot.
- `candidate`: that same snapshot plus `project-lifecycle.md`.
- Both conditions receive the same task, reference techniques, execution
  tools, and acceptance criteria. The project instruction selects the guide.
- One candidate run is initially authorized, using the configured model and
  existing ChatGPT/Codex quota, with a total process deadline of 300 seconds.
- A baseline run or retry needs separate authorization. No comparative
  improvement claim can be made from the single candidate run.
- No API-key billing, installs, GPU work, commits, pushes, deployment, live
  service calls, or additional agents. Do not change global instructions.

## Acceptance and measurements

The parent scorer checks:

1. Actual CLI output against independent pooled-count calculations, Unicode
   group names, unequal batch sizes, and invalid or empty input.
2. The original goal and protected input/workflow bytes are preserved.
3. A1 is recorded as rejected with a concrete explanation and retained
   evidence; its dependent D0 decision is explicitly superseded/rejected.
4. The execution trace contains a completed public acceptance command and
   a read of the imported pstack verification technique.
5. The final structured result reports completion and no pending owner
   decisions. Plain-text questions and undeclared external actions still
   require manual trace review; a schema cannot certify their absence.

Record wall time, process exit/timeout, emitted token usage when available,
commands, changed files, and raw events. Do not invent USD cost, quota use,
or human-intervention counts that the trace cannot establish. An elapsed
deadline is a failed run, even if some output exists.

## Interpretation

Fixture regression tests validate the task/scorer and failure handling.
They do not validate agent behavior. A successful live run establishes this
one model/session/fixture combination. Resume behavior, automatic native skill
selection, independent reviewer quality, and other kits remain untested.

Any candidate instruction improvement discovered while inspecting this case
is development tuning. A later general comparison needs held-out tasks and
matched baseline/candidate runs with separately approved resource limits.
