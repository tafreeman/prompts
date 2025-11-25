using System;
using System.ComponentModel;
using System.Threading.Tasks;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Microsoft.SemanticKernel.Planning.Handlebars;

namespace SemanticKernel.Examples
{
    /// <summary>
    /// Example showing how to set up Semantic Kernel with DI, plugins, and planners.
    /// </summary>
    public class SemanticKernelBootstrap
    {
        public static async Task RunAsync()
        {
            // 1. Setup Dependency Injection
            var services = new ServiceCollection();
            
            // Add Logging
            services.AddLogging(c => c.AddConsole().SetMinimumLevel(LogLevel.Information));
            
            // Add Semantic Kernel
            services.AddKernel()
                .AddAzureOpenAIChatCompletion(
                    deploymentName: "gpt-4",
                    endpoint: Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")!,
                    apiKey: Environment.GetEnvironmentVariable("AZURE_OPENAI_KEY")!
                );
                
            // Register Native Plugins as Services
            services.AddSingleton<EmailPlugin>();
            services.AddSingleton<CrmPlugin>();

            var sp = services.BuildServiceProvider();
            
            // 2. Get Kernel and Import Plugins
            var kernel = sp.GetRequiredService<Kernel>();
            
            // Import Native Plugins
            kernel.ImportPluginFromType<EmailPlugin>("Email");
            kernel.ImportPluginFromType<CrmPlugin>("CRM");
            
            // Import Semantic Plugins (Prompts)
            var skPrompt = @"
            Rewrite the following email to be more professional and polite.
            
            Email: {{$input}}
            
            Professional Version:
            ";
            
            kernel.CreateFunctionFromPrompt(skPrompt, 
                functionName: "PoliteRewrite", 
                description: "Rewrites text to be professional");

            // 3. Execute with Planner
            var planner = new HandlebarsPlanner();
            
            var goal = "Find the latest deal for customer 'Contoso', rewrite a follow-up email for them, and send it.";
            
            Console.WriteLine($"Goal: {goal}");
            
            try 
            {
                var plan = await planner.CreatePlanAsync(kernel, goal);
                Console.WriteLine("Plan created. Executing...");
                
                var result = await plan.InvokeAsync(kernel);
                Console.WriteLine($"Result: {result}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }
    }

    /// <summary>
    /// Example Native Plugin for CRM operations.
    /// </summary>
    public class CrmPlugin
    {
        [KernelFunction, Description("Retrieves the latest deal information for a customer")]
        public string GetLatestDeal([Description("Customer Name")] string customerName)
        {
            Console.WriteLine($"[CRM] Getting deal for {customerName}...");
            return $"Deal: Enterprise License Renewal, Value: $50k, Status: Negotiating";
        }
    }

    /// <summary>
    /// Example Native Plugin for Email operations.
    /// </summary>
    public class EmailPlugin
    {
        [KernelFunction, Description("Sends an email to a recipient")]
        public string SendEmail(
            [Description("The email content")] string content, 
            [Description("The recipient name")] string recipient)
        {
            Console.WriteLine($"[Email] Sending to {recipient}: {content}");
            return "Email sent successfully.";
        }
    }
}
