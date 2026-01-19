---
title: "Agentic AI Patterns"
shortTitle: "Agentic"
intro: "Advanced patterns for autonomous agents, multi-agent systems, and tool-augmented AI workflows."
type: "reference"
difficulty: "advanced"
audience:
  - "senior-engineer"
  - "ai-researcher"
platforms:
  - "langchain"
  - "semantic-kernel"
  - "anthropic"
  - "openai"
author: "AI Research Team"
version: "1.0"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
dataClassification: "public"
reviewStatus: "approved"
---

# Agentic AI Patterns

Advanced patterns and architectures for building autonomous AI agents, multi-agent systems, and tool-augmented workflows. These patterns enable AI systems to make decisions, use tools, and collaborate to solve complex problems.

## 📋 Contents

```text
agentic/
├── README.md                      # This file
├── multi-agent/                   # Multi-agent coordination
│   └── multi-agent-workflow.md    # Orchestrated multi-agent systems
└── single-agent/                  # Enhanced single-agent patterns
    └── code-review-agent.md       # Single agent with specialized role
```

## 🎯 What are Agentic Patterns?

**Agentic AI** refers to AI systems that can:
- **Plan**: Break down complex goals into steps
- **Act**: Take actions and use tools
- **Observe**: Monitor results and adapt
- **Reason**: Make decisions based on context
- **Collaborate**: Work with other agents or humans

These patterns go beyond simple prompt-response by enabling autonomous, goal-directed behavior.

## ✨ Key Concepts

### Agent Anatomy

```text
┌─────────────────────────────────────┐
│           AI Agent                  │
├─────────────────────────────────────┤
│  Planning        │  Reasoning       │
│  - Goal setting  │  - Context       │
│  - Task decomp.  │  - Decision      │
│  - Scheduling    │  - Adaptation    │
├──────────────────┼──────────────────┤
│  Memory          │  Tools           │
│  - Short-term    │  - Functions     │
│  - Long-term     │  - APIs          │
│  - Episodic      │  - Databases     │
├──────────────────┴──────────────────┤
│         Action Execution            │
│  Execute, Observe, Reflect          │
└─────────────────────────────────────┘
```

### Agent Types

| Type | Description | Complexity | Use Case |
|------|-------------|------------|----------|
| **Reactive** | Respond to inputs directly | Low | Simple tasks, chatbots |
| **Deliberative** | Plan before acting | Medium | Problem-solving |
| **Learning** | Improve from experience | High | Adaptive systems |
| **Hybrid** | Combine approaches | Variable | Production systems |

## 🚀 Quick Start

### Single Agent Example

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate

# Define tools
@tool
def search_database(query: str) -> str:
    """Search the database for information."""
    # Your search logic here
    return f"Results for: {query}"

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        return str(eval(expression))
    except:
        return "Error in calculation"

# Create agent
llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
tools = [search_database, calculate]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant with access to tools.
    Use the search_database tool to find information.
    Use the calculate tool for math operations.
    Always explain your reasoning."""),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Execute
result = agent_executor.invoke({
    "input": "Find the average sales for Q4 and calculate 15% growth"
})
```

### Multi-Agent Example

```python
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI

# Define specialized agents
researcher_tools = [web_search, database_query]
writer_tools = [format_text, save_document]

# Researcher agent
researcher_agent = create_openai_functions_agent(
    llm=ChatOpenAI(model="gpt-4"),
    tools=researcher_tools,
    prompt=researcher_prompt
)

# Writer agent
writer_agent = create_openai_functions_agent(
    llm=ChatOpenAI(model="gpt-4"),
    tools=writer_tools,
    prompt=writer_prompt
)

# Orchestrate
research_result = researcher_agent.invoke({
    "input": "Research quantum computing trends"
})

article = writer_agent.invoke({
    "input": f"Write article based on: {research_result}"
})
```

## 📚 Pattern Categories

### Single-Agent Patterns

**Location:** `single-agent/`

Patterns for individual autonomous agents with specialized capabilities.

#### Code Review Agent

**File:** [code-review-agent.md](./single-agent/code-review-agent.md)

Autonomous code reviewer with deep analysis capabilities.

**Features:**
- Static analysis integration
- Security vulnerability detection
- Performance profiling
- Best practices enforcement
- Automated fix suggestions

**Example Use:**
```python
review_result = code_review_agent.invoke({
    "code": source_code,
    "language": "python",
    "focus": ["security", "performance"]
})
```

#### Other Single-Agent Patterns

- **Research Agent**: Autonomous research with source verification
- **Writing Agent**: Content creation with style consistency
- **Debug Agent**: Systematic bug identification and fixing
- **Test Agent**: Comprehensive test generation and execution

### Multi-Agent Patterns

**Location:** `multi-agent/`

Patterns for coordinating multiple agents working together.

#### Multi-Agent Workflow

**File:** [multi-agent-workflow.md](./multi-agent-workflow.md)

Orchestrated collaboration between specialized agents.

**Architectures:**

1. **Sequential**: Agents work in sequence
   ```text
   Agent A → Agent B → Agent C → Result
   ```

2. **Parallel**: Agents work simultaneously
   ```text
         ┌─ Agent A ─┐
   Input ├─ Agent B ─┤ → Aggregation → Result
         └─ Agent C ─┘
   ```

3. **Hierarchical**: Manager coordinates workers
   ```text
   Manager Agent
      ├─ Worker A (specialized task 1)
      ├─ Worker B (specialized task 2)
      └─ Worker C (specialized task 3)
   ```

4. **Collaborative**: Agents negotiate and iterate
   ```text
   Agent A ←→ Agent B ←→ Agent C
   (Iterative improvement through discussion)
   ```

## 🎓 Core Patterns

### 1. ReAct (Reasoning + Acting)

Interleave reasoning and action:

```text
Thought: I need to find the user's order history
Action: search_database("orders WHERE user_id=123")
Observation: Found 5 orders
Thought: Now I'll summarize the results
Action: format_summary(orders)
Observation: Summary created
Thought: Task complete
```

**Implementation:**
```python
prompt = """Answer the following question: {input}

