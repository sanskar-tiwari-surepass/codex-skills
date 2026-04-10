---
name: ralplan
description: Consensus planning alias for plan --consensus
argument-hint: "[--interactive] <task>"
---

# Ralplan

`ralplan` is a high-rigor planning shortcut for:

```text
plan --consensus <task>
```

## Purpose

Use this when a normal plan is not enough and you want a multi-perspective plan review before execution.

## Workflow

1. Draft a plan with `planner`
2. Review the design and tradeoffs with `architect`
3. Pressure-test the plan with `critic`
4. Revise until the plan is clear, testable, and internally consistent

## Output

A final plan with:

- Decision summary
- Main tradeoffs
- Ordered execution steps
- Risks and mitigations
- Verification approach

## Rules

- Keep Architect and Critic reviews sequential, not parallel.
- Use this only when the task is important enough to justify the extra review loop.
- Output the plan by default; do not automatically implement it.
