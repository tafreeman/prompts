# Comprehensive Evaluation Strategy

## ✅ Setup Status

**Your Environment:**
- ✅ **Local ONNX Models**: phi4, mistral, phi3.5 (FREE)
- ✅ **GitHub Models**: gpt-4o-mini, gpt-4.1, llama-70b (configured)
- ✅ **Azure OpenAI**: Configured
- ⚠️ **Phi Silica (AMD NPU)**: Hardware detected, LAF configured, but currently unavailable (AMD support pending)

See [tools/windows_ai_bridge/PHI_SILICA_STATUS.md](tools/windows_ai_bridge/PHI_SILICA_STATUS.md) for Phi Silica details.

---

## Overview
This strategy balances **local** (free, CPU-based) and **cloud** (GitHub Models) evaluations across different tiers to get thorough coverage without excessive cost.

---

## Phase 1: Local Triage (FREE - ~6 minutes)

### Tier 0: Instant Structural Check
```bash
cd tools
python -m prompteval ../prompts/ --tier 0 -o ../results/tier0-structural.json
```
**What it does:** Static analysis only - checks frontmatter, structure, formatting  
**Cost:** $0 | **Time:** <1s per prompt  
**Use case:** Quick filter before deeper evaluation

---

### Tier 2: Local G-Eval (Recommended Baseline)
```bash
cd tools
python -m prompteval ../prompts/advanced/ --tier 2 -o ../results/tier2-geval.json --verbose
```
**What it does:** Single local model (phi4) with G-Eval reasoning  
**Cost:** $0 | **Time:** ~60s per prompt  
**Use case:** Standard quality check during development

---

### Tier 3: Local Cross-Validation
```bash
cd tools
python -m prompteval ../prompts/advanced/ --tier 3 -o ../results/tier3-cross-local.json --verbose
```
**Models:** phi4, mistral, phi3.5 (2 runs each = 6 evaluations per prompt)  
**Cost:** $0 | **Time:** ~5min per prompt  
**Use case:** Pre-commit validation, confidence check

---

## Phase 2: Cloud Validation ($$$ - ~35s + API costs)

### Tier 4: Cloud Quick Check
```bash
cd tools
export GITHUB_TOKEN=ghp_your_token_here  # Set your token first
python -m prompteval ../prompts/advanced/ --tier 4 -o ../results/tier4-cloud-quick.json --verbose
```
**Model:** gpt-4o-mini (1 run)  
**Cost:** ~$0.01 per prompt | **Time:** ~5s per prompt  
**Use case:** Fast cloud baseline, compare to local scores

---

### Tier 5: Cloud Cross-Validation
```bash
cd tools
python -m prompteval ../prompts/advanced/ --tier 5 -o ../results/tier5-cloud-cross.json --verbose
```
**Models:** gpt-4o-mini, gpt-4.1, llama-70b (2 runs each = 6 evaluations)  
**Cost:** ~$0.10 per prompt | **Time:** ~30s per prompt  
**Use case:** Release candidate validation

---

## Phase 3: Premium/Enterprise ($$$ - High confidence)

### Tier 6: Premium Mixed Validation
```bash
cd tools
python -m prompteval ../prompts/critical/ --tier 6 -o ../results/tier6-premium.json --verbose
```
**Models:** phi4, mistral, gpt-4o-mini, gpt-4.1, llama-70b (3 runs each = 15 evaluations)  
**Mix:** 2 local + 3 cloud  
**Cost:** ~$0.30 per prompt | **Time:** ~2min per prompt  
**Use case:** Production-ready prompts, critical workflows

---

### Tier 7: Enterprise Full Pipeline
```bash
cd tools
python -m prompteval ../prompts/production/ --tier 7 -o ../results/tier7-enterprise.json --verbose
```
**Models:** phi4, mistral, gpt-4o-mini, gpt-4.1, llama-70b (4 runs each = 20 evaluations)  
**Mix:** 2 local + 3 cloud  
**Cost:** ~$0.50 per prompt | **Time:** ~5min per prompt  
**Use case:** Mission-critical prompts, maximum confidence

