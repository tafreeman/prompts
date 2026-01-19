---
title: "Microsoft AI Platform Prompts"
shortTitle: "Microsoft"
intro: "Prompts and patterns for Microsoft AI platforms including Semantic Kernel, GitHub Copilot, and .NET."
type: "reference"
difficulty: "intermediate"
audience:
  - "senior-engineer"
  - "junior-engineer"
platforms:
  - "github-copilot"
  - "semantic-kernel"
  - "dotnet"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
dataClassification: "public"
reviewStatus: "approved"
---

# Microsoft AI Platform Prompts

Comprehensive collection of prompts, patterns, and integration examples for Microsoft's AI ecosystem, including Semantic Kernel, GitHub Copilot, M365 Copilot, and .NET AI development.

## 📋 Contents

```text
microsoft/
├── README.md                      # This file
├── copilot-patterns/              # GitHub Copilot patterns
│   └── github-copilot-instructions.md
├── dotnet/                        # .NET AI development
│   └── (AI integration patterns)
└── semantic-kernel/               # Semantic Kernel framework
    └── (SK plugins and patterns)
```

## 🎯 What's Inside

Microsoft's AI platform includes:

- **Semantic Kernel**: Lightweight SDK for AI orchestration
- **GitHub Copilot**: AI pair programmer with custom agents
- **M365 Copilot**: AI assistant for Microsoft 365
- **.NET AI**: AI capabilities in .NET applications
- **Azure OpenAI**: Enterprise-grade OpenAI services

## ✨ Platform Overview

### 1. Semantic Kernel

Enterprise AI orchestration framework for .NET, Python, and Java.

**Key Features:**
- Plugin-based architecture
- Memory and embeddings
- Planning and orchestration
- Multi-provider support (OpenAI, Azure OpenAI, Hugging Face)
- Native .NET integration

**Example:**

```csharp
using Microsoft.SemanticKernel;

var kernel = Kernel.CreateBuilder()
    .AddAzureOpenAIChatCompletion(
        deploymentName: "gpt-4",
        endpoint: "https://your-endpoint.openai.azure.com/",
        apiKey: "your-api-key"
    )
    .Build();

var result = await kernel.InvokePromptAsync(
    "Translate '{{$input}}' to {{$language}}",
    new() {
        { "input", "Hello, world!" },
        { "language", "Spanish" }
    }
);
```

### 2. GitHub Copilot

AI-powered code completion and chat.

**Key Features:**
- Context-aware code suggestions
- Natural language to code
- Custom agents (.agent.md files)
- Workspace context integration
- Multi-file editing

**Custom Agent Example:**

```markdown
---
name: code-reviewer
description: Expert code reviewer
---

You are an expert code reviewer. Review code for:
- Best practices
- Security vulnerabilities
- Performance issues
- Code smells

Provide actionable feedback with specific suggestions.
```

### 3. M365 Copilot

AI assistant integrated into Microsoft 365 apps.

**Available In:**
- Word (document creation)
- Excel (data analysis)
- PowerPoint (presentation design)
- Teams (meeting summaries)
- Outlook (email management)

**See:** [M365 Copilot Prompts](../../m365/README.md)

### 4. .NET AI Development

Build AI-powered applications with .NET.

**Key Libraries:**
- Microsoft.SemanticKernel
- Azure.AI.OpenAI
- Microsoft.ML
- Azure Cognitive Services SDKs

## 🚀 Quick Start

### Semantic Kernel - C#

```bash
# Install Semantic Kernel
dotnet add package Microsoft.SemanticKernel
```

```csharp
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;

// Create kernel
var builder = Kernel.CreateBuilder();
builder.AddAzureOpenAIChatCompletion(
    deploymentName: "gpt-4",
    endpoint: "https://your-endpoint.openai.azure.com/",
    apiKey: "your-api-key"
);
var kernel = builder.Build();

// Simple prompt
var response = await kernel.InvokePromptAsync(
    "What is the capital of France?"
);
Console.WriteLine(response);

// With variables
var translate = kernel.CreateFunctionFromPrompt(
    "Translate '{{$text}}' to {{$language}}"
);
var result = await kernel.InvokeAsync(translate, new() {
    { "text", "Hello" },
    { "language", "Japanese" }
});
```

