#!/usr/bin/env python3
"""
Comprehensive Prompt Validation Framework
Author: AI Research Team
Version: 2.0.0
Last Updated: 2025-11-23

This module provides a comprehensive validation system for prompt templates,
including structure, metadata, performance, security, and accessibility validation.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ValidationLevel(Enum):
    """Validation severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    """Represents a single validation issue"""
    level: ValidationLevel
    category: str
    message: str
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class ValidationReport:
    """Comprehensive validation report"""
    file_path: str
    issues: List[ValidationIssue] = field(default_factory=list)
    structure_score: float = 0.0
    metadata_score: float = 0.0
    performance_score: float = 0.0
    security_score: float = 0.0
    accessibility_score: float = 0.0
    overall_score: float = 0.0
    
    def add_issue(self, issue: ValidationIssue):
        """Add a validation issue to the report"""
        self.issues.append(issue)
    
    def calculate_overall_score(self):
        """Calculate weighted overall score"""
        weights = {
            'structure': 0.25,
            'metadata': 0.25,
            'performance': 0.20,
            'security': 0.20,
            'accessibility': 0.10
        }
        
        self.overall_score = (
            self.structure_score * weights['structure'] +
            self.metadata_score * weights['metadata'] +
            self.performance_score * weights['performance'] +
            self.security_score * weights['security'] +
            self.accessibility_score * weights['accessibility']
        )
        
        return self.overall_score
    
    def get_severity_counts(self) -> Dict[str, int]:
        """Get count of issues by severity level"""
        counts = {level.value: 0 for level in ValidationLevel}
        for issue in self.issues:
            counts[issue.level.value] += 1
        return counts
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary"""
        return {
            'file_path': self.file_path,
            'scores': {
                'structure': self.structure_score,
                'metadata': self.metadata_score,
                'performance': self.performance_score,
                'security': self.security_score,
                'accessibility': self.accessibility_score,
                'overall': self.overall_score
            },
            'issues': [
                {
                    'level': issue.level.value,
                    'category': issue.category,
                    'message': issue.message,
                    'line_number': issue.line_number,
                    'suggestion': issue.suggestion
                }
                for issue in self.issues
            ],
            'severity_counts': self.get_severity_counts()
        }


class StructureValidator:
    """Validates prompt structure and format"""
    
    def validate(self, file_path: str, content: str, metadata: Dict) -> tuple[float, List[ValidationIssue]]:
        """Validate prompt structure"""
        issues = []
        score = 100.0
        
        # Check for YAML frontmatter
        if not content.strip().startswith('---'):
            issues.append(ValidationIssue(
                ValidationLevel.ERROR,
                "structure",
                "Missing YAML frontmatter",
                line_number=1,
                suggestion="Add YAML frontmatter with metadata at the top of the file"
            ))
            score -= 30
        
        # Check for proper markdown structure
        lines = content.split('\n')
        has_h1 = any(line.strip().startswith('# ') for line in lines)
        if not has_h1:
            issues.append(ValidationIssue(
                ValidationLevel.WARNING,
                "structure",
                "No H1 heading found",
                suggestion="Add a clear H1 heading to describe the prompt"
            ))
            score -= 10
        
        # Check for sections
        required_sections = ['## Purpose', '## Prompt', '## Example', '## Usage']
        content_lower = content.lower()
        for section in required_sections:
            if section.lower() not in content_lower:
                issues.append(ValidationIssue(
                    ValidationLevel.WARNING,
                    "structure",
                    f"Missing recommended section: {section}",
                    suggestion=f"Add a {section} section for better documentation"
                ))
                score -= 5
        
        # Check file length
        if len(lines) < 20:
            issues.append(ValidationIssue(
                ValidationLevel.INFO,
                "structure",
                "File seems very short, consider adding more documentation"
            ))
            score -= 5
        
        return max(0, score), issues


class MetadataValidator:
    """Validates YAML metadata compliance"""
    
    def __init__(self, schema_path: Optional[str] = None):
        """Initialize with schema path"""
        if schema_path is None:
            schema_path = Path(__file__).parent / "metadata_schema.yaml"
        
        self.schema = self._load_schema(schema_path)
    
    def _load_schema(self, schema_path: str) -> Dict:
        """Load metadata schema"""
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load schema from {schema_path}: {e}")
            return {}
    
    def validate(self, file_path: str, content: str, metadata: Dict) -> tuple[float, List[ValidationIssue]]:
        """Validate metadata fields"""
        issues = []
        score = 100.0
        
        if not metadata:
            issues.append(ValidationIssue(
                ValidationLevel.ERROR,
                "metadata",
                "No metadata found in file",
                suggestion="Add YAML frontmatter with required metadata fields"
            ))
            return 0.0, issues
        
        # Check required fields
        required_fields = self.schema.get('required_fields', [
            'title', 'category', 'difficulty', 'version', 'author', 'last_updated'
        ])
        
        for field in required_fields:
            if field not in metadata:
                issues.append(ValidationIssue(
                    ValidationLevel.ERROR,
                    "metadata",
                    f"Missing required field: {field}",
                    suggestion=f"Add '{field}' to the metadata frontmatter"
                ))
                score -= 15
        
        # Validate field values
        if 'difficulty' in metadata:
            valid_difficulties = ['beginner', 'intermediate', 'advanced', 'expert']
            if metadata['difficulty'] not in valid_difficulties:
                issues.append(ValidationIssue(
                    ValidationLevel.ERROR,
                    "metadata",
                    f"Invalid difficulty value: {metadata['difficulty']}",
                    suggestion=f"Use one of: {', '.join(valid_difficulties)}"
                ))
                score -= 10
        
        if 'version' in metadata:
            if not re.match(r'^\d+\.\d+\.\d+$', str(metadata['version'])):
                issues.append(ValidationIssue(
                    ValidationLevel.WARNING,
                    "metadata",
                    "Version should follow semantic versioning (x.y.z)",
                    suggestion="Use format like '1.0.0' or '2.1.3'"
                ))
                score -= 5
        
        # Check date format
        if 'last_updated' in metadata:
            try:
                datetime.strptime(str(metadata['last_updated']), '%Y-%m-%d')
            except ValueError:
                issues.append(ValidationIssue(
                    ValidationLevel.WARNING,
                    "metadata",
                    "Invalid date format for last_updated",
                    suggestion="Use ISO 8601 format: YYYY-MM-DD"
                ))
                score -= 5
        
        # Check for recommended optional fields
        recommended_fields = ['tags', 'use_cases', 'framework_compatibility']
        for field in recommended_fields:
            if field not in metadata:
                issues.append(ValidationIssue(
                    ValidationLevel.INFO,
                    "metadata",
                    f"Missing recommended field: {field}",
                    suggestion=f"Consider adding '{field}' for better discoverability"
                ))
                score -= 3
        
        return max(0, score), issues


class PerformanceValidator:
    """Validates performance-related aspects"""
    
    def validate(self, file_path: str, content: str, metadata: Dict) -> tuple[float, List[ValidationIssue]]:
        """Validate performance characteristics"""
        issues = []
        score = 100.0
        
        # Check for performance metrics in metadata
        if 'performance_metrics' not in metadata:
            issues.append(ValidationIssue(
                ValidationLevel.INFO,
                "performance",
                "No performance metrics documented",
                suggestion="Add 'performance_metrics' section with expected performance"
            ))
            score -= 20
        else:
            metrics = metadata['performance_metrics']
            recommended_metrics = ['accuracy_improvement', 'latency_impact', 'cost_multiplier']
            
            for metric in recommended_metrics:
                if metric not in metrics:
                    issues.append(ValidationIssue(
                        ValidationLevel.INFO,
                        "performance",
                        f"Missing performance metric: {metric}",
                        suggestion=f"Document expected {metric}"
                    ))
                    score -= 10
        
        # Check prompt token efficiency (basic heuristic)
        prompt_section = self._extract_prompt_section(content)
        if prompt_section:
            token_estimate = len(prompt_section.split())
            if token_estimate > 1000:
                issues.append(ValidationIssue(
                    ValidationLevel.WARNING,
                    "performance",
                    f"Large prompt detected (~{token_estimate} tokens)",
                    suggestion="Consider optimizing prompt length for cost efficiency"
                ))
                score -= 15
        
        # Check for testing documentation
        if 'testing' not in metadata:
            issues.append(ValidationIssue(
                ValidationLevel.INFO,
                "performance",
                "No testing results documented",
                suggestion="Add 'testing' section with validation results"
            ))
            score -= 15
        
        return max(0, score), issues
    
    def _extract_prompt_section(self, content: str) -> str:
        """Extract the main prompt content"""
        # Simple heuristic: find content after metadata
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return parts[2]
        return content


class SecurityValidator:
    """Validates security and safety aspects"""
    
    SECURITY_PATTERNS = {
        'injection': r'(exec\s*\(|eval\s*\(|__import__|system\s*\()',
        'pii': r'(ssn|social\s+security|credit\s+card|password)',
        'credentials': r'(api[_-]?key|secret[_-]?key)',  # Removed token/bearer to reduce false positives in API docs
    }
    
    def validate(self, file_path: str, content: str, metadata: Dict) -> tuple[float, List[ValidationIssue]]:
        """Validate security aspects"""
        issues = []
        score = 100.0
        
        # Check for potential security issues in prompt content
        # Skip regex checks for security-focused prompts or code reviews
        exempt_subcategories = ['security', 'code-review']
        if metadata.get('subcategory') not in exempt_subcategories:
            content_lower = content.lower()
            
            for pattern_name, pattern in self.SECURITY_PATTERNS.items():
                matches = re.finditer(pattern, content_lower, re.IGNORECASE)
                for match in matches:
                    issues.append(ValidationIssue(
                        ValidationLevel.WARNING,
                        "security",
                        f"Potential security concern: {pattern_name} pattern detected",
                        suggestion=f"Review usage of '{match.group()}' for security implications"
                    ))
                    score -= 10
        
        # Check governance metadata
        if 'governance' in metadata:
            gov = metadata['governance']
            if 'data_classification' not in gov:
                issues.append(ValidationIssue(
                    ValidationLevel.WARNING,
                    "security",
                    "Missing data classification",
                    suggestion="Add 'data_classification' to governance section"
                ))
                score -= 15
            
            if 'risk_level' not in gov:
                issues.append(ValidationIssue(
                    ValidationLevel.WARNING,
                    "security",
                    "Missing risk level assessment",
                    suggestion="Add 'risk_level' to governance section"
                ))
                score -= 15
        else:
            issues.append(ValidationIssue(
                ValidationLevel.INFO,
                "security",
                "No governance section found",
                suggestion="Add 'governance' metadata for enterprise compliance"
            ))
            score -= 20
        
        return max(0, score), issues


class AccessibilityValidator:
    """Validates accessibility and usability"""
    
    def validate(self, file_path: str, content: str, metadata: Dict) -> tuple[float, List[ValidationIssue]]:
        """Validate accessibility aspects"""
        issues = []
        score = 100.0
        
        # Check for usage documentation
        if '## usage' not in content.lower():
            issues.append(ValidationIssue(
                ValidationLevel.WARNING,
                "accessibility",
                "Missing usage documentation",
                suggestion="Add a '## Usage' section with clear instructions"
            ))
            score -= 20
        
        # Check for examples
        if '## example' not in content.lower():
            issues.append(ValidationIssue(
                ValidationLevel.WARNING,
                "accessibility",
                "Missing examples",
                suggestion="Add an '## Example' section with concrete use cases"
            ))
            score -= 20
        
        # Check for code blocks
        code_blocks = content.count('```')
        if code_blocks == 0:
            issues.append(ValidationIssue(
                ValidationLevel.INFO,
                "accessibility",
                "No code examples found",
                suggestion="Include code blocks to demonstrate usage"
            ))
            score -= 15
        
        # Check for table of contents (for longer documents)
        lines = content.split('\n')
        if len(lines) > 100 and '## table of contents' not in content.lower():
            issues.append(ValidationIssue(
                ValidationLevel.INFO,
                "accessibility",
                "Long document without table of contents",
                suggestion="Add a table of contents for better navigation"
            ))
            score -= 10
        
        return max(0, score), issues


class PromptValidationFramework:
    """Comprehensive prompt validation and testing system"""
    
    def __init__(self, schema_path: Optional[str] = None):
        """Initialize validation framework"""
        self.validators = {
            'structure': StructureValidator(),
            'metadata': MetadataValidator(schema_path),
            'performance': PerformanceValidator(),
            'security': SecurityValidator(),
            'accessibility': AccessibilityValidator()
        }
    
    def validate_prompt(self, prompt_file: str) -> ValidationReport:
        """Run comprehensive validation suite on a prompt file"""
        report = ValidationReport(file_path=prompt_file)
        
        # Read file content
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            report.add_issue(ValidationIssue(
                ValidationLevel.ERROR,
                "file",
                f"Could not read file: {e}"
            ))
            return report
        
        # Extract metadata
        metadata = self._extract_metadata(content)
        
        # Run all validators
        for validator_name, validator in self.validators.items():
            try:
                score, issues = validator.validate(prompt_file, content, metadata)
                
                # Set score on report
                setattr(report, f"{validator_name}_score", score)
                
                # Add issues to report
                for issue in issues:
                    report.add_issue(issue)
                    
            except Exception as e:
                report.add_issue(ValidationIssue(
                    ValidationLevel.ERROR,
                    validator_name,
                    f"Validator error: {e}"
                ))
        
        # Calculate overall score
        report.calculate_overall_score()
        
        return report
    
    def _extract_metadata(self, content: str) -> Dict:
        """Extract YAML frontmatter metadata"""
        try:
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1]) or {}
        except Exception as e:
            print(f"Warning: Could not parse metadata: {e}")
        
        return {}
    
    def generate_improvement_suggestions(self, report: ValidationReport) -> List[str]:
        """Generate actionable improvement suggestions"""
        suggestions = []
        
        # Score-based suggestions
        if report.structure_score < 80:
            suggestions.append("Improve prompt structure and organization with clear sections")
        
        if report.metadata_score < 70:
            suggestions.append("Complete all required metadata fields and follow schema")
        
        if report.performance_score < 70:
            suggestions.append("Document performance metrics and testing results")
        
        if report.security_score < 80:
            suggestions.append("Add governance metadata and review security implications")
        
        if report.accessibility_score < 75:
            suggestions.append("Add usage examples and clear documentation for users")
        
        # Issue-based suggestions
        error_count = sum(1 for issue in report.issues if issue.level == ValidationLevel.ERROR)
        if error_count > 0:
            suggestions.insert(0, f"Fix {error_count} critical errors before deployment")
        
        return suggestions


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate prompt template files")
    parser.add_argument("file", help="Prompt file to validate")
    parser.add_argument("--schema", help="Path to metadata schema YAML")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--min-score", type=float, default=75.0, help="Minimum passing score")
    
    args = parser.parse_args()
    
    # Validate file
    framework = PromptValidationFramework(args.schema)
    report = framework.validate_prompt(args.file)
    
    # Output results
    if args.json:
        import json
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(f"\n{'='*70}")
        print(f"Validation Report: {report.file_path}")
        print(f"{'='*70}\n")
        
        print("Scores:")
        print(f"  Structure:     {report.structure_score:5.1f}/100")
        print(f"  Metadata:      {report.metadata_score:5.1f}/100")
        print(f"  Performance:   {report.performance_score:5.1f}/100")
        print(f"  Security:      {report.security_score:5.1f}/100")
        print(f"  Accessibility: {report.accessibility_score:5.1f}/100")
        print(f"  {'-'*40}")
        print(f"  Overall:       {report.overall_score:5.1f}/100\n")
        
        if report.issues:
            print("Issues Found:")
            for issue in report.issues:
                # Use ASCII characters instead of Unicode emojis to avoid encoding errors
                icon = "[!]" if issue.level == ValidationLevel.ERROR else "[*]" if issue.level == ValidationLevel.WARNING else "[i]"
                print(f"  {icon} [{issue.category}] {issue.message}")
                if issue.suggestion:
                    print(f"     >> {issue.suggestion}")
            print()
        
        suggestions = framework.generate_improvement_suggestions(report)
        if suggestions:
            print("Improvement Suggestions:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
            print()
        
        # Exit with appropriate code
        if report.overall_score < args.min_score:
            print(f"[FAIL] Validation failed (score {report.overall_score:.1f} < {args.min_score})")
            exit(1)
        else:
            print(f"[PASS] Validation passed (score {report.overall_score:.1f})")
            exit(0)


if __name__ == "__main__":
    main()
