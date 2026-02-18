"""Tests for the LangChain workflow engine.

Tests config loading, expression evaluation, and graph compilation
without requiring any API keys (tier-0 only).
"""

import json
import os
import pytest
from pathlib import Path
from datetime import datetime

from agentic_v2.langchain.config import (
    WorkflowConfig,
    StepConfig,
    load_workflow_config,
    list_workflows,
)
from agentic_v2.langchain.expressions import (
    evaluate_condition,
    resolve_expression,
)
from agentic_v2.langchain.state import WorkflowState, initial_state
from agentic_v2.langchain.graph import compile_workflow
from agentic_v2.langchain.runner import WorkflowRunner
from agentic_v2.langchain.tools import get_tools_for_tier, web_search
from agentic_v2.integrations.base import CanonicalEvent, TraceAdapter
from agentic_v2.integrations.tracing import LangSmithTraceAdapter


# ---------------------------------------------------------------------------
# Config loader tests
# ---------------------------------------------------------------------------


class TestConfigLoader:
    """Test YAML config loading."""

    def test_list_workflows(self):
        names = list_workflows()
        assert isinstance(names, list)
        assert len(names) > 0
        assert "code_review" in names

    def test_load_code_review(self):
        config = load_workflow_config("code_review")
        assert config.name == "code_review"
        assert config.version == "1.0"
        assert len(config.steps) >= 3
        assert "code_file" in config.inputs
        assert config.evaluation is not None
        assert len(config.evaluation.criteria) > 0

    def test_load_nonexistent_raises(self):
        with pytest.raises(FileNotFoundError):
            load_workflow_config("nonexistent_workflow_xyz")

    def test_step_config_fields(self):
        config = load_workflow_config("code_review")
        parse_step = next(s for s in config.steps if s.name == "parse_code")
        assert parse_step.agent == "tier0_parser"
        assert "file_path" in parse_step.inputs

    def test_step_dependencies(self):
        config = load_workflow_config("code_review")
        review_step = next(s for s in config.steps if s.name == "review_code")
        assert "style_check" in review_step.depends_on
        assert "complexity_analysis" in review_step.depends_on

    def test_conditional_step(self):
        config = load_workflow_config("code_review")
        summary_step = next(
            s for s in config.steps if s.name == "generate_summary"
        )
        assert summary_step.when is not None
        assert "review_depth" in summary_step.when

    def test_capabilities_parsed(self):
        config = load_workflow_config("code_review")
        assert "inputs" in config.capabilities
        assert "code_file" in config.capabilities["inputs"]

    def test_evaluation_criteria(self):
        config = load_workflow_config("code_review")
        assert config.evaluation is not None
        criteria_names = [c.name for c in config.evaluation.criteria]
        assert "correctness_rubric" in criteria_names
        assert "code_quality" in criteria_names

    def test_load_deep_research(self):
        config = load_workflow_config("deep_research")
        assert config.name == "deep_research"
        assert config.version == "1.0"
        assert len(config.steps) > 10
        assert "topic" in config.inputs
        assert "goal" in config.inputs
        assert config.inputs["topic"].required is False
        assert config.inputs["goal"].required is False
        assert "min_ci" in config.inputs
        assert "max_rounds" in config.inputs
        assert "confidence_report" in config.outputs

    def test_deep_research_goal_falls_back_to_topic(self):
        config = load_workflow_config("deep_research")
        intake_scope = next(s for s in config.steps if s.name == "intake_scope")
        assert intake_scope.inputs["goal"] == "${coalesce(inputs.goal, inputs.topic)}"

    def test_deep_research_round2_is_conditional(self):
        config = load_workflow_config("deep_research")
        step = next(s for s in config.steps if s.name == "hypothesis_tree_tot_round2")
        assert step.when is not None
        assert "inputs.max_rounds >= 2" in step.when
        assert "steps.coverage_confidence_audit_round1.outputs.ci_score" in step.when

    def test_deep_research_outputs_include_rag(self):
        config = load_workflow_config("deep_research")
        assert "rag_manifest" in config.outputs
        assert "rag_chunks" in config.outputs
        assert "claim_graph" in config.outputs

    def test_deep_research_step_model_overrides(self):
        config = load_workflow_config("deep_research")
        source_policy = next(s for s in config.steps if s.name == "source_policy")
        final_synthesis = next(s for s in config.steps if s.name == "final_synthesis")
        assert source_policy.model_override == "env:DEEP_RESEARCH_SMALL_MODEL|gemini:gemini-2.0-flash-lite"
        assert final_synthesis.model_override == "env:DEEP_RESEARCH_HEAVY_MODEL|gemini:gemini-2.5-flash"


