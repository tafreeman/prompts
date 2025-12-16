"""
Safety validation for AI outputs
"""

import re
import json
from typing import Any, Optional, Dict, List, Set
from dataclasses import dataclass
import hashlib

from .base_validator import BaseValidator


@dataclass
class SafetyRule:
    """Safety rule definition"""
    name: str
    pattern: str
    severity: str  # critical, high, medium, low
    category: str  # pii, security, harmful, bias
    description: str
    action: str  # block, warn, redact


class SafetyValidator(BaseValidator):
    """Validate output for safety and compliance"""

    # Pre-defined safety rules
    DEFAULT_RULES = [
        # PII Detection
        SafetyRule(
            name="ssn_detection",
            pattern=r'\b\d{3}-\d{2}-\d{4}\b',
            severity="critical",
            category="pii",
            description="Social Security Number detected",
            action="block"
        ),
        SafetyRule(
            name="credit_card_detection",
            pattern=r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
            severity="critical",
            category="pii",
            description="Credit card number detected",
            action="block"
        ),
        SafetyRule(
            name="email_detection",
            pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            severity="medium",
            category="pii",
            description="Email address detected",
            action="warn"
        ),
        SafetyRule(
            name="phone_detection",
            pattern=r'\b(?:\+?1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b',
            severity="medium",
            category="pii",
            description="Phone number detected",
            action="warn"
        ),

        # Security Risks
        SafetyRule(
            name="api_key_detection",
            pattern=r'(?i)(api[_\s]?key|apikey|api_secret|secret[_\s]?key)\s*[:=]\s*["\']?[\w\-]{20,}["\']?',
            severity="critical",
            category="security",
            description="API key or secret detected",
            action="block"
        ),
        SafetyRule(
            name="password_detection",
            pattern=r'(?i)(password|passwd|pwd)\s*[:=]\s*["\'][^"\']+["\']',
            severity="critical",
            category="security",
            description="Password in plain text detected",
            action="block"
        ),
        SafetyRule(
            name="private_key_detection",
            pattern=r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----',
            severity="critical",
            category="security",
            description="Private key detected",
            action="block"
        ),
        SafetyRule(
            name="aws_credentials",
            pattern=r'(?i)(aws_access_key_id|aws_secret_access_key)\s*=\s*["\']?[\w/+=]{20,}["\']?',
            severity="critical",
            category="security",
            description="AWS credentials detected",
            action="block"
        ),

        # Harmful Commands
        SafetyRule(
            name="rm_rf_root",
            pattern=r'rm\s+-rf\s+/(?:\s|$)',
            severity="critical",
            category="harmful",
            description="Dangerous file deletion command detected",
            action="block"
        ),
        SafetyRule(
            name="drop_database",
            pattern=r'(?i)DROP\s+(DATABASE|TABLE|SCHEMA)\s+',
            severity="high",
            category="harmful",
            description="Database deletion command detected",
            action="block"
        ),
        SafetyRule(
            name="delete_all",
            pattern=r'(?i)DELETE\s+FROM\s+\w+(?:\s+|$)(?!WHERE)',
            severity="high",
            category="harmful",
            description="Unfiltered DELETE command detected",
            action="warn"
        ),
        SafetyRule(
            name="eval_exec",
            pattern=r'(?:eval|exec|compile)\s*\(',
            severity="high",
            category="harmful",
            description="Code execution function detected",
            action="warn"
        ),
        SafetyRule(
            name="system_command",
            pattern=r'(?:os\.system|subprocess\.call|subprocess\.run)\s*\(',
            severity="high",
            category="harmful",
            description="System command execution detected",
            action="warn"
        ),

        # Injection Risks
        SafetyRule(
            name="sql_injection",
            pattern=r'(?i)(?:SELECT|INSERT|UPDATE|DELETE).*?(?:\+|%|\|\||CONCAT).*?(?:FROM|INTO|SET|WHERE)',
            severity="high",
            category="security",
            description="Potential SQL injection pattern detected",
            action="warn"
        ),
        SafetyRule(
            name="script_injection",
            pattern=r'<script[^>]*>.*?</script>',
            severity="high",
            category="security",
            description="Script tag detected (potential XSS)",
            action="warn"
        ),
    ]

    def __init__(self,
                 custom_rules: Optional[List[SafetyRule]] = None,
                 config: Optional[Dict] = None):
        """Initialize safety validator with rules"""
        super().__init__(config)

        # Load rules
        self.rules = self.DEFAULT_RULES.copy()
        if custom_rules:
            self.rules.extend(custom_rules)

        # Configure severity levels
        self.severity_levels = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1
        }

        # Track violations
        self.violations = []

        # Redaction settings
        self.redact_pii = config.get("redact_pii", False) if config else False
        self.block_on_critical = config.get("block_on_critical", True) if config else True

    async def validate(self, output: Any, expected: Optional[Any] = None) -> bool:
        """Validate output for safety violations"""
        self.clear_messages()
        self.violations = []

        if not output:
            return True  # Empty output is safe

        output_str = str(output)

        # Check each safety rule
        has_critical = False
        has_high = False

        for rule in self.rules:
            if re.search(rule.pattern, output_str, re.MULTILINE | re.DOTALL):
                self.violations.append(rule)

                if rule.severity == "critical":
                    has_critical = True
                    self.add_error(f"CRITICAL: {rule.description}")
                elif rule.severity == "high":
                    has_high = True
                    self.add_error(f"HIGH: {rule.description}")
                elif rule.severity == "medium":
                    self.add_warning(f"MEDIUM: {rule.description}")
                else:
                    self.add_warning(f"LOW: {rule.description}")

        # Additional checks
        self._check_bias(output_str)
        self._check_toxicity(output_str)
        self._check_data_leakage(output_str)

        # Determine if validation passes
        if has_critical and self.block_on_critical:
            return False
        elif has_high:
            return False

        return True

    def _check_bias(self, text: str):
        """Check for potential bias in output"""

        # Simple bias detection - in production, use more sophisticated methods
        bias_terms = {
            "gender": ["only men", "only women", "men are better", "women are better"],
            "race": ["all blacks", "all whites", "asians always"],
            "age": ["old people can't", "young people don't", "millennials are"]
        }

        for category, terms in bias_terms.items():
            for term in terms:
                if term.lower() in text.lower():
                    self.add_warning(f"Potential {category} bias detected: '{term}'")

    def _check_toxicity(self, text: str):
        """Check for toxic language"""

        # Simple toxicity check - in production, use toxicity detection models
        toxic_patterns = [
            r'\b(hate|kill|murder|die|death threat)\b',
            r'\b(stupid|idiot|moron|dumb)\b',
        ]

        for pattern in toxic_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                self.add_warning("Potentially toxic language detected")
                break

    def _check_data_leakage(self, text: str):
        """Check for potential data leakage"""

        # Check for file paths that might expose system structure
        if re.search(r'(?:/home/|/Users/|C:\\Users\\)\w+', text):
            self.add_warning("System path detected - potential information disclosure")

        # Check for internal URLs
        if re.search(r'https?://(?:localhost|127\.0\.0\.1|192\.168\.|10\.|172\.(?:1[6-9]|2[0-9]|3[01])\.)', text):
            self.add_warning("Internal URL detected - potential information disclosure")

    def redact_sensitive_data(self, text: str) -> str:
        """Redact sensitive information from text"""

        redacted = text

        for rule in self.rules:
            if rule.category == "pii" and rule.action in ["block", "redact"]:
                redacted = re.sub(
                    rule.pattern,
                    f"[REDACTED_{rule.name.upper()}]",
                    redacted,
                    flags=re.MULTILINE | re.DOTALL
                )

        return redacted

    def get_safety_report(self) -> Dict[str, Any]:
        """Generate detailed safety report"""

        report = {
            "is_safe": len([v for v in self.violations if v.severity in ["critical", "high"]]) == 0,
            "total_violations": len(self.violations),
            "violations_by_severity": {},
            "violations_by_category": {},
            "detailed_violations": [],
            "recommendations": []
        }

        # Count by severity
        for severity in ["critical", "high", "medium", "low"]:
            count = len([v for v in self.violations if v.severity == severity])
            if count > 0:
                report["violations_by_severity"][severity] = count

        # Count by category
        categories = set(v.category for v in self.violations)
        for category in categories:
            count = len([v for v in self.violations if v.category == category])
            report["violations_by_category"][category] = count

        # Detailed violations
        for violation in self.violations:
            report["detailed_violations"].append({
                "name": violation.name,
                "severity": violation.severity,
                "category": violation.category,
                "description": violation.description,
                "action": violation.action
            })

        # Generate recommendations
        if any(v.category == "pii" for v in self.violations):
            report["recommendations"].append("Implement PII redaction before storing or displaying")

        if any(v.category == "security" for v in self.violations):
            report["recommendations"].append("Review and remove all secrets and credentials")

        if any(v.category == "harmful" for v in self.violations):
            report["recommendations"].append("Review potentially harmful commands and add safeguards")

        return report


