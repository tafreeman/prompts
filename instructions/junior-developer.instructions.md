---
applyTo: "**/*.cs,**/*.cshtml"
description: "Guidance for junior developers focusing on fundamentals and best practices"
---

# Junior Developer Guidance

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
```csharp
// Request detailed repository pattern implementations
"Generate a repository class for User entity with full CRUD operations, 
error handling, and detailed comments explaining each method"

// Ask for comprehensive validation examples
"Create model validation for user registration with detailed error messages 
and security considerations explained"

// Request secure API controller patterns
"Generate an API controller with proper authentication, authorization, 
input validation, and detailed comments on security measures"
```

## DoD-Specific Learning Points
- Always ask about compliance implications of code suggestions
- Request explanations of audit logging requirements
- Ask for secure coding practices specific to government applications
- Generate examples that demonstrate STIG compliance patterns