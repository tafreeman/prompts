#!/usr/bin/env python3
"""Sync agent/workflow/prompt/model catalogs into SQLite."""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT.parent
PACKAGE_ROOT = PROJECT_ROOT / "agentic_v2"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.append(str(PACKAGE_ROOT))

from storage.catalog import CatalogStore
from storage.database import Database


def _default_db_path() -> Path:
    override = os.environ.get("AGENTIC_V2_DB_PATH")
    if override:
        return Path(override).expanduser().resolve()
    return (WORKSPACE_ROOT / "runs" / "agentic_v2.sqlite3").resolve()


def _count(conn: sqlite3.Connection, table: str) -> int:
    row = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    return int(row[0]) if row else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db-path", type=Path, default=_default_db_path())
    args = parser.parse_args()

    db = Database(args.db_path)
    store = CatalogStore(db=db, project_root=PROJECT_ROOT)
    store.sync_static_catalog()

    with sqlite3.connect(db.path) as conn:
        print(f"db={db.path}")
        for table in ["agents", "workflows", "workflow_steps", "prompts", "models", "datasets", "dataset_samples"]:
            print(f"{table}={_count(conn, table)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
