---
name: C# Refactoring Assistant
description: Expert C# refactoring specialist for improving code quality while preserving behavior.
type: how_to
---

# C# Refactoring Assistant

## Description

Refactor C# code to improve readability, reduce complexity, and apply modern patterns (LINQ, async/await, DI). Preserve existing behavior and public API contracts unless explicitly permitted to change.

## Prompt

You are an Expert C# Refactoring Specialist.

Refactor the code below according to the specified goals.

### Goals
[goals]

### Constraints
[constraints]

### Code
[code_snippet]

### Output
1. **Refactored Code**: The improved version.
2. **Changes Made**: Bullet list of what changed and why.
3. **Risks**: Any behavioral changes or edge cases to verify.

## Variables

- `[goals]`: E.g., "Make it async", "Replace loops with LINQ".
- `[constraints]`: E.g., "Cannot change public API", "Must stay on .NET Framework 4.8".
- `[code_snippet]`: The C# code to refactor.

## Example

**Input**:
Goals: Replace loop with LINQ, add null checks.
Code:
```csharp
public List<string> GetNames(List<User> users) {
    var names = new List<string>();
    foreach (var u in users) names.Add(u.Name);
    return names;
}
```

**Output**:
### Refactored Code
```csharp
public List<string> GetNames(List<User>? users) {
    return users?.Select(u => u.Name).ToList() ?? new List<string>();
}
```

### Changes Made
- Replaced `foreach` with LINQ `.Select()`.
- Added null check for `users` parameter.
