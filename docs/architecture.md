# Architecture

The active Codex agent owns the goal. g3stack supplies the full converted pstack
workflow, selected playbooks and specialist skills; it is not another agent
process and does not run a second DevFlow controller.

```text
Owner goal and constraints
  -> g3stack main entry + goal ownership contract
  -> matching full playbook / specialist skill
  -> source investigation / experiment / implementation
  -> verification on the actual artifact
  -> evidence and premise check
  -> next justified activity, accepted completion, or explicit boundary
```

`codex/GOAL.md` defines cross-activity continuation and premise recovery.
`codex/CODEX.md` translates Cursor terminology into supported Codex actions.
Neither is concatenated into global instructions. `instructions/personal.md`
remains the single global source. Existing owner and host policy governs every
skill, worker, model, external action and resource boundary.

The full source-derived procedure bodies are retained in `codex/skills/`.
`codex/provenance.json` accounts for every pinned pstack file. Source-only Cursor
metadata, automations and the Claude adapter are retained as context, not active
Codex services. Worker Markdown files are prompts, not registered agent types.
Native workers are optional and require real capability and authorization.

The 16 earlier summaries are archived and their owned user-scope links are
retired during migration. `task-router` is a compatibility pointer to the main
entry. It has no independent workflow or catalog. No runtime references select
the archived library or the DevFlow controller.

See [development](development.md) for integrity, installation and recovery.
Historical runs retain their original input identities and conclusions; they
are not validation of this new distribution.
