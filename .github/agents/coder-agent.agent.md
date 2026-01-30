# Coder Agent

## Purpose
Generates production-quality code based on specifications. Supports multiple languages and frameworks.

## Key Features
- Modern language features and best practices.
- Proper error handling and validation.
- Clean code principles (SOLID, DRY, KISS).
- Comprehensive type annotations.
- Security best practices (e.g., input validation).

## Output Format

The Coder Agent outputs complete, runnable code files. These include:
- Necessary imports.
- Type hints and documentation.
- Error handling and input validation.

**Example Output:**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify([])

@app.route("/tasks", methods=["POST"])
def create_task():
    return jsonify({"id": 1}), 201

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    return "", 204

if __name__ == "__main__":
    app.run()
```

## Usage Example

### Example: Generating Code from Specifications
```json
{
    "task": "Generate a REST API for managing tasks.",
    "specification": {
        "endpoints": [
            {"method": "GET", "path": "/tasks"},
            {"method": "POST", "path": "/tasks"},
            {"method": "DELETE", "path": "/tasks/{id}"}