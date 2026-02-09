"""Minimal LATS Self-Refine Evaluator workflow demo using LangChainAdapter.

This script simulates one iteration of the workflow, calling the
Evaluator and Implementer roles using the adapter.
"""

from tools.llm.langchain_adapter import LangChainAdapter

PROMPT_CONTENT = "Generate deployment checklist for a Django app."
GRADING_CRITERIA = {
    "clarity": 20,
    "specificity": 15,
    "robustness": 15,
    "actionability": 10,
    "testability": 10,
    "alignment_safety": 10,
    "efficiency": 5,
    "reproducibility": 5,
    "business_impact": 10,
}

# Use the first discovered model (or hardcode for demo)
MODEL_NAME = "local:phi4"
adapter = LangChainAdapter(MODEL_NAME)


def evaluator_agent(prompt, criteria):
    eval_prompt = f"You are the Evaluator. Score the following prompt using these criteria: {criteria}\nPrompt: {prompt}\nReturn JSON with criterion_scores and weighted_score."
    result = adapter.predict(eval_prompt)
    return result


def implementer_agent(prompt, top_action):
    impl_prompt = f"You are the Implementer. Apply the following fix to the prompt: {top_action}\nPrompt: {prompt}\nReturn JSON with before_snippet, after_snippet, change_summary, estimated_delta."
    result = adapter.predict(impl_prompt)
    return result


def main():
    print("--- LATS Self-Refine Evaluator Demo ---")
    print("Prompt Content:", PROMPT_CONTENT)
    print("Grading Criteria:", GRADING_CRITERIA)

    # Step 1: Evaluator
    score_report = evaluator_agent(PROMPT_CONTENT, GRADING_CRITERIA)
    print("\nEvaluator Output:\n", score_report)

    # For demo, fake a top_action
    top_action = "Add edge-case handling and explicit security checks"

    # Step 2: Implementer
    patch = implementer_agent(PROMPT_CONTENT, top_action)
    print("\nImplementer Output:\n", patch)


if __name__ == "__main__":
    main()
