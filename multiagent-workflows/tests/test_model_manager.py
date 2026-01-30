"""
Tests for ModelManager

Tests model manager functionality with mocked backends.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestModelManager:
    """Test ModelManager class."""
    
    def test_init(self):
        """Test ModelManager initialization."""
        from multiagent_workflows.core.model_manager import ModelManager
        
        manager = ModelManager(allow_remote=False)
        assert manager.allow_remote is False
    
    def test_get_optimal_model_local_preference(self):
        """Test that local models are preferred when specified."""
        from multiagent_workflows.core.model_manager import ModelManager
        
        manager = ModelManager()
        
        # Should prefer local models
        model = manager.get_optimal_model("code_gen", 5, prefer_local=True)
        assert model.startswith("local:") or model.startswith("ollama:")
    
    def test_is_remote_model(self):
        """Test remote model detection."""
        from multiagent_workflows.core.model_manager import ModelManager
        
        manager = ModelManager()
        
        assert manager._is_remote_model("gh:gpt-4o") is True
        assert manager._is_remote_model("local:phi4") is False
        assert manager._is_remote_model("ollama:qwen2.5") is False
    
    def test_estimate_tokens(self):
        """Test token estimation."""
        from multiagent_workflows.core.model_manager import ModelManager
        
        manager = ModelManager()
        
        # Rough estimate: ~4 chars per token
        tokens = manager._estimate_tokens("Hello world", "Response text")
        assert tokens > 0
        assert tokens == (len("Hello world") + len("Response text")) // 4
    
    def test_estimate_cost(self):
        """Test cost estimation."""
        from multiagent_workflows.core.model_manager import ModelManager
        
        manager = ModelManager()
        
        # Local models should be free
        cost = manager._estimate_cost("local:phi4", 1000)
        assert cost == 0.0
        
        # Cloud models should have cost
        cost = manager._estimate_cost("gh:openai/gpt-4o", 1000000)
        assert cost > 0


class TestModelManagerAsync:
    """Async tests for ModelManager."""
    
    @pytest.mark.asyncio
    async def test_generate_with_mock(self, mock_model_manager):
        """Test generate with mocked backend."""
        result = await mock_model_manager.generate(
            model_id="mock:test",
            prompt="Test prompt",
        )
        
        assert result.text is not None
        assert result.model_id == "mock:test"
        assert result.tokens_used >= 0
    
    @pytest.mark.asyncio
    async def test_check_availability(self, mock_model_manager):
        """Test availability checking."""
        available = await mock_model_manager.check_availability("mock:test")
        assert available is True
    
    @pytest.mark.asyncio
    async def test_list_models(self):
        """Test listing models."""
        from multiagent_workflows.core.model_manager import ModelManager
        
        manager = ModelManager()
        models = await manager.list_models()
        
        # Should return a list
        assert isinstance(models, list)
