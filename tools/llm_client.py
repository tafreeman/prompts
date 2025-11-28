from typing import Optional
import os


class LLMClient:
    """
    Unified client for interacting with different LLM providers (Gemini, Claude, etc.).
    """

    @staticmethod
    def generate_text(model_name: str, prompt: str, system_instruction: Optional[str] = None) -> str:
        """
        Dispatches the request to the appropriate provider based on model_name.
        """
        print(f"[{model_name}] Processing request...")

        try:
            if "gemini" in model_name.lower():
                return LLMClient._call_gemini(model_name, prompt, system_instruction)
            elif "claude" in model_name.lower():
                return LLMClient._call_claude(model_name, prompt, system_instruction)
            elif "gpt" in model_name.lower():
                return LLMClient._call_openai(model_name, prompt, system_instruction)
            else:
                return f"Mock response from {model_name}: {prompt[:50]}..."
        except Exception as e:
            return f"Error calling {model_name}: {str(e)}"

    @staticmethod
    def _call_gemini(model_name: str, prompt: str, system_instruction: Optional[str]) -> str:
        try:
            import google.generativeai as genai
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not set")

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)

            # Gemini handles system instructions differently (often in the prompt or config)
            # For simplicity, we prepend it if provided
            full_prompt = prompt
            if system_instruction:
                full_prompt = f"System Instruction: {system_instruction}\n\n{prompt}"

            response = model.generate_content(full_prompt)
            return response.text
        except ImportError:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")

    @staticmethod
    def _call_claude(model_name: str, prompt: str, system_instruction: Optional[str]) -> str:
        try:
            from anthropic import Anthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")

            client = Anthropic(api_key=api_key)

            messages = [{"role": "user", "content": prompt}]
            kwargs = {
                "model": model_name,
                "max_tokens": 4096,
                "messages": messages
            }
            if system_instruction:
                kwargs["system"] = system_instruction

            response = client.messages.create(**kwargs)
            return response.content[0].text
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")

    @staticmethod
    def _call_openai(model_name: str, prompt: str, system_instruction: Optional[str]) -> str:
        try:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")

            client = OpenAI(api_key=api_key)

            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=model_name,
                messages=messages
            )
            return response.choices[0].message.content
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
