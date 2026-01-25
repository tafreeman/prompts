"""
Tests for VerboseLogger

Tests logging functionality and exports.
"""

import json
import pytest
from pathlib import Path


class TestVerboseLogger:
    """Test VerboseLogger functionality."""
    
    def test_logger_creation(self, logger):
        """Test logger initialization."""
        assert logger.workflow_id == "test-workflow"
        assert logger.events == []
    
    def test_workflow_logging(self, logger):
        """Test workflow start/complete logging."""
        # Start workflow
        wf_id = logger.log_workflow_start(
            workflow_name="test_workflow",
            inputs={"key": "value"},
        )
        
        assert wf_id is not None
        assert len(logger.events) == 1
        assert logger.events[0].event_type == "workflow.start"
        
        # Complete workflow
        logger.log_workflow_complete(
            workflow_id=wf_id,
            success=True,
            summary={"steps": 5},
        )
        
        assert len(logger.events) == 2
        assert logger.events[1].event_type == "workflow.complete"
    
    def test_step_logging(self, logger):
        """Test step logging."""
        wf_id = logger.log_workflow_start("test", {})
        
        step_id = logger.log_step_start(
            workflow_id=wf_id,
            step_name="test_step",
            context={"input": "data"},
        )
        
        assert step_id is not None
        
        logger.log_step_complete(
            step_id=step_id,
            success=True,
            outputs={"result": "done"},
        )
        
        # Should have workflow start, step start, step complete
        assert len(logger.events) == 3
    
    def test_model_call_logging(self, logger):
        """Test model call logging."""
        wf_id = logger.log_workflow_start("test", {})
        step_id = logger.log_step_start(wf_id, "step1")
        agent_id = logger.log_agent_start(step_id, "agent1", "mock:model")
        
        call_id = logger.log_model_call(
            agent_id=agent_id,
            model_id="mock:model",
            prompt="Test prompt",
            params={"temperature": 0.7},
        )
        
        assert call_id is not None
        
        logger.log_model_response(
            call_id=call_id,
            response="Test response",
            timing_ms=100.0,
            tokens=50,
            cost=0.001,
        )
        
        # Check metrics
        assert 50 in logger.metrics["tokens"]
        assert 0.001 in logger.metrics["cost"]
    
    def test_sanitize_secrets(self, logger):
        """Test that sensitive data is sanitized."""
        data = {
            "api_key": "secret123",
            "password": "secret456",
            "normal": "visible",
        }
        
        sanitized = logger._sanitize(data)
        
        assert sanitized["api_key"] == "[REDACTED]"
        assert sanitized["password"] == "[REDACTED]"
        assert sanitized["normal"] == "visible"
    
    def test_structured_log(self, logger):
        """Test getting structured log."""
        logger.log_workflow_start("test", {"input": "data"})
        
        structured = logger.get_structured_log()
        
        assert "workflow_id" in structured
        assert "events" in structured
        assert "metrics" in structured
        assert len(structured["events"]) == 1


class TestLoggerExports:
    """Test logger export functionality."""
    
    def test_export_to_json(self, logger, temp_output_dir):
        """Test JSON export."""
        logger.log_workflow_start("test", {})
        logger.log_workflow_complete("wf-1", True, {"done": True})
        
        output_path = temp_output_dir / "test_log.json"
        logger.export_to_json(output_path)
        
        assert output_path.exists()
        
        with open(output_path) as f:
            data = json.load(f)
        
        assert "events" in data
        assert len(data["events"]) == 2
    
    def test_export_to_markdown(self, logger, temp_output_dir):
        """Test Markdown export."""
        wf_id = logger.log_workflow_start("test", {})
        logger.log_workflow_complete(wf_id, True, {"done": True})
        
        output_path = temp_output_dir / "test_log.md"
        logger.export_to_markdown(output_path)
        
        assert output_path.exists()
        
        content = output_path.read_text()
        assert "# Workflow Log" in content
        assert "workflow.start" in content
