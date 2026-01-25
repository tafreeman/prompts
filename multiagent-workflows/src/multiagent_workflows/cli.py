from __future__ import annotations

import argparse
import sys
import webbrowser


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="multiagent", description="Multi-Agent Workflows CLI")
    sub = parser.add_subparsers(dest="command")

    p_ui = sub.add_parser("ui", help="Start the local UI + API server")
    p_ui.add_argument("--host", default="127.0.0.1")
    p_ui.add_argument("--port", default=8000, type=int)
    p_ui.add_argument("--open", action="store_true", help="Open the UI in your default browser")
    p_ui.set_defaults(func=_cmd_ui)

    # Back-compat alias
    p_serve = sub.add_parser("serve", help="Alias for 'ui'")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", default=8000, type=int)
    p_serve.add_argument("--open", action="store_true", help="Open the UI in your default browser")
    p_serve.set_defaults(func=_cmd_ui)

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