### Semantic Kernel - Python

```bash
# Install Semantic Kernel
pip install semantic-kernel
```

```python
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# Create kernel
kernel = sk.Kernel()

# Add chat completion service
kernel.add_service(
    AzureChatCompletion(
        deployment_name="gpt-4",
        endpoint="https://your-endpoint.openai.azure.com/",
        api_key="your-api-key"
    )
)

# Execute prompt
result = await kernel.invoke_prompt(
    "What is the capital of France?"
)
print(result)
```

### GitHub Copilot Custom Agent

1. Create `.github/agents/reviewer.agent.md`:

```markdown
---
name: reviewer
description: Code review expert
---

You are an expert code reviewer specializing in:
- Security best practices
- Performance optimization
- Code maintainability
- Testing coverage

When reviewing code:
1. Identify potential issues
2. Explain the impact
3. Suggest specific improvements
4. Provide code examples
```

2. Use in Copilot Chat:

```
@reviewer Review this function for security issues:

def process_user_input(data):
    query = f"SELECT * FROM users WHERE id = {data}"
    return execute_query(query)
```

## 📚 Semantic Kernel Patterns

### Plugin Architecture

```csharp
using Microsoft.SemanticKernel;
using System.ComponentModel;

public class MathPlugin
{
    [KernelFunction]
    [Description("Add two numbers")]
    public int Add(
        [Description("First number")] int a,
        [Description("Second number")] int b
    )
    {
        return a + b;
    }
}

// Register plugin
kernel.ImportPluginFromType<MathPlugin>();

// Use plugin
var result = await kernel.InvokeAsync("MathPlugin", "Add", new() {
    { "a", 5 },
    { "b", 3 }
});
```

### Memory and Embeddings

```csharp
using Microsoft.SemanticKernel.Memory;

// Add memory store
var memoryBuilder = new MemoryBuilder();
memoryBuilder.WithAzureOpenAITextEmbeddingGeneration(
    deploymentName: "text-embedding-ada-002",
    endpoint: "https://your-endpoint.openai.azure.com/",
    apiKey: "your-api-key"
);
var memory = memoryBuilder.Build();

// Save information
await memory.SaveInformationAsync(
    collection: "facts",
    text: "The capital of France is Paris",
    id: "fact1"
);

// Search memory
var results = await memory.SearchAsync(
    collection: "facts",
    query: "What is the capital of France?",
    limit: 1
);
```

### Planning and Orchestration

```csharp
using Microsoft.SemanticKernel.Planning;

// Create planner
var planner = new HandlebarsPlanner();

// Create plan from goal
var plan = await planner.CreatePlanAsync(
    kernel,
    "Send an email to John summarizing the Q4 sales report"
);

// Execute plan
var result = await plan.InvokeAsync(kernel);
```

### Streaming Responses

```csharp
var chatService = kernel.GetRequiredService<IChatCompletionService>();

await foreach (var message in chatService.GetStreamingChatMessageContentsAsync(
    chatHistory,
    kernel: kernel
))
{
    Console.Write(message.Content);
}
```

## 🎓 GitHub Copilot Best Practices

### 1. Write Clear Comments

✅ **Do:**
```python
# Create a function that validates email addresses using regex
# Should return True for valid emails, False otherwise
# Handle common edge cases like multiple @ symbols
```

❌ **Don't:**
```python
# email validator
```

### 2. Use Descriptive Function Names

✅ **Do:**
```python
def calculate_compound_interest_with_monthly_contributions(
    principal: float,
    annual_rate: float,
    years: int,
    monthly_contribution: float
) -> float:
```

❌ **Don't:**
```python
def calc(p, r, y, m):
```

### 3. Leverage Chat for Complex Tasks

```
Generate a FastAPI endpoint that:
1. Accepts user registration data
2. Validates email format
3. Hashes password with bcrypt
4. Stores in PostgreSQL
5. Returns JWT token
Include error handling and rate limiting
```

### 4. Create Custom Agents

Define specialized agents for your workflow:

- **@docs-agent**: Documentation generation
- **@test-agent**: Test creation
- **@security-agent**: Security reviews
- **@refactor-agent**: Code improvements

## 🔧 .NET AI Integration

