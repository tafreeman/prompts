#!/usr/bin/env python3
"""
Multi-Agent Orchestrator
========================

A real execution engine for multi-agent workflows. This implements the pattern
described in prompts/techniques/agentic/multi-agent/multi-agent-workflow.md.

Unlike the prompt template (which simulates multi-agent coordination in a single
LLM call), this module actually:
- Spawns separate LLM calls for each specialist agent
- Executes tasks in sequence or parallel based on dependencies
- Integrates results from multiple agents
- Handles errors and retries

Usage:
    # Basic usage
    from tools.agents.multi_agent_orchestrator import MultiAgentOrchestrator

    orchestrator = MultiAgentOrchestrator(model="gh:gpt-4o-mini")
    result = orchestrator.run("Design a scalable microservices architecture")

    # CLI usage
    python -m tools.agents.multi_agent_orchestrator "Your complex task here"

    # With specific model
    python -m tools.agents.multi_agent_orchestrator --model local:phi4 "Your task"

Author: Prompts Library Team
Version: 1.0
"""

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Add parent directory to path for imports
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parents[2]))

from tools.llm.llm_client import LLMClient

# =============================================================================
# DATA STRUCTURES
# =============================================================================


class AgentType(Enum):
    """Types of specialist agents available."""

    ORCHESTRATOR = "orchestrator"
    ANALYST = "analyst"
    RESEARCHER = "researcher"
    STRATEGIST = "strategist"
    IMPLEMENTER = "implementer"
    VALIDATOR = "validator"


class TaskPriority(Enum):
    """Task priority levels."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(Enum):
    """Task execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Task:
    """Represents a delegated subtask."""

    id: str
    description: str
    agent_type: AgentType
    inputs: Dict[str, Any] = field(default_factory=dict)
    expected_output: str = ""
    priority: TaskPriority = TaskPriority.MEDIUM
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    confidence: float = 0.0
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @property
    def duration_seconds(self) -> Optional[float]:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


@dataclass
class ExecutionPlan:
    """Represents the orchestrated execution plan."""

    phases: List[List[Task]]  # Each phase is a list of parallel tasks
    integration_strategy: str = ""


@dataclass
class OrchestratorResult:
    """Final result from the multi-agent workflow."""

    task_description: str
    plan: ExecutionPlan
    agent_results: Dict[str, Task]
    final_output: str
    total_duration_seconds: float
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# AGENT PROMPTS
# =============================================================================

ORCHESTRATOR_PROMPT = """You are the Orchestrator for a multi-agent system designed to solve complex problems.

## Your Role
- Analyze incoming tasks and decompose them into subtasks
- Delegate subtasks to appropriate specialist agents
- Create an execution plan with phases

## Available Specialist Agents
1. **Analyst Agent**: Deep analysis, pattern recognition, data interpretation
2. **Researcher Agent**: Information gathering, fact-checking, source verification
3. **Strategist Agent**: Planning, optimization, decision-making
4. **Implementer Agent**: Practical solutions, code generation, implementation details

## Task to Orchestrate
{task_description}

## Instructions
Decompose this task and create a structured execution plan.

Output your plan in this EXACT JSON format (no markdown, just JSON):
{{
    "subtasks": [
        {{
            "id": "task_1",
            "description": "Description of the subtask",
            "agent": "analyst|researcher|strategist|implementer",
            "inputs": {{"key": "value"}},
            "expected_output": "What this task should produce",
            "priority": "high|medium|low",
            "dependencies": []
        }}
    ],
    "phases": [
        ["task_1"],
        ["task_2", "task_3"],
        ["task_4"]
    ],
    "integration_strategy": "How to combine results into final output"
}}

Rules:
- Tasks in the same phase can run in parallel
- Tasks can only depend on tasks from earlier phases
- Aim for 3-6 subtasks maximum
- Be specific about inputs and expected outputs"""


ANALYST_PROMPT = """You are the Analyst Agent, specialized in deep analysis and pattern recognition.

## Your Capabilities
- Data analysis and interpretation
- Pattern identification
- Trend analysis
- Critical evaluation

## Task from Orchestrator
{task_description}

## Context from Previous Tasks
{context}

## Required Inputs
{inputs}

## Instructions
Provide a thorough analysis. Be specific and actionable.

Output your analysis in this format:

**KEY FINDINGS:**
1. [Finding with supporting evidence]
2. [Finding with supporting evidence]

**PATTERNS IDENTIFIED:**
- [Pattern and its implications]

**CONFIDENCE ASSESSMENT:**
- Overall confidence: X/10
- Key uncertainties: [list any gaps]

**RECOMMENDATIONS:**
- [Actionable recommendation based on analysis]"""


