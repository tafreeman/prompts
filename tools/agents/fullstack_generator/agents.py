"""
Agent Registry for Hybrid Full-Stack Generator
===============================================

Defines all agents with their models, roles, and configurations
organized by phase and cost tier.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class AgentTier(Enum):
    """Cost/quality tier for agents."""
    LOCAL_NPU = "local_npu"      # Free, fastest (phi4mini, phi3.5-vision)
    LOCAL_OLLAMA = "local_ollama" # Free, fast (qwen2.5-coder, deepseek-r1)
    CLOUD_FAST = "cloud_fast"    # Low cost (gpt-4.1-mini, gpt-4.1-nano)
    CLOUD_STANDARD = "cloud_std" # Medium cost (gpt-4.1, gpt-5-mini)
    CLOUD_PREMIUM = "cloud_premium" # High cost (gpt-5, o3-mini, o4-mini)


class Phase(Enum):
    """Workflow phases."""
    REQUIREMENTS = "requirements"
    DESIGN = "design"
    CODEGEN = "codegen"
    QA = "qa"


@dataclass
class AgentConfig:
    """Configuration for a single agent."""
    id: str
    name: str
    model: str
    role: str
    output_format: str
    phase: Phase
    tier: AgentTier
    why: str = ""
    fallback_model: Optional[str] = None
    supplement_model: Optional[str] = None
    system_prompt: str = ""
    temperature: float = 0.7
    max_tokens: int = 4096
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "role": self.role,
            "output_format": self.output_format,
            "phase": self.phase.value,
            "tier": self.tier.value,
            "why": self.why,
            "fallback_model": self.fallback_model,
            "supplement_model": self.supplement_model,
        }


# =============================================================================
# PHASE 1: REQUIREMENTS → TECHNICAL SPECS
# =============================================================================

VISION_AGENT = AgentConfig(
    id="vision_agent",
    name="Vision Agent",
    model="local:phi3.5-vision",
    role="Extract UI elements from mockups",
    output_format="Structured JSON of UI components",
    phase=Phase.REQUIREMENTS,
    tier=AgentTier.LOCAL_NPU,
    why="NPU - best for local image processing, free",
    system_prompt="""You are a UI analysis expert. Extract all UI elements from the provided mockup.
Output a structured JSON with:
- components: list of UI components (buttons, inputs, cards, etc.)
- layout: page structure and hierarchy
- interactions: clickable elements and their expected behaviors
- styling: colors, fonts, spacing patterns detected"""
)

REQUIREMENTS_ANALYZER = AgentConfig(
    id="requirements_analyzer",
    name="Requirements Analyzer",
    model="gh:openai/gpt-5-mini",
    role="Deep analysis of business requirements",
    output_format="Comprehensive user stories, edge cases, business rules",
    phase=Phase.REQUIREMENTS,
    tier=AgentTier.CLOUD_STANDARD,
    why="Superior understanding of ambiguous/incomplete requirements",
    system_prompt="""You are a senior business analyst. Analyze the provided requirements thoroughly.

Output:
1. USER STORIES: Detailed user stories in Given/When/Then format
2. ACCEPTANCE CRITERIA: Specific, testable criteria for each story
3. EDGE CASES: Potential edge cases and error scenarios
4. BUSINESS RULES: Extracted business logic and constraints
5. ASSUMPTIONS: Any assumptions made about unclear requirements
6. QUESTIONS: Critical questions that need clarification"""
)

TECHNICAL_PLANNER = AgentConfig(
    id="technical_planner",
    name="Technical Planner",
    model="gh:openai/o3-mini",
    role="Convert requirements into technical specifications",
    output_format="Detailed technical specs with architecture options",
    phase=Phase.REQUIREMENTS,
    tier=AgentTier.CLOUD_PREMIUM,
    why="Deep reasoning about technical trade-offs",
    fallback_model="gh:openai/o1-mini",
    temperature=0.3,  # Lower for reasoning tasks
    system_prompt="""You are a principal engineer creating technical specifications.

Given the requirements analysis, produce:
1. TECHNICAL REQUIREMENTS: Specific technical constraints and needs
2. ARCHITECTURE OPTIONS: 2-3 viable architecture approaches with trade-offs
3. TECHNOLOGY STACK: Recommended technologies with justification
4. NON-FUNCTIONAL REQUIREMENTS: Performance, scalability, security needs
5. INTEGRATION POINTS: External systems and APIs needed
6. RISK ASSESSMENT: Technical risks and mitigation strategies"""
)

DOMAIN_MODELER = AgentConfig(
    id="domain_modeler",
    name="Domain Modeler",
    model="gh:deepseek/deepseek-r1",
    role="Create domain model and entity relationships",
    output_format="Domain-driven design model",
    phase=Phase.REQUIREMENTS,
    tier=AgentTier.CLOUD_PREMIUM,
    why="Excellent at complex relationship modeling",
    system_prompt="""You are a domain-driven design expert. Create a comprehensive domain model.

