#!/usr/bin/env python3
"""End-to-end pattern evaluation test using library prompts.

Demonstrates the full evaluation pipeline without needing an LLM.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.prompteval.parser import parse_output
from tools.prompteval.pattern_evaluator import (
    DimensionScore,
    PatternScore,
    SingleRunResult,
)


def test_react_with_library_output():
    """Test ReAct pattern with a well-formed output."""

    # This simulates a model output following the react-tool-augmented.md pattern
    output = """
**Thought:** I need to analyze the error logs to determine why the API is returning 500 errors.
Let me search for recent error patterns in the monitoring system.

**Action:** search_logs("api-gateway", time_range="last_hour", level="ERROR")

**Observation:**
Found 47 ERROR entries:
- 35x: "Database connection timeout after 30s"
- 8x: "Rate limit exceeded for user_id: X"
- 4x: "Invalid JSON payload in request body"

The majority (74%) of errors are database connection timeouts.

**Thought:** The database timeout is the primary issue. I should check the database
connection pool status and recent queries.

**Action:** query_metrics("db_connection_pool", dimensions=["active", "idle", "waiting"])

**Observation:**
Connection Pool Metrics (last hour):
- Active: 95-100 (max: 100) - SATURATED
- Idle: 0-2
- Waiting: 15-45 requests in queue

The connection pool is completely saturated with requests waiting in queue.

**Thought:** Now I understand the issue. The database connection pool is maxed out,
causing timeouts. I should check what's consuming all the connections.

**Action:** query_slow_logs("database", duration_threshold="5s")

**Observation:**
Top slow queries:
1. SELECT * FROM user_sessions WHERE last_active > ? (avg: 12s, count: 450)
2. SELECT * FROM audit_logs WHERE created_at > ? (avg: 8s, count: 230)

There are two problematic queries consuming connections for too long.

**Final Answer:**

## Root Cause Analysis

The API 500 errors are caused by **database connection pool exhaustion**:

1. **Primary Issue**: The connection pool (max 100) is completely saturated
2. **Root Cause**: Two slow queries are holding connections for 8-12 seconds each:
   - `user_sessions` query: 450 executions, 12s average
   - `audit_logs` query: 230 executions, 8s average

## Recommended Actions

1. **Immediate**: Increase connection pool size to 200 (short-term fix)
2. **Short-term**: Add indexes to `user_sessions.last_active` and `audit_logs.created_at`
3. **Medium-term**: Implement query pagination and connection timeout policies

## Impact

- 74% of errors will be resolved by fixing the database issues
- Estimated resolution time: 2-4 hours for immediate fixes
"""

    result = parse_output(output, "react")

    print("=" * 60)
    print("ReAct Pattern Test - Error Log Analysis")
    print("=" * 60)
    print(f"\n✓ Valid output: {result.is_valid}")
    print(f"✓ Phases found: {len(result.phases)}")
    print(f"✓ Ordering valid: {result.ordering_valid}")
    print(f"✓ Phase sequence: {' → '.join(result.phase_types)}")

    if result.missing_phases:
        print(f"⚠ Missing: {result.missing_phases}")

    # Simulate scoring
    score = PatternScore(pattern_name="react")
    run = SingleRunResult(run_id=0)
    run.dimensions = {
        "PIF": DimensionScore(
            name="Pattern Invocation Fidelity",
            abbreviation="PIF",
            score=5.0,
            weight=0.2,
        ),
        "POI": DimensionScore(
            name="Phase Ordering Integrity", abbreviation="POI", score=5.0, weight=0.2
        ),
        "PC": DimensionScore(
            name="Phase Completeness", abbreviation="PC", score=5.0, weight=0.2
        ),
        "CA": DimensionScore(
            name="Constraint Adherence", abbreviation="CA", score=4.5, weight=0.2
        ),
    }
    score.runs.append(run)
    score.compute_aggregates()

    print(f"\n📊 Simulated Score: {score.overall_score:.2f}/5.0")
    print(f"   Hard Gates: {'PASS ✓' if score.passes_hard_gates else 'FAIL ✗'}")


def test_cove_with_library_output():
    """Test CoVe pattern with a verification output."""

    output = """
**Baseline Response:**
The Python Global Interpreter Lock (GIL) prevents multiple threads from executing
Python bytecode simultaneously, making Python inefficient for CPU-bound parallel
processing. The GIL was introduced in Python 2.0 to simplify memory management.

