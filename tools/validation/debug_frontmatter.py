import re, yaml
from pathlib import Path

paths = [
    'prompts/advanced/react-knowledge-base-research.md',
    'prompts/advanced/tree-of-thoughts-architecture-evaluator.md',
    'prompts/analysis/business-case-developer.md',
    'prompts/creative/ad-copy-generator.md',
    'prompts/creative/brand-voice-developer.md',
    'prompts/techniques/reflexion/multi-step-reflexion/multi-step-reflexion.md',
]

for p in paths:
    path = Path(p)
    print('----', p)
    text = path.read_text(encoding='utf-8')
    m = re.search(r'^\s*---\r?\n(.*?)\r?\n---', text, re.DOTALL | re.MULTILINE)
    print('match:', bool(m))
    if not m:
        continue
    fm_text = m.group(1)
    print('frontmatter snippet:')
    print(fm_text[:400])
    try:
        fm = yaml.safe_load(fm_text)
        print('parsed keys:', list(fm.keys()))
    except Exception as e:
        print('yaml error:', e)
