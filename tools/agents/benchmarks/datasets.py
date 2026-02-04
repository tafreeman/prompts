"""
Benchmark Dataset Definitions
=============================

Stores metadata about available benchmarks. Actual data is fetched on demand.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class BenchmarkType(Enum):
    """Types of coding benchmarks."""

    SOFTWARE_ENGINEERING = "software_engineering"  # End-to-end issue resolution
    FUNCTION_LEVEL = "function_level"  # Single function completion
    BASIC_PROGRAMMING = "basic_programming"  # Simple coding tasks
    GOAL_ORIENTED = "goal_oriented"  # Real-world development goals
    CUSTOM = "custom"  # User-defined tasks


class DataSource(Enum):
    """Where benchmark data comes from."""

    HUGGINGFACE = "huggingface"  # HuggingFace datasets
    GITHUB = "github"  # GitHub repositories
    LOCAL = "local"  # Local JSON files
    API = "api"  # REST API endpoints


@dataclass
class BenchmarkDefinition:
    """Definition of a benchmark dataset.

    Only stores metadata - actual tasks are fetched on demand.
    """

    id: str  # Unique identifier
    name: str  # Display name
    description: str  # What this benchmark tests
    benchmark_type: BenchmarkType  # Category
    size: int  # Number of tasks (approximate)

    # Data source configuration
    source: DataSource  # Where to fetch from
    source_url: str  # URL/path to dataset
    source_config: Dict[str, Any] = field(
        default_factory=dict
    )  # Source-specific config

    # Evaluation info
    metrics: List[str] = field(default_factory=list)  # How results are measured
    evaluation_method: str = "pass@1"  # Default evaluation approach

    # Metadata
    paper_url: Optional[str] = None  # Research paper
    leaderboard_url: Optional[str] = None  # Public leaderboard
    license: str = "unknown"  # Data license
    citation: Optional[str] = None  # How to cite

    # Filtering options
    languages: List[str] = field(default_factory=lambda: ["python"])
    difficulty_range: Optional[tuple] = None  # (min, max) if applicable
    tags: List[str] = field(default_factory=list)


# =============================================================================
# BENCHMARK DEFINITIONS
# =============================================================================

BENCHMARK_DEFINITIONS: Dict[str, BenchmarkDefinition] = {
    # -------------------------------------------------------------------------
    # SWE-bench Family - Software Engineering
    # -------------------------------------------------------------------------
    "swe-bench": BenchmarkDefinition(
        id="swe-bench",
        name="SWE-bench",
        description="Real GitHub issues requiring code patches. Tests end-to-end software engineering ability.",
        benchmark_type=BenchmarkType.SOFTWARE_ENGINEERING,
        size=2294,
        source=DataSource.HUGGINGFACE,
        source_url="princeton-nlp/SWE-bench",
        source_config={
            "split": "test",
            "subset": None,
        },
        metrics=["resolved_rate", "patch_apply_rate"],
        evaluation_method="execution",
        paper_url="https://arxiv.org/abs/2310.06770",
        leaderboard_url="https://www.swebench.com/",
        license="MIT",
        citation="@article{jimenez2024swebench, title={SWE-bench: Can Language Models Resolve Real-World GitHub Issues?}}",
        languages=["python"],
        tags=["github", "issues", "patches", "real-world"],
    ),
    "swe-bench-verified": BenchmarkDefinition(
        id="swe-bench-verified",
        name="SWE-bench Verified",
        description="Human-validated subset of SWE-bench with confirmed solvable issues.",
        benchmark_type=BenchmarkType.SOFTWARE_ENGINEERING,
        size=500,
        source=DataSource.HUGGINGFACE,
        source_url="princeton-nlp/SWE-bench_Verified",
        source_config={
            "split": "test",
        },
        metrics=["resolved_rate"],
        evaluation_method="execution",
        paper_url="https://arxiv.org/abs/2310.06770",
        leaderboard_url="https://www.swebench.com/",
        license="MIT",
        languages=["python"],
        tags=["github", "verified", "reliable"],
    ),
    "swe-bench-lite": BenchmarkDefinition(
        id="swe-bench-lite",
        name="SWE-bench Lite",
        description="Smaller subset for faster evaluation and iteration.",
        benchmark_type=BenchmarkType.SOFTWARE_ENGINEERING,
        size=300,
        source=DataSource.HUGGINGFACE,
        source_url="princeton-nlp/SWE-bench_Lite",
        source_config={
            "split": "test",
        },
        metrics=["resolved_rate"],
        evaluation_method="execution",
        paper_url="https://arxiv.org/abs/2310.06770",
        leaderboard_url="https://www.swebench.com/",
        license="MIT",
        languages=["python"],
        tags=["github", "lite", "fast"],
    ),
    # -------------------------------------------------------------------------
    # HumanEval - Function-Level Coding
    # -------------------------------------------------------------------------
    "humaneval": BenchmarkDefinition(
        id="humaneval",
        name="HumanEval",
        description="Hand-written Python programming problems with unit tests. Tests function-level code generation.",
        benchmark_type=BenchmarkType.FUNCTION_LEVEL,
        size=164,
        source=DataSource.HUGGINGFACE,
        source_url="openai/openai_humaneval",
        source_config={
            "split": "test",
        },
        metrics=["pass@1", "pass@10", "pass@100"],
        evaluation_method="unit_tests",
        paper_url="https://arxiv.org/abs/2107.03374",
        leaderboard_url="https://paperswithcode.com/sota/code-generation-on-humaneval",
        license="MIT",
        citation="@article{chen2021evaluating, title={Evaluating Large Language Models Trained on Code}}",
        languages=["python"],
        tags=["functions", "unit-tests", "canonical"],
    ),
    "humaneval-plus": BenchmarkDefinition(
        id="humaneval-plus",
        name="HumanEval+",
        description="Extended HumanEval with 80x more test cases per problem.",
        benchmark_type=BenchmarkType.FUNCTION_LEVEL,
        size=164,
        source=DataSource.HUGGINGFACE,
        source_url="evalplus/humanevalplus",
        source_config={
            "split": "test",
        },
        metrics=["pass@1"],
        evaluation_method="unit_tests",
        paper_url="https://arxiv.org/abs/2305.01210",
        license="Apache-2.0",
        languages=["python"],
        tags=["functions", "extended-tests", "rigorous"],
    ),
    # -------------------------------------------------------------------------
    # MBPP - Basic Python Programming
    # -------------------------------------------------------------------------
    "mbpp": BenchmarkDefinition(
        id="mbpp",
        name="MBPP",
        description="Mostly Basic Python Problems. Entry-level programming tasks with test cases.",
        benchmark_type=BenchmarkType.BASIC_PROGRAMMING,
        size=974,
        source=DataSource.HUGGINGFACE,
        source_url="google-research-datasets/mbpp",
        source_config={
            "split": "test",
        },
        metrics=["pass@1", "pass@80"],
        evaluation_method="unit_tests",
        paper_url="https://arxiv.org/abs/2108.07732",
        leaderboard_url="https://paperswithcode.com/sota/code-generation-on-mbpp",
        license="CC-BY-4.0",
        citation="@article{austin2021program, title={Program Synthesis with Large Language Models}}",
        languages=["python"],
        tags=["basic", "entry-level", "crowd-sourced"],
    ),
    "mbpp-sanitized": BenchmarkDefinition(
        id="mbpp-sanitized",
        name="MBPP Sanitized",
        description="Cleaned subset of MBPP with verified solutions.",
        benchmark_type=BenchmarkType.BASIC_PROGRAMMING,
        size=427,
        source=DataSource.HUGGINGFACE,
        source_url="google-research-datasets/mbpp",
        source_config={
            "split": "test",
            "sanitized": True,
        },
        metrics=["pass@1"],
        evaluation_method="unit_tests",
        paper_url="https://arxiv.org/abs/2108.07732",
        license="CC-BY-4.0",
        languages=["python"],
        tags=["basic", "sanitized", "verified"],
    ),
    # -------------------------------------------------------------------------
    # CodeClash - Goal-Oriented Development (Newer)
    # -------------------------------------------------------------------------
    "codeclash": BenchmarkDefinition(
        id="codeclash",
        name="CodeClash",
        description="Goal-oriented development tasks simulating real-world software projects.",
        benchmark_type=BenchmarkType.GOAL_ORIENTED,
        size=100,  # Varies
        source=DataSource.GITHUB,
        source_url="codeclash-eval/codeclash",
        source_config={
            "branch": "main",
            "tasks_path": "tasks/",
        },
        metrics=["goal_completion", "code_quality", "test_coverage"],
        evaluation_method="goal_verification",
        license="Apache-2.0",
        languages=["python", "javascript", "typescript"],
        tags=["goals", "real-world", "multi-file"],
    ),
    # -------------------------------------------------------------------------
    # Custom/Local Benchmarks
    # -------------------------------------------------------------------------
    "custom-local": BenchmarkDefinition(
        id="custom-local",
        name="Custom Local Tasks",
        description="User-defined tasks stored in the local gold_standards directory.",
        benchmark_type=BenchmarkType.CUSTOM,
        size=10,
        source=DataSource.LOCAL,
        source_url="gold_standards/",
        source_config={
            "pattern": "task_*.json",
        },
        metrics=["component_coverage", "pattern_matching", "decision_coverage"],
        evaluation_method="heuristic",
        license="proprietary",
        languages=["python", "any"],
        tags=["custom", "local", "curated"],
    ),
}


def get_benchmark(benchmark_id: str) -> Optional[BenchmarkDefinition]:
    """Get a benchmark definition by ID."""
    return BENCHMARK_DEFINITIONS.get(benchmark_id)


def list_benchmarks(
    benchmark_type: Optional[BenchmarkType] = None,
    language: Optional[str] = None,
) -> Dict[str, BenchmarkDefinition]:
    """List available benchmarks with optional filtering.

    Args:
        benchmark_type: Filter by type (e.g., SOFTWARE_ENGINEERING)
        language: Filter by supported language

    Returns:
        Dict of matching benchmarks
    """
    result = {}
    for bid, bdef in BENCHMARK_DEFINITIONS.items():
        if benchmark_type and bdef.benchmark_type != benchmark_type:
            continue
        if language and language not in bdef.languages:
            continue
        result[bid] = bdef
    return result
