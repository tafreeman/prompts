"""Audit for files that should be gitignored but aren't.

Usage:
    python scripts/audit-gitignore-gaps.py

Checks tracked files against common patterns that indicate they
shouldn't be in version control (secrets, build artifacts, logs, etc.).
"""

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Patterns that indicate a file should be gitignored
SUSPECT_PATTERNS = [
    # Secrets / credentials
    (r"\.env\.local$", "Local environment file (may contain secrets)"),
    (r"\.env\.\w+$", "Environment variant file"),
    (r"credentials.*\.json$", "Credentials file"),
    (r"\.key$", "Key file"),
    (r"\.pem$", "Certificate file"),
    # Build artifacts
    (r"dist/", "Build output directory"),
    (r"\.egg-info/", "Python egg metadata"),
    (r"storybook-static/", "Storybook build output"),
    # Logs and temp
    (r"\.log$", "Log file"),
    (r"tmp[^/]*$", "Temporary file"),
    # Large binaries
    (r"\.pptx$", "PowerPoint file (binary)"),
    (r"\.xlsx$", "Excel file (binary)"),
    (r"\.zip$", "Archive file"),
    (r"\.tar\.gz$", "Archive file"),
    # IDE
    (r"\.idea/", "JetBrains IDE config"),
    (r"\.vscode/settings\.json$", "VS Code user settings"),
]

# Patterns for potential secrets in file content
SECRET_PATTERNS = [
    (r"sk-[a-zA-Z0-9]{20,}", "OpenAI-style API key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub personal access token"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"Bearer\s+[a-zA-Z0-9\-._~+/]+=*", "Bearer token (may be example)"),
]


def get_tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return result.stdout.strip().splitlines()


def scan_file_content(path: pathlib.Path) -> list[tuple[str, int, str]]:
    """Scan a file for potential embedded secrets."""
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return findings

    for line_num, line in enumerate(text.splitlines(), 1):
        for pattern, desc in SECRET_PATTERNS:
            if re.search(pattern, line):
                # Skip if it's clearly a placeholder/example
                if any(
                    w in line.lower()
                    for w in ["example", "placeholder", "xxx", "your_", "TODO"]
                ):
                    continue
                findings.append((desc, line_num, line.strip()[:80]))

    return findings


def main() -> None:
    tracked = get_tracked_files()

    print("=== Gitignore Gap Analysis ===\n")

    # Check file path patterns
    path_findings = []
    for filepath in tracked:
        for pattern, desc in SUSPECT_PATTERNS:
            if re.search(pattern, filepath):
                path_findings.append((filepath, desc))
                break

    if path_findings:
        print(f"Files that may need gitignoring ({len(path_findings)}):")
        for filepath, desc in sorted(path_findings):
            print(f"  {filepath}  ({desc})")
    else:
        print("No suspicious tracked file paths found.")

    # Check content for secrets (sample first 500 tracked .py/.yaml/.json/.env files)
    print("\n=== Embedded Secret Scan ===\n")
    secret_findings = []
    scannable_exts = {".py", ".yaml", ".yml", ".json", ".env", ".toml", ".cfg", ".ini"}

    for filepath in tracked:
        p = pathlib.Path(filepath)
        if p.suffix in scannable_exts:
            full_path = ROOT / filepath
            if full_path.exists():
                for desc, line_num, text in scan_file_content(full_path):
                    secret_findings.append((filepath, line_num, desc, text))

    if secret_findings:
        print(f"Potential embedded secrets ({len(secret_findings)}):")
        for filepath, line_num, desc, text in sorted(secret_findings):
            print(f"  {filepath}:{line_num}  [{desc}]  {text}")
    else:
        print("No embedded secrets detected.")

    total = len(path_findings) + len(secret_findings)
    sys.exit(1 if total > 0 else 0)


if __name__ == "__main__":
    main()
