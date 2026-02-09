import json
import sys
from pathlib import Path

# Add the repository root to sys.path to allow importing tools
repo_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

try:
    from tools.agents.benchmarks.loader import load_benchmark
except ImportError:
    # Fallback if tools package is not found
    print(f"Error: Could not import tools from {repo_root}")
    print("Please ensure you are running this script from the correct environment.")
    sys.exit(1)

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "ui" / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def map_humaneval(task):
    """Map HumanEval task to UI format."""
    return {
        "task_id": task.task_id,
        "name": task.task_id.split("/")[-1] if "/" in task.task_id else task.task_id,
        "difficulty": "Medium",  # Heuristic as it's not in the base data always
        "prompt": task.prompt,
        "entry_point": task.test_cases[0].get("entry_point") if task.test_cases else "",
        "test": task.test_cases[0].get("test") if task.test_cases else "",
        "canonical_solution": task.expected_output,
    }


def map_mbpp(task):
    """Map MBPP task to UI format."""
    return {
        "task_id": task.task_id,
        "name": f"task_{task.task_id}",
        "difficulty": "Easy",  # Predominantly easy
        "prompt": task.prompt,
        "code": task.expected_output,
        "test_list": task.test_cases[0].get("test_list") if task.test_cases else [],
    }


def map_swebench(task):
    """Map SWE-bench task to UI format."""
    return {
        "instance_id": task.task_id,
        "repo": task.repo,
        "difficulty": task.difficulty or "Hard",
        "problem_statement": task.issue_text,
        "patch": task.golden_patch,
        "test_patch": task.test_cases[0].get("test_patch") if task.test_cases else "",
    }


def fetch_and_save(benchmark_id, mapper, filename, limit=None, use_cache=True):
    print(f"Fetching {benchmark_id}...")
    try:
        tasks = load_benchmark(benchmark_id, limit=limit, use_cache=use_cache)
        mapped_tasks = [mapper(t) for t in tasks]

        output_data = {"source": benchmark_id, "tasks": mapped_tasks}

        output_file = OUTPUT_DIR / filename
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)

        print(f"✓ Saved {len(mapped_tasks)} tasks to {output_file}")

    except Exception as e:
        print(f"Error fetching {benchmark_id}: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch benchmark datasets.")
    parser.add_argument(
        "--no-cache", action="store_true", help="Force fresh fetch from source"
    )
    args = parser.parse_args()

    use_cache = not args.no_cache
    print(
        f"Starting dataset fetch... (Cache: {'Enabled' if use_cache else 'Disabled'})"
    )

    # Fetch HumanEval
    fetch_and_save(
        "humaneval", map_humaneval, "humaneval.json", limit=None, use_cache=use_cache
    )

    # Fetch MBPP (limit to 100 for UI responsiveness)
    fetch_and_save("mbpp", map_mbpp, "mbpp.json", limit=100, use_cache=use_cache)

    # Fetch SWE-bench Lite
    fetch_and_save(
        "swe-bench-lite", map_swebench, "swebench.json", limit=None, use_cache=use_cache
    )

    print("Done!")
