#!/usr/bin/env python3
"""
Chain-of-Verification (CoVe) Runner
====================================

Executes the CoVe technique to reduce hallucinations through independent verification.

Supports:
  - Local ONNX models (free, no API key)
  - GitHub Models API (free tier available)
  - OpenAI API
  - Ollama (local)

Usage:
    # With local ONNX model (default, free)
    python tools/cove_runner.py "What year was Python created and by whom?"

    # With GitHub Models (free tier)
    python tools/cove_runner.py --provider github "Your question here"

    # With OpenAI
    python tools/cove_runner.py --provider openai "Your question here"

    # With Ollama
    python tools/cove_runner.py --provider ollama --model llama3 "Your question here"

    # Interactive mode
    python tools/cove_runner.py --interactive

Author: Prompts Library Team
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable

# Add tools directory to path for local_model import
sys.path.insert(0, str(Path(__file__).parent))


# Load environment variables from .env file if present


def _load_dotenv():
    """Load .env file from project root if it exists."""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_path)
            return True
        except ImportError:
            # Fallback: simple .env parser
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if value and not os.environ.get(key):
                            os.environ[key] = value
            return True
    return False

_dotenv_loaded = _load_dotenv()


@dataclass
class CoVeResult:
    """Result of a Chain-of-Verification run."""
    question: str
    draft: str
    verification_questions: List[str]
    verified_answers: List[Dict[str, str]]
    final_answer: str
    verification_summary: List[Dict[str, Any]]
    confidence: str
    provider: str
    model: str


def get_llm_function(provider: str, model: Optional[str] = None, verbose: bool = False, model_path: Optional[str] = None) -> Callable[[str, Optional[str]], str]:
    """
    Returns a function that calls the LLM with (prompt, system_prompt) -> response.

    Supported providers:
      - local: Uses local ONNX model via onnxruntime-genai (free)
      - windows: Uses Windows AI Gallery models or Copilot Runtime (free)
      - ollama: Uses local Ollama server (free)
      - github: Uses GitHub Models API (free tier)
      - openai: Uses OpenAI API (paid)
      - azure_foundry: Uses Azure Foundry endpoints (pay-per-use)
      - claude: Uses Anthropic Claude API (paid)
      - gemini: Uses Google Gemini API (paid)

    Args:
      model_path: For local provider, explicit path to ONNX model directory
    """

    if provider == "windows" or provider == "windows-ai":
        # Windows AI - uses Local NPU (Phi Silica) via Windows App SDK
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from windows_ai import WindowsAIModel
            
            w_model = WindowsAIModel(verbose=verbose)
            model_name = "phi-silica (NPU)"

            def windows_call(prompt: str, system_prompt: Optional[str] = None) -> str:
                return w_model.generate(prompt, system_instruction=system_prompt)

            windows_call.model_name = model_name
            return windows_call

        except Exception as e:
            if verbose:
                print(f"⚠️  Windows AI NPU not available: {e}")
            raise ValueError(f"Windows AI NPU provider not available: {e}")

    if provider == "local":
        try:
            from local_model import LocalModel
            lm = LocalModel(model_path=model_path, verbose=verbose)
            model_name = lm.model_path.name if lm.model_path else "local-onnx"

            def local_call(prompt: str, system_prompt: Optional[str] = None) -> str:
                return lm.generate(prompt, system_prompt=system_prompt, temperature=0.7, max_tokens=1500)

            local_call.model_name = model_name
            return local_call
        except Exception as e:
            print(f"⚠️  Local model not available: {e}")
            print("Falling back to Ollama...")
            provider = "ollama"

    if provider == "ollama":
        import urllib.request
        import urllib.error

        model_name = model or "llama3"
        ollama_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

        def ollama_call(prompt: str, system_prompt: Optional[str] = None) -> str:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            payload = json.dumps({
                                 "model": model_name,
                                 "messages": messages,
                                 "stream": False,
                                 "options": {"temperature": 0.7}
            }).encode("utf-8")

            req = urllib.request.Request(
                                         f"{ollama_url}/api/chat",
                                         data=payload,
                                         headers={"Content-Type": "application/json"}
            )

            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    return data.get("message", {}).get("content", "")
            except urllib.error.URLError as e:
                raise RuntimeError(f"Ollama not reachable at {ollama_url}: {e}")

        ollama_call.model_name = model_name
        return ollama_call

    if provider == "github":
        # GitHub Models API (free tier available)
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if not token:
            raise ValueError(
                             "GitHub token required. Set GITHUB_TOKEN or GH_TOKEN environment variable.\n"
                             "Get a token at: https://github.com/settings/tokens"
                             )

        import urllib.request

        # GitHub Models uses just model name, not org/model format
        model_name = model or "gpt-4o-mini"
        endpoint = "https://models.inference.ai.azure.com/chat/completions"

        def github_call(prompt: str, system_prompt: Optional[str] = None) -> str:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            payload = json.dumps({
                                 "model": model_name,
                                 "messages": messages,
                                 "temperature": 0.7,
                                 "max_tokens": 2000
                                 }).encode("utf-8")

            req = urllib.request.Request(
                                         endpoint,
                                         data=payload,
                                         headers={
                                         "Content-Type": "application/json",
                                         "Authorization": f"Bearer {token}"
                                         }
            )

            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]

        github_call.model_name = model_name
        return github_call

    if provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable required")

        import urllib.request
        import urllib.error
        import time

        model_name = model or "gpt-4o-mini"

        def openai_call(prompt: str, system_prompt: Optional[str] = None) -> str:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            payload = json.dumps({
                                 "model": model_name,
                                 "messages": messages,
                                 "temperature": 0.7,
                                 "max_tokens": 2000
                                 }).encode("utf-8")

            req = urllib.request.Request(
                                         "https://api.openai.com/v1/chat/completions",
                                         data=payload,
                                         headers={
                                         "Content-Type": "application/json",
                                         "Authorization": f"Bearer {api_key}"
                                         }
            )

            # Retry with exponential backoff on rate limit
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(req, timeout=60) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                        return data["choices"][0]["message"]["content"]
                except urllib.error.HTTPError as e:
                    if e.code == 429 and attempt < 2:
                        wait = (attempt + 1) * 5  # 5s, 10s
                        if verbose:
                            print(f"   ⏳ Rate limited, waiting {wait}s...")
                        time.sleep(wait)
                        continue
                    raise

        openai_call.model_name = model_name
        return openai_call

    if provider == "azure_foundry" or provider == "azure-foundry":
        # Azure Foundry API - uses Azure OpenAI-compatible endpoints
        api_key = os.environ.get("AZURE_FOUNDRY_API_KEY")
        if not api_key:
            raise ValueError(
                "AZURE_FOUNDRY_API_KEY environment variable required.\n"
                "Set this in your .env file with your Azure Foundry API key."
            )

        import urllib.request
        import urllib.error

        # Determine which endpoint to use based on model
        # Supports: phi4mini, phi4, phi, mistral, or numeric (1, 2)
        model_part = model or "phi4mini"
        
        if model_part in ("phi4mini", "phi4", "phi", "1"):
            endpoint = os.environ.get("AZURE_FOUNDRY_ENDPOINT_1")
            model_name = f"azure-foundry-phi4mini"
        elif model_part in ("mistral", "2"):
            endpoint = os.environ.get("AZURE_FOUNDRY_ENDPOINT_2")
            model_name = f"azure-foundry-mistral"
        else:
            # Try to get numbered endpoint
            endpoint = os.environ.get(f"AZURE_FOUNDRY_ENDPOINT_{model_part}")
            model_name = f"azure-foundry-{model_part}"
            if not endpoint:
                # Default to endpoint 1
                endpoint = os.environ.get("AZURE_FOUNDRY_ENDPOINT_1")
                model_name = "azure-foundry-phi4mini"

        if not endpoint:
            raise ValueError(
                "Azure Foundry endpoint not configured.\n"
                "Set AZURE_FOUNDRY_ENDPOINT_1 and/or AZURE_FOUNDRY_ENDPOINT_2 in .env"
            )

        # Ensure endpoint ends with /chat/completions
        if not endpoint.endswith("/chat/completions"):
            endpoint = endpoint.rstrip("/") + "/chat/completions"
        
        # Add API version if not present
        if "api-version" not in endpoint:
            endpoint += "?api-version=2024-02-15-preview"

        def azure_foundry_call(prompt: str, system_prompt: Optional[str] = None) -> str:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            payload = json.dumps({
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000
            }).encode("utf-8")

            req = urllib.request.Request(
                endpoint,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "api-key": api_key
                }
            )

            # Retry with exponential backoff on rate limit
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(req, timeout=120) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                        return data["choices"][0]["message"]["content"]
                except urllib.error.HTTPError as e:
                    if e.code == 429 and attempt < 2:
                        wait = (attempt + 1) * 5  # 5s, 10s
                        if verbose:
                            print(f"   ⏳ Rate limited, waiting {wait}s...")
                        import time as time_module
                        time_module.sleep(wait)
                        continue
                    error_body = e.read().decode("utf-8") if e.fp else str(e)
                    raise RuntimeError(f"Azure Foundry API error ({e.code}): {error_body}")
                except urllib.error.URLError as e:
                    raise RuntimeError(f"Azure Foundry connection error: {e}")

        azure_foundry_call.model_name = model_name
        return azure_foundry_call

    if provider in ("claude", "gemini"):
        # Claude/Gemini API - delegate to llm_client
        try:
            from llm_client import LLMClient
        except ImportError:
            raise ValueError(f"llm_client.py not found - required for {provider} provider")

        if provider == "claude":
            model_name = model or "claude-3-5-sonnet-20241022"
        else:
            model_name = model or "gemini-1.5-flash"

        def api_call(prompt: str, system_prompt: Optional[str] = None) -> str:
            return LLMClient.generate_text(model_name, prompt, system_prompt)

        api_call.model_name = model_name
        return api_call

    raise ValueError(
        f"Unknown provider: {provider}. "
        "Use: local, windows, ollama, github, openai, azure_foundry, claude, gemini"
    )


COVE_SYSTEM_PROMPT = """You are a factual assistant. Answer questions accurately and concisely."""


def run_cove(
             question: str,
             llm_call: Callable[[str, Optional[str]], str],
             n_questions: int = 5,
             domain: Optional[str] = None,
             verbose: bool = False
             ) -> CoVeResult:
    """
    Execute the Chain-of-Verification process.

    Args:
        question: The user's question
        llm_call: Function to call LLM with (prompt, system_prompt) -> response
        n_questions: Number of verification questions to generate
        domain: Optional domain context
        verbose: Print progress

    Returns:
        CoVeResult with all phases documented
    """

    model_name = getattr(llm_call, 'model_name', 'unknown')

    # ─────────────────────────────────────────────────────────────────────────
    # Phase 1: Generate Draft
    # ─────────────────────────────────────────────────────────────────────────
    if verbose:
        print("\n📝 Phase 1: Generating draft response...")

    domain_hint = f" ({domain})" if domain else ""
    draft_prompt = """Question{domain_hint}: {question}

