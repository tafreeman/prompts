from __future__ import annotations

from multiagent_workflows.server.models import ModelRegistry


def test_flatten_discovery_marks_selectable_and_missing() -> None:
    providers = {
        "local_onnx": {
            "available": ["local:phi4"],
            "missing": ["local:phi3"],
            "count": 1,
        },
        "github_models": {
            "available": ["gh:openai/gpt-4o-mini"],
            "count": 1,
        },
    }

    models = ModelRegistry._flatten_discovery(providers)

    ids = [m.id for m in models]
    assert "local:phi4" in ids
    assert "local:phi3" in ids
    assert "gh:openai/gpt-4o-mini" in ids

    by_id = {m.id: m for m in models}
    assert by_id["local:phi4"].selectable is True
    assert by_id["gh:openai/gpt-4o-mini"].selectable is True

    assert by_id["local:phi3"].selectable is False
    assert by_id["local:phi3"].usable is False


def test_flatten_discovery_sort_selectable_first() -> None:
    providers = {
        "p": {"available": ["local:b"], "missing": ["local:a"]},
    }

    models = ModelRegistry._flatten_discovery(providers)
    assert [m.id for m in models] == ["local:b", "local:a"]
