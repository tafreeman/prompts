#!/usr/bin/env python3
"""
Local ONNX Model Runner for Prompt Evaluation
==============================================

Uses locally cached ONNX models (like Mistral 7B) for fast, free evaluations.

Requirements:
    pip install onnxruntime-genai

Usage:
    # Direct usage
    python tools/local_model.py "Evaluate this prompt for clarity"
    
    # As a module
    from tools.local_model import LocalModel
    model = LocalModel()
    response = model.generate("Your prompt here")

Author: Prompts Library Team
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any
import json

# Default model paths (Windows AI Gallery cache)
DEFAULT_MODEL_PATHS = [
    # User's Mistral 7B INT4 model (AI Gallery format - double dash, no space)
    Path(r"C:\Users\tandf\.cache\aigallery\microsoft--mistral-7b-instruct-v0.2-ONNX\main\onnx\cpu_and_mobile\mistral-7b-instruct-v0.2-cpu-int4-rtn-block-32-acc-level-4"),
    # Phi-4 mini (also in AI Gallery)
    Path(r"C:\Users\tandf\.cache\aigallery\microsoft--Phi-4-mini-instruct-onnx"),
    # Alternative paths
    Path.home() / ".cache" / "aigallery" / "microsoft--mistral-7b-instruct-v0.2-ONNX" / "main" / "onnx" / "cpu_and_mobile" / "mistral-7b-instruct-v0.2-cpu-int4-rtn-block-32-acc-level-4",
    Path.home() / ".cache" / "huggingface" / "hub" / "models--mistralai--Mistral-7B-Instruct-v0.2",
]


class LocalModel:
    """Wrapper for local ONNX models using onnxruntime-genai."""
    
    def __init__(self, model_path: Optional[str] = None, verbose: bool = False):
        self.verbose = verbose
        self.model = None
        self.tokenizer = None
        self.model_path = None
        
        # Find model path
        if model_path:
            self.model_path = Path(model_path)
        else:
            for path in DEFAULT_MODEL_PATHS:
                if path.exists():
                    self.model_path = path
                    break
        
        if not self.model_path or not self.model_path.exists():
            raise FileNotFoundError(
                f"No local model found. Checked paths:\n" + 
                "\n".join(f"  - {p}" for p in DEFAULT_MODEL_PATHS)
            )
        
        if self.verbose:
            print(f"Loading model from: {self.model_path}")
        
        self._load_model()
    
    def _load_model(self):
        """Load the ONNX model using onnxruntime-genai."""
        try:
            import onnxruntime_genai as og
            
            self.model = og.Model(str(self.model_path))
            self.tokenizer = og.Tokenizer(self.model)
            
            if self.verbose:
                print("Model loaded successfully!")
                
        except ImportError:
            raise ImportError(
                "onnxruntime-genai not installed. Install with:\n"
                "  pip install onnxruntime-genai\n"
                "Or for GPU support:\n"
                "  pip install onnxruntime-genai-cuda  # NVIDIA\n"
                "  pip install onnxruntime-genai-directml  # AMD/Intel on Windows"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 0.9,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Generate text from the model.
        
        Args:
            prompt: The user prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 = deterministic)
            top_p: Nucleus sampling parameter
            system_prompt: Optional system prompt
            
        Returns:
            Generated text response
        """
        import onnxruntime_genai as og
        
        # Format as Mistral instruction format
        if system_prompt:
            full_prompt = f"<s>[INST] {system_prompt}\n\n{prompt} [/INST]"
        else:
            full_prompt = f"<s>[INST] {prompt} [/INST]"
        
        # Tokenize
        input_tokens = self.tokenizer.encode(full_prompt)
        
        # Set up generation parameters (updated API for onnxruntime-genai)
        params = og.GeneratorParams(self.model)
        search_options = {
            "max_length": len(input_tokens) + max_tokens,
            "batch_size": 1,
        }
        params.set_search_options(**search_options)
        
        # Create generator and append input tokens
        generator = og.Generator(self.model, params)
        generator.append_tokens(input_tokens)
        
        # Generate tokens using the updated loop pattern
        try:
            while True:
                generator.generate_next_token()
                if generator.is_done():
                    break
        except KeyboardInterrupt:
            if self.verbose:
                print("\n[Generation interrupted]")
        
        # Get the full sequence and decode
        output_sequence = generator.get_sequence(0)
        response = self.tokenizer.decode(output_sequence)
        
        # Clean up response - extract just the model's reply
        if "[/INST]" in response:
            response = response.split("[/INST]")[-1].strip()
        response = response.replace("</s>", "").strip()
        
        del generator
        return response
    
    def evaluate_prompt(self, prompt_content: str) -> Dict[str, Any]:
        """
        Evaluate a prompt using the local model.
        
        Returns a structured evaluation similar to the cloud-based evaluators.
        """
        eval_prompt = f"""Evaluate this prompt template on a 1-10 scale for each criterion.
Return ONLY valid JSON with scores and brief reasoning.

Criteria:
- clarity: Is it unambiguous and easy to understand?
- specificity: Enough detail for consistent outputs?
- actionability: Can the AI determine what to do?
- structure: Well-organized with clear sections?
- completeness: Covers all necessary aspects?
- safety: Avoids harmful patterns?

Prompt to evaluate:
```
{prompt_content[:3000]}
```

Return ONLY valid JSON in this exact format:
{{"scores": {{"clarity": N, "specificity": N, "actionability": N, "structure": N, "completeness": N, "safety": N}}, "overall": N, "summary": "brief assessment"}}"""

        response = self.generate(eval_prompt, max_tokens=500, temperature=0.3)

        # Some model exports (or generation modes) may return a JSON string with
        # escaped quotes (e.g. "{\"scores\": {...}}") which defeats the
        # normal JSON extraction. Try to unescape obvious cases first.
        try:
            resp_strip = response.strip()
            # If the entire response looks like a quoted JSON string, unescape it
            if (resp_strip.startswith('"') and resp_strip.endswith('"')) or (resp_strip.startswith("'") and resp_strip.endswith("'")):
                try:
                    # json.loads will unescape a JSON string literal
                    unquoted = json.loads(resp_strip)
                    if isinstance(unquoted, str) and unquoted.count('{'):
                        response = unquoted
                except Exception:
                    # Fallback: try python literal eval
                    try:
                        import ast
                        unquoted = ast.literal_eval(resp_strip)
                        if isinstance(unquoted, str) and unquoted.count('{'):
                            response = unquoted
                    except Exception:
                        pass

            # If response contains many escaped quotes like \"scores\", try a unicode-escape pass
            if '\\"' in response or '\\n' in response:
                try:
                    unescaped = bytes(response, 'utf-8').decode('unicode_escape')
                    # If unescaped looks more like JSON (contains { and }), prefer it
                    if unescaped.count('{') >= response.count('{'):
                        response = unescaped
                except Exception:
                    pass
        except Exception:
            # Non-fatal; we'll fall back to other parsing heuristics below
            pass
        
        # Try to parse JSON from response
        try:
            import re
            # Look for JSON object in response - use a more inclusive pattern
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                json_str = json_match.group()
                
                # Fix common JSON issues from LLM output
                # 1. Remove trailing commas before } or ]
                json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
                
                # 2. Handle literal \n (backslash-n as two characters)
                if '\\n' in json_str:
                    json_str = json_str.replace('\\n', ' ')
                
                try:
                    result = json.loads(json_str)
                except json.JSONDecodeError:
                    # Try more aggressive cleaning - collapse all whitespace
                    json_str = ' '.join(json_str.split())
                    result = json.loads(json_str)
                
                # Normalize the result structure
                # Some models put overall/summary inside scores
                if "scores" in result and "overall" not in result:
                    # Check if overall is inside scores
                    scores = result.get("scores", {})
                    if "overall" in scores:
                        result["overall"] = scores.pop("overall")
                    if "summary" in scores:
                        result["summary"] = scores.pop("summary")
                
                # Ensure overall exists
                if "overall" not in result:
                    # Calculate from scores if available
                    scores = result.get("scores", {})
                    if scores:
                        numeric_scores = [v for v in scores.values() if isinstance(v, (int, float))]
                        if numeric_scores:
                            result["overall"] = sum(numeric_scores) / len(numeric_scores)
                        else:
                            result["overall"] = 0
                    else:
                        result["overall"] = 0
                
                return result
                    
        except json.JSONDecodeError as e:
            # Return raw response with error details
            return {
                "raw_response": response,
                "error": f"JSON parse error: {e}",
                "overall": 0,  # Default to 0 on parse error
            }
        except Exception as e:
            return {
                "raw_response": response,
                "error": f"Unexpected error: {e}",
                "overall": 0,
            }
        
        # Return raw response if no JSON found
        return {
            "raw_response": response,
            "error": "Could not find JSON in response",
            "overall": 0,  # Default to 0
        }


