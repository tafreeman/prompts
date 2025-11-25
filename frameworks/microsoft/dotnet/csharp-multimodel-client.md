---
title: "C# Prompt Engineering Utilities"
category: "frameworks"
subcategory: "microsoft"
technique_type: "dotnet-integration"
framework_compatibility:
  dotnet: ">=6.0"
  csharp: ">=10.0"
difficulty: "intermediate"
use_cases:
  - multi-model-integration
  - prompt-templating
  - enterprise-integration
version: "1.0.0"
author: "AI Research Team"
last_updated: "2025-11-23"
tags:
  - csharp
  - dotnet
  - multi-model
  - enterprise
---

# C# Prompt Engineering Utilities

## Purpose

Provides C# utilities for prompt templating, multi-model AI integration, and enterprise patterns suitable for .NET/MuleSoft environments.

## Multi-Model Client

```csharp
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace PromptEngineering.Core
{
    /// <summary>
    /// Unified client for multiple AI model providers (OpenAI, Anthropic, Azure OpenAI).
    /// </summary>
    public class MultiModelClient : IDisposable
    {
        private readonly HttpClient _httpClient;
        private readonly IConfiguration _configuration;
        private readonly ILogger<MultiModelClient> _logger;
        
        public MultiModelClient(
            HttpClient httpClient,
            IConfiguration configuration,
            ILogger<MultiModelClient> logger)
        {
            _httpClient = httpClient ?? throw new ArgumentNullException(nameof(httpClient));
            _configuration = configuration ?? throw new ArgumentNullException(nameof(configuration));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }
        
        /// <summary>
        /// Calls the specified AI model with the given prompt.
        /// </summary>
        public async Task<ModelResponse> CallAsync(
            ModelRequest request,
            CancellationToken cancellationToken = default)
        {
            _logger.LogInformation("Calling {Provider} model {Model}", request.Provider, request.Model);
            
            return request.Provider switch
            {
                ModelProvider.OpenAI => await CallOpenAIAsync(request, cancellationToken),
                ModelProvider.Anthropic => await CallAnthropicAsync(request, cancellationToken),
                ModelProvider.AzureOpenAI => await CallAzureOpenAIAsync(request, cancellationToken),
                _ => throw new NotSupportedException($"Provider {request.Provider} is not supported")
            };
        }
        
        private async Task<ModelResponse> CallOpenAIAsync(
            ModelRequest request,
            CancellationToken cancellationToken)
        {
            var apiKey = _configuration["OpenAI:ApiKey"] 
                ?? throw new InvalidOperationException("OpenAI API key not configured");
            
            _httpClient.DefaultRequestHeaders.Authorization = 
                new AuthenticationHeaderValue("Bearer", apiKey);
            
            var payload = new
            {
                model = request.Model,
                messages = new[]
                {
                    new { role = "system", content = request.SystemPrompt ?? "You are a helpful assistant." },
                    new { role = "user", content = request.Prompt }
                },
                temperature = request.Temperature,
                max_tokens = request.MaxTokens
            };
            
            var content = new StringContent(
                JsonSerializer.Serialize(payload),
                Encoding.UTF8,
                "application/json");
            
            var response = await _httpClient.PostAsync(
                "https://api.openai.com/v1/chat/completions",
                content,
                cancellationToken);
            
            response.EnsureSuccessStatusCode();
            
            var jsonResponse = await response.Content.ReadAsStringAsync(cancellationToken);
            var openAIResponse = JsonSerializer.Deserialize<OpenAIResponse>(jsonResponse);
            
            return new ModelResponse
            {
                Content = openAIResponse.Choices[0].Message.Content,
                Provider = ModelProvider.OpenAI,
                Model = request.Model,
                TokensUsed = openAIResponse.Usage.TotalTokens
            };
        }
        
        private async Task<ModelResponse> CallAnthropicAsync(
            ModelRequest request,
            CancellationToken cancellationToken)
        {
            var apiKey = _configuration["Anthropic:ApiKey"] 
                ?? throw new InvalidOperationException("Anthropic API key not configured");
            
            _httpClient.DefaultRequestHeaders.Clear();
            _httpClient.DefaultRequestHeaders.Add("x-api-key", apiKey);
            _httpClient.DefaultRequestHeaders.Add("anthropic-version", "2023-06-01");
            
            var payload = new
            {
                model = request.Model,
                max_tokens = request.MaxTokens,
                messages = new[]
                {
                    new { role = "user", content = request.Prompt }
                },
                system = request.SystemPrompt
            };
            
            var content = new StringContent(
                JsonSerializer.Serialize(payload),
                Encoding.UTF8,
                "application/json");
            
            var response = await _httpClient.PostAsync(
                "https://api.anthropic.com/v1/messages",
                content,
                cancellationToken);
            
            response.EnsureSuccessStatusCode();
            
            var jsonResponse = await response.Content.ReadAsStringAsync(cancellationToken);
            var anthropicResponse = JsonSerializer.Deserialize<AnthropicResponse>(jsonResponse);
            
            return new ModelResponse
            {
                Content = anthropicResponse.Content[0].Text,
                Provider = ModelProvider.Anthropic,
                Model = request.Model,
                TokensUsed = anthropicResponse.Usage.InputTokens + anthropicResponse.Usage.OutputTokens
            };
        }
        
        private async Task<ModelResponse> CallAzureOpenAIAsync(
            ModelRequest request,
            CancellationToken cancellationToken)
        {
            var apiKey = _configuration["AzureOpenAI:ApiKey"];
            var endpoint = _configuration["AzureOpenAI:Endpoint"];
            var deploymentName = _configuration["AzureOpenAI:DeploymentName"];
            
            _httpClient.DefaultRequestHeaders.Clear();
            _httpClient.DefaultRequestHeaders.Add("api-key", apiKey);
            
            var payload = new
            {
                messages = new[]
                {
                    new { role = "system", content = request.SystemPrompt ?? "You are a helpful assistant." },
                    new { role = "user", content = request.Prompt }
                },
                temperature = request.Temperature,
                max_tokens = request.MaxTokens
            };
            
            var url = $"{endpoint}/openai/deployments/{deploymentName}/chat/completions?api-version=2023-05-15";
            
            var content = new StringContent(
                JsonSerializer.Serialize(payload),
                Encoding.UTF8,
                "application/json");
            
            var response = await _httpClient.PostAsync(url, content, cancellationToken);
            response.EnsureSuccessStatusCode();
            
            var jsonResponse = await response.Content.ReadAsStringAsync(cancellationToken);
            var azureResponse = JsonSerializer.Deserialize<OpenAIResponse>(jsonResponse);
            
            return new ModelResponse
            {
                Content = azureResponse.Choices[0].Message.Content,
                Provider = ModelProvider.AzureOpenAI,
                Model = deploymentName,
                TokensUsed = azureResponse.Usage.TotalTokens
            };
        }
        
        public void Dispose()
        {
            _httpClient?.Dispose();
        }
    }
    
    // DTOs
    public enum ModelProvider
    {
        OpenAI,
        Anthropic,
        AzureOpenAI,
        Google
    }
    
    public class ModelRequest
    {
        public ModelProvider Provider { get; set; }
        public string Model { get; set; }
        public string Prompt { get; set; }
        public string? SystemPrompt { get; set; }
        public double Temperature { get; set; } = 0.7;
        public int MaxTokens { get; set; } = 1000;
    }
    
    public class ModelResponse
    {
        public string Content { get; set; }
        public ModelProvider Provider { get; set; }
        public string Model { get; set; }
        public int TokensUsed { get; set; }
    }
    
    // API Response DTOs
    internal class OpenAIResponse
    {
        public Choice[] Choices { get; set; }
        public Usage Usage { get; set; }
        
        public class Choice
        {
            public Message Message { get; set; }
        }
        
        public class Message
        {
            public string Content { get; set; }
        }
    }
    
    internal class AnthropicResponse
    {
        public ContentBlock[] Content { get; set; }
        public AnthropicUsage Usage { get; set; }
        
        public class ContentBlock
        {
            public string Text { get; set; }
        }
        
        public class AnthropicUsage
        {
            public int InputTokens { get; set; }
            public int OutputTokens { get; set; }
        }
    }
    
    internal class Usage
    {
        public int TotalTokens { get; set; }
    }
}
```

## Configuration (appsettings.json)

```json
{
  "OpenAI": {
    "ApiKey": "your-openai-key-here-or-use-keyvault"
  },
  "Anthropic": {
    "ApiKey": "your-anthropic-key-here-or-use-keyvault"
  },
  "AzureOpenAI": {
    "Endpoint": "https://your-resource.openai.azure.com",
    "ApiKey": "your-azure-key-here-or-use-managed-identity",
    "DeploymentName": "gpt-4"
  }
}
```

## Dependency Injection Setup

```csharp
using Microsoft.Extensions.DependencyInjection;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddPromptEngineering(this IServiceCollection services)
    {
        services.AddHttpClient<MultiModelClient>();
        services.AddSingleton<IPromptTemplateEngine, PromptTemplateEngine>();
        services.AddScoped<IPromptValidator, PromptValidator>();
        
        return services;
    }
}
```

## Usage Example

```csharp
public class PromptService
{
    private readonly MultiModelClient _client;
    private readonly ILogger<PromptService> _logger;
    
    public PromptService(MultiModelClient client, ILogger<PromptService> logger)
    {
        _client = client;
        _logger = logger;
    }
    
    public async Task<string> GenerateCodeReviewAsync(string code)
    {
        var request = new ModelRequest
        {
            Provider = ModelProvider.Anthropic,
            Model = "claude-3-opus-20240229",
            SystemPrompt = "You are an expert code reviewer for .NET/C# applications.",
            Prompt = $"Review this code and provide detailed feedback:\n\n{code}",
            Temperature = 0.3,
            MaxTokens = 2000
        };
        
        try
        {
            var response = await _client.CallAsync(request);
            _logger.LogInformation("Generated review using {Model}, tokens: {Tokens}", 
                response.Model, response.TokensUsed);
            
            return response.Content;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to generate code review");
            throw;
        }
    }
}
```

## Best Practices

1. **Use Dependency Injection**: Register clients and services in DI container.
2. **Environment Variables**: Never hardcode API keys; use configuration providers or Azure Key Vault.
3. **Logging**: Use `ILogger` for structured logging with correlation IDs.
4. **Async/Await**: All HTTP calls should be async.
5. **Cancellation Tokens**: Support cancellation for long-running operations.
6. **Error Handling**: Implement retry policies with Polly for transient failures.

## Related Patterns

- [OpenAI Function Calling](../openai/function-calling/openai-function-calling.md)
- [Anthropic Claude Patterns](../anthropic/claude_patterns.py)