---

## Recommended Workflow

### 🚀 Quick Development Cycle
```bash
# While editing
python -m prompteval prompt.md --tier 0  # Instant check
python -m prompteval prompt.md --tier 2  # Local G-Eval
```

### ✅ Pre-Commit Validation
```bash
# Before commit
python -m prompteval $(git diff --name-only --cached | grep '\.md$') --tier 3 --ci
```

### 🎯 Release Preparation
```bash
# Sample testing with cloud validation
python -m prompteval prompts/new-feature/ --tier 4  # Cloud quick
python -m prompteval prompts/new-feature/ --tier 5  # Cloud cross-validate
```

### 🏆 Production Deployment
```bash
# Full validation for critical prompts
python -m prompteval prompts/production/ --tier 6 --ci --threshold 80
```

---

## Custom Mix: Balanced Evaluation

For a custom balance of local + cloud without using preset tiers:

```bash
# Local diversity + Cloud baseline
cd tools
python -m prompteval ../prompts/advanced/ \
  --models phi4,mistral,phi3.5,gpt-4o-mini \
  --runs 2 \
  -o ../results/custom-balanced.json

# Heavy cloud mix
python -m prompteval ../prompts/critical/ \
  --models gpt-4o-mini,gpt-4.1,llama-70b,mistral-small \
  --runs 3 \
  -o ../results/custom-cloud-heavy.json

# All local (maximum free validation)
python -m prompteval ../prompts/ \
  --all-local \
  --runs 3 \
  -o ../results/all-local-deep.json
```

---

## Cost Estimation

| Scope | Tier | Prompts | Cost | Time |
|-------|------|---------|------|------|
| Single prompt | 0-3 | 1 | $0 | <6min |
| Single prompt | 4 | 1 | ~$0.01 | ~5s |
| Single prompt | 5 | 1 | ~$0.10 | ~30s |
| Single prompt | 6-7 | 1 | ~$0.30-0.50 | ~2-5min |
| Advanced folder (20) | 2 | 20 | $0 | ~20min |
| Advanced folder (20) | 3 | 20 | $0 | ~2hrs |
| Advanced folder (20) | 5 | 20 | ~$2.00 | ~10min |
| Full library (100+) | 2 | 100 | $0 | ~2hrs |
| Full library (100+) | 5 | 100 | ~$10 | ~50min |

---

## Batch Evaluation Script

Create a thorough evaluation sweep:

```bash
#!/bin/bash
# eval-sweep.sh - Comprehensive evaluation across tiers

PROMPT_DIR="../prompts/advanced"
OUTPUT_DIR="../results/sweep-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo "🔍 Starting comprehensive evaluation sweep..."

# Phase 1: Local (FREE)
echo "Phase 1: Local evaluation..."
python -m prompteval "$PROMPT_DIR" --tier 0 -o "$OUTPUT_DIR/tier0-structural.json"
python -m prompteval "$PROMPT_DIR" --tier 2 -o "$OUTPUT_DIR/tier2-geval.json" --verbose
python -m prompteval "$PROMPT_DIR" --tier 3 -o "$OUTPUT_DIR/tier3-local-cross.json" --verbose

# Phase 2: Cloud validation (requires token)
if [ -n "$GITHUB_TOKEN" ]; then
  echo "Phase 2: Cloud validation..."
  python -m prompteval "$PROMPT_DIR" --tier 4 -o "$OUTPUT_DIR/tier4-cloud-quick.json" --verbose
  python -m prompteval "$PROMPT_DIR" --tier 5 -o "$OUTPUT_DIR/tier5-cloud-cross.json" --verbose
else
  echo "⚠️  Skipping cloud tiers (GITHUB_TOKEN not set)"
fi

echo "✅ Evaluation complete! Results in: $OUTPUT_DIR"
```

