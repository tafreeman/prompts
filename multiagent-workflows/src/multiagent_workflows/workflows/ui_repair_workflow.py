from __future__ import annotations

from typing import List

from tools.llm.langchain_adapter import LangChainAdapter

from multiagent_workflows.agents.coder_agent import CoderAgent
from multiagent_workflows.core.agent_base import AgentConfig, SimpleAgent
from multiagent_workflows.workflows.base import BaseWorkflow, WorkflowStep


class UiRepairWorkflow(BaseWorkflow):
    """Workflow to diagnose and repair UI issues using existing agents."""

    name = "ui_repair"
    description = "Diagnose and repair UI issues."

    def define_steps(self) -> List[WorkflowStep]:
        return [
            WorkflowStep(
                name="diagnosis",
                agent="bug_analyst",
                description="Analyze the UI code and identiy why evaluations are not shown.",
                required_inputs=["file_content", "issue_description"],
                outputs=["diagnosis"],
            ),
            WorkflowStep(
                name="planning",
                agent="architect",
                description="Plan the necessary code changes.",
                required_inputs=["diagnosis"],
                outputs=["plan"],
            ),
            WorkflowStep(
                name="coding",
                agent="coder",
                description="Apply the fix to the code.",
                required_inputs=["file_content", "plan"],
                outputs=["code", "files"],
            ),
        ]

    @property
    def step_dependencies(self):
        return {
            "diagnosis": [],
            "planning": ["diagnosis"],
            "coding": ["planning"],
        }

    async def _create_agent(self, step: WorkflowStep):
        # Configuration for agents
        agent_details = {
            "bug_analyst": {
                "class": SimpleAgent,
                "prompt": (
                    "You are a Senior Bug Analyst. Analyze the provided file content and issue description. "
                    "Identify explicitly why the reported feature (evaluations) is missing or broken. "
                    "Locate the specific functions or HTML sections that need modification. "
                    "Output a JSON object with a key 'diagnosis' containing your analysis."
                ),
            },
            "architect": {
                "class": SimpleAgent,
                "prompt": (
                    "You are a System Architect. Based on the diagnosis, create a detailed plan to fix the code. "
                    "Specify exactly what functions to modify and how. "
                    "Output a JSON object with a key 'plan' containing the implementation plan."
                ),
            },
            "coder": {
                "class": CoderAgent,
                "prompt": (
                    "You are a Senior Frontend Developer. Apply the fixes described in the plan to the provided file content. "
                    "Ensure you preserve the existing code structure and only apply the necessary changes. "
                    "Generate the full updated file content. "
                    "Output a JSON object with keys: 'code', 'files'."
                ),
            },
        }

        details = agent_details.get(step.agent)
        if not details:
            return None

        agent_class = details["class"]
        system_prompt = details["prompt"]

        # Use a strong model for coding
        model_id = self.model_manager.get_optimal_model(
            "code_gen" if step.agent == "coder" else "reasoning", complexity=7
        )

        config = AgentConfig(
            name=step.agent.title(),
            role=step.description,
            model_id=model_id,
            system_prompt=system_prompt,
        )
        setattr(config, "langchain_adapter", LangChainAdapter(config.model_id))

        if agent_class == SimpleAgent:
            # Pass inputs into prompt context
            return SimpleAgent(
                config=config,
                model_manager=self.model_manager,
                tool_registry=self.tool_registry,
                logger=self.logger,
                prompt_template=f"Task: {{task}}\n\nContext:\n{{context}}\n\n{system_prompt}",
            )
        elif agent_class == CoderAgent:
            # CoderAgent constructs its own prompt, but we can override or subclass if needed.
            # Standard CoderAgent uses "specification" from task.
            # We map inputs to "specification" in _execute_step or rely on CoderAgent to read context.
            # CoderAgent reads "architecture" and "api_spec" from context['artifacts'].
            # We need to ensure 'plan' is passed nicely.
            # We will rely on CoderAgent being smart enough or modify how we call it?
            # Actually CoderAgent._process uses task.get("specification").
            # BaseWorkflow._execute_step passes step_inputs to agent.execute(step_inputs, ...).
            # SimpleAgent wraps this. CoderAgent inherits AgentBase.
            # AgentBase.execute calls _process(task, context).
            # So step_inputs == task.
            # So we need to map 'plan' and 'file_content' to 'specification' for CoderAgent to see it.
            # Or we can customize CoderAgent usage here.
            # For simplicity, we'll let CoderAgent see "plan" if it's in the input dict.
            # But standard CoderAgent prompt builder checks 'specification'.

            # We'll create a custom instance that maps inputs
            return CoderAgent(
                config=config,
                model_manager=self.model_manager,
                tool_registry=self.tool_registry,
                logger=self.logger,
            )
        return None

    async def _execute_step(self, step, context):
        # Override to map inputs for CoderAgent
        if step.agent == "coder":
            inputs = {}
            # Get plan and file content
            plan = context.artifacts.get("plan", "")
            content = context.inputs.get("file_content", "")

            # Construct specification for CoderAgent
            inputs["specification"] = (
                f"We need to fix the UI code.\n\n"
                f"## PLAN\n{plan}\n\n"
                f"## CURRENT FILE CONTENT (ui/index.html)\n"
                f"```html\n{content}\n```\n"
                f"Please generate the fully corrected index.html file."
            )
            inputs["language"] = "html"
            inputs["framework"] = "vanilla"
            inputs["output_type"] = "frontend"

            agent = await self._create_agent(step)
            result = await agent.execute(inputs, {"artifacts": context.artifacts})
            if result.success:
                return result.output
            else:
                raise RuntimeError(f"Step {step.name} failed: {result.error}")

        return await super()._execute_step(step, context)
