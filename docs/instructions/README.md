# Instructions

GitHub Copilot instruction files and custom personas for team-based AI-assisted development. These `.instructions.md` files ensure consistent code generation, enforce coding standards, and provide role-specific guidance across your entire team.

## 📚 Overview

The **Instructions** directory contains specialized configuration files that customize GitHub Copilot's behavior, enforce coding standards, and adopt specific developer personas. By adding these instructions to your project or user settings, you ensure all team members receive consistent, high-quality code suggestions aligned with your organization's standards.

**Target Audience**: Development teams using GitHub Copilot, ChatGPT, or Claude for code generation.

## 📁 Contents

### Developer Personas

Role-based instructions that adapt AI assistance to experience levels:

| Instruction File | Description | Best For |
|-----------------|-------------|----------|
| **[Junior Developer](junior-developer.instructions.md)** | Verbose explanations, learning-focused guidance | New developers, interns, bootcamp graduates |
| **[Mid-Level Developer](mid-level-developer.instructions.md)** | Balanced detail, best practices emphasis | Engineers with 2-5 years experience |
| **[Senior Developer](senior-developer.instructions.md)** | Concise, production-ready, design patterns | Experienced engineers, tech leads |
| **[Team Lead](team-lead.instructions.md)** | Code review focus, mentorship guidance, architecture | Tech leads, engineering managers |

### Technology Standards

Language and framework-specific coding conventions:

| Instruction File | Description | Best For |
|-----------------|-------------|----------|
| **[C# Standards](csharp-standards.instructions.md)** | C# coding conventions, naming, patterns | .NET development teams |
| **[.NET Stack](dotnet-stack.instructions.md)** | ASP.NET Core, Entity Framework patterns | Full-stack .NET projects |
| **[Razor Standards](razor-standards.instructions.md)** | Razor Pages, Blazor conventions | ASP.NET web UI development |
| **[Project Structure](project-structure.instructions.md)** | Solution architecture, file organization | Enterprise .NET applications |

### Security & Compliance

Security-focused instructions for hardened code generation:

| Instruction File | Description | Best For |
|-----------------|-------------|----------|
| **[Security Compliance](security-compliance.instructions.md)** | Secure coding practices, OWASP guidelines | Security-critical applications |
| **[SQL Security](sql-security.instructions.md)** | Parameterized queries, injection prevention | Database-heavy applications |

## 🎯 Use These Instructions When...

- ✅ You want **consistent code style** across your team
- ✅ You need to **enforce security standards** in AI-generated code
- ✅ You're **onboarding new developers** and need consistent guidance
- ✅ You want **role-appropriate code suggestions** (junior vs senior)
- ✅ You're working on **regulated projects** requiring compliance
- ✅ You need **framework-specific patterns** (e.g., ASP.NET Core)

## 🚀 Getting Started

### Quick Setup (5 minutes)

**For Individual Use (GitHub Copilot)**:

1. Open VS Code / Visual Studio
2. Go to Copilot settings → Custom Instructions
3. Copy content from relevant `.instructions.md` file
4. Paste into custom instructions field
5. Save and restart your editor

**For Team Use (Repository-Level)**:

1. Add `.github/copilot-instructions.md` to your repo
2. Combine multiple instruction files as needed
3. Commit to your repository
4. All team members automatically inherit these instructions

**For ChatGPT/Claude**:

1. Copy instruction file content
2. Paste into custom instructions or system prompt
3. Use for all coding sessions

### Recommended Combinations

**Full-Stack .NET Developer**:
```markdown
Combine:
- Senior Developer (senior-developer.instructions.md)
- C# Standards (csharp-standards.instructions.md)
- .NET Stack (dotnet-stack.instructions.md)
- Security Compliance (security-compliance.instructions.md)
```

**Security-Focused Team**:
```markdown
Combine:
- Senior Developer (senior-developer.instructions.md)
- Security Compliance (security-compliance.instructions.md)
- SQL Security (sql-security.instructions.md)
```

**Junior Developer Onboarding**:
```markdown
Combine:
- Junior Developer (junior-developer.instructions.md)
- C# Standards (csharp-standards.instructions.md)
- Project Structure (project-structure.instructions.md)
```

**Tech Lead / Code Reviewer**:
```markdown
Combine:
- Team Lead (team-lead.instructions.md)
- Security Compliance (security-compliance.instructions.md)
- C# Standards (csharp-standards.instructions.md)
```

## 📖 How to Use

### Individual Developer Workflow

1. **Choose your persona** (Junior/Mid/Senior/Lead)
2. **Add technology standards** for your stack
3. **Include security guidelines** for sensitive projects
4. **Test the instructions** with a few code generation tasks
5. **Refine** based on output quality

### Team Adoption Strategy

1. **Discuss standards** with your team
2. **Create repository instructions** combining relevant files
3. **Document in team wiki** which instructions to use
4. **Train team members** on how instructions affect output
5. **Iterate** based on team feedback

### Before/After Examples

**Without Instructions**:
```csharp
// Generic, may not follow team standards
public string GetUser(int id) {
    var user = db.Users.Find(id);
    return user.Name;
}
```

**With Senior Developer + C# Standards + SQL Security Instructions**:
```csharp
/// <summary>
/// Retrieves user name by ID with parameterized query to prevent SQL injection.
/// </summary>
/// <param name="userId">The unique identifier of the user.</param>
/// <returns>The user's full name, or null if not found.</returns>
/// <exception cref="ArgumentException">Thrown when userId is less than 1.</exception>
public async Task<string?> GetUserNameAsync(int userId)
{
    if (userId < 1)
        throw new ArgumentException("User ID must be positive", nameof(userId));

    return await _context.Users
        .Where(u => u.Id == userId)
        .Select(u => u.FullName)
        .FirstOrDefaultAsync();
}
```

## 🔗 Related Documentation

### Setup & Configuration
- **[GitHub Copilot Documentation](https://docs.github.com/en/copilot)** — Official setup guide
- **[VS Code Copilot Settings](https://code.visualstudio.com/docs/copilot/overview)** — Editor configuration
- **[Custom Instructions Guide](https://platform.openai.com/docs/guides/prompt-engineering)** — General guidance

### Learning Resources
- **[Concepts](../concepts/)** — Understand prompting theory
- **[Tutorials](../tutorials/)** — Hands-on prompt engineering practice
- **[Reference](../reference/)** — Quick lookups and cheat sheets

### Enterprise Use
- **[Planning](../planning/)** — Architecture and governance frameworks
- **[Research](../research/)** — Evidence-based best practices

## 💡 Key Capabilities

### Role-Based Personas

**Junior Developer Instructions Provide**:
- Detailed explanations for each code suggestion
- Links to documentation and learning resources
- Step-by-step guidance for complex tasks
- Emphasis on understanding over speed

**Senior Developer Instructions Provide**:
- Concise, production-ready code
- Design patterns and SOLID principles
- Performance and scalability considerations
- Minimal comments, self-documenting code

**Team Lead Instructions Provide**:
- Code review checklists
- Architectural guidance and trade-offs
- Mentorship-focused explanations
- Cross-cutting concerns (security, performance, maintainability)

### Technology Standards

- **Naming Conventions**: Pascal/camelCase rules
- **Code Organization**: File structure, namespaces
- **Framework Patterns**: Repository, dependency injection, middleware
- **Error Handling**: Exception strategies, logging
- **Documentation**: XML comments, README standards

### Security Features

- **Input Validation**: Prevent injection attacks
- **Authentication/Authorization**: Secure access patterns
- **Data Protection**: Encryption, sensitive data handling
- **Dependency Management**: Secure package usage
- **Logging**: Audit trails without exposing secrets

## 🛠️ Customization

### Creating Your Own Instructions

1. **Start with a base** (e.g., `senior-developer.instructions.md`)
2. **Add organization-specific rules**:
   ```markdown
   ## Company-Specific Standards
   - Use internal NuGet feed: https://nuget.company.com
   - Follow CompanyName.Namespace.Project naming
   - Include JIRA ticket references in commit messages
   ```
3. **Test thoroughly** with various code generation scenarios
4. **Share with team** and iterate based on feedback

### Maintaining Instructions

- **Review quarterly** to align with evolving best practices
- **Update for new framework versions** (e.g., .NET 9)
- **Gather feedback** from developers using them
- **Version control** changes for rollback capability
- **Document updates** in team communications

## 📊 Measuring Impact

Track these metrics to validate instruction effectiveness:

- **Code Review Feedback**: Fewer standards violations
- **Security Findings**: Reduced vulnerability reports
- **Onboarding Time**: Faster new developer productivity
- **Consistency**: More uniform codebase style
- **Developer Satisfaction**: Improved AI assistance quality

## ❓ Frequently Asked Questions

**Q: Can I use multiple instruction files at once?**  
A: Yes! Combine them by copying all relevant sections into a single file or your Copilot settings.

**Q: Do instructions work with all AI coding assistants?**  
A: Yes. While optimized for GitHub Copilot, they work with ChatGPT, Claude, and other LLM-based coding tools.

**Q: How long are instructions "remembered"?**  
A: Instructions persist for the entire session. Repository-level instructions are always active.

**Q: Can instructions conflict with each other?**  
A: Generally no, but be mindful when combining. Test combined instructions to ensure coherent behavior.

**Q: Are these instructions updated for new language versions?**  
A: Yes. We update standards when new framework versions release (e.g., C# 13, .NET 9).

**Q: Can I share customized instructions with the community?**  
A: Absolutely! Submit a PR to add organization-specific instructions (with sensitive info removed).

## 🤝 Contributing

Help expand and improve instruction files:

- **Add new personas** (QA Engineer, DevOps, Data Scientist)
- **Create language standards** (Python, TypeScript, Go)
- **Enhance security guidelines** with emerging threats
- **Share before/after examples** showing instruction impact
- **Translate instructions** for non-English teams

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## 📄 License

All instruction files are licensed under [MIT License](../../LICENSE).

---

**Next Steps**:
- 🚀 Quick setup: Copy [Senior Developer](senior-developer.instructions.md) to your Copilot settings
- 📖 Learn more: [About Prompt Engineering](../concepts/about-prompt-engineering.md)
- 💬 Share feedback: [GitHub Discussions](https://github.com/tafreeman/prompts/discussions)
