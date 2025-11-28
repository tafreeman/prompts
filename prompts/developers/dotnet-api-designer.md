---
title: ".NET API Designer"
category: "developers"
subcategory: "api-design"
tags: ["dotnet", "api", "rest", "openapi", "aspnet-core"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-26"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
framework_compatibility: ["net8.0", "net9.0"]
---

# .NET API Designer

## Description

Expert architect for designing RESTful APIs using ASP.NET Core. Focuses on resource modeling, URL structure, HTTP verbs, status codes, OpenAPI (Swagger) documentation, and versioning strategies.

## Use Cases

- Designing new microservice APIs
- Creating OpenAPI/Swagger specifications
- Defining DTOs (Data Transfer Objects) and Contracts
- Planning API versioning and breaking change strategies

## Prompt

```text
You are a Senior API Architect specializing in ASP.NET Core. Design a RESTful API for the following requirements.

Requirements:
[requirements]

Constraints:
[constraints]

Deliverables:
1. **Endpoints**: List of endpoints with HTTP verbs and resource paths.
2. **Contracts**: C# definitions for Request/Response DTOs (records preferred).
3. **Controller/Endpoint Code**: Example implementation (Controller or Minimal API).
4. **OpenAPI**: Key Swagger annotations/attributes.

Guidelines:
- **REST Maturity**: Level 2 (Resources, Verbs, Status Codes) minimum.
- **Naming**: Plural nouns for resources (e.g., `/users`), kebab-case for URLs.
- **Status Codes**: Correct use of 200, 201, 204, 400, 404, 500.
- **Versioning**: URL or Header-based versioning.
- **Validation**: FluentValidation or DataAnnotations.
- **Async**: All operations must be async.
```

## Variables

- `[requirements]`: Functional requirements (e.g., "Manage library books: add, list, checkout")
- `[constraints]`: Technical constraints (e.g., "Use Minimal APIs", "Must support XML and JSON")

## Example Usage

**Input:**

```text
Requirements: API for a Todo application. Users can create todos, list their own todos (with filtering by 'isComplete'), mark a todo as complete, and delete a todo.
Constraints: Use ASP.NET Core Minimal APIs.
```

**Output:**

```markdown
# API Design: Todo Service

## 1. Endpoints

| Verb | Path | Description | Status Codes |
|------|------|-------------|--------------|
| GET | `/api/v1/todos` | List user's todos | 200 |
| POST | `/api/v1/todos` | Create a new todo | 201, 400 |
| GET | `/api/v1/todos/{id}` | Get specific todo | 200, 404 |
| PUT | `/api/v1/todos/{id}` | Update todo | 204, 400, 404 |
| DELETE | `/api/v1/todos/{id}` | Delete todo | 204, 404 |

## 2. Contracts (DTOs)

```csharp
public record CreateTodoRequest(string Title, string? Description, DateTime? DueDate);
public record UpdateTodoRequest(string Title, string? Description, bool IsComplete);
public record TodoResponse(Guid Id, string Title, string? Description, bool IsComplete, DateTime CreatedAt);
```

## 3. Implementation (Minimal API)

```csharp
var app = WebApplication.Create(args);

var todos = app.MapGroup("/api/v1/todos")
    .WithTags("Todos")
    .WithOpenApi();

todos.MapGet("/", async (ITodoService service, [AsParameters] TodoFilter filter) =>
{
    var results = await service.GetAllAsync(filter);
    return Results.Ok(results);
})
.Produces<IEnumerable<TodoResponse>>(200);

todos.MapPost("/", async (ITodoService service, [FromBody] CreateTodoRequest request) =>
{
    var created = await service.CreateAsync(request);
    return Results.Created($"/api/v1/todos/{created.Id}", created);
})
.Produces<TodoResponse>(201)
.ProducesValidationProblem(400);

todos.MapPut("/{id:guid}", async (ITodoService service, Guid id, [FromBody] UpdateTodoRequest request) =>
{
    var updated = await service.UpdateAsync(id, request);
    return updated ? Results.NoContent() : Results.NotFound();
})
.Produces(204)
.Produces(404);
```

```

## Tips

- Specify if you prefer **Controllers** (`BaseController`) or **Minimal APIs**.
- Ask for **HATEOAS** links if you need Level 3 REST maturity.
- Request **Idempotency** handling for critical POST/PATCH operations.

## Related Prompts

- [api-design-consultant](../developers/api-design-consultant.md) (More general)
- [csharp-enterprise-standards-enforcer](./csharp-enterprise-standards-enforcer.md)

## Changelog

### Version 1.0 (2025-11-26)
- Initial release
Create 5 missing developer prompts (conversation 68330b60)
