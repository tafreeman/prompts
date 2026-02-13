"""CLI interface for agentic workflows v2.

Commands:
- agentic run <workflow> --input <file.json>  - Run a static DAG workflow
- agentic orchestrate "task description"      - Dynamic DAG via Orchestrator
- agentic list workflows|agents|tools         - List available components
- agentic validate <workflow.yaml>            - Validate a workflow file
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

from ..agents import (
    ArchitectAgent,
    CoderAgent,
    OrchestratorAgent,
    OrchestratorInput,
    ReviewerAgent,
    TestAgent,
)
from ..engine import DAG, DAGExecutor, ExecutionContext
from ..workflows import (WorkflowLoader, WorkflowLoadError)

# Create CLI app
app = typer.Typer(
    name="agentic",
    help="Agentic Workflows V2 - Tier-based multi-model AI workflow orchestration",
    add_completion=False,
)

console = Console()


def _get_workflow_loader() -> WorkflowLoader:
    """Get workflow loader with default definitions directory."""
    return WorkflowLoader()


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
        # Load the workflow
        loader = _get_workflow_loader()

        if workflow.endswith((".yaml", ".yml")):
            # Load from file path
            workflow_path = Path(workflow)
            if not workflow_path.exists():
                console.print(f"[red]Error:[/red] Workflow file not found: {workflow}")
                raise typer.Exit(1)
            workflow_def = loader.load_file(workflow_path)
        else:
            # Load by name
            try:
                workflow_def = loader.load(workflow)
            except WorkflowLoadError as e:
                console.print(f"[red]Error:[/red] {e}")
                raise typer.Exit(1)

        dag = workflow_def.dag

        # Load input variables
        input_data = {}
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
            _show_execution_plan(dag)

        if dry_run:
            console.print("\n[yellow]Dry run - skipping execution[/yellow]")
            return

        # Execute the workflow
        ctx = ExecutionContext(workflow_id=workflow_def.name)
        for key, value in input_data.items():
            ctx.set_sync(key, value)

        executor = DAGExecutor()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Executing {workflow_def.name}...", total=None)
            result = asyncio.run(executor.execute(dag, ctx=ctx))
            progress.update(task, completed=True)

        # Display results
        _show_results(result, verbose)

        # Write output if requested
        if output_file:
            output_data = {
                "workflow_id": result.workflow_id,
                "status": result.overall_status.value,
                "steps": [
                    {
                        "name": step.step_name,
                        "status": step.status.value,
                        "output": step.output_data,
                    }
                    for step in result.steps
                ],
                "final_output": result.final_output,
            }
            output_file.write_text(json.dumps(output_data, indent=2, default=str))
            console.print(f"\n[green]Results written to:[/green] {output_file}")

        # Exit with error code if workflow failed
        if result.overall_status.value != "success":
            raise typer.Exit(1)

    except WorkflowLoadError as e:
        console.print(f"[red]Error loading workflow:[/red] {e}")
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
        help="Maximum number of steps to run in parallel (legacy alias: --max-steps)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed execution info",
    ),
):
    """Dynamically generate and execute a workflow from a task description.

    The Orchestrator agent will analyze the task and create an appropriate
    DAG workflow, then execute it.

    Examples:
        agentic orchestrate "Review the code in src/main.py"
        agentic orchestrate "Generate a REST API for user management" --max-steps 15
    """
    console.print(
        Panel(
            f"[bold]Task:[/bold] {task}",
            title="Dynamic Orchestration",
            border_style="cyan",
        )
    )

    # Create orchestrator and register built-in agents.
    #
    # Note: Agents will fall back to a mock response when no LLM backend is configured,
    # which makes this command usable in offline/dev environments.
    orchestrator = OrchestratorAgent()
    orchestrator.register_agent("coder", CoderAgent())
    orchestrator.register_agent("reviewer", ReviewerAgent())
    orchestrator.register_agent("tester", TestAgent())
    orchestrator.register_agent("architect", ArchitectAgent())

    orch_input = OrchestratorInput(task=task, max_parallel=max_parallel)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        plan_task = progress.add_task("Planning + executing workflow...", total=None)

        try:
            ctx = ExecutionContext(workflow_id="orchestrate")
            result = asyncio.run(orchestrator.execute_as_dag(orch_input, ctx=ctx))
            progress.update(plan_task, completed=True)

            if verbose:
                console.print("\n[bold]Results:[/bold]")
                _show_results(result, verbose=True)

        except Exception as e:
            progress.update(plan_task, completed=True)
            console.print(f"\n[red]Orchestration failed:[/red] {e}")
            raise typer.Exit(1)

    console.print("\n[green]Orchestration complete![/green]")


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
    - YAML syntax
    - Step dependencies (no cycles, no missing deps)
    - Input/output schema

    Examples:
        agentic validate code_review
        agentic validate ./custom_workflow.yaml --verbose
    """
    try:
        loader = _get_workflow_loader()

        if workflow.endswith((".yaml", ".yml")):
            workflow_path = Path(workflow)
            if not workflow_path.exists():
                console.print(f"[red]Error:[/red] File not found: {workflow}")
                raise typer.Exit(1)
            workflow_def = loader.load_file(workflow_path)
        else:
            workflow_def = loader.load(workflow)

        dag = workflow_def.dag

        # Validate the DAG
        dag.validate()

        # Show validation results
        console.print(
            f"\n[green]✓[/green] Workflow '[bold]{workflow_def.name}[/bold]' is valid!"
        )

        if verbose:
            console.print("\n[bold]Details:[/bold]")
            console.print(f"  Version: {workflow_def.version}")
            console.print(f"  Steps: {len(dag.steps)}")
            console.print(f"  Inputs: {len(workflow_def.inputs)}")
            console.print(f"  Outputs: {len(workflow_def.outputs)}")

            # Show step summary
            _show_execution_plan(dag)

    except WorkflowLoadError as e:
        console.print(f"[red]✗ Validation failed:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Validation error:[/red] {e}")
        raise typer.Exit(1)


