"""Test the updated unified_scorer with example-anchored evaluation."""

from tools.prompteval.unified_scorer import (
    _parse_standard_response,
    _extract_choice_scores,
    _normalize_standard_result,
)


def test_json_parse():
    """Test basic JSON parsing."""
    json_test = '{"scores": {"clarity": 8, "effectiveness": 7}, "improvements": ["test"]}'
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
    new_format = '''```json
{
  "thoughtchain": "This prompt has good clarity matching the 8 anchor.",
  "scores": {"clarity": 8, "effectiveness": 7, "structure": 6, "specificity": 7, "completeness": 6},
  "justifications": {"clarity": "Clear like the example."},
  "improvements": ["Add examples"],
  "confidence": 0.9
}
```'''
    result = _parse_standard_response(new_format)
    assert result is not None
    assert "thoughtchain" in result
    assert result["scores"]["clarity"] == 8
    assert result["confidence"] == 0.9
    print(f"✅ New format with thoughtchain: preserved={result.get('thoughtchain', '')[:40]}...")


def test_fallback_to_choice():
    """Test that invalid JSON falls back to choice extraction."""
    invalid_json_with_choices = "Invalid JSON but [Clarity: 7] [Effectiveness: 6] [Structure: 5] [Specificity: 8] [Completeness: 7]"
    result = _parse_standard_response(invalid_json_with_choices)
    assert result is not None
    assert result["scores"]["clarity"] == 7
    assert result["confidence"] == 0.7  # Lower confidence for choice extraction
    print(f"✅ Fallback to choice: {result}")


if __name__ == "__main__":
    test_json_parse()
    test_choice_extraction()
    test_choice_extraction_markdown()
    test_new_format_with_thoughtchain()
    test_fallback_to_choice()
    print("\n✅ All tests passed!")
