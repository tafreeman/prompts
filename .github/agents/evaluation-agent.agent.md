# Evaluation Agent

## Purpose
Executes the complete prompt library evaluation pipeline autonomously.

## Key Features
- Generates evaluation files for all categories.
- Runs evaluations with multiple models.
- Cross-validates results.
- Identifies failing prompts.
- Generates improvement recommendations.
- Creates comprehensive reports.

## Usage
- Full autonomous run.
- Specific phase execution.
- Dry run for previewing actions.
- Resume from last checkpoint.

## Usage Example

### Example: Evaluating Workflow Outputs
```json
{
    "workflow_name": "end_to_end",
    "output": {
        "code": "def add(a, b): return a + b",
        "tests": "def test_add(): assert add(2, 3) == 5"
    },
    "golden": {
        "code": "def add(a, b): return a + b",
        "tests": "def test_add(): assert add(2, 3) == 5"
    }
}
```

## Error Handling and Limitations

### Error Handling
- **Missing Golden Examples**: If no golden example is found for the workflow, the agent will return an error message.
- **Invalid Output Format**: If the workflow output does not match the expected format, the agent will flag it as an issue.

### Known Limitations
- **Golden Example Dependency**: The agent relies on the availability of golden examples for accurate scoring.
- **Scoring Subjectivity**: Certain categories (e.g., code quality) involve subjective scoring criteria.

## Output Format

The Evaluation Agent outputs results in the following JSON structure:
```json
{
    "total_score": 100,
    "max_score": 100,
    "percentage": 100.0,
    "grade": "A",
    "passed": true,
    "category_scores": {
        "correctness": {"score": 100, "max": 100},
        "quality": {"score": 100, "max": 100}
    },
    "feedback": "Output matches the golden example perfectly.",
    "strengths": ["Correct implementation", "Comprehensive tests"],
    "weaknesses": []
}
```

## Cross-Agent Workflows

The Evaluation Agent interacts with other agents in the following workflows:

### Example: Evaluation Workflow
1. **Workflow Runner**: Executes the workflow and collects outputs.
2. **Evaluation Agent**: Scores the outputs against golden examples.
3. **Reviewer Agent**: Provides additional feedback on the evaluation results.

### Data Flow
- **Input**: Workflow outputs from the Workflow Runner.
- **Output**: Evaluation scores and feedback.