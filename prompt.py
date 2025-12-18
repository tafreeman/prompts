#!/usr/bin/env python3
"""
Unified Prompt Toolkit - Single Entry Point
============================================

One script to rule them all. Run prompts, evaluate, verify, and improve
across 8 providers and 7 evaluation tiers.

Usage:
    python prompt.py                     # Interactive menu
    python prompt.py run <file>          # Execute a prompt
    python prompt.py eval <path>         # Evaluate prompts
    python prompt.py cove <question>     # Chain-of-Verification
    python prompt.py batch <folder>      # Batch processing
    python prompt.py improve <path>      # Get improvement suggestions
    python prompt.py models              # List available models
    python prompt.py help                # Show detailed help

Examples:
    python prompt.py run prompts/basic/greeting.md -p local
    python prompt.py eval prompts/advanced/ -t 3
    python prompt.py cove "When was Python created?" -p github
"""

import sys
import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

# Fix Windows console encoding for Unicode support
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, OSError):
        # Fallback for older Python or restricted environments
        pass

# Add tools directory to path
SCRIPT_DIR = Path(__file__).parent
TOOLS_DIR = SCRIPT_DIR / "tools"
sys.path.insert(0, str(TOOLS_DIR))


# =============================================================================
# BANNER AND HELP
# =============================================================================

BANNER = """
╔════════════════════════════════════════════════════════════════════════════╗
║                      🚀 UNIFIED PROMPT TOOLKIT                            ║
╠════════════════════════════════════════════════════════════════════════════╣
║  Execute, evaluate, and verify prompts across 8 providers                  ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

PROVIDERS = {
    "local": "Local ONNX Models (Phi-4, Mistral) - CPU/GPU, cross-platform",
    "windows": "Windows AI APIs (Phi Silica) - Local NPU, Copilot+ PCs only",
    "gh": "GitHub Models (gpt-4o-mini, gpt-4.1) - Cloud-based, FREE tier",
    "azure": "Azure Foundry (Enterprise) - Cloud-based, PAY-PER-USE",
    "openai": "OpenAI API (GPT-4o) - Cloud-based, PAID",
    "ollama": "Local Ollama Server - Local models (Llama, etc.)",
    "claude": "Anthropic Claude API - Cloud-based, PAID",
    "gemini": "Google Gemini API - Cloud-based, PAID",
}

TIERS = {
    0: ("Local ONNX", "Local ONNX via CPU/GPU - cross-platform, ~30-60s"),
    7: ("Windows AI", "Local NPU via Windows App SDK - Copilot+ PCs only, ~10-20s"),
    1: ("Quick Triage", "Structural only - <1 second"),
    2: ("Single Model", "One cloud model (gpt-4o-mini) - 15-45s"),
    3: ("Cross-Validate", "3 models × 2 runs - 2-4 min"),
    4: ("Full Pipeline", "5 models × 3 runs - 5-10 min"),
    5: ("Premium", "5 models × 4 runs - 10-20 min"),
    6: ("Azure Foundry", "Your Azure models - 15-30s"),
}


def print_help():
    """Print detailed help information."""
    print(BANNER)
    print("""
COMMANDS:
─────────────────────────────────────────────────────────────────────────────

  run <file> [options]     Execute a prompt file with an LLM
      -p, --provider       Provider: local, gh, azure, openai, ollama
      -m, --model          Model name (provider-specific)
      -i, --input          Input text to pass to prompt
      -o, --output         Output file path
      -s, --system         System prompt/instruction
      --temperature        Sampling temperature (0.0-2.0, default: 0.7)
      --max-tokens         Maximum tokens to generate (default: 2000)

  eval <path> [options]    Run tiered evaluation on prompt(s)
      -t, --tier           Tier 0-6 (default: 2)
      -o, --output         Output file path
      -f, --format         Output format: json, markdown

  cove <question>          Run Chain-of-Verification analysis
      -p, --provider       Provider (default: local)
      -n, --questions      Number of verification questions (default: 5)
      -o, --output         Output file path

  batch <folder>           Batch evaluate all prompts in a folder
      -p, --provider       Provider (default: local)
      -o, --output         Output directory

  improve <path>           Get improvement suggestions for prompts
      -o, --output         Output file path

  models                   List all available models by provider

  tiers                    Show evaluation tier details