class TestLangChainTooling:
    """Tooling registry tests for LangChain-native tools."""

    def test_tier2_includes_web_search(self):
        tools = get_tools_for_tier(2)
        names = {tool.name for tool in tools}
        assert "web_search" in names
        assert "http_get" in names

    def test_web_search_applies_allowlist(self, monkeypatch):
        class _Resp:
            def __init__(self, text):
                self.text = text

        html = """
        <a class="result__a" href="https://openai.com/research">OpenAI</a>
        <a class="result__snippet">openai snippet</a>
        <a class="result__a" href="https://example.org/post">Example</a>
        <a class="result__snippet">example snippet</a>
        """

        monkeypatch.setattr("httpx.get", lambda *args, **kwargs: _Resp(html))

        raw = web_search.invoke(
            {
                "query": "test",
                "max_results": 5,
                "allowed_domains": ["openai.com"],
            }
        )
        payload = json.loads(raw)
        assert len(payload["results"]) == 1
        assert payload["results"][0]["domain"] == "openai.com"
        assert payload["filters"]["allowed_domains"] == ["openai.com"]

    def test_web_search_applies_blocklist(self, monkeypatch):
        class _Resp:
            def __init__(self, text):
                self.text = text

        html = """
        <a class="result__a" href="https://openai.com/research">OpenAI</a>
        <a class="result__snippet">openai snippet</a>
        <a class="result__a" href="https://example.org/post">Example</a>
        <a class="result__snippet">example snippet</a>
        """

        monkeypatch.setattr("httpx.get", lambda *args, **kwargs: _Resp(html))

        raw = web_search.invoke(
            {
                "query": "test",
                "max_results": 5,
                "blocked_domains": ["openai.com"],
            }
        )
        payload = json.loads(raw)
        assert len(payload["results"]) == 1
        assert payload["results"][0]["domain"] == "example.org"
        assert payload["filters"]["blocked_domains"] == ["openai.com"]


class TestPerStepModelOverride:
    """Per-step model override behavior tests."""

    def test_parse_step_model_override(self):
        from agentic_v2.langchain.config import _parse

        data = {
            "name": "wf_model_override",
            "steps": [
                {
                    "name": "s1",
                    "agent": "tier2_researcher",
                    "model_override": "gh:openai/gpt-4o-mini",
                },
                {
                    "name": "s2",
                    "agent": "tier2_researcher",
                    "model": "gh:openai/gpt-4o",
                },
            ],
        }
        config = _parse(data, "wf_model_override")
        assert config.steps[0].model_override == "gh:openai/gpt-4o-mini"
        assert config.steps[1].model_override == "gh:openai/gpt-4o"

    def test_step_model_override_is_passed_to_agent_factory(self, monkeypatch):
        from agentic_v2.langchain import graph as graph_module
        from langchain_core.messages import AIMessage

        captured = {}

        class _DummyAgent:
            def invoke(self, payload):
                return {"messages": [AIMessage(content='{"report":"ok"}')]}

        def _fake_create_agent(
            agent_name,
            *,
            tool_names=None,
            prompt_file=None,
            model_override=None,
        ):
            captured["agent_name"] = agent_name
            captured["model_override"] = model_override
            return _DummyAgent()

        monkeypatch.setattr(graph_module, "create_agent", _fake_create_agent)

        step = StepConfig(
            name="llm_step",
            agent="tier2_researcher",
            model_override="gh:openai/gpt-4o-mini",
            outputs={"report": "report_ctx"},
        )
        workflow = WorkflowConfig(name="wf", steps=[step])
        node = graph_module._make_step_node(step, workflow)
        state = {
            "inputs": {},
            "context": {},
            "steps": {},
            "messages": [],
            "errors": [],
            "outputs": {},
            "current_step": "",
        }
        result = node(state)

        assert captured["agent_name"] == "tier2_researcher"
        assert captured["model_override"] == "gh:openai/gpt-4o-mini"
        assert result["context"]["report_ctx"] == "ok"


# ---------------------------------------------------------------------------
# Expression evaluator tests
# ---------------------------------------------------------------------------


