"""Tests for W3-FL-001: feature flags."""

from __future__ import annotations

import pytest

from agentic_v2.engine import DagOnceStrategy, IterativeRepairStrategy, create_execution_strategy
from agentic_v2.feature_flags import FeatureFlags, load_feature_flags, reset_flags


@pytest.fixture(autouse=True)
def _reset_global_flags():
    """Ensure the global singleton is clean for each test."""
    reset_flags()
    yield
    reset_flags()


def test_feature_flag_disabled_hides_feature():
    """With iterative_strategy=False, requesting iterative falls back to dag_once."""
    # Default flags have iterative_strategy=False
    strategy = create_execution_strategy({"strategy": "iterative_repair", "max_attempts": 3})
    assert isinstance(strategy, DagOnceStrategy)


def test_feature_flag_enabled_exposes_feature(monkeypatch):
    """With iterative_strategy=True, iterative strategy is returned."""
    monkeypatch.setenv("AGENTIC_FF_ITERATIVE_STRATEGY", "true")
    strategy = create_execution_strategy({"strategy": "iterative_repair", "max_attempts": 3})
    assert isinstance(strategy, IterativeRepairStrategy)


def test_feature_flag_env_override(monkeypatch):
    """Env var AGENTIC_FF_DOCKER_RUNTIME=true overrides the default."""
    monkeypatch.setenv("AGENTIC_FF_DOCKER_RUNTIME", "true")
    flags = load_feature_flags()
    assert flags.docker_runtime is True
    # Others remain default
    assert flags.iterative_strategy is False


def test_feature_flags_all_defaults():
    """All flags default to False."""
    flags = FeatureFlags()
    assert flags.iterative_strategy is False
    assert flags.per_agent_scoring is False
    assert flags.microsoft_adapter is False
    assert flags.docker_runtime is False


def test_feature_flags_from_yaml(tmp_path):
    """Flags can be loaded from a YAML config file."""
    config = tmp_path / "flags.yaml"
    config.write_text(
        "feature_flags:\n  iterative_strategy: true\n  docker_runtime: false\n",
        encoding="utf-8",
    )
    flags = load_feature_flags(config)
    assert flags.iterative_strategy is True
    assert flags.docker_runtime is False
    assert flags.per_agent_scoring is False
