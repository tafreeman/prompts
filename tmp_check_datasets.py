import json, glob, sys, os
sys.path.insert(0, 'agentic-workflows-v2')
from agentic_v2.server.evaluation import adapt_sample_to_workflow_inputs
from agentic_v2.workflows.loader import WorkflowLoader
from pathlib import Path

loader = WorkflowLoader()
wf = loader.load('code_review')
inputs = wf.inputs

for d in sorted(glob.glob('agentic-workflows-v2/tests/fixtures/datasets/*.json')):
    with open(d) as f:
        data = json.load(f)
    sample = data[0] if isinstance(data, list) else data
    adapted = adapt_sample_to_workflow_inputs(inputs, sample, run_id='test', artifacts_dir=Path('C:/Temp'))
    missing = [k for k, v in inputs.items() if v.default is None and k not in adapted]
    name = os.path.basename(d)
    status = 'OK' if not missing else f'MISSING: {missing}'
    print(f'{name}: {status}  -> adapted keys: {list(adapted.keys())}')
