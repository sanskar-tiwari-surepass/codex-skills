---
name: ask-codex
description: Ask a focused Codex specialist and capture a reusable artifact
argument-hint: "[--role <agent-role>] <question or task>"
---

# Ask Codex

Use a bounded Codex specialist consult for second opinions, focused reviews, or narrow research questions.

## Usage

```text
/ask-codex [--role <agent-role>] <question or task>
```

Examples:

```text
/ask-codex --role architect review this migration plan
/ask-codex --role researcher summarize the latest official docs for X
/ask-codex what edge cases am I missing in this API design?
```

## Default Behavior

- Prefer a native subagent, not an external CLI wrapper.
- Keep the ask narrow and concrete.
- Choose the smallest role that can answer well.
- Save a markdown artifact so the result is reusable later.

## Role Selection

If `--role` is provided, use it.

Otherwise choose the closest fit:
- `architect` for design and tradeoffs
- `researcher` for external docs and references
- `code-reviewer` for review findings
- `security-reviewer` for security concerns
- `verifier` for completion or proof checks
- `writer` for documentation feedback
- `critic` for challenging a plan

If no specialist clearly fits, use a general subagent and keep the task tightly scoped.

## Execution

1. Restate the focused question in one clear sentence.
2. Spawn a bounded subagent or specialist with only the context it needs.
3. Wait for the result.
4. Save an artifact under:

```text
.codex-artifacts/ask-codex-<slug>-<timestamp>.md
```

5. Return the answer plus the artifact path.

## Artifact Format

Minimum sections:
1. Original user task
2. Focused prompt sent
3. Selected role
4. Raw response
5. Concise summary
6. Action items or next steps

## Rules

- Do not broaden the question unless needed for correctness.
- Prefer direct, reusable answers over long transcripts.
- If the result is uncertain, say so explicitly.
- If a cited source or file is important, include it in the artifact.

Task: {{ARGUMENTS}}
