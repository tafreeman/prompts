# Frameworks Reference

**Generated:** 2025-12-19  
**Files analyzed:** 13  
**Recommendation summary:** 10 KEEP, 2 CONSOLIDATE, 1 ARCHIVE

## Summary

The `frameworks/` directory provides a curated set of prompt patterns, code utilities, and integration templates for major AI frameworks: LangChain, Anthropic (Claude), OpenAI, and Microsoft Semantic Kernel/Copilot. It serves as a reference and toolkit for building, validating, and orchestrating advanced prompt workflows and agentic behaviors across these platforms. Each subfolder contains framework-specific best practices, reusable code, and prompt templates to accelerate AI solution development and ensure consistency.

---

### `anthropic/claude_patterns.py`

| Attribute   | Value |
|-------------|-------|
| **Location** | `frameworks/anthropic/claude_patterns.py` |
| **Type** | Library |
| **Lines** | ~127 |

#### Function
Implements Claude-specific prompt optimization patterns, including XML tag structuring, Constitutional AI principles, Chain of Thought (CoT) enforcement, and tool use formatting. Provides a class for optimizing prompts for Anthropic Claude models and helpers for tool definition formatting.

#### Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| api_key | str | None | Anthropic API key (env: ANTHROPIC_API_KEY) |
| prompt | str | required | Input prompt text |
| optimization_type | str | 'xml_structure' | Optimization strategy |

#### Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| ANTHROPIC_API_KEY | No | Used if api_key not provided |

#### Workflow Usage
- **Used by**: Anthropic prompt engineering scripts, documentation examples
- **Calls**: os, logging
- **Example**: `optimizer.optimize_for_claude(prompt, 'cot')`

#### Value Assessment
- **Unique Value**: Centralizes Claude prompt best practices and reusable logic
- **Overlap**: Some overlap with OpenAI utilities for prompt formatting
- **Recommendation**: KEEP

---

### `anthropic/tool-use/claude-tool-use.md`

| Attribute   | Value |
|-------------|-------|
| **Location** | `frameworks/anthropic/tool-use/claude-tool-use.md` |
| **Type** | How-To / Reference |
| **Frontmatter** | Complete |

#### Function
Demonstrates how to define and use tools (functions) with Anthropic Claude models, including JSON schema structure, system prompting, chain of thought, and tool result handling. Includes best practices and Python implementation.

#### Variables
| Variable | Required | Description |
|----------|----------|-------------|
| tool_definitions | Yes | List of available tools |
| user_input | Yes | User's request |

#### Use Cases
1. Data extraction
2. API integration
3. Complex workflows

#### Value Assessment
- **Recommendation**: KEEP

---

### `langchain/agent-patterns/langchain-agents.md`

| Attribute   | Value |
|-------------|-------|
| **Location** | `frameworks/langchain/agent-patterns/langchain-agents.md` |
| **Type** | How-To / Reference |
| **Frontmatter** | Complete |

#### Function
Describes patterns for building autonomous AI agents using LangChain, including ReAct, function-calling, and structured chat agents. Provides system prompt templates, code examples, and best practices for tool orchestration and agent design.

#### Variables
| Variable | Required | Description |
|----------|----------|-------------|
| tools | Yes | List of available tools |
| tool_names | Yes | Names of tools for agent selection |

#### Use Cases
1. Autonomous research agents
2. Tool orchestration
3. Data analysis

#### Value Assessment
- **Recommendation**: KEEP

---

### `langchain/lcel-patterns/langchain-reflexion-example.md`

| Attribute   | Value |
|-------------|-------|
| **Location** | `frameworks/langchain/lcel-patterns/langchain-reflexion-example.md` |
| **Type** | How-To |
| **Frontmatter** | Complete |

#### Function
Demonstrates Reflexion patterns using LangChain Expression Language (LCEL) for composable, iterative improvement workflows. Includes code for multi-iteration reflexion, structured output, and best practices.

#### Variables
| Variable | Required | Description |
|----------|----------|-------------|
| code | Yes | Code to analyze |
| initial_analysis | Yes | First-pass analysis |
| reflection | Yes | Self-evaluation |

#### Use Cases
1. Chain composition
2. Iterative improvement
3. Error correction

#### Value Assessment
- **Recommendation**: KEEP

---

### `microsoft/copilot-patterns/github-copilot-instructions.md`

| Attribute   | Value |
|-------------|-------|
| **Location** | `frameworks/microsoft/copilot-patterns/github-copilot-instructions.md` |
| **Type** | How-To |
| **Frontmatter** | Complete |

#### Function
Documents how to use `.github/copilot-instructions.md` to provide persistent project context and coding standards for GitHub Copilot. Includes templates, best practices, and project-specific patterns.

#### Variables
| Variable | Required | Description |
|----------|----------|-------------|
| project context | Yes | Project-specific info |

#### Use Cases
1. Code generation
2. Code review
3. Refactoring

#### Value Assessment
- **Recommendation**: KEEP

---

### `microsoft/dotnet/csharp-multimodel-client.md`

| Attribute   | Value |
|-------------|-------|
| **Location** | `frameworks/microsoft/dotnet/csharp-multimodel-client.md` |
| **Type** | How-To |
| **Frontmatter** | Complete |

#### Function
Provides C# utilities for prompt templating, multi-model AI integration, and enterprise patterns for .NET environments. Includes a unified client for OpenAI, Anthropic, and Azure OpenAI, with configuration and DI setup.

#### Variables
| Variable | Required | Description |
|----------|----------|-------------|
| Provider | Yes | Model provider (OpenAI, Anthropic, AzureOpenAI) |
| Model | Yes | Model name |
| Prompt | Yes | Prompt text |

