#!/usr/bin/env pwsh
# Run LATS Evaluation in Visible Terminal
# This script starts the LATS evaluation in a new terminal window you can monitor

param(
    [string]$Model = "ollama:phi4-reasoning",
    [string]$Folder = "advanced",
    [int]$MaxIterations = 3,
    [int]$Threshold = 80
)

Write-Host "Starting LATS Evaluation..." -ForegroundColor Green
Write-Host "Model: $Model" -ForegroundColor Cyan
Write-Host "Folder: $Folder" -ForegroundColor Cyan
Write-Host "Max Iterations: $MaxIterations" -ForegroundColor Cyan
Write-Host "Threshold: $Threshold%" -ForegroundColor Cyan
Write-Host ""

Set-Location "D:\source\prompts\tools"

python -u run_lats_improvement.py `
    --folder $Folder `
    --model $Model `
    --threshold $Threshold `
    --max-iterations $MaxIterations `
    --delay 1 `
    --verbose

Write-Host ""
Write-Host "Evaluation complete!" -ForegroundColor Green
Read-Host "Press Enter to close"
