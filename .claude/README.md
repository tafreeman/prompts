# `.claude/` Directory Guide

Canonical Claude/Codex workflow configuration for this repository.

## Structure

```
.claude/
├── agents/         # Canonical Claude/Codex execution specialists
├── commands/       # Slash commands (invoked via /command-name)
├── rules/          # Auto-loaded rules organized by language/topic
│   ├── common/     # Language-agnostic (agents, git, security, testing, patterns)
│   └── python/     # Python-specific rules
├── skills/         # On-demand multi-step protocols
├── launch.json     # Dev server configurations for Claude Preview
└── settings.local.json  # Local permission overrides
```

## Commands (11)

Slash commands for common workflows. Invoked with `/command-name`.

| Command | Purpose |
|---------|---------|
| `build-fix` | Resolve build and type errors |
| `checkpoint` | Run checkpoint review |
| `code-review` | Review code changes |
| `eval` | Run evaluation suite |
| `orchestrate` | Multi-agent orchestration |
| `plan` | Create implementation plan |
| `python-review` | Python-specific code review |
| `refactor-clean` | Dead code cleanup |
| `tdd` | Test-driven development workflow |
| `test-coverage` | Analyze and improve test coverage |
| `update-docs` | Update documentation and codemaps |

## Rules

Auto-loaded rules that guide behavior. Organized by scope:

- **`common/`** — agents, coding-style, git-workflow, ml-practices, patterns, security, testing
- **`python/`** — Python-specific conventions

## Loading Hierarchy

When content overlaps between layers, this precedence applies:

1. **Rules** (`rules/`) — Auto-loaded behavioral constraints. **Authoritative source of truth.**
2. **Commands** (`commands/`) — Slash-command entry points. Delegate to agents; should not duplicate rule content.
3. **Skills** (`skills/`) — Multi-step protocols. Loaded on-demand via `/skill-name`.
4. **Agents** (`agents/`) — Execution specialists. Invoked by commands or skills and constrained by rules.

## Agent Surfaces

- **`.claude/agents/`** is the authoritative agent layer for Claude/Codex workflows in this repo.
- **`.github/agents/`** is an optional GitHub Copilot integration surface. Update `.claude/` first, then sync `.github/agents/` only when Copilot support is intentionally being maintained.

## Skills (14)

Multi-step skill definitions with structured workflows.

| Skill | Purpose |
|-------|---------|
| `build-all` | Build and verify all packages in the monorepo |
| `changelog-generator` | Generate changelogs from git history |
| `code-review` | Structured code review workflow |
| `codebase-audit` | Parallel agent audit across deps, quality, security |
| `context-engineering` | AI context design patterns |
| `debugging` | Systematic debugging frameworks |
| `langsmith-fetch` | Fetch LangSmith execution traces |
| `mcp-builder` | Create MCP servers |
| `problem-solving` | Creative problem-solving techniques |
| `run-ci-local` | Mirror the CI pipeline locally |
| `sequential-thinking` | Step-by-step reasoning with revision |
| `session-plan` | Plan focused sessions with scoped goals |
| `test-fix` | Autonomous test-and-fix loop (max 3 attempts) |
| `webapp-testing` | Web application testing with Playwright |

## Retired Surfaces

The repo no longer ships `.claude/contexts/*.md` entrypoints such as `@dev`, `@research`, or `@review`. Their guidance was too thin and duplicated the active rules, commands, and skills above.
