"""Tests for Tier 0 tools (no LLM required)."""

from __future__ import annotations

import pytest
from agentic_v2.tools.builtin.file_ops import (
    DirectoryCreateTool,
    FileCopyTool,
    FileReadTool,
    FileWriteTool,
)
from agentic_v2.tools.builtin.transform import (
    ConfigMergeTool,
    JsonDumpTool,
    JsonLoadTool,
    JsonTransformTool,
    TemplateRenderTool,
    YamlDumpTool,
    YamlLoadTool,
)


class TestFileCopyTool:
    """Tests for FileCopyTool."""

    @pytest.mark.asyncio
    async def test_copy_file_success(self, tmp_path):
        """Test successful file copy."""
        source = tmp_path / "source.txt"
        dest = tmp_path / "dest.txt"
        source.write_text("test content")

        tool = FileCopyTool()
        result = await tool(source=str(source), destination=str(dest))

        assert result.success
        assert dest.exists()
        assert dest.read_text() == "test content"

    @pytest.mark.asyncio
    async def test_copy_file_nonexistent_source(self, tmp_path):
        """Test copy with nonexistent source."""
        source = tmp_path / "nonexistent.txt"
        dest = tmp_path / "dest.txt"

        tool = FileCopyTool()
        result = await tool(source=str(source), destination=str(dest))

        assert not result.success
        assert "does not exist" in result.error

    @pytest.mark.asyncio
    async def test_copy_file_existing_dest_no_overwrite(self, tmp_path):
        """Test copy when destination exists and overwrite=False."""
        source = tmp_path / "source.txt"
        dest = tmp_path / "dest.txt"
        source.write_text("source content")
        dest.write_text("dest content")

        tool = FileCopyTool()
        result = await tool(source=str(source), destination=str(dest), overwrite=False)

        assert not result.success
        assert "already exists" in result.error
        assert dest.read_text() == "dest content"  # Unchanged

    @pytest.mark.asyncio
    async def test_copy_file_with_overwrite(self, tmp_path):
        """Test copy with overwrite=True."""
        source = tmp_path / "source.txt"
        dest = tmp_path / "dest.txt"
        source.write_text("new content")
        dest.write_text("old content")

        tool = FileCopyTool()
        result = await tool(source=str(source), destination=str(dest), overwrite=True)

        assert result.success
        assert dest.read_text() == "new content"


class TestFileWriteReadTools:
    """Tests for FileWriteTool and FileReadTool."""

    @pytest.mark.asyncio
    async def test_write_and_read(self, tmp_path):
        """Test writing and reading a file."""
        file_path = tmp_path / "test.txt"
        content = "Hello, World!"

        # Write
        write_tool = FileWriteTool()
        write_result = await write_tool(path=str(file_path), content=content)
        assert write_result.success

        # Read
        read_tool = FileReadTool()
        read_result = await read_tool(path=str(file_path))
        assert read_result.success
        assert read_result.data["content"] == content

    @pytest.mark.asyncio
    async def test_read_nonexistent_file(self, tmp_path):
        """Test reading nonexistent file."""
        file_path = tmp_path / "nonexistent.txt"

        tool = FileReadTool()
        result = await tool(path=str(file_path))

        assert not result.success
        assert "does not exist" in result.error


class TestDirectoryCreateTool:
    """Tests for DirectoryCreateTool."""

    @pytest.mark.asyncio
    async def test_create_directory(self, tmp_path):
        """Test creating a directory."""
        dir_path = tmp_path / "subdir" / "nested"

        tool = DirectoryCreateTool()
        result = await tool(path=str(dir_path))

        assert result.success
        assert dir_path.exists()
        assert dir_path.is_dir()

    @pytest.mark.asyncio
    async def test_create_existing_directory(self, tmp_path):
        """Test creating existing directory with exist_ok=True."""
        dir_path = tmp_path / "existing"
        dir_path.mkdir()

        tool = DirectoryCreateTool()
        result = await tool(path=str(dir_path), exist_ok=True)

        assert result.success


