"""Tests for pattern evaluation modules.

Tests the parser, evaluator, and integration components.
"""

import pytest

from tools.prompteval.failures import FailureMode, FailureReport, PatternFailureSummary
from tools.prompteval.mutations import (
    ContentInjectMutator,
    MutationType,
    run_mutation_tests,
)

# Import modules under test
from tools.prompteval.parser import (
    ParseResult,
    Phase,
    detect_pattern,
    get_available_patterns,
    load_pattern_definition,
    parse_output,
)
from tools.prompteval.pattern_evaluator import (
    HARD_GATES,
    DimensionScore,
    PatternScore,
    SingleRunResult,
    get_dimension_config,
    load_scoring_schema,
    parse_judge_output,
)

# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def react_output():
    """Sample ReAct pattern output."""
    return """
Thought: I need to find information about Python list comprehensions.
This is a common programming topic that I should be able to explain.

Action: Search for "Python list comprehension syntax and examples"

Observation: List comprehensions provide a concise way to create lists.
The basic syntax is [expression for item in iterable if condition].

Thought: Now I have the basic information. Let me formulate a clear answer.

Action: Compile the explanation with examples

Observation: Created explanation with syntax and three examples.

Final Answer: Python list comprehensions are a concise way to create lists.
The syntax is: [expression for item in iterable if condition]

Examples:
- [x**2 for x in range(10)] creates squares
- [x for x in items if x > 0] filters positives
- [[i*j for j in range(3)] for i in range(3)] creates a matrix
"""


@pytest.fixture
def cove_output():
    """Sample CoVe pattern output."""
    return """
Draft Answer: The capital of Australia is Sydney, which is the largest city.

Verification Questions:
1. Is Sydney actually the capital of Australia?
2. What is the relationship between largest city and capital?
3. When was the current capital established?

Independent Verification:
1. No, Sydney is not the capital. Canberra is the capital of Australia.
2. The largest city is not always the capital. Sydney is largest but not capital.
3. Canberra became the capital in 1927 as a planned city.

Revised Answer: The capital of Australia is Canberra, not Sydney.
While Sydney is the largest and most well-known Australian city,
Canberra was specifically built as the capital and has served that
role since 1927.
"""


@pytest.fixture
def reflexion_output():
    """Sample Reflexion pattern output."""
    return """
Initial Attempt:
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

Self-Critique:
- The recursive solution has exponential time complexity O(2^n)
- No memoization leads to redundant calculations
- Will be very slow for large n values
- Could cause stack overflow for very large inputs

Reflection Memory:
I should use dynamic programming or memoization to improve efficiency.
The key insight is that we're recalculating the same values many times.

Improved Attempt:
def fibonacci(n):
    if n <= 1:
        return n
    dp = [0, 1]
    for i in range(2, n + 1):
        dp.append(dp[i-1] + dp[i-2])
    return dp[n]

This solution has O(n) time complexity and O(n) space complexity.
"""


@pytest.fixture
def rag_output():
    """Sample RAG pattern output."""
    return """
Query Analysis:
The user wants to know about the health benefits of green tea.
Key concepts: green tea, health benefits, scientific evidence.

Retrieval:
Retrieved 3 relevant documents:
- Doc1: "Green tea contains catechins, powerful antioxidants..."
- Doc2: "Studies show green tea may reduce risk of heart disease..."
- Doc3: "The caffeine in green tea provides mild stimulant effects..."

Evidence Integration:
From the retrieved documents, the main benefits are:
1. Antioxidant properties (Doc1: catechins)
2. Cardiovascular health (Doc2: reduced heart disease risk)
3. Mental alertness (Doc3: caffeine effects)

Grounded Answer:
Based on the retrieved evidence, green tea offers several health benefits:

1. **Antioxidant Protection**: Green tea contains catechins, which are
   powerful antioxidants that help protect cells from damage.

2. **Heart Health**: Studies indicate that regular green tea consumption
   may reduce the risk of heart disease.

3. **Mental Alertness**: The caffeine content provides a mild stimulant
   effect that can improve focus and alertness.

All claims are supported by the retrieved documents.
"""


@pytest.fixture
def incomplete_react():
    """ReAct output missing Final Answer."""
    return """
Thought: I need to solve this problem.

Action: Search for solution

Observation: Found some information.

Thought: Let me think about this more.
"""


