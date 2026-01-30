
# Workflow Execution Examples

This directory contains scripts to run the agentic workflows.

## Prerequisites

- Ensure you have the necessary API keys set (e.g., `GITHUB_TOKEN`).
- Install dependencies: `pip install -r requirements.txt` (if not already installed).

## Scripts

### 1. Code Grading (`run_code_grading.py`)

Runs the code grading workflow on a sample Python snippet.

```bash
python run_code_grading.py
```

Options:

- `--check`: Only check model availability.
- `--poor`: Grade a poor quality code sample.

### 2. Defect Resolution (`run_defect_resolution.py`)

Runs the bug fixing workflow on a sample buggy Flask application (`buggy_app/`).

```bash
python run_defect_resolution.py
```

This script creates a local `buggy_app` if it doesn't exist (note: `app.py` is expected in `buggy_app/`).

### 3. System Design (`run_system_design.py`)

Runs the architecture evolution workflow on the `multiagent-workflows/src` codebase itself.

```bash
python run_system_design.py
```

### 4. Fullstack Generation (`run_fullstack.py`)

Runs the fullstack generation workflow to create a Personal Finance Dashboard app.

```bash
python run_fullstack.py [--check]
```

## Logs and Results

Results are saved in `evaluation/results/<workflow_name>/`.
Logs (verbose JSON) are also saved in the same directory.
