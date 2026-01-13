#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Run comprehensive evaluations on advanced prompts using local Ollama models
.DESCRIPTION
    Executes both PromptEval (Tier 2 - Local G-Eval) and LATS improvement
    evaluations on the prompts/advanced/ folder using only local models.
    No cloud services or paid APIs required.
.EXAMPLE
    .\run-advanced-eval-local.ps1
.EXAMPLE
    .\run-advanced-eval-local.ps1 -SkipPromptEval
.EXAMPLE
    .\run-advanced-eval-local.ps1 -Model "qwen2.5-coder:14b"
#>

[CmdletBinding()]
param(
    [Parameter(HelpMessage="Skip PromptEval and only run LATS")]
    [switch]$SkipPromptEval,
    
    [Parameter(HelpMessage="Skip LATS and only run PromptEval")]
    [switch]$SkipLATS,
    
    [Parameter(HelpMessage="Specific Ollama model to use (auto-detects best if not specified)")]
    [string]$Model = "",
    
    [Parameter(HelpMessage="Maximum LATS iterations per prompt")]
    [int]$MaxIterations = 3,
    
    [Parameter(HelpMessage="Quality threshold percentage")]
    [int]$Threshold = 80,
    
    [Parameter(HelpMessage="Verbose output")]
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# UTF-8 encoding for console
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚀 ADVANCED PROMPTS EVALUATION - LOCAL MODELS ONLY           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# ============================================================================
# PRE-FLIGHT CHECKS
# ============================================================================

Write-Host "[1/5] 🔍 Checking prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Error "Python not found. Install Python 3.11+ and add to PATH."
    exit 1
}

# Check Ollama service
Write-Host "   Checking Ollama service..." -ForegroundColor Gray
try {
    $ollamaTest = ollama list 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Ollama not responding"
    }
    Write-Host "   ✓ Ollama: Running" -ForegroundColor Green
} catch {
    Write-Error @"
Ollama service not running or not installed.

To install Ollama:
1. Download from: https://ollama.ai/download
2. Run: ollama serve
3. Pull models: ollama pull qwen2.5-coder:14b

Then re-run this script.
"@
    exit 1
}

# Detect available models
Write-Host "`n[2/5] 🤖 Detecting available local models..." -ForegroundColor Yellow
$availableModels = @()
$modelPriority = @(
    "qwen2.5-coder:14b",      # Fast, code-focused, 14B params
    "phi4-reasoning:latest",   # Good reasoning, 14B params
    "deepseek-r1:14b",        # Excellent but slower
    "qwen2.5-coder:7b",       # Faster fallback
    "phi4:latest"             # Smaller fallback
)

foreach ($modelName in $modelPriority) {
    if ($ollamaTest -match [regex]::Escape($modelName)) {
        $availableModels += $modelName
        Write-Host "   ✓ Found: $modelName" -ForegroundColor Green
    }
}

if ($availableModels.Count -eq 0) {
    Write-Error @"
No suitable models found in Ollama.

Recommended models for this evaluation:
- qwen2.5-coder:14b  (BEST - Fast + Smart)
- phi4-reasoning     (Good reasoning)
- deepseek-r1:14b    (Excellent but slow)

Pull a model with:
    ollama pull qwen2.5-coder:14b
"@
    exit 1
}

# Select model
if ($Model -and ($availableModels -contains $Model)) {
    $selectedModel = $Model
    Write-Host "`n   🎯 Using specified model: $selectedModel" -ForegroundColor Cyan
} elseif ($Model) {
    Write-Warning "   ⚠️  Specified model '$Model' not found. Auto-selecting..."
    $selectedModel = $availableModels[0]
    Write-Host "   🎯 Auto-selected: $selectedModel" -ForegroundColor Cyan
} else {
    $selectedModel = $availableModels[0]
    Write-Host "`n   🎯 Auto-selected best model: $selectedModel" -ForegroundColor Cyan
}

# Count prompts
Write-Host "`n[3/5] 📊 Analyzing prompt library..." -ForegroundColor Yellow
$advancedPrompts = Get-ChildItem -Path "prompts\advanced\*.md" -File | Where-Object { $_.Name -notmatch "^(index|README)" }
$promptCount = $advancedPrompts.Count
Write-Host "   Found $promptCount advanced prompts to evaluate" -ForegroundColor Green

if ($promptCount -eq 0) {
    Write-Error "No prompts found in prompts/advanced/"
    exit 1
}

# Estimate duration
$estimatedMinutes = if (-not $SkipPromptEval -and -not $SkipLATS) {
    # Both: PromptEval ~1-2 min/prompt, LATS ~5-8 min/prompt
    [math]::Ceiling($promptCount * 8)
} elseif (-not $SkipLATS) {
    # LATS only: ~5-8 min/prompt
    [math]::Ceiling($promptCount * 7)
} else {
    # PromptEval only: ~1-2 min/prompt
    [math]::Ceiling($promptCount * 2)
}

Write-Host "   ⏱️  Estimated duration: $estimatedMinutes-$($estimatedMinutes + 10) minutes" -ForegroundColor Yellow

# ============================================================================
# EXECUTION CONFIRMATION
# ============================================================================

Write-Host "`n[4/5] 📋 Execution Plan:" -ForegroundColor Yellow
Write-Host "   Target: prompts/advanced/ ($promptCount prompts)" -ForegroundColor White
Write-Host "   Model: ollama:$selectedModel" -ForegroundColor White
if (-not $SkipPromptEval) {
    Write-Host "   ✓ PromptEval: Tier 2 (Local G-Eval)" -ForegroundColor Green
}
if (-not $SkipLATS) {
    Write-Host "   ✓ LATS: Improvement evaluation (max $MaxIterations iterations)" -ForegroundColor Green
}
Write-Host "   Threshold: ${Threshold}%" -ForegroundColor White
Write-Host "   Incremental saving: ENABLED (no data loss on crashes)" -ForegroundColor Green

