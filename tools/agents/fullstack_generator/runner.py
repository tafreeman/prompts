#!/usr/bin/env python3
"""
Hybrid Full-Stack Generator CLI Runner
======================================

Command-line interface for running the hybrid full-stack generator.

Usage:
    python -m tools.agents.fullstack_generator.runner "Your requirements here"
    python -m tools.agents.fullstack_generator.runner --file requirements.txt
    python -m tools.agents.fullstack_generator.runner --interactive
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

# Ensure imports work
sys.path.insert(0, str(Path(__file__).parents[3]))

from tools.agents.fullstack_generator.agents import (
    AGENT_REGISTRY,
    AgentTier,
    Phase,
    get_cost_summary,
)
from tools.agents.fullstack_generator.workflow import HybridFullStackGenerator


def print_banner():
    """Print welcome banner."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║         HYBRID FULL-STACK GENERATOR (LangChain)                 ║
║                                                                  ║
║  Combines local NPU + Ollama + GitHub cloud models for          ║
║  optimal quality/speed/cost in code generation                  ║
╚══════════════════════════════════════════════════════════════════╝
""")


def print_agent_summary():
    """Print summary of available agents."""
    print("\n📋 AGENT CONFIGURATION")
    print("=" * 60)

    for phase in Phase:
        agents = [a for a in AGENT_REGISTRY.values() if a.phase == phase]
        print(f"\n{phase.value.upper()} ({len(agents)} agents):")
        for agent in agents:
            tier_icon = {
                AgentTier.LOCAL_NPU: "⚡",  # Fast
                AgentTier.LOCAL_OLLAMA: "🏠",  # Local
                AgentTier.CLOUD_FAST: "☁️",  # Cloud fast
                AgentTier.CLOUD_STANDARD: "🌐",  # Cloud standard
                AgentTier.CLOUD_PREMIUM: "💎",  # Premium
            }.get(agent.tier, "?")
            print(f"  {tier_icon} {agent.name}: {agent.model}")


def print_cost_summary():
    """Print cost tier breakdown."""
    print("\n💰 COST TIER SUMMARY")
    print("=" * 60)

    summary = get_cost_summary()
    tier_descriptions = {
        "local_npu": "⚡ FREE - Local NPU (fastest)",
        "local_ollama": "🏠 FREE - Local Ollama",
        "cloud_fast": "☁️ LOW - Fast cloud (gpt-4.1-mini)",
        "cloud_std": "🌐 MEDIUM - Standard cloud (gpt-4.1, gpt-5-mini)",
        "cloud_premium": "💎 HIGH - Premium cloud (gpt-5, o3-mini, o4-mini)",
    }

    for tier, agents in summary.items():
        desc = tier_descriptions.get(tier, tier)
        print(f"\n{desc}:")
        for agent in agents:
            print(f"    - {agent}")


async def run_fullstack_workflow(
    requirements: str,
    project_name: str = "generated_app",
    output_dir: str = "./generated",
    verbose: bool = True,
    save_output: bool = True,
) -> dict:
    """Run the full-stack generation workflow.

    Args:
        requirements: Natural language requirements
        project_name: Name for the generated project
        output_dir: Directory to save output
        verbose: Print progress
        save_output: Save generated code to files

    Returns:
        Result dictionary
    """
    generator = HybridFullStackGenerator(
        verbose=verbose,
        use_local_fallbacks=True,
        output_dir=Path(output_dir),
    )

    result = await generator.generate(
        requirements=requirements,
        project_name=project_name,
    )

    if save_output:
        generator.save_output(result)

    return result.to_dict()


def main():
    parser = argparse.ArgumentParser(
        description="Generate full-stack applications using hybrid AI models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate from inline requirements
    python -m tools.agents.fullstack_generator.runner "Build a task management app with user auth"
    
    # Generate from requirements file
    python -m tools.agents.fullstack_generator.runner --file requirements.md
    
    # Interactive mode
    python -m tools.agents.fullstack_generator.runner --interactive
    
    # List available agents
    python -m tools.agents.fullstack_generator.runner --list-agents
        """,
    )

    parser.add_argument(
        "requirements", nargs="?", help="Requirements for the application to generate"
    )
    parser.add_argument("--file", "-f", help="Read requirements from file")
    parser.add_argument(
        "--project",
        "-p",
        default="generated_app",
        help="Project name (default: generated_app)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="./generated",
        help="Output directory (default: ./generated)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", default=True, help="Verbose output"
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Quiet mode (minimal output)"
    )
    parser.add_argument(
        "--no-save", action="store_true", help="Don't save output to files"
    )
    parser.add_argument(
        "--list-agents", action="store_true", help="List all available agents"
    )
    parser.add_argument(
        "--cost-summary", action="store_true", help="Show cost tier breakdown"
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive mode"
    )
    parser.add_argument("--json", action="store_true", help="Output result as JSON")

    args = parser.parse_args()

    # Handle info commands
    if args.list_agents:
        print_banner()
        print_agent_summary()
        return

    if args.cost_summary:
        print_banner()
        print_cost_summary()
        return

    # Get requirements
    requirements = None

    if args.requirements:
        requirements = args.requirements
    elif args.file:
        requirements = Path(args.file).read_text(encoding="utf-8")
    elif args.interactive:
        print_banner()
        print("Enter your requirements (press Enter twice to finish):\n")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        requirements = "\n".join(lines).strip()

    if not requirements:
        parser.print_help()
        print("\nError: No requirements provided. Use --help for usage.")
        sys.exit(1)

    # Print banner
    if not args.quiet:
        print_banner()
        print(f"Project: {args.project}")
        print(f"Output:  {args.output}")
        print(f"Requirements length: {len(requirements)} chars")

    # Run workflow
    verbose = args.verbose and not args.quiet

    try:
        result = asyncio.run(
            run_fullstack_workflow(
                requirements=requirements,
                project_name=args.project,
                output_dir=args.output,
                verbose=verbose,
                save_output=not args.no_save,
            )
        )

        if args.json:
            print(json.dumps(result, indent=2))
        elif not args.quiet:
            print("\n" + "=" * 60)
            print("GENERATION SUMMARY")
            print("=" * 60)
            print(f"Success: {result['success']}")
            print(f"Duration: {result['total_duration_seconds']:.1f}s")
            print(f"Models used: {len(result['models_used'])}")
            print(f"Cost breakdown: {result['cost_breakdown']}")

            if not args.no_save:
                print(f"\nOutput saved to: {args.output}/{args.project}")

    except KeyboardInterrupt:
        print("\n\nAborted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
