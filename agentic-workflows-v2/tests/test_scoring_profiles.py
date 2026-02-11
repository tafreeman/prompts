"""Tests for scoring profile templates."""

from __future__ import annotations

import pytest

from agentic_v2.server.scoring_profiles import SCORING_PROFILES, get_profile


def test_profile_a_weights_sum_to_one():
    profile = SCORING_PROFILES["A"]
    assert sum(profile.weights.values()) == pytest.approx(1.0, abs=0.01)


def test_profile_b_weights_correct():
    profile = SCORING_PROFILES["B"]
    assert profile.weights["correctness_rubric"] == pytest.approx(0.35)


def test_get_unknown_profile_fallback():
    fallback = get_profile("does_not_exist")
    assert fallback.profile_id == "B"


def test_profile_extra_gates_included():
    profile = SCORING_PROFILES["A"]
    assert "fail_to_pass" in profile.extra_gates

