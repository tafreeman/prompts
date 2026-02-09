"""Tests for Agent Data Contracts.

Tests the contracts module for input/output validation between agents.
"""

import pytest


class TestFieldType:
    """Test FieldType enum."""

    def test_field_type_values(self):
        """Test that all field types have correct string values."""
        from multiagent_workflows.core.contracts import FieldType

        assert FieldType.STRING.value == "string"
        assert FieldType.TEXT.value == "text"
        assert FieldType.INTEGER.value == "integer"
        assert FieldType.FLOAT.value == "float"
        assert FieldType.BOOLEAN.value == "boolean"
        assert FieldType.LIST.value == "list"
        assert FieldType.DICT.value == "dict"
        assert FieldType.FILE.value == "file"
        assert FieldType.OBJECT.value == "object"
        assert FieldType.ANY.value == "any"


class TestFieldSpec:
    """Test FieldSpec dataclass."""

    def test_field_spec_creation(self):
        """Test creating a FieldSpec."""
        from multiagent_workflows.core.contracts import FieldSpec, FieldType

        spec = FieldSpec(
            name="test_field",
            field_type=FieldType.STRING,
            description="A test field",
            required=True,
        )

        assert spec.name == "test_field"
        assert spec.field_type == FieldType.STRING
        assert spec.description == "A test field"
        assert spec.required is True
        assert spec.default is None
        assert spec.example is None

    def test_field_spec_with_defaults(self):
        """Test FieldSpec with default values."""
        from multiagent_workflows.core.contracts import FieldSpec, FieldType

        spec = FieldSpec(
            name="optional_field",
            field_type=FieldType.INTEGER,
            description="An optional integer",
            required=False,
            default=42,
            example=100,
        )

        assert spec.required is False
        assert spec.default == 42
        assert spec.example == 100

    def test_field_spec_with_nested_type(self):
        """Test FieldSpec with nested types."""
        from multiagent_workflows.core.contracts import FieldSpec, FieldType

        spec = FieldSpec(
            name="items",
            field_type=FieldType.LIST,
            description="A list of dictionaries",
            item_type=FieldType.DICT,
        )

        assert spec.field_type == FieldType.LIST
        assert spec.item_type == FieldType.DICT


class TestAgentContract:
    """Test AgentContract class."""

    @pytest.fixture
    def sample_contract(self):
        """Create a sample contract for testing."""
        from multiagent_workflows.core.contracts import (
            AgentContract,
            FieldSpec,
            FieldType,
        )

        return AgentContract(
            agent_id="test_agent",
            name="Test Agent",
            description="An agent for testing",
            inputs={
                "required_input": FieldSpec(
                    name="required_input",
                    field_type=FieldType.STRING,
                    description="A required string input",
                    required=True,
                ),
                "optional_input": FieldSpec(
                    name="optional_input",
                    field_type=FieldType.INTEGER,
                    description="An optional integer input",
                    required=False,
                    default=0,
                ),
            },
            outputs={
                "result": FieldSpec(
                    name="result",
                    field_type=FieldType.DICT,
                    description="The result dictionary",
                    required=True,
                ),
            },
        )

    def test_contract_creation(self, sample_contract):
        """Test creating an AgentContract."""
        assert sample_contract.agent_id == "test_agent"
        assert sample_contract.name == "Test Agent"
        assert len(sample_contract.inputs) == 2
        assert len(sample_contract.outputs) == 1

    def test_validate_inputs_valid(self, sample_contract):
        """Test validating valid inputs."""
        errors = sample_contract.validate_inputs(
            {
                "required_input": "test value",
                "optional_input": 42,
            }
        )

        assert len(errors) == 0

    def test_validate_inputs_missing_required(self, sample_contract):
        """Test validation fails for missing required input."""
        errors = sample_contract.validate_inputs(
            {
                "optional_input": 42,
            }
        )

        assert len(errors) == 1
        assert "Missing required input: required_input" in errors[0]

    def test_validate_inputs_wrong_type(self, sample_contract):
        """Test validation fails for wrong type."""
        errors = sample_contract.validate_inputs(
            {
                "required_input": 123,  # Should be string, not int
                "optional_input": 42,
            }
        )

        assert len(errors) == 1
        assert "Expected string" in errors[0]

    def test_validate_inputs_optional_missing(self, sample_contract):
        """Test validation passes when optional input is missing."""
        errors = sample_contract.validate_inputs(
            {
                "required_input": "test value",
            }
        )

        assert len(errors) == 0

    def test_validate_outputs_valid(self, sample_contract):
        """Test validating valid outputs."""
        errors = sample_contract.validate_outputs(
            {
                "result": {"key": "value"},
            }
        )

        assert len(errors) == 0

    def test_validate_outputs_missing(self, sample_contract):
        """Test validation fails for missing required output."""
        errors = sample_contract.validate_outputs({})

        assert len(errors) == 1
        assert "Missing required output: result" in errors[0]

    def test_validate_type_any(self):
        """Test that ANY type accepts any value."""
        from multiagent_workflows.core.contracts import (
            AgentContract,
            FieldSpec,
            FieldType,
        )

        contract = AgentContract(
            agent_id="any_test",
            name="Any Test",
            description="Test ANY type",
            inputs={
                "data": FieldSpec(
                    name="data",
                    field_type=FieldType.ANY,
                    description="Any data",
                    required=True,
                ),
            },
        )

        # Should accept any type
        assert len(contract.validate_inputs({"data": "string"})) == 0
        assert len(contract.validate_inputs({"data": 123})) == 0
        assert len(contract.validate_inputs({"data": [1, 2, 3]})) == 0
        assert len(contract.validate_inputs({"data": {"key": "value"}})) == 0

    def test_get_example_input(self, sample_contract):
        """Test generating example input."""
        example = sample_contract.get_example_input()

        assert "required_input" in example
        assert "optional_input" in example
        # Default for STRING is empty string
        assert example["required_input"] == ""
        # Default for INTEGER is 0
        assert example["optional_input"] == 0

    def test_get_example_output(self, sample_contract):
        """Test generating example output."""
        example = sample_contract.get_example_output()

        assert "result" in example
        # Default for DICT is empty dict
        assert example["result"] == {}


