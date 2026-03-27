---
name: scratchpad
description: Read and maintain per-repo `.scratchpad/` markdown memory for most repository-backed runs so durable context survives across sessions. Use by default when a repo contains `.scratchpad/`, especially for repeated work, investigations, user corrections, project runbooks, preferences, commands, pitfalls, or workflow patterns. Also use when the user asks for a scratchpad, repo memory, persistent notes, or long-term memory.
---

# Scratchpad

## Overview

Maintain `.scratchpad/` as a small, curated memory layer for the current repository. Prefer durable guidance over raw history so future sessions can reuse what matters quickly.

## Default Use

- For most repository-backed runs, check whether `.scratchpad/` exists near the repo root early in the turn.
- If `.scratchpad/` exists, read `.scratchpad/index.md` before substantial work unless the task is clearly trivial, purely one-off, or unrelated to repo context.
- After reading `index.md`, read only the relevant files for the current task.
- During work, update `.scratchpad/` whenever you learn something reusable enough to help a future run move faster or avoid a repeat mistake.
- Treat scratchpad as the default durable memory layer for repo work, not as an opt-in note system used only when the user names it explicitly.

## Bootstrap

1. Resolve the repo root before doing substantive work.
2. If `.scratchpad/` does not exist, run `scripts/bootstrap_scratchpad.py --repo <repo-root>`.
3. If `.scratchpad/` already exists, do not recreate it and do not re-add `.scratchpad/` to `.gitignore` if the user removed that entry manually.
4. Keep scratchpad files in Markdown unless there is a strong reason not to.

## Read Order

1. Read `.scratchpad/index.md` first.
2. Read only the other files that are relevant to the task at hand.
3. Apply what you learn silently. Do not waste user-facing output announcing that you read the scratchpad.
4. If the task produces a reusable lesson, update the relevant scratchpad file before finishing the turn.

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

- Default to writing a short update after substantial investigations, bug hunts, workflow discoveries, user corrections, or other reusable findings.
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
