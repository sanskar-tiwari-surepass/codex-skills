---
name: scratchpad
description: Read and maintain per-repo `.scratchpad/` markdown memory for durable context, reusable notes, and quick persistent reminders
---

# Scratchpad

## Overview

Maintain `.scratchpad/` as a compact memory layer for the current repository. Use it for durable notes, quick reminders worth keeping, reusable workflow knowledge, and active context that should survive across sessions.

## Default Use

- For most repository-backed runs, check whether `.scratchpad/` exists near the repo root early in the turn.
- If `.scratchpad/` exists, read `.scratchpad/index.md` before substantial work unless the task is clearly trivial or unrelated to repo context.
- Read only the scratchpad files that matter for the current task.
- Update the scratchpad when you learn something reusable enough to help a later session move faster or avoid a repeat mistake.

## Bootstrap

1. Resolve the repo root before doing substantive work.
2. If `.scratchpad/` does not exist, create it with a small Markdown layout.
3. Keep scratchpad files in Markdown unless there is a strong reason not to.

## Default File Set

- `.scratchpad/index.md`: map of the scratchpad and current high-value reminders
- `.scratchpad/preferences.md`: user and team preferences
- `.scratchpad/patterns.md`: commands, workflows, and conventions that repeatedly work
- `.scratchpad/pitfalls.md`: recurring mistakes, gotchas, and failure modes
- `.scratchpad/active.md`: short-lived but still relevant context

Create additional files only when they materially improve retrieval.

## Quick Note Capture

This skill also absorbs the useful part of the old `note` workflow.

When the user wants to save a quick durable note:

- Put short temporary or in-flight context in `.scratchpad/active.md`
- Put durable preferences in `.scratchpad/preferences.md`
- Put repeated workflow lessons in `.scratchpad/patterns.md`
- Put failure warnings or traps in `.scratchpad/pitfalls.md`

Prefer rewriting and merging notes over appending diary-style logs.

## What To Store

- Repeated user corrections and durable preferences
- Repo-specific workflow surprises
- Commands and validation patterns that repeatedly work
- Non-obvious architecture or process conventions
- Short active-context notes that will matter again soon

## What Not To Store

- Full conversation transcripts
- Long command outputs or stack traces
- Secrets or credentials
- One-off dead ends with no reusable lesson
- Notes with no action or behavioral consequence

## Writing Style

- Use short Markdown bullets
- Add dates only when freshness matters
- Keep notes compact and easy to scan
- Write for future execution speed, not storytelling

## Rule

Treat `.scratchpad/` as durable project memory, not a diary.
