from typing import Optional
import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path


# =============================================================================
# WINDOWS CONSOLE ENCODING FIX - Use shared module
# =============================================================================
try:
    from tools.core._encoding import setup_encoding
    setup_encoding()
except ImportError:
    # Fallback if running as standalone script
    import io
    if sys.platform == "win32":
        os.environ["PYTHONIOENCODING"] = "utf-8"
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except (AttributeError, IOError):
            pass


class LLMClient:
    """
    Unified client for interacting with different LLM providers.

    Supported providers:
      - local:* -> Local ONNX models (phi4mini, phi3, phi3.5, mistral-7b, etc.)
            - ollama:* -> Local Ollama server (OpenAI-unrelated HTTP API)
      - azure-foundry:* -> Azure Foundry API
            - azure-openai:* -> Azure OpenAI Service (deployment-based)
      - gh:* -> GitHub Models API
            - openai:* -> OpenAI hosted API (explicit prefix)
            - gemini:* -> Google Gemini API (explicit prefix)
            - claude:* -> Anthropic Claude API (explicit prefix)
      - gemini* -> Google Gemini API
      - claude* -> Anthropic Claude API
      - gpt* -> OpenAI API
    """

    # Available local models (from AI Gallery cache)
    # Updated 2025-12-18 - Full model list from ~/.cache/aigallery
    # Format: "key": ("base_dir", "subpath") or just "base_dir" for auto-detect
    LOCAL_MODELS = {
        # ═══════════════════════════════════════════════════════════════════
        # PHI-4 (Latest - 3.8B params)
        # ═══════════════════════════════════════════════════════════════════
        "phi4": "microsoft--Phi-4-mini-instruct-onnx",
        "phi4mini": "microsoft--Phi-4-mini-instruct-onnx",
        "phi4-cpu": "microsoft--Phi-4-mini-instruct-onnx/main/cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4",
        "phi4-gpu": "microsoft--Phi-4-mini-instruct-onnx/main/gpu/gpu-int4-rtn-block-32",
        
        # ═══════════════════════════════════════════════════════════════════
        # PHI-3.5 (3.8B params)
        # ═══════════════════════════════════════════════════════════════════
        "phi3.5": "microsoft--Phi-3.5-mini-instruct-onnx",
        "phi3.5-cpu": "microsoft--Phi-3.5-mini-instruct-onnx/main/cpu_and_mobile/cpu-int4-awq-block-128-acc-level-4",
        "phi3.5-vision": "microsoft--Phi-3.5-vision-instruct-onnx/main/cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4",
        
        # ═══════════════════════════════════════════════════════════════════
        # PHI-3 MINI (3.8B params)
        # ═══════════════════════════════════════════════════════════════════
        "phi3": "microsoft--Phi-3-mini-4k-instruct-onnx",
        "phi3-cpu": "microsoft--Phi-3-mini-4k-instruct-onnx/main/cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4",
        "phi3-cpu-acc1": "microsoft--Phi-3-mini-4k-instruct-onnx/main/cpu_and_mobile/cpu-int4-rtn-block-32",
        "phi3-dml": "microsoft--Phi-3-mini-4k-instruct-onnx/main/directml/directml-int4-awq-block-128",
        "phi3-vision": "microsoft--Phi-3-vision-128k-instruct-onnx/main/cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4",
        
        # ═══════════════════════════════════════════════════════════════════
        # PHI-3 MEDIUM (14B params - larger, slower, more capable)
        # ═══════════════════════════════════════════════════════════════════
        "phi3-medium": "microsoft--Phi-3-medium-4k-instruct-onnx-cpu",
        "phi3-medium-cpu": "microsoft--Phi-3-medium-4k-instruct-onnx-cpu/main/cpu-int4-rtn-block-32-acc-level-4",
        "phi3-medium-dml": "microsoft--Phi-3-medium-4k-instruct-onnx-directml/main/directml-int4-awq-block-128",
        
        # ═══════════════════════════════════════════════════════════════════
        # MISTRAL 7B (7B params)
        # ═══════════════════════════════════════════════════════════════════
        "mistral": "microsoft--mistral-7b-instruct-v0.2-ONNX",
        "mistral-7b": "microsoft--mistral-7b-instruct-v0.2-ONNX",
        "mistral-cpu": "microsoft--mistral-7b-instruct-v0.2-ONNX/main/onnx/cpu_and_mobile/mistral-7b-instruct-v0.2-cpu-int4-rtn-block-32-acc-level-4",
        "mistral-cpu-acc1": "microsoft--mistral-7b-instruct-v0.2-ONNX/main/onnx/cpu_and_mobile/mistral-7b-instruct-v0.2-cpu-int4-rtn-block-32",
        "mistral-dml": "microsoft--mistral-7b-instruct-v0.2-ONNX/main/onnx/directml/mistralai_Mistral-7B-Instruct-v0.2",
        
        # ═══════════════════════════════════════════════════════════════════
        # EMBEDDING MODELS (for RAG, similarity search)
        # ═══════════════════════════════════════════════════════════════════
        "minilm-l6": "sentence-transformers--all-MiniLM-L6-v2",
        "minilm-l12": "sentence-transformers--all-MiniLM-L12-v2",
        
        # ═══════════════════════════════════════════════════════════════════
        # WHISPER (Speech-to-Text)
        # ═══════════════════════════════════════════════════════════════════
        "whisper-tiny": "khmyznikov--whisper-int8-cpu-ort.onnx",
        "whisper-small": "khmyznikov--whisper-int8-cpu-ort.onnx",
        "whisper-medium": "khmyznikov--whisper-int8-cpu-ort.onnx",
        "whisper": "khmyznikov--whisper-int8-cpu-ort.onnx",
        
        # ═══════════════════════════════════════════════════════════════════
        # IMAGE MODELS
        # ═══════════════════════════════════════════════════════════════════
        "stable-diffusion": "CompVis--stable-diffusion-v1-4",
        "esrgan": "microsoft--dml-ai-hub-models",
    }

    @staticmethod
    def _pick_preferred_model(
        available: list[str],
        preferred: list[str],
    ) -> Optional[str]:
        """Pick the first model in preferred that is present in available.

        Matching is exact; callers should normalize names if needed.
        """
        available_set = set(available)
        for m in preferred:
            if m in available_set:
                return m
        return None

    @staticmethod
    def list_openai_models() -> list[str]:
        """Return model IDs available to the current OPENAI_API_KEY.

        Uses the OpenAI API. Returns an empty list if not configured.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return []

        try:
            from openai import OpenAI
        except ImportError:
            return []

        client = OpenAI(api_key=api_key)
        try:
            # openai>=1.x returns an object with .data
            models = client.models.list()
            ids: list[str] = []
            for m in models.data:
                mid = getattr(m, "id", None)
                if mid:
                    ids.append(mid)
            return sorted(ids)
        except Exception:
            return []

    @staticmethod
    def list_gemini_models() -> list[str]:
        """Return the list of Gemini model IDs usable for generateContent.

        Uses google-generativeai's model listing when available.
        Returns an empty list if not configured.
        """
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            return []

        try:
            import google.generativeai as genai
        except ImportError:
            return []

        genai.configure(api_key=api_key)
        models_out: list[str] = []
        try:
            for m in genai.list_models():
                name = getattr(m, "name", None)
                if not name:
                    continue
                # names commonly come back like "models/gemini-1.5-pro"
                model_id = name.split("/", 1)[1] if "/" in name else name
                methods = (
                    getattr(m, "supported_generation_methods", None) or []
                )
                # Only include models that can generate content.
                if "generateContent" in methods:
                    models_out.append(model_id)
                elif "generate_content" in methods:
                    models_out.append(model_id)
        except Exception:
            return []

        return sorted(set(models_out))

    @staticmethod
    def generate_text(
        model_name: str,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
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
          - windows-ai:* -> Windows AI APIs / Phi Silica (NPU-accelerated, local)
          - azure-foundry:* -> Azure Foundry API (e.g., "azure-foundry:phi4mini")
          - gh:* -> GitHub Models (e.g., "gh:gpt-4o-mini", "gh:llama-3.3-70b")
          - gemini* -> Google Gemini API
          - claude* -> Anthropic Claude API
          - gpt* -> OpenAI API
        
        Caching:
          - Set PROMPTS_CACHE_ENABLED=0 to disable response caching
          - Use tools/cache.py to manage cache manually
        """
        # Check cache first (if enabled)
        # Check env var at runtime to allow tests to disable caching
        cache_enabled = os.environ.get("PROMPTS_CACHE_ENABLED", "1").lower() in ("1", "true", "yes")
        cache_response_func = None
        try:
            from cache import get_cached_response, cache_response as cache_response_func
            if cache_enabled:
                cached = get_cached_response(
                    model_name, prompt, system_instruction,
                    temperature=temperature, max_tokens=max_tokens
                )
                if cached is not None:
                    print(f"[{model_name}] Cache hit")
                    return cached
        except ImportError:
            cache_enabled = False
        
        def _remote_allowed() -> bool:
            v = (os.getenv("PROMPTEVAL_ALLOW_REMOTE") or "").strip().lower()
            return v in {"1", "true", "yes", "y", "on"}

        # Safe-by-default: only allow local + GitHub Models unless explicitly enabled.
        # GitHub Models are remote, but are explicitly allowed here.
        lower = (model_name or "").lower()
        default_allowed = (
            "local:",
            "gh:",
            "windows-ai:",
            "ollama:",
            "aitk:",
            "ai-toolkit:",
        )
        if not lower.startswith(default_allowed):
            remote_patterns = (
                "azure-foundry:",
                "azure-openai:",
                "openai:",
                "gemini:",
                "claude:",
            )
            if lower.startswith(remote_patterns) or ("gpt" in lower) or ("gemini" in lower) or ("claude" in lower):
                if not _remote_allowed():
                    raise RuntimeError(
                        f"Remote provider disabled by default: '{model_name}'. "
                        "Set PROMPTEVAL_ALLOW_REMOTE=1 to enable remote providers."
                    )

        print(f"[{model_name}] Processing request...")

        try:
            result = None
            if model_name.lower().startswith("local:"):
                result = LLMClient._call_local(model_name, prompt, system_instruction, temperature, max_tokens)
            elif model_name.lower().startswith("ollama:"):
                result = LLMClient._call_ollama(model_name, prompt, system_instruction)
            elif model_name.lower().startswith("windows-ai:"):
                result = LLMClient._call_windows_ai(model_name, prompt, system_instruction, temperature, max_tokens)
            elif model_name.lower().startswith("azure-foundry:"):
                result = LLMClient._call_azure_foundry(
                    model_name, prompt, system_instruction, temperature, max_tokens)
            elif model_name.lower().startswith("azure-openai:"):
                result = LLMClient._call_azure_openai(
                    model_name, prompt, system_instruction, temperature, max_tokens)
            elif model_name.lower().startswith("gh:"):
                result = LLMClient._call_github_models(model_name, prompt, system_instruction)
            elif model_name.lower().startswith("openai:"):
                # Explicit prefix for OpenAI hosted models
                model_id = model_name.split(":", 1)[1]
                result = LLMClient._call_openai(model_id, prompt, system_instruction,
                                              temperature, max_tokens)
            elif model_name.lower().startswith("gemini:"):
                model_id = model_name.split(":", 1)[1]
                result = LLMClient._call_gemini(model_id, prompt, system_instruction)
            elif model_name.lower().startswith("claude:"):
                model_id = model_name.split(":", 1)[1]
                result = LLMClient._call_claude(model_id, prompt, system_instruction)
            elif "gemini" in model_name.lower():
                result = LLMClient._call_gemini(model_name, prompt, system_instruction)
            elif "claude" in model_name.lower():
                result = LLMClient._call_claude(model_name, prompt, system_instruction)
            elif "gpt" in model_name.lower():
                result = LLMClient._call_openai(model_name, prompt, system_instruction,
                                              temperature, max_tokens)
            else:
                return (
                    f"Unknown model: {model_name}. Use local:, ollama:, windows-ai:, azure-foundry:, "
                    "azure-openai:, gh:, openai:, gemini:, claude:, or a plain model name containing gemini/claude/gpt"
                )
            
            # Cache successful response
            if result and cache_enabled and cache_response_func:
                try:
                    cache_response_func(
                        model_name, prompt, result, system_instruction,
                        temperature=temperature, max_tokens=max_tokens
                    )
                except Exception:
                    pass  # Don't fail on cache errors
            
            return result
        except Exception as e:
            return f"Error calling {model_name}: {str(e)}"

    @staticmethod
    def _call_ollama(model_name: str, prompt: str, system_instruction: Optional[str]) -> str:
        """
        Call a local Ollama server using its REST API.

        Model name format: ollama:<model>
        Example: ollama:llama3

        Environment variables:
          - OLLAMA_HOST: URL of the Ollama server (default: http://localhost:11434)
        
        Args:
            model_name: Name of the model in Ollama.
            prompt: User message.
            system_instruction: System instructions to prepend.
            
        Returns:
            Generated text response.
        """
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
        model = model_name.split(":", 1)[1] if ":" in model_name else "llama3"

        full_prompt = prompt
        if system_instruction:
            full_prompt = f"System: {system_instruction}\n\nUser: {prompt}"

        payload = json.dumps({
            "model": model,
            "prompt": full_prompt,
            "stream": False,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{host}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(req, timeout=600) as resp:  # 10 minutes for reasoning models
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("response", "")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else str(e)
            raise RuntimeError(f"Ollama API error ({e.code}): {error_body}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Ollama connection error: {e}")

    @staticmethod
    def _call_azure_openai(
        model_name: str,
        prompt: str,
        system_instruction: Optional[str],
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """
        Call Azure OpenAI Service via the OpenAI Python SDK (deployment-based).

        Model name formats:
          - azure-openai:<deployment>
          - azure-openai:<slot>:<deployment> (uses slot-specific env vars)

        Environment variables:
          - AZURE_OPENAI_ENDPOINT: Main service endpoint.
          - AZURE_OPENAI_API_KEY: Authentication key.
          - AZURE_OPENAI_API_VERSION: API version (default: 2024-02-15-preview).
          
        Args:
            model_name: Deployment string including optional slot.
            prompt: User message.
            system_instruction: System prompt.
            temperature: Sampling temperature.
            max_tokens: Token limit.
            
        Returns:
            Generated text content.
        """
        parts = model_name.split(":")
        # parts[0] == "azure-openai"
        slot: Optional[int] = None
        deployment: Optional[str] = None

        if len(parts) == 2:
            deployment = parts[1]
        elif len(parts) >= 3:
            # azure-openai:<slot>:<deployment...>
            try:
                slot = int(parts[1])
                deployment = ":".join(parts[2:])
            except ValueError:
                # If slot isn't an int, treat everything after prefix as deployment
                deployment = ":".join(parts[1:])

        if not deployment:
            raise ValueError("Azure OpenAI deployment name not provided (azure-openai:<deployment>)")

        if slot is not None:
            endpoint = os.getenv(f"AZURE_OPENAI_ENDPOINT_{slot}")
            api_key = os.getenv(f"AZURE_OPENAI_API_KEY_{slot}")
        else:
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT_0")
            api_key = os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY_0")

        if not endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT(_<n>) environment variable not set")
        if not api_key:
            raise ValueError("AZURE_OPENAI_API_KEY(_<n>) environment variable not set")

        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

        try:
            from openai import AzureOpenAI
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")

        client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version,
        )

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    @staticmethod
    def _call_local(model_name: str, prompt: str, system_instruction: Optional[str],
                    temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        Call a local ONNX model using the LocalModel class (onnxruntime-genai).

        Model name format: local:<model_key>
        Supported keys are defined in LLMClient.LOCAL_MODELS.
        
        Args:
            model_name: Key for the local model.
            prompt: User message.
            system_instruction: System prompt.
            temperature: Sampling temperature.
            max_tokens: Token limit.
            
        Returns:
            Generated text from local inference.
        """
        # Import local_model module
        try:
            from tools.llm.local_model import LocalModel
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
    def _call_windows_ai(model_name: str, prompt: str, system_instruction: Optional[str],
                         temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        Call Windows AI APIs (Phi Silica via Windows Copilot Runtime).
        
        Model name format: windows-ai:phi-silica
        
        Requirements:
          - Windows 11 with NPU (Copilot+ PC)
          - Windows App SDK 1.7+
          - pip install winrt-runtime
        
        Reference:
          https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica
        """
        try:
            from windows_ai import WindowsAIModel
            
            model = WindowsAIModel(verbose=False)
            return model.generate(
                prompt,
                system_instruction=system_instruction,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
        except ImportError:
            return (
                "❌ Windows AI integration not available.\n\n"
                "Requirements:\n"
                "  • Windows 11 with NPU (Copilot+ PC)\n"
                "  • Windows App SDK 1.7+\n"
                "  • pip install winrt-runtime\n\n"
                "Documentation: https://learn.microsoft.com/en-us/windows/ai/apis/\n\n"
                "Falling back to other providers..."
            )
        except Exception as e:
            return f"Windows AI error: {str(e)}"

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
                capture_output=True, text=True, timeout=120, encoding='utf-8', errors='replace'
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
            # Support either GOOGLE_API_KEY (legacy) or GEMINI_API_KEY (preferred in this repo's .env)
            api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY environment variable not set")

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
            api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY or CLAUDE_API_KEY environment variable not set")

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
