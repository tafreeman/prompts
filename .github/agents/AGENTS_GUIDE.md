---
name: agents_guide
description: Comprehensive guide to creating and using GitHub Copilot custom agents
---
# GitHub Copilot Custom Agents Guide

A comprehensive guide to creating, deploying, and using custom agents with GitHub Copilot for effective AI-assisted development.

---

## 📋 Table of Contents

- [What Are Custom Agents?](#what-are-custom-agents)
- [Quick Start](#quick-start)
- [Creating Agents](#creating-agents)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

---

## What Are Custom Agents?

Custom agents are specialized AI personas that extend GitHub Copilot's capabilities with domain-specific knowledge and behaviors. They allow you to:

- **Standardize workflows** across your team
- **Encode expertise** in reusable formats
- **Ensure consistency** in code reviews, documentation, and testing
- **Accelerate development** by automating repetitive tasks

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Agent Profile** | A markdown file defining the agent's persona, capabilities, and constraints |
| **Role** | The agent's area of expertise (e.g., documentation, testing, security) |
| **Boundaries** | What the agent should and should not do |
| **Tools** | What capabilities the agent has access to (read, write, execute, etc.) |

---

## Quick Start

### 1. Choose an Agent

Browse our [pre-built agents](./README.md) or create your own from the [template](./agent-template.md).

### 2. Copy to Your Repository

```bash
# Copy agent to your repository's .github/agents/ directory
cp agents/docs-agent.agent.md your-repo/.github/agents/
```text
### 3. Merge to Default Branch

Push the agent to your repository's default branch to activate it.

### 4. Invoke the Agent

In GitHub Copilot Chat, use `@agent-name`:

```text
@docs_agent Create a README for this project
@test_agent Generate tests for the UserService class
@code_review_agent Review my latest changes
```text
---

## Creating Agents

### Agent File Structure

Every agent file follows this structure:

```markdown
---
name: agent_name          # Unique identifier (snake_case)
description: Short desc   # Brief description (shown in UI)
tools: ["read", "write"]  # Allowed tools
---

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
|-------|------|----------|-------------|
| `name` | string | Yes | Unique agent identifier (snake_case) |
| `description` | string | Yes | Brief description for UI display |
| `tools` | array | No | List of allowed tools |

### Tool Options

| Tool | Permission | Use Case |
|------|------------|----------|
| `read` | Read files | Viewing code, configuration |
| `write` | Create/modify files | Generating code, docs |
| `search` | Search codebase | Finding patterns, references |
| `execute` | Run commands | Building, testing |
| `github` | GitHub API access | PR operations, issues |

---

## Best Practices

### 1. 🎯 Define Specialized Roles

Create focused agents with narrow responsibilities:

```markdown
# ❌ Too Broad
name: helper
description: Helps with various tasks

# ✅ Focused
name: python_test_agent
description: Expert in Python testing with pytest and coverage analysis
```text
### 2. 📋 Be Explicit About Tech Stack

Specify exact versions and tools:

```markdown
## Tech Stack
- Python 3.11+
- pytest 7.x with pytest-cov
- Black formatter (line length 88)
- mypy for type checking
```text
### 3. 🚫 Set Clear Boundaries

Define what the agent should NOT do:

```markdown
## Boundaries
- Do NOT modify production code
- Do NOT commit changes directly
- Do NOT access external APIs
- Do NOT expose secrets or credentials
```text
### 4. 📝 Provide Concrete Examples

Show exactly what output looks like:

```markdown
## Example Output

### Unit Test Example
```python
def test_user_creation_with_valid_data():
    """Test that a user can be created with valid data."""
    user = User(name="John", email="john@example.com")
    assert user.name == "John"
    assert user.email == "john@example.com"
```text
```text
### 5. 🔧 Include Relevant Commands

Add commands the agent should use:

```markdown
## Commands
```bash
# Run tests
pytest --cov=src --cov-report=html

# Format code
black src/ tests/

# Type check
mypy src/
```text
```sql
### 6. 🔄 Iterate and Improve

- Test agents locally before deploying
- Gather feedback from team members
- Update agent profiles based on real usage

---

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
---

## Deployment Locations

| Location | Scope | Best For |
|----------|-------|----------|
| `repo/.github/agents/` | Single repository | Project-specific agents |
| `org/.github-private/agents/` | All org repos | Organization standards |

### Repository-Level Deployment

```text
your-repo/
├── .github/
│   └── agents/
│       ├── docs-agent.agent.md
│       └── test-agent.agent.md
```text
### Organization-Level Deployment

```text
.github-private/
└── agents/
    ├── security-agent.agent.md
    └── code-review-agent.agent.md
```text
---

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

---

## Resources

### Official Documentation

- [Creating Custom Agents](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents)
- [Custom Agents Configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Copilot CLI for Testing](https://gh.io/customagents/cli)

### Community Resources

- [GitHub Blog: Writing Great Custom Agents](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- [Awesome Copilot Repository](https://github.com/github/awesome-copilot)
- [Community Agent Examples](https://montemagno.com/building-better-apps-with-github-copilot-custom-agents/)

### Related Files in This Repository

- [Agent Template](./agent-template.md)
- [Pre-built Agents](./README.md)
- [Prompt Engineering Guide](../docs/ultimate-prompting-guide.md)
- [Contributing Guidelines](../CONTRIBUTING.md)

---

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

**Happy coding with custom agents! 🚀**
