---
name: Tools Ecosystem Evaluator (Lite)
description: Compact version of the tools ecosystem evaluator for local models with limited context windows.
type: how_to
---
## Description

## Prompt

```text
---
name: Tools Ecosystem Evaluator (Lite)
description: Compact version of the tools ecosystem evaluator for local models with limited context windows.
type: how_to
---
```

Compact version of the tools ecosystem evaluator for local models with limited context windows.

## Description

## Prompt

```text
---
name: Tools Ecosystem Evaluator (Lite)
description: Compact version of the tools ecosystem evaluator for local models with limited context windows.
type: how_to
---
```

Compact version of the tools ecosystem evaluator for local models with limited context windows.


# Tools Ecosystem Evaluator (Lite)

A compact version of the evaluator designed to fit within local model context windows (~4K-8K tokens).

## Description

Use this prompt to quickly evaluate a `tools/` folder (or similar developer tooling ecosystem) and return JSON findings suitable for smaller context windows.

## Variables

| Variable            | Description                        |
| ------------------- | ---------------------------------- |
| `{TOOLS_STRUCTURE}` | Directory tree of tools folder     |
| `{KEY_FILES}`       | Contents of 1-3 key files (brief)  |

## Usage

This lite version is designed for:

- Local models (phi4, mistral, etc.) with 4K-8K context
- Quick evaluations where full analysis isn't needed
- CI pipelines where speed matters

For comprehensive analysis, use the full `tools-ecosystem-evaluator.md`.## Variables

_No bracketed variables detected._

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````
## Variables

| Variable | Description |
|---|---|
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

