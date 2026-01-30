# Agentic Workflow Construction Plan

## Objective

Build four specific agentic workflows based on the user's requirements and example format.

## Workflows to Build

1. **End-to-End Development**: Mockups/Requirements -> Delivered & Tested Code.
2. **Defect Resolution**: Evaluation -> Defect Identification -> Resolution.
3. **Iterative System Design**: High-level Requirements -> Architectural Decisions -> Iterative Refinement.
4. **Code Grading**: Analysis of agent-produced code -> Grading/Scoring.

## Tasks

### Task 1: Research & Model Selection

* **Goal**: Select the best models and a range of suited models for each role in the workflows.
* **Source**: User-provided `providers` list (Local ONNX, GitHub Models, Ollama, AI Toolkit).
* **Output**: `model_selection_matrix.md` detailing the rationale, best choice, and alternatives for each role (Vision, Coding, Reasoning, Reviewing).

### Task 2: Define Workflow 1 - End-to-End Development

* **Goal**: Create `workflow_end_to_end.json`.
* **Agents**:
  * `Vision Analyst` (Mockup extraction)
  * `Requirements Engineer` (User Story expansion)
  * `Tech Lead` (Architecture & Stack decisions)
  * `Full Stack Developer` (Implementation)
  * `QA Engineer` (Test generation & execution)
  * `DevOps` (Configuration & Delivery)

### Task 3: Define Workflow 2 - Defect Resolution

* **Goal**: Create `workflow_defect_resolution.json`.
* **Agents**:
  * `Triage Agent` (Analyze issue/log)
  * `Reproduction Specialist` (Create reproduction script)
  * `Debugger` (Root cause analysis)
  * `Patcher` (Implement fix)
  * `Verifier` (Run regression tests)

### Task 4: Define Workflow 3 - Iterative System Design

* **Goal**: Create `workflow_system_design.json`.
* **Agents**:
  * `Architect` (Initial design)
  * `Critic` (Review against requirements & thresholds)
  * `Refiner` (Apply feedback)
  * `Documenter` (Final specification)
  * *Mechanism*: Define the iterative loop logic (this might be metadata in the JSON).

### Task 5: Define Workflow 4 - Code Grading

* **Goal**: Create `workflow_code_grading.json`.
* **Agents**:
  * `Static Analyst` (Linting, complexity, style)
  * `Security Auditor` (Vuln scanning)
  * `Performance Reviewer` (Efficiency check)
  * `Head Judge` (Final scoring & Report generation)

### Task 6: Execution Strategy & Usage

* **Goal**: Provide instructions on how to interpret these JSONs and run them using the `agent_framework` or similar.

---

## ✅ Implementation Status (Completed)

### Phase 1: Planning & Definition

* Model Selection Matrix: ✅
* JSON Configurations: ✅
* Rubric Definitions: ✅

### Phase 2: Core Validation

* Integration Tests: ✅
* Engine Configuration: ✅

### Phase 3: Pilot Workflow (Code Grading)

* **Status**: ✅ Completed
* **Achievements**:
  * Fixed model ID format for GitHub Models (`gh:openai/...`)
  * Configured reliable routing for tasks (Coding, Reasoning, Review)
  * Successfully executed `code_grading` workflow end-to-end
  * Generated detailed JSON grading report
* **Key Findings**:
  * `o3-mini` has restrictive context limits on current tier; swapped to `gpt-4o` for heavy reasoning tasks.
  * Local model fallback logic verified.

### Phase 4: Full Execution & Validation

* **Status**: 🔄 Ready for Execution (Pending Credentials)
* **Scripts Created**:
  * `examples/run_defect_resolution.py`: ✅
  * `examples/run_system_design.py`: ✅
  * `examples/run_fullstack.py`: ✅
* **Validation**:
  * Model routing updated to use `gpt-4o` for stability.
  * Verified environment check functionality.
  * **Note**: Execution requires `GITHUB_TOKEN` to be set in the active terminal.

---

### Artifacts Delivered

* `multiagent-workflows/config/agentic_planning/workflow_*.json`
* `multiagent-workflows/examples/run_*.py`
* `multiagent-workflows/evaluation/results/`
