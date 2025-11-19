import sqlite3
from datetime import datetime
import os
import re

def load_prompts_from_repo():
    """Load prompts from existing markdown files in the repository"""
    prompts_from_files = []
    
    # Define the prompts directory
    prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'prompts')
    
    # Categories to scan (must match actual folder names on disk)
    categories = ['developers', 'business', 'creative', 'analysis', 'system', 'advanced', 'governance']
    
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
                    'platform': metadata.get('platform', 'Claude Sonnet 4.5'),  # Use metadata platform if available
                    'template': template,
                    'description': description[:500],  # Limit description length
                    'tags': metadata.get('tags', category),
                    'difficulty': metadata.get('difficulty', 'intermediate'),
                    'governance_tags': metadata.get('governance_tags', ''),
                    'data_classification': metadata.get('data_classification', 'Internal'),
                    'risk_level': metadata.get('risk_level', 'Low'),
                    'regulatory_scope': metadata.get('regulatory_scope', ''),
                    'approval_required': metadata.get('approval_required', 'None'),
                    'retention_period': metadata.get('retention_period', 'Standard')
                }
    except Exception as e:
        print(f"Error parsing markdown: {e}")
    
    return None

def load_expanded_prompts():
    """Load comprehensive enterprise prompts into the database.

    The table schema here is intentionally kept in sync with `app.init_db()`
    so that whether the database is first created by the web app or by this
    loader script, the `prompts` table has the same columns.
    """
    conn = sqlite3.connect('prompt_library.db')
    c = conn.cursor()
    
    # Create tables if they don't exist (schema must match app.init_db)
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
        usage_count INTEGER DEFAULT 0,
        difficulty TEXT,
        governance_tags TEXT,
        data_classification TEXT,
        risk_level TEXT,
        regulatory_scope TEXT,
        approval_required TEXT,
        retention_period TEXT
    )''')
    
    # Clear existing data
    c.execute('DELETE FROM prompts')
    
    # Load prompts from existing markdown files
    print("Loading prompts from repository files...")
    prompts_from_repo = load_prompts_from_repo()
    print(f"Found {len(prompts_from_repo)} prompts from repository files")
    
    # Add additional comprehensive enterprise prompts (existing + migrated set)
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

    # Merge in migrated prompts from the historical expanded dataset
    additional_prompts.extend(get_migrated_prompts_from_legacy_dataset())
    
    # Combine all prompts
    all_prompts = prompts_from_repo + additional_prompts
    
    # Insert prompts
    for prompt in all_prompts:
        c.execute('''INSERT INTO prompts 
                     (title, persona, use_case, category, platform, template, description, tags, created_date, usage_count,
                      difficulty, governance_tags, data_classification, risk_level, regulatory_scope, approval_required, retention_period)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (prompt['title'], prompt['persona'], prompt['use_case'], prompt['category'],
                   prompt['platform'], prompt['template'], prompt['description'], prompt['tags'],
                   datetime.now().isoformat(), 0,
                   prompt.get('difficulty', 'intermediate'),
                   prompt.get('governance_tags', ''),
                   prompt.get('data_classification', 'Internal'),
                   prompt.get('risk_level', 'Low'),
                   prompt.get('regulatory_scope', ''),
                   prompt.get('approval_required', 'None'),
                   prompt.get('retention_period', 'Standard')))
    
    conn.commit()
    conn.close()
    print(f"✅ Loaded {len(all_prompts)} prompts into the database ({len(prompts_from_repo)} from repo, {len(additional_prompts)} additional).")


