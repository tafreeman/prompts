---
title: "Single-Agent Code Review Workflow"
category: "techniques"
subcategory: "agentic"
technique_type: "autonomous-agent"
framework_compatibility:
  openai: ">=1.0.0"
  anthropic: ">=0.8.0"
difficulty: "intermediate"
use_cases:
  - code-review
  - refactoring
  - technical-debt-analysis
  - security-scanning
performance_metrics:
  accuracy_improvement: "25-35%"
  latency_impact: "low"
  cost_multiplier: "1.2-1.5x"
version: "1.0.0"
author: "AI Research Team"
last_updated: "2025-11-23"
tags:
  - single-agent
  - code-review
  - autonomous
  - dotnet
  - csharp
---

# Single-Agent Code Review Workflow

## Purpose

Implements an autonomous single-agent pattern for comprehensive code review that handles the entire review lifecycle—from initial analysis through generating actionable feedback—without requiring multiple specialized agents.

## Overview

This pattern uses a single, well-instructed AI agent with clear phases to:

1. Understand the code context and purpose
2. Analyze for issues (bugs, security, performance, style)
3. Prioritize findings by severity
4. Generate detailed, actionable feedback

Ideal for .NET/C# codebases where you need consistent, thorough reviews.

## Prompt Template

```markdown
You are an expert C# code reviewer with deep knowledge of:
- .NET best practices and patterns
- SOLID principles and clean architecture
- Security vulnerabilities (OWASP Top 10)
- Performance optimization
- SQL injection and data access patterns

**Your Task**: Review the following C# code and provide comprehensive feedback.

**Code to Review**:
```csharp
{{code}}
```

**Context**:

- Project Type: {{project_type}} (e.g., ASP.NET Core Web API, Console App)
- Framework: {{framework}} (e.g., .NET 6, .NET Framework 4.8)
- Database: {{database}} (e.g., SQL Server, PostgreSQL)

**Review Process**:

### Phase 1: Initial Analysis

1. Understand the code's purpose and intended behavior
2. Identify the key components and their responsibilities
3. Note any missing context that would affect the review

### Phase 2: Issue Detection

Scan for issues in these categories:

- **Bugs**: Logic errors, null reference risks, edge cases
- **Security**: SQL injection, XSS, sensitive data exposure, authentication/authorization
- **Performance**: N+1 queries, inefficient algorithms, memory leaks
- **Maintainability**: Code smells, SOLID violations, poor naming
- **Style**: Inconsistent formatting, missing documentation

### Phase 3: Prioritization

Classify each finding as:

- **Critical**: Security vulnerabilities, data loss risks, production blockers
- **High**: Bugs that affect functionality, performance bottlenecks
- **Medium**: Code quality issues, maintainability concerns
- **Low**: Style inconsistencies, minor improvements

### Phase 4: Recommendations

For each issue:

1. Explain the problem clearly
2. Show the problematic code snippet
3. Provide a corrected version
4. Explain why the fix is better

**Output Format**:

```markdown
## Summary
[2-3 sentence overview of code quality and major concerns]

## Critical Issues
[If any, list with code examples and fixes]

## High Priority Issues
[List with examples and fixes]

## Medium Priority Issues
[List with examples and fixes]

## Low Priority Issues
[List with examples and fixes]

## Positive Observations
[What the code does well]

## Overall Score: X/10
[Brief justification]
```

```

## Usage Example

### Input

**Code**:
```csharp
public class UserService
{
    private string _connectionString = "Server=prod;Database=Users;User Id=admin;Password=admin123;";
    
    public User GetUser(string userId)
    {
        using (var conn = new SqlConnection(_connectionString))
        {
            conn.Open();
            var cmd = new SqlCommand("SELECT * FROM Users WHERE Id = '" + userId + "'", conn);
            var reader = cmd.ExecuteReader();
            
            if (reader.Read())
            {
                return new User 
                { 
                    Id = reader["Id"].ToString(),
                    Name = reader["Name"].ToString(),
                    Email = reader["Email"].ToString()
                };
            }
        }
        return null;
    }
}
```

**Context**:

- Project Type: ASP.NET Core Web API
- Framework: .NET 6
- Database: SQL Server

### Output

```markdown
## Summary
This UserService contains critical security vulnerabilities (SQL injection, hardcoded credentials) and lacks proper error handling. The code needs immediate refactoring before deployment.

## Critical Issues

### 1. SQL Injection Vulnerability
**Problem**: User input (`userId`) is concatenated directly into SQL query.
**Risk**: Attackers can execute arbitrary SQL commands.

**Problematic Code**:
```csharp
var cmd = new SqlCommand("SELECT * FROM Users WHERE Id = '" + userId + "'", conn);
```

**Fix**:

```csharp
var cmd = new SqlCommand("SELECT * FROM Users WHERE Id = @UserId", conn);
cmd.Parameters.AddWithValue("@UserId", userId);
```

### 2. Hardcoded Credentials

**Problem**: Database credentials are hardcoded in source code.
**Risk**: Credentials exposed in version control, logs, or memory dumps.

**Fix**: Use configuration and dependency injection:

```csharp
public class UserService
{
    private readonly string _connectionString;
    
