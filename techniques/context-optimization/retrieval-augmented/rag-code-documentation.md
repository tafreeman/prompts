---
title: "Retrieval-Augmented Code Documentation"
category: "techniques"
subcategory: "context-optimization"
technique_type: "retrieval-augmented"
framework_compatibility:
  openai: ">=1.0.0"
  anthropic: ">=0.8.0"
difficulty: "advanced"
use_cases:
  - code-documentation
  - api-documentation
  - knowledge-retrieval
  - codebase-qa
performance_metrics:
  accuracy_improvement: "35-50%"
  latency_impact: "medium"
  cost_multiplier: "1.3-1.8x"
version: "1.0.0"
author: "AI Research Team"
last_updated: "2025-11-23"
tags:
  - rag
  - retrieval
  - documentation
  - csharp
  - vector-search
---

# Retrieval-Augmented Code Documentation

## Purpose

Combines vector search with LLM generation to create accurate, context-aware documentation by retrieving relevant code snippets, existing docs, and related patterns before generating new documentation.

## Overview

Traditional documentation generation lacks context. RAG solves this by:

1. **Indexing** your codebase (classes, methods, XML comments) into a vector database
2. **Retrieving** most relevant code when documenting a new class/method
3. **Augmenting** the prompt with retrieved context
4. **Generating** documentation consistent with existing patterns

Perfect for maintaining consistent documentation across large .NET codebases.

## Architecture

```
User Input: "Document UserService.GetUserAsync"
        ↓
Vector Search: Find similar methods + existing docs
        ↓
Context Assembly: Code + XML comments + patterns
        ↓
LLM Generation: Create documentation
        ↓
Output: XML comments + README section
```

## Prompt Template

```markdown
You are a technical writer creating C# XML documentation comments.

**Task**: Generate comprehensive XML documentation for the following method.

**Method to Document**:
```csharp
{{target_method}}
```

**Retrieved Context** (similar methods and their documentation):

### Example 1: Similar Method

```csharp
{{similar_method_1}}
```

### Example 2: Similar Pattern

```csharp
{{similar_method_2}}
```

**Project Documentation Standards**:
{{doc_standards}}

**Generate**:

1. XML documentation comments (`<summary>`, `<param>`, `<returns>`, `<exception>`)
2. Follow the style from retrieved examples
3. Include code examples if appropriate
4. Note any potential pitfalls

**Format**:

```csharp
/// <summary>
/// [Your summary]
/// </summary>
/// <param name="[param]">[Description]</param>
/// <returns>[Description]</returns>
/// <exception cref="[ExceptionType]">[When thrown]</exception>
/// <example>
/// [Code example]
/// </example>
```

```

