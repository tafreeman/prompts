# Evaluation Agent Test Suite

This directory contains comprehensive tests for the Evaluation Agent.

## Test Files

### `test_evaluation_agent.py`
Unit tests for core functionality:

- Configuration validation
- Logging setup
- Checkpoint save/load
- Data structures (TaskResult, CategoryResult, AgentState)
- Command-line argument parsing
- Prompt counting

**Run with:**

```bash
python tools/test_evaluation_agent.py
```text

### `test_evaluation_agent_integration.py`
Integration tests for agent workflows:

- Full pipeline in dry-run mode
- Phase execution
- Command-line integration
- State management
- Category prioritization
- Error handling

**Run with:**

```bash
python tools/test_evaluation_agent_integration.py
```sql

### `test_evaluation_agent_e2e.py`
End-to-end tests with mocked dependencies:

- Complete pipeline execution
- Single phase execution
- Resume from checkpoint
- Command-line interface

**Run with:**

```bash
python tools/test_evaluation_agent_e2e.py
```text

## Running All Tests

To run all test suites:

```bash
python tools/test_evaluation_agent.py && \
python tools/test_evaluation_agent_integration.py && \
python tools/test_evaluation_agent_e2e.py
```sql

## Test Coverage

The test suite covers:

- ✅ Configuration validation
- ✅ Agent initialization
- ✅ Checkpoint management
- ✅ Command-line parsing
- ✅ Dry-run mode
- ✅ Phase execution
- ✅ State tracking
- ✅ Error handling
- ✅ Resume capability

Total: **38 tests** across 3 test files

## Test Philosophy

Tests follow these principles:

1. **Fast**: All tests run in < 1 second
2. **Isolated**: Tests don't depend on external services
3. **Comprehensive**: Cover all major code paths
4. **Maintainable**: Clear test names and documentation

## Mocking Strategy

Tests mock external dependencies:

- GitHub CLI (`gh` command)
- File system operations (where appropriate)
- API calls to AI models
- Network requests

This allows tests to run:

- Without authentication
- In CI/CD environments
- Quickly and reliably
- Without external service costs

## Continuous Integration

These tests should be run:

- Before committing changes
- In CI/CD pipelines
- After dependency updates
- When modifying evaluation_agent.py

## Adding New Tests

When adding new functionality to `evaluation_agent.py`:

1. Add unit tests to `test_evaluation_agent.py`
2. Add integration tests to `test_evaluation_agent_integration.py`
3. Add end-to-end scenarios to `test_evaluation_agent_e2e.py`
4. Update this README with new test count

## Debugging Tests

To get verbose output:

```bash
python tools/test_evaluation_agent.py -v
```text

To run a specific test:

```bash
python -m unittest tools.test_evaluation_agent.TestAgentConfiguration.test_agent_config_paths_exist
```text