class TestPredefinedContracts:
    """Test pre-defined agent contracts."""

    def test_get_contract(self):
        """Test retrieving a contract by agent ID."""
        from multiagent_workflows.core.contracts import get_contract

        contract = get_contract("vision_agent")

        assert contract is not None
        assert contract.agent_id == "vision_agent"
        assert "mockup_path" in contract.inputs

    def test_get_contract_not_found(self):
        """Test retrieving non-existent contract returns None."""
        from multiagent_workflows.core.contracts import get_contract

        contract = get_contract("nonexistent_agent")
        assert contract is None

    def test_get_all_contracts(self):
        """Test retrieving all contracts."""
        from multiagent_workflows.core.contracts import get_all_contracts

        contracts = get_all_contracts()

        assert isinstance(contracts, dict)
        assert len(contracts) > 0
        assert "vision_agent" in contracts
        assert "requirements_agent" in contracts

    def test_requirements_agent_contract(self):
        """Test requirements agent contract structure."""
        from multiagent_workflows.core.contracts import get_contract

        contract = get_contract("requirements_agent")

        assert contract is not None
        assert "requirements" in contract.inputs
        assert "user_stories" in contract.outputs
        assert "data_entities" in contract.outputs

    def test_architect_agent_contract(self):
        """Test architect agent contract structure."""
        from multiagent_workflows.core.contracts import get_contract

        contract = get_contract("architect_agent")

        assert contract is not None
        assert "user_stories" in contract.inputs
        assert "tech_stack" in contract.outputs
        assert "component_diagram" in contract.outputs


class TestStepTransitionValidation:
    """Test validation when passing data between agents."""

    def test_validate_step_transition(self):
        """Test validating data when transitioning between steps."""
        from multiagent_workflows.core.contracts import validate_step_transition

        output_data = {
            "user_stories": [{"id": "US001", "title": "Login"}],
            "data_entities": [{"name": "User"}],
        }

        # Should pass through with validation
        result = validate_step_transition(
            from_agent="requirements_agent",
            to_agent="architect_agent",
            output_data=output_data,
        )

        assert "user_stories" in result

    def test_validate_step_transition_with_mapping(self):
        """Test field mapping during transition."""
        from multiagent_workflows.core.contracts import validate_step_transition

        output_data = {
            "stories": [{"id": "US001"}],  # Different key name
        }

        # Map output field to expected input field
        result = validate_step_transition(
            from_agent="custom_agent",
            to_agent="architect_agent",
            output_data=output_data,
            field_mapping={"stories": "user_stories"},
        )

        assert "user_stories" in result

    def test_validate_step_transition_unknown_target(self):
        """Test transition to unknown agent passes through."""
        from multiagent_workflows.core.contracts import validate_step_transition

        output_data = {"any_key": "any_value"}

        # Should pass through when target contract is unknown
        result = validate_step_transition(
            from_agent="any",
            to_agent="unknown_agent",
            output_data=output_data,
        )

        assert result == output_data
