"""Directed Acyclic Graph (DAG) workflow definition.

Provides:
- Step registration
- Dependency validation
- Cycle detection
- Topological ordering
- Ready-step discovery
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .step import StepDefinition


class MissingDependencyError(ValueError):
    """Raised when a step depends on an unknown step."""

    def __init__(self, step: str, missing_dep: str):
        super().__init__(f"Step '{step}' depends on missing step '{missing_dep}'")
        self.step = step
        self.missing_dep = missing_dep


class CycleDetectedError(ValueError):
    """Raised when a dependency cycle is detected."""

    def __init__(self, cycle_path: list[str]):
        cycle_str = " -> ".join(cycle_path)
        super().__init__(f"Cycle detected in DAG: {cycle_str}")
        self.cycle_path = cycle_path


@dataclass
class DAG:
    """Directed Acyclic Graph for workflow execution.

    Key advantages over Pipeline:
    - No sync barriers between "layers"
    - Maximum parallelism from dependency graph
    - Automatic topological ordering
    - Cycle detection at definition time
    """

    name: str
    description: str = ""
    steps: dict[str, StepDefinition] = field(default_factory=dict)

    def add(self, step: StepDefinition) -> "DAG":
        """Add a step to the DAG."""
        if step.name in self.steps:
            raise ValueError(f"Step '{step.name}' already exists in DAG")
        self.steps[step.name] = step
        return self

    def add_many(self, steps: Iterable[StepDefinition]) -> "DAG":
        """Add multiple steps to the DAG."""
        for step in steps:
            self.add(step)
        return self

    def validate(self) -> None:
        """Validate DAG structure for missing dependencies and cycles."""
        self._check_missing_dependencies()
        adjacency = self._build_adjacency_list()
        self._detect_cycles(adjacency)

    def _check_missing_dependencies(self) -> None:
        for step_name, step in self.steps.items():
            for dep in step.depends_on:
                if dep not in self.steps:
                    raise MissingDependencyError(step_name, dep)

    def _build_adjacency_list(self) -> dict[str, list[str]]:
        """Build adjacency list from depends_on fields."""
        adjacency: dict[str, list[str]] = {name: [] for name in self.steps}
        for step_name, step in self.steps.items():
            for dep in step.depends_on:
                adjacency.setdefault(dep, []).append(step_name)
        return adjacency

    def build_adjacency_list(self) -> dict[str, list[str]]:
        """Public adjacency list builder."""
        return self._build_adjacency_list()

    def _detect_cycles(self, adjacency: dict[str, list[str]]) -> None:
        """Detect cycles using DFS with coloring."""
        color: dict[str, str] = {name: "white" for name in self.steps}
        stack: list[str] = []

        def visit(node: str) -> None:
            color[node] = "gray"
            stack.append(node)

            for neighbor in adjacency.get(node, []):
                if color[neighbor] == "gray":
                    cycle_start = stack.index(neighbor)
                    cycle_path = stack[cycle_start:] + [neighbor]
                    raise CycleDetectedError(cycle_path)
                if color[neighbor] == "white":
                    visit(neighbor)

            stack.pop()
            color[node] = "black"

        for node in self.steps:
            if color[node] == "white":
                visit(node)

    def get_execution_order(self) -> list[str]:
        """Return a topologically sorted list of step names."""
        self.validate()
        adjacency = self._build_adjacency_list()
        in_degree = {name: len(step.depends_on) for name, step in self.steps.items()}

        ready = [name for name, deg in in_degree.items() if deg == 0]
        order: list[str] = []

        while ready:
            current = ready.pop(0)
            order.append(current)
            for dependent in adjacency.get(current, []):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    ready.append(dependent)

        if len(order) != len(self.steps):
            raise CycleDetectedError(order)

        return order

    def get_ready_steps(self, completed: set[str]) -> list[str]:
        """Get steps whose dependencies are all met."""
        ready: list[str] = []
        for name, step in self.steps.items():
            if name in completed:
                continue
            if all(dep in completed for dep in step.depends_on):
                ready.append(name)
        return ready

    def get_dependents(self, step_name: str) -> list[str]:
        """Get direct dependents of a step."""
        adjacency = self._build_adjacency_list()
        return adjacency.get(step_name, [])
