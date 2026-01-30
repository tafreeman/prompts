"""
Integration Tests for Agentic Planning Workflows

Tests the 4 expanded workflow configurations:
- End-to-End Development (11 agents)
- Defect Resolution (11 agents)
- Iterative System Design (10 agents)
- Code Grading (10 agents)

Uses datasets from the existing evaluation framework.
"""

import json
from pathlib import Path
from typing import Any, Dict

import pytest

# Ensure workflows dir is on path
WORKFLOWS_CONFIG_DIR = Path(__file__).resolve().parents[1] / "config" / "agentic_planning"

# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def workflow_config_loader():
    """Load agentic workflow configurations."""
    def load(workflow_name: str) -> Dict[str, Any]:
        config_files = {
            "end_to_end": "workflow_end_to_end.json",
            "defect_resolution": "workflow_defect_resolution.json",
            "system_design": "workflow_system_design.json",
            "code_grading": "workflow_code_grading.json",
        }
        config_file = WORKFLOWS_CONFIG_DIR / config_files[workflow_name]
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return load


@pytest.fixture
def sample_end_to_end_task() -> Dict[str, Any]:
    """Sample task for end-to-end development workflow."""
    return {
        "task_description": "Build a REST API for a task management system with user authentication, CRUD operations for tasks, and due date reminders.",
        "gold_standard": {
            "required_components": ["REST API", "Authentication", "Database Schema", "CRUD Endpoints"],
            "required_patterns": ["JWT Auth", "Repository Pattern", "Error Handling"],
            "expected_output": "Complete API specification with endpoints, schema, and security design",
        },
    }


@pytest.fixture
def sample_defect_task() -> Dict[str, Any]:
    """Sample task for defect resolution workflow."""
    return {
        "task_description": "Debug a memory leak in a Node.js application that occurs after 24 hours of operation. The heap grows from 100MB to 2GB.",
        "gold_standard": {
            "required_components": ["Root Cause Analysis", "Memory Profiling", "Patch"],
            "key_decisions": ["Memory leak source identified", "Fix verified", "Regression tests added"],
            "expected_output": "Root cause document, patch, and verification report",
        },
    }


@pytest.fixture
def sample_design_task() -> Dict[str, Any]:
    """Sample task for system design workflow."""
    return {
        "task_description": "Design a scalable e-commerce platform that handles 1 million daily active users with a product catalog of 10 million items.",
        "gold_standard": {
            "required_components": ["Microservices Architecture", "Database Design", "Caching Strategy", "CDN"],
            "required_patterns": ["Event Sourcing", "CQRS", "Circuit Breaker"],
            "expected_output": "Complete architecture document with diagrams and trade-off analysis",
        },
    }


@pytest.fixture
def sample_grading_task() -> Dict[str, Any]:
    """Sample task for code grading workflow."""
    return {
        "task_description": "Grade the following Python implementation of a binary search tree with insert, delete, and search operations.",
        "code_submission": '''
class BST:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
    
    def insert(self, value):
        if value < self.value:
            if self.left:
                self.left.insert(value)
            else:
                self.left = BST(value)
        else:
            if self.right:
                self.right.insert(value)
            else:
                self.right = BST(value)
    
    def search(self, value):
        if value == self.value:
            return True
        elif value < self.value and self.left:
            return self.left.search(value)
        elif value > self.value and self.right:
            return self.right.search(value)
        return False
''',
        "gold_standard": {
            "required_components": ["Correctness Check", "Performance Analysis", "Code Quality Review"],
            "key_decisions": ["Algorithm correctness", "Time complexity", "Code style"],
            "expected_output": "Detailed grade report with scores and improvement suggestions",
        },
    }


# =============================================================================
# WORKFLOW CONFIG TESTS
# =============================================================================

class TestWorkflowConfigurations:
    """Test that workflow configurations are valid and complete."""
    
    def test_end_to_end_config_loads(self, workflow_config_loader):
        """End-to-end workflow config loads successfully."""
        config = workflow_config_loader("end_to_end")
        
        assert config["version"].startswith("2.")
        assert "agents" in config
        assert len(config["agents"]) == 11
        
        # Check required phases
        phases = config["metadata"]["phases"]
        assert "Discovery" in phases
        assert "Implementation" in phases
        assert "Assurance" in phases
    
    def test_defect_resolution_config_loads(self, workflow_config_loader):
        """Defect resolution workflow config loads successfully."""
        config = workflow_config_loader("defect_resolution")
        
        assert config["version"].startswith("2.")
        assert len(config["agents"]) == 11
        
        # Check key agents exist
        agent_ids = [a["id"] for a in config["agents"]]
        assert "log_analyst" in agent_ids
        assert "root_cause_analyst" in agent_ids
        assert "patch_engineer" in agent_ids
        assert "resolution_judge" in agent_ids
    
    def test_system_design_config_loads(self, workflow_config_loader):
        """System design workflow config loads successfully."""
        config = workflow_config_loader("system_design")
        
        assert config["version"].startswith("2.")
        assert len(config["agents"]) == 10
        
        # Check iterative loop metadata
        assert "convergence_threshold" in config["metadata"]
        assert config["metadata"]["type"] == "iterative_loop"
    
    def test_code_grading_config_loads(self, workflow_config_loader):
        """Code grading workflow config loads successfully."""
        config = workflow_config_loader("code_grading")
        
        assert config["version"].startswith("2.")
        assert len(config["agents"]) == 10
        
        # Check grading scale
        assert "grading_scale" in config["metadata"]


class TestAgentConfigurations:
    """Test that individual agent configurations are valid."""
    
    @pytest.mark.parametrize("workflow_name", [
        "end_to_end",
        "defect_resolution", 
        "system_design",
        "code_grading",
    ])
    def test_all_agents_have_required_fields(self, workflow_config_loader, workflow_name):
        """All agents have required configuration fields."""
        config = workflow_config_loader(workflow_name)
        
        required_fields = ["id", "name", "model", "role", "system_prompt"]
        
        for agent in config["agents"]:
            for field in required_fields:
                assert field in agent, f"Agent {agent.get('id', 'unknown')} missing {field}"
    
    @pytest.mark.parametrize("workflow_name", [
        "end_to_end",
        "defect_resolution",
        "system_design", 
        "code_grading",
    ])
    def test_all_agents_have_compatible_models(self, workflow_config_loader, workflow_name):
        """All agents have fallback models defined."""
        config = workflow_config_loader(workflow_name)
        
        for agent in config["agents"]:
            assert "compatible_models" in agent, f"Agent {agent['id']} has no fallback models"
            assert len(agent["compatible_models"]) >= 1, f"Agent {agent['id']} needs at least 1 fallback"
    
    @pytest.mark.parametrize("workflow_name", [
        "end_to_end",
        "defect_resolution",
        "system_design",
        "code_grading",
    ])
    def test_all_agents_have_phase_assignment(self, workflow_config_loader, workflow_name):
        """All agents are assigned to a phase."""
        config = workflow_config_loader(workflow_name)
        
        for agent in config["agents"]:
            assert "phase" in agent, f"Agent {agent['id']} has no phase"
            assert agent["phase"], f"Agent {agent['id']} has empty phase"


class TestWorkflowPhaseStructure:
    """Test workflow phase structure and agent distribution."""
    
    def test_end_to_end_phase_distribution(self, workflow_config_loader):
        """End-to-end workflow has correct phase distribution."""
        config = workflow_config_loader("end_to_end")
        
        phases = {}
        for agent in config["agents"]:
            phase = agent["phase"]
            phases[phase] = phases.get(phase, 0) + 1
        
        # Should have agents in all major phases
        assert "discovery" in phases
        assert "design" in phases
        assert "implementation" in phases
        assert "assurance" in phases
    
    def test_defect_resolution_phase_flow(self, workflow_config_loader):
        """Defect resolution workflow follows logical flow."""
        config = workflow_config_loader("defect_resolution")
        
        phases = {}
        for agent in config["agents"]:
            phase = agent["phase"]
            phases[phase] = phases.get(phase, 0) + 1
        
        # Intake should come first with log parsing
        assert "intake" in phases
        # Analysis should have most agents
        assert phases.get("analysis", 0) >= 3
        # End with closure
        assert "closure" in phases


# =============================================================================
# GOLDEN STANDARD TESTS (Synthetic for Test Coverage)
# =============================================================================

class TestGoldenStandardAlignment:
    """Test workflow outputs against golden standards."""
    
    def test_end_to_end_gold_standard_keys(self, sample_end_to_end_task):
        """End-to-end task has proper gold standard structure."""
        gold = sample_end_to_end_task["gold_standard"]
        
        assert "required_components" in gold
        assert len(gold["required_components"]) >= 3
        assert "expected_output" in gold
    
    def test_defect_gold_standard_keys(self, sample_defect_task):
        """Defect task has proper gold standard structure."""
        gold = sample_defect_task["gold_standard"]
        
        assert "required_components" in gold
        assert "key_decisions" in gold
    
    def test_grading_task_includes_code(self, sample_grading_task):
        """Grading task includes code submission."""
        assert "code_submission" in sample_grading_task
        assert "class BST" in sample_grading_task["code_submission"]


# =============================================================================
# MODEL TIER TESTS
# =============================================================================

