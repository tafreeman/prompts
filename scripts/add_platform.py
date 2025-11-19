import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")

DEFAULT_PLATFORM = "Claude Sonnet 4.5"
SPECIAL_PLATFORMS = {
    "m365/": "Microsoft 365 Copilot",
}

updated_files = []

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
        body = parts[2]

        rel_path = os.path.relpath(path, PROMPTS_DIR).replace("\\", "/")
        desired_platform = DEFAULT_PLATFORM
        force_update = False
        for prefix, platform in SPECIAL_PLATFORMS.items():
            if rel_path.startswith(prefix):
                desired_platform = platform
                force_update = True
                break

        front_lines = [line for line in frontmatter.strip().splitlines() if line.strip()]
        platform_index = None
        current_value = None
        for i, line in enumerate(front_lines):
            if line.strip().lower().startswith("platform:"):
                platform_index = i
                current_value = line.split(":", 1)[1].strip().strip('"').strip("'")
                break

        changed = False
        if platform_index is not None:
            if force_update and current_value != desired_platform:
                front_lines[platform_index] = f'platform: "{desired_platform}"'
                changed = True
        else:
            front_lines.append(f'platform: "{desired_platform}"')
            changed = True

        if not changed:
            continue

        new_frontmatter = "\n".join(front_lines).strip() + "\n"
        new_content = "---\n" + new_frontmatter + "---" + body
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        updated_files.append(rel_path)

print(f"Updated {len(updated_files)} prompt files by adding or correcting platform metadata")
for rel in sorted(updated_files):
    print(rel)