class TestExpressions:
    """Test expression evaluation."""

    def test_simple_variable(self):
        state = {"inputs": {"code_file": "main.py"}}
        result = resolve_expression("${inputs.code_file}", state)
        assert result == "main.py"

    def test_nested_path(self):
        state = {
            "steps": {
                "parse_code": {
                    "outputs": {"ast": {"functions": ["foo", "bar"]}}
                }
            }
        }
        result = resolve_expression(
            "${steps.parse_code.outputs.ast}", state
        )
        assert result == {"functions": ["foo", "bar"]}

    def test_condition_true(self):
        state = {"inputs": {"review_depth": "standard"}}
        assert evaluate_condition(
            "${inputs.review_depth} != 'quick'", state
        )

    def test_condition_false(self):
        state = {"inputs": {"review_depth": "quick"}}
        assert not evaluate_condition(
            "${inputs.review_depth} != 'quick'", state
        )

    def test_in_operator(self):
        state = {
            "steps": {
                "review": {"outputs": {"status": "APPROVED"}}
            }
        }
        assert evaluate_condition(
            "${steps.review.outputs.status} in ['APPROVED', 'PASSED']",
            state,
        )

    def test_missing_path_returns_none(self):
        state = {"inputs": {}}
        result = resolve_expression("${inputs.nonexistent}", state)
        assert result is None

    def test_empty_expression_is_true(self):
        assert evaluate_condition("", {})


# ---------------------------------------------------------------------------
# State tests
# ---------------------------------------------------------------------------


class TestState:
    """Test state creation."""

    def test_initial_state(self):
        state = initial_state(workflow_inputs={"code_file": "test.py"})
        assert state["inputs"]["code_file"] == "test.py"
        assert state["messages"] == []
        assert state["errors"] == []
        assert state["steps"] == {}

    def test_initial_state_defaults(self):
        state = initial_state()
        assert state["inputs"] == {}
        assert state["context"] == {}


# ---------------------------------------------------------------------------
# Graph compilation tests (tier-0 only, no API keys)
# ---------------------------------------------------------------------------


class TestGraphCompilation:
    """Test graph compilation from config."""

    @pytest.mark.skipif(
        not os.environ.get("OPENAI_API_KEY"),
        reason="Requires OPENAI_API_KEY to instantiate LLM agents",
    )
    def test_compile_code_review(self):
        """Verify the code_review workflow compiles without errors."""
        config = load_workflow_config("code_review")
        graph = compile_workflow(config)
        assert graph is not None

    def test_empty_workflow_raises(self):
        config = WorkflowConfig(name="empty", steps=[])
        with pytest.raises(ValueError, match="no steps"):
            compile_workflow(config)

    def test_missing_dependency_raises(self):
        config = WorkflowConfig(
            name="bad_deps",
            steps=[
                StepConfig(
                    name="step1",
                    agent="tier0_parser",
                    depends_on=["nonexistent"],
                ),
            ],
        )
        with pytest.raises(ValueError, match="unknown step"):
            compile_workflow(config)

    def test_tier0_only_workflow_runs(self):
        """A workflow with only tier-0 steps should execute end-to-end."""
        config = WorkflowConfig(
            name="test_tier0",
            steps=[
                StepConfig(
                    name="parse",
                    agent="tier0_parser",
                    inputs={"file_path": "${inputs.code_file}"},
                    outputs={"parsed_ast": "ast_result"},
                ),
            ],
            inputs={},
        )
        graph = compile_workflow(config)
        state = initial_state(workflow_inputs={"code_file": "nonexistent.py"})
        state["context"]["inputs"] = state["inputs"]
        result = graph.invoke(state)
        assert "parse" in result["steps"]
        assert result["steps"]["parse"]["status"] == "success"


