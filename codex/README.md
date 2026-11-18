# g3stack for Codex

A full pstack-derived skill distribution adapted for Codex and g3stack's
Research–Engineering goal ownership. Start with `$g3stack` and a project goal;
use `$g3-help` for the catalog. The agent selects the detailed playbooks.

- `skills/`: all 58 converted upstream skills, including 24 principle leaves.
- `skills/g3stack/playbooks/`: all 22 playbooks and original helper resources.
- `CODEX.md`: authoritative host translation and execution boundaries.
- `GOAL.md`: g3stack's goal ownership and premise recovery contract.
- `agents/`: both worker briefs, supplied as prompt resources.
- `provenance.json`: every original file, destination and content identity.
- `LICENSE`: original MIT notice. Source attribution is retained throughout.

Source: pstack 0.15.43, cursor/plugins commit
`2f87c854fe3e2fcda44ca86b46ede35aad3c46b7`.
The untouched original is `../vendor/pstack/`. `docs/upstream-readme.md`,
`docs/harness/claude-code.md`, `automations/` and `upstream/` preserve source-host
context; they are not a second runtime adapter or activated Cursor service.
Read `CODEX.md` before following a recipe with Cursor terminology.

This conversion preserves full procedure bodies and resources. It changes names,
relative skill references, supported metadata and host interpretation. It does
not shorten the workflows into summaries. Source fixtures and executable helper
code remain byte-identical. Main goal ownership is the explicit g3stack addition.
Native skill catalogs can shorten descriptions when their metadata budget is
exhausted. The main entry resolves sibling procedures directly by path.
Native workers, providers, formal tools, browsers, watchers and unattended wakes
remain conditional on actual capabilities and owner authorization.

Regenerate source-derived files with `python3 -B scripts/convert-pstack.py` from
the repository root. Check retention with `python3 -B scripts/convert-pstack.py
--check`. The three local files CODEX.md, GOAL.md and this README are maintained
separately. Installation is a separate reviewed transaction; see the root README.