Output:
1. BOUNDED CONTEXTS: Identify distinct domains and their boundaries
2. ENTITIES: Core business entities with attributes
3. VALUE OBJECTS: Immutable value objects
4. AGGREGATES: Aggregate roots and their members
5. DOMAIN EVENTS: Key events in the system
6. RELATIONSHIPS: Entity relationships with cardinality
7. UBIQUITOUS LANGUAGE: Glossary of domain terms"""
)


# =============================================================================
# PHASE 2: SYSTEM DESIGN
# =============================================================================

SYSTEM_ARCHITECT = AgentConfig(
    id="system_architect",
    name="System Architect",
    model="gh:openai/gpt-5",
    role="Design overall system architecture",
    output_format="Complete architecture with microservices, APIs, infrastructure",
    phase=Phase.DESIGN,
    tier=AgentTier.CLOUD_PREMIUM,
    why="Superior at holistic system design and trade-off analysis",
    system_prompt="""You are a senior system architect designing production systems.

Create a complete system architecture including:
1. ARCHITECTURE DIAGRAM: Describe the high-level architecture (components, services)
2. SERVICE DECOMPOSITION: Microservices/modules with responsibilities
3. COMMUNICATION PATTERNS: Sync/async, REST/GraphQL/gRPC, message queues
4. DATA FLOW: How data moves through the system
5. INFRASTRUCTURE: Cloud services, containers, orchestration
6. SCALABILITY STRATEGY: How the system scales horizontally/vertically
7. DEPLOYMENT TOPOLOGY: Environments, CI/CD pipeline structure"""
)

DATABASE_ARCHITECT = AgentConfig(
    id="database_architect",
    name="Database Architect",
    model="gh:openai/gpt-4.1",
    role="Design database schema with optimization",
    output_format="Normalized schema, indexes, query patterns",
    phase=Phase.DESIGN,
    tier=AgentTier.CLOUD_STANDARD,
    why="Better at complex relationships and performance optimization",
    system_prompt="""You are a database architect optimizing for performance and maintainability.

Design the database including:
1. SCHEMA DESIGN: Tables/collections with fields, types, constraints
2. NORMALIZATION: Proper normalization level with justification
3. INDEXES: Primary, secondary, composite indexes for query optimization
4. RELATIONSHIPS: Foreign keys, junction tables, references
5. QUERY PATTERNS: Common queries and their optimization
6. MIGRATIONS: Initial migration scripts
7. SCALING STRATEGY: Sharding, replication, partitioning considerations"""
)

API_DESIGNER = AgentConfig(
    id="api_designer",
    name="API Designer",
    model="gh:openai/gpt-4.1-mini",
    role="Design REST/GraphQL API contracts",
    output_format="OpenAPI spec, versioning strategy",
    phase=Phase.DESIGN,
    tier=AgentTier.CLOUD_FAST,
    why="Fast, cheaper than GPT-5, excellent at API design",
    system_prompt="""You are an API design expert following REST best practices.

Design the API including:
1. ENDPOINTS: Full list with methods, paths, descriptions
2. REQUEST/RESPONSE: Schemas for all endpoints
3. AUTHENTICATION: Auth strategy (JWT, OAuth, API keys)
4. VERSIONING: API versioning approach
5. ERROR HANDLING: Standard error response format
6. PAGINATION: Pagination strategy for list endpoints
7. RATE LIMITING: Rate limit policies
8. OPENAPI SPEC: Complete OpenAPI 3.0 specification"""
)

SECURITY_ARCHITECT = AgentConfig(
    id="security_architect",
    name="Security Architect",
    model="gh:openai/o3-mini",
    role="Design security model and identify vulnerabilities",
    output_format="Auth strategy, data protection, security controls",
    phase=Phase.DESIGN,
    tier=AgentTier.CLOUD_PREMIUM,
    why="Deep reasoning about security implications",
    temperature=0.3,
    system_prompt="""You are a security architect identifying and mitigating risks.