# =============================================================================
# PARSER TESTS
# =============================================================================


class TestPatternDefinitions:
    """Test pattern definition loading."""

    def test_get_available_patterns(self):
        patterns = get_available_patterns()
        assert "react" in patterns
        assert "cove" in patterns
        assert "reflexion" in patterns
        assert "rag" in patterns

    def test_load_react_definition(self):
        pattern = load_pattern_definition("react")
        assert pattern["name"] == "ReAct"  # Full name in YAML
        assert "required_phases" in pattern
        assert "phase_markers" in pattern

    def test_load_cove_definition(self):
        pattern = load_pattern_definition("cove")
        assert "Verification" in pattern["name"]  # Chain-of-Verification
        assert len(pattern["required_phases"]) == 4


class TestParser:
    """Test the output parser."""

    def test_parse_react_output(self, react_output):
        result = parse_output(react_output, "react")
        assert result.is_valid
        assert len(result.phases) >= 3
        assert "thought" in [p.type for p in result.phases]
        assert "action" in [p.type for p in result.phases]

    def test_parse_cove_output(self, cove_output):
        result = parse_output(cove_output, "cove")
        assert result.is_valid
        # Phase types are normalized to lowercase
        assert "draft answer" in [p.type for p in result.phases]
        assert "revised answer" in [p.type for p in result.phases]

    def test_parse_incomplete_react(self, incomplete_react):
        result = parse_output(incomplete_react, "react")
        # Phase names are normalized to lowercase
        assert "final answer" in result.missing_phases or len(result.phases) < 4

    def test_detect_pattern_react(self, react_output):
        detected = detect_pattern(react_output)
        assert detected == "react"

    def test_detect_pattern_cove(self, cove_output):
        detected = detect_pattern(cove_output)
        assert detected == "cove"


class TestParseResult:
    """Test ParseResult dataclass."""

    def test_empty_result(self):
        result = ParseResult()
        assert not result.is_valid
        assert result.phase_types == []

    def test_result_with_phases(self):
        result = ParseResult(
            phases=[
                Phase(type="thought", content="test", line_start=0, line_end=1),
                Phase(type="action", content="test", line_start=2, line_end=3),
            ]
        )
        assert result.is_valid
        assert result.phase_types == ["thought", "action"]

    def test_to_dict(self):
        result = ParseResult(
            phases=[Phase(type="test", content="content", line_start=0, line_end=1)],
            ordering_valid=True,
        )
        d = result.to_dict()
        assert "phases" in d
        assert "ordering_valid" in d


# =============================================================================
# FAILURE TAXONOMY TESTS
# =============================================================================


class TestFailures:
    """Test failure mode handling."""

    def test_failure_mode_enum(self):
        assert FailureMode.PHASE_SKIP.value == "phase_skip"
        assert FailureMode.ORDER_VIOLATION.value == "order_violation"

    def test_failure_report(self):
        report = FailureReport(
            mode=FailureMode.PHASE_SKIP,
            phase="final_answer",
            details="Missing final answer phase",
        )
        d = report.to_dict()
        assert d["mode"] == "phase_skip"
        assert d["phase"] == "final_answer"

    def test_failure_summary(self):
        summary = PatternFailureSummary(pattern="react")
        summary.add_failure(FailureReport(mode=FailureMode.PHASE_SKIP))
        summary.add_failure(FailureReport(mode=FailureMode.PHASE_SKIP))
        summary.add_failure(FailureReport(mode=FailureMode.ORDER_VIOLATION))

        assert summary.total == 3
        assert summary.by_mode[FailureMode.PHASE_SKIP] == 2
        assert summary.by_mode[FailureMode.ORDER_VIOLATION] == 1


# =============================================================================
# SCORING TESTS
# =============================================================================


