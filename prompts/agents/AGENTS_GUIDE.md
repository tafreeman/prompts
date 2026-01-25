---
name: GitHub Copilot Custom Agents Guide
description: Comprehensive guide to creating and using GitHub Copilot custom agents.
type: reference
---
## Description

## Prompt

```markdown
# Agent Title

## Role
[Persona definition and expertise]

## Responsibilities

- [What this agent does]

## Tech Stack

- [Technologies the agent knows]

## Boundaries

- [What the agent should NOT do]

## Output Format
[Expected response structure]

## Process

1. [Step-by-step workflow]

## Examples
[Concrete examples of expected output]
```

Comprehensive guide to creating and using GitHub Copilot custom agents.

## Description

## Prompt

```markdown
# Agent Title

## Role
[Persona definition and expertise]

## Responsibilities

- [What this agent does]

## Tech Stack

- [Technologies the agent knows]

## Boundaries

- [What the agent should NOT do]

## Output Format
[Expected response structure]

## Process

1. [Step-by-step workflow]

## Examples
[Concrete examples of expected output]
```

Comprehensive guide to creating and using GitHub Copilot custom agents.


# GitHub Copilot Custom Agents Guide

A comprehensive guide to creating, deploying, and using custom agents with GitHub Copilot for effective AI-assisted development.

## What Are Custom Agents
Custom agents are specialized AI personas that extend GitHub Copilot's capabilities with domain-specific knowledge and behaviors. They allow you to:

- **Standardize workflows** across your team
- **Encode expertise** in reusable formats
- **Ensure consistency** in code reviews, documentation, and testing
- **Accelerate development** by automating repetitive tasks

### Key Concepts

| Concept | Description |
| --------- | ------------- |
| **Agent Profile** | A markdown file defining the agent's persona, capabilities, and constraints |
| **Role** | The agent's area of expertise (e.g., documentation, testing, security) |
| **Boundaries** | What the agent should and should not do |
| **Tools** | What capabilities the agent has access to (read, write, execute, etc.) |

## Creating Agents

### Agent File Structure

Every agent file follows this structure:

```markdown
# Agent Title

## Role
[Persona definition and expertise]

## Responsibilities

- [What this agent does]

## Tech Stack

- [Technologies the agent knows]

## Boundaries

- [What the agent should NOT do]

## Output Format
[Expected response structure]

## Process

1. [Step-by-step workflow]

## Examples
[Concrete examples of expected output]
```text

### Frontmatter Reference

| Field | Type | Required | Description |
| ------- | ------ | ---------- | ------------- |
| `name` | string | Yes | Unique agent identifier (snake_case) |
| `description` | string | Yes | Brief description for UI display |
| `tools` | array | No | List of allowed tools |

### Tool Options

| Tool | Permission | Use Case |
| ------ | ------------ | ---------- |
| `read` | Read files | Viewing code, configuration |
| `write` | Create/modify files | Generating code, docs |
| `search` | Search codebase | Finding patterns, references |
| `execute` | Run commands | Building, testing |
| `github` | GitHub API access | PR operations, issues |

## Common Patterns

### Pattern 1: Review-Only Agent

For agents that analyze but don't modify:

```yaml
tools: ["read", "search"]  # No write access
```text

```markdown
## Boundaries

- Do NOT modify any files
- Provide analysis and recommendations only

```text

### Pattern 2: Generator Agent

For agents that create new files:

```yaml
tools: ["read", "write", "search"]
```text

```markdown
## Working Directory
Focus only on files in:

- `src/generated/`
- `tests/`

```text

### Pattern 3: Executor Agent

For agents that run commands:

```yaml
tools: ["read", "write", "search", "execute"]
```text

```markdown
## Commands (Allowed)

- `npm test`
- `npm run lint`

## Commands (NOT Allowed)

- `rm -rf`
- `git push`

```text

## Troubleshooting

### Agent Not Appearing

1. ✅ Ensure file is in `.github/agents/` directory
2. ✅ Verify file extension is `.agent.md`
3. ✅ Check file is merged to default branch
4. ✅ Confirm frontmatter is valid YAML

### Agent Not Following Instructions

1. ✅ Make instructions more explicit and specific
2. ✅ Add concrete examples of expected output
3. ✅ Reduce scope to fewer responsibilities
4. ✅ Check for conflicting instructions

### Agent Accessing Wrong Files

1. ✅ Define explicit working directories
2. ✅ Add boundaries for excluded directories
3. ✅ Use specific file patterns (globs)

### Agent Output Quality Issues

1. ✅ Add more examples of good output
2. ✅ Define output format structure
3. ✅ Include quality checklist
4. ✅ Reference coding standards

## Summary Checklist

Before deploying an agent, verify:

- [ ] **Name** is unique and descriptive (snake_case)
- [ ] **Description** clearly explains purpose
- [ ] **Role** defines expertise specifically
- [ ] **Responsibilities** are well-defined
- [ ] **Tech Stack** matches your project
- [ ] **Boundaries** are explicit (what NOT to do)
- [ ] **Output Format** is well-defined
- [ ] **Examples** are realistic and helpful
- [ ] **Commands** are accurate for your environment
- [ ] **Tested** locally with Copilot CLI

---

**Happy coding with custom agents! 🚀**## Variables

| Variable | Description |
|---|---|
| `[ ]` | AUTO-GENERATED: describe ` ` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````
## Variables

| Variable | Description |
|---|---|
| `[ ]` | AUTO-GENERATED: describe ` ` |
| `["read", "search"]` | AUTO-GENERATED: describe `"read", "search"` |
| `["read", "write", "search"]` | AUTO-GENERATED: describe `"read", "write", "search"` |
| `["read", "write", "search", "execute"]` | AUTO-GENERATED: describe `"read", "write", "search", "execute"` |
| `[Concrete examples of expected output]` | AUTO-GENERATED: describe `Concrete examples of expected output` |
| `[Expected response structure]` | AUTO-GENERATED: describe `Expected response structure` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Persona definition and expertise]` | AUTO-GENERATED: describe `Persona definition and expertise` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[Step-by-step workflow]` | AUTO-GENERATED: describe `Step-by-step workflow` |
| `[Technologies the agent knows]` | AUTO-GENERATED: describe `Technologies the agent knows` |
| `[What the agent should NOT do]` | AUTO-GENERATED: describe `What the agent should NOT do` |
| `[What this agent does]` | AUTO-GENERATED: describe `What this agent does` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

