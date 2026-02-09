import json
import time

import requests


def run_benchmarks():
    # Load dataset
    with open("ui/data/humaneval.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)

    tasks = dataset["tasks"][:2]  # Pick first 2 tasks

    started_runs = []

    print(f"Starting {len(tasks)} benchmark runs...")

    for task in tasks:
        task_id = task["task_id"]
        print(f"\n--- Submitting Task: {task_id} ---")

        url = "http://localhost:5050/api/start"
        payload = {
            "workflow_id": "code_grading",
            "inputs": {
                "task_id": task_id,
                "prompt": task["prompt"],
                "dataset": "humaneval",
                "language": "python",
            },
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                run_id = data.get("run_id")
                print(f"✅ Started successfully. Run ID: {run_id}")
                started_runs.append(run_id)
            else:
                print(
                    f"❌ Failed to start. Status: {response.status_code}, Response: {response.text}"
                )
        except Exception as e:
            print(f"❌ Connection error: {e}")

    # Monitor
    print(f"\nMonitoring {len(started_runs)} runs...")

    while started_runs:
        for run_id in started_runs[:]:
            try:
                r = requests.get(f"http://localhost:5050/api/runs/{run_id}", timeout=5)
                if r.status_code == 200:
                    status = r.json().get("status")
                    steps = len(r.json().get("steps", []))
                    print(f"Run {run_id}: {status} ({steps} steps completed)")

                    if status in ["complete", "error"]:
                        print(f"Run {run_id} finished with status: {status}")
                        started_runs.remove(run_id)
            except Exception as e:
                print(f"Error checking run {run_id}: {e}")

        if started_runs:
            time.sleep(5)

    print("\nAll benchmark runs finished.")


if __name__ == "__main__":
    run_benchmarks()
