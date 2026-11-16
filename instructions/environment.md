# Owner Environment Restrictions

These restrictions apply to the owner's WSL environment and compute services.
Use with Shared Core. They do not authorize installation, execution,
commits, or pushes.

## Toolchain

- MUST NOT install or use `uv` or `uvx`, including through a tool backend.
- Use apt for system packages, mise for non-Python runtimes and general CLI
  tools, and pixi for project Python and ML environments. Select the
  appropriate layer before installing anything.
- Shared ML CLI tools such as `hf`, `modal`, and `kaggle` belong in
  `pixi global` from conda-forge. Expose only the commands needed. Python
  libraries imported by a project belong in that project's environment.
- MUST obtain explicit approval before an action that requires sudo.

## Compute

- Verify current hardware capacity, available memory, provider features,
  prices, quota rules, and stop/log capabilities before relying on them.
  Historical environment figures are not current verified facts.
- Select GPU execution using verified resource fit, current provider rates
  and quota rules, and owner authorization. Apply Core's paid-job approval
  and spending controls. Among suitable, authorized venues, assign the
  heaviest GPU jobs to external platforms first.
- Use the local GPU only when memory and acceptable runtime fit the job.
  Jobs that cannot fit locally MUST NOT fall back to the laptop when
  external venues are busy.
- Use representative runtime measurements when feasible; report the
  measured runtime and its basis. Otherwise, report timing uncertainty
  and the measurement needed;
  do not invent an estimate. Before a long local GPU run, MUST establish
  acceptable runtime from representative timing evidence. Uncertainty
  alone does not authorize that run; propose an authorized, bounded
  measurement when needed.
- Before a GPU job, perform feasible local checks, including a small
  real-model test when it fits. If a path cannot run locally, record why
  and what remains unverified, then verify it on the approved target.
- Before submitting a Kaggle GPU job, MUST obtain the owner's remaining
  quota and verify the current charging rules. Do not submit with unknown
  remaining quota.

## Version-control authorization

Commits and pushes require separate authorization. Authorization for either
does not imply authorization for the other. Updating shared tooling or its
manifests does not authorize a commit, push, or Git remote change.
