---
name: security-review
description: Run a comprehensive security review on code
---

# Security Review

Conduct a focused security audit of the relevant code or change set.

## When To Use

- The user asks for a security review
- Code handles authentication, authorization, secrets, or untrusted input
- New endpoints, integrations, or dependencies were added
- A change affects trust boundaries or sensitive data

## Purpose

Find exploitable issues, unsafe assumptions, and meaningful security risks with clear remediation advice.

## Review Areas

- authentication and authorization
- input validation and injection risks
- secrets and credential handling
- data exposure and logging
- unsafe file, network, or command execution
- dependency risk when relevant

## Workflow

1. Define the review scope.
2. Inspect the code paths that handle trust boundaries or sensitive behavior.
3. Use the `security-reviewer` agent for deep review when appropriate.
4. Focus on concrete vulnerabilities and risky patterns, not generic best-practice padding.

## Severity

- `critical`: exploitable issue with major impact
- `high`: serious vulnerability or unsafe exposure
- `medium`: meaningful weakness that should be fixed
- `low`: hardening recommendation or lower-risk concern

## Output

Return:
- overall verdict
- findings ordered by severity
- file and line references
- short remediation guidance

If no material security findings are present, say so and mention any limits of the review scope.
