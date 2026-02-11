"""Architect agent for system design and architecture tasks.

Designs system architecture based on requirements including:
- Tech stack recommendations with justifications
- Component diagrams (Mermaid)
- API strategy
- Database design
- Deployment architecture
"""

from __future__ import annotations

import json
import re
from typing import Any, Optional

from pydantic import BaseModel, Field

from ..contracts import TaskInput, TaskOutput
from ..models import ModelTier
from .base import AgentConfig, BaseAgent


class ArchitectureInput(TaskInput):
    """Input for architecture design tasks."""

    requirements: str = Field(
        description="System requirements to design for", min_length=1
    )
    arch_constraints: Optional[str] = Field(
        default=None,
        description="Architecture constraints (not to be confused with TaskInput.constraints)",
    )
    user_stories: Optional[str] = Field(
        default=None, description="User stories to consider"
    )
    existing_architecture: Optional[str] = Field(
        default=None, description="Existing architecture to extend or integrate with"
    )
    preferences: dict[str, Any] = Field(
        default_factory=dict, description="Technology preferences"
    )


class TechStackChoice(BaseModel):
    """A technology choice with justification."""

    name: str = Field(default="", description="Technology name")
    justification: str = Field(default="", description="Why this choice")
    alternatives: list[str] = Field(
        default_factory=list, description="Alternative options considered"
    )


class ArchitectureOutput(TaskOutput):
    """Output from architecture design."""

    tech_stack: dict[str, TechStackChoice] = Field(default_factory=dict)
    component_diagram: str = Field(default="", description="Mermaid diagram")
    api_strategy: dict[str, Any] = Field(default_factory=dict)
    data_flow: str = Field(default="", description="Data flow description")
    deployment: dict[str, Any] = Field(default_factory=dict)
    scalability: dict[str, Any] = Field(default_factory=dict)
    security: dict[str, Any] = Field(default_factory=dict)
    raw_response: str = Field(default="", description="Raw model response")


SYSTEM_PROMPT = """You are a senior software architect with expertise in full-stack application design.

Your task is to design comprehensive system architecture including:
1. Tech stack recommendation with justification for each choice
2. Component diagram using Mermaid syntax
3. API strategy (REST/GraphQL, versioning, authentication)
4. Database design and data flow
5. Authentication and authorization strategy
6. Deployment architecture (environments, CI/CD)
7. Scalability considerations and bottleneck analysis
8. Security considerations

Design Principles:
- Separation of concerns
- Domain-driven design where appropriate
- Security by design
- Performance optimization
- Cost-effectiveness
- Developer experience

Output your response as valid JSON with this structure:
{
    "tech_stack": {
        "frontend": {"name": "...", "justification": "...", "alternatives": [...]},
        "backend": {"name": "...", "justification": "...", "alternatives": [...]},
        "database": {"name": "...", "justification": "...", "alternatives": [...]},
        "infrastructure": {"name": "...", "justification": "...", "alternatives": [...]}
    },
    "component_diagram": "```mermaid\\ngraph TD\\n...\\n```",
    "api_strategy": {
        "type": "REST|GraphQL|gRPC",
        "versioning": "...",
        "authentication": "...",
        "rate_limiting": "..."
    },
    "data_flow": "Description of data flow...",
    "deployment": {
        "strategy": "blue-green|rolling|canary",
        "environments": ["dev", "staging", "prod"],
        "ci_cd": "..."
    },
    "scalability": {
        "bottlenecks": ["..."],
        "recommendations": ["..."],
        "estimated_capacity": "..."
    },
    "security": {
        "authentication": "...",
        "authorization": "...",
        "data_protection": "...",
        "compliance": ["..."]
    }
}
"""