RESEARCHER_PROMPT = """You are the Researcher Agent, specialized in information gathering and verification.

## Your Capabilities
- Comprehensive research synthesis
- Fact verification
- Source evaluation
- Knowledge synthesis

## Research Task
{task_description}

## Context from Previous Tasks
{context}

## Research Requirements
{inputs}

## Instructions
Synthesize knowledge on this topic. Distinguish between established facts and inferences.

Output your research in this format:

**RESEARCH FINDINGS:**
1. [Fact/Finding]
   - Basis: [Why this is likely true]
   - Reliability: High/Medium/Low

**INFORMATION GAPS:**
- [What's unknown or uncertain]

**KEY TAKEAWAYS:**
- [Most important points for the project]"""


STRATEGIST_PROMPT = """You are the Strategist Agent, specialized in planning and decision-making.

## Your Capabilities
- Strategic planning
- Option analysis
- Risk assessment
- Optimization

## Strategy Task
{task_description}

## Context from Previous Tasks
{context}

## Strategic Requirements
{inputs}

## Instructions
Develop a clear strategy. Consider tradeoffs and alternatives.

Output your strategy in this format:

**STRATEGIC APPROACH:**
[High-level strategy summary]

**OPTIONS CONSIDERED:**
1. [Option A] - Pros: ... Cons: ...
2. [Option B] - Pros: ... Cons: ...

**RECOMMENDED APPROACH:**
[Chosen approach with rationale]

**RISK MITIGATION:**
- Risk: [risk] → Mitigation: [approach]

**SUCCESS METRICS:**
- [How to measure success]"""


IMPLEMENTER_PROMPT = """You are the Implementer Agent, specialized in practical solutions and implementation.

## Your Capabilities
- Practical solutions
- Code generation
- Implementation details
- Technical specifications

## Implementation Task
{task_description}

## Context from Previous Tasks
{context}

## Implementation Requirements
{inputs}

## Instructions
Provide concrete, actionable implementation details. Include code or specifications where appropriate.

Output your implementation in this format:

**IMPLEMENTATION APPROACH:**
[How to implement this]

**TECHNICAL SPECIFICATIONS:**
- [Spec 1]
- [Spec 2]

**CODE/ARTIFACTS:**
```
[Code or configuration if applicable]
```

**NEXT STEPS:**
1. [Immediate action item]
2. [Follow-up action]

**DEPENDENCIES:**
- [What's needed to implement this]"""


INTEGRATION_PROMPT = """You are integrating results from multiple specialist agents into a cohesive final output.

## Original Task
{task_description}

## Integration Strategy
{integration_strategy}

## Agent Results

{agent_results}

## Instructions
Synthesize all agent outputs into a comprehensive, actionable final deliverable.

Requirements:
- Resolve any conflicts between agent outputs
- Ensure logical flow and consistency
- Highlight the most important findings and recommendations
- Make it actionable for the end user

Provide the final integrated output:"""


AGENT_PROMPTS = {
    AgentType.ANALYST: ANALYST_PROMPT,
    AgentType.RESEARCHER: RESEARCHER_PROMPT,
    AgentType.STRATEGIST: STRATEGIST_PROMPT,
    AgentType.IMPLEMENTER: IMPLEMENTER_PROMPT,
}


# =============================================================================
# MULTI-AGENT ORCHESTRATOR
# =============================================================================