**Verification Questions:**
1. Does the GIL actually prevent ALL parallel execution, or just bytecode execution?
2. When exactly was the GIL introduced - was it in Python 2.0?
3. Is Python inefficient for ALL types of parallel processing?
4. What was the primary reason for introducing the GIL?

**Independent Verification:**
1. The GIL prevents parallel execution of Python bytecode only. I/O operations,
   NumPy operations, and C extensions can release the GIL and run in parallel.
2. The GIL was actually present in CPython from the beginning (Python 1.x),
   not introduced in Python 2.0. It's a CPython implementation detail.
3. Python is efficient for I/O-bound parallel processing. The GIL limitation
   primarily affects CPU-bound tasks using pure Python code.
4. The primary reason was reference counting for memory management - it needs
   thread-safe operations to prevent race conditions.

**Revised Answer:**
The Python Global Interpreter Lock (GIL) is a mutex in CPython (the reference
implementation) that prevents multiple native threads from executing Python
bytecode simultaneously. Key clarifications:

1. **Scope**: The GIL only blocks Python bytecode execution - I/O operations,
   NumPy computations, and C extensions can release the GIL and run in parallel.

2. **History**: The GIL has existed since CPython's inception (Python 1.x),
   not Python 2.0. It's a CPython implementation detail, not a Python language requirement.

3. **Impact**: Python IS efficient for I/O-bound parallel processing (web servers,
   file operations). The limitation affects CPU-bound pure Python code.

4. **Purpose**: The GIL simplifies memory management by making reference counting
   thread-safe, avoiding race conditions without fine-grained locking.

For true CPU parallelism in Python, use multiprocessing, concurrent.futures, or
alternative implementations like PyPy-STM or Jython (which has no GIL).
"""

    result = parse_output(output, "cove")

    print("\n" + "=" * 60)
    print("CoVe Pattern Test - Python GIL Verification")
    print("=" * 60)
    print(f"\n✓ Valid output: {result.is_valid}")
    print(f"✓ Phases found: {len(result.phases)}")
    print(f"✓ Ordering valid: {result.ordering_valid}")
    print(f"✓ Phase sequence: {' → '.join(result.phase_types)}")

    # Simulate scoring
    score = PatternScore(pattern_name="cove")
    run = SingleRunResult(run_id=0)
    run.dimensions = {
        "PIF": DimensionScore(
            name="Pattern Invocation Fidelity",
            abbreviation="PIF",
            score=5.0,
            weight=0.2,
        ),
        "POI": DimensionScore(
            name="Phase Ordering Integrity", abbreviation="POI", score=5.0, weight=0.2
        ),
        "PC": DimensionScore(
            name="Phase Completeness", abbreviation="PC", score=5.0, weight=0.2
        ),
        "CA": DimensionScore(
            name="Constraint Adherence", abbreviation="CA", score=4.8, weight=0.2
        ),
    }
    score.runs.append(run)
    score.compute_aggregates()

    print(f"\n📊 Simulated Score: {score.overall_score:.2f}/5.0")
    print(f"   Hard Gates: {'PASS ✓' if score.passes_hard_gates else 'FAIL ✗'}")


def test_rag_with_library_output():
    """Test RAG pattern with document retrieval output."""

    output = """
**Query Analysis:**
The user asks about implementing retry logic in Azure Functions.
Key information needs:
- Azure Functions retry policy configuration
- Built-in vs custom retry approaches
- Best practices for transient failures
- Code examples

**Retrieval:**
Retrieved 3 relevant documents from knowledge base:

[Doc-AF-001] Azure Functions Retry Policies Documentation
Source: docs.microsoft.com/azure/azure-functions/functions-bindings-error-pages
"Azure Functions provides built-in retry support. For trigger-based functions,
you can configure retry policies using host.json. Supported retry strategies
include fixed delay and exponential backoff..."

[Doc-AF-002] Best Practices for Resilient Azure Functions
Source: learn.microsoft.com/azure/architecture/best-practices/retry-service-specific
"When implementing retries, consider idempotency of operations. Use correlation
IDs for tracing. Set reasonable maximum retry counts (typically 3-5) to avoid
cascading failures..."

