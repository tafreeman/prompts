# tools/eval_quick_runner.py
# Usage:
#   .venv\Scripts\Activate.ps1
#   python tools/eval_quick_runner.py --prompts prompts/ --tier 1 --sample 5 --models "gh-model-1,gh-model-2"
import argparse, subprocess, json, csv, shutil, pathlib, time, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

def run_cmd(cmd, timeout=600):
    print(">", " ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr

def run_tiered_eval(target, tier, limit=None):
    """Run tiered evaluation using prompteval (the canonical evaluator)."""
    cmd = [sys.executable, "-m", "prompteval", str(target), "--tier", str(tier)]
    if limit:
        cmd += ["--limit", str(limit)]
    rc, out, err = run_cmd(cmd, timeout=900)
    if rc != 0:
        print("prompteval failed:", err)
    return rc, out

def gen_eval_files(target, outdir):
    cmd = [sys.executable, str(ROOT / "tools" / "generate_eval_files.py"), str(target), "--out", str(outdir)]
    rc, out, err = run_cmd(cmd)
    return rc, out

def gh_eval_file(evalfile, model=None):
    cmd = ["gh", "models", "eval", str(evalfile), "--json"]
    if model:
        cmd += ["--model", model]
    rc, out, err = run_cmd(cmd, timeout=600)
    return rc, out

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompts", required=True)
    p.add_argument("--tier", default=1, type=int)
    p.add_argument("--sample", type=int, default=5)
    p.add_argument("--models", type=str, default="")
    p.add_argument("--out", type=str, default="testing/evals/results/quick_run")
    args = p.parse_args()

    outdir = ROOT / args.out
    outdir.mkdir(parents=True, exist_ok=True)

    print("Running tiered eval (quick)...")
    run_tiered_eval(args.prompts, args.tier, limit=args.sample)

    gen_dir = ROOT / "testing" / "evals"  # many tools generate here
    # fallback: generate eval files into gen_dir if not present
    # (generate_eval_files.py may create different layout depending on repo)
    # We try to find .prompt.yml files under testing/evals
    eval_files = list(gen_dir.rglob("*.prompt.yml"))
    if not eval_files:
        print("No .prompt.yml found under testing/evals, attempting generator")
        gen_eval_files(args.prompts, gen_dir)
        eval_files = list(gen_dir.rglob("*.prompt.yml"))

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    results = []
    for ef in eval_files:
        for model in (models or [None]):
            start = time.time()
            rc, out = gh_eval_file(ef, model=model) if shutil.which("gh") else (1, "")
            dur = time.time() - start
            row = {
                "eval_file": str(ef),
                "model": model or "gh-default",
                "rc": rc,
                "duration_s": round(dur, 2),
                "raw": out[:2000]
            }
            # quick try parse overall_score if present
            try:
                j = json.loads(out)
                # Depending on gh output structure, try to extract common field names:
                if isinstance(j, dict) and "overall_score" in j:
                    row["score"] = j["overall_score"]
                elif isinstance(j, list) and j:
                    if isinstance(j[0], dict) and "overall_score" in j[0]:
                        row["score"] = j[0]["overall_score"]
            except Exception:
                pass
            results.append(row)
            print("=>", row["eval_file"], "model", row["model"], "rc", row["rc"], "dur", row["duration_s"], "score", row.get("score"))

    # write summary csv
    csvf = outdir / "quick_eval_summary.csv"
    with open(csvf, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["eval_file","model","rc","duration_s","score"])
        writer.writeheader()
        for r in results:
            writer.writerow({k:r.get(k,"") for k in writer.fieldnames})
    print("Summary written to", csvf)

if __name__ == "__main__":
    main()