**PowerShell version:**
```powershell
# eval-sweep.ps1
$PromptDir = "..\prompts\advanced"
$OutputDir = "..\results\sweep-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
New-Item -ItemType Directory -Path $OutputDir -Force

Write-Host "🔍 Starting comprehensive evaluation sweep..."

# Phase 1: Local (FREE)
Write-Host "Phase 1: Local evaluation..."
python -m prompteval $PromptDir --tier 0 -o "$OutputDir\tier0-structural.json"
python -m prompteval $PromptDir --tier 2 -o "$OutputDir\tier2-geval.json" --verbose
python -m prompteval $PromptDir --tier 3 -o "$OutputDir\tier3-local-cross.json" --verbose

# Phase 2: Cloud validation
if ($env:GITHUB_TOKEN) {
  Write-Host "Phase 2: Cloud validation..."
  python -m prompteval $PromptDir --tier 4 -o "$OutputDir\tier4-cloud-quick.json" --verbose
  python -m prompteval $PromptDir --tier 5 -o "$OutputDir\tier5-cloud-cross.json" --verbose
} else {
  Write-Host "⚠️  Skipping cloud tiers (GITHUB_TOKEN not set)"
}

Write-Host "✅ Evaluation complete! Results in: $OutputDir"
```

---

## Model Selection Rationale

### Local Models (FREE, CPU/ONNX)
- **phi4/phi4mini** - Fast, Microsoft's latest small model, good baseline
- **mistral** - Strong open-source alternative, different architecture
- **phi3.5** - Slightly older but stable, good for cross-validation

### Cloud Models (GitHub Models, API cost)
- **gpt-4o-mini** - Fast, cheap, OpenAI baseline (~$0.003/prompt)
- **gpt-4.1** - Higher quality OpenAI model for validation
- **llama-70b** - Large open-source model, different training/perspective
- **mistral-small** - Good mid-tier alternative

### Mix Strategy
- **Development:** Tiers 0-3 (all local, free)
- **Validation:** Tier 4-5 (cloud quick check)
- **Production:** Tier 6-7 (mixed local+cloud, high confidence)

---

## Next Steps

1. **Start with local triage:**
   ```bash
   cd tools
   python -m prompteval ../prompts/advanced/ --tier 2 -v
   ```

2. **Set up GitHub token for cloud:**
   ```bash
   export GITHUB_TOKEN=ghp_xxxxx
   # or in PowerShell: $env:GITHUB_TOKEN="ghp_xxxxx"
   ```

3. **Run balanced evaluation:**
   ```bash
   python -m prompteval ../prompts/advanced/ --tier 5 -v
   ```

4. **Compare results:**
   ```bash
   # Generate comparison report
   python -c "
   import json
   t2 = json.load(open('../results/tier2-geval.json'))
   t5 = json.load(open('../results/tier5-cloud-cross.json'))
   print(f'Local avg: {t2[\"avg_score\"]:.1f}%')
   print(f'Cloud avg: {t5[\"avg_score\"]:.1f}%')
   print(f'Delta: {abs(t2[\"avg_score\"] - t5[\"avg_score\"]):.1f}%')
   "
   ```

---

## Key Insights

### Local vs Cloud Score Calibration
- Local models (ONNX) tend to score **3-5 points higher** than cloud models
- Use local for **triage/development** (fast feedback)
- Use cloud for **final scores** (production decisions)
- Tier 6-7 **mixes both** for best confidence

### When to Use Each Compute Type

**Local (CPU/ONNX):**
- ✅ Rapid iteration during development
- ✅ Bulk evaluation of entire library
- ✅ CI/CD pre-commit checks
- ✅ No API costs or rate limits

**Cloud (GitHub Models):**
- ✅ Final validation before release
- ✅ Cross-reference local scores
- ✅ Different model architectures
- ✅ Higher quality models (GPT-4, Llama-70B)

**Mixed (Tier 6-7):**
- ✅ Production deployment
- ✅ Critical prompts
- ✅ Maximum confidence
- ✅ Reproducibility checks
