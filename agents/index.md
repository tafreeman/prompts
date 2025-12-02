---
title: "AI Agents & Personas"
shortTitle: "Agents"
intro: "Specialized agent definitions for autonomous workflows and multi-turn tasks."
type: "reference"
difficulty: "advanced"
audience:
  - "senior-engineer"
  - "solution-architect"
platforms:
  - "github-copilot"
  - "azure-openai"
author: "Prompt Library Team"
version: "1.0"
date: "2025-12-02"
governance_tags:
  - "PII-safe"
dataClassification: "public"
reviewStatus: "draft"
layout: "category-landing"
children:
  - /agents/architecture-agent.agent
  - /agents/code-review-agent.agent
  - /agents/docs-agent.agent
  - /agents/prompt-agent.agent
  - /agents/refactor-agent.agent
  - /agents/security-agent.agent
  - /agents/test-agent.agent
featuredLinks:
  gettingStarted:
    - /agents/AGENTS_GUIDE
    - /agents/agent-template
  popular:
    - /agents/code-review-agent.agent
    - /agents/docs-agent.agent
    - /agents/test-agent.agent
---

# AI Agents & Personas

Deploy specialized AI personas to handle complex, multi-step development tasks. These agents are designed to work autonomously or as part of a team, each with a defined role, set of tools, and operational boundaries.

## In This Section

| Agent | Role | Best For |
|-------|------|----------|
| **[Docs Agent](/agents/docs-agent.agent)** | Technical Writer | Generating READMEs, API docs, and guides |
| **[Code Review Agent](/agents/code-review-agent.agent)** | Senior Engineer | Reviewing PRs for quality, security, and style |
| **[Test Agent](/agents/test-agent.agent)** | QA Engineer | Writing unit and integration tests |
| **[Refactor Agent](/agents/refactor-agent.agent)** | Code Cleaner | Optimizing legacy code and reducing debt |
| **[Security Agent](/agents/security-agent.agent)** | Security Analyst | Identifying vulnerabilities and hardening code |
| **[Architecture Agent](/agents/architecture-agent.agent)** | System Architect | Designing systems and evaluating patterns |
| **[Prompt Agent](/agents/prompt-agent.agent)** | Prompt Engineer | Crafting and refining AI prompts |

## Quick Starts

- **Need documentation?** Invoke `@docs-agent` to draft a README or explain a complex module.
- **Reviewing code?** Ask `@code-review-agent` to analyze your changes before submitting a PR.
- **Writing tests?** Let `@test-agent` generate a test suite for your new class.

## Browse by Capability

### Development & Quality
- [Code Review Agent](/agents/code-review-agent.agent)
- [Test Agent](/agents/test-agent.agent)
- [Refactor Agent](/agents/refactor-agent.agent)

### Design & Security
- [Architecture Agent](/agents/architecture-agent.agent)
- [Security Agent](/agents/security-agent.agent)

### Content & Operations
- [Docs Agent](/agents/docs-agent.agent)
- [Prompt Agent](/agents/prompt-agent.agent)

---

**Tip:** Use the [Agent Template](/agents/agent-template) to create your own custom agents tailored to your specific workflow.
