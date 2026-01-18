"""
Code validation for different programming languages
"""

import ast
import re
import subprocess
import tempfile
from typing import Any, Optional, Dict, List
from pathlib import Path
import asyncio

from .base_validator import BaseValidator


class CodeValidator(BaseValidator):
    """Validate code output for syntax and functionality"""

    SUPPORTED_LANGUAGES = {
        'python': {
            'extension': '.py',
            'comment': '#',
            'run_command': ['python', '-m', 'py_compile'],
            'syntax_check': 'ast'
        },
        'javascript': {
            'extension': '.js',
            'comment': '//',
            'run_command': ['node', '--check'],
            'syntax_check': 'regex'
        },
        'typescript': {
            'extension': '.ts',
            'comment': '//',
            'run_command': ['npx', 'tsc', '--noEmit'],
            'syntax_check': 'regex'
        },
        'java': {
            'extension': '.java',
            'comment': '//',
            'run_command': ['javac', '-Xlint'],
            'syntax_check': 'regex'
        },
        'sql': {
            'extension': '.sql',
            'comment': '--',
            'run_command': None,
            'syntax_check': 'keywords'
        },
        'rust': {
            'extension': '.rs',
            'comment': '//',
            'run_command': ['rustc', '--edition=2021', '-Z', 'parse-only'],
            'syntax_check': 'regex'
        },
        'go': {
            'extension': '.go',
            'comment': '//',
            'run_command': ['gofmt', '-e'],
            'syntax_check': 'regex'
        }
    }

    def __init__(self, language: str = "python", config: Optional[Dict] = None):
        """Initialize code validator for specific language"""
        super().__init__(config)
        self.language = language.lower()

        if self.language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}. Supported: {list(self.SUPPORTED_LANGUAGES.keys())}")

        self.lang_config = self.SUPPORTED_LANGUAGES[self.language]

    async def validate(self, output: Any, expected: Optional[Any] = None) -> bool:
        """Validate code output"""
        self.clear_messages()

        if not output:
            self.add_error("No output provided")
            return False

        # Extract code from markdown if needed
        code = self._extract_code(str(output))

        if not code:
            self.add_error("No code found in output")
            return False

        # Validate syntax
        syntax_valid = await self._validate_syntax(code)

        # Check for required patterns if specified
        if expected and isinstance(expected, dict):
            patterns_valid = self._validate_patterns(code, expected.get('patterns', []))
            contains_valid = self._validate_contains(code, expected.get('contains', []))
            structure_valid = self._validate_structure(code, expected.get('structure', {}))

            return syntax_valid and patterns_valid and contains_valid and structure_valid

        return syntax_valid

    def _extract_code(self, text: str) -> str:
        """Extract code from markdown code blocks or plain text"""

        # Try to extract from markdown code blocks
        pattern = r'```(?:' + re.escape(self.language) + r')?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        if matches:
            return '\n'.join(matches)

        # Try generic code block
        pattern = r'```\w*\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)

        if matches:
            return '\n'.join(matches)

        # Return as-is if no code blocks found
        return text.strip()

    async def _validate_syntax(self, code: str) -> bool:
        """Validate code syntax based on language"""

        syntax_check = self.lang_config['syntax_check']

        if syntax_check == 'ast' and self.language == 'python':
            return self._validate_python_syntax(code)
        elif syntax_check == 'regex':
            return self._validate_with_regex(code)
        elif syntax_check == 'keywords':
            return self._validate_keywords(code)
        elif self.lang_config['run_command']:
            return await self._validate_with_compiler(code)
        else:
            self.add_warning(f"No syntax validation available for {self.language}")
            return True

    def _validate_python_syntax(self, code: str) -> bool:
        """Validate Python syntax using AST"""
        try:
            ast.parse(code)
            return True
        except SyntaxError as e:
            self.add_error(f"Python syntax error at line {e.lineno}: {e.msg}")
            return False
        except Exception as e:
            self.add_error(f"Python parsing error: {str(e)}")
            return False

    def _validate_with_regex(self, code: str) -> bool:
        """Basic syntax validation using regex patterns"""

        # Check for balanced brackets
        brackets = {
            '{': '}',
            '[': ']',
            '(': ')'
        }

        stack = []
        in_string = False
        string_char = None
        escaped = False

        for char in code:
            if escaped:
                escaped = False
                continue

            if char == '\\':
                escaped = True
                continue

            if char in ('"', "'", '`') and not in_string:
                in_string = True
                string_char = char
            elif char == string_char and in_string:
                in_string = False
                string_char = None
            elif not in_string:
                if char in brackets.keys():
                    stack.append(char)
                elif char in brackets.values():
                    if not stack:
                        self.add_error(f"Unmatched closing bracket: {char}")
                        return False
                    expected = brackets[stack.pop()]
                    if char != expected:
                        self.add_error(f"Mismatched brackets: expected {expected}, got {char}")
                        return False

        if stack:
            self.add_error(f"Unclosed brackets: {stack}")
            return False

        return True

    def _validate_keywords(self, code: str) -> bool:
        """Validate presence of language keywords"""

        if self.language == 'sql':
            sql_keywords = ['SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER']
            code_upper = code.upper()

            if not any(keyword in code_upper for keyword in sql_keywords):
                self.add_error("No SQL keywords found")
                return False

        return True

    async def _validate_with_compiler(self, code: str) -> bool:
        """Validate code using language compiler/interpreter"""

        if not self.lang_config['run_command']:
            return True

        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix=self.lang_config['extension'],
                delete=False
            ) as f:
                f.write(code)
                temp_file = f.name

            # Run compiler/syntax checker
            cmd = self.lang_config['run_command'] + [temp_file]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=5.0
            )

            # Clean up
            Path(temp_file).unlink(missing_ok=True)

            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else stdout.decode()
                self.add_error(f"Syntax validation failed: {error_msg}")
                return False

            return True

        except asyncio.TimeoutError:
            self.add_error("Syntax validation timed out")
            return False
        except FileNotFoundError:
            self.add_warning(f"Compiler/interpreter not found for {self.language}")
            return True  # Pass if tool not available
        except Exception as e:
            self.add_error(f"Syntax validation error: {str(e)}")
            return False
        finally:
            # Ensure cleanup
            if 'temp_file' in locals():
                Path(temp_file).unlink(missing_ok=True)

    def _validate_patterns(self, code: str, patterns: List[str]) -> bool:
        """Validate that code matches required patterns"""

        all_match = True
        for pattern in patterns:
            if not re.search(pattern, code, re.MULTILINE | re.DOTALL):
                self.add_error(f"Code does not match required pattern: {pattern}")
                all_match = False

        return all_match

    def _validate_contains(self, code: str, required_items: List[str]) -> bool:
        """Validate that code contains required elements"""

        missing = []
        for item in required_items:
            if item not in code:
                missing.append(item)

        if missing:
            self.add_error(f"Code missing required elements: {missing}")
            return False

        return True

    def _validate_structure(self, code: str, structure: Dict[str, Any]) -> bool:
        """Validate code structure (functions, classes, etc.)"""

        if not structure:
            return True

        if self.language == 'python':
            return self._validate_python_structure(code, structure)
        else:
            self.add_warning(f"Structure validation not implemented for {self.language}")
            return True

    def _validate_python_structure(self, code: str, structure: Dict[str, Any]) -> bool:
        """Validate Python code structure"""

        try:
            tree = ast.parse(code)

            # Check for required functions
            if 'functions' in structure:
                functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                for required_func in structure['functions']:
                    if required_func not in functions:
                        self.add_error(f"Missing required function: {required_func}")
                        return False

            # Check for required classes
            if 'classes' in structure:
                classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                for required_class in structure['classes']:
                    if required_class not in classes:
                        self.add_error(f"Missing required class: {required_class}")
                        return False

            # Check for imports
            if 'imports' in structure:
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        imports.extend([alias.name for alias in node.names])
                    elif isinstance(node, ast.ImportFrom):
                        imports.append(node.module)

                for required_import in structure['imports']:
                    if required_import not in imports:
                        self.add_warning(f"Missing expected import: {required_import}")

            return True

        except Exception as e:
            self.add_error(f"Structure validation error: {str(e)}")
            return False


