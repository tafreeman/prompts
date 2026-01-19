# Reference

Quick-access documentation for schemas, terminology, templates, and standards. This directory provides fast lookups for prompt engineers working with the library on a daily basis.

## 📚 Overview

The **Reference** section is your quick-lookup hub for terminology, schemas, templates, and standards. Unlike tutorials (learning-focused) or concepts (theory-focused), reference docs are optimized for fast answers when you're actively working.

**Target Audience**: All users, especially those who need quick answers while building prompts or contributing to the library.

## 📁 Contents

| Document | Description | Use When... |
|----------|-------------|-------------|
| **[Cheat Sheet](cheat-sheet.md)** | ⚡ Quick patterns and templates for common tasks | You need a fast pattern right now |
| **[Glossary](glossary.md)** | Prompt engineering terminology and definitions | You encounter an unfamiliar term |
| **[Content Types](content-types.md)** | Guide to the six documentation types in the library | You're creating or categorizing docs |
| **[Frontmatter Schema](frontmatter-schema.md)** | Complete YAML metadata field reference | You're writing docs with frontmatter |
| **[Tasks Quick Reference](TASKS_QUICK_REFERENCE.md)** | Common prompt patterns organized by task type | You need a prompt for a specific task |

## 🎯 Use These Documents When...

- ✅ You need a **quick answer** without reading lengthy tutorials
- ✅ You're **actively coding** and need a pattern fast
- ✅ You encounter an **unfamiliar term** or acronym
- ✅ You're **writing documentation** and need metadata guidance
- ✅ You're **categorizing prompts** and need content type definitions
- ✅ You want a **quick reminder** of common patterns

## 🚀 Quick Access

### By Need

| I Need To... | Go To... | Time |
|--------------|----------|------|
| Find a prompt pattern quickly | [Cheat Sheet](cheat-sheet.md) | 2 min |
| Look up a term (CoT, RAG, etc.) | [Glossary](glossary.md) | 1 min |
| Understand content types | [Content Types](content-types.md) | 5 min |
| Add frontmatter to a doc | [Frontmatter Schema](frontmatter-schema.md) | 3 min |
| Get task-specific prompts | [Tasks Quick Reference](TASKS_QUICK_REFERENCE.md) | 5 min |

### By Experience Level

| Level | Start Here | Why |
|-------|-----------|-----|
| 🟢 Beginner | [Glossary](glossary.md) | Learn terminology first |
| 🟡 Intermediate | [Cheat Sheet](cheat-sheet.md) | Quick patterns for common tasks |
| 🔴 Advanced | [Tasks Quick Reference](TASKS_QUICK_REFERENCE.md) | Task-specific optimizations |

### By Activity

| What You're Doing | Reference Doc | What You'll Find |
|-------------------|---------------|------------------|
| **Writing prompts** | [Cheat Sheet](cheat-sheet.md) | Templates, patterns, examples |
| **Reading research** | [Glossary](glossary.md) | Technical term definitions |
| **Contributing docs** | [Frontmatter Schema](frontmatter-schema.md) | Required metadata fields |
| **Organizing content** | [Content Types](content-types.md) | Category definitions |
| **Solving specific problems** | [Tasks Quick Reference](TASKS_QUICK_REFERENCE.md) | Task-based prompt patterns |

## 📖 Reference Document Types

### Cheat Sheets

**Format**: Quick tables, code blocks, minimal explanation  
**Purpose**: Fast pattern lookup during active work  
**Example**: "Need a Chain-of-Thought prompt? Here's the template."

### Glossaries

**Format**: Alphabetical terms with concise definitions  
**Purpose**: Terminology lookup and disambiguation  
**Example**: "What does 'few-shot' mean?"

### Schemas

**Format**: Field definitions, types, validation rules  
**Purpose**: Structured data reference for metadata/config  
**Example**: "What fields are required in YAML frontmatter?"

### Quick References

**Format**: Organized lists, categorized patterns, decision trees  
**Purpose**: Task-based lookup for common scenarios  
**Example**: "What prompt pattern should I use for code review?"

## 🔗 Related Documentation

### Learning Resources
- **[Concepts](../concepts/)** — Theory and principles (read for understanding)
- **[Tutorials](../tutorials/)** — Step-by-step guides (read for learning)
- **[Research](../research/)** — Evidence and analysis (read for validation)

### Application
- **[Prompts Library](../../prompts/)** — Ready-to-use prompt templates
- **[Instructions](../instructions/)** — Team coding standards and personas
- **[Tools](../../tools/)** — CLI utilities for prompt management

### Contributing
- **[CONTRIBUTING.md](../../CONTRIBUTING.md)** — How to add or improve docs
- **[Planning](../planning/)** — Roadmap and architectural decisions

## 💡 Key Reference Resources

### Cheat Sheet Highlights

Quick access to:
- **Chain-of-Thought** (CoT) templates
- **Few-Shot** example structures
- **ReAct** reasoning loops
- **Structured output** formats (JSON, tables, lists)
- **Common roles** (code reviewer, technical writer, analyst)
- **Output constraints** (length, tone, format)

