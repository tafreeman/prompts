#!/usr/bin/env python3
"""
Test pattern evaluation using actual prompts from the library.

This script demonstrates the pattern evaluation system by:
1. Loading real prompts from prompts/advanced/
2. Running parser tests on sample outputs
3. Showing pattern detection and scoring capabilities
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.prompteval.parser import (
    parse_output,
    detect_pattern,
    load_pattern_definition,
    get_available_patterns,
)
from tools.prompteval.failures import FailureMode, PatternFailureSummary
from tools.prompteval.pattern_evaluator import (
    load_scoring_schema,
    get_dimension_config,
    PatternScore,
    SingleRunResult,
    DimensionScore,
)
from tools.prompteval.parse_utils import parse_frontmatter


# =============================================================================
# SAMPLE MODEL OUTPUTS (simulating what an LLM would produce)
# =============================================================================

REACT_SAMPLE_OUTPUT = """
**Thought:** I need to find information about the performance characteristics 
of different sorting algorithms to answer this comparison question. Let me start 
by identifying the key algorithms to compare.

**Action:** search_knowledge_base("sorting algorithm time complexity comparison")

**Observation:** Retrieved document showing:
- QuickSort: O(n log n) average, O(n²) worst
- MergeSort: O(n log n) all cases
- HeapSort: O(n log n) all cases
- BubbleSort: O(n²) average and worst

**Thought:** I have the time complexity data. Now I need to also consider 
space complexity and stability for a complete comparison.

**Action:** search_knowledge_base("sorting algorithm space complexity stability")

**Observation:** Retrieved document showing:
- QuickSort: O(log n) space, unstable
- MergeSort: O(n) space, stable
- HeapSort: O(1) space, unstable
- BubbleSort: O(1) space, stable

**Thought:** I now have comprehensive information about time complexity, 
space complexity, and stability. I can provide a complete answer.

**Final Answer:**
Here's a comprehensive comparison of sorting algorithms:

| Algorithm | Time (Avg) | Time (Worst) | Space | Stable |
|-----------|------------|--------------|-------|--------|
| QuickSort | O(n log n) | O(n²) | O(log n) | No |
| MergeSort | O(n log n) | O(n log n) | O(n) | Yes |
| HeapSort | O(n log n) | O(n log n) | O(1) | No |
| BubbleSort| O(n²) | O(n²) | O(1) | Yes |

**Recommendation:** For general use, QuickSort is often fastest in practice. 
For guaranteed performance, use MergeSort. For memory-constrained systems, 
use HeapSort.
"""

COVE_SAMPLE_OUTPUT = """
**Baseline Response:**
Python was created by Guido van Rossum and was first released in 1989. 
It was named after the Monty Python comedy group. Python 3.0 was released 
in 2010 and introduced many breaking changes from Python 2.

**Verification Questions:**
1. When was Python actually first released?
2. Was Python named specifically after Monty Python's Flying Circus?
3. What year was Python 3.0 actually released?
4. What were the main breaking changes in Python 3?

**Independent Verification:**
1. Python was first released in February 1991, not 1989. The development 
   started in the late 1980s, but public release was 1991.
2. Yes, Guido van Rossum confirmed he named it after Monty Python's Flying 
   Circus because he wanted a short, unique, and slightly mysterious name.
3. Python 3.0 was released on December 3, 2008, not 2010.
4. Major changes included: print becoming a function, integer division 
   changes, Unicode by default, and iterators instead of lists for 
   range/map/filter.

**Revised Answer:**
Python was created by Guido van Rossum and was first released in **February 1991** 
(development began in the late 1980s). It was named after Monty Python's Flying 
Circus comedy group. Python 3.0 was released on **December 3, 2008** and 
introduced significant breaking changes including:
- print() as a function instead of statement
- True division for integers
- Unicode strings by default
- Many functions returning iterators instead of lists
"""

REFLEXION_SAMPLE_OUTPUT = """
**Initial Attempt:**
```python
def find_longest_palindrome(s):
    if not s:
        return ""
    longest = s[0]
    for i in range(len(s)):
        for j in range(i+1, len(s)+1):
            substring = s[i:j]
            if substring == substring[::-1] and len(substring) > len(longest):
                longest = substring
    return longest
```

**Self-Critique:**
Issues identified with the initial solution:
1. **Time Complexity**: O(n³) - checking every substring and reversing each
2. **Redundant Work**: We recalculate palindrome status for substrings we've 
   already partially verified
3. **No Early Termination**: Continues checking even when we can't beat current best
4. **Missing Optimization**: Could use dynamic programming or expand-around-center

**Reflection Memory:**
Key insights for improvement:
- Palindromes have symmetric structure - can expand from center
- Two cases: odd length (single center) and even length (two centers)
- This gives O(n²) time complexity with O(1) space
- Should handle edge cases explicitly