Design security including:
1. AUTHENTICATION: Identity verification strategy
2. AUTHORIZATION: Role-based/attribute-based access control
3. DATA PROTECTION: Encryption at rest and in transit
4. INPUT VALIDATION: Validation and sanitization rules
5. THREAT MODEL: STRIDE analysis of potential threats
6. SECURITY CONTROLS: Specific controls for each threat
7. COMPLIANCE: Relevant compliance requirements (GDPR, SOC2, etc.)
8. SECURITY TESTING: Recommended security test strategies"""
)


# =============================================================================
# PHASE 3: CODE GENERATION
# =============================================================================

FRONTEND_GENERATOR = AgentConfig(
    id="frontend_generator",
    name="Frontend Generator",
    model="gh:openai/gpt-4.1",
    role="Generate React/Vue components with best practices",
    output_format="Modern, accessible, performant UI code",
    phase=Phase.CODEGEN,
    tier=AgentTier.CLOUD_STANDARD,
    why="Generates cleaner, more maintainable code than local models",
    fallback_model="ollama:qwen2.5-coder:14b",
    system_prompt="""You are a senior frontend developer writing production-quality code.

Generate frontend code following:
1. COMPONENT STRUCTURE: Proper component hierarchy and composition
2. STATE MANAGEMENT: Appropriate state handling (local, context, store)
3. STYLING: CSS-in-JS or Tailwind with consistent design system
4. ACCESSIBILITY: WCAG 2.1 AA compliance
5. PERFORMANCE: Code splitting, lazy loading, memoization
6. ERROR HANDLING: Error boundaries and user feedback
7. TYPESCRIPT: Full type safety with proper interfaces"""
)

BACKEND_GENERATOR = AgentConfig(
    id="backend_generator",
    name="Backend Generator",
    model="gh:openai/gpt-5-mini",
    role="Generate API endpoints, business logic, services",
    output_format="Well-structured backend with error handling",
    phase=Phase.CODEGEN,
    tier=AgentTier.CLOUD_STANDARD,
    why="Better at complex business logic and edge cases",
    supplement_model="ollama:qwen3-coder:30b",
    system_prompt="""You are a senior backend developer writing production-quality code.

Generate backend code following:
1. CLEAN ARCHITECTURE: Proper separation of concerns
2. ERROR HANDLING: Comprehensive error handling and logging
3. VALIDATION: Input validation at controller and service layers
4. TRANSACTIONS: Proper transaction management
5. TESTING: Testable code with dependency injection
6. SECURITY: Secure coding practices
7. DOCUMENTATION: JSDoc/docstrings for all public methods"""
)

DATABASE_GENERATOR = AgentConfig(
    id="database_generator",
    name="Database Generator",
    model="gh:openai/gpt-4.1-mini",
    role="Generate migrations, models, optimized queries",
    output_format="Efficient ORM models with proper indexes",
    phase=Phase.CODEGEN,
    tier=AgentTier.CLOUD_FAST,
    why="Better query optimization and migration strategies",
    system_prompt="""You are a database developer creating efficient data access code.

Generate database code including:
1. ORM MODELS: Entity definitions with relationships
2. MIGRATIONS: Versioned migration files
3. REPOSITORIES: Data access layer with query methods
4. QUERIES: Optimized queries for common operations
5. SEEDS: Sample data for development/testing
6. INDEXES: Index definitions in migrations"""
)

INTEGRATION_ORCHESTRATOR = AgentConfig(
    id="integration_orchestrator",
    name="Integration Orchestrator",
    model="local:phi4mini",
    role="Coordinate generation order and dependencies",
    output_format="Build pipeline, dependency resolution",
    phase=Phase.CODEGEN,
    tier=AgentTier.LOCAL_NPU,
    why="Fast local coordination, frequent calls",
    system_prompt="""You are a build coordinator managing code generation order.

Determine:
1. DEPENDENCY ORDER: Which files must be generated first
2. IMPORT GRAPH: How files depend on each other
3. BUILD SEQUENCE: Optimal order for code generation
4. INTEGRATION POINTS: Where components connect"""
)


# =============================================================================
# PHASE 4: QUALITY ASSURANCE
# =============================================================================

CODE_REVIEWER = AgentConfig(
    id="code_reviewer",
    name="Code Reviewer",
    model="gh:openai/o4-mini",
    role="Comprehensive code review (security, performance, maintainability)",
    output_format="Detailed review with refactoring suggestions",
    phase=Phase.QA,
    tier=AgentTier.CLOUD_PREMIUM,
    why="Superior reasoning about code quality and potential issues",
    fallback_model="gh:openai/o3-mini",
    temperature=0.3,
    system_prompt="""You are a principal engineer conducting a thorough code review.

Review for:
1. SECURITY: Vulnerabilities, injection risks, auth issues
2. PERFORMANCE: N+1 queries, memory leaks, inefficient algorithms
3. MAINTAINABILITY: Code clarity, DRY violations, complexity
4. ERROR HANDLING: Missing error cases, poor error messages
5. TESTING: Testability, missing test coverage areas
6. BEST PRACTICES: Framework-specific best practices
7. SUGGESTIONS: Specific refactoring recommendations with code examples"""
)

TEST_GENERATOR = AgentConfig(
    id="test_generator",
    name="Test Generator",
    model="gh:openai/gpt-4.1",
    role="Generate unit, integration, E2E tests",
    output_format="Complete test suites with edge cases",
    phase=Phase.QA,
    tier=AgentTier.CLOUD_STANDARD,
    why="Better at identifying edge cases and test scenarios",
    system_prompt="""You are a QA engineer writing comprehensive test suites.

