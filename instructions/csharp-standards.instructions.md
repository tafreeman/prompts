---
applyTo: "**/*.cs"
---

# C# Enterprise Coding Standards

## General Principles
- Write self-documenting code with clear, descriptive names
- Follow SOLID principles and clean architecture patterns
- Implement comprehensive error handling with custom exceptions
- Use async/await patterns for all I/O operations

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

## Security Practices
- Never hardcode sensitive information (connection strings, API keys)
- Use configuration providers for environment-specific settings
- Implement proper input validation and sanitization
- Use secure random number generation for cryptographic operations

## Performance Considerations
- Use appropriate data structures and algorithms
- Implement caching strategies for frequently accessed data
- Optimize database queries and use connection pooling
- Profile and monitor application performance regularly