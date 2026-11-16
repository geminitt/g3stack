# Codex Adapter

g3stack is the authoritative source for these instructions. This adapter is
intended for a generated global `AGENTS.md` containing the approved Shared
Core and Owner Environment Restrictions.

## Instruction use

- When approved Core and Environment contents are embedded and supplied
  in context, apply them directly. Do not reread their source merely
  because an ordinary task starts. Recheck only when active instructions
  require it or needed content is missing, incomplete, or possibly stale.
  Follow Core's required-source rules; do not invent source paths.
- Apply the relevant project instructions supplied by Codex. Read an
  additional project `CLAUDE.md` only when the owner or applicable project
  instructions explicitly require it, or it is an explicit task input.
- Do not treat Markdown links or `@path` expressions as imports or proof
  that Codex loaded their targets.

## Skills

- Select `$task-router` through native Codex skill discovery when invoked
  or when its advertised scope fits. Read the selected `SKILL.md` from
  its discovered location unless its complete, current instructions are
  already available. Skill metadata alone is not the loaded body.
- Resolve a selected `SKILL.md` to its real filesystem path before
  resolving relative references, not from the target project's working
  directory.
- Repository availability does not establish global discovery. If a
  requested skill is unavailable, report that limitation instead of
  claiming its use.
