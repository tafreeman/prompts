# Gold Standards for Test Tasks

This directory contains gold standard definitions for evaluating multi-agent orchestrator outputs.

## Structure

Each task has a corresponding JSON file:
- `task_001_rest_api.json` - Simple REST API (bookmark manager)
- `task_002_config_parser.json` - Configuration file parser
- `task_003_notification_system.json` - Event-driven notification system
- etc.

## Gold Standard Schema

```json
{
  "task_id": 1,
  "version": "1.0",
  "last_updated": "2026-01-23",
  "source_references": [
    {
      "type": "github",
      "url": "https://github.com/example/bookmark-api",
      "commit": "abc123",
      "description": "Reference implementation"
    }
  ],
  "required_components": ["list of strings that must appear"],
  "required_patterns": ["regex patterns to match"],
  "api_endpoints": [{"method": "GET", "path": "/bookmarks"}],
  "database_tables": ["table names"],
  "key_decisions": ["architecture decisions"],
  "code_structure": {
    "filename.py": ["class names", "function names"]
  }
}
```

## Fetching from External Sources

Gold standards can reference external benchmarks:

### SWE-bench
```python
GoldStandardRef(
    source_type="swe-bench",
    source_url="princeton-nlp/SWE-bench",
    benchmark_id="django__django-12345"
)
```

### GitHub Reference Implementations
```python
GoldStandardRef(
    source_type="github",
    source_url="owner/repo",
    commit_hash="abc123def456",
    file_path="tests/golden/task_001.json"
)
```

## Cache

Fetched gold standards are cached in `.gold_standard_cache/` to avoid repeated network requests.
Clear the cache with: `rm -rf tools/agents/.gold_standard_cache/`
