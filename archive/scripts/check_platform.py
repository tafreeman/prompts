import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
DEFAULT_PLATFORM = "Claude Sonnet 4.5"
SPECIAL_PLATFORMS = {
    "m365/": "Microsoft 365 Copilot",
}

missing = []
mismatched = []

for root, dirs, files in os.walk(PROMPTS_DIR):
    for name in files:
        if not name.endswith(".md"):
            continue
        if name.lower() == "readme.md":
            continue
        path = os.path.join(root, name)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if not content.startswith("---"):
            continue
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        frontmatter = parts[1]
        rel_path = os.path.relpath(path, PROMPTS_DIR).replace("\\", "/")

        expected_platform = DEFAULT_PLATFORM
        check_match = False
        for prefix, platform in SPECIAL_PLATFORMS.items():
            if rel_path.startswith(prefix):
                expected_platform = platform
                check_match = True
                break

        platform_line = None
        platform_value = None
        for line in frontmatter.strip().splitlines():
            if line.strip().lower().startswith("platform:"):
                platform_line = line
                platform_value = line.split(":", 1)[1].strip().strip('"').strip("'")
                break

        if not platform_line:
            missing.append(rel_path)
            continue

        if check_match and platform_value != expected_platform:
            mismatched.append((rel_path, platform_value, expected_platform))

print(f"Found {len(missing)} prompts missing platform metadata")
for path in sorted(missing):
    print(path)

if mismatched:
    print(f"\n{len(mismatched)} m365 prompts with incorrect platform values:")
    for rel, actual, expected in sorted(mismatched):
        print(f"  - {rel}: {actual} (expected {expected})")
else:
    print("\nAll m365 prompts have the correct platform metadata.")
