import pytest
from tools.prompteval.core import PromptEval
from tools.prompteval.config import EvalConfig

class DummyLLM:
    def __init__(self, response):
        self._response = response
    def generate_text(self, model_name, prompt, temperature, max_tokens):
        return self._response


def run_geval_with_response(response_str):
    cfg = EvalConfig()
    pe = PromptEval(cfg)
    pe.llm_client = DummyLLM(response_str)
    return pe._run_geval("dummy content")


def test_parse_valid_integer_score():
    r = run_geval_with_response('{"reasoning":"ok","score":3}')
    assert "clarity" in r
    assert round(r["clarity"]["score"], 1) == 60.0


def test_parse_fractional_score():
    r = run_geval_with_response('{"reasoning":"fine","score":3.333}')
    assert round(r["clarity"]["score"], 2) == round(3.333 * 20.0, 2)


def test_missing_score_fallsback_to_zero():
    r = run_geval_with_response('{"reasoning":"no score"}')
    assert r["clarity"]["score"] == 0.0


def test_null_score_fallsback_to_zero():
    r = run_geval_with_response('{"reasoning":"null","score": null}')
    assert r["clarity"]["score"] == 0.0
