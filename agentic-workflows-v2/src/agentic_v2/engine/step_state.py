"""Step lifecycle state machine."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class StepState(str, Enum):
    """Lifecycle states for a workflow step."""

    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    RETRYING = "retrying"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


_ALLOWED_TRANSITIONS: dict[StepState, set[StepState]] = {
    StepState.PENDING: {StepState.READY, StepState.SKIPPED},
    StepState.READY: {StepState.RUNNING, StepState.CANCELLED},
    StepState.RUNNING: {
        StepState.SUCCESS,
        StepState.FAILED,
        StepState.RETRYING,
        StepState.SKIPPED,
        StepState.CANCELLED,
    },
    StepState.RETRYING: {StepState.RUNNING, StepState.FAILED, StepState.CANCELLED},
    StepState.SUCCESS: set(),
    StepState.FAILED: set(),
    StepState.SKIPPED: set(),
    StepState.CANCELLED: set(),
}


@dataclass
class StepStateManager:
    """Track and validate step state transitions."""

    _states: dict[str, StepState] = field(default_factory=dict)

    def get_state(self, step_name: str) -> StepState:
        """Get current state for a step (default: PENDING)."""
        return self._states.get(step_name, StepState.PENDING)

    def set_state(self, step_name: str, new_state: StepState) -> StepState:
        """Set state without validation (use with caution)."""
        self._states[step_name] = new_state
        return new_state

    def transition(self, step_name: str, new_state: StepState) -> StepState:
        """Transition to a new state, validating the state machine."""
        current = self.get_state(step_name)
        if not self.can_transition(current, new_state):
            raise ValueError(
                f"Invalid transition {current.value} -> {new_state.value} for {step_name}"
            )
        self._states[step_name] = new_state
        return new_state

    def can_transition(self, current: StepState, new_state: StepState) -> bool:
        """Check whether a transition is allowed."""
        return new_state in _ALLOWED_TRANSITIONS.get(current, set())

    def reset(self, step_name: str) -> None:
        """Reset a step to PENDING."""
        self._states.pop(step_name, None)
