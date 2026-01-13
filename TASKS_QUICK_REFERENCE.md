# Quick Evaluation Tasks

All evaluation tasks are now available in VS Code Tasks menu!

## Access Tasks

**Two ways to run:**

1. **Command Palette** (Ctrl+Shift+P / Cmd+Shift+P):
   - Type: `Tasks: Run Task`
   - Select from the menu

2. **Keyboard Shortcut**:
   - Windows/Linux: `Ctrl+Shift+B`
   - Mac: `Cmd+Shift+B`

---

## 📂 Per-Folder Evaluation Tasks

Each folder has a dedicated task with **verbose output** and **CI mode** (shows failures):

### Available Folder Tasks:

| Task Name | Folder | Tier | Flags |
|-----------|--------|------|-------|
| 📂 Eval: Advanced Folder | `prompts/advanced/` | 2 | `--verbose --ci` |
| 📂 Eval: Analysis Folder | `prompts/analysis/` | 2 | `--verbose --ci` |
| 📂 Eval: Business Folder | `prompts/business/` | 2 | `--verbose --ci` |
| 📂 Eval: Creative Folder | `prompts/creative/` | 2 | `--verbose --ci` |
| 📂 Eval: Developers Folder | `prompts/developers/` | 2 | `--verbose --ci` |
| 📂 Eval: Governance Folder | `prompts/governance/` | 2 | `--verbose --ci` |
| 📂 Eval: M365 Folder | `prompts/m365/` | 2 | `--verbose --ci` |
| 📂 Eval: SOCMINT Folder | `prompts/socmint/` | 2 | `--verbose --ci` |
| 📂 Eval: System Folder | `prompts/system/` | 2 | `--verbose --ci` |

**Features:**
- ✅ **Verbose output** - See detailed per-criterion scores
- ✅ **CI mode** - Task fails if any prompts fail (threshold < 70%)
- ✅ **Dedicated panel** - Each task opens in its own terminal
- ✅ **Clickable** - One-click execution from Tasks menu

---

## 🚀 Bulk Evaluation Tasks

### Full Library Evaluations:

| Task Name | Scope | Tier | Output |
|-----------|-------|------|--------|
| 🚀 Eval: All Folders - Tier 2 | All prompts | 2 (Local G-Eval) | `results/full-eval-tier2.json` |
| 🔥 Eval: All Folders - Tier 3 | All prompts | 3 (Cross-Validate) | `results/full-eval-tier3.json` |
| ☁️ Eval: All Folders - Tier 5 | All prompts | 5 (Cloud) | `results/full-eval-tier5.json` |

---

## 📊 Standard Tier Tasks

General-purpose tasks with folder picker:

| Task Name | Description |
|-----------|-------------|
| 📊 Eval: Run Tiered Evaluation | Interactive folder + tier picker |
| 📊 Eval: Tier 0 - Structural Only | Instant structural check |
| 📊 Eval: Tier 1 - Local Quick | Single local model |
| 📊 Eval: Tier 2 - Local G-Eval | Default evaluation |
| 📊 Eval: Tier 3 - Local Cross-Validate | 3 models × 2 runs |
| 📊 Eval: Tier 4 - Cloud Quick | gpt-4o-mini |
| 📊 Eval: Tier 5 - Cloud Cross-Validate | 3 cloud models |
| 📊 Eval: Current File Only | Evaluate currently open file |

---

## 🔍 Diagnostic Tasks

| Task Name | Description |
|-----------|-------------|
| 📋 Eval: List All Tiers | Show tier configurations |
| 📋 Eval: List Available Models | Show configured models |
| 🔍 Validate All Prompts | Validate frontmatter/structure |
| 📈 Analyze Prompt Library | Generate analysis report |
| 🧪 Run Python Tests | Run pytest suite |

---

## Typical Workflow

### 1. **Quick Check** (for development)
   - Run: `📂 Eval: Advanced Folder` (or your working folder)
   - Duration: ~2-3 minutes per prompt
   - Cost: FREE (local phi4)

### 2. **Pre-Commit Validation**
   - Run: `📂 Eval: [Your Folder]` with `--ci` flag
   - Fails if any prompt scores < 70%
   - Fix issues before committing

### 3. **Full Library Check**
   - Run: `🚀 Eval: All Folders - Tier 2`
   - Reviews entire library
   - Saves report to `results/`

### 4. **Release Validation**
   - Run: `🔥 Eval: All Folders - Tier 3`
   - Cross-validates with 3 models
   - Higher confidence before release

### 5. **Cloud Verification** (if GitHub token set)
   - Run: `☁️ Eval: All Folders - Tier 5`
   - Uses cloud models for final check
   - Cost: ~$0.10 per prompt

---

## Understanding Verbose Output

With `--verbose` flag, you'll see:

```
[1/10] prompt-name.md
  → phi4 (run 1/1) 
    Clarity: 90%
    Specificity: 85%
    Actionability: 88%
    Structure: 82%
    Completeness: 80%
    Safety: 87%
  ✓ 85.3%
  PASS -> 85.3% +/-0.0 (stable)
```

**Issue Detection:**
- ❌ Red scores = Below 50%
- ⚠️ Yellow scores = 50-70%
- ✅ Green scores = Above 70%

**CI Mode:**
- Task exit code 1 = Failures detected
- Task exit code 0 = All passed

---

## Quick Tips

1. **Run specific folder while editing:**
   - Open any prompt file
   - Press `Ctrl+Shift+B`
   - Select the folder task

2. **Watch for issues in real-time:**
   - Verbose output shows per-criterion scores
   - Identify weak areas immediately

3. **Save results for tracking:**
   - Bulk tasks auto-save to `results/`
   - Compare over time to track improvements

4. **Iterate quickly:**
   - Edit prompt
   - Run folder task
   - See updated scores
   - Repeat

---

## Troubleshooting

**Task not found?**
- Reload VS Code window (Ctrl+Shift+P → "Reload Window")

**Python module not found?**
- Ensure virtual environment is activated
- Run: `.venv\Scripts\Activate.ps1` (Windows)

**GitHub Models failing?**
- Check `GITHUB_TOKEN` environment variable
- Set in `.env` file: `GITHUB_TOKEN=ghp_...`

**Scores seem wrong?**
- Use `--verbose` to see criterion breakdown
- Compare Tier 2 (local) vs Tier 5 (cloud) for calibration

---

## What's Next?

- ✅ All folders have dedicated clickable tasks
- ✅ Verbose output enabled by default
- ✅ CI mode catches failures automatically
- ✅ Results saved to `results/` directory

**Try it now:**
1. Press `Ctrl+Shift+B`
2. Select `📂 Eval: Advanced Folder`
3. Watch the evaluation run!
