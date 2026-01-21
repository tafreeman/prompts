from tools.prompteval.unified_scorer import score_prompt, score_pattern
import json

# Simple scoring - use an actual prompt from the library
result = score_prompt("prompts/advanced/CoVe.md", runs=3, verbose=True)

print(f"\n{'='*60}")
print(f" FINAL RESULTS")
print(f"{'='*60}")
print(f"Eval Type: {result.eval_type}")
print(f"Prompt: {result.prompt_file}")
print(f"Model: {result.model}")
print(f"Runs: {result.successful_runs}/{result.runs}")
print(f"Temperature: {result.temperature}")
print(f"Score: {result.overall_score}/100 ({result.grade})")
print(f"Passed: {'✓' if result.passed else '✗'}")
print(f"Confidence: {result.confidence:.2f}")
print(f"\nDimension Scores:")
for dim, score in result.scores.items():
    print(f"  {dim.capitalize():15} {score:4.1f}/10")
if result.improvements:
    print(f"\nSuggested Improvements:")
    for imp in result.improvements:
        print(f"  - {imp}")

# Pattern scoring example (commented - needs actual model output)
# output_text = "..." # Your model's output here
# result = score_pattern("prompts/advanced/CoVe.md", output_text, pattern="cove", runs=20)
# print(f"Hard gates passed: {result.hard_gates_passed}")