class MultiAgentOrchestrator:
    """Orchestrates multi-agent workflows with real LLM execution.

    This is a real implementation - not a simulation. Each agent gets its own
    LLM call, tasks execute in parallel where possible, and results are
    integrated at the end.
    """

    def __init__(
        self,
        model: str = "gh:gpt-4o-mini",
        temperature: float = 0.7,
        max_parallel: int = 3,
        verbose: bool = False,
    ):
        """Initialize the orchestrator.

        Args:
            model: Model to use for all agents (e.g., "gh:gpt-4o-mini", "local:phi4")
            temperature: Sampling temperature (0.0-2.0)
            max_parallel: Maximum parallel agent executions
            verbose: Print detailed progress information
        """
        self.model = model
        self.temperature = temperature
        self.max_parallel = max_parallel
        self.verbose = verbose
        self.tasks: Dict[str, Task] = {}
        self.context: Dict[str, str] = {}  # Accumulated context from completed tasks

    def _log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[Orchestrator] {message}")

    def _call_llm(self, prompt: str, system: Optional[str] = None) -> str:
        """Make an LLM call using the configured model."""
        return LLMClient.generate_text(
            model_name=self.model,
            prompt=prompt,
            system_instruction=system,
            temperature=self.temperature,
            max_tokens=4096,
        )

    def _parse_plan(self, response: str) -> Tuple[List[Task], ExecutionPlan]:
        """Parse the orchestrator's JSON response into tasks and execution
        plan."""
        # Extract JSON from response (handle markdown code blocks)
        json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", response)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find raw JSON
            json_match = re.search(r"\{[\s\S]*\}", response)
            if json_match:
                json_str = json_match.group(0)
            else:
                raise ValueError(
                    f"Could not parse JSON from orchestrator response: {response[:500]}"
                )

        try:
            plan_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in orchestrator response: {e}")

        # Parse subtasks
        tasks = []
        for subtask in plan_data.get("subtasks", []):
            agent_type_str = subtask.get("agent", "analyst").lower()
            agent_type = {
                "analyst": AgentType.ANALYST,
                "researcher": AgentType.RESEARCHER,
                "strategist": AgentType.STRATEGIST,
                "implementer": AgentType.IMPLEMENTER,
            }.get(agent_type_str, AgentType.ANALYST)

            priority_str = subtask.get("priority", "medium").lower()
            priority = {
                "high": TaskPriority.HIGH,
                "medium": TaskPriority.MEDIUM,
                "low": TaskPriority.LOW,
            }.get(priority_str, TaskPriority.MEDIUM)

            task = Task(
                id=subtask.get("id", f"task_{len(tasks)+1}"),
                description=subtask.get("description", ""),
                agent_type=agent_type,
                inputs=subtask.get("inputs", {}),
                expected_output=subtask.get("expected_output", ""),
                priority=priority,
                dependencies=subtask.get("dependencies", []),
            )
            tasks.append(task)
            self.tasks[task.id] = task

        # Parse phases
        phases_data = plan_data.get("phases", [[t.id for t in tasks]])
        phases = []
        for phase_ids in phases_data:
            phase_tasks = [self.tasks[tid] for tid in phase_ids if tid in self.tasks]
            if phase_tasks:
                phases.append(phase_tasks)

        # If no phases specified, run all tasks sequentially
        if not phases:
            phases = [[t] for t in tasks]

        plan = ExecutionPlan(
            phases=phases,
            integration_strategy=plan_data.get(
                "integration_strategy", "Combine all results"
            ),
        )

        return tasks, plan

    def _build_context(self, task: Task) -> str:
        """Build context string from completed dependency tasks."""
        if not task.dependencies:
            return "No previous context available."

        context_parts = []
        for dep_id in task.dependencies:
            if dep_id in self.context:
                dep_task = self.tasks.get(dep_id)
                dep_name = dep_task.description if dep_task else dep_id
                context_parts.append(f"### From {dep_name}:\n{self.context[dep_id]}")

        if not context_parts:
            return "No previous context available."

        return "\n\n".join(context_parts)

    def _execute_task(self, task: Task) -> Task:
        """Execute a single agent task."""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        desc_preview = task.description[:50] if task.description else "(no description)"
        self._log(
            f"Starting task '{task.id}' ({task.agent_type.value}): {desc_preview}..."
        )

        try:
            # Get the appropriate prompt template
            prompt_template = AGENT_PROMPTS.get(task.agent_type)
            if not prompt_template:
                raise ValueError(
                    f"No prompt template for agent type: {task.agent_type}"
                )

            # Build the prompt - use safe substitution to avoid format string errors
            context = self._build_context(task)
            inputs_str = (
                json.dumps(task.inputs, indent=2) if task.inputs else "None specified"
            )

            # Replace placeholders manually to avoid issues with curly braces in content
            prompt = prompt_template
            prompt = prompt.replace("{task_description}", task.description or "")
            prompt = prompt.replace("{context}", context)
            prompt = prompt.replace("{inputs}", inputs_str)

            # Call the LLM
            result = self._call_llm(prompt)

            # Store result
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = (
                datetime.now()
            )  # Set completion time BEFORE logging duration
            task.confidence = 0.8  # Default confidence; could parse from response

            # Add to accumulated context
            self.context[task.id] = result

            duration = task.duration_seconds or 0.0
            self._log(f"Completed task '{task.id}' ({duration:.1f}s)")

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()
            self._log(f"Failed task '{task.id}': {e}")

        return task

    def _execute_phase(self, phase: List[Task]) -> List[Task]:
        """Execute all tasks in a phase (potentially in parallel)."""
        if len(phase) == 1:
            # Single task - execute directly
            return [self._execute_task(phase[0])]

        # Multiple tasks - execute in parallel
        results = []
        with ThreadPoolExecutor(
            max_workers=min(len(phase), self.max_parallel)
        ) as executor:
            futures = {
                executor.submit(self._execute_task, task): task for task in phase
            }
            for future in as_completed(futures):
                results.append(future.result())

        return results

    def _integrate_results(self, task_description: str, plan: ExecutionPlan) -> str:
        """Integrate all agent results into a final output."""
        self._log("Integrating results from all agents...")

        # Build agent results summary
        results_parts = []
        for task_id, task in self.tasks.items():
            if task.status == TaskStatus.COMPLETED and task.result:
                results_parts.append(
                    f"### {task.agent_type.value.title()} Agent - {task.description}\n"
                    f"{task.result}"
                )

        agent_results = "\n\n---\n\n".join(results_parts)

        # Call integration prompt
        prompt = INTEGRATION_PROMPT.format(
            task_description=task_description,
            integration_strategy=plan.integration_strategy,
            agent_results=agent_results,
        )

        return self._call_llm(prompt)

    def run(self, task_description: str) -> OrchestratorResult:
        """Execute a complete multi-agent workflow.

        Args:
            task_description: The complex task to orchestrate

        Returns:
            OrchestratorResult with final output and all agent results
        """
        start_time = datetime.now()
        self._log(f"Starting multi-agent workflow for: {task_description[:100]}...")

        # Phase 1: Orchestrator decomposes the task
        self._log("Phase 1: Task decomposition...")
        orchestrator_prompt = ORCHESTRATOR_PROMPT.format(
            task_description=task_description
        )
        orchestrator_response = self._call_llm(
            orchestrator_prompt,
            system="You are a task orchestrator. Output only valid JSON.",
        )

        # Parse the execution plan
        tasks, plan = self._parse_plan(orchestrator_response)
        self._log(f"Created {len(tasks)} subtasks in {len(plan.phases)} phases")

        # Phase 2: Execute tasks by phase
        for i, phase in enumerate(plan.phases):
            self._log(
                f"Phase {i+1}/{len(plan.phases)}: Executing {len(phase)} task(s)..."
            )
            self._execute_phase(phase)

        # Phase 3: Integrate results
        final_output = self._integrate_results(task_description, plan)

        # Build result
        end_time = datetime.now()
        result = OrchestratorResult(
            task_description=task_description,
            plan=plan,
            agent_results=self.tasks,
            final_output=final_output,
            total_duration_seconds=(end_time - start_time).total_seconds(),
            metadata={
                "model": self.model,
                "temperature": self.temperature,
                "num_tasks": len(tasks),
                "num_phases": len(plan.phases),
                "successful_tasks": sum(
                    1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED
                ),
                "failed_tasks": sum(
                    1 for t in self.tasks.values() if t.status == TaskStatus.FAILED
                ),
            },
        )

        self._log(f"Workflow complete in {result.total_duration_seconds:.1f}s")
        return result


