from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class DataSource(str, Enum):
    HUGGINGFACE = "huggingface"
    GITHUB = "github"
    LOCAL = "local"
    API = "api"


class BenchmarkType(str, Enum):
    SOFTWARE_ENGINEERING = "software_engineering"
    FUNCTION_LEVEL = "function_level"
    BASIC_PROGRAMMING = "basic_programming"
    GOAL_ORIENTED = "goal_oriented"
    CUSTOM = "custom"


@dataclass(frozen=True)
class BenchmarkDefinition:
    id: str
    name: str
    description: str
    benchmark_type: BenchmarkType
    size: int
    source: DataSource
    source_url: str
    source_config: Dict[str, Any] = field(default_factory=dict)
    metrics: List[str] = field(default_factory=list)
    evaluation_method: str = "pass@1"
    license: str = "unknown"
    languages: List[str] = field(default_factory=lambda: ["python"])
    tags: List[str] = field(default_factory=list)


# Minimal, self-contained fallback definitions.
# If the repo's benchmark tooling (`tools.agents.benchmarks`) is importable,
# the server will use that instead.
FALLBACK_BENCHMARKS: Dict[str, BenchmarkDefinition] = {
    "humaneval": BenchmarkDefinition(
        id="humaneval",
        name="HumanEval",
        description="Hand-written Python programming problems with unit tests.",
        benchmark_type=BenchmarkType.FUNCTION_LEVEL,
        size=164,
        source=DataSource.HUGGINGFACE,
        source_url="openai/openai_humaneval",
        source_config={"split": "test"},
        metrics=["pass@1", "pass@10", "pass@100"],
        evaluation_method="unit_tests",
        license="MIT",
        languages=["python"],
        tags=["functions", "unit-tests"],
    ),
    "mbpp": BenchmarkDefinition(
        id="mbpp",
        name="MBPP",
        description="Mostly Basic Python Problems with test cases.",
        benchmark_type=BenchmarkType.BASIC_PROGRAMMING,
        size=974,
        source=DataSource.HUGGINGFACE,
        source_url="google-research-datasets/mbpp",
        source_config={"split": "test"},
        metrics=["pass@1", "pass@80"],
        evaluation_method="unit_tests",
        license="CC-BY-4.0",
        languages=["python"],
        tags=["basic", "entry-level"],
    ),
    "swe-bench-lite": BenchmarkDefinition(
        id="swe-bench-lite",
        name="SWE-bench Lite",
        description="Smaller SWE-bench subset for faster evaluation.",
        benchmark_type=BenchmarkType.SOFTWARE_ENGINEERING,
        size=300,
        source=DataSource.HUGGINGFACE,
        source_url="princeton-nlp/SWE-bench_Lite",
        source_config={"split": "test"},
        metrics=["resolved_rate"],
        evaluation_method="execution",
        license="MIT",
        languages=["python"],
        tags=["github", "issues", "patches", "lite"],
    ),
}


def try_get_repo_benchmarks() -> Optional[Dict[str, Any]]:
    """Try to load benchmark definitions from the repo benchmark tool.

    Returns the module-level BENCHMARK_DEFINITIONS mapping if importable.
    """
    try:
        from tools.agents.benchmarks.datasets import BENCHMARK_DEFINITIONS  # type: ignore

        return BENCHMARK_DEFINITIONS
    except Exception:
        return None
