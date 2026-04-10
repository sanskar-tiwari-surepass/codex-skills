---
name: master-loop
description: Supervise a within-session subagent loop until a terminal state is reached. Use when Codex should break work into bounded subagent lanes, continuously re-prompt or replace those subagents, integrate results, and keep iterating within the current session until the task is complete, blocked, failed, or cancelled.
---

# Master Loop

Run a leader-controlled subagent loop inside the current Codex session.

## Purpose

Use this skill when a task benefits from repeated subagent execution and refinement, but does not require tmux, hooks, background daemons, or cross-session resume.

This skill is for **within-session persistence only**.

## Terminal States

The loop must end in exactly one of:

- `complete`: requested outcome achieved and verified
- `blocked`: progress cannot continue without missing input, credentials, or authority
- `failed`: repeated attempts did not converge
- `cancelled`: user explicitly stopped the workflow

Do not stop on vague states like "probably done" or "good enough" unless that is the user's explicit acceptance bar.

## When To Use

- A task can be split into bounded lanes and may need multiple subagent passes
- One or more subagents should be re-prompted with follow-up work
- A leader should evaluate convergence after each round
- The task is long enough that a single delegation round is too weak

## When Not To Use

- The task is trivial enough to do directly
- The work is fully sequential and subagents would add overhead
- The task requires persistence after the parent session exits
- The task needs external orchestration, tmux, hooks, or daemon behavior

## Core Model

One leader owns:
- the task ledger
- lane definitions
- terminal-state decisions
- retry and escalation policy
- final integration and verification

Subagents own:
- one bounded slice each
- one write scope each when editing code
- one concrete output contract each

## Workflow

### 1. Define the loop

Before spawning anything, write down:
- goal
- terminal state conditions
- current blockers
- lanes
- ownership per lane
- max retry count per lane

### 2. Spawn bounded lanes

Spawn subagents only for work that is:
- concrete
- independently useful
- non-overlapping
- materially helpful

Examples:
- implementation lane
- verification lane
- research lane
- review lane

### 3. Evaluate every return

For each subagent result, classify it as:
- `done`
- `needs-follow-up`
- `replace-agent`
- `blocked`
- `discard`

Do not blindly trust the result. The leader must decide what happens next.

### 4. Re-prompt or replace

- Reuse the same subagent when the next step depends on its recent context
- Replace the subagent when the lane needs a different role or a fresh attempt
- Never loop without a concrete next ask

### 5. Integrate frequently

Do not let subagents drift too long without integration.

After each meaningful round:
- merge usable results
- update the task ledger
- reduce duplication
- tighten the remaining asks

### 6. Verify before exit

`complete` requires evidence:
- tests
- build
- diagnostics
- file inspection
- artifact review

Choose verification appropriate to the task, then read the output before deciding the loop is done.

## Retry Policy

- Set a default retry limit of `2` per lane unless the task clearly justifies more
- If the same failure pattern repeats, stop retrying and classify it as `blocked` or `failed`
- Prefer changing the prompt, lane scope, or agent role over repeating the same ask

## Escalation Rules

Escalate to the user only for:
- missing business decisions
- destructive actions
- missing credentials or external authority
- ambiguous requirements that materially affect outcome

Otherwise keep the loop moving.

## Good Patterns

- one implementation lane plus one verifier lane
- one researcher lane feeding one executor lane
- one reviewer lane after a code-writing lane

## Bad Patterns

- multiple agents editing the same small file without ownership
- reflexively spawning new agents instead of reusing context
- retrying identical prompts after identical failures
- declaring success without verification

## Output

Progress updates should state:
- current terminal-state target
- open lanes
- decisions made after each round
- remaining blockers or verification work

Final output should state:
- terminal state
- evidence
- what each lane contributed
- what remains, if not complete
