---
applyTo: "**/*.cs,**/*.cshtml,**/*.razor"
name: "dotnet-enterprise-technology-stack"
description: "Standardize the default .NET, database, and security stack for enterprise applications"
---

# .NET Enterprise Technology Stack

> Purpose: Provide a default, opinionated .NET stack for enterprise projects so AI assistants and developers consistently target the same frameworks, libraries, and security posture.

## Backend Framework

- ASP.NET Core 8.0+ for web applications
- Entity Framework Core for data access with SQL Server
- Dependency injection using built-in ASP.NET Core DI container
- Repository pattern with Unit of Work for data layer abstraction

### Backend Example (✅ Target Stack)

```csharp
var builder = WebApplication.CreateBuilder(args);

// ASP.NET Core 8 backend with EF Core and DI
builder.Services.AddDbContext<AppDbContext>(options =>
	options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();

var app = builder.Build();
app.MapControllers();
app.Run();
```

## Frontend Technology

- Razor Pages for server-side rendering
- Bootstrap 5+ for responsive UI components
- jQuery for client-side interactions (minimal usage)
- SignalR for real-time communications when required

### Frontend Example (✅ Razor + Bootstrap)

```cshtml
@page
@model IndexModel

<div class="container mt-4">
	<h1 class="display-6">Dashboard</h1>
	<button class="btn btn-primary">Refresh</button>
</div>
```

## Database Standards

- SQL Server 2022 with Always Encrypted for sensitive data
- Stored procedures for complex business logic
- Database migrations using Entity Framework Core
- Connection string encryption and secure configuration

## Security Framework

- ASP.NET Core Identity for authentication/authorization
- JWT tokens for API authentication
- HTTPS enforcement with HSTS headers
- Content Security Policy (CSP) implementation

## Constraints and Fallbacks

- Do NOT introduce alternative web frameworks or ORMs (e.g., NancyFX, Dapper-only) for new services without explicit architecture approval.
- When an existing system cannot adopt this full stack, align to it where feasible (e.g., keep SQL Server + EF Core) and document justified deviations.
- If stack details are missing (e.g., database version, auth mechanism), state assumptions explicitly in your response and label them as assumptions.

## Response Format Expectations

When using this instructions file to guide AI-generated designs or code, use this structure:

1. **Summary paragraph** – ≤3 sentences describing how the proposed solution aligns to this .NET stack.
2. **Bullet list of stack choices** – backend, frontend, database, security, each mapped back to sections above.
3. **Code examples** – up to two short snippets (e.g., `Program.cs` setup, Razor page) demonstrating correct stack usage.
4. **Fallback note** – describe any deviations from the standard stack, why they are required, and proposed mitigation.
