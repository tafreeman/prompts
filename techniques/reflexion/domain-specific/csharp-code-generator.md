---
title: "C# Code Generator with Reflexion"
category: "techniques"
subcategory: "reflexion"
technique_type: "domain-specific"
framework_compatibility:
  openai: ">=1.0.0"
  anthropic: ">=0.8.0"
difficulty: "advanced"
use_cases:
  - code-generation
  - refactoring
  - boilerplate-reduction
  - dotnet-development
performance_metrics:
  accuracy_improvement: "30-45%"
  latency_impact: "medium"
  cost_multiplier: "1.5-2.0x"
version: "1.0.0"
author: "AI Research Team"
last_updated: "2025-11-23"
tags:
  - reflexion
  - csharp
  - code-generation
  - domain-specific
---

# C# Code Generator with Reflexion

## Purpose

Domain-specific reflexion pattern for generating high-quality C# code with built-in self-correction. Ensures generated code follows .NET best practices, includes error handling, uses async/await properly, and adheres to SOLID principles.

## Overview

This pattern applies reflexion specifically to C# code generation by:

1. Generating initial code based on requirements
2. Self-reviewing against C# best practices checklist
3. Identifying issues (missing async, no error handling, etc.)
4. Regenerating improved code
5. Repeating until quality threshold is met

## Prompt Template

### Initial Generation Prompt

```markdown
You are an expert C# developer specializing in .NET 6+ and clean architecture.

**Requirements**:
{{requirements}}

**Constraints**:
- Target Framework: {{framework_version}}
- Use async/await for I/O operations
- Include XML documentation comments
- Follow C# naming conventions (PascalCase for public, camelCase for private)
- Use nullable reference types (string?)
- Include comprehensive error handling
- Add logging with ILogger<T>
- Use dependency injection where appropriate

**Generate**:
1. The complete C# class(es) meeting the requirements
2. Include all necessary using statements
3. Add unit test examples

**Output Format**:
```csharp
// [Namespace and using statements]
// [Class implementation]
// [Unit tests]
```

```

### Reflexion (Self-Critique) Prompt

```markdown
You just generated the following C# code:

```csharp
{{generated_code}}
```

**Critique This Code** against these criteria:

### 1. Async/Await Correctness

- [ ] All I/O operations are async
- [ ] Methods suffix correctly with `Async`
- [ ] No `Task.Wait()` or `.Result` usage
- [ ] Proper ConfigureAwait usage (if library)

### 2. Error Handling

- [ ] Try-catch blocks for all I/O
- [ ] Specific exception types caught
- [ ] Errors logged with context
- [ ] Appropriate exception messages

### 3. Dependency Injection

- [ ] Dependencies injected via constructor
- [ ] No `new` for services/repositories
- [ ] Interfaces used for dependencies

### 4. Null Safety

- [ ] Nullable reference types used
- [ ] Null checks where needed
- [ ] ArgumentNullException for null parameters

### 5. SOLID Principles

- [ ] Single Responsibility: Each class has one purpose
- [ ] Open/Closed: Extensible without modification
- [ ] Dependency Inversion: Depends on abstractions

### 6. Documentation & Naming

- [ ] XML comments on public members
- [ ] Clear, descriptive names
- [ ] No magic numbers or strings

**List All Issues Found** (be specific with line numbers if possible):

1. [Issue 1]
2. [Issue 2]
...

**Self-Assessment Score**: X/10

```

### Refinement Prompt

```markdown
Based on your critique:

**Issues Identified**:
{{issues_list}}

**Original Code**:
```csharp
{{original_code}}
```

**Generate Improved Code** that fixes all identified issues while maintaining the original functionality.

**Requirements Refresh**:
{{requirements}}

**Produce**:

1. Fixed code with all issues resolved
2. Explanation of major changes
3. Updated unit tests

```

## Usage Example

### Requirements
"Create a UserRepository for SQL Server that retrieves users by ID with caching. Include error handling and logging."

### Iteration 1: Initial Generation

```csharp
using System;
using System.Data.SqlClient;

public class UserRepository
{
    private string connectionString = "Server=...";
    
    public User GetUser(int userId)
    {
        using (var conn = new SqlConnection(connectionString))
        {
            conn.Open();
            var cmd = new SqlCommand($"SELECT * FROM Users WHERE Id = {userId}", conn);
            var reader = cmd.ExecuteReader();
            return new User { Id = (int)reader["Id"], Name = reader["Name"].ToString() };
        }
    }
}
```

### Reflexion Output

**Issues Found**:

1. ❌ SQL Injection vulnerability (string concatenation)
2. ❌ Not using async/await
3. ❌ Hardcoded connection string
4. ❌ No error handling
5. ❌ No null checks
6. ❌ No caching (requirement missed)
7. ❌ Missing XML documentation
8. ❌ No dependency injection

**Score**: 2/10

### Iteration 2: Improved Code