[Doc-AF-003] Custom Retry Implementation Example
Source: github.com/Azure-Samples/functions-retry-pattern
"For custom retry logic, use Polly library: services.AddHttpClient<MyService>()
.AddTransientHttpErrorPolicy(p => p.WaitAndRetryAsync(3,
retryAttempt => TimeSpan.FromSeconds(Math.Pow(2, retryAttempt))));"

**Evidence Integration:**
Combining the retrieved documents:
1. Built-in retry via host.json [Doc-AF-001]
2. Idempotency and correlation IDs are critical [Doc-AF-002]
3. Polly library for HTTP client retries [Doc-AF-003]

**Grounded Answer:**

## Azure Functions Retry Implementation

Based on the retrieved documentation, here are the approaches for implementing retry logic:

### 1. Built-in Retry Policies [Doc-AF-001]

Configure in `host.json`:
```json
{
  "retry": {
    "strategy": "exponentialBackoff",
    "maxRetryCount": 5,
    "minimumInterval": "00:00:05",
    "maximumInterval": "00:15:00"
  }
}
```

### 2. Custom Retry with Polly [Doc-AF-003]

For HTTP clients:
```csharp
services.AddHttpClient<MyService>()
    .AddTransientHttpErrorPolicy(p =>
        p.WaitAndRetryAsync(3, retryAttempt =>
            TimeSpan.FromSeconds(Math.Pow(2, retryAttempt))));
```

### Best Practices [Doc-AF-002]

- Ensure operations are **idempotent**
- Use **correlation IDs** for tracing
- Limit retries to **3-5 attempts** to prevent cascading failures

**Confidence**: High - All claims supported by official documentation.

**Sources Used**:
- [Doc-AF-001]: Retry policy configuration options
- [Doc-AF-002]: Best practices and guardrails
- [Doc-AF-003]: Polly implementation example
"""

    result = parse_output(output, "rag")

    print("\n" + "=" * 60)
    print("RAG Pattern Test - Azure Functions Documentation")
    print("=" * 60)
    print(f"\n✓ Valid output: {result.is_valid}")
    print(f"✓ Phases found: {len(result.phases)}")
    print(f"✓ Ordering valid: {result.ordering_valid}")
    print(f"✓ Phase sequence: {' → '.join(result.phase_types)}")

    # Simulate scoring
    score = PatternScore(pattern_name="rag")
    run = SingleRunResult(run_id=0)
    run.dimensions = {
        "PIF": DimensionScore(
            name="Pattern Invocation Fidelity",
            abbreviation="PIF",
            score=5.0,
            weight=0.2,
        ),
        "POI": DimensionScore(
            name="Phase Ordering Integrity", abbreviation="POI", score=5.0, weight=0.2
        ),
        "PC": DimensionScore(
            name="Phase Completeness", abbreviation="PC", score=5.0, weight=0.2
        ),
        "CA": DimensionScore(
            name="Constraint Adherence", abbreviation="CA", score=4.5, weight=0.2
        ),
    }
    score.runs.append(run)
    score.compute_aggregates()

    print(f"\n📊 Simulated Score: {score.overall_score:.2f}/5.0")
    print(f"   Hard Gates: {'PASS ✓' if score.passes_hard_gates else 'FAIL ✗'}")


def test_failing_pattern():
    """Test detection of a poorly-formed pattern output."""

    # This output has problems: skips phases, bad ordering
    output = """
Here's my answer to your question about sorting algorithms:

QuickSort is generally the fastest in practice with O(n log n) average time.
MergeSort is stable and always O(n log n).
HeapSort has O(1) space complexity.

Let me know if you need more details!
"""

    result = parse_output(output, "react")

    print("\n" + "=" * 60)
    print("Failing Pattern Test - Missing Phases")
    print("=" * 60)
    print(f"\n✗ Valid output: {result.is_valid}")
    print(f"✗ Phases found: {len(result.phases)}")
    print(f"✗ Missing phases: {result.missing_phases}")

    if result.leakage_detected:
        print("⚠ Leakage detected: Content outside phases")


def main():
    print("\n" + "=" * 60)
    print(" END-TO-END PATTERN EVALUATION TESTS ")
    print("=" * 60)

    test_react_with_library_output()
    test_cove_with_library_output()
    test_rag_with_library_output()
    test_failing_pattern()

    print("\n" + "=" * 60)
    print(" ALL TESTS COMPLETE ")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
