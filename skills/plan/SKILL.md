---
name: plan
description: Strategic planning workflow for turning a task into an actionable implementation plan
argument-hint: "[--direct|--consensus|--review|--interactive] <task or plan>"
---

# Plan

Use this skill when the task should be planned before implementation.

## Purpose

Create a practical, test-aware plan that is specific enough to execute without guesswork.

## Modes

- `default`: choose between interview-style clarification and direct planning
- `--direct`: skip clarification and draft the plan immediately
- `--consensus`: use multiple specialist perspectives before finalizing the plan
- `--review`: review an existing plan instead of creating a new one
- `--interactive`: pause for user feedback at key points

## When To Use

- The user says "plan this", "plan the", or "let's plan"
- The task is broad enough that execution order matters
- Risks, tradeoffs, or testing strategy should be explicit before coding
- An existing plan needs a serious review

## Workflow

### Default / Direct Planning

1. Determine whether clarification is needed.
2. Gather codebase facts before asking the user about internal structure.
3. Identify assumptions, risks, and likely touchpoints.
4. Produce a plan sized to the task.

### Consensus Planning

Use a three-part review loop:

1. `planner` drafts the plan
2. `architect` reviews structure and tradeoffs
3. `critic` challenges weak assumptions and unclear verification

Repeat only when the objections materially improve the plan.

### Plan Review

1. Read the existing plan.
2. Check for vague scope, untestable criteria, missing risks, and weak verification.
3. Return a verdict: approve, revise, or reject.

## Plan Output

Every plan should include:

- Goal
- Scope
- Assumptions
- Risks and mitigations
- Ordered implementation steps
- Verification approach
- Open questions, if any

## Rules

- Right-size the number of steps to the task.
- Prefer specific file, system, or workflow references when known.
- Make acceptance and verification concrete.
- Do not treat planning as implementation.
- If the user later says to execute, hand off from the plan rather than rewriting it from scratch.