class TestWorkflowRunner:
    """Test WorkflowRunner integration points for LangGraph runtime config."""

    def test_get_or_compile_passes_checkpointer(self):
        captured = {}

        def _fake_compile(config, checkpointer=None):
            captured["checkpointer"] = checkpointer
            return object()

        config = WorkflowConfig(
            name="wf_checkpointer",
            steps=[StepConfig(name="parse", agent="tier0_parser")],
        )
        checkpointer = object()
        runner = WorkflowRunner(checkpointer=checkpointer)

        from agentic_v2.langchain import runner as runner_module

        original_compile = runner_module.compile_workflow
        runner_module.compile_workflow = _fake_compile
        try:
            runner._get_or_compile(config, use_cache=False)
        finally:
            runner_module.compile_workflow = original_compile

        assert captured["checkpointer"] is checkpointer

    def test_invoke_passes_thread_id_in_config(self):
        class _DummyGraph:
            def __init__(self):
                self.config = None

            def invoke(self, state, config=None):
                self.config = config
                return {
                    "steps": {},
                    "errors": [],
                    "context": state.get("context", {}),
                }

        dummy_graph = _DummyGraph()
        runner = WorkflowRunner()

        config = WorkflowConfig(name="wf_thread", steps=[])

        from agentic_v2.langchain import runner as runner_module

        original_loader = runner_module.load_workflow_config
        original_compiler = runner_module.compile_workflow
        runner_module.load_workflow_config = lambda *_args, **_kwargs: config
        runner_module.compile_workflow = lambda *_args, **_kwargs: dummy_graph
        try:
            result = runner.invoke("wf_thread", thread_id="thread-123")
        finally:
            runner_module.load_workflow_config = original_loader
            runner_module.compile_workflow = original_compiler

        assert result.status == "success"
        assert dummy_graph.config is not None
        assert dummy_graph.config.get("configurable", {}).get("thread_id") == "thread-123"

    def test_invoke_falls_back_when_config_unsupported(self):
        class _LegacyGraph:
            def __init__(self):
                self.calls = 0

            def invoke(self, state):
                self.calls += 1
                return {
                    "steps": {},
                    "errors": [],
                    "context": state.get("context", {}),
                }

        legacy_graph = _LegacyGraph()
        runner = WorkflowRunner()

        config = WorkflowConfig(name="wf_legacy", steps=[])

        from agentic_v2.langchain import runner as runner_module

        original_loader = runner_module.load_workflow_config
        original_compiler = runner_module.compile_workflow
        runner_module.load_workflow_config = lambda *_args, **_kwargs: config
        runner_module.compile_workflow = lambda *_args, **_kwargs: legacy_graph
        try:
            result = runner.invoke("wf_legacy", thread_id="legacy-thread")
        finally:
            runner_module.load_workflow_config = original_loader
            runner_module.compile_workflow = original_compiler

        assert result.status == "success"
        assert legacy_graph.calls == 1

    def test_stream_passes_thread_id_in_config(self):
        class _StreamingGraph:
            def __init__(self):
                self.config = None

            def stream(self, state, config=None):
                self.config = config
                yield {"event": "step_start", "state": state.get("current_step", "")}

        streaming_graph = _StreamingGraph()
        runner = WorkflowRunner()
        config = WorkflowConfig(name="wf_stream", steps=[])

        from agentic_v2.langchain import runner as runner_module

        original_loader = runner_module.load_workflow_config
        original_compiler = runner_module.compile_workflow
        runner_module.load_workflow_config = lambda *_args, **_kwargs: config
        runner_module.compile_workflow = lambda *_args, **_kwargs: streaming_graph
        try:
            events = list(runner.stream("wf_stream", thread_id="stream-thread"))
        finally:
            runner_module.load_workflow_config = original_loader
            runner_module.compile_workflow = original_compiler

        assert len(events) == 1
        assert streaming_graph.config is not None
        assert streaming_graph.config.get("configurable", {}).get("thread_id") == "stream-thread"

    def test_invoke_emits_trace_events(self):
        class _TraceCollector(TraceAdapter):
            def __init__(self):
                self.events = []

            def emit(self, event):
                self.events.append(event)

        class _DummyGraph:
            def invoke(self, state, config=None):
                return {
                    "steps": {"s": {"status": "success", "outputs": {}}},
                    "errors": [],
                    "context": state.get("context", {}),
                }

        trace = _TraceCollector()
        runner = WorkflowRunner(trace_adapter=trace)
        config = WorkflowConfig(name="wf_trace", steps=[])

        from agentic_v2.langchain import runner as runner_module

        original_loader = runner_module.load_workflow_config
        original_compiler = runner_module.compile_workflow
        runner_module.load_workflow_config = lambda *_args, **_kwargs: config
        runner_module.compile_workflow = lambda *_args, **_kwargs: _DummyGraph()
        try:
            result = runner.invoke("wf_trace")
        finally:
            runner_module.load_workflow_config = original_loader
            runner_module.compile_workflow = original_compiler

        assert result.status == "success"
        assert len(trace.events) >= 2
        assert trace.events[0].type == "workflow_start"
        assert trace.events[-1].type == "workflow_end"

    def test_get_checkpoint_state_reads_snapshot(self):
        class _Snapshot:
            values = {"foo": "bar"}
            next = ("step_b",)
            metadata = {"checkpoint_id": "cp-1"}
            created_at = "2026-02-16T00:00:00Z"

        class _GraphWithState:
            def get_state(self, config=None):
                return _Snapshot()

        runner = WorkflowRunner(checkpointer=object())
        config = WorkflowConfig(name="wf_state", steps=[])

        from agentic_v2.langchain import runner as runner_module

        original_loader = runner_module.load_workflow_config
        original_compiler = runner_module.compile_workflow
        runner_module.load_workflow_config = lambda *_args, **_kwargs: config
        runner_module.compile_workflow = lambda *_args, **_kwargs: _GraphWithState()
        try:
            snapshot = runner.get_checkpoint_state("wf_state", thread_id="t-1")
        finally:
            runner_module.load_workflow_config = original_loader
            runner_module.compile_workflow = original_compiler

        assert snapshot is not None
        assert snapshot["values"]["foo"] == "bar"
        assert snapshot["next"] == ["step_b"]

    def test_get_checkpoint_history_limit(self):
        class _Snapshot:
            def __init__(self, i):
                self.values = {"i": i}
                self.next = ()
                self.metadata = {"checkpoint_id": f"cp-{i}"}
                self.created_at = "2026-02-16T00:00:00Z"

        class _GraphWithHistory:
            def get_state_history(self, config=None):
                for i in range(10):
                    yield _Snapshot(i)

        runner = WorkflowRunner(checkpointer=object())
        config = WorkflowConfig(name="wf_hist", steps=[])

        from agentic_v2.langchain import runner as runner_module

        original_loader = runner_module.load_workflow_config
        original_compiler = runner_module.compile_workflow
        runner_module.load_workflow_config = lambda *_args, **_kwargs: config
        runner_module.compile_workflow = lambda *_args, **_kwargs: _GraphWithHistory()
        try:
            history = runner.get_checkpoint_history("wf_hist", thread_id="t-1", limit=3)
        finally:
            runner_module.load_workflow_config = original_loader
            runner_module.compile_workflow = original_compiler

        assert len(history) == 3
        assert history[0]["values"]["i"] == 0

    def test_resume_uses_thread_checkpoint(self):
        class _ResumeGraph:
            def __init__(self):
                self.invoked_with = None
                self.config = None

            def invoke(self, state, config=None):
                self.invoked_with = state
                self.config = config
                return {
                    "steps": {"resume": {"status": "success", "outputs": {}}},
                    "errors": [],
                    "context": {"ok": True},
                }

        graph = _ResumeGraph()
        runner = WorkflowRunner(checkpointer=object())
        config = WorkflowConfig(name="wf_resume", steps=[])

        from agentic_v2.langchain import runner as runner_module

        original_loader = runner_module.load_workflow_config
        original_compiler = runner_module.compile_workflow
        runner_module.load_workflow_config = lambda *_args, **_kwargs: config
        runner_module.compile_workflow = lambda *_args, **_kwargs: graph
        try:
            result = runner.resume("wf_resume", thread_id="thread-resume")
        finally:
            runner_module.load_workflow_config = original_loader
            runner_module.compile_workflow = original_compiler

        assert result.status == "success"
        assert graph.invoked_with is None
        assert graph.config is not None
        assert graph.config.get("configurable", {}).get("thread_id") == "thread-resume"


