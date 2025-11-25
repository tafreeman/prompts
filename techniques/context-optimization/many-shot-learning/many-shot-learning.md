---
title: "Many-Shot Learning Pattern"
category: "techniques"
subcategory: "context-optimization"
technique_type: "many-shot-learning"
framework_compatibility:
  anthropic: ">=0.8.0"
  openai: ">=1.0.0"
  google-vertex: ">=1.0.0"
difficulty: "intermediate"
use_cases:
  - complex-pattern-learning
  - domain-specific-tasks
  - edge-case-handling
  - consistent-formatting
performance_metrics:
  accuracy_improvement: "15-35%"
  latency_impact: "low"
  cost_multiplier: "1.2-1.8x"
version: "1.0.0"
author: "AI Research Team"
last_updated: "2025-11-23"
governance:
  data_classification: "internal"
  risk_level: "low"
  approval_required: false
testing:
  benchmark_score: 88
  validation_status: "passed"
  last_tested: "2025-11-23"
tags:
  - many-shot
  - few-shot
  - in-context-learning
  - long-context
platform:
  - anthropic
  - openai
  - google-vertex
---

# Many-Shot Learning Pattern

## Purpose

Many-shot learning leverages the extended context windows of modern LLMs (100K-200K+ tokens) to provide numerous examples, dramatically improving performance on complex, nuanced tasks. This pattern moves beyond traditional few-shot (3-5 examples) to use dozens or hundreds of examples.

## Overview

Traditional few-shot learning provides 2-5 examples. Many-shot learning provides:

- **Moderate**: 10-30 examples
- **High**: 30-100 examples  
- **Extreme**: 100+ examples

### When to Use Many-Shot

✅ **Good fit:**

- Complex domain-specific tasks
- Tasks requiring nuanced understanding
- Consistent formatting requirements
- Edge case handling is critical
- Pattern recognition from examples

❌ **Not recommended:**

- Simple classification tasks
- When examples aren't representative
- Limited context window (<32K tokens)
- Cost is primary concern

## Prompt Template

```
You are an expert {domain} assistant trained on extensive examples.

## Task
{task_description}

## Guidelines
{guidelines_and_constraints}

## Examples
Below are {N} examples demonstrating the expected input-output pattern. Study these carefully to understand:
- Expected output format
- Level of detail required
- Handling of edge cases
- Domain-specific conventions

---

### Example 1
**Input:**
{example_1_input}

**Output:**
{example_1_output}

**Rationale:** {why_this_example_matters}

---

### Example 2
**Input:**
{example_2_input}

**Output:**
{example_2_output}

**Rationale:** {why_this_example_matters}

---

[Continue with examples 3-N...]

---

## Your Task

Now, apply the same approach to this new input:

**Input:**
{actual_task_input}

**Output:**
```

## Usage Example: Code Review Comments

### Setup

Task: Generate constructive, specific code review comments following team conventions.

### Many-Shot Examples (showing 3 of 25)

```
### Example 1
**Input:**
```python
def calculate_total(items):
    return sum([item.price for item in items])
```

**Output:**

```
✅ **Good**: Clean use of list comprehension and sum()
⚠️ **Suggestion**: Consider adding type hints for better IDE support
```python
def calculate_total(items: List[Item]) -> float:
    return sum(item.price for item in items)
```

📝 **Note**: Generator expression (without brackets) is slightly more memory-efficient than list comprehension for large lists.

```

**Rationale:** Shows our team's convention of using emoji status indicators, providing code snippets for suggestions, and including educational notes.

---

### Example 2
**Input:**
```python
def validate_email(email):
    if '@' in email and '.' in email:
        return True
    return False
```

**Output:**

```
⚠️ **Issue**: Overly simplistic email validation that will accept invalid emails like "a@b.c" or "@example.com"
🔧 **Recommendation**: Use a proper regex or validation library
```python
import re

EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_email(email: str) -> bool:
    """Validate email format using regex pattern."""
    return bool(re.match(EMAIL_PATTERN, email))
```

