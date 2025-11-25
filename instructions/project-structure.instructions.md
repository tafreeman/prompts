---
applyTo: "**/*"
name: "enterprise-project-structure"
description: "Define the standard layered solution structure, responsibilities, and testing organization for enterprise .NET projects"
---

# Enterprise Project Structure

> Purpose: Enforce a consistent, layered project structure across all enterprise .NET solutions to improve maintainability, testability, and onboarding.

## Solution Organization

```
/src
  /Web                    # ASP.NET Core web application
    /Pages               # Razor Pages
    /Controllers         # API Controllers
    /Models              # View Models and DTOs
    /Services            # Application services
  /Core                  # Business logic and domain models
    /Entities            # Domain entities
    /Interfaces          # Service contracts
    /Services            # Business services
  /Infrastructure        # Data access and external services
    /Data                # Entity Framework context, configurations, migrations, and repositories
    /Services            # External service implementations
/tests
  /UnitTests            # Unit test projects
  /IntegrationTests     # Integration test projects
/docs                   # Project documentation
/scripts                # Build and deployment scripts
```

## Layering and Responsibilities

- Web layer
  - Controllers and Razor Pages are thin endpoints responsible for HTTP concerns (routing, model binding, status codes)
  - All business logic is delegated to services defined in the Core layer
  - Do not place data access logic or complex business rules in controllers
- Core layer
  - Contains domain entities, value objects, and business service interfaces/implementations
  - Business rules live here and should be unit-testable without infrastructure dependencies
- Infrastructure layer
  - Contains Entity Framework DbContext, entity configurations, migrations, repositories, and external service implementations
  - Implements interfaces defined in the Core layer

## Configuration Management

- Use appsettings.json for environment-specific configuration
- Implement Azure Key Vault or similar for sensitive data
- Use environment variables for deployment-specific settings
- Maintain separate configurations for dev, test, and production

## Documentation Standards

- Maintain comprehensive README files
- Document API endpoints with OpenAPI/Swagger
- Create architecture decision records (ADRs)
- Provide deployment and operational guides
- When code comments or configuration reference traceability IDs (e.g., CAT-REQ-001.25, UAT-REQ-002.5), update the corresponding documentation in the /docs folder

## Testing Structure and Expectations

- Place unit tests under /tests/UnitTests and integration tests under /tests/IntegrationTests
- Ensure business services in the Core layer have unit tests that follow the Arrange-Act-Assert (AAA) pattern
- Mock external dependencies (e.g., infrastructure services, HTTP clients) in unit tests
- Use integration tests to validate behavior across Web, Core, and Infrastructure boundaries

### Example: Unit Test Structure

✅ **Correct placement and naming:**

```
/tests
  /UnitTests
    /Core
      /Services
        UserServiceTests.cs
```

```csharp
public class UserServiceTests
{
    [Fact]
    public async Task GetByIdAsync_ValidId_ReturnsUser()
    {
        // Arrange
        var mockRepo = new Mock<IUserRepository>();
        mockRepo.Setup(r => r.GetByIdAsync(It.IsAny<Guid>())).ReturnsAsync(new User());
        var service = new UserService(mockRepo.Object);

        // Act
        var result = await service.GetByIdAsync(Guid.NewGuid());

        // Assert
        Assert.NotNull(result);
    }
}
```

## Constraints and Fallbacks

- Do NOT deviate from the three-layer structure (Web, Core, Infrastructure) without architecture review and documented justification.
- When migrating legacy code, incrementally refactor toward this structure rather than creating parallel architectures.
- If project constraints prevent full layering (e.g., small utility services), document the simplified structure in the README and ensure Core business logic remains testable.

## Response Format Expectations

When generating or reviewing code structure using this guidance, use this format:

1. **Summary paragraph** – ≤3 sentences describing how the proposed structure aligns with the layered architecture.
2. **Bullet list of file/folder placements** – map each component (controller, service, repository, test) to its correct layer and folder.
3. **Code or folder structure example** – a short snippet or tree diagram showing the correct organization.
4. **Deviations note** – if the structure cannot fully match this template, explain why and propose the closest compliant alternative.
