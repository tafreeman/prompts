# Golden Outputs

This directory contains golden (expected) outputs for evaluation comparison.

## Structure

Each workflow has a subdirectory with:

- `golden.json` - Expected output structure
- Sample input/output pairs

## Example

```
golden/
├── fullstack_generation/
│   ├── golden.json
│   └── todo_app/
│       ├── input.json
│       └── expected_output/
├── legacy_refactoring/
│   └── ...
└── bug_fixing/
    └── ...
```
