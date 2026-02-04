"""
GitHub MCP Server Client

Provides GitHub API access via MCP protocol.
"""

from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, List, Optional

from multiagent_workflows.mcp.base import (
    MCPClient,
    MCPServerConfig,
    MCPToolSchema,
    MCPResponse,
)


class GitHubMCPClient(MCPClient):
    """
    MCP client for GitHub operations.
    
    This is a local implementation using the GitHub API directly.
    Requires GITHUB_TOKEN environment variable.
    """
    
    TOOLS = [
        MCPToolSchema(
            name="search_repositories",
            description="Search for GitHub repositories",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                    },
                    "page": {
                        "type": "integer",
                        "description": "Page number for pagination",
                    },
                    "perPage": {
                        "type": "integer",
                        "description": "Results per page (max 100)",
                    },
                },
                "required": ["query"],
            },
        ),
        MCPToolSchema(
            name="get_file_contents",
            description="Get contents of a file in a repository",
            input_schema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "path": {"type": "string"},
                    "branch": {"type": "string"},
                },
                "required": ["owner", "repo", "path"],
            },
        ),
        MCPToolSchema(
            name="create_or_update_file",
            description="Create or update a file in a repository",
            input_schema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                    "message": {"type": "string"},
                    "branch": {"type": "string"},
                    "sha": {"type": "string", "description": "SHA if updating existing file"},
                },
                "required": ["owner", "repo", "path", "content", "message"],
            },
        ),
        MCPToolSchema(
            name="create_issue",
            description="Create a new issue in a repository",
            input_schema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "title": {"type": "string"},
                    "body": {"type": "string"},
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "assignees": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": ["owner", "repo", "title"],
            },
        ),
        MCPToolSchema(
            name="create_pull_request",
            description="Create a pull request",
            input_schema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "title": {"type": "string"},
                    "body": {"type": "string"},
                    "head": {"type": "string"},
                    "base": {"type": "string"},
                    "draft": {"type": "boolean"},
                },
                "required": ["owner", "repo", "title", "head", "base"],
            },
        ),
        MCPToolSchema(
            name="list_commits",
            description="List commits in a repository",
            input_schema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "sha": {"type": "string", "description": "Branch or commit SHA"},
                    "page": {"type": "integer"},
                    "perPage": {"type": "integer"},
                },
                "required": ["owner", "repo"],
            },
        ),
        MCPToolSchema(
            name="list_issues",
            description="List issues in a repository",
            input_schema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed", "all"],
                    },
                    "labels": {"type": "string"},
                    "page": {"type": "integer"},
                    "perPage": {"type": "integer"},
                },
                "required": ["owner", "repo"],
            },
        ),
        MCPToolSchema(
            name="search_code",
            description="Search for code in GitHub repositories",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "page": {"type": "integer"},
                    "perPage": {"type": "integer"},
                },
                "required": ["query"],
            },
        ),
        MCPToolSchema(
            name="fork_repository",
            description="Fork a repository",
            input_schema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "organization": {"type": "string"},
                },
                "required": ["owner", "repo"],
            },
        ),
        MCPToolSchema(
            name="create_branch",
            description="Create a new branch",
            input_schema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "branch": {"type": "string"},
                    "from_branch": {"type": "string"},
                },
                "required": ["owner", "repo", "branch"],
            },
        ),
    ]
    
    def __init__(
        self,
        token: Optional[str] = None,
        config: Optional[MCPServerConfig] = None,
    ):
        if config is None:
            config = MCPServerConfig(
                name="github",
                server_type="local",
                endpoint="https://api.github.com",
                capabilities=["repos", "issues", "pulls", "search"],
            )
        super().__init__(config)
        
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self._tools = self.TOOLS.copy()
    
    async def connect(self) -> bool:
        """Verify GitHub token is available."""
        if not self.token:
            raise ValueError(
                "GitHub token required. Set GITHUB_TOKEN environment variable."
            )
        self.connected = True
        return True
    
    async def disconnect(self) -> None:
        """No disconnection needed."""
        self.connected = False
    
    async def list_tools(self) -> List[MCPToolSchema]:
        """Return available GitHub tools."""
        return self._tools
    
    async def invoke_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> MCPResponse:
        """Invoke a GitHub API tool."""
        try:
            handlers = {
                "search_repositories": self._search_repositories,
                "get_file_contents": self._get_file_contents,
                "create_or_update_file": self._create_or_update_file,
                "create_issue": self._create_issue,
                "create_pull_request": self._create_pull_request,
                "list_commits": self._list_commits,
                "list_issues": self._list_issues,
                "search_code": self._search_code,
                "fork_repository": self._fork_repository,
                "create_branch": self._create_branch,
            }
            
            handler = handlers.get(tool_name)
            if not handler:
                return MCPResponse(
                    success=False,
                    result=None,
                    error=f"Unknown tool: {tool_name}",
                )
            
            result = await handler(arguments)
            return MCPResponse(success=True, result=result)
            
        except Exception as e:
            return MCPResponse(success=False, result=None, error=str(e))
    
    def _headers(self) -> Dict[str, str]:
        """Get request headers."""
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a request to the GitHub API."""
        import aiohttp
        
        url = f"{self.base_url}{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                url,
                headers=self._headers(),
                json=data,
                params=params,
            ) as response:
                if response.status >= 400:
                    error_text = await response.text()
                    raise Exception(f"GitHub API error {response.status}: {error_text}")
                
                return await response.json()
    
    async def _search_repositories(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search for repositories."""
        params = {
            "q": args["query"],
            "page": args.get("page", 1),
            "per_page": args.get("perPage", 30),
        }
        return await self._request("GET", "/search/repositories", params=params)
    
    async def _get_file_contents(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get file contents."""
        endpoint = f"/repos/{args['owner']}/{args['repo']}/contents/{args['path']}"
        params = {}
        if "branch" in args:
            params["ref"] = args["branch"]
        return await self._request("GET", endpoint, params=params)
    
    async def _create_or_update_file(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update a file."""
        import base64
        
        endpoint = f"/repos/{args['owner']}/{args['repo']}/contents/{args['path']}"
        
        data = {
            "message": args["message"],
            "content": base64.b64encode(args["content"].encode()).decode(),
        }
        
        if "branch" in args:
            data["branch"] = args["branch"]
        if "sha" in args:
            data["sha"] = args["sha"]
        
        return await self._request("PUT", endpoint, data=data)
    
    async def _create_issue(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create an issue."""
        endpoint = f"/repos/{args['owner']}/{args['repo']}/issues"
        
        data = {
            "title": args["title"],
        }
        if "body" in args:
            data["body"] = args["body"]
        if "labels" in args:
            data["labels"] = args["labels"]
        if "assignees" in args:
            data["assignees"] = args["assignees"]
        
        return await self._request("POST", endpoint, data=data)
    
    async def _create_pull_request(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a pull request."""
        endpoint = f"/repos/{args['owner']}/{args['repo']}/pulls"
        
        data = {
            "title": args["title"],
            "head": args["head"],
            "base": args["base"],
        }
        if "body" in args:
            data["body"] = args["body"]
        if "draft" in args:
            data["draft"] = args["draft"]
        
        return await self._request("POST", endpoint, data=data)
    
    async def _list_commits(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """List commits."""
        endpoint = f"/repos/{args['owner']}/{args['repo']}/commits"
        
        params = {}
        if "sha" in args:
            params["sha"] = args["sha"]
        if "page" in args:
            params["page"] = args["page"]
        if "perPage" in args:
            params["per_page"] = args["perPage"]
        
        commits = await self._request("GET", endpoint, params=params)
        return {"commits": commits}
    
    async def _list_issues(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """List issues."""
        endpoint = f"/repos/{args['owner']}/{args['repo']}/issues"
        
        params = {}
        if "state" in args:
            params["state"] = args["state"]
        if "labels" in args:
            params["labels"] = args["labels"]
        if "page" in args:
            params["page"] = args["page"]
        if "perPage" in args:
            params["per_page"] = args["perPage"]
        
        issues = await self._request("GET", endpoint, params=params)
        return {"issues": issues}
    
    async def _search_code(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search code."""
        params = {
            "q": args["query"],
            "page": args.get("page", 1),
            "per_page": args.get("perPage", 30),
        }
        return await self._request("GET", "/search/code", params=params)
    
    async def _fork_repository(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Fork a repository."""
        endpoint = f"/repos/{args['owner']}/{args['repo']}/forks"
        
        data = {}
        if "organization" in args:
            data["organization"] = args["organization"]
        
        return await self._request("POST", endpoint, data=data if data else None)
    
    async def _create_branch(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new branch."""
        # First get the SHA of the source branch
        from_branch = args.get("from_branch", "main")
        ref_endpoint = f"/repos/{args['owner']}/{args['repo']}/git/ref/heads/{from_branch}"
        
        ref_data = await self._request("GET", ref_endpoint)
        sha = ref_data["object"]["sha"]
        
        # Create the new branch
        create_endpoint = f"/repos/{args['owner']}/{args['repo']}/git/refs"
        
        return await self._request("POST", create_endpoint, data={
            "ref": f"refs/heads/{args['branch']}",
            "sha": sha,
        })
