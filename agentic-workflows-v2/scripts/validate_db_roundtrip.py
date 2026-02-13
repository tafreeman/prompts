#!/usr/bin/env python3
"""Validate database save/update/query behavior with a deterministic roundtrip."""

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

from storage.database import Database


def _default_db_path() -> Path:
    override = os.environ.get("AGENTIC_V2_DB_PATH")
    if override:
        return Path(override).expanduser().resolve()
    return (WORKSPACE_ROOT / "runs" / "agentic_v2.sqlite3").resolve()


def _cleanup_test_rows(db_path: Path, dataset_id: str) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM dataset_samples WHERE dataset_id = ?", (dataset_id,))
        conn.execute("DELETE FROM datasets WHERE dataset_id = ?", (dataset_id,))
        if conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='dataset_samples_fts'"
        ).fetchone():
            conn.execute("DELETE FROM dataset_samples_fts WHERE dataset_id = ?", (dataset_id,))
        if conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='dataset_sample_search'"
        ).fetchone():
            conn.execute("DELETE FROM dataset_sample_search WHERE dataset_id = ?", (dataset_id,))
        conn.commit()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db-path", type=Path, default=_default_db_path())
    args = parser.parse_args()

    db = Database(args.db_path)
    dataset_id = "__db_roundtrip_test__"
    _cleanup_test_rows(db.path, dataset_id)

    db.upsert_dataset_metadata(
        {
            "id": dataset_id,
            "source": "test",
            "name": "DB Roundtrip Test",
            "description": "Synthetic validation dataset",
            "sample_count": 1,
        }
    )
    db.upsert_dataset_sample(
        dataset_id=dataset_id,
        sample_index=0,
        task_id="roundtrip-0",
        sample={"prompt": "hello world", "expected_output": "v1"},
        metadata={"version": 1},
    )

    initial = db.get_dataset_sample(dataset_id, 0)
    if not initial or initial["sample"].get("expected_output") != "v1":
        raise SystemExit("roundtrip failed: initial save not found")

    db.upsert_dataset_sample(
        dataset_id=dataset_id,
        sample_index=0,
        task_id="roundtrip-0",
        sample={"prompt": "hello world updated", "expected_output": "v2"},
        metadata={"version": 2},
    )
    updated = db.get_dataset_sample(dataset_id, 0)
    if not updated or updated["sample"].get("expected_output") != "v2":
        raise SystemExit("roundtrip failed: update not persisted")

    search = db.query_dataset_samples(dataset_id=dataset_id, text_query="updated", limit=10)
    if not search:
        raise SystemExit("roundtrip failed: updated sample not searchable")

    _cleanup_test_rows(db.path, dataset_id)
    print("PASS: save/update/query roundtrip succeeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
