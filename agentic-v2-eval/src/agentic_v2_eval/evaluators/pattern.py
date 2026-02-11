"""Pattern-based scoring for complex prompts (ReAct, CoVe, etc.)."""

import json
import re
import statistics
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from agentic_v2_eval.interfaces import LLMClientProtocol
from agentic_v2_eval.rubrics import load_rubric
from .base import EvaluatorRegistry

@dataclass
class PatternScore:
    """Result from pattern (complex) prompt scoring."""

    prompt_file: str
    pattern: str

    # Universal dimension scores (7 dimensions)
    universal_scores: Dict[str, float]  # PIF, POI, PC, CA, SRC, PR, IR

    # Pattern-specific scores
    pattern_scores: Dict[str, float]  # R1-R3, C1-C3, F1-F3, G1-G3

    # Aggregated
    overall_universal: float  # 0-35
    overall_pattern: float  # varies by pattern
    combined_score: float

    # Pass/fail
    hard_gates_passed: bool
    hard_gate_failures: List[str] = field(default_factory=list)
    failures: List[str] = field(default_factory=list)

    # Stats
    pass_rate: float = 1.0
    confidence: float = 1.0
    model: str = ""
    # Metadata
    eval_type: str = "pattern"
    runs: int = 20
    temperature: float = 0.1
    successful_runs: int = 0

    def to_dict(self) -> dict:
        return {
            "eval_type": self.eval_type,
            "prompt_file": self.prompt_file,
            "pattern": self.pattern,
            "model": self.model,
            "runs": self.runs,
            "successful_runs": self.successful_runs,
            "temperature": self.temperature,
            "universal_scores": self.universal_scores,
            "pattern_scores": self.pattern_scores,
            "overall_universal": self.overall_universal,
            "overall_pattern": self.overall_pattern,
            "combined_score": self.combined_score,
            "hard_gates_passed": self.hard_gates_passed,
            "hard_gate_failures": self.hard_gate_failures,
            "failures": self.failures,
            "pass_rate": self.pass_rate,
            "confidence": self.confidence,
        }

# =============================================================================
# CONSTANTS & PROMPTS (Loaded from YAML)
# =============================================================================

def _load_pattern_data():
    """Load pattern data from rubrics/prompt_pattern.yaml."""
    instructions = {}
    fields = {}
    phases = {}
    state_machines = {}
    judge_prompt = ""
    
    try:
        data = load_rubric("prompt_pattern")
        judge_prompt = data.get("judge_prompt", "")
        
        patterns = data.get("patterns", {})
        for name, pdata in patterns.items():
            instructions[name] = pdata.get("instructions", "")
            fields[name] = pdata.get("score_fields", "")
            phases[name] = pdata.get("phases", [])
            state_machines[name] = pdata.get("state_machine", "")
            
    except Exception as e:
        print(f"Warning: Failed to load prompt_pattern.yaml: {e}")
        
    return judge_prompt, instructions, fields, phases, state_machines

(
    PATTERN_JUDGE_PROMPT,
    PATTERN_SPECIFIC_INSTRUCTIONS,
    PATTERN_SCORE_FIELDS,
    PATTERN_PHASES,
    PATTERN_STATE_MACHINES
) = _load_pattern_data()

# =============================================================================
# SCORING LOGIC
# =============================================================================

