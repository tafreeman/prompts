---
applyTo: "**/*"
---

# Enterprise Project Structure

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
    /Data                # Entity Framework context and repositories
    /Services            # External service implementations
/tests
  /UnitTests            # Unit test projects
  /IntegrationTests     # Integration test projects
/docs                   # Project documentation
/scripts                # Build and deployment scripts
```

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