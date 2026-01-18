import os
from typing import List, Dict, Optional, Union, Any
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIPromptUtilities:
    """
    Utilities for OpenAI-specific prompt engineering patterns.
    Includes helpers for:
    - Function definition formatting
    - System message optimization
    - Token estimation (rough approximation)
    - Structured output validation
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def format_function_def(self, name: str, description: str, parameters: Dict) -> Dict:
        """
        Format a function definition for the OpenAI API tools parameter.
        """
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        }

    def optimize_system_message(self, role: str, goal: str, constraints: List[str]) -> str:
        """
        Constructs a highly effective system message based on best practices.
        """
        constraints_str = "\n".join([f"- {c}" for c in constraints])
        
        return f"""
You are an expert {role}.
Your primary goal is: {goal}

<constraints>
{constraints_str}
</constraints>

Please think step-by-step before answering.
"""

    def estimate_tokens(self, text: str) -> int:
        """
        Rough token estimation (approx 4 chars/token).
        In production, use `tiktoken`.
        """
        return len(text) // 4

    def validate_json_schema(self, schema: Dict) -> bool:
        """
        Basic validation to ensure a dict looks like a valid JSON schema for OpenAI functions.
        """
        required_keys = ["type", "properties"]
        if not all(k in schema for k in required_keys):
            logger.warning("Schema missing 'type' or 'properties' keys.")
            return False
        return True

    def create_structured_output_prompt(self, data_structure: str) -> str:
        """
        Generates a prompt snippet to encourage structured JSON output 
        (useful for models that don't support native JSON mode or as reinforcement).
        """
        return f"""
You must output valid JSON only. Do not include any markdown formatting (like ```json).
The JSON must adhere to this structure:
{data_structure}
"""

# Example Usage
if __name__ == "__main__":
    utils = OpenAIPromptUtilities(api_key="dummy")
    
    # 1. Format Function
    func_def = utils.format_function_def(
        name="get_weather",
        description="Get current weather",
        parameters={
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"]
        }
    )
    print("--- Function Definition ---")
    print(json.dumps(func_def, indent=2))
    
    # 2. Optimize System Message
    sys_msg = utils.optimize_system_message(
        role="Python Developer",
        goal="Write efficient, documented code",
        constraints=["Use type hints", "Follow PEP 8", "Include docstrings"]
    )
    print("\n--- System Message ---")
    print(sys_msg)
