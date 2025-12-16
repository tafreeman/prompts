from typing import Optional
import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path


class LLMClient:
    """
    Unified client for interacting with different LLM providers.

    Supported providers:
      - local:* -> Local ONNX models (phi4mini, phi3, phi3.5, mistral-7b, etc.)
      - azure-foundry:* -> Azure Foundry API
      - gh:* -> GitHub Models API
      - gemini* -> Google Gemini API
      - claude* -> Anthropic Claude API
      - gpt* -> OpenAI API
    """

    # Available local models (from AI Gallery cache)
    LOCAL_MODELS = {
        "phi4mini": "microsoft--Phi-4-mini-instruct-onnx",
        "phi4": "microsoft--Phi-4-mini-instruct-onnx",
        "phi3.5": "microsoft--Phi-3.5-mini-instruct-onnx",
        "phi3.5-vision": "microsoft--Phi-3.5-vision-instruct-onnx",
        "phi3": "microsoft--Phi-3-mini-4k-instruct-onnx",
        "phi3-medium": "microsoft--Phi-3-medium-4k-instruct-onnx",
        "phi3-vision": "microsoft--Phi-3-vision-128k-instruct-onnx",
        "mistral-7b": "microsoft--mistral-7b-instruct-v0.2-ONNX",
        "mistral": "microsoft--mistral-7b-instruct-v0.2-ONNX",
    }

    @staticmethod
    def generate_text(model_name: str, prompt: str, system_instruction: Optional[str] = None,
                      temperature: float = 0.7, max_tokens: int = 4096) -> str:
        """
        Dispatches the request to the appropriate provider based on model_name.

        Args:
            model_name: Model identifier (e.g., "local:phi4mini", "azure-foundry:phi4mini")
            prompt: The user prompt
            system_instruction: Optional system prompt
            temperature: Sampling temperature (0.0-2.0, default: 0.7)
            max_tokens: Maximum tokens to generate (default: 4096)

        Supported model name patterns:
          - local:* -> Local ONNX models (e.g., "local:phi4mini", "local:mistral-7b")
          - azure-foundry:* -> Azure Foundry API (e.g., "azure-foundry:phi4mini")
          - gh:* -> GitHub Models (e.g., "gh:gpt-4o-mini", "gh:llama-3.3-70b")
          - gemini* -> Google Gemini API
          - claude* -> Anthropic Claude API
          - gpt* -> OpenAI API
        """
        print(f"[{model_name}] Processing request...")

        try:
            if model_name.lower().startswith("local:"):
                return LLMClient._call_local(model_name, prompt, system_instruction,
                                             temperature, max_tokens)
            elif model_name.lower().startswith("azure-foundry:"):
                return LLMClient._call_azure_foundry(
                    model_name, prompt, system_instruction, temperature, max_tokens)
            elif model_name.lower().startswith("gh:"):
                return LLMClient._call_github_models(model_name, prompt, system_instruction)
            elif "gemini" in model_name.lower():
                return LLMClient._call_gemini(model_name, prompt, system_instruction)
            elif "claude" in model_name.lower():
                return LLMClient._call_claude(model_name, prompt, system_instruction)
            elif "gpt" in model_name.lower():
                return LLMClient._call_openai(model_name, prompt, system_instruction,
                                              temperature, max_tokens)
            else:
                return f"Unknown model: {model_name}. Use local:, azure-foundry:, gh:, gemini, claude, or gpt"
        except Exception as e:
            return f"Error calling {model_name}: {str(e)}"

    @staticmethod
    def _call_local(model_name: str, prompt: str, system_instruction: Optional[str],
                    temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        Call local ONNX model via local_model.py.

        Model name format: local:<model_key>
        Examples:
          - local:phi4mini -> Phi-4 Mini
          - local:phi3.5 -> Phi-3.5 Mini
          - local:mistral-7b -> Mistral 7B Instruct
        """
        # Import local_model module
        tools_dir = Path(__file__).parent
        sys.path.insert(0, str(tools_dir))

        try:
            from local_model import LocalModel
        except ImportError:
            return "Error: local_model.py not found or onnxruntime-genai not installed"

        # Parse model key
        model_key = model_name.split(":", 1)[1] if ":" in model_name else "phi4mini"

        # Find model path
        model_dir_name = LLMClient.LOCAL_MODELS.get(model_key.lower())
        if model_dir_name:
            ai_gallery = Path.home() / ".cache" / "aigallery" / model_dir_name
            if ai_gallery.exists():
                # Find the ONNX subdirectory
                for subdir in ai_gallery.rglob("*cpu*"):
                    if subdir.is_dir() and any(subdir.glob("*.onnx")):
                        model_path = str(subdir)
                        break
                else:
                    model_path = None
            else:
                model_path = None
        else:
            model_path = None

        try:
            lm = LocalModel(model_path=model_path, verbose=False)
            full_prompt = prompt
            if system_instruction:
                full_prompt = f"System: {system_instruction}\n\nUser: {prompt}"
            return lm.generate(full_prompt, max_tokens=max_tokens, temperature=temperature)
        except Exception as e:
            return f"Local model error: {str(e)}"

    @staticmethod
    def _call_github_models(model_name: str, prompt: str, system_instruction: Optional[str]) -> str:
        """
        Call GitHub Models API.

        Model name format: gh:<model_name>
        Examples:
          - gh:gpt-4o-mini
          - gh:gpt-4.1
          - gh:llama-3.3-70b-instruct
          - gh:mistral-small-2503
        """
        import subprocess

        # Parse model name (remove gh: prefix)
        model = model_name.split(":", 1)[1] if ":" in model_name else "gpt-4o-mini"

        # Map short names to full names
        model_map = {
            "gpt-4o-mini": "openai/gpt-4o-mini",
            "gpt-4o": "openai/gpt-4o",
            "gpt-4.1": "openai/gpt-4.1",
            "llama-3.3-70b": "meta/llama-3.3-70b-instruct",
            "mistral-small": "mistral-ai/mistral-small-2503",
        }
        full_model = model_map.get(model, model)

        # Build prompt with system instruction
        if system_instruction:
            full_prompt = f"System: {system_instruction}\n\nUser: {prompt}"
        else:
            full_prompt = prompt

        try:
            result = subprocess.run(
                ["gh", "models", "run", full_model, "--", full_prompt],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"gh models error: {result.stderr}"
        except FileNotFoundError:
            return "Error: gh CLI not found. Install GitHub CLI with gh-models extension."
        except subprocess.TimeoutExpired:
            return "Error: GitHub Models request timed out"

    @staticmethod
    def _call_azure_foundry(model_name: str, prompt: str, system_instruction: Optional[str],
                            temperature: float = 0.7, max_tokens: int = 4096) -> str:
        """
        Call Azure Foundry API using Azure OpenAI-compatible REST endpoint.
        
        Model name format: azure-foundry:<endpoint_key>
        Examples:
          - azure-foundry:1 -> Uses AZURE_FOUNDRY_ENDPOINT_1
          - azure-foundry:2 -> Uses AZURE_FOUNDRY_ENDPOINT_2
          - azure-foundry:phi4mini -> Uses AZURE_FOUNDRY_ENDPOINT_1 (default)
          - azure-foundry:mistral -> Uses AZURE_FOUNDRY_ENDPOINT_2
        
        Environment variables:
          - AZURE_FOUNDRY_API_KEY: API key for authentication
          - AZURE_FOUNDRY_ENDPOINT_1: First endpoint URL
          - AZURE_FOUNDRY_ENDPOINT_2: Second endpoint URL
        """
        api_key = os.getenv("AZURE_FOUNDRY_API_KEY")
        if not api_key:
            raise ValueError("AZURE_FOUNDRY_API_KEY environment variable not set")
        
        # Parse model name to determine endpoint
        # Format: azure-foundry:<endpoint_id_or_name>
        model_part = model_name.split(":", 1)[1] if ":" in model_name else "1"
        
        # Map model part to endpoint
        if model_part in ("1", "phi4mini", "phi4", "phi"):
            endpoint = os.getenv("AZURE_FOUNDRY_ENDPOINT_1")
        elif model_part in ("2", "mistral"):
            endpoint = os.getenv("AZURE_FOUNDRY_ENDPOINT_2")
        else:
            # Try numbered endpoint first
            endpoint = os.getenv(f"AZURE_FOUNDRY_ENDPOINT_{model_part}")
            if not endpoint:
                # Default to endpoint 1
                endpoint = os.getenv("AZURE_FOUNDRY_ENDPOINT_1")
        
        if not endpoint:
            raise ValueError(f"Azure Foundry endpoint not configured for '{model_part}'")
        
        # Ensure endpoint ends with /chat/completions
        if not endpoint.endswith("/chat/completions"):
            endpoint = endpoint.rstrip("/") + "/chat/completions"
        
        # Add API version if not present
        if "api-version" not in endpoint:
            endpoint += "?api-version=2024-02-15-preview"
        
        # Build messages
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        payload = json.dumps({
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }).encode("utf-8")
        
        req = urllib.request.Request(
            endpoint,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "api-key": api_key
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else str(e)
            raise RuntimeError(f"Azure Foundry API error ({e.code}): {error_body}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Azure Foundry connection error: {e}")

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
    def _call_openai(model_name: str, prompt: str, system_instruction: Optional[str],
                     temperature: float = 0.7, max_tokens: int = 4096) -> str:
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
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
