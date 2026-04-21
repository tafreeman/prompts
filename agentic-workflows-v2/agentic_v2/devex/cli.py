"""Typer sub-application for developer-experience commands.

Registered in the main CLI as:  ``agentic devex <command>``
"""

from __future__ import annotations

import typer

from .port_guard import DEFAULT_PORTS, guard_ports

devex_app = typer.Typer(
    name="devex",
    help="Developer experience utilities.",
    add_completion=False,
)


@devex_app.command("port-guard")
def port_guard_cmd(
    backend_port: int = typer.Option(
        DEFAULT_PORTS["backend"],
        "--backend-port",
        help="Backend service port to check.",
    ),
    frontend_port: int = typer.Option(
        DEFAULT_PORTS["frontend"],
        "--frontend-port",
        help="Frontend service port to check.",
    ),
) -> None:
    """Check whether required service ports are available before starting."""
    from rich.console import Console

    console = Console()
    console.print("\n[bold]Port availability check[/bold]")

    ports = {"backend": backend_port, "frontend": frontend_port}
    all_free = guard_ports(ports)

    if all_free:
        console.print(
            f"\n[green]All ports free[/green] "
            f"(checked: {', '.join(str(p) for p in ports.values())})"
        )
        raise typer.Exit(code=0)
    else:
        console.print(
            "\n[red]Port conflict detected.[/red] "
            "Stop the conflicting process before starting services."
        )
        raise typer.Exit(code=1)
