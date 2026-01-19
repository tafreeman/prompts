from tools.llm.local_model import LocalModel


def test_parse_geval_criterion_null_score_does_not_crash():
    # Bypass __init__ to avoid requiring local ONNX model availability.
    m = LocalModel.__new__(LocalModel)

    parsed = m._parse_geval_criterion(
        '{"reasoning": ["ok"], "score": null, "summary": "x"}'
    )

    assert parsed is not None
    assert parsed["score"] == 0.0
    assert parsed["summary"] == "x"
    assert parsed["reasoning"] == ["ok"]
