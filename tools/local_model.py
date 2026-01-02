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
from typing import Optional, Dict, Any, List
import json

# Default model locations.
# Keep these portable: avoid hard-coded user paths.
_AI_GALLERY_ROOT = Path.home() / ".cache" / "aigallery"

# Known AI Gallery directories keyed by short model names.
# NOTE: These are directory names, not the final ONNX compute subfolder.
_MODEL_DIRS = {
    "phi4": ["microsoft--Phi-4-mini-instruct-onnx"],
    "phi4mini": ["microsoft--Phi-4-mini-instruct-onnx"],
    "phi3": ["microsoft--Phi-3-mini-4k-instruct-onnx"],
    "phi3.5": ["microsoft--Phi-3.5-mini-instruct-onnx"],
    "mistral": ["microsoft--mistral-7b-instruct-v0.2-ONNX"],
    "mistral-7b": ["microsoft--mistral-7b-instruct-v0.2-ONNX"],
}


def _find_onnx_model_dir(base: Path) -> Optional[Path]:
    """Return the first directory under base that looks like an ONNX model folder."""
    if not base.exists() or not base.is_dir():
        return None

    # Heuristic: prefer folders containing *.onnx; often nested under main/**/cpu_* or directml.
    for d in base.rglob("*"):
        if not d.is_dir():
            continue
        try:
            if any(d.glob("*.onnx")):
                return d
        except OSError:
            continue

    return None


def _resolve_model_path(model_key: Optional[str]) -> Optional[Path]:
    """Resolve a model key to a concrete ONNX folder path, if available."""
    if not _AI_GALLERY_ROOT.exists():
        return None

    if model_key:
        key = model_key.strip().lower()
        candidates = _MODEL_DIRS.get(key, [])
        for dirname in candidates:
            base = _AI_GALLERY_ROOT / dirname
            p = _find_onnx_model_dir(base)
            if p:
                return p

    # Fallback: first available known model (in a stable order)
    for key in ["phi4mini", "phi3.5", "phi3", "mistral"]:
        for dirname in _MODEL_DIRS.get(key, []):
            base = _AI_GALLERY_ROOT / dirname
            p = _find_onnx_model_dir(base)
            if p:
                return p

    return None


class LocalModel:
    """Wrapper for local ONNX models using onnxruntime-genai."""
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        model_key: Optional[str] = None,
        verbose: bool = False,
    ):
        self.verbose = verbose
        self.model = None
        self.tokenizer = None
        self.model_path = None
        
        # Find model path
        if model_path:
            self.model_path = Path(model_path)
        else:
            self.model_path = _resolve_model_path(model_key)
        
        if not self.model_path or not self.model_path.exists():
            raise FileNotFoundError(
                "No local ONNX model found.\n"
                f"AI Gallery cache root checked: {_AI_GALLERY_ROOT}\n"
                "Tip: install a local ONNX model (e.g., Phi-4 mini) via your tooling, or set --model-path explicitly."
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
        
        return self._parse_evaluation_response(response)
    
    def _parse_evaluation_response(self, response: str) -> Dict[str, Any]:
        """
        Parse evaluation response with multiple fallback strategies.
        Handles various JSON formatting issues from LLM output.
        """
        import re
        
        original_response = response
        
        # Step 1: Clean up the response
        response = response.strip()
        
        # Remove markdown code blocks if present
        if '```json' in response:
            match = re.search(r'```json\s*([\s\S]*?)\s*```', response)
            if match:
                response = match.group(1)
        elif '```' in response:
            match = re.search(r'```\s*([\s\S]*?)\s*```', response)
            if match:
                response = match.group(1)
        
        # Step 2: Try to unescape quoted JSON strings
        try:
            resp_strip = response.strip()
            if (resp_strip.startswith('"') and resp_strip.endswith('"')) or \
               (resp_strip.startswith("'") and resp_strip.endswith("'")):
                try:
                    unquoted = json.loads(resp_strip)
                    if isinstance(unquoted, str) and '{' in unquoted:
                        response = unquoted
                except Exception:
                    pass
            
            # Handle escaped quotes
            if '\\"' in response or '\\n' in response:
                try:
                    unescaped = response.encode().decode('unicode_escape')
                    if '{' in unescaped:
                        response = unescaped
                except Exception:
                    pass
        except Exception:
            pass
        
        # Step 3: Try multiple JSON extraction strategies
        json_result = None
        
        # Strategy 3a: Find outermost { } pair
        try:
            # Find first { and last }
            first_brace = response.find('{')
            last_brace = response.rfind('}')
            if first_brace != -1 and last_brace > first_brace:
                json_str = response[first_brace:last_brace + 1]
                json_result = self._try_parse_json(json_str)
        except Exception:
            pass
        
        # Strategy 3b: Look for JSON with "scores" key specifically
        if not json_result:
            try:
                match = re.search(r'\{[^{}]*"scores"[^{}]*\{[^{}]*\}[^{}]*\}', response, re.IGNORECASE)
                if match:
                    json_result = self._try_parse_json(match.group())
            except Exception:
                pass
        
        # Strategy 3c: Try to extract individual fields with regex
        if not json_result:
            try:
                scores = {}
                # Look for patterns like "clarity": 9 or clarity: 9
                for field in ['clarity', 'specificity', 'actionability', 'structure', 'completeness', 'safety']:
                    match = re.search(rf'["\']?{field}["\']?\s*:\s*(\d+(?:\.\d+)?)', response, re.IGNORECASE)
                    if match:
                        scores[field] = float(match.group(1))
                
                # Look for overall score
                overall = 0
                overall_match = re.search(r'["\']?overall["\']?\s*:\s*(\d+(?:\.\d+)?)', response, re.IGNORECASE)
                if overall_match:
                    overall = float(overall_match.group(1))
                elif scores:
                    overall = sum(scores.values()) / len(scores)
                
                # Look for summary
                summary = ""
                summary_match = re.search(r'["\']?summary["\']?\s*:\s*["\']([^"\']+)["\']', response, re.IGNORECASE)
                if summary_match:
                    summary = summary_match.group(1)
                
                if scores or overall > 0:
                    json_result = {
                        "scores": scores,
                        "overall": round(overall, 1),
                        "summary": summary
                    }
            except Exception:
                pass
        
        # Step 4: Validate and normalize the result
        if json_result:
            # Normalize the result structure
            if "scores" in json_result and "overall" not in json_result:
                scores = json_result.get("scores", {})
                if "overall" in scores:
                    json_result["overall"] = scores.pop("overall")
                if "summary" in scores:
                    json_result["summary"] = scores.pop("summary")
            
            # Ensure overall exists
            if "overall" not in json_result or json_result["overall"] == 0:
                scores = json_result.get("scores", {})
                if scores:
                    numeric_scores = [v for v in scores.values() if isinstance(v, (int, float))]
                    if numeric_scores:
                        json_result["overall"] = round(sum(numeric_scores) / len(numeric_scores), 1)
            
            # Ensure summary exists
            if "summary" not in json_result:
                json_result["summary"] = ""
            
            return json_result
        
        # Step 5: Return error with raw response for debugging
        return {
            "raw_response": original_response[:500],  # Truncate for readability
            "error": "Could not parse JSON from response",
            "overall": 0,
            "scores": {},
            "summary": ""
        }
    
    def _try_parse_json(self, json_str: str) -> Optional[Dict[str, Any]]:
        """Try to parse a JSON string with various cleanup attempts."""
        import re
        
        # List of cleanup transformations to try
        cleanups = [
            lambda s: s,  # Try as-is first
            lambda s: re.sub(r',\s*([}\]])', r'\1', s),  # Remove trailing commas
            lambda s: s.replace("'", '"'),  # Single to double quotes
            lambda s: re.sub(r'(\w+):', r'"\1":', s),  # Unquoted keys
            lambda s: ' '.join(s.split()),  # Collapse whitespace
            lambda s: s.replace('\n', ' ').replace('\r', ''),  # Remove newlines
        ]
        
        for cleanup in cleanups:
            try:
                cleaned = cleanup(json_str)
                result = json.loads(cleaned)
                if isinstance(result, dict):
                    return result
            except (json.JSONDecodeError, Exception):
                continue
        
        # Try combining cleanups
        try:
            cleaned = json_str
            for cleanup in cleanups[1:]:  # Skip the identity function
                cleaned = cleanup(cleaned)
            result = json.loads(cleaned)
            if isinstance(result, dict):
                return result
        except Exception:
            pass
        
        return None
    
    def _parse_geval_criterion(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Parse a G-Eval criterion response with fallback strategies.
        Expected format: {"reasoning": [...], "score": N, "summary": "..."}
        """
        import re
        
        response = response.strip()
        
        # Remove markdown code blocks
        if '```json' in response:
            match = re.search(r'```json\s*([\s\S]*?)\s*```', response)
            if match:
                response = match.group(1)
        elif '```' in response:
            match = re.search(r'```\s*([\s\S]*?)\s*```', response)
            if match:
                response = match.group(1)
        
        # Try JSON parsing first
        json_result = self._try_parse_json(response)
        
        # If that didn't work, try extracting first { to last }
        if not json_result:
            first_brace = response.find('{')
            last_brace = response.rfind('}')
            if first_brace != -1 and last_brace > first_brace:
                json_result = self._try_parse_json(response[first_brace:last_brace + 1])
        
        # If we got a result, validate and return
        if json_result:
            return {
                "score": float(json_result.get("score", 0)),
                "reasoning": json_result.get("reasoning", []),
                "summary": json_result.get("summary", "")
            }
        
        # Fallback: extract with regex
        try:
            # Extract score
            score = 0
            score_match = re.search(r'["\']?score["\']?\s*:\s*(\d+(?:\.\d+)?)', response, re.IGNORECASE)
            if score_match:
                score = float(score_match.group(1))
            
            # Extract summary
            summary = ""
            summary_match = re.search(r'["\']?summary["\']?\s*:\s*["\']([^"\']+)["\']', response, re.IGNORECASE)
            if summary_match:
                summary = summary_match.group(1)
            
            # Extract reasoning (look for array-like content)
            reasoning = []
            # Try to find array content
            array_match = re.search(r'\[([^\]]+)\]', response)
            if array_match:
                # Split by quotes and commas
                items = re.findall(r'["\']([^"\']+)["\']', array_match.group(1))
                reasoning = items[:4]  # Take up to 4 items
            
            if score > 0:
                return {
                    "score": score,
                    "reasoning": reasoning,
                    "summary": summary
                }
        except Exception:
            pass
        
        return None

    def evaluate_prompt_geval(
        self, 
        prompt_content: str, 
        criteria: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate a prompt using G-Eval with Chain-of-Thought reasoning.
        
        G-Eval (NeurIPS 2023) differs from evaluate_prompt() by:
        - Generating evaluation STEPS first (Chain-of-Thought)
        - Having the model reason through each step before scoring
        - Providing more transparent, explainable evaluations
        
        Both methods are FREE when using local models - use both for robust evaluation!
        
        Args:
            prompt_content: The prompt text to evaluate
            criteria: List of criteria to evaluate. Options:
                      coherence, clarity, effectiveness, relevance, safety, completeness
                      Default: ["coherence", "clarity", "effectiveness", "relevance"]
        
        Returns:
            Dict with scores, reasoning steps, and overall assessment
        """
        if criteria is None:
            criteria = ["coherence", "clarity", "effectiveness", "relevance"]
        
        # G-Eval criteria definitions with evaluation steps
        GEVAL_CRITERIA = {
            "coherence": {
                "description": "The collective quality of all sentences - logical flow and structure",
                "steps": [
                    "Identify the main topic and purpose",
                    "Check for clear beginning, middle, end structure", 
                    "Assess logical flow between ideas",
                    "Check for contradictions or confusion"
                ]
            },
            "clarity": {
                "description": "How easy the prompt is to understand and follow",
                "steps": [
                    "Read from a first-time user perspective",
                    "Identify ambiguous words or instructions",
                    "Check if placeholders are clearly named",
                    "Assess if expected output format is clear"
                ]
            },
            "effectiveness": {
                "description": "How likely to produce quality outputs consistently",
                "steps": [
                    "Consider what response this would generate",
                    "Evaluate if instructions are specific enough",
                    "Check for guardrails against failure modes",
                    "Assess cross-model compatibility"
                ]
            },
            "relevance": {
                "description": "How well the prompt addresses its stated purpose",
                "steps": [
                    "Identify the stated goal",
                    "Check if all components contribute to that goal",
                    "Evaluate for off-topic elements",
                    "Assess if important aspects are missing"
                ]
            },
            "safety": {
                "description": "Whether the prompt avoids harmful patterns",
                "steps": [
                    "Check for instructions leading to harmful outputs",
                    "Evaluate guardrails presence",
                    "Assess misuse potential",
                    "Consider bias and privacy implications"
                ]
            },
            "completeness": {
                "description": "Whether the prompt covers all necessary aspects",
                "steps": [
                    "Identify the task being addressed",
                    "List what information would be needed",
                    "Check if sufficient context is provided",
                    "Assess if examples and edge cases are covered"
                ]
            }
        }
        
        results = {"method": "g-eval-cot", "criteria_results": {}}
        all_scores = []
        
        for criterion in criteria:
            if criterion not in GEVAL_CRITERIA:
                continue
                
            defn = GEVAL_CRITERIA[criterion]
            steps_text = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(defn["steps"]))
            
            geval_prompt = f"""You are evaluating a prompt for {criterion.upper()}.

Definition: {defn["description"]}

Evaluation Steps (follow each in order):
{steps_text}

PROMPT TO EVALUATE:
```
{prompt_content[:3000]}
```

Think through each evaluation step, then score 1-5.
Return ONLY valid JSON:
{{"reasoning": ["step 1 observation", "step 2 observation", "step 3 observation", "step 4 observation"], "score": N, "summary": "brief assessment"}}"""

            response = self.generate(geval_prompt, max_tokens=600, temperature=0.3)
            
            # Parse response with improved parsing
            parsed = self._parse_geval_criterion(response)
            if parsed:
                score = parsed.get("score", 0)
                all_scores.append(score)
                results["criteria_results"][criterion] = parsed
            else:
                results["criteria_results"][criterion] = {
                    "score": 0,
                    "error": "Could not parse response"
                }
        
        # Calculate overall - normalize to 1-10 scale (G-Eval uses 1-5, multiply by 2)
        # This makes G-Eval scores comparable to evaluate_prompt() which uses 1-10
        normalized_scores = {c: min(r.get("score", 0) * 2, 10) for c, r in results["criteria_results"].items()}
        results["scores"] = normalized_scores
        results["scores_raw"] = {c: r.get("score", 0) for c, r in results["criteria_results"].items()}  # Keep original 1-5 scores
        all_normalized = [s * 2 for s in all_scores]
        results["overall"] = round(sum(all_normalized) / len(all_normalized), 2) if all_normalized else 0
        results["overall_raw"] = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0  # Keep original
        
        return results
    
    def evaluate_prompt_dual(self, prompt_content: str) -> Dict[str, Any]:
        """
        Run BOTH evaluation methods and return combined results.
        
        This gives you the most robust evaluation by combining:
        - evaluate_prompt(): Direct 6-criteria scoring
        - evaluate_prompt_geval(): Chain-of-Thought reasoning first
        
        Both are FREE when using local models!
        
        Returns:
            Dict with results from both methods and a combined score
        """
        direct_result = self.evaluate_prompt(prompt_content)
        geval_result = self.evaluate_prompt_geval(prompt_content)
        
        # Average the two overall scores
        direct_score = direct_result.get("overall", 0)
        geval_score = geval_result.get("overall", 0)
        
        valid_scores = [s for s in [direct_score, geval_score] if s > 0]
        combined_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
        
        return {
            "combined_score": round(combined_score, 2),
            "direct_evaluation": direct_result,
            "geval_evaluation": geval_result,
            "method": "dual-evaluation"
        }


def check_model_available() -> bool:
    """Check if a local model is available."""
    return _resolve_model_path(None) is not None


def get_model_info() -> Dict[str, Any]:
    """Get information about available local models."""
    info = {
        "available": False,
        "paths_checked": [str(_AI_GALLERY_ROOT)],
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
    found = _resolve_model_path(None)
    if found:
        info["available"] = True
        info["found_path"] = str(found)
        try:
            model_files = list(found.glob("*.onnx"))
            info["model_files"] = [f.name for f in model_files]
        except OSError:
            info["model_files"] = []
    
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
            model = LocalModel(model_path=args.model_path, verbose=args.verbose)
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

            model = LocalModel(model_path=args.model_path, verbose=args.verbose)
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
