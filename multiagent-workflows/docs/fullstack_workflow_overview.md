# Full-Stack Generation Workflow - Visual Overview

This document provides a comprehensive visual overview of the Full-Stack Application Generation workflow using Mermaid diagrams.

## Workflow Architecture

### High-Level Flow

```mermaid
flowchart TB
    subgraph INPUT["📥 INPUTS"]
        REQ[Business Requirements]
        MOCK[UI Mockups<br/>Optional]
        TECH[Tech Preferences<br/>Optional]
    end

    subgraph ANALYSIS["🔍 ANALYSIS PHASE"]
        VA[Vision Agent]
        RA[Requirements Agent]
    end

    subgraph DESIGN["🏗️ DESIGN PHASE"]
        AA[Architect Agent]
        DA[Database Agent]
        API[API Agent]
    end

    subgraph BUILD["⚙️ BUILD PHASE"]
        BE[Backend Coder]
        FE[Frontend Coder]
    end

    subgraph QUALITY["✅ QUALITY PHASE"]
        RV[Reviewer Agent]
        TA[Test Agent]
        DOC[Documentation Agent]
    end

    subgraph OUTPUT["📤 OUTPUTS"]
        APP[Complete Application]
        TESTS[Test Suite]
        DOCS[Documentation]
    end

    INPUT --> ANALYSIS
    ANALYSIS --> DESIGN
    DESIGN --> BUILD
    BUILD --> QUALITY
    QUALITY --> OUTPUT

    style INPUT fill:#e1f5fe
    style ANALYSIS fill:#fff3e0
    style DESIGN fill:#f3e5f5
    style BUILD fill:#e8f5e9
    style QUALITY fill:#fce4ec
    style OUTPUT fill:#e0f2f1
```

### Detailed Step Sequence

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant WE as Workflow Engine
    participant VA as Vision Agent
    participant RA as Requirements Agent
    participant AA as Architect Agent
    participant DA as Database Agent
    participant API as API Agent
    participant BE as Backend Coder
    participant FE as Frontend Coder
    participant RV as Reviewer Agent
    participant TA as Test Agent
    participant DOC as Doc Agent

    U->>WE: Submit Requirements
    
    rect rgb(255, 243, 224)
        Note over WE,RA: Analysis Phase
        WE->>VA: Analyze UI Mockups
        VA-->>WE: UI Components
        WE->>RA: Parse Requirements
        RA-->>WE: User Stories, Entities
    end

    rect rgb(243, 229, 245)
        Note over WE,API: Design Phase
        WE->>AA: Design Architecture
        AA-->>WE: Tech Stack, Patterns
        WE->>DA: Design Database
        DA-->>WE: Schema, Migrations
        WE->>API: Design API
        API-->>WE: OpenAPI Spec
    end

    rect rgb(232, 245, 233)
        Note over WE,FE: Build Phase
        WE->>BE: Generate Backend
        BE-->>WE: Backend Code
        WE->>FE: Generate Frontend
        FE-->>WE: Frontend Code
    end

    rect rgb(252, 228, 236)
        Note over WE,DOC: Quality Phase
        WE->>RV: Review Code
        RV-->>WE: Issues, Scores
        WE->>TA: Generate Tests
        TA-->>WE: Test Suite
        WE->>DOC: Generate Docs
        DOC-->>WE: README, API Docs
    end

    WE->>U: Complete Application
```

## Agent Interactions

### Data Flow Between Agents

```mermaid
flowchart LR
    subgraph Step1["Step 1: Vision"]
        M[UI Mockups] --> VA[Vision Agent]
        VA --> UC[UI Components]
        VA --> UX[UX Patterns]
    end

    subgraph Step2["Step 2: Requirements"]
        REQ[Requirements] --> RA[Requirements Agent]
        UC --> RA
        RA --> US[User Stories]
        RA --> DE[Data Entities]
        RA --> NFR[Non-Functional Reqs]
    end

    subgraph Step3["Step 3: Architecture"]
        US --> AA[Architect Agent]
        NFR --> AA
        AA --> TS[Tech Stack]
        AA --> ARCH[Architecture Design]
        AA --> APIST[API Strategy]
    end

    subgraph Step4["Step 4: Database"]
        DE --> DA[Database Agent]
        TS --> DA
        DA --> SCH[Schema DDL]
        DA --> MIG[Migrations]
    end

    subgraph Step5["Step 5: API"]
        US --> APIA[API Agent]
        ARCH --> APIA
        APIA --> OAS[OpenAPI Spec]
        APIA --> EP[Endpoints]
    end

    subgraph Step6["Step 6: Backend"]
        OAS --> BE[Backend Coder]
        SCH --> BE
        BE --> BCODE[Backend Code]
        BE --> BFILES[Backend Files]
    end

    subgraph Step7["Step 7: Frontend"]
        OAS --> FE[Frontend Coder]
        UC --> FE
        FE --> FCODE[Frontend Code]
        FE --> FFILES[Frontend Files]
    end

    subgraph Step8["Step 8: Review"]
        BCODE --> RV[Reviewer Agent]
        FCODE --> RV
        RV --> ISS[Issues]
        RV --> SCR[Scores]
    end

    subgraph Step9["Step 9: Tests"]
        BCODE --> TA[Test Agent]
        FCODE --> TA
        TA --> UNIT[Unit Tests]
        TA --> INT[Integration Tests]
    end

    Step1 --> Step2
    Step2 --> Step3
    Step3 --> Step4
    Step3 --> Step5
    Step4 --> Step6
    Step5 --> Step6
    Step5 --> Step7
    Step6 --> Step8
    Step7 --> Step8
    Step8 --> Step9
