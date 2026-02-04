"""Test the updated unified_scorer with example-anchored evaluation."""

from tools.prompteval.unified_scorer import (
    _extract_choice_scores,
    _parse_standard_response,
)


def test_json_parse():
    """Test basic JSON parsing."""
    json_test = (
        '{"scores": {"clarity": 8, "effectiveness": 7}, "improvements": ["test"]}'
    )
    result = _parse_standard_response(json_test)
    assert result is not None
    assert result["scores"]["clarity"] == 8
    assert result["scores"]["effectiveness"] == 7
    print(f"✅ JSON parse: {result}")


def test_choice_extraction():
    """Test choice-based score extraction (gh-models pattern)."""
    choice_test = "[Clarity: 8] [Effectiveness: 7] [Structure: 6] [Specificity: 5] [Completeness: 9]"
    result = _extract_choice_scores(choice_test)
    assert result is not None
    assert result["clarity"] == 8
    assert result["effectiveness"] == 7
    assert result["structure"] == 6
    assert result["specificity"] == 5
    assert result["completeness"] == 9
    print(f"✅ Choice extract: {result}")


def test_choice_extraction_markdown():
    """Test choice extraction from markdown format."""
    md_test = "**Clarity**: 9\n**Effectiveness**: 8\n**Structure**: 7\n**Specificity**: 6\n**Completeness**: 8"
    result = _extract_choice_scores(md_test)
    assert result is not None
    assert result["clarity"] == 9
    print(f"✅ Markdown choice extract: {result}")


def test_new_format_with_thoughtchain():
    """Test new format with thoughtchain and justifications."""
    new_format = """```json
{
  "thoughtchain": "This prompt has good clarity matching the 8 anchor.",
  "scores": {"clarity": 8, "effectiveness": 7, "structure": 6, "specificity": 7, "completeness": 6},
  "justifications": {"clarity": "Clear like the example."},
  "improvements": ["Add examples"],
  "confidence": 0.9
}
```"""
    result = _parse_standard_response(new_format)
    assert result is not None
    assert "thoughtchain" in result
    assert result["scores"]["clarity"] == 8
    assert result["confidence"] == 0.9
    print(
        f"✅ New format with thoughtchain: preserved={result.get('thoughtchain', '')[:40]}..."
    )


def test_fallback_to_choice():
    """Test that invalid JSON falls back to choice extraction."""
    invalid_json_with_choices = "Invalid JSON but [Clarity: 7] [Effectiveness: 6] [Structure: 5] [Specificity: 8] [Completeness: 7]"
    result = _parse_standard_response(invalid_json_with_choices)
    assert result is not None
    assert result["scores"]["clarity"] == 7
    assert result["confidence"] == 0.7  # Lower confidence for choice extraction
    print(f"✅ Fallback to choice: {result}")


def test_parse_with_leading_text_and_braces():
    """Parser should ignore non-JSON braces and find the correct JSON
    object."""
    response = (
        "Thoughts: this is not JSON {just braces} and more text.\n"
        "Here are the results:\n"
        '{"scores": {"clarity": 6, "effectiveness": 7, "structure": 8, "specificity": 5, "completeness": 6}, '
        '"improvements": ["Add examples"], "confidence": 0.8}\n'
        "(end)"
    )
    result = _parse_standard_response(response)
    assert result is not None
    assert result["scores"]["structure"] == 8


def test_parse_unlabeled_code_fence():
    """Models sometimes return ``` ...

    ``` without a json language tag.
    """
    response = """Here you go:
```
{"scores": {"clarity": 9, "effectiveness": 8, "structure": 8, "specificity": 7, "completeness": 8}, "improvements": [], "confidence": 0.9}
```
"""
    result = _parse_standard_response(response)
    assert result is not None
    assert result["scores"]["clarity"] == 9


def test_parse_multiple_json_objects_prefers_scores_schema():
    """If multiple JSON objects appear, prefer the one matching the scores
    schema."""
    response = (
        'debug={"a":1}\n'
        "{"  # start a non-matching object
        '"a": 1'
        "}\n"
        "{"  # now the real one
        '"scores": {"clarity": 8, "effectiveness": 7, "structure": 6, "specificity": 7, "completeness": 6},'
        '"improvements": ["Tighten constraints"],'
        '"confidence": 0.7'
        "}"
    )
    result = _parse_standard_response(response)
    assert result is not None
    assert result["scores"]["clarity"] == 8


if __name__ == "__main__":
    test_json_parse()
    test_choice_extraction()
    test_choice_extraction_markdown()
    test_new_format_with_thoughtchain()
    test_fallback_to_choice()
    test_parse_with_leading_text_and_braces()
    test_parse_unlabeled_code_fence()
    test_parse_multiple_json_objects_prefers_scores_schema()
    print("\n✅ All tests passed!")
