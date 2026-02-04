from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Optional

from aiohttp import web

from .dataset_loader import list_benchmarks, load_tasks
from .models import ModelRegistry
from .run_manager import RunStore


def _json_response(payload: Any, status: int = 200) -> web.Response:
    return web.Response(
        status=status,
        text=json.dumps(payload, ensure_ascii=False, indent=2),
        content_type="application/json",
    )


def _parse_int(value: Optional[str], default: int) -> int:
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


async def handle_health(_: web.Request) -> web.Response:
    return _json_response({"ok": True})


async def handle_benchmarks(_: web.Request) -> web.Response:
    return _json_response({"benchmarks": list_benchmarks()})


async def handle_tasks(request: web.Request) -> web.Response:
    benchmark_id = request.query.get("benchmark_id")
    if not benchmark_id:
        return _json_response({"error": "benchmark_id is required"}, status=400)

    limit = _parse_int(request.query.get("limit"), default=300)
    offset = _parse_int(request.query.get("offset"), default=0)
    use_cache = request.query.get("use_cache", "true").lower() != "false"

    try:
        loaded = load_tasks(benchmark_id=benchmark_id, limit=limit, offset=offset, use_cache=use_cache)
        return _json_response({"benchmark_id": loaded.benchmark_id, "tasks": loaded.tasks})
    except KeyError:
        return _json_response({"error": f"unknown benchmark_id: {benchmark_id}"}, status=404)
    except ImportError as e:
        return _json_response({"error": str(e)}, status=500)
    except Exception as e:
        return _json_response({"error": f"failed to load tasks: {e}"}, status=500)


async def handle_models(request: web.Request) -> web.Response:
    registry: ModelRegistry = request.app["model_registry"]
    return _json_response(registry.snapshot())


async def handle_refresh_models(request: web.Request) -> web.Response:
    registry: ModelRegistry = request.app["model_registry"]
    # Kick off background discovery and return immediately.
    await registry.start_background_discovery()
    return _json_response({"ok": True, "status": registry.snapshot().get("status")})


async def handle_probe_model(request: web.Request) -> web.Response:
    model_id = request.match_info.get("model_id")
    if not model_id:
        return _json_response({"error": "model_id is required"}, status=400)
    registry: ModelRegistry = request.app["model_registry"]
    try:
        result = await asyncio.to_thread(registry.check_model, model_id)
        return _json_response({"probe": result})
    except Exception as e:
        return _json_response({"error": str(e)}, status=500)


async def handle_create_run(request: web.Request) -> web.Response:
    try:
        payload = await request.json()
    except Exception:
        return _json_response({"error": "invalid JSON"}, status=400)

    benchmark_id = payload.get("benchmark_id")
    if not benchmark_id:
        return _json_response({"error": "benchmark_id is required"}, status=400)

    task_ids = payload.get("task_ids") or []
    if not isinstance(task_ids, list) or not all(isinstance(x, (str, int)) for x in task_ids):
        return _json_response({"error": "task_ids must be a list of strings"}, status=400)

    workflow = payload.get("workflow") or "fullstack"
    model = payload.get("model") or None
    use_cache = bool(payload.get("use_cache", True))

    # If a model is specified, probe it once up front so we fail fast with a useful message.
    if model:
        registry: ModelRegistry = request.app["model_registry"]
        try:
            probe = await asyncio.to_thread(registry.check_model, str(model))
            if probe and (probe.get("usable") is False):
                return _json_response(
                    {
                        "error": f"Model not usable: {model}",
                        "probe": probe,
                    },
                    status=400,
                )
        except Exception as e:
            return _json_response({"error": f"failed to probe model: {e}"}, status=500)

    store: RunStore = request.app["run_store"]
    run_id = store.create_run(
        benchmark_id=str(benchmark_id),
        task_ids=[str(x) for x in task_ids],
        workflow=str(workflow),
        model=str(model) if model else None,
        use_cache=use_cache,
    )
    return _json_response({"run_id": run_id})


async def handle_get_run(request: web.Request) -> web.Response:
    run_id = request.match_info.get("run_id")
    if not run_id:
        return _json_response({"error": "run_id is required"}, status=400)
    store: RunStore = request.app["run_store"]
    run = store.get_run(run_id)
    if not run:
        return _json_response({"error": f"unknown run_id: {run_id}"}, status=404)
    return _json_response(run)


async def handle_list_runs(request: web.Request) -> web.Response:
    store: RunStore = request.app["run_store"]
    return _json_response({"runs": store.list_runs()})


