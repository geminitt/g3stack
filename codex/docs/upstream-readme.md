# pstack

i'm [poteto](https://x.com/poteto). i'm not a president or ceo, but i've worked with millions of lines of code at Meta, Netflix, and Cursor. i'm also on the react core team where i help build and maintain react compiler.

there's a growing sense that ai writes too much slop code. i agree. i don't want to ship like a team of twenty slop artists. throughput without quality is not a goal i aspire to. if you want to go fast, go deep first. 

**pstack is my answer.** these are the same skills i use every day to ship high quality code at Cursor. this turns cursor into a real engineering team. the goal is not to maximize loc, in fact it's the opposite. pstack helps you write less, but higher quality code.

**pstack gives you fearless parallelism.** when you can go deep on one agent and trust it to write good, verifiable code, you can truly parallelize with confidence. start multiple agents up with `g3stack` and trust that they'll apply rigorous engineering principles to their work.

**cursor gives you the best of all worlds.** every frontier model has its strengths and weaknesses. use any model with pstack. in fact, many of my skills use multi-model workflows to take advantage of each model's unique strengths.

fork it. improve it. make it yours. PRs are welcome! 

## install

```bash
/add-plugin pstack
```

in claude code:

```bash
/plugin marketplace add cursor/plugins
/plugin install pstack@cursor-plugins
```

claude code leaves auto-update off for third-party marketplaces, so pstack stays on the version you installed. to turn it on, run `/plugin`, open the **marketplaces** tab, select `cursor-plugins`, and choose **enable auto-update**. to update once by hand, run `claude plugin update pstack@cursor-plugins`.

claude code prefixes plugin commands and agents, so `$g3stack` is `/pstack:g3stack`. the [claude code adapter](.././docs/harness/claude-code.md) maps every other cursor name. in claude code, `/pstack:g3-setup` writes your model choices to `~/.claude/rules/pstack-models.md`, and a step that needs a cursor-only feature, such as bugbot or automations, is skipped with a one-line note.

