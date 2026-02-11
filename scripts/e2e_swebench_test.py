import asyncio
import os
import sys
from pathlib import Path

# Setup paths
REPO_ROOT = Path(__file__).parents[1].resolve()
EVAL_SRC = (REPO_ROOT / "agentic-v2-eval" / "src").resolve()
WORKFLOWS_SRC = (REPO_ROOT / "agentic-workflows-v2" / "src").resolve()

# Add to sys.path
if str(EVAL_SRC) not in sys.path:
    sys.path.insert(0, str(EVAL_SRC))
if str(WORKFLOWS_SRC) not in sys.path:
    # This might conflict if agentic_v2 is installed, but useful for dev
    sys.path.insert(0, str(WORKFLOWS_SRC))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Enable logging
import logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

def load_env_file():

    """Load .env file from current or parent directories."""
    current = Path(__file__).resolve()
    for _ in range(5):  # Look up 5 levels
        env_path = current.parent / ".env"
        if env_path.exists():
            print(f"📄 Found .env at: {env_path}")
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip()
                            if key and value and not os.environ.get(key):
                                os.environ[key] = value
                                # Mask token in output
                                masked = value[:4] + "***" if len(value) > 4 else "***"
                                if key == "GITHUB_TOKEN":
                                    print(f"   🔑 Loaded {key}")
            except Exception as e:
                print(f"   ⚠️ Failed to load .env: {e}")
            return
        current = current.parent

load_env_file()

# Imports
try:
    from agentic_v2_eval.datasets import load_benchmark
    from agentic_v2.agents.orchestrator import OrchestratorAgent, OrchestratorInput
    from agentic_v2.agents.coder import CoderAgent
    from agentic_v2.agents.reviewer import ReviewerAgent
    from agentic_v2.agents.capabilities import TestGenerationMixin
    from agentic_v2.contracts import StepStatus
    from agentic_v2_eval.evaluators.quality import QualityEvaluator, RELEVANCE, COHERENCE
    from agentic_v2_eval.adapters.llm_client import LLMClientAdapter
    # Import LLMClient from tools
    from tools.llm.llm_client import LLMClient
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Define RealAgentMixin to use LLMClient
class RealAgentMixin:
    async def _call_model(self, messages, tools=None):
        """Override to use real LLM."""
        system_prompt = None
        user_content = []
        
        for m in messages:
            if m.get('role') == 'system':
                system_prompt = m.get('content')
            else:
                # Basic chat-to-text conversion
                user_content.append(f"{m.get('role').upper()}: {m.get('content')}")
        
        prompt = "\n\n".join(user_content)
        
        # Use simple model selection
        model = os.environ.get("AGENT_TIER_3_MODEL", "gh:gpt-4o")
        os.environ["PROMPTEVAL_ALLOW_REMOTE"] = "1"
        
        try:
            # Run in executor since LLMClient is synchronous
            loop = asyncio.get_running_loop()
            response_text = await loop.run_in_executor(
                None, 
                lambda: LLMClient.generate_text(
                    model,
                    prompt,
                    system_instruction=system_prompt,
                    temperature=0.1
                )
            )
            # print(f"DEBUG: LLM Response ({self.__class__.__name__}):\n{response_text[:200]}...\n")
            return {"content": response_text}
        except Exception as e:
            logging.error(f"LLM Call failed for {self.__class__.__name__}: {e}")
            raise

class RealCoderAgent(RealAgentMixin, CoderAgent, TestGenerationMixin):
    """CoderAgent with real LLM and Test capabilities."""
    pass

class RealReviewerAgent(RealAgentMixin, ReviewerAgent):
    """ReviewerAgent with real LLM."""
    pass

# Define a real orchestrator that uses LLMClient
class RealOrchestratorAgent(RealAgentMixin, OrchestratorAgent):
    pass

