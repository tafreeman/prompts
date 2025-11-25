---
title: "Semantic Kernel Integration Patterns"
category: "frameworks"
subcategory: "microsoft"
technique_type: "semantic-kernel"
framework_compatibility:
  dotnet: ">=6.0"
  semantic-kernel: ">=1.0.0"
difficulty: "intermediate"
use_cases:
  - enterprise-orchestration
  - plugin-architecture
  - planner-usage
  - memory-integration
performance_metrics:
  productivity_improvement: "40-60%"
  integration_speed: "high"
  cost_multiplier: "1.0x"
testing:
  framework: "xUnit"
  coverage: "85%"
  validation_status: "passed"
governance:
  data_classification: "internal"
  risk_level: "low"
  compliance_standards: ["ISO27001"]
version: "1.0.0"
author: "AI Research Team"
last_updated: "2025-11-23"
tags:
  - semantic-kernel
  - csharp
  - dotnet
  - plugins
  - planners
---

# Semantic Kernel Integration Patterns

## Purpose

Leverage Microsoft Semantic Kernel (SK) to build enterprise-grade AI applications in .NET. SK provides a robust abstraction for orchestrating AI services, managing memory, and executing plugins.

## Overview

Semantic Kernel is the recommended SDK for .NET developers building AI apps. It unifies:

1. **AI Services**: OpenAI, Azure OpenAI, Hugging Face.
2. **Plugins**: Native code (C#) and semantic functions (Prompts).
3. **Planners**: Auto-orchestration of steps to achieve a goal.
4. **Memory**: Vector database integration for RAG.

## Prompt

In SK, prompts are often stored as `skprompt.txt` alongside `config.json`.

**skprompt.txt**:

```text
Summarize the following conversation into a concise project status update.

Context:
{{$input}}

Requirements:
- Identify key risks
- List completed milestones
- Estimate remaining timeline

Status Update:
```

**config.json**:

```json
{
  "schema": 1,
  "type": "completion",
  "description": "Generates a project status update from conversation logs.",
  "completion": {
    "max_tokens": 500,
    "temperature": 0.5,
    "top_p": 0.0,
    "presence_penalty": 0.0,
    "frequency_penalty": 0.0
  },
  "input": {
    "parameters": [
      {
        "name": "input",
        "description": "The conversation log to summarize",
        "defaultValue": ""
      }
    ]
  }
}
```

## Example

### 1. Kernel Setup

```csharp
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;

var builder = Kernel.CreateBuilder();

// Add Azure OpenAI Chat Completion
builder.AddAzureOpenAIChatCompletion(
    deploymentName: "gpt-4",
    endpoint: "https://your-resource.openai.azure.com/",
    apiKey: "your-api-key"
);

// Build the kernel
var kernel = builder.Build();
```

### 2. Defining a Native Plugin

```csharp
using System.ComponentModel;
using Microsoft.SemanticKernel;

public class SqlDataPlugin
{
    private readonly string _connectionString;

    public SqlDataPlugin(IConfiguration config)
    {
        _connectionString = config.GetConnectionString("DefaultConnection");
    }

    [KernelFunction, Description("Retrieves the latest order status for a customer")]
    public string GetOrderStatus(
        [Description("The customer ID")] string customerId)
    {
        // Implementation using Dapper or ADO.NET
        return $"Order status for {customerId}: Shipped";
    }
}

// Import into Kernel
kernel.ImportPluginFromType<SqlDataPlugin>("SqlData");
```

### 3. Defining a Semantic Plugin (Inline)

```csharp
var summarizeFunction = kernel.CreateFunctionFromPrompt(
    @"Summarize this text in 2 sentences: {{$input}}",
    functionName: "Summarize",
    description: "Summarizes text concisely"
);
```

## Usage

Planners are one of the most powerful features of Semantic Kernel. They allow the kernel to automatically select and chain plugins together to achieve a high-level goal.

### Handlebars Planner Usage

The `HandlebarsPlanner` creates a plan using Handlebars syntax, which is then executed by the kernel.

```csharp
using Microsoft.SemanticKernel.Planning.Handlebars;

// 1. Create the planner with options
var options = new HandlebarsPlannerOptions() 
{ 
    AllowLoops = true // Allow iterative steps
};
var planner = new HandlebarsPlanner(options);

// 2. Define the goal
var goal = "Check the order status for customer 123. If shipped, summarize the order details and draft an email to them.";

// 3. Create the plan
// The planner analyzes available plugins (e.g., SqlDataPlugin, EmailPlugin) to construct the steps
var plan = await planner.CreatePlanAsync(kernel, goal);

// 4. Execute the plan
Console.WriteLine($"Plan:\n{plan}");
var result = await plan.InvokeAsync(kernel);

Console.WriteLine($"Result: {result}");
```

### Memory and RAG Usage

Semantic Kernel simplifies RAG (Retrieval-Augmented Generation) through `ISemanticTextMemory`.

```csharp
using Microsoft.SemanticKernel.Connectors.Qdrant;
using Microsoft.SemanticKernel.Memory;

// 1. Configure Memory Store (e.g., Qdrant, Volatile, AzureSearch)
var memoryStore = new QdrantMemoryStore("http://localhost:6333", 1536);

// 2. Build Memory Client
var memoryBuilder = new MemoryBuilder();
memoryBuilder.WithOpenAITextEmbeddingGeneration("text-embedding-ada-002", apiKey);
memoryBuilder.WithMemoryStore(memoryStore);
var memory = memoryBuilder.Build();

// 3. Save Information
await memory.SaveInformationAsync(
    collection: "company_policies",
    text: "All employees are entitled to 4 weeks of vacation.",
    id: "vacation_policy"
);

// 4. Search Memory
var results = memory.SearchAsync(
    collection: "company_policies",
    query: "How much time off do I get?",
    limit: 1
);

await foreach (var result in results)
{
    Console.WriteLine($"Answer found: {result.Metadata.Text}");
}
```

## Best Practices

1. **Dependency Injection**: Always use `Kernel.CreateBuilder()` with `IServiceCollection` in ASP.NET Core apps to ensure proper lifecycle management of HTTP clients and services.
2. **Plugin Granularity**: Keep plugins focused on single responsibilities (SRP). Avoid creating "God Plugins" with too many unrelated functions.
3. **Description Quality**: The Planner relies *heavily* on the `[Description]` attributes of your C# methods and the `description` fields in your semantic functions. Be verbose and precise.
    - ❌ `[Description("Gets data")]`
    - ✅ `[Description("Retrieves the latest order status and shipping details for a given customer ID")]`
4. **Memory Management**: Use `ISemanticTextMemory` for RAG patterns instead of stuffing context manually into the prompt. This scales better and reduces token costs.
5. **Error Handling**: Wrap kernel execution in try-catch blocks. AI services can be transiently unavailable, and planners might fail to generate valid plans for ambiguous goals. Implement retry logic (e.g., using Polly) for robustness.

## Related Patterns

- [OpenAI Function Calling](../../openai/function-calling/openai-function-calling.md)
- [Agentic Workflows](../../../techniques/agentic/multi-agent/multi-agent-workflow.md)
