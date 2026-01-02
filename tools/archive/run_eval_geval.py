#!/usr/bin/env python3
"""
Run evaluate_prompt_geval() in batches of 3 with pause between batches.
Uses Mistral 7B model. Saves results after EACH file.
"""
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from local_model import LocalModel
from model_locks import create_model_lock

BATCH_SIZE = 3
OUTPUT_FILE = Path(__file__).parent.parent / "eval_geval_results.json"

def save_results(results, model_name="mistral-7b"):
    """Save results to JSON after each evaluation."""
    scores = [r["score"] for r in results if "score" in r and r["score"] > 0]
    avg = sum(scores) / len(scores) if scores else 0
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump({
            "method": "geval", 
            "model": model_name,
            "date": datetime.now().isoformat(), 
            "avg_score": round(avg, 2),
            "total_evaluated": len(results),
            "results": results
        }, f, indent=2)

def main():
    folder = Path(__file__).parent.parent / "prompts" / "advanced"
    all_prompts = [f for f in sorted(folder.glob("*.md")) 
                   if f.name not in ["README.md", "index.md"]]
    
    # Take first half
    midpoint = len(all_prompts) // 2
    prompts = all_prompts[:midpoint]
    
    print(f"\n{'='*60}")
    print(f"G-EVAL EVALUATION (Batch Mode)")
    print(f"Model: Mistral 7B")
    print(f"Prompts: {len(prompts)} | Batch size: {BATCH_SIZE}")
    print(f"Output: {OUTPUT_FILE}")
    print(f"{'='*60}\n")
    
    # Use Mistral 7B
    model = LocalModel(
        model_path=str(Path.home() / ".cache/aigallery/microsoft--mistral-7b-instruct-v0.2-ONNX/main/onnx/cpu_and_mobile/mistral-7b-instruct-v0.2-cpu-int4-rtn-block-32-acc-level-4"),
        verbose=False
    )
    create_model_lock("Mistral 7B")  # Mark model as in use
    print("✓ Model loaded\n")
    
    results = []
    batch_num = 0
    
    for i in range(0, len(prompts), BATCH_SIZE):
        batch = prompts[i:i+BATCH_SIZE]
        batch_num += 1
        
        print(f"\n{'='*60}")
        print(f"BATCH {batch_num} ({len(batch)} prompts)")
        print(f"{'='*60}")
        
        for j, p in enumerate(batch, 1):
            idx = i + j
            print(f"\n[{idx}/{len(prompts)}] {p.name}")
            print("-" * 50)
            try:
                content = p.read_text(encoding="utf-8")
                result = model.evaluate_prompt_geval(content)
                score = result.get("overall", 0)
                raw_score = result.get("overall_raw", 0)
                scores_detail = result.get("scores", {})
                criteria_results = result.get("criteria_results", {})
                
                # Display individual criteria scores (normalized 1-10)
                if scores_detail:
                    criteria_line = " | ".join(f"{k[:4]}:{v:.1f}" for k, v in scores_detail.items())
                    print(f"  Criteria: {criteria_line}")
                
                # Display key reasoning insights from each criterion
                for criterion, data in criteria_results.items():
                    if isinstance(data, dict) and "summary" in data:
                        summary = data.get("summary", "")
                        if summary:
                            summary_display = summary[:80] + "..." if len(summary) > 80 else summary
                            print(f"  {criterion.capitalize()}: {summary_display}")
                
                print(f"  ★ Overall: {score:.1f} (raw: {raw_score:.1f}/5)")
                
                results.append({
                    "file": p.name, 
                    "score": score, 
                    "details": scores_detail,
                    "raw_score": raw_score,
                    "criteria_results": criteria_results
                })
            except Exception as e:
                print(f"  ❌ Error: {e}")
                results.append({"file": p.name, "error": str(e)})
            
            # Save after EACH file
            save_results(results)
            print(f"  → Saved to {OUTPUT_FILE.name}")
        
        # Show batch summary
        batch_scores = [r["score"] for r in results[-len(batch):] if "score" in r and r["score"] > 0]
        batch_avg = sum(batch_scores) / len(batch_scores) if batch_scores else 0
        print(f"\n📊 Batch {batch_num} average: {batch_avg:.2f}")
        
        # Check if more batches remain
        if i + BATCH_SIZE < len(prompts):
            remaining = len(prompts) - (i + BATCH_SIZE)
            print(f"\n{remaining} prompts remaining.")
            response = input("Continue to next batch? (y/n): ").strip().lower()
            if response != 'y':
                print("Stopping. Results already saved.")
                break
    
    # Final summary with score distribution
    scores = [r["score"] for r in results if "score" in r and r["score"] > 0]
    avg = sum(scores) / len(scores) if scores else 0
    
    # Calculate score distribution
    excellent = len([s for s in scores if s >= 9])
    good = len([s for s in scores if 7 <= s < 9])
    fair = len([s for s in scores if 5 <= s < 7])
    poor = len([s for s in scores if s < 5])
    
    print(f"\n{'='*60}")
    print(f"FINAL SUMMARY - G-Eval (Mistral 7B)")
    print(f"{'='*60}")
    print(f"Prompts evaluated: {len(results)}")
    print(f"Average score: {avg:.2f} (normalized 1-10)")
    print(f"\nScore Distribution:")
    print(f"  ★★★ Excellent (9+):  {excellent}")
    print(f"  ★★  Good (7-8.9):    {good}")
    print(f"  ★   Fair (5-6.9):    {fair}")
    print(f"  ✗   Poor (<5):       {poor}")
    
    # Show top and bottom performers
    if scores:
        sorted_results = sorted([r for r in results if "score" in r and r["score"] > 0], 
                                key=lambda x: x["score"], reverse=True)
        print(f"\n🏆 Top 3:")
        for r in sorted_results[:3]:
            print(f"  {r['score']:.1f} - {r['file']}")
        
        if len(sorted_results) > 3:
            print(f"\n⚠️  Needs Improvement:")
            for r in sorted_results[-3:]:
                print(f"  {r['score']:.1f} - {r['file']}")
    
    print(f"\nResults: {OUTPUT_FILE}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
