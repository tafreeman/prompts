"""
LangChain Chain Implementations

Provides concrete LangChain chains and runnables for each agent role.
Replaces stub functions with real LLM-backed chains.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Type, Union

try:
    from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    Runnable = object

from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.core.tool_registry import ToolRegistry
from multiagent_workflows.langchain.tools import create_langchain_tools


@dataclass
class ChainConfig:
    """Configuration for creating chains."""
    agent_id: str
    name: str
    role: str
    system_prompt: str
    model_id: str
    tools: List[str] = None
    output_schema: Optional[Dict[str, Any]] = None
    temperature: float = 0.7
    max_tokens: int = 4096
    
    def __post_init__(self):
        if self.tools is None:
            self.tools = []


class AgentChainFactory:
    """
    Factory for creating LangChain chains/runnables for agent roles.
    
    Maps agent configurations to appropriate chain implementations.
    """
    
    def __init__(
        self,
        model_manager: ModelManager,
        tool_registry: Optional[ToolRegistry] = None,
    ):
        self.model_manager = model_manager
        self.tool_registry = tool_registry
        self._chain_cache: Dict[str, Any] = {}
    
    def create_chain(
        self,
        config: ChainConfig,
        use_tools: bool = False,
    ) -> Any:
        """
        Create a LangChain chain for the given configuration.
        
        Args:
            config: Chain configuration
            use_tools: Whether to enable tool use
            
        Returns:
            LangChain Runnable or AgentExecutor
        """
        cache_key = f"{config.agent_id}:{config.model_id}:{use_tools}"
        if cache_key in self._chain_cache:
            return self._chain_cache[cache_key]
        
        if LANGCHAIN_AVAILABLE:
            chain = self._create_langchain_chain(config, use_tools)
        else:
            chain = self._create_fallback_chain(config)
        
        self._chain_cache[cache_key] = chain
        return chain
    
    def _create_langchain_chain(
        self,
        config: ChainConfig,
        use_tools: bool,
    ) -> Runnable:
        """Create a real LangChain chain."""
        from langchain_core.runnables import RunnableSequence
        
        # Get LLM from model manager via LangChain adapter
        llm = self._get_langchain_llm(config.model_id)
        
        # Build prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", config.system_prompt),
            MessagesPlaceholder(variable_name="history", optional=True),
            ("human", "{input}"),
        ])
        
        if use_tools and config.tools:
            return self._create_tool_agent(config, llm, prompt)
        else:
            return self._create_simple_chain(config, llm, prompt)
    
    def _create_simple_chain(
        self,
        config: ChainConfig,
        llm: Any,
        prompt: Any,
    ) -> Any:
        """Create a simple prompt -> LLM -> output chain."""
        from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
        
        # Choose parser based on expected output
        if config.output_schema:
            parser = JsonOutputParser()
        else:
            parser = StrOutputParser()
        
        chain = prompt | llm | parser
        
        # Wrap with input/output formatting
        return RunnableLambda(self._format_input) | chain | RunnableLambda(
            lambda x: self._format_output(x, config)
        )
    
    def _create_tool_agent(
        self,
        config: ChainConfig,
        llm: Any,
        prompt: Any,
    ) -> Any:
        """Create an agent with tool use capability."""
        try:
            from langchain.agents import AgentExecutor, create_openai_tools_agent
            from langchain_core.tools import BaseTool
            
            # Get tools from registry
            tools = create_langchain_tools(registry=self.tool_registry)
            
            # Filter to only requested tools
            if config.tools:
                tools = [t for t in tools if t.name in config.tools]
            
            # Create agent
            if hasattr(llm, 'bind_tools'):
                # Modern approach with tool binding
                llm_with_tools = llm.bind_tools(tools)
                
                from langchain.agents import create_tool_calling_agent
                agent = create_tool_calling_agent(llm_with_tools, tools, prompt)
            else:
                # Fallback to OpenAI tools agent
                agent = create_openai_tools_agent(llm, tools, prompt)
            
            return AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5,
            )
            
        except ImportError:
            # Fallback to simple chain if agent creation fails
            return self._create_simple_chain(config, llm, prompt)
    
    def _get_langchain_llm(self, model_id: str) -> Any:
        """Get a LangChain-compatible LLM from model manager."""
        import os
        
        # Try to use the existing LangChainAdapter first
        try:
            from tools.llm.langchain_adapter import LangChainAdapter
            return LangChainAdapter(model_id)
        except ImportError:
            pass
        
        # Try direct LangChain model creation
        try:
            if model_id.startswith("gh:"):
                # GitHub Models - use Azure OpenAI endpoint
                # Extract model name (e.g., "gh:openai/gpt-4o" -> "gpt-4o")
                model_name = model_id.split("/")[-1] if "/" in model_id else model_id.split(":")[-1]
                
                # Check if GITHUB_TOKEN is available
                github_token = os.environ.get("GITHUB_TOKEN")
                if github_token:
                    from langchain_openai import AzureChatOpenAI
                    return AzureChatOpenAI(
                        model=model_name,
                        azure_endpoint="https://models.inference.ai.azure.com",
                        api_key=github_token,
                        api_version="2024-02-15-preview",
                    )
                else:
                    # Fall back to model manager
                    return _FallbackLLM(self.model_manager, model_id)
            elif model_id.startswith("azure:"):
                from langchain_openai import AzureChatOpenAI
                return AzureChatOpenAI(model=model_id.split(":")[-1])
            elif model_id.startswith("openai:"):
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(model=model_id.split(":")[-1])
            elif model_id.startswith("ollama:") or model_id.startswith("local:"):
                from langchain_ollama import ChatOllama
                return ChatOllama(model=model_id.split(":")[-1])
            else:
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(model=model_id)
        except ImportError:
            # Ultimate fallback: custom wrapper
            return _FallbackLLM(self.model_manager, model_id)
        except Exception:
            # Any other error - use fallback
            return _FallbackLLM(self.model_manager, model_id)
    
    def _create_fallback_chain(self, config: ChainConfig) -> Callable:
        """Create a fallback chain when LangChain is not available."""
        def fallback_chain(inputs: Dict[str, Any]) -> Dict[str, Any]:
            # Use model manager directly
            prompt = f"{config.system_prompt}\n\n{inputs.get('input', '')}"
            
            result = self.model_manager.generate_text(
                model_id=config.model_id,
                prompt=prompt,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
            )
            
            # Parse response with robust JSON extraction
            response_text = getattr(result, 'text', str(result))
            return _parse_json_response(response_text)
        
        return fallback_chain
    
    def _format_input(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Format state into chain input."""
        # Extract relevant parts of state for the chain
        input_text = state.get("input", "")
        
        # Build context from artifacts
        context_parts = []
        if "artifacts" in state:
            for key, value in state["artifacts"].items():
                if isinstance(value, str):
                    context_parts.append(f"{key}:\n{value[:2000]}")
                else:
                    context_parts.append(f"{key}: {json.dumps(value, default=str)[:1000]}")
        
        if context_parts:
            input_text = f"{input_text}\n\nContext:\n" + "\n\n".join(context_parts)
        
        return {
            "input": input_text,
            "history": state.get("messages", []),
        }
    
    def _format_output(
        self,
        output: Any,
        config: ChainConfig,
    ) -> Dict[str, Any]:
        """Format chain output into state update."""
        if isinstance(output, dict):
            return output
        elif isinstance(output, str):
            # Try to parse as JSON, handling code fences
            return _parse_json_response(output)
        else:
            return {"output": output}