### Glossary Coverage

Definitions for:
- **Prompting Techniques**: CoT, ReAct, ToT, RAG, few-shot, zero-shot
- **AI Models**: GPT-4, Claude, Copilot, LLM concepts
- **Technical Terms**: Context window, temperature, tokens, embeddings
- **Patterns**: Meta-prompting, self-consistency, reflection
- **Evaluation**: Rubrics, benchmarks, quality metrics

### Frontmatter Fields

Complete reference for:
- **Required Fields**: title, type, difficulty, author
- **Optional Fields**: tags, platforms, audience, version
- **Governance Fields**: dataClassification, reviewStatus, PII handling
- **Organizational Fields**: category, subcategory, children
- **Metadata Fields**: date, lastUpdated, estimatedTime

### Content Types

Six primary types:
1. **Conceptual** — Theory and principles
2. **Reference** — Quick lookups and schemas
3. **Tutorial** — Step-by-step guides
4. **Prompt** — Ready-to-use templates
5. **Instruction** — Copilot configuration files
6. **Planning** — Architecture and roadmaps

## 🛠️ Using References Effectively

### During Development

**Keep cheat sheet open** in a second monitor or tab:
```bash
# Quick terminal access
cat docs/reference/cheat-sheet.md | less
```

**Bookmark glossary** for unfamiliar terms:
- Add browser bookmark for quick access
- Use Ctrl+F to search within the page

**Reference schema** when writing docs:
- Validate frontmatter fields before committing
- Ensure required fields are present
- Use consistent field formats

### For Teams

**Share quick references** in team channels:
```markdown
"Need a code review prompt? Check reference/cheat-sheet.md#code-review"
```

**Create custom reference docs** for team-specific patterns:
```markdown
# internal-reference.md
See [main cheat sheet](docs/reference/cheat-sheet.md)
Plus our team's custom patterns...
```

**Link to references** in PR templates:
```markdown
- [ ] Frontmatter follows [schema](docs/reference/frontmatter-schema.md)
- [ ] Content type matches [definitions](docs/reference/content-types.md)
```

## 📊 Reference Maintenance

### Update Frequency

- **Cheat Sheet**: Add new patterns as they're validated
- **Glossary**: Add terms when introduced in main docs
- **Schema**: Update when frontmatter fields change
- **Content Types**: Stable, rarely changes
- **Task Reference**: Add tasks as library grows

### Quality Standards

All reference docs must:
- ✅ Be **concise** — no lengthy explanations
- ✅ Be **scannable** — tables, bullets, headers
- ✅ Be **accurate** — regularly validated
- ✅ Be **complete** — cover all common cases
- ✅ Be **up-to-date** — reflect current standards

### Contributing Updates

Help keep references current:
- **Add new patterns** to cheat sheet
- **Define new terms** in glossary
- **Document new fields** in schema
- **Suggest reorganization** for better findability
- **Fix errors** or outdated information

## ❓ Frequently Asked Questions

**Q: What's the difference between reference and concepts?**  
A: **Reference** = quick lookup while working. **Concepts** = learning and understanding theory.

**Q: Should I read all reference docs?**  
A: No. Use them as needed. Skim once, then bookmark for lookups.

**Q: Can I print these for offline use?**  
A: Yes! Markdown renders well as PDF. Cheat sheet is especially useful printed.

**Q: Are references updated when library changes?**  
A: Yes. References are updated with each significant library change.

**Q: Can I add custom reference docs for my team?**  
A: Absolutely! Copy existing format and add team-specific content. Consider contributing back if generally useful.

**Q: How do I search across all reference docs?**  
A: Use GitHub's repository search or clone locally and use `grep`:
```bash
grep -r "chain-of-thought" docs/reference/
```

## 🤝 Contributing

Improve reference documentation:

- **Add missing patterns** to cheat sheet
- **Define new terms** in glossary
- **Clarify confusing sections** in any reference doc
- **Add examples** to schema documentation
- **Organize content** for better navigation
- **Create new quick references** for emerging needs

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## 📄 License

All reference documentation is licensed under [MIT License](../../LICENSE).

---

**Quick Links**:
- ⚡ [Cheat Sheet](cheat-sheet.md) — Fast patterns
- 📖 [Glossary](glossary.md) — Term definitions
- 📋 [Frontmatter Schema](frontmatter-schema.md) — Metadata reference
- 🎯 [Tasks Quick Reference](TASKS_QUICK_REFERENCE.md) — Task-based prompts
- 📚 [Content Types](content-types.md) — Doc categorization

---

**Next Steps**:
- 🚀 Bookmark: [Cheat Sheet](cheat-sheet.md) for daily use
- 📖 Learn: [Tutorials](../tutorials/) for deeper understanding
- 💬 Discuss: [GitHub Discussions](https://github.com/tafreeman/prompts/discussions)
