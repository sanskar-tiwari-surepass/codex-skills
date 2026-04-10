---
name: code-review
description: Run a comprehensive code review
---

# Code Review

Conduct a serious review for correctness, regressions, security, and maintainability.

## When To Use

- The user asks for a code review
- A feature or refactor is complete and needs review
- A diff should be checked before merge

## Purpose

Produce findings with severity, file references, and fix guidance. Focus on real risk before style.

## Workflow

1. Identify the review scope:
   - current diff
   - named files
   - whole change set
2. Review for:
   - correctness and regressions
   - spec or requirement mismatches
   - security issues
   - maintainability problems
   - missing or weak tests
3. Use the `code-reviewer` agent for deep review when that adds value.
4. If the change is trivial, keep the review short.

## Severity

- `critical`: must fix before merge
- `high`: likely bug, regression, or serious risk
- `medium`: meaningful issue but not immediately dangerous
- `low`: minor improvement or cleanup suggestion

## Output

Return:
- overall verdict
- findings ordered by severity
- file and line references for each substantive issue
- concise fix guidance

If no findings are discovered, say so explicitly and mention any residual risk or test gaps.
