# GitHub Copilot Custom Agents

This directory contains specialized GitHub Copilot custom agents designed for common development tasks. These agents are optimized for use with GitHub Copilot's coding agent feature.

## 📖 Overview

Custom agents are specialized AI personas that can be invoked to handle specific types of tasks. Each agent has:

- **Clear Role**: A specific domain expertise and responsibility
- **Defined Boundaries**: What the agent should and should not do
- **Consistent Output**: Predictable response format and quality
- **Tool Access**: Specific tools the agent is allowed to use

## 🚀 Quick Start

### Using Agents in GitHub Copilot

1. **Copy an agent file** to your repository's `.github/agents/` directory
2. **Merge to your default branch** to make the agent available
3. **Invoke the agent** using `@agent-name` in Copilot Chat

```sql
@docs-agent Update the README with installation instructions
@test-agent Generate unit tests for the UserService class
@code-review-agent Review the changes in this PR
```text
### Testing Locally

Use the [Copilot CLI](https://gh.io/customagents/cli) to test agents before deploying:

```bash
gh copilot agent test agents/docs-agent.agent.md
```text
## 📁 Available Agents

| Agent | File | Description | Best For |
|-------|------|-------------|----------|
| **Documentation** | `docs-agent.agent.md` | Technical writing specialist | README, API docs, guides |
| **Code Review** | `code-review-agent.agent.md` | Code quality reviewer | PR reviews, best practices |
| **Testing** | `test-agent.agent.md` | Test generation expert | Unit tests, integration tests |
| **Refactoring** | `refactor-agent.agent.md` | Code improvement specialist | Code cleanup, optimization |
| **Prompt Engineer** | `prompt-agent.agent.md` | Prompt creation expert | AI prompts, templates |
| **Security** | `security-agent.agent.md` | Security analysis expert | Vulnerability review, hardening |
| **Architecture** | `architecture-agent.agent.md` | System design specialist | Design decisions, patterns |

## 📋 Agent Template

Use the [agent-template.md](./agent-template.md) as a starting point for creating new agents.

## 🎯 Best Practices

### 1. Define Specialized Roles

Create agents with narrow, specific responsibilities rather than general-purpose helpers:

```yaml
# ❌ Too broad
name: helper
description: Helps with coding tasks

# ✅ Specific and focused
name: test_agent
description: Expert in test generation for Python applications using pytest
```text
### 2. Be Explicit About Tech Stack

Specify exact frameworks, versions, and tools:

```markdown
## Tech Stack
- Python 3.11+
- pytest with pytest-cov
- unittest.mock for mocking
- Black for formatting (line length 88)
```text
### 3. Set Clear Boundaries

Define what the agent should NOT do:

```markdown
## Boundaries
- Do NOT modify production code
- Do NOT access external APIs
- Do NOT commit changes directly
- Only work with files in `tests/` directory
```text
### 4. Provide Examples

Include concrete examples of expected output:

```markdown
## Example Output
```python
def test_user_creation():
    """Test that users can be created with valid data."""
    user = User(name="John", email="john@example.com")
    assert user.name == "John"
    assert user.email == "john@example.com"
```text
```text
### 5. Configure Tools Appropriately

Use the `tools` property to limit agent capabilities:

```yaml
---
name: docs_agent
description: Documentation specialist
tools: ["read", "write", "search"]
---
```text
## 🔧 Configuration Reference

### Frontmatter Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique identifier (use snake_case) |
| `description` | string | Yes | Brief description of agent purpose |
| `tools` | array | No | List of allowed tools |

### Tool Options

- `read` - Read file contents
- `write` - Create/modify files
- `search` - Search code and files
- `execute` - Run commands
- `github` - Access GitHub APIs

## 📚 Resources

- [GitHub Copilot Custom Agents Documentation](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents)
- [Custom Agents Configuration Reference](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [How to Write Great Custom Agents](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- [Community Examples](https://github.com/github/awesome-copilot)

## 🔄 Deployment Locations

| Location | Scope | Usage |
|----------|-------|-------|
| `.github/agents/` | Repository | Available in specific repo |
| `.github-private/agents/` | Organization | Available across all org repos |

## 🤝 Contributing

To add a new agent:

1. Copy `agent-template.md` to a new file
2. Fill in all required sections
3. Test locally with Copilot CLI
4. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

---

**Built with ❤️ for efficient AI-assisted development**
