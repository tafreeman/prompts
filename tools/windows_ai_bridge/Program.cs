using Microsoft.Windows.AI;
using Microsoft.Windows.AI.Text;
using System.Text.Json;

namespace PhiSilicaBridge;

/// <summary>
/// Command-line bridge for Windows AI Phi Silica.
/// Called from Python via subprocess.
/// </summary>
class Program
{
    static async Task<int> Main(string[] args)
    {
        try
        {
            if (args.Length == 0 || args[0] == "--help" || args[0] == "-h")
            {
                PrintHelp();
                return args.Length == 0 ? 1 : 0;
            }

            if (args[0] == "--check")
            {
                return await CheckAvailability();
            }

            if (args[0] == "--info")
            {
                return await GetModelInfo();
            }

            // Generate text from prompt
            var prompt = string.Join(" ", args);
            return await GenerateText(prompt);
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"FATAL ERROR: {ex.Message}");
            return 1;
        }

        static void PrintHelp()
        {
            Console.WriteLine(@"PhiSilicaBridge - Windows AI Phi Silica CLI

Usage:
  PhiSilicaBridge <prompt>       Generate text from prompt
  PhiSilicaBridge --check        Check if Phi Silica is available
  PhiSilicaBridge --info         Get model information as JSON
  PhiSilicaBridge --help         Show this help

Requirements:
  - Windows 11 with NPU (Copilot+ PC)
  - Windows App SDK 1.8+

Example:
  PhiSilicaBridge ""Explain quantum computing in simple terms""
");
        }

        static async Task<int> CheckAvailability()
        {
            try
            {
                var state = LanguageModel.GetReadyState();
                Console.WriteLine(state == AIFeatureReadyState.Ready ? "AVAILABLE" : "NOT_AVAILABLE");
                return state == AIFeatureReadyState.Ready ? 0 : 1;
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"ERROR: {ex.Message}");
                return 1;
            }
        }

        static async Task<int> GetModelInfo()
        {
            try
            {
                var state = LanguageModel.GetReadyState();
                var info = new
                {
                    model = "phi-silica",
                    provider = "windows-ai",
                    available = state == AIFeatureReadyState.Ready,
                    readyState = state.ToString(),
                    platform = Environment.OSVersion.ToString(),
                    runtime = System.Runtime.InteropServices.RuntimeInformation.FrameworkDescription
                };

                Console.WriteLine(JsonSerializer.Serialize(info, new JsonSerializerOptions
                {
                    WriteIndented = true
                }));
                return 0;
            }
            catch (UnauthorizedAccessException)
            {
                Console.WriteLine(JsonSerializer.Serialize(new
                {
                    model = "phi-silica",
                    provider = "windows-ai",
                    available = false,
                    error = "Limited Access Feature - requires unlock token",
                    platform = Environment.OSVersion.ToString()
                }, new JsonSerializerOptions { WriteIndented = true }));
                return 1;
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"ERROR: {ex.Message}");
                return 1;
            }
        }

        static async Task<int> GenerateText(string prompt)
        {
            try
            {
                // Check if model is ready
                if (LanguageModel.GetReadyState() == AIFeatureReadyState.NotReady)
                {
                    Console.Error.WriteLine("[PhiSilica] Model not ready, initializing...");
                    await LanguageModel.EnsureReadyAsync();
                }

                Console.Error.WriteLine("[PhiSilica] Creating model...");
                using var languageModel = await LanguageModel.CreateAsync();

                Console.Error.WriteLine("[PhiSilica] Generating response...");
                var result = await languageModel.GenerateResponseAsync(prompt);

                Console.WriteLine(result.Text);
                return 0;
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"ERROR: {ex.Message}");

                // Provide helpful message for common errors
                if (ex.Message.Contains("not found") || ex.Message.Contains("not supported"))
                {
                    Console.Error.WriteLine(@"
Phi Silica requires:
  - Windows 11 Copilot+ PC with NPU
  - Windows App SDK 1.8+
  - Model may need to be downloaded first
");
                }
                return 1;
            }
        }
    }
}


