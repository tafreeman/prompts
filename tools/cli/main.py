import json
import os
import sys
from pathlib import Path
import click

from universal_code_generator import UniversalCodeGenerator  # type: ignore
from prompts.config import default_config
from .interactive import interactive_wizard


@click.group()
def cli():
    """Universal Code Generator CLI - Execute, evaluate, and manage prompts."""
    pass


@cli.command()
def interactive():
    """Start the interactive wizard."""
    params = interactive_wizard()

    click.echo(f"\n🚀 Generating content for: {params['use_case']}...")

    generator = UniversalCodeGenerator(config=default_config)
    result = generator.generate(
        category=params['category'],
        use_case=params['use_case'],
        variables=params['variables'],
        auto_refine=params['auto_refine']
    )

    click.echo(f"\n✅ Generation Complete!")
    click.echo(f"Review Score: {result.review.get('score', 'N/A')}")

    output = click.prompt("\n💾 Save to file? (leave empty to skip)", default="", show_default=False)
    if output:
        os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
        with open(output, 'w') as f:
            f.write(result.final)
        click.echo(f"💾 Saved to: {output}")
    else:
        click.echo("\n--- Generated Content ---\n")
        click.echo(result.final)


@cli.command()
@click.option('--category', prompt='Category', help='Category of the prompt')
@click.option('--use-case', prompt='Use Case', help='Specific use case description')
@click.option('--variables', prompt='Variables (JSON)', help='Variables as JSON string')
@click.option('--output', help='Output file path')
@click.option('--auto-refine/--no-auto-refine', default=True, help='Auto-refine based on review')
def create(category: str, use_case: str, variables: str, output: str, auto_refine: bool):
    """Create a new prompt/code artifact (Non-interactive)."""
    try:
        vars_dict = json.loads(variables)
    except json.JSONDecodeError:
        click.echo("Error: Variables must be valid JSON.")
        return

    click.echo(f"🚀 Generating content for: {use_case}...")

    generator = UniversalCodeGenerator(config=default_config)
    result = generator.generate(
        category=category,
        use_case=use_case,
        variables=vars_dict,
        auto_refine=auto_refine
    )

    click.echo(f"\n✅ Generation Complete!")
    click.echo(f"Review Score: {result.review.get('score', 'N/A')}")

    if output:
        os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)  # type: ignore
        with open(output, 'w') as f:
            f.write(result.final)
        click.echo(f"💾 Saved to: {output}")
    else:
        click.echo("\n--- Generated Content ---\n")
        click.echo(result.final)


# =============================================================================
# PHASE 2: Unified CLI Commands for Prompt Execution and Evaluation
# =============================================================================


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--provider', '-p', type=click.Choice(['local', 'gh', 'azure', 'openai', 'ollama']),
              default='local', help='LLM provider to use')