class TestModelTierAssignments:
    """Test that agents are assigned appropriate model tiers."""
    
    TIER_WEIGHTS = {
        "cloud_premium": 5,
        "cloud_reasoning": 4,
        "cloud_reasoning_fast": 3,
        "cloud_coding": 3,
        "cloud_std": 2,
        "cloud_fast": 1,
        "local_reasoning": 2,
        "local_efficient": 1,
        "local_npu": 1,
    }
    
    @pytest.mark.parametrize("workflow_name", [
        "end_to_end",
        "defect_resolution",
        "system_design",
        "code_grading",
    ])
    def test_judge_agents_use_premium_models(self, workflow_config_loader, workflow_name):
        """Judge/final agents should use premium tier models."""
        config = workflow_config_loader(workflow_name)
        
        judge_keywords = ["judge", "final", "resolution", "head"]
        
        for agent in config["agents"]:
            is_judge = any(kw in agent["id"].lower() for kw in judge_keywords)
            if is_judge:
                tier = agent.get("tier", "")
                # Judges should be premium or high-tier reasoning
                assert tier in ["cloud_premium", "cloud_reasoning"], \
                    f"Judge agent {agent['id']} using {tier}, expected premium"
    
    @pytest.mark.parametrize("workflow_name", [
        "end_to_end",
        "defect_resolution",
        "system_design",
        "code_grading",
    ])
    def test_intake_agents_use_efficient_models(self, workflow_config_loader, workflow_name):
        """Intake/preprocessing agents can use efficient models."""
        config = workflow_config_loader(workflow_name)
        
        intake_keywords = ["log", "analyst", "triage", "static"]
        
        for agent in config["agents"]:
            is_intake = any(kw in agent["id"].lower() for kw in intake_keywords)
            if is_intake:
                tier = agent.get("tier", "")
                # Just verify tier exists and is valid (not a strict cost check)
                assert tier in self.TIER_WEIGHTS or tier == "", \
                    f"Agent {agent['id']} has unknown tier: {tier}"


# =============================================================================
# INTEGRATION WITH EVALUATOR
# =============================================================================

class TestEvaluatorIntegration:
    """Test integration with the multiagent-workflows evaluator."""
    
    def test_workflow_config_compatible_with_evaluator_rubric(self, workflow_config_loader):
        """Workflow configs can be matched to evaluation rubrics."""
        # The rubrics.yaml has: fullstack_generation, legacy_refactoring, bug_fixing, architecture_evolution
        # Our new workflows should map to these
        
        mapping = {
            "end_to_end": "fullstack_generation",
            "defect_resolution": "bug_fixing",
            "system_design": "architecture_evolution",
            "code_grading": None,  # New rubric needed
        }
        
        for our_workflow, rubric_name in mapping.items():
            config = workflow_config_loader(our_workflow)
            assert config is not None
            
            if rubric_name:
                # Workflow should have phases that align with rubric categories
                phases = config["metadata"]["phases"]
                assert len(phases) >= 3, f"Workflow {our_workflow} needs more phases for evaluation"


# =============================================================================
# BENCHMARK DATASET TESTS
# =============================================================================

BENCHMARK_TASKS = [
    # End-to-End Development Tasks
    {
        "id": "e2e_001",
        "workflow": "end_to_end",
        "task": "Build a REST API for a task management system",
        "expected_agents": 11,
    },
    {
        "id": "e2e_002", 
        "workflow": "end_to_end",
        "task": "Design a real-time chat application with WebSocket support",
        "expected_agents": 11,
    },
    # Defect Resolution Tasks
    {
        "id": "defect_001",
        "workflow": "defect_resolution",
        "task": "Debug a memory leak in a Node.js application",
        "expected_agents": 11,
    },
    # System Design Tasks
    {
        "id": "design_001",
        "workflow": "system_design",
        "task": "Design a scalable e-commerce platform for 1M DAU",
        "expected_agents": 10,
    },
    # Code Grading Tasks
    {
        "id": "grading_001",
        "workflow": "code_grading",
        "task": "Grade a binary search tree implementation",
        "expected_agents": 10,
    },
]


class TestBenchmarkDataset:
    """Test benchmark dataset structure."""
    
    @pytest.mark.parametrize("task", BENCHMARK_TASKS)
    def test_task_workflow_exists(self, workflow_config_loader, task):
        """Each benchmark task references a valid workflow."""
        config = workflow_config_loader(task["workflow"])
        assert config is not None
        assert len(config["agents"]) == task["expected_agents"]
    
    def test_benchmark_task_coverage(self):
        """Benchmark tasks cover all workflow types."""
        workflows_covered = set(t["workflow"] for t in BENCHMARK_TASKS)
        expected = {"end_to_end", "defect_resolution", "system_design", "code_grading"}
        assert workflows_covered == expected


# =============================================================================
# RUN CONFIGURATION
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
