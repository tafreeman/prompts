#!/usr/bin/env python3
"""
Agentic Workflow Runner & Evaluator
====================================

Executes agentic workflows from JSON configurations and evaluates them
using the Code Grading workflow as an LLM-based scoring system.

This integrates:
- The 4 agentic workflow configurations from workflows/agentic_planning/
- The existing benchmarks infrastructure (datasets, runner, llm_evaluator)
- A multi-agent orchestration loop

Usage:
    # Run a single workflow
    python workflow_runner.py --workflow end_to_end --task "Build a TODO app"

    # Run evaluation benchmark
    python workflow_runner.py --benchmark workflow-eval --model gh:openai/gpt-4o

    # Run with the code grading workflow as evaluator
    python workflow_runner.py --workflow defect_resolution --task "Fix bug #123" --evaluate
"""

import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

WORKFLOW_CONFIGS_DIR = (
    Path(__file__).parents[2] / "workflows" / "agentic_planning" / "configs"
)
BENCHMARK_OUTPUT_DIR = Path(__file__).parent / "benchmark_runs"

# Default model for orchestration (can be overridden per-agent)
DEFAULT_ORCHESTRATOR_MODEL = "gh:openai/gpt-4o"

# Evaluation model (from the Code Grading workflow)
DEFAULT_EVALUATOR_MODEL = "gh:openai/gpt-4o"

# Available workflows
WORKFLOW_CONFIGS = {
    "end_to_end": "workflow_end_to_end.json",
    "defect_resolution": "workflow_defect_resolution.json",
    "system_design": "workflow_system_design.json",
    "code_grading": "workflow_code_grading.json",
}


# =============================================================================
# DATA STRUCTURES
# =============================================================================


class AgentStatus(Enum):
    """Status of an agent's execution."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class AgentConfig:
    """Configuration for a single agent."""

    id: str
    name: str
    model: str
    role: str
    output_format: str
    phase: str
    system_prompt: str
    temperature: float = 0.7
    max_tokens: int = 4096
    compatible_models: List[str] = field(default_factory=list)
    tier: str = "cloud_std"
    why: str = ""


@dataclass
class AgentResult:
    """Result from an agent's execution."""

    agent_id: str
    agent_name: str
    model_used: str
    status: AgentStatus
    output: str = ""
    error: Optional[str] = None
    duration_seconds: float = 0.0
    input_context: str = ""
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "model_used": self.model_used,
            "status": self.status.value,
            "output": self.output,
            "error": self.error,
            "duration_seconds": self.duration_seconds,
            "timestamp": self.timestamp,
        }


@dataclass
class WorkflowResult:
    """Complete workflow execution result."""

    workflow_name: str
    task_description: str
    phases: List[str]
    agent_results: Dict[str, AgentResult]
    final_output: str = ""
    total_duration_seconds: float = 0.0
    evaluation_score: Optional[float] = None
    evaluation_grade: Optional[str] = None
    evaluation_details: Optional[Dict[str, Any]] = None
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_name": self.workflow_name,
            "task_description": self.task_description,
            "phases": self.phases,
            "agent_results": {k: v.to_dict() for k, v in self.agent_results.items()},
            "final_output": self.final_output,
            "total_duration_seconds": self.total_duration_seconds,
            "evaluation_score": self.evaluation_score,
            "evaluation_grade": self.evaluation_grade,
            "evaluation_details": self.evaluation_details,
            "timestamp": self.timestamp,
        }


# =============================================================================
# WORKFLOW LOADER
# =============================================================================