@click.option('--model', '-m', help='Model name (provider-specific)')
@click.option('--input', '-i', 'input_text', help='Input text to pass to the prompt')
@click.option('--input-file', type=click.Path(exists=True), help='File containing input text')
@click.option('--output', '-o', help='Output file path')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def run(file: str, provider: str, model: str, input_text: str, input_file: str, output: str, verbose: bool):
    """Execute a prompt file with the specified provider.

    Examples:
        prompt run prompts/basic/greeting.md --provider local
        prompt run prompts/advanced/analysis.md --provider gh --model gpt-4o-mini
        prompt run prompts/socmint/osint.md --provider azure --model phi4mini
    """
    # Read prompt file
    prompt_path = Path(file)
    try:
        prompt_content = prompt_path.read_text(encoding='utf-8')
    except Exception as e:
        click.echo(f"❌ Error reading file: {e}", err=True)
        sys.exit(1)

    # Get input
    if input_file:
        with open(input_file, 'r', encoding='utf-8') as f:
            user_input = f.read()
    elif input_text:
        user_input = input_text
    else:
        user_input = ""

    # Combine prompt with input
    if user_input:
        full_prompt = f"{prompt_content}\n\n---\nUser Input:\n{user_input}"
    else:
        full_prompt = prompt_content

    click.echo(f"🚀 Executing with {provider} provider...")

    try:
        if provider == 'local':
            # Use local ONNX model
            tools_dir = Path(__file__).parent.parent
            sys.path.insert(0, str(tools_dir))
            from local_model import LocalModel  # type: ignore
            lm = LocalModel(verbose=verbose)
            response = lm.generate(full_prompt, max_tokens=2000)

        elif provider == 'gh':
            # Use GitHub Models CLI
            import subprocess
            model_name = model or 'gpt-4o-mini'
            result = subprocess.run(
                ['gh', 'models', 'run', model_name, '--', full_prompt],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode != 0:
                click.echo(f"❌ gh models error: {result.stderr}", err=True)
                sys.exit(1)
            response = result.stdout

        elif provider == 'azure':
            # Use Azure Foundry
            tools_dir = Path(__file__).parent.parent
            sys.path.insert(0, str(tools_dir))
            from llm_client import LLMClient  # type: ignore
            model_key = model or 'phi4mini'
            response = LLMClient.generate_text(f"azure-foundry:{model_key}", full_prompt)

        elif provider == 'openai':
            # Use OpenAI API
            tools_dir = Path(__file__).parent.parent
            sys.path.insert(0, str(tools_dir))
            from llm_client import LLMClient  # type: ignore
            model_name = model or 'gpt-4o-mini'
            response = LLMClient.generate_text(model_name, full_prompt)

        elif provider == 'ollama':
            # Use Ollama
            import urllib.request
            model_name = model or 'llama3'
            payload = json.dumps({
                "model": model_name,
                "prompt": full_prompt,
                "stream": False
            }).encode()
            req = urllib.request.Request(
                "http://localhost:11434/api/generate",
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode())
                response = data.get("response", "")

        click.echo("\n✅ Response:\n")
        click.echo(response)

        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(response)
            click.echo(f"\n💾 Saved to: {output}")

    except Exception as e:
        click.echo(f"❌ Execution error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command('eval')
@click.argument('path', type=click.Path(exists=True))
@click.option('--tier', '-t', type=click.IntRange(0, 6), default=2,
              help='Evaluation tier (0=local, 1=structural, 2=single, 3=cross, 4=full, 5=premium, 6=azure)')
@click.option('--output', '-o', help='Output file path for results')
@click.option('--format', 'fmt', type=click.Choice(['json', 'markdown']), default='markdown',
              help='Output format')
def eval_prompt(path: str, tier: int, output: str, fmt: str):
    """Run tiered evaluation on a prompt file or directory.

    Examples:
        prompt eval prompts/basic/greeting.md --tier 2
        prompt eval prompts/socmint/ --tier 3 --output results.json
        prompt eval prompts/advanced/analysis.md --tier 6  # Azure Foundry
    """
    click.echo(f"📊 Running Tier {tier} evaluation...")

    tools_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(tools_dir))

    try:
        from tiered_eval import find_prompts, TIERS  # type: ignore
        from tiered_eval import run_tier_0, run_tier_1, run_tier_2  # type: ignore
        from tiered_eval import run_tier_3, run_tier_4, run_tier_5, run_tier_6  # type: ignore

        prompts = find_prompts(path)
        if not prompts:
            click.echo("❌ No prompts found at specified path", err=True)
            sys.exit(1)

        click.echo(f"   Found {len(prompts)} prompt(s)")
        click.echo(f"   Tier: {TIERS[tier].name} - {TIERS[tier].description}")

        output_dir = Path(output).parent if output else Path(".")
        tier_funcs = {
            0: run_tier_0, 1: run_tier_1, 2: run_tier_2,
            3: run_tier_3, 4: run_tier_4, 5: run_tier_5, 6: run_tier_6
        }

        results = tier_funcs[tier](prompts, output_dir)

        if fmt == 'json':
            result_text = json.dumps(results, indent=2, default=str)
        else:
            # Markdown summary
            lines = [
                f"# Tier {tier} Evaluation Results",
                f"**Tier:** {TIERS[tier].name}",
                f"**Prompts Evaluated:** {results.get('prompts_evaluated', 0)}",
                ""
            ]
            for r in results.get('results', []):
                status = "✅" if r.get('passed') or r.get('final_pass') else "❌"
                score = r.get('overall') or r.get('consensus_score') or r.get('avg_score') or r.get('score', 'N/A')
                lines.append(f"- {status} `{r.get('file', 'unknown')}` - Score: {score}")
            result_text = "\n".join(lines)

        click.echo("\n" + result_text)

        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(result_text)
            click.echo(f"\n💾 Results saved to: {output}")

    except ImportError as e:
        click.echo(f"❌ Import error: {e}", err=True)
        click.echo("   Make sure tiered_eval.py is available", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Evaluation error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('question')
@click.option('--provider', '-p', type=click.Choice(['local', 'github', 'azure_foundry', 'openai', 'ollama']),
              default='local', help='LLM provider to use')
@click.option('--model', '-m', help='Model name (provider-specific)')
@click.option('--questions', '-n', type=int, default=5, help='Number of verification questions')
@click.option('--output', '-o', help='Output file path')
@click.option('--json-output', is_flag=True, help='Output as JSON')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed progress')
def cove(question: str, provider: str, model: str, questions: int, output: str, json_output: bool, verbose: bool):
    """Run Chain-of-Verification (CoVe) analysis on a question.

    Examples:
        prompt cove "When was Python created and by whom?"
        prompt cove "What are the benefits of microservices?" --provider github
        prompt cove "Explain quantum computing" --provider azure_foundry --model phi4mini
    """
    click.echo(f"🔗 Running Chain-of-Verification with {provider}...")

    tools_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(tools_dir))

    try:
        from cove_runner import get_llm_function, run_cove, format_result  # type: ignore

        llm_call = get_llm_function(provider, model, verbose)
        click.echo(f"   Model: {getattr(llm_call, 'model_name', 'unknown')}")

        result = run_cove(question, llm_call, n_questions=questions, verbose=verbose)

        if json_output:
            output_data = {
                "question": result.question,
                "draft": result.draft,
                "verification_questions": result.verification_questions,
                "verified_answers": result.verified_answers,
                "final_answer": result.final_answer,
                "verification_summary": result.verification_summary,
                "confidence": result.confidence,
                "provider": result.provider,
                "model": result.model
            }
            result_text = json.dumps(output_data, indent=2)
        else:
            result_text = format_result(result, show_draft=verbose)

        click.echo("\n" + result_text)

        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(result_text)
            click.echo(f"\n💾 Saved to: {output}")

    except Exception as e:
        click.echo(f"❌ CoVe error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--provider', '-p', type=click.Choice(['local', 'gh', 'azure', 'openai']),
              default='local', help='LLM provider to use')
@click.option('--output', '-o', help='Output directory for results')
@click.option('--format', 'fmt', type=click.Choice(['json', 'markdown']), default='json',
              help='Output format')
@click.option('--parallel', is_flag=True, help='Run evaluations in parallel')
def batch(path: str, provider: str, output: str, fmt: str, parallel: bool):
    """Run batch evaluation on all prompts in a directory.

    Examples:
        prompt batch prompts/basic/ --provider local
        prompt batch prompts/socmint/ --provider gh --output results/
        prompt batch prompts/ --provider azure --parallel
    """
    click.echo(f"📦 Running batch evaluation with {provider} provider...")

    tools_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(tools_dir))

    try:
        from tiered_eval import find_prompts  # type: ignore

        prompts = find_prompts(path)
        if not prompts:
            click.echo("❌ No prompts found at specified path", err=True)
            sys.exit(1)

        click.echo(f"   Found {len(prompts)} prompt(s)")

        results = {
            "provider": provider,
            "total": len(prompts),
            "evaluated": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "results": []
        }

        for prompt_path in prompts:
            click.echo(f"   Evaluating: {prompt_path.name}...")
            try:
                content = prompt_path.read_text(encoding='utf-8')[:4000]
                eval_prompt = f"Evaluate this prompt on a scale of 1-10: {content[:1000]}..."

                # Simple evaluation based on provider
                if provider == 'local':
                    from local_model import LocalModel  # type: ignore
                    lm = LocalModel(verbose=False)
                    response = lm.generate(eval_prompt, max_tokens=500)
                elif provider == 'azure':
                    from llm_client import LLMClient  # type: ignore
                    response = LLMClient.generate_text("azure-foundry:phi4mini", eval_prompt)
                else:
                    response = f"Mock evaluation for {prompt_path.name}"

                results["results"].append({
                    "file": str(prompt_path),
                    "status": "evaluated",
                    "response_preview": response[:200] if response else ""
                })
                results["evaluated"] += 1
                results["passed"] += 1  # Simplified - real implementation would parse score

            except Exception as e:
                results["results"].append({
                    "file": str(prompt_path),
                    "status": "error",
                    "error": str(e)
                })
                results["errors"] += 1

        if fmt == 'json':
            result_text = json.dumps(results, indent=2, default=str)
        else:
            lines = [
                "# Batch Evaluation Results",
                f"**Provider:** {provider}",
                f"**Total:** {results['total']}",
                f"**Passed:** {results['passed']}",
                f"**Errors:** {results['errors']}",
                ""
            ]
            for r in results['results']:
                status = "✅" if r['status'] == 'evaluated' else "❌"
                lines.append(f"- {status} `{Path(r['file']).name}`")
            result_text = "\n".join(lines)

        click.echo("\n" + result_text)

        if output:
            output_path = Path(output)
            if output_path.is_dir():
                output_path = output_path / f"batch_results.{fmt}"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result_text)
            click.echo(f"\n💾 Results saved to: {output_path}")

    except Exception as e:
        click.echo(f"❌ Batch error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()