```

## Model Selection Strategy

```mermaid
flowchart TD
    subgraph ModelRouting["Model Selection"]
        TASK[Task Type] --> ROUTER{Router}
        
        ROUTER -->|Vision| VIS[Vision Models]
        ROUTER -->|Reasoning| REASON[Reasoning Models]
        ROUTER -->|Code Gen| CODE[Code Models]
        ROUTER -->|Review| REV[Review Models]
        ROUTER -->|Docs| DOCS[Doc Models]
        
        VIS --> V1[gh:gpt-4o-vision]
        VIS --> V2[local:phi-3.5-vision]
        
        REASON --> R1[gh:o3-mini]
        REASON --> R2[gh:deepseek-r1]
        REASON --> R3[ollama:deepseek-r1:14b]
        
        CODE --> C1[gh:gpt-4o]
        CODE --> C2[ollama:qwen2.5-coder:14b]
        CODE --> C3[local:phi4mini]
        
        REV --> RV1[gh:gpt-4o]
        REV --> RV2[ollama:qwen2.5-coder:14b]
        
        DOCS --> D1[gh:gpt-4o-mini]
        DOCS --> D2[local:phi4mini]
    end

    subgraph Fallback["Fallback Strategy"]
        TRY[Try Preferred] --> CHECK{Available?}
        CHECK -->|Yes| USE[Use Model]
        CHECK -->|No| NEXT[Try Next]
        NEXT --> CHECK
        NEXT -->|All Failed| LOCAL[Use Local Fallback]
    end
```

## Artifact Generation

### Output Structure

```mermaid
flowchart TD
    subgraph Artifacts["Generated Artifacts"]
        APP[Application]
        
        APP --> BE[Backend/]
        BE --> BEAPI[api/]
        BE --> BEMOD[models/]
        BE --> BESVC[services/]
        BE --> BECFG[config/]
        
        APP --> FE[Frontend/]
        FE --> FECMP[components/]
        FE --> FEPG[pages/]
        FE --> FEST[styles/]
        FE --> FEUT[utils/]
        
        APP --> DB[Database/]
        DB --> DBSCH[schema.sql]
        DB --> DBMIG[migrations/]
        DB --> DBSED[seeds/]
        
        APP --> TESTS[Tests/]
        TESTS --> TUNIT[unit/]
        TESTS --> TINT[integration/]
        TESTS --> TE2E[e2e/]
        
        APP --> DOCS[Documentation/]
        DOCS --> README[README.md]
        DOCS --> APIDOC[api-docs.md]
        DOCS --> SETUP[setup-guide.md]
    end

    style Artifacts fill:#f5f5f5
```

## Scoring & Evaluation

### Rubric Breakdown

```mermaid
pie showData
    title "Scoring Weight Distribution"
    "Functional Correctness" : 40
    "Code Quality" : 25
    "Completeness" : 20
    "Documentation" : 10
    "Efficiency" : 5
```

### Evaluation Flow

```mermaid
flowchart LR
    subgraph Evaluation["Evaluation Pipeline"]
        OUT[Workflow Output] --> EVAL[Evaluator]
        GOLD[Golden Output] --> EVAL
        RUB[Rubrics] --> EVAL
        
        EVAL --> SC1[Correctness Score]
        EVAL --> SC2[Quality Score]
        EVAL --> SC3[Completeness Score]
        EVAL --> SC4[Documentation Score]
        EVAL --> SC5[Efficiency Score]
        
        SC1 --> AGG[Aggregator]
        SC2 --> AGG
        SC3 --> AGG
        SC4 --> AGG
        SC5 --> AGG
        
        AGG --> TOTAL[Total Score]
        AGG --> GRADE[Grade A-F]
        AGG --> PASS{Pass?}
        
        PASS -->|≥70%| YES[✅ Passed]
        PASS -->|<70%| NO[❌ Failed]
    end