@EvaluatorRegistry.register("pattern")
class PatternEvaluator:
    """Evaluator for Agentic Patterns."""
    
    def __init__(self, llm_client: LLMClientProtocol):
        self.llm_client = llm_client

    def score_pattern(
        self,
        prompt_name: str,
        prompt_content: str,
        model_output: str,
        pattern: str,
        model: str = "gh:gpt-4o",
        runs: int = 1, # Default reduced for speed, usually 20
        temperature: float = 0.1,
    ) -> PatternScore:
        """Score a prompt using pattern (complex) evaluation."""
        
        pattern = pattern.lower()
        if pattern not in PATTERN_PHASES:
             # Just a basic validation, could be extended
             valid_patterns = list(PATTERN_PHASES.keys())
             raise ValueError(f"Unknown pattern: {pattern}. Must be one of: {valid_patterns}")

        # Safe formatting
        safe_prompt_content = prompt_content.replace("{", "{{").replace("}", "}}")
        safe_model_output = model_output.replace("{", "{{").replace("}", "}}")
        
        judge_prompt = PATTERN_JUDGE_PROMPT.format(
            pattern_name=pattern.upper(),
            phases=", ".join(PATTERN_PHASES[pattern]),
            state_machine=PATTERN_STATE_MACHINES[pattern],
            pattern_specific_instructions=PATTERN_SPECIFIC_INSTRUCTIONS.get(pattern, ""),
            pattern_score_fields=PATTERN_SCORE_FIELDS.get(pattern, ""),
            prompt_content=safe_prompt_content,
            model_output=safe_model_output,
        )

        all_results = []
        for i in range(runs):
            try:
                response = self.llm_client.generate_text(
                    model_name=model,
                    prompt=judge_prompt,
                    temperature=temperature,
                )
                
                result = self._parse_json_response(response)
                if result:
                    all_results.append(result)
            except Exception as e:
                print(f"Pattern eval run {i+1} failed: {e}")

        if not all_results:
             return self._create_empty_score(prompt_name, pattern, model, runs)

        # Robust aggregation: median across all successful runs
        universal = self._aggregate_scores(
            [r.get("universal_scores", {}) for r in all_results]
        )
        pattern_s = self._aggregate_scores(
            [r.get("pattern_scores", {}) for r in all_results]
        )

        # Universal: sum of 0-5 dimensions (PIF, POI, PC, CA, SRC, IR → max 30)
        uni_keys = ["PIF", "POI", "PC", "CA", "SRC", "IR"]
        overall_uni = sum(universal.get(k, 0) for k in uni_keys)

        # Pattern-specific total
        overall_pat = sum(pattern_s.values())

        # Hard gates check (using aggregated medians)
        hard_gates_passed = True
        hard_failures: List[str] = []

        if universal.get("POI", 0) < 4:
            hard_gates_passed = False
            hard_failures.append("Phase Ordering Integrity < 4")
        if universal.get("PC", 0) < 4:
            hard_gates_passed = False
            hard_failures.append("Phase Completeness < 4")
        if universal.get("CA", 0) < 4:
            hard_gates_passed = False
            hard_failures.append("Constraint Adherence < 4")
        if universal.get("PR", 0) < 0.75:
            hard_gates_passed = False
            hard_failures.append("Pattern Robustness < 0.75")

        # Aggregate failures and confidence across runs
        all_failures: List[str] = []
        for r in all_results:
            all_failures.extend(r.get("failures", []))
        unique_failures = list(dict.fromkeys(all_failures))  # dedupe, preserve order

        confidences = [r.get("confidence", 1.0) for r in all_results]
        median_confidence = statistics.median(confidences) if confidences else 1.0

        return PatternScore(
            prompt_file=prompt_name,
            pattern=pattern,
            universal_scores=universal,
            pattern_scores=pattern_s,
            overall_universal=overall_uni,
            overall_pattern=overall_pat,
            combined_score=overall_uni + overall_pat,
            hard_gates_passed=hard_gates_passed,
            hard_gate_failures=hard_failures,
            failures=unique_failures,
            pass_rate=len(all_results) / runs if runs > 0 else 0.0,
            confidence=median_confidence,
            model=model,
            runs=runs,
            successful_runs=len(all_results),
        )

    @staticmethod
    def _aggregate_scores(score_dicts: List[Dict[str, float]]) -> Dict[str, float]:
        """Aggregate multiple score dicts using median per key."""
        if not score_dicts:
            return {}
        all_keys: set[str] = set()
        for d in score_dicts:
            all_keys.update(d.keys())
        aggregated: Dict[str, float] = {}
        for key in sorted(all_keys):
            values = [d[key] for d in score_dicts if key in d]
            aggregated[key] = statistics.median(values) if values else 0
        return aggregated

    def _create_empty_score(self, prompt_file: str, pattern: str, model: str, runs: int) -> PatternScore:
        return PatternScore(
            prompt_file=prompt_file,
            pattern=pattern,
            universal_scores={},
            pattern_scores={},
            overall_universal=0.0,
            overall_pattern=0.0,
            combined_score=0.0,
            hard_gates_passed=False,
            hard_gate_failures=["Execution failed"],
            failures=["No valid JSON response from judge"],
            model=model,
            runs=runs
        )

    def _parse_json_response(self, text: str) -> Optional[dict]:
        """Extract and parse JSON from text (handles markdown blocks)."""
        # remove markdown code blocks
        match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            text = match.group(1)
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Fallback: find first { and last }
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1:
                try:
                    return json.loads(text[start:end+1])
                except:
                    pass
            return None
