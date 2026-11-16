# g3stack Development Instructions

## Purpose

g3stack is the source repository for a reusable AI agent environment for OpenAI Codex and Claude Code.

It supports Research, Engineering, and hybrid workflows. It is not a test application or a storage location for unrelated project state.

## Design Principles

- Keep global instructions concise and independent of specific projects.
- Separate shared behavior from agent-specific integrations.
- Use skills for reusable, task-specific procedures.
- Add tools, hooks, scripts, and specialized agents only when they solve a defined problem.
- Support exploration in empty projects without requiring extensive documentation.
- Prefer executable verification over additional prose instructions.
- Keep the environment simple, portable, and maintainable.

## Development Rules

- Inspect existing files and decisions before proposing changes.
- Explain the problem, proposed change, expected result, and verification method.
- Prefer targeted, reversible changes over broad redesigns.
- Preserve existing user-approved requirements unless their revision is explicitly approved.
- Verify agent-specific behavior against current official documentation.
- Distinguish documented facts, observations, hypotheses, and recommendations.
- Do not claim successful verification without supporting evidence.
- Do not install, activate, overwrite, or deploy configurations without authorization.
- Never expose credentials or execute paid operations without approval.

## Communication

- Communicate with the owner in Vietnamese.
- Write code, configurations, instructions, and technical documentation in English.
- Apply the clarity and consistency principles of ASD-STE100 Issue 9.
- Provide complete, copy-ready content and explain how to apply and verify it.