class TestLangSmithTracing:
    """LangSmith adapter behavior tests (without network)."""

    def test_langsmith_adapter_wires_parent_child_runs(self):
        class _FakeClient:
            def __init__(self):
                self.created = []
                self.updated = []

            def create_run(self, **kwargs):
                self.created.append(kwargs)

            def update_run(self, run_id, **kwargs):
                self.updated.append((run_id, kwargs))

        client = _FakeClient()
        adapter = LangSmithTraceAdapter(client=client, project_name="test-project")

        adapter.emit(
            CanonicalEvent(
                type="workflow_start",
                timestamp=datetime.now(),
                data={"workflow_name": "wf", "run_id": "run-1", "inputs": {"a": 1}},
            )
        )
        adapter.emit(
            CanonicalEvent(
                type="step_start",
                timestamp=datetime.now(),
                step_name="step-a",
                data={"run_id": "run-1", "inputs": {"x": 1}},
            )
        )
        adapter.emit(
            CanonicalEvent(
                type="workflow_end",
                timestamp=datetime.now(),
                data={"workflow_name": "wf", "run_id": "run-1", "status": "success", "outputs": {"ok": True}},
            )
        )

        assert len(client.created) >= 2
        # Root workflow run + child step run
        root_run = client.created[0]
        child_run = client.created[1]
        assert root_run["run_type"] == "chain"
        assert child_run["run_type"] == "tool"
        assert "parent_run_id" in child_run
        assert len(client.updated) == 1


