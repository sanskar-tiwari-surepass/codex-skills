---
name: agent-creator
description: Create or update one custom Codex agent definition as a standalone TOML file. Use when Codex needs to turn a user request into a narrow, opinionated subagent/custom-agent config under `~/.codex/agents/` or a project's `.codex/agents/` directory, gather any missing requirements before writing, choose appropriate model and sandbox settings, and confirm the final plan before saving the agent file.
---

# Agent Creator

## Overview

Create one custom Codex agent file at user or project scope. Ask only for missing requirements, keep the agent narrow enough to own one job, and confirm the draft before writing or overwriting anything.

## Workflow

1. Check whether the user wants a new agent or an update to an existing one.
2. Determine scope and destination.
   - If scope is explicit, use it.
   - Otherwise ask whether the agent belongs in user-level `~/.codex/agents/` or project-level `.codex/agents/`.
   - If project scope is requested and the repo root is unclear, ask for the target repo path before writing.
3. Gather only the missing requirements, in small batches.
   - Always confirm or derive `name`, `description`, and `developer_instructions`.
   - Ask for `sandbox_mode` when write access is unclear.
   - Ask about `model`, `model_reasoning_effort`, `nickname_candidates`, `mcp_servers`, or `skills.config` only when the request actually needs them.
4. Shape the agent before writing.
   - Keep the agent narrow and opinionated. One agent should own one primary responsibility.
   - Prefer inherited defaults by omitting optional fields when there is no strong reason to override them.
   - Do not create multiple agents from this skill.
   - Do not edit global `[agents]` settings from this skill.
   - Do not override built-in agent names unless the user explicitly asks for that behavior.
5. Present the draft before saving.
   - Summarize the planned file path and the fields that will be written.
   - Ask for final confirmation before creating or overwriting the TOML file.
6. Write and validate.
   - Save the file under the correct agents directory.
   - Ensure the TOML is syntactically valid and required fields are present.
   - Return the absolute path and a short example prompt that uses the new agent.

## Required Questions

Ask these only when the prompt does not already answer them:

- What job should this agent own?
- Should the file be written to user-level or project-level agent config?
- What should the agent be called?
- What write access does it need: inherited, `read-only`, or `workspace-write`?

## Placement Rules

- User-level agent: `~/.codex/agents/<agent-name>.toml`
- Project-level agent: `<repo>/.codex/agents/<agent-name>.toml`
- Create the `agents/` directory if it does not exist.
- If the target repo or scope is ambiguous, stop and ask before writing.

## Drafting Rules

- Keep `description` focused on when the agent should be used.
- Keep `developer_instructions` concrete, task-shaped, and action-oriented.
- Prefer omission over speculative config. If a field can inherit safely, leave it out.
- Add MCP servers or skills only when the user explicitly wants them or the task clearly depends on them.
- Use `nickname_candidates` only when the user wants more readable display labels.

See [custom-agent-best-practices.md](references/custom-agent-best-practices.md) for field guidance, heuristics, and example TOML patterns.

## Minimum TOML Shape

```toml
name = "agent_name"
description = "When and why to use this agent."
developer_instructions = """
Own one clear job.
Stay within that scope.
"""
```

Add optional fields only when justified by the user request.
