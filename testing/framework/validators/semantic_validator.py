"""
Semantic Validator for Prompt Templates

Validates the semantic correctness of prompts, including:
- Logical coherence and flow
- Intent clarity
- Consistency of instructions
- Semantic completeness
"""

import re
from typing import Any, Dict, List, Optional, Tuple
import logging

from .base_validator import BaseValidator

logger = logging.getLogger(__name__)


class SemanticValidator(BaseValidator):
    """
    Validates semantic correctness of prompt content.
    
    Checks for:
    - Logical coherence between sections
    - Consistent terminology
    - Clear intent and purpose
    - Semantic completeness
    - Contradiction detection
    """
    
    # Keywords indicating different prompt intents
    INTENT_KEYWORDS = {
        'analysis': ['analyze', 'examine', 'evaluate', 'assess', 'review', 'investigate'],
        'generation': ['create', 'generate', 'write', 'produce', 'compose', 'develop'],
        'transformation': ['convert', 'transform', 'translate', 'reformat', 'modify'],
        'extraction': ['extract', 'identify', 'find', 'locate', 'detect', 'parse'],
        'summarization': ['summarize', 'condense', 'brief', 'outline', 'abstract'],
        'classification': ['classify', 'categorize', 'label', 'sort', 'group'],
        'comparison': ['compare', 'contrast', 'differentiate', 'distinguish'],
        'explanation': ['explain', 'describe', 'clarify', 'elaborate', 'define'],
    }
    
    # Contradiction patterns (pairs that shouldn't appear together)
    CONTRADICTION_PATTERNS = [
        (r'\bbrief\b', r'\bdetailed\b'),
        (r'\bsimple\b', r'\bcomplex\b'),
        (r'\bshort\b', r'\blong\b'),
        (r'\bignore\b', r'\binclude\b'),
        (r'\bskip\b', r'\bmust include\b'),
    ]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize semantic validator with configuration."""
        super().__init__(config)
        self.min_coherence_score = config.get('min_coherence_score', 0.6) if config else 0.6
        self.require_clear_intent = config.get('require_clear_intent', True) if config else True
    
    async def validate(self, output: Any, expected: Optional[Any] = None) -> bool:
        """
        Validate semantic correctness of prompt content.
        
        Args:
            output: The prompt content to validate
            expected: Optional expected semantic properties (dict with keys like 'intent', 'topics')
            
        Returns:
            bool: True if semantically valid, False otherwise
        """
        self.clear_messages()
        
        if not output:
            self.add_error("No content provided for semantic validation")
            return False
        
        content = str(output)
        is_valid = True
        
        # Check intent clarity
        intent_valid, detected_intents = self._validate_intent(content)
        if not intent_valid and self.require_clear_intent:
            is_valid = False
        
        # Check for contradictions
        contradictions = self._detect_contradictions(content)
        if contradictions:
            for contra in contradictions:
                self.add_warning(f"Potential contradiction detected: '{contra[0]}' vs '{contra[1]}'")
        
        # Check logical coherence
        coherence_score = self._calculate_coherence(content)
        if coherence_score < self.min_coherence_score:
            self.add_warning(f"Low coherence score: {coherence_score:.2f} (minimum: {self.min_coherence_score})")
        
        # Check semantic completeness
        completeness_issues = self._check_completeness(content, detected_intents)
        for issue in completeness_issues:
            self.add_warning(issue)
        
        # Validate against expected semantics if provided
        if expected and isinstance(expected, dict):
            expected_intent = expected.get('intent')
            if expected_intent and expected_intent not in detected_intents:
                self.add_error(f"Expected intent '{expected_intent}' not detected in content")
                is_valid = False
            
            expected_topics = expected.get('topics', [])
            for topic in expected_topics:
                if topic.lower() not in content.lower():
                    self.add_warning(f"Expected topic '{topic}' not found in content")
        
        return is_valid and len(self.validation_errors) == 0
    
    def _validate_intent(self, content: str) -> Tuple[bool, List[str]]:
        """
        Validate that the prompt has a clear intent.
        
        Returns:
            Tuple of (is_valid, list of detected intents)
        """
        content_lower = content.lower()
        detected_intents = []
        
        for intent, keywords in self.INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in content_lower:
                    detected_intents.append(intent)
                    break
        
        if not detected_intents:
            self.add_warning("No clear intent detected in prompt. Consider adding action verbs.")
            return False, []
        
        # Multiple conflicting intents might indicate unclear purpose
        if len(detected_intents) > 3:
            self.add_warning(f"Multiple intents detected ({len(detected_intents)}). Consider focusing the prompt.")
        
        return True, list(set(detected_intents))
    
    def _detect_contradictions(self, content: str) -> List[Tuple[str, str]]:
        """Detect potential contradictions in the content."""
        content_lower = content.lower()
        contradictions = []
        
        for pattern1, pattern2 in self.CONTRADICTION_PATTERNS:
            match1 = re.search(pattern1, content_lower)
            match2 = re.search(pattern2, content_lower)
            
            if match1 and match2:
                # Only flag if they're in relatively close proximity (same paragraph)
                pos1, pos2 = match1.start(), match2.start()
                if abs(pos1 - pos2) < 500:  # Within ~500 characters
                    contradictions.append((match1.group(), match2.group()))
        
        return contradictions
    
    def _calculate_coherence(self, content: str) -> float:
        """
        Calculate a coherence score for the content.
        
        Higher scores indicate better logical flow and structure.
        """
        score = 1.0
        
        # Check for section markers and structure
        has_sections = bool(re.search(r'^##?\s+\w+', content, re.MULTILINE))
        if not has_sections:
            score -= 0.1
        
        # Check for numbered lists or clear steps
        has_steps = bool(re.search(r'^\s*\d+[\.\)]\s+', content, re.MULTILINE))
        has_bullets = bool(re.search(r'^\s*[-*]\s+', content, re.MULTILINE))
        if has_steps or has_bullets:
            score += 0.1
        
        # Check for transition words indicating logical flow
        transition_words = [
            'first', 'second', 'then', 'next', 'finally', 
            'however', 'therefore', 'because', 'if', 'when',
            'additionally', 'furthermore', 'moreover'
        ]
        content_lower = content.lower()
        transition_count = sum(1 for word in transition_words if word in content_lower)
        score += min(0.2, transition_count * 0.05)
        
        # Penalize very short content
        word_count = len(content.split())
        if word_count < 50:
            score -= 0.2
        
        # Penalize very long unstructured content
        if word_count > 1000 and not has_sections:
            score -= 0.2
        
        return max(0.0, min(1.0, score))
    
    def _check_completeness(self, content: str, intents: List[str]) -> List[str]:
        """Check for semantic completeness based on detected intents."""
        issues = []
        content_lower = content.lower()
        
        # Check for output format specification
        output_keywords = ['output', 'result', 'response', 'return', 'format', 'produce']
        if not any(kw in content_lower for kw in output_keywords):
            issues.append("Consider specifying the expected output format")
        
        # Intent-specific checks
        if 'analysis' in intents:
            analysis_elements = ['criteria', 'factor', 'aspect', 'dimension', 'consider']
            if not any(elem in content_lower for elem in analysis_elements):
                issues.append("Analysis prompts should specify criteria or aspects to consider")
        
        if 'generation' in intents:
            gen_elements = ['style', 'tone', 'length', 'format', 'example']
            if not any(elem in content_lower for elem in gen_elements):
                issues.append("Generation prompts should specify style, tone, or format")
        
        if 'classification' in intents:
            class_elements = ['categor', 'class', 'label', 'type', 'group']
            if not any(elem in content_lower for elem in class_elements):
                issues.append("Classification prompts should define the categories or classes")
        
        return issues
    
    def get_semantic_analysis(self, content: str) -> Dict[str, Any]:
        """
        Get a comprehensive semantic analysis of the content.
        
        Returns a dictionary with semantic properties and metrics.
        """
        _, detected_intents = self._validate_intent(content)
        contradictions = self._detect_contradictions(content)
        coherence = self._calculate_coherence(content)
        completeness_issues = self._check_completeness(content, detected_intents)
        
        return {
            'detected_intents': detected_intents,
            'contradictions': contradictions,
            'coherence_score': coherence,
            'completeness_issues': completeness_issues,
            'word_count': len(content.split()),
            'has_structure': bool(re.search(r'^##?\s+\w+', content, re.MULTILINE)),
            'has_examples': 'example' in content.lower(),
            'has_constraints': any(word in content.lower() for word in ['must', 'should', 'required', 'constraint']),
        }
