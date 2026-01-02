# Agents Reference

- Generated: 2025-12-19
- Files analyzed: 13
- Recommendation summary: 10 KEEP, 3 CONSOLIDATE, 0 ARCHIVE

## Summary

The `agents/` directory contains curated GitHub Copilot custom agent definitions, templates, and supporting guides. Each file encodes an agent persona, roles, boundaries, and tool capabilities intended to be deployed as Copilot custom agents or used as internal documentation for teams.

---

### `agent-template.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `agents/agent-template.md` |
| **Type** | Template |
| **Frontmatter** | Complete |
| **Lines** | ~140 |

#### Function

Provides a reusable template for authoring new agent persona files: frontmatter, role, responsibilities, tech stack, boundaries, and examples.

#### Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `name` | Yes | Agent identifier (snake_case) |

#### Use Cases

1. Create a new custom agent file.
2. Standardize agent metadata and guidance across repo.

#### Value Assessment

- **Recommendation**: KEEP

---

### `AGENTS_GUIDE.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `agents/AGENTS_GUIDE.md` |
| **Type** | Guide / How-To |
| **Frontmatter** | Complete |
| **Lines** | ~820 |

#### Function

Comprehensive guide describing how to create, deploy, and operate Copilot custom agents. Includes best practices, templates, and troubleshooting.

#### Variables

None (static guide)

#### Use Cases

1. Onboarding teams to custom agents.
2. Reference for creating agent frontmatter and tooling guidance.

#### Value Assessment

- **Recommendation**: CONSOLIDATE (merge with `README.md`/`index.md` into a single guide under `docs/`)

---

### `architecture-agent.agent.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `agents/architecture-agent.agent.md` |
| **Type** | Agent (Architecture) |
| **Frontmatter** | Complete |
| **Lines** | ~420 |

#### Function

Provides an expert architecture persona to produce ADRs, system design docs, diagrams, and trade-off analysis.

#### Variables

None

#### Use Cases

1. Draft ADRs and system design documentation.
2. Evaluate architecture trade-offs for projects.

#### Value Assessment

- **Unique Value**: Domain-specific architecture guidance and ADR templates
- **Overlap**: High-level guidance may overlap with cloud-agent for infra choices
- **Recommendation**: KEEP

---

### `cloud-agent.agent.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `agents/cloud-agent.agent.md` |
| **Type** | Agent (Cloud / Infra) |
| **Frontmatter** | Complete |
| **Lines** | ~1700 |

#### Function

Cloud architect persona covering IaC, migration, cost optimization, security, and operational recommendations. Includes command examples and templates.

#### Variables

None

#### Use Cases

1. Design cloud-native architectures and IaC patterns.
2. Generate migration and deployment plans.

#### Value Assessment

- **Unique Value**: Detailed IaC and cloud guidance across providers
- **Overlap**: Some overlap with `architecture-agent` on design rationale
- **Recommendation**: KEEP

---

### `code-review-agent.agent.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `agents/code-review-agent.agent.md` |
| **Type** | Agent (Code Review) |
| **Frontmatter** | Complete |
| **Lines** | ~560 |

#### Function

Multi-language code review persona that provides structured review comments, categories (security, performance, testing), and output templates for PR feedback.

#### Variables

None (expects PR/context input)

#### Use Cases

1. Generate PR review summaries and actionable comments.
2. Enforce coding standards and suggest improvements.

#### Value Assessment

- **Unique Value**: Rich, multi-language review format and tool integration notes
- **Overlap**: Compliments `security-agent` and `refactor-agent` but has distinct review focus
- **Recommendation**: KEEP

---

### `devsecops-tooling-agent.agent.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `agents/devsecops-tooling-agent.agent.md` |
| **Type** | Agent (DevSecOps Tooling) |
| **Frontmatter** | Complete |
| **Lines** | ~1400 |

#### Function

Persona for building CLI tools, evaluation frameworks, and CI/CD-focused automation. Includes coding style, testing, and improvement plans for tooling.

#### Variables

None

#### Use Cases

1. Implement or improve CLI tooling and evaluation scripts.
2. Define CI/CD patterns and testing workflows.

#### Value Assessment

- **Unique Value**: Deep, actionable guidance for tooling engineers and concrete improvement plans
- **Overlap**: Integrates with `test-agent` and repo tooling, but remains specialized
- **Recommendation**: KEEP

---

### `docs-agent.agent.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `agents/docs-agent.agent.md` |
| **Type** | Agent (Documentation) |
| **Frontmatter** | Complete |
| **Lines** | ~400 |

#### Function

Technical writing persona focused on READMEs, API docs, guides, and consistent markdown output formats and commands for local preview/validation.

#### Variables

None

#### Use Cases

1. Draft and improve repository documentation.
2. Produce consistent README and API references.

#### Value Assessment

- **Unique Value**: Practical docs templates and markdown tooling guidance
- **Overlap**: Minimal overlap; distinct role
- **Recommendation**: KEEP

---

### `index.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `agents/index.md` |
| **Type** | Category Landing / Index |
| **Frontmatter** | Complete |
| **Lines** | ~220 |

#### Function

Landing page that catalogs available agents and links to each agent definition and quick starts.

