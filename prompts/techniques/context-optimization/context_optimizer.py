import re
from typing import List, Dict, Optional, Union, Callable
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CompressionResult:
    """Result of a context compression operation."""
    original_length: int
    compressed_length: int
    compression_ratio: float
    content: str
    strategy: str
    metadata: Dict

class ContextOptimizer:
    """
    Advanced context management for long-form prompts.
    Implements compression, chunking, and retrieval strategies to optimize
    token usage while preserving semantic meaning.
    """

    def __init__(self, max_context_length: int = 128000, target_compression_ratio: float = 0.5):
        self.max_context_length = max_context_length
        self.target_compression_ratio = target_compression_ratio
        self.strategies = {
            'semantic': self._semantic_compression,
            'hierarchical': self._hierarchical_compression,
            'sliding_window': self._sliding_window,
            'selective': self._selective_retention
        }

    def optimize_context(self, content: str, strategy: str = 'semantic', **kwargs) -> CompressionResult:
        """
        Optimize context length using the specified strategy.
        
        Args:
            content: The input text to compress.
            strategy: The compression strategy to use ('semantic', 'hierarchical', 'sliding_window', 'selective').
            **kwargs: Additional arguments for specific strategies.
            
        Returns:
            CompressionResult object containing compressed content and metrics.
        """
        if strategy not in self.strategies:
            raise ValueError(f"Unknown strategy: {strategy}. Available: {list(self.strategies.keys())}")

        logger.info(f"Optimizing context with strategy: {strategy}, Input length: {len(content)}")
        
        # If content is already within limits and no forced compression, return as is
        if len(content) <= self.max_context_length and not kwargs.get('force', False):
            return CompressionResult(
                original_length=len(content),
                compressed_length=len(content),
                compression_ratio=1.0,
                content=content,
                strategy='none',
                metadata={'reason': 'within_limits'}
            )

        compressed_content = self.strategies[strategy](content, **kwargs)
        
        return CompressionResult(
            original_length=len(content),
            compressed_length=len(compressed_content),
            compression_ratio=len(compressed_content) / len(content) if len(content) > 0 else 1.0,
            content=compressed_content,
            strategy=strategy,
            metadata=kwargs
        )

    def _semantic_compression(self, content: str, **kwargs) -> str:
        """
        Compresses content by removing redundant words, stop words, and formatting 
        while preserving key semantic meaning.
        
        Note: In a production environment, this would use an LLM or NLP library (spacy/nltk).
        Here we implement a heuristic-based approach for demonstration.
        """
        # 1. Remove extra whitespace
        text = re.sub(r'\s+', ' ', content).strip()
        
        # 2. Remove filler phrases (heuristic list)
        fillers = [
            r"please note that", r"it is important to mention", r"basically",
            r"actually", r"literally", r"in order to", r"for the purpose of"
        ]
        for filler in fillers:
            text = re.sub(filler, "", text, flags=re.IGNORECASE)
            
        # 3. Simple summarization simulation (truncating verbose sections)
        # In real implementation: Use LLM to summarize paragraphs
        
        return text

    def _hierarchical_compression(self, content: str, **kwargs) -> str:
        """
        Compresses by retaining headers and the first/last sentences of paragraphs.
        Useful for structured documents.
        """
        lines = content.split('\n')
        compressed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Keep headers
            if line.startswith('#') or line.isupper():
                compressed_lines.append(line)
                continue
            
            # For paragraphs, keep first sentence (heuristic split by .)
            sentences = line.split('. ')
            if sentences:
                compressed_lines.append(sentences[0] + '.')
                
        return '\n'.join(compressed_lines)

    def _sliding_window(self, content: str, window_size: int = 2000, overlap: int = 200, **kwargs) -> str:
        """
        Retains the most recent context (end of string) and a summary of the beginning.
        """
        if len(content) <= window_size:
            return content
            
        # Keep the last 'window_size' characters
        recent_context = content[-window_size:]
        
        # Add a placeholder for the truncated part
        # In real app: Summarize content[:-window_size]
        summary_marker = f"[...Previous {len(content) - window_size} characters summarized...]\n"
        
        return summary_marker + recent_context

    def _selective_retention(self, content: str, keywords: List[str] = None, **kwargs) -> str:
        """
        Retains sentences or paragraphs that contain specific keywords.
        """
        if not keywords:
            return content
            
        lines = content.split('\n')
        kept_lines = []
        
        for line in lines:
            if any(k.lower() in line.lower() for k in keywords):
                kept_lines.append(line)
                
        return '\n'.join(kept_lines)

    def estimate_tokens(self, text: str) -> int:
        """
        Rough estimation of token count (approx 4 chars per token).
        For production, use tiktoken.
        """
        return len(text) // 4

# Example Usage
if __name__ == "__main__":
    optimizer = ContextOptimizer()
    
    sample_text = """
    # Introduction
    This is a very long document that needs to be compressed. It contains many details that might not be relevant.
    For example, we are talking about the weather, which is nice today, but not relevant to the code.
    
    # Main Point
    The core logic of the application relies on the ContextOptimizer class. This class is essential.
    It allows us to handle large prompts without hitting token limits.
    
    # Conclusion
    In summary, optimization is good. We should use it often.
    """
    
    result = optimizer.optimize_context(sample_text, strategy='hierarchical')
    print(f"Original Length: {result.original_length}")
    print(f"Compressed Length: {result.compressed_length}")
    print(f"Ratio: {result.compression_ratio:.2f}")
    print("\nCompressed Content:")
    print(result.content)
