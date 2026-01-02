from .dimensions import Dimension, Criterion, PerformanceLevel

# Data extracted from enterprise-prompt-evaluation-framework.md

TECHNICAL_QUALITY = Dimension(
    id="technical_quality",
    name="Technical Quality",
    weight=0.25,
    description="Evaluates prompt construction excellence, including clarity, syntax, structure, and utilization of advanced prompting techniques.",
    criteria=[
        Criterion("clarity", "Unambiguous language, specific terminology, clear instructions"),
        Criterion("structure", "Logical organization, proper formatting, section coherence"),
        Criterion("syntax", "Grammatical accuracy, consistent style, appropriate punctuation"),
        Criterion("advanced_techniques", "Implementation of CoT, Few-Shot, ToT, ReAct, and other methodologies")
    ],
    rubric={
        PerformanceLevel.EXCEPTIONAL: {
            "description": "Exceeds enterprise standards significantly",
            "criteria": """
- Clarity: Instructions are crystal clear with zero ambiguity; terminology precisely defined
- Structure: Perfect logical flow with clear sections, headers, and formatting conventions
- Syntax: Flawless grammar and punctuation; consistent professional style throughout
- Advanced Techniques: Masterful integration of multiple techniques (CoT, Few-Shot, ToT, ReAct) with clear reasoning
- Example: Prompt includes explicit step-by-step reasoning, 3+ diverse examples, and built-in self-verification
"""
        },
        PerformanceLevel.PROFICIENT: {
             "description": "Meets all enterprise standards with excellence",
             "criteria": """
- Clarity: Clear instructions with minimal ambiguity; terms well-defined
- Structure: Strong logical organization; consistent formatting
- Syntax: Minor grammatical variations that don't impact comprehension
- Advanced Techniques: Effective use of at least two advanced techniques with appropriate application
- Example: Prompt uses Chain-of-Thought with relevant examples; structure supports intended use case
"""
        },
        PerformanceLevel.COMPETENT: {
            "description": "Meets basic enterprise standards adequately",
             "criteria": """
- Clarity: Generally clear with some areas requiring interpretation
- Structure: Adequate organization; some formatting inconsistencies
- Syntax: Occasional grammar issues; style variations present
- Advanced Techniques: Basic implementation of one advanced technique
- Example: Prompt includes step-by-step instructions but lacks examples or verification
"""
        },
        PerformanceLevel.DEVELOPING: {
            "description": "Approaches standards but requires improvement",
             "criteria": """
- Clarity: Significant ambiguity in key instructions
- Structure: Weak organization affecting comprehension
- Syntax: Multiple grammar/style issues impacting readability
- Advanced Techniques: Attempted but incorrectly implemented techniques
- Example: Prompt attempts Chain-of-Thought but reasoning steps are unclear or illogical
"""
        },
        PerformanceLevel.INADEQUATE: {
            "description": "Fails to meet minimum enterprise standards",
             "criteria": """
- Clarity: Instructions are confusing or contradictory
- Structure: No discernible organization; formatting absent
- Syntax: Pervasive errors affecting comprehension
- Advanced Techniques: No advanced techniques or complete misapplication
- Example: Prompt is a single run-on instruction with no structure or technique application
"""
        }
    }
)

