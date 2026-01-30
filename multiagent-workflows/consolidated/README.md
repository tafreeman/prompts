# Consolidated Multi-Agent Workflows

This folder contains the consolidated workflows, agents, and evaluation rubrics for the multi-agent system.

## Structure
```
consolidated/
├── agents/          # Consolidated agent implementations
├── workflows.json   # Unified workflow definitions
├── rubrics.yaml     # Scoring criteria for workflows
├── README.md        # Documentation for the consolidated folder
```

## Workflows
The `workflows.json` file defines the following workflows:

1. **Full-Stack Application Generation**
   - Converts business requirements and UI mockups into a deployable full-stack application.

2. **Legacy Code Refactoring & Modernization**
   - Refactors legacy codebases to modern patterns while preserving behavior.

3. **Intelligent Bug Triage & Automated Fixing**
   - Automates bug fixing by analyzing reports, reproducing issues, and generating fixes.

4. **Architecture Evolution & Technical Debt Assessment**
   - Evolves architecture by assessing technical debt and creating a roadmap.

## Agents
The `agents/` folder contains the implementations of all agents used in the workflows. Each agent adheres to the `AgentBase` class and implements the `_process` method for task execution.

## Rubrics
The `rubrics.yaml` file defines the scoring criteria for evaluating workflow outputs. Each workflow has specific categories and weights for scoring.

## Evaluation
The evaluation process uses the `evaluation_agent.py` script and the `Scorer` class to:
- Score workflow outputs against golden examples.
- Generate evaluation reports.
- Identify areas for improvement.

## Testing
- Unit tests for agents are located in `tests/test_agents.py`.
- Integration tests for workflows are located in `tests/test_workflow_integration.py`.

## Usage
1. Define your inputs and outputs in `workflows.json`.
2. Implement or update agents in the `agents/` folder.
3. Run evaluations using the `evaluation_agent.py` script.
4. Review scores and reports to improve workflows and agents.

For more details, refer to the documentation in the `docs/` folder.