"""Catalog sync utilities for file-backed configuration artifacts."""

from __future__ import annotations

import json
import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

import yaml

from .database import Database, resolve_default_db_path, resolve_project_root

logger = logging.getLogger(__name__)


def _safe_load_yaml(path: Path) -> dict[str, Any]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        logger.warning("Failed loading YAML %s: %s", path, exc)
        return {}
    return payload if isinstance(payload, dict) else {}


def _safe_load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _pascal_case(value: str) -> str:
    return "".join(part.capitalize() for part in value.split("_") if part)


def _infer_tier(default_model: str | None) -> str:
    model = (default_model or "").lower()
    if not model:
        return "2"
    if any(prefix in model for prefix in ("local:", "ollama:", "windows-ai:")):
        return "1"
    if any(token in model for token in ("gpt-5", "claude-opus", "tier5")):
        return "5"
    if any(token in model for token in ("o4", "o3", "gpt-4", "claude-sonnet")):
        return "3"
    return "2"


def _safe_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except Exception:
        return path.resolve().as_posix()


class CatalogStore:
    """Synchronize static config files to SQLite cache tables."""

    def __init__(
        self,
        *,
        db: Database | None = None,
        project_root: Path | str | None = None,
    ):
        self.project_root = (
            Path(project_root).expanduser().resolve()
            if project_root is not None
            else resolve_project_root()
        )
        self.package_root = self.project_root / "agentic_v2"
        self.db = db or Database()

        self.agents_config_path = self.package_root / "config" / "defaults" / "agents.yaml"
        self.models_config_path = self.package_root / "config" / "defaults" / "models.yaml"
        self.workflow_definitions_dir = self.package_root / "workflows" / "definitions"
        self.prompts_dir = self.package_root / "prompts"
        self.local_dataset_roots = [
            self.project_root / "tests" / "fixtures" / "datasets",
            self.project_root / "evaluation" / "datasets",
        ]

    # ------------------------------------------------------------------
    # Top-level sync orchestration
    # ------------------------------------------------------------------

    def sync_static_catalog(self) -> None:
        self.sync_agents_config()
        self.sync_models_config()
        self.sync_prompt_directory()
        self.sync_workflow_definitions()
        self.sync_local_dataset_files()

    # ------------------------------------------------------------------
    # Agents / prompts
    # ------------------------------------------------------------------

    def sync_agents_config(self) -> None:
        path = self.agents_config_path
        if not path.exists():
            return

        raw = path.read_text(encoding="utf-8")
        payload = _safe_load_yaml(path)
        self.db.upsert_catalog_file(
            kind="config_agents_yaml",
            logical_id="default",
            source_path=path,
            raw_content=raw,
            parsed=payload,
        )

        agents = payload.get("agents", {})
        if not isinstance(agents, dict):
            return

        for agent_id, config in agents.items():
            if not isinstance(config, dict):
                continue
            tier = _infer_tier(str(config.get("default_model", "")))
            self.db.upsert_agent(
                agent_id=str(agent_id),
                payload=config,
                source_path=path,
                tier=tier,
            )
            prompt_file = config.get("prompt_file")
            if isinstance(prompt_file, str) and prompt_file.strip():
                prompt_path = self._resolve_prompt_path(prompt_file)
                if prompt_path is not None and prompt_path.exists():
                    self.sync_prompt_file(prompt_path, prompt_name=Path(prompt_file).stem)

    def _resolve_prompt_path(self, prompt_ref: str) -> Path | None:
        candidate = Path(prompt_ref.replace("\\", "/"))
        if candidate.is_absolute():
            return candidate

        direct = (self.package_root / candidate).resolve()
        if direct.exists():
            return direct

        by_name = (self.prompts_dir / candidate.name).resolve()
        if by_name.exists():
            return by_name

        return None

    def sync_prompt_directory(self) -> None:
        if not self.prompts_dir.exists():
            return
        for prompt_path in sorted(self.prompts_dir.glob("*.md")):
            self.sync_prompt_file(prompt_path)

    def sync_prompt_file(self, prompt_path: Path, prompt_name: str | None = None) -> None:
        if not prompt_path.exists():
            return
        name = prompt_name or prompt_path.stem
        content = prompt_path.read_text(encoding="utf-8")
        self.db.upsert_prompt(
            prompt_name=name,
            content=content,
            source_path=prompt_path,
            metadata={"path": _safe_relative(prompt_path, self.project_root)},
        )

    # ------------------------------------------------------------------
    # Workflows
    # ------------------------------------------------------------------

    def sync_workflow_definitions(self, definitions_dir: Path | None = None) -> None:
        root = definitions_dir or self.workflow_definitions_dir
        if not root.exists():
            return
        for path in sorted(root.iterdir()):
            if path.suffix.lower() not in {".yaml", ".yml"}:
                continue
            self.sync_workflow_file(path)

    def sync_workflow_file(self, path: Path, data: Mapping[str, Any] | None = None) -> None:
        if not path.exists():
            return
        raw = path.read_text(encoding="utf-8")
        payload: Mapping[str, Any]
        if data is not None:
            payload = data
        else:
            parsed = yaml.safe_load(raw)
            if not isinstance(parsed, dict):
                return
            payload = parsed

        workflow_name = str(payload.get("name", path.stem))
        self.db.upsert_workflow_definition(
            workflow_name=workflow_name,
            raw_definition=payload,
            raw_yaml=raw,
            source_path=path,
        )

    # ------------------------------------------------------------------
    # Models / providers / routes
    # ------------------------------------------------------------------

    def sync_models_config(self) -> None:
        path = self.models_config_path
        if not path.exists():
            return

        raw = path.read_text(encoding="utf-8")
        payload = _safe_load_yaml(path)
        self.db.upsert_catalog_file(
            kind="config_models_yaml",
            logical_id="default",
            source_path=path,
            raw_content=raw,
            parsed=payload,
        )

        providers = payload.get("providers", {})
        if isinstance(providers, dict):
            for provider_id, cfg in providers.items():
                if not isinstance(cfg, dict):
                    continue
                available = cfg.get("available", [])
                provider_payload = dict(cfg)
                provider_payload.pop("available", None)
                self.db.upsert_model_provider(
                    provider_id=str(provider_id),
                    description=str(cfg.get("description", "")),
                    payload=provider_payload,
                    source_path=path,
                )
                if isinstance(available, list):
                    for model in available:
                        if not isinstance(model, dict):
                            continue
                        model_id = model.get("id")
                        if not model_id:
                            continue
                        self.db.upsert_model(
                            model_id=str(model_id),
                            provider_id=str(provider_id),
                            payload=model,
                            source_path=path,
                        )

        routing = payload.get("routing", {})
        if isinstance(routing, dict):
            for rule_name, cfg in routing.items():
                if not isinstance(cfg, dict):
                    continue
                preferred = cfg.get("preferred")
                fallback = cfg.get("fallback")
                self.db.upsert_model_routing_rule(
                    rule_name=str(rule_name),
                    preferred=preferred if isinstance(preferred, list) else [],
                    fallback=fallback if isinstance(fallback, list) else [],
                    payload=cfg,
                    source_path=path,
                )

        fallback_cfg = payload.get("fallback")
        if isinstance(fallback_cfg, dict):
            chain = fallback_cfg.get("chain")
            self.db.upsert_model_routing_rule(
                rule_name="_global_fallback",
                preferred=[],
                fallback=chain if isinstance(chain, list) else [],
                payload=fallback_cfg,
                source_path=path,
            )

    # ------------------------------------------------------------------
    # Datasets
    # ------------------------------------------------------------------

    def sync_dataset_affinity(self, mapping: Mapping[str, list[str]]) -> None:
        self.db.replace_dataset_affinity(mapping)

    def sync_dataset_options(self, options: list[dict[str, Any]]) -> None:
        for option in options:
            self.db.upsert_dataset_metadata(option)

    def sync_dataset_sample(
        self,
        *,
        dataset_id: str,
        sample_index: int,
        sample: dict[str, Any],
        task_id: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        source = None
        if isinstance(metadata, Mapping):
            source = metadata.get("source")

        self.db.upsert_dataset_metadata(
            {
                "id": dataset_id,
                "source": source or "unknown",
                "name": dataset_id.replace("_", " "),
                "path": metadata.get("dataset_path") if isinstance(metadata, Mapping) else None,
                "description": "",
                "sample_count": None,
            }
        )
        self.db.upsert_dataset_sample(
            dataset_id=dataset_id,
            sample_index=sample_index,
            sample=sample,
            task_id=task_id,
            metadata=metadata,
        )

    def sync_local_dataset_files(self) -> None:
        max_samples = int(os.environ.get("AGENTIC_V2_DB_MAX_DATASET_SAMPLES", "2000"))
        if max_samples <= 0:
            return

        for root in self.local_dataset_roots:
            if not root.exists() or not root.is_dir():
                continue

            for json_path in sorted(root.rglob("*.json")):
                payload = _safe_load_json(json_path)
                if payload is None:
                    continue

                dataset_id = _safe_relative(json_path, self.project_root)
                samples = self._normalize_samples(payload)
                self.db.upsert_dataset_metadata(
                    {
                        "id": dataset_id,
                        "source": "local",
                        "name": json_path.stem.replace("_", " "),
                        "path": dataset_id,
                        "description": f"Local JSON dataset ({json_path.parent.name})",
                        "sample_count": len(samples),
                    }
                )

                rows: list[dict[str, Any]] = []
                for index, sample in enumerate(samples[:max_samples]):
                    if not isinstance(sample, dict):
                        sample = {"value": sample}
                    task_id = str(sample.get("task_id") or sample.get("id") or index)
                    rows.append(
                        {
                            "sample_index": index,
                            "sample": sample,
                            "task_id": task_id,
                            "metadata": {
                                "source": "local",
                                "dataset_path": dataset_id,
                            },
                        }
                    )
                self.db.upsert_dataset_samples_bulk(dataset_id=dataset_id, rows=rows)

    @staticmethod
    def _normalize_samples(payload: Any) -> list[Any]:
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            for key in ("tasks", "samples", "items"):
                value = payload.get(key)
                if isinstance(value, list):
                    return value
            return [payload]
        return [payload]

    # ------------------------------------------------------------------
    # Read helpers
    # ------------------------------------------------------------------

    def list_agents(self) -> list[dict[str, Any]]:
        rows = self.db.list_agents()
        for row in rows:
            row["class_name"] = f"{_pascal_case(str(row['agent_id']))}Agent"
            if not row.get("name"):
                row["name"] = row["class_name"]
        return rows


@lru_cache(maxsize=8)
def _cached_store(path_key: str) -> CatalogStore:
    return CatalogStore(db=Database(path_key))


def get_catalog_store(db_path: Path | str | None = None) -> CatalogStore:
    resolved = (
        Path(db_path).expanduser().resolve()
        if db_path is not None
        else resolve_default_db_path()
    )
    return _cached_store(str(resolved))


__all__ = ["CatalogStore", "get_catalog_store"]
