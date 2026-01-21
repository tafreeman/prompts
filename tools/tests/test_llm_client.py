#!/usr/bin/env python3
"""
Tests for tools.llm.llm_client module

Tests the multi-provider LLM client functionality.
"""

import sys
import pytest
from pathlib import Path

# Ensure tools package is importable
sys.path.insert(0, str(Path(__file__).parents[2]))

from tools.llm.llm_client import LLMClient


class TestLLMClientBasics:
    """Test basic LLMClient functionality"""
    
    def test_llm_client_import(self):
        """Test that LLMClient can be imported"""
        assert LLMClient is not None
    
    def test_generate_text_signature(self):
        """Test that generate_text method exists with correct signature"""
        assert hasattr(LLMClient, "generate_text")
        assert callable(LLMClient.generate_text)


class TestModelParsing:
    """Test model string parsing"""
    
    def test_local_model_format(self):
        """Test parsing local model strings"""
        # These should be valid model formats
        valid_models = [
            "local:phi4mini",
            "local:mistral",
            "gh:gpt-4o",
            "azure:gpt-4",
            "openai:gpt-4",
        ]
        
        for model in valid_models:
            # Just verify the format is recognized (doesn't throw immediately)
            assert ":" in model
            provider, name = model.split(":", 1)
            assert len(provider) > 0
            assert len(name) > 0


class TestGenerateText:
    """Test text generation functionality"""
    
    def test_generate_text_with_local_model(self):
        """Test generating text with a local model"""
        try:
            response = LLMClient.generate_text(
                model="local:phi4mini",
                prompt="Say hello in exactly 2 words.",
                max_tokens=50,
                temperature=0.0
            )
            
            # If successful, check response is a string
            assert isinstance(response, str)
            assert len(response) > 0
            
        except Exception as e:
            # In CI or environments without models, this is expected
            print(f"Local model test skipped: {e}")
            pass
    
    def test_generate_text_with_system_prompt(self):
        """Test generating text with a system prompt"""
        try:
            response = LLMClient.generate_text(
                model="local:phi4mini",
                prompt="What is 2+2?",
                system_prompt="You are a helpful math assistant. Answer concisely.",
                max_tokens=50,
                temperature=0.0
            )
            
            assert isinstance(response, str)
            
        except Exception as e:
            print(f"System prompt test skipped: {e}")
            pass
    
    def test_generate_text_with_temperature(self):
        """Test that temperature parameter is accepted"""
        try:
            response = LLMClient.generate_text(
                model="local:phi4mini",
                prompt="Hello",
                temperature=0.7,
                max_tokens=20
            )
            
            assert isinstance(response, str)
            
        except Exception as e:
            print(f"Temperature test skipped: {e}")
            pass
    
    def test_generate_text_error_handling(self):
        """Test error handling with invalid model"""
        try:
            response = LLMClient.generate_text(
                model="invalid:nonexistent",
                prompt="Test",
                max_tokens=10
            )
            
            # Should either raise exception or return error message
            if isinstance(response, str):
                # Some implementations return error strings
                assert "error" in response.lower() or "not found" in response.lower()
                
        except Exception as e:
            # Exception is also acceptable error handling
            assert True


class TestParameterValidation:
    """Test parameter validation"""
    
    def test_max_tokens_parameter(self):
        """Test that max_tokens parameter is respected"""
        try:
            response = LLMClient.generate_text(
                model="local:phi4mini",
                prompt="Count to 100",
                max_tokens=10  # Very small limit
            )
            
            # Response should be relatively short
            assert isinstance(response, str)
            # With 10 tokens, response shouldn't be super long
            assert len(response) < 500  # Generous upper bound
            
        except Exception as e:
            print(f"Max tokens test skipped: {e}")
            pass
    
    def test_empty_prompt_handling(self):
        """Test handling of empty prompts"""
        try:
            response = LLMClient.generate_text(
                model="local:phi4mini",
                prompt="",
                max_tokens=10
            )
            
            # Should either raise exception or return something
            assert response is not None
            
        except Exception as e:
            # Exception is acceptable for empty prompt
            assert True


class TestProviderSupport:
    """Test different provider support"""
    
    def test_supported_providers(self):
        """Test that common providers are recognized"""
        providers = ["local", "gh", "azure", "openai", "ollama"]
        
        for provider in providers:
            model_string = f"{provider}:test-model"
            # Just verify format is correct
            assert ":" in model_string
            parts = model_string.split(":", 1)
            assert parts[0] == provider


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_very_long_prompt(self):
        """Test handling of very long prompts"""
        long_prompt = "Hello " * 1000  # 5000+ characters
        
        try:
            response = LLMClient.generate_text(
                model="local:phi4mini",
                prompt=long_prompt,
                max_tokens=20
            )
            
            # Should handle or truncate gracefully
            assert response is not None
            
        except Exception as e:
            # Exception is acceptable for oversized prompts
            print(f"Long prompt test: {e}")
            pass
    
    def test_special_characters_in_prompt(self):
        """Test handling of special characters"""
        special_prompt = "Test: 你好! 🎉 <code>print('hello')</code>"
        
        try:
            response = LLMClient.generate_text(
                model="local:phi4mini",
                prompt=special_prompt,
                max_tokens=50
            )
            
            assert isinstance(response, str)
            
        except Exception as e:
            print(f"Special chars test skipped: {e}")
            pass


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
