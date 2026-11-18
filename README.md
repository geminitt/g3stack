# g3stack

A full pstack conversion for Codex, with g3stack's goal ownership across Research
and Engineering. It retains all 58 skills, 24 principle leaves, 22 playbooks,
both worker briefs, helpers, templates, fixtures, guide pages and MIT attribution.
The previous 16 condensed skills are superseded and archived.

Give the agent the goal and constraints; it chooses the steps and carries them
through to supported completion or a concrete decision/resource boundary.
Research and Engineering can alternate. A counterexample reopens only the
assumptions and artifacts it invalidates. No background service is implied.

```text
$g3stack Take this project from its current state to the accepted outcome.
$g3-help Explain which workflow fits this task.
$g3-how Investigate how this subsystem works, with source evidence.
$g3-architect Resolve the ownership and interface design before implementation.
```

## Reuse on another machine

The provided installer supports Linux/WSL and requires Python 3.11 or later.
Install Codex separately using its official instructions. No Python packages or
model/API calls are needed to clone, validate or install this distribution.

```sh
git clone https://github.com/geminitt/g3stack.git
cd g3stack
python3 -B scripts/convert-pstack.py --check
python3 -B scripts/manage-codex-integration.py plan
```

Review the plan's exact paths, global instructions and any conflicts. If you
approve that installation, copy its printed `plan_hash` into the command below:

```sh
python3 -B scripts/manage-codex-integration.py install --approve-plan PLAN_HASH
python3 -B scripts/check-codex-integration.py
```

Installation copies the personal agreements to the new machine's global
AGENTS.md and links the skills to this checkout. Review those agreements first
if the new machine needs different restrictions. Existing global instructions
are backed up; skill-name collisions and unsupported overrides block activation.
Keep the checkout at its installed path. In Codex, use `$g3stack` with your goal.
If the skill does not appear, start a new Codex session.

Local execution logs and deployment backups are excluded from Git. The complete
runtime, vendor resources, licenses and required test fixtures are included.

| Location | Responsibility |
| --- | --- |
| `codex/skills/g3stack/SKILL.md` | Full main workflow, adapted from poteto-mode |
| `codex/skills/g3stack/playbooks/` | Full task playbooks, selected when needed |
| `codex/skills/g3-*/` | Full specialist and principle skills, not summaries |
| `codex/CODEX.md` | Actual host, model, tool and authorization mappings |
| `codex/GOAL.md` | Goal ownership and Research ↔ Engineering recovery |
| `codex/provenance.json` | All 551 source-to-destination identities |
| `instructions/personal.md` | Sole global instruction source |
| `vendor/pstack/` | Untouched pinned original and author notice |
| `archive/pre-pstack-conversion/` | Superseded condensed library, recovery only |

[Distribution and limits](codex/README.md) · [Install/check/restore](docs/development.md)
· [Architecture](docs/architecture.md)

The dedicated installer exposes 58 native skills and a legacy `task-router`
compatibility alias, and retires only the 16 recognized old global symlinks.
The alias simply reads the full g3stack entry. It owns no routing policy.
The installer does not configure model/provider selection, install dependencies,
activate DevFlow, register custom agents or start Cursor automations.

Source: pstack 0.15.43, cursor/plugins commit
`2f87c854fe3e2fcda44ca86b46ede35aad3c46b7` (MIT, Lauren Tan).
Original files and upstream URLs remain attributed. DevFlow stays in the
historical vendor snapshot; it is not the active workflow base. Matt Pocock
skills are not included. Keep the full checkout available for relative resources.

Static retention, packaging and recovery checks do not establish native
fresh-session discovery, task performance or autonomous reasoning quality.
Conditional dependencies and unsupported source-host operations are documented
in [Codex execution mapping](codex/CODEX.md).