def load_workflow_config(workflow_name: str) -> Dict[str, Any]:
    """Load a workflow configuration from JSON."""
    if workflow_name not in WORKFLOW_CONFIGS:
        raise ValueError(
            f"Unknown workflow: {workflow_name}. Available: {list(WORKFLOW_CONFIGS.keys())}"
        )

    config_file = WORKFLOW_CONFIGS_DIR / WORKFLOW_CONFIGS[workflow_name]

    if not config_file.exists():
        raise FileNotFoundError(f"Workflow config not found: {config_file}")

    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_agents(config: Dict[str, Any]) -> List[AgentConfig]:
    """Parse agent configurations from workflow config."""
    agents = []
    for agent_data in config.get("agents", []):
        agents.append(
            AgentConfig(
                id=agent_data["id"],
                name=agent_data["name"],
                model=agent_data["model"],
                role=agent_data["role"],
                output_format=agent_data.get("output_format", ""),
                phase=agent_data.get("phase", ""),
                system_prompt=agent_data.get("system_prompt", ""),
                temperature=agent_data.get("temperature", 0.7),
                max_tokens=agent_data.get("max_tokens", 4096),
                compatible_models=agent_data.get("compatible_models", []),
                tier=agent_data.get("tier", "cloud_std"),
                why=agent_data.get("why", ""),
            )
        )
    return agents


def group_agents_by_phase(
    agents: List[AgentConfig], phases: List[str]
) -> Dict[str, List[AgentConfig]]:
    """Group agents by their phase."""
    grouped = {phase: [] for phase in phases}
    for agent in agents:
        phase = agent.phase.lower()
        if phase in grouped:
            grouped[phase].append(agent)
        else:
            # Add to first available phase if unknown
            grouped[phases[0]].append(agent)
    return grouped


# =============================================================================
# EXECUTION ENGINE
# =============================================================================


