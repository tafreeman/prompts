"""
Format Validator for Prompt Templates

Validates markdown and YAML format compliance, including:
- YAML frontmatter structure
- Markdown syntax correctness
- Required field presence
- File structure conventions
"""

import re
import yaml
from typing import Any, Dict, List, Optional, Set
import logging

from .base_validator import BaseValidator

logger = logging.getLogger(__name__)


class FormatValidator(BaseValidator):
    """
    Validates markdown and YAML format of prompt templates.
    
    Checks for:
    - Valid YAML frontmatter
    - Required frontmatter fields
    - Proper markdown structure
    - Consistent heading hierarchy
    - Code block formatting
    """
    
    # Required frontmatter fields for a valid prompt
    REQUIRED_FIELDS = {'title'}
    
    # Recommended frontmatter fields
    RECOMMENDED_FIELDS = {
        'shortTitle', 'intro', 'type', 'difficulty', 
        'audience', 'platforms', 'author', 'version'
    }
    
    # Valid values for enumerated fields
    VALID_TYPES = {
        'how_to', 'quickstart', 'tutorial', 'reference', 
        'conceptual', 'troubleshooting', 'sample'
    }
    
    VALID_DIFFICULTIES = {'beginner', 'intermediate', 'advanced', 'expert'}
    
    VALID_PLATFORMS = {
        'github-copilot', 'chatgpt', 'claude', 'm365-copilot', 
        'gemini', 'llama', 'universal'
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize format validator with configuration."""
        super().__init__(config)
        self.strict_mode = config.get('strict_mode', False) if config else False
        self.required_fields = set(config.get('required_fields', self.REQUIRED_FIELDS)) if config else self.REQUIRED_FIELDS
    
    async def validate(self, output: Any, expected: Optional[Any] = None) -> bool:
        """
        Validate format of prompt content.
        
        Args:
            output: The prompt content (markdown with YAML frontmatter)
            expected: Optional expected format specification
            
        Returns:
            bool: True if format is valid, False otherwise
        """
        self.clear_messages()
        
        if not output:
            self.add_error("No content provided for format validation")
            return False
        
        content = str(output)
        is_valid = True
        
        # Validate YAML frontmatter
        frontmatter_valid, frontmatter = self._validate_frontmatter(content)
        if not frontmatter_valid:
            is_valid = False
        
        # Validate frontmatter fields
        if frontmatter:
            fields_valid = self._validate_fields(frontmatter)
            if not fields_valid:
                is_valid = False
        
        # Validate markdown structure
        body = self._extract_body(content)
        markdown_valid = self._validate_markdown(body)
        if not markdown_valid and self.strict_mode:
            is_valid = False
        
        # Validate heading hierarchy
        headings_valid = self._validate_headings(body)
        if not headings_valid and self.strict_mode:
            is_valid = False
        
        # Validate code blocks
        code_valid = self._validate_code_blocks(body)
        if not code_valid:
            # Code block issues are warnings, not errors
            pass
        
        return is_valid
    
    def _validate_frontmatter(self, content: str) -> tuple[bool, Optional[Dict]]:
        """Validate YAML frontmatter presence and syntax."""
        if not content.strip().startswith('---'):
            self.add_error("Missing YAML frontmatter (should start with '---')")
            return False, None
        
        # Find the closing ---
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            self.add_error("Invalid frontmatter format (missing closing '---')")
            return False, None
        
        frontmatter_text = match.group(1)
        
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if frontmatter is None:
                self.add_error("Empty frontmatter")
                return False, None
            if not isinstance(frontmatter, dict):
                self.add_error("Frontmatter must be a YAML dictionary")
                return False, None
            return True, frontmatter
        except yaml.YAMLError as e:
            self.add_error(f"YAML parsing error: {e}")
            return False, None
    
    def _validate_fields(self, frontmatter: Dict) -> bool:
        """Validate frontmatter field presence and values."""
        is_valid = True
        
        # Check required fields
        for field in self.required_fields:
            if field not in frontmatter:
                self.add_error(f"Missing required field: '{field}'")
                is_valid = False
            elif not frontmatter[field]:
                self.add_error(f"Required field '{field}' is empty")
                is_valid = False
        
        # Check recommended fields
        for field in self.RECOMMENDED_FIELDS:
            if field not in frontmatter:
                self.add_warning(f"Missing recommended field: '{field}'")
        
        # Validate field values
        if 'type' in frontmatter:
            type_value = str(frontmatter['type']).lower()
            if type_value not in self.VALID_TYPES:
                self.add_warning(f"Unknown type '{type_value}'. Valid types: {', '.join(self.VALID_TYPES)}")
        
        if 'difficulty' in frontmatter:
            diff_value = str(frontmatter['difficulty']).lower()
            if diff_value not in self.VALID_DIFFICULTIES:
                self.add_warning(f"Unknown difficulty '{diff_value}'. Valid values: {', '.join(self.VALID_DIFFICULTIES)}")
        
        if 'platforms' in frontmatter:
            platforms = frontmatter['platforms']
            if isinstance(platforms, list):
                for platform in platforms:
                    if str(platform).lower() not in self.VALID_PLATFORMS:
                        self.add_warning(f"Unknown platform '{platform}'. Valid platforms: {', '.join(self.VALID_PLATFORMS)}")
        
        # Check effectivenessScore if present
        if 'effectivenessScore' in frontmatter:
            score = frontmatter['effectivenessScore']
            if score != 'pending':
                try:
                    score_float = float(score)
                    if score_float < 1.0 or score_float > 5.0:
                        self.add_warning(f"effectivenessScore {score_float} is out of range (1.0-5.0)")
                except (ValueError, TypeError):
                    self.add_error(f"Invalid effectivenessScore format: '{score}'")
                    is_valid = False
        
        return is_valid
    
    def _extract_body(self, content: str) -> str:
        """Extract the markdown body after frontmatter."""
        match = re.match(r'^---\s*\n.*?\n---\s*\n', content, re.DOTALL)
        if match:
            return content[match.end():]
        return content
    
    def _validate_markdown(self, body: str) -> bool:
        """Validate basic markdown structure."""
        is_valid = True
        
        # Check for common markdown issues
        lines = body.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for broken links
            broken_links = re.findall(r'\[([^\]]*)\]\s+\(', line)
            if broken_links:
                self.add_warning(f"Line {i}: Potentially broken markdown link (space between ] and ()")
            
            # Check for unclosed code blocks
            # This is a simple check - a more thorough one would track state
            
        # Check for balanced code fences
        fence_count = len(re.findall(r'^```', body, re.MULTILINE))
        if fence_count % 2 != 0:
            self.add_error("Unbalanced code fences (odd number of ```)")
            is_valid = False
        
        return is_valid
    
    def _validate_headings(self, body: str) -> bool:
        """Validate heading hierarchy."""
        is_valid = True
        headings = re.findall(r'^(#+)\s+(.+)$', body, re.MULTILINE)
        
        if not headings:
            self.add_warning("No headings found in document body")
            return True
        
        prev_level = 0
        for hashes, text in headings:
            level = len(hashes)
            
            # Check for skipped levels (e.g., going from # to ###)
            if level > prev_level + 1 and prev_level > 0:
                self.add_warning(f"Heading hierarchy skip: '{text}' (h{level}) after h{prev_level}")
            
            # Check for very deep headings
            if level > 4:
                self.add_warning(f"Deep heading level (h{level}): '{text}'. Consider restructuring.")
            
            prev_level = level
        
        return is_valid
    
    def _validate_code_blocks(self, body: str) -> bool:
        """Validate code block formatting."""
        is_valid = True
        
        # Find all code blocks
        code_blocks = re.findall(r'```(\w*)\n(.*?)```', body, re.DOTALL)
        
        for language, code in code_blocks:
            if not language:
                self.add_warning("Code block without language specification")
            
            # Check for common issues in code blocks
            if code.strip() and not code.strip().endswith('\n') == False:
                # Code exists, check for issues
                if '```' in code:
                    self.add_warning("Nested code fence markers detected in code block")
        
        # Check for inline code
        inline_code = re.findall(r'`[^`\n]+`', body)
        for code in inline_code:
            if len(code) > 100:
                self.add_warning(f"Very long inline code ({len(code)} chars). Consider using a code block.")
        
        return is_valid
    
    def get_format_analysis(self, content: str) -> Dict[str, Any]:
        """
        Get a comprehensive format analysis of the content.
        
        Returns a dictionary with format properties and metrics.
        """
        _, frontmatter = self._validate_frontmatter(content)
        body = self._extract_body(content)
        
        # Count various elements
        headings = re.findall(r'^(#+)\s+(.+)$', body, re.MULTILINE)
        code_blocks = re.findall(r'```(\w*)\n', body)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', body)
        images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', body)
        lists = len(re.findall(r'^\s*[-*+]\s+', body, re.MULTILINE))
        numbered_lists = len(re.findall(r'^\s*\d+[\.\)]\s+', body, re.MULTILINE))
        
        return {
            'has_frontmatter': frontmatter is not None,
            'frontmatter_fields': list(frontmatter.keys()) if frontmatter else [],
            'heading_count': len(headings),
            'heading_levels': [len(h[0]) for h in headings],
            'code_block_count': len(code_blocks),
            'code_languages': [lang for lang in code_blocks if lang],
            'link_count': len(links),
            'image_count': len(images),
            'list_items': lists,
            'numbered_list_items': numbered_lists,
            'word_count': len(body.split()),
            'line_count': len(body.split('\n')),
        }
