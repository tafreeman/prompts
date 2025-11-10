# Prompts Library

A comprehensive, community-driven prompt library designed for everyone—from developers to business professionals. This repository provides well-organized, reusable prompts for AI/LLM interactions across diverse use cases.

## 🎯 Who This Library Is For

- **Developers**: Technical prompts for code generation, debugging, testing, and architecture
- **Business Professionals**: Prompts for analysis, strategy, reporting, and communication
- **Creative Teams**: Content creation, marketing, and storytelling prompts
- **Data Analysts**: Prompts for data analysis, insights extraction, and visualization
- **Everyone**: General-purpose system prompts and templates

## 📁 Repository Structure

```
prompts/
├── prompts/              # Main prompt collection
│   ├── developers/       # Technical & coding prompts
│   ├── business/         # Business analysis & strategy prompts
│   ├── creative/         # Content creation & marketing prompts
│   ├── analysis/         # Data analysis & research prompts
│   └── system/           # System-level AI agent prompts
├── templates/            # Reusable prompt templates
├── examples/             # Example usage and outputs
├── docs/                 # Documentation and guides
└── README.md            # This file
```

## 🚀 Quick Start

### For Non-Technical Users

1. **Browse by Category**: Navigate to the folder that matches your need (business, creative, etc.)
2. **Find a Prompt**: Each prompt file contains:
   - Description of what it does
   - When to use it
   - Example usage
   - Expected output
3. **Copy & Use**: Copy the prompt text and paste it into your AI tool
4. **Customize**: Replace placeholder text (marked with `[brackets]`) with your specific information

### For Developers

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tafreeman/prompts.git
   cd prompts
   ```

2. **Use prompts programmatically**:
   - Prompts are stored in Markdown format with YAML frontmatter
   - Parse metadata for categorization, versioning, and filtering
   - Integrate into your prompt management systems

3. **Version control**: All prompts are version-controlled via Git
   - Track changes and improvements
   - Roll back to previous versions
   - Collaborate through pull requests

## 📝 Prompt Format

Each prompt follows a consistent structure:

```markdown
---
title: "Prompt Title"
category: "developers|business|creative|analysis|system"
tags: ["tag1", "tag2", "tag3"]
author: "Author Name"
version: "1.0"
date: "2025-10-29"
difficulty: "beginner|intermediate|advanced"
---

# Prompt Title

## Description
Brief description of what this prompt does and when to use it.

## Use Cases
- Use case 1
- Use case 2
- Use case 3

## Prompt

[Your actual prompt text goes here]

## Variables
- `[variable1]`: Description of what to replace this with
- `[variable2]`: Description of what to replace this with

## Example Usage

**Input:**
```
Example of the prompt with real values
```

**Output:**
```
Example of expected output
```

## Tips
- Tip 1 for better results
- Tip 2 for customization
```

## 🤝 Contributing

We welcome contributions from everyone! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Adding new prompts
- Improving existing prompts
- Reporting issues
- Suggesting new categories

## 📚 Documentation

- **[Getting Started Guide](docs/getting-started.md)**: For first-time users
- **[Developer Guide](docs/developer-guide.md)**: For technical integration
- **[Best Practices](docs/best-practices.md)**: Tips for effective prompt engineering
- **[Prompt Template](templates/prompt-template.md)**: Template for creating new prompts

## 🏷️ Categories

### Developers
Code generation, debugging, testing, architecture design, documentation, refactoring, and technical problem-solving.

### Business
Business analysis, strategy planning, market research, financial analysis, reporting, and decision-making support.

### Creative
Content creation, copywriting, marketing campaigns, social media, storytelling, brainstorming, and brand development.

### Analysis
Data analysis, research synthesis, statistical interpretation, trend analysis, and insight generation.

### System
System-level prompts for AI agents, role definitions, behavior guidelines, and general-purpose configurations.

## 📖 Learning Resources

- **New to Prompt Engineering?** Start with our [Introduction to Prompts](docs/intro-to-prompts.md)
- **Advanced Techniques**: Check out [Advanced Prompt Engineering](docs/advanced-techniques.md)
- **Examples**: Browse [examples/](examples/) for real-world use cases

## 🔍 Finding the Right Prompt

1. **By Use Case**: Navigate to the relevant category folder
2. **By Tag**: Search for specific tags in prompt metadata
3. **By Difficulty**: Filter by beginner, intermediate, or advanced levels
4. **By Search**: Use GitHub's search feature to find keywords

## 📊 Prompt Quality Standards

All prompts in this library:
- ✅ Are tested and validated
- ✅ Include clear descriptions and examples
- ✅ Follow consistent formatting
- ✅ Include metadata for easy discovery
- ✅ Are reviewed by the community

## 🔄 Version History

Prompts are versioned to track improvements:
- **1.0**: Initial version
- **1.1**: Minor improvements
- **2.0**: Major changes or rewrites

Check individual prompt files for version history.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

This library is inspired by popular prompt libraries including:
- weam-ai/weam
- danielrosehill/System-Prompt-Library
- kevin-hammond/prompt-library

Thank you to all contributors who help improve this resource!

## 📞 Support

- **Issues**: Report bugs or suggest improvements via [GitHub Issues](https://github.com/tafreeman/prompts/issues)
- **Discussions**: Join conversations in [GitHub Discussions](https://github.com/tafreeman/prompts/discussions)
- **Pull Requests**: Contribute directly via [Pull Requests](https://github.com/tafreeman/prompts/pulls)

---

**Made with ❤️ by the community, for the community.**