#### Variables

None

#### Use Cases

1. Navigation hub for readers browsing agent docs.
2. Quick-start pointers for common tasks.

#### Value Assessment

- **Recommendation**: CONSOLIDATE (merge into central guide to reduce duplication with `AGENTS_GUIDE.md` and `README.md`)

---

### `prompt-agent.agent.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `agents/prompt-agent.agent.md` |
| **Type** | Agent (Prompt Engineering) |
| **Frontmatter** | Complete |
| **Lines** | ~560 |

#### Function

Prompt engineering persona providing standards, scoring rubric, prompt templates, and advanced techniques (CoT, ReAct, RTF).

#### Variables

None

#### Use Cases

1. Create and refine prompts for various LLM platforms.
2. Provide validation rubrics and examples.

#### Value Assessment

- **Unique Value**: Centralized prompt engineering best practices and templates
- **Recommendation**: KEEP

---

### `refactor-agent.agent.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `agents/refactor-agent.agent.md` |
| **Type** | Agent (Refactor) |
| **Frontmatter** | Complete |
| **Lines** | ~730 |

#### Function

Refactoring persona with patterns, safe refactor rules, process steps, and examples across languages. Emphasizes tests-first and preserving behavior.

#### Variables

None

#### Use Cases

1. Propose incremental refactors with tests.
2. Generate before/after comparisons and rationale.

#### Value Assessment

- **Unique Value**: Practical refactoring patterns and safety processes
- **Recommendation**: KEEP

---

### `security-agent.agent.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `agents/security-agent.agent.md` |
| **Type** | Agent (Security) |
| **Frontmatter** | Complete |
| **Lines** | ~840 |

#### Function

Security analyst persona that identifies vulnerabilities, provides remediation, and supplies checks and scanning commands (bandit, gitleaks, etc.).

#### Variables

None

#### Use Cases

1. Perform code security assessments and produce remediation guidance.
2. Scan for secrets and common vulnerability patterns.

#### Value Assessment

- **Unique Value**: Security-focused checks and severity-driven output
- **Overlap**: Complements `code-review-agent` but with deep security heuristics
- **Recommendation**: KEEP

---

### `README.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `agents/README.md` |
| **Type** | Directory Overview / How-To |
| **Frontmatter** | Complete |
| **Lines** | ~260 |

#### Function

Repository-level overview of the agents directory, quick starts, and deployment notes for Copilot custom agents.

#### Use Cases

1. Quick onboarding for repository users.
2. Reference for where to place agent files and how to test locally.

#### Value Assessment

- **Recommendation**: CONSOLIDATE (merge into `AGENTS_GUIDE.md` or `docs/` single authoritative guide)

---

### `test-agent.agent.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `agents/test-agent.agent.md` |
| **Type** | Agent (Testing) |
| **Frontmatter** | Complete |
| **Lines** | ~920 |

#### Function

Test generation persona covering unit, integration, and e2e testing strategies across Python, JS/TS, and .NET. Provides examples and templates.

#### Variables

None

#### Use Cases

1. Generate test cases and fixtures for new or legacy code.
2. Recommend test strategies and tools.

#### Value Assessment

- **Unique Value**: Cross-language testing patterns and practical examples
- **Recommendation**: KEEP

---

## Workflow Map

- `index.md` / `README.md` / `AGENTS_GUIDE.md` — landing + how-to documentation; link to individual agent files.
- Individual agent files (e.g., `code-review-agent.agent.md`, `security-agent.agent.md`) — focused personas used independently in workflows (PR review, security assessment, documentation updates, infra design).
- `devsecops-tooling-agent.agent.md` and `test-agent.agent.md` — interact with repo tooling (`tools/`, `testing/`) and CI workflows.
- `agent-template.md` — starting point used when adding new agents; referenced by `AGENTS_GUIDE.md` and `README.md`.

## Consolidation Recommendations

| Source | Suggested Action | Rationale |
|--------|------------------|-----------|
| `AGENTS_GUIDE.md`, `README.md`, `index.md` | CONSOLIDATE into a single `docs/agents-guide.md` (or move `AGENTS_GUIDE.md` to `docs/` and deprecate `README.md`/`index.md`) | Reduce duplication, centralize onboarding and quick-starts for easier maintenance and linking from site generator |
| (optional) `AGENTS_GUIDE.md` examples | Move long command examples and deep reference sections into `docs/` pages and keep `agent-template.md` as the terse in-repo template | Improves discoverability and keeps repo agent files focused and small |

---

## Final Recommendations Summary

- KEEP (10): `agent-template.md`, and all individual agent personality files (`architecture-agent.agent.md`, `cloud-agent.agent.md`, `code-review-agent.agent.md`, `devsecops-tooling-agent.agent.md`, `docs-agent.agent.md`, `prompt-agent.agent.md`, `refactor-agent.agent.md`, `security-agent.agent.md`, `test-agent.agent.md`)
- CONSOLIDATE (3): `AGENTS_GUIDE.md`, `README.md`, `index.md` -> Merge into single guide under `docs/` and update links
- ARCHIVE (0)

---

Generated by an automated review of files in `agents/` on 2025-12-19.
