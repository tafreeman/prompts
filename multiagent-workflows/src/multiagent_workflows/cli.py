from __future__ import annotations

import argparse
import asyncio
import json
import sys
import webbrowser
from pathlib import Path


def _cmd_ui(args: argparse.Namespace) -> int:
    from multiagent_workflows.server.app import main as server_main

    if args.open:
        url = f"http://{args.host}:{args.port}/"
        try:
            webbrowser.open(url)
        except Exception:
            # Non-fatal: server will still start.
            pass

    return server_main(["--host", args.host, "--port", str(args.port)])


def _cmd_run(args: argparse.Namespace) -> int:
    """Run a workflow from the command line."""
    from multiagent_workflows.core.model_manager import ModelManager
    from multiagent_workflows.core.workflow_engine import WorkflowEngine

    model_manager = ModelManager()
    engine = WorkflowEngine(model_manager=model_manager)

    # List workflows if requested
    if args.list:
        print("Available workflows:")
        for wf in engine.list_workflows():
            print(f"  - {wf['name']}: {wf.get('description', '')}")
        return 0

    if not args.workflow:
        print("Error: --workflow is required (or use --list)")
        return 1

    # Load inputs
    inputs = {}
    if args.input:
        input_path = Path(args.input)
        if input_path.exists():
            with open(input_path) as f:
                inputs = json.load(f)
        else:
            # Try parsing as JSON directly
            try:
                inputs = json.loads(args.input)
            except json.JSONDecodeError:
                # Treat as simple requirements text
                inputs = {"requirements": args.input}

    print(f"Running workflow: {args.workflow}")
    print(f"Inputs: {json.dumps(inputs, indent=2)[:200]}...")

    # Run the workflow
    try:
        result = asyncio.run(engine.execute_workflow(
            workflow_name=args.workflow,
            inputs=inputs,
        ))
        print("\n" + "=" * 60)
        print(f"Workflow completed: {'SUCCESS' if result.success else 'FAILED'}")
        if result.error:
            print(f"Error: {result.error}")
        print(f"Output keys: {list(result.outputs.keys())}")

        # Save output
        if args.output:
            with open(args.output, "w") as f:
                json.dump({
                    "success": result.success,
                    "outputs": result.outputs,
                    "error": result.error,
                }, f, indent=2, default=str)
            print(f"Output saved to: {args.output}")

        return 0 if result.success else 1

    except Exception as e:
        print(f"Error running workflow: {e}")
        import traceback
        traceback.print_exc()
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="multiagent", description="Multi-Agent Workflows CLI"
    )
    sub = parser.add_subparsers(dest="command")

    p_ui = sub.add_parser("ui", help="Start the local UI + API server")
    p_ui.add_argument("--host", default="127.0.0.1")
    p_ui.add_argument("--port", default=8000, type=int)
    p_ui.add_argument(
        "--open", action="store_true", help="Open the UI in your default browser"
    )
    p_ui.set_defaults(func=_cmd_ui)

    # Back-compat alias
    p_serve = sub.add_parser("serve", help="Alias for 'ui'")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", default=8000, type=int)
    p_serve.add_argument(
        "--open", action="store_true", help="Open the UI in your default browser"
    )
    p_serve.set_defaults(func=_cmd_ui)

    # Run command
    p_run = sub.add_parser("run", help="Run a workflow")
    p_run.add_argument("--workflow", "-w", help="Workflow name to run")
    p_run.add_argument("--input", "-i", help="Input JSON file or JSON string")
    p_run.add_argument("--output", "-o", help="Output file path for results")
    p_run.add_argument("--list", "-l", action="store_true", help="List available workflows")
    p_run.set_defaults(func=_cmd_run)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not getattr(args, "command", None):
        parser.print_help()
        return 2

    func = getattr(args, "func", None)
    if not func:
        parser.print_help()
        return 2

    return int(func(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

