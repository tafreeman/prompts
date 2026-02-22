# Sub-Agents

This project supports sub-agent patterns at two levels.

## 1) Workflow-Tier Agents (YAML)

Workflow definitions assign each step to an agent label such as:
- `tier0_parser`
- `tier1_linter`
- `tier2_reviewer`
- `tier3_architect`

These are role names used by the runtime for model/tool routing.

## 2) Claude SDK Sub-Agents (Markdown Definitions)

`agentic_v2/agents/implementations/agent_loader.py` can load named sub-agents from Markdown files with YAML frontmatter and register them for Claude SDK delegation.

Expected frontmatter fields:
- `name`
- `description`
- `tools` (list)
- `model` (`opus`, `sonnet`, or `haiku` shorthand)

Example:

```markdown
---
name: code-reviewer
description: Focused code review specialist
tools: ["Read", "Glob", "Grep", "Bash"]
model: sonnet
---

You are a strict code reviewer. Prioritize correctness and safety.
```

## External Agent Packs

Set `AGENTIC_EXTERNAL_AGENTS_DIR` to load local sub-agent packs without hardcoded paths:

```bash
export AGENTIC_EXTERNAL_AGENTS_DIR=/absolute/path/to/agents
```

The loader prefers bundled definitions first, then this external directory.

## Repository-Level Subagent Manifest

The workspace also includes a higher-level sub-agent registry in `../../docs/subagents.yml` for planning and operational documentation. That manifest is complementary to runtime tier labels and Claude SDK Markdown agents.

## Recommended Practices

- Keep sub-agent prompts narrowly scoped.
- Restrict tool access per sub-agent role.
- Document outputs and acceptance criteria.
- Do not include secrets or PII in prompts.
