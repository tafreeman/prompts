#!/usr/bin/env python3
"""
Benchmark Runner - Interactive CLI
==================================

Interactive command-line interface for running multi-agent benchmarks.
Supports dataset, model, and workflow selection.

Usage:
    # Interactive mode
    python -m tools.agents.benchmarks.runner

    # Direct mode with arguments
    python -m tools.agents.benchmarks.runner --benchmark humaneval --model gh:gpt-4o-mini --limit 5

    # Use preset configuration
    python -m tools.agents.benchmarks.runner --preset quick-test
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add parent directory to path for imports
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parents[3]))

from tools.agents.benchmarks.datasets import BENCHMARK_DEFINITIONS
from tools.agents.benchmarks.loader import BenchmarkTask, clear_cache, load_benchmark
from tools.agents.benchmarks.registry import (
    PRESET_CONFIGS,
    BenchmarkConfig,
    BenchmarkRegistry,
)

# Import gold standard evaluation (legacy pattern-matching)
try:
    from tools.agents.test_tasks import (
        TEST_TASKS,
        evaluate_against_gold_standard,
        print_gold_standard_report,
    )

    HAS_GOLD_STANDARD = True
except ImportError:
    HAS_GOLD_STANDARD = False

# Import LLM-based evaluator (new)
try:
    from tools.agents.benchmarks.llm_evaluator import (
        EvaluationResult,
        evaluate_with_llm,
        print_evaluation_report,
        save_evaluation_report,
        summarize_batch_results,
    )

    HAS_LLM_EVALUATOR = True
except ImportError:
    HAS_LLM_EVALUATOR = False


# =============================================================================
# MODEL DISCOVERY INTEGRATION
# =============================================================================


def load_discovered_models() -> Dict[str, List[str]]:
    """Load discovered models from discovery_results.json or run discovery."""
    # Check for existing discovery results
    discovery_file = Path(__file__).parents[3] / "discovery_results.json"

    if discovery_file.exists():
        try:
            data = json.loads(discovery_file.read_text(encoding="utf-8"))
            return data.get("providers", {})
        except Exception:
            pass

    # Fall back to running discovery
    try:
        from tools.llm.model_probe import discover_all_models

        result = discover_all_models(verbose=False)
        return result.get("providers", {})
    except ImportError:
        return {}


def get_available_models_by_provider() -> Dict[str, List[str]]:
    """Get all available models grouped by provider."""
    providers = load_discovered_models()
    result = {}

    for provider_name, provider_data in providers.items():
        if isinstance(provider_data, dict):
            available = provider_data.get("available", [])
            if available:
                result[provider_name] = available

    return result


def get_flat_model_list() -> List[str]:
    """Get a flat list of all available models."""
    models = []
    for provider_models in get_available_models_by_provider().values():
        models.extend(provider_models)
    return sorted(set(models))


# =============================================================================
# DISPLAY HELPERS
# =============================================================================


def print_header(text: str, char: str = "=") -> None:
    """Print a header line."""
    print(f"\n{char * 80}")
    print(f" {text}")
    print(f"{char * 80}")


def print_table(headers: List[str], rows: List[List[str]], widths: List[int]) -> None:
    """Print a formatted table."""
    # Header
    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, widths))
    print(header_line)
    print("-" * len(header_line))

    # Rows
    for row in rows:
        print(" | ".join(str(c).ljust(w)[:w] for c, w in zip(row, widths)))


def colorize(text: str, color: str) -> str:
    """Add ANSI color codes (for terminals that support it)."""
    colors = {
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "reset": "\033[0m",
    }
    return f"{colors.get(color, '')}{text}{colors.get('reset', '')}"


# =============================================================================
# INTERACTIVE MENU SYSTEM
# =============================================================================


def prompt_choice(options: List[str], prompt: str = "Select") -> int:
    """Prompt user to select from options."""
    for i, opt in enumerate(options, 1):
        print(f"  [{i}] {opt}")

    while True:
        try:
            choice = input(f"\n{prompt} [1-{len(options)}]: ").strip()
            if choice.lower() == "q":
                return -1
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return idx
        except ValueError:
            pass
        print("Invalid choice. Try again (or 'q' to quit).")


def prompt_input(prompt: str, default: str = "") -> str:
    """Prompt for text input with default."""
    if default:
        result = input(f"{prompt} [{default}]: ").strip()
        return result if result else default
    return input(f"{prompt}: ").strip()


def prompt_yes_no(prompt: str, default: bool = True) -> bool:
    """Prompt for yes/no."""
    suffix = "[Y/n]" if default else "[y/N]"
    result = input(f"{prompt} {suffix}: ").strip().lower()
    if not result:
        return default
    return result in ("y", "yes", "1", "true")


# =============================================================================
# BENCHMARK SELECTION UI
# =============================================================================


def select_benchmark() -> Optional[str]:
    """Interactive benchmark selection."""
    print_header("SELECT BENCHMARK")

    # Group by type
    groups = {}
    for bid, bdef in BENCHMARK_DEFINITIONS.items():
        type_name = bdef.benchmark_type.value
        if type_name not in groups:
            groups[type_name] = []
        groups[type_name].append((bid, bdef))

    # Display grouped
    options = []
    for type_name, benchmarks in sorted(groups.items()):
        print(f"\n  {colorize(type_name.upper(), 'cyan')}:")
        for bid, bdef in benchmarks:
            idx = len(options) + 1
            size_str = f"~{bdef.size} tasks"
            print(f"    [{idx}] {bdef.name} ({size_str})")
            print(f"        {bdef.description[:60]}...")
            options.append(bid)

    print("\n    [q] Quit")

    choice = prompt_choice(options, "Select benchmark")
    if choice < 0:
        return None
    return options[choice]


def select_model() -> Optional[str]:
    """Interactive model selection using discovered models."""
    print_header("SELECT MODEL")

    # Load discovered models
    providers = get_available_models_by_provider()

    if not providers:
        print(colorize("  No models discovered. Run model discovery first:", "yellow"))
        print(
            "    python -m tools.llm.model_probe --discover --force -o discovery_results.json"
        )
        print()
        return prompt_input("Enter model ID manually (e.g., 'gh:gpt-4o-mini')")

    # Provider display names and recommended models
    provider_display = {
        "github_models": (
            "🌐 GitHub Models",
            ["gh:openai/gpt-4o-mini", "gh:openai/gpt-4o", "gh:microsoft/phi-4"],
        ),
        "local_onnx": (
            "💻 Local ONNX",
            ["local:phi4", "local:phi3.5", "local:mistral"],
        ),
        "ollama": (
            "🦙 Ollama",
            [
                "ollama:deepseek-r1:8b",
                "ollama:qwen2.5-coder:14b",
                "ollama:phi4-reasoning:latest",
            ],
        ),
        "ai_toolkit": (
            "🧰 AI Toolkit",
            ["aitk:phi-4-mini-instruct", "aitk:qwen2.5-coder-7b-instruct"],
        ),
    }

    all_models = []
    print()

    for provider_key, (display_name, recommended) in provider_display.items():
        if provider_key in providers:
            available = providers[provider_key]
            # Show recommended models that are actually available
            shown = [m for m in recommended if m in available][:3]
            if not shown:
                shown = available[:3]

            print(f"  {display_name} ({len(available)} available)")
            for model in shown:
                idx = len(all_models) + 1
                all_models.append(model)
                short_name = model.split(":", 1)[1] if ":" in model else model
                print(f"    [{idx}] {short_name}")
            if len(available) > 3:
                print(f"        ... +{len(available) - 3} more")
            print()

    print(f"  [{len(all_models) + 1}] Browse all models...")
    print(f"  [{len(all_models) + 2}] Enter custom model ID...")
    print("  [q] Quit")

    while True:
        try:
            choice = input(f"\nSelect model [1-{len(all_models) + 2}]: ").strip()
            if choice.lower() == "q":
                return None
            idx = int(choice) - 1
            if 0 <= idx < len(all_models):
                return all_models[idx]
            elif idx == len(all_models):
                return browse_all_models(providers)
            elif idx == len(all_models) + 1:
                return prompt_input("Enter model ID (e.g., 'gh:openai/gpt-4o')")
        except ValueError:
            pass
        print("Invalid choice.")


def browse_all_models(providers: Dict[str, List[str]]) -> Optional[str]:
    """Browse all discovered models with filtering."""
    print_header("BROWSE ALL MODELS")

    # Select provider first
    provider_names = list(providers.keys())
    print("  Select provider:")
    for i, name in enumerate(provider_names, 1):
        count = len(providers[name])
        print(f"    [{i}] {name} ({count} models)")
    print("    [a] All providers")
    print("    [q] Back")

    choice = input("\nSelect: ").strip().lower()
    if choice == "q":
        return None

    if choice == "a":
        models = get_flat_model_list()
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(provider_names):
                models = providers[provider_names[idx]]
            else:
                return None
        except ValueError:
            return None

    # Show paginated list
    page_size = 15
    page = 0

    while True:
        start = page * page_size
        end = min(start + page_size, len(models))
        page_models = models[start:end]

        print(f"\n  Models {start + 1}-{end} of {len(models)}:")
        for i, model in enumerate(page_models, start + 1):
            print(f"    [{i}] {model}")

        print("\n  [n] Next page | [p] Prev page | [#] Select | [q] Back")
        choice = input("Select: ").strip().lower()

        if choice == "q":
            return None
        elif choice == "n" and end < len(models):
            page += 1
        elif choice == "p" and page > 0:
            page -= 1
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(models):
                    return models[idx]
            except ValueError:
                pass


def select_workflow() -> Optional[str]:
    """Interactive workflow selection."""
    print_header("SELECT AGENT WORKFLOW")

    workflows = [
        (
            "multi-agent",
            "Multi-Agent Orchestrator",
            "4 specialized agents: Analyst → Researcher → Strategist → Implementer",
        ),
        (
            "single-agent",
            "Single Agent",
            "Direct LLM call without multi-agent coordination",
        ),
        (
            "chain-of-thought",
            "Chain of Thought",
            "Step-by-step reasoning with single model",
        ),
        ("react", "ReAct", "Reasoning + Acting with tool use"),
    ]

    for i, (wf_id, name, desc) in enumerate(workflows, 1):
        print(f"  [{i}] {name}")
        print(f"      {desc}")

    print("  [q] Quit")

    choice = prompt_choice([w[1] for w in workflows], "Select workflow")
    if choice < 0:
        return None
    return workflows[choice][0]


def configure_options(config: BenchmarkConfig) -> BenchmarkConfig:
    """Configure additional options."""
    print_header("CONFIGURE OPTIONS")

    # Task limit
    limit_str = prompt_input(
        "Max tasks to run (empty for all)", str(config.limit or "")
    )
    config.limit = int(limit_str) if limit_str else None

    # Verbose
    config.verbose = prompt_yes_no("Verbose output?", config.verbose)

    # Timeout
    timeout_str = prompt_input(
        "Timeout per task (seconds)", str(config.timeout_seconds)
    )
    config.timeout_seconds = int(timeout_str)

    # Save intermediate
    config.save_intermediate = prompt_yes_no("Save intermediate agent outputs?", False)

    return config


# =============================================================================
# MAIN INTERACTIVE UI
# =============================================================================


def interactive_mode() -> Optional[BenchmarkConfig]:
    """Run interactive configuration wizard."""
    print_header("MULTI-AGENT BENCHMARK RUNNER", "=")
    print("\nConfigure and run benchmarks for multi-agent coding workflows.")
    print("Press Ctrl+C at any time to cancel.\n")

    # Start with default config
    config = BenchmarkConfig()

    # Step 1: Select benchmark
    benchmark_id = select_benchmark()
    if not benchmark_id:
        return None
    config.benchmark_id = benchmark_id

    # Step 2: Select model
    model = select_model()
    if not model:
        return None
    config.model = model

    # Step 3: Select workflow
    workflow = select_workflow()
    if not workflow:
        return None
    config.workflow = workflow

    # Step 4: Additional options
    if prompt_yes_no("\nConfigure additional options?", False):
        config = configure_options(config)

    # Show summary
    print_header("CONFIGURATION SUMMARY")
    print(f"  Benchmark: {config.benchmark_id}")
    print(f"  Model:     {config.model}")
    print(f"  Workflow:  {config.workflow}")
    print(f"  Limit:     {config.limit or 'all'}")
    print(f"  Timeout:   {config.timeout_seconds}s")
    print(f"  Verbose:   {config.verbose}")

    if not prompt_yes_no("\nProceed with this configuration?", True):
        return None

    return config


def evaluate_task_output_llm(
    task: BenchmarkTask,
    output: str,
    model: str,
    benchmark_id: str,
    verbose: bool = False,
    output_dir: Optional[Path] = None,
    evaluator_model: str = None,
) -> Optional[Dict[str, Any]]:
    """Evaluate task output using LLM-based evaluation.

    Uses structured rubric scoring (0.0-10.0) with detailed reasoning.
    """
    if not HAS_LLM_EVALUATOR:
        if verbose:
            print("  [!] LLM evaluator not available, falling back to pattern matching")
        return evaluate_task_output_legacy(task, output, verbose, output_dir)

    task_id = str(task.task_id)

    # Get gold standard data
    gold_data = get_gold_standard_for_task(task)
    if not gold_data:
        if verbose:
            print(f"  [!] No gold standard found for task: {task_id}")
        # Create minimal gold standard from task data
        gold_data = {
            "expected_output": task.expected_output or "",
            "test_cases": task.test_cases or [],
        }

    # Run LLM evaluation
    eval_result = evaluate_with_llm(
        task_id=task_id,
        task_prompt=task.prompt,
        generated_output=output,
        gold_standard=gold_data,
        model=model,
        benchmark_id=benchmark_id,
        evaluator_model=evaluator_model,
        verbose=verbose,
    )

    # Print report
    if verbose:
        print_evaluation_report(eval_result, verbose=True)
    else:
        print(
            f"  Score: {eval_result.overall_score:.1f}/10.0 (Grade: {eval_result.grade})"
        )

    # Save reports
    if output_dir:
        save_evaluation_report(eval_result, output_dir)
        print(f"  Evaluation saved: task_{task_id}_eval.md")

    # Return as dict for compatibility
    return eval_result.to_dict()


def get_gold_standard_for_task(task: BenchmarkTask) -> Optional[Dict[str, Any]]:
    """Get gold standard data for a task."""
    if not HAS_GOLD_STANDARD:
        return None

    task_id = str(task.task_id)

    # Try to find matching TEST_TASKS gold standard
    for tt in TEST_TASKS:
        tt_id_str = str(tt.id)
        if task_id == tt_id_str or task_id == f"task_{tt.id:03d}":
            return tt.get_gold_standard()
        try:
            if int(task_id) == tt.id:
                return tt.get_gold_standard()
        except ValueError:
            pass

    return None


def evaluate_task_output_legacy(
    task: BenchmarkTask,
    output: str,
    verbose: bool = False,
    output_dir: Optional[Path] = None,
) -> Optional[Dict[str, Any]]:
    """Legacy pattern-matching evaluation (fallback)."""
    if not HAS_GOLD_STANDARD:
        return None

    task_id = str(task.task_id)

    # Try to find matching gold standard
    gold_task = None
    for tt in TEST_TASKS:
        tt_id_str = str(tt.id)
        # Match by task ID (numeric or formatted)
        if task_id == tt_id_str or task_id == f"task_{tt.id:03d}":
            gold_task = tt
            break
        # Match by numeric ID
        try:
            if int(task_id) == tt.id:
                gold_task = tt
                break
        except ValueError:
            pass

    if not gold_task:
        if verbose:
            print(f"  [!] No gold standard found for task: {task_id}")
        return None

    # Get gold standard data
    gold_data = gold_task.get_gold_standard()
    if not gold_data:
        if verbose:
            print(f"  [!] Could not load gold standard for task: {task_id}")
        return None

    # Evaluate
    eval_result = evaluate_against_gold_standard(output, gold_data)

    # Print report if verbose
    if verbose:
        print_gold_standard_report(eval_result, verbose=True)

        # Print detailed mismatch analysis
        print_mismatch_analysis(eval_result, gold_data, output)
    else:
        # Compact summary
        score = eval_result.get("overall_score", 0)
        grade = eval_result.get("grade", "N/A")
        print(f"  Score: {score:.1f}/100 (Grade: {grade})")

    # Save detailed evaluation report
    if output_dir:
        save_evaluation_report_legacy(
            task_id, eval_result, gold_data, output, output_dir
        )

    return eval_result


def print_mismatch_analysis(
    eval_result: Dict[str, Any], gold_data: Dict[str, Any], output: str
) -> None:
    """Print detailed analysis of why items didn't match."""
    print("\n" + "-" * 60)
    print("DETAILED MISMATCH ANALYSIS")
    print("-" * 60)

    has_issues = False

    # Components
    missing_components = eval_result.get("components", {}).get("missing", [])
    if missing_components:
        has_issues = True
        print("\n[!] MISSING COMPONENTS:")
        for comp in missing_components:
            print(f"    Expected: '{comp}'")
            # Show what might be similar in output
            comp_lower = comp.lower()
            for line in output.split("\n"):
                line_lower = line.lower()
                # Check for partial matches
                words = comp_lower.split()
                if any(word in line_lower for word in words if len(word) > 3):
                    print(f"    Similar:  '{line.strip()[:80]}'")
                    break

    # Patterns
    missing_patterns = eval_result.get("patterns", {}).get("missing", [])
    if missing_patterns:
        has_issues = True
        print("\n[!] MISSING PATTERNS:")
        for pattern in missing_patterns:
            print(f"    Expected regex: {pattern}")

    # Key Decisions
    missing_decisions = eval_result.get("decisions", {}).get("missing", [])
    if missing_decisions:
        has_issues = True
        print("\n[!] MISSING KEY DECISIONS:")
        for decision in missing_decisions:
            print(f"    Expected mention of: '{decision}'")
            # Show keywords we looked for
            keywords = [w for w in decision.lower().split() if len(w) > 3]
            print(f"    Keywords checked: {keywords}")

    # Endpoints
    missing_endpoints = eval_result.get("endpoints", {}).get("missing", [])
    if missing_endpoints:
        has_issues = True
        print("\n[!] MISSING API ENDPOINTS:")
        for ep in missing_endpoints:
            print(f"    Expected: '{ep}'")

    # Tables
    missing_tables = eval_result.get("tables", {}).get("missing", [])
    if missing_tables:
        has_issues = True
        print("\n[!] MISSING DATABASE TABLES:")
        for table in missing_tables:
            print(f"    Expected: '{table}'")

    if not has_issues:
        print("\n  [+] All gold standard criteria met!")
    else:
        print("\n  TIP: Review the output file and gold standard to understand gaps.")


