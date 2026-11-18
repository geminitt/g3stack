# Codex execution mapping

Read this file once before following any g3stack procedure. Resolve the skill's
real directory first. This file translates the retained Cursor terminology; it
does not grant execution permission. Host instructions, current owner decisions,
project instructions and personal agreements govern every procedure and worker.
When an upstream example conflicts with this mapping, apply this mapping and
state a consequential limitation. Do not pass fields a tool does not accept.

## Tools and skill calls

| Source notation | Codex execution |
| --- | --- |
| `Read`, `Grep`, `Glob`, `Bash` | Available file tools or bounded shell commands; prefer `rg` for search. |
| `/skill-name`, bold skill names | Read the corresponding `g3-*` SKILL.md by its real path and follow it. For explicit owner invocation use `$g3-name`; the main entry is `$g3stack`. |
| Cursor Plan Mode, todo tool | Use the host plan tool if offered. Otherwise retain a short working plan in the existing project record or response; do not require a new state file. |
| `AskQuestion` | Use the available user-input tool, or a concise text question. Routine reversible choices proceed; important owner decisions and required authorization remain required. |
| `Task`, `Agent`, `Project worker` | Only an available and authorized native subagent tool. Pass supported fields only; send the complete goal, scope, source identity, acceptance checks and evidence destinations. |
| `poteto-agent` / `g3-agent`, `comment-sicko` | Worker briefs at `agents/g3-agent.md` and `agents/comment-sicko.md`, not registered Codex agent types. Read and include the relevant brief and `skills/g3stack/worker.md` when delegating. |
| `readonly`, `cloud`, `cloud_base_branch`, background flags | Describe allowed effects and exact source revision in the brief. These flags do not create isolation, remote machines or read-only tools in Codex. Use a real isolated worktree only when authorized and needed. |
| `/loop`, routines, cloud wakes | No emulation by unbounded sleep, detached shells, or nested `codex exec`. Continue in the active turn within the approved boundary. Report unsupported unattended scheduling. |

Use native discovery and actual tool schemas. Missing optional tools permit a
scoped direct approach. Required isolation, independent judging or cross-vendor
comparison cannot be silently replaced by self-review. Report the gap and stop
only dependent work. A serial same-model pass is not a multi-model panel.
Do not install companions automatically. `/deslop`, `control-cli`, `control-ui`,
Cursor `/create-skill`, Cursor Automations, Bugbot configuration, Grok Bot tools,
cloud agents and built-in PR tools are not supplied by this conversion. Use an
existing project harness or an equivalent discovered capability when adequate;
otherwise identify the unavailable result. Ordinary existing PR comments can be
reviewed with an authorized forge integration. A source checkout proves none of
these services is available.

## Models and provider costs

Keep the configured session model and effort. Native workers inherit by default.
The named Claude/Gemini models, role defaults, vendor fallback ladders, budget
levels and `.cursor/rules/pstack-models.mdc` in retained procedures are source-host
examples, not executable defaults on Codex. Do not send those slugs to Codex,
change model/effort/provider, write a global model rule or launch a paid job from
a playbook. Only use an explicitly authorized change supported by the current
host schema and verified provider/quota controls. A model rejection is a failed
capability check, not permission to try other providers.

For `g3-setup`, use its inventory, role mapping and proposal stages, but report
actual configured Codex capabilities instead of Cursor model slugs. Default all
roles to inheritance. Show any requested configuration change and its target
path before asking for activation authorization; do not write `.mdc` rules or
copy Cursor example configurations into `config.toml`.

## Authorization and scope

The source phrases “just do it”, “never ask”, “never block”, “ready PR”, automatic
commits, shipping, eval launches and external messages remain subject to the
owner's actual authorization. A playbook, worker brief, test command or user
request to investigate grants no extra installation, configuration activation,
spending, commit, push, deployment, deletion or messaging permission. An
unattended request does not expand scope or budget. Workers can and must surface
an unresolved owner decision or boundary to the coordinator; the coordinator
keeps working on independent authorized parts.

Preserve public compatibility unless its change was accepted. Cleanup, comment
removal, refactoring, lesson encoding and skill creation stay within the agreed
task. Do not remove useful comments, relax meaningful checks, broaden audits,
or edit global instructions because a source leaf suggests doing so. Keep the
source's actual procedures and verification criteria where compatible.

## Paths, history and skill authoring

- This directory is the converted distribution. Local sibling paths are the
  authority for bundled resources; upstream repository URLs are attribution or
  source references, not instructions to fetch another controller.
- `.cursor/skills/` maps to project `.agents/skills/`; user skills use
  `~/.agents/skills/`. A slash command in a generated artifact becomes a `$skill`
  invocation. Generated project skills need valid Codex frontmatter.
- `.cursor/rules/*.mdc`, plugin manifests and Cursor settings are not Codex
  configuration. Propose the smallest appropriate project instruction/skill
  change; global edits and activation still require owner authorization.
- Cursor transcript paths and guessed session slugs do not map to Codex history.
  Prefer current project records and supported session facilities. Read only
  authorized project/session history; never guess a “newest” transcript as proof
  of the current session. Revalidate the source, environment and artifacts.
- `agents/*.md` are full worker briefs, not auto-registered Codex agents. No agent
  configuration or global model/provider configuration is installed here.
- Preserve existing records and frozen evidence. Create a plan, verification
  skill or durable handoff when the task needs it, not to satisfy a template.

## Optional executable resources

All source scripts and fixtures are retained. Availability of a script is not
installation or a successful execution. Inspect its code and dependencies before
running it. No automatic downloads or bootstrap installs are authorized.

| Resource | Consequential requirements and limits |
| --- | --- |
| PR watcher under `skills/g3stack/scripts/` | Bun, locked dependencies, forge authentication and network. `bootstrap.ts` installs packages; do not run it without installation authorization. Use a bounded existing forge check when adequate. |
| `worktree-audit.sh` | Git inspection is reusable; its Cursor transcript lookup is not Codex session evidence. Never let that lookup authorize cleanup. |
| `g3-statechart/scripts` | Node, and Java/TLA+ or other tools required by the chosen operation. Missing dependencies block that operation, not all verification. |
| Video, browser/CDP, bot and formal-verification recipes | Inspect the selected recipe's actual runtime, network, credentials, resource fit and output effects. They are conditional, not installed services. |

Use the owner's package managers: pixi for Python/ML, mise for general runtimes,
apt for system packages when authorized. Never use `uv` or `uvx`, including a
source recipe that suggests them. Never expose credentials in evidence.

Describe static conversion checks separately from actual native discovery,
invocation, application verification, model quality and autonomous effectiveness.
