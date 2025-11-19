# System Prompts

This directory contains system-level prompts for configuring AI assistants, chatbots, and agents.

## Available Prompts

### AI Configuration

- **[AI Assistant System Prompt](ai-assistant-system-prompt.md)** - Comprehensive system prompt template
  - Difficulty: Advanced
  - Tags: system-prompt, ai-assistant, configuration, behavior

### AI Evaluation & Analysis

- **[Tree-of-Thoughts Repository Evaluator](tree-of-thoughts-repository-evaluator.md)** - GPT-5.1 ToT framework for analyzing repositories
  - Difficulty: Advanced
  - Tags: tree-of-thoughts, tot, evaluation, repository-analysis, gpt-5.1, enterprise

## What Are System Prompts?

System prompts define the foundational behavior, personality, and capabilities of an AI assistant. They are typically:

- Set at the beginning of a conversation
- Persistent across interactions
- Used to establish consistent behavior
- Hidden from end users (in chatbot applications)

## Categories

### AI Assistant Configuration

Prompts for setting up general-purpose AI assistants.

### Chatbot Personality

Prompts for defining chatbot personalities and tone.

### Domain-Specific Agents

Prompts for specialized AI agents (customer service, technical support, etc.).

### Behavioral Guidelines

Prompts for setting boundaries and ethical guidelines.

### Role-Based Assistants

Prompts for specific roles (tutor, coach, advisor, consultant).

## Using System Prompts

### For Chatbot Development

1. **Define the role** clearly
2. **Set boundaries** and limitations
3. **Establish personality** and tone
4. **Define expertise areas**
5. **Create interaction protocols**
6. **Test thoroughly** with edge cases

### For Personal AI Assistants

1. **Customize the template** for your needs
2. **Add domain knowledge** relevant to you
3. **Set communication preferences**
4. **Test with real queries**
5. **Refine based on results**

## Best Practices

### Do

✅ Be specific about capabilities and limitations
✅ Define clear behavioral guidelines
✅ Include example interactions
✅ Test with edge cases
✅ Update based on user feedback
✅ Set appropriate ethical boundaries

### Don't

❌ Make claims about capabilities the AI doesn't have
❌ Be vague about role or purpose
❌ Forget to define what it should NOT do
❌ Skip testing with problematic inputs
❌ Ignore edge cases and exceptions

## System Prompt Structure

```text
1. Core Identity
   - Role and expertise
   - Personality traits
   - Primary purpose

2. Responsibilities
   - What it should do
   - Priority areas
   - Success criteria

3. Communication Style
   - Tone and language
   - Response structure
   - Length preferences

4. Behavioral Guidelines
   - Always do
   - Never do
   - How to handle situations

5. Domain Knowledge
   - Expertise areas
   - Known limitations
   - Uncertainty handling

6. Interaction Protocols
   - Unclear requests
   - Knowledge gaps
   - Disagreements
   - Ethical concerns
```

## Testing Your System Prompts

Test with these scenarios:

- ✅ Normal use cases
- ✅ Edge cases
- ✅ Unclear requests
- ✅ Out-of-scope requests
- ✅ Problematic or unethical requests
- ✅ Requests for information you don't have
- ✅ Corrections and feedback

## Examples by Use Case

### Customer Service Agent

- Helpful, patient, solution-oriented
- Escalation protocols
- Empathy and understanding
- Product knowledge

### Technical Support

- Diagnostic approach
- Step-by-step guidance
- Troubleshooting protocols
- Technical accuracy

### Educational Tutor

- Socratic method
- Encouraging tone
- Progressive difficulty
- Understanding checks

### Business Advisor

- Analytical approach
- Risk consideration
- Strategic thinking
- Practical recommendations

## Advanced Techniques

### Context Windows

Manage what the AI remembers across conversations.

### Dynamic Behavior

Adjust behavior based on user expertise level.

### Multi-Turn Protocols

Define how to handle complex, multi-step interactions.

### Error Recovery

Specify how to recover from mistakes or misunderstandings.

## Real-World Applications

- Custom chatbots for websites
- Specialized AI assistants
- Customer service automation
- Educational tutoring systems
- Personal productivity assistants
- Technical support bots
- Research assistants

## Security & Ethics

**Important Considerations:**

⚠️ **Privacy**: Never request or store personal information
⚠️ **Safety**: Set clear boundaries on harmful content
⚠️ **Bias**: Actively work to reduce biased outputs
⚠️ **Transparency**: Be clear about AI limitations
⚠️ **Honesty**: Don't claim capabilities you don't have

## Version Control

System prompts should be versioned:

- Track what changes were made
- Document why changes were made
- Test each version thoroughly
- Roll back if issues arise

## Performance Monitoring

Track these metrics:

- User satisfaction
- Task completion rate
- Error rate
- Escalation rate
- Response quality
- Behavior consistency

## Contributing

Share your system prompt templates! [Contribution guidelines](../../CONTRIBUTING.md)

**What to include:**

- Clear use case description
- Complete prompt template
- Example interactions
- Testing notes
- Lessons learned

## Related Resources

- [Getting Started Guide](../../docs/getting-started.md)
- [Best Practices](../../docs/best-practices.md)
- [Introduction to Prompts](../../docs/intro-to-prompts.md)

## Further Reading

- Prompt engineering best practices
- AI safety and ethics guidelines
- Chatbot design principles
- Conversational AI patterns

---

**Note**: System prompts are powerful tools. Use them responsibly and test thoroughly before deployment.