Answer with specific facts, dates, and names."""

    draft = llm_call(draft_prompt, COVE_SYSTEM_PROMPT)

    # Clean up draft - remove echoed system/user prompts (common with local models)
    for noise in [COVE_SYSTEM_PROMPT, draft_prompt, "Question:", "Answer with specific"]:
        if noise in draft:
            draft = draft.split(noise)[-1].strip()
    draft = draft.strip()

    if verbose:
        print(f"   Draft: {draft[:200]}...")

    # ─────────────────────────────────────────────────────────────────────────
    # Phase 2: Plan Verification Questions
    # ─────────────────────────────────────────────────────────────────────────
    if verbose:
        print(f"\n🔍 Phase 2: Generating {n_questions} verification questions...")
    verification_prompt = """Read this answer and write {n_questions} fact-checking questions:

"{draft[:500]}"

Write {n_questions} simple questions to verify the facts. Each question should check one specific claim (a date, name, number, or event).

Questions:
1."""

    vq_response = llm_call(verification_prompt, None)

    # Parse verification questions - look for numbered list or question marks
    verification_questions = []

    # First try numbered format: 1. Question? 2. Question?
    numbered = re.findall(r'\d+[\.\)]\s*([^?\n]+\?)', vq_response)
    if numbered:
        verification_questions = [q.strip() for q in numbered[:n_questions]]
    else:
        # Fallback: any line with a question mark
        lines = [l.strip() for l in vq_response.split('\n') if '?' in l]
        verification_questions = [re.sub(r'^[\d\.\-\*\)]+\s*', '', l).strip() for l in lines[:n_questions]]

    # Clean up any remaining numbering (e.g., "1. Question?" -> "Question?")
    verification_questions = [re.sub(r'^\d+[\.\)]\s*', '', q).strip() for q in verification_questions]

    # Final fallback: generate basic questions from the original question
    if not verification_questions or all(q in ['Question 1?', 'Question 2?', 'Question 3?'] for q in verification_questions):
        verification_questions = [
                                  f"Who {question.lower().replace('?', '')}?" if 'who' not in question.lower() else question,
                                  f"When {question.lower().replace('?', '')}?" if 'when' not in question.lower() else question,
                                  f"What facts support the answer to: {question}"
                                  ][:n_questions]

    if verbose:
        print(f"   Generated {len(verification_questions)} questions:")
        for i, q in enumerate(verification_questions, 1):
            print(f"      {i}. {q}")

    # ─────────────────────────────────────────────────────────────────────────
    # Phase 3: Execute Verification (Independent)
    # ─────────────────────────────────────────────────────────────────────────
    if verbose:
        print("\n✅ Phase 3: Answering verification questions independently...")

    verified_answers = []
    for i, vq in enumerate(verification_questions):
        if verbose:
            print(f"   Verifying Q{i+1}: {vq[:60]}...")

        # CRITICAL: Answer each question as a fresh query, NOT referencing the draft
        domain_ctx = f" (in {domain})" if domain else ""
        verify_prompt = """Question{domain_ctx}: {vq}