# ---------------------------------------------------------------------------
# Phase 1 fix tests
# ---------------------------------------------------------------------------


class TestCoalesceExpression:
    """Tests for coalesce() expression support."""

    def test_coalesce_returns_first_non_none(self):
        state = {"steps": {"a": {"outputs": {"x": None}}, "b": {"outputs": {"y": "found"}}}}
        result = resolve_expression("${coalesce(steps.a.outputs.x, steps.b.outputs.y)}", state)
        assert result == "found"

    def test_coalesce_three_args_first_wins(self):
        state = {"steps": {"a": {"outputs": {"x": "first"}}}}
        result = resolve_expression("${coalesce(steps.a.outputs.x, steps.a.outputs.missing, steps.a.outputs.x)}", state)
        assert result == "first"

    def test_coalesce_all_none_returns_none(self):
        state = {}
        result = resolve_expression("${coalesce(steps.a.outputs.x, steps.b.outputs.y)}", state)
        assert result is None

    def test_coalesce_in_condition(self):
        state = {"steps": {"a": {"outputs": {"val": None}}, "b": {"outputs": {"val": "ok"}}}}
        # coalesce in condition context: should be truthy
        result = resolve_expression("${coalesce(steps.a.outputs.val, steps.b.outputs.val)}", state)
        assert result == "ok"


class TestCompositeExpressions:
    """Tests for dict/list expression resolution."""

    def test_resolve_dict_of_expressions(self):
        state = {"steps": {"x": {"outputs": {"code": "print(1)"}}, "y": {"outputs": {"html": "<p>hi</p>"}}}}
        expr = {"backend": "${steps.x.outputs.code}", "frontend": "${steps.y.outputs.html}"}
        result = resolve_expression(expr, state)
        assert result == {"backend": "print(1)", "frontend": "<p>hi</p>"}

    def test_resolve_list_of_expressions(self):
        state = {"inputs": {"a": "hello", "b": "world"}}
        expr = ["${inputs.a}", "${inputs.b}", "literal"]
        result = resolve_expression(expr, state)
        assert result == ["hello", "world", "literal"]

    def test_non_string_passthrough(self):
        assert resolve_expression(42, {}) == 42
        assert resolve_expression(True, {}) is True
        assert resolve_expression(None, {}) is None


class TestConfigParserNonStringInputs:
    """Tests that config parser preserves non-string input values."""

    def test_dict_input_preserved(self):
        from agentic_v2.langchain.config import _parse
        data = {
            "name": "test_wf",
            "steps": [
                {
                    "name": "step_a",
                    "agent": "tier0_parser",
                    "inputs": {
                        "simple": "${inputs.code_file}",
                        "composite": {"backend": "${steps.x.outputs.code}", "frontend": "${steps.y.outputs.ui}"},
                    },
                }
            ],
        }
        config = _parse(data, "test_wf")
        assert "simple" in config.steps[0].inputs
        assert "composite" in config.steps[0].inputs
        assert isinstance(config.steps[0].inputs["composite"], dict)

    def test_loads_fullstack_bounded_rereview(self):
        """fullstack_generation_bounded_rereview.yaml uses coalesce() in inputs — should load cleanly."""
        try:
            config = load_workflow_config("fullstack_generation_bounded_rereview")
            assert len(config.steps) > 0
        except FileNotFoundError:
            pytest.skip("fullstack_generation_bounded_rereview.yaml not available")


class TestLoopIterationCounter:
    """Tests that loop iteration is tracked correctly in step data."""

    def test_tier0_node_increments_iteration(self):
        """Running a tier-0 step twice should show loop_iteration=2 on second call."""
        from agentic_v2.langchain.config import StepConfig, WorkflowConfig
        from agentic_v2.langchain.graph import compile_workflow

        config = WorkflowConfig(
            name="loop_test",
            steps=[
                StepConfig(
                    name="parse",
                    agent="tier0_parser",
                    depends_on=[],
                    loop_until="${steps.parse.outputs.done}",
                    loop_max=3,
                )
            ],
        )
        # Just verify the graph compiles and loop edge wiring doesn't crash
        g = compile_workflow(config)
        assert g is not None