**Improved Attempt:**
```python
def find_longest_palindrome(s):
    if not s:
        return ""
    
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left+1:right]
    
    longest = ""
    for i in range(len(s)):
        # Odd length palindromes
        odd = expand_around_center(i, i)
        if len(odd) > len(longest):
            longest = odd
        
        # Even length palindromes
        even = expand_around_center(i, i+1)
        if len(even) > len(longest):
            longest = even
    
    return longest
```

This solution has O(n²) time complexity and O(1) space complexity (excluding output).
"""

RAG_SAMPLE_OUTPUT = """
**Query Analysis:**
User wants to understand Kubernetes pod scheduling. Key concepts to retrieve:
- Pod scheduling mechanisms
- Node selectors and affinity
- Resource requests and limits
- Taints and tolerations

**Retrieval:**
Retrieved 4 relevant documents from knowledge base:

[Doc1 - k8s-scheduling-basics.md]: "The Kubernetes scheduler watches for newly 
created Pods that have no Node assigned. For every Pod that the scheduler 
discovers, the scheduler becomes responsible for finding the best Node for 
that Pod to run on..."

[Doc2 - node-affinity.md]: "Node affinity is conceptually similar to nodeSelector, 
allowing you to constrain which nodes your Pod can be scheduled on based on 
node labels. There are two types: requiredDuringSchedulingIgnoredDuringExecution 
and preferredDuringSchedulingIgnoredDuringExecution..."

[Doc3 - resource-management.md]: "When you specify a Pod, you can optionally 
specify how much of each resource a Container needs. The most common resources 
to specify are CPU and memory..."

[Doc4 - taints-tolerations.md]: "Taints allow a node to repel a set of pods. 
Tolerations are applied to pods, and allow the pods to schedule onto nodes 
with matching taints..."

**Evidence Integration:**
From the retrieved documents, the key scheduling mechanisms are:
1. Default scheduler algorithm (Doc1)
2. Node affinity rules (Doc2)
3. Resource-based filtering (Doc3)
4. Taints and tolerations (Doc4)

**Grounded Answer:**
Kubernetes pod scheduling works through several mechanisms [Doc1]:

1. **Default Scheduling**: The scheduler watches for unassigned Pods and finds 
   the best Node based on available resources and constraints.

2. **Node Affinity** [Doc2]: You can constrain Pods to specific nodes using:
   - `requiredDuringSchedulingIgnoredDuringExecution`: Hard requirements
   - `preferredDuringSchedulingIgnoredDuringExecution`: Soft preferences

3. **Resource Requests/Limits** [Doc3]: Pods specify CPU and memory needs, 
   and the scheduler only places them on nodes with sufficient resources.

4. **Taints and Tolerations** [Doc4]: Nodes can "repel" pods with taints, 
   and pods must have matching tolerations to be scheduled on tainted nodes.

All information is grounded in the retrieved documentation.
"""

# Incomplete/failing examples for testing edge cases
INCOMPLETE_REACT = """
**Thought:** I need to solve this problem about database optimization.

**Action:** search_docs("database indexing strategies")

**Observation:** Found some articles about B-tree indexes.

**Thought:** I should dig deeper into this...
"""  # Missing Final Answer

MALFORMED_COVE = """
Here's my answer about the question:

Python is a great programming language. It was made by Guido van Rossum.

Some verification thoughts:
- Is this accurate? Probably.
- Should I check? Maybe later.