def _show_execution_plan(dag: DAG):
    """Display the execution plan as a tree."""
    tree = Tree(f"[bold blue]{dag.name}[/bold blue] - Execution Plan")

    # Get execution order
    try:
        order = dag.get_execution_order()
    except Exception:
        order = list(dag.steps.keys())

    # Group by dependency level
    levels: dict[int, list[str]] = {}
    step_levels: dict[str, int] = {}

    for step_name in order:
        step = dag.steps[step_name]
        if not step.depends_on:
            level = 0
        else:
            level = max(step_levels.get(dep, 0) for dep in step.depends_on) + 1
        step_levels[step_name] = level
        levels.setdefault(level, []).append(step_name)

    for level in sorted(levels.keys()):
        level_steps = levels[level]
        if len(level_steps) > 1:
            level_node = tree.add(f"[cyan]Level {level}[/cyan] (parallel)")
            for step_name in level_steps:
                step = dag.steps[step_name]
                deps = f" ← {step.depends_on}" if step.depends_on else ""
                level_node.add(f"[yellow]{step_name}[/yellow]{deps}")
        else:
            step_name = level_steps[0]
            step = dag.steps[step_name]
            deps = f" ← {step.depends_on}" if step.depends_on else ""
            tree.add(f"[cyan]Level {level}:[/cyan] [yellow]{step_name}[/yellow]{deps}")

    console.print("\n")
    console.print(tree)


def _show_results(result, verbose: bool):
    """Display workflow execution results."""
    status_color = "green" if result.overall_status.value == "success" else "red"

    console.print(
        f"\n[bold {status_color}]Status: {result.overall_status.value.upper()}[/bold {status_color}]"
    )

    if verbose or result.overall_status.value != "success":
        table = Table(title="Step Results")
        table.add_column("Step", style="cyan")
        table.add_column("Status")
        table.add_column("Duration")

        for step in result.steps:
            status = step.status.value
            if status == "success":
                status_styled = "[green]✓[/green] success"
            elif status == "failed":
                status_styled = "[red]✗[/red] failed"
            elif status == "skipped":
                status_styled = "[yellow]⊘[/yellow] skipped"
            else:
                status_styled = status

            duration = "N/A"
            if hasattr(step, "duration_ms") and step.duration_ms:
                duration = f"{step.duration_ms:.0f}ms"

            table.add_row(step.step_name, status_styled, duration)

        console.print(table)


def _list_workflows():
    """List available workflows."""
    loader = _get_workflow_loader()
    workflows = loader.list_workflows()

    if not workflows:
        console.print("[yellow]No workflows found in definitions directory.[/yellow]")
        return

    table = Table(title="Available Workflows")
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    table.add_column("Steps", justify="right")

    for name in workflows:
        try:
            wf = loader.load(name)
            table.add_row(name, wf.description or "-", str(len(wf.dag.steps)))
        except Exception:
            table.add_row(name, "[red]Error loading[/red]", "-")

    console.print(table)


def _list_agents():
    """List available agents."""
    agents = [
        ("CoderAgent", "Tier 2", "Code generation and modification"),
        ("ReviewerAgent", "Tier 2", "Code review and quality analysis"),
        ("TestAgent", "Tier 2", "Test generation and validation"),
        ("ArchitectAgent", "Tier 2", "Architecture planning and tech stack selection"),
        ("OrchestratorAgent", "Tier 3", "Dynamic workflow planning and coordination"),
    ]

    table = Table(title="Available Agents")
    table.add_column("Agent", style="cyan")
    table.add_column("Tier")
    table.add_column("Description")

    for name, tier, desc in agents:
        table.add_row(name, tier, desc)

    console.print(table)


def _list_tools():
    """List available tools."""
    # Import tools registry
    try:
        from ..tools import ToolRegistry

        registry = ToolRegistry()
        tools = registry.list_tools()
    except Exception:
        tools = []

    if not tools:
        console.print(
            "[yellow]No tools registered or tools module not available.[/yellow]"
        )
        console.print(
            "\n[dim]Tools are registered at runtime. Run a workflow to see available tools.[/dim]"
        )
        return

    table = Table(title="Available Tools")
    table.add_column("Tool", style="cyan")
    table.add_column("Tier")
    table.add_column("Description")

    for tool in tools:
        table.add_row(tool.name, str(tool.tier), tool.description or "-")

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