def _parse_json_response(text: str) -> Dict[str, Any]:
    """
    Parse JSON from LLM response, handling code fences and markdown.
    
    Handles formats:
    - Plain JSON: {"key": "value"}
    - Code fenced: ```json\n{"key": "value"}\n```
    - Generic fenced: ```\n{"key": "value"}\n```
    - Embedded in text: Some text {"key": "value"} more text
    """
    if not text or not text.strip():
        return {"raw_response": text}
    
    text = text.strip()
    
    # Try direct parse first (already clean JSON)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try extracting from ```json ... ``` code fence
    if "```json" in text:
        try:
            start = text.index("```json") + 7
            end = text.index("```", start)
            json_str = text[start:end].strip()
            return json.loads(json_str)
        except (ValueError, json.JSONDecodeError):
            pass
    
    # Try extracting from generic ``` ... ``` code fence
    if "```" in text:
        try:
            start = text.index("```") + 3
            # Skip language identifier if present (e.g., ```python)
            newline = text.find("\n", start)
            if newline != -1 and newline - start < 15:  # Reasonable language id length
                start = newline + 1
            end = text.index("```", start)
            json_str = text[start:end].strip()
            if json_str.startswith("{") or json_str.startswith("["):
                return json.loads(json_str)
        except (ValueError, json.JSONDecodeError):
            pass
    
    # Try finding JSON object in text
    if "{" in text:
        try:
            start = text.index("{")
            # Find matching closing brace
            depth = 0
            for i, c in enumerate(text[start:], start):
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        json_str = text[start:i + 1]
                        return json.loads(json_str)
        except (ValueError, json.JSONDecodeError):
            pass
    
    # Try finding JSON array in text
    if "[" in text and "{" not in text[:text.index("[")]:
        try:
            start = text.index("[")
            depth = 0
            for i, c in enumerate(text[start:], start):
                if c == "[":
                    depth += 1
                elif c == "]":
                    depth -= 1
                    if depth == 0:
                        json_str = text[start:i + 1]
                        return json.loads(json_str)
        except (ValueError, json.JSONDecodeError):
            pass
    
    # Failed to parse - return raw response
    return {"raw_response": text}