class TestJsonTransformTool:
    """Tests for JsonTransformTool."""

    @pytest.mark.asyncio
    async def test_simple_query(self):
        """Test simple JMESPath query."""
        data = {"name": "Alice", "age": 30}

        tool = JsonTransformTool()
        result = await tool(data=data, query="name")

        assert result.success
        assert result.data == "Alice"

    @pytest.mark.asyncio
    async def test_array_query(self):
        """Test JMESPath query on array."""
        data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}

        tool = JsonTransformTool()
        result = await tool(data=data, query="users[0].name")

        assert result.success
        assert result.data == "Alice"

    @pytest.mark.asyncio
    async def test_projection_query(self):
        """Test JMESPath projection."""
        data = {"users": [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]}

        tool = JsonTransformTool()
        result = await tool(data=data, query="users[*].name")

        assert result.success
        assert result.data == ["Alice", "Bob"]


class TestTemplateRenderTool:
    """Tests for TemplateRenderTool."""

    @pytest.mark.asyncio
    async def test_simple_template(self):
        """Test simple template rendering."""
        template = "Hello, {{ name }}!"
        variables = {"name": "World"}

        tool = TemplateRenderTool()
        result = await tool(template=template, variables=variables)

        assert result.success
        assert result.data == "Hello, World!"

    @pytest.mark.asyncio
    async def test_complex_template(self):
        """Test template with loops and conditions."""
        template = """
        {% for item in items %}
        - {{ item }}
        {% endfor %}
        """
        variables = {"items": ["apple", "banana", "cherry"]}

        tool = TemplateRenderTool()
        result = await tool(template=template, variables=variables)

        assert result.success
        assert "apple" in result.data
        assert "banana" in result.data


class TestConfigMergeTool:
    """Tests for ConfigMergeTool."""

    @pytest.mark.asyncio
    async def test_simple_merge(self):
        """Test merging two configs."""
        configs = [{"a": 1, "b": 2}, {"b": 3, "c": 4}]

        tool = ConfigMergeTool()
        result = await tool(configs=configs)

        assert result.success
        assert result.data == {"a": 1, "b": 3, "c": 4}

    @pytest.mark.asyncio
    async def test_deep_merge(self):
        """Test deep merging nested dicts."""
        configs = [{"a": {"x": 1, "y": 2}}, {"a": {"y": 3, "z": 4}}]

        tool = ConfigMergeTool()
        result = await tool(configs=configs)

        assert result.success
        assert result.data == {"a": {"x": 1, "y": 3, "z": 4}}

    @pytest.mark.asyncio
    async def test_empty_configs(self):
        """Test with empty config list."""
        tool = ConfigMergeTool()
        result = await tool(configs=[])

        assert not result.success
        assert "No configs" in result.error


class TestYamlTools:
    """Tests for YAML load/dump tools."""

    @pytest.mark.asyncio
    async def test_yaml_round_trip(self):
        """Test loading and dumping YAML."""
        data = {"name": "Alice", "age": 30, "hobbies": ["reading", "coding"]}

        # Dump
        dump_tool = YamlDumpTool()
        dump_result = await dump_tool(data=data)
        assert dump_result.success

        # Load
        load_tool = YamlLoadTool()
        load_result = await load_tool(yaml_string=dump_result.data)
        assert load_result.success
        assert load_result.data == data


class TestJsonTools:
    """Tests for JSON load/dump tools."""

    @pytest.mark.asyncio
    async def test_json_round_trip(self):
        """Test loading and dumping JSON."""
        data = {"name": "Alice", "age": 30, "active": True}

        # Dump
        dump_tool = JsonDumpTool()
        dump_result = await dump_tool(data=data)
        assert dump_result.success

        # Load
        load_tool = JsonLoadTool()
        load_result = await load_tool(json_string=dump_result.data)
        assert load_result.success
        assert load_result.data == data

    @pytest.mark.asyncio
    async def test_json_invalid_input(self):
        """Test JSON loading with invalid input."""
        load_tool = JsonLoadTool()
        result = await load_tool(json_string="not valid json {")

        assert not result.success
        assert "JSON parsing failed" in result.error