Or consider using `email-validator` library for production use:

```python
from email_validator import validate_email, EmailNotValidError

def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
```

```

**Rationale:** Demonstrates critical security/correctness issues get detailed explanations with multiple solution options.

---

### Example 3
**Input:**
```python
users = []
for user_id in user_ids:
    user = db.query(User).filter(User.id == user_id).first()
    users.append(user)
```

**Output:**

```
🚨 **Performance Issue**: N+1 query problem - executes one database query per user
🔧 **Fix**: Use single query with IN clause
```python
users = db.query(User).filter(User.id.in_(user_ids)).all()
```

📊 **Impact**: For 100 users, reduces database round-trips from 100 to 1
⏱️ **Performance**: ~50-100x faster depending on network latency

```

**Rationale:** Shows how to flag performance issues with quantified impact measurement.

---

[... Examples 4-25 would continue here, covering:]
- Missing error handling
- Naming conventions
- Documentation gaps
- Testing considerations
- Security vulnerabilities
- Accessibility issues
- etc.

```

### Actual Task

```
## Your Task

Now, review this code following the same conventions:

**Input:**
```python
def get_user_posts(user_id):
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    return [p.title for p in posts]
```

**Output:**
[AI generates review in the learned format]

```

## Implementation Examples

### Python Implementation

```python
class ManyShotPromptBuilder:
    """Build many-shot prompts with example management"""
    
    def __init__(self, max_context_tokens: int = 100000):
        self.max_context_tokens = max_context_tokens
        self.examples = []
    
    def add_example(self, input_data: str, output_data: str, 
                    rationale: str = "", priority: int = 1):
        """Add example with priority (1=highest)"""
        self.examples.append({
            'input': input_data,
            'output': output_data,
            'rationale': rationale,
            'priority': priority,
            'tokens': self._estimate_tokens(input_data + output_data + rationale)
        })
    
    def build_prompt(self, task_input: str, 
                     task_description: str,
                     guidelines: str = "") -> str:
        """Build optimized many-shot prompt"""
        # Sort examples by priority
        sorted_examples = sorted(self.examples, key=lambda x: x['priority'])
        
        # Calculate available tokens
        task_tokens = self._estimate_tokens(task_input + task_description + guidelines)
        available_tokens = self.max_context_tokens - task_tokens - 1000  # Buffer
        
        # Select examples that fit
        selected_examples = []
        current_tokens = 0
        
        for ex in sorted_examples:
            if current_tokens + ex['tokens'] <= available_tokens:
                selected_examples.append(ex)
                current_tokens += ex['tokens']
            else:
                break
        
        # Build prompt
        return self._format_prompt(
            task_description,
            guidelines,
            selected_examples,
            task_input
        )
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation"""
        return int(len(text.split()) * 1.3)
    
    def _format_prompt(self, description, guidelines, examples, task_input):
        """Format the complete prompt"""
        prompt = f"""You are an expert assistant.

## Task
{description}

## Guidelines
{guidelines}

## Examples
Below are {len(examples)} examples:

"""
        for i, ex in enumerate(examples, 1):
            prompt += f"""---
### Example {i}
**Input:**
{ex['input']}

**Output:**
{ex['output']}

"""
            if ex['rationale']:
                prompt += f"**Rationale:** {ex['rationale']}\n"
            prompt += "\n"
        
        prompt += f"""---

## Your Task

**Input:**
{task_input}

**Output:**
"""
        return prompt

# Usage
builder = ManyShotPromptBuilder(max_context_tokens=100000)

# Load examples from database/file
for example in load_examples():
    builder.add_example(
        input_data=example['input'],
        output_data=example['output'],
        rationale=example['rationale'],
        priority=example['priority']
    )

# Build prompt
prompt = builder.build_prompt(
    task_input="def process_data(data): ...",
    task_description="Generate code review comments",
    guidelines="Follow team conventions"
)

# Send to LLM
response = llm.generate(prompt)
```

