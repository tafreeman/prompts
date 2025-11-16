import sqlite3
from datetime import datetime
import os
import re

def load_prompts_from_repo():
    """Load prompts from existing markdown files in the repository"""
    prompts_from_files = []
    
    # Define the prompts directory
    prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'prompts')
    
    # Categories to scan
    categories = ['developers', 'business', 'creative', 'analysis', 'system']
    
    for category in categories:
        category_path = os.path.join(prompts_dir, category)
        if os.path.exists(category_path):
            for filename in os.listdir(category_path):
                if filename.endswith('.md') and filename != 'README.md':
                    filepath = os.path.join(category_path, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            prompt_data = parse_markdown_prompt(content, category)
                            if prompt_data:
                                prompts_from_files.append(prompt_data)
                    except Exception as e:
                        print(f"Error loading {filepath}: {e}")
    
    return prompts_from_files

def parse_markdown_prompt(content, category):
    """Parse a markdown prompt file and extract metadata"""
    try:
        # Extract YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]
                
                # Parse frontmatter
                metadata = {}
                for line in frontmatter.strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip().strip('"\'[]')
                
                # Extract prompt template from body
                prompt_match = re.search(r'```\n(.*?)\n```', body, re.DOTALL)
                if prompt_match:
                    template = prompt_match.group(1)
                else:
                    # If no code block, try to find the ## Prompt section
                    prompt_section = re.search(r'## Prompt\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL)
                    if prompt_section:
                        template = prompt_section.group(1).strip()
                    else:
                        template = "No template found in file"
                
                # Extract description
                desc_match = re.search(r'## Description\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL)
                description = desc_match.group(1).strip() if desc_match else metadata.get('title', 'No description')
                
                return {
                    'title': metadata.get('title', 'Untitled'),
                    'persona': metadata.get('category', category).capitalize(),
                    'use_case': metadata.get('tags', '').split(',')[0] if metadata.get('tags') else category,
                    'category': category.capitalize(),
                    'platform': 'Claude Sonnet 4.5',  # Default to Sonnet 4.5 per requirement
                    'template': template,
                    'description': description[:500],  # Limit description length
                    'tags': metadata.get('tags', category)
                }
    except Exception as e:
        print(f"Error parsing markdown: {e}")
    
    return None

def load_expanded_prompts():
    """Load comprehensive enterprise prompts into the database"""
    
    conn = sqlite3.connect('prompt_library.db')
    c = conn.cursor()
    
    # Create tables if they don't exist
    c.execute('''CREATE TABLE IF NOT EXISTS prompts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        persona TEXT NOT NULL,
        use_case TEXT,
        category TEXT NOT NULL,
        platform TEXT NOT NULL,
        template TEXT NOT NULL,
        description TEXT,
        tags TEXT,
        created_date TEXT,
        usage_count INTEGER DEFAULT 0
    )''')
    
    # Clear existing data
    c.execute('DELETE FROM prompts')
    
    # Load prompts from existing markdown files
    print("Loading prompts from repository files...")
    prompts_from_repo = load_prompts_from_repo()
    print(f"Found {len(prompts_from_repo)} prompts from repository files")
    
    # Add additional comprehensive enterprise prompts
    additional_prompts = [
        # DEVELOPER PERSONA
        {
            'title': 'Code Generation & Review',
            'persona': 'Developer',
            'use_case': 'Code Generation',
            'category': 'Development',
            'platform': 'Claude Sonnet 4.5',
            'template': '''ROLE: Senior Software Engineer with [Language/Framework] expertise
CONTEXT: Enterprise application development following [Company] coding standards
TASK: Generate production-ready code for [specific functionality]
AUDIENCE: Development team and technical reviewers
FORMAT: Well-documented code with inline comments and unit tests
CONSTRAINTS: Must follow security best practices, performance requirements, and accessibility standards
VALIDATION: Code review checklist, automated testing, security scan approval''',
            'description': 'Generate production-ready code with comprehensive review criteria',
            'tags': 'code,review,security,testing,enterprise'
        },
        {
            'title': 'API Documentation Generator',
            'persona': 'Developer',
            'use_case': 'Documentation',
            'category': 'Development',
            'platform': 'Claude Sonnet 4.5',
            'template': '''Generate comprehensive API documentation for [API name].

Include:
- Endpoint descriptions and purposes
- Request/response formats with examples
- Authentication requirements
- Error codes and handling
- Rate limiting information
- Sample code in [languages]

API Details:
[Paste your API specifications or code here]''',
            'description': 'Generate professional API documentation from code or specifications',
            'tags': 'api,documentation,swagger,openapi'
        },
        {
            'title': 'Test Case Generator',
            'persona': 'Developer',
            'use_case': 'Testing',
            'category': 'Development',
            'platform': 'Claude Sonnet 4.5',
            'template': '''Create comprehensive test cases for [feature/function name].

Context: [Brief description of functionality]
Testing Framework: [Jest/PyTest/JUnit/etc.]

Please generate:
1. Unit tests covering all code paths
2. Edge cases and boundary conditions
3. Error handling scenarios
4. Integration test scenarios
5. Mock data requirements

Code to test:
[Paste code here]''',
            'description': 'Generate comprehensive test suites for your code',
            'tags': 'testing,unit-tests,quality-assurance'
        },
        {
            'title': 'SQL Query Optimizer',
            'persona': 'Developer',
            'use_case': 'Database',
            'category': 'Development',
            'platform': 'Claude Sonnet 4.5',
            'template': '''Analyze and optimize this SQL query:

Database: [PostgreSQL/MySQL/SQL Server/etc.]
Current Query:
[Paste your SQL query]

Table Schema:
[Paste relevant table structures]

Issues noticed: [slow performance / high resource usage / etc.]

Please provide:
1. Analysis of current query performance
2. Optimization recommendations
3. Rewritten optimized query
4. Index suggestions
5. Explanation of improvements''',
            'description': 'Optimize SQL queries for better performance',
            'tags': 'sql,database,optimization,performance'
        },
        # BUSINESS PERSONA
        {
            'title': 'Executive Summary Generator',
            'persona': 'Business',
            'use_case': 'Reporting',
            'category': 'Business',
            'platform': 'Claude Sonnet 4.5',
            'template': '''Create an executive summary for [project/initiative name].

Background: [Context]
Key Findings: [Main points]
Data: [Key metrics and results]
Target Audience: [CXO level/Board/Investors]

Please create:
1. One-page executive summary
2. Key takeaways (3-5 bullet points)
3. Recommendation with rationale
4. Next steps
5. Visual data presentation suggestions''',
            'description': 'Generate concise executive summaries for leadership',
            'tags': 'executive,summary,reporting,business'
        },
        {
            'title': 'Competitive Analysis Framework',
            'persona': 'Business',
            'use_case': 'Analysis',
            'category': 'Business',
            'platform': 'Claude Sonnet 4.5',
            'template': '''Conduct a competitive analysis for [product/service] in [market/industry].

Our Product: [Description]
Key Competitors: [List competitors]
Market Position: [Your current position]

Analyze:
1. Competitive landscape overview
2. Feature comparison matrix
3. Pricing strategy comparison
4. Market positioning
5. Strengths and weaknesses
6. Opportunities for differentiation
7. Threat assessment''',
            'description': 'Comprehensive competitive analysis framework',
            'tags': 'competitive-analysis,market-research,strategy'
        },
        {
            'title': 'ROI Calculator Assistant',
            'persona': 'Business',
            'use_case': 'Financial',
            'category': 'Business',
            'platform': 'Claude Sonnet 4.5',
            'template': '''Calculate ROI for [initiative/investment name].

Investment Details:
- Initial Cost: [amount]
- Ongoing Costs: [amount/period]
- Time Frame: [duration]

Expected Benefits:
- [Benefit 1]: [quantified]
- [Benefit 2]: [quantified]
- [Benefit 3]: [quantified]

Please provide:
1. ROI calculation with formula
2. Payback period
3. Break-even analysis
4. Risk factors
5. Sensitivity analysis
6. Recommendation''',
            'description': 'Calculate and analyze return on investment',
            'tags': 'roi,financial,analysis,investment'
        },
        # CREATIVE PERSONA
        {
            'title': 'Social Media Campaign Creator',
            'persona': 'Creative',
            'use_case': 'Marketing',
            'category': 'Creative',
            'platform': 'Claude Sonnet 4.5',
            'template': '''Create a social media campaign for [product/event/announcement].

Campaign Goal: [awareness/engagement/conversion]
Target Audience: [demographics]
Platforms: [LinkedIn/Twitter/Instagram/Facebook]
Duration: [timeframe]
Tone: [professional/casual/humorous]

Please create:
1. Campaign theme and hashtag
2. Content calendar (posts for [X] days)
3. Post copy for each platform
4. Visual content suggestions
5. Engagement strategy
6. Success metrics''',
            'description': 'Design comprehensive social media campaigns',
            'tags': 'social-media,marketing,campaign,content'
        },
        {
            'title': 'Email Marketing Sequence',
            'persona': 'Creative',
            'use_case': 'Email Marketing',
            'category': 'Creative',
            'platform': 'Claude Sonnet 4.5',
            'template': '''Design an email marketing sequence for [purpose].

Product/Service: [name and description]
Audience: [target audience]
Goal: [nurture leads/onboard users/promote offer]
Sequence Length: [number of emails]

For each email provide:
1. Subject line (with A/B test variant)
2. Preview text
3. Email body copy
4. Call-to-action
5. Send timing recommendation
6. Personalization suggestions''',
            'description': 'Create engaging email marketing sequences',
            'tags': 'email,marketing,sequence,automation'
        },
        {
            'title': 'Brand Voice Guide Creator',
            'persona': 'Creative',
            'use_case': 'Branding',
            'category': 'Creative',
            'platform': 'Claude Sonnet 4.5',
            'template': '''Create a brand voice guide for [company/product name].

Company Description: [brief description]
Values: [core values]
Target Audience: [who you serve]
Industry: [your industry]
Desired Perception: [how you want to be seen]

Create comprehensive guide including:
1. Brand personality traits
2. Voice characteristics
3. Tone variations for different contexts
4. Vocabulary (words to use/avoid)
5. Writing examples (dos and don'ts)
6. Channel-specific guidelines''',
            'description': 'Develop consistent brand voice guidelines',
            'tags': 'branding,voice,guidelines,content'
        },
        # ANALYSIS PERSONA
        {
            'title': 'Data Visualization Recommender',
            'persona': 'Analyst',
            'use_case': 'Visualization',
            'category': 'Analysis',
            'platform': 'Claude Sonnet 4.5',
            'template': '''Recommend the best data visualization approach for this dataset.

Data Description:
- Type: [time series/categorical/numerical/mixed]
- Variables: [list key variables]
- Size: [row count, complexity]
- Purpose: [what you want to show]

Audience: [technical/executive/general]
Tool: [Tableau/PowerBI/Python/D3.js/Excel]

Please provide:
1. Recommended chart types (with rationale)
2. Visual design suggestions
3. Interactive elements to include
4. Key insights to highlight
5. Accessibility considerations
6. Implementation tips''',
            'description': 'Get expert recommendations for data visualization',
            'tags': 'visualization,charts,data,analytics'
        },
        {
            'title': 'Survey Data Analyzer',
            'persona': 'Analyst',
            'use_case': 'Research',
            'category': 'Analysis',
            'platform': 'Claude Sonnet 4.5',
            'template': '''Analyze survey results and provide insights.

Survey Topic: [topic]
Respondents: [number and demographics]
Key Questions: [list main questions]

Data Summary:
[Paste summary statistics or key findings]

Please provide:
1. Key findings and trends
2. Statistical significance analysis
3. Segment analysis
4. Actionable recommendations
5. Visualization suggestions
6. Executive summary
7. Areas for follow-up research''',
            'description': 'Analyze survey data and extract insights',
            'tags': 'survey,research,analysis,statistics'
        },
        {
            'title': 'Trend Analysis Report',
            'persona': 'Analyst',
            'use_case': 'Analysis',
            'category': 'Analysis',
            'platform': 'Claude Sonnet 4.5',
            'template': '''Analyze trends in [industry/market/metric].

Time Period: [duration]
Data Points: [what you're tracking]
Context: [relevant background]

Current Data:
[Paste your trend data]

Please analyze:
1. Historical trends and patterns
2. Current state assessment
3. Future projections
4. Driving factors
5. Risks and opportunities
6. Strategic implications
7. Recommended actions''',
            'description': 'Comprehensive trend analysis and forecasting',
            'tags': 'trends,forecasting,analysis,research'
        },
        # SYSTEM PROMPTS
        {
            'title': 'Technical Documentation Writer',
            'persona': 'System',
            'use_case': 'Documentation',
            'category': 'System',
            'platform': 'Claude Sonnet 4.5',
            'template': '''You are a technical documentation specialist. Your role is to create clear, comprehensive, and user-friendly documentation.

Guidelines:
- Write in clear, concise language
- Use consistent terminology
- Include code examples where appropriate
- Provide step-by-step instructions
- Anticipate user questions
- Add troubleshooting sections
- Include visual aids descriptions
- Keep security best practices in mind

When creating documentation:
1. Start with overview and prerequisites
2. Provide clear step-by-step instructions
3. Include code snippets with explanations
4. Add common pitfalls and how to avoid them
5. Include troubleshooting section
6. End with next steps or related topics''',
            'description': 'System prompt for technical documentation writing',
            'tags': 'documentation,technical-writing,system-prompt'
        },
        {
            'title': 'Code Review Assistant System',
            'persona': 'System',
            'use_case': 'Development',
            'category': 'System',
            'platform': 'Claude Sonnet 4.5',
            'template': '''You are an experienced software engineer conducting code reviews. Your expertise spans multiple programming languages, design patterns, and best practices.

Review Focus Areas:
1. **Code Quality**: Readability, maintainability, consistency
2. **Correctness**: Logic errors, edge cases, potential bugs
3. **Performance**: Efficiency, optimization opportunities
4. **Security**: Vulnerabilities, data validation, authentication
5. **Best Practices**: Language idioms, design patterns, SOLID principles
6. **Testing**: Test coverage, test quality, edge cases

Review Style:
- Be constructive and educational
- Explain the "why" behind suggestions
- Provide specific code examples
- Prioritize issues (critical vs. nice-to-have)
- Acknowledge good practices
- Suggest resources for learning

Format reviews with:
- Overall assessment
- Critical issues (must fix)
- Suggestions for improvement
- Praise for good practices
- Learning opportunities''',
            'description': 'System prompt for code review AI assistant',
            'tags': 'code-review,system-prompt,development'
        }
    ]
    
    # Combine all prompts
    all_prompts = prompts_from_repo + additional_prompts
    
    # Insert prompts
    for prompt in all_prompts:
        c.execute('''INSERT INTO prompts 
                     (title, persona, use_case, category, platform, template, description, tags, created_date, usage_count)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (prompt['title'], prompt['persona'], prompt['use_case'], prompt['category'],
                   prompt['platform'], prompt['template'], prompt['description'], prompt['tags'],
                   datetime.now().isoformat(), 0))
    
    conn.commit()
    conn.close()
    print(f"✅ Loaded {len(all_prompts)} prompts into the database ({len(prompts_from_repo)} from repo, {len(additional_prompts)} additional).")

if __name__ == '__main__':
    # Change to src directory to access database
    os.chdir(os.path.dirname(__file__))
    load_expanded_prompts()
