# Development and integration

## Install or verify Codex integration

From the repository root:

```sh
python3 -B scripts/manage-codex-integration.py plan
```

Review the exact plan and obtain authorization for its changed global paths.
Then use its printed fingerprint:

```sh
python3 -B scripts/manage-codex-integration.py install --approve-plan PLAN_HASH
python3 -B scripts/check-codex-integration.py
```

The hash is a state check, not authorization. The installer preserves recovery
artifacts and does not commit or push. It links the compatibility alias plus all 58 full
`codex/skills/` directories into `~/.agents/skills/`, refusing collisions, disabled
members and changed plans. The sole global source is
`instructions/personal.md`; the installer copies its raw bytes without
concatenating Core or host adapters. Generated host candidates are deployment
copies, not independent policy. Codex mapping, goal contract and skill changes affect conditional
procedures and still require relevant checks and authorization.

After an approved personal-source edit, regenerate candidates from one source:

```sh
cp instructions/personal.md integrations/codex/AGENTS.generated.md
cp instructions/personal.md integrations/claude-code/CLAUDE.generated.md
```

The Codex installer also regenerates its candidate during installation. Claude
activation remains separately authorized and is not performed by that installer.

For a global installation rollback, use the installer-reported backup path:

```sh
python3 -B scripts/manage-codex-integration.py restore --backup BACKUP_PATH
```

Restore refuses intervening destination edits. It restores managed global
resources, not repository sources. Because the router follows this checkout,
a full instruction migration rollback also needs the matching source snapshot.
The current migration's verified source archive and recovery instructions are
in the relevant migration record. For the skill-library migration, restore the
installer backup **before** reverting source: the current manager understands
the added skill-link roles. Then apply its matching source rollback patch.
Local migration receipts are kept under the ignored `runs/` directory.
They are specific to the machine where activation occurred.

## Source and runtime checks

```sh
python3 -B scripts/convert-pstack.py --check
python3 -B kits/engineering/check.py
python3 -B scripts/test-engineering.py
python3 -B scripts/test-codex-integration.py
python3 -B scripts/test-library.py
# Optional: installed Codex CLI, temporary HOME, no model call
python3 -B scripts/check-native-skills.py
python3 -B scripts/test-capabilities.py
python3 -B scripts/test-handoff.py
python3 -B scripts/test-lifecycle-eval.py
```

The source check validates the one shared tree in `vendor/` against its
manifest. It does not establish model quality or target-system behavior.
Keep upstream bytes, resources and licenses together; do not prune a
component without reviewing its dependencies and updating the manifest.

Use `python3 -B` or per-process `PYTHONDONTWRITEBYTECODE=1` for bundled helpers.
Keep generated output outside the vendor tree. Optional OCR, browser,
Graphviz, Bun or formal-verification tools are not installed by g3stack.
Their absence remains a limitation on dependent execution.

The [capability helper](capability-integration.md) and
[handoff helper](handoffs.md) are optional developer tools, not mandatory
runtime stages. The converted library shares resources and requires the complete checkout;
use its dedicated installer rather than the generic single-folder helper.

## Full pstack conversion

The source conversion is reproducible with `scripts/convert-pstack.py`. Every
one of 551 original files has an attributed destination. Tests independently
reverse the skill-identity translation and compare complete procedure bodies;
helpers, fixtures and assets retain their original bytes. `CODEX.md`, `GOAL.md`
and the distribution README are the three locally maintained additions.

Activation retires only old symlinks pointing to this checkout's 16 former
`skills/g3-*` directories. A foreign file, directory or link blocks migration.
The old source is retained in `archive/pre-pstack-conversion/skills/`.
For a full rollback, restore the recorded global transaction first, then restore
its matching `before.tar.gz` source snapshot and remove only new paths recorded
by that conversion. Restoring global links alone does not revert source content.
Keep the newer manager available until all added roles have been restored.

Native skill metadata is not evidence that a model followed a procedure. The
current lifecycle scorer is a guided development fixture, not a fresh unguided
agent test. Archived pilot results apply only to their frozen source snapshots.

## Portable source and local evidence

The GitHub repository contains the complete current runtime, pinned upstream
sources, licenses, tests and installation tools. Keep the checkout available
at the path used for installation because native skills resolve its resources.

`runs/`, `experiments/` and superseded local assessments are excluded from Git.
They retain this machine's logs, recovery archives and activation receipts.
Do not copy old deployment backups onto another machine as an installation
method. Clone the source and use the guarded installer with that machine's HOME.

The frozen historical evaluator inputs used by the regression suite are retained
byte for byte under `tests/fixtures/lifecycle-pilot-2026-11-17/`. Its manifest
records only their original source identities. It omits historical machine paths
and deployment state. These inputs establish neither current agent performance
nor an installed configuration on another machine.

The current fixture's `baseline` label does not recreate the pre-activation
control. A new comparative evaluation needs explicit frozen comparison
conditions and separately authorized model resources. Prepare/score commands
make no model calls; a run flag never supplies user authorization.
