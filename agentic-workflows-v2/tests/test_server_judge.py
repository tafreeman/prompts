"""Tests for LLM-as-judge protocol helpers."""

from __future__ import annotations

from agentic_v2.server.judge import (
    JudgeCriterionDefinition,
    LLMJudge,
    evaluate_calibration_set,
    validate_judge_structured_output,
)


def _criteria() -> list[JudgeCriterionDefinition]:
    return [
        JudgeCriterionDefinition(
            name="correctness",
            definition="Task correctness",
            scale={"1": "bad", "3": "ok", "5": "excellent"},
        ),
        JudgeCriterionDefinition(
            name="completeness",
            definition="Coverage of requirements",
            scale={"1": "missing", "3": "partial", "5": "complete"},
        ),
    ]


def test_judge_structured_output_schema():
    valid_payload = {
        "criteria": [
            {"name": "correctness", "score": 4, "evidence": "good mapping"},
            {"name": "completeness", "score": 3, "evidence": "covers most requirements"},
        ]
    }
    ok, errors = validate_judge_structured_output(
        valid_payload,
        expected_criteria={"correctness", "completeness"},
    )
    assert ok is True
    assert errors == []

    bad_payload = {"criteria": [{"name": "correctness", "score": 8}]}
    ok_bad, bad_errors = validate_judge_structured_output(
        bad_payload,
        expected_criteria={"correctness", "completeness"},
    )
    assert ok_bad is False
    assert bad_errors


def test_judge_swapped_order_consistency():
    def _provider(*, prompt: str, model: str, temperature: float):
        if "SWAPPED_ORDER" in prompt:
            return {
                "criteria": [
                    {"name": "correctness", "score": 4, "evidence": "swapped still close"},
                    {"name": "completeness", "score": 3, "evidence": "swapped still close"},
                ]
            }
        return {
            "criteria": [
                {"name": "correctness", "score": 5, "evidence": "forward score"},
                {"name": "completeness", "score": 4, "evidence": "forward score"},
            ]
        }

    judge = LLMJudge(response_provider=_provider, model_version="mock-judge-swap")
    result = judge.evaluate(
        candidate_output="candidate output",
        expected_output="expected output",
        pairwise_reference_output="baseline output",
        criteria=_criteria(),
    )
    assert result.pairwise_consistent is True
    assert result.inconsistency_reasons == []


def test_judge_calibration_within_tolerance():
    def _provider(*, prompt: str, model: str, temperature: float):
        return {
            "criteria": [
                {"name": "correctness", "score": 4.0, "evidence": "close to human"},
                {"name": "completeness", "score": 3.5, "evidence": "close to human"},
            ]
        }

    judge = LLMJudge(response_provider=_provider, model_version="mock-judge-calibration")
    report = evaluate_calibration_set(
        judge=judge,
        fixtures=[
            {
                "candidate_output": "candidate 1",
                "expected_output": "expected 1",
                "criteria": _criteria(),
                "human_scores": {"correctness": 4.0, "completeness": 3.0},
            },
            {
                "candidate_output": "candidate 2",
                "expected_output": "expected 2",
                "criteria": _criteria(),
                "human_scores": {"correctness": 4.0, "completeness": 4.0},
            },
        ],
        tolerance=0.5,
    )
    assert report["within_tolerance"] is True
    assert report["mae"] <= 0.5


def test_judge_logs_model_version():
    def _provider(*, prompt: str, model: str, temperature: float):
        return {
            "criteria": [
                {"name": "correctness", "score": 4, "evidence": "solid"},
                {"name": "completeness", "score": 4, "evidence": "solid"},
            ]
        }

    judge = LLMJudge(
        response_provider=_provider,
        model="gh:openai/o3-mini",
        model_version="o3-mini-2026-02-01",
        prompt_version="judge-v1.2",
        temperature=0.1,
    )
    result = judge.evaluate(
        candidate_output="candidate",
        expected_output="expected",
        criteria=_criteria(),
    )
    payload = result.to_payload()
    assert payload["model"] == "gh:openai/o3-mini"
    assert payload["model_version"] == "o3-mini-2026-02-01"
    assert payload["prompt_version"] == "judge-v1.2"
    assert payload["temperature"] == 0.1
