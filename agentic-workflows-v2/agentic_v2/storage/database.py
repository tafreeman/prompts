"""SQLite storage backend for workflow runtime metadata.

The database is intentionally lightweight and stdlib-only (`sqlite3`), with:
- schema versioning via `schema_version`
- idempotent upserts for file-backed catalogs and runtime artifacts
- query helpers for common dashboard and analysis use cases
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _json_dumps(value: Any) -> str | None:
    if value is None:
        return None
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    except TypeError:
        return json.dumps(str(value), ensure_ascii=False)


def _json_loads(value: str | None) -> Any:
    if value in (None, ""):
        return None
    try:
        return json.loads(value)
    except Exception:
        return value


def _to_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def resolve_project_root() -> Path:
    """Resolve repo root for the package layout."""
    return Path(__file__).resolve().parents[2]


def resolve_default_db_path() -> Path:
    """Resolve default SQLite file path."""
    override = os.environ.get("AGENTIC_V2_DB_PATH")
    if override:
        return Path(override).expanduser().resolve()
    return resolve_project_root() / "runs" / "agentic_v2.sqlite3"


class Database:
    """Minimal repository + analytics wrapper around sqlite3."""

    SCHEMA_VERSION = 2

    def __init__(self, db_path: Path | str | None = None):
        resolved = (
            Path(db_path).expanduser().resolve()
            if db_path is not None
            else resolve_default_db_path()
        )
        self.path = resolved
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    # ------------------------------------------------------------------
    # Init / migration
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        return conn

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_version (
                    version INTEGER PRIMARY KEY,
                    applied_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS import_state (
                    key TEXT PRIMARY KEY,
                    completed_at TEXT NOT NULL,
                    details_json TEXT
                )
                """
            )
            row = conn.execute(
                "SELECT MAX(version) AS version FROM schema_version"
            ).fetchone()
            current = int(row["version"]) if row and row["version"] is not None else 0

            while current < self.SCHEMA_VERSION:
                target = current + 1
                self._apply_migration(conn, target)
                conn.execute(
                    "INSERT INTO schema_version(version, applied_at) VALUES (?, ?)",
                    (target, _utcnow()),
                )
                current = target
            conn.commit()

    def _apply_migration(self, conn: sqlite3.Connection, version: int) -> None:
        if version == 1:
            conn.executescript(_MIGRATION_001)
            return
        if version == 2:
            conn.executescript(_MIGRATION_002)
            try:
                conn.execute(
                    """
                    CREATE VIRTUAL TABLE IF NOT EXISTS dataset_samples_fts
                    USING fts5(
                        dataset_id UNINDEXED,
                        sample_index UNINDEXED,
                        task_id UNINDEXED,
                        search_text
                    )
                    """
                )
            except sqlite3.OperationalError:
                # FTS may be unavailable on some sqlite builds. Fall back to a
                # normal indexed table for prefix/LIKE queries.
                conn.executescript(_MIGRATION_002_FALLBACK)
            return
        raise ValueError(f"Unknown schema migration target: {version}")

    @staticmethod
    def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
        row = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type IN ('table','view') AND name = ?",
            (name,),
        ).fetchone()
        return row is not None

    @staticmethod
    def _build_search_text(payload: Mapping[str, Any]) -> str:
        """Extract searchable text from heterogeneous dataset sample shapes."""
        preferred_fields = [
            "prompt",
            "instruction",
            "issue_text",
            "problem_statement",
            "text",
            "question",
            "description",
            "query",
            "request",
            "body",
            "content",
            "code",
            "canonical_solution",
            "expected_output",
            "golden_patch",
        ]
        parts: list[str] = []
        for field in preferred_fields:
            value = payload.get(field)
            if isinstance(value, str) and value.strip():
                parts.append(value.strip())

        # Include nested text fragments for chat-style and benchmark metadata.
        for nested_key in ("messages", "tests", "test_cases", "test_list", "inputs"):
            value = payload.get(nested_key)
            if isinstance(value, (list, dict)):
                serialized = _json_dumps(value)
                if serialized:
                    parts.append(serialized)

        if not parts:
            serialized = _json_dumps(payload) or ""
            return serialized[:20000]

        text = "\n".join(parts)
        return text[:20000]

    # ------------------------------------------------------------------
    # Import state
    # ------------------------------------------------------------------

    def has_import_state(self, key: str) -> bool:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM import_state WHERE key = ?",
                (key,),
            ).fetchone()
            return row is not None

    def record_import_state(self, key: str, details: Mapping[str, Any] | None = None) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO import_state(key, completed_at, details_json)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    completed_at = excluded.completed_at,
                    details_json = excluded.details_json
                """,
                (key, _utcnow(), _json_dumps(details)),
            )
            conn.commit()

    # ------------------------------------------------------------------
    # Catalog upserts (YAML/markdown/JSON source caches)
    # ------------------------------------------------------------------

    def upsert_catalog_file(
        self,
        *,
        kind: str,
        logical_id: str,
        source_path: Path | str | None = None,
        raw_content: str | None = None,
        parsed: Any = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        source = None
        mtime = None
        if source_path is not None:
            try:
                path = Path(source_path).resolve()
                source = str(path)
                if path.exists():
                    mtime = datetime.fromtimestamp(
                        path.stat().st_mtime,
                        tz=timezone.utc,
                    ).isoformat()
            except Exception:
                source = str(source_path)

        content_hash = _sha256_text(raw_content) if raw_content is not None else None
        now = _utcnow()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO catalog_files (
                    kind, logical_id, source_path, content_hash, mtime,
                    raw_content, parsed_json, metadata_json, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(kind, logical_id) DO UPDATE SET
                    source_path = excluded.source_path,
                    content_hash = excluded.content_hash,
                    mtime = excluded.mtime,
                    raw_content = excluded.raw_content,
                    parsed_json = excluded.parsed_json,
                    metadata_json = excluded.metadata_json,
                    updated_at = excluded.updated_at
                """,
                (
                    kind,
                    logical_id,
                    source,
                    content_hash,
                    mtime,
                    raw_content,
                    _json_dumps(parsed),
                    _json_dumps(metadata),
                    now,
                    now,
                ),
            )
            conn.commit()

    def upsert_workflow_definition(
        self,
        *,
        workflow_name: str,
        raw_definition: Mapping[str, Any],
        raw_yaml: str,
        source_path: Path | str | None = None,
    ) -> None:
        self.upsert_catalog_file(
            kind="workflow_yaml",
            logical_id=workflow_name,
            source_path=source_path,
            raw_content=raw_yaml,
            parsed=raw_definition,
            metadata={"workflow_name": workflow_name},
        )

        description = str(raw_definition.get("description", ""))
        version = str(raw_definition.get("version", "1.0"))
        experimental = bool(raw_definition.get("experimental", False))
        capabilities = raw_definition.get("capabilities", {})
        if not isinstance(capabilities, dict):
            capabilities = {}
        steps = raw_definition.get("steps", [])
        if not isinstance(steps, list):
            steps = []
        evaluation = raw_definition.get("evaluation")
        if evaluation is not None and not isinstance(evaluation, dict):
            evaluation = {"raw": evaluation}
        now = _utcnow()

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO workflows (
                    workflow_name, version, description, experimental,
                    capabilities_inputs_json, capabilities_outputs_json,
                    evaluation_json, source_path, raw_yaml, parsed_json,
                    updated_at, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(workflow_name) DO UPDATE SET
                    version = excluded.version,
                    description = excluded.description,
                    experimental = excluded.experimental,
                    capabilities_inputs_json = excluded.capabilities_inputs_json,
                    capabilities_outputs_json = excluded.capabilities_outputs_json,
                    evaluation_json = excluded.evaluation_json,
                    source_path = excluded.source_path,
                    raw_yaml = excluded.raw_yaml,
                    parsed_json = excluded.parsed_json,
                    updated_at = excluded.updated_at
                """,
                (
                    workflow_name,
                    version,
                    description,
                    1 if experimental else 0,
                    _json_dumps(capabilities.get("inputs", [])),
                    _json_dumps(capabilities.get("outputs", [])),
                    _json_dumps(evaluation),
                    str(Path(source_path).resolve()) if source_path else None,
                    raw_yaml,
                    _json_dumps(raw_definition),
                    now,
                    now,
                ),
            )

            conn.execute("DELETE FROM workflow_steps WHERE workflow_name = ?", (workflow_name,))
            for step_index, step in enumerate(steps):
                if not isinstance(step, dict):
                    continue
                conn.execute(
                    """
                    INSERT INTO workflow_steps (
                        workflow_name, step_name, step_index, agent_name,
                        description, depends_on_json, when_expr, inputs_json,
                        outputs_json, raw_json
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        workflow_name,
                        str(step.get("name", f"step_{step_index}")),
                        step_index,
                        step.get("agent"),
                        str(step.get("description", "")),
                        _json_dumps(step.get("depends_on", [])),
                        step.get("when"),
                        _json_dumps(step.get("inputs", {})),
                        _json_dumps(step.get("outputs", {})),
                        _json_dumps(step),
                    ),
                )
            conn.commit()

    def upsert_agent(
        self,
        *,
        agent_id: str,
        payload: Mapping[str, Any],
        source_path: Path | str | None = None,
        tier: str | None = None,
    ) -> None:
        name = str(payload.get("name", agent_id))
        role = str(payload.get("role", ""))
        description = str(payload.get("description", ""))
        default_model = str(payload.get("default_model", ""))
        fallback_models = payload.get("fallback_models", [])
        tools = payload.get("tools", [])
        prompt_file = payload.get("prompt_file")
        capabilities = payload.get("capabilities")
        config = payload.get("config")
        now = _utcnow()

        self.upsert_catalog_file(
            kind="agent_yaml_entry",
            logical_id=agent_id,
            source_path=source_path,
            parsed=payload,
            metadata={"agent_id": agent_id},
        )

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO agents (
                    agent_id, name, role, description, default_model,
                    fallback_models_json, tools_json, prompt_file,
                    capabilities_json, config_json, tier,
                    source_path, updated_at, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(agent_id) DO UPDATE SET
                    name = excluded.name,
                    role = excluded.role,
                    description = excluded.description,
                    default_model = excluded.default_model,
                    fallback_models_json = excluded.fallback_models_json,
                    tools_json = excluded.tools_json,
                    prompt_file = excluded.prompt_file,
                    capabilities_json = excluded.capabilities_json,
                    config_json = excluded.config_json,
                    tier = excluded.tier,
                    source_path = excluded.source_path,
                    updated_at = excluded.updated_at
                """,
                (
                    agent_id,
                    name,
                    role,
                    description,
                    default_model,
                    _json_dumps(fallback_models if isinstance(fallback_models, list) else []),
                    _json_dumps(tools if isinstance(tools, list) else []),
                    str(prompt_file) if prompt_file is not None else None,
                    _json_dumps(capabilities),
                    _json_dumps(config),
                    tier,
                    str(Path(source_path).resolve()) if source_path else None,
                    now,
                    now,
                ),
            )
            conn.commit()

    def upsert_prompt(
        self,
        *,
        prompt_name: str,
        content: str,
        source_path: Path | str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        self.upsert_catalog_file(
            kind="prompt_markdown",
            logical_id=prompt_name,
            source_path=source_path,
            raw_content=content,
            metadata=metadata,
        )
        now = _utcnow()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO prompts (
                    prompt_name, content, source_path, content_hash, updated_at, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(prompt_name) DO UPDATE SET
                    content = excluded.content,
                    source_path = excluded.source_path,
                    content_hash = excluded.content_hash,
                    updated_at = excluded.updated_at
                """,
                (
                    prompt_name,
                    content,
                    str(Path(source_path).resolve()) if source_path else None,
                    _sha256_text(content),
                    now,
                    now,
                ),
            )
            conn.commit()

    def upsert_model_provider(
        self,
        *,
        provider_id: str,
        description: str,
        payload: Mapping[str, Any],
        source_path: Path | str | None = None,
    ) -> None:
        now = _utcnow()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO model_providers (
                    provider_id, description, config_json, source_path, updated_at, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(provider_id) DO UPDATE SET
                    description = excluded.description,
                    config_json = excluded.config_json,
                    source_path = excluded.source_path,
                    updated_at = excluded.updated_at
                """,
                (
                    provider_id,
                    description,
                    _json_dumps(payload),
                    str(Path(source_path).resolve()) if source_path else None,
                    now,
                    now,
                ),
            )
            conn.commit()

    def upsert_model(
        self,
        *,
        model_id: str,
        provider_id: str | None,
        payload: Mapping[str, Any],
        source_path: Path | str | None = None,
    ) -> None:
        now = _utcnow()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO models (
                    model_id, provider_id, name, capabilities_json, device,
                    context_length, cost_tier, config_json, source_path,
                    updated_at, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(model_id) DO UPDATE SET
                    provider_id = excluded.provider_id,
                    name = excluded.name,
                    capabilities_json = excluded.capabilities_json,
                    device = excluded.device,
                    context_length = excluded.context_length,
                    cost_tier = excluded.cost_tier,
                    config_json = excluded.config_json,
                    source_path = excluded.source_path,
                    updated_at = excluded.updated_at
                """,
                (
                    model_id,
                    provider_id,
                    str(payload.get("name", model_id)),
                    _json_dumps(payload.get("capabilities", [])),
                    payload.get("device"),
                    _to_int(payload.get("context_length")),
                    payload.get("cost_tier"),
                    _json_dumps(payload),
                    str(Path(source_path).resolve()) if source_path else None,
                    now,
                    now,
                ),
            )
            conn.commit()

    def upsert_model_routing_rule(
        self,
        *,
        rule_name: str,
        preferred: list[str] | None,
        fallback: list[str] | None,
        payload: Mapping[str, Any],
        source_path: Path | str | None = None,
    ) -> None:
        now = _utcnow()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO model_routing_rules (
                    rule_name, preferred_json, fallback_json, config_json,
                    source_path, updated_at, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(rule_name) DO UPDATE SET
                    preferred_json = excluded.preferred_json,
                    fallback_json = excluded.fallback_json,
                    config_json = excluded.config_json,
                    source_path = excluded.source_path,
                    updated_at = excluded.updated_at
                """,
                (
                    rule_name,
                    _json_dumps(preferred or []),
                    _json_dumps(fallback or []),
                    _json_dumps(payload),
                    str(Path(source_path).resolve()) if source_path else None,
                    now,
                    now,
                ),
            )
            conn.commit()

    def replace_dataset_affinity(self, mapping: Mapping[str, list[str]]) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM dataset_affinity")
            for dataset_stem, workflows in mapping.items():
                for workflow_name in workflows:
                    conn.execute(
                        """
                        INSERT INTO dataset_affinity(dataset_stem, workflow_name)
                        VALUES (?, ?)
                        """,
                        (dataset_stem, workflow_name),
                    )
            conn.commit()

    def upsert_dataset_metadata(self, option: Mapping[str, Any]) -> None:
        dataset_id = str(option.get("id", "")).strip()
        if not dataset_id:
            return
        now = _utcnow()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO datasets (
                    dataset_id, source, name, path, description, sample_count,
                    metadata_json, updated_at, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(dataset_id) DO UPDATE SET
                    source = excluded.source,
                    name = excluded.name,
                    path = excluded.path,
                    description = excluded.description,
                    sample_count = excluded.sample_count,
                    metadata_json = excluded.metadata_json,
                    updated_at = excluded.updated_at
                """,
                (
                    dataset_id,
                    option.get("source"),
                    option.get("name"),
                    option.get("path"),
                    option.get("description"),
                    _to_int(option.get("sample_count")),
                    _json_dumps(option),
                    now,
                    now,
                ),
            )
            conn.commit()

    def upsert_dataset_sample(
        self,
        *,
        dataset_id: str,
        sample_index: int,
        sample: Mapping[str, Any] | Any,
        task_id: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        payload = sample if isinstance(sample, Mapping) else {"value": sample}
        sample_json = _json_dumps(payload) or "{}"
        search_text = self._build_search_text(payload)
        now = _utcnow()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO dataset_samples (
                    dataset_id, sample_index, task_id, sample_hash,
                    sample_json, metadata_json, updated_at, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(dataset_id, sample_index) DO UPDATE SET
                    task_id = excluded.task_id,
                    sample_hash = excluded.sample_hash,
                    sample_json = excluded.sample_json,
                    metadata_json = excluded.metadata_json,
                    updated_at = excluded.updated_at
                """,
                (
                    dataset_id,
                    int(sample_index),
                    task_id,
                    _sha256_text(sample_json),
                    sample_json,
                    _json_dumps(metadata),
                    now,
                    now,
                ),
            )
            row = conn.execute(
                """
                SELECT id
                FROM dataset_samples
                WHERE dataset_id = ? AND sample_index = ?
                """,
                (dataset_id, int(sample_index)),
            ).fetchone()
            sample_row_id = int(row["id"]) if row and row["id"] is not None else None

            if self._table_exists(conn, "dataset_samples_fts"):
                conn.execute(
                    "DELETE FROM dataset_samples_fts WHERE dataset_id = ? AND sample_index = ?",
                    (dataset_id, str(sample_index)),
                )
                conn.execute(
                    """
                    INSERT INTO dataset_samples_fts(dataset_id, sample_index, task_id, search_text)
                    VALUES (?, ?, ?, ?)
                    """,
                    (dataset_id, str(sample_index), task_id or "", search_text),
                )
            elif self._table_exists(conn, "dataset_sample_search") and sample_row_id is not None:
                conn.execute(
                    """
                    INSERT INTO dataset_sample_search(sample_id, dataset_id, sample_index, task_id, search_text)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(sample_id) DO UPDATE SET
                        dataset_id = excluded.dataset_id,
                        sample_index = excluded.sample_index,
                        task_id = excluded.task_id,
                        search_text = excluded.search_text
                    """,
                    (sample_row_id, dataset_id, int(sample_index), task_id, search_text),
                )
            conn.commit()

    def upsert_dataset_samples_bulk(
        self,
        *,
        dataset_id: str,
        rows: list[dict[str, Any]],
    ) -> int:
        """Bulk upsert dataset samples in a single transaction."""
        if not rows:
            return 0

        now = _utcnow()
        inserted = 0
        with self._connect() as conn:
            has_fts = self._table_exists(conn, "dataset_samples_fts")
            has_fallback_search = self._table_exists(conn, "dataset_sample_search")

            for row in rows:
                sample_index = int(row["sample_index"])
                task_id = row.get("task_id")
                payload = row.get("sample")
                metadata = row.get("metadata")
                if not isinstance(payload, Mapping):
                    payload = {"value": payload}
                sample_json = _json_dumps(payload) or "{}"
                search_text = self._build_search_text(payload)

                conn.execute(
                    """
                    INSERT INTO dataset_samples (
                        dataset_id, sample_index, task_id, sample_hash,
                        sample_json, metadata_json, updated_at, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(dataset_id, sample_index) DO UPDATE SET
                        task_id = excluded.task_id,
                        sample_hash = excluded.sample_hash,
                        sample_json = excluded.sample_json,
                        metadata_json = excluded.metadata_json,
                        updated_at = excluded.updated_at
                    """,
                    (
                        dataset_id,
                        sample_index,
                        task_id,
                        _sha256_text(sample_json),
                        sample_json,
                        _json_dumps(metadata),
                        now,
                        now,
                    ),
                )

                if has_fts:
                    conn.execute(
                        "DELETE FROM dataset_samples_fts WHERE dataset_id = ? AND sample_index = ?",
                        (dataset_id, str(sample_index)),
                    )
                    conn.execute(
                        """
                        INSERT INTO dataset_samples_fts(dataset_id, sample_index, task_id, search_text)
                        VALUES (?, ?, ?, ?)
                        """,
                        (dataset_id, str(sample_index), task_id or "", search_text),
                    )
                elif has_fallback_search:
                    sample_row = conn.execute(
                        """
                        SELECT id
                        FROM dataset_samples
                        WHERE dataset_id = ? AND sample_index = ?
                        """,
                        (dataset_id, sample_index),
                    ).fetchone()
                    if sample_row and sample_row["id"] is not None:
                        conn.execute(
                            """
                            INSERT INTO dataset_sample_search(
                                sample_id, dataset_id, sample_index, task_id, search_text
                            )
                            VALUES (?, ?, ?, ?, ?)
                            ON CONFLICT(sample_id) DO UPDATE SET
                                dataset_id = excluded.dataset_id,
                                sample_index = excluded.sample_index,
                                task_id = excluded.task_id,
                                search_text = excluded.search_text
                            """,
                            (
                                int(sample_row["id"]),
                                dataset_id,
                                sample_index,
                                task_id,
                                search_text,
                            ),
                        )
                inserted += 1
            conn.commit()
        return inserted

    def list_datasets(self, source: str | None = None, limit: int = 200) -> list[dict[str, Any]]:
        where = ""
        params: list[Any] = []
        if source:
            where = "WHERE source = ?"
            params.append(source)
        params.append(max(1, int(limit)))

        sql = f"""
            SELECT dataset_id, source, name, path, description, sample_count, metadata_json
            FROM datasets
            {where}
            ORDER BY dataset_id
            LIMIT ?
        """
        with self._connect() as conn:
            rows = conn.execute(sql, tuple(params)).fetchall()
        output: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            item["metadata"] = _json_loads(item.pop("metadata_json"))
            output.append(item)
        return output

    def get_dataset_sample(self, dataset_id: str, sample_index: int) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT dataset_id, sample_index, task_id, sample_json, metadata_json
                FROM dataset_samples
                WHERE dataset_id = ? AND sample_index = ?
                """,
                (dataset_id, int(sample_index)),
            ).fetchone()
        if row is None:
            return None
        item = dict(row)
        item["sample"] = _json_loads(item.pop("sample_json"))
        item["metadata"] = _json_loads(item.pop("metadata_json"))
        return item

    def query_dataset_samples(
        self,
        *,
        dataset_id: str | None = None,
        text_query: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Query dataset samples quickly using FTS when available."""
        with self._connect() as conn:
            use_fts = self._table_exists(conn, "dataset_samples_fts")
            use_fallback_search = self._table_exists(conn, "dataset_sample_search")

            if text_query and use_fts:
                clauses = ["f.search_text MATCH ?"]
                params: list[Any] = [text_query]
                if dataset_id:
                    clauses.append("s.dataset_id = ?")
                    params.append(dataset_id)
                params.extend([max(1, int(limit)), max(0, int(offset))])
                sql = f"""
                    SELECT s.dataset_id, s.sample_index, s.task_id, s.sample_json, s.metadata_json
                    FROM dataset_samples s
                    JOIN dataset_samples_fts f
                      ON f.dataset_id = s.dataset_id
                     AND CAST(f.sample_index AS INTEGER) = s.sample_index
                    WHERE {' AND '.join(clauses)}
                    ORDER BY s.dataset_id, s.sample_index
                    LIMIT ? OFFSET ?
                """
                rows = conn.execute(sql, tuple(params)).fetchall()
            elif text_query and use_fallback_search:
                clauses = ["q.search_text LIKE ?"]
                params = [f"%{text_query}%"]
                if dataset_id:
                    clauses.append("s.dataset_id = ?")
                    params.append(dataset_id)
                params.extend([max(1, int(limit)), max(0, int(offset))])
                sql = f"""
                    SELECT s.dataset_id, s.sample_index, s.task_id, s.sample_json, s.metadata_json
                    FROM dataset_samples s
                    JOIN dataset_sample_search q ON q.sample_id = s.id
                    WHERE {' AND '.join(clauses)}
                    ORDER BY s.dataset_id, s.sample_index
                    LIMIT ? OFFSET ?
                """
                rows = conn.execute(sql, tuple(params)).fetchall()
            else:
                clauses = []
                params = []
                if dataset_id:
                    clauses.append("dataset_id = ?")
                    params.append(dataset_id)
                if text_query:
                    clauses.append("sample_json LIKE ?")
                    params.append(f"%{text_query}%")
                where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
                params.extend([max(1, int(limit)), max(0, int(offset))])
                sql = f"""
                    SELECT dataset_id, sample_index, task_id, sample_json, metadata_json
                    FROM dataset_samples
                    {where}
                    ORDER BY dataset_id, sample_index
                    LIMIT ? OFFSET ?
                """
                rows = conn.execute(sql, tuple(params)).fetchall()

        output: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            item["sample"] = _json_loads(item.pop("sample_json"))
            item["metadata"] = _json_loads(item.pop("metadata_json"))
            output.append(item)
        return output

    # ------------------------------------------------------------------
    # Runtime artifacts (runs/steps/evaluations/attempts)
    # ------------------------------------------------------------------

    def upsert_run_record(self, record: Mapping[str, Any], source_file: Path | str | None = None) -> None:
        run_id = str(record.get("run_id", "")).strip()
        if not run_id:
            return

        run_filename = Path(source_file).name if source_file is not None else None
        source_path = str(Path(source_file).resolve()) if source_file is not None else None
        extra = record.get("extra") if isinstance(record.get("extra"), Mapping) else {}
        evaluation = extra.get("evaluation") if isinstance(extra, Mapping) else None
        if not isinstance(evaluation, Mapping):
            evaluation = None
        now = _utcnow()

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO runs (
                    run_id, run_filename, workflow_name, status, success_rate,
                    total_duration_ms, total_retries, step_count, failed_step_count,
                    start_time, end_time, dataset_json, inputs_json, final_output_json,
                    extra_json, source_path, updated_at, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(run_id) DO UPDATE SET
                    run_filename = excluded.run_filename,
                    workflow_name = excluded.workflow_name,
                    status = excluded.status,
                    success_rate = excluded.success_rate,
                    total_duration_ms = excluded.total_duration_ms,
                    total_retries = excluded.total_retries,
                    step_count = excluded.step_count,
                    failed_step_count = excluded.failed_step_count,
                    start_time = excluded.start_time,
                    end_time = excluded.end_time,
                    dataset_json = excluded.dataset_json,
                    inputs_json = excluded.inputs_json,
                    final_output_json = excluded.final_output_json,
                    extra_json = excluded.extra_json,
                    source_path = excluded.source_path,
                    updated_at = excluded.updated_at
                """,
                (
                    run_id,
                    run_filename,
                    record.get("workflow_name"),
                    record.get("status"),
                    _to_float(record.get("success_rate")),
                    _to_float(record.get("total_duration_ms")),
                    _to_int(record.get("total_retries")),
                    _to_int(record.get("step_count")),
                    _to_int(record.get("failed_step_count")),
                    record.get("start_time"),
                    record.get("end_time"),
                    _json_dumps(record.get("dataset")),
                    _json_dumps(record.get("inputs")),
                    _json_dumps(record.get("final_output")),
                    _json_dumps(record.get("extra")),
                    source_path,
                    now,
                    now,
                ),
            )

            conn.execute("DELETE FROM run_steps WHERE run_id = ?", (run_id,))
            for step_index, step in enumerate(record.get("steps", [])):
                if not isinstance(step, Mapping):
                    continue
                conn.execute(
                    """
                    INSERT INTO run_steps (
                        run_id, step_index, step_name, status, agent_role, tier,
                        model_used, duration_ms, retry_count, tokens_used,
                        input_json, output_json, error, error_type, start_time,
                        end_time, metadata_json
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        run_id,
                        step_index,
                        step.get("step_name"),
                        step.get("status"),
                        step.get("agent_role"),
                        step.get("tier"),
                        step.get("model_used"),
                        _to_float(step.get("duration_ms")),
                        _to_int(step.get("retry_count")),
                        _to_int(step.get("tokens_used")),
                        _json_dumps(step.get("input")),
                        _json_dumps(step.get("output")),
                        step.get("error"),
                        step.get("error_type"),
                        step.get("start_time"),
                        step.get("end_time"),
                        _json_dumps(step.get("metadata")),
                    ),
                )

            if evaluation is not None:
                conn.execute(
                    """
                    INSERT INTO run_evaluations (
                        run_id, rubric, rubric_id, rubric_version, weighted_score,
                        overall_score, grade, passed, pass_threshold, criteria_json,
                        hard_gates_json, hard_gate_failures_json, step_scores_json,
                        agent_scores_json, floor_violations_json, grade_capped,
                        reporting_bundle_json, payload_json, updated_at, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(run_id) DO UPDATE SET
                        rubric = excluded.rubric,
                        rubric_id = excluded.rubric_id,
                        rubric_version = excluded.rubric_version,
                        weighted_score = excluded.weighted_score,
                        overall_score = excluded.overall_score,
                        grade = excluded.grade,
                        passed = excluded.passed,
                        pass_threshold = excluded.pass_threshold,
                        criteria_json = excluded.criteria_json,
                        hard_gates_json = excluded.hard_gates_json,
                        hard_gate_failures_json = excluded.hard_gate_failures_json,
                        step_scores_json = excluded.step_scores_json,
                        agent_scores_json = excluded.agent_scores_json,
                        floor_violations_json = excluded.floor_violations_json,
                        grade_capped = excluded.grade_capped,
                        reporting_bundle_json = excluded.reporting_bundle_json,
                        payload_json = excluded.payload_json,
                        updated_at = excluded.updated_at
                    """,
                    (
                        run_id,
                        evaluation.get("rubric"),
                        evaluation.get("rubric_id"),
                        evaluation.get("rubric_version"),
                        _to_float(evaluation.get("weighted_score")),
                        _to_float(evaluation.get("overall_score")),
                        evaluation.get("grade"),
                        1 if bool(evaluation.get("passed")) else 0,
                        _to_float(evaluation.get("pass_threshold")),
                        _json_dumps(evaluation.get("criteria")),
                        _json_dumps(evaluation.get("hard_gates")),
                        _json_dumps(evaluation.get("hard_gate_failures")),
                        _json_dumps(evaluation.get("step_scores")),
                        _json_dumps(evaluation.get("agent_scores")),
                        _json_dumps(evaluation.get("floor_violations")),
                        1 if bool(evaluation.get("grade_capped")) else 0,
                        _json_dumps(evaluation.get("reporting_bundle")),
                        _json_dumps(evaluation),
                        now,
                        now,
                    ),
                )

            conn.commit()

    def upsert_run_attempt(
        self,
        *,
        run_id: str,
        attempt_number: int,
        record: Mapping[str, Any],
        source_file: Path | str | None = None,
    ) -> None:
        now = _utcnow()
        source = str(Path(source_file).resolve()) if source_file is not None else None
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO run_attempts (
                    run_id, attempt_number, status, steps_json, final_output_json,
                    feedback_json, timestamp, source_path, updated_at, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(run_id, attempt_number) DO UPDATE SET
                    status = excluded.status,
                    steps_json = excluded.steps_json,
                    final_output_json = excluded.final_output_json,
                    feedback_json = excluded.feedback_json,
                    timestamp = excluded.timestamp,
                    source_path = excluded.source_path,
                    updated_at = excluded.updated_at
                """,
                (
                    run_id,
                    int(attempt_number),
                    record.get("status"),
                    _json_dumps(record.get("steps")),
                    _json_dumps(record.get("final_output")),
                    _json_dumps(record.get("feedback")),
                    record.get("timestamp"),
                    source,
                    now,
                    now,
                ),
            )
            conn.commit()

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def summarize_runs(self, workflow_name: str | None = None) -> dict[str, Any]:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT
                    COUNT(*) AS total_runs,
                    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) AS success,
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed,
                    AVG(total_duration_ms) AS avg_duration_ms
                FROM runs
                WHERE (? IS NULL OR workflow_name = ?)
                """,
                (workflow_name, workflow_name),
            ).fetchone()
            workflows = [
                item["workflow_name"]
                for item in conn.execute(
                    """
                    SELECT DISTINCT workflow_name
                    FROM runs
                    WHERE (? IS NULL OR workflow_name = ?)
                    ORDER BY workflow_name
                    """,
                    (workflow_name, workflow_name),
                ).fetchall()
                if item["workflow_name"] is not None
            ]
        total_runs = int(row["total_runs"]) if row and row["total_runs"] is not None else 0
        if total_runs == 0:
            return {"total_runs": 0}
        return {
            "total_runs": total_runs,
            "success": int(row["success"] or 0),
            "failed": int(row["failed"] or 0),
            "avg_duration_ms": _to_float(row["avg_duration_ms"]),
            "workflows": workflows,
        }

    def query_runs(
        self,
        *,
        workflow_name: str | None = None,
        status: str | None = None,
        min_weighted_score: float | None = None,
        model_used: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        clauses: list[str] = []
        params: list[Any] = []

        if workflow_name:
            clauses.append("r.workflow_name = ?")
            params.append(workflow_name)
        if status:
            clauses.append("r.status = ?")
            params.append(status)
        if min_weighted_score is not None:
            clauses.append("COALESCE(e.weighted_score, -1) >= ?")
            params.append(float(min_weighted_score))
        if model_used:
            clauses.append(
                """
                EXISTS (
                    SELECT 1 FROM run_steps rs
                    WHERE rs.run_id = r.run_id AND rs.model_used = ?
                )
                """
            )
            params.append(model_used)

        where_sql = ""
        if clauses:
            where_sql = "WHERE " + " AND ".join(f"({clause.strip()})" for clause in clauses)

        sql = f"""
            SELECT
                r.run_id,
                r.run_filename,
                r.workflow_name,
                r.status,
                r.success_rate,
                r.total_duration_ms,
                r.step_count,
                r.failed_step_count,
                r.start_time,
                r.end_time,
                e.weighted_score AS evaluation_score,
                e.grade AS evaluation_grade
            FROM runs r
            LEFT JOIN run_evaluations e ON e.run_id = r.run_id
            {where_sql}
            ORDER BY COALESCE(r.start_time, r.created_at) DESC
            LIMIT ?
        """
        params.append(max(1, int(limit)))

        with self._connect() as conn:
            rows = conn.execute(sql, tuple(params)).fetchall()
            return [dict(row) for row in rows]

    def agent_failure_rates(self, limit: int = 20) -> list[dict[str, Any]]:
        sql = """
            SELECT
                agent_role,
                COUNT(*) AS total_steps,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed_steps,
                ROUND(
                    100.0 * SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) / COUNT(*),
                    2
                ) AS failure_rate
            FROM run_steps
            WHERE agent_role IS NOT NULL AND agent_role <> ''
            GROUP BY agent_role
            ORDER BY failure_rate DESC, total_steps DESC
            LIMIT ?
        """
        with self._connect() as conn:
            rows = conn.execute(sql, (max(1, int(limit)),)).fetchall()
            return [dict(row) for row in rows]

    def model_score_comparison(self, limit: int = 20) -> list[dict[str, Any]]:
        sql = """
            SELECT
                rs.model_used,
                COUNT(DISTINCT rs.run_id) AS run_count,
                ROUND(AVG(e.weighted_score), 2) AS avg_weighted_score,
                ROUND(
                    100.0 * AVG(CASE WHEN r.status = 'success' THEN 1.0 ELSE 0.0 END),
                    2
                ) AS success_rate
            FROM run_steps rs
            JOIN runs r ON r.run_id = rs.run_id
            LEFT JOIN run_evaluations e ON e.run_id = rs.run_id
            WHERE rs.model_used IS NOT NULL AND rs.model_used <> ''
            GROUP BY rs.model_used
            ORDER BY avg_weighted_score IS NULL, avg_weighted_score DESC, run_count DESC
            LIMIT ?
        """
        with self._connect() as conn:
            rows = conn.execute(sql, (max(1, int(limit)),)).fetchall()
            return [dict(row) for row in rows]

    def get_run_by_filename(self, filename: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT run_id, workflow_name, status, success_rate, total_duration_ms,
                       total_retries, step_count, failed_step_count, start_time, end_time,
                       dataset_json, inputs_json, final_output_json, extra_json
                FROM runs
                WHERE run_filename = ?
                """,
                (filename,),
            ).fetchone()
            if row is None:
                return None
            payload = dict(row)
            payload["dataset"] = _json_loads(payload.pop("dataset_json"))
            payload["inputs"] = _json_loads(payload.pop("inputs_json"))
            payload["final_output"] = _json_loads(payload.pop("final_output_json"))
            payload["extra"] = _json_loads(payload.pop("extra_json"))

            steps = conn.execute(
                """
                SELECT step_name, status, agent_role, tier, model_used, duration_ms,
                       retry_count, tokens_used, input_json, output_json, error,
                       error_type, start_time, end_time, metadata_json
                FROM run_steps
                WHERE run_id = ?
                ORDER BY step_index
                """,
                (payload["run_id"],),
            ).fetchall()
            payload["steps"] = []
            for step in steps:
                item = dict(step)
                item["input"] = _json_loads(item.pop("input_json"))
                item["output"] = _json_loads(item.pop("output_json"))
                item["metadata"] = _json_loads(item.pop("metadata_json"))
                payload["steps"].append(item)
            return payload

    def get_attempt(self, run_id: str, attempt_number: int) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT attempt_number, status, steps_json, final_output_json,
                       feedback_json, timestamp
                FROM run_attempts
                WHERE run_id = ? AND attempt_number = ?
                """,
                (run_id, int(attempt_number)),
            ).fetchone()
            if row is None:
                return None
            payload = dict(row)
            payload["steps"] = _json_loads(payload.pop("steps_json"))
            payload["final_output"] = _json_loads(payload.pop("final_output_json"))
            payload["feedback"] = _json_loads(payload.pop("feedback_json"))
            return payload

    def list_agents(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT agent_id, name, role, description, default_model,
                       fallback_models_json, tools_json, prompt_file,
                       capabilities_json, config_json, tier
                FROM agents
                ORDER BY agent_id
                """
            ).fetchall()
        output: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            item["fallback_models"] = _json_loads(item.pop("fallback_models_json")) or []
            item["tools"] = _json_loads(item.pop("tools_json")) or []
            item["capabilities"] = _json_loads(item.pop("capabilities_json")) or []
            item["config"] = _json_loads(item.pop("config_json")) or {}
            output.append(item)
        return output

    # ------------------------------------------------------------------
    # Legacy file imports
    # ------------------------------------------------------------------

    def _normalize_subagent_run_payload(
        self, payload: Mapping[str, Any], source_path: Path
    ) -> Mapping[str, Any] | None:
        # Support legacy subagent logs under runs/subagents/*.json.
        subagents = payload.get("subagents")
        if not isinstance(subagents, list):
            return None

        timestamp = payload.get("timestamp")
        wave = str(payload.get("wave") or "subagent").strip().lower().replace(" ", "_")
        workflow_name = f"{wave}_subagents" if wave else "subagents"

        steps: list[dict[str, Any]] = []
        failed = 0
        for index, item in enumerate(subagents):
            if not isinstance(item, Mapping):
                continue

            evaluation = item.get("evaluation")
            verdict = ""
            if isinstance(evaluation, Mapping):
                verdict = str(evaluation.get("verdict") or "").strip().lower()

            status = "failed" if verdict in {"blocked", "failed", "poor", "weak"} else "success"
            if status == "failed":
                failed += 1

            steps.append(
                {
                    "step_name": str(item.get("id") or f"subagent_{index}"),
                    "status": status,
                    "agent_role": item.get("title") or item.get("id"),
                    "output": item.get("parsed_output"),
                    "metadata": {
                        "focus": item.get("focus"),
                        "verdict": verdict or None,
                        "overall_score": (
                            evaluation.get("overall_score")
                            if isinstance(evaluation, Mapping)
                            else None
                        ),
                    },
                }
            )

        return {
            "run_id": source_path.stem,
            "run_filename": source_path.name,
            "workflow_name": workflow_name,
            "status": "failed" if failed else "success",
            "step_count": len(steps),
            "failed_step_count": failed,
            "start_time": timestamp,
            "end_time": timestamp,
            "steps": steps,
            "extra": dict(payload),
        }

    def import_run_file(self, path: Path) -> bool:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return False
        if not isinstance(payload, Mapping):
            return False

        normalized: Mapping[str, Any]
        if "run_id" in payload:
            normalized = payload
        else:
            normalized = self._normalize_subagent_run_payload(payload, path) or {}
            if not normalized:
                return False

        self.upsert_run_record(normalized, source_file=path)
        return True

    def import_attempt_file(self, path: Path, run_id: str | None = None) -> bool:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return False
        if not isinstance(payload, Mapping):
            return False
        attempt_number = _to_int(payload.get("attempt_number"))
        if attempt_number is None:
            return False
        if run_id is None:
            # .../<run_id>/attempts/<n>/attempt.json
            parts = path.parts
            if "attempts" in parts:
                idx = parts.index("attempts")
                if idx > 0:
                    run_id = parts[idx - 1]
        if not run_id:
            return False
        self.upsert_run_attempt(
            run_id=run_id,
            attempt_number=attempt_number,
            record=payload,
            source_file=path,
        )
        return True

    def import_runs_directory(self, runs_dir: Path | str) -> dict[str, int]:
        root = Path(runs_dir)
        imported_runs = 0
        imported_attempts = 0
        if not root.exists():
            return {"runs": 0, "attempts": 0}

        for candidate in sorted(root.rglob("*.json")):
            if candidate.name == "attempt.json" and "attempts" in candidate.parts:
                continue
            if self.import_run_file(candidate):
                imported_runs += 1

        for attempt_file in sorted(root.rglob("attempt.json")):
            if self.import_attempt_file(attempt_file):
                imported_attempts += 1

        return {"runs": imported_runs, "attempts": imported_attempts}

    def import_runs_directory_once(self, runs_dir: Path | str) -> dict[str, Any]:
        key = f"runs_import::{Path(runs_dir).resolve()}"
        if self.has_import_state(key):
            return {"skipped": True, "runs": 0, "attempts": 0}
        details = self.import_runs_directory(runs_dir)
        self.record_import_state(key, details)
        return {"skipped": False, **details}


