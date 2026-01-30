"""Orchestrator that uses LangChain chains when available, otherwise falls back to stubs.

This module wires the chain constructors from `workflows.langchain_chains` into a
similar orchestrator flow as `workflows/langchain_orchestrator.py`. It does not
execute LLM calls on import; call `main()` to run.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from datetime import datetime
import json
from workflows.langchain_orchestrator import load_yaml



def main():
    p = argparse.ArgumentParser()
    p.add_argument('--manifest', default='run-manifest.yaml')
    p.add_argument('--iteration-plan', default='iteration-plan.yaml')
    p.add_argument('--workflow', default='workflows/langchain_workflow.yaml')
    p.add_argument('--prompt-path', default='prompts/advanced/lats-self-refine-evaluator-agentic-workflow.md')
    p.add_argument('--output-dir', default='results')
    p.add_argument('--max-iterations', type=int, default=None, help='Override max iterations')
    args = p.parse_args()

    manifest = load_yaml(Path(args.manifest)) if Path(args.manifest).exists() else {}
    iteration_plan = load_yaml(Path(args.iteration_plan)) if Path(args.iteration_plan).exists() else {}
    workflow_map = load_yaml(Path(args.workflow)) if Path(args.workflow).exists() else {}

    run_id = manifest.get('run_id') or f"langchain_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    run_dir = Path(args.output_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    # Use the repo's LLM wrapper for all LLM calls
    try:
        from examples.langchain_llmclient_wrapper import LangChainLLMWrapper
        model_name = manifest.get('model_version')
        if not model_name:
            # Fallback: try to pick from discovery_results.json
            from examples.langchain_llmclient_wrapper import pick_first_discovered_model
            model_name = pick_first_discovered_model(Path('discovery_results.json'))
        if not model_name:
            raise RuntimeError('No model_version in manifest and no discovered model found.')
        llm = LangChainLLMWrapper(model_name)
    except Exception as e:
        print('Could not load LangChainLLMWrapper:', e)
        return 2

    # Construct chains using the wrapper
    try:
        from workflows.langchain_chains import (
            create_criteria_validator_chain,
            create_scoring_chain,
            create_implementer_chain,
            create_validator_chain,
        )
        cv_chain = create_criteria_validator_chain(llm=llm)
        scoring_chain = create_scoring_chain(llm=llm)
        impl_chain = create_implementer_chain(llm=llm)
        val_chain = create_validator_chain(llm=llm)
    except Exception as e:
        print('LangChain chains could not be constructed:', e)
        return 2

    # Iteration loop
    max_iters = args.max_iterations or manifest.get('max_iterations', 3)
    quality_threshold = manifest.get('quality_threshold', 8.0)
    prompt_path = args.prompt_path
    prompt_text = Path(prompt_path).read_text(encoding='utf-8') if Path(prompt_path).exists() else prompt_path
    artifacts = []
    for iteration in range(1, max_iters + 1):
        step_artifacts = {'iteration': iteration}
        # Criteria validation (can be parallelized)
        cv_res = cv_chain.run(manifest=manifest)
        step_artifacts['criteria_validator'] = cv_res
        effective_criteria = cv_res.get('effective_criteria', manifest.get('grading_criteria', {}))
        # Scoring (can be parallelized)
        scoring_res = scoring_chain.run(prompt_text=prompt_text, criteria_json=json.dumps(effective_criteria))
        step_artifacts['scoring'] = scoring_res
        weighted_score = None
        try:
            weighted_score = float(scoring_res.get('weighted_score', 0))
        except Exception:
            weighted_score = 0
        # Implementer
        top_fix = 'Add explicit output format and examples'  # Could be dynamic from scoring_res
        impl_res = impl_chain.run(prompt_text=prompt_text, top_fix=top_fix)
        step_artifacts['implementer'] = impl_res
        # Validator
        val_res = val_chain.run(updated_prompt=impl_res)
        step_artifacts['validator'] = val_res
        # Store per-iteration artifact
        iter_path = run_dir / f"iteration_{iteration}.json"
        iter_path.write_text(json.dumps(step_artifacts, indent=2), encoding='utf-8')
        artifacts.append(step_artifacts)
        # Check stop conditions
        if weighted_score >= quality_threshold:
            print(f"Terminating: weighted_score {weighted_score} >= quality_threshold {quality_threshold}")
            break
        if iteration == max_iters:
            print(f"Terminating: reached max_iterations {max_iters}")

    # Write run summary
    out = {
        'run_id': run_id,
        'timestamp': timestamp,
        'iterations': len(artifacts),
        'artifacts': artifacts
    }
    out_path = run_dir / f"langchain_run_{timestamp}.json"
    out_path.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print('LangChain-run summary written to', out_path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