Answer briefly and factually:"""

        answer = llm_call(verify_prompt, None)

        # Clean up answer - remove echoed prompt (common with local models)
        clean_answer = answer.strip()
        for noise in [verify_prompt, "Question:", "Answer briefly", vq]:
            if noise in clean_answer:
                clean_answer = clean_answer.split(noise)[-1].strip()
        # Remove leading colons/punctuation
        clean_answer = re.sub(r'^[:\-\s]+', '', clean_answer).strip()

        verified_answers.append({"question": vq, "answer": clean_answer})

    # ─────────────────────────────────────────────────────────────────────────
    # Phase 4: Generate Final Verified Response
    # ─────────────────────────────────────────────────────────────────────────
    if verbose:
        print("\n📋 Phase 4: Synthesizing final verified response...")

    # Build verification context
    verification_context = "\n".join([
                                     f"- {va['question']} → {va['answer']}"
                                     for va in verified_answers
                                     ])
    final_prompt = """Answer the question using ONLY the verified facts below.

Question: {question}

Verified facts:
{verification_context}

Final answer:"""

    final_answer = llm_call(final_prompt, COVE_SYSTEM_PROMPT)

    # Clean up final answer
    for noise in [final_prompt, COVE_SYSTEM_PROMPT, "Final answer:", "Verified facts:"]:
        if noise in final_answer:
            final_answer = final_answer.split(noise)[-1].strip()
    final_answer = re.sub(r'^[:\-\s]+', '', final_answer).strip()

    # ─────────────────────────────────────────────────────────────────────────
    # Build Verification Summary
    # ─────────────────────────────────────────────────────────────────────────
    verification_summary = []
    for va in verified_answers:
        # Simple heuristic for verification status
        answer_lower = va['answer'].lower()
        if any(w in answer_lower for w in ['uncertain', 'not sure', 'cannot verify', 'no information']):
            status = "Uncertain"
        else:
            status = "Verified"

        verification_summary.append({
                                    "claim": va['question'],
                                    "verified": status,
                                    "note": va['answer'][:100] + ("..." if len(va['answer']) > 100 else "")
        })

    # Calculate confidence
    verified_count = sum(1 for v in verification_summary if v['verified'] == "Verified")
    total = len(verification_summary)
    if total == 0:
        confidence = "Low"
    elif verified_count / total >= 0.8:
        confidence = "High"
    elif verified_count / total >= 0.5:
        confidence = "Medium"
    else:
        confidence = "Low"

    return CoVeResult(
                      question=question,
                      draft=draft,
                      verification_questions=verification_questions,
                      verified_answers=verified_answers,
                      final_answer=final_answer,
                      verification_summary=verification_summary,
                      confidence=confidence,
                      provider=getattr(llm_call, '__name__', 'unknown').replace('_call', ''),
                      model=model_name
                      )


def format_result(result: CoVeResult, show_draft: bool = False) -> str:
    """Format CoVeResult as readable Markdown."""

    lines = [
             "# Chain-of-Verification (CoVe) Result",
             "",
             f"**Question:** {result.question}",
             f"**Model:** {result.model}",
             f"**Confidence:** {result.confidence}",
             "",
             ]

    if show_draft:
        lines.extend([
                     "## Draft (Phase 1)",
                     "",
                     result.draft,
                     "",
                     ])

    lines.extend([
                 "## Verification Questions (Phase 2)",
                 "",
                 ])
    for i, q in enumerate(result.verification_questions, 1):
        lines.append(f"{i}. {q}")

    lines.extend([
                 "",
                 "## Verified Answers (Phase 3)",
                 "",
                 ])
    for va in result.verified_answers:
        lines.append(f"**Q:** {va['question']}")
        lines.append(f"**A:** {va['answer']}")
        lines.append("")

    lines.extend([
                 "## Final Answer (Phase 4)",
                 "",
                 result.final_answer,
                 "",
                 "## Verification Summary",
                 "",
                 "| Claim | Status | Note |",
                 "|-------|--------|------|",
                 ])
    for v in result.verification_summary:
        lines.append(f"| {v['claim'][:50]}... | {v['verified']} | {v['note'][:40]}... |")

    lines.extend([
                 "",
                 f"**Overall Confidence:** {result.confidence}",
                 ])

    return "\n".join(lines)


def interactive_mode(llm_call: Callable, verbose: bool = False):
    """Run CoVe in interactive mode."""
    print("\n🔗 Chain-of-Verification Interactive Mode")
    print(f"   Model: {getattr(llm_call, 'model_name', 'unknown')}")
    print("   Type 'quit' to exit, 'help' for commands\n")

    while True:
        try:
            question = input("❓ Question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in ('quit', 'exit', 'q'):
            print("Goodbye!")
            break
        if question.lower() == 'help':
            print("""
                  Commands:
                  quit, exit, q  - Exit interactive mode
                  help           - Show this help

                  Just type your question and press Enter to run CoVe verification.
                  """)
            continue

        try:
            result = run_cove(question, llm_call, verbose=verbose)
            print("\n" + format_result(result, show_draft=verbose))
            print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(
                                     description="Run Chain-of-Verification (CoVe) to reduce hallucinations",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=r"""
                                     Examples:
                                     # Local ONNX model (free, no API)
  python tools/cove_runner.py "When was Python created?"

  # Local with specific model path
  python tools/cove_runner.py --model-path "C:\Users\tandf\.cache\aigallery\microsoft--Phi-4-mini-instruct-onnx\main\cpu_and_mobile\cpu-int4-rtn-block-32-acc-level-4" "Your question"

  # GitHub Models (free tier)
  python tools/cove_runner.py --provider github "What is the capital of France?"

  # Windows AI / Copilot Runtime (Windows 11)
  python tools/cove_runner.py --provider windows "What is machine learning?"

  # Ollama (local)
  python tools/cove_runner.py --provider ollama --model llama3 "Who invented the telephone?"

  # Interactive mode
  python tools/cove_runner.py --interactive