## C# Implementation with Vector Search

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace PromptEngineering.RAG
{
    /// <summary>
    /// Retrieval-Augmented Generation for code documentation.
    /// </summary>
    public class RAGDocumentationGenerator
    {
        private readonly IVectorStore _vectorStore;
        private readonly AIModelClient _aiClient;
        private readonly ILogger<RAGDocumentationGenerator> _logger;
        
        public RAGDocumentationGenerator(
            IVectorStore vectorStore,
            AIModelClient aiClient,
            ILogger<RAGDocumentationGenerator> logger)
        {
            _vectorStore = vectorStore ?? throw new ArgumentNullException(nameof(vectorStore));
            _aiClient = aiClient ?? throw new ArgumentNullException(nameof(aiClient));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }
        
        /// <summary>
        /// Generates documentation for a method using RAG.
        /// </summary>
        /// <param name="methodCode">The source code of the method to document.</param>
        /// <param name="topK">Number of similar examples to retrieve.</param>
        /// <returns>Generated XML documentation comments.</returns>
        public async Task<string> GenerateDocumentationAsync(string methodCode, int topK = 3)
        {
            _logger.LogInformation("Generating documentation with RAG (retrieving top {TopK} examples)", topK);
            
            // Step 1: Retrieve similar documented methods
            var similarMethods = await _vectorStore.FindSimilarAsync(methodCode, topK);
            
            _logger.LogDebug("Retrieved {Count} similar methods", similarMethods.Count);
            
            // Step 2: Build context-augmented prompt
            var prompt = BuildRAGPrompt(methodCode, similarMethods);
            
            // Step 3: Generate documentation
            var response = await _aiClient.CallAsync(new ModelRequest
            {
                Provider = ModelProvider.Anthropic,
                Model = "claude-3-opus-20240229",
                SystemPrompt = "You are an expert technical writer for C# documentation.",
                Prompt = prompt,
                Temperature = 0.3,
                MaxTokens = 1500
            });
            
            return response.Content;
        }
        
        private string BuildRAGPrompt(string targetMethod, List<CodeSnippet> similarMethods)
        {
            var examples = string.Join("\n\n", similarMethods.Select((snippet, i) => 
                $@"### Example {i + 1}: {snippet.MethodName}
```csharp
{snippet.Code}
```

"));

            return $@"
You are a technical writer creating C# XML documentation comments.

**Task**: Generate comprehensive XML documentation for the following method.

**Method to Document**:

```csharp
{targetMethod}
```

**Retrieved Context** (similar methods and their documentation from this codebase):

{examples}

**Generate**:

1. XML documentation comments following the style of the examples
2. Include <summary>, <param>, <returns>, <exception> tags
3. Be specific about behavior, not just restating the method name
4. Include <example> if the method has complex usage

**Output Format**:

```csharp
/// <summary>
/// [Detailed summary]
/// </summary>
/// [Other tags]
```

";
        }
    }

    /// <summary>
    /// Interface for vector storage and similarity search.
    /// </summary>
    public interface IVectorStore
    {
        /// <summary>
        /// Finds code snippets similar to the query.
        /// </summary>
        Task<List<CodeSnippet>> FindSimilarAsync(string query, int topK);
        
        /// <summary>
        /// Indexes a code snippet for later retrieval.
        /// </summary>
        Task IndexAsync(CodeSnippet snippet);
    }
    
    public class CodeSnippet
    {
        public string MethodName { get; set; }
        public string Code { get; set; }
        public string Documentation { get; set; }
        public List<string> Tags { get; set; } = new();
    }
}

```

## Vector Store Implementation (Example with Qdrant)

```csharp
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace PromptEngineering.RAG
{
    /// <summary>
    /// Qdrant vector store implementation for code similarity search.
    /// </summary>
    public class QdrantVectorStore : IVectorStore
    {
        private readonly HttpClient _httpClient;
        private readonly string _collectionName;
        private readonly AIModelClient _embeddingClient;
        
        public QdrantVectorStore(
            HttpClient httpClient,
            string collectionName,
            AIModelClient embeddingClient)
        {
            _httpClient = httpClient;
            _collectionName = collectionName;
            _embeddingClient = embeddingClient;
        }
        
        public async Task<List<CodeSnippet>> FindSimilarAsync(string query, int topK)
        {
            // 1. Generate embedding for query
            var queryEmbedding = await GenerateEmbeddingAsync(query);
            
            // 2. Search Qdrant
            var searchRequest = new
            {
                vector = queryEmbedding,
                limit = topK,
                with_payload = true
            };
            
            var response = await _httpClient.PostAsync(
                $"collections/{_collectionName}/points/search",
                new StringContent(
                    JsonSerializer.Serialize(searchRequest),
                    Encoding.UTF8,
                    "application/json"));
            
            response.EnsureSuccessStatusCode();
            
            var result = await response.Content.ReadFromJsonAsync<QdrantSearchResponse>();
            
            return result.Result.Select(r => new CodeSnippet
            {
                MethodName = r.Payload["methodName"].ToString(),
                Code = r.Payload["code"].ToString(),
                Documentation = r.Payload["documentation"].ToString()
            }).ToList();
        }
        
        public async Task IndexAsync(CodeSnippet snippet)
        {
            // 1. Generate embedding for code
            var embedding = await GenerateEmbeddingAsync(snippet.Code);
            
            // 2. Store in Qdrant
            var point = new
            {
                id = Guid.NewGuid(),
                vector = embedding,
                payload = new
                {
                    methodName = snippet.MethodName,
                    code = snippet.Code,
                    documentation = snippet.Documentation
                }
            };
            
            var response = await _httpClient.PutAsync(
                $"collections/{_collectionName}/points",
                new StringContent(
                    JsonSerializer.Serialize(new { points = new[] { point } }),
                    Encoding.UTF8,
                    "application/json"));
            
            response.EnsureSuccessStatusCode();
        }
        
        private async Task<List<float>> GenerateEmbeddingAsync(string text)
        {
            // Use OpenAI embeddings or similar
            var response = await _embeddingClient.CallAsync(new ModelRequest
            {
                Provider = ModelProvider.OpenAI,
                Model = "text-embedding-3-small",
                Prompt = text
            });
            
            // Parse embedding from response (simplified)
            return ParseEmbedding(response.Content);
        }
        
        private List<float> ParseEmbedding(string json)
        {
            // Simplified - actual implementation would parse JSON properly
            return new List<float>();
        }
    }
    
    internal class QdrantSearchResponse
    {
        public List<SearchResult> Result { get; set; }
    }
    
    internal class SearchResult
    {
        public Dictionary<string, object> Payload { get; set; }
        public double Score { get; set; }
    }
}
```

## Usage Example

```csharp
// 1. Index existing documented methods
var vectorStore = new QdrantVectorStore(httpClient, "csharp-docs", aiClient);

await vectorStore.IndexAsync(new CodeSnippet
{
    MethodName = "GetUserAsync",
    Code = @"
public async Task<User?> GetUserAsync(int userId)
{
    // ... implementation
}",
    Documentation = @"
/// <summary>
/// Retrieves a user by ID from the database asynchronously.
/// </summary>
/// <param name=""userId"">The unique identifier of the user.</param>
/// <returns>The user object if found; otherwise, null.</returns>
/// <exception cref=""DataAccessException"">Thrown when database access fails.</exception>"
});

// 2. Generate docs for new method
var ragGenerator = new RAGDocumentationGenerator(vectorStore, aiClient, logger);

var newMethod = @"
public async Task<Order> CreateOrderAsync(int userId, List<OrderItem> items)
{
    // ... implementation
}";

var generatedDocs = await ragGenerator.GenerateDocumentationAsync(newMethod);

Console.WriteLine(generatedDocs);
```

## Output Example

```csharp
/// <summary>
/// Creates a new order for the specified user with the provided items asynchronously.
/// </summary>
/// <param name="userId">The unique identifier of the user placing the order.</param>
/// <param name="items">The list of items to include in the order. Cannot be null or empty.</param>
/// <returns>The newly created order object with assigned order ID and timestamp.</returns>
/// <exception cref="ArgumentNullException">Thrown when <paramref name="items"/> is null.</exception>
/// <exception cref="ArgumentException">Thrown when <paramref name="items"/> is empty.</exception>
/// <exception cref="DataAccessException">Thrown when database transaction fails.</exception>
/// <exception cref="InvalidOperationException">Thrown when user does not exist or is inactive.</exception>
/// <example>
/// <code>
/// var items = new List&lt;OrderItem&gt; 
/// {
///     new OrderItem { ProductId = 123, Quantity = 2 }
/// };
/// var order = await orderService.CreateOrderAsync(userId: 456, items);
/// </code>
/// </example>
```

## Best Practices

1. **Index Strategy**: Index all well-documented methods first to build quality retrieval base.
2. **Chunk Size**: For large classes, index method-by-method, not entire classes.
3. **Metadata**: Include tags (async, database, API) to improve retrieval relevance.
4. **Embedding Model**: Use `text-embedding-3-small` for cost efficiency.
5. **Top-K**: Retrieve 3-5 examples; more adds noise.
6. **Cache**: Cache embeddings for frequently accessed code.

## Related Patterns

- [Many-Shot Learning](../many-shot-learning/many-shot-learning.md)
- [Context Optimization](../context_optimizer.py)
