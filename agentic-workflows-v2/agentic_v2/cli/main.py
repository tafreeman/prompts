"""CLI interface for agentic workflows v2.

Commands:
- agentic run <workflow> --input <file.json>  - Run a workflow via LangChain engine
- agentic list workflows|agents|tools         - List available components
- agentic validate <workflow>                 - Validate a workflow definition
- agentic serve                               - Start the dashboard server
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.tree import Tree

from ..langchain import WorkflowRunner, list_workflows as lc_list_workflows
from ..langchain import load_workflow_config
from ..langchain.graph import compile_workflow

# Create CLI app
app = typer.Typer(
    name="agentic",
    help="Agentic Workflows V2 - LangChain/LangGraph workflow orchestration",
    add_completion=False,
)

console = Console()
_runner = WorkflowRunner()


@app.command()
def run(
    workflow: str = typer.Argument(
        ...,
        help="Workflow name (e.g., 'code_review') or path to YAML file",
    ),
    input_file: Optional[Path] = typer.Option(
        None,
        "--input",
        "-i",
        help="JSON file with input variables",
    ),
    output_file: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Write results to JSON file",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Validate and show execution plan without running",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed execution info",
    ),
):
    """Execute a workflow from a YAML definition.

    Examples:
        agentic run code_review --input review_input.json
        agentic run ./my_workflow.yaml --dry-run
    """
    try:
        # Resolve name from file path
        workflow_name = workflow
        definitions_dir: Optional[Path] = None
        if workflow.endswith((".yaml", ".yml")):
            workflow_path = Path(workflow)
            if not workflow_path.exists():
                console.print(f"[red]Error:[/red] Workflow file not found: {workflow}")
                raise typer.Exit(1)
            workflow_name = workflow_path.stem
            definitions_dir = workflow_path.parent

        try:
            workflow_def = load_workflow_config(workflow_name, definitions_dir)
        except FileNotFoundError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

        # Load input variables
        input_data: dict = {}
        if input_file:
            if not input_file.exists():
                console.print(f"[red]Error:[/red] Input file not found: {input_file}")
                raise typer.Exit(1)
            input_data = json.loads(input_file.read_text())

        # Display workflow info
        console.print(
            Panel(
                f"[bold]{workflow_def.name}[/bold]\n{workflow_def.description or 'No description'}",
                title="Workflow",
                border_style="blue",
            )
        )

        # Show execution plan
        if verbose or dry_run:
            _show_execution_plan(workflow_def)

        if dry_run:
            console.print("\n[yellow]Dry run - skipping execution[/yellow]")
            return

        # Execute the workflow via LangChain runner
        runner = WorkflowRunner(definitions_dir=definitions_dir)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Executing {workflow_def.name}...", total=None)
            result = asyncio.run(runner.run(workflow_name, **input_data))
            progress.update(task, completed=True)

        # Display results
        _show_results(result, verbose)

        # Write output if requested
        if output_file:
            output_data = {
                "workflow_name": result.workflow_name,
                "status": result.status,
                "outputs": result.outputs,
                "steps": result.steps,
                "errors": result.errors,
                "elapsed_seconds": result.elapsed_seconds,
            }
            output_file.write_text(json.dumps(output_data, indent=2, default=str))
            console.print(f"\n[green]Results written to:[/green] {output_file}")

        if result.status == "failed":
            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def orchestrate(
    task: str = typer.Argument(
        ...,
        help="Natural language description of the task to accomplish",
    ),
    max_parallel: int = typer.Option(
        3,
        "--max-parallel",
        "--max-steps",
        help="Maximum number of steps to run in parallel",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed execution info",
    ),
):
    """Dynamically generate and execute a workflow from a task description.

    Note: Dynamic orchestration is not yet available in the LangChain engine.
    Use 'agentic run <workflow>' to run a YAML-defined workflow.
    """
    console.print(
        "[yellow]Dynamic orchestration is not yet implemented in the LangChain engine.[/yellow]"
    )
    console.print("Use [bold]agentic run <workflow>[/bold] to run a YAML-defined workflow.")
    raise typer.Exit(1)


@app.command("list")
def list_components(
    component_type: str = typer.Argument(
        "workflows",
        help="Type of component to list: workflows, agents, or tools",
    ),
):
    """List available workflows, agents, or tools.

    Examples:
        agentic list workflows
        agentic list agents
        agentic list tools
    """
    component_type = component_type.lower()

    if component_type == "workflows":
        _list_workflows()
    elif component_type == "agents":
        _list_agents()
    elif component_type == "tools":
        _list_tools()
    else:
        console.print(f"[red]Unknown component type:[/red] {component_type}")
        console.print("Available types: workflows, agents, tools")
        raise typer.Exit(1)


@app.command()
def validate(
    workflow: str = typer.Argument(
        ...,
        help="Workflow name or path to YAML file to validate",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed validation info",
    ),
):
    """Validate a workflow definition without executing it.

    Checks:
    - YAML syntax and schema
    - Step dependencies (no cycles, no missing deps)
    - Graph compilation via LangGraph

    Examples:
        agentic validate code_review
        agentic validate ./custom_workflow.yaml --verbose
    """
    try:
        definitions_dir: Optional[Path] = None
        workflow_name = workflow
        if workflow.endswith((".yaml", ".yml")):
            workflow_path = Path(workflow)
            if not workflow_path.exists():
                console.print(f"[red]Error:[/red] File not found: {workflow}")
                raise typer.Exit(1)
            workflow_name = workflow_path.stem
            definitions_dir = workflow_path.parent

        workflow_def = load_workflow_config(workflow_name, definitions_dir)

        # Compile through LangGraph to catch graph-level errors
        compile_workflow(workflow_def)

        console.print(
            f"\n[green]✓[/green] Workflow '[bold]{workflow_def.name}[/bold]' is valid!"
        )

        if verbose:
            console.print("\n[bold]Details:[/bold]")
            console.print(f"  Version: {workflow_def.version}")
            console.print(f"  Steps: {len(workflow_def.steps)}")
            console.print(f"  Inputs: {len(workflow_def.inputs)}")
            console.print(f"  Outputs: {len(workflow_def.outputs)}")
            _show_execution_plan(workflow_def)

    except FileNotFoundError as e:
        console.print(f"[red]✗ Workflow not found:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Validation error:[/red] {e}")
        raise typer.Exit(1)


def _step_label(step) -> str:
    label = f"[yellow]{step.name}[/yellow]"
    if step.agent:
        label += f" [dim]({step.agent})[/dim]"
    if step.depends_on:
        label += f" ← {step.depends_on}"
    return label


def _compute_step_levels(workflow_def) -> dict[int, list]:
    step_index = {s.name: s for s in workflow_def.steps}
    step_levels: dict[str, int] = {}

    def _depth(name: str, visited: set) -> int:
        if name in step_levels:
            return step_levels[name]
        if name in visited:
            return 0
        visited.add(name)
        step = step_index.get(name)
        d = 0 if (not step or not step.depends_on) else max(_depth(d, visited) for d in step.depends_on) + 1
        step_levels[name] = d
        return d

    for step in workflow_def.steps:
        _depth(step.name, set())

    levels: dict[int, list] = {}
    for step in workflow_def.steps:
        levels.setdefault(step_levels.get(step.name, 0), []).append(step)
    return levels


def _show_execution_plan(workflow_def) -> None:
    """Display the execution plan as a tree from WorkflowConfig."""
    tree = Tree(f"[bold blue]{workflow_def.name}[/bold blue] - Execution Plan")
    for lvl, lvl_steps in sorted(_compute_step_levels(workflow_def).items()):
        if len(lvl_steps) > 1:
            node = tree.add(f"[cyan]Level {lvl}[/cyan] (parallel)")
            for s in lvl_steps:
                node.add(_step_label(s))
        else:
            tree.add(f"[cyan]Level {lvl}:[/cyan] {_step_label(lvl_steps[0])}")
    console.print("\n")
    console.print(tree)


_STATUS_STYLE = {
    "success": "[green]✓[/green] success",
    "failed": "[red]✗[/red] failed",
    "skipped": "[yellow]⊘[/yellow] skipped",
}


def _step_info(step_data: dict) -> str:
    if step_data.get("error"):
        return f"[red]{step_data['error']}[/red]"
    if step_data.get("outputs"):
        return "outputs: " + ", ".join(step_data["outputs"])
    return ""


def _show_results(result, verbose: bool) -> None:
    """Display WorkflowResult."""
    status_color = "green" if result.status == "success" else "red"
    console.print(f"\n[bold {status_color}]Status: {result.status.upper()}[/bold {status_color}]")
    console.print(f"[dim]Elapsed: {result.elapsed_seconds:.1f}s[/dim]")

    for err in result.errors:
        console.print(f"[red]Error:[/red] {err}")

    if verbose or result.status != "success":
        table = Table(title="Step Results")
        table.add_column("Step", style="cyan")
        table.add_column("Status")
        table.add_column("Info")
        for step_name, step_data in result.steps.items():
            status = step_data.get("status", "unknown")
            table.add_row(step_name, _STATUS_STYLE.get(status, status), _step_info(step_data))
        console.print(table)

    if result.outputs:
        console.print("\n[bold]Outputs:[/bold]")
        for key, value in result.outputs.items():
            preview = str(value)
            if len(preview) > 120:
                preview = preview[:117] + "..."
            console.print(f"  [cyan]{key}:[/cyan] {preview}")


def _list_workflows() -> None:
    """List available workflows using LangChain config loader."""
    workflows = lc_list_workflows()

    if not workflows:
        console.print("[yellow]No workflows found in definitions directory.[/yellow]")
        return

    table = Table(title="Available Workflows")
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    table.add_column("Steps", justify="right")

    for name in workflows:
        try:
            wf = load_workflow_config(name)
            table.add_row(name, wf.description or "-", str(len(wf.steps)))
        except Exception:
            table.add_row(name, "[red]Error loading[/red]", "-")

    console.print(table)


def _list_agents() -> None:
    """List tier-based agent roles used by the LangChain engine."""
    agents = [
        ("tier1_*", "Tier 1", "Fast/cheap model (e.g. gpt-4o-mini, gemini-flash-lite)"),
        ("tier2_*", "Tier 2", "Standard model (e.g. gpt-4o, gemini-flash)"),
        ("tier3_*", "Tier 3", "Powerful model (e.g. o3-mini, gemini-2.5-pro)"),
        ("tier0_*", "Tier 0", "Deterministic/no-LLM step"),
    ]

    table = Table(title="Agent Tiers (LangChain Engine)")
    table.add_column("Pattern", style="cyan")
    table.add_column("Tier")
    table.add_column("Description")

    for pattern, tier, desc in agents:
        table.add_row(pattern, tier, desc)

    console.print(table)
    console.print(
        "\n[dim]Agent names in YAML follow the pattern tier{N}_{role} "
        "(e.g. tier2_reviewer, tier1_analyst)[/dim]"
    )


def _list_tools() -> None:
    """List LangChain tools registered in the engine."""
    try:
        from ..langchain.tools import get_tools_for_tier
        tools = get_tools_for_tier(tier=2)  # tier 2 has the broadest set
    except Exception:
        tools = []

    if not tools:
        console.print("[yellow]No LangChain tools available.[/yellow]")
        return

    table = Table(title="Available LangChain Tools")
    table.add_column("Tool", style="cyan")
    table.add_column("Description")

    for tool in tools:
        table.add_row(tool.name, getattr(tool, "description", "-") or "-")

    console.print(table)


@app.command()
def serve(
    port: int = typer.Option(8000, "--port", "-p", help="Port to serve on"),
    dev: bool = typer.Option(False, "--dev", help="Run with auto-reload"),
    no_open: bool = typer.Option(False, "--no-open", help="Don't open browser"),
):
    """Start the workflow dashboard server.

    In dev mode, run `npm run dev` in the ui/ directory for the frontend dev server.

    Examples:
        agentic serve
        agentic serve --port 9000 --dev
    """
    try:
        import uvicorn
    except ImportError:
        console.print("[red]Error:[/red] uvicorn not installed. Run: pip install uvicorn")
        raise typer.Exit(1)

    if not no_open:
        import webbrowser
        webbrowser.open(f"http://localhost:{port}")

    console.print(f"[bold blue]Starting dashboard server on port {port}[/bold blue]")
    if dev:
        console.print("[dim]Dev mode: auto-reload enabled[/dim]")

    uvicorn.run(
        "agentic_v2.server.app:create_app",
        host="0.0.0.0",
        port=port,
        reload=dev,
        factory=True,
    )


@app.command()
def version():
    """Show version information."""
    try:
        from .. import __version__
        ver = __version__
    except ImportError:
        ver = "0.1.0"

    console.print(f"[bold]agentic-workflows-v2[/bold] version {ver}")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
