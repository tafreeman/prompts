---
applyTo: "**/*.cs,**/*.cshtml,**/*.razor"
---

# .NET Enterprise Technology Stack

## Backend Framework
- ASP.NET Core 8.0+ for web applications
- Entity Framework Core for data access with SQL Server
- Dependency injection using built-in ASP.NET Core DI container
- Repository pattern with Unit of Work for data layer abstraction

## Frontend Technology
- Razor Pages for server-side rendering
- Bootstrap 5+ for responsive UI components
- jQuery for client-side interactions (minimal usage)
- SignalR for real-time communications when required

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