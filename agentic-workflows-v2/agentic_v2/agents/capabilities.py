"""Agent capability system for dynamic composition.

Aggressive design improvements:
- Composable capabilities via mixins
- Runtime capability discovery
- Capability requirements for tasks
- Capability negotiation between agents
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Optional

if TYPE_CHECKING:
    from .base import BaseAgent


class CapabilityType(str, Enum):
    """Standard capability types."""

    # Code capabilities
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    CODE_REFACTORING = "code_refactoring"
    CODE_EXPLANATION = "code_explanation"

    # Test capabilities
    TEST_GENERATION = "test_generation"
    TEST_EXECUTION = "test_execution"

    # Documentation
    DOCUMENTATION = "documentation"
    API_DOCS = "api_docs"

    # Analysis
    STATIC_ANALYSIS = "static_analysis"
    SECURITY_ANALYSIS = "security_analysis"
    PERFORMANCE_ANALYSIS = "performance_analysis"

    # Planning
    TASK_DECOMPOSITION = "task_decomposition"
    ARCHITECTURE_DESIGN = "architecture_design"

    # Tool use
    FILE_OPERATIONS = "file_operations"
    SHELL_EXECUTION = "shell_execution"
    WEB_SEARCH = "web_search"

    # Meta
    ORCHESTRATION = "orchestration"
    SELF_REFLECTION = "self_reflection"


@dataclass
class Capability:
    """A capability that an agent possesses.

    Capabilities can have:
    - Type classification
    - Proficiency level (0-1)
    - Requirements (other capabilities needed)
    - Metadata
    """

    type: CapabilityType
    proficiency: float = 1.0  # 0.0 to 1.0
    requirements: list[CapabilityType] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.proficiency = max(0.0, min(1.0, self.proficiency))

    def meets_requirement(self, required: "Capability") -> bool:
        """Check if this capability meets a requirement."""
        if self.type != required.type:
            return False
        return self.proficiency >= required.proficiency


@dataclass
class CapabilitySet:
    """A set of capabilities with matching and negotiation."""

    capabilities: dict[CapabilityType, Capability] = field(default_factory=dict)

    def add(self, capability: Capability) -> None:
        """Add a capability."""
        self.capabilities[capability.type] = capability

    def remove(self, cap_type: CapabilityType) -> bool:
        """Remove a capability."""
        if cap_type in self.capabilities:
            del self.capabilities[cap_type]
            return True
        return False

    def has(self, cap_type: CapabilityType, min_proficiency: float = 0.0) -> bool:
        """Check if capability exists with minimum proficiency."""
        cap = self.capabilities.get(cap_type)
        return cap is not None and cap.proficiency >= min_proficiency

    def get(self, cap_type: CapabilityType) -> Optional[Capability]:
        """Get a capability."""
        return self.capabilities.get(cap_type)

    def list_types(self) -> list[CapabilityType]:
        """List all capability types."""
        return list(self.capabilities.keys())

    def meets_requirements(self, required: "CapabilitySet") -> bool:
        """Check if this set meets all requirements from another set."""
        for cap_type, req_cap in required.capabilities.items():
            if not self.has(cap_type, req_cap.proficiency):
                return False
        return True

    def missing_capabilities(self, required: "CapabilitySet") -> list[CapabilityType]:
        """Get list of missing capabilities."""
        missing = []
        for cap_type, req_cap in required.capabilities.items():
            if not self.has(cap_type, req_cap.proficiency):
                missing.append(cap_type)
        return missing

    def score_match(self, required: "CapabilitySet") -> float:
        """Score how well this set matches requirements.

        Returns:
            0.0-1.0 score (1.0 = perfect match)
        """
        if not required.capabilities:
            return 1.0

        total_score = 0.0
        for cap_type, req_cap in required.capabilities.items():
            our_cap = self.capabilities.get(cap_type)
            if our_cap:
                # Score based on proficiency ratio
                total_score += min(
                    1.0, our_cap.proficiency / max(0.01, req_cap.proficiency)
                )
            # Missing capability contributes 0

        return total_score / len(required.capabilities)

    @classmethod
    def from_types(cls, *cap_types: CapabilityType) -> "CapabilitySet":
        """Create from capability types with default proficiency."""
        cap_set = cls()
        for cap_type in cap_types:
            cap_set.add(Capability(type=cap_type))
        return cap_set


class CapabilityMixin(ABC):
    """Mixin for adding capabilities to agents.

    Usage:
        class MyAgent(BaseAgent, CodeGenerationMixin, TestGenerationMixin):
            pass
    """

    @abstractmethod
    def get_capabilities(self) -> CapabilitySet:
        """Return the capabilities provided by this mixin."""
        pass


class CodeGenerationMixin(CapabilityMixin):
    """Mixin for code generation capability."""

    def get_capabilities(self) -> CapabilitySet:
        return CapabilitySet.from_types(
            CapabilityType.CODE_GENERATION, CapabilityType.CODE_EXPLANATION
        )

    async def generate_code(
        self, description: str, language: str = "python", context: Optional[str] = None
    ) -> str:
        """Generate code from description."""
        # Default implementation - override in subclass
        raise NotImplementedError("Subclass must implement generate_code")


class CodeReviewMixin(CapabilityMixin):
    """Mixin for code review capability."""

    def get_capabilities(self) -> CapabilitySet:
        return CapabilitySet.from_types(
            CapabilityType.CODE_REVIEW, CapabilityType.STATIC_ANALYSIS
        )

    async def review_code(
        self,
        code: str,
        language: str = "python",
        focus_areas: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """Review code and return issues."""
        raise NotImplementedError("Subclass must implement review_code")


class TestGenerationMixin(CapabilityMixin):
    """Mixin for test generation capability."""

    def get_capabilities(self) -> CapabilitySet:
        return CapabilitySet.from_types(CapabilityType.TEST_GENERATION)

    async def generate_tests(
        self, code: str, language: str = "python", framework: str = "pytest"
    ) -> str:
        """Generate tests for code."""
        raise NotImplementedError("Subclass must implement generate_tests")


class OrchestrationMixin(CapabilityMixin):
    """Mixin for orchestration capability."""

    def get_capabilities(self) -> CapabilitySet:
        return CapabilitySet.from_types(
            CapabilityType.ORCHESTRATION, CapabilityType.TASK_DECOMPOSITION
        )

    async def decompose_task(self, task: str) -> list[dict[str, Any]]:
        """Decompose a task into subtasks."""
        raise NotImplementedError("Subclass must implement decompose_task")

    async def select_agent(
        self, task: dict[str, Any], available_agents: list["BaseAgent"]
    ) -> Optional["BaseAgent"]:
        """Select best agent for a task."""
        raise NotImplementedError("Subclass must implement select_agent")


def requires_capabilities(*cap_types: CapabilityType):
    """Decorator to mark a method as requiring certain capabilities.

    Usage:
        @requires_capabilities(CapabilityType.CODE_GENERATION)
        async def generate(self, ...):
            ...
    """

    def decorator(func: Callable) -> Callable:
        func._required_capabilities = cap_types
        return func

    return decorator


def get_agent_capabilities(agent: "BaseAgent") -> CapabilitySet:
    """Get all capabilities from an agent (including mixins)."""
    cap_set = CapabilitySet()

    # Check for capability mixins
    for base in type(agent).__mro__:
        if (
            base is not CapabilityMixin
            and issubclass(base, CapabilityMixin)
            and hasattr(base, "get_capabilities")
        ):
            try:
                mixin_caps = base.get_capabilities(agent)
                for cap in mixin_caps.capabilities.values():
                    cap_set.add(cap)
            except Exception:
                pass

    return cap_set
