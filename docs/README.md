# Documentation

This directory contains comprehensive documentation for the Enterprise AI Prompt Library, organized by content type to help users learn, reference, and understand prompt engineering concepts.

## 📁 Directory Structure

```text
docs/
├── concepts/           # 📚 Fundamental concepts and theory
├── instructions/       # 🎯 GitHub Copilot instructions files
├── planning/          # 📋 Planning and architecture documents
├── reference/         # 🔍 Quick reference guides and lookups
├── research/          # 🔬 Research findings and analysis
└── tutorials/         # 🎓 Step-by-step learning guides
```

## 📚 Contents Overview

### Concepts

Foundational knowledge and theory behind prompt engineering:

- **[About Advanced Patterns](concepts/about-advanced-patterns.md)**: Introduction to CoT, ReAct, RAG, and other advanced techniques
- **[About Prompt Engineering](concepts/about-prompt-engineering.md)**: Core principles and strategies
- **[Model Capabilities](concepts/model-capabilities.md)**: Understanding different AI model strengths
- **[Prompt Anatomy](concepts/prompt-anatomy.md)**: Structure and components of effective prompts

**Best for**: Understanding the "why" behind prompting techniques, learning foundations before diving into implementation.

### Instructions

GitHub Copilot `.instructions.md` files for team-based consistency:

- **[C# Standards](instructions/csharp-standards.instructions.md)**: C# coding conventions
- **[.NET Stack](instructions/dotnet-stack.instructions.md)**: .NET development patterns
- **[Junior/Mid/Senior Developer](instructions/)**: Role-specific guidelines
- **[Security Compliance](instructions/security-compliance.instructions.md)**: Security best practices
- **[SQL Security](instructions/sql-security.instructions.md)**: Database security patterns

**Best for**: Teams using GitHub Copilot who need consistent code generation across developers.

### Planning

Strategic planning documents and architecture frameworks:

- **[Repository Cleanup Analysis](planning/REPOSITORY_CLEANUP_ANALYSIS.md)**: Repo maintenance planning
- **[Repo Update Tracking](planning/REPO_UPDATE_TRACKING.md)**: Change management documentation
- **[Tree-of-Thoughts Architecture](planning/tree-of-thoughts-architecture-evaluator.md)**: Advanced reasoning architecture
- **[Prompt Library Refactor](planning/prompt-library-refactor-react.md)**: Library evolution planning

**Best for**: Contributors, maintainers, and architects planning improvements or understanding library evolution.

### Reference

Quick lookup guides for fast answers:

- **[Cheat Sheet](reference/cheat-sheet.md)**: Quick patterns and templates (⚡ **Start here for fast answers**)
- **[Glossary](reference/glossary.md)**: Prompt engineering terminology
- **[Content Types](reference/content-types.md)**: Understanding different prompt formats
- **[Frontmatter Schema](reference/frontmatter-schema.md)**: Metadata standards for prompts
- **[Tasks Quick Reference](reference/TASKS_QUICK_REFERENCE.md)**: Common task patterns

**Best for**: Experienced users who need quick lookups, or anyone needing terminology definitions.

### Research

Research findings, analysis, and evidence-based documentation:

- **[Citation and Governance Research](research/CITATION_AND_GOVERNANCE_RESEARCH.md)**: Compliance frameworks
- **[CoVe Research](research/CoVe.md)**: Chain-of-Verification methodology
- **[Advanced Technique Research](research/advanced-technique-research.md)**: Peer-reviewed techniques
- **[Library Analysis](research/library-analysis-react.md)**: Prompt effectiveness studies
- **[RAG Document Retrieval](research/rag-document-retrieval.md)**: Retrieval-augmented generation patterns

**Best for**: Understanding the scientific basis behind prompting techniques, validating approaches, citing sources.

### Tutorials

Step-by-step learning guides for hands-on practice:

- **[Your First Prompt](tutorials/first-prompt.md)**: ⭐ **15-minute starter tutorial**
- **[Building Effective Prompts](tutorials/building-effective-prompts.md)**: Core skills development
- **[Prompt Iteration](tutorials/prompt-iteration.md)**: Improving prompt quality iteratively

**Best for**: New users, hands-on learners, anyone wanting practical step-by-step guidance.

## 🚀 Quick Start

### I'm brand new to prompts
→ Start with **[tutorials/first-prompt.md](tutorials/first-prompt.md)** (15 min)

### I need a quick pattern right now
→ Check the **[reference/cheat-sheet.md](reference/cheat-sheet.md)** (5 min)

### I want to understand the theory
→ Read **[concepts/about-prompt-engineering.md](concepts/about-prompt-engineering.md)** (20 min)

### I'm looking for research citations
→ Browse **[research/](research/)** directory

### I need team coding standards
→ Use **[instructions/](instructions/)** for Copilot

## 📖 Documentation Standards

All documentation follows these principles:

- ✅ **Clear structure**: Consistent heading hierarchy and sections
- ✅ **Practical examples**: Real-world code and usage samples
- ✅ **Metadata**: YAML frontmatter for categorization
- ✅ **Accessibility**: Written for multiple skill levels
- ✅ **Maintenance**: Regular updates tracked via Git

### Metadata Schema

Documentation files include YAML frontmatter:

```yaml
---
title: "Document Title"
description: "Brief description"
category: "concepts|instructions|planning|reference|research|tutorials"
tags: ["tag1", "tag2"]
author: "Author Name"
version: "1.0"
date: "2025-11-30"
difficulty: "beginner|intermediate|advanced"
estimated_time: "10 min"
---
```

## 🎯 Finding What You Need

| I Want To... | Go To... |
|-------------|----------|
| Learn from scratch | [tutorials/first-prompt.md](tutorials/first-prompt.md) |
| Get quick answers | [reference/cheat-sheet.md](reference/cheat-sheet.md) |
| Understand concepts | [concepts/](concepts/) |
| Set up team standards | [instructions/](instructions/) |
| Read research | [research/](research/) |
| See library evolution | [planning/](planning/) |

## 🤝 Contributing Documentation

We welcome documentation improvements! When contributing:

1. **Choose the right directory**:
   - `concepts/` for foundational knowledge
   - `tutorials/` for step-by-step guides
   - `reference/` for quick lookups
   - `research/` for evidence-based analysis
   - `instructions/` for Copilot team standards
   - `planning/` for architecture/strategy docs

2. **Follow the template**: Use existing docs as examples
3. **Include metadata**: Add YAML frontmatter
4. **Add examples**: Practical code samples required
5. **Test links**: Ensure all internal links work

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

## 📚 Related Resources

- **[Prompt Library](../prompts/)**: The actual prompt collection
- **[Tools](../tools/)**: CLI and evaluation utilities
- **[Main README](../README.md)**: Repository overview

## 🔄 Documentation Lifecycle

Documentation is continuously improved:

- **Version Control**: Track changes via Git
- **Community Review**: Open for feedback and PRs
- **Regular Updates**: Quarterly review cycles
- **Deprecation**: Outdated docs moved to `archive/`

## 📄 License

All documentation is licensed under [MIT License](../LICENSE).

---

**Questions or suggestions?** Open an issue or discussion in the [main repository](https://github.com/tafreeman/prompts).