def _repo_root_from_here() -> Path:
    # .../multiagent-workflows/src/multiagent_workflows/server/app.py -> parents[3] == multiagent-workflows
    return Path(__file__).resolve().parents[3]


def _monorepo_root_from_here() -> Path:
    # .../multiagent-workflows/src/multiagent_workflows/server/app.py -> parents[4] == repo root
    return Path(__file__).resolve().parents[4]


async def handle_list_agents(request: web.Request) -> web.Response:
    try:
        agents_map = {}
        config_dir = _monorepo_root_from_here() / "workflows" / "agentic_planning" / "configs"
        if not config_dir.exists():
             return _json_response({"error": f"Config dir not found: {config_dir}"}, status=404)

        for p in config_dir.glob("workflow_*.json"):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for a in data.get("agents", []):
                        # Ensure we capture tool/mcp fields if missing
                        if "tools" not in a: a["tools"] = []
                        if "mcp_servers" not in a: a["mcp_servers"] = []
                        
                        a["_source_workflow"] = data.get("description", p.name)
                        a["_source_file"] = p.name
                        agents_map[a["id"]] = a
            except Exception as e:
                print(f"Error reading {p}: {e}")

        return _json_response({"agents": list(agents_map.values())})
    except Exception as e:
        return _json_response({"error": str(e)}, status=500)


async def handle_update_agent(request: web.Request) -> web.Response:
    try:
        payload = await request.json()
        agent_id = payload.get("id")
        if not agent_id:
            return _json_response({"error": "id is required"}, status=400)

        config_dir = _monorepo_root_from_here() / "workflows" / "agentic_planning" / "configs"
        updated = False
        
        for p in config_dir.glob("workflow_*.json"):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                found = False
                for a in data.get("agents", []):
                    if a["id"] == agent_id:
                        # Update fields
                        for k in ["system_prompt", "model", "temperature", "max_tokens", "tools", "mcp_servers"]:
                            if k in payload:
                                a[k] = payload[k]
                        found = True
                        updated = True
                
                if found:
                    with open(p, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent="\t") # Use tab/4 spaces to match style
                    return _json_response({"ok": True, "agent_id": agent_id})
                    
            except Exception as e:
                print(f"Error updating {p}: {e}")
                
        if not updated:
            return _json_response({"error": "Agent not found"}, status=404)
            
    except Exception as e:
        return _json_response({"error": str(e)}, status=500)


def create_app() -> web.Application:
    app = web.Application()

    # Ensure repo root is on sys.path so `import tools.*` works even when cwd is multiagent-workflows.
    repo_root = str(_monorepo_root_from_here())
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    app["run_store"] = RunStore()
    app["model_registry"] = ModelRegistry()

    async def _startup(app_: web.Application) -> None:
        # Start model discovery in the background; do not block server startup.
        registry: ModelRegistry = app_["model_registry"]
        await registry.start_background_discovery()

    app.on_startup.append(_startup)

    async def _cleanup_ctx(app_: web.Application):
        yield
        store: RunStore = app_["run_store"]
        await store.shutdown()

    app.cleanup_ctx.append(_cleanup_ctx)

    # API
    app.router.add_get("/api/health", handle_health)
    app.router.add_get("/api/benchmarks", handle_benchmarks)
    app.router.add_get("/api/tasks", handle_tasks)
    app.router.add_get("/api/models", handle_models)
    app.router.add_post("/api/models/refresh", handle_refresh_models)
    app.router.add_get("/api/models/{model_id}/probe", handle_probe_model)
    app.router.add_get("/api/runs", handle_list_runs)
    app.router.add_post("/api/runs", handle_create_run)
    app.router.add_get("/api/runs/{run_id}", handle_get_run)
    app.router.add_get("/api/agents", handle_list_agents)
    app.router.add_post("/api/agents/update", handle_update_agent)

    # UI (served from same origin to avoid CORS issues)
    ui_dir = _repo_root_from_here() / "ui"
    index_path = ui_dir / "index.html"

    async def handle_index(_: web.Request) -> web.StreamResponse:
        if not index_path.exists():
            return _json_response({"error": f"UI not found at {index_path}"}, status=404)
        return web.FileResponse(path=index_path)

    app.router.add_get("/", handle_index)
    app.router.add_static("/ui/", path=ui_dir, show_index=True)

    return app


def main(argv: Optional[list[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Multi-Agent Workflows UI + Dataset API server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8000, type=int)
    args = parser.parse_args(argv)

    web.run_app(create_app(), host=args.host, port=args.port)
    return 0
