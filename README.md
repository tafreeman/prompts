# Enterprise AI Prompt Library

A comprehensive, community-driven prompt library with a **web application** designed for everyone—from developers to business professionals. This repository provides well-organized, reusable prompts for AI/LLM interactions across diverse use cases, optimized for **Claude Sonnet 4.5** and **Code 5**.

## 🌟 New: Web Application!

We've built a full-featured web application to make browsing and using prompts even easier:

- **🔍 Smart Search & Filtering**: Find prompts quickly by persona, category, platform, or keywords
- **✏️ Dynamic Customization**: Fill in placeholders with an easy-to-use form interface
- **✓ Spell-Check Built-in**: Automatic spell checking and autocorrect for your inputs
- **📊 Analytics Dashboard**: Track prompt usage and popular prompts
- **📱 Responsive Design**: Works on desktop, tablet, and mobile
- **🚀 One-Command Deployment**: Deploy to IIS, AWS, Azure, Docker, or run locally

### Quick Start - Web Application

```bash
# Clone and run locally
git clone https://github.com/tafreeman/prompts.git
cd prompts/src
pip install -r requirements.txt
python load_prompts.py
python app.py
# Open http://localhost:5000
```

For deployment options (IIS, AWS, Azure, Docker), see [src/README.md](src/README.md).

## 🎯 Who This Library Is For

- **Developers**: Technical prompts for code generation, debugging, testing, and architecture
- **Business Professionals**: Prompts for analysis, strategy, reporting, and communication
- **Creative Teams**: Content creation, marketing, and storytelling prompts
- **Data Analysts**: Prompts for data analysis, insights extraction, and visualization
- **Advanced Users**: Chain-of-Thought, ReAct, RAG, and Tree-of-Thoughts patterns 🆕
- **Enterprise Teams**: Legal, compliance, security, and governance prompts with audit controls 🆕
- **Everyone**: General-purpose system prompts and templates

## ✨ New: Advanced Techniques & Enterprise Governance

### Advanced Prompting Techniques
Frontier model capabilities require advanced prompting patterns. We now include:

- **Chain-of-Thought (CoT)**: Step-by-step reasoning with concise and detailed modes
- **ReAct**: Reasoning + Acting patterns for tool-augmented tasks
- **RAG (Retrieval-Augmented Generation)**: Document retrieval with citation frameworks
- **Reflection**: Self-critique and iterative improvement patterns
- **Tree-of-Thoughts (ToT)**: Multi-branch reasoning with backtracking

📚 **[Explore Advanced Techniques →](prompts/advanced-techniques/)**

### Enterprise Governance & Compliance
Production AI requires governance, risk management, and compliance controls:

- **Legal Prompts**: Contract review, compliance checks, policy drafting
- **Security Prompts**: Incident response, threat modeling, vulnerability assessment
- **Governance Metadata**: PII-handling, risk levels, approval requirements, audit trails
- **Regulatory Compliance**: GDPR, CCPA, SOX, HIPAA, ISO 27001, NIST frameworks
- **Access Controls**: Role-based permissions, human review requirements

📋 **[Explore Governance & Compliance →](prompts/governance-compliance/)**

## 📁 Repository Structure

```
prompts/
├── src/                   # 🆕 Web Application
│   ├── app.py            # Flask application
│   ├── templates/        # HTML templates  
│   ├── static/           # CSS, JavaScript
│   ├── load_prompts.py  # Database initialization
│   └── README.md         # Web app documentation
├── deployment/           # 🆕 Deployment Configurations
│   ├── iis/              # IIS deployment guide
│   ├── docker/           # Docker & docker-compose
│   ├── aws/              # AWS deployment guide
│   └── azure/            # Azure deployment guide
├── prompts/              # Markdown prompt collection
│   ├── developers/       # Technical & coding prompts
│   ├── business/         # Business analysis & strategy prompts
│   ├── creative/         # Content creation & marketing prompts
│   ├── analysis/         # Data analysis & research prompts
│   ├── system/           # System-level AI agent prompts
│   ├── advanced-techniques/  # 🆕 Advanced prompting (CoT, ReAct, RAG, ToT)
│   └── governance-compliance/  # 🆕 Legal, security, compliance prompts
├── templates/            # Reusable prompt templates
├── examples/             # Example usage and outputs
├── docs/                 # Documentation and guides
└── README.md            # This file
```

## 🚀 Quick Start

### Option 1: Use the Web Application (Recommended)

**Run Locally:**
```bash
git clone https://github.com/tafreeman/prompts.git
cd prompts/src
pip install -r requirements.txt
python load_prompts.py  # Initialize database with 20+ prompts
python app.py           # Start the application
# Open http://localhost:5000
```

**Or Deploy to Cloud:**
- **IIS (One Command)**: `deployment\iis\deploy.ps1` - Free on Windows Server
- **Docker**: `docker-compose -f deployment/docker/docker-compose.yml up -d`
- **AWS Lightsail**: $7/month (see [deployment/aws/README.md](deployment/aws/README.md))
- **Azure Container**: $10-20/month (see [deployment/azure/README.md](deployment/azure/README.md))

### Option 2: Browse Markdown Files

For direct access to prompt markdown files:

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

### Web Application
- **[Web App README](src/README.md)**: Complete guide for the web application
- **[IIS Deployment](deployment/iis/README.md)**: Windows Server deployment
- **[Docker Deployment](deployment/docker/README.md)**: Containerized deployment
- **[AWS Deployment](deployment/aws/README.md)**: Amazon Web Services options
- **[Azure Deployment](deployment/azure/README.md)**: Microsoft Azure options

### General Documentation
- **[Getting Started Guide](docs/getting-started.md)**: For first-time users
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

## 🎨 Web Application Features

The web application provides an enhanced user experience:

### Core Features
- **📚 20+ Prompts**: Loaded from repository + additional enterprise prompts
- **🔍 Advanced Search**: Filter by persona, category, platform, or search text
- **✏️ Smart Customization**: Dynamic forms based on prompt placeholders
- **✓ Spell-Check**: Built-in spell checking with autocorrect
- **📊 Analytics**: Usage tracking and insights dashboard
- **📱 Responsive**: Works on all devices
- **🎯 One-Click Copy**: Copy prompts to clipboard instantly

### Technical Features
- **Flask Backend**: Lightweight Python web framework
- **SQLite Database**: Simple, file-based storage
- **Bootstrap 5 UI**: Modern, accessible interface
- **Chart.js Analytics**: Visual data representation
- **No External APIs**: Runs completely offline

### Fixed Issues
- ✅ **Text Visibility Fixed**: All text now shows with proper contrast and colors
- ✅ **Spell-Check Added**: HTML5 + custom autocorrect for typos and model names
- ✅ **Easy Deployment**: Multiple options from $7/month to free (IIS)
- ✅ **Optimized for Claude**: All prompts work with Sonnet 4.5 and Code 5

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