---
applyTo: "**/*.cs,**/*.cshtml"
name: "junior-developer-guidance"
description: "Guidance for junior developers focusing on fundamentals and best practices"
---

# Junior Developer Guidance

> Purpose: Help junior engineers learn secure, maintainable .NET development through detailed explanations, clear examples, and learning-oriented prompts.

## Code Generation Focus

- Always request detailed comments explaining complex logic
- Ask for step-by-step breakdowns of algorithms and patterns
- Generate comprehensive error handling with clear error messages
- Include logging statements for debugging and monitoring

## Learning-Oriented Prompts

When asking Copilot for help, use these prompt patterns:

- "Explain the purpose of each line in this code"
- "Generate this method with detailed comments explaining the business logic"
- "Show me the best practice way to implement [specific pattern]"
- "What security considerations should I be aware of for this code?"

## Security-First Development

- Always validate user inputs with detailed validation attributes
- Request explanations of security implications for each code suggestion
- Ask for OWASP Top 10 compliance checks in generated code
- Generate secure configuration examples with explanations

## Code Review Preparation

- Generate comprehensive unit tests with clear test names
- Request code documentation following XML documentation standards
- Ask for performance considerations and optimization suggestions
- Generate logging statements for audit trail requirements

## Common Patterns to Request

### Example: Repository Pattern Request

✅ **Prompt to use:**

```
Generate a repository class for User entity with full CRUD operations,
error handling, and detailed comments explaining each method
```

✅ **Expected output includes:**

```csharp
public interface IUserRepository
{
    Task<User?> GetByIdAsync(Guid id);
    Task<IEnumerable<User>> GetAllAsync();
    Task AddAsync(User user);
    Task UpdateAsync(User user);
    Task DeleteAsync(Guid id);
}

public class UserRepository : IUserRepository
{
    private readonly AppDbContext _context;

    public UserRepository(AppDbContext context)
    {
        _context = context;
    }

    // Retrieves a user by ID with null-safety
    public async Task<User?> GetByIdAsync(Guid id)
    {
        return await _context.Users.FindAsync(id);
    }
    // ... additional methods with detailed comments
}
```

### Example: Model Validation Request

✅ **Prompt to use:**

```
Create model validation for user registration with detailed error messages
and security considerations explained
```

✅ **Expected output includes:**

```csharp
public class UserRegistrationModel
{
    [Required(ErrorMessage = "Email is required")]
    [EmailAddress(ErrorMessage = "Invalid email format")]
    public string Email { get; set; } = string.Empty;

    [Required(ErrorMessage = "Password is required")]
    [StringLength(100, MinimumLength = 8, ErrorMessage = "Password must be 8-100 characters")]
    [RegularExpression(@"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        ErrorMessage = "Password must contain uppercase, lowercase, digit, and special character")]
    public string Password { get; set; } = string.Empty;
}
```

## DoD-Specific Learning Points

- Always ask about compliance implications of code suggestions
- Request explanations of audit logging requirements
- Ask for secure coding practices specific to government applications
- Generate examples that demonstrate STIG compliance patterns

## Constraints and Fallbacks

- Do NOT accept code suggestions without detailed comments and explanations; always request clarity if missing.
- When security or compliance requirements are unclear, ask explicitly before proceeding (e.g., "What are the audit logging requirements for this feature?").
- If a generated pattern seems too complex for your current understanding, request a simpler alternative with step-by-step commentary.

## Response Format Expectations

When using this guidance to generate code or request AI assistance, expect responses in this structure:

1. **Summary paragraph** – ≤3 sentences explaining what the code does and which best practices it follows.
2. **Bullet list of learning points** – key concepts, patterns, or security considerations highlighted in the code.
3. **Code examples** – fully commented snippets (≤2 blocks) showing correct implementation.
4. **Next steps or additional resources** – suggestions for further learning or related patterns to explore.
