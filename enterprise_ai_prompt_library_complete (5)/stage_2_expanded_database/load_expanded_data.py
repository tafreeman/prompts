import sqlite3
import json

def load_expanded_prompts():
    """Load 70 comprehensive enterprise prompts into the database"""
    
    conn = sqlite3.connect('prompt_library.db')
    c = conn.cursor()
    
    # Clear existing data
    c.execute("DELETE FROM prompts")
    
    # Expanded prompt collection (70 prompts)
    expanded_prompts = [
        # DEVELOPER PERSONA (15 prompts)
        ("Code Generation Assistant", "Generates clean, efficient code based on requirements", "Developer", "Code Generation", 
         "Generate {language} code for the following requirements:\n\nFunctionality: {functionality}\nInput: {input_format}\nOutput: {output_format}\nConstraints: {constraints}\n\nPlease provide:\n1. Clean, well-commented code\n2. Error handling\n3. Unit tests\n4. Documentation\n5. Performance considerations", 
         '["language", "functionality", "input_format", "output_format", "constraints"]'),
        
        ("API Design Consultant", "Creates RESTful API specifications", "Developer", "API Design", 
         "Design a RESTful API for {service_name} with the following requirements:\n\nCore Functionality: {core_features}\nData Models: {data_models}\nAuthentication: {auth_method}\nRate Limiting: {rate_limits}\n\nProvide:\n1. Endpoint specifications\n2. Request/Response schemas\n3. Error handling\n4. Security considerations\n5. Documentation structure", 
         '["service_name", "core_features", "data_models", "auth_method", "rate_limits"]'),
        
        ("Database Schema Designer", "Designs optimized database schemas", "Developer", "Database Design", 
         "Design a database schema for {application_name}:\n\nBusiness Requirements: {requirements}\nExpected Scale: {scale}\nPerformance Needs: {performance}\nCompliance: {compliance}\n\nInclude:\n1. Entity-Relationship diagram\n2. Table structures with constraints\n3. Indexing strategy\n4. Normalization analysis\n5. Migration scripts", 
         '["application_name", "requirements", "scale", "performance", "compliance"]'),
        
        ("Code Review Expert", "Provides comprehensive code reviews", "Developer", "Code Quality", 
         "Review the following {language} code for:\n\nCode: {code_snippet}\nContext: {context}\nCritical Areas: {focus_areas}\n\nAnalyze:\n1. Code quality and best practices\n2. Security vulnerabilities\n3. Performance bottlenecks\n4. Maintainability issues\n5. Testing coverage\n6. Documentation quality\n\nProvide specific recommendations with examples.", 
         '["language", "code_snippet", "context", "focus_areas"]'),
        
        ("Legacy System Modernization", "Plans legacy system upgrades", "Developer", "Modernization", 
         "Create a modernization plan for:\n\nLegacy System: {system_name}\nCurrent Technology: {current_tech}\nTarget Technology: {target_tech}\nBusiness Constraints: {constraints}\nTimeline: {timeline}\n\nProvide:\n1. Migration strategy\n2. Risk assessment\n3. Phased approach\n4. Resource requirements\n5. Testing strategy\n6. Rollback plans", 
         '["system_name", "current_tech", "target_tech", "constraints", "timeline"]'),
        
        ("DevOps Pipeline Architect", "Designs CI/CD pipelines", "Developer", "DevOps", 
         "Design a CI/CD pipeline for {project_name}:\n\nTechnology Stack: {tech_stack}\nDeployment Environment: {environment}\nTesting Requirements: {testing}\nSecurity Requirements: {security}\n\nInclude:\n1. Pipeline stages\n2. Automated testing strategy\n3. Deployment automation\n4. Monitoring and alerting\n5. Security scanning\n6. Rollback mechanisms", 
         '["project_name", "tech_stack", "environment", "testing", "security"]'),
        
        ("Performance Optimization Specialist", "Optimizes application performance", "Developer", "Performance", 
         "Analyze and optimize performance for:\n\nApplication: {app_name}\nCurrent Issues: {performance_issues}\nTarget Metrics: {target_metrics}\nConstraints: {constraints}\n\nProvide:\n1. Performance bottleneck analysis\n2. Optimization recommendations\n3. Caching strategies\n4. Database optimization\n5. Code-level improvements\n6. Monitoring setup", 
         '["app_name", "performance_issues", "target_metrics", "constraints"]'),
        
        ("Security Code Auditor", "Conducts security code audits", "Developer", "Security", 
         "Perform a security audit on:\n\nApplication: {app_name}\nCode Base: {code_description}\nSecurity Framework: {security_framework}\nCompliance Requirements: {compliance}\n\nAnalyze:\n1. Authentication and authorization\n2. Input validation\n3. Data encryption\n4. SQL injection vulnerabilities\n5. XSS vulnerabilities\n6. OWASP Top 10 compliance", 
         '["app_name", "code_description", "security_framework", "compliance"]'),
        
        ("Microservices Architect", "Designs microservices architectures", "Developer", "Architecture", 
         "Design a microservices architecture for:\n\nApplication: {app_name}\nBusiness Domains: {domains}\nScale Requirements: {scale}\nTechnology Preferences: {tech_prefs}\n\nProvide:\n1. Service decomposition strategy\n2. Inter-service communication\n3. Data management approach\n4. Service discovery\n5. Monitoring and observability\n6. Deployment strategy", 
         '["app_name", "domains", "scale", "tech_prefs"]'),
        
        ("Test Automation Engineer", "Creates comprehensive test strategies", "Developer", "Testing", 
         "Design a test automation strategy for:\n\nApplication: {app_name}\nTesting Scope: {scope}\nTechnology Stack: {tech_stack}\nQuality Goals: {quality_goals}\n\nInclude:\n1. Test pyramid strategy\n2. Unit testing approach\n3. Integration testing\n4. End-to-end testing\n5. Performance testing\n6. Test data management", 
         '["app_name", "scope", "tech_stack", "quality_goals"]'),
        
        ("Cloud Migration Specialist", "Plans cloud migration strategies", "Developer", "Cloud Migration", 
         "Create a cloud migration plan for:\n\nApplication: {app_name}\nCurrent Infrastructure: {current_infra}\nTarget Cloud: {target_cloud}\nBusiness Requirements: {requirements}\n\nProvide:\n1. Migration assessment\n2. Cloud architecture design\n3. Migration phases\n4. Cost optimization\n5. Security considerations\n6. Performance validation", 
         '["app_name", "current_infra", "target_cloud", "requirements"]'),
        
        ("Documentation Generator", "Creates technical documentation", "Developer", "Documentation", 
         "Generate comprehensive documentation for:\n\nProject: {project_name}\nAudience: {audience}\nDocumentation Type: {doc_type}\nTechnical Details: {tech_details}\n\nInclude:\n1. Architecture overview\n2. API documentation\n3. Setup instructions\n4. Usage examples\n5. Troubleshooting guide\n6. Contributing guidelines", 
         '["project_name", "audience", "doc_type", "tech_details"]'),
        
        ("Mobile App Developer", "Guides mobile application development", "Developer", "Mobile Development", 
         "Plan mobile app development for:\n\nApp Concept: {app_concept}\nTarget Platforms: {platforms}\nKey Features: {features}\nUser Experience Goals: {ux_goals}\n\nProvide:\n1. Technical architecture\n2. Platform-specific considerations\n3. Performance optimization\n4. Security implementation\n5. Testing strategy\n6. Deployment process", 
         '["app_concept", "platforms", "features", "ux_goals"]'),
        
        ("Data Pipeline Engineer", "Designs data processing pipelines", "Developer", "Data Engineering", 
         "Design a data pipeline for:\n\nData Sources: {data_sources}\nProcessing Requirements: {processing}\nTarget Systems: {targets}\nVolume and Velocity: {scale}\n\nInclude:\n1. Pipeline architecture\n2. Data transformation logic\n3. Error handling and recovery\n4. Monitoring and alerting\n5. Scalability considerations\n6. Data quality validation", 
         '["data_sources", "processing", "targets", "scale"]'),
        
        ("Frontend Architecture Consultant", "Designs frontend architectures", "Developer", "Frontend", 
         "Design frontend architecture for:\n\nApplication: {app_name}\nUser Requirements: {user_requirements}\nTechnology Stack: {tech_stack}\nPerformance Goals: {performance}\n\nProvide:\n1. Component architecture\n2. State management strategy\n3. Routing and navigation\n4. Performance optimization\n5. Accessibility compliance\n6. Testing approach", 
         '["app_name", "user_requirements", "tech_stack", "performance"]'),
        
        # PROJECT MANAGER PERSONA (15 prompts)
        ("Project Charter Creator", "Develops comprehensive project charters", "Project Manager", "Planning", 
         "Create a project charter for:\n\nProject Name: {project_name}\nBusiness Objective: {objective}\nKey Stakeholders: {stakeholders}\nBudget Range: {budget}\nTimeline: {timeline}\n\nInclude:\n1. Executive summary\n2. Scope and deliverables\n3. Success criteria\n4. Resource requirements\n5. Risk assessment\n6. Communication plan", 
         '["project_name", "objective", "stakeholders", "budget", "timeline"]'),
        
        ("Agile Sprint Planner", "Plans and manages agile sprints", "Project Manager", "Agile", 
         "Plan sprint for:\n\nProject: {project_name}\nSprint Duration: {duration}\nTeam Capacity: {capacity}\nPriority Features: {features}\nDefinition of Done: {dod}\n\nProvide:\n1. Sprint goal\n2. User story breakdown\n3. Task estimation\n4. Capacity planning\n5. Risk mitigation\n6. Success metrics", 
         '["project_name", "duration", "capacity", "features", "dod"]'),
        
        ("Risk Management Analyst", "Identifies and manages project risks", "Project Manager", "Risk Management", 
         "Analyze risks for:\n\nProject: {project_name}\nProject Phase: {phase}\nKey Concerns: {concerns}\nStakeholder Impact: {impact}\n\nProvide:\n1. Risk identification matrix\n2. Probability and impact assessment\n3. Risk mitigation strategies\n4. Contingency plans\n5. Monitoring procedures\n6. Escalation protocols", 
         '["project_name", "phase", "concerns", "impact"]'),
        
        ("Stakeholder Communication Manager", "Manages stakeholder communications", "Project Manager", "Communication", 
         "Develop communication strategy for:\n\nProject: {project_name}\nStakeholders: {stakeholders}\nProject Phase: {phase}\nCommunication Challenges: {challenges}\n\nInclude:\n1. Stakeholder analysis\n2. Communication matrix\n3. Meeting schedules\n4. Reporting templates\n5. Escalation procedures\n6. Feedback mechanisms", 
         '["project_name", "stakeholders", "phase", "challenges"]'),
        
        ("Resource Allocation Optimizer", "Optimizes project resource allocation", "Project Manager", "Resource Management", 
         "Optimize resources for:\n\nProject: {project_name}\nAvailable Resources: {resources}\nProject Constraints: {constraints}\nPriority Areas: {priorities}\n\nProvide:\n1. Resource allocation matrix\n2. Skill gap analysis\n3. Workload balancing\n4. Timeline optimization\n5. Cost efficiency measures\n6. Contingency planning", 
         '["project_name", "resources", "constraints", "priorities"]'),
        
        ("Quality Assurance Planner", "Develops QA strategies and plans", "Project Manager", "Quality Assurance", 
         "Create QA plan for:\n\nProject: {project_name}\nQuality Standards: {standards}\nDeliverables: {deliverables}\nTesting Requirements: {testing}\n\nInclude:\n1. Quality objectives\n2. QA processes and procedures\n3. Testing strategy\n4. Quality metrics\n5. Review and approval workflows\n6. Continuous improvement", 
         '["project_name", "standards", "deliverables", "testing"]'),
        
        ("Change Management Coordinator", "Manages project changes effectively", "Project Manager", "Change Management", 
         "Manage change for:\n\nProject: {project_name}\nProposed Changes: {changes}\nImpact Assessment: {impact}\nStakeholder Concerns: {concerns}\n\nProvide:\n1. Change impact analysis\n2. Approval workflow\n3. Communication strategy\n4. Implementation plan\n5. Risk mitigation\n6. Success measurement", 
         '["project_name", "changes", "impact", "concerns"]'),
        
        ("Budget and Cost Controller", "Manages project budgets and costs", "Project Manager", "Financial Management", 
         "Manage budget for:\n\nProject: {project_name}\nTotal Budget: {budget}\nCurrent Spend: {current_spend}\nRemaining Timeline: {timeline}\nCost Concerns: {concerns}\n\nProvide:\n1. Budget variance analysis\n2. Cost forecasting\n3. Expense optimization\n4. Financial reporting\n5. Risk assessment\n6. Corrective actions", 
         '["project_name", "budget", "current_spend", "timeline", "concerns"]'),
        
        ("Team Performance Manager", "Optimizes team performance", "Project Manager", "Team Management", 
         "Improve team performance for:\n\nTeam: {team_name}\nCurrent Challenges: {challenges}\nPerformance Goals: {goals}\nTeam Dynamics: {dynamics}\n\nInclude:\n1. Performance assessment\n2. Skill development plan\n3. Motivation strategies\n4. Communication improvement\n5. Conflict resolution\n6. Recognition programs", 
         '["team_name", "challenges", "goals", "dynamics"]'),
        
        ("Project Closure Specialist", "Manages project closure activities", "Project Manager", "Project Closure", 
         "Plan project closure for:\n\nProject: {project_name}\nDeliverables Status: {deliverables}\nStakeholder Satisfaction: {satisfaction}\nLessons Learned: {lessons}\n\nProvide:\n1. Closure checklist\n2. Final deliverable review\n3. Stakeholder sign-off\n4. Documentation handover\n5. Team transition plan\n6. Post-project evaluation", 
         '["project_name", "deliverables", "satisfaction", "lessons"]'),
        
        ("Vendor Management Coordinator", "Manages vendor relationships", "Project Manager", "Vendor Management", 
         "Manage vendors for:\n\nProject: {project_name}\nVendor Services: {services}\nContract Terms: {terms}\nPerformance Issues: {issues}\n\nInclude:\n1. Vendor evaluation criteria\n2. Contract management\n3. Performance monitoring\n4. Relationship management\n5. Issue resolution\n6. Payment processing", 
         '["project_name", "services", "terms", "issues"]'),
        
        ("Timeline and Milestone Tracker", "Tracks project progress and milestones", "Project Manager", "Progress Tracking", 
         "Track progress for:\n\nProject: {project_name}\nCurrent Phase: {phase}\nUpcoming Milestones: {milestones}\nProgress Concerns: {concerns}\n\nProvide:\n1. Progress dashboard\n2. Milestone analysis\n3. Schedule variance\n4. Critical path assessment\n5. Recovery planning\n6. Stakeholder updates", 
         '["project_name", "phase", "milestones", "concerns"]'),
        
        ("Meeting Facilitator", "Facilitates effective project meetings", "Project Manager", "Meeting Management", 
         "Plan meeting for:\n\nMeeting Purpose: {purpose}\nAttendees: {attendees}\nDuration: {duration}\nKey Decisions Needed: {decisions}\n\nInclude:\n1. Meeting agenda\n2. Pre-meeting preparation\n3. Facilitation techniques\n4. Decision-making process\n5. Action item tracking\n6. Follow-up procedures", 
         '["purpose", "attendees", "duration", "decisions"]'),
        
        ("Project Documentation Manager", "Manages project documentation", "Project Manager", "Documentation", 
         "Organize documentation for:\n\nProject: {project_name}\nDocument Types: {doc_types}\nAudience: {audience}\nCompliance Requirements: {compliance}\n\nProvide:\n1. Documentation strategy\n2. Template library\n3. Version control\n4. Access management\n5. Review processes\n6. Archive procedures", 
         '["project_name", "doc_types", "audience", "compliance"]'),
        
        ("Crisis Management Coordinator", "Manages project crises", "Project Manager", "Crisis Management", 
         "Handle crisis for:\n\nProject: {project_name}\nCrisis Description: {crisis}\nImpact Assessment: {impact}\nUrgency Level: {urgency}\n\nProvide:\n1. Crisis response plan\n2. Stakeholder communication\n3. Resource mobilization\n4. Risk mitigation\n5. Recovery strategy\n6. Lessons learned", 
         '["project_name", "crisis", "impact", "urgency"]'),
        
        # ARCHITECT PERSONA (15 prompts)
        ("Solution Architecture Designer", "Designs comprehensive solution architectures", "Architect", "Solution Design", 
         "Design solution architecture for:\n\nBusiness Problem: {problem}\nFunctional Requirements: {functional_req}\nNon-functional Requirements: {nonfunctional_req}\nConstraints: {constraints}\nIntegration Needs: {integrations}\n\nProvide:\n1. High-level architecture diagram\n2. Component specifications\n3. Technology stack recommendations\n4. Integration patterns\n5. Scalability considerations\n6. Security architecture", 
         '["problem", "functional_req", "nonfunctional_req", "constraints", "integrations"]'),
        
        ("Enterprise Integration Architect", "Designs enterprise integration solutions", "Architect", "Integration", 
         "Design integration architecture for:\n\nSystems to Integrate: {systems}\nData Flow Requirements: {data_flow}\nPerformance Requirements: {performance}\nSecurity Requirements: {security}\n\nInclude:\n1. Integration patterns\n2. API design strategy\n3. Data transformation\n4. Error handling\n5. Monitoring and logging\n6. Governance framework", 
         '["systems", "data_flow", "performance", "security"]'),
        
        ("Cloud Architecture Consultant", "Designs cloud-native architectures", "Architect", "Cloud Architecture", 
         "Design cloud architecture for:\n\nApplication: {application}\nCloud Provider: {provider}\nScalability Needs: {scalability}\nCompliance Requirements: {compliance}\nBudget Constraints: {budget}\n\nProvide:\n1. Cloud service selection\n2. Architecture patterns\n3. Cost optimization\n4. Security design\n5. Disaster recovery\n6. Migration strategy", 
         '["application", "provider", "scalability", "compliance", "budget"]'),
        
        ("Security Architecture Specialist", "Designs secure system architectures", "Architect", "Security", 
         "Design security architecture for:\n\nSystem: {system_name}\nSecurity Requirements: {security_req}\nCompliance Standards: {compliance}\nThreat Landscape: {threats}\n\nInclude:\n1. Security controls framework\n2. Identity and access management\n3. Data protection strategy\n4. Network security design\n5. Monitoring and incident response\n6. Compliance mapping", 
         '["system_name", "security_req", "compliance", "threats"]'),
        
        ("Data Architecture Designer", "Designs enterprise data architectures", "Architect", "Data Architecture", 
         "Design data architecture for:\n\nBusiness Requirements: {requirements}\nData Sources: {sources}\nData Volume: {volume}\nAnalytics Needs: {analytics}\nGovernance Requirements: {governance}\n\nProvide:\n1. Data model design\n2. Storage strategy\n3. Data pipeline architecture\n4. Governance framework\n5. Quality management\n6. Analytics platform", 
         '["requirements", "sources", "volume", "analytics", "governance"]'),
        
        ("Microservices Architecture Expert", "Designs microservices ecosystems", "Architect", "Microservices", 
         "Design microservices architecture for:\n\nDomain: {domain}\nBusiness Capabilities: {capabilities}\nScale Requirements: {scale}\nTeam Structure: {teams}\n\nInclude:\n1. Service decomposition\n2. Communication patterns\n3. Data management\n4. Service mesh design\n5. Observability strategy\n6. Deployment architecture", 
         '["domain", "capabilities", "scale", "teams"]'),
        
        ("Performance Architecture Optimizer", "Optimizes system performance architecture", "Architect", "Performance", 
         "Optimize performance architecture for:\n\nSystem: {system_name}\nPerformance Issues: {issues}\nTarget Metrics: {targets}\nUser Load: {load}\nBudget Constraints: {budget}\n\nProvide:\n1. Performance bottleneck analysis\n2. Architecture optimization\n3. Caching strategy\n4. Load balancing design\n5. Database optimization\n6. Monitoring framework", 
         '["system_name", "issues", "targets", "load", "budget"]'),
        
        ("API Architecture Designer", "Designs comprehensive API architectures", "Architect", "API Design", 
         "Design API architecture for:\n\nBusiness Domain: {domain}\nAPI Consumers: {consumers}\nIntegration Requirements: {integrations}\nSecurity Needs: {security}\nScalability Goals: {scalability}\n\nInclude:\n1. API design patterns\n2. Authentication strategy\n3. Rate limiting and throttling\n4. Versioning strategy\n5. Documentation framework\n6. Monitoring and analytics", 
         '["domain", "consumers", "integrations", "security", "scalability"]'),
        
        ("DevOps Architecture Planner", "Designs DevOps and CI/CD architectures", "Architect", "DevOps", 
         "Design DevOps architecture for:\n\nDevelopment Team: {team}\nTechnology Stack: {stack}\nDeployment Environments: {environments}\nQuality Requirements: {quality}\n\nProvide:\n1. CI/CD pipeline design\n2. Infrastructure as code\n3. Monitoring and observability\n4. Security integration\n5. Deployment strategies\n6. Automation framework", 
         '["team", "stack", "environments", "quality"]'),
        
        ("Mobile Architecture Consultant", "Designs mobile application architectures", "Architect", "Mobile Architecture", 
         "Design mobile architecture for:\n\nApp Type: {app_type}\nTarget Platforms: {platforms}\nUser Base: {users}\nPerformance Requirements: {performance}\nSecurity Needs: {security}\n\nInclude:\n1. Architecture patterns\n2. Backend integration\n3. Offline capabilities\n4. Security implementation\n5. Performance optimization\n6. Testing strategy", 
         '["app_type", "platforms", "users", "performance", "security"]'),
        
        ("IoT Architecture Designer", "Designs IoT system architectures", "Architect", "IoT", 
         "Design IoT architecture for:\n\nUse Case: {use_case}\nDevice Types: {devices}\nData Volume: {data_volume}\nConnectivity: {connectivity}\nSecurity Requirements: {security}\n\nProvide:\n1. Device architecture\n2. Communication protocols\n3. Data processing pipeline\n4. Cloud integration\n5. Security framework\n6. Management platform", 
         '["use_case", "devices", "data_volume", "connectivity", "security"]'),
        
        ("Blockchain Architecture Specialist", "Designs blockchain-based architectures", "Architect", "Blockchain", 
         "Design blockchain architecture for:\n\nUse Case: {use_case}\nBlockchain Type: {blockchain_type}\nConsensus Requirements: {consensus}\nIntegration Needs: {integrations}\n\nInclude:\n1. Blockchain platform selection\n2. Smart contract architecture\n3. Integration patterns\n4. Security considerations\n5. Scalability solutions\n6. Governance model", 
         '["use_case", "blockchain_type", "consensus", "integrations"]'),
        
        ("Disaster Recovery Architect", "Designs disaster recovery architectures", "Architect", "Disaster Recovery", 
         "Design disaster recovery for:\n\nSystems: {systems}\nRTO Requirements: {rto}\nRPO Requirements: {rpo}\nBudget Constraints: {budget}\nCompliance Needs: {compliance}\n\nProvide:\n1. DR strategy and design\n2. Backup and replication\n3. Failover procedures\n4. Testing framework\n5. Recovery automation\n6. Communication plan", 
         '["systems", "rto", "rpo", "budget", "compliance"]'),
        
        ("Legacy Modernization Architect", "Architects legacy system modernization", "Architect", "Modernization", 
         "Plan modernization for:\n\nLegacy System: {system}\nBusiness Drivers: {drivers}\nModernization Goals: {goals}\nConstraints: {constraints}\nTimeline: {timeline}\n\nInclude:\n1. Current state assessment\n2. Target architecture\n3. Migration strategy\n4. Risk mitigation\n5. Phased approach\n6. Success metrics", 
         '["system", "drivers", "goals", "constraints", "timeline"]'),
        
        ("Compliance Architecture Designer", "Designs compliance-focused architectures", "Architect", "Compliance", 
         "Design compliant architecture for:\n\nRegulatory Requirements: {regulations}\nBusiness Domain: {domain}\nData Sensitivity: {sensitivity}\nAudit Requirements: {audit}\n\nProvide:\n1. Compliance framework\n2. Control implementation\n3. Data governance\n4. Audit trail design\n5. Monitoring strategy\n6. Reporting mechanisms", 
         '["regulations", "domain", "sensitivity", "audit"]'),
        
        # BUSINESS ANALYST PERSONA (10 prompts)
        ("Requirements Analysis Expert", "Analyzes and documents business requirements", "Business Analyst", "Requirements", 
         "Analyze requirements for:\n\nProject: {project_name}\nStakeholders: {stakeholders}\nBusiness Objectives: {objectives}\nCurrent Challenges: {challenges}\n\nProvide:\n1. Functional requirements\n2. Non-functional requirements\n3. User stories\n4. Acceptance criteria\n5. Requirements traceability\n6. Impact analysis", 
         '["project_name", "stakeholders", "objectives", "challenges"]'),
        
        ("Process Optimization Consultant", "Optimizes business processes", "Business Analyst", "Process Improvement", 
         "Optimize process for:\n\nProcess Name: {process_name}\nCurrent Issues: {issues}\nStakeholders: {stakeholders}\nSuccess Metrics: {metrics}\n\nInclude:\n1. Current state analysis\n2. Process mapping\n3. Bottleneck identification\n4. Optimization recommendations\n5. Implementation roadmap\n6. Change management", 
         '["process_name", "issues", "stakeholders", "metrics"]'),
        
        ("Data Analysis Specialist", "Performs comprehensive data analysis", "Business Analyst", "Data Analysis", 
         "Analyze data for:\n\nBusiness Question: {question}\nData Sources: {sources}\nAnalysis Scope: {scope}\nDecision Context: {context}\n\nProvide:\n1. Data exploration\n2. Statistical analysis\n3. Trend identification\n4. Insights and findings\n5. Recommendations\n6. Visualization strategy", 
         '["question", "sources", "scope", "context"]'),
        
        ("Stakeholder Requirements Gatherer", "Gathers and manages stakeholder requirements", "Business Analyst", "Stakeholder Management", 
         "Gather requirements from:\n\nProject: {project_name}\nStakeholder Groups: {groups}\nBusiness Domain: {domain}\nComplexity Level: {complexity}\n\nInclude:\n1. Stakeholder analysis\n2. Interview planning\n3. Requirements elicitation\n4. Conflict resolution\n5. Prioritization framework\n6. Communication strategy", 
         '["project_name", "groups", "domain", "complexity"]'),
        
        ("Business Case Developer", "Develops compelling business cases", "Business Analyst", "Business Case", 
         "Develop business case for:\n\nInitiative: {initiative}\nInvestment Required: {investment}\nExpected Benefits: {benefits}\nRisks: {risks}\nTimeline: {timeline}\n\nProvide:\n1. Executive summary\n2. Cost-benefit analysis\n3. ROI calculations\n4. Risk assessment\n5. Implementation plan\n6. Success metrics", 
         '["initiative", "investment", "benefits", "risks", "timeline"]'),
        
        ("Gap Analysis Expert", "Conducts comprehensive gap analyses", "Business Analyst", "Gap Analysis", 
         "Perform gap analysis for:\n\nCurrent State: {current_state}\nDesired State: {desired_state}\nBusiness Area: {area}\nConstraints: {constraints}\n\nInclude:\n1. Current state assessment\n2. Future state definition\n3. Gap identification\n4. Impact analysis\n5. Bridging strategy\n6. Implementation roadmap", 
         '["current_state", "desired_state", "area", "constraints"]'),
        
        ("User Experience Analyst", "Analyzes and improves user experiences", "Business Analyst", "User Experience", 
         "Analyze user experience for:\n\nSystem/Process: {system}\nUser Groups: {users}\nCurrent Pain Points: {pain_points}\nBusiness Goals: {goals}\n\nProvide:\n1. User journey mapping\n2. Pain point analysis\n3. Improvement opportunities\n4. Solution recommendations\n5. Success metrics\n6. Implementation approach", 
         '["system", "users", "pain_points", "goals"]'),
        
        ("Competitive Analysis Researcher", "Conducts competitive market analysis", "Business Analyst", "Market Analysis", 
         "Analyze competition for:\n\nProduct/Service: {product}\nMarket Segment: {segment}\nKey Competitors: {competitors}\nAnalysis Focus: {focus}\n\nInclude:\n1. Competitive landscape\n2. Feature comparison\n3. Pricing analysis\n4. Market positioning\n5. Opportunities and threats\n6. Strategic recommendations", 
         '["product", "segment", "competitors", "focus"]'),
        
        ("Workflow Designer", "Designs efficient business workflows", "Business Analyst", "Workflow Design", 
         "Design workflow for:\n\nBusiness Process: {process}\nStakeholders: {stakeholders}\nComplexity Level: {complexity}\nAutomation Goals: {automation}\n\nProvide:\n1. Workflow diagram\n2. Role definitions\n3. Decision points\n4. Exception handling\n5. Automation opportunities\n6. Performance metrics", 
         '["process", "stakeholders", "complexity", "automation"]'),
        
        ("Metrics and KPI Designer", "Designs business metrics and KPIs", "Business Analyst", "Metrics", 
         "Design metrics for:\n\nBusiness Objective: {objective}\nStakeholders: {stakeholders}\nData Availability: {data}\nReporting Frequency: {frequency}\n\nInclude:\n1. KPI framework\n2. Metric definitions\n3. Data sources\n4. Calculation methods\n5. Reporting strategy\n6. Action triggers", 
         '["objective", "stakeholders", "data", "frequency"]'),
        
        # CONSULTANT PERSONA (10 prompts)
        ("Strategic Planning Consultant", "Develops strategic plans and roadmaps", "Consultant", "Strategy", 
         "Develop strategic plan for:\n\nOrganization: {organization}\nIndustry: {industry}\nCurrent Challenges: {challenges}\nGrowth Objectives: {objectives}\nTimeframe: {timeframe}\n\nProvide:\n1. Situation analysis\n2. Strategic options\n3. Recommended strategy\n4. Implementation roadmap\n5. Success metrics\n6. Risk mitigation", 
         '["organization", "industry", "challenges", "objectives", "timeframe"]'),
        
        ("Digital Transformation Advisor", "Guides digital transformation initiatives", "Consultant", "Digital Transformation", 
         "Plan digital transformation for:\n\nOrganization: {organization}\nCurrent State: {current_state}\nTransformation Goals: {goals}\nBudget: {budget}\nTimeline: {timeline}\n\nInclude:\n1. Digital maturity assessment\n2. Transformation strategy\n3. Technology roadmap\n4. Change management\n5. Implementation phases\n6. Success measurement", 
         '["organization", "current_state", "goals", "budget", "timeline"]'),
        
        ("Management Consulting Expert", "Provides management consulting solutions", "Consultant", "Management", 
         "Provide consulting for:\n\nClient: {client}\nBusiness Challenge: {challenge}\nIndustry Context: {industry}\nStakeholders: {stakeholders}\nSuccess Criteria: {criteria}\n\nDeliver:\n1. Problem diagnosis\n2. Root cause analysis\n3. Solution alternatives\n4. Recommendation\n5. Implementation plan\n6. Change management", 
         '["client", "challenge", "industry", "stakeholders", "criteria"]'),
        
        ("Organizational Change Manager", "Manages organizational change initiatives", "Consultant", "Change Management", 
         "Manage change for:\n\nOrganization: {organization}\nChange Initiative: {initiative}\nImpacted Groups: {groups}\nResistance Factors: {resistance}\n\nProvide:\n1. Change impact assessment\n2. Stakeholder analysis\n3. Communication strategy\n4. Training plan\n5. Resistance management\n6. Success measurement", 
         '["organization", "initiative", "groups", "resistance"]'),
        
        ("Business Process Reengineering", "Reengineers business processes", "Consultant", "Process Reengineering", 
         "Reengineer process for:\n\nProcess: {process_name}\nCurrent Performance: {performance}\nTarget Improvements: {targets}\nConstraints: {constraints}\n\nInclude:\n1. Process analysis\n2. Reengineering approach\n3. New process design\n4. Technology enablers\n5. Implementation strategy\n6. Performance metrics", 
         '["process_name", "performance", "targets", "constraints"]'),
        
        ("Client Presentation Designer", "Creates compelling client presentations", "Consultant", "Presentations", 
         "Create presentation for:\n\nClient: {client}\nPresentation Purpose: {purpose}\nAudience: {audience}\nKey Messages: {messages}\nTime Allocation: {duration}\n\nInclude:\n1. Executive summary\n2. Situation analysis\n3. Recommendations\n4. Implementation approach\n5. Expected outcomes\n6. Next steps", 
         '["client", "purpose", "audience", "messages", "duration"]'),
        
        ("Market Entry Strategist", "Develops market entry strategies", "Consultant", "Market Entry", 
         "Develop market entry strategy for:\n\nCompany: {company}\nTarget Market: {market}\nProduct/Service: {offering}\nCompetitive Landscape: {competition}\nResources: {resources}\n\nProvide:\n1. Market analysis\n2. Entry strategy options\n3. Go-to-market plan\n4. Resource requirements\n5. Risk assessment\n6. Success metrics", 
         '["company", "market", "offering", "competition", "resources"]'),
        
        ("Performance Improvement Consultant", "Improves organizational performance", "Consultant", "Performance", 
         "Improve performance for:\n\nOrganization: {organization}\nPerformance Issues: {issues}\nCurrent Metrics: {metrics}\nImprovement Goals: {goals}\n\nInclude:\n1. Performance diagnosis\n2. Root cause analysis\n3. Improvement opportunities\n4. Action plan\n5. Implementation support\n6. Monitoring framework", 
         '["organization", "issues", "metrics", "goals"]'),
        
        ("Due Diligence Analyst", "Conducts comprehensive due diligence", "Consultant", "Due Diligence", 
         "Conduct due diligence for:\n\nTransaction: {transaction}\nTarget Company: {target}\nFocus Areas: {focus}\nTimeline: {timeline}\nStakeholders: {stakeholders}\n\nProvide:\n1. Due diligence plan\n2. Information requests\n3. Analysis framework\n4. Risk assessment\n5. Findings summary\n6. Recommendations", 
         '["transaction", "target", "focus", "timeline", "stakeholders"]'),
        
        ("Innovation Strategy Consultant", "Develops innovation strategies", "Consultant", "Innovation", 
         "Develop innovation strategy for:\n\nOrganization: {organization}\nInnovation Goals: {goals}\nCurrent Capabilities: {capabilities}\nMarket Opportunities: {opportunities}\n\nInclude:\n1. Innovation assessment\n2. Opportunity identification\n3. Innovation framework\n4. Implementation roadmap\n5. Governance model\n6. Success metrics", 
         '["organization", "goals", "capabilities", "opportunities"]'),
        
        # RESEARCHER PERSONA (5 prompts)
        ("Market Research Analyst", "Conducts comprehensive market research", "Researcher", "Market Research", 
         "Conduct market research for:\n\nResearch Topic: {topic}\nTarget Market: {market}\nResearch Objectives: {objectives}\nMethodology Preference: {methodology}\nTimeline: {timeline}\n\nProvide:\n1. Research design\n2. Data collection plan\n3. Analysis framework\n4. Key findings\n5. Market insights\n6. Strategic implications", 
         '["topic", "market", "objectives", "methodology", "timeline"]'),
        
        ("Industry Analysis Expert", "Performs detailed industry analysis", "Researcher", "Industry Analysis", 
         "Analyze industry:\n\nIndustry: {industry}\nAnalysis Scope: {scope}\nKey Questions: {questions}\nStakeholder Interest: {stakeholders}\n\nInclude:\n1. Industry overview\n2. Market dynamics\n3. Competitive landscape\n4. Trends and drivers\n5. Future outlook\n6. Strategic recommendations", 
         '["industry", "scope", "questions", "stakeholders"]'),
        
        ("Consumer Behavior Researcher", "Studies consumer behavior patterns", "Researcher", "Consumer Research", 
         "Research consumer behavior for:\n\nProduct/Service: {product}\nTarget Demographics: {demographics}\nBehavior Focus: {behavior}\nResearch Methods: {methods}\n\nProvide:\n1. Research methodology\n2. Data collection approach\n3. Behavioral analysis\n4. Consumer insights\n5. Implications for business\n6. Recommendations", 
         '["product", "demographics", "behavior", "methods"]'),
        
        ("Trend Analysis Specialist", "Identifies and analyzes market trends", "Researcher", "Trend Analysis", 
         "Analyze trends for:\n\nIndustry/Market: {market}\nTrend Categories: {categories}\nTime Horizon: {horizon}\nBusiness Impact: {impact}\n\nInclude:\n1. Trend identification\n2. Trend analysis\n3. Impact assessment\n4. Future projections\n5. Business implications\n6. Strategic responses", 
         '["market", "categories", "horizon", "impact"]'),
        
        ("Competitive Intelligence Researcher", "Gathers competitive intelligence", "Researcher", "Competitive Intelligence", 
         "Research competitive intelligence for:\n\nCompany: {company}\nCompetitors: {competitors}\nIntelligence Focus: {focus}\nDecision Context: {context}\n\nProvide:\n1. Intelligence framework\n2. Data collection strategy\n3. Competitive analysis\n4. Strategic insights\n5. Threat assessment\n6. Opportunity identification", 
         '["company", "competitors", "focus", "context"]')
    ]
    
    # Insert all prompts
    for prompt in expanded_prompts:
        c.execute("INSERT INTO prompts (title, description, persona, category, prompt_text, variables) VALUES (?, ?, ?, ?, ?, ?)", prompt)
    
    conn.commit()
    conn.close()
    print(f"Successfully loaded {len(expanded_prompts)} prompts into the database!")

if __name__ == "__main__":
    load_expanded_prompts()