def check_model_available() -> bool:
    """Check if a local model is available."""
    for path in DEFAULT_MODEL_PATHS:
        if path.exists():
            return True
    return False


def get_model_info() -> Dict[str, Any]:
    """Get information about available local models."""
    info = {
        "available": False,
        "paths_checked": [str(p) for p in DEFAULT_MODEL_PATHS],
        "found_path": None,
        "onnxruntime_genai_installed": False,
    }
    
    # Check for onnxruntime-genai
    try:
        import onnxruntime_genai
        info["onnxruntime_genai_installed"] = True
        info["onnxruntime_genai_version"] = onnxruntime_genai.__version__
    except ImportError:
        pass
    
    # Check for model
    for path in DEFAULT_MODEL_PATHS:
        if path.exists():
            info["available"] = True
            info["found_path"] = str(path)
            
            # Get model files info
            model_files = list(path.glob("*.onnx"))
            info["model_files"] = [f.name for f in model_files]
            break
    
    return info


def main():
    parser = argparse.ArgumentParser(
        description="Run prompts through local ONNX model"
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Prompt to send to the model"
    )
    parser.add_argument(
        "--model-path", "-m",
        help="Path to ONNX model directory"
    )
    parser.add_argument(
        "--max-tokens", "-t",
        type=int,
        default=1024,
        help="Maximum tokens to generate"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if local model is available"
    )
    parser.add_argument(
        "--evaluate", "-e",
        type=str,
        help="Path to prompt file to evaluate"
    )
    parser.add_argument(
        "--batch-evaluate",
        type=str,
        help="Path to a JSON file containing a list of prompt file paths to evaluate in batch (loads model once)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Check mode
    if args.check:
        info = get_model_info()
        print(json.dumps(info, indent=2))
        sys.exit(0 if info["available"] else 1)
    
    # Evaluate mode
    if args.evaluate:
        prompt_path = Path(args.evaluate)
        if not prompt_path.exists():
            print(f"Error: File not found: {prompt_path}")
            sys.exit(1)
        
        try:
            model = LocalModel(args.model_path, verbose=args.verbose)
            content = prompt_path.read_text(encoding="utf-8")
            result = model.evaluate_prompt(content)
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        
        sys.exit(0)

    # Batch evaluate mode: accepts a JSON file listing prompt file paths
    if args.batch_evaluate:
        batch_file = Path(args.batch_evaluate)
        if not batch_file.exists():
            print(f"Error: Batch file not found: {batch_file}")
            sys.exit(1)

        try:
            paths = json.loads(batch_file.read_text(encoding="utf-8"))
            if not isinstance(paths, list):
                print("Error: batch file must contain a JSON array of file paths")
                sys.exit(1)

            model = LocalModel(args.model_path, verbose=args.verbose)
            results = []
            for p in paths:
                try:
                    prompt_path = Path(p)
                    if not prompt_path.exists():
                        results.append({"file": str(p), "error": "file not found"})
                        continue
                    content = prompt_path.read_text(encoding="utf-8")
                    res = model.evaluate_prompt(content)
                    # Normalize return
                    out = {
                        "file": str(prompt_path),
                        "result": res,
                    }
                    results.append(out)
                except Exception as e:
                    results.append({"file": str(p), "error": str(e)})

            print(json.dumps({"results": results}, indent=2))
            sys.exit(0)
        except Exception as e:
            print(f"Error during batch evaluation: {e}")
            sys.exit(1)
    
    # Interactive mode
    if not args.prompt:
        parser.print_help()
        sys.exit(1)
    
    try:
        model = LocalModel(args.model_path, verbose=args.verbose)
        response = model.generate(
            args.prompt,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )
        print(response)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
