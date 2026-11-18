---
name: g3-ui
description: Implement or critique a web/native UI within its accepted scope, brand and stack. Use for screens, interactions, accessibility or visual design; not an automatic full product redesign.
license: See ../PROVENANCE.md and retained upstream notices.
---

Apply [shared execution boundaries](../compatibility.md). This is the selected
work procedure, not a new project controller. Return evidence and unresolved
questions to the existing project record.

# UI

Adapted from DevFlow's shared UI task policy and coordinated specialist resources.

First identify the route: focused fix, new screen in an accepted system, new visual
direction, or review-only. Reuse the accepted brand, stack and components. A small
fix does not trigger full brainstorming, a replacement design system or an image server.

- Inspect affected component/state, callers, tokens and acceptance criteria.
- Implement only the requested behavior and connected changes. Preserve layout
  and identity unless a real functional/accessibility requirement conflicts.
- Check loading, empty, success, error and recovery states; keyboard/focus,
  relevant viewport sizes and actual rendered interaction when tools permit.
- Inspect asynchronous ownership and stale responses when the UI handles mutations,
  identity changes or resets. Screenshots alone do not prove interaction or storage.
- Report observed behavior, render/interaction evidence and unavailable target
  checks. Browser evidence does not establish native-device behavior.

Read only the applicable specialist resources under
`../../vendor/devflow/plugin/skills/`: `frontend-design/SKILL.md` for visual
implementation, `ui-ux-pro-max/SKILL.md` for targeted UX/stack lookup,
`taste-skill/SKILL.md` or `ui-taste/SKILL.md` for relevant direction/craft/critique.
Before their longer guidance, apply `devflow/references/ui-task-policy.md` and
its selected acceptance resources. One accepted direction governs all components;
aesthetic defaults do not override owner choices. Retain their full sibling assets,
helpers, data, licenses and notices; optional image/MCP tooling is not mandatory.

[Source attribution and adaptations](../PROVENANCE.md).