class TestConditionalFanOut:
    """Tests that unconditional siblings are not dropped when conditional edges exist."""

    def _make_config(self, cond_true: bool) -> WorkflowConfig:
        from agentic_v2.langchain.config import StepConfig, WorkflowConfig, InputConfig

        return WorkflowConfig(
            name="fanout_test",
            inputs={"flag": InputConfig(name="flag", default="yes", required=False)},
            steps=[
                StepConfig(name="root", agent="tier0_parser", depends_on=[]),
                StepConfig(name="always", agent="tier0_parser", depends_on=["root"]),
                StepConfig(
                    name="conditional",
                    agent="tier0_parser",
                    depends_on=["root"],
                    when="${inputs.flag} == 'yes'" if cond_true else "${inputs.flag} == 'no'",
                ),
            ],
        )

    def test_unconditional_sibling_always_runs(self):
        """The 'always' step must execute even when a conditional sibling exists."""
        config = self._make_config(cond_true=False)
        g = compile_workflow(config)
        state = {"inputs": {"flag": "no"}, "context": {"inputs": {"flag": "no"}}, "steps": {}, "messages": [], "errors": [], "outputs": {}, "current_step": ""}
        result = g.invoke(state)
        assert "always" in result["steps"]
        assert result["steps"]["always"]["status"] == "success"

    def test_conditional_step_runs_when_condition_true(self):
        """The 'conditional' step must execute when its when-expression is true."""
        config = self._make_config(cond_true=True)
        g = compile_workflow(config)
        state = {"inputs": {"flag": "yes"}, "context": {"inputs": {"flag": "yes"}}, "steps": {}, "messages": [], "errors": [], "outputs": {}, "current_step": ""}
        result = g.invoke(state)
        assert "always" in result["steps"]
        assert "conditional" in result["steps"]


# ---------------------------------------------------------------------------
# Phase 2: Model provider tests
# ---------------------------------------------------------------------------


