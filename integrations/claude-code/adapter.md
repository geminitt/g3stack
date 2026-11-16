# Claude Code Adapter

g3stack is the authoritative source for these instructions.

## Instruction use

- Claude Code loads user instructions from `~/.claude/CLAUDE.md` by default
  and applicable project `CLAUDE.md` files. Apply instructions actually
  supplied by the host; a path alone does not establish that a file loaded.
- Apply embedded Core and Environment directly. Do not reread their sources
  at each task start; follow Core's rules for missing or possibly stale content.
- Apply existing project instructions and their native imports. In g3stack,
  project `CLAUDE.md` uses `@AGENTS.md` to import its project instructions.
  Native relative imports resolve from the importing file. Markdown links
  are references, not imports; code spans keep import examples literal.

## Shared workflows

- Select the shared Task Router when invoked or when its advertised scope
  fits. Its default personal discovery path is
  `~/.claude/skills/task-router/SKILL.md`; the skill directory can be a symlink
  to g3stack's shared source. Invoke it as `/task-router`. If
  `CLAUDE_CONFIG_DIR` is overridden, verify the active personal location.
- Repository availability or a Codex skill installation does not establish
  Claude discovery. Read the selected skill's complete body unless its current
  instructions are already available. If discovery or access fails, report it
  and follow Core's unavailable-source rules; do not claim invocation.
- Resolve the selected `SKILL.md` to its real filesystem path before resolving
  Core or playbook references. Follow the Router's conditional playbook reads
  from that source directory, preserving its direct-answer bypass.

## Permissions and compatibility

- Markdown instructions guide behavior; Claude Code's permission system and
  host restrictions enforce access. Neither tool approval nor skill invocation
  expands Core's authorization for edits, installation, remote execution,
  commits, or pushes. Commits and pushes remain separately authorized.
- Use the current Claude Code tool schemas. Report unsupported capabilities
  rather than assuming Codex tool names or permission mechanisms apply.
- Third-party workflow plugins, including Superpowers, can add instructions.
  Do not assume they cooperate with Task Router. Resolve conflicts through
  Core before dependent action; do not change plugin configuration implicitly.
- Do not claim native loading, skill invocation, or runtime effectiveness
  from artifact review alone. Report only session behavior actually verified.