_MIGRATION_001 = """
CREATE TABLE IF NOT EXISTS catalog_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,
    logical_id TEXT NOT NULL,
    source_path TEXT,
    content_hash TEXT,
    mtime TEXT,
    raw_content TEXT,
    parsed_json TEXT,
    metadata_json TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(kind, logical_id)
);

CREATE TABLE IF NOT EXISTS workflows (
    workflow_name TEXT PRIMARY KEY,
    version TEXT,
    description TEXT,
    experimental INTEGER NOT NULL DEFAULT 0,
    capabilities_inputs_json TEXT,
    capabilities_outputs_json TEXT,
    evaluation_json TEXT,
    source_path TEXT,
    raw_yaml TEXT,
    parsed_json TEXT,
    updated_at TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS workflow_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_name TEXT NOT NULL,
    step_name TEXT NOT NULL,
    step_index INTEGER NOT NULL,
    agent_name TEXT,
    description TEXT,
    depends_on_json TEXT,
    when_expr TEXT,
    inputs_json TEXT,
    outputs_json TEXT,
    raw_json TEXT,
    UNIQUE(workflow_name, step_name),
    FOREIGN KEY(workflow_name) REFERENCES workflows(workflow_name) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS prompts (
    prompt_name TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    source_path TEXT,
    content_hash TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS agents (
    agent_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT,
    description TEXT,
    default_model TEXT,
    fallback_models_json TEXT,
    tools_json TEXT,
    prompt_file TEXT,
    capabilities_json TEXT,
    config_json TEXT,
    tier TEXT,
    source_path TEXT,
    updated_at TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS model_providers (
    provider_id TEXT PRIMARY KEY,
    description TEXT,
    config_json TEXT,
    source_path TEXT,
    updated_at TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS models (
    model_id TEXT PRIMARY KEY,
    provider_id TEXT,
    name TEXT,
    capabilities_json TEXT,
    device TEXT,
    context_length INTEGER,
    cost_tier TEXT,
    config_json TEXT,
    source_path TEXT,
    updated_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(provider_id) REFERENCES model_providers(provider_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS model_routing_rules (
    rule_name TEXT PRIMARY KEY,
    preferred_json TEXT,
    fallback_json TEXT,
    config_json TEXT,
    source_path TEXT,
    updated_at TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS datasets (
    dataset_id TEXT PRIMARY KEY,
    source TEXT,
    name TEXT,
    path TEXT,
    description TEXT,
    sample_count INTEGER,
    metadata_json TEXT,
    updated_at TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dataset_samples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id TEXT NOT NULL,
    sample_index INTEGER NOT NULL,
    task_id TEXT,
    sample_hash TEXT,
    sample_json TEXT NOT NULL,
    metadata_json TEXT,
    updated_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(dataset_id, sample_index),
    FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS dataset_affinity (
    dataset_stem TEXT NOT NULL,
    workflow_name TEXT NOT NULL,
    PRIMARY KEY(dataset_stem, workflow_name)
);

CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    run_filename TEXT,
    workflow_name TEXT,
    status TEXT,
    success_rate REAL,
    total_duration_ms REAL,
    total_retries INTEGER,
    step_count INTEGER,
    failed_step_count INTEGER,
    start_time TEXT,
    end_time TEXT,
    dataset_json TEXT,
    inputs_json TEXT,
    final_output_json TEXT,
    extra_json TEXT,
    source_path TEXT,
    updated_at TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS run_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    step_index INTEGER NOT NULL,
    step_name TEXT,
    status TEXT,
    agent_role TEXT,
    tier TEXT,
    model_used TEXT,
    duration_ms REAL,
    retry_count INTEGER,
    tokens_used INTEGER,
    input_json TEXT,
    output_json TEXT,
    error TEXT,
    error_type TEXT,
    start_time TEXT,
    end_time TEXT,
    metadata_json TEXT,
    UNIQUE(run_id, step_index),
    FOREIGN KEY(run_id) REFERENCES runs(run_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS run_evaluations (
    run_id TEXT PRIMARY KEY,
    rubric TEXT,
    rubric_id TEXT,
    rubric_version TEXT,
    weighted_score REAL,
    overall_score REAL,
    grade TEXT,
    passed INTEGER,
    pass_threshold REAL,
    criteria_json TEXT,
    hard_gates_json TEXT,
    hard_gate_failures_json TEXT,
    step_scores_json TEXT,
    agent_scores_json TEXT,
    floor_violations_json TEXT,
    grade_capped INTEGER,
    reporting_bundle_json TEXT,
    payload_json TEXT,
    updated_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(run_id) REFERENCES runs(run_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS run_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    attempt_number INTEGER NOT NULL,
    status TEXT,
    steps_json TEXT,
    final_output_json TEXT,
    feedback_json TEXT,
    timestamp TEXT,
    source_path TEXT,
    updated_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(run_id, attempt_number),
    FOREIGN KEY(run_id) REFERENCES runs(run_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_catalog_kind ON catalog_files(kind);
CREATE INDEX IF NOT EXISTS idx_workflow_steps_workflow ON workflow_steps(workflow_name, step_index);
CREATE INDEX IF NOT EXISTS idx_models_provider ON models(provider_id);
CREATE INDEX IF NOT EXISTS idx_dataset_samples_dataset ON dataset_samples(dataset_id, sample_index);
CREATE INDEX IF NOT EXISTS idx_dataset_affinity_workflow ON dataset_affinity(workflow_name);
CREATE INDEX IF NOT EXISTS idx_runs_workflow_start ON runs(workflow_name, start_time DESC);
CREATE INDEX IF NOT EXISTS idx_runs_status ON runs(status);
CREATE INDEX IF NOT EXISTS idx_runs_filename ON runs(run_filename);
CREATE INDEX IF NOT EXISTS idx_run_steps_run ON run_steps(run_id, step_index);
CREATE INDEX IF NOT EXISTS idx_run_steps_model ON run_steps(model_used);
CREATE INDEX IF NOT EXISTS idx_run_steps_agent ON run_steps(agent_role);
CREATE INDEX IF NOT EXISTS idx_run_eval_score ON run_evaluations(weighted_score);
"""

_MIGRATION_002 = """
CREATE INDEX IF NOT EXISTS idx_dataset_samples_task_id ON dataset_samples(task_id);
CREATE INDEX IF NOT EXISTS idx_dataset_samples_hash ON dataset_samples(sample_hash);
"""

_MIGRATION_002_FALLBACK = """
CREATE TABLE IF NOT EXISTS dataset_sample_search (
    sample_id INTEGER PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    sample_index INTEGER NOT NULL,
    task_id TEXT,
    search_text TEXT NOT NULL,
    FOREIGN KEY(sample_id) REFERENCES dataset_samples(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_dataset_search_dataset ON dataset_sample_search(dataset_id, sample_index);
CREATE INDEX IF NOT EXISTS idx_dataset_search_task_id ON dataset_sample_search(task_id);
"""


__all__ = [
    "Database",
    "resolve_default_db_path",
    "resolve_project_root",
]