class TestScoring:
    """Test scoring schema and structures."""

    def test_load_scoring_schema(self):
        schema = load_scoring_schema()
        assert "universal_dimensions" in schema
        assert "hard_gates" in schema

    def test_get_dimension_config(self):
        dims = get_dimension_config("react")
        assert len(dims) > 0
        abbrevs = [d["abbreviation"] for d in dims]
        assert "PIF" in abbrevs
        assert "POI" in abbrevs

    def test_dimension_score(self):
        score = DimensionScore(
            name="Phase Identification Fidelity",
            abbreviation="PIF",
            score=4.0,
            weight=1.2,
        )
        assert score.normalized == 0.8
        assert score.weighted == 4.8

    def test_single_run_result(self):
        result = SingleRunResult(run_id=0)
        result.dimensions = {
            "PIF": DimensionScore(name="PIF", abbreviation="PIF", score=4.0),
            "POI": DimensionScore(name="POI", abbreviation="POI", score=5.0),
        }
        assert 4.0 <= result.composite_score <= 5.0

    def test_hard_gates(self):
        assert HARD_GATES["PC"] == 4
        assert HARD_GATES["PR"] == 0.75


class TestJudgeOutputParsing:
    """Test judge output parsing."""

    def test_parse_valid_json(self):
        output = """
        Here's my evaluation:
        ```json
        {
            "scores": {
                "PIF": {"score": 4, "rationale": "Good phase identification"},
                "POI": {"score": 5, "rationale": "Correct ordering"}
            },
            "failure_modes": ["leakage"],
            "summary": "Overall good"
        }
        ```
        """
        dims = [
            {"abbreviation": "PIF", "name": "PIF", "weight": 1.0},
            {"abbreviation": "POI", "name": "POI", "weight": 1.0},
        ]
        scores, failures, error = parse_judge_output(output, dims)

        assert error is None
        assert "PIF" in scores
        assert scores["PIF"].score == 4
        assert FailureMode.LEAKAGE in failures

    def test_parse_invalid_json(self):
        output = "This is not JSON at all"
        dims = []
        scores, failures, error = parse_judge_output(output, dims)

        assert error is not None
        assert "No JSON found" in error


class TestPatternScore:
    """Test aggregated pattern scores."""

    def test_empty_pattern_score(self):
        score = PatternScore(pattern_name="react")
        score.compute_aggregates()
        assert score.overall_score == 0.0
        assert score.pass_rate == 0.0

    def test_pattern_score_aggregation(self):
        score = PatternScore(pattern_name="react")

        for i in range(5):
            run = SingleRunResult(run_id=i)
            run.dimensions = {
                "PIF": DimensionScore(
                    name="PIF", abbreviation="PIF", score=4.0 + (i * 0.2)
                ),
            }
            score.runs.append(run)

        score.compute_aggregates()

        assert score.pass_rate == 1.0
        assert "PIF" in score.dimension_medians


# =============================================================================
# MUTATION TESTS
# =============================================================================


class TestMutations:
    """Test mutation module."""

    def test_mutation_types(self):
        assert len(MutationType) == 6
        assert MutationType.PHASE_REORDER.value == "phase_reorder"

    def test_content_inject_mutator(self, react_output):
        mutator = ContentInjectMutator()
        pattern_def = load_pattern_definition("react")
        result = mutator.mutate(react_output, pattern_def)

        assert result.mutation_type == MutationType.CONTENT_INJECT
        assert len(result.mutated) > len(result.original)
        assert "leakage" in result.expected_failures

    def test_run_mutation_tests(self, react_output):
        pattern_def = load_pattern_definition("react")
        results, mutated = run_mutation_tests(
            react_output,
            "react",
            pattern_def,
            mutations=[MutationType.CONTENT_INJECT],
        )

        assert len(results) == 1
        assert len(mutated) == 1


# =============================================================================
# INTEGRATION TESTS
# =============================================================================


class TestIntegration:
    """Test integration module."""

    def test_pattern_keywords(self):
        from tools.prompteval.integration import PATTERN_KEYWORDS

        assert "react" in PATTERN_KEYWORDS
        assert "cove" in PATTERN_KEYWORDS

    def test_detect_pattern_from_frontmatter(self):
        from tools.prompteval.integration import detect_pattern_from_frontmatter

        fm = {"pattern": "react"}
        assert detect_pattern_from_frontmatter(fm) == "react"

        fm = {"tags": ["advanced", "react", "reasoning"]}
        assert detect_pattern_from_frontmatter(fm) == "react"

        fm = {"tags": "cove, verification"}
        assert detect_pattern_from_frontmatter(fm) == "cove"


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
