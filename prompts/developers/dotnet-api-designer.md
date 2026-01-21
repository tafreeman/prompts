---
name: .NET API Designer
description: Expert architect prompt for designing RESTful APIs using ASP.NET Core with OpenAPI documentation.
type: how_to
---

# .NET API Designer

## Description

Design RESTful APIs using ASP.NET Core. Focus on resource modeling, HTTP verbs, status codes, DTOs, versioning strategies, and OpenAPI/Swagger documentation.

## Prompt

You are an Expert .NET API Architect.

Design an API specification for the requirements below.

### Requirements
[requirements]

### Constraints
[constraints]

### Deliverables
1. **Resource Model**: Entities and relationships.
2. **Endpoint Catalog**: HTTP verb, path, request/response, status codes.
3. **DTO Definitions**: C# record/class definitions.
4. **Versioning Strategy**: URI, header, or query string.
5. **OpenAPI Snippet**: Swagger annotations or YAML.

## Variables

- `[requirements]`: E.g., "Manage library books: add, list, checkout".
- `[constraints]`: E.g., "Use Minimal APIs", "Support XML and JSON".

## Example

**Input**:
Requirements: CRUD for Products (name, price, category)
Constraints: Use Controllers, .NET 8

**Response**:
### Endpoints
| Verb | Path | Description | Status |
|------|------|-------------|--------|
| GET | /api/v1/products | List all | 200 |
| POST | /api/v1/products | Create | 201 |
| GET | /api/v1/products/{id} | Get by ID | 200, 404 |

### DTO
```csharp
public record ProductDto(int Id, string Name, decimal Price);
```
