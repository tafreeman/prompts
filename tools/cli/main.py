import json
import os
import click

from universal_code_generator import UniversalCodeGenerator # type: ignore
from prompts.config import default_config
from .interactive import interactive_wizard

@click.group()
def cli():
    """Universal Code Generator CLI"""
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
        os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True) # type: ignore
        with open(output, 'w') as f:
            f.write(result.final)
        click.echo(f"💾 Saved to: {output}")
    else:
        click.echo("\n--- Generated Content ---\n")
        click.echo(result.final)


if __name__ == '__main__':
    cli()