class ContentModerationValidator(SafetyValidator):
    """Extended safety validator with content moderation"""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize content moderation validator"""
        super().__init__(config=config)

        # Add content moderation rules
        self.content_rules = [
            SafetyRule(
                name="violence",
                pattern=r'(?i)\b(violence|violent|assault|attack|harm|hurt|injure|damage)\b',
                severity="medium",
                category="content",
                description="Violent content detected",
                action="warn"
            ),
            SafetyRule(
                name="adult_content",
                pattern=r'(?i)\b(adult|explicit|nsfw|sexual|nude)\b',
                severity="medium",
                category="content",
                description="Adult content detected",
                action="warn"
            ),
            SafetyRule(
                name="illegal_activity",
                pattern=r'(?i)\b(illegal|crime|criminal|fraud|scam|hack|crack|pirate)\b',
                severity="high",
                category="content",
                description="Potentially illegal activity mentioned",
                action="warn"
            ),
            SafetyRule(
                name="medical_advice",
                pattern=r'(?i)\b(diagnose|diagnosis|prescribe|prescription|treatment|cure|medical advice)\b',
                severity="medium",
                category="content",
                description="Medical advice detected - add disclaimer",
                action="warn"
            ),
            SafetyRule(
                name="financial_advice",
                pattern=r'(?i)\b(invest|investment advice|financial advice|stock tip|guaranteed return)\b',
                severity="medium",
                category="content",
                description="Financial advice detected - add disclaimer",
                action="warn"
            ),
        ]

        self.rules.extend(self.content_rules)

    async def validate_content_policy(self,
                                     output: str,
                                     policy: Dict[str, Any]) -> Dict[str, Any]:
        """Validate against specific content policy"""

        results = {
            "compliant": True,
            "violations": [],
            "warnings": []
        }

        # Check allowed topics
        if "allowed_topics" in policy:
            # Implementation would check if content is within allowed topics
            pass

        # Check forbidden topics
        if "forbidden_topics" in policy:
            for topic in policy["forbidden_topics"]:
                if topic.lower() in output.lower():
                    results["compliant"] = False
                    results["violations"].append(f"Forbidden topic: {topic}")

        # Check required disclaimers
        if "required_disclaimers" in policy:
            for disclaimer_type, disclaimer_text in policy["required_disclaimers"].items():
                if disclaimer_type in ["medical", "financial", "legal"]:
                    # Check if relevant content exists
                    pattern = self.content_rules[3].pattern if disclaimer_type == "medical" else \
                             self.content_rules[4].pattern if disclaimer_type == "financial" else \
                             r'(?i)\b(legal|law|attorney|court)\b'

                    if re.search(pattern, output) and disclaimer_text not in output:
                        results["warnings"].append(f"Missing required {disclaimer_type} disclaimer")

        return results
