from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class PerformanceLevel(Enum):
    EXCEPTIONAL = "Exceptional"
    PROFICIENT = "Proficient"
    COMPETENT = "Competent"
    DEVELOPING = "Developing"
    INADEQUATE = "Inadequate"


@dataclass
class Criterion:
    name: str
    description: str
    weight: float = 1.0  # internal relative weight if needed, usually just average


@dataclass
class Dimension:
    id: str
    name: str
    weight: float
    description: str
    criteria: List[Criterion]
    rubric: Dict[PerformanceLevel, Dict[str, str]]


@dataclass
class EvaluationResult:
    dimension_id: str
    score: float
    level: PerformanceLevel
    evidence: List[str]
    reasoning: str
