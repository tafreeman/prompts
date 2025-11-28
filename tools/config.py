import os
from dataclasses import dataclass


@dataclass
class ModelConfig:
    generator_model: str = "gemini-1.5-pro"
    reviewer_model: str = "claude-sonnet-4"
    refiner_model: str = "gemini-1.5-pro"
    generator_temp: float = 0.7
    reviewer_temp: float = 0.0
    refiner_temp: float = 0.5


@dataclass
class PathConfig:
    templates_dir: str = "prompts/"
    instructions_dir: str = "instructions/"
    rubric_path: str = "tools/rubrics/quality_standards.json"


class Config:
    """
    Centralized configuration for the Universal Code Generator.
    Loads from environment variables or uses defaults.
    """
    def __init__(self):
        self.models = ModelConfig(
            generator_model=os.getenv("GEN_MODEL", "gemini-1.5-pro"),
            reviewer_model=os.getenv("REV_MODEL", "claude-sonnet-4"),
            refiner_model=os.getenv("REF_MODEL", "gemini-1.5-pro")
        )
        self.paths = PathConfig()


# Global config instance
default_config = Config()
