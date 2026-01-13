# =====================================================
# Run All Evaluation Phases (Ollama + Local)
# =====================================================
# This script runs a complete evaluation using the best
# available local models (Ollama + ONNX)

$PROMPT_DIR = "..\prompts\advanced"
$OUTPUT_DIR = "..\results"

# Ensure output directory exists
New-Item -ItemType Directory -Force -Path $OUTPUT_DIR | Out-Null

Write-Host "`n🚀 EVALUATION STRATEGY - ALL PHASES" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# =====================================================
# PHASE 1: LOCAL TRIAGE (Tiers 0-3)
# =====================================================

Write-Host "`n📋 PHASE 1: LOCAL TRIAGE" -ForegroundColor Yellow
Write-Host "Using: Ollama (deepseek-v3.2) + ONNX (mistral, phi4)`n" -ForegroundColor Yellow

# Tier 0: Structural Only (instant)
Write-Host "▶ Tier 0: Structural Analysis (instant)..." -ForegroundColor Green
python -m prompteval $PROMPT_DIR --tier 0 -o "$OUTPUT_DIR/phase1-tier0-structural.json" --verbose --ci

# Tier 1: Quick Check with best Ollama model
Write-Host "`n▶ Tier 1: Quick Check with DeepSeek V3..." -ForegroundColor Green
python -m prompteval $PROMPT_DIR --tier 1 --models deepseek-v3.2:cloud -o "$OUTPUT_DIR/phase1-tier1-quick.json" --verbose --ci

# Tier 2: G-Eval with DeepSeek V3
Write-Host "`n▶ Tier 2: G-Eval with DeepSeek V3..." -ForegroundColor Green
python -m prompteval $PROMPT_DIR --tier 2 --models deepseek-v3.2:cloud -o "$OUTPUT_DIR/phase1-tier2-geval.json" --verbose --ci

# Tier 3: Cross-validation with mixed models
Write-Host "`n▶ Tier 3: Cross-Validation (DeepSeek + Mistral + Phi4)..." -ForegroundColor Green
python -m prompteval $PROMPT_DIR --tier 3 --models deepseek-v3.2:cloud,mistral,phi4 --runs 2 -o "$OUTPUT_DIR/phase1-tier3-cross.json" --verbose --ci

# =====================================================
# PHASE 2: CLOUD VALIDATION (Tiers 4-5)
# =====================================================

Write-Host "`n`n☁️  PHASE 2: CLOUD VALIDATION" -ForegroundColor Cyan
Write-Host "Using: GitHub Models API (requires GITHUB_TOKEN)`n" -ForegroundColor Cyan

# Check if GITHUB_TOKEN is set
if ($env:GITHUB_TOKEN) {
    # Tier 4: Cloud Quick
    Write-Host "▶ Tier 4: Cloud Quick (DeepSeek R1)..." -ForegroundColor Green
    python -m prompteval $PROMPT_DIR --tier 4 --models deepseek-r1 -o "$OUTPUT_DIR/phase2-tier4-cloud-quick.json" --verbose --ci
    
    # Tier 5: Cloud Cross-Validation
    Write-Host "`n▶ Tier 5: Cloud Cross-Validation (3 models × 2 runs)..." -ForegroundColor Green
    python -m prompteval $PROMPT_DIR --tier 5 --models deepseek-r1,gpt-4o-mini,llama-70b --runs 2 -o "$OUTPUT_DIR/phase2-tier5-cloud-cross.json" --verbose --ci
} else {
    Write-Host "⚠️  GITHUB_TOKEN not set - skipping cloud validation" -ForegroundColor Yellow
    Write-Host "   Set GITHUB_TOKEN in .env to enable cloud evaluation" -ForegroundColor Yellow
}

# =====================================================
# SUMMARY
# =====================================================

Write-Host "`n`n✅ EVALUATION COMPLETE!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "`nResults saved to: $OUTPUT_DIR/" -ForegroundColor Cyan
Write-Host "`nGenerated files:" -ForegroundColor Cyan
Get-ChildItem $OUTPUT_DIR\phase*.json | ForEach-Object {
    $size = [math]::Round($_.Length / 1KB, 1)
    Write-Host "  📄 $($_.Name) ($size KB)" -ForegroundColor White
}

Write-Host "`n💡 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Review results in $OUTPUT_DIR/" -ForegroundColor White
Write-Host "  2. Compare Tier 3 (local) vs Tier 5 (cloud) for calibration" -ForegroundColor White
Write-Host "  3. Fix prompts scoring < 70%" -ForegroundColor White
Write-Host "  4. Re-run evaluation to verify improvements" -ForegroundColor White
Write-Host ""
