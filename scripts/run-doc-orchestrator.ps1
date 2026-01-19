# run-doc-orchestrator.ps1
# Analyze all repository directories with GitHub Models
param(
    [string]$Model = "openai/gpt-4o",
    [string]$Temperature = "0.3",
    [string]$MaxTokens = "16000"
)

$dirs = @("tools", "agents", "toolkit", "testing", "frameworks", "_archive")

Write-Host "=== Repository Documentation Orchestrator ===" -ForegroundColor Cyan
Write-Host "Model: $Model" -ForegroundColor Yellow
Write-Host "Temperature: $Temperature"
Write-Host "Max Tokens: $MaxTokens"
Write-Host ""

# Create docs folder if needed
if (!(Test-Path "docs")) {
    New-Item -ItemType Directory -Path "docs" | Out-Null
    Write-Host "Created docs/ directory"
}

foreach ($dir in $dirs) {
    Write-Host "[$dir] Analyzing..." -ForegroundColor Green
    
    python prompt.py run archive/clutter/toolkit_prompts/orchestrator/repo-doc-orchestrator.md `
        -p gh -m $Model `
        --temperature $Temperature `
        --max-tokens $MaxTokens `
        -s "Analyze only: $dir/" `
        -o "docs/$dir-reference.md"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[$dir] ✅ Saved to docs/$dir-reference.md" -ForegroundColor Green
    } else {
        Write-Host "[$dir] ❌ Failed (rate limit?)" -ForegroundColor Red
    }
    
    Start-Sleep -Seconds 5  # Rate limit buffer
}

Write-Host ""
Write-Host "=== Done! ===" -ForegroundColor Cyan
Write-Host "Output files in docs/:"
Get-ChildItem docs/*-reference.md | ForEach-Object { Write-Host "  - $($_.Name)" }