claude code installs a generated copy of pstack, including this readme and the guide, from [`harness/pstack/`](https://github.com/cursor/plugins/tree/main/harness/pstack) at the repository root. after you change pstack, run `node scripts/generate-pstack-harness-trees.mjs` from the repository root and commit the result. ci fails while the generated copy is out of date.

## get started

two steps:

1. run [`$g3-setup`](.././skills/g3-setup/SKILL.md), pick a reasoning budget, and choose which models you want.
2. use [`$g3stack`](.././skills/g3stack/SKILL.md) whenever you're doing anything that requires rigor.

new here? the [pstack guide](.././docs/guide/README.md) walks you through a first real task, from setup and prompting through verification and overnight runs. stuck, or unsure which skill fits? ask [`$g3-help`](.././skills/g3-help/SKILL.md).

that's it. the other skills are situational, and the mode skill uses them for you as needed. out of the box, code delegates (feature, refactoring, bug fix, perf, hillclimb), prose, and judgment go to opus 5.5 at xhigh, and no role runs above xhigh. outside a review panel, fable 5.2 runs only when you name it or after two opus 5.5 runs of the same brief fail. the default panel is fable 5.2 / opus 5.5 / gemini 4 carbon. [`$g3-setup`](.././skills/g3-setup/SKILL.md) changes any of it.

## usage

use [`$g3stack`](.././skills/g3stack/SKILL.md) at the start of a task. it reads your request, picks from a set of playbooks, and runs the other skills as the steps need them.

pick `$g3stack` from the `/` menu before you type your task, so cursor attaches the skill to the message.

### just use [`$g3stack`](.././skills/g3stack/SKILL.md)

this skill is the main shortcut. i use it whenever i need the agent to do rigorous engineering work. it comes with twenty-two playbooks:

```
$g3stack this pr has a subtle bug where the scroll drifts every 750ms even when idle. repro
first, then fix and verify.
```

```
$g3stack i'm going to bed. land the stack even if ci flakes. i want everything merged by
morning.
```

<details>
<summary>the twenty-two playbooks</summary>

| playbook | for |
|---|---|
| [investigation](.././skills/g3stack/playbooks/investigation.md) | a read-only question. how does x work, why was y built this way, are we sure. |
| [bug fix](.././skills/g3stack/playbooks/bug-fix.md) | reproduce a defect, root-cause it, and fix with runtime evidence. |
| [perf](.././skills/g3stack/playbooks/perf-issue.md) | trace a measured slowness and improve it against a baseline. |
| [hillclimb](.././skills/g3stack/playbooks/hillclimb.md) | sustained, scientific improvement of one metric against a target, looping hypotheses with before/after measurement and one commit per accepted win. |
| [runtime forensics](.././skills/g3stack/playbooks/runtime-forensics.md) | diagnose a live symptom (leak, idle-cpu spin, glitch) from instrumentation. |
| [trace forensics](.././skills/g3stack/playbooks/trace-forensics.md) | diagnose a captured profiling artifact (cpuprofile, trace, spindump, heap snapshot). |
| [feature](.././skills/g3stack/playbooks/feature.md) | new or changed behavior, built from a named data shape. |
| [refactoring](.././skills/g3stack/playbooks/refactoring.md) | a behavior-preserving change to structure or shape. |
| [prototype](.././skills/g3stack/playbooks/prototype.md) | a throwaway sketch to make a design or behavioral decision cheaply, or to settle an empirical fork by observing it. |
| [visual parity](.././skills/g3stack/playbooks/visual-parity.md) | pixel-exact ui equivalence between two implementations. |
| [authoring a skill](.././skills/g3stack/playbooks/authoring-a-skill.md) | writing or editing a SKILL.md. |
| [eval](.././skills/g3stack/playbooks/eval.md) | test how a skill or prompt change affects agent behavior, blinded. |
| [babysit](.././skills/g3stack/playbooks/babysit.md) | drive a pr or a stack to merge-ready: conflicts, review threads, ci. |
| [shipping](.././skills/g3stack/playbooks/shipping.md) | independently verify a green stack, then land the contiguous verified run bottom-up through github by default or origin when available. |
| [autonomous run](.././skills/g3stack/playbooks/autonomous-run.md) | drive a long task to completion without stopping. |
| [autopilot-full](.././skills/g3stack/playbooks/autopilot-full.md) | run independent prs to merged with one owner per pr. a swarm verifies each code-ready head, and every later change to the patch gets a fresh check. |
| [autopilot-stack](.././skills/g3stack/playbooks/autopilot-stack.md) | autopilot-full without the merge. build and verify prs for the operator to review and land, stacking a pr only on a pr it builds on. |
| [session pickup](.././skills/g3stack/playbooks/session-pickup.md) | resume or take over a prior agent's in-flight work. |
| [pause safely](.././skills/g3stack/playbooks/pause-safely.md) | suspend in-flight work cleanly so it can be resumed later. |
| [multi-phase plan](.././skills/g3stack/playbooks/multi-phase-plan.md) | work that spans phases or stacked PRs. |
| [worktree cleanup](.././skills/g3stack/playbooks/worktree-cleanup.md) | reclaim disk by pruning merged or abandoned worktrees and stale ios simulators, safety-gated. |
| [opening a pr](.././skills/g3stack/playbooks/opening-a-pr.md) | open a ready pr from small ordered commits with a conventional commits title and a briefing-style body. invoked at the end of every other playbook. |

</details>



when invoked it:

1. matches your task to a [playbook](.././skills/g3stack/playbooks/) and opens a todo list whose first items are its steps, copied in verbatim.
2. routes to the other skills as the steps fire.
3. writes unslopped replies framed for the consumer and the maintainer.

the full rules and playbooks live in [`skills/g3stack/SKILL.md`](.././skills/g3stack/SKILL.md).

to keep [`$g3stack`](.././skills/g3stack/SKILL.md) on across turns, pick it from the `/` menu and press option+enter (mac) or alt+enter (windows) instead of enter. that makes it a [custom mode](https://cursor.com/docs/skills#using-a-skill-as-a-custom-mode), which cursor offers in the agents window and the cli. it stays in context every turn until you exit the mode. plain enter attaches it to one message only.

[`$g3stack`](.././skills/g3stack/SKILL.md) works extremely well with cursor's `/loop` command. you can make cursor work for many hours without sacrificing rigor.

## skills

[`$g3stack`](.././skills/g3stack/SKILL.md) runs most of these for you when a step needs them (`why`, `architect`, `arena`, `swarm`, `interrogate`, `unslop`, `no-comments`, `technical-writing`, `tdd`, and the principles). the table below is for when you want one directly:

```
$g3-how do we cancel runs? do we have an n+1 when we look up every run to cancel?
```

```
$g3-interrogate review this pr.
```

<details>
<summary>all skills</summary>

| skill | use it when |
|---|---|
| [`$g3stack`](.././skills/g3stack/SKILL.md) | default entry point for any non-trivial task. |
| [`$g3-help`](.././skills/g3-help/SKILL.md) | you're new to pstack, or unsure which skill, playbook, or principle fits. finds out what you're trying to do, answers that part, and hands you a prompt to type. runs only when you type `$g3-help`. |
| [`$g3-in-your-own-words`](.././skills/g3-in-your-own-words/SKILL.md) | you want the agent to play back your goal and the problem before it starts. runs only when you type `$g3-in-your-own-words`. |
| [`$g3-sharpen`](.././skills/g3-sharpen/SKILL.md) | you want a prompt made deeper, not bigger, before you send it: what a top professional would do that you didn't ask for, the raw material they'd start from, their methods and tools, and an outside check that the result is right. hands back the rewritten prompt, which asks the agent to prototype any choice an experiment can settle and leaves product and preference choices to you. doesn't do the task. runs only when you type `$g3-sharpen`. |
| [`$g3-how`](.././skills/g3-how/SKILL.md) | you want a walkthrough of how a subsystem works. |
| [`$g3-why`](.././skills/g3-why/SKILL.md) | you want to know why something was built this way. answers from the record, not the code: the commits and pr discussions that introduced it and each later change, and other sources when that trail is thin. cites what the authors wrote, marks its own inferences, and says what the record does not answer. |
| [`$g3-recall`](.././skills/g3-recall/SKILL.md) | you're starting or resuming work and want your recent context on a topic rebuilt from your own chat history and the shared record, handed back as a tight current-state brief. |
| [`$g3-ketchup`](.././skills/g3-ketchup/SKILL.md) | you want what changed in this chat since your last message, in plain words and small visuals, with every item waiting on you listed and decidable from the reply alone, even when that makes the reply long. |
| [`$g3-ketchup-video`](.././skills/g3-ketchup-video/SKILL.md) | you want the `$g3-ketchup` catch-up as a short subtitled video of slides, with the calls waiting on you as text under it. |
| [`$g3-blast-radius`](.././skills/g3-blast-radius/SKILL.md) | you have a small-looking change and want to know what else it could break, with the one fact it's safe because of proven by running code, not asserted. |
| [`$g3-architect`](.././skills/g3-architect/SKILL.md) | you're about to write code that crosses a function boundary and want the caller's usage, types, and module shape settled first. |
| [`$g3-arena`](.././skills/g3-arena/SKILL.md) | you want N parallel attempts at the same thing, then to grab the best parts of each. |
| [`$g3-swarm`](.././skills/g3-swarm/SKILL.md) | you want N parallel workers across different slices or races, then one aggregated report. |
| [`$g3-interrogate`](.././skills/g3-interrogate/SKILL.md) | you have a diff and want different models to try to break it, keeping only findings a run proves. |
| [`$g3-automate-me`](.././skills/g3-automate-me/SKILL.md) | you want your own `-mode` skill, drafted from how you've actually worked. |
| [`$g3-make-bot-ui`](.././skills/g3-make-bot-ui/SKILL.md) | you want a page or dashboard whose buttons wake a Grok Bot over a webhook, including the sender-key handoff and Tailscale. |
| [`$g3-setup`](.././skills/g3-setup/SKILL.md) | you want to pick which models pstack uses per role. detects your models and writes a config rule. |
| [`$g3-reflect`](.././skills/g3-reflect/SKILL.md) | a long task landed and you want the recipe captured as a skill edit. |
| [`$g3-correct`](.././skills/g3-correct/SKILL.md) | you keep correcting agents for the same mistakes. mines history for mistake classes, fixes each at the highest level that works (architecture, then types, lint, and ci, then tests, with docs last), and keeps a table pairing each rule with what enforces it. |
| [`$g3-teach`](.././skills/g3-teach/SKILL.md) | you want to actually understand a change or subsystem, not just have it summarized. runs how + why and weaves one plain explanation, built up diagram by diagram. |
| [`$g3-tdd`](.././skills/g3-tdd/SKILL.md) | you're fixing a bug and there's a cheap local test path. write the failing test first, then the fix. |
| [`$g3-benchmark-checklist`](.././skills/g3-benchmark-checklist/SKILL.md) | you ran a benchmark or measured a speedup or regression. vets the number (limiter, tuning, errors, repeat runs, end-to-end relevance) before you report or act on it. |
| [`$g3-no-comments`](.././skills/g3-no-comments/SKILL.md) | strip comments before review; spawns Comment Sicko, fixes accepted findings, offers encodings for claimed constraints. |
| [`$g3-typescript-best-practices`](.././skills/g3-typescript-best-practices/SKILL.md) | you're reading or editing typescript. grounds the type-system-discipline principle in syntax. |
| [`$g3-figure-it-out`](.././skills/g3-figure-it-out/SKILL.md) | no bundled playbook fits. designs a rigorous, auditable playbook for the task. |
| [`$g3-show-me-your-work`](.././skills/g3-show-me-your-work/SKILL.md) | you want a reviewable decision trail. logs decisions to a tsv you can commit. |
| [`$g3-create-verification-skill`](.././skills/g3-create-verification-skill/SKILL.md) | your project has no scripted way to prove app behavior. generates a project-local verify skill with a feature map, for any language or platform. |
| [`$g3-maintain-verification-skill`](.././skills/g3-maintain-verification-skill/SKILL.md) | your verify skill's feature map has drifted from the app. source wave + one live pass, at most one PR of proven corrections. |
| [`$g3-create-formal-verification-skill`](.././skills/g3-create-formal-verification-skill/SKILL.md) | tests can't reach the case that breaks a race, retry, state machine, parser, or unsafe code. verifies one property with the tool that fits and generates a project-local skill to recheck it on every change. |
| [`$g3-maintain-formal-verification-skill`](.././skills/g3-maintain-formal-verification-skill/SKILL.md) | code your formal verification covers has changed since it was last checked. updates the model, harness, or properties to match the code, reruns, and says whether each failure is drift in the verification or a bug in the code. |
| [`$g3-statechart`](.././skills/g3-statechart/SKILL.md) | someone who owns the behavior needs to see it, not read a spec. checks a tla+ model, draws what the user sees as a mermaid statechart, marks each state that breaks a rule, and gives the shortest path to each one. |
| [`$g3-unslop`](.././skills/g3-unslop/SKILL.md) | you're cleaning up writing. removes AI tells. |
| [`$g3-bro`](.././skills/g3-bro/SKILL.md) | you want the last message restated in plain human language, no jargon. |
| [`$g3-technical-writing`](.././skills/g3-technical-writing/SKILL.md) | layered doc standard (Diátaxis + Google developer style + STE + Global English) for docs, RFCs, readmes, PR descriptions, commit messages. |

</details>



### examples

mostly i type [`$g3stack`](.././skills/g3stack/SKILL.md) at the start of a task and let it route to a playbook. the other skills fire as the steps need them. a few i reach for directly.


<details>
<summary>all the examples</summary>

```
bug fix:           $g3stack this pr has a subtle bug where the scroll drifts every 750ms even
                   when idle. repro first, then fix and verify.
perf:              $g3stack a big list takes a second or two to load even though we virtualize.
                   run a cpu trace and tell me why.
feature:           $g3stack build a small feature behind a feature flag. verify it really works.
prototype:         $g3stack build two prototypes of the markdown renderer so we can compare.
                   spawn an agent for each.
multi-phase:       $g3stack open source these skills as a plugin. nothing internal leaks, work
                   in a temp dir, show me the dependency graph first.
overnight run:     $g3stack i'm going to bed. land the stack even if ci flakes. i want
                   everything merged by morning.
babysit:           $g3stack check on pr 123. anything outstanding?
visual parity:     $g3stack the row spacing is too tall when this flag is on. the second image
                   is correct. repro and fix until it matches.
figure it out:     $g3stack i'm stepping away. migrate every caller from the synchronous store
                   to the new async one, keeping behavior identical. i want to trust it was done
                   right when i'm back.
how:               $g3-how do we cancel runs? do we have an n+1 when we look up every run to cancel?
why:               $g3-why is this feature flag not on yet?
architect:         design this instrumentation to be high signal with no false positives. $g3-architect
                   this first.
arena:             $g3-arena take my prompt to the arena verbatim. i want to compare their proposals
                   with yours.
swarm:             $g3-swarm check every package under packages/ against its check.sh. one worker per
                   package. one report.
interrogate:       $g3-interrogate review this pr.
tdd:               $g3-tdd implement
unslop:            can we unslop and tighten the new changes?
reflect:           $g3-reflect that took too long. capture what we learned so the next run doesn't
                   repeat it.
correct:           $g3-correct
show-me-your-work: $g3-show-me-your-work keep a decision trail i can review when i'm back.
automate-me:       $g3-automate-me
help:              $g3-help which skill should i use to review this branch?
```

</details>

## the `g3-agent` and Comment Sicko subagents

[`$g3stack`](.././skills/g3stack/SKILL.md) runs in the chat that receives it. that chat owns the playbook, the todo list, and every subagent spawn.

pstack also ships [`subagent_type: "g3-agent"`](.././agents/g3-agent.md) as the wrapper for delegates spawned during a run. it reads `g3stack` in full, including its inline principles index, before doing any work. substituting `generalPurpose` skips that read and drifts. do not spawn `g3-agent` to run the playbook itself.

[`$g3stack`](.././skills/g3stack/SKILL.md) and [`subagent_type: "g3-agent"`](.././agents/g3-agent.md) route through the same wrapper.

pstack also ships [Comment Sicko](.././agents/comment-sicko.md), a read-only comment reviewer available as `subagent_type: "comment-sicko"`. usually invoke it through [`$g3-no-comments`](.././skills/g3-no-comments/SKILL.md), not directly.

## principles

twenty-four short skills, one principle each. `g3stack` indexes them inline and reads that index at task start. the standalone files are there so other skills can reference a principle by name, and so the index can point at the full rule for each.

<details>
<summary>all twenty-four principles</summary>

| principle | group | rule |
|---|---|---|
| [laziness-protocol](.././skills/g3-principle-laziness-protocol/SKILL.md) | core | Bias toward deletion and the smallest change that solves the problem. |
| [foundational-thinking](.././skills/g3-principle-foundational-thinking/SKILL.md) | core | Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. Get the data structures right so downstream code becomes obvious. |
| [redesign-from-first-principles](.././skills/g3-principle-redesign-from-first-principles/SKILL.md) | core | Redesign as if the requirement had been a foundational assumption from day one, instead of bolting it on. |
| [attack-the-premise](.././skills/g3-principle-attack-the-premise/SKILL.md) | core | Apply when two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before you write another fix that assumes it. |
| [subtract-before-you-add](.././skills/g3-principle-subtract-before-you-add/SKILL.md) | core | Remove dead weight, redundant validators, and stub references first, then build on the simpler base. |
| [minimize-reader-load](.././skills/g3-principle-minimize-reader-load/SKILL.md) | core | Count layers between question and answer, and hidden state in the reader's head; collapse one-caller wrappers and shrink mutable scope. |
| [outcome-oriented-execution](.././skills/g3-principle-outcome-oriented-execution/SKILL.md) | core | Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve smooth intermediate states with throwaway compatibility code. |
| [experience-first](.././skills/g3-principle-experience-first/SKILL.md) | core | Choose user delight over implementation convenience; ship fewer polished features over more rough ones. |
| [exhaust-the-design-space](.././skills/g3-principle-exhaust-the-design-space/SKILL.md) | core | Build 2-3 competing prototypes and compare side by side before committing. |
| [build-the-lever](.././skills/g3-principle-build-the-lever/SKILL.md) | core | Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. Build the tool that does it or proves it (codemod, script, generator, or a skill your subagents follow) instead of working by hand. The tool is the artifact a reviewer can rerun. |
| [model-the-domain](.././skills/g3-principle-model-the-domain/SKILL.md) | architecture | Encode the domain in a structure instead of scattered conditionals. |
| [boundary-discipline](.././skills/g3-principle-boundary-discipline/SKILL.md) | architecture | Concentrate guards at system boundaries (CLI, config, network, external APIs); trust internal types and keep business logic in pure functions. |
| [type-system-discipline](.././skills/g3-principle-type-system-discipline/SKILL.md) | architecture | Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, exhaust variants, derive from authoritative schemas. |
| [make-operations-idempotent](.././skills/g3-principle-make-operations-idempotent/SKILL.md) | architecture | Converge to the same end state regardless of partial prior runs. |
| [migrate-callers-then-delete-legacy-apis](.././skills/g3-principle-migrate-callers-then-delete-legacy-apis/SKILL.md) | architecture | Migrate callers and delete the old API in the same wave instead of preserving compatibility layers. |
| [separate-before-serializing-shared-state](.././skills/g3-principle-separate-before-serializing-shared-state/SKILL.md) | architecture | Eliminate the sharing first; serialize structurally only when one shared writer is a real invariant. |
| [prove-it-works](.././skills/g3-principle-prove-it-works/SKILL.md) | verification | Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'. |
| [fix-root-causes](.././skills/g3-principle-fix-root-causes/SKILL.md) | verification | Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate. |
| [sequence-verifiable-units](.././skills/g3-principle-sequence-verifiable-units/SKILL.md) | verification | Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery so the sequence proves itself to a reviewer. |
| [test-behavior-not-implementation](.././skills/g3-principle-test-behavior-not-implementation/SKILL.md) | verification | Apply when you write, change, or keep a test. Assert what the code's users can observe, so the test fails when that behavior breaks and keeps passing when only the internals change. |
| [explain-the-number](.././skills/g3-principle-explain-the-number/SKILL.md) | verification | Apply before you trust, report, or act on a number you measured: a speedup, a regression, a throughput, a latency, or an eval result. Find what limits it, and rule out that it measured something other than the work you think. |
| [guard-the-context-window](.././skills/g3-principle-guard-the-context-window/SKILL.md) | delegation | Route bulk to subagents; keep summaries in the main thread, not raw payloads. |
| [never-block-on-the-human](.././skills/g3-principle-never-block-on-the-human/SKILL.md) | delegation | Proceed, present the result, let the human course-correct after the fact; reserve confirmation for irreversible actions. |
| [encode-lessons-in-structure](.././skills/g3-principle-encode-lessons-in-structure/SKILL.md) | meta | Encode the rule as a lint, metadata flag, runtime check, or script instead of more text. |

</details>

## not shipped here

a few things `g3stack` references but doesn't bundle:

- `/deslop` and the `deslop` skill ship in the `cursor-team-kit` plugin.
- `control-cli` (for CLIs and TUIs) and `control-ui` (for browser, Electron, web) ship in `cursor-team-kit` too.
- `/create-skill` is a cursor built-in. cursor also ships a built-in `/autopilot` that watches a pr. inside `g3stack`, pr-status requests go to the [babysit playbook](.././skills/g3stack/playbooks/babysit.md) instead.

install `cursor-team-kit` alongside pstack if you want the full set.

## why are there no planning skills?

cursor already has a great plan mode which works great with pstack. but personally, i don't believe in planning. the best spec is code. if you do want to make a plan, [`$g3stack`](.././skills/g3stack/SKILL.md) covers it, but it's not a default. 

## make it yours

`g3stack` is my style. you may not want exactly that.

type [`$g3-automate-me`](.././skills/g3-automate-me/SKILL.md). it mines your recent transcripts, drafts a `<your-name>-mode` skill from how you've actually worked, and routes through pstack underneath. you keep pstack as the base and end up with your own routing skill alongside `g3stack`.

models are configurable too. type [`$g3-setup`](.././skills/g3-setup/SKILL.md). it detects the models you have access to and writes a small always-applied rule mapping each role (code, judgment, the review panels) to a model. every skill reads it and falls back to sensible defaults when the rule is absent, so you override only what you want.

when a default changes, a rule written before the change still pins the old default until you run `$g3-setup` again. that run replaces the old defaults it recognizes and keeps any other role whose model differs from the default. to drop a pin it does not recognize, delete that role's line or the file first.

## automations

pstack also ships a dormant [benny automation pack](.././automations/benny/). benny triages slack issue reports, then reproduces and fixes confirmed bugs with real ui evidence. its files are not registered as slash skills.

to set it up, point cursor at [`FOR_AGENTS.md`](.././automations/benny/FOR_AGENTS.md). setup copies the pack into the target repository at `.cursor/automations/benny/`, enables pstack there for shared skills, and keeps user configuration outside the copied pack. benny runs on cursor automations, so it is cursor-only.

## license

MIT