You have access to these tools:
{tools}

Use this format:
Thought: [your reasoning]
Action: [tool name]
Action Input: [tool input]
Observation: [tool result]
... (repeat as needed)
Thought: I have the final answer
Final Answer: [your answer]
"""
```

### 2. Plan-and-Execute

Separate planning from execution:

```python
# Planning phase
planner_prompt = """Create a step-by-step plan to: {goal}

Available tools: {tools}

Return a JSON plan:
{
  "steps": [
    {"action": "tool_name", "input": "...", "reasoning": "..."},
    ...
  ]
}
"""

# Execution phase
for step in plan["steps"]:
    result = execute_tool(step["action"], step["input"])
    if needs_replanning(result):
        plan = replan(goal, results_so_far)
```

### 3. Tool Use

Equip agents with capabilities:

```python
from langchain.tools import Tool

tools = [
    Tool(
        name="Calculator",
        func=lambda x: eval(x),
        description="Useful for math. Input: mathematical expression"
    ),
    Tool(
        name="Search",
        func=search_function,
        description="Search for information. Input: search query"
    ),
    Tool(
        name="Database",
        func=db_query,
        description="Query database. Input: SQL query"
    )
]
```

### 4. Memory Management

Maintain context across interactions:

```python
from langchain.memory import ConversationBufferMemory

# Short-term memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Long-term memory with vector store
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

long_term_memory = Chroma(
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./agent_memory"
)
```

### 5. Self-Reflection

Agents critique their own work:

```python
reflection_prompt = """Review your previous response:

Original Task: {task}
Your Response: {response}

Evaluate:
1. Completeness: Did you fully address the task?
2. Accuracy: Are your facts correct?
3. Quality: Could the response be improved?

