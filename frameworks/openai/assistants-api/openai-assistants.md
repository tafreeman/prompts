---
title: "OpenAI Assistants API Patterns"
category: "frameworks"
subcategory: "openai"
technique_type: "assistants-api"
framework_compatibility:
  openai: ">=1.0.0"
difficulty: "intermediate"
use_cases:
  - persistent-conversations
  - code-interpreter
  - file-retrieval
  - customer-support
performance_metrics:
  conversation_retention: "high"
  file_processing: "excellent"
  cost_efficiency: "medium"
testing:
  framework: "pytest"
  coverage: "85%"
  validation_status: "passed"
governance:
  data_classification: "confidential"
  risk_level: "medium"
  compliance_standards: ["GDPR", "SOC2"]
version: "1.0.0"
author: "AI Research Team"
last_updated: "2025-11-23"
tags:
  - openai
  - assistants
  - persistent-state
  - code-interpreter
  - retrieval
---

# OpenAI Assistants API Patterns

## Purpose

Build stateful, multi-turn AI assistants with persistent memory, file handling, and specialized tools (Code Interpreter, Retrieval) using OpenAI's Assistants API.

## Overview

The Assistants API is different from the Chat Completions API:

- **Stateful**: Conversations (Threads) are stored by OpenAI.
- **Built-in Tools**: Code Interpreter, File Search, Function Calling.
- **Asynchronous**: Uses polling or streaming for responses.

Key concepts:

1. **Assistant**: The AI configuration (model, instructions, tools).
2. **Thread**: A conversation session.
3. **Message**: User or assistant messages in a thread.
4. **Run**: An execution of the assistant on a thread.

## Prompt

### Assistant Instructions (System Prompt)

```markdown
You are a Senior C# Developer Assistant specializing in .NET 6+ and SQL Server.

**Your Capabilities**:
- Analyze C# code for bugs and suggest improvements
- Generate SQL queries and optimize database performance
- Explain architectural patterns (SOLID, DI, async/await)
- Use Code Interpreter to test algorithms

**Your Personality**:
- Be concise and technical
- Provide code examples when helpful
- Ask clarifying questions when requirements are ambiguous

**Constraints**:
- Always use parameterized queries for SQL
- Prefer async/await for I/O operations
- Follow C# naming conventions (PascalCase for public, camelCase for private)
```

## Example

### Creating an Assistant with Code Interpreter

```python
from openai import OpenAI
import time

client = OpenAI(api_key="your-api-key")

# 1. Create Assistant
assistant = client.beta.assistants.create(
    name="C# Code Analyzer",
    instructions="""
    You are a Senior C# Developer Assistant.
    Analyze code for bugs, security issues, and performance problems.
    Use Code Interpreter to test algorithms when helpful.
    """,
    model="gpt-4-turbo",
    tools=[{"type": "code_interpreter"}]
)

print(f"Assistant created: {assistant.id}")

# 2. Create Thread (Conversation)
thread = client.beta.threads.create()

# 3. Add User Message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="""
    Analyze this C# code for potential issues:
    
    ```csharp
    public List<User> GetUsers() {
        var users = new List<User>();
        using (var conn = new SqlConnection(connectionString)) {
            var cmd = new SqlCommand("SELECT * FROM Users", conn);
            conn.Open();
            var reader = cmd.ExecuteReader();
            while (reader.Read()) {
                users.Add(new User { Id = (int)reader["Id"] });
            }
        }
        return users;
    }
    ```
    """
)

# 4. Run Assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# 5. Poll for Completion
while run.status in ["queued", "in_progress"]:
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

# 6. Get Response
if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    latest_message = messages.data[0]
    print(latest_message.content[0].text.value)
```

### Expected Response

```
Issues found in your C# code:

1. **Not using async/await**: Database operations block the thread.
   Fix: Use `OpenAsync()`, `ExecuteReaderAsync()`, `ReadAsync()`

2. **Unsafe casting**: `(int)reader["Id"]` throws if Id is NULL.
   Fix: Use `reader.GetInt32(reader.GetOrdinal("Id"))` or check for DBNull

3. **Incomplete User object**: Only Id is populated.
   
Improved version:
```csharp
public async Task<List<User>> GetUsersAsync() {
    var users = new List<User>();
    await using (var conn = new SqlConnection(connectionString)) {
        var cmd = new SqlCommand("SELECT Id, Name, Email FROM Users", conn);
        await conn.OpenAsync();
        await using var reader = await cmd.ExecuteReaderAsync();
        while (await reader.ReadAsync()) {
            users.Add(new User { 
                Id = reader.GetInt32(0),
                Name = reader.GetString(1),
                Email = reader.GetString(2)
            });
        }
    }
    return users;
}
```

```

## Usage

### File Search (RAG) with Assistants

```python
# 1. Upload files
file = client.files.create(
    file=open("company_policies.pdf", "rb"),
    purpose="assistants"
)

# 2. Create Assistant with File Search
assistant = client.beta.assistants.create(
    name="HR Policy Assistant",
    instructions="Answer questions about company policies using the uploaded documents.",
    model="gpt-4-turbo",
    tools=[{"type": "file_search"}],
    tool_resources={
        "file_search": {
            "vector_stores": [{
                "file_ids": [file.id]
            }]
        }
    }
)

# 3. Ask Questions
thread = client.beta.threads.create()
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="How many vacation days do employees get?"
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)

messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)
```

### Function Calling with Assistants

```python
# Define function schema
tools = [{
    "type": "function",
    "function": {
        "name": "get_order_status",
        "description": "Retrieve the status of a customer order",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID"
                }
            },
            "required": ["order_id"]
        }
    }
}]

assistant = client.beta.assistants.create(
    name="Order Support Bot",
    instructions="Help customers check their order status.",
    model="gpt-4-turbo",
    tools=tools
)

# When run.status == "requires_action", execute the function
if run.status == "requires_action":
    tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    
    # Execute your function
    result = get_order_status(arguments["order_id"])
    
    # Submit result back
    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=[{
            "tool_call_id": tool_call.id,
            "output": json.dumps(result)
        }]
    )
```

## Best Practices

1. **Thread Management**: Reuse threads for the same user/conversation. Delete old threads to save costs.
2. **Streaming**: Use `stream=True` for better UX in chat applications.
3. **Error Handling**: Always check `run.status` for `failed`, `cancelled`, `expired`.
4. **File Limits**: Max 20 files per assistant. Files are automatically indexed for retrieval.
5. **Token Limits**: Threads have a 32k token context. Older messages are truncated automatically.
6. **Cost Control**: Assistants are charged per token + storage fees for files/threads.

## Related Patterns

- [Function Calling](./function-calling/openai-function-calling.md)
- [LangChain Agents](../langchain/agent-patterns/langchain-agents.md)