Final: Python is indeed great.
"""  # Wrong phase markers


# =============================================================================
# TEST FUNCTIONS
# =============================================================================

def test_pattern_detection():
    """Test automatic pattern detection."""
    print("\n" + "="*60)
    print("Testing Pattern Detection")
    print("="*60)
    
    test_cases = [
        ("ReAct output", REACT_SAMPLE_OUTPUT, "react"),
        ("CoVe output", COVE_SAMPLE_OUTPUT, "cove"),
        ("Reflexion output", REFLEXION_SAMPLE_OUTPUT, "reflexion"),
        ("RAG output", RAG_SAMPLE_OUTPUT, "rag"),
    ]
    
    for name, output, expected in test_cases:
        detected = detect_pattern(output)
        status = "✓" if detected == expected else "✗"
        print(f"  {status} {name}: detected '{detected}' (expected '{expected}')")


def test_parser_with_library_patterns():
    """Test parser against sample outputs."""
    print("\n" + "="*60)
    print("Testing Parser with Sample Outputs")
    print("="*60)
    
    test_cases = [
        ("ReAct", REACT_SAMPLE_OUTPUT, "react"),
        ("CoVe", COVE_SAMPLE_OUTPUT, "cove"),
        ("Reflexion", REFLEXION_SAMPLE_OUTPUT, "reflexion"),
        ("RAG", RAG_SAMPLE_OUTPUT, "rag"),
        ("Incomplete ReAct", INCOMPLETE_REACT, "react"),
        ("Malformed CoVe", MALFORMED_COVE, "cove"),
    ]
    
    for name, output, pattern in test_cases:
        print(f"\n--- {name} ({pattern}) ---")
        result = parse_output(output, pattern)
        
        print(f"  Phases found: {len(result.phases)}")
        for p in result.phases:
            print(f"    - {p.type} (lines {p.line_start}-{p.line_end})")
        
        print(f"  Valid: {result.is_valid}")
        print(f"  Ordering valid: {result.ordering_valid}")
        
        if result.missing_phases:
            print(f"  Missing phases: {result.missing_phases}")
        if result.leakage_detected:
            print(f"  Leakage detected: Yes")
        if result.parse_errors:
            print(f"  Parse errors: {result.parse_errors[:2]}")


def test_scoring_schema():
    """Test scoring schema loading and dimension configuration."""
    print("\n" + "="*60)
    print("Testing Scoring Schema")
    print("="*60)
    
    schema = load_scoring_schema()
    universal_dims = schema.get('universal_dimensions', {})
    print(f"\n  Universal dimensions: {len(universal_dims)}")
    
    for name, dim in list(universal_dims.items())[:3]:
        abbrev = dim.get('id', name[:3].upper())
        weight = dim.get('weight', 1.0)
        print(f"    - {abbrev}: {name} (weight: {weight})")
    
    print(f"\n  Hard gates:")
    for gate, threshold in schema.get('hard_gates', {}).items():
        print(f"    - {gate} >= {threshold}")
    
    print(f"\n  Pattern-specific dimensions:")
    for pattern, dims in schema.get('pattern_specific', {}).items():
        print(f"    - {pattern}: {len(dims)} dimensions")


def test_with_library_prompts():
    """Test using actual prompts from the library."""
    print("\n" + "="*60)
    print("Testing with Library Prompts")
    print("="*60)
    
    prompts_dir = Path(__file__).parent.parent / "prompts" / "advanced"
    
    pattern_prompts = [
        ("CoVe.md", "cove"),
        ("react-tool-augmented.md", "react"),
        ("reflection-self-critique.md", "reflexion"),
        ("rag-document-retrieval.md", "rag"),
    ]
    
    for filename, expected_pattern in pattern_prompts:
        prompt_path = prompts_dir / filename
        if not prompt_path.exists():
            print(f"\n  ⚠ {filename}: Not found")
            continue
        
        content = prompt_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        
        print(f"\n  📄 {filename}")
        print(f"     Title: {fm.get('title', 'N/A')}")
        print(f"     Category: {fm.get('category', fm.get('type', 'N/A'))}")
        print(f"     Tags: {fm.get('tags', [])[:3]}")
        
        # Get scoring dimensions for this pattern
        dims = get_dimension_config(expected_pattern)
        print(f"     Scoring dimensions: {[d['abbreviation'] for d in dims[:4]]}")


def test_simulated_scoring():
    """Simulate a full scoring run without LLM."""
    print("\n" + "="*60)
    print("Simulated Pattern Scoring (no LLM)")
    print("="*60)
    
    # Simulate a PatternScore for ReAct
    score = PatternScore(pattern_name="react")
    
    # Add simulated runs
    for i in range(5):
        run = SingleRunResult(run_id=i)
        run.dimensions = {
            "PIF": DimensionScore(name="Phase Identification Fidelity", abbreviation="PIF", score=4.0 + (i * 0.1)),
            "POI": DimensionScore(name="Pattern Ordering Integrity", abbreviation="POI", score=4.5),
            "PC": DimensionScore(name="Phase Completeness", abbreviation="PC", score=4.0),
            "CA": DimensionScore(name="Constraint Adherence", abbreviation="CA", score=4.2),
        }
        run.failure_modes = []
        score.runs.append(run)
    
    score.compute_aggregates()
    
    print(f"\n  Pattern: {score.pattern_name}")
    print(f"  Runs: {len(score.runs)}")
    print(f"  Overall Score: {score.overall_score:.2f}/5.0")
    print(f"  Pass Rate: {score.pass_rate:.1%}")
    print(f"  Passes Hard Gates: {'✓' if score.passes_hard_gates else '✗'}")
    
    print(f"\n  Dimension Medians:")
    for dim, median in score.dimension_medians.items():
        stdev = score.dimension_stdevs.get(dim, 0)
        print(f"    - {dim}: {median:.2f} (σ={stdev:.2f})")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print(" PATTERN EVALUATION - LIBRARY TEST ")
    print("="*60)
    
    # Check available patterns
    patterns = get_available_patterns()
    print(f"\nAvailable patterns: {patterns}")
    
    # Run tests
    test_pattern_detection()
    test_parser_with_library_patterns()
    test_scoring_schema()
    test_with_library_prompts()
    test_simulated_scoring()
    
    print("\n" + "="*60)
    print(" ALL TESTS COMPLETE ")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
