"""Agent Data Contracts.

Defines explicit input/output schemas for each agent to ensure
consistent context passing between workflow steps.

Each contract specifies:
- Required inputs with types
- Optional inputs with defaults
- Expected outputs with types
- Validation rules
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class FieldType(Enum):
    """Supported field types for contracts."""

    STRING = "string"
    TEXT = "text"  # Long text (prompts, code)
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    FILE = "file"
    OBJECT = "object"
    ANY = "any"


@dataclass
class FieldSpec:
    """Specification for a single input/output field."""

    name: str
    field_type: FieldType
    description: str
    required: bool = True
    default: Any = None
    example: Any = None
    # For nested types
    item_type: Optional[FieldType] = None
    nested_spec: Optional[Dict[str, "FieldSpec"]] = None


@dataclass
class AgentContract:
    """Contract defining an agent's input/output specification.

    Ensures that data passed between agents is properly formatted and
    contains all required fields.
    """

    agent_id: str
    name: str
    description: str
    inputs: Dict[str, FieldSpec] = field(default_factory=dict)
    outputs: Dict[str, FieldSpec] = field(default_factory=dict)

    def validate_inputs(self, data: Dict[str, Any]) -> List[str]:
        """Validate input data against the contract.

        Returns list of validation errors (empty if valid).
        """
        errors = []
        for field_name, spec in self.inputs.items():
            if spec.required and field_name not in data:
                errors.append(f"Missing required input: {field_name}")
            elif field_name in data:
                value = data[field_name]
                type_error = self._validate_type(value, spec)
                if type_error:
                    errors.append(f"Input {field_name}: {type_error}")
        return errors

    def validate_outputs(self, data: Dict[str, Any]) -> List[str]:
        """Validate output data against the contract.

        Returns list of validation errors (empty if valid).
        """
        errors = []
        for field_name, spec in self.outputs.items():
            if spec.required and field_name not in data:
                errors.append(f"Missing required output: {field_name}")
            elif field_name in data:
                value = data[field_name]
                type_error = self._validate_type(value, spec)
                if type_error:
                    errors.append(f"Output {field_name}: {type_error}")
        return errors

    def _validate_type(self, value: Any, spec: FieldSpec) -> Optional[str]:
        """Validate a value against its type specification."""
        if value is None:
            return None if not spec.required else "Value is None"

        type_map = {
            FieldType.STRING: str,
            FieldType.TEXT: str,
            FieldType.INTEGER: int,
            FieldType.FLOAT: (int, float),
            FieldType.BOOLEAN: bool,
            FieldType.LIST: list,
            FieldType.DICT: dict,
            FieldType.OBJECT: dict,
        }

        if spec.field_type == FieldType.ANY:
            return None

        expected_type = type_map.get(spec.field_type)
        if expected_type and not isinstance(value, expected_type):
            return f"Expected {spec.field_type.value}, got {type(value).__name__}"

        return None

    def get_example_input(self) -> Dict[str, Any]:
        """Generate example input data for documentation."""
        return {
            name: (
                spec.example
                if spec.example is not None
                else self._default_for_type(spec.field_type)
            )
            for name, spec in self.inputs.items()
        }

    def get_example_output(self) -> Dict[str, Any]:
        """Generate example output data for documentation."""
        return {
            name: (
                spec.example
                if spec.example is not None
                else self._default_for_type(spec.field_type)
            )
            for name, spec in self.outputs.items()
        }

    def _default_for_type(self, field_type: FieldType) -> Any:
        """Get a default value for a field type."""
        defaults = {
            FieldType.STRING: "",
            FieldType.TEXT: "",
            FieldType.INTEGER: 0,
            FieldType.FLOAT: 0.0,
            FieldType.BOOLEAN: False,
            FieldType.LIST: [],
            FieldType.DICT: {},
            FieldType.OBJECT: {},
            FieldType.ANY: None,
        }
        return defaults.get(field_type, None)


# =============================================================================
# Pre-defined Agent Contracts
# =============================================================================

AGENT_CONTRACTS: Dict[str, AgentContract] = {
    # Full-Stack Generation Agents
    "vision_agent": AgentContract(
        agent_id="vision_agent",
        name="Vision Agent",
        description="Analyzes UI mockups and extracts component structure",
        inputs={
            "mockup_path": FieldSpec(
                name="mockup_path",
                field_type=FieldType.FILE,
                description="Path to UI mockup image",
                required=True,
            ),
            "context": FieldSpec(
                name="context",
                field_type=FieldType.TEXT,
                description="Additional context about the mockup",
                required=False,
            ),
        },
        outputs={
            "ui_components": FieldSpec(
                name="ui_components",
                field_type=FieldType.LIST,
                description="List of identified UI components",
                item_type=FieldType.DICT,
                example=[
                    {"type": "button", "label": "Submit", "position": "bottom-right"},
                    {"type": "input", "label": "Email", "position": "center"},
                ],
            ),
            "layout_structure": FieldSpec(
                name="layout_structure",
                field_type=FieldType.DICT,
                description="Page layout structure",
                example={
                    "header": True,
                    "sidebar": False,
                    "main": True,
                    "footer": True,
                },
            ),
            "color_palette": FieldSpec(
                name="color_palette",
                field_type=FieldType.DICT,
                description="Extracted color palette",
                example={
                    "primary": "#3b82f6",
                    "secondary": "#22c55e",
                    "accent": "#f59e0b",
                },
            ),
        },
    ),
    "requirements_agent": AgentContract(
        agent_id="requirements_agent",
        name="Requirements Analyst",
        description="Parses business requirements into structured user stories",
        inputs={
            "requirements": FieldSpec(
                name="requirements",
                field_type=FieldType.TEXT,
                description="Raw business requirements text",
                required=True,
            ),
        },
        outputs={
            "user_stories": FieldSpec(
                name="user_stories",
                field_type=FieldType.LIST,
                description="Parsed user stories with acceptance criteria",
                item_type=FieldType.DICT,
                example=[
                    {
                        "id": "US001",
                        "title": "User can login",
                        "description": "As a user, I want to login so that I can access my account",
                        "acceptance_criteria": [
                            "Given valid credentials, When I login, Then I see the dashboard",
                        ],
                        "priority": "high",
                    }
                ],
            ),
            "data_entities": FieldSpec(
                name="data_entities",
                field_type=FieldType.LIST,
                description="Identified data entities and relationships",
                item_type=FieldType.DICT,
                example=[
                    {
                        "name": "User",
                        "fields": ["id", "email", "password_hash", "created_at"],
                        "relationships": [{"type": "has_many", "target": "Order"}],
                    }
                ],
            ),
            "acceptance_criteria": FieldSpec(
                name="acceptance_criteria",
                field_type=FieldType.LIST,
                description="All acceptance criteria consolidated",
                item_type=FieldType.STRING,
            ),
        },
    ),
    "architect_agent": AgentContract(
        agent_id="architect_agent",
        name="Technical Architect",
        description="Designs system architecture and tech stack",
        inputs={
            "user_stories": FieldSpec(
                name="user_stories",
                field_type=FieldType.LIST,
                description="User stories from requirements agent",
                required=True,
            ),
            "ui_components": FieldSpec(
                name="ui_components",
                field_type=FieldType.LIST,
                description="UI components from vision agent",
                required=False,
            ),
            "tech_preferences": FieldSpec(
                name="tech_preferences",
                field_type=FieldType.DICT,
                description="Optional tech stack preferences",
                required=False,
            ),
        },
        outputs={
            "tech_stack": FieldSpec(
                name="tech_stack",
                field_type=FieldType.DICT,
                description="Recommended technology stack",
                example={
                    "frontend": {"framework": "react", "language": "typescript"},
                    "backend": {"framework": "fastapi", "language": "python"},
                    "database": {"type": "postgresql", "orm": "sqlalchemy"},
                    "deployment": {"platform": "docker", "orchestration": "compose"},
                },
            ),
            "component_diagram": FieldSpec(
                name="component_diagram",
                field_type=FieldType.TEXT,
                description="Component diagram in Mermaid format",
            ),
            "api_strategy": FieldSpec(
                name="api_strategy",
                field_type=FieldType.DICT,
                description="API design strategy",
                example={
                    "style": "REST",
                    "versioning": "url",
                    "auth": "JWT",
                    "rate_limiting": True,
                },
            ),
        },
    ),
    "coder_agent": AgentContract(
        agent_id="coder_agent",
        name="Code Generator",
        description="Generates production-quality code",
        inputs={
            "spec": FieldSpec(
                name="spec",
                field_type=FieldType.DICT,
                description="Specification for code to generate (API spec, component spec, etc.)",
                required=True,
            ),
            "context": FieldSpec(
                name="context",
                field_type=FieldType.DICT,
                description="Additional context (tech stack, conventions, etc.)",
                required=False,
            ),
            "language": FieldSpec(
                name="language",
                field_type=FieldType.STRING,
                description="Target programming language",
                required=False,
                default="python",
            ),
            "framework": FieldSpec(
                name="framework",
                field_type=FieldType.STRING,
                description="Target framework",
                required=False,
            ),
        },
        outputs={
            "code": FieldSpec(
                name="code",
                field_type=FieldType.TEXT,
                description="Generated code",
            ),
            "files": FieldSpec(
                name="files",
                field_type=FieldType.DICT,
                description="Map of filename to code content",
                required=False,
            ),
            "dependencies": FieldSpec(
                name="dependencies",
                field_type=FieldType.LIST,
                description="Required dependencies",
                item_type=FieldType.STRING,
                required=False,
            ),
        },
    ),
    "reviewer_agent": AgentContract(
        agent_id="reviewer_agent",
        name="Code Reviewer",
        description="Reviews code for security and quality issues",
        inputs={
            "code": FieldSpec(
                name="code",
                field_type=FieldType.TEXT,
                description="Code to review",
                required=True,
            ),
            "context": FieldSpec(
                name="context",
                field_type=FieldType.DICT,
                description="Context about the code (language, framework, purpose)",
                required=False,
            ),
        },
        outputs={
            "issues": FieldSpec(
                name="issues",
                field_type=FieldType.LIST,
                description="List of identified issues",
                item_type=FieldType.DICT,
                example=[
                    {
                        "severity": "high",
                        "type": "security",
                        "location": "line 45",
                        "description": "SQL injection vulnerability",
                        "fix": "Use parameterized queries",
                    }
                ],
            ),
            "score": FieldSpec(
                name="score",
                field_type=FieldType.FLOAT,
                description="Overall code quality score (0-100)",
            ),
            "approved": FieldSpec(
                name="approved",
                field_type=FieldType.BOOLEAN,
                description="Whether code passes review",
            ),
            "summary": FieldSpec(
                name="summary",
                field_type=FieldType.TEXT,
                description="Human-readable review summary",
            ),
        },
    ),
    "test_agent": AgentContract(
        agent_id="test_agent",
        name="Test Generator",
        description="Generates comprehensive test suites",
        inputs={
            "code": FieldSpec(
                name="code",
                field_type=FieldType.TEXT,
                description="Code to test",
                required=True,
            ),
            "spec": FieldSpec(
                name="spec",
                field_type=FieldType.DICT,
                description="Specification of expected behavior",
                required=False,
            ),
            "language": FieldSpec(
                name="language",
                field_type=FieldType.STRING,
                description="Programming language",
                default="python",
            ),
        },
        outputs={
            "tests": FieldSpec(
                name="tests",
                field_type=FieldType.TEXT,
                description="Generated test code",
            ),
            "test_files": FieldSpec(
                name="test_files",
                field_type=FieldType.DICT,
                description="Map of test filename to content",
                required=False,
            ),
            "coverage_estimate": FieldSpec(
                name="coverage_estimate",
                field_type=FieldType.FLOAT,
                description="Estimated code coverage percentage",
                required=False,
            ),
        },
    ),
}


def get_contract(agent_id: str) -> Optional[AgentContract]:
    """Get the contract for a specific agent."""
    return AGENT_CONTRACTS.get(agent_id)


def validate_step_transition(
    from_agent: str,
    to_agent: str,
    output_data: Dict[str, Any],
    field_mapping: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Validate and transform data when passing between agents.

    Args:
        from_agent: ID of the agent producing the output
        to_agent: ID of the agent receiving the input
        output_data: Output data from the source agent
        field_mapping: Optional mapping of output fields to input fields

    Returns:
        Transformed data suitable for the target agent

    Raises:
        ValueError: If required fields are missing
    """
    from_contract = get_contract(from_agent)
    to_contract = get_contract(to_agent)

    if not to_contract:
        # No contract defined, pass through
        return output_data

    # Apply field mapping
    if field_mapping:
        mapped_data = {}
        for output_field, input_field in field_mapping.items():
            if output_field in output_data:
                mapped_data[input_field] = output_data[output_field]
        # Include unmapped fields
        for key, value in output_data.items():
            if key not in field_mapping:
                mapped_data[key] = value
        output_data = mapped_data

    # Validate against target contract
    errors = to_contract.validate_inputs(output_data)
    if errors:
        raise ValueError(f"Invalid data for {to_agent}: {'; '.join(errors)}")

    return output_data


def get_all_contracts() -> Dict[str, AgentContract]:
    """Get all defined agent contracts."""
    return AGENT_CONTRACTS.copy()