Providers:
  local   - Local ONNX model (default, free)
  windows - Windows AI / Copilot Runtime with Phi Silica (Windows 11, free)
  ollama  - Local Ollama server (free)
  github  - GitHub Models API (free tier with GITHUB_TOKEN)
  openai  - OpenAI API (requires OPENAI_API_KEY)
"""
    )

    parser.add_argument("question", nargs="?", help="Question to verify (or use --prompt-file)")
    parser.add_argument("--prompt-file", type=str, help="Path to a file containing the prompt or question to audit")
    parser.add_argument("--provider", "-p", default="local",
                        choices=["local", "windows", "ollama", "github", "openai"],
                        help="LLM provider (default: local)")
    parser.add_argument("--model", "-m", help="Model name (provider-specific)")
    parser.add_argument("--model-path", dest="model_path",
                        help="(local provider) Path to ONNX model directory")
    parser.add_argument("--questions", "-n", type=int, default=5,
                        help="Number of verification questions (default: 5)")
    parser.add_argument("--domain", "-d", help="Domain context for verification")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed progress")
    parser.add_argument("--show-draft", action="store_true",
                        help="Include draft in output")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Run in interactive mode")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()


    # Get LLM function
    try:
        llm_call = get_llm_function(args.provider, args.model, args.verbose, model_path=getattr(args, 'model_path', None))
        print(f"✅ Using {args.provider} provider with model: {getattr(llm_call, 'model_name', 'unknown')}")
    except Exception as e:
        print(f"❌ Failed to initialize provider '{args.provider}': {e}")
        sys.exit(1)

    # Interactive mode
    if args.interactive:
        interactive_mode(llm_call, args.verbose)
        return

    # Support --prompt-file for file-based prompt/question
    prompt_text = None
    if getattr(args, "prompt_file", None):
        try:
            with open(args.prompt_file, "r", encoding="utf-8") as f:
                prompt_text = f.read().strip()
        except Exception as e:
            print(f"❌ Error reading prompt file: {e}")
            sys.exit(1)

    # Single question mode (from file or argument)
    question_input = prompt_text if prompt_text else args.question
    if not question_input:
        parser.print_help()
        print("\n❌ Error: Please provide a question, --prompt-file, or use --interactive mode")
        sys.exit(1)

    try:
        result = run_cove(
            question_input,
            llm_call,
            n_questions=args.questions,
            domain=args.domain,
            verbose=args.verbose
        )

        if args.json:
            output = {
                "question": result.question,
                "draft": result.draft,
                "verification_questions": result.verification_questions,
                "verified_answers": result.verified_answers,
                "final_answer": result.final_answer,
                "verification_summary": result.verification_summary,
                "confidence": result.confidence,
                "provider": result.provider,
                "model": result.model
            }
            print(json.dumps(output, indent=2))
        else:
            print("\n" + format_result(result, show_draft=args.show_draft))

    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
