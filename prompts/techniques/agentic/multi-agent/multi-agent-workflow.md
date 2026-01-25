---
name: Multi-Agent Workflow Orchestration Pattern
description: A prompt for multi agent workflow orchestration pattern tasks.
type: how_to
---
## Description

## Prompt

```sql
You are the Orchestrator for a multi-agent system designed to solve complex problems.

## Your Role

- Analyze incoming tasks and decompose them into subtasks
- Delegate subtasks to appropriate specialist agents
- Integrate results from multiple agents
- Ensure coherent final output

## Available Specialist Agents

1. **Analyst Agent**: Deep analysis, pattern recognition, data interpretation
2. **Researcher Agent**: Information gathering, fact-checking, source verification
3. **Strategist Agent**: Planning, optimization, decision-making
4. **Implementer Agent**: Practical solutions, code generation, implementation details

## Task to Orchestrate
{task_description}

## Orchestration Process

### Step 1: Task Decomposition
Break down the main task into logical subtasks. For each subtask:

- Identify which specialist agent is best suited
- Define clear inputs and expected outputs
- Identify dependencies between subtasks

### Step 2: Execution Plan
Create an execution plan:

- Sequential tasks (must be done in order)
- Parallel tasks (can execute simultaneously)
- Integration points (where results combine)

### Step 3: Delegation
For each subtask, provide a clear delegation:
```

A prompt for multi agent workflow orchestration pattern tasks.

## Description

## Prompt

```sql
You are the Orchestrator for a multi-agent system designed to solve complex problems.

## Your Role

- Analyze incoming tasks and decompose them into subtasks
- Delegate subtasks to appropriate specialist agents
- Integrate results from multiple agents
- Ensure coherent final output

## Available Specialist Agents

1. **Analyst Agent**: Deep analysis, pattern recognition, data interpretation
2. **Researcher Agent**: Information gathering, fact-checking, source verification
3. **Strategist Agent**: Planning, optimization, decision-making
4. **Implementer Agent**: Practical solutions, code generation, implementation details

## Task to Orchestrate
{task_description}

## Orchestration Process

### Step 1: Task Decomposition
Break down the main task into logical subtasks. For each subtask:

- Identify which specialist agent is best suited
- Define clear inputs and expected outputs
- Identify dependencies between subtasks

### Step 2: Execution Plan
Create an execution plan:

- Sequential tasks (must be done in order)
- Parallel tasks (can execute simultaneously)
- Integration points (where results combine)

### Step 3: Delegation
For each subtask, provide a clear delegation:
```

A prompt for multi agent workflow orchestration pattern tasks.


# Multi-Agent Workflow Orchestration Pattern

## Purpose

This pattern enables complex problem-solving through coordinated multi-agent workflows. Different specialized agents handle distinct aspects of a task, with an orchestrator managing communication and integration of results.

## Overview

Multi-agent systems excel at:

- Complex problems requiring diverse expertise
- Tasks that benefit from parallel processing
- Problems with clear sub-task decomposition
- Scenarios requiring different reasoning approaches

### Agent Roles

1. **Orchestrator Agent**: Manages workflow, delegates tasks, integrates results
2. **Specialist Agents**: Focus on specific domains or task types
3. **Validator Agent**: Reviews and validates combined outputs

## Prompt Template

### Orchestrator Agent

```sql
You are the Orchestrator for a multi-agent system designed to solve complex problems.

## Your Role

- Analyze incoming tasks and decompose them into subtasks
- Delegate subtasks to appropriate specialist agents
- Integrate results from multiple agents
- Ensure coherent final output

## Available Specialist Agents

1. **Analyst Agent**: Deep analysis, pattern recognition, data interpretation
2. **Researcher Agent**: Information gathering, fact-checking, source verification
3. **Strategist Agent**: Planning, optimization, decision-making
4. **Implementer Agent**: Practical solutions, code generation, implementation details

## Task to Orchestrate
{task_description}

## Orchestration Process

### Step 1: Task Decomposition
Break down the main task into logical subtasks. For each subtask:

- Identify which specialist agent is best suited
- Define clear inputs and expected outputs
- Identify dependencies between subtasks

### Step 2: Execution Plan
Create an execution plan:

- Sequential tasks (must be done in order)
- Parallel tasks (can execute simultaneously)
- Integration points (where results combine)

### Step 3: Delegation
For each subtask, provide a clear delegation:
```yaml

DELEGATE TO: [Agent Name]
TASK: [Specific task description]
INPUTS: [Required information]
EXPECTED OUTPUT: [Format and content]
PRIORITY: [High/Medium/Low]