class WorkflowExecutor:
    """Executes a multi-agent workflow."""

    def __init__(
        self,
        model_override: Optional[str] = None,
        verbose: bool = False,
        use_fallback: bool = True,
    ):
        self.model_override = model_override
        self.verbose = verbose
        self.use_fallback = use_fallback
        self._llm_client = None

    @property
    def llm_client(self):
        """Lazy load LLM client."""
        if self._llm_client is None:
            # Add parent to path for imports
            sys.path.insert(0, str(Path(__file__).parents[2]))
            from tools.llm.llm_client import LLMClient

            self._llm_client = LLMClient
        return self._llm_client

    def _log(self, message: str):
        """Print if verbose mode is enabled."""
        if self.verbose:
            print(f"  [Executor] {message}")

    def _select_model(self, agent: AgentConfig) -> str:
        """Select the model to use for an agent."""
        if self.model_override:
            return self.model_override
        return agent.model

    def _build_agent_prompt(
        self,
        agent: AgentConfig,
        task_description: str,
        previous_outputs: Dict[str, str],
    ) -> str:
        """Build the prompt for an agent including context from previous
        agents."""

        context_parts = []

        if previous_outputs:
            context_parts.append("## CONTEXT FROM PREVIOUS AGENTS\n")
            for agent_id, output in previous_outputs.items():
                # Truncate long outputs
                truncated = output[:3000] + "..." if len(output) > 3000 else output
                context_parts.append(f"### {agent_id}\n{truncated}\n")

        context = "\n".join(context_parts)

        prompt = f"""# TASK
{task_description}

{context}

# YOUR ROLE: {agent.name}
{agent.role}

# EXPECTED OUTPUT FORMAT
{agent.output_format}

# INSTRUCTIONS
Using the context provided, perform your role and produce the expected output.
Be specific, detailed, and actionable.
"""
        return prompt

    def _execute_agent(
        self,
        agent: AgentConfig,
        task_description: str,
        previous_outputs: Dict[str, str],
    ) -> AgentResult:
        """Execute a single agent."""
        agent_id = agent.id
        start_time = datetime.now()

        self._log(f"Starting agent: {agent.name} ({agent.id})")

        try:
            model = self._select_model(agent)
            prompt = self._build_agent_prompt(agent, task_description, previous_outputs)

            self._log(f"  Model: {model}")
            self._log(f"  Prompt length: {len(prompt)} chars")

            # Call LLM
            response = self.llm_client.generate_text(
                model,
                prompt,
                system_instruction=agent.system_prompt,
                temperature=agent.temperature,
                max_tokens=agent.max_tokens,
            )

            duration = (datetime.now() - start_time).total_seconds()
            self._log(f"  Completed in {duration:.1f}s")

            return AgentResult(
                agent_id=agent_id,
                agent_name=agent.name,
                model_used=model,
                status=AgentStatus.COMPLETED,
                output=response,
                duration_seconds=duration,
                input_context=prompt[:500],
                timestamp=datetime.now().isoformat(),
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            self._log(f"  FAILED: {str(e)}")

            # Try fallback model if enabled
            if self.use_fallback and agent.compatible_models:
                self._log(f"  Trying fallback model: {agent.compatible_models[0]}")
                try:
                    fallback_model = agent.compatible_models[0]
                    prompt = self._build_agent_prompt(
                        agent, task_description, previous_outputs
                    )

                    response = self.llm_client.generate_text(
                        fallback_model,
                        prompt,
                        system=agent.system_prompt,
                        temperature=agent.temperature,
                        max_tokens=agent.max_tokens,
                    )

                    duration = (datetime.now() - start_time).total_seconds()

                    return AgentResult(
                        agent_id=agent_id,
                        agent_name=agent.name,
                        model_used=fallback_model,
                        status=AgentStatus.COMPLETED,
                        output=response,
                        duration_seconds=duration,
                        input_context=prompt[:500],
                        timestamp=datetime.now().isoformat(),
                    )
                except Exception as fallback_error:
                    return AgentResult(
                        agent_id=agent_id,
                        agent_name=agent.name,
                        model_used=agent.model,
                        status=AgentStatus.FAILED,
                        error=f"Primary: {str(e)}, Fallback: {str(fallback_error)}",
                        duration_seconds=duration,
                        timestamp=datetime.now().isoformat(),
                    )

            return AgentResult(
                agent_id=agent_id,
                agent_name=agent.name,
                model_used=agent.model,
                status=AgentStatus.FAILED,
                error=str(e),
                duration_seconds=duration,
                timestamp=datetime.now().isoformat(),
            )

    def _synthesize_final_output(
        self,
        workflow_name: str,
        task_description: str,
        agent_results: Dict[str, AgentResult],
    ) -> str:
        """Synthesize a final output from all agent results."""
        outputs = []
        for agent_id, result in agent_results.items():
            if result.status == AgentStatus.COMPLETED:
                outputs.append(f"## {result.agent_name}\n{result.output}\n")

        # Could use an LLM to synthesize, but for now just concatenate
        return (
            f"# {workflow_name} Results\n\n**Task:** {task_description}\n\n"
            + "\n".join(outputs)
        )

    def run(
        self,
        workflow_name: str,
        task_description: str,
    ) -> WorkflowResult:
        """Execute a complete workflow.

        Args:
            workflow_name: One of the available workflows (end_to_end, defect_resolution, etc.)
            task_description: The task to execute

        Returns:
            WorkflowResult with all agent outputs and final synthesis
        """
        start_time = datetime.now()

        print(f"\n{'='*60}")
        print(f"EXECUTING WORKFLOW: {workflow_name}")
        print(f"{'='*60}\n")

        # Load configuration
        config = load_workflow_config(workflow_name)
        agents = parse_agents(config)
        phases = config.get("metadata", {}).get("phases", ["default"])
        phases_lower = [p.lower() for p in phases]

        print(f"Workflow: {config.get('description', workflow_name)}")
        print(f"Version: {config.get('version', '1.0')}")
        print(f"Agents: {len(agents)}")
        print(f"Phases: {phases}")
        print(f"Task: {task_description[:100]}...")
        print()

        # Group agents by phase
        agents_by_phase = group_agents_by_phase(agents, phases_lower)

        # Execute phase by phase
        agent_results: Dict[str, AgentResult] = {}
        previous_outputs: Dict[str, str] = {}

        for phase in phases_lower:
            phase_agents = agents_by_phase.get(phase, [])
            if not phase_agents:
                continue

            print(f"\n--- Phase: {phase.upper()} ({len(phase_agents)} agents) ---")

            for agent in phase_agents:
                result = self._execute_agent(agent, task_description, previous_outputs)
                agent_results[agent.id] = result

                # Add successful output to context for next agents
                if result.status == AgentStatus.COMPLETED:
                    previous_outputs[agent.id] = result.output

                # Print status
                status_icon = "✓" if result.status == AgentStatus.COMPLETED else "✗"
                print(
                    f"  {status_icon} {agent.name}: {result.status.value} ({result.duration_seconds:.1f}s)"
                )

        # Synthesize final output
        final_output = self._synthesize_final_output(
            workflow_name, task_description, agent_results
        )

        total_duration = (datetime.now() - start_time).total_seconds()

        print(f"\n{'='*60}")
        print(f"WORKFLOW COMPLETED in {total_duration:.1f}s")
        print(f"{'='*60}\n")

        return WorkflowResult(
            workflow_name=workflow_name,
            task_description=task_description,
            phases=phases,
            agent_results=agent_results,
            final_output=final_output,
            total_duration_seconds=total_duration,
            timestamp=datetime.now().isoformat(),
        )


# =============================================================================
# WORKFLOW EVALUATOR (Using Code Grading Workflow)
# =============================================================================


class WorkflowEvaluator:
    """Evaluates workflow outputs using the Code Grading workflow agents.

    This creates a meta-evaluation: the Code Grading workflow scores
    the output of other workflows.
    """

    def __init__(
        self,
        evaluator_model: str = DEFAULT_EVALUATOR_MODEL,
        verbose: bool = False,
    ):
        self.evaluator_model = evaluator_model
        self.verbose = verbose
        self._llm_client = None

    @property
    def llm_client(self):
        if self._llm_client is None:
            sys.path.insert(0, str(Path(__file__).parents[2]))
            from tools.llm.llm_client import LLMClient

            self._llm_client = LLMClient
        return self._llm_client

    def evaluate(
        self,
        workflow_result: WorkflowResult,
        gold_standard: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Evaluate a workflow result using the grading workflow's dimensions.

        Uses the same scoring rubric from llm_evaluator.py (0.0-10.0
        scale) with workflow-specific dimensions.
        """
        # Load grading workflow config for reference
        grading_config = load_workflow_config("code_grading")

        # Build evaluation prompt using the Head Judge's perspective
        eval_prompt = self._build_eval_prompt(workflow_result, gold_standard)

        if self.verbose:
            print(
                f"  [Evaluator] Evaluating {workflow_result.workflow_name} with {self.evaluator_model}"
            )

        try:
            response = self.llm_client.generate_text(
                self.evaluator_model,
                eval_prompt,
                max_tokens=2000,
            )

            # Parse the evaluation response
            result = self._parse_eval_response(response)
            return result

        except Exception as e:
            if self.verbose:
                print(f"  [Evaluator] Error: {e}")
            return {
                "overall_score": 0.0,
                "grade": "F",
                "error": str(e),
            }

    def _build_eval_prompt(
        self,
        workflow_result: WorkflowResult,
        gold_standard: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build evaluation prompt for workflow output."""

        # Summarize agent outputs
        agent_summary = []
        for agent_id, result in workflow_result.agent_results.items():
            if result.status == AgentStatus.COMPLETED:
                output_preview = (
                    result.output[:500] + "..."
                    if len(result.output) > 500
                    else result.output
                )
                agent_summary.append(f"### {result.agent_name}\n{output_preview}")

        agent_outputs = "\n\n".join(agent_summary)

        gold_info = ""
        if gold_standard:
            gold_info = f"""
## GOLD STANDARD EXPECTATIONS
{json.dumps(gold_standard, indent=2)[:2000]}
"""

        return f"""You are an expert workflow evaluator. Evaluate the following multi-agent workflow execution.

## WORKFLOW
Name: {workflow_result.workflow_name}
Task: {workflow_result.task_description}
Phases: {workflow_result.phases}
Agents Run: {len(workflow_result.agent_results)}
Duration: {workflow_result.total_duration_seconds:.1f}s

{gold_info}

## AGENT OUTPUTS
{agent_outputs}

## EVALUATION DIMENSIONS (0.0-10.0 scale)
1. **Completeness** (25%): Did all agents contribute meaningful output?
2. **Correctness** (25%): Is the output technically accurate and follows best practices?
3. **Quality** (20%): Is the output well-structured and actionable?
4. **Coherence** (15%): Do the agent outputs work together cohesively?
5. **Value** (15%): Does the final output provide real value for the task?

## SCORING RUBRIC
10.0: Perfect - Flawless execution
8.0-9.0: Excellent - Production-ready quality
6.0-7.0: Good - Solid with minor improvements needed
4.0-5.0: Fair - Significant gaps, needs work
0.0-3.0: Poor - Major deficiencies

## OUTPUT FORMAT (respond with valid JSON only, no markdown):
{{
  "dimension_scores": {{
    "completeness": {{"score": <0-10>, "reasoning": "<why>"}},
    "correctness": {{"score": <0-10>, "reasoning": "<why>"}},
    "quality": {{"score": <0-10>, "reasoning": "<why>"}},
    "coherence": {{"score": <0-10>, "reasoning": "<why>"}},
    "value": {{"score": <0-10>, "reasoning": "<why>"}}
  }},
  "overall_score": <weighted average>,
  "grade": "<A/B/C/D/F>",
  "strengths": ["<strength 1>", ...],
  "weaknesses": ["<weakness 1>", ...],
  "recommendations": ["<recommendation 1>", ...]
}}"""

    def _parse_eval_response(self, response: str) -> Dict[str, Any]:
        """Parse evaluation response from LLM."""
        import re

        response = response.strip()

        # Remove markdown code blocks if present
        if response.startswith("```"):
            first_newline = response.find("\n")
            if first_newline != -1:
                response = response[first_newline + 1 :]
            if response.endswith("```"):
                response = response[:-3].strip()

        try:
            result = json.loads(response)

            # Calculate grade from score if not provided
            if "grade" not in result and "overall_score" in result:
                score = result["overall_score"]
                if score >= 9.0:
                    result["grade"] = "A"
                elif score >= 8.0:
                    result["grade"] = "B"
                elif score >= 7.0:
                    result["grade"] = "C"
                elif score >= 6.0:
                    result["grade"] = "D"
                else:
                    result["grade"] = "F"

            return result

        except json.JSONDecodeError:
            # Try to find JSON in response
            json_match = re.search(r"\{[\s\S]*\}", response)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    pass

            return {
                "overall_score": 0.0,
                "grade": "F",
                "error": "Failed to parse evaluation response",
                "raw_response": response[:500],
            }


# =============================================================================
# BENCHMARK INTEGRATION
# =============================================================================


@dataclass
class WorkflowBenchmarkTask:
    """A benchmark task for workflow evaluation."""

    task_id: str
    workflow_type: str  # end_to_end, defect_resolution, system_design, code_grading
    task_description: str
    gold_standard: Dict[str, Any]
    tags: List[str] = field(default_factory=list)


# Sample benchmark tasks for each workflow type
WORKFLOW_BENCHMARK_TASKS = [
    # End-to-End Development Tasks
    WorkflowBenchmarkTask(
        task_id="e2e_001",
        workflow_type="end_to_end",
        task_description="Build a REST API for a task management system with user authentication, CRUD operations for tasks, and due date reminders.",
        gold_standard={
            "required_components": [
                "REST API",
                "Authentication",
                "Database Schema",
                "CRUD Endpoints",
            ],
            "required_patterns": ["JWT Auth", "Repository Pattern", "Error Handling"],
            "expected_output": "Complete API specification with endpoints, schema, and security design",
        },
        tags=["api", "full-stack", "medium"],
    ),
    WorkflowBenchmarkTask(
        task_id="e2e_002",
        workflow_type="end_to_end",
        task_description="Design and implement a real-time chat application with WebSocket support, message history, and user presence indicators.",
        gold_standard={
            "required_components": [
                "WebSocket Server",
                "Message Queue",
                "User Presence",
                "History Storage",
            ],
            "required_patterns": ["Pub/Sub", "Event-Driven", "Connection Pooling"],
            "expected_output": "Architecture design, API contracts, and implementation plan",
        },
        tags=["real-time", "full-stack", "hard"],
    ),
    # Defect Resolution Tasks
    WorkflowBenchmarkTask(
        task_id="defect_001",
        workflow_type="defect_resolution",
        task_description="Debug a memory leak in a Node.js application that occurs after 24 hours of operation. The heap grows from 100MB to 2GB.",
        gold_standard={
            "required_components": ["Root Cause Analysis", "Memory Profiling", "Patch"],
            "key_decisions": [
                "Memory leak source identified",
                "Fix verified",
                "Regression tests added",
            ],
            "expected_output": "Root cause document, patch, and verification report",
        },
        tags=["memory", "nodejs", "performance"],
    ),
    WorkflowBenchmarkTask(
        task_id="defect_002",
        workflow_type="defect_resolution",
        task_description="Fix a race condition in a multi-threaded Python application causing intermittent data corruption in the database.",
        gold_standard={
            "required_components": [
                "Reproduction Script",
                "Thread Analysis",
                "Synchronization Fix",
            ],
            "key_decisions": [
                "Race condition identified",
                "Locking strategy chosen",
                "Tests added",
            ],
            "expected_output": "Detailed analysis, fix implementation, and concurrency tests",
        },
        tags=["concurrency", "python", "database"],
    ),
    # System Design Tasks
    WorkflowBenchmarkTask(
        task_id="design_001",
        workflow_type="system_design",
        task_description="Design a scalable e-commerce platform that handles 1 million daily active users with a product catalog of 10 million items.",
        gold_standard={
            "required_components": [
                "Microservices Architecture",
                "Database Design",
                "Caching Strategy",
                "CDN",
            ],
            "required_patterns": ["Event Sourcing", "CQRS", "Circuit Breaker"],
            "expected_output": "Complete architecture document with diagrams and trade-off analysis",
        },
        tags=["scale", "e-commerce", "hard"],
    ),
    # Code Grading Tasks
    WorkflowBenchmarkTask(
        task_id="grading_001",
        workflow_type="code_grading",
        task_description="Grade the following Python implementation of a binary search tree with insert, delete, and search operations.",
        gold_standard={
            "required_components": [
                "Correctness Check",
                "Performance Analysis",
                "Code Quality Review",
            ],
            "key_decisions": ["Algorithm correctness", "Time complexity", "Code style"],
            "expected_output": "Detailed grade report with scores and improvement suggestions",
        },
        tags=["algorithms", "python", "grading"],
    ),
]


def get_benchmark_tasks(
    workflow_type: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> List[WorkflowBenchmarkTask]:
    """Get benchmark tasks with optional filtering."""
    tasks = WORKFLOW_BENCHMARK_TASKS

    if workflow_type:
        tasks = [t for t in tasks if t.workflow_type == workflow_type]

    if tags:
        tasks = [t for t in tasks if any(tag in t.tags for tag in tags)]

    return tasks


# =============================================================================
# CLI
# =============================================================================


def main():
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Run and evaluate agentic workflows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--workflow",
        choices=list(WORKFLOW_CONFIGS.keys()),
        help="Workflow to run",
    )
    parser.add_argument(
        "--task",
        type=str,
        help="Task description to execute",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Override model for all agents (e.g., 'gh:openai/gpt-4o')",
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Evaluate the workflow output using the grading workflow",
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run benchmark evaluation on all workflow tasks",
    )
    parser.add_argument(
        "--benchmark-type",
        choices=list(WORKFLOW_CONFIGS.keys()),
        help="Filter benchmark tasks by workflow type",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to save results",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output",
    )
    parser.add_argument(
        "--list-workflows",
        action="store_true",
        help="List available workflows and exit",
    )
    parser.add_argument(
        "--list-tasks",
        action="store_true",
        help="List available benchmark tasks and exit",
    )

    args = parser.parse_args()

    # List workflows
    if args.list_workflows:
        print("\nAvailable Workflows:")
        print("-" * 60)
        for name, filename in WORKFLOW_CONFIGS.items():
            try:
                config = load_workflow_config(name)
                desc = config.get("description", "No description")
                agents = len(config.get("agents", []))
                print(f"  {name:20} - {desc[:40]} ({agents} agents)")
            except:
                print(f"  {name:20} - (config not found)")
        return

    # List benchmark tasks
    if args.list_tasks:
        print("\nBenchmark Tasks:")
        print("-" * 60)
        for task in WORKFLOW_BENCHMARK_TASKS:
            print(f"  [{task.task_id}] {task.workflow_type}")
            print(f"      {task.task_description[:60]}...")
            print(f"      Tags: {', '.join(task.tags)}")
            print()
        return

    # Run benchmark
    if args.benchmark:
        run_benchmark(
            workflow_type=args.benchmark_type,
            model=args.model,
            output_dir=args.output_dir,
            verbose=args.verbose,
        )
        return

    # Run single workflow
    if args.workflow and args.task:
        run_single_workflow(
            workflow_name=args.workflow,
            task_description=args.task,
            model=args.model,
            evaluate=args.evaluate,
            output_dir=args.output_dir,
            verbose=args.verbose,
        )
        return

    # Interactive mode
    interactive_mode(verbose=args.verbose)


def run_single_workflow(
    workflow_name: str,
    task_description: str,
    model: Optional[str] = None,
    evaluate: bool = False,
    output_dir: Optional[str] = None,
    verbose: bool = False,
):
    """Run a single workflow with optional evaluation."""
    executor = WorkflowExecutor(
        model_override=model,
        verbose=verbose,
    )

    result = executor.run(workflow_name, task_description)

    if evaluate:
        print("\n--- Evaluating Workflow Output ---")
        evaluator = WorkflowEvaluator(verbose=verbose)
        eval_result = evaluator.evaluate(result)

        result.evaluation_score = eval_result.get("overall_score", 0.0)
        result.evaluation_grade = eval_result.get("grade", "F")
        result.evaluation_details = eval_result

        print(
            f"\nEvaluation Score: {result.evaluation_score:.1f}/10.0 (Grade: {result.evaluation_grade})"
        )

        if "strengths" in eval_result:
            print("\nStrengths:")
            for s in eval_result["strengths"][:3]:
                print(f"  + {s}")

        if "weaknesses" in eval_result:
            print("\nWeaknesses:")
            for w in eval_result["weaknesses"][:3]:
                print(f"  - {w}")

    # Save results
    if output_dir:
        output_path = Path(output_dir)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = BENCHMARK_OUTPUT_DIR / f"{workflow_name}_{timestamp}"

    output_path.mkdir(parents=True, exist_ok=True)

    # Save JSON
    with open(output_path / "result.json", "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, indent=2)

    # Save final output as markdown
    with open(output_path / "final_output.md", "w", encoding="utf-8") as f:
        f.write(result.final_output)

    print(f"\nResults saved to: {output_path}")


def run_benchmark(
    workflow_type: Optional[str] = None,
    model: Optional[str] = None,
    output_dir: Optional[str] = None,
    verbose: bool = False,
):
    """Run benchmark evaluation on workflow tasks."""
    tasks = get_benchmark_tasks(workflow_type=workflow_type)

    print(f"\n{'='*60}")
    print("WORKFLOW BENCHMARK")
    print(f"{'='*60}")
    print(f"Tasks: {len(tasks)}")
    print(f"Model: {model or 'per-agent defaults'}")
    print()

    results = []
    executor = WorkflowExecutor(model_override=model, verbose=verbose)
    evaluator = WorkflowEvaluator(verbose=verbose)

    for task in tasks:
        print(f"\n--- Task: {task.task_id} ({task.workflow_type}) ---")

        try:
            result = executor.run(task.workflow_type, task.task_description)
            eval_result = evaluator.evaluate(result, task.gold_standard)

            result.evaluation_score = eval_result.get("overall_score", 0.0)
            result.evaluation_grade = eval_result.get("grade", "F")
            result.evaluation_details = eval_result

            print(
                f"Score: {result.evaluation_score:.1f}/10.0 (Grade: {result.evaluation_grade})"
            )

            results.append(
                {
                    "task_id": task.task_id,
                    "workflow_type": task.workflow_type,
                    "score": result.evaluation_score,
                    "grade": result.evaluation_grade,
                    "duration": result.total_duration_seconds,
                }
            )

        except Exception as e:
            print(f"FAILED: {e}")
            results.append(
                {
                    "task_id": task.task_id,
                    "workflow_type": task.workflow_type,
                    "score": 0.0,
                    "grade": "F",
                    "error": str(e),
                }
            )

    # Summary
    print(f"\n{'='*60}")
    print("BENCHMARK SUMMARY")
    print(f"{'='*60}")

    scores = [r["score"] for r in results if "error" not in r]
    if scores:
        avg_score = sum(scores) / len(scores)
        print(f"Average Score: {avg_score:.1f}/10.0")
        print(
            f"Tasks Passed (≥7.0): {sum(1 for s in scores if s >= 7.0)}/{len(scores)}"
        )

    # Save benchmark results
    if output_dir:
        output_path = Path(output_dir)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = BENCHMARK_OUTPUT_DIR / f"benchmark_{timestamp}"

    output_path.mkdir(parents=True, exist_ok=True)

    with open(output_path / "benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "model": model,
                "tasks": results,
                "summary": {
                    "total_tasks": len(results),
                    "average_score": avg_score if scores else 0.0,
                    "passed": sum(1 for s in scores if s >= 7.0) if scores else 0,
                },
            },
            f,
            indent=2,
        )

    print(f"\nResults saved to: {output_path}")


def interactive_mode(verbose: bool = False):
    """Interactive workflow selection and execution."""
    print("\n" + "=" * 60)
    print("AGENTIC WORKFLOW RUNNER")
    print("=" * 60)

    # Select workflow
    print("\nAvailable Workflows:")
    workflows = list(WORKFLOW_CONFIGS.keys())
    for i, wf in enumerate(workflows, 1):
        print(f"  {i}. {wf}")

    try:
        choice = int(input("\nSelect workflow (number): ")) - 1
        if 0 <= choice < len(workflows):
            workflow_name = workflows[choice]
        else:
            print("Invalid choice")
            return
    except ValueError:
        print("Invalid input")
        return

    # Get task description
    task = input("\nEnter task description: ").strip()
    if not task:
        print("Task description required")
        return

    # Ask about evaluation
    evaluate = input("Evaluate output? (y/n): ").strip().lower() == "y"

    # Run
    run_single_workflow(
        workflow_name=workflow_name,
        task_description=task,
        evaluate=evaluate,
        verbose=verbose,
    )


if __name__ == "__main__":
    main()
