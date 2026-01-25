"""Dataset loaders for evaluation integration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List
import json


@dataclass
class DatasetItem:
    id: str
    input: Dict[str, Any]
    golden: str
    metadata: Dict[str, Any]


class DatasetRegistry:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def load(self, name: str, dataset_config: Dict[str, Any]) -> List[DatasetItem]:
        loader = getattr(self, f"_load_{name}", None)
        if loader is None:
            raise ValueError(f"Unknown dataset: {name}")
        return loader(dataset_config)

    def _load_custom(self, dataset_config: Dict[str, Any]) -> List[DatasetItem]:
        path = Path(dataset_config.get("path", self.base_dir / "datasets" / "custom.jsonl"))
        if not path.exists():
            raise FileNotFoundError(f"Custom dataset not found: {path}")
        items: List[DatasetItem] = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                raw = json.loads(line)
                items.append(
                    DatasetItem(
                        id=str(raw.get("id")),
                        input=raw.get("input", {}),
                        golden=raw.get("golden", ""),
                        metadata=raw.get("metadata", {}),
                    )
                )
        return items

    def _load_humaneval(self, dataset_config: Dict[str, Any]) -> List[DatasetItem]:
        return self._load_huggingface(dataset_config, "openai_humaneval", "test")

    def _load_mbpp(self, dataset_config: Dict[str, Any]) -> List[DatasetItem]:
        return self._load_huggingface(dataset_config, "mbpp", "test")

    def _load_swe_bench(self, dataset_config: Dict[str, Any]) -> List[DatasetItem]:
        return self._load_huggingface(dataset_config, "princeton-nlp/SWE-bench", "test")

    def _load_huggingface(self, dataset_config: Dict[str, Any], dataset_id: str, split: str) -> List[DatasetItem]:
        try:
            from datasets import load_dataset
        except ImportError as exc:
            raise ImportError("datasets package required for Hugging Face datasets") from exc

        ds = load_dataset(dataset_config.get("id", dataset_id), split=dataset_config.get("split", split))
        items: List[DatasetItem] = []
        for row in ds:
            input_payload = {k: row.get(k) for k in row.keys() if k not in {"canonical_solution", "solution", "patch"}}
            golden = row.get("canonical_solution") or row.get("solution") or row.get("patch") or ""
            items.append(
                DatasetItem(
                    id=str(row.get("task_id") or row.get("id") or row.get("instance_id") or "unknown"),
                    input=input_payload,
                    golden=golden,
                    metadata={"source": dataset_id},
                )
            )
        return items
