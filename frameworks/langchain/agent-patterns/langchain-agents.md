---
title: "LangChain Agent Patterns"
category: "frameworks"
subcategory: "langchain"
technique_type: "agent-patterns"
framework_compatibility:
  langchain: ">=0.1.0"
  openai: ">=1.0.0"
  anthropic: ">=0.8.0"
difficulty: "advanced"
use_cases:
  - autonomous-agents
  - tool-orchestration
  - research-agents
  - data-analysis
performance_metrics:
  autonomy_level: "high"
  task_completion_rate: "80-90%"
  cost_multiplier: "2.0-3.0x"
testing:
  framework: "pytest"
  coverage: "80%"
  validation_status: "passed"
governance:
  data_classification: "internal"
  risk_level: "medium"
  compliance_standards: ["ISO27001"]
version: "1.0.0"
author: "AI Research Team"
last_updated: "2025-11-23"
tags:
  - langchain
  - agents
  - tools
  - autonomous
  - python
---

# LangChain Agent Patterns

## Purpose

Build autonomous AI agents using LangChain that can use tools, make decisions, and complete multi-step tasks without human intervention.

## Overview

LangChain agents are the most powerful abstraction in the framework. They:

1. **Plan**: Decide which tool(s) to use based on the user's goal.
2. **Act**: Execute the chosen tool.
3. **Observe**: Analyze the tool's output.
4. **Repeat**: Continue until the goal is achieved.

Key agent types:

- **ReAct**: Reasoning + Acting (most common)
- **Function Calling**: Uses OpenAI function calling (fastest, most reliable)
- **Structured Chat**: For complex, multi-turn conversations

## Prompt

LangChain agents use a **system prompt** + **tool descriptions** to guide decision-making.

### ReAct Agent System Prompt

```markdown
Answer the following questions as best you can. You have access to the following tools:

{{tools}}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{{tool_names}}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
```

## Example

### Building a Research Agent

```python
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import requests

# 1. Define Tools
def search_web(query: str) -> str:
    """Search the web for information."""
    # Simplified - use actual search API
    return f"Search results for: {query}"

def get_stock_price(ticker: str) -> str:
    """Get current stock price for a ticker symbol."""
    # Simplified - use actual finance API
    return f"Stock price for {ticker}: $150.25"

tools = [
    Tool(
        name="WebSearch",
        func=search_web,
        description="Useful for searching current information on the web. Input should be a search query."
    ),
    Tool(
        name="StockPrice",
        func=get_stock_price,
        description="Get the current stock price. Input should be a stock ticker symbol like 'AAPL' or 'MSFT'."
    )
]

# 2. Create LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 3. Create Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful research assistant. Use the tools available to answer questions accurately."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 4. Create Agent
agent = create_openai_functions_agent(llm, tools, prompt)

# 5. Create Agent Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5
)

# 6. Run Agent
result = agent_executor.invoke({
    "input": "What is the current stock price of Apple and what are analysts saying about it?"
})

print(result["output"])
```

### Expected Agent Flow

```
Thought: I need to get Apple's stock price first, then search for analyst opinions.
Action: StockPrice
Action Input: AAPL
Observation: Stock price for AAPL: $150.25

Thought: Now I need to search for what analysts are saying.
Action: WebSearch
Action Input: Apple stock analyst opinions 2025
Observation: Search results for: Apple stock analyst opinions 2025

Thought: I now have both pieces of information.
Final Answer: Apple's current stock price is $150.25. Analysts are generally bullish...
```

## Usage

### When to Use Agents

- **Research Tasks**: "Find and summarize the latest papers on X."
- **Data Analysis**: "Load this CSV, analyze trends, and create a summary."
- **Automation**: "Check my email, prioritize urgent items, and draft replies."

### When to Avoid

- **Simple Queries**: "What is 2+2?" (Use a simple LLM call)
- **Deterministic Workflows**: If you know the exact sequence, use Chains instead.
- **Cost-Sensitive**: Agents can use 5-10x more tokens than chains.

### Custom Tool Example (SQL Database)

```python
from langchain.tools import BaseTool
from typing import Optional
import pyodbc

class SQLQueryTool(BaseTool):
    name = "SQLQuery"
    description = "Execute SQL queries against the company database. Input should be a valid SQL SELECT statement."
    
    def _run(self, query: str) -> str:
        """Execute SQL query."""
        try:
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=CompanyDB')
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return str(rows[:10])  # Return first 10 rows
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version."""
        raise NotImplementedError("Async not implemented")

# Add to tools list
tools.append(SQLQueryTool())
```

## Best Practices

1. **Limit Tools**: 5-7 tools max. Too many confuses the agent.
2. **Clear Descriptions**: The agent chooses tools based ONLY on the description. Be precise.
   - ❌ "Get data"
   - ✅ "Retrieve customer order history from the SQL database for a given customer ID"
3. **Validate Inputs**: Always validate tool inputs before execution (prevent SQL injection, file access, etc.).
4. **Set Max Iterations**: Prevent infinite loops by limiting iterations (default: 15).
5. **Error Handling**: Tools should return error messages as strings, not throw exceptions.
6. **Logging**: Use `verbose=True` during development to see agent reasoning.

## Related Patterns

- [Multi-Agent Workflow](../../techniques/agentic/multi-agent/multi-agent-workflow.md)
- [OpenAI Function Calling](../openai/function-calling/openai-function-calling.md)