class _FallbackLLM:
    """Fallback LLM wrapper when LangChain models aren't available."""
    
    def __init__(self, model_manager: ModelManager, model_id: str):
        self.model_manager = model_manager
        self.model_id = model_id
    
    def __call__(self, prompt: str, **kwargs) -> str:
        result = self.model_manager.generate_text(
            model_id=self.model_id,
            prompt=prompt,
            max_tokens=kwargs.get("max_tokens", 4096),
            temperature=kwargs.get("temperature", 0.7),
        )
        return getattr(result, 'text', str(result))
    
    def invoke(self, input_data: Any, **kwargs) -> Any:
        if isinstance(input_data, str):
            return self(input_data, **kwargs)
        elif hasattr(input_data, 'to_string'):
            return self(input_data.to_string(), **kwargs)
        else:
            return self(str(input_data), **kwargs)


# =============================================================================
# Pre-defined Chain Templates for Common Roles
# =============================================================================

ROLE_CHAIN_CONFIGS: Dict[str, Dict[str, Any]] = {
    "requirements_analyzer": {
        "system_prompt": """You are a senior business analyst. Analyze the provided requirements thoroughly.

Your task is to:
1. Extract clear user stories with acceptance criteria
2. Identify data entities and relationships
3. Define non-functional requirements
4. Note any ambiguities or missing information

Output your analysis as a JSON object with keys: user_stories, data_entities, nfrs, clarifications_needed""",
        "output_keys": ["user_stories", "data_entities"],
    },
    "system_architect": {
        "system_prompt": """You are a senior software architect. Design a complete system architecture.

Create:
1. High-level component diagram (describe in structured format)
2. Technology stack recommendations with justifications
3. API strategy and patterns
4. Data flow design
5. Security considerations

Output as JSON with keys: architecture, tech_stack, api_strategy, security_notes""",
        "output_keys": ["architecture", "tech_stack"],
    },
    "database_architect": {
        "system_prompt": """You are a database architect. Design the database schema.

Create:
1. Entity-relationship model
2. Table definitions with proper types and constraints
3. Index strategy
4. Migration scripts

Output as JSON with keys: schema, migrations, indexes""",
        "output_keys": ["schema", "migrations"],
    },
    "api_designer": {
        "system_prompt": """You are an API design expert. Design RESTful API contracts.

Create:
1. OpenAPI 3.0 specification
2. Endpoint definitions with request/response schemas
3. Authentication flow
4. Error handling patterns

Output as JSON with keys: api_spec, endpoints, auth_flow""",
        "output_keys": ["api_spec", "endpoints"],
    },
    "backend_generator": {
        "system_prompt": """You are a senior backend developer. Generate production-quality backend code.

Follow:
1. Clean architecture principles
2. Proper error handling
3. Input validation
4. Security best practices
5. Comprehensive type annotations

Output as JSON with keys: backend_code, backend_files (list of file objects with path and content)""",
        "output_keys": ["backend_code", "backend_files"],
    },
    "frontend_generator": {
        "system_prompt": """You are a senior frontend developer. Generate production-quality frontend code.

Follow:
1. Component-based architecture
2. Proper state management
3. Accessibility standards
4. Responsive design
5. Modern CSS practices

Output as JSON with keys: frontend_code, frontend_files (list of file objects with path and content)""",
        "output_keys": ["frontend_code", "frontend_files"],
    },
    "code_reviewer": {
        "system_prompt": """You are a senior security engineer and code reviewer.

Review the code for:
1. Security vulnerabilities (OWASP Top 10)
2. Performance issues
3. Code quality and maintainability
4. Best practices violations

For each issue provide: severity, location, description, recommendation.

Output as JSON with keys: review_results, issues (list), summary""",
        "output_keys": ["review_results", "issues"],
    },
    "test_generator": {
        "system_prompt": """You are a QA automation expert. Generate comprehensive tests.

Create:
1. Unit tests (target >80% coverage)
2. Integration tests
3. E2E test scenarios
4. Edge case tests

Use appropriate testing frameworks. Follow Arrange-Act-Assert pattern.

Output as JSON with keys: tests, test_files, coverage_targets""",
        "output_keys": ["tests", "test_files"],
    },
    "documentation_writer": {
        "system_prompt": """You are a technical writer. Generate comprehensive documentation.

Create:
1. README with project overview
2. Installation guide
3. API documentation
4. Architecture overview
5. Configuration guide

Use clear markdown formatting with code examples.

Output as JSON with keys: readme, api_docs, setup_guide""",
        "output_keys": ["readme", "api_docs"],
    },
}


def create_agent_chain(
    agent_id: str,
    model_manager: ModelManager,
    tool_registry: Optional[ToolRegistry] = None,
    model_id: Optional[str] = None,
    custom_prompt: Optional[str] = None,
) -> Any:
    """
    Convenience function to create an agent chain.
    
    Args:
        agent_id: ID of the agent (e.g., "requirements_analyzer")
        model_manager: Model manager instance
        tool_registry: Optional tool registry
        model_id: Override model ID
        custom_prompt: Override system prompt
        
    Returns:
        LangChain Runnable or callable
    """
    factory = AgentChainFactory(model_manager, tool_registry)
    
    # Get role config or use defaults
    role_config = ROLE_CHAIN_CONFIGS.get(agent_id, {})
    
    config = ChainConfig(
        agent_id=agent_id,
        name=agent_id.replace("_", " ").title(),
        role=agent_id,
        system_prompt=custom_prompt or role_config.get(
            "system_prompt",
            f"You are a {agent_id.replace('_', ' ')}. Complete the assigned task."
        ),
        model_id=model_id or model_manager.get_optimal_model("reasoning", complexity=6),
        tools=role_config.get("tools", []),
    )
    
    return factory.create_chain(config, use_tools=bool(config.tools))
