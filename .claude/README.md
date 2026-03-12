# `.claude/` Directory Guide

Configuration and extensions for Claude Code in this repository.

## Structure

```
.claude/
├── commands/       # Slash commands (invoked via /command-name)
├── contexts/       # Context files loaded with @context-name
├── rules/          # Auto-loaded rules organized by language/topic
│   ├── common/     # Language-agnostic (agents, git, security, testing, patterns)
│   └── python/     # Python-specific rules
├── skills/         # Multi-step skill definitions (invoked via /skill-name)
├── launch.json     # Dev server configurations for Claude Preview
└── settings.local.json  # Local overrides (not committed)
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

## Contexts (3)

Loaded into conversation via `@context-name` for domain-specific knowledge.

| Context | When to use |
|---------|-------------|
| `dev` | Day-to-day development tasks |
| `research` | Research and deep analysis work |
| `review` | Code review and quality checks |

## Rules

Auto-loaded rules that guide behavior. Organized by scope:

- **`common/`** — agents, coding-style, git-workflow, ml-practices, patterns, security, testing
- **`python/`** — Python-specific conventions

## Skills (9)

Multi-step skill definitions with structured workflows.

| Skill | Purpose |
|-------|---------|
| `changelog-generator` | Generate changelogs from git history |
| `code-review` | Structured code review workflow |
| `context-engineering` | AI context design patterns |
| `debugging` | Systematic debugging frameworks |
| `langsmith-fetch` | Fetch LangSmith execution traces |
| `mcp-builder` | Create MCP servers |
| `problem-solving` | Creative problem-solving techniques |
| `sequential-thinking` | Step-by-step reasoning with revision |
| `webapp-testing` | Web application testing with Playwright |