class ArchitectAgent(BaseAgent[ArchitectureInput, ArchitectureOutput]):
    """Agent specialized for system architecture design.

    Takes requirements and produces:
    - Tech stack recommendations with justifications
    - Component diagrams (Mermaid)
    - API strategy
    - Deployment architecture
    - Scalability analysis
    """

    def __init__(self, config: Optional[AgentConfig] = None, **kwargs):
        if config is None:
            config = AgentConfig(
                name="architect",
                description="System architecture design agent",
                system_prompt=SYSTEM_PROMPT,
                default_tier=ModelTier.TIER_3,  # Higher tier for complex reasoning
                max_iterations=3,
            )

        super().__init__(config=config, **kwargs)

    async def _call_model(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        """Call the underlying LLM to generate architecture design.

        Args:
            messages: Chat messages to send
            tools: Optional tools (not typically used for architecture)

        Returns:
            Model response dict with "content" key
        """
        # If no backend is configured, return a mock response for testing
        if self.llm_client.backend is None:
            return {
                "content": json.dumps(
                    {
                        "tech_stack": {
                            "frontend": {
                                "name": "React",
                                "justification": "Mock response",
                            },
                            "backend": {
                                "name": "Python/FastAPI",
                                "justification": "Mock response",
                            },
                        },
                        "component_diagram": "```mermaid\ngraph TD\n    A[Frontend] --> B[Backend]\n```",
                        "api_strategy": {"style": "REST", "versioning": "URL path"},
                        "data_flow": "Frontend -> API -> Database",
                        "deployment": {"platform": "Cloud", "containerized": True},
                        "scalability": {"recommendations": ["Horizontal scaling"]},
                        "security": {"authentication": "JWT"},
                    }
                )
            }

        # Use real LLM client
        result = await self.llm_client.backend.complete_chat(
            messages=messages,
            model=self.llm_client.model_id,
            temperature=0.3,  # Lower temp for architecture consistency
        )

        return {"content": result.get("content", result.get("message", ""))}

    def _format_task_message(self, task: ArchitectureInput) -> str:
        """Format architecture design task."""
        parts = ["## Requirements", "", task.requirements, ""]

        if task.user_stories:
            parts.extend(
                [
                    "## User Stories",
                    "",
                    task.user_stories,
                    "",
                ]
            )

        if task.arch_constraints:
            parts.extend(
                [
                    "## Constraints",
                    "",
                    task.arch_constraints,
                    "",
                ]
            )

        if task.existing_architecture:
            parts.extend(
                [
                    "## Existing Architecture",
                    "",
                    task.existing_architecture,
                    "",
                ]
            )

        if task.preferences:
            parts.extend(
                [
                    "## Preferences",
                    "",
                    json.dumps(task.preferences, indent=2),
                    "",
                ]
            )

        parts.extend(
            [
                "## Task",
                "",
                "Design a comprehensive system architecture for the above requirements.",
                "Provide your response as valid JSON matching the specified structure.",
                "Include Mermaid diagrams where applicable.",
            ]
        )

        return "\n".join(parts)

    async def _is_task_complete(self, task: ArchitectureInput, response: str) -> bool:
        """Check if response contains valid architecture."""
        # Must have some JSON structure
        return "{" in response and "}" in response

    async def _parse_output(
        self, task: ArchitectureInput, response: str
    ) -> ArchitectureOutput:
        """Parse response into ArchitectureOutput."""
        architecture = self._parse_architecture_json(response)

        # Convert tech_stack dict entries to TechStackChoice objects
        tech_stack = {}
        for key, value in architecture.get("tech_stack", {}).items():
            if isinstance(value, dict):
                tech_stack[key] = TechStackChoice(
                    name=value.get("name", value.get("framework", "")),
                    justification=value.get("justification", ""),
                    alternatives=value.get("alternatives", []),
                )
            else:
                tech_stack[key] = TechStackChoice(name=str(value), justification="")

        return ArchitectureOutput(
            tech_stack=tech_stack,
            component_diagram=architecture.get("component_diagram", ""),
            api_strategy=architecture.get("api_strategy", {}),
            data_flow=architecture.get("data_flow", ""),
            deployment=architecture.get("deployment", {}),
            scalability=architecture.get("scalability", {}),
            security=architecture.get("security", {}),
            raw_response=response,
        )

    def _parse_architecture_json(self, response: str) -> dict[str, Any]:
        """Extract JSON architecture from model response."""
        try:
            # Try to extract JSON block
            if "```json" in response:
                start = response.index("```json") + 7
                end = response.index("```", start)
                json_str = response[start:end].strip()
            elif "```" in response and "{" in response:
                # Find JSON within code blocks
                match = re.search(r"```\s*\n?(\{.*?\})\s*\n?```", response, re.DOTALL)
                if match:
                    json_str = match.group(1)
                else:
                    # Fall back to finding raw JSON
                    start = response.index("{")
                    end = response.rindex("}") + 1
                    json_str = response[start:end]
            elif "{" in response:
                start = response.index("{")
                end = response.rindex("}") + 1
                json_str = response[start:end]
            else:
                return {"raw_response": response}

            return json.loads(json_str)

        except (json.JSONDecodeError, ValueError) as e:
            # Return structured fallback
            return {
                "raw_response": response,
                "parse_error": str(e),
                "tech_stack": {},
                "component_diagram": self._extract_mermaid(response),
                "api_strategy": {},
            }

    def _extract_mermaid(self, response: str) -> str:
        """Extract Mermaid diagram from response."""
        match = re.search(r"```mermaid\n(.*?)\n```", response, re.DOTALL)
        if match:
            return f"```mermaid\n{match.group(1)}\n```"
        return ""


# Convenience factory
def create_architect_agent(**kwargs) -> ArchitectAgent:
    """Create an architect agent with optional overrides."""
    return ArchitectAgent(**kwargs)
