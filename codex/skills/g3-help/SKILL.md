---
name: g3-help
description: Guides users through pstack setup, $g3stack, and picking the skill, playbook, or principle for a task. Type $g3-help with a question.
---

Read [Codex execution mapping](../../CODEX.md) before following this
procedure. It governs source-host tools, models, permissions and paths.


# Poteto help

Answer the user's question about pstack, hand them a prompt they can send, and link the file the answer came from. For a help question, don't start the work. The user asked how, and a pstack run spends real tokens, so let them send the prompt.

A message that asks for work, such as "use pstack to fix this bug", is not a help question. Read [`g3stack`](../g3stack/SKILL.md), do the work under it, and mention once that a Custom Mode keeps it on.

This file maps questions to the skills and guide pages that hold the answers. Those files own the details. Read the file you route to before you quote it, and trust it when it disagrees with this map. The links here point into the installed plugin, which the user may not be able to open, so give the user the file's public copy: `https://github.com/cursor/plugins/blob/main/pstack/` followed by its path.

## Find out what they need

Infer the need from the message and the conversation. A named situation, such as "which skill reviews a PR?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick:

- Get set up
- Start a task with `$g3stack`
- Pick a skill for a situation
- Fix a run that went wrong
- Make pstack my own

Check the state that changes the answer, and mention it only when it does:

- No `~/.cursor/rules/pstack-models.mdc` means `$g3-setup` hasn't run for this user, so every role uses its default model.
- No `verify-*` skill or other app harness in the project means agents have no scripted way to drive the app. Mention `$g3-create-verification-skill` when the question is about proving a change works.
- No formal verification skill in the project means no property is checked past what tests reach. Mention `$g3-create-formal-verification-skill` when the question is about a race, an invariant, or another case tests rarely hit. When one exists and the code it covers changed after the commit it records as last in sync, mention `$g3-maintain-formal-verification-skill` if the question touches that code.

When the model rule is missing and it matters, ask whether the user wants to pick a model for each role and a reasoning budget now. It matters when the user is new, the question is about setup or cost, or the answer depends on which models run. Ask at most once per chat. If the need is also unclear, ask both questions together. Offer two choices:

- Now: give them `$g3-setup` to type, and answer their question too.
- Later: answer their question, and add one line saying every role keeps its default model until they run `$g3-setup`.

## Get set up

1. Install with `/add-plugin pstack` in chat, or from Customize in the sidebar.
2. Run [`$g3-setup`](../g3-setup/SKILL.md). It asks for a reasoning budget, maps a model to each role, and writes a rule. The rule applies to new chats. Then it offers once each to generate a verification skill and a formal verification skill for the project, unless the project already has one.
3. Start a real task with `$g3stack`, a goal, and a check that can pass or fail.

Installing changes nothing until the user invokes a skill. Only `$g3-setup` loads from the user's words. The [README](../../README.md) and [guide page 1](../../docs/guide/01-setup.md) have the details. Offer to word their first prompt with them, per [`references/prompting.md`](references/prompting.md).

If cost is the worry, say where the tokens go and how to spend fewer. pstack spends extra tokens on subagents and review panels. Rerun `$g3-setup` and pick a smaller budget or cheaper models. A role set to `auto` or `inherit-parent` runs on the chat's model, which saves tokens when the chat runs on Auto or a cheaper model. A shorter panel list runs fewer subagents, one for each entry. Save `$g3stack` for work that needs rigor.

pstack is built for Cursor, and it also installs in Claude Code with `/plugin marketplace add cursor/plugins`, then `/plugin install pstack@cursor-plugins`. There, each command takes a `pstack:` prefix, such as `/pstack:g3stack`. The [Claude Code adapter](../../docs/harness/claude-code.md) maps the Cursor names, and a step that needs a Cursor-only feature, such as Bugbot or Automations, is skipped with a one-line note.

Other tools can read the skills, because they use the Agent Skills format. But most workflow skills, including `$g3stack`, `$g3-how`, and `$g3-teach`, spawn Cursor subagents, some with per-role models, and Custom Modes and `/loop` are Cursor features, so those parts may not work there.

## Start a task with `$g3stack`

`$g3stack` matches the task to a playbook, copies the playbook's steps into the todo list, and runs the other skills as the steps need them. A good prompt states the goal and how to tell it's done. It doesn't list skills, because a hand-written sequence tends to drop or reorder steps the playbook would keep. Read [`references/prompting.md`](references/prompting.md) before you help word one. [Guide page 2](../../docs/guide/02-g3stack.md) has examples.