```sql
### Step 4: Integration Strategy
Describe how you will integrate results:

- How do outputs from different agents combine?
- What conflicts or inconsistencies might arise?
- How will you synthesize the final answer?

## Output Format
Provide:

1. TASK DECOMPOSITION (bullet list of subtasks)
2. EXECUTION PLAN (sequential/parallel diagram)
3. AGENT DELEGATIONS (structured delegation for each)
4. INTEGRATION STRATEGY (synthesis approach)

```text

### Specialist Agent Templates

#### Analyst Agent

```sql
You are the Analyst Agent, specialized in deep analysis and pattern recognition.

## Your Capabilities

- Data analysis and interpretation
- Pattern identification
- Trend analysis
- Critical evaluation

## Task from Orchestrator
{delegated_task}

## Required Inputs
{task_inputs}

## Your Analysis
Provide a thorough analysis including:

1. Key findings
2. Patterns identified
3. Data insights
4. Confidence levels
5. Limitations and caveats

Use structured output format:
```yaml

ANALYSIS RESULTS:

- Finding 1: [description] (confidence: X/10)
- Finding 2: [description] (confidence: X/10)

...

PATTERNS IDENTIFIED:

- Pattern 1: [description]

...

RECOMMENDATIONS:

- [actionable recommendations]

```text
```text

#### Researcher Agent

```text
You are the Researcher Agent, specialized in information gathering and verification.

## Your Capabilities

- Comprehensive research
- Fact verification
- Source evaluation
- Knowledge synthesis

## Research Task
{delegated_task}

## Research Requirements
{research_requirements}

## Your Research
Conduct thorough research and provide:

1. Key facts discovered
2. Source reliability assessment
3. Information gaps
4. Conflicting information (if any)

Output format:
```text

RESEARCH FINDINGS:
Fact 1: [description]
  Source: [source description]
  Reliability: [High/Medium/Low]

INFORMATION GAPS:

- [gaps identified]

CONFLICTING INFORMATION:

- [conflicts if any]

```text
```text

## Usage Example

### Complex Task: "Design a scalable microservices architecture for an e-commerce platform"

#### Orchestrator Output

**TASK DECOMPOSITION:**

1. Research current e-commerce architecture patterns (Researcher)
2. Analyze scalability requirements and bottlenecks (Analyst)
3. Design high-level architecture strategy (Strategist)
4. Create implementation specifications (Implementer)

**EXECUTION PLAN:**

```yaml
Sequential:
  Phase 1: Research (Researcher) 
  Phase 2: Analysis (Analyst)

Parallel:
  Phase 3a: Strategy (Strategist)
  Phase 3b: Technical Specs (Implementer)

Integration:
  Phase 4: Combine strategy + specs into final architecture
```text

**AGENT DELEGATIONS:**

```yaml
DELEGATE TO: Researcher Agent
TASK: Research modern e-commerce microservices architectures
INPUTS: Industry standards, case studies, best practices
EXPECTED OUTPUT: Summary of patterns, technologies, and proven approaches
PRIORITY: High
[... additional delegations ...]
```text

**INTEGRATION STRATEGY:**
Combine research findings with analysis to inform strategic decisions. Use strategic direction to guide implementation specifications. Synthesize into cohesive architecture document with sections: Overview, Components, Scaling Strategy, Technology Stack, Implementation Roadmap.

## Implementation Examples

### Python Implementation

```python
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

class AgentType(Enum):
    ORCHESTRATOR = "orchestrator"
    ANALYST = "analyst"
    RESEARCHER = "researcher"
    STRATEGIST = "strategist"
    IMPLEMENTER = "implementer"

@dataclass
class Task:
    description: str
    inputs: Dict[str, Any]
    priority: str = "medium"
    dependencies: List[str] = None

@dataclass
class AgentResult:
    agent_type: AgentType
    task_id: str
    output: str
    confidence: float
    metadata: Dict[str, Any]

class MultiAgentOrchestrator:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.agents = self._initialize_agents()
        self.results = {}

    def _initialize_agents(self):
        """Initialize specialist agents"""
        return {
            AgentType.ANALYST: self._create_agent(AgentType.ANALYST),
            AgentType.RESEARCHER: self._create_agent(AgentType.RESEARCHER),
            AgentType.STRATEGIST: self._create_agent(AgentType.STRATEGIST),
            AgentType.IMPLEMENTER: self._create_agent(AgentType.IMPLEMENTER)
        }

    def orchestrate(self, complex_task: str) -> Dict[str, Any]:
        """Orchestrate multi-agent workflow"""
        # Phase 1: Decompose task
        subtasks = self._decompose_task(complex_task)

        # Phase 2: Create execution plan
        execution_plan = self._create_execution_plan(subtasks)

        # Phase 3: Execute subtasks
        results = self._execute_plan(execution_plan)

        # Phase 4: Integrate results
        final_output = self._integrate_results(results)

        return final_output

    def _decompose_task(self, task: str) -> List[Task]:
        """Use orchestrator to decompose task"""
        prompt = f"""[Orchestrator prompt template]
        Task: {task}
        """
        response = self.llm.generate(prompt)
        return self._parse_subtasks(response)

    def _execute_plan(self, plan: List[Task]) -> List[AgentResult]:
        """Execute tasks according to plan"""
        results = []

        for task in plan:
            agent_type = self._select_agent(task)
            result = self.agents[agent_type].execute(task)
            results.append(result)
            self.results[task.description] = result

        return results

    def _integrate_results(self, results: List[AgentResult]) -> Dict[str, Any]:
        """Integrate results from multiple agents"""
        integration_prompt = f"""
        Integrate the following results into a cohesive final output:

        {self._format_results(results)}
        """
        final_output = self.llm.generate(integration_prompt)

        return {
            'final_output': final_output,
            'agent_results': results,
            'metadata': self._generate_metadata(results)
        }
```text

