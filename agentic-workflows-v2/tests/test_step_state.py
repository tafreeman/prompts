"""Tests for StepState lifecycle state machine.

Covers:
- State transitions
- Valid/invalid transition validation
- State manager operations
"""

import pytest
from agentic_v2.engine.step_state import StepState, StepStateManager


class TestStepState:
    """Tests for the StepState enum."""

    def test_state_values(self):
        """All expected states exist with correct values."""
        assert StepState.PENDING.value == "pending"
        assert StepState.READY.value == "ready"
        assert StepState.RUNNING.value == "running"
        assert StepState.RETRYING.value == "retrying"
        assert StepState.SUCCESS.value == "success"
        assert StepState.FAILED.value == "failed"
        assert StepState.SKIPPED.value == "skipped"
        assert StepState.CANCELLED.value == "cancelled"

    def test_state_is_string_enum(self):
        """StepState inherits from str for JSON serialization."""
        assert isinstance(StepState.PENDING, str)
        assert StepState.PENDING == "pending"


class TestStepStateManager:
    """Tests for the StepStateManager."""

    def test_get_state_default_pending(self):
        """Unknown steps default to PENDING state."""
        manager = StepStateManager()
        assert manager.get_state("unknown_step") == StepState.PENDING

    def test_set_state_bypasses_validation(self):
        """set_state bypasses transition validation."""
        manager = StepStateManager()
        # This would be invalid via transition(), but set_state allows it
        manager.set_state("step1", StepState.SUCCESS)
        assert manager.get_state("step1") == StepState.SUCCESS

    def test_valid_transition_pending_to_ready(self):
        """PENDING → READY is a valid transition."""
        manager = StepStateManager()
        result = manager.transition("step1", StepState.READY)
        assert result == StepState.READY
        assert manager.get_state("step1") == StepState.READY

    def test_valid_transition_ready_to_running(self):
        """READY → RUNNING is a valid transition."""
        manager = StepStateManager()
        manager.transition("step1", StepState.READY)
        result = manager.transition("step1", StepState.RUNNING)
        assert result == StepState.RUNNING

    def test_valid_transition_running_to_success(self):
        """RUNNING → SUCCESS is a valid transition."""
        manager = StepStateManager()
        manager.transition("step1", StepState.READY)
        manager.transition("step1", StepState.RUNNING)
        result = manager.transition("step1", StepState.SUCCESS)
        assert result == StepState.SUCCESS

    def test_valid_transition_running_to_failed(self):
        """RUNNING → FAILED is a valid transition."""
        manager = StepStateManager()
        manager.transition("step1", StepState.READY)
        manager.transition("step1", StepState.RUNNING)
        result = manager.transition("step1", StepState.FAILED)
        assert result == StepState.FAILED

    def test_valid_transition_running_to_retrying(self):
        """RUNNING → RETRYING is a valid transition."""
        manager = StepStateManager()
        manager.transition("step1", StepState.READY)
        manager.transition("step1", StepState.RUNNING)
        result = manager.transition("step1", StepState.RETRYING)
        assert result == StepState.RETRYING

    def test_valid_transition_retrying_to_running(self):
        """RETRYING → RUNNING is a valid transition (retry attempt)."""
        manager = StepStateManager()
        manager.transition("step1", StepState.READY)
        manager.transition("step1", StepState.RUNNING)
        manager.transition("step1", StepState.RETRYING)
        result = manager.transition("step1", StepState.RUNNING)
        assert result == StepState.RUNNING

    def test_valid_transition_pending_to_skipped(self):
        """PENDING → SKIPPED is valid (condition not met)."""
        manager = StepStateManager()
        result = manager.transition("step1", StepState.SKIPPED)
        assert result == StepState.SKIPPED

    def test_invalid_transition_pending_to_success(self):
        """PENDING → SUCCESS is invalid (must go through RUNNING)."""
        manager = StepStateManager()
        with pytest.raises(ValueError, match="Invalid transition"):
            manager.transition("step1", StepState.SUCCESS)

    def test_invalid_transition_success_to_anything(self):
        """SUCCESS is terminal - no transitions allowed."""
        manager = StepStateManager()
        manager.set_state("step1", StepState.SUCCESS)
        with pytest.raises(ValueError, match="Invalid transition"):
            manager.transition("step1", StepState.RUNNING)

    def test_invalid_transition_failed_to_anything(self):
        """FAILED is terminal - no transitions allowed."""
        manager = StepStateManager()
        manager.set_state("step1", StepState.FAILED)
        with pytest.raises(ValueError, match="Invalid transition"):
            manager.transition("step1", StepState.RUNNING)

    def test_can_transition_true(self):
        """can_transition returns True for valid transitions."""
        manager = StepStateManager()
        assert manager.can_transition(StepState.PENDING, StepState.READY) is True
        assert manager.can_transition(StepState.READY, StepState.RUNNING) is True
        assert manager.can_transition(StepState.RUNNING, StepState.SUCCESS) is True

    def test_can_transition_false(self):
        """can_transition returns False for invalid transitions."""
        manager = StepStateManager()
        assert manager.can_transition(StepState.PENDING, StepState.SUCCESS) is False
        assert manager.can_transition(StepState.SUCCESS, StepState.RUNNING) is False
        assert manager.can_transition(StepState.FAILED, StepState.SUCCESS) is False

    def test_reset_clears_state(self):
        """Reset returns step to PENDING."""
        manager = StepStateManager()
        manager.set_state("step1", StepState.SUCCESS)
        manager.reset("step1")
        assert manager.get_state("step1") == StepState.PENDING

    def test_reset_nonexistent_step_no_error(self):
        """Reset on nonexistent step doesn't raise."""
        manager = StepStateManager()
        manager.reset("never_existed")  # Should not raise
        assert manager.get_state("never_existed") == StepState.PENDING

    def test_multiple_steps_independent(self):
        """Different steps have independent state."""
        manager = StepStateManager()
        manager.transition("step1", StepState.READY)
        manager.transition("step2", StepState.SKIPPED)

        assert manager.get_state("step1") == StepState.READY
        assert manager.get_state("step2") == StepState.SKIPPED
        assert manager.get_state("step3") == StepState.PENDING
