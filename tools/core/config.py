import os
from dataclasses import dataclass


@dataclass
class ModelConfig:
    # Defaults chosen to be broadly available and work out-of-the-box.
    # Override via GEN_MODEL / REV_MODEL / REF_MODEL as needed.
    generator_model: str = "gpt-4o-mini"
    reviewer_model: str = "gpt-4o-mini"
    refiner_model: str = "gpt-4o-mini"
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
            generator_model=os.getenv("GEN_MODEL", "gpt-4o-mini"),
            reviewer_model=os.getenv("REV_MODEL", "gpt-4o-mini"),
            refiner_model=os.getenv("REF_MODEL", "gpt-4o-mini")
        )
        self.paths = PathConfig()


# Global config instance
default_config = Config()
