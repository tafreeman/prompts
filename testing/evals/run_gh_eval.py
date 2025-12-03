#!/usr/bin/env python3
"""
Run gh models eval and parse results into a readable report.

This script wraps `gh models eval` to provide better formatted output
and summary statistics from prompt evaluations.

Usage:
    python run_gh_eval.py testing/evals/developers-eval.prompt.yml
    python run_gh_eval.py testing/evals/*.prompt.yml --report report.md
"""

import argparse
import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional


def run_gh_models_eval(eval_file: str) -> Optional[Dict[str, Any]]:
    """Run gh models eval and return JSON results."""
    try:
        result = subprocess.run(
            ['gh', 'models', 'eval', eval_file, '--json'],
            capture_output=True,
            timeout=300,  # 5 minute timeout
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode != 0:
            print(f"Error running eval: {result.stderr}")
            return None
        
        if not result.stdout:
            print("No output from gh models eval")
            return None
        
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        print(f"Timeout running eval for {eval_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON output: {e}")
        return None
    except FileNotFoundError:
        print("Error: 'gh' command not found. Install GitHub CLI and gh-models extension.")
        return None


def parse_model_response(response: str) -> Dict[str, Any]:
    """Parse the model's JSON response from the evaluation."""
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to extract JSON from the response
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        return {}


# Pass/fail thresholds based on industry best practices
PASS_THRESHOLD = 7.0
MIN_CRITERION_SCORE = 5.0


def calculate_pass_fail(scores: Dict[str, int], overall: float) -> tuple:
    """Calculate pass/fail based on Promptfoo-style thresholds."""
    if overall < PASS_THRESHOLD:
        return False, f"Overall score {overall:.1f} < {PASS_THRESHOLD}"
    
    for criterion, score in scores.items():
        if score < MIN_CRITERION_SCORE:
            return False, f"{criterion} score {score} < {MIN_CRITERION_SCORE}"
    
    return True, "All criteria passed"


def extract_scores(results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract scores from all test results."""
    scores = []
    
    for test_result in results.get('testResults', []):
        test_case = test_result.get('testCase', {})
        model_response = test_result.get('modelResponse', '')
        
        parsed = parse_model_response(model_response)
        criterion_scores = parsed.get('scores', {})
        overall = parsed.get('overall_score', 0)
        
        # Calculate pass/fail if not provided by model
        model_pass = parsed.get('pass')
        if model_pass is None and criterion_scores:
            passed, reason = calculate_pass_fail(criterion_scores, overall)
        else:
            passed = model_pass
            reason = "Model evaluated" if model_pass else "Model failed"
        
        score_data = {
            'title': test_case.get('promptTitle', 'Unknown'),
            'category': test_case.get('category', 'unknown'),
            'difficulty': test_case.get('difficulty', 'unknown'),
            'scores': criterion_scores,
            'overall_score': overall,
            'grade': parsed.get('grade', 'N/A'),
            'pass': passed,
            'pass_reason': reason,
            'reasoning': parsed.get('reasoning', ''),
            'strengths': parsed.get('strengths', []),
            'improvements': parsed.get('improvements', []),
            'summary': parsed.get('summary', '')
        }
        scores.append(score_data)
    
    return scores


def print_results(scores: List[Dict[str, Any]], eval_name: str):
    """Print formatted results to console."""
    print(f"\n{'='*70}")
    print(f"📊 EVALUATION RESULTS: {eval_name}")
    print(f"{'='*70}\n")
    
    if not scores:
        print("No scores found!")
        return
    
    # Sort by overall score
    sorted_scores = sorted(scores, key=lambda x: x.get('overall_score', 0), reverse=True)
    
    # Print individual results
    for i, s in enumerate(sorted_scores, 1):
        grade = s.get('grade', 'N/A')
        overall = s.get('overall_score', 0)
        passed = s.get('pass', None)
        
        # Status emoji based on pass/fail
        if passed is True:
            status = '✅ PASS'
        elif passed is False:
            status = '❌ FAIL'
        else:
            status = '⚠️ N/A'
        
        # Grade emoji
        if grade.startswith('A'):
            emoji = '🏆'
        elif grade.startswith('B'):
            emoji = '✅'
        elif grade.startswith('C'):
            emoji = '🟡'
        else:
            emoji = '🔴'
        
        print(f"{i}. {emoji} {s['title']} [{status}]")
        print(f"   Score: {overall}/10 (Grade: {grade})")
        print(f"   Category: {s['category']} | Difficulty: {s['difficulty']}")
        
        # Individual scores - group by category
        if s.get('scores'):
            core = ['clarity', 'specificity', 'actionability', 'structure', 'completeness']
            advanced = ['factuality', 'consistency', 'safety']
            
            core_parts = [f"{k}: {v}" for k, v in s['scores'].items() if k in core]
            advanced_parts = [f"{k}: {v}" for k, v in s['scores'].items() if k in advanced]
            
            if core_parts:
                print(f"   Core: {' | '.join(core_parts)}")
            if advanced_parts:
                print(f"   Advanced: {' | '.join(advanced_parts)}")
        
        # Reasoning (chain-of-thought)
        if s.get('reasoning'):
            reasoning = s['reasoning'][:100] + '...' if len(s['reasoning']) > 100 else s['reasoning']
            print(f"   Reasoning: {reasoning}")
        
        # Summary
        if s.get('summary'):
            print(f"   Summary: {s['summary']}")
        
        print()
    
    # Print summary statistics
    overall_scores = [s.get('overall_score', 0) for s in scores if s.get('overall_score')]
    
    if overall_scores:
        avg = sum(overall_scores) / len(overall_scores)
        min_score = min(overall_scores)
        max_score = max(overall_scores)
        
        # Pass/fail counts
        passed_count = sum(1 for s in scores if s.get('pass') is True)
        failed_count = sum(1 for s in scores if s.get('pass') is False)
        
        print(f"{'-'*70}")
        print(f"📈 SUMMARY STATISTICS")
        print(f"{'-'*70}")
        print(f"   Prompts Evaluated: {len(scores)}")
        print(f"   Average Score: {avg:.1f}/10")
        print(f"   Highest Score: {max_score}/10")
        print(f"   Lowest Score: {min_score}/10")
        
        # Pass/Fail summary (Promptfoo-style)
        print(f"\n   Pass/Fail Results:")
        print(f"      ✅ Passed: {passed_count} ({100*passed_count/len(scores):.0f}%)")
        print(f"      ❌ Failed: {failed_count} ({100*failed_count/len(scores):.0f}%)")
        print(f"   Pass Threshold: >= {PASS_THRESHOLD}/10, no criterion < {MIN_CRITERION_SCORE}")
        
        # Grade distribution
        grades = [s.get('grade', 'N/A') for s in scores]
        grade_counts = {}
        for g in grades:
            grade_counts[g] = grade_counts.get(g, 0) + 1
        
        print(f"\n   Grade Distribution:")
        for grade, count in sorted(grade_counts.items()):
            print(f"      {grade}: {count} prompt(s)")
        
        # Criterion averages
        all_scores = {}
        for s in scores:
            for k, v in s.get('scores', {}).items():
                if k not in all_scores:
                    all_scores[k] = []
                all_scores[k].append(v)
        
        if all_scores:
            print(f"\n   Criterion Averages:")
            for criterion, vals in sorted(all_scores.items()):
                avg_crit = sum(vals) / len(vals)
                status = '✅' if avg_crit >= MIN_CRITERION_SCORE else '⚠️'
                print(f"      {status} {criterion}: {avg_crit:.1f}/10")


def generate_markdown_report(
    all_results: Dict[str, List[Dict[str, Any]]],
    output_path: str
):
    """Generate a markdown report from all evaluation results."""
    lines = [
        "# Prompt Library Evaluation Report",
        f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "> Based on industry best practices from OpenAI, Anthropic, Google, and Promptfoo",
        "",
        "## Summary",
        ""
    ]
    
    # Aggregate all scores
    all_scores = []
    for eval_name, scores in all_results.items():
        all_scores.extend(scores)
    
    if all_scores:
        overall_scores = [s.get('overall_score', 0) for s in all_scores if s.get('overall_score')]
        avg = sum(overall_scores) / len(overall_scores) if overall_scores else 0
        
        passed_count = sum(1 for s in all_scores if s.get('pass') is True)
        failed_count = sum(1 for s in all_scores if s.get('pass') is False)
        pass_rate = 100 * passed_count / len(all_scores) if all_scores else 0
        
        lines.extend([
            f"- **Total Prompts Evaluated:** {len(all_scores)}",
            f"- **Average Score:** {avg:.1f}/10",
            f"- **Pass Rate:** {pass_rate:.0f}% ({passed_count}/{len(all_scores)})",
            f"- **Pass Threshold:** >= {PASS_THRESHOLD}/10, no criterion < {MIN_CRITERION_SCORE}",
            f"- **Evaluations Run:** {len(all_results)}",
            ""
        ])
        
        # Criterion averages
        criterion_scores = {}
        for s in all_scores:
            for k, v in s.get('scores', {}).items():
                if k not in criterion_scores:
                    criterion_scores[k] = []
                criterion_scores[k].append(v)
        
        if criterion_scores:
            lines.extend([
                "### Criterion Averages",
                "",
                "| Criterion | Average | Status |",
                "|-----------|---------|--------|"
            ])
            for crit, vals in sorted(criterion_scores.items()):
                avg_crit = sum(vals) / len(vals)
                status = '✅ Pass' if avg_crit >= MIN_CRITERION_SCORE else '⚠️ Needs Work'
                lines.append(f"| {crit.title()} | {avg_crit:.1f}/10 | {status} |")
            lines.append("")
    
    # Results by evaluation
    for eval_name, scores in all_results.items():
        lines.extend([
            f"## {eval_name}",
            "",
            "| Prompt | Score | Grade | Pass | Summary |",
            "|--------|-------|-------|------|---------|"
        ])
        
        sorted_scores = sorted(scores, key=lambda x: x.get('overall_score', 0), reverse=True)
        
        for s in sorted_scores:
            title = s.get('title', 'Unknown')[:35]
            score = s.get('overall_score', 0)
            grade = s.get('grade', 'N/A')
            passed = '✅' if s.get('pass') else '❌'
            summary = s.get('summary', '')[:50] + ('...' if len(s.get('summary', '')) > 50 else '')
            
            lines.append(f"| {title} | {score}/10 | {grade} | {passed} | {summary} |")
        
        lines.append("")
    
    # Top performers
    if all_scores:
        lines.extend([
            "## Top Performers 🏆",
            ""
        ])
        
        top = sorted(all_scores, key=lambda x: x.get('overall_score', 0), reverse=True)[:5]
        for i, s in enumerate(top, 1):
            passed = '✅' if s.get('pass') else '❌'
            lines.append(f"{i}. **{s.get('title', 'Unknown')}** - {s.get('overall_score', 0)}/10 ({s.get('grade', 'N/A')}) {passed}")
        
        lines.append("")
    
    # Failed prompts (Promptfoo-style)
    failed = [s for s in all_scores if s.get('pass') is False]
    if failed:
        lines.extend([
            "## ❌ Failed Evaluations",
            "",
            "> These prompts did not meet the pass threshold and need improvement",
            ""
        ])
        
        for s in sorted(failed, key=lambda x: x.get('overall_score', 0)):
            title = s.get('title', 'Unknown')
            score = s.get('overall_score', 0)
            reason = s.get('pass_reason', 'Score below threshold')
            improvements = s.get('improvements', [])
            
            lines.append(f"### {title} ({score}/10)")
            lines.append(f"**Failure Reason:** {reason}")
            lines.append("")
            if improvements:
                lines.append("**Suggested Improvements:**")
                for imp in improvements:
                    lines.append(f"- {imp}")
            lines.append("")
    
    # Needs improvement (below threshold but passed)
    needs_work = [s for s in all_scores if s.get('pass') is True and s.get('overall_score', 0) < 8.0]
    if needs_work:
        lines.extend([
            "## ⚠️ Needs Improvement",
            "",
            "> These prompts passed but could benefit from enhancement",
            ""
        ])
        
        for s in sorted(needs_work, key=lambda x: x.get('overall_score', 0)):
            title = s.get('title', 'Unknown')
            score = s.get('overall_score', 0)
            improvements = s.get('improvements', [])
            
            lines.append(f"### {title} ({score}/10)")
            if improvements:
                lines.append("**Suggested improvements:**")
                for imp in improvements:
                    lines.append(f"- {imp}")
            lines.append("")
    
    # Evaluation methodology
    lines.extend([
        "---",
        "",
        "## Evaluation Methodology",
        "",
        "This evaluation uses industry best practices from:",
        "- **OpenAI Evals**: Chain-of-thought grading with model-graded evaluation",
        "- **Promptfoo**: Pass/fail assertions with thresholds",
        "- **Anthropic**: Structured test formats and state tracking",
        "- **Google Gemini**: Clear criteria and parameter tuning",
        "",
        "### Criteria Evaluated",
        "",
        "| Category | Criterion | Description |",
        "|----------|-----------|-------------|",
        "| Core | Clarity | How clear and unambiguous are the instructions? |",
        "| Core | Specificity | Does it provide enough detail for consistent outputs? |",
        "| Core | Actionability | Can the AI clearly determine what actions to take? |",
        "| Core | Structure | Is it well-organized with clear sections? |",
        "| Core | Completeness | Does it cover all necessary aspects? |",
        "| Advanced | Factuality | Are any claims/examples accurate? |",
        "| Advanced | Consistency | Will it produce reproducible outputs? |",
        "| Advanced | Safety | Does it avoid harmful patterns or vulnerabilities? |",
        ""
    ])
    
    # Write file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"\nReport saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Run gh models eval and generate reports'
    )
    parser.add_argument(
        'eval_files',
        nargs='+',
        help='Evaluation file(s) to run (.prompt.yml)'
    )
    parser.add_argument(
        '--report', '-r',
        help='Generate markdown report to this file'
    )
    parser.add_argument(
        '--json-output', '-j',
        help='Save raw JSON results to this file'
    )
    
    args = parser.parse_args()
    
    all_results = {}
    all_raw = {}
    
    for eval_file in args.eval_files:
        print(f"\n🔄 Running evaluation: {eval_file}")
        
        results = run_gh_models_eval(eval_file)
        
        if results:
            eval_name = results.get('name', Path(eval_file).stem)
            scores = extract_scores(results)
            all_results[eval_name] = scores
            all_raw[eval_name] = results
            
            print_results(scores, eval_name)
        else:
            print(f"❌ Failed to run evaluation for {eval_file}")
    
    # Generate report if requested
    if args.report and all_results:
        generate_markdown_report(all_results, args.report)
    
    # Save raw JSON if requested
    if args.json_output and all_raw:
        with open(args.json_output, 'w', encoding='utf-8') as f:
            json.dump(all_raw, f, indent=2)
        print(f"\nRaw results saved to: {args.json_output}")
    
    # Exit with error if any evaluation failed
    if len(all_results) < len(args.eval_files):
        sys.exit(1)


if __name__ == '__main__':
    main()
