# Advanced Prompting Techniques

This directory contains advanced prompting techniques optimized for frontier AI models (GPT-5.1, Claude Sonnet 4.5/Code 5, and similar reasoning-capable models).

## What's Inside

### Core Techniques

1. **Chain-of-Thought (CoT)** - Step-by-step reasoning prompts
   - `chain-of-thought-concise.md` - Concise reasoning mode
   - `chain-of-thought-detailed.md` - Detailed reasoning mode
   - `chain-of-thought-guide.md` - When and how to use CoT

2. **ReAct** - Reasoning + Acting patterns for tool-augmented tasks
   - `react-tool-augmented.md` - Think/Act/Observe/Reflect framework
   - `react-doc-search-synthesis.md` - Document retrieval + answer synthesis
   - `react-api-integration.md` - API calling with reasoning

3. **RAG (Retrieval-Augmented Generation)** - Context-aware generation
   - `rag-code-ingestion.md` - Code repository ingestion patterns
   - `rag-document-retrieval.md` - Document chunking and retrieval
   - `rag-citation-framework.md` - Citation and reference management

4. **Reflection & Self-Critique** - Iterative improvement patterns
   - `reflection-initial-answer.md` - Initial response generation
   - `reflection-evaluator.md` - Quality evaluation and critique
   - `reflection-iterative-improvement.md` - Multi-round refinement

5. **Tree-of-Thoughts (ToT)** - Multi-branch reasoning
   - `tree-of-thoughts-template.md` - Multi-branch exploration
   - `tree-of-thoughts-vs-linear.md` - Comparative analysis
   - `tree-of-thoughts-decision-guide.md` - When to escalate to ToT

## When to Use Advanced Techniques

### Use Chain-of-Thought When:
- Problems require step-by-step logical reasoning
- You need to show your work or explain reasoning
- Breaking down complex problems into steps improves accuracy
- **Example**: Math problems, logical puzzles, debugging complex issues

### Use ReAct When:
- You need to interact with external tools or APIs
- Tasks require iterative information gathering
- You want to see the reasoning behind each action
- **Example**: Research tasks, data analysis, multi-step workflows

### Use RAG When:
- You need to ground responses in specific documents or code
- Working with proprietary or recent information not in training data
- Citation and source attribution are critical
- **Example**: Internal documentation queries, code repository questions

### Use Reflection When:
- Quality and accuracy are paramount
- You want to improve initial responses iteratively
- Self-assessment can catch errors or gaps
- **Example**: Critical decision-making, high-stakes communications

### Use Tree-of-Thoughts When:
- Multiple solution paths exist and need evaluation
- You want to explore trade-offs systematically
- Complex decisions require comparing alternatives
- **Example**: Architecture decisions, strategic planning, complex problem-solving

## Integration with Enterprise Workflows

All prompts in this directory include:
- **Governance tags**: PII-safe, requires-human-review, audit-required
- **Platform adaptations**: Copilot, chat interfaces, API usage
- **Output schemas**: JSON, XML, YAML templates for automation
- **Risk assessments**: Security and compliance considerations

## Contributing

When adding new advanced technique prompts:
1. Follow the template in `/templates/prompt-template.md`
2. Include governance metadata in frontmatter
3. Add comparative examples showing when to use vs. simpler approaches
4. Include both theory and practical examples
5. Document limitations and edge cases

## Related Resources

- [System Prompts](../system/) - System-level configurations
- [Developer Prompts](../developers/) - Technical use cases
- [Business Prompts](../business/) - Enterprise workflows
- [Template Library](../../templates/) - Reusable templates
