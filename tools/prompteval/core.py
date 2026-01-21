"""Legacy PromptEval API (minimal).

Some tests expect a `PromptEval` class with a `_run_geval` method that parses a
JSON response containing a numeric `score`.

This file intentionally implements only the narrow surface area needed by the
test suite.
"""

from __future__ import annotations

import json
from typing import Any

from .config import EvalConfig


class PromptEval:
    def __init__(self, cfg: EvalConfig):
        self.cfg = cfg
        self.llm_client: Any | None = None

    def _run_geval(self, content: str) -> dict:
        """Run a single G-Eval style judge call and normalize to 0..100.

        Expected judge response format (string):
            {"reasoning": "...", "score": 3.5}

        The legacy tests treat the score as 0..5 and scale it by 20.
        """
        if self.llm_client is None:
            raise RuntimeError("PromptEval.llm_client must be set")

        raw = self.llm_client.generate_text(
            model_name=self.cfg.model,
            prompt=content,
            temperature=self.cfg.temperature,
            max_tokens=self.cfg.max_tokens,
        )

        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = {}

        score = parsed.get("score")
        if score is None:
            score_val = 0.0
        else:
            try:
                score_val = float(score)
            except Exception:
                score_val = 0.0

        # Legacy normalization: 0..5 => 0..100
        score_pct = max(0.0, min(100.0, score_val * 20.0))

        return {
            "clarity": {
                "score": score_pct,
                "reasoning": parsed.get("reasoning", ""),
            }
        }
