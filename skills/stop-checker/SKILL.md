---
name: stop-checker
description: Explicit completion-control skill for tasks that must not end early. Use only when the user explicitly mentions `$stop-checker`, especially in prompts like `implement X using $stop-checker` or `research Y using $stop-checker`. This skill makes Codex define observable completion criteria, keep a live checklist, and treat the turn as incomplete until the requested work is implemented, researched, verified, or explicitly blocked.
---

# Stop Checker

## Overview

Use this skill only when the user explicitly asks for `$stop-checker`.

Treat the request as completion-sensitive work. Do not end the turn on partial progress, a draft answer, or an unverified implementation.
Once `$stop-checker` is activated in a thread, emit a final XML stop artifact in every assistant final message until the hook is cleared.
The XML is metadata only. It never replaces the normal user-facing answer.

Premature `done` is a known model failure mode.
Treat early exit as a model limitation to correct for, not as a neutral choice.
When you are uncertain, prefer `continue` over a false `done`.
Most stop-checked turns should not end with `done`.

## Workflow

1. Turn the request into an explicit completion checklist early.
Use `update_plan` for multi-step work.
Write steps so they are observable, not vague.

2. Keep the checklist honest while you work.
Mark steps `in_progress` and `completed` as work actually happens.
Do not leave hidden pending work outside the plan.

3. Match the completion standard to the task type.

Implementation:
- Do not stop until the requested code changes are made.
- Run relevant verification when practical.
- If verification is blocked, say exactly what blocked it.

Research or investigation:
- Do not stop after a thin skim.
- Inspect enough concrete evidence to support the answer.
- Name the files, docs, logs, or sources that drove the conclusion.

Review or audit:
- Do not stop at a vague overview.
- Return findings, risks, or an explicit `no findings` statement.

4. Before ending, run a final self-check.
- Are all plan steps completed or explicitly blocked?
- If code changed, was verification attempted?
- If research was requested, is the answer grounded in specific evidence?
- If something remains, continue instead of wrapping up.

If you feel the urge to stop because you have a plausible answer, pause and check whether the requested execution or evidence-gathering is actually complete.
Opting out of an early exit is better than forcing the user to re-prompt you to continue.

5. If blocked, be precise.
State the exact unfinished step, the blocker, and the smallest next action needed.

## Completion Rules

- Do not confuse “I know what to do next” with “the work is finished”.
- Do not stop just because the main insight is found if requested execution is still pending.
- Do not stop after delegating work until the delegated results are integrated into the final outcome.
- Prefer one solid end-to-end pass over an early summary followed by a user nudge.

## Stop Artifact

When `$stop-checker` is active, append this XML block near the end of every final assistant message:

```xml
<stop_checker>
  <status>continue</status>
  <reason>Short reason here.</reason>
</stop_checker>
```

Allowed `status` values:
- `done`
- `continue`
- `blocked`

Use:
- `done` when the requested work is actually complete.
- `continue` when more work is still required in the same thread.
- `blocked` when progress cannot continue without a real blocker.

When `status=done`, also include a short `<completion_evidence>` element that states why the work is truly complete.

Rules:
- Keep the XML short and explicit.
- Always include exactly one `status`.
- Always include a short `reason`.
- For `done`, always include `<completion_evidence>`.
- Put the XML at the very end of the message.
- Prefer a compact one-block artifact over a longer XML structure.
- Never reply with XML only; always answer the user first.
- If the work is not done, do not emit `done`.
- If unsure, prefer `continue` over a premature `done`.
- Treat `continue` as the default and `done` as the exceptional case.
- Use `done` only when you would be comfortable if the user immediately ended the thread and did not give you another chance to continue.
- If there is any meaningful unfinished execution, verification, integration, or evidence-gathering left, do not emit `done`.
- If the hook asks for recovery because the XML is missing or invalid, default to `continue` unless completion is unquestionably true.

Clearing:
- A valid `done` stop artifact clears `$stop-checker` for later turns in the thread.
- You can also clear it explicitly with a user message like `$stop-checker clear`.

## Response Style

- Keep progress updates concise.
- Keep the final answer brief, but only after the work is actually complete.
- If `$stop-checker` is active and the work is not done, continue working instead of summarizing partial progress.
- The visible answer comes first. The XML block comes last.
