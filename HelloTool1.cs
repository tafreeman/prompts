using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Extensions.Mcp;
using Microsoft.Extensions.Logging;

namespace Company.Function;

public class HelloTool1
{
    private ILogger<HelloTool1> _logger;

    public HelloTool1(ILogger<HelloTool1> logger)
    {
        _logger = logger;
    }

    [Function(nameof(HelloTool1))]
    public string Run(
        [McpToolTrigger(nameof(HelloTool1), "Responds to the user with a hello message.")] ToolInvocationContext context,
        [McpToolProperty(nameof(name), "The name of the person to greet.")] string? name
    )
    {
        _logger.LogInformation("C# MCP tool trigger function processed a request.");
        return $"Hello, {name ?? "world"}! This is an MCP Tool!";
    }
}
