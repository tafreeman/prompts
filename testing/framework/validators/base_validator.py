"""Base validator class and common validation utilities."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class BaseValidator(ABC):
    """Base class for all validators."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize validator with optional configuration."""
        self.config = config or {}
        self.validation_errors = []
        self.validation_warnings = []

    @abstractmethod
    async def validate(self, output: Any, expected: Optional[Any] = None) -> bool:
        """Validate output against expected result.

        Args:
            output: The actual output to validate
            expected: Optional expected output for comparison

        Returns:
            bool: True if validation passes, False otherwise
        """
        pass

    def add_error(self, message: str):
        """Add validation error."""
        self.validation_errors.append(message)
        logger.error(f"Validation error: {message}")

    def add_warning(self, message: str):
        """Add validation warning."""
        self.validation_warnings.append(message)
        logger.warning(f"Validation warning: {message}")

    def clear_messages(self):
        """Clear all validation messages."""
        self.validation_errors = []
        self.validation_warnings = []

    def get_validation_report(self) -> Dict[str, Any]:
        """Get detailed validation report."""
        return {
            "errors": self.validation_errors.copy(),
            "warnings": self.validation_warnings.copy(),
            "error_count": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
            "is_valid": len(self.validation_errors) == 0,
        }

    def _deep_compare(self, actual: Any, expected: Any, path: str = "") -> bool:
        """Deep comparison of nested structures.

        Args:
            actual: Actual value
            expected: Expected value
            path: Current path in nested structure (for error messages)

        Returns:
            bool: True if structures match
        """
        if isinstance(expected, dict) and isinstance(actual, dict):
            for key, value in expected.items():
                if key not in actual:
                    self.add_error(f"Missing key at {path}.{key}")
                    return False
                if not self._deep_compare(actual[key], value, f"{path}.{key}"):
                    return False
            return True

        elif isinstance(expected, list) and isinstance(actual, list):
            if len(expected) != len(actual):
                self.add_error(
                    f"List length mismatch at {path}: expected {len(expected)}, got {len(actual)}"
                )
                return False
            for i, (exp_item, act_item) in enumerate(zip(expected, actual)):
                if not self._deep_compare(act_item, exp_item, f"{path}[{i}]"):
                    return False
            return True

        else:
            if actual != expected:
                self.add_error(
                    f"Value mismatch at {path}: expected {expected}, got {actual}"
                )
                return False
            return True

    def _contains_all(self, output: str, required_items: List[str]) -> bool:
        """Check if output contains all required items."""
        missing = []
        for item in required_items:
            if item not in output:
                missing.append(item)

        if missing:
            self.add_error(f"Output missing required items: {missing}")
            return False
        return True

    def _matches_pattern(self, text: str, pattern: str) -> bool:
        """Check if text matches a pattern."""
        import re

        try:
            return bool(re.search(pattern, text))
        except re.error as e:
            self.add_error(f"Invalid regex pattern: {e}")
            return False