#### Use Cases
1. Multi-model integration
2. Prompt templating
3. Enterprise AI orchestration

#### Value Assessment
- **Recommendation**: KEEP

---

### `microsoft/semantic-kernel/semantic-kernel-patterns.md`

| Attribute   | Value |
|-------------|-------|
| **Location** | `frameworks/microsoft/semantic-kernel/semantic-kernel-patterns.md` |
| **Type** | How-To |
| **Frontmatter** | Complete |

#### Function
Describes integration patterns for Microsoft Semantic Kernel, including plugin architecture, planners, memory integration, and best practices for .NET AI apps.

#### Variables
| Variable | Required | Description |
|----------|----------|-------------|
| input | Yes | Input for semantic functions |

#### Use Cases
1. Enterprise orchestration
2. Plugin-based AI
3. Planner usage

#### Value Assessment
- **Recommendation**: KEEP

---

### `microsoft/semantic-kernel/sk-csharp-examples.cs`

| Attribute   | Value |
|-------------|-------|
| **Location** | `frameworks/microsoft/semantic-kernel/sk-csharp-examples.cs` |
| **Type** | Script / Example |
| **Lines** | ~110 |

#### Function
Provides C# example code for setting up Semantic Kernel with dependency injection, plugins, planners, and native/semantic functions. Demonstrates practical usage for CRM and email plugins.

#### Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| customerName | string | required | CRM plugin example |
| content | string | required | Email plugin example |

#### Workflow Usage
- **Used by**: Developers learning SK integration
- **Calls**: Microsoft.SemanticKernel, plugins
- **Example**: `SemanticKernelBootstrap.RunAsync()`

#### Value Assessment
- **Unique Value**: Realistic, end-to-end SK usage
- **Overlap**: None significant
- **Recommendation**: KEEP

---

### `openai/openai_utilities.py`

| Attribute   | Value |
|-------------|-------|
| **Location** | `frameworks/openai/openai_utilities.py` |
| **Type** | Library |
| **Lines** | ~106 |

#### Function
Provides utilities for OpenAI prompt engineering, including function definition formatting, system message optimization, token estimation, and structured output validation.

#### Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| api_key | str | None | OpenAI API key (env: OPENAI_API_KEY) |
| name | str | required | Function name |
| description | str | required | Function description |
| parameters | dict | required | Function parameters |

#### Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| OPENAI_API_KEY | No | Used if api_key not provided |

#### Workflow Usage
- **Used by**: OpenAI prompt engineering scripts, documentation examples
- **Calls**: os, logging, json
- **Example**: `utils.format_function_def(...)`

#### Value Assessment
- **Unique Value**: Centralizes OpenAI prompt best practices
- **Overlap**: Some overlap with Claude utilities
- **Recommendation**: CONSOLIDATE (with Claude utilities for shared logic)

---

### `openai/assistants-api/openai-assistants.md`

| Attribute   | Value |
|-------------|-------|
| **Location** | `frameworks/openai/assistants-api/openai-assistants.md` |
| **Type** | How-To |
| **Frontmatter** | Complete |

#### Function
Documents patterns for building stateful, multi-turn AI assistants with OpenAI's Assistants API, including persistent memory, file handling, and tool integration. Provides code examples and best practices.

#### Variables
| Variable | Required | Description |
|----------|----------|-------------|
| assistant | Yes | Assistant configuration |
| thread | Yes | Conversation session |
| message | Yes | User/assistant message |

#### Use Cases
1. Persistent conversations
2. Code interpreter
3. File retrieval

#### Value Assessment
- **Recommendation**: KEEP

---

### `openai/function-calling/openai-function-calling.md`

| Attribute   | Value |
|-------------|-------|
| **Location** | `frameworks/openai/function-calling/openai-function-calling.md` |
| **Type** | How-To |
| **Frontmatter** | Complete |

#### Function
Describes OpenAI's function calling (tool use) capability for structured data extraction and API integration. Includes JSON schema examples, prompt templates, and Python implementation.

#### Variables
| Variable | Required | Description |
|----------|----------|-------------|
| extract_customer_info | Yes | Function for extracting customer info |
| ticket_content | Yes | Support ticket text |

#### Use Cases
1. Structured data extraction
2. API integration
3. Decision making

#### Value Assessment
- **Recommendation**: KEEP

---

## Workflow Map

```
Anthropic:
  claude_patterns.py <-> tool-use/claude-tool-use.md
OpenAI:
  openai_utilities.py <-> function-calling/openai-function-calling.md
  assistants-api/openai-assistants.md
LangChain:
  agent-patterns/langchain-agents.md <-> lcel-patterns/langchain-reflexion-example.md
Microsoft:
  semantic-kernel/semantic-kernel-patterns.md <-> sk-csharp-examples.cs
  dotnet/csharp-multimodel-client.md
Cross-links:
  Many markdowns reference each other for related patterns and best practices.
```

## Consolidation Recommendations

| File(s) | Action | Rationale |
|---------|--------|-----------|
| openai_utilities.py, claude_patterns.py | CONSOLIDATE | Merge shared prompt formatting logic |
| assistants-api/openai-assistants.md | KEEP | Unique to OpenAI Assistants API |
| function-calling/openai-function-calling.md | KEEP | Core OpenAI pattern |
| sk-csharp-examples.cs | KEEP | Example code, no overlap |
| All markdown patterns | KEEP | Each covers a distinct workflow |
| (none) | ARCHIVE | No files currently recommended for archive |

---
