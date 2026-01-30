"""LangChain wrapper around the repo's LLMClient

This example provides a minimal LangChain-friendly LLM wrapper that delegates
to `tools.llm.llm_client.LLMClient.generate_text`. It is intentionally
lightweight and does not require `langchain` to be installed to import and
run a basic demo. If `langchain` is present, the example will demonstrate a
simple `LLMChain` call; otherwise it prints the raw response from the wrapper.

Usage:
  python examples/langchain_llmclient_wrapper.py

The script will pick the first model listed in `discovery_results.json` and
call it with a short prompt.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional


try:
    # Import the project's unified LLM client
    from tools.llm.llm_client import LLMClient
except Exception as e:
    raise ImportError("Could not import tools.llm.llm_client. Run this from the repo root.") from e


class LangChainLLMWrapper:
    """Minimal wrapper that delegates to LLMClient.generate_text.

    Provides a small compatibility surface: __call__, predict, and generate.
    LangChain integrations that expect a BaseLLM subclass may need a thin
    adapter for your LangChain version; this wrapper is intentionally simple
    so it imports cleanly in environments without langchain installed.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name

    def __call__(self, prompt: str, system: Optional[str] = None, **kwargs) -> str:
        # Delegate to the repo LLMClient. Keyword args are passed through when
        # applicable by LLMClient.generate_text (temperature, max_tokens, ...)
        return LLMClient.generate_text(self.model_name, prompt, system_instruction=system,
                                       temperature=kwargs.get("temperature", 0.7),
                                       max_tokens=kwargs.get("max_tokens", 1024))

    def predict(self, prompt: str) -> str:
        return self.__call__(prompt)

    def generate(self, prompts: List[str], **kwargs) -> List[str]:
        return [self.__call__(p, **kwargs) for p in prompts]


def pick_first_discovered_model(discovery_path: Path) -> Optional[str]:
    if not discovery_path.exists():
        return None
    data = json.loads(discovery_path.read_text(encoding="utf-8"))
    providers = data.get("providers", {})
    # Look for the first provider with an "available" list and return its first model
    for prov_name, prov in providers.items():
        avail = prov.get("available") or prov.get("available", [])
        if isinstance(avail, list) and len(avail) > 0:
            return avail[0]
    return None


def main():
    repo_root = Path(__file__).parents[1]
    discovery_file = repo_root / "discovery_results.json"

    model_name = pick_first_discovered_model(discovery_file)
    if not model_name:
        print("No model found in discovery_results.json. Run model probe first:")
        print("  python -m tools.llm.model_probe --discover -o discovery_results.json")
        return

    print(f"Using discovered model: {model_name}")
    wrapper = LangChainLLMWrapper(model_name)

    # Import the adapter so we can present a stable interface to LangChain
    try:
        from tools.llm.langchain_adapter import LangChainAdapter
        adapter = LangChainAdapter(model_name)
        print("LangChainAdapter loaded.")
    except Exception as e:
        adapter = None
        print(f"Could not load LangChainAdapter: {e}")

    demo_prompt = (
        "Summarize the following in one sentence: LangChain integration demo for the prompts repo."
    )

    # If langchain is installed, try a small LLMChain demo. Otherwise just call.
    # Try multiple import patterns across langchain versions and provide
    # clear debug messages. If LLMChain or PromptTemplate aren't available
    # or the wrapper isn't compatible, fall back to a direct call.
    # First, introspect the installed langchain package to help debug
    try:
        import langchain as _lc
        print("langchain package location:", getattr(_lc, "__file__", None))
        try:
            import pkgutil
            submods = [m.name for m in pkgutil.iter_modules(_lc.__path__)]
            print("langchain submodules:", submods)
        except Exception as _:
            print("Could not list langchain submodules")
    except Exception as _:
        print("langchain package not importable for introspection")
    LLMChain = None
    PromptTemplate = None
    template = None
    try:
        # Preferred locations
        from langchain.chains import LLMChain  # type: ignore
        from langchain.prompts import PromptTemplate  # type: ignore
        print("Imported LLMChain from langchain.chains and PromptTemplate from langchain.prompts")
    except Exception:
        try:
            # Alternate locations in other releases
            from langchain import LLMChain  # type: ignore
            from langchain.schema import PromptTemplate  # type: ignore
            print("Imported LLMChain from langchain and PromptTemplate from langchain.schema")
        except Exception as e:
            print(f"Could not import LLMChain/PromptTemplate from langchain: {e}")

    if PromptTemplate is not None:
        try:
            template = PromptTemplate(input_variables=["text"], template="{text}")
            print("PromptTemplate created successfully.")
        except Exception as e:
            print(f"PromptTemplate creation_failed: {e}")

    # We won't depend on LLMChain due to API instability across versions.
    # Instead use PromptTemplate (if available) to format the prompt and
    # call the repo LLMClient via the wrapper.
    formatted_prompt = demo_prompt
    if template is not None:
        try:
            # PromptTemplate objects may offer a variety of formatting APIs.
            if hasattr(template, "format"):
                formatted_prompt = template.format(text=demo_prompt)  # type: ignore
            elif hasattr(template, "format_prompt"):
                # Some PromptTemplate implementations return a PromptValue
                pv = template.format_prompt(text=demo_prompt)  # type: ignore
                formatted_prompt = getattr(pv, "to_string", lambda: str(pv))()
            else:
                # Fallback: simple replacement
                formatted_prompt = demo_prompt.replace("{text}", demo_prompt)
            print("Using PromptTemplate to format the prompt.")
        except Exception as e:
            print(f"PromptTemplate formatting failed: {e}")

    # If an adapter and LLMChain are available, prefer using them.
    if adapter is not None and 'LLMChain' in globals() and globals()['LLMChain'] is not None:
        try:
            chain = globals()['LLMChain'](llm=adapter, prompt=template)  # type: ignore
            out = chain.run(text=formatted_prompt)
            print("LLMChain result via adapter:\n", out)
            return
        except Exception as e:
            print(f"LLMChain via adapter failed: {e}")

    # Fallback: direct call
    try:
        out = wrapper.predict(formatted_prompt)
        print("Direct wrapper result:\n", out)
    except Exception as e:
        print(f"Direct LLMClient call failed: {e}")


if __name__ == "__main__":
    main()