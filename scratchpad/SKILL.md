---
name: scratchpad
description: Create and maintain a per-repo `.scratchpad/` folder of markdown notes that preserve durable context across sessions. Use when the user asks for a scratchpad, napkin, repo memory, persistent notes, long-term memory, project runbooks, or wants Codex to remember mistakes, corrections, preferences, commands, or workflow patterns over time.
---

# Scratchpad

## Overview

Maintain `.scratchpad/` as a small, curated memory layer for the current repository. Prefer durable guidance over raw history so future sessions can reuse what matters quickly.

## Bootstrap

1. Resolve the repo root before doing substantive work.
2. If `.scratchpad/` does not exist, run `scripts/bootstrap_scratchpad.py --repo <repo-root>`.
3. If `.scratchpad/` already exists, do not recreate it and do not re-add `.scratchpad/` to `.gitignore` if the user removed that entry manually.
4. Keep scratchpad files in Markdown unless there is a strong reason not to.

## Read Order

1. Read `.scratchpad/index.md` first.
2. Read only the other files that are relevant to the task at hand.
3. Apply what you learn silently. Do not waste user-facing output announcing that you read the scratchpad.

## Default File Set

Use this layout unless the repo clearly needs something different:

- `.scratchpad/index.md`: map of the scratchpad and current high-value reminders
- `.scratchpad/preferences.md`: user and team preferences that change how work should be done
- `.scratchpad/patterns.md`: commands, workflows, and project conventions that repeatedly work
- `.scratchpad/pitfalls.md`: recurring mistakes, gotchas, and failure modes
- `.scratchpad/active.md`: live context worth carrying across nearby sessions

Create additional Markdown files only when they clearly improve retrieval or reduce clutter.

## What To Store

- Repeated user corrections and durable preferences
- Repo-specific toolchain surprises and environment quirks
- Commands and validation patterns that repeatedly work
- Non-obvious architecture or workflow conventions
- Short active-context notes that will matter again soon

## What Not To Store

- Full conversation transcripts
- Long command outputs, stack traces, or copied logs
- Secrets, tokens, credentials, or private personal data
- One-off dead ends that have no reusable lesson
- Notes with no action, preference, or behavioral consequence

## Update Policy

- Update during work when you learn something reusable.
- Rewrite and merge notes instead of appending raw journal entries.
- Prefer short dated entries or bullets over paragraphs.
- Remove or rewrite stale notes when reality changes.
- Keep `active.md` current; archive or delete stale active context instead of letting it accumulate.

## Writing Style

- Prefer terse Markdown bullets and short headings.
- Include a concrete directive, preference, or lesson in each note.
- Add a date when freshness matters.
- Write notes for future execution speed, not for storytelling.

## Practical Rule

Treat `.scratchpad/` as durable project memory, not a diary. Keep it compact, useful, and easy to scan at the start of later sessions.