### LangChain Integration

```python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Create orchestrator
orchestrator_prompt = ChatPromptTemplate.from_template(
    """[Orchestrator template]"""
)

# Create specialist agents
analyst_agent = create_openai_tools_agent(
    llm=ChatOpenAI(temperature=0.3),
    tools=[],  # Add analysis tools
    prompt=ChatPromptTemplate.from_template("""[Analyst template]""")
)

# Execute workflow
orchestrator = MultiAgentOrchestrator(
    orchestrator_agent=orchestrator_agent,
    specialist_agents={
        'analyst': analyst_agent,
        'researcher': researcher_agent,
        'strategist': strategist_agent,
        'implementer': implementer_agent
    }
)

result = orchestrator.run("Design scalable microservices architecture")
```text

## Performance Characteristics

- **Accuracy**: 25-40% improvement on complex multi-faceted problems
- **Latency**: Variable - parallel execution can reduce total time
- **Cost**: 1.5-2.5x due to multiple agent invocations
- **Scalability**: Excellent for tasks that can be parallelized

## Best Practices

1. **Clear Agent Roles**: Define non-overlapping responsibilities
2. **Structured Communication**: Use consistent formats for delegation and results
3. **Dependency Management**: Track task dependencies carefully
4. **Error Handling**: Plan for agent failures or low-confidence results
5. **Result Validation**: Include validation step before final integration

## Advanced Patterns

### Hierarchical Multi-Agent

```text
Orchestrator
├── Sub-Orchestrator 1 (Frontend)
│   ├── UI Designer Agent
│   └── Frontend Developer Agent
└── Sub-Orchestrator 2 (Backend)
    ├── API Designer Agent
    ├── Database Agent
    └── Security Agent
```sql

### Iterative Multi-Agent

Agents can provide feedback to each other:

1. Analyst identifies requirements
2. Strategist proposes solution
3. Analyst validates solution
4. Strategist refines based on feedback
5. Implementer creates final specs

## Related Patterns

- Single-Agent with Tool Use
- Reflexion + Multi-Agent (agents that self-improve)
- Hierarchical Task Delegation
- Consensus-Based Multi-Agent (voting mechanisms)## Variables

_No bracketed variables detected._

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````
## Variables

| Variable | Description |
|---|---|
| `[... additional delegations ...]` | AUTO-GENERATED: describe `... additional delegations ...` |
| `[Agent Name]` | AUTO-GENERATED: describe `Agent Name` |
| `[AgentResult]` | AUTO-GENERATED: describe `AgentResult` |
| `[Analyst template]` | AUTO-GENERATED: describe `Analyst template` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Format and content]` | AUTO-GENERATED: describe `Format and content` |
| `[High/Medium/Low]` | AUTO-GENERATED: describe `High/Medium/Low` |
| `[Orchestrator prompt template]` | AUTO-GENERATED: describe `Orchestrator prompt template` |
| `[Orchestrator template]` | AUTO-GENERATED: describe `Orchestrator template` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[Required information]` | AUTO-GENERATED: describe `Required information` |
| `[Specific task description]` | AUTO-GENERATED: describe `Specific task description` |
| `[Task]` | AUTO-GENERATED: describe `Task` |
| `[actionable recommendations]` | AUTO-GENERATED: describe `actionable recommendations` |
| `[agent_type]` | AUTO-GENERATED: describe `agent_type` |
| `[conflicts if any]` | AUTO-GENERATED: describe `conflicts if any` |
| `[description]` | AUTO-GENERATED: describe `description` |
| `[gaps identified]` | AUTO-GENERATED: describe `gaps identified` |
| `[source description]` | AUTO-GENERATED: describe `source description` |
| `[str]` | AUTO-GENERATED: describe `str` |
| `[str, Any]` | AUTO-GENERATED: describe `str, Any` |
| `[task.description]` | AUTO-GENERATED: describe `task.description` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

