# Custom Agent Best Practices

Use this reference when a request needs more than the minimum TOML shape.

## Required Fields

- `name`: The identifier used when spawning or referring to the agent.
- `description`: Human-facing guidance for when the agent should be used.
- `developer_instructions`: The behavior contract for the agent.

Every custom agent file must define those three fields.

## Scope And Placement

- User-level agents live in `~/.codex/agents/`.
- Project-level agents live in `<repo>/.codex/agents/`.
- The `name` field is the source of truth. Matching the filename to `name` is the simplest convention.

## Intake Checklist

Collect only what is missing:

1. Agent job: What single responsibility should the agent own?
2. Scope: user-level or project-level?
3. Name: short, clear, and stable.
4. Write access: inherit, `read-only`, or `workspace-write`?
5. Optional overrides:
   - `model`
   - `model_reasoning_effort`
   - `nickname_candidates`
   - `mcp_servers`
   - `skills.config`

If the request asks for multiple responsibilities, split them conceptually and ask the user to choose one for this agent.

## Design Heuristics

- Prefer narrow and opinionated agents over general-purpose ones.
- Prefer inherited defaults when there is no concrete reason to override parent session settings.
- Prefer `read-only` for research, review, and documentation agents.
- Prefer `workspace-write` only when the agent is expected to edit files or produce artifacts.
- Avoid shadowing built-in agent names such as `default`, `worker`, or `explorer` unless the user explicitly wants that override.

## Optional Field Guidance

### `model`

Omit it unless the user has a clear reason to pin a model.

- Use a smaller model for bounded, read-heavy, repetitive work.
- Use a stronger model for complex review or multi-step reasoning.

### `model_reasoning_effort`

Omit it unless the user wants an explicit tradeoff. Increase it only when the task is genuinely complex.

### `nickname_candidates`

Use only when the user wants friendlier display names in the app or CLI.

Rules:

- Non-empty list of unique names
- ASCII letters, digits, spaces, hyphens, and underscores only

### `sandbox_mode`

- Omit to inherit parent behavior
- `read-only` for evidence gathering and safe inspection
- `workspace-write` for implementation-focused work

### `mcp_servers`

Add only when the agent depends on a specific external tool surface, such as docs or browser tooling.

### `skills.config`

Add only when the user wants a skill enabled or disabled for that agent.

## Confirmation Pattern

Before writing, summarize:

- Target file path
- Required fields
- Any optional overrides
- Any overwrite risk if the file already exists

Ask for confirmation before creating or replacing the file.

## Example Minimal Agent

```toml
name = "reviewer"
description = "Review code for correctness, regressions, and missing tests."
developer_instructions = """
Review code like an owner.
Prioritize correctness, security, regressions, and missing tests.
Lead with concrete findings.
"""
```

## Example With Optional Fields

```toml
name = "docs_researcher"
description = "Verify APIs and framework behavior against documentation."
model = "gpt-5.4-mini"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"
developer_instructions = """
Use documentation sources to confirm APIs, options, and version-specific behavior.
Return concise answers with references when available.
Do not make code changes.
"""
nickname_candidates = ["Atlas", "Delta", "Echo"]
```
