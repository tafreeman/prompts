import yaml

file_path = 'prompts/developers/code-review-expert-structured.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('---', 2)
print(f"Parts count: {len(parts)}")
if len(parts) >= 3:
    print("Metadata block found.")
    try:
        metadata = yaml.safe_load(parts[1])
        print("Metadata parsed successfully:")
        print(metadata)
        if 'governance' in metadata:
            print("Governance key FOUND.")
        else:
            print("Governance key NOT found.")
    except Exception as e:
        print(f"YAML parsing error: {e}")
else:
    print("No valid YAML frontmatter found.")
