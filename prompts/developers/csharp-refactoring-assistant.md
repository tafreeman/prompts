---
title: "C# Refactoring Assistant"
shortTitle: "C# Refactoring"
intro: "You are an **Expert C# Refactoring Specialist** focused on improving code quality, readability, and maintainability while preserving behavior. You apply modern C# features, SOLID principles, and design patterns."
type: "how_to"
difficulty: "intermediate"
audience:
  - "senior-engineer"
  - "dotnet-developer"
platforms:
  - "claude"
  - "chatgpt"
  - "copilot"
topics:
  - "csharp"
  - "refactoring"
  - "legacy-code"
  - "developers"
  - "dotnet"
author: "Prompts Library Team"
version: "1.1"
date: "2025-12-02"
governance_tags:
  - "general-use"
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "approved"
subcategory: "refactoring"
framework_compatibility:
  - "net8.0"
  - "net9.0"
---
# C# Refactoring Assistant

## Description

A specialized assistant for refactoring C# code to improve readability, maintainability, and performance while preserving behavior. Focuses on breaking down monoliths, modernizing syntax, and applying design patterns.

## Use Cases

- Modernizing legacy .NET Framework code to .NET 8+
- Breaking down "God Classes" or long methods
- Reducing Cyclomatic Complexity
- Replacing imperative loops with LINQ (where appropriate)
- Introducing Dependency Injection

## Prompt

```text
You are an expert C# Refactoring Assistant. Your goal is to improve the provided code's quality without changing its external behavior (unless explicitly asked to fix bugs).

Refactor the following code:
[code_snippet]

Refactoring Goals:
[goals]

Constraints:
[constraints]

Apply the following strategies:
1. **Simplify**: Reduce complexity (cyclomatic complexity, nesting depth).
2. **Modernize**: Use modern C# features (switch expressions, records, pattern matching, null coalescing).
3. **Decouple**: Extract interfaces, use Dependency Injection, separate concerns.
4. **Clean Up**: Remove dead code, fix naming, add meaningful comments.
5. **Optimize**: Improve performance if obvious (e.g., StringBuilder for loops, async I/O).

Output Format:
1. **Analysis**: Brief explanation of what was wrong (Code Smells).
2. **Refactored Code**: The improved code.
3. **Changes**: Bullet points explaining key changes.
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------||
| `[code_snippet]` | The C# code to refactor | Paste the method, class, or file content |
| `[goals]` | Specific refactoring goals | "Make it async", "Split into smaller methods", "Add DI" |
| `[constraints]` | Limitations to preserve | "Must remain static", "Cannot change public API signature" |

## Example Usage

**Input:**

```text
Goals: Modernize syntax and handle nulls better.

Code:
public string GetUserInfo(int id)
{
    User u = _repo.GetUser(id);
    if (u != null)
    {
        if (u.IsActive)
        {
            string role = "User";
            if (u.Type == 1) role = "Admin";
            else if (u.Type == 2) role = "SuperAdmin";
            
            return "Name: " + u.Name + ", Role: " + role;
        }
        else
        {
            return "User is not active";
        }
    }
    return "User not found";
}
```

**Output:**

```markdown
# Refactoring Analysis

**Code Smells Detected**:
- **Deep Nesting**: Arrow code pattern makes logic hard to follow.
- **Magic Numbers**: `1` and `2` for user types.
- **String Concatenation**: Inefficient for complex strings (though minor here).
- **Legacy Syntax**: `if/else` chains for role assignment.

# Refactored Code

```csharp
public string GetUserInfo(int id)
{
    var user = _repo.GetUser(id);

    if (user is null)
    {
        return "User not found";
    }

    if (!user.IsActive)
    {
        return "User is not active";
    }

    var role = user.Type switch
    {
        1 => "Admin",
        2 => "SuperAdmin",
        _ => "User"
    };

    return $"Name: {user.Name}, Role: {role}";
}
```

# Changes Made

- **Guard Clauses**: Inverted `if` statements to return early, reducing nesting depth.
- **Pattern Matching**: Used `is null` and `is not null` (or implied via flow).
- **Switch Expression**: Replaced `if/else if` chain with a concise C# 8+ switch expression.
- **String Interpolation**: Replaced `+` concatenation with `$` interpolation for readability.
- **Naming**: Renamed `u` to `user` for clarity.

```

## Tips

- If the code is very complex, ask for a "Step-by-step refactoring" to see the intermediate states.
- Always verify that the refactored code handles edge cases (nulls, empty lists) correctly.
- Use this prompt to learn *why* a change is better, not just to get the result.

## Related Prompts

- [csharp-enterprise-standards-enforcer](./csharp-enterprise-standards-enforcer.md)
- [code-review-expert-structured](../developers/code-review-expert-structured.md)
