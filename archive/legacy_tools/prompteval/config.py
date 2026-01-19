from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from enum import Enum, IntEnum
from pathlib import Path
from datetime import datetime
import json

class Tier(IntEnum):
    """Evaluation tiers with increasing rigor and cost."""
    STRUCTURAL = 0      # No LLM - structural analysis only ($0, <1s)
    LOCAL_QUICK = 1     # Single local model, 1 run ($0, ~30s)
    LOCAL_GEVAL = 2     # Local model with G-Eval reasoning ($0, ~60s)
    LOCAL_CROSS = 3     # 3 local models x 2 runs ($0, ~5min)
    CLOUD_QUICK = 4     # Single cloud model ($0.01, ~5s)
    CLOUD_CROSS = 5     # 3 cloud models x 2 runs ($0.10, ~30s)
    PREMIUM = 6         # 5 models x 3 runs + reproducibility ($0.30, ~2min)
    ENTERPRISE = 7      # Full pipeline + CoVe ($0.50, ~5min)


@dataclass
class CriterionScore:
    """Score for a single evaluation criterion."""
    name: str
    score: float           # 0-100 normalized
    weight: float          # 0.0-1.0
    grade: str             # "Exceptional", "Proficient", etc.
    reasoning: str = ""    # G-Eval reasoning (if available)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvalResult:
    """Complete evaluation result for a prompt."""
    file_path: str
    title: str
    category: str
    
    # Scores
    overall_score: float           # 0-100 weighted average
    structural_score: float        # 0-100 from static analysis
    geval_score: Optional[float]   # 0-100 from G-Eval (if run)
    
    # Breakdown
    criteria: List[CriterionScore] = field(default_factory=list)
    
    # Metadata
    grade: str = ""                # "Exceptional", "Proficient", etc.
    passed: bool = False           # Met threshold?
    threshold: float = 70.0
    
    # Execution info
    model: str = ""
    tier: int = 2
    duration_seconds: float = 0.0
    timestamp: str = ""
    
    # Recommendations
    recommendations: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class EvalConfig:
    """Configuration for evaluation run."""
    tier: Tier = Tier.LOCAL_GEVAL
    threshold: float = 70.0
    model: str = "local:phi4mini"
    path: Path = field(default_factory=lambda: Path("prompts"))
    recursive: bool = True
    output: Optional[Path] = None
    output_format: str = "console"  # console, json, markdown
    verbose: bool = False
    parallel: int = 1
    
    # Scoring weights (from prompt-scoring.yaml)
    weights: Dict[str, float] = field(default_factory=lambda: {
        "clarity": 0.25,
        "effectiveness": 0.30,
        "reusability": 0.20,
        "simplicity": 0.15,
        "examples": 0.10,
    })
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['tier'] = self.tier.value
        result['path'] = str(self.path)
        if self.output:
            result['output'] = str(self.output)
        return result