async def run_e2e_test():
    print("\n=== 1. Loading Benchmark (SWE-bench Lite) ===")
    try:
        tasks = load_benchmark("swe-bench-lite", limit=1)
        if not tasks:
            print("❌ No tasks found.")
            return
        task = tasks[0]
        print(f"✅ Loaded task: {task.task_id}")
        print(f"   Repo: {task.repo}")
        print(f"   Problem: {task.prompt[:100]}...")
    except Exception as e:
        print(f"❌ Failed to load benchmark: {e}")
        return

    print("\n=== 2. Running Orchestrator ===")
    try:
        if not os.environ.get("GITHUB_TOKEN"):
             print("⚠️  Warning: GITHUB_TOKEN not found. Execution likely to fail.")

        # Initialize sub-agents
        print("   Initializing sub-agents...")
        coder = RealCoderAgent()
        reviewer = RealReviewerAgent()
        
        # Use our Real Orchestrator
        orchestrator = RealOrchestratorAgent(agents={
            "coder": coder, 
            "reviewer": reviewer
        })
        # Manually register to ensure capabilities are picked up
        orchestrator.register_agent("coder", coder)
        orchestrator.register_agent("reviewer", reviewer)
        
        # Construct the task input
        input_desc = f"Fix the following issue in repository {task.repo}:\n\n{task.prompt}"
        
        print(f"🚀 Initialized Orchestrator. executing task...")
        
        # Force a strong model for orchestration if not set
        if not os.environ.get("AGENT_TIER_3_MODEL"):
             os.environ["AGENT_TIER_3_MODEL"] = "gh:gpt-4o"
             print("   Set AGENT_TIER_3_MODEL = gh:gpt-4o")

        # Run!
        result = await orchestrator.execute_as_dag(OrchestratorInput(task=input_desc))
        
        print(f"✅ Execution Complete. Status: {result.overall_status}")
        print(f"   Steps taken: {len(result.steps)}")
        
        # Extract output for evaluation
        steps_text = []
        for s in result.steps:
             content = "No Output"
             # output_data is a dict from the step function, e.g. {"result": <TaskOutput>}
             if s.output_data:
                 result_obj = s.output_data.get("result")
                 if result_obj is not None:
                     if hasattr(result_obj, "code") and result_obj.code:
                         content = result_obj.code
                     elif hasattr(result_obj, "summary") and result_obj.summary:
                         content = result_obj.summary
                     elif hasattr(result_obj, "model_dump"):
                         content = str(result_obj.model_dump())
                     else:
                         content = str(result_obj)
                 else:
                     content = str(s.output_data)
             
             # truncate if too long
             if len(content) > 1000:
                 content = content[:1000] + "...[truncated]"
             steps_text.append(f"Step '{s.step_name}' ({s.status}):\n{content}")
             
             if s.status == StepStatus.FAILED:
                 print(f"   FAILED Step '{s.step_name}': {s.error}")
         
        output_text = "\n\n".join(steps_text)
        if not output_text:
             output_text = "No output generated from steps."
        
        print(f"   Output length: {len(output_text)} chars")
        print(f"   Full Output:\n{output_text}")

    except Exception as e:
        print(f"❌ Execution failed: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\n=== 3. Evaluating Result (LLM-as-Judge) ===")
    try:
        # Initialize evaluator with adapter
        # Using gpt-4o for evaluation excellence, falling back to 4o-mini if needed
        adapter = LLMClientAdapter(default_model="gh:gpt-4o")
        evaluator = QualityEvaluator(llm_client=adapter)
        
        # Evaluate Relevance
        print("   Evaluating Relevance...")
        rel_score = evaluator.evaluate(
            definition=RELEVANCE,
            inputs={"input": input_desc},
            output=output_text
        )
        print(f"   Relevance Score: {rel_score}/5")
        
        # Evaluate Coherence
        print("   Evaluating Coherence...")
        coh_score = evaluator.evaluate(
            definition=COHERENCE,
            inputs={"input": input_desc}, 
            output=output_text
        )
        print(f"   Coherence Score: {coh_score}/5")
        
        # Result Summary
        if rel_score >= 3 and coh_score >= 3:
            print("\n✅ E2E Test PASSED (Scores >= 3)")
        else:
            print(f"\n⚠️ E2E Test FAILED or INCONCLUSIVE (Relevance: {rel_score}, Coherence: {coh_score})")

    except Exception as e:
        print(f"❌ Evaluation failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_e2e_test())
