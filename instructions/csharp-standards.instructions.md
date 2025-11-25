---
applyTo: "**/*.cs"
name: "csharp-enterprise-coding-standards"
description: "Enforce secure, consistent enterprise C# coding and data access standards for mid-level and senior .NET backend engineers"
---

# C# Enterprise Coding Standards

> Prompt reference: see `dotnet-prompts/developers/csharp-enterprise-standards-enforcer.md` for the Tier 1 enforcement template that mirrors this instruction set.

## Prompt Integration

- Treat `csharp-enterprise-standards-enforcer.md` as the canonical AI prompt for these rules. Any edits to this file must be mirrored there (frontmatter metadata + section content) so the prompt and instructions stay synchronized.
- When new standards or response-format tweaks are required, update this document first, then apply the same wording to the prompt sections (`General Principles` through `Constraints and Fallbacks` plus the response-structure block).
- Use the prompt whenever AI output is needed; it already bakes in the response structure defined below (summary, standards-linked actions, code, deviations/assumptions).

## General Principles

- Write self-documenting code with clear, descriptive names
- Add XML documentation comments for all public classes, interfaces, and methods
- Follow SOLID principles and clean architecture patterns
- Implement comprehensive error handling with custom exceptions and structured logging
- Use async/await patterns for all I/O operations, including all database access

## Naming Conventions

- PascalCase for classes, methods, properties, and public fields
- camelCase for private fields, parameters, and local variables
- Prefix interfaces with 'I' (e.g., IUserService)
- Use meaningful names that describe purpose and intent

## Code Organization

- Separate concerns using layered architecture (Presentation, Business, Data)
- Use dependency injection for loose coupling
- Implement repository pattern for data access
- Create service classes for business logic
- Keep controllers and Razor pages thin; delegate business logic to services in the Core layer

## Security Practices

- Never hardcode sensitive information (connection strings, API keys)
- Use configuration providers for environment-specific settings
- Implement proper input validation and sanitization
- Use secure random number generation for cryptographic operations
- Use policy-based authorization and [Authorize] attributes on protected endpoints
- Always use parameterized queries or Entity Framework; never build SQL via string concatenation
- Log security-relevant events (authentication failures, authorization denials, unexpected input patterns)

## Performance Considerations

- Use appropriate data structures and algorithms
- Implement caching strategies for frequently accessed data
- Optimize database queries and use connection pooling
- Profile and monitor application performance regularly
- Implement pagination for endpoints that return large collections
- Use appropriate Entity Framework loading patterns (projection, Include, AsNoTracking) to avoid N+1 queries

## Error Handling Patterns

- In controllers and minimal APIs, use a consistent pattern:
  - Log when operations start and when they complete
- Catch unexpected exceptions at a central boundary (e.g., middleware) and map them to appropriate HTTP status codes
- Always log exceptions before mapping them to HTTP status codes. For unexpected exceptions, log the exception type, message, and stack trace using structured logging.
- Avoid returning raw exception details to callers
- Prefer domain-specific exception types for business rule violations and handle them explicitly (e.g., map to 400/404)

## Database and Persistence Practices

- Configure entity relationships explicitly in the Entity Framework model configuration (e.g., OnModelCreating or configuration classes)
- Include standard audit fields (e.g., CreatedAt, CreatedBy, UpdatedAt, UpdatedBy) on persisted entities where appropriate
- Prefer a soft-delete approach (e.g., IsDeleted flag) for entities that require logical deletion and auditing
- Ensure appropriate database indexes exist for frequently queried columns and foreign keys
- Follow the team's agreed naming conventions for tables, columns, and keys (see SQL and data modeling standards)

## Examples

### Secure Data Access (Parameterized Queries)

✅ Preferred:

```csharp
using var command = new SqlCommand(
    "SELECT * FROM Users WHERE Email = @email", connection);
command.Parameters.AddWithValue("@email", email);
```

❌ Avoid:

```csharp
var sql = $"SELECT * FROM Users WHERE Email = '{email}'";
```

### Layered Architecture Usage

✅ Preferred:

```csharp
public class UserController : ControllerBase
{
    private readonly IUserService _userService;

    public UserController(IUserService userService)
    {
        _userService = userService;
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetUser(Guid id)
    {
        var user = await _userService.GetByIdAsync(id);
        return user is null ? NotFound() : Ok(user);
    }
}
```

❌ Avoid:

```csharp
public class UserController : ControllerBase
{
    [HttpGet("{id}")]
    public async Task<IActionResult> GetUser(Guid id)
    {
        // Business logic and data access mixed in controller
        // ... direct DbContext or SqlCommand usage here ...
    }
}
```

## Constraints and Fallbacks

- Do NOT introduce new frameworks or patterns that conflict with these standards without explicit team approval.
- When a business requirement appears to violate these standards, first propose a compliant alternative. If no compliant option exists, explain the trade-offs and recommend the least risky deviation.
- If you cannot apply a standard due to missing context, state the assumption you are making and clearly label it as an assumption in your response.

## Response Format Expectations

When applying these standards in an AI-generated response or review, instruct the assistant to use this structure:

1. **Summary paragraph** – ≤3 sentences describing the main changes or recommendations.
2. **Bullet list of actions** – each bullet tied to a specific section of this document (e.g., "Security Practices", "Performance Considerations").
3. **Code block examples** – up to two short C# snippets that materially clarify the recommendation.
4. **Fallback note** – when a standard cannot be fully applied, include rationale and proposed alternatives.

Use the prompt referenced above whenever you need an AI-ready scaffold that guarantees these standards are enforced in generated or refactored C# code.
