---
name: deep-interview
description: Socratic clarification workflow for vague requests before planning or implementation
argument-hint: "[--quick|--standard|--deep] <idea or vague request>"
---

# Deep Interview

Use this skill when the request is too vague to execute safely.

## Purpose

Turn a fuzzy request into a clear, testable brief by asking one high-leverage question at a time.

## When To Use

- The user says things like "don't assume", "interview me", or "ask me everything"
- The request is broad, underspecified, or missing acceptance criteria
- The likely problem and the proposed solution may not be the same thing
- Planning or implementation would otherwise be guesswork

## When Not To Use

- The task already has clear file targets and acceptance criteria
- The user explicitly wants immediate execution
- Lightweight brainstorming is enough

## Modes

- `--quick`: fast clarification pass, usually 3-5 rounds
- `--standard`: default, enough for most feature or refactor requests
- `--deep`: high-rigor clarification for complex, risky, or ambiguous work

## Workflow

1. Restate the request in plain language.
2. Identify the biggest uncertainty.
3. Ask exactly one question.
4. Prefer intent, scope, non-goals, and decision boundaries before implementation detail.
5. Revisit weak answers with a pressure question:
   - ask for an example
   - ask what should be excluded
   - ask what failure would look like
   - ask which tradeoff is unacceptable
6. Stop when the brief is clear enough to plan or execute.

## Output

Produce a compact brief with:

- Intent
- Desired outcome
- In scope
- Out of scope
- Constraints
- Acceptance criteria
- Open questions, if any

## Rules

- Ask one question per round.
- Do not ask the user for facts you can discover from the codebase.
- Prefer clarity over completeness.
- End as soon as the work is safely scoping itself.
