# Multi-Agent Workflow Scripts

This directory contains utility scripts for the Multi-Agent Workflow system.

## `fetch_datasets.py`

This script bridges the frontend UI with the backend `tools` library by fetching real benchmark data and populating the `ui/data/` directory.

### Usage

1. Ensure the `tools` directory is in your python path (managed automatically by the script relative to this project).
2. Install dependencies:

   ```bash
   pip install datasets huggingface_hub
   ```

3. Run the script:

   ```bash
   python scripts/fetch_datasets.py
   # Or to fetch fresh data (ignoring cache):
   python scripts/fetch_datasets.py --no-cache
   ```

### What it does

- Imports `tools.agents.benchmarks.loader` to fetch standardized task data.
- Fetches:
  - **HumanEval** (164 tasks)
  - **MBPP** (Limited to 100 tasks for UI performance)
  - **SWE-bench Lite** (300 tasks)
- Maps the Python `BenchmarkTask` objects to the JSON format expected by `ui/index.html`.
- Saves the resulting JSON files to `../ui/data/`.
