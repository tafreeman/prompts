# Enterprise AI Prompt Library - Web Application

A comprehensive web application for managing and customizing AI prompts, optimized for Claude Sonnet 4.5 and Code 5.

## ✨ Features

- **70+ Curated Prompts**: Comprehensive library spanning Developer, Business, Creative, Analyst, and System personas
- **Smart Search & Filtering**: Find prompts by persona, category, platform, or keywords
- **Dynamic Customization**: Fill in placeholders to generate personalized prompts
- **Spell-Check Integration**: Built-in spell checking and autocorrect for text inputs
- **Usage Analytics**: Track prompt usage and identify popular prompts
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **One-Click Copy**: Copy prompts to clipboard with visual feedback
- **Multiple Deployment Options**: Deploy to IIS, AWS, Azure, Docker, or locally

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/tafreeman/prompts.git
cd prompts/src

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with prompts
python load_prompts.py

# Run the application
python app.py
```

Open your browser to `http://localhost:5000`

### Using Docker

```bash
# Clone the repository
git clone https://github.com/tafreeman/prompts.git
cd prompts

# Build and run with Docker Compose
docker-compose -f deployment/docker/docker-compose.yml up -d

# Access at http://localhost:5000
```

## 📋 Requirements

- Python 3.8 or higher
- Flask 3.1.2
- SQLite 3.x (included with Python)
- wfastcgi 3.0.0 (for IIS deployment only)
- Modern web browser with JavaScript enabled

## 🏗️ Project Structure

```text
prompts/
├── src/                          # Application source code
│   ├── app.py                    # Main Flask application
│   ├── load_prompts.py          # Database initialization script
│   ├── requirements.txt         # Python dependencies
│   ├── templates/               # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── index.html          # Main library view
│   │   ├── customize.html      # Prompt customization
│   │   ├── prompt_detail.html  # Detailed prompt view
│   │   └── analytics.html      # Analytics dashboard
│   └── static/                  # Static assets
│       ├── css/
│       │   └── style.css       # Custom styles (fixes text visibility)
│       └── js/
│           └── app.js          # Client-side functionality & spell-check
├── deployment/                   # Deployment configurations
│   ├── iis/                     # IIS deployment
│   ├── docker/                  # Docker deployment
│   ├── aws/                     # AWS deployment guides
│   └── azure/                   # Azure deployment guides
├── prompts/                      # Original markdown prompts
├── docs/                         # Documentation
└── README.md                     # This file
```

## 🎯 Key Features Explained

### Text Visibility Fix

The application includes comprehensive CSS fixes to ensure all text is visible:

- Explicit color definitions for all text elements
- High-contrast color schemes
- Proper text rendering on all backgrounds
- Accessible color combinations

### Spell-Check & Autocorrect

Built-in spell-checking features:

- Browser-native spell checking enabled on all text inputs
- Custom autocorrect for common typos
- Automatic correction of Claude model names (e.g., "Sonnet 4" → "Sonnet 4.5")
- Visual indicators for spelling errors
- Real-time spell-check feedback

### Prompt Customization

Dynamic form generation based on prompt placeholders:

1. System detects `[placeholder]` tokens in prompt templates
2. Generates form fields automatically
3. Validates required fields
4. Replaces placeholders with user input
5. Displays customized prompt ready to copy

### Analytics Dashboard

Track prompt usage with visual insights:

- Total prompts and usage statistics
- Usage by persona (doughnut chart)
- Usage by platform (bar chart)
- Top 10 most-used prompts table
- Category and platform breakdowns

## 🔧 Configuration

### Environment Variables

```bash
# Development
export FLASK_ENV=development
export FLASK_APP=app.py
export FLASK_DEBUG=1

# Production
export FLASK_ENV=production
export FLASK_APP=app.py
```

### Database Location

By default, the SQLite database is created at `src/prompt_library.db`. To change:

```python
# In app.py
DATABASE = '/path/to/your/database.db'
```

## 📊 Prompts Included

The application includes prompts from:

1. **Existing Repository**: All prompts from `prompts/` directory are automatically loaded
2. **Enhanced Collection**: 15+ additional enterprise prompts covering:
   - Code generation & review
   - API documentation
   - Test case generation
   - SQL optimization
   - Business analysis
   - ROI calculations
   - Social media campaigns
   - Email marketing
   - Data visualization
   - Trend analysis
   - System prompts for AI assistants

All prompts are optimized for **Claude Sonnet 4.5** and **Code 5**.

## 🚢 Deployment Options

### Local IIS (Windows)

See [deployment/iis/README.md](deployment/iis/README.md) for detailed instructions.

**One-command deployment:**

