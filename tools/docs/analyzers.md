# Analyzers

> **Prompt analysis and improvement tools** - 5-dimension scoring, AI-powered improvements, and audit reports.

---

## ⚡ Quick Start

```powershell
# Analyze prompts (5-dimension scoring)
python tools/analyzers/prompt_analyzer.py prompts/advanced/

# Generate improvement recommendations
python tools/improve_prompts.py prompts/ --worst 10

# Create audit report
python tools/audit_prompts.py prompts/ --output audit_report.csv
```

---

## Available Tools

| Tool | Purpose | Output |
| ------ | --------- | -------- |
| `prompt_analyzer.py` | 5-dimension scoring | Scorecard |
| `improve_prompts.py` | AI-powered improvements | Recommendations |
| `audit_prompts.py` | Migration/validation audit | CSV report |
| `scan_prompts_dual.py` | Dual scanning utility | Analysis |

---

## Prompt Analyzer

5-dimension scoring analysis for prompt quality assessment.

### Scoring Dimensions

| Dimension | Weight | Description |
| ----------- | -------- | ------------- |
| Clarity | 25% | Clear, unambiguous instructions |
| Effectiveness | 25% | Achieves intended outcome |
| Reusability | 20% | Works across contexts |
| Simplicity | 15% | Minimal complexity |
| Examples | 15% | Quality of included examples |

### CLI Usage

```powershell
# Analyze folder
python tools/analyzers/prompt_analyzer.py prompts/advanced/

# Generate markdown scorecard
python tools/analyzers/prompt_analyzer.py prompts/ --output scorecard.md

# JSON output for processing
python tools/analyzers/prompt_analyzer.py prompts/ --json -o analysis.json

# Verbose output
python tools/analyzers/prompt_analyzer.py prompts/developers/ -v
```

### Python API

```python
from tools.analyzers.prompt_analyzer import PromptAnalyzer

analyzer = PromptAnalyzer()

# Analyze single file
result = analyzer.analyze_file("prompts/example.md")
print(f"Overall Score: {result.overall_score}")
print(f"Clarity: {result.scores['clarity']}")
print(f"Effectiveness: {result.scores['effectiveness']}")

# Analyze folder
results = analyzer.analyze_folder("prompts/advanced/")
for r in results:
    print(f"{r.file}: {r.overall_score}")
```

---

## Prompt Improver

AI-powered improvement recommendations using LLMs.

### CLI Usage

```powershell
# Analyze and suggest improvements
python tools/improve_prompts.py prompts/

# Focus on worst-scoring prompts
python tools/improve_prompts.py prompts/ --worst 10

# Generate improvement prompts to folder
python tools/improve_prompts.py prompts/ --generate-prompts -o improvements/

# Use specific model
python tools/improve_prompts.py prompts/ --model phi4

# Dry run (show what would be improved)
python tools/improve_prompts.py prompts/ --dry-run
```

### Through prompt.py CLI

```powershell
python prompt.py improve prompts/basic/
python prompt.py improve prompts/advanced/react-pattern.md
```

### Python API

```python
from tools.improve_prompts import PromptImprover

improver = PromptImprover(model="local:phi4")

# Get improvement suggestions
suggestions = improver.analyze("prompts/example.md")
print(f"Issues Found: {len(suggestions.issues)}")
print(f"Recommendations: {suggestions.recommendations}")

# Generate improved version
improved = improver.improve("prompts/example.md")
print(improved.content)
```

---

## Audit Prompts

Generate CSV audit reports for migration and validation.

### CLI Usage

```powershell
# Generate audit report
python tools/audit_prompts.py prompts/ --output audit_report.csv

# Include scores
python tools/audit_prompts.py prompts/ --with-scores -o audit.csv

# Specific folder
python tools/audit_prompts.py prompts/developers/ -o developers_audit.csv
```

### Output Format

```csv
file,title,type,platforms,audience,word_count,has_examples,score
prompts/basic/greeting.md,Greeting,prompt,copilot,junior-engineer,150,true,85
prompts/advanced/react.md,React Pattern,pattern,all,senior-engineer,450,true,92
```

---

## Scan Prompts Dual

Dual scanning utility for comprehensive analysis.

```powershell
python tools/scan_prompts_dual.py prompts/
python tools/scan_prompts_dual.py prompts/advanced/ -v
```

---

## Workflow: Improve Low-Scoring Prompts

```powershell
# Step 1: Analyze all prompts
python tools/analyzers/prompt_analyzer.py prompts/ --json -o analysis.json

# Step 2: Get improvement suggestions for worst 10
python tools/improve_prompts.py prompts/ --worst 10 -o improvements/

# Step 3: Review and apply improvements
# (Manual step - review suggestions)

# Step 4: Re-analyze to verify improvements
python tools/analyzers/prompt_analyzer.py prompts/ --json -o analysis_after.json
```

---

## See Also

- [validators.md](./validators.md) - Validation tools
- [../prompteval/README.md](../prompteval/README.md) - Evaluation with LLMs