def get_migrated_prompts_from_legacy_dataset():
    """Return prompts migrated from the legacy expanded dataset.

    These were originally defined in `enterprise_ai_prompt_library_complete (5)/stage_2_expanded_database/load_expanded_data.py`
    using `{variable}` syntax and a different schema. Here we:
    - Map personas into the current categories (Development/Business/System/Analysis)
    - Use the original category as `use_case`
    - Convert `{name}` placeholders to `[name]` for consistency with the main app
    - Generate simple tag strings from persona/use_case
    """

    def to_new_template(text):
        return re.sub(r"\{([^}]+)\}", r"[\1]", text)

    def map_category(persona):
        if persona == "Developer":
            return "Development"
        if persona in ("Project Manager", "Consultant"):
            return "Business"
        if persona in ("Business Analyst", "Researcher"):
            return "Analysis"
        if persona == "Architect":
            return "System"
        return persona

    def make_tags(persona, use_case):
        base = [persona.lower().replace(" ", "-"), use_case.lower().replace(" ", "-"), "enterprise"]
        return ",".join(base)

    legacy = [
        ("Code Generation Assistant", "Generates clean, efficient code based on requirements", "Developer", "Code Generation",
         "Generate {language} code for the following requirements:\n\nFunctionality: {functionality}\nInput: {input_format}\nOutput: {output_format}\nConstraints: {constraints}\n\nPlease provide:\n1. Clean, well-commented code\n2. Error handling\n3. Unit tests\n4. Documentation\n5. Performance considerations"),
        ("API Design Consultant", "Creates RESTful API specifications", "Developer", "API Design",
         "Design a RESTful API for {service_name} with the following requirements:\n\nCore Functionality: {core_features}\nData Models: {data_models}\nAuthentication: {auth_method}\nRate Limiting: {rate_limits}\n\nProvide:\n1. Endpoint specifications\n2. Request/Response schemas\n3. Error handling\n4. Security considerations\n5. Documentation structure"),
        ("Database Schema Designer", "Designs optimized database schemas", "Developer", "Database Design",
         "Design a database schema for {application_name}:\n\nBusiness Requirements: {requirements}\nExpected Scale: {scale}\nPerformance Needs: {performance}\nCompliance: {compliance}\n\nInclude:\n1. Entity-Relationship diagram\n2. Table structures with constraints\n3. Indexing strategy\n4. Normalization analysis\n5. Migration scripts"),
        ("Code Review Expert", "Provides comprehensive code reviews", "Developer", "Code Quality",
         "Review the following {language} code for:\n\nCode: {code_snippet}\nContext: {context}\nCritical Areas: {focus_areas}\n\nAnalyze:\n1. Code quality and best practices\n2. Security vulnerabilities\n3. Performance bottlenecks\n4. Maintainability issues\n5. Testing coverage\n6. Documentation quality\n\nProvide specific recommendations with examples."),
        ("Legacy System Modernization", "Plans legacy system upgrades", "Developer", "Modernization",
         "Create a modernization plan for:\n\nLegacy System: {system_name}\nCurrent Technology: {current_tech}\nTarget Technology: {target_tech}\nBusiness Constraints: {constraints}\nTimeline: {timeline}\n\nProvide:\n1. Migration strategy\n2. Risk assessment\n3. Phased approach\n4. Resource requirements\n5. Testing strategy\n6. Rollback plans"),
        ("DevOps Pipeline Architect", "Designs CI/CD pipelines", "Developer", "DevOps",
         "Design a CI/CD pipeline for {project_name}:\n\nTechnology Stack: {tech_stack}\nDeployment Environment: {environment}\nTesting Requirements: {testing}\nSecurity Requirements: {security}\n\nInclude:\n1. Pipeline stages\n2. Automated testing strategy\n3. Deployment automation\n4. Monitoring and alerting\n5. Security scanning\n6. Rollback mechanisms"),
        ("Performance Optimization Specialist", "Optimizes application performance", "Developer", "Performance",
         "Analyze and optimize performance for:\n\nApplication: {app_name}\nCurrent Issues: {performance_issues}\nTarget Metrics: {target_metrics}\nConstraints: {constraints}\n\nProvide:\n1. Performance bottleneck analysis\n2. Optimization recommendations\n3. Caching strategies\n4. Database optimization\n5. Code-level improvements\n6. Monitoring setup"),
        ("Security Code Auditor", "Conducts security code audits", "Developer", "Security",
         "Perform a security audit on:\n\nApplication: {app_name}\nCode Base: {code_description}\nSecurity Framework: {security_framework}\nCompliance Requirements: {compliance}\n\nAnalyze:\n1. Authentication and authorization\n2. Input validation\n3. Data encryption\n4. SQL injection vulnerabilities\n5. XSS vulnerabilities\n6. OWASP Top 10 compliance"),
        ("Microservices Architect", "Designs microservices architectures", "Developer", "Architecture",
         "Design a microservices architecture for:\n\nApplication: {app_name}\nBusiness Domains: {domains}\nScale Requirements: {scale}\nTechnology Preferences: {tech_prefs}\n\nProvide:\n1. Service decomposition strategy\n2. Inter-service communication\n3. Data management approach\n4. Service discovery\n5. Monitoring and observability\n6. Deployment strategy"),
        ("Test Automation Engineer", "Creates comprehensive test strategies", "Developer", "Testing",
         "Design a test automation strategy for:\n\nApplication: {app_name}\nTesting Scope: {scope}\nTechnology Stack: {tech_stack}\nQuality Goals: {quality_goals}\n\nInclude:\n1. Test pyramid strategy\n2. Unit testing approach\n3. Integration testing\n4. End-to-end testing\n5. Performance testing\n6. Test data management"),
        ("Cloud Migration Specialist", "Plans cloud migration strategies", "Developer", "Cloud Migration",
         "Create a cloud migration plan for:\n\nApplication: {app_name}\nCurrent Infrastructure: {current_infra}\nTarget Cloud: {target_cloud}\nBusiness Requirements: {requirements}\n\nProvide:\n1. Migration assessment\n2. Cloud architecture design\n3. Migration phases\n4. Cost optimization\n5. Security considerations\n6. Performance validation"),
        ("Documentation Generator", "Creates technical documentation", "Developer", "Documentation",
         "Generate comprehensive documentation for:\n\nProject: {project_name}\nAudience: {audience}\nDocumentation Type: {doc_type}\nTechnical Details: {tech_details}\n\nInclude:\n1. Architecture overview\n2. API documentation\n3. Setup instructions\n4. Usage examples\n5. Troubleshooting guide\n6. Contributing guidelines"),
        ("Mobile App Developer", "Guides mobile application development", "Developer", "Mobile Development",
         "Plan mobile app development for:\n\nApp Concept: {app_concept}\nTarget Platforms: {platforms}\nKey Features: {features}\nUser Experience Goals: {ux_goals}\n\nProvide:\n1. Technical architecture\n2. Platform-specific considerations\n3. Performance optimization\n4. Security implementation\n5. Testing strategy\n6. Deployment process"),
        ("Data Pipeline Engineer", "Designs data processing pipelines", "Developer", "Data Engineering",
         "Design a data pipeline for:\n\nData Sources: {data_sources}\nProcessing Requirements: {processing}\nTarget Systems: {targets}\nVolume and Velocity: {scale}\n\nInclude:\n1. Pipeline architecture\n2. Data transformation logic\n3. Error handling and recovery\n4. Monitoring and alerting\n5. Scalability considerations\n6. Data quality validation"),
        ("Frontend Architecture Consultant", "Designs frontend architectures", "Developer", "Frontend",
         "Design frontend architecture for:\n\nApplication: {app_name}\nUser Requirements: {user_requirements}\nTechnology Stack: {tech_stack}\nPerformance Goals: {performance}\n\nProvide:\n1. Component architecture\n2. State management strategy\n3. Routing and navigation\n4. Performance optimization\n5. Accessibility compliance\n6. Testing approach"),
        ("Project Charter Creator", "Develops comprehensive project charters", "Project Manager", "Planning",
         "Create a project charter for:\n\nProject Name: {project_name}\nBusiness Objective: {objective}\nKey Stakeholders: {stakeholders}\nBudget Range: {budget}\nTimeline: {timeline}\n\nInclude:\n1. Executive summary\n2. Scope and deliverables\n3. Success criteria\n4. Resource requirements\n5. Risk assessment\n6. Communication plan"),
        ("Agile Sprint Planner", "Plans and manages agile sprints", "Project Manager", "Agile",
         "Plan sprint for:\n\nProject: {project_name}\nSprint Duration: {duration}\nTeam Capacity: {capacity}\nPriority Features: {features}\nDefinition of Done: {dod}\n\nProvide:\n1. Sprint goal\n2. User story breakdown\n3. Task estimation\n4. Capacity planning\n5. Risk mitigation\n6. Success metrics"),
        ("Risk Management Analyst", "Identifies and manages project risks", "Project Manager", "Risk Management",
         "Analyze risks for:\n\nProject: {project_name}\nProject Phase: {phase}\nKey Concerns: {concerns}\nStakeholder Impact: {impact}\n\nProvide:\n1. Risk identification matrix\n2. Probability and impact assessment\n3. Risk mitigation strategies\n4. Contingency plans\n5. Monitoring procedures\n6. Escalation protocols"),
        ("Stakeholder Communication Manager", "Manages stakeholder communications", "Project Manager", "Communication",
         "Develop communication strategy for:\n\nProject: {project_name}\nStakeholders: {stakeholders}\nProject Phase: {phase}\nCommunication Challenges: {challenges}\n\nInclude:\n1. Stakeholder analysis\n2. Communication matrix\n3. Meeting schedules\n4. Reporting templates\n5. Escalation procedures\n6. Feedback mechanisms"),
        ("Resource Allocation Optimizer", "Optimizes project resource allocation", "Project Manager", "Resource Management",
         "Optimize resources for:\n\nProject: {project_name}\nAvailable Resources: {resources}\nProject Constraints: {constraints}\nPriority Areas: {priorities}\n\nProvide:\n1. Resource allocation matrix\n2. Skill gap analysis\n3. Workload balancing\n4. Timeline optimization\n5. Cost efficiency measures\n6. Contingency planning"),
        ("Quality Assurance Planner", "Develops QA strategies and plans", "Project Manager", "Quality Assurance",
         "Create QA plan for:\n\nProject: {project_name}\nQuality Standards: {standards}\nDeliverables: {deliverables}\nTesting Requirements: {testing}\n\nInclude:\n1. Quality objectives\n2. QA processes and procedures\n3. Testing strategy\n4. Quality metrics\n5. Review and approval workflows\n6. Continuous improvement"),
        ("Change Management Coordinator", "Manages project changes effectively", "Project Manager", "Change Management",
         "Manage change for:\n\nProject: {project_name}\nProposed Changes: {changes}\nImpact Assessment: {impact}\nStakeholder Concerns: {concerns}\n\nProvide:\n1. Change impact analysis\n2. Approval workflow\n3. Communication strategy\n4. Implementation plan\n5. Risk mitigation\n6. Success measurement"),
        ("Budget and Cost Controller", "Manages project budgets and costs", "Project Manager", "Financial Management",
         "Manage budget for:\n\nProject: {project_name}\nTotal Budget: {budget}\nCurrent Spend: {current_spend}\nRemaining Timeline: {timeline}\nCost Concerns: {concerns}\n\nProvide:\n1. Budget variance analysis\n2. Cost forecasting\n3. Expense optimization\n4. Financial reporting\n5. Risk assessment\n6. Corrective actions"),
        ("Team Performance Manager", "Optimizes team performance", "Project Manager", "Team Management",
         "Improve team performance for:\n\nTeam: {team_name}\nCurrent Challenges: {challenges}\nPerformance Goals: {goals}\nTeam Dynamics: {dynamics}\n\nInclude:\n1. Performance assessment\n2. Skill development plan\n3. Motivation strategies\n4. Communication improvement\n5. Conflict resolution\n6. Recognition programs"),
        ("Project Closure Specialist", "Manages project closure activities", "Project Manager", "Project Closure",
         "Plan project closure for:\n\nProject: {project_name}\nDeliverables Status: {deliverables}\nStakeholder Satisfaction: {satisfaction}\nLessons Learned: {lessons}\n\nProvide:\n1. Closure checklist\n2. Final deliverable review\n3. Stakeholder sign-off\n4. Documentation handover\n5. Team transition plan\n6. Post-project evaluation"),
        ("Vendor Management Coordinator", "Manages vendor relationships", "Project Manager", "Vendor Management",
         "Manage vendors for:\n\nProject: {project_name}\nVendor Services: {services}\nContract Terms: {terms}\nPerformance Issues: {issues}\n\nInclude:\n1. Vendor evaluation criteria\n2. Contract management\n3. Performance monitoring\n4. Relationship management\n5. Issue resolution\n6. Payment processing"),
        ("Timeline and Milestone Tracker", "Tracks project progress and milestones", "Project Manager", "Progress Tracking",
         "Track progress for:\n\nProject: {project_name}\nCurrent Phase: {phase}\nUpcoming Milestones: {milestones}\nProgress Concerns: {concerns}\n\nProvide:\n1. Progress dashboard\n2. Milestone analysis\n3. Schedule variance\n4. Critical path assessment\n5. Recovery planning\n6. Stakeholder updates"),
        ("Meeting Facilitator", "Facilitates effective project meetings", "Project Manager", "Meeting Management",
         "Plan meeting for:\n\nMeeting Purpose: {purpose}\nAttendees: {attendees}\nDuration: {duration}\nKey Decisions Needed: {decisions}\n\nInclude:\n1. Meeting agenda\n2. Pre-meeting preparation\n3. Facilitation techniques\n4. Decision-making process\n5. Action item tracking\n6. Follow-up procedures"),
        ("Project Documentation Manager", "Manages project documentation", "Project Manager", "Documentation",
         "Organize documentation for:\n\nProject: {project_name}\nDocument Types: {doc_types}\nAudience: {audience}\nCompliance Requirements: {compliance}\n\nProvide:\n1. Documentation strategy\n2. Template library\n3. Version control\n4. Access management\n5. Review processes\n6. Archive procedures"),
        ("Crisis Management Coordinator", "Manages project crises", "Project Manager", "Crisis Management",
         "Handle crisis for:\n\nProject: {project_name}\nCrisis Description: {crisis}\nImpact Assessment: {impact}\nUrgency Level: {urgency}\n\nProvide:\n1. Crisis response plan\n2. Stakeholder communication\n3. Resource mobilization\n4. Risk mitigation\n5. Recovery strategy\n6. Lessons learned"),
        ("Solution Architecture Designer", "Designs comprehensive solution architectures", "Architect", "Solution Design",
         "Design solution architecture for:\n\nBusiness Problem: {problem}\nFunctional Requirements: {functional_req}\nNon-functional Requirements: {nonfunctional_req}\nConstraints: {constraints}\nIntegration Needs: {integrations}\n\nProvide:\n1. High-level architecture diagram\n2. Component specifications\n3. Technology stack recommendations\n4. Integration patterns\n5. Scalability considerations\n6. Security architecture"),
        ("Enterprise Integration Architect", "Designs enterprise integration solutions", "Architect", "Integration",
         "Design integration architecture for:\n\nSystems to Integrate: {systems}\nData Flow Requirements: {data_flow}\nPerformance Requirements: {performance}\nSecurity Requirements: {security}\n\nInclude:\n1. Integration patterns\n2. API design strategy\n3. Data transformation\n4. Error handling\n5. Monitoring and logging\n6. Governance framework"),
        ("Cloud Architecture Consultant", "Designs cloud-native architectures", "Architect", "Cloud Architecture",
         "Design cloud architecture for:\n\nApplication: {application}\nCloud Provider: {provider}\nScalability Needs: {scalability}\nCompliance Requirements: {compliance}\nBudget Constraints: {budget}\n\nProvide:\n1. Cloud service selection\n2. Architecture patterns\n3. Cost optimization\n4. Security design\n5. Disaster recovery\n6. Migration strategy"),
        ("Security Architecture Specialist", "Designs secure system architectures", "Architect", "Security",
         "Design security architecture for:\n\nSystem: {system_name}\nSecurity Requirements: {security_req}\nCompliance Standards: {compliance}\nThreat Landscape: {threats}\n\nInclude:\n1. Security controls framework\n2. Identity and access management\n3. Data protection strategy\n4. Network security design\n5. Monitoring and incident response\n6. Compliance mapping"),
        ("Data Architecture Designer", "Designs enterprise data architectures", "Architect", "Data Architecture",
         "Design data architecture for:\n\nBusiness Requirements: {requirements}\nData Sources: {sources}\nData Volume: {volume}\nAnalytics Needs: {analytics}\nGovernance Requirements: {governance}\n\nProvide:\n1. Data model design\n2. Storage strategy\n3. Data pipeline architecture\n4. Governance framework\n5. Quality management\n6. Analytics platform"),
        ("Microservices Architecture Expert", "Designs microservices ecosystems", "Architect", "Microservices",
         "Design microservices architecture for:\n\nDomain: {domain}\nBusiness Capabilities: {capabilities}\nScale Requirements: {scale}\nTeam Structure: {teams}\n\nInclude:\n1. Service decomposition\n2. Communication patterns\n3. Data management\n4. Service mesh design\n5. Observability strategy\n6. Deployment architecture"),
        ("Performance Architecture Optimizer", "Optimizes system performance architecture", "Architect", "Performance",
         "Optimize performance architecture for:\n\nSystem: {system_name}\nPerformance Issues: {issues}\nTarget Metrics: {targets}\nUser Load: {load}\nBudget Constraints: {budget}\n\nProvide:\n1. Performance bottleneck analysis\n2. Architecture optimization\n3. Caching strategy\n4. Load balancing design\n5. Database optimization\n6. Monitoring framework"),
        ("API Architecture Designer", "Designs comprehensive API architectures", "Architect", "API Design",
         "Design API architecture for:\n\nBusiness Domain: {domain}\nAPI Consumers: {consumers}\nIntegration Requirements: {integrations}\nSecurity Needs: {security}\nScalability Goals: {scalability}\n\nInclude:\n1. API design patterns\n2. Authentication strategy\n3. Rate limiting and throttling\n4. Versioning strategy\n5. Documentation framework\n6. Monitoring and analytics"),
        ("DevOps Architecture Planner", "Designs DevOps and CI/CD architectures", "Architect", "DevOps",
         "Design DevOps architecture for:\n\nDevelopment Team: {team}\nTechnology Stack: {stack}\nDeployment Environments: {environments}\nQuality Requirements: {quality}\n\nProvide:\n1. CI/CD pipeline design\n2. Infrastructure as code\n3. Monitoring and observability\n4. Security integration\n5. Deployment strategies\n6. Automation framework"),
        ("Mobile Architecture Consultant", "Designs mobile application architectures", "Architect", "Mobile Architecture",
         "Design mobile architecture for:\n\nApp Type: {app_type}\nTarget Platforms: {platforms}\nUser Base: {users}\nPerformance Requirements: {performance}\nSecurity Needs: {security}\n\nInclude:\n1. Architecture patterns\n2. Backend integration\n3. Offline capabilities\n4. Security implementation\n5. Performance optimization\n6. Testing strategy"),
        ("IoT Architecture Designer", "Designs IoT system architectures", "Architect", "IoT",
         "Design IoT architecture for:\n\nUse Case: {use_case}\nDevice Types: {devices}\nData Volume: {data_volume}\nConnectivity: {connectivity}\nSecurity Requirements: {security}\n\nProvide:\n1. Device architecture\n2. Communication protocols\n3. Data processing pipeline\n4. Cloud integration\n5. Security framework\n6. Management platform"),
        ("Blockchain Architecture Specialist", "Designs blockchain-based architectures", "Architect", "Blockchain",
         "Design blockchain architecture for:\n\nUse Case: {use_case}\nBlockchain Type: {blockchain_type}\nConsensus Requirements: {consensus}\nIntegration Needs: {integrations}\n\nInclude:\n1. Blockchain platform selection\n2. Smart contract architecture\n3. Integration patterns\n4. Security considerations\n5. Scalability solutions\n6. Governance model"),
        ("Disaster Recovery Architect", "Designs disaster recovery architectures", "Architect", "Disaster Recovery",
         "Design disaster recovery for:\n\nSystems: {systems}\nRTO Requirements: {rto}\nRPO Requirements: {rpo}\nBudget Constraints: {budget}\nCompliance Needs: {compliance}\n\nProvide:\n1. DR strategy and design\n2. Backup and replication\n3. Failover procedures\n4. Testing framework\n5. Recovery automation\n6. Communication plan"),
        ("Legacy Modernization Architect", "Architects legacy system modernization", "Architect", "Modernization",
         "Plan modernization for:\n\nLegacy System: {system}\nBusiness Drivers: {drivers}\nModernization Goals: {goals}\nConstraints: {constraints}\nTimeline: {timeline}\n\nInclude:\n1. Current state assessment\n2. Target architecture\n3. Migration strategy\n4. Risk mitigation\n5. Phased approach\n6. Success metrics"),
        ("Compliance Architecture Designer", "Designs compliance-focused architectures", "Architect", "Compliance",
         "Design compliant architecture for:\n\nRegulatory Requirements: {regulations}\nBusiness Domain: {domain}\nData Sensitivity: {sensitivity}\nAudit Requirements: {audit}\n\nProvide:\n1. Compliance framework\n2. Control implementation\n3. Data governance\n4. Audit trail design\n5. Monitoring strategy\n6. Reporting mechanisms"),
        ("Requirements Analysis Expert", "Analyzes and documents business requirements", "Business Analyst", "Requirements",
         "Analyze requirements for:\n\nProject: {project_name}\nStakeholders: {stakeholders}\nBusiness Objectives: {objectives}\nCurrent Challenges: {challenges}\n\nProvide:\n1. Functional requirements\n2. Non-functional requirements\n3. User stories\n4. Acceptance criteria\n5. Requirements traceability\n6. Impact analysis"),
        ("Process Optimization Consultant", "Optimizes business processes", "Business Analyst", "Process Improvement",
         "Optimize process for:\n\nProcess Name: {process_name}\nCurrent Issues: {issues}\nStakeholders: {stakeholders}\nSuccess Metrics: {metrics}\n\nInclude:\n1. Current state analysis\n2. Process mapping\n3. Bottleneck identification\n4. Optimization recommendations\n5. Implementation roadmap\n6. Change management"),
        ("Data Analysis Specialist", "Performs comprehensive data analysis", "Business Analyst", "Data Analysis",
         "Analyze data for:\n\nBusiness Question: {question}\nData Sources: {sources}\nAnalysis Scope: {scope}\nDecision Context: {context}\n\nProvide:\n1. Data exploration\n2. Statistical analysis\n3. Trend identification\n4. Insights and findings\n5. Recommendations\n6. Visualization strategy"),
        ("Stakeholder Requirements Gatherer", "Gathers and manages stakeholder requirements", "Business Analyst", "Stakeholder Management",
         "Gather requirements from:\n\nProject: {project_name}\nStakeholder Groups: {groups}\nBusiness Domain: {domain}\nComplexity Level: {complexity}\n\nInclude:\n1. Stakeholder analysis\n2. Interview planning\n3. Requirements elicitation\n4. Conflict resolution\n5. Prioritization framework\n6. Communication strategy"),
        ("Business Case Developer", "Develops compelling business cases", "Business Analyst", "Business Case",
         "Develop business case for:\n\nInitiative: {initiative}\nInvestment Required: {investment}\nExpected Benefits: {benefits}\nRisks: {risks}\nTimeline: {timeline}\n\nProvide:\n1. Executive summary\n2. Cost-benefit analysis\n3. ROI calculations\n4. Risk assessment\n5. Implementation plan\n6. Success metrics"),
        ("Gap Analysis Expert", "Conducts comprehensive gap analyses", "Business Analyst", "Gap Analysis",
         "Perform gap analysis for:\n\nCurrent State: {current_state}\nDesired State: {desired_state}\nBusiness Area: {area}\nConstraints: {constraints}\n\nInclude:\n1. Current state assessment\n2. Future state definition\n3. Gap identification\n4. Impact analysis\n5. Bridging strategy\n6. Implementation roadmap"),
        ("User Experience Analyst", "Analyzes and improves user experiences", "Business Analyst", "User Experience",
         "Analyze user experience for:\n\nSystem/Process: {system}\nUser Groups: {users}\nCurrent Pain Points: {pain_points}\nBusiness Goals: {goals}\n\nProvide:\n1. User journey mapping\n2. Pain point analysis\n3. Improvement opportunities\n4. Solution recommendations\n5. Success metrics\n6. Implementation approach"),
        ("Competitive Analysis Researcher", "Conducts competitive market analysis", "Business Analyst", "Market Analysis",
         "Analyze competition for:\n\nProduct/Service: {product}\nMarket Segment: {segment}\nKey Competitors: {competitors}\nAnalysis Focus: {focus}\n\nInclude:\n1. Competitive landscape\n2. Feature comparison\n3. Pricing analysis\n4. Market positioning\n5. Opportunities and threats\n6. Strategic recommendations"),
        ("Workflow Designer", "Designs efficient business workflows", "Business Analyst", "Workflow Design",
         "Design workflow for:\n\nBusiness Process: {process}\nStakeholders: {stakeholders}\nComplexity Level: {complexity}\nAutomation Goals: {automation}\n\nProvide:\n1. Workflow diagram\n2. Role definitions\n3. Decision points\n4. Exception handling\n5. Automation opportunities\n6. Performance metrics"),
        ("Metrics and KPI Designer", "Designs business metrics and KPIs", "Business Analyst", "Metrics",
         "Design metrics for:\n\nBusiness Objective: {objective}\nStakeholders: {stakeholders}\nData Availability: {data}\nReporting Frequency: {frequency}\n\nInclude:\n1. KPI framework\n2. Metric definitions\n3. Data sources\n4. Calculation methods\n5. Reporting strategy\n6. Action triggers"),
        ("Strategic Planning Consultant", "Develops strategic plans and roadmaps", "Consultant", "Strategy",
         "Develop strategic plan for:\n\nOrganization: {organization}\nIndustry: {industry}\nCurrent Challenges: {challenges}\nGrowth Objectives: {objectives}\nTimeframe: {timeframe}\n\nProvide:\n1. Situation analysis\n2. Strategic options\n3. Recommended strategy\n4. Implementation roadmap\n5. Success metrics\n6. Risk mitigation"),
        ("Digital Transformation Advisor", "Guides digital transformation initiatives", "Consultant", "Digital Transformation",
         "Plan digital transformation for:\n\nOrganization: {organization}\nCurrent State: {current_state}\nTransformation Goals: {goals}\nBudget: {budget}\nTimeline: {timeline}\n\nInclude:\n1. Digital maturity assessment\n2. Transformation strategy\n3. Technology roadmap\n4. Change management\n5. Implementation phases\n6. Success measurement"),
        ("Management Consulting Expert", "Provides management consulting solutions", "Consultant", "Management",
         "Provide consulting for:\n\nClient: {client}\nBusiness Challenge: {challenge}\nIndustry Context: {industry}\nStakeholders: {stakeholders}\nSuccess Criteria: {criteria}\n\nDeliver:\n1. Problem diagnosis\n2. Root cause analysis\n3. Solution alternatives\n4. Recommendation\n5. Implementation plan\n6. Change management"),
        ("Organizational Change Manager", "Manages organizational change initiatives", "Consultant", "Change Management",
         "Manage change for:\n\nOrganization: {organization}\nChange Initiative: {initiative}\nImpacted Groups: {groups}\nResistance Factors: {resistance}\n\nProvide:\n1. Change impact assessment\n2. Stakeholder analysis\n3. Communication strategy\n4. Training plan\n5. Resistance management\n6. Success measurement"),
        ("Business Process Reengineering", "Reengineers business processes", "Consultant", "Process Reengineering",
         "Reengineer process for:\n\nProcess: {process_name}\nCurrent Performance: {performance}\nTarget Improvements: {targets}\nConstraints: {constraints}\n\nInclude:\n1. Process analysis\n2. Reengineering approach\n3. New process design\n4. Technology enablers\n5. Implementation strategy\n6. Performance metrics"),
        ("Client Presentation Designer", "Creates compelling client presentations", "Consultant", "Presentations",
         "Create presentation for:\n\nClient: {client}\nPresentation Purpose: {purpose}\nAudience: {audience}\nKey Messages: {messages}\nTime Allocation: {duration}\n\nInclude:\n1. Executive summary\n2. Situation analysis\n3. Recommendations\n4. Implementation approach\n5. Expected outcomes\n6. Next steps"),
        ("Market Entry Strategist", "Develops market entry strategies", "Consultant", "Market Entry",
         "Develop market entry strategy for:\n\nCompany: {company}\nTarget Market: {market}\nProduct/Service: {offering}\nCompetitive Landscape: {competition}\nResources: {resources}\n\nProvide:\n1. Market analysis\n2. Entry strategy options\n3. Go-to-market plan\n4. Resource requirements\n5. Risk assessment\n6. Success metrics"),
        ("Performance Improvement Consultant", "Improves organizational performance", "Consultant", "Performance",
         "Improve performance for:\n\nOrganization: {organization}\nPerformance Issues: {issues}\nCurrent Metrics: {metrics}\nImprovement Goals: {goals}\n\nInclude:\n1. Performance diagnosis\n2. Root cause analysis\n3. Improvement opportunities\n4. Action plan\n5. Implementation support\n6. Monitoring framework"),
        ("Due Diligence Analyst", "Conducts comprehensive due diligence", "Consultant", "Due Diligence",
         "Conduct due diligence for:\n\nTransaction: {transaction}\nTarget Company: {target}\nFocus Areas: {focus}\nTimeline: {timeline}\nStakeholders: {stakeholders}\n\nProvide:\n1. Due diligence plan\n2. Information requests\n3. Analysis framework\n4. Risk assessment\n5. Findings summary\n6. Recommendations"),
        ("Innovation Strategy Consultant", "Develops innovation strategies", "Consultant", "Innovation",
         "Develop innovation strategy for:\n\nOrganization: {organization}\nInnovation Goals: {goals}\nCurrent Capabilities: {capabilities}\nMarket Opportunities: {opportunities}\n\nInclude:\n1. Innovation assessment\n2. Opportunity identification\n3. Innovation framework\n4. Implementation roadmap\n5. Governance model\n6. Success metrics"),
        ("Market Research Analyst", "Conducts comprehensive market research", "Researcher", "Market Research",
         "Conduct market research for:\n\nResearch Topic: {topic}\nTarget Market: {market}\nResearch Objectives: {objectives}\nMethodology Preference: {methodology}\nTimeline: {timeline}\n\nProvide:\n1. Research design\n2. Data collection plan\n3. Analysis framework\n4. Key findings\n5. Market insights\n6. Strategic implications"),
        ("Industry Analysis Expert", "Performs detailed industry analysis", "Researcher", "Industry Analysis",
         "Analyze industry:\n\nIndustry: {industry}\nAnalysis Scope: {scope}\nKey Questions: {questions}\nStakeholder Interest: {stakeholders}\n\nInclude:\n1. Industry overview\n2. Market dynamics\n3. Competitive landscape\n4. Trends and drivers\n5. Future outlook\n6. Strategic recommendations"),
        ("Consumer Behavior Researcher", "Studies consumer behavior patterns", "Researcher", "Consumer Research",
         "Research consumer behavior for:\n\nProduct/Service: {product}\nTarget Demographics: {demographics}\nBehavior Focus: {behavior}\nResearch Methods: {methods}\n\nProvide:\n1. Research methodology\n2. Data collection approach\n3. Behavioral analysis\n4. Consumer insights\n5. Implications for business\n6. Recommendations"),
        ("Trend Analysis Specialist", "Identifies and analyzes market trends", "Researcher", "Trend Analysis",
         "Analyze trends for:\n\nIndustry/Market: {market}\nTrend Categories: {categories}\nTime Horizon: {horizon}\nBusiness Impact: {impact}\n\nInclude:\n1. Trend identification\n2. Trend analysis\n3. Impact assessment\n4. Future projections\n5. Business implications\n6. Strategic responses"),
        ("Competitive Intelligence Researcher", "Gathers competitive intelligence", "Researcher", "Competitive Intelligence",
         "Research competitive intelligence for:\n\nCompany: {company}\nCompetitors: {competitors}\nIntelligence Focus: {focus}\nDecision Context: {context}\n\nProvide:\n1. Intelligence framework\n2. Data collection strategy\n3. Competitive analysis\n4. Strategic insights\n5. Threat assessment\n6. Opportunity identification")
    ]

    migrated = []
    for title, description, persona, use_case, prompt_text in legacy:
        migrated.append({
            "title": title,
            "persona": persona,
            "use_case": use_case,
            "category": map_category(persona),
            "platform": "Claude Sonnet 4.5",
            "template": to_new_template(prompt_text),
            "description": description,
            "tags": make_tags(persona, use_case),
        })

    return migrated

if __name__ == '__main__':
    # Change to src directory to access database
    os.chdir(os.path.dirname(__file__))
    load_expanded_prompts()