    public UserService(IConfiguration configuration)
    {
        _connectionString = configuration.GetConnectionString("UsersDb");
    }
}
```

## High Priority Issues

### 3. No Error Handling

**Problem**: Exceptions will crash the application.
**Fix**: Wrap in try-catch and log errors:

```csharp
public User GetUser(string userId)
{
    try
    {
        // ... existing code with fixes ...
    }
    catch (SqlException ex)
    {
        _logger.LogError(ex, "Database error while fetching user {UserId}", userId);
        throw new DataAccessException("Failed to retrieve user", ex);
    }
}
```

### 4. Missing Input Validation

**Problem**: No validation of `userId` parameter.
**Fix**:

```csharp
if (string.IsNullOrWhiteSpace(userId))
    throw new ArgumentException("User ID cannot be null or empty", nameof(userId));
```

## Medium Priority Issues

### 5. Not Using Async/Await

**Problem**: Blocking I/O in a web API reduces scalability.
**Fix**: Use async methods:

```csharp
public async Task<User> GetUserAsync(string userId)
{
    // ... use SqlCommand.ExecuteReaderAsync()
}
```

### 6. Manual Object Mapping

**Problem**: Brittle, error-prone mapping from DataReader.
**Suggestion**: Use Dapper or Entity Framework Core for safer mapping.

## Positive Observations

- Proper use of `using` statement for resource disposal
- Clear class and method names

## Overall Score: 3/10

Critical security vulnerabilities and lack of error handling make this unsuitable for production. After applying fixes, would rate 8/10.

```

## C# Implementation

```csharp
using System;
using System.Threading.Tasks;

namespace PromptEngineering.Agents
{
    public class CodeReviewAgent
    {
        private readonly AIModelClient _aiClient;
        private readonly ILogger<CodeReviewAgent> _logger;
        
        public CodeReviewAgent(AIModelClient aiClient, ILogger<CodeReviewAgent> logger)
        {
            _aiClient = aiClient;
            _logger = logger;
        }
        
        public async Task<CodeReviewResult> ReviewCodeAsync(
            string code,
            string projectType = "ASP.NET Core Web API",
            string framework = ".NET 6",
            string database = "SQL Server")
        {
            var prompt = BuildReviewPrompt(code, projectType, framework, database);
            
            _logger.LogInformation("Starting code review for {ProjectType}", projectType);
            
            var response = await _aiClient.CallAsync(new ModelRequest
            {
                Provider = ModelProvider.Anthropic,
                Model = "claude-3-opus-20240229",
                SystemPrompt = "You are an expert C# code reviewer.",
                Prompt = prompt,
                Temperature = 0.3,
                MaxTokens = 3000
            });
            
            return ParseReviewResult(response.Content);
        }
        
        private string BuildReviewPrompt(string code, string projectType, string framework, string database)
        {
            return $@"
You are an expert C# code reviewer with deep knowledge of .NET best practices, security, and performance.

**Code to Review**:
```csharp
{code}
```

**Context**:

- Project Type: {projectType}
- Framework: {framework}
- Database: {database}

[... rest of template ...]
";
        }

        private CodeReviewResult ParseReviewResult(string content)
        {
            // Parse the markdown output into structured data
            // In production, use a proper markdown parser or structured output
            return new CodeReviewResult
            {
                RawContent = content,
                OverallScore = ExtractScore(content),
                CriticalIssues = ExtractSection(content, "Critical Issues"),
                HighPriorityIssues = ExtractSection(content, "High Priority Issues")
            };
        }
        
        private int ExtractScore(string content)
        {
            // Simple regex to extract score from "Overall Score: X/10"
            var match = System.Text.RegularExpressions.Regex.Match(
                content, @"Overall Score:\s*(\d+)/10");
            return match.Success ? int.Parse(match.Groups[1].Value) : 0;
        }
        
        private string ExtractSection(string content, string sectionTitle)
        {
            // Extract content between section headers
            var pattern = $@"## {sectionTitle}\s*(.*?)(?=##|$)";
            var match = System.Text.RegularExpressions.Regex.Match(
                content, pattern, System.Text.RegularExpressions.RegexOptions.Singleline);
            return match.Success ? match.Groups[1].Value.Trim() : string.Empty;
        }
    }
    
    public class CodeReviewResult
    {
        public string RawContent { get; set; }
        public int OverallScore { get; set; }
        public string CriticalIssues { get; set; }
        public string HighPriorityIssues { get; set; }
    }
}

```

## Best Practices

1. **Temperature**: Use low temperature (0.2-0.4) for consistency in code reviews.
2. **Context**: Always provide project type, framework version, and database context.
3. **Iteration**: For large files, review in chunks (classes or methods).
4. **Human Review**: Use as first-pass; always have human review for production code.
5. **Custom Rules**: Extend the prompt with project-specific rules (e.g., "Always use ILogger, never Console.WriteLine").

## Related Patterns
- [Multi-Agent Workflow](../multi-agent/multi-agent-workflow.md)
- [Reflexion Pattern](../../reflexion/basic-reflexion/basic-reflexion.md)