```csharp
using System;
using System.Data;
using System.Threading.Tasks;
using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Logging;

namespace MyApp.Repositories
{
    /// <summary>
    /// Repository for user data access with caching.
    /// </summary>
    public class UserRepository : IUserRepository
    {
        private readonly string _connectionString;
        private readonly IMemoryCache _cache;
        private readonly ILogger<UserRepository> _logger;
        private const int CacheDurationMinutes = 10;
        
        public UserRepository(
            string connectionString,
            IMemoryCache cache,
            ILogger<UserRepository> logger)
        {
            _connectionString = connectionString ?? throw new ArgumentNullException(nameof(connectionString));
            _cache = cache ?? throw new ArgumentNullException(nameof(cache));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }
        
        /// <summary>
        /// Retrieves a user by ID with caching.
        /// </summary>
        /// <param name="userId">The user identifier.</param>
        /// <returns>User object or null if not found.</returns>
        /// <exception cref="DataAccessException">Database error occurred.</exception>
        public async Task<User?> GetUserAsync(int userId)
        {
            string cacheKey = $"User_{userId}";
            
            // Check cache first
            if (_cache.TryGetValue(cacheKey, out User? cachedUser))
            {
                _logger.LogDebug("User {UserId} retrieved from cache", userId);
                return cachedUser;
            }
            
            try
            {
                await using var conn = new SqlConnection(_connectionString);
                await conn.OpenAsync();
                
                await using var cmd = new SqlCommand(
                    "SELECT Id, Name, Email FROM Users WHERE Id = @UserId", 
                    conn);
                cmd.Parameters.Add("@UserId", SqlDbType.Int).Value = userId;
                
                await using var reader = await cmd.ExecuteReaderAsync();
                
                if (await reader.ReadAsync())
                {
                    var user = new User
                    {
                        Id = reader.GetInt32(0),
                        Name = reader.GetString(1),
                        Email = reader.GetString(2)
                    };
                    
                    // Cache the result
                    _cache.Set(cacheKey, user, TimeSpan.FromMinutes(CacheDurationMinutes));
                    
                    _logger.LogInformation("User {UserId} retrieved from database", userId);
                    return user;
                }
                
                _logger.LogWarning("User {UserId} not found", userId);
                return null;
            }
            catch (SqlException ex)
            {
                _logger.LogError(ex, "Database error retrieving user {UserId}", userId);
                throw new DataAccessException($"Failed to retrieve user {userId}", ex);
            }
        }
    }
    
    public interface IUserRepository
    {
        Task<User?> GetUserAsync(int userId);
    }
    
    public class DataAccessException : Exception
    {
        public DataAccessException(string message, Exception innerException) 
            : base(message, innerException) { }
    }
}
```

### Final Reflexion

**Issues Fixed**: ✅ All 8 issues resolved

**Score**: 9/10 (Production-ready)

## C# Implementation

```csharp
public class CSharpReflexionGenerator
{
    private readonly AIModelClient _client;
    private readonly int _maxIterations;
    
    public CSharpReflexionGenerator(AIModelClient client, int maxIterations = 3)
    {
        _client = client;
        _maxIterations = maxIterations;
    }
    
    public async Task<GenerationResult> GenerateCodeAsync(
        string requirements,
        string frameworkVersion = ".NET 6")
    {
        string currentCode = null;
        var iterations = new List<IterationResult>();
        
        for (int i = 0; i < _maxIterations; i++)
        {
            // Step 1: Generate or Refine
            var generatePrompt = i == 0
                ? BuildInitialPrompt(requirements, frameworkVersion)
                : BuildRefinementPrompt(requirements, currentCode, iterations[i-1].Issues);
            
            currentCode = await CallModelAsync(generatePrompt);
            
            // Step 2: Reflexion (Self-Critique)
            var critiquePrompt = BuildCritiquePrompt(currentCode);
            var critique = await CallModelAsync(critiquePrompt);
            
            var iterationResult = ParseCritique(critique);
            iterationResult.GeneratedCode = currentCode;
            iterations.Add(iterationResult);
            
            // Stop if quality threshold met
            if (iterationResult.Score >= 8)
            {
                break;
            }
        }
        
        return new GenerationResult
        {
            FinalCode = currentCode,
            Iterations = iterations,
            TotalIterations = iterations.Count
        };
    }
    
    private async Task<string> CallModelAsync(string prompt)
    {
        var response = await _client.CallAsync(new ModelRequest
        {
            Provider = ModelProvider.Anthropic,
            Model = "claude-3-opus-20240229",
            Prompt = prompt,
            Temperature = 0.4
        });
        return response.Content;
    }
}
```

## Best Practices

1. **Start Simple**: Initial generation should be basic but functional.
2. **Specific Criteria**: Tailor reflexion checklists to your coding standards.
3. **Limit Iterations**: 2-3 iterations usually sufficient; diminishing returns after.
4. **Context Window**: For large classes, generate and reflex one method at a time.
5. **Human Review**: Always review final generation, especially for critical code.

## Related Patterns

- [Basic Reflexion](../basic-reflexion/basic-reflexion.md)
- [Multi-Step Reflexion](../multi-step-reflexion/multi-step-reflexion.md)
