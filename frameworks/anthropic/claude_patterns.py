import os
from typing import List, Dict, Optional, Union, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClaudePromptOptimizer:
    """
    Anthropic Claude-specific prompt optimization patterns.
    Implements best practices for Claude 3 models including:
    - XML tag structuring
    - Constitutional AI principles
    - Chain of Thought (CoT) enforcement
    - Tool use formatting
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        # In a real implementation, we would initialize the Anthropic client here
        # self.client = anthropic.Anthropic(api_key=self.api_key)
        
    def optimize_for_claude(self, prompt: str, optimization_type: str = 'xml_structure') -> str:
        """
        Optimize a generic prompt for Claude's specific capabilities.
        
        Args:
            prompt: The input prompt text
            optimization_type: Strategy ('xml_structure', 'constitutional', 'cot', 'prefill')
            
        Returns:
            Optimized prompt string
        """
        optimizers = {
            'xml_structure': self._apply_xml_structure,
            'constitutional': self._apply_constitutional_principles,
            'cot': self._enforce_chain_of_thought,
            'prefill': self._add_assistant_prefill
        }
        
        if optimization_type not in optimizers:
            raise ValueError(f"Unknown optimization type: {optimization_type}")
            
        return optimizers[optimization_type](prompt)

    def _apply_xml_structure(self, prompt: str) -> str:
        """
        Wraps prompt components in XML tags, which Claude prefers.
        """
        return f"""
<instruction>
You are a helpful AI assistant. Please follow these instructions carefully.
</instruction>

<user_request>
{prompt}
</user_request>

<guidelines>
- Use clear and concise language.
- Answer directly.
</guidelines>
"""

    def _apply_constitutional_principles(self, prompt: str) -> str:
        """
        Adds Constitutional AI principles to the prompt for safety and helpfulness.
        """
        principles = """
<constitution>
1. Be helpful and harmless.
2. Respect the user's intent.
3. Avoid stereotypes and bias.
4. If you cannot answer, explain why.
</constitution>
"""
        return f"{principles}\n\n{prompt}"

    def _enforce_chain_of_thought(self, prompt: str) -> str:
        """
        Encourages Claude to think step-by-step before answering.
        """
        return f"""
{prompt}

<thinking>
Please think step-by-step about how to answer this request. 
Break down the problem into components and analyze each one.
Wrap your thinking process in <thinking> tags.
</thinking>
"""

    def _add_assistant_prefill(self, prompt: str) -> str:
        """
        Simulates the 'prefill' technique where we start the assistant's response.
        Note: In API usage, this is passed as the 'messages' parameter, not the prompt itself.
        This method returns a string representation for documentation/template purposes.
        """
        return f"""
User: {prompt}

Assistant: Here is the answer to your request:
"""

    def format_tool_definition(self, tool_name: str, description: str, parameters: Dict) -> Dict:
        """
        Helper to format a tool definition for Claude's API.
        """
        return {
            "name": tool_name,
            "description": description,
            "input_schema": parameters
        }

# Example Usage
if __name__ == "__main__":
    optimizer = ClaudePromptOptimizer(api_key="dummy")
    
    raw_prompt = "Explain quantum entanglement to a 5-year-old."
    
    print("--- XML Optimized ---")
    print(optimizer.optimize_for_claude(raw_prompt, 'xml_structure'))
    
    print("\n--- CoT Optimized ---")
    print(optimizer.optimize_for_claude(raw_prompt, 'cot'))
