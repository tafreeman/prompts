# Test Evaluation Setup Script
# This script tests all configured models and APIs

Write-Host "🔍 Testing Evaluation Setup..." -ForegroundColor Cyan
Write-Host ""

# Load environment variables from .env
Write-Host "📋 Loading .env configuration..." -ForegroundColor Yellow
$envFile = Join-Path $PSScriptRoot ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^([A-Z_][A-Z0-9_]*)=(.*)$') {
            $key = $matches[1]
            $value = $matches[2]
            [Environment]::SetEnvironmentVariable($key, $value, 'Process')
            Write-Host "  ✓ $key" -ForegroundColor Green
        }
    }
    Write-Host ""
} else {
    Write-Host "  ⚠️  .env file not found" -ForegroundColor Yellow
    Write-Host ""
}

# Test 1: Local ONNX Models
Write-Host "🧪 Test 1: Local ONNX Models (FREE)" -ForegroundColor Cyan
Write-Host "  Running: prompteval with local phi4..." -ForegroundColor Gray
Set-Location tools
$result = python -m prompteval ../prompts/advanced/chain-of-thought-concise.md --models phi4 --runs 1 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Local models working!" -ForegroundColor Green
} else {
    Write-Host "  ❌ Local models failed" -ForegroundColor Red
}
Write-Host ""

# Test 2: GitHub Models
Write-Host "🧪 Test 2: GitHub Models (Cloud)" -ForegroundColor Cyan
if ($env:GITHUB_TOKEN) {
    Write-Host "  Token found: $($env:GITHUB_TOKEN.Substring(0, 10))..." -ForegroundColor Gray
    Write-Host "  Running: prompteval with gpt-4o-mini..." -ForegroundColor Gray
    $result = python -m prompteval ../prompts/advanced/chain-of-thought-concise.md --models gpt-4o-mini --runs 1 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ GitHub Models working!" -ForegroundColor Green
    } else {
        Write-Host "  ❌ GitHub Models failed" -ForegroundColor Red
        Write-Host "  Error: $result" -ForegroundColor Red
    }
} else {
    Write-Host "  ⚠️  GITHUB_TOKEN not set - skipping" -ForegroundColor Yellow
}
Write-Host ""

# Test 3: Windows AI / Phi Silica
Write-Host "🧪 Test 3: Windows AI / Phi Silica (NPU)" -ForegroundColor Cyan
if ($env:PHI_SILICA_LAF_TOKEN) {
    Write-Host "  LAF Token configured" -ForegroundColor Gray
    Set-Location ../tools/windows_ai_bridge
    $info = dotnet run -- --info 2>&1 | ConvertFrom-Json
    if ($info.available) {
        Write-Host "  ✅ Phi Silica available!" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Phi Silica unavailable" -ForegroundColor Yellow
        Write-Host "  Reason: $($info.error)" -ForegroundColor Gray
        Write-Host "  LAF Status: $($info.laf.status)" -ForegroundColor Gray
        if ($info.laf.status -eq "Unavailable") {
            Write-Host ""
            Write-Host "  ℹ️  This may be expected if:" -ForegroundColor Cyan
            Write-Host "     - Device doesn't have NPU (Copilot+ PC)" -ForegroundColor Gray
            Write-Host "     - Windows version doesn't support Phi Silica" -ForegroundColor Gray
            Write-Host "     - Additional app packaging required" -ForegroundColor Gray
        }
    }
    Set-Location ../../tools
} else {
    Write-Host "  ⚠️  PHI_SILICA_LAF_TOKEN not set - skipping" -ForegroundColor Yellow
}
Write-Host ""

# Test 4: Azure OpenAI
Write-Host "🧪 Test 4: Azure OpenAI" -ForegroundColor Cyan
if ($env:AZURE_OPENAI_API_KEY_0) {
    Write-Host "  ✅ Azure OpenAI key configured" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  AZURE_OPENAI_API_KEY_0 not set" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "✅ SUMMARY" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "Available for evaluation:" -ForegroundColor Cyan
Write-Host "  • Local ONNX models (phi4, mistral, phi3.5)" -ForegroundColor Green
if ($env:GITHUB_TOKEN) {
    Write-Host "  • GitHub Models (gpt-4o-mini, gpt-4.1, llama-70b)" -ForegroundColor Green
}
if ($env:AZURE_OPENAI_API_KEY_0) {
    Write-Host "  • Azure OpenAI" -ForegroundColor Green
}
Write-Host ""

# Recommended next steps
Write-Host "🎯 RECOMMENDED EVALUATION STRATEGY:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  Quick Local Check (FREE, ~60s):" -ForegroundColor Yellow
Write-Host "   python -m prompteval ../prompts/advanced/ --tier 2" -ForegroundColor White
Write-Host ""
Write-Host "2️⃣  Local Cross-Validation (FREE, ~5min per prompt):" -ForegroundColor Yellow
Write-Host "   python -m prompteval ../prompts/advanced/ --tier 3" -ForegroundColor White
Write-Host ""
if ($env:GITHUB_TOKEN) {
    Write-Host "3️⃣  Cloud Validation (~$0.10 per prompt):" -ForegroundColor Yellow
    Write-Host "   python -m prompteval ../prompts/advanced/ --tier 5" -ForegroundColor White
    Write-Host ""
    Write-Host "4️⃣  Premium Mixed (local + cloud, ~$0.30 per prompt):" -ForegroundColor Yellow
    Write-Host "   python -m prompteval ../prompts/critical/ --tier 6" -ForegroundColor White
    Write-Host ""
}

Write-Host "📚 See eval-strategy.md for complete guide" -ForegroundColor Cyan
Write-Host ""

Set-Location ..