def save_evaluation_report_legacy(
    task_id: str,
    eval_result: Dict[str, Any],
    gold_data: Dict[str, Any],
    output: str,
    output_dir: Path,
) -> None:
    """Save detailed evaluation report to file (legacy pattern-matching
    format)."""
    report_file = output_dir / f"task_{task_id}_evaluation.md"

    lines = [
        f"# Evaluation Report: Task {task_id}",
        "",
        f"**Score:** {eval_result.get('overall_score', 0):.1f}/100",
        f"**Grade:** {eval_result.get('grade', 'N/A')}",
        "",
        "## Category Scores",
        "",
    ]

    # Category breakdown
    for category in ["components", "patterns", "decisions", "endpoints", "tables"]:
        cat_data = eval_result.get(category, {})
        score = cat_data.get("score", 0)
        matched = cat_data.get("matched", [])
        missing = cat_data.get("missing", [])

        lines.append(f"### {category.title()}: {score:.0f}%")
        lines.append("")

        if matched:
            lines.append("**Matched:**")
            for item in matched:
                lines.append(f"- [x] {item}")
            lines.append("")

        if missing:
            lines.append("**Missing:**")
            for item in missing:
                lines.append(f"- [ ] {item}")
            lines.append("")

    # Gold standard reference
    api_endpoints = gold_data.get("api_endpoints", [])
    endpoints_str = [f"{e['method']} {e['path']}" for e in api_endpoints]

    lines.extend(
        [
            "## Gold Standard Reference",
            "",
            f"**Required Components:** {gold_data.get('required_components', [])}",
            "",
            f"**Required Patterns:** {gold_data.get('required_patterns', [])}",
            "",
            f"**Key Decisions:** {gold_data.get('key_decisions', [])}",
            "",
            f"**API Endpoints:** {endpoints_str}",
            "",
            f"**Database Tables:** {gold_data.get('database_tables', [])}",
            "",
            "## Output Preview (first 2000 chars)",
            "",
            "```",
            output[:2000],
            "```",
        ]
    )

    report_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Evaluation report: {report_file.name}")


