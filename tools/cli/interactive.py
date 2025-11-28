import click
import json
from typing import Dict, Any

def prompt_for_variables() -> Dict[str, str]:
    """Interactively prompt for variables."""
    click.echo("\n📝 Enter variables (leave empty to finish):")
    variables = {}
    while True:
        key = click.prompt("Variable name", default="", show_default=False)
        if not key:
            break
        value = click.prompt(f"Value for '{key}'")
        variables[key] = value
    return variables

def interactive_wizard() -> Dict[str, Any]:
    """Runs the interactive wizard to collect generation parameters."""
    click.clear()
    click.echo("🎯 Universal Code Generator - Interactive Mode")
    click.echo("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    category = click.prompt(
        "📁 Category",
        type=click.Choice(['business', 'developers', 'analysis', 'creative', 'governance'], case_sensitive=False)
    )
    
    use_case = click.prompt("\n📝 Use Case (be specific)")
    
    variables = prompt_for_variables()
    
    auto_refine = click.confirm("\n🛠️  Enable auto-refinement?", default=True)
    
    return {
        "category": category,
        "use_case": use_case,
        "variables": variables,
        "auto_refine": auto_refine
    }