BUSINESS_ALIGNMENT = Dimension(
    id="business_alignment",
    name="Business Alignment",
    weight=0.20,
    description="Assesses strategic value, use case appropriateness, ROI potential, and organizational goal support.",
    criteria=[
        Criterion("strategic_value", "Contribution to organizational objectives and priorities"),
        Criterion("use_case_fit", "Appropriateness for intended application domain"),
        Criterion("roi_potential", "Cost-benefit analysis and efficiency gains"),
        Criterion("stakeholder_requirements", "Alignment with business user needs and expectations")
    ],
    rubric={
        PerformanceLevel.EXCEPTIONAL: {
             "description": "Exceeds enterprise standards significantly",
             "criteria": """
- Strategic Value: Directly supports key organizational objectives with measurable impact
- Use Case Fit: Perfectly tailored to intended application with domain expertise evident
- ROI Potential: Clear, quantifiable efficiency gains or cost reductions documented
- Stakeholder Requirements: Exceeds stated requirements; anticipates future needs
"""
        },
        PerformanceLevel.PROFICIENT: {
             "description": "Meets all enterprise standards with excellence",
             "criteria": """
- Strategic Value: Supports organizational objectives with identifiable benefits
- Use Case Fit: Well-suited to application domain with appropriate customization
- ROI Potential: Reasonable efficiency expectations with supporting rationale
- Stakeholder Requirements: Meets documented requirements comprehensively
"""
        },
        PerformanceLevel.COMPETENT: {
             "description": "Meets basic enterprise standards adequately",
             "criteria": """
- Strategic Value: Indirect support for objectives; connection requires explanation
- Use Case Fit: Adequate for domain with minor adjustments needed
- ROI Potential: General efficiency claims without specific metrics
- Stakeholder Requirements: Meets core requirements; some gaps in secondary needs
"""
        },
        PerformanceLevel.DEVELOPING: {
             "description": "Approaches standards but requires improvement",
             "criteria": """
- Strategic Value: Weak connection to organizational objectives
- Use Case Fit: Generic approach not tailored to specific domain
- ROI Potential: No clear efficiency justification provided
- Stakeholder Requirements: Partial fulfillment of stated requirements
"""
        },
        PerformanceLevel.INADEQUATE: {
             "description": "Fails to meet minimum enterprise standards",
             "criteria": """
- Strategic Value: No connection to organizational objectives
- Use Case Fit: Misaligned with intended application domain
- ROI Potential: Negative ROI likely due to inefficiency or rework
- Stakeholder Requirements: Fails to meet basic stakeholder needs
"""
        }
    }
)

SECURITY_COMPLIANCE = Dimension(
    id="security_compliance",
    name="Security & Compliance",
    weight=0.20,
    description="Evaluates data protection measures, regulatory adherence, risk mitigation, and privacy safeguards.",
    criteria=[
        Criterion("data_protection", "Handling of sensitive information, PII safeguards, data minimization"),
        Criterion("regulatory_compliance", "GDPR, CCPA, HIPAA, industry-specific requirements"),
        Criterion("risk_mitigation", "Prompt injection prevention, output validation, guardrails"),
        Criterion("privacy_safeguards", "User consent considerations, data retention policies")
    ],
    rubric={
        PerformanceLevel.EXCEPTIONAL: {
             "description": "Exceeds enterprise standards significantly",
             "criteria": """
- Data Protection: Comprehensive safeguards; no sensitive data exposure possible
- Regulatory Compliance: Full adherence to all applicable regulations with documentation
- Risk Mitigation: Multi-layer defenses against injection, jailbreaking, and misuse
- Privacy Safeguards: Privacy-by-design principles fully implemented
"""
        },
        PerformanceLevel.PROFICIENT: {
             "description": "Meets all enterprise standards with excellence",
             "criteria": """
- Data Protection: Strong safeguards with clear data handling instructions
- Regulatory Compliance: Meets all required regulations with evidence of consideration
- Risk Mitigation: Effective guardrails and output validation implemented
- Privacy Safeguards: Privacy considerations addressed in design
"""
        },
        PerformanceLevel.COMPETENT: {
             "description": "Meets basic enterprise standards adequately",
             "criteria": """
- Data Protection: Basic safeguards present; some edge cases unaddressed
- Regulatory Compliance: Compliant with major regulations; minor gaps may exist
- Risk Mitigation: Basic guardrails implemented; some vulnerabilities possible
- Privacy Safeguards: Privacy mentioned but not comprehensively addressed
"""
        },
        PerformanceLevel.DEVELOPING: {
             "description": "Approaches standards but requires improvement",
             "criteria": """
- Data Protection: Minimal safeguards; potential exposure risks identified
- Regulatory Compliance: Partial compliance; remediation required
- Risk Mitigation: Limited guardrails; known vulnerabilities present
- Privacy Safeguards: Privacy not systematically considered
"""
        },
        PerformanceLevel.INADEQUATE: {
             "description": "Fails to meet minimum enterprise standards",
             "criteria": """
- Data Protection: No safeguards; sensitive data exposure likely
- Regulatory Compliance: Non-compliant with critical regulations
- Risk Mitigation: No protections against known attack vectors
- Privacy Safeguards: Privacy violations possible or likely
"""
        }
    }
)