### Azure OpenAI in .NET

```csharp
using Azure;
using Azure.AI.OpenAI;

var client = new OpenAIClient(
    new Uri("https://your-endpoint.openai.azure.com/"),
    new AzureKeyCredential("your-api-key")
);

var chatOptions = new ChatCompletionsOptions()
{
    DeploymentName = "gpt-4",
    Messages =
    {
        new ChatRequestSystemMessage("You are a helpful assistant."),
        new ChatRequestUserMessage("Explain quantum computing")
    }
};

var response = await client.GetChatCompletionsAsync(chatOptions);
Console.WriteLine(response.Value.Choices[0].Message.Content);
```

### Function Calling

```csharp
var functions = new List<ChatCompletionsFunctionToolDefinition>
{
    new ChatCompletionsFunctionToolDefinition
    {
        Name = "get_weather",
        Description = "Get current weather",
        Parameters = BinaryData.FromObjectAsJson(new
        {
            type = "object",
            properties = new
            {
                location = new { type = "string" }
            },
            required = new[] { "location" }
        })
    }
};

var options = new ChatCompletionsOptions
{
    DeploymentName = "gpt-4",
    Tools = { functions[0] }
};
```

## 📊 Platform Comparison

| Platform | Language | Use Case | Deployment |
|----------|----------|----------|------------|
| **Semantic Kernel** | C#, Python, Java | AI orchestration | Cloud + On-prem |
| **GitHub Copilot** | Any | Code generation | Cloud (GitHub) |
| **M365 Copilot** | N/A | Productivity | Cloud (Microsoft 365) |
| **.NET AI** | C#, F# | Custom apps | Any |
| **Azure OpenAI** | Any (REST) | Enterprise AI | Azure Cloud |

## 🛠️ Tools & Utilities

### Semantic Kernel Tools

```bash
# SK CLI (if available)
sk plugin create MyPlugin
sk function create MyFunction
sk test "my test prompt"
```

### GitHub Copilot Commands

In Copilot Chat:
- `/explain` - Explain code
- `/fix` - Fix bugs
- `/test` - Generate tests
- `/doc` - Create documentation
- `@workspace` - Use workspace context
- `@terminal` - Use terminal context

## 📖 Additional Resources

### Official Documentation
- [Semantic Kernel Docs](https://learn.microsoft.com/en-us/semantic-kernel/)
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [M365 Copilot](https://learn.microsoft.com/en-us/microsoft-365-copilot/)

### GitHub Repositories
- [Semantic Kernel](https://github.com/microsoft/semantic-kernel)
- [Semantic Kernel Samples](https://github.com/microsoft/semantic-kernel/tree/main/samples)

### Learning Resources
- [Semantic Kernel Learn Path](https://learn.microsoft.com/en-us/training/paths/develop-ai-agents-azure-open-ai-semantic-kernel-sdk/)
- [GitHub Copilot Quickstart](https://docs.github.com/en/copilot/quickstart)

## 🤝 Contributing

When adding Microsoft platform patterns:

1. Test with latest SDK versions
2. Include both C# and Python examples (where applicable)
3. Document Azure setup requirements
4. Provide deployment instructions
5. Include error handling and best practices

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines.

## 🐛 Common Issues

### Issue: Semantic Kernel authentication fails

**Solution:** Verify Azure OpenAI endpoint and key:
```csharp
// Ensure correct format
endpoint: "https://YOUR-RESOURCE-NAME.openai.azure.com/"
// Not: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai"
```

### Issue: GitHub Copilot suggestions not appearing

**Solution:** 
1. Check Copilot subscription status
2. Verify file type is supported
3. Ensure clear context in comments
4. Restart IDE/editor

### Issue: Plugin not found

**Solution:**
```csharp
// Register plugin before use
kernel.ImportPluginFromType<MyPlugin>();

// Or use plugin directory
kernel.ImportPluginFromPromptDirectory("./plugins");
```

## 📝 Version History

- **1.0** (2025-11-30): Initial release with Semantic Kernel, Copilot, and .NET patterns

---

**Need Help?** Check [Microsoft Learn](https://learn.microsoft.com/) or [open an issue](https://github.com/tafreeman/prompts/issues).