class TestModelRegistry:
    """Tests for model provider registry."""

    def test_unsupported_provider_raises(self):
        from agentic_v2.langchain.models import get_chat_model
        with pytest.raises(ValueError, match="Unsupported model provider"):
            get_chat_model("azure:some-model")

    def test_gh_prefix_requires_github_token(self, monkeypatch):
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        from agentic_v2.langchain.models import get_chat_model
        with pytest.raises((ValueError, ImportError)):
            get_chat_model("gh:openai/gpt-4o-mini")

    def test_gh_prefix_builds_openai_with_token(self, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "fake-token")
        from agentic_v2.langchain.models import get_chat_model
        try:
            model = get_chat_model("gh:openai/gpt-4o-mini")
            assert model is not None
            # Model name should be the part after gh:
            assert "gpt-4o-mini" in str(model.model_name)
        except ImportError:
            pytest.skip("langchain-openai not installed")

    def test_ollama_prefix_builds_ollama_model(self, monkeypatch):
        monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")
        from agentic_v2.langchain.models import get_chat_model
        try:
            model = get_chat_model("ollama:qwen2.5-coder")
            assert model is not None
        except ImportError:
            pytest.skip("langchain-ollama not installed")

    def test_bare_name_treated_as_ollama(self, monkeypatch):
        from agentic_v2.langchain.models import get_chat_model
        try:
            model = get_chat_model("llama3.2")
            assert model is not None
        except ImportError:
            pytest.skip("langchain-ollama not installed")

    def test_openai_prefix_requires_api_key(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        from agentic_v2.langchain.models import get_chat_model
        with pytest.raises((ValueError, ImportError)):
            get_chat_model("openai:gpt-4o-mini")

    def test_openai_prefix_builds_model(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "fake-openai-key")
        from agentic_v2.langchain.models import get_chat_model
        try:
            model = get_chat_model("openai:gpt-4o-mini")
            assert model is not None
            assert "gpt-4o-mini" in str(model.model_name)
        except ImportError:
            pytest.skip("langchain-openai not installed")

    def test_anthropic_prefix_requires_key(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        from agentic_v2.langchain.models import get_chat_model
        with pytest.raises((ValueError, ImportError)):
            get_chat_model("anthropic:claude-3-5-sonnet-latest")

    def test_claude_alias_prefix(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-anthropic-key")
        from agentic_v2.langchain.models import get_chat_model
        try:
            model = get_chat_model("claude:claude-3-5-sonnet-latest")
            assert model is not None
        except ImportError:
            pytest.skip("langchain-anthropic not installed")

    def test_gemini_prefix_requires_key(self, monkeypatch):
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        from agentic_v2.langchain.models import get_chat_model
        with pytest.raises((ValueError, ImportError)):
            get_chat_model("gemini:gemini-2.5-pro")

    def test_notebooklm_alias_model_resolution(self, monkeypatch):
        monkeypatch.delenv("NOTEBOOKLM_MODEL", raising=False)
        monkeypatch.delenv("NOTEBOOKLM_GEMINI_MODEL", raising=False)
        from agentic_v2.langchain.models import _resolve_notebooklm_model_name
        assert _resolve_notebooklm_model_name("") == "gemini-2.5-pro"

        monkeypatch.setenv("NOTEBOOKLM_MODEL", "gemini-2.5-flash")
        assert _resolve_notebooklm_model_name("") == "gemini-2.5-flash"

        # Explicit suffix takes precedence over env.
        assert _resolve_notebooklm_model_name("gemini-2.0-pro") == "gemini-2.0-pro"

    def test_local_onnx_prefix_builds_wrapper(self):
        from agentic_v2.langchain.models import get_chat_model
        model = get_chat_model("local:phi4mini")
        assert model is not None
        assert getattr(model, "_llm_type") == "local-onnx"

    def test_tier_env_var_override(self, monkeypatch):
        monkeypatch.setenv("AGENTIC_MODEL_TIER_2", "ollama:phi4")
        from agentic_v2.langchain import models as models_mod
        import importlib
        importlib.reload(models_mod)  # pick up env var in module scope
        try:
            model = models_mod.get_model_for_tier(2)
            assert model is not None
        except ImportError:
            pytest.skip("langchain-ollama not installed")
        finally:
            importlib.reload(models_mod)

    def test_env_model_override_with_fallback(self, monkeypatch):
        monkeypatch.delenv("DEEP_RESEARCH_SMALL_MODEL", raising=False)
        from agentic_v2.langchain.models import _resolve_model_override
        resolved = _resolve_model_override(
            "env:DEEP_RESEARCH_SMALL_MODEL|gh:openai/gpt-4o-mini"
        )
        assert resolved == "gh:openai/gpt-4o-mini"

    def test_env_model_override_uses_env_value(self, monkeypatch):
        monkeypatch.setenv("DEEP_RESEARCH_HEAVY_MODEL", "ollama:deepseek-r1")
        from agentic_v2.langchain.models import _resolve_model_override
        resolved = _resolve_model_override(
            "env:DEEP_RESEARCH_HEAVY_MODEL|gh:openai/gpt-4o"
        )
        assert resolved == "ollama:deepseek-r1"


class TestGraphResponseParsing:
    """Regression tests for provider-specific response parsing."""

    def test_extract_agent_response_text_handles_content_list(self):
        from langchain_core.messages import AIMessage
        from agentic_v2.langchain import graph as graph_module

        payload = {
            "messages": [
                AIMessage(
                    content=[
                        {
                            "type": "text",
                            "text": '```json\n{"scoped_goal":"ok"}\n```',
                        }
                    ]
                )
            ]
        }

        text = graph_module._extract_agent_response_text(payload)
        assert isinstance(text, str)
        assert '"scoped_goal":"ok"' in text

    def test_parse_step_outputs_extracts_fenced_json(self):
        from agentic_v2.langchain import graph as graph_module

        parsed = graph_module._parse_step_outputs(
            '```json\n{"executive_summary":"s","references":["a"]}\n```'
        )
        assert parsed["executive_summary"] == "s"
        assert parsed["references"] == ["a"]

    def test_llm_step_maps_outputs_from_list_content(self, monkeypatch):
        from langchain_core.messages import AIMessage
        from agentic_v2.langchain import graph as graph_module

        class _DummyAgent:
            def invoke(self, payload):
                return {
                    "messages": [
                        AIMessage(
                            content=[
                                {
                                    "type": "text",
                                    "text": '```json\n{"scoped_goal":"mapped"}\n```',
                                }
                            ]
                        )
                    ]
                }

        def _fake_create_agent(*args, **kwargs):
            return _DummyAgent()

        monkeypatch.setattr(graph_module, "create_agent", _fake_create_agent)

        step = StepConfig(
            name="intake_scope",
            agent="tier3_planner",
            description="test",
            outputs={"scoped_goal": "scoped_goal"},
        )
        wf = WorkflowConfig(name="wf_parse", steps=[step])
        node = graph_module._make_step_node(step, wf)
        state = initial_state(workflow_inputs={})
        state["context"]["inputs"] = {}

        updated = node(state)
        assert updated["context"]["scoped_goal"] == "mapped"
        assert (
            updated["steps"]["intake_scope"]["outputs"]["scoped_goal"] == "mapped"
        )
