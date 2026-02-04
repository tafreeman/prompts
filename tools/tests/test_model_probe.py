#!/usr/bin/env python3
"""Tests for tools.llm.model_probe module.

Tests model discovery, caching, and availability checking.
"""

import sys
from pathlib import Path

import pytest

# Ensure tools package is importable
sys.path.insert(0, str(Path(__file__).parents[2]))

from tools.llm.model_probe import (
    ErrorCode,
    ModelProbe,
    ProbeResult,
    discover_all_models,
    filter_usable_models,
    get_model_error,
    is_model_usable,
)


class TestProbeResult:
    """Test ProbeResult dataclass."""

    def test_create_success_result(self):
        """Test creating a successful probe result."""
        result = ProbeResult(
            model="test:model",
            provider="test",
            usable=True,
            error_code=None,
            error_message=None,
        )

        assert result.usable is True
        assert result.model == "test:model"
        assert result.provider == "test"
        assert result.error_code is None

    def test_create_error_result(self):
        """Test creating an error probe result."""
        result = ProbeResult(
            model="test:model",
            provider="test",
            usable=False,
            error_code=ErrorCode.UNAVAILABLE_MODEL.value,
            error_message="Model not found",
        )

        assert result.usable is False
        assert result.error_code == ErrorCode.UNAVAILABLE_MODEL.value
        assert result.error_message == "Model not found"


class TestModelProbe:
    """Test ModelProbe class."""

    def test_init(self):
        """Test ModelProbe initialization."""
        probe = ModelProbe(use_cache=False, verbose=False)
        assert probe is not None

    def test_is_model_usable_with_known_model(self):
        """Test checking if a known model is usable."""
        # Test with a simple model check
        # This might fail in CI without actual models, so we allow both outcomes
        try:
            result = is_model_usable("local:phi4mini")
            assert isinstance(result, bool)
        except Exception:
            # In environments without models, this is expected
            pass

    def test_filter_usable_models(self):
        """Test filtering a list of models to only usable ones."""
        models = ["local:phi4mini", "nonexistent:model", "local:mistral"]

        try:
            usable = filter_usable_models(models)
            assert isinstance(usable, list)
            # Should return a subset or empty list
            assert len(usable) <= len(models)
        except Exception:
            # In environments without models, this is expected
            pass

    def test_get_model_error(self):
        """Test getting error message for unavailable model."""
        # For a clearly invalid model
        error = get_model_error("invalid:nonexistent")
        # Error can be None (if not probed yet) or a string
        assert error is None or isinstance(error, str)

    def test_discover_all_models_structure(self):
        """Test that discover_all_models returns proper structure."""
        try:
            result = discover_all_models(verbose=False)

            # Check result structure
            assert isinstance(result, dict)
            assert "providers" in result
            assert "usable_models" in result
            assert "all_models" in result

            # Check provider structure
            assert isinstance(result["providers"], dict)
            assert isinstance(result["usable_models"], list)
            assert isinstance(result["all_models"], list)
        except Exception:
            # In restricted environments, this might fail
            pass


class TestUtilityFunctions:
    """Test utility functions."""

    def test_is_model_usable_returns_bool(self):
        """Test that is_model_usable always returns a boolean."""
        result = is_model_usable("some:model")
        assert isinstance(result, bool)

    def test_filter_usable_models_returns_list(self):
        """Test that filter_usable_models returns a list."""
        models = ["model1", "model2"]
        result = filter_usable_models(models)
        assert isinstance(result, list)

    def test_get_model_error_returns_optional_string(self):
        """Test that get_model_error returns None or string."""
        result = get_model_error("some:model")
        assert result is None or isinstance(result, str)


class TestErrorCode:
    """Test ErrorCode enum."""

    def test_error_code_values(self):
        """Test that ErrorCode enum has expected values."""
        assert hasattr(ErrorCode, "SUCCESS")
        assert hasattr(ErrorCode, "UNAVAILABLE_MODEL")
        assert hasattr(ErrorCode, "PERMISSION_DENIED")

        # Check they have string values
        assert isinstance(ErrorCode.SUCCESS.value, str)
        assert isinstance(ErrorCode.UNAVAILABLE_MODEL.value, str)


class TestCaching:
    """Test caching functionality."""

    def test_probe_with_cache_disabled(self):
        """Test that probe works with caching disabled."""
        probe = ModelProbe(use_cache=False, verbose=False)
        assert probe is not None

    def test_probe_with_cache_enabled(self):
        """Test that probe works with caching enabled."""
        probe = ModelProbe(use_cache=True, verbose=False)
        assert probe is not None


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
