# Prompts worth copying

Swap in the real paths, skills, and done checks. Informal wording works.

## Understand

- `$g3stack read <thread>. restate the underlying issue in your own words, in plain english.`
- `$g3-in-your-own-words <long or messy ask>`
- `$g3-sharpen <the prompt you're about to send>`
- `$g3stack investigate why <symptom>. give me what we know, what data you used, and your best hypotheses. don't change any code yet.`
- `use $g3-how to understand <subsystem>. then use $g3-why to find out why it broke recently.`
- `$g3-recall my work on <topic> from last week, then read <issue>.`
- `$g3-teach me why you implemented it this way and not <other way>. what did you trade off?`
- `$g3stack take over this branch. read the decision log, find what's done, and continue. don't redo finished work.`

## Build

- Bug: `$g3stack <symptom>. repro first, then fix and verify.`
- Bug in an app: `$g3stack repro this with /verify-<app>. if it repros on main, fix it and show me a video as proof.`
- Bug with a cheap test: `$g3stack repro <bug> first. if there's a cheap test path, $g3-tdd it. then fix and rerun.`
- Feature: `$g3stack add <behavior>. <current output> stays byte-identical. verify both.`
- Refactor: `$g3stack move <code> into one module, zero behavior change. record the current output first and prove it's unchanged after.`
- Perf: `$g3stack <operation> takes <time> on <fixture>. trace it, fix the measured cause, show me before and after.`

## Design and plan

- `$g3stack prototype a few options for <feature>. take screenshots or videos for me to compare.`
- `$g3stack we need <feature>. $g3-architect it first, and answer open questions with prototypes. let me review before proceeding.`
- `$g3stack write a tutorial for how i would use <new package> first. then $g3-teach me why it beats the current one.`
- `ask $g3-arena for a second opinion on this thread and our approach.`
- `$g3stack turn this design into a plan. small verifiable PRs, each with its own verification steps.`
- `$g3stack plan the migration of <library> to <target>. small verifiable PRs. the result must match the original exactly, bugs included.`

## Review and ship

- `$g3-interrogate the whole branch, but skeptically. don't change anything yet. no nitpicks unless it's a real bug or regression.` Read the Dropped list too.
- `$g3-create-formal-verification-skill prove <property> holds in <module>, even when <steps> interleave or retry.` After merges or refactors in that code: `$g3-maintain-formal-verification-skill`.
- `$g3-swarm check every package under <dir> against its check script. one worker per package. one report.`
- `$g3stack open the pr. small ordered commits, evidence in the description.`
- `$g3stack babysit this pr. get it green.` For status only: `$g3stack check on pr <number>. anything outstanding?`
- `$g3stack land the stack.`

## Away and back

- `$g3stack im going to bed. <goal> in a fresh worktree off <base>. done means <checks>. keep a decision log. don't ask me before committing. /loop until done. if you're truly stuck after a few hours, stop and write up why.`
- `$g3-show-me-your-work catch me up on what you did last night.` Read its Attention section first.
- `$g3-ketchup` catches you up on this chat since your last message and lists every call that waits on you.
- `$g3stack full autopilot on this queue. each item is independent.`
- `$g3stack autopilot these changes, but don't merge. i'll land them.`
- `$g3-reflect capture what we learned so the next run doesn't repeat it.` Approve only edits that change a future decision.
- `$g3-bro` restates the last reply in plain words.
