from pathlib import Path


def test_extract_prompt_block_finds_markdown_fence(repo_root: Path):
    # Import without triggering heavy tool imports.
    from tools.analysis.tools_ecosystem_evaluator import extract_prompt_block

    prompt_path = repo_root / "prompts" / "analysis" / "tools-ecosystem-evaluator.md"
    md = prompt_path.read_text(encoding="utf-8", errors="replace")

    prompt = extract_prompt_block(md)
    assert isinstance(prompt, str)
    assert "You are an expert software architect" in prompt


def test_extract_first_json_object_handles_code_fence():
    from tools.analysis.tools_ecosystem_evaluator import extract_first_json_object

    text = """```json
    {\"a\": 1, \"b\": {\"c\": 2}}
    ```"""

    obj = extract_first_json_object(text)
    assert obj == {"a": 1, "b": {"c": 2}}


def test_extract_first_json_object_handles_prefix_suffix():
    from tools.analysis.tools_ecosystem_evaluator import extract_first_json_object

    text = "noise... {\"ok\": true, \"n\": 3} ...tail"
    obj = extract_first_json_object(text)
    assert obj["ok"] is True
    assert obj["n"] == 3