### Dynamic Example Selection

```python
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class SmartExampleSelector:
    """Select most relevant examples using embeddings"""
    
    def __init__(self, examples: List[Dict]):
        self.examples = examples
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self.model.encode([ex['input'] for ex in examples])
    
    def select_examples(self, task_input: str, n_examples: int = 30) -> List[Dict]:
        """Select N most relevant examples"""
        # Embed the task input
        task_embedding = self.model.encode([task_input])
        
        # Calculate similarity
        similarities = cosine_similarity(task_embedding, self.embeddings)[0]
        
        # Get top N
        top_indices = similarities.argsort()[-n_examples:][::-1]
        
        return [self.examples[i] for i in top_indices]

# Usage
selector = SmartExampleSelector(all_examples)
relevant_examples = selector.select_examples(new_task_input, n_examples=25)
```

## Optimization Strategies

### 1. Example Diversity

Ensure examples cover:

- Common cases (60%)
- Edge cases (25%)
- Error cases (15%)

```python
def categorize_examples(examples):
    return {
        'common': [ex for ex in examples if ex['category'] == 'common'],
        'edge': [ex for ex in examples if ex['category'] == 'edge'],
        'error': [ex for ex in examples if ex['category'] == 'error']
    }

def build_balanced_set(categorized, total=30):
    """Build balanced example set"""
    return (
        random.sample(categorized['common'], 18) +
        random.sample(categorized['edge'], 8) +
        random.sample(categorized['error'], 4)
    )
```

### 2. Progressive Complexity

Order examples from simple to complex:

```python
def order_by_complexity(examples):
    """Order examples by increasing complexity"""
    return sorted(examples, key=lambda ex: ex['complexity_score'])
```

### 3. Token Budget Management

```python
def fit_examples_to_budget(examples, max_tokens):
    """Include as many examples as possible within token budget"""
    selected = []
    total_tokens = 0
    
    for ex in examples:
        ex_tokens = estimate_tokens(ex)
        if total_tokens + ex_tokens <= max_tokens:
            selected.append(ex)
            total_tokens += ex_tokens
        else:
            break
    
    return selected, total_tokens
```

## Performance Characteristics

- **Accuracy**: 15-35% improvement over few-shot on complex tasks
- **Context Usage**: Can consume 50K-150K tokens depending on examples
- **Cost**: 1.2-1.8x more expensive due to larger prompts
- **Latency**: Minimal increase (<10%) despite larger context

## Best Practices

1. **Quality Over Quantity**: 25 diverse, high-quality examples > 100 redundant ones
2. **Include Rationales**: Explanations help model understand *why* each example is correct
3. **Cover Edge Cases**: Explicitly include examples of tricky situations
4. **Consistent Formatting**: Maintain uniform structure across all examples
5. **Progressive Complexity**: Start simple, build to complex
6. **Regular Updates**: Refresh example set based on real-world usage

## Comparison: Few-Shot vs Many-Shot

| Aspect | Few-Shot (3-5) | Many-Shot (25-50) |
|--------|---------------|-------------------|
| Accuracy | Baseline | +15-35% |
| Context Used | 2K-5K tokens | 30K-80K tokens |
| Cost | Baseline | +20-80% |
| Setup Time | Minutes | Hours (curating examples) |
| Best For | Simple tasks | Complex, nuanced tasks |

## Related Patterns

- Few-Shot Learning (fewer examples, smaller context)
- Retrieval-Augmented Generation (dynamic example retrieval)
- Context Compression (condensing many examples)
- Curriculum Learning (ordered example presentation)

## References

- "Many-Shot In-Context Learning" (Anthropic Research, 2024)
- Claude 3 Long Context Capabilities
- OpenAI GPT-4 Turbo Context Optimization Guide
