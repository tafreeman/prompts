"""
Hybrid Full-Stack Generator Workflow
=====================================

LangChain/LangGraph-based workflow that orchestrates multiple agents
across 4 phases to generate a complete full-stack application.
"""

import asyncio
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum

from .agents import (
    AGENT_REGISTRY,
    AgentConfig,
    AgentTier,
    Phase,
    get_agent_config,
    list_agents_by_phase,
)
from .langchain_models import HybridLLM, create_llm_from_config


@dataclass
class AgentResult:
    """Result from a single agent execution."""
    agent_id: str
    agent_name: str
    model_used: str
    phase: str
    started_at: str
    completed_at: str
    duration_seconds: float
    output: str
    success: bool
    error: Optional[str] = None
    tokens_used: int = 0
    cost_tier: str = ""


@dataclass
class PhaseResult:
    """Result from a complete phase."""
    phase: str
    started_at: str
    completed_at: str
    duration_seconds: float
    agent_results: List[AgentResult]
    combined_output: Dict[str, Any]
    success: bool


@dataclass
class FullStackResult:
    """Complete result from the full-stack generation workflow."""
    project_name: str
    started_at: str
    completed_at: str
    total_duration_seconds: float
    phases: List[PhaseResult]
    final_output: Dict[str, Any]
    success: bool
    
    # Code artifacts
    frontend_code: Dict[str, str] = field(default_factory=dict)
    backend_code: Dict[str, str] = field(default_factory=dict)
    database_code: Dict[str, str] = field(default_factory=dict)
    tests: Dict[str, str] = field(default_factory=dict)
    documentation: Dict[str, str] = field(default_factory=dict)
    
    # Metadata
    models_used: List[str] = field(default_factory=list)
    total_tokens: int = 0
    cost_breakdown: Dict[str, int] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "total_duration_seconds": self.total_duration_seconds,
            "phases": [
                {
                    "phase": p.phase,
                    "duration_seconds": p.duration_seconds,
                    "success": p.success,
                    "agents": [
                        {
                            "agent_id": a.agent_id,
                            "model": a.model_used,
                            "duration": a.duration_seconds,
                            "success": a.success,
                        }
                        for a in p.agent_results
                    ],
                }
                for p in self.phases
            ],
            "success": self.success,
            "models_used": self.models_used,
            "cost_breakdown": self.cost_breakdown,
        }


class HybridFullStackGenerator:
    """
    Multi-agent workflow for generating full-stack applications.
    
    Uses a hybrid approach combining:
    - Local NPU models for fast, free operations
    - Ollama models for local fallback/supplement
    - GitHub cloud models for premium quality
    """
    
    def __init__(
        self,
        verbose: bool = True,
        use_local_fallbacks: bool = True,
        max_parallel: int = 3,
        output_dir: Optional[Path] = None,
    ):
        self.verbose = verbose
        self.use_local_fallbacks = use_local_fallbacks
        self.max_parallel = max_parallel
        self.output_dir = output_dir or Path("./generated")
        
        # Initialize LLMs for each agent
        self.llms: Dict[str, HybridLLM] = {}
        self._init_llms()
        
        # Track results
        self.results: Dict[str, AgentResult] = {}
        self.phase_outputs: Dict[str, Any] = {}
    
    def _init_llms(self):
        """Initialize LLM instances for all agents."""
        for agent_id, config in AGENT_REGISTRY.items():
            fallback = config.fallback_model if self.use_local_fallbacks else None
            self.llms[agent_id] = create_llm_from_config(
                model=config.model,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                fallback_model=fallback,
            )
    
    def _log(self, message: str, indent: int = 0):
        """Log message if verbose."""
        if self.verbose:
            prefix = "  " * indent
            print(f"{prefix}{message}")
    
    async def _run_agent(
        self,
        agent_id: str,
        context: Dict[str, Any],
    ) -> AgentResult:
        """Run a single agent with context."""
        config = AGENT_REGISTRY[agent_id]
        llm = self.llms[agent_id]
        
        self._log(f"[{config.name}] Starting ({config.model})...", indent=1)
        
        start_time = datetime.now()
        started_at = start_time.isoformat()
        
        # Build prompt with context
        prompt = self._build_agent_prompt(config, context)
        
        try:
            # Run LLM
            output = await asyncio.to_thread(
                llm._call,
                prompt,
                system_instruction=config.system_prompt,
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self._log(f"[{config.name}] Completed in {duration:.1f}s", indent=1)
            
            return AgentResult(
                agent_id=agent_id,
                agent_name=config.name,
                model_used=config.model,
                phase=config.phase.value,
                started_at=started_at,
                completed_at=end_time.isoformat(),
                duration_seconds=duration,
                output=output,
                success=True,
                cost_tier=config.tier.value,
            )
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self._log(f"[{config.name}] Failed: {e}", indent=1)
            
            return AgentResult(
                agent_id=agent_id,
                agent_name=config.name,
                model_used=config.model,
                phase=config.phase.value,
                started_at=started_at,
                completed_at=end_time.isoformat(),
                duration_seconds=duration,
                output="",
                success=False,
                error=str(e),
                cost_tier=config.tier.value,
            )
    
    def _build_agent_prompt(
        self,
        config: AgentConfig,
        context: Dict[str, Any],
    ) -> str:
        """Build prompt for agent with context."""
        parts = []
        
        # Add relevant context
        if "requirements" in context:
            parts.append(f"## REQUIREMENTS\n{context['requirements']}")
        
        if "mockups" in context:
            parts.append(f"## UI MOCKUPS\n{context['mockups']}")
        
        if "previous_outputs" in context:
            parts.append("## PREVIOUS PHASE OUTPUTS")
            for key, value in context["previous_outputs"].items():
                if isinstance(value, str):
                    parts.append(f"### {key}\n{value[:2000]}...")
                else:
                    parts.append(f"### {key}\n{json.dumps(value, indent=2)[:2000]}...")
        
        parts.append(f"## YOUR TASK\n{config.role}")
        parts.append(f"\n## EXPECTED OUTPUT FORMAT\n{config.output_format}")
        
        return "\n\n".join(parts)
    
    async def _run_phase(
        self,
        phase: Phase,
        context: Dict[str, Any],
        parallel_agents: Optional[List[str]] = None,
        sequential_agents: Optional[List[str]] = None,
    ) -> PhaseResult:
        """Run a complete phase."""
        self._log(f"\n{'='*60}")
        self._log(f"PHASE: {phase.value.upper()}")
        self._log(f"{'='*60}")
        
        start_time = datetime.now()
        agent_results: List[AgentResult] = []
        
        # Run parallel agents
        if parallel_agents:
            self._log(f"Running {len(parallel_agents)} agents in parallel...")
            tasks = [
                self._run_agent(agent_id, context)
                for agent_id in parallel_agents
            ]
            parallel_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in parallel_results:
                if isinstance(result, AgentResult):
                    agent_results.append(result)
                    self.results[result.agent_id] = result
        
        # Update context with parallel results
        for result in agent_results:
            if result.success:
                context.setdefault("previous_outputs", {})[result.agent_id] = result.output
        
        # Run sequential agents
        if sequential_agents:
            for agent_id in sequential_agents:
                result = await self._run_agent(agent_id, context)
                agent_results.append(result)
                self.results[result.agent_id] = result
                
                if result.success:
                    context.setdefault("previous_outputs", {})[result.agent_id] = result.output
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Combine outputs
        combined = {
            r.agent_id: r.output
            for r in agent_results
            if r.success
        }
        
        success = all(r.success for r in agent_results)
        
        self._log(f"\nPhase {phase.value} completed in {duration:.1f}s")
        self._log(f"Success: {sum(1 for r in agent_results if r.success)}/{len(agent_results)} agents")
        
        return PhaseResult(
            phase=phase.value,
            started_at=start_time.isoformat(),
            completed_at=end_time.isoformat(),
            duration_seconds=duration,
            agent_results=agent_results,
            combined_output=combined,
            success=success,
        )
    
    async def generate(
        self,
        requirements: str,
        mockups: Optional[str] = None,
        project_name: str = "fullstack_app",
    ) -> FullStackResult:
        """
        Generate a complete full-stack application.
        
        Args:
            requirements: Natural language requirements
            mockups: Optional UI mockup descriptions or paths
            project_name: Name for the generated project
        
        Returns:
            FullStackResult with all generated code and artifacts
        """
        self._log(f"\n{'#'*60}")
        self._log(f"HYBRID FULL-STACK GENERATOR")
        self._log(f"Project: {project_name}")
        self._log(f"{'#'*60}")
        
        start_time = datetime.now()
        phases: List[PhaseResult] = []
        context = {
            "requirements": requirements,
            "mockups": mockups or "No mockups provided",
            "project_name": project_name,
        }
        
        # =================================================================
        # PHASE 1: Requirements Analysis
        # =================================================================
        phase1 = await self._run_phase(
            Phase.REQUIREMENTS,
            context,
            parallel_agents=["requirements_analyzer", "domain_modeler"],
            sequential_agents=["technical_planner"],
        )
        phases.append(phase1)
        context["previous_outputs"] = phase1.combined_output
        
        # =================================================================
        # PHASE 2: System Design
        # =================================================================
        phase2 = await self._run_phase(
            Phase.DESIGN,
            context,
            parallel_agents=["database_architect", "api_designer", "security_architect"],
            sequential_agents=["system_architect"],
        )
        phases.append(phase2)
        context["previous_outputs"].update(phase2.combined_output)
        
        # =================================================================
        # PHASE 3: Code Generation
        # =================================================================
        phase3 = await self._run_phase(
            Phase.CODEGEN,
            context,
            parallel_agents=["frontend_generator", "database_generator"],
            sequential_agents=["backend_generator"],
        )
        phases.append(phase3)
        context["previous_outputs"].update(phase3.combined_output)
        
        # =================================================================
        # PHASE 4: Quality Assurance
        # =================================================================
        phase4 = await self._run_phase(
            Phase.QA,
            context,
            parallel_agents=["test_generator", "documentation_writer"],
            sequential_agents=["code_reviewer", "performance_auditor"],
        )
        phases.append(phase4)
        
        # Compile final result
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        # Extract code artifacts
        frontend_code = self._extract_code(phase3.combined_output.get("frontend_generator", ""))
        backend_code = self._extract_code(phase3.combined_output.get("backend_generator", ""))
        database_code = self._extract_code(phase3.combined_output.get("database_generator", ""))
        tests = self._extract_code(phase4.combined_output.get("test_generator", ""))
        docs = {"README.md": phase4.combined_output.get("documentation_writer", "")}
        
        # Calculate cost breakdown
        cost_breakdown = {}
        models_used = set()
        for result in self.results.values():
            models_used.add(result.model_used)
            tier = result.cost_tier
            cost_breakdown[tier] = cost_breakdown.get(tier, 0) + 1
        
        result = FullStackResult(
            project_name=project_name,
            started_at=start_time.isoformat(),
            completed_at=end_time.isoformat(),
            total_duration_seconds=total_duration,
            phases=phases,
            final_output=context["previous_outputs"],
            success=all(p.success for p in phases),
            frontend_code=frontend_code,
            backend_code=backend_code,
            database_code=database_code,
            tests=tests,
            documentation=docs,
            models_used=list(models_used),
            cost_breakdown=cost_breakdown,
        )
        
        self._log(f"\n{'#'*60}")
        self._log(f"GENERATION COMPLETE")
        self._log(f"Total time: {total_duration:.1f}s")
        self._log(f"Success: {result.success}")
        self._log(f"Models used: {len(models_used)}")
        self._log(f"{'#'*60}")
        
        return result
    
    def _extract_code(self, output: str) -> Dict[str, str]:
        """Extract code blocks from output."""
        import re
        
        code_files = {}
        
        # Find code blocks with filenames
        pattern = r'```(\w+)?\s*(?:#\s*)?(\S+\.\w+)?\n(.*?)```'
        matches = re.findall(pattern, output, re.DOTALL)
        
        for i, (lang, filename, code) in enumerate(matches):
            if filename:
                code_files[filename] = code.strip()
            elif lang:
                ext = {"python": "py", "javascript": "js", "typescript": "ts", "sql": "sql"}.get(lang, lang)
                code_files[f"code_{i}.{ext}"] = code.strip()
        
        return code_files
    
    def save_output(self, result: FullStackResult, output_dir: Optional[Path] = None):
        """Save generated code to files."""
        output_dir = output_dir or self.output_dir / result.project_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save frontend
        frontend_dir = output_dir / "frontend" / "src"
        frontend_dir.mkdir(parents=True, exist_ok=True)
        for filename, code in result.frontend_code.items():
            (frontend_dir / filename).write_text(code, encoding="utf-8")
        
        # Save backend
        backend_dir = output_dir / "backend" / "src"
        backend_dir.mkdir(parents=True, exist_ok=True)
        for filename, code in result.backend_code.items():
            (backend_dir / filename).write_text(code, encoding="utf-8")
        
        # Save database
        db_dir = output_dir / "database"
        db_dir.mkdir(parents=True, exist_ok=True)
        for filename, code in result.database_code.items():
            (db_dir / filename).write_text(code, encoding="utf-8")
        
        # Save tests
        tests_dir = output_dir / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)
        for filename, code in result.tests.items():
            (tests_dir / filename).write_text(code, encoding="utf-8")
        
        # Save docs
        for filename, content in result.documentation.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
        
        # Save workflow result
        result_file = output_dir / "generation_result.json"
        result_file.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
        
        self._log(f"\nOutput saved to: {output_dir}")
        return output_dir