PERFORMANCE_RELIABILITY = Dimension(
    id="performance_reliability",
    name="Performance & Reliability",
    weight=0.15,
    description="Measures output consistency, accuracy, response quality, and operational effectiveness.",
    criteria=[
        Criterion("output_consistency", "Reproducible results across multiple executions"),
        Criterion("accuracy", "Factual correctness and alignment with expected outcomes"),
        Criterion("response_quality", "Completeness, relevance, and usefulness of outputs"),
        Criterion("operational_effectiveness", "Token efficiency, latency optimization, error handling")
    ],
    rubric={
        PerformanceLevel.EXCEPTIONAL: {
             "description": "Exceeds enterprise standards significantly",
             "criteria": """
- Consistency: 95%+ reproducibility across executions with documented variance
- Accuracy: Verified factual correctness with source attribution where applicable
- Response Quality: Comprehensive, actionable outputs exceeding expectations
- Operational Effectiveness: Optimized token usage; sub-second latency where applicable
"""
        },
        PerformanceLevel.PROFICIENT: {
             "description": "Meets all enterprise standards with excellence",
             "criteria": """
- Consistency: 85%+ reproducibility with acceptable variance
- Accuracy: High factual correctness with rare, minor errors
- Response Quality: Complete, relevant outputs meeting requirements
- Operational Effectiveness: Efficient resource usage; acceptable latency
"""
        },
        PerformanceLevel.COMPETENT: {
             "description": "Meets basic enterprise standards adequately",
             "criteria": """
- Consistency: 75%+ reproducibility; some notable variance
- Accuracy: Generally accurate with occasional errors requiring review
- Response Quality: Adequate outputs; may require supplementation
- Operational Effectiveness: Acceptable efficiency; room for optimization
"""
        },
        PerformanceLevel.DEVELOPING: {
            "description": "Approaches standards but requires improvement",
             "criteria": """
- Consistency: Variable results; inconsistency affects reliability
- Accuracy: Frequent errors or hallucinations in outputs
- Response Quality: Incomplete or partially relevant outputs
- Operational Effectiveness: Inefficient resource usage; performance issues
"""
        },
        PerformanceLevel.INADEQUATE: {
             "description": "Fails to meet minimum enterprise standards",
             "criteria": """
- Consistency: Unpredictable; results vary significantly
- Accuracy: High error rate; outputs unreliable
- Response Quality: Outputs require extensive revision or are unusable
- Operational Effectiveness: Excessive resource consumption; operational failures
"""
        }
    }
)

