#!/usr/bin/env python3
"""Query helper for the agentic SQLite database."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT.parent
PACKAGE_ROOT = PROJECT_ROOT / "agentic_v2"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.append(str(PACKAGE_ROOT))

from storage.database import Database


def _default_db_path() -> Path:
    override = os.environ.get("AGENTIC_V2_DB_PATH")
    if override:
        return Path(override).expanduser().resolve()
    return (WORKSPACE_ROOT / "runs" / "agentic_v2.sqlite3").resolve()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db-path", type=Path, default=_default_db_path())

    sub = parser.add_subparsers(dest="command", required=True)

    p_datasets = sub.add_parser("datasets", help="List dataset metadata")
    p_datasets.add_argument("--source", type=str, default=None)
    p_datasets.add_argument("--limit", type=int, default=200)

    p_samples = sub.add_parser("samples", help="List or search dataset samples")
    p_samples.add_argument("--dataset-id", type=str, default=None)
    p_samples.add_argument("--query", type=str, default=None, help="Full text search query")
    p_samples.add_argument("--limit", type=int, default=20)
    p_samples.add_argument("--offset", type=int, default=0)

    p_runs = sub.add_parser("runs", help="Query run summaries")
    p_runs.add_argument("--workflow", type=str, default=None)
    p_runs.add_argument("--status", type=str, default=None)
    p_runs.add_argument("--min-score", type=float, default=None)
    p_runs.add_argument("--model", type=str, default=None)
    p_runs.add_argument("--limit", type=int, default=50)
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    db = Database(args.db_path)

    if args.command == "datasets":
        data = db.list_datasets(source=args.source, limit=args.limit)
    elif args.command == "samples":
        data = db.query_dataset_samples(
            dataset_id=args.dataset_id,
            text_query=args.query,
            limit=args.limit,
            offset=args.offset,
        )
    elif args.command == "runs":
        data = db.query_runs(
            workflow_name=args.workflow,
            status=args.status,
            min_weighted_score=args.min_score,
            model_used=args.model,
            limit=args.limit,
        )
    else:
        parser.error(f"unknown command: {args.command}")
        return 2

    print(json.dumps(data, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