Generate tests including:
1. UNIT TESTS: Tests for individual functions/methods
2. INTEGRATION TESTS: Tests for component interactions
3. E2E TESTS: End-to-end user flow tests
4. EDGE CASES: Boundary conditions, error cases
5. MOCKING: Proper mocks for dependencies
6. FIXTURES: Test data and setup/teardown
7. COVERAGE: Ensure high code coverage"""
)

DOCUMENTATION_WRITER = AgentConfig(
    id="documentation_writer",
    name="Documentation Writer",
    model="gh:openai/gpt-4.1-mini",
    role="Generate API docs, README, guides",
    output_format="Clear, comprehensive documentation",
    phase=Phase.QA,
    tier=AgentTier.CLOUD_FAST,
    why="Better writing quality than local models",
    supplement_model="local:phi4",
    system_prompt="""You are a technical writer creating clear documentation.

Generate documentation including:
1. README: Project overview, setup, usage
2. API DOCS: Endpoint documentation with examples
3. ARCHITECTURE DOCS: System design documentation
4. DEVELOPER GUIDE: Contributing, coding standards
5. DEPLOYMENT GUIDE: Deployment instructions
6. TROUBLESHOOTING: Common issues and solutions"""
)

PERFORMANCE_AUDITOR = AgentConfig(
    id="performance_auditor",
    name="Performance Auditor",
    model="gh:openai/o3-mini",
    role="Analyze performance bottlenecks and optimization opportunities",
    output_format="Performance report with specific optimizations",
    phase=Phase.QA,
    tier=AgentTier.CLOUD_PREMIUM,
    why="Deep reasoning about algorithmic complexity and optimization",
    temperature=0.3,
    system_prompt="""You are a performance engineer analyzing system performance.

Analyze and report on:
1. ALGORITHMIC COMPLEXITY: Big-O analysis of key operations
2. DATABASE PERFORMANCE: Query optimization opportunities
3. CACHING STRATEGY: What to cache and where
4. BUNDLE SIZE: Frontend optimization opportunities
5. MEMORY USAGE: Potential memory leaks or bloat
6. CONCURRENCY: Thread safety and parallelization opportunities
7. RECOMMENDATIONS: Prioritized list of optimizations"""
)


# =============================================================================
# AGENT REGISTRY
# =============================================================================

AGENT_REGISTRY: Dict[str, AgentConfig] = {
    # Phase 1: Requirements
    "vision_agent": VISION_AGENT,
    "requirements_analyzer": REQUIREMENTS_ANALYZER,
    "technical_planner": TECHNICAL_PLANNER,
    "domain_modeler": DOMAIN_MODELER,
    
    # Phase 2: Design
    "system_architect": SYSTEM_ARCHITECT,
    "database_architect": DATABASE_ARCHITECT,
    "api_designer": API_DESIGNER,
    "security_architect": SECURITY_ARCHITECT,
    
    # Phase 3: Code Generation
    "frontend_generator": FRONTEND_GENERATOR,
    "backend_generator": BACKEND_GENERATOR,
    "database_generator": DATABASE_GENERATOR,
    "integration_orchestrator": INTEGRATION_ORCHESTRATOR,
    
    # Phase 4: QA
    "code_reviewer": CODE_REVIEWER,
    "test_generator": TEST_GENERATOR,
    "documentation_writer": DOCUMENTATION_WRITER,
    "performance_auditor": PERFORMANCE_AUDITOR,
}


def get_agent_config(agent_id: str) -> Optional[AgentConfig]:
    """Get agent configuration by ID."""
    return AGENT_REGISTRY.get(agent_id)


def list_agents_by_phase(phase: Phase) -> List[AgentConfig]:
    """Get all agents for a specific phase."""
    return [a for a in AGENT_REGISTRY.values() if a.phase == phase]


def list_agents_by_tier(tier: AgentTier) -> List[AgentConfig]:
    """Get all agents for a specific cost tier."""
    return [a for a in AGENT_REGISTRY.values() if a.tier == tier]


def get_cost_summary() -> Dict[str, Any]:
    """Get summary of agents by cost tier."""
    summary = {tier.value: [] for tier in AgentTier}
    for agent in AGENT_REGISTRY.values():
        summary[agent.tier.value].append(agent.id)
    return summary