Provide:
- Issues found
- Improvements needed
- Revised response (if necessary)
"""
```

## 🔧 Advanced Techniques

### Error Recovery

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def resilient_agent_call(agent, input_data):
    try:
        return agent.invoke(input_data)
    except ToolException as e:
        # Handle tool errors
        return handle_tool_error(e)
    except Exception as e:
        # General error handling
        log_error(e)
        raise
```

### Parallel Execution

```python
import asyncio
from typing import List

async def execute_agents_parallel(agents: List, inputs: List):
    tasks = [
        agent.ainvoke(input_data)
        for agent, input_data in zip(agents, inputs)
    ]
    results = await asyncio.gather(*tasks)
    return results

# Usage
results = asyncio.run(execute_agents_parallel(
    agents=[agent1, agent2, agent3],
    inputs=[input1, input2, input3]
))
```

### Dynamic Tool Selection

```python
def select_tools(task_type: str) -> List[Tool]:
    """Dynamically select tools based on task."""
    tool_map = {
        "research": [search_tool, summarize_tool],
        "coding": [code_gen_tool, test_tool, debug_tool],
        "analysis": [data_tool, viz_tool, stats_tool]
    }
    return tool_map.get(task_type, [])

# Use appropriate tools for task
tools = select_tools(task_type)
agent = create_agent(llm, tools, prompt)
```

## 📊 Comparison: Single vs Multi-Agent

| Aspect | Single Agent | Multi-Agent |
|--------|--------------|-------------|
| **Complexity** | Low-Medium | High |
| **Latency** | Lower | Higher (coordination overhead) |
| **Specialization** | Generalist | Deep expertise per agent |
| **Scalability** | Limited | Better horizontal scaling |
| **Debugging** | Easier | More challenging |
| **Cost** | Lower | Higher (multiple LLM calls) |
| **Use Cases** | Simple tasks | Complex, multi-faceted problems |

**When to Use Single Agent:**
- Task is well-defined and focused
- Latency is critical
- Cost constraints
- Simpler debugging needs

**When to Use Multi-Agent:**
- Task requires diverse expertise
- Parallel processing beneficial
- Quality > speed
- Complex problem decomposition

## 🛠️ Tools & Frameworks

### Agent Frameworks

| Framework | Language | Strengths | Learning Curve |
|-----------|----------|-----------|----------------|
| **LangChain** | Python | Comprehensive, well-documented | Medium |
| **AutoGPT** | Python | Autonomous, goal-directed | Low |
| **BabyAGI** | Python | Task-driven autonomy | Low |
| **Semantic Kernel** | C#, Python | .NET integration, planning | Medium |
| **LlamaIndex** | Python | Data-focused agents | Medium |

### Development Tools

```bash
# LangChain agent development
pip install langchain langchain-openai

# Semantic Kernel
pip install semantic-kernel

# Agent observability
pip install langsmith  # LangChain tracing
pip install wandb      # Experiment tracking
```

## 📖 Best Practices

### 1. Design Clear Roles

✅ **Do:**
```python
researcher_prompt = """You are a research specialist.
Your role:
- Find accurate information
- Verify sources
- Cite references
Do NOT attempt to write or format content."""
```

❌ **Don't:**
```python
agent_prompt = "You are a helpful assistant."
```

### 2. Limit Tool Access

```python
# Give each agent only needed tools
researcher_agent = create_agent(llm, [search, database], researcher_prompt)
writer_agent = create_agent(llm, [format, save], writer_prompt)

# Not: all_tools for every agent
```

### 3. Implement Guardrails

```python
def safe_agent_execution(agent, input_data, max_iterations=10):
    """Execute with safety limits."""
    for i in range(max_iterations):
        result = agent.invoke(input_data)
        
        if is_complete(result):
            return result
        
        if is_stuck(result):
            return fallback_handler(input_data)
    
    raise MaxIterationsExceeded()
```

### 4. Monitor and Log

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def logged_agent_call(agent, input_data):
    logger.info(f"Agent call started: {input_data}")
    start_time = time.time()
    
    result = agent.invoke(input_data)
    
    duration = time.time() - start_time
    logger.info(f"Agent call completed in {duration:.2f}s")
    
    return result
```

## 📚 Additional Resources

### Research Papers
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)
- [Generative Agents](https://arxiv.org/abs/2304.03442)
- [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT)

### Frameworks & Tools
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [Semantic Kernel Planning](https://learn.microsoft.com/en-us/semantic-kernel/agents/)
- [AutoGen](https://microsoft.github.io/autogen/)

### Tutorials
- [Building Autonomous Agents](https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/)
- [Multi-Agent Systems](https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai/)

## 🤝 Contributing

When adding agentic patterns:

1. **Test thoroughly**: Verify agent behavior in various scenarios
2. **Document limitations**: What can/cannot the agent do?
3. **Include safety measures**: Error handling, iteration limits
4. **Provide examples**: Show both success and failure cases
5. **Measure performance**: Latency, cost, success rate

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines.

## ⚠️ Common Pitfalls

### 1. Infinite Loops

**Problem:** Agent gets stuck repeating actions

**Solution:**
```python
max_iterations = 10
iteration_count = 0

while not task_complete and iteration_count < max_iterations:
    result = agent.step()
    iteration_count += 1
```

### 2. Tool Hallucination

**Problem:** Agent invents non-existent tools

**Solution:**
```python
# Strict tool validation
available_tools = ["search", "calculate", "database"]
if requested_tool not in available_tools:
    return "Error: Tool not available"
```

### 3. Context Overflow

**Problem:** Memory grows too large

**Solution:**
```python
from langchain.memory import ConversationSummaryMemory

# Summarize old conversations
memory = ConversationSummaryMemory(
    llm=llm,
    max_token_limit=1000
)
```

## 📝 Version History

- **1.0** (2025-11-30): Initial release with single and multi-agent patterns

---

**Need Help?** Check the [LangChain agents documentation](https://python.langchain.com/docs/modules/agents/) or [open an issue](https://github.com/tafreeman/prompts/issues).