EXAMPLES:
─────────────────────────────────────────────────────────────────────────────

  # Run with Local ONNX (Mistral)
  python prompt.py run prompts/basic/greeting.md -p local

  # Run with Windows AI (Phi Silica on NPU)
  python prompt.py run prompts/basic/greeting.md -p windows

  # Evaluate with Tier 7 (Windows AI NPU)
  python prompt.py eval prompts/advanced/ -t 7
""")


# =============================================================================
# INTERACTIVE MENU
# =============================================================================

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def interactive_menu():
    """Show interactive menu for easy navigation."""
    while True:
        clear_screen()
        print(BANNER)
        print("""
┌─────────────────────────────────────────────┐
│              MAIN MENU                      │
├─────────────────────────────────────────────┤
│  1. 🚀 Run a Prompt                         │
│  2. 📊 Evaluate Prompts                     │
│  3. ✅ Chain-of-Verification (CoVe)         │
│  4. 📦 Batch Processing                     │
│  5. 💡 Get Improvement Suggestions          │
│  6. 🔧 List Available Models                │
│  7. 📖 View Documentation                   │
│  8. ❓ Help                                  │
│  0. 🚪 Exit                                  │
└─────────────────────────────────────────────┘
""")
        choice = input("Enter choice [0-8]: ").strip()

        if choice == "0":
            print("\n👋 Goodbye!")
            break
        elif choice == "1":
            menu_run_prompt()
        elif choice == "2":
            menu_evaluate()
        elif choice == "3":
            menu_cove()
        elif choice == "4":
            menu_batch()
        elif choice == "5":
            menu_improve()
        elif choice == "6":
            menu_list_models()
        elif choice == "7":
            menu_docs()
        elif choice == "8":
            print_help()
            input("\nPress Enter to continue...")
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue...")


def menu_run_prompt():
    """Interactive prompt execution."""
    clear_screen()
    print("\n🚀 RUN A PROMPT\n")

    # Get file
    file_path = input("Prompt file path: ").strip()
    if not file_path or not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        input("\nPress Enter to continue...")
        return

    # Select provider
    print("\nAvailable providers:")
    for i, (key, desc) in enumerate(PROVIDERS.items(), 1):
        print(f"  {i}. {key}: {desc}")
    provider_choice = input("\nProvider [1-8, default=1 (local)]: ").strip() or "1"
    providers = list(PROVIDERS.keys())
    try:
        provider = providers[int(provider_choice) - 1]
    except (ValueError, IndexError):
        provider = "local"

    # Model (optional)
    model = input(f"Model name (press Enter for default): ").strip() or None

    # Execute
    print(f"\n⏳ Executing with {provider}...")
    run_prompt(file_path, provider, model)
    input("\nPress Enter to continue...")


def menu_evaluate():
    """Interactive evaluation."""
    clear_screen()
    print("\n📊 EVALUATE PROMPTS\n")

    # Get path
    eval_path = input("Path to prompt or folder: ").strip()
    if not eval_path or not Path(eval_path).exists():
        print(f"❌ Path not found: {eval_path}")
        input("\nPress Enter to continue...")
        return

    # Select tier
    print("\nAvailable tiers:")
    for tier_num, (name, desc) in TIERS.items():
        print(f"  {tier_num}. {name}: {desc}")
    tier_choice = input("\nTier [0-6, default=2]: ").strip() or "2"
    try:
        tier = int(tier_choice)
    except ValueError:
        tier = 2

    # Execute
    print(f"\n⏳ Running Tier {tier} evaluation...")
    eval_prompts(eval_path, tier)
    input("\nPress Enter to continue...")


def menu_cove():
    """Interactive CoVe analysis."""
    clear_screen()
    print("\n✅ CHAIN-OF-VERIFICATION (CoVe)\n")

    question = input("Enter question to verify: ").strip()
    if not question:
        print("❌ No question provided")
        input("\nPress Enter to continue...")
        return

    # Select provider
    print("\nAvailable providers:")
    cove_providers = ["local", "gh", "azure", "openai", "claude", "gemini"]
    for i, p in enumerate(cove_providers, 1):
        print(f"  {i}. {p}")
    provider_choice = input("\nProvider [1-6, default=1 (local)]: ").strip() or "1"
    try:
        provider = cove_providers[int(provider_choice) - 1]
        # Map gh to github for cove_runner
        if provider == "gh":
            provider = "github"
    except (ValueError, IndexError):
        provider = "local"

    n_questions = input("Number of verification questions [5]: ").strip() or "5"
    try:
        n = int(n_questions)
    except ValueError:
        n = 5

    # Execute
    print(f"\n⏳ Running CoVe with {provider}...")
    run_cove(question, provider, n)
    input("\nPress Enter to continue...")


def menu_batch():
    """Interactive batch processing."""
    clear_screen()
    print("\n📦 BATCH PROCESSING\n")

    folder = input("Folder path: ").strip()
    if not folder or not Path(folder).exists():
        print(f"❌ Folder not found: {folder}")
        input("\nPress Enter to continue...")
        return

    # Select provider
    print("\nAvailable providers: local, gh, azure")
    provider = input("Provider [default=local]: ").strip() or "local"

    # Execute
    print(f"\n⏳ Running batch with {provider}...")
    batch_process(folder, provider)
    input("\nPress Enter to continue...")


def menu_improve():
    """Interactive improvement suggestions."""
    clear_screen()
    print("\n💡 GET IMPROVEMENT SUGGESTIONS\n")

    path = input("Path to prompt or folder: ").strip()
    if not path or not Path(path).exists():
        print(f"❌ Path not found: {path}")
        input("\nPress Enter to continue...")
        return

    # Execute
    print("\n⏳ Analyzing prompts...")
    get_improvements(path)
    input("\nPress Enter to continue...")


def menu_list_models():
    """Show available models."""
    clear_screen()
    print("\n🔧 AVAILABLE MODELS\n")

    print("LOCAL ONNX MODELS (FREE):")
    print("  • local:phi4mini     - Phi-4 Mini (latest)")
    print("  • local:phi3.5       - Phi-3.5 Mini")
    print("  • local:phi3         - Phi-3 Mini")
    print("  • local:phi3-medium  - Phi-3 Medium (larger)")
    print("  • local:mistral-7b   - Mistral 7B Instruct")
    print()
    print("GITHUB MODELS (FREE TIER):")
    print("  • openai/gpt-4o-mini")
    print("  • openai/gpt-4.1")
    print("  • openai/gpt-4o")
    print("  • meta/llama-3.3-70b-instruct")
    print("  • mistral-ai/mistral-small-2503")
    print()
    print("AZURE FOUNDRY (YOUR DEPLOYMENT):")
    print("  • azure-foundry:phi4mini")
    print("  • azure-foundry:mistral")
    print()
    print("API MODELS (PAID):")
    print("  • gpt-4o, gpt-4-turbo        - OpenAI")
    print("  • claude-3-5-sonnet-20241022 - Anthropic")
    print("  • gemini-1.5-flash           - Google")

    input("\nPress Enter to continue...")


def menu_docs():
    """Open documentation."""
    clear_screen()
    print("\n📖 DOCUMENTATION\n")
    print("Available documentation:")
    print("  1. docs/UNIFIED_TOOLING_GUIDE.md    - Complete tooling reference")
    print("  2. docs/CLI_TOOLS.md                - CLI quick reference")
    print("  3. CoVE Reflexion Prompt Library... - CoVe methodology")
    print("  4. tools/README.md                  - Tools overview")
    print()

    choice = input("Open file [1-4, Enter to skip]: ").strip()
    docs = {
        "1": "docs/UNIFIED_TOOLING_GUIDE.md",
        "2": "docs/CLI_TOOLS.md",
        "3": "CoVE Reflexion Prompt Library Evaluation.md",
        "4": "tools/README.md",
    }
    if choice in docs:
        doc_path = SCRIPT_DIR / docs[choice]
        if doc_path.exists():
            print(f"\n--- {docs[choice]} ---\n")
            print(doc_path.read_text(encoding='utf-8')[:3000])
            print("\n... (truncated)\n")
        else:
            print(f"❌ File not found: {docs[choice]}")

    input("\nPress Enter to continue...")


# =============================================================================
# COMMAND IMPLEMENTATIONS
# =============================================================================

def run_prompt(file_path: str, provider: str = "local", model: Optional[str] = None,
               input_text: Optional[str] = None, output: Optional[str] = None,
               system: Optional[str] = None, temperature: float = 0.7,
               max_tokens: int = 2000):
    """Execute a prompt with the specified provider."""
    try:
        content = Path(file_path).read_text(encoding='utf-8')
        if input_text:
            content = f"{content}\n\n---\nUser Input:\n{input_text}"

        if provider == "local":
            from local_model import LocalModel
            lm = LocalModel(verbose=False)
            response = lm.generate(content, max_tokens=max_tokens, temperature=temperature,
                                   system_prompt=system)

        elif provider in ("gh", "github"):
            import subprocess
            model_name = model or "openai/gpt-4o-mini"
            result = subprocess.run(
                ["gh", "models", "run", model_name, "--", content[:8000]],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode != 0:
                print(f"❌ Error: {result.stderr}")
                return
            response = result.stdout

        elif provider == "azure":
            from llm_client import LLMClient
            model_key = model or "phi4mini"
            response = LLMClient.generate_text(f"azure-foundry:{model_key}", content)

        elif provider == "openai":
            from llm_client import LLMClient
            model_name = model or "gpt-4o-mini"
            response = LLMClient.generate_text(model_name, content)

        elif provider in ("windows", "windows-ai", "win"):
            from llm_client import LLMClient
            model_name = model or "phi-silica"
            response = LLMClient.generate_text(f"windows-ai:{model_name}", content)

        else:
            print(f"❌ Provider {provider} not implemented yet")
            return

        print("\n✅ Response:\n")
        print(response)

        if output:
            Path(output).write_text(response, encoding='utf-8')
            print(f"\n💾 Saved to: {output}")

    except Exception as e:
        print(f"❌ Error: {e}")


def eval_prompts(path: str, tier: int = 2, output: Optional[str] = None):
    """Run tiered evaluation on prompts."""
    try:
        from tiered_eval import find_prompts, TIERS as TIER_CONFIGS
        from tiered_eval import run_tier_0, run_tier_1, run_tier_2
        from tiered_eval import run_tier_3, run_tier_4, run_tier_5, run_tier_6

        prompts = find_prompts(path)
        if not prompts:
            print(f"❌ No prompts found at: {path}")
            return

        print(f"📊 Found {len(prompts)} prompt(s)")
        print(f"   Tier: {TIER_CONFIGS[tier].name} - {TIER_CONFIGS[tier].description}")

        tier_funcs = {
            0: run_tier_0, 1: run_tier_1, 2: run_tier_2,
            3: run_tier_3, 4: run_tier_4, 5: run_tier_5, 6: run_tier_6
        }

        output_dir = Path(output).parent if output else Path(".")
        results = tier_funcs[tier](prompts, output_dir)

        # Print summary
        print("\n✅ Results:\n")
        for r in results.get('results', []):
            status = "✅" if r.get('passed') or r.get('final_pass') else "❌"
            score = r.get('overall') or r.get('consensus_score') or r.get('score', 'N/A')
            print(f"  {status} {Path(r.get('file', '')).name}: {score}")

    except Exception as e:
        print(f"❌ Error: {e}")


def run_cove(question: str, provider: str = "local", n_questions: int = 5):
    """Run Chain-of-Verification analysis."""
    try:
        from cove_runner import get_llm_function, run_cove as _run_cove, format_result

        llm_call = get_llm_function(provider, None, verbose=True)
        print(f"   Model: {getattr(llm_call, 'model_name', 'unknown')}")

        result = _run_cove(question, llm_call, n_questions=n_questions, verbose=True)
        print("\n" + format_result(result, show_draft=False))

    except Exception as e:
        print(f"❌ Error: {e}")


def batch_process(folder: str, provider: str = "local", output: Optional[str] = None):
    """Batch process prompts in a folder."""
    try:
        from tiered_eval import find_prompts

        prompts = find_prompts(folder)
        if not prompts:
            print(f"❌ No prompts found in: {folder}")
            return

        print(f"📦 Found {len(prompts)} prompt(s)")

        results = {"total": len(prompts), "processed": 0, "errors": 0}

        for prompt_path in prompts:
            print(f"   Processing: {prompt_path.name}...", end="")
            try:
                if provider == "local":
                    from local_model import LocalModel
                    lm = LocalModel(verbose=False)
                    content = prompt_path.read_text(encoding='utf-8')[:4000]
                    response = lm.generate(f"Evaluate this prompt (1-10): {content[:500]}", max_tokens=200)
                    print(" ✅")
                    results["processed"] += 1
                else:
                    print(" ⏭️ (skipped - use local for demo)")
            except Exception as e:
                print(f" ❌ {e}")
                results["errors"] += 1

        print(f"\n📊 Summary: {results['processed']}/{results['total']} processed")

    except Exception as e:
        print(f"❌ Error: {e}")


def get_improvements(path: str, output: Optional[str] = None):
    """Get improvement suggestions for prompts."""
    try:
        from improve_prompts import find_prompt_files, assess_prompt, print_worst_prompts

        root = Path(path)
        if root.is_file():
            prompts = [root]
        else:
            prompts = find_prompt_files(root)

        if not prompts:
            print(f"❌ No prompts found at: {path}")
            return

        print(f"💡 Analyzing {len(prompts)} prompt(s)...\n")

        assessments = []
        for prompt_path in prompts[:10]:  # Limit for speed
            try:
                assessment = assess_prompt(prompt_path)
                assessments.append(assessment)
                tier = assessment.quality_tier
                print(f"  {tier} {prompt_path.name}: {assessment.quality_total:.0f}/100")
            except Exception as e:
                print(f"  ❌ {prompt_path.name}: {e}")

        if assessments:
            print("\n📋 Top Recommendations:")
            for a in sorted(assessments, key=lambda x: x.quality_total)[:5]:
                print(f"\n  {a.title or a.file_path}:")
                for issue in a.issues[:3]:
                    print(f"    • {issue.description}")

    except Exception as e:
        print(f"❌ Error: {e}")


def show_tiers():
    """Show tier details."""
    print("\n📊 EVALUATION TIERS\n")
    for tier_num, (name, desc) in TIERS.items():
        print(f"  Tier {tier_num}: {name}")
        print(f"          {desc}\n")


# =============================================================================
# ARGUMENT PARSING
# =============================================================================

def parse_args(args: List[str]) -> Dict[str, Any]:
    """Simple argument parser."""
    result = {"command": None, "args": [], "options": {}}

    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith("-"):
            # Option
            key = arg.lstrip("-")
            # Handle short options
            short_map = {"p": "provider", "m": "model", "t": "tier",
                         "o": "output", "n": "questions", "i": "input",
                         "f": "format", "v": "verbose", "s": "system"}
            key = short_map.get(key, key)

            if i + 1 < len(args) and not args[i + 1].startswith("-"):
                result["options"][key] = args[i + 1]
                i += 1
            else:
                result["options"][key] = True
        elif result["command"] is None:
            result["command"] = arg
        else:
            result["args"].append(arg)
        i += 1

    return result


def main():
    """Main entry point."""
    if len(sys.argv) == 1:
        # No arguments - show interactive menu
        interactive_menu()
        return

    # Parse arguments
    parsed = parse_args(sys.argv[1:])
    cmd = parsed["command"]
    args = parsed["args"]
    opts = parsed["options"]

    if cmd in ("help", "-h", "--help"):
        print_help()

    elif cmd == "run":
        if not args:
            print("❌ Usage: prompt.py run <file> [-p provider] [-m model]")
            sys.exit(1)
        run_prompt(args[0], opts.get("provider", "local"),
                   opts.get("model"), opts.get("input"), opts.get("output"),
                   opts.get("system"),
                   float(opts.get("temperature", 0.7)),
                   int(opts.get("max-tokens", opts.get("max_tokens", 2000))))

    elif cmd == "eval":
        if not args:
            print("❌ Usage: prompt.py eval <path> [-t tier] [-o output]")
            sys.exit(1)
        tier = int(opts.get("tier", 2))
        eval_prompts(args[0], tier, opts.get("output"))

    elif cmd == "cove":
        if not args:
            print("❌ Usage: prompt.py cove <question> [-p provider] [-n questions]")
            sys.exit(1)
        question = " ".join(args)
        provider = opts.get("provider", "local")
        n = int(opts.get("questions", 5))
        run_cove(question, provider, n)

    elif cmd == "batch":
        if not args:
            print("❌ Usage: prompt.py batch <folder> [-p provider]")
            sys.exit(1)
        batch_process(args[0], opts.get("provider", "local"), opts.get("output"))

    elif cmd == "improve":
        if not args:
            print("❌ Usage: prompt.py improve <path> [-o output]")
            sys.exit(1)
        get_improvements(args[0], opts.get("output"))

    elif cmd == "models":
        menu_list_models()

    elif cmd == "tiers":
        show_tiers()

    else:
        print(f"❌ Unknown command: {cmd}")
        print("   Run 'python prompt.py help' for usage")
        sys.exit(1)


if __name__ == "__main__":
    main()