Whether `$g3stack` stays on depends on how the user starts it:

- Enter on `$g3stack` attaches the skill to one message. It fades as the chat moves on.
- Option+Enter on Mac or Alt+Enter on Windows, or Use as Mode from the skill entry, makes it a Custom Mode. It stays in context every turn until the user exits the mode, and it stays out of casual turns.
- Cursor's docs list Custom Modes in the Agents Window and the CLI. Elsewhere, start each new task with `$g3stack`.

Link [Cursor's skills docs](https://cursor.com/docs/skills) when this comes up. Mid-chat, "new task" makes the mode match a fresh playbook. `$g3stack` already uses `g3-agent` for the subagents its playbook steps spawn. To get the same style from a subagent of your own, spawn it with `subagent_type: "g3-agent"`.

## Pick a skill

The default answer is `$g3stack`, which runs most of the others when its steps need them. Name a skill directly when the user wants more or less of something than the playbook gives. Read the skill before you recommend it, and give one example prompt.

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`$g3stack`](../g3stack/SKILL.md) |
| Check that the agent understood their goal and the problem before it starts | [`$g3-in-your-own-words`](../g3-in-your-own-words/SKILL.md) |
| Get a prompt rewritten deeper, not bigger, before sending it: what a top professional would add, their raw material and methods, and an outside check. It returns the prompt and doesn't do the task | [`$g3-sharpen`](../g3-sharpen/SKILL.md) |
| Know how code works now, or where new code should live | [`$g3-how`](../g3-how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`$g3-why`](../g3-why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`$g3-teach`](../g3-teach/SKILL.md) |
| Catch up on their own recent work on a topic | [`$g3-recall`](../g3-recall/SKILL.md) |
| Catch up on what changed in this chat since their last message, in plain words and small visuals, with every item waiting on them listed and decidable from the reply alone | [`$g3-ketchup`](../g3-ketchup/SKILL.md) |
| Catch up like `$g3-ketchup`, in a short subtitled video of slides, with the waiting calls as text under it | [`$g3-ketchup-video`](../g3-ketchup-video/SKILL.md) |
| Know what a small diff could break outside itself | [`$g3-blast-radius`](../g3-blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`$g3-architect`](../g3-architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`$g3-arena`](../g3-arena/SKILL.md) |
| Run parallel checks over slices, or race workers, as cloud agents | [`$g3-swarm`](../g3-swarm/SKILL.md) |
| Have different models review a diff and try to break it | [`$g3-interrogate`](../g3-interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`$g3-tdd`](../g3-tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`$g3-typescript-best-practices`](../g3-typescript-best-practices/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`$g3-no-comments`](../g3-no-comments/SKILL.md) |
| Clean AI tells out of prose | [`$g3-unslop`](../g3-unslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`$g3-technical-writing`](../g3-technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`$g3-bro`](../g3-bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`$g3-create-verification-skill`](../g3-create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`$g3-maintain-verification-skill`](../g3-maintain-verification-skill/SKILL.md) |
| Formally verify a race, invariant, or other property that tests rarely reach | [`$g3-create-formal-verification-skill`](../g3-create-formal-verification-skill/SKILL.md) |
| Bring a formal verification back in line after the code it covers changed, and learn whether a failure is drift or a bug | [`$g3-maintain-formal-verification-skill`](../g3-maintain-formal-verification-skill/SKILL.md) |
| Show a PM or designer what the user sees as a chart checked by a TLA+ model, with the shortest path to each state that breaks a rule | [`$g3-statechart`](../g3-statechart/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`$g3-benchmark-checklist`](../g3-benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`$g3-figure-it-out`](../g3-figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`$g3-show-me-your-work`](../g3-show-me-your-work/SKILL.md) |
| Pick a model for each role and a reasoning budget | [`$g3-setup`](../g3-setup/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`$g3-automate-me`](../g3-automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`$g3-reflect`](../g3-reflect/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`$g3-correct`](../g3-correct/SKILL.md) |
| Build a page whose buttons wake a Grok Bot over a webhook | [`$g3-make-bot-ui`](../g3-make-bot-ui/SKILL.md) |
| Find their way around pstack | `$g3-help` |

If a skill directory next to this one is missing from the table, read its frontmatter and route by its description. The `g3-principle-*` directories are covered under principles below.

Close calls:

- `$g3-how` explains what the code does. `$g3-why` explains the reasons. `$g3-teach` runs one or both and explains the result plainly.
- `$g3-arena` gives every worker the same brief and merges the best parts. `$g3-swarm` splits work into slices or a race and returns one report.
- `$g3-interrogate` reviews the diff. `$g3-blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `$g3-recall` rebuilds context across recent chats. `$g3-ketchup` covers only this chat since the user's last message. Resuming one specific chat or branch is the Session pickup playbook.
- `$g3-figure-it-out` designs one rigorous run. The Autonomous run playbook drives one task to a finish condition.

Not in pstack:

- `/deslop`, `control-cli`, and `control-ui` ship in the `cursor-team-kit` plugin.
- `/loop` and `/create-skill` are Cursor built-ins.
- pstack has no `/orchestrate` skill. If the slash menu shows `/orchestrate`, another plugin provides it.

## Playbooks and principles

Playbooks are step lists inside `$g3stack`, not skills, so they have no slash command. Inside `$g3stack`, describing the task picks one, and these phrases name one directly:

- "babysit this pr" or "check on pr 123" runs Babysit. It drives the PR to merge-ready and stops there. It doesn't merge unless the user asks to merge, land, or ship.
- "land the stack" runs Shipping.
- "take over this branch" runs Session pickup.
- "pause safely" runs Pause safely.
- "full autopilot on this queue" runs Autopilot-full. "autopilot, don't merge" runs Autopilot-stack.
- "run the eval playbook" runs Eval.

Without `$g3stack`, a phrase such as "babysit this pr" can start Cursor's own skill for the same job instead. The Playbooks section of [`g3stack`](../g3stack/SKILL.md) lists every playbook. [Guide page 6](../../docs/guide/06-verify-and-ship.md) covers opening, babysitting, and landing a PR.

pstack has no planning skill. Cursor's Plan Mode works alongside it. For work that spans phases or stacked PRs, asking `$g3stack` for a plan runs the [Multi-phase plan playbook](../g3stack/playbooks/multi-phase-plan.md), which writes the plan and doesn't implement it. For a design question, the Prototype playbook or `$g3-architect` settles it in code first.

Principles are one-rule skills that `$g3stack` reads and cites in its replies. The user rarely invokes one. They steer with the names instead, as in "apply prove it works. show me the real output." Typing `/g3-principle-<name>` still loads one on demand. [Guide page 8](../../docs/guide/08-principles.md) lists them.

## Fix a run that went wrong

| Symptom | Fix |
|---|---|
| The mode stopped applying after a few turns | It was started with Enter. Start it as a Custom Mode, or start each task with `$g3stack`. |
| A question got treated as the next step of the last task | Say "new task", or say the turn doesn't need the mode. |
| A new model choice had no effect | The rule from `$g3-setup` applies to new chats. Start one. |
| Runs cost more than expected | See the cost paragraph under Get set up. |
| A skill didn't load on its own | Only `$g3-setup` loads from the user's words. The others load when the user types them or when `$g3stack` runs them, and it doesn't run every skill. |
| Parallel agents overwrote each other | Give each agent its own worktree, or run them as cloud agents, which each get their own machine. |
| An overnight run moved but finished nothing | `/loop` needs a check that can pass or fail, not a duration. See [guide page 7](../../docs/guide/07-overnight.md). |
| The reply claims success from a green build | Ask for the real command, flow, stored value, or profile. That's the prove-it-works principle. |

For a run that drifts, [`references/prompting.md`](references/prompting.md) has one-line steers. [Guide page 10](../../docs/guide/10-recipes-and-pitfalls.md) has more pitfalls and the recipes worth copying.

## Make pstack my own

- [`$g3-automate-me`](../g3-automate-me/SKILL.md) drafts a personal mode skill from the user's own history, to use alongside `$g3stack`.
- [`$g3-reflect`](../g3-reflect/SKILL.md) after a session turns its lessons into skill edits the user approves.
- `$g3stack write a skill for <workflow>` runs the authoring playbook. The eval playbook tests a skill change blind.
- Fix a misbehaving skill in its own PR, not inside the feature work where it went wrong.

[Guide page 9](../../docs/guide/09-make-it-yours.md) covers each of these.

## Reply

Lead with the answer. Give at most one example prompt in a code block, adapted from [`references/recipes.md`](references/recipes.md) when one fits, then the link to that file. Keep it short unless the user asked for the whole map.