# =============================================================================
# CLI
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Orchestrator - Execute complex tasks with coordinated AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (uses GitHub Models gpt-4o-mini by default)
  python -m tools.agents.multi_agent_orchestrator "Design a REST API for a todo app"
  
  # Use local model
  python -m tools.agents.multi_agent_orchestrator --model local:phi4 "Your task"
  
  # Verbose output with custom temperature
  python -m tools.agents.multi_agent_orchestrator -v --temperature 0.5 "Your task"
  
  # Output as JSON
  python -m tools.agents.multi_agent_orchestrator --json "Your task"
        """,
    )
    parser.add_argument(
        "task",
        type=str,
        help="The complex task to orchestrate",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="gh:gpt-4o-mini",
        help="Model to use (e.g., 'gh:gpt-4o-mini', 'local:phi4', 'openai:gpt-4')",
    )
    parser.add_argument(
        "--temperature",
        "-t",
        type=float,
        default=0.7,
        help="Sampling temperature (0.0-2.0, default: 0.7)",
    )
    parser.add_argument(
        "--max-parallel",
        "-p",
        type=int,
        default=3,
        help="Maximum parallel agent executions (default: 3)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed progress information",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON",
    )

    args = parser.parse_args()

    # Create orchestrator
    orchestrator = MultiAgentOrchestrator(
        model=args.model,
        temperature=args.temperature,
        max_parallel=args.max_parallel,
        verbose=args.verbose,
    )

    # Run the workflow
    try:
        result = orchestrator.run(args.task)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.json:
        # Convert to JSON-serializable format
        output = {
            "task_description": result.task_description,
            "final_output": result.final_output,
            "total_duration_seconds": result.total_duration_seconds,
            "metadata": result.metadata,
            "tasks": {
                tid: {
                    "description": t.description,
                    "agent_type": t.agent_type.value,
                    "status": t.status.value,
                    "result": t.result,
                    "duration_seconds": t.duration_seconds,
                }
                for tid, t in result.agent_results.items()
            },
        }
        print(json.dumps(output, indent=2))
    else:
        print("\n" + "=" * 80)
        print("MULTI-AGENT WORKFLOW RESULT")
        print("=" * 80)
        print(f"\nTask: {result.task_description}")
        print(f"Duration: {result.total_duration_seconds:.1f}s")
        print(
            f"Tasks: {result.metadata['successful_tasks']}/{result.metadata['num_tasks']} successful"
        )
        print("\n" + "-" * 80)
        print("FINAL OUTPUT:")
        print("-" * 80)
        print(result.final_output)


if __name__ == "__main__":
    main()