class CodeExecutionValidator(CodeValidator):
    """Validate code by executing it and checking output"""

    def __init__(self, language: str = "python", sandbox: bool = True, config: Optional[Dict] = None):
        """Initialize code execution validator"""
        super().__init__(language, config)
        self.sandbox = sandbox

    async def validate_with_execution(self,
                                     code: str,
                                     test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate code by running test cases"""

        results = {
            "total_tests": len(test_cases),
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "test_results": []
        }

        for test_case in test_cases:
            try:
                result = await self._run_test_case(code, test_case)

                if result["passed"]:
                    results["passed"] += 1
                else:
                    results["failed"] += 1

                results["test_results"].append(result)

            except Exception as e:
                results["errors"] += 1
                results["test_results"].append({
                    "test_id": test_case.get("id", "unknown"),
                    "error": str(e),
                    "passed": False
                })

        results["success_rate"] = results["passed"] / results["total_tests"] if results["total_tests"] > 0 else 0

        return results

    async def _run_test_case(self, code: str, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test case against code"""

        if self.language == "python":
            return await self._run_python_test(code, test_case)
        else:
            raise NotImplementedError(f"Execution validation not implemented for {self.language}")

    async def _run_python_test(self, code: str, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run Python code with test case"""

        import json

        # Create test wrapper
        test_wrapper = f"""
import json
import sys

# User code
{code}

# Test execution
test_input = {json.dumps(test_case.get('input', {}))}
expected_output = {json.dumps(test_case.get('output'))}

# Find and execute the main function
import ast
tree = ast.parse('''{code.replace("'''", "\\'\\'\\'")}''')

# Find function to test
func_name = "{test_case.get('function', 'main')}"
result = None

if func_name in locals():
    if isinstance(test_input, dict):
        result = locals()[func_name](**test_input)
    else:
        result = locals()[func_name](test_input)

    success = result == expected_output
    print(json.dumps({{
        'passed': success,
        'expected': expected_output,
        'actual': result,
        'test_id': '{test_case.get("id", "test")}'
    }}))
else:
    print(json.dumps({{
        'passed': False,
        'error': f'Function {{func_name}} not found',
        'test_id': '{test_case.get("id", "test")}'
    }}))
"""

        # Execute in subprocess for safety
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(test_wrapper)
                temp_file = f.name

            process = await asyncio.create_subprocess_exec(
                'python', temp_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=5.0
            )

            Path(temp_file).unlink(missing_ok=True)

            if stderr:
                return {
                    "passed": False,
                    "error": stderr.decode(),
                    "test_id": test_case.get("id", "test")
                }

            return json.loads(stdout.decode())

        except asyncio.TimeoutError:
            return {
                "passed": False,
                "error": "Test execution timed out",
                "test_id": test_case.get("id", "test")
            }
        except json.JSONDecodeError as e:
            return {
                "passed": False,
                "error": f"Invalid test output: {e}",
                "test_id": test_case.get("id", "test")
            }
        except Exception as e:
            return {
                "passed": False,
                "error": str(e),
                "test_id": test_case.get("id", "test")
            }
        finally:
            if 'temp_file' in locals():
                Path(temp_file).unlink(missing_ok=True)