# =============================================================================
# WORKFLOW DATA EXTRACTION
# =============================================================================


def evaluate_agent_output(
    agent_task_id: str,
    agent_type: str,
    task_description: str,
    agent_output: str,
    original_prompt: str,
    model: str,
    benchmark_id: str,
    evaluator_model: str = None,
    verbose: bool = False,
) -> Optional[Dict[str, Any]]:
    """Evaluate a single agent's output using LLM-based evaluation.

    Returns evaluation result dict or None if evaluation fails.
    """
    if not HAS_LLM_EVALUATOR:
        return None

    if not agent_output or len(agent_output.strip()) < 50:
        return {
            "score": 0.0,
            "grade": "F",
            "reason": "Output too short or empty",
        }

    # Build agent-specific gold standard based on task type
    agent_gold_standard = {
        "task_type": agent_type,
        "task_description": task_description,
        "original_prompt": original_prompt,
        "expected_qualities": get_agent_expectations(agent_type),
    }

    try:
        eval_result = evaluate_with_llm(
            task_id=agent_task_id,
            task_prompt=f"[{agent_type.upper()} AGENT TASK]\n{task_description}\n\n[CONTEXT]\nOriginal request: {original_prompt[:500]}",
            generated_output=agent_output,
            gold_standard=agent_gold_standard,
            model=model,
            benchmark_id=benchmark_id,
            evaluator_model=evaluator_model,
            verbose=False,  # Don't print full report for each agent
        )

        return {
            "score": eval_result.overall_score,
            "grade": eval_result.grade,
            "dimension_scores": {
                k: v.score for k, v in eval_result.dimension_scores.items()
            },
            "strengths": eval_result.strengths[:2] if eval_result.strengths else [],
            "weaknesses": eval_result.weaknesses[:2] if eval_result.weaknesses else [],
        }
    except Exception as e:
        if verbose:
            print(f"    [!] Agent eval error: {e}")
        return {
            "score": 0.0,
            "grade": "F",
            "reason": f"Evaluation failed: {str(e)}",
        }


