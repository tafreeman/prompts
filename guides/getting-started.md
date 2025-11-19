# Getting Started with the Prompts Library

Welcome! This guide will help you start using prompts from our library, whether you're a developer or a non-technical user.

## What Are Prompts?

Prompts are instructions you give to AI language models (like ChatGPT, Claude, or other AI assistants) to get specific types of responses. Think of them as recipes—they tell the AI exactly what you want and how you want it.

## For Non-Technical Users

### Step 1: Find a Prompt

1. **Browse by category** in the `prompts/` folder:
   - `business/` - For analysis, strategy, and business tasks
   - `creative/` - For content creation and marketing
   - `analysis/` - For data analysis and insights

2. **Look at the file name** - they're descriptive (e.g., `business-strategy-analysis.md`)

3. **Open the file** - Each prompt includes:
   - Description of what it does
   - When to use it
   - Example usage
   - Tips for best results

### Step 2: Customize the Prompt

1. **Find the "Prompt" section** in the file
2. **Look for text in [brackets]** - these are placeholders you need to replace
3. **Replace [brackets] with your information**:
   - `[YOUR COMPANY]` → "My Company Name"
   - `[YOUR GOAL]` → "Increase sales by 20%"
   - And so on...

### Step 3: Use the Prompt

1. **Copy the entire customized prompt**
2. **Paste it into your AI tool**:
   - ChatGPT (chat.openai.com)
   - Claude (claude.ai)
   - Your organization's AI assistant
3. **Hit send** and wait for the response

### Step 4: Refine if Needed

If the response isn't quite what you wanted:

- Provide more details
- Ask follow-up questions
- Try again with different information

### Quick Example

Let's say you want to write a blog post. Here's what you'd do:

1. **Navigate to:** `prompts/creative/content-marketing-blog-post.md`
2. **Open the file** and find the prompt section
3. **Replace placeholders:**
   - `[YOUR BLOG TOPIC]` → "How to organize your home office"
   - `[TARGET AUDIENCE]` → "Remote workers"
   - `[TONE]` → "Friendly and practical"
4. **Copy and paste** into ChatGPT or Claude
5. **Review the output** and ask for changes if needed

## For Developers

### Installation & Integration

```bash
# Clone the repository
git clone https://github.com/tafreeman/prompts.git
cd prompts

# Browse prompts
ls prompts/developers/
```

### Using Prompts Programmatically

Each prompt file uses Markdown with YAML frontmatter:

```python
import yaml
import re

def parse_prompt(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if match:
        metadata = yaml.safe_load(match.group(1))
        body = match.group(2)
        return metadata, body
    return None, content

# Example usage
metadata, body = parse_prompt('prompts/developers/code-review-assistant.md')
print(f"Title: {metadata['title']}")
print(f"Category: {metadata['category']}")
print(f"Tags: {metadata['tags']}")
```

### Integration with LLM APIs

```python
import openai

# Load a prompt
metadata, prompt_template = parse_prompt('prompts/developers/code-review-assistant.md')

# Extract the actual prompt section (you'll need to parse the markdown)
# ... parsing logic ...

# Use with OpenAI
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)
```

### Version Control Best Practices

```bash
# Check prompt history
git log -- prompts/developers/code-review-assistant.md

# Compare versions
git diff v1.0 v2.0 -- prompts/developers/code-review-assistant.md

# Use specific versions
git checkout v1.0 -- prompts/developers/code-review-assistant.md
```

### Creating a Prompt Management System

```python
class PromptLibrary:
    def __init__(self, library_path):
        self.library_path = library_path
        self.prompts = self._load_all_prompts()
    
    def _load_all_prompts(self):
        # Implementation to load all prompts
        pass
    
    def get_by_category(self, category):
        return [p for p in self.prompts if p['category'] == category]
    
    def get_by_tag(self, tag):
        return [p for p in self.prompts if tag in p['tags']]
    
    def search(self, query):
        # Implementation for full-text search
        pass

# Usage
library = PromptLibrary('prompts/')
dev_prompts = library.get_by_category('developers')
```

## Common Questions

### How do I know which prompt to use?

- **Start with your goal**: What do you want to accomplish?
- **Browse the category** that matches your goal
- **Read the descriptions** and use cases
- **Try the closest match** and refine from there

### Can I modify prompts?

Absolutely! Prompts are starting points. Feel free to:

- Add more specific details
- Adjust the tone or style
- Combine multiple prompts
- Create your own variations

### What if a prompt doesn't work?

- **Check your placeholders**: Did you replace all [brackets]?
- **Add more context**: More specific = better results
- **Try a different AI model**: Some prompts work better on certain models
- **Read the tips section**: Each prompt has suggestions
- **Ask for help**: Open a GitHub issue or discussion

### How do I contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines on adding or improving prompts.

## Best Practices

### For Better Results

1. **Be Specific**: More details = better outputs
2. **Provide Context**: Explain your situation and goals
3. **Use Examples**: Show what you want when possible
4. **Iterate**: First response is a starting point, refine it
5. **Save Good Results**: Keep track of what works for you

### For Consistency

1. **Use the same prompt** for similar tasks
2. **Create variations** for different scenarios
3. **Document your changes** if you modify prompts
4. **Share with your team** for consistency

## Next Steps

- **Explore Categories**: Browse different prompt categories
- **Try Examples**: Start with example prompts to get familiar
- **Read Best Practices**: Check out [docs/best-practices.md](best-practices.md)
- **Join the Community**: Contribute your own prompts
- **Stay Updated**: Watch the repository for new prompts

## Need Help?

- **GitHub Issues**: Report problems or ask questions
- **GitHub Discussions**: Share ideas and get feedback
- **Documentation**: Read advanced guides in `docs/`
- **Examples**: Check out `examples/` for inspiration

---

Happy prompting! 🚀