```

## Logging Hierarchy

```mermaid
flowchart TD
    subgraph Logging["5-Level Hierarchical Logging"]
        L1[🔷 Workflow Level]
        L2[🔶 Step Level]
        L3[🔵 Agent Level]
        L4[🟢 Model Level]
        L5[🟣 Tool Level]
        
        L1 --> L2
        L2 --> L3
        L3 --> L4
        L3 --> L5
        
        L1 ---|"workflow.start<br/>workflow.complete"| E1[Events]
        L2 ---|"step.start<br/>step.complete"| E2[Events]
        L3 ---|"agent.start<br/>agent.complete"| E3[Events]
        L4 ---|"model.call<br/>model.response"| E4[Events]
        L5 ---|"tool.invoke<br/>tool.result"| E5[Events]
    end

    subgraph Metrics["Captured Metrics"]
        M1[Tokens Used]
        M2[Cost Estimate]
        M3[Duration MS]
        M4[Success Rate]
    end

    L4 --> M1
    L4 --> M2
    L1 --> M3
    L1 --> M4
```

## State Machine

```mermaid
stateDiagram-v2
    [*] --> Initialized: Create Workflow

    Initialized --> Running: execute()
    
    Running --> AnalysisPhase: Start
    
    state AnalysisPhase {
        [*] --> VisionAnalysis
        VisionAnalysis --> RequirementsParsing
        RequirementsParsing --> [*]
    }
    
    AnalysisPhase --> DesignPhase
    
    state DesignPhase {
        [*] --> ArchitectureDesign
        ArchitectureDesign --> DatabaseDesign
        ArchitectureDesign --> APIDesign
        DatabaseDesign --> [*]
        APIDesign --> [*]
    }
    
    DesignPhase --> BuildPhase
    
    state BuildPhase {
        [*] --> BackendGeneration
        [*] --> FrontendGeneration
        BackendGeneration --> [*]
        FrontendGeneration --> [*]
    }
    
    BuildPhase --> QualityPhase
    
    state QualityPhase {
        [*] --> CodeReview
        CodeReview --> TestGeneration
        TestGeneration --> Documentation
        Documentation --> [*]
    }
    
    QualityPhase --> Completed
    Running --> Failed: Error
    
    Completed --> [*]: Return Results
    Failed --> [*]: Return Error
```

## Example Execution Timeline

```mermaid
gantt
    title Full-Stack Generation Timeline
    dateFormat X
    axisFormat %s

    section Analysis
    Vision Analysis     :a1, 0, 30s
    Requirements Parse  :a2, after a1, 45s

    section Design
    Architecture Design :d1, after a2, 60s
    Database Design     :d2, after d1, 45s
    API Design          :d3, after d1, 45s

    section Build
    Backend Generation  :b1, after d2 d3, 120s
    Frontend Generation :b2, after d3, 90s

    section Quality
    Code Review         :q1, after b1 b2, 60s
    Test Generation     :q2, after q1, 90s
    Documentation       :q3, after q2, 30s
```

## Usage Example

```python
import asyncio
from multiagent_workflows import ModelManager, WorkflowEngine, VerboseLogger
from multiagent_workflows.workflows import FullStackWorkflow

async def generate_application():
    # Initialize components
    model_manager = ModelManager(allow_remote=True)
    logger = VerboseLogger(workflow_id="demo")
    
    # Create workflow
    workflow = FullStackWorkflow(
        model_manager=model_manager,
        logger=logger,
    )
    
    # Execute with requirements
    result = await workflow.execute({
        "requirements": """
        Build a task management application with:
        - User authentication (email/password, OAuth)
        - Task CRUD with due dates and priorities
        - Team collaboration features
        - Real-time notifications
        - Dashboard with analytics
        """,
        "tech_stack": {
            "frontend": "React + TypeScript",
            "backend": "Python FastAPI",
            "database": "PostgreSQL"
        }
    })
    
    # Access outputs
    print(f"Generated {len(result['artifacts'])} artifacts")
    print(f"Backend files: {result['artifacts'].get('backend_files', {}).keys()}")
    print(f"Frontend files: {result['artifacts'].get('frontend_files', {}).keys()}")
    
    # Export logs
    logger.export_to_markdown("execution_log.md")
    
    return result

asyncio.run(generate_application())
```

## Key Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Generation Time | <30 min | Total workflow execution time |
| Test Coverage | >80% | Generated test coverage |
| Code Quality Score | >7/10 | Based on review agent |
| Requirements Coverage | 100% | All requirements addressed |
| Security Score | >8/10 | No critical vulnerabilities |