def get_agent_expectations(agent_type: str) -> Dict[str, str]:
    """Get expected qualities for each agent type."""
    expectations = {
        "analyst": {
            "key_qualities": "Deep analysis, pattern recognition, evidence-based findings",
            "expected_sections": "KEY FINDINGS, PATTERNS IDENTIFIED, RECOMMENDATIONS",
            "success_criteria": "Provides actionable insights with supporting evidence",
        },
        "researcher": {
            "key_qualities": "Thorough research, fact verification, source reliability",
            "expected_sections": "RESEARCH FINDINGS, INFORMATION GAPS, KEY TAKEAWAYS",
            "success_criteria": "Comprehensive information gathering with reliability assessment",
        },
        "strategist": {
            "key_qualities": "Strategic planning, risk assessment, clear recommendations",
            "expected_sections": "STRATEGIC APPROACH, OPTIONS CONSIDERED, RISK MITIGATION",
            "success_criteria": "Clear strategy with trade-offs and success metrics",
        },
        "implementer": {
            "key_qualities": "Practical solutions, working code, technical specifications",
            "expected_sections": "IMPLEMENTATION APPROACH, CODE/ARTIFACTS, NEXT STEPS",
            "success_criteria": "Concrete implementation with runnable code or clear specs",
        },
        "validator": {
            "key_qualities": "Quality assurance, edge case identification, test coverage",
            "expected_sections": "VALIDATION RESULTS, ISSUES FOUND, RECOMMENDATIONS",
            "success_criteria": "Thorough validation with clear pass/fail criteria",
        },
    }
    return expectations.get(
        agent_type,
        {
            "key_qualities": "Clear, relevant, actionable output",
            "expected_sections": "Structured response addressing the task",
            "success_criteria": "Addresses the task requirements effectively",
        },
    )


def extract_workflow_data(
    result,
    evaluate_phases: bool = False,
    model: str = None,
    benchmark_id: str = None,
    original_prompt: str = None,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Extract full workflow data from an OrchestratorResult.

    Captures all phases, agent outputs, and metadata for comprehensive
    logging. Optionally evaluates each agent's output.
    """
    workflow_data = {
        "task_description": result.task_description,
        "total_duration_seconds": result.total_duration_seconds,
        "metadata": result.metadata,
        "phases": [],
        "agent_results": {},
        "phase_evaluations": {},  # Per-agent evaluations
    }

    # Extract plan phases
    if result.plan and result.plan.phases:
        for phase_idx, phase_tasks in enumerate(result.plan.phases):
            phase_data = {"phase_number": phase_idx + 1, "tasks": []}
            for task in phase_tasks:
                task_data = {
                    "task_id": task.id,
                    "description": task.description,
                    "agent_type": (
                        task.agent_type.value
                        if hasattr(task.agent_type, "value")
                        else str(task.agent_type)
                    ),
                    "status": (
                        task.status.value
                        if hasattr(task.status, "value")
                        else str(task.status)
                    ),
                    "priority": (
                        task.priority.value
                        if hasattr(task.priority, "value")
                        else str(task.priority)
                    ),
                    "dependencies": task.dependencies,
                    "expected_output": task.expected_output,
                    "inputs": task.inputs,
                }
                phase_data["tasks"].append(task_data)
            workflow_data["phases"].append(phase_data)

        workflow_data["integration_strategy"] = result.plan.integration_strategy

    # Extract individual agent results with full outputs
    if result.agent_results:
        for task_id, task in result.agent_results.items():
            agent_type = (
                task.agent_type.value
                if hasattr(task.agent_type, "value")
                else str(task.agent_type)
            )
            agent_output = task.result or ""

            agent_data = {
                "task_id": task.id,
                "description": task.description,
                "agent_type": agent_type,
                "status": (
                    task.status.value
                    if hasattr(task.status, "value")
                    else str(task.status)
                ),
                "output": agent_output,
                "confidence": task.confidence,
                "error": task.error,
                "duration_seconds": task.duration_seconds,
                "started_at": task.started_at.isoformat() if task.started_at else None,
                "completed_at": (
                    task.completed_at.isoformat() if task.completed_at else None
                ),
            }
            workflow_data["agent_results"][task_id] = agent_data

            # Evaluate this agent's output if requested
            if evaluate_phases and agent_output and model:
                if verbose:
                    print(f"    [Eval] Scoring {task_id} ({agent_type})...")

                eval_result = evaluate_agent_output(
                    agent_task_id=task_id,
                    agent_type=agent_type,
                    task_description=task.description,
                    agent_output=agent_output,
                    original_prompt=original_prompt or result.task_description,
                    model=model,
                    benchmark_id=benchmark_id,
                    evaluator_model=model,
                    verbose=verbose,
                )

                if eval_result:
                    workflow_data["phase_evaluations"][task_id] = eval_result
                    agent_data["evaluation"] = eval_result

                    if verbose:
                        score = eval_result.get("score", 0)
                        grade = eval_result.get("grade", "?")
                        print(f"           Score: {score:.1f}/10 (Grade: {grade})")

    # Calculate phase summary scores
    if workflow_data["phase_evaluations"]:
        scores = [
            e.get("score", 0) for e in workflow_data["phase_evaluations"].values()
        ]
        workflow_data["phase_summary"] = {
            "total_agents": len(scores),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "min_score": min(scores) if scores else 0,
            "max_score": max(scores) if scores else 0,
            "scores_by_agent": {
                k: v.get("score", 0)
                for k, v in workflow_data["phase_evaluations"].items()
            },
        }

    return workflow_data


def save_workflow_phases_md(
    workflow_data: Dict[str, Any], task_id: str, output_dir: Path
) -> None:
    """Save workflow phases as readable markdown file.

    Shows each phase and agent output clearly.
    """
    lines = [
        f"# Workflow Phases: Task {task_id}",
        "",
        f"**Total Duration:** {workflow_data.get('total_duration_seconds', 0):.1f}s",
        f"**Integration Strategy:** {workflow_data.get('integration_strategy', 'N/A')}",
        "",
        "---",
        "",
    ]

    # Document each phase
    for phase in workflow_data.get("phases", []):
        phase_num = phase.get("phase_number", "?")
        lines.append(f"## Phase {phase_num}")
        lines.append("")

        for task_info in phase.get("tasks", []):
            task_id_str = task_info.get("task_id", "unknown")
            agent = task_info.get("agent_type", "unknown")
            status = task_info.get("status", "unknown")
            desc = task_info.get("description", "No description")

            lines.append(f"### {task_id_str} ({agent}) - {status}")
            lines.append("")
            lines.append(f"**Task:** {desc}")
            lines.append("")

            # Get the actual output from agent_results
            agent_result = workflow_data.get("agent_results", {}).get(task_id_str, {})
            output = agent_result.get("output", "")
            duration = agent_result.get("duration_seconds")

            if duration:
                lines.append(f"**Duration:** {duration:.1f}s")
                lines.append("")

            # Show evaluation score for this agent
            agent_eval = workflow_data.get("phase_evaluations", {}).get(task_id_str, {})
            if agent_eval:
                score = agent_eval.get("score", 0)
                grade = agent_eval.get("grade", "?")
                lines.append(f"**Evaluation:** {score:.1f}/10 (Grade: {grade})")

                # Dimension scores if available
                dim_scores = agent_eval.get("dimension_scores", {})
                if dim_scores:
                    dims_str = ", ".join(
                        [f"{k}: {v:.1f}" for k, v in dim_scores.items()]
                    )
                    lines.append(f"  - Dimensions: {dims_str}")

                # Strengths/weaknesses
                strengths = agent_eval.get("strengths", [])
                if strengths:
                    lines.append(f"  - Strengths: {'; '.join(strengths)}")
                weaknesses = agent_eval.get("weaknesses", [])
                if weaknesses:
                    lines.append(f"  - Weaknesses: {'; '.join(weaknesses)}")
                lines.append("")

            if output:
                lines.append("**Output:**")
                lines.append("")
                # Indent the output or use code block
                lines.append("```")
                lines.append(output[:3000] if len(output) > 3000 else output)
                if len(output) > 3000:
                    lines.append(f"... [truncated, {len(output)} chars total]")
                lines.append("```")
                lines.append("")
            else:
                lines.append("**Output:** (none)")
                lines.append("")

        lines.append("---")
        lines.append("")

    # Phase evaluation summary
    phase_summary = workflow_data.get("phase_summary", {})
    if phase_summary:
        lines.append("## Phase Evaluation Summary")
        lines.append("")
        lines.append(
            f"**Total Agents Evaluated:** {phase_summary.get('total_agents', 0)}"
        )
        lines.append(
            f"**Average Score:** {phase_summary.get('average_score', 0):.1f}/10"
        )
        lines.append(
            f"**Score Range:** {phase_summary.get('min_score', 0):.1f} - {phase_summary.get('max_score', 0):.1f}"
        )
        lines.append("")

        scores_by_agent = phase_summary.get("scores_by_agent", {})
        if scores_by_agent:
            lines.append("| Agent | Score | Grade |")
            lines.append("|-------|-------|-------|")
            for agent_id, score in scores_by_agent.items():
                grade = (
                    "A"
                    if score >= 9
                    else (
                        "B"
                        if score >= 8
                        else "C" if score >= 7 else "D" if score >= 6 else "F"
                    )
                )
                lines.append(f"| {agent_id} | {score:.1f} | {grade} |")
            lines.append("")
        lines.append("---")
        lines.append("")

    # Summary metadata
    metadata = workflow_data.get("metadata", {})
    if metadata:
        lines.append("## Workflow Metadata")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(metadata, indent=2, default=str))
        lines.append("```")

    # Write file
    phases_file = output_dir / f"task_{task_id}_phases.md"
    phases_file.write_text("\n".join(lines), encoding="utf-8")


def run_benchmark(config: BenchmarkConfig) -> Dict[str, Any]:
    """Execute benchmark with given configuration.

    Returns results dictionary.
    """
    print_header("RUNNING BENCHMARK")

    # Create output directory for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = (
        Path(__file__).parents[3]
        / "results"
        / "benchmark_runs"
        / f"{config.benchmark_id}_{timestamp}"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"  Output directory: {output_dir}")

    # Load tasks
    tasks = load_benchmark(
        config.benchmark_id,
        limit=config.limit,
        use_cache=config.use_cache,
    )

    if not tasks:
        print("⚠ No tasks loaded!")
        return {"error": "No tasks loaded", "tasks_run": 0}

    print(f"\n✓ Loaded {len(tasks)} tasks")

    # Initialize orchestrator based on workflow
    results = {
        "config": config.to_dict(),
        "started_at": datetime.now().isoformat(),
        "tasks": [],
        "summary": {},
    }

    if config.workflow == "multi-agent":
        from tools.agents.multi_agent_orchestrator import MultiAgentOrchestrator

        orchestrator = MultiAgentOrchestrator(
            model=config.model,
            verbose=config.verbose,
        )
    else:
        # Placeholder for other workflows
        orchestrator = None
        print(f"⚠ Workflow '{config.workflow}' not yet implemented")
        print("  Using direct execution mode")

    # Run each task
    successful = 0
    failed = 0

    for i, task in enumerate(tasks, 1):
        print(f"\n{'─' * 60}")
        print(f"Task {i}/{len(tasks)}: {task.task_id}")
        print(f"{'─' * 60}")

        if config.verbose:
            prompt_preview = (
                task.prompt[:200] + "..." if len(task.prompt) > 200 else task.prompt
            )
            print(f"\nPrompt: {prompt_preview}\n")

        try:
            start_time = datetime.now()
            workflow_data = None  # Track multi-agent workflow details

            if orchestrator:
                # Multi-agent execution
                result = orchestrator.run(task.prompt)
                output = result.final_output
                task_success = result.metadata.get("successful_tasks", 0) > 0

                # Capture full workflow data for all phases WITH per-agent evaluation
                print("  Evaluating individual agent outputs...")
                workflow_data = extract_workflow_data(
                    result,
                    evaluate_phases=True,
                    model=config.model,
                    benchmark_id=config.benchmark_id,
                    original_prompt=task.prompt,
                    verbose=config.verbose,
                )
            else:
                # Direct LLM call (placeholder)
                from tools.llm.llm_client import LLMClient

                output = LLMClient.generate_text(config.model, task.prompt)
                task_success = bool(output)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            task_result = {
                "task_id": task.task_id,
                "success": task_success,
                "duration_seconds": duration,
                "output_length": len(output) if output else 0,
            }

            # Save workflow phases data (all agent outputs)
            if workflow_data:
                task_result["workflow"] = workflow_data
                # Save detailed workflow file
                workflow_file = output_dir / f"task_{task.task_id}_workflow.json"
                with open(workflow_file, "w", encoding="utf-8") as f:
                    json.dump(workflow_data, f, indent=2, default=str)
                print(f"  Workflow saved: {workflow_file.name}")

                # Save each phase output as markdown for readability
                save_workflow_phases_md(workflow_data, task.task_id, output_dir)

            # Save generated output to file
            if output:
                output_file = output_dir / f"task_{task.task_id}_output.md"
                output_file.write_text(output, encoding="utf-8")
                task_result["output_file"] = str(output_file)
                print(f"  Output saved: {output_file.name}")

            # LLM-based evaluation (new default)
            if output:
                eval_result = evaluate_task_output_llm(
                    task=task,
                    output=output,
                    model=config.model,
                    benchmark_id=config.benchmark_id,
                    verbose=config.verbose,
                    output_dir=output_dir,
                    evaluator_model=config.model,  # Use same model for eval
                )
                if eval_result:
                    task_result["evaluation"] = eval_result
                    # Score is now 0-10, convert display
                    task_result["score"] = eval_result.get("overall_score", 0)
                    task_result["grade"] = eval_result.get("grade", "N/A")

            if config.save_intermediate:
                task_result["output"] = output

            results["tasks"].append(task_result)

            if task_success:
                successful += 1
                print(f"✓ Completed in {duration:.1f}s")
            else:
                failed += 1
                print(f"✗ Failed in {duration:.1f}s")

        except Exception as e:
            failed += 1
            results["tasks"].append(
                {
                    "task_id": task.task_id,
                    "success": False,
                    "error": str(e),
                }
            )
            print(f"✗ Error: {e}")

    # Summary
    results["completed_at"] = datetime.now().isoformat()
    results["summary"] = {
        "total_tasks": len(tasks),
        "successful": successful,
        "failed": failed,
        "success_rate": successful / len(tasks) if tasks else 0,
    }

    # Calculate average score if evaluations exist
    scores = [t.get("score", 0) for t in results["tasks"] if "score" in t]
    if scores:
        avg_score = sum(scores) / len(scores)
        results["summary"]["average_score"] = avg_score
        results["summary"]["evaluated_tasks"] = len(scores)

        # Grade distribution
        grades = [t.get("grade", "N/A") for t in results["tasks"] if "grade" in t]
        grade_counts = {g: grades.count(g) for g in set(grades)}
        results["summary"]["grade_distribution"] = grade_counts

    print_header("RESULTS SUMMARY")
    print(f"  Total:     {len(tasks)}")
    print(f"  Successful: {successful} ({results['summary']['success_rate']:.1%})")
    print(f"  Failed:    {failed}")

    # Show evaluation summary
    if scores:
        print("\n  EVALUATION SCORES (0.0-10.0 scale)")
        print(f"  Average Score: {avg_score:.2f}/10.0")
        print("  Grade Distribution:")
        for grade in ["A", "B", "C", "D", "F"]:
            if grade in grade_counts:
                print(f"    {grade}: {grade_counts[grade]}")

    # Save results summary
    results["output_directory"] = str(output_dir)
    results_file = output_dir / "results_summary.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to: {results_file}")

    return results


# =============================================================================
# CLI COMMANDS
# =============================================================================


def cmd_list_benchmarks(args: argparse.Namespace) -> None:
    """List available benchmarks."""
    print_header("AVAILABLE BENCHMARKS")

    headers = ["ID", "Name", "Type", "Size", "Source"]
    widths = [20, 25, 20, 10, 15]
    rows = []

    for bid, bdef in BENCHMARK_DEFINITIONS.items():
        rows.append(
            [
                bid,
                bdef.name,
                bdef.benchmark_type.value,
                f"~{bdef.size}",
                bdef.source.value,
            ]
        )

    print_table(headers, rows, widths)

    print(f"\nTotal: {len(BENCHMARK_DEFINITIONS)} benchmarks")
    print("\nUse --benchmark <id> to run a specific benchmark")


def cmd_list_presets(args: argparse.Namespace) -> None:
    """List preset configurations."""
    print_header("PRESET CONFIGURATIONS")

    for name, cfg in PRESET_CONFIGS.items():
        print(f"\n  {colorize(name, 'cyan')}:")
        print(f"    Benchmark: {cfg.benchmark_id}")
        print(f"    Model:     {cfg.model}")
        print(f"    Workflow:  {cfg.workflow}")
        print(f"    Limit:     {cfg.limit or 'all'}")


def cmd_info(args: argparse.Namespace) -> None:
    """Show detailed info about a benchmark."""
    benchmark = BENCHMARK_DEFINITIONS.get(args.benchmark)
    if not benchmark:
        print(f"Unknown benchmark: {args.benchmark}")
        return

    print_header(f"BENCHMARK: {benchmark.name}")
    print(f"\n  ID:          {benchmark.id}")
    print(f"  Type:        {benchmark.benchmark_type.value}")
    print(f"  Size:        ~{benchmark.size} tasks")
    print(f"  Source:      {benchmark.source.value}")
    print(f"  URL:         {benchmark.source_url}")
    print(f"  Languages:   {', '.join(benchmark.languages)}")
    print("\n  Description:")
    print(f"    {benchmark.description}")
    print(f"\n  Metrics:     {', '.join(benchmark.metrics)}")
    print(f"  Evaluation:  {benchmark.evaluation_method}")

    if benchmark.paper_url:
        print(f"\n  Paper:       {benchmark.paper_url}")
    if benchmark.leaderboard_url:
        print(f"  Leaderboard: {benchmark.leaderboard_url}")


def cmd_clear_cache(args: argparse.Namespace) -> None:
    """Clear benchmark cache."""
    deleted = clear_cache(args.benchmark if hasattr(args, "benchmark") else None)
    print(f"Cleared {deleted} cached files")


def cmd_list_models(args: argparse.Namespace) -> None:
    """List all available models from discovery."""
    print_header("AVAILABLE MODELS")

    providers = get_available_models_by_provider()

    if not providers:
        print("  No models discovered.")
        print("  Run: python -m tools.agents.benchmarks.runner --discover")
        return

    total = 0
    for provider_name, models in sorted(providers.items()):
        print(f"\n  {colorize(provider_name.upper(), 'cyan')} ({len(models)} models)")
        total += len(models)
        for model in sorted(models)[:10]:
            print(f"    {model}")
        if len(models) > 10:
            print(f"    ... +{len(models) - 10} more")

    print(f"\n  {colorize(f'Total: {total} models available', 'green')}")


def cmd_discover_models(args: argparse.Namespace) -> None:
    """Run model discovery and save results."""
    print_header("MODEL DISCOVERY")
    print("  Discovering available models...\n")

    try:
        from tools.llm.model_probe import discover_all_models

        results = discover_all_models(verbose=True)

        # Save to discovery_results.json
        output_file = Path(__file__).parents[3] / "discovery_results.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        print(f"\n  Results saved to: {output_file}")

        # Show summary
        summary = results.get("summary", {})
        print(f"  Total models: {summary.get('total_available', 0)}")
        print(f"  Providers: {summary.get('providers_configured', 0)}")

    except ImportError as e:
        print(f"  Error: Could not import model_probe: {e}")
    except Exception as e:
        print(f"  Error during discovery: {e}")


def cmd_run(args: argparse.Namespace) -> None:
    """Run benchmark with given configuration."""
    # Build config from args
    config = BenchmarkConfig(
        benchmark_id=args.benchmark,
        model=args.model,
        workflow=args.workflow,
        limit=args.limit,
        verbose=args.verbose,
        timeout_seconds=args.timeout,
    )

    # Validate
    errors = BenchmarkRegistry.validate_config(config)
    if errors:
        print("Configuration errors:")
        for err in errors:
            print(f"  - {err}")
        return

    # Run
    results = run_benchmark(config)

    # Save results
    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {output_path}")


# =============================================================================
# MAIN
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Benchmark Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python -m tools.agents.benchmarks.runner
    
  Run HumanEval with GPT-4o-mini:
    python -m tools.agents.benchmarks.runner --benchmark humaneval --model gh:gpt-4o-mini --limit 5
    
  Use a preset:
    python -m tools.agents.benchmarks.runner --preset quick-test
    
  List available benchmarks:
    python -m tools.agents.benchmarks.runner --list
        """,
    )

    # Mode selection
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Interactive configuration mode",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List available benchmarks",
    )
    parser.add_argument(
        "--presets",
        action="store_true",
        help="List preset configurations",
    )
    parser.add_argument(
        "--info",
        metavar="BENCHMARK",
        help="Show detailed info about a benchmark",
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear benchmark data cache",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List all available models from discovery",
    )
    parser.add_argument(
        "--discover",
        action="store_true",
        help="Run model discovery and update discovery_results.json",
    )

    # Run configuration
    parser.add_argument(
        "--benchmark",
        "-b",
        type=str,
        default="custom-local",
        help="Benchmark ID to run",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="gh:gpt-4o-mini",
        help="Model to use",
    )
    parser.add_argument(
        "--workflow",
        "-w",
        type=str,
        default="multi-agent",
        choices=["multi-agent", "single-agent", "chain-of-thought", "react"],
        help="Agent workflow",
    )
    parser.add_argument(
        "--limit",
        "-n",
        type=int,
        help="Max tasks to run",
    )
    parser.add_argument(
        "--preset",
        "-p",
        type=str,
        help="Use a preset configuration",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout per task (seconds)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file for results (JSON)",
    )

    args = parser.parse_args()

    try:
        # Handle info commands
        if args.list:
            cmd_list_benchmarks(args)
            return

        if args.presets:
            cmd_list_presets(args)
            return

        if args.info:
            args.benchmark = args.info
            cmd_info(args)
            return

        if args.clear_cache:
            cmd_clear_cache(args)
            return

        if args.list_models:
            cmd_list_models(args)
            return

        if args.discover:
            cmd_discover_models(args)
            return

        # Handle preset
        if args.preset:
            preset = PRESET_CONFIGS.get(args.preset)
            if not preset:
                print(f"Unknown preset: {args.preset}")
                print(f"Available: {list(PRESET_CONFIGS.keys())}")
                return

            # Apply preset but allow overrides
            config = preset
            if args.benchmark != "custom-local":
                config.benchmark_id = args.benchmark
            if args.model != "gh:gpt-4o-mini":
                config.model = args.model
            if args.limit:
                config.limit = args.limit
            config.verbose = args.verbose or config.verbose

            results = run_benchmark(config)

            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(results, f, indent=2)
            return

        # Interactive mode (default if no benchmark specified via CLI)
        if args.interactive or (len(sys.argv) == 1):
            config = interactive_mode()
            if config:
                results = run_benchmark(config)

                # Optionally save
                if prompt_yes_no("\nSave results to file?", False):
                    output_path = prompt_input("Output file", "benchmark_results.json")
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(results, f, indent=2)
                    print(f"Saved to: {output_path}")
            return

        # Direct run mode
        cmd_run(args)

    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()