```powershell
# Run as Administrator
.\deployment\iis\deploy.ps1
```

This automated script will:

- Detect your Python installation
- Install all dependencies (including wfastcgi)
- Create application directories
- Configure IIS and FastCGI
- Initialize the database
- Set permissions
- Start the website

**Cost**: Free (uses existing Windows Server)

### Docker

See [deployment/docker/README.md](deployment/docker/README.md) for detailed instructions.

```bash
# Build and run
docker-compose -f deployment/docker/docker-compose.yml up -d
```

**Cost**: Infrastructure cost only (~$5-15/month on cloud)

### AWS

See [deployment/aws/README.md](deployment/aws/README.md) for detailed instructions.

**Options:**

- AWS Lightsail Container: $7/month
- ECS Fargate: $15-30/month
- Elastic Beanstalk: $20-40/month

### Azure

See [deployment/azure/README.md](deployment/azure/README.md) for detailed instructions.

**Options:**

- Container Instances: $10-20/month
- App Service: $13-55/month
- AKS: $70+/month

### GitHub Pages (Static Documentation Only)

The application includes a GitHub Actions workflow that automatically updates documentation on GitHub Pages.

## 🛠️ Development

### Adding New Prompts

#### Method 1: Via Markdown Files

1. Create a new markdown file in `prompts/[category]/`
2. Use the standard format (see existing files)
3. Run `python load_prompts.py` to reload database

#### Method 2: Directly in Python

Edit `load_prompts.py` and add to the `additional_prompts` list:

```python
{
    'title': 'Your Prompt Title',
    'persona': 'Developer|Business|Creative|Analyst|System',
    'use_case': 'Your Use Case',
    'category': 'Your Category',
    'platform': 'Claude Sonnet 4.5',
    'template': '''Your prompt template with [placeholders]''',
    'description': 'Brief description',
    'tags': 'tag1,tag2,tag3'
}
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests (if test suite exists)
pytest
```

### Code Style

```bash
# Install formatting tools
pip install black flake8

# Format code
black src/

# Check style
flake8 src/
```

## 🐛 Troubleshooting

### Text Not Showing

- **Fixed in this version**: CSS includes explicit color definitions
- Check browser console for errors
- Ensure JavaScript is enabled
- Try hard refresh (Ctrl+F5 or Cmd+Shift+R)

### Database Errors

```bash
# Reinitialize database
cd src
rm prompt_library.db
python load_prompts.py
```

### Port Already in Use

```bash
# Change port in app.py
app.run(port=8080)  # Use different port

# Or kill process using port 5000
# On Linux/Mac:
lsof -ti:5000 | xargs kill

# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Spell-Check Not Working

- Ensure browser supports HTML5 spellcheck attribute
- Check that JavaScript is enabled
- Verify `app.js` is loading correctly

## 📈 Performance

- **Lightweight**: SQLite database, no external dependencies
- **Fast**: Indexed database queries
- **Scalable**: Can handle 1000+ prompts efficiently
- **Optimized**: Minified CSS, efficient JavaScript

## 🔒 Security

- **Input Validation**: All user inputs are sanitized
- **SQL Injection Prevention**: Using parameterized queries
- **XSS Protection**: Jinja2 autoescaping enabled
- **CSRF Protection**: Add Flask-WTF for forms
- **HTTPS**: Supported via reverse proxy or cloud platform

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🙏 Acknowledgments

- Built for Big 4 consulting teams and enterprise users
- Optimized for Claude Sonnet 4.5 and Code 5
- Inspired by the prompt engineering community
- Bootstrap for UI components
- Chart.js for analytics visualizations

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/tafreeman/prompts/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tafreeman/prompts/discussions)
- **Documentation**: [docs/](../docs/)

## 🗺️ Roadmap

- [ ] User authentication and personal prompt libraries
- [ ] Prompt versioning and history
- [ ] API endpoints for programmatic access
- [ ] Export prompts to various formats (JSON, CSV)
- [ ] Collaborative prompt editing
- [ ] Integration with Claude API for direct testing
- [ ] Advanced analytics and usage insights
- [ ] Mobile app (iOS/Android)

## 📊 Stats

- **20+ Prompts**: Growing library with 5 from repository + 15 enterprise prompts
- **5 Personas**: Developer, Business, Creative, Analyst, System
- **Multiple Platforms**: Claude Sonnet 4.5, Code 5, and more
- **Deployment Options**: 6+ deployment methods (IIS one-command!)
- **Cost-Effective**: Free (IIS) to $7/month (AWS)

---

**Made with ❤️ for the AI community**

Optimized for Claude Sonnet 4.5 and Code 5
