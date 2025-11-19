import os
import sqlite3

from load_prompts import load_prompts_from_repo, parse_markdown_prompt

BASE_DIR = os.path.dirname(__file__)
PROMPTS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "prompts"))
DB_PATH = os.path.join(BASE_DIR, "prompt_library.db")


def list_markdown_files():
    """Return all .md prompt files (excluding README.md) under prompts/."""
    md_files = []
    for root, dirs, files in os.walk(PROMPTS_DIR):
        for name in files:
            if not name.endswith(".md"):
                continue
            if name.lower() == "readme.md":
                continue
            full_path = os.path.join(root, name)
            rel_path = os.path.relpath(full_path, PROMPTS_DIR)
            md_files.append(rel_path.replace("\\", "/"))
    return sorted(md_files)


def list_db_titles():
    """Return set of titles currently stored in the prompts table."""
    if not os.path.exists(DB_PATH):
        return set()
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("SELECT title FROM prompts")
        return {row[0] for row in cur.fetchall()}
    finally:
        conn.close()


def main():
    print(f"PROMPTS_DIR: {PROMPTS_DIR}")

    # 1) All markdown files on disk
    md_files = list_markdown_files()
    print(f"Found {len(md_files)} markdown prompt files (excluding README.md)")

    # 2) What load_prompts_from_repo() can parse
    parsed_prompts = load_prompts_from_repo()
    parsed_titles = {p["title"] for p in parsed_prompts}
    print(f"load_prompts_from_repo() parsed {len(parsed_prompts)} prompts")

    # Also check which individual files fail parsing, to standardize them.
    failed_files = []
    for rel_path in md_files:
        full_path = os.path.join(PROMPTS_DIR, rel_path)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            result = parse_markdown_prompt(content, category="unknown")
            if result is None:
                failed_files.append(rel_path)
        except Exception as exc:
            failed_files.append(f"{rel_path} (error: {exc})")

    # 3) Titles currently in the DB
    db_titles = list_db_titles()
    print(f"Database currently contains {len(db_titles)} prompt titles")

    # 4) Any files whose *title* wasn't parsed by load_prompts_from_repo()
    # We can't know title without parsing, so we rely on the function itself.
    # The authoritative signal of "missed" is: file exists but its title isn't
    # among parsed_titles.

    # To help investigation, we list titles parsed but missing in DB and vice versa.
    missing_in_db = parsed_titles - db_titles
    if missing_in_db:
        print("\nTitles parsed from repo but missing in DB:")
        for t in sorted(missing_in_db):
            print(f"  - {t}")
    else:
        print("\nAll parsed titles are present in the DB.")

    # Also report DB titles that did not come from markdown (i.e., Python-defined prompts)
    extra_in_db = db_titles - parsed_titles
    if extra_in_db:
        print("\nTitles present in DB but not from markdown (likely Python-defined or legacy prompts):")
        for t in sorted(extra_in_db):
            print(f"  - {t}")
    else:
        print("\nNo DB titles beyond those parsed from markdown.")

    # 5) Report markdown files that could not be parsed at all
    if failed_files:
        print("\nMarkdown files that FAILED parse_markdown_prompt (need template cleanup):")
        for path in sorted(failed_files):
            print(f"  - {path}")
    else:
        print("\nAll markdown prompt files successfully parsed by parse_markdown_prompt().")


if __name__ == "__main__":
    main()
