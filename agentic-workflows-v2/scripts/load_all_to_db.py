#!/usr/bin/env python3
"""Load catalog metadata + datasets (including full Hugging Face pulls) into SQLite."""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT.parent
PACKAGE_ROOT = PROJECT_ROOT / "agentic_v2"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.append(str(PACKAGE_ROOT))

from storage.catalog import CatalogStore
from storage.database import Database
from tools.agents.benchmarks.datasets import BENCHMARK_DEFINITIONS, DataSource
from tools.agents.benchmarks.loader import load_benchmark


def _default_db_path() -> Path:
    override = os.environ.get("AGENTIC_V2_DB_PATH")
    if override:
        return Path(override).expanduser().resolve()
    return (WORKSPACE_ROOT / "runs" / "agentic_v2.sqlite3").resolve()


def _table_count(db_path: Path, table: str) -> int:
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        return int(row[0]) if row else 0


def _sync_catalog(db: Database) -> None:
    store = CatalogStore(db=db, project_root=PROJECT_ROOT)
    store.sync_static_catalog()


def _sync_hf_datasets(
    db: Database,
    *,
    use_cache: bool,
    include: set[str] | None = None,
    exclude: set[str] | None = None,
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "benchmarks": 0,
        "rows_inserted": 0,
        "dataset_ids": [],
    }
    include = include or set()
    exclude = exclude or set()

    for benchmark_id, definition in BENCHMARK_DEFINITIONS.items():
        if definition.source != DataSource.HUGGINGFACE:
            continue
        if include and benchmark_id not in include:
            continue
        if benchmark_id in exclude:
            continue

        tasks = load_benchmark(
            benchmark_id=benchmark_id,
            limit=None,
            offset=0,
            use_cache=use_cache,
        )
        db.upsert_dataset_metadata(
            {
                "id": benchmark_id,
                "source": "huggingface",
                "name": definition.name,
                "path": definition.source_url,
                "description": definition.description,
                "sample_count": len(tasks),
                "benchmark_type": definition.benchmark_type.value,
                "source_config": definition.source_config,
                "metrics": definition.metrics,
                "evaluation_method": definition.evaluation_method,
                "license": definition.license,
                "paper_url": definition.paper_url,
                "leaderboard_url": definition.leaderboard_url,
            }
        )

        rows = []
        for index, task in enumerate(tasks):
            payload = task.to_dict() if hasattr(task, "to_dict") else dict(task)
            rows.append(
                {
                    "sample_index": index,
                    "task_id": str(payload.get("task_id") or index),
                    "sample": payload,
                    "metadata": {
                        "source": "huggingface",
                        "benchmark_id": benchmark_id,
                        "hf_dataset": definition.source_url,
                    },
                }
            )
        inserted = db.upsert_dataset_samples_bulk(dataset_id=benchmark_id, rows=rows)
        summary["benchmarks"] += 1
        summary["rows_inserted"] += inserted
        summary["dataset_ids"].append(benchmark_id)
        print(f"[hf] {benchmark_id}: {inserted} rows")

    return summary


def _import_runs(db: Database) -> dict[str, int]:
    totals = {"runs": 0, "attempts": 0}
    for root in [WORKSPACE_ROOT / "runs", PROJECT_ROOT / "runs"]:
        result = db.import_runs_directory(root)
        totals["runs"] += int(result.get("runs", 0))
        totals["attempts"] += int(result.get("attempts", 0))
        print(f"[runs] {root}: runs={result.get('runs', 0)} attempts={result.get('attempts', 0)}")
    return totals


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--db-path",
        type=Path,
        default=_default_db_path(),
        help="SQLite file path (default: workspace runs/agentic_v2.sqlite3)",
    )
    parser.add_argument(
        "--no-hf",
        action="store_true",
        help="Skip Hugging Face benchmark ingestion",
    )
    parser.add_argument(
        "--use-cache",
        action="store_true",
        help="Use cached benchmark pulls instead of forcing remote fetch",
    )
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Benchmark id to include (repeatable)",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Benchmark id to exclude (repeatable)",
    )
    parser.add_argument(
        "--skip-runs",
        action="store_true",
        help="Skip importing JSON run logs",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    db = Database(args.db_path)

    print(f"[db] {db.path}")
    _sync_catalog(db)
    print("[catalog] synced agents/workflows/prompts/models/local datasets")

    hf_summary = {"benchmarks": 0, "rows_inserted": 0}
    if not args.no_hf:
        hf_summary = _sync_hf_datasets(
            db,
            use_cache=args.use_cache,
            include=set(args.include),
            exclude=set(args.exclude),
        )
        print(
            "[hf] benchmarks={benchmarks} rows={rows_inserted}".format(
                benchmarks=hf_summary["benchmarks"],
                rows_inserted=hf_summary["rows_inserted"],
            )
        )

    if not args.skip_runs:
        _import_runs(db)

    print("[counts]")
    for table in [
        "datasets",
        "dataset_samples",
        "agents",
        "workflows",
        "prompts",
        "models",
        "runs",
        "run_steps",
        "run_evaluations",
        "run_attempts",
    ]:
        print(f"  {table}={_table_count(db.path, table)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