MAINTAINABILITY = Dimension(
    id="maintainability",
    name="Maintainability",
    weight=0.10,
    description="Assesses documentation quality, version control practices, sustainability, and ease of modification.",
    criteria=[
        Criterion("documentation", "Clear purpose statements, usage instructions, example outputs"),
        Criterion("version_control", "Change history, deprecation notices, migration guides"),
        Criterion("sustainability", "Long-term viability, model-agnostic design, update ease"),
        Criterion("modification_ease", "Modular structure, clear parameterization, extension points")
    ],
    rubric={
        PerformanceLevel.EXCEPTIONAL: {
             "description": "Exceeds enterprise standards significantly",
             "criteria": """
- Documentation: Comprehensive docs including purpose, usage, examples, troubleshooting
- Version Control: Full change history; clear versioning scheme; migration guides
- Sustainability: Model-agnostic design; future-proofed for evolving capabilities
- Modification Ease: Modular, parameterized structure; clear extension points
"""
        },
        PerformanceLevel.PROFICIENT: {
             "description": "Meets all enterprise standards with excellence",
             "criteria": """
- Documentation: Clear documentation covering purpose, usage, and examples
- Version Control: Maintained version history with change notes
- Sustainability: Considers model differences; reasonable longevity
- Modification Ease: Well-structured; modifications straightforward
"""
        },
        PerformanceLevel.COMPETENT: {
             "description": "Meets basic enterprise standards adequately",
             "criteria": """
- Documentation: Basic documentation; purpose and usage described
- Version Control: Version tracked; limited change documentation
- Sustainability: May require updates for different models
- Modification Ease: Structure allows modification with some effort
"""
        },
        PerformanceLevel.DEVELOPING: {
             "description": "Approaches standards but requires improvement",
             "criteria": """
- Documentation: Minimal documentation; gaps in critical information
- Version Control: Ad-hoc versioning; poor change tracking
- Sustainability: Model-specific; limited longevity
- Modification Ease: Modifications difficult; structure unclear
"""
        },
        PerformanceLevel.INADEQUATE: {
             "description": "Fails to meet minimum enterprise standards",
             "criteria": """
- Documentation: No documentation or severely incomplete
- Version Control: No versioning; changes untracked
- Sustainability: Unlikely to remain functional; obsolescence imminent
- Modification Ease: Modifications require complete rewrite
"""
        }
    }
)

INNOVATION_OPTIMIZATION = Dimension(
    id="innovation_optimization",
    name="Innovation & Optimization",
    weight=0.10,
    description="Evaluates creative problem-solving, efficiency improvements, and advanced technique adoption.",
    criteria=[
        Criterion("creative_solutions", "Novel approaches to complex problems"),
        Criterion("efficiency_improvements", "Token optimization, cost reduction strategies"),
        Criterion("technique_adoption", "Implementation of cutting-edge prompting methodologies"),
        Criterion("continuous_improvement", "Evidence of iteration and refinement")
    ],
    rubric={
        PerformanceLevel.EXCEPTIONAL: {
             "description": "Exceeds enterprise standards significantly",
             "criteria": """
- Creative Solutions: Novel approach demonstrating thought leadership
- Efficiency Improvements: Measurable optimization (e.g., 30%+ token reduction)
- Technique Adoption: Cutting-edge techniques expertly implemented
- Continuous Improvement: Evidence of multiple refinement iterations with metrics
"""
        },
        PerformanceLevel.PROFICIENT: {
             "description": "Meets all enterprise standards with excellence",
             "criteria": """
- Creative Solutions: Thoughtful approach improving on standard methods
- Efficiency Improvements: Demonstrated optimization efforts with results
- Technique Adoption: Modern techniques appropriately applied
- Continuous Improvement: Clear iteration history with improvements
"""
        },
        PerformanceLevel.COMPETENT: {
             "description": "Meets basic enterprise standards adequately",
             "criteria": """
- Creative Solutions: Standard approach with some customization
- Efficiency Improvements: Basic optimization present
- Technique Adoption: Established techniques used correctly
- Continuous Improvement: Some evidence of refinement
"""
        },
        PerformanceLevel.DEVELOPING: {
             "description": "Approaches standards but requires improvement",
             "criteria": """
- Creative Solutions: Generic approach without customization
- Efficiency Improvements: No optimization attempted
- Technique Adoption: Outdated or basic techniques only
- Continuous Improvement: No evidence of iteration
"""
        },
        PerformanceLevel.INADEQUATE: {
             "description": "Fails to meet minimum enterprise standards",
             "criteria": """
- Creative Solutions: Copy-paste approach with no adaptation
- Efficiency Improvements: Actively inefficient design
- Technique Adoption: No technique application; raw instructions only
- Continuous Improvement: Static; no development evident
"""
        }
    }
)

ALL_DIMENSIONS = [
    TECHNICAL_QUALITY,
    BUSINESS_ALIGNMENT,
    SECURITY_COMPLIANCE,
    PERFORMANCE_RELIABILITY,
    MAINTAINABILITY,
    INNOVATION_OPTIMIZATION
]