Write-Host "`n   Press ENTER to continue or Ctrl+C to cancel..." -ForegroundColor Cyan
$null = Read-Host

# ============================================================================
# EXECUTE EVALUATIONS
# ============================================================================

Write-Host "`n[5/5] 🎬 Starting evaluation..." -ForegroundColor Yellow
$startTime = Get-Date
$results = @{
    PromptEval = $null
    LATS = $null
}

# PromptEval - Tier 2 (Local G-Eval)
if (-not $SkipPromptEval) {
    Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║  📊 PHASE 1: PromptEval (Tier 2 - Local G-Eval)              ║" -ForegroundColor Magenta
    Write-Host "╚════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Magenta
    
    $promptEvalArgs = @(
        "-m", "prompteval",
        "..\prompts\advanced",
        "--tier", "2"
    )
    
    if ($Verbose) {
        $promptEvalArgs += "--verbose"
    }
    
    try {
        Push-Location "tools"
        Write-Host "Command: python $($promptEvalArgs -join ' ')`n" -ForegroundColor Gray
        
        python @promptEvalArgs
        
        if ($LASTEXITCODE -eq 0) {
            $results.PromptEval = "✅ SUCCESS"
            Write-Host "`n✅ PromptEval completed successfully!" -ForegroundColor Green
        } else {
            $results.PromptEval = "⚠️ COMPLETED WITH ERRORS (Exit code: $LASTEXITCODE)"
            Write-Warning "PromptEval completed with errors. Check logs above."
        }
    } catch {
        $results.PromptEval = "❌ FAILED: $($_.Exception.Message)"
        Write-Error "PromptEval failed: $_"
    } finally {
        Pop-Location
    }
    
    Write-Host "`n" + ("─" * 65) -ForegroundColor Gray
    Write-Host "Pausing 5 seconds before LATS evaluation..." -ForegroundColor Gray
    Start-Sleep -Seconds 5
}

# LATS Improvement Evaluation
if (-not $SkipLATS) {
    Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║  🔄 PHASE 2: LATS Improvement Evaluation                      ║" -ForegroundColor Magenta
    Write-Host "╚════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Magenta
    
    $latsArgs = @(
        "tools\run_lats_improvement.py",
        "prompts\advanced",
        "--model", "ollama:$selectedModel",
        "--threshold", $Threshold,
        "--max-iterations", $MaxIterations,
        "--output", "results\lats-advanced-$(Get-Date -Format 'yyyy-MM-dd-HHmm').json"
    )
    
    if ($Verbose) {
        $latsArgs += "--verbose"
    }
    
    try {
        Write-Host "Command: python $($latsArgs -join ' ')`n" -ForegroundColor Gray
        Write-Host "💾 Progress will be saved incrementally to results/ folder" -ForegroundColor Cyan
        Write-Host "   You can monitor progress in real-time by opening the JSON file`n" -ForegroundColor Cyan
        
        python @latsArgs
        
        if ($LASTEXITCODE -eq 0) {
            $results.LATS = "✅ SUCCESS"
            Write-Host "`n✅ LATS evaluation completed successfully!" -ForegroundColor Green
        } else {
            $results.LATS = "⚠️ COMPLETED WITH ERRORS (Exit code: $LASTEXITCODE)"
            Write-Warning "LATS evaluation completed with errors. Check logs above."
        }
    } catch {
        $results.LATS = "❌ FAILED: $($_.Exception.Message)"
        Write-Error "LATS evaluation failed: $_"
    }
}

# ============================================================================
# FINAL SUMMARY
# ============================================================================

$endTime = Get-Date
$duration = $endTime - $startTime
$durationMinutes = [math]::Round($duration.TotalMinutes, 1)

Write-Host "`n`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  📊 EVALUATION SUMMARY                                         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "Target:        prompts/advanced/ ($promptCount prompts)" -ForegroundColor White
Write-Host "Model:         ollama:$selectedModel" -ForegroundColor White
Write-Host "Duration:      $durationMinutes minutes" -ForegroundColor White
Write-Host "Timestamp:     $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor White

Write-Host "`nResults:" -ForegroundColor Yellow
if (-not $SkipPromptEval) {
    $color = if ($results.PromptEval -match "SUCCESS") { "Green" } elseif ($results.PromptEval -match "ERRORS") { "Yellow" } else { "Red" }
    Write-Host "  PromptEval:  $($results.PromptEval)" -ForegroundColor $color
}
if (-not $SkipLATS) {
    $color = if ($results.LATS -match "SUCCESS") { "Green" } elseif ($results.LATS -match "ERRORS") { "Yellow" } else { "Red" }
    Write-Host "  LATS:        $($results.LATS)" -ForegroundColor $color
}

Write-Host "`nOutput Locations:" -ForegroundColor Yellow
if (-not $SkipPromptEval) {
    Write-Host "  📄 PromptEval logs: results/eval-logs/$(Get-Date -Format 'yyyy-MM-dd').jsonl" -ForegroundColor Cyan
}
if (-not $SkipLATS) {
    $latsFiles = Get-ChildItem -Path "results\lats-advanced-*.json" -ErrorAction SilentlyContinue | 
                 Sort-Object LastWriteTime -Descending | 
                 Select-Object -First 1
    if ($latsFiles) {
        Write-Host "  📄 LATS results:    $($latsFiles.FullName)" -ForegroundColor Cyan
    }
}

Write-Host "`n✨ Evaluation complete! Review the results above." -ForegroundColor Green
Write-Host ""
