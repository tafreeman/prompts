# Prompt Library Web Application - Architecture & Design (Azure Edition)

## 1. Executive Summary

The goal is to expose the existing prompt repository as a user-friendly web application. Users will be able to browse prompts, fill out dynamic forms, and generate executable prompts.

**Azure Advantage:** By leveraging free Azure credits, we will deploy a robust, enterprise-grade architecture using Azure Static Web Apps, Cosmos DB, and Azure OpenAI Service, ensuring high availability and security without out-of-pocket costs during the credit period.

---

## 2. Research & Pattern Analysis

We analyzed several popular open-source prompt engineering tools to determine best practices.

| Solution       | Tech Stack              | Key Pattern Adopted                              |
|----------------|-------------------------|--------------------------------------------------|
| Dify           | Next.js, Python, Postgres | Form generation from template variables.        |
| Flowise        | React, Express          | Visual node-based construction (too complex for this use case). |
| AutoGPT        | Next.js, Prisma         | Block-based architecture.                       |
| LangChain Hub  | React, Python           | "Forkable" templates with `{variable}` syntax.  |

**Selected Approach:** A hybrid "Static-First, Dynamic-Overlay" architecture. The prompts live in Git (static), but are indexed into Cosmos DB (dynamic) to support search, filtering, and live execution features.

---

## 3. System Architecture

### High-Level Design

```mermaid
graph TD
    User[User] -->|Access| SWA[Azure Static Web App]
    SWA -->|Next.js SSR/API| Functions[Azure Managed Functions]
    Functions -->|Query| Cosmos[(Azure Cosmos DB - Mongo API)]
    Functions -->|Generate| OpenAI[Azure OpenAI Service]

    subgraph "CI/CD Pipeline"
        Repo[GitHub Repo] -->|Push Event| Action[GitHub Action]
        Action -->|Sync Content| Cosmos
    end
```text
### Components

#### A. Frontend & Hosting (Azure Static Web Apps)

- **Service:** Azure Static Web Apps (Standard Tier)
- **Framework:** Next.js (App Router) - fully supported by SWA
- **Features:**
  - Global CDN distribution
  - Built-in Authentication (Easy Auth) with GitHub/Azure AD
  - Preview environments for Pull Requests automatically

#### B. Database (Azure Cosmos DB)

- **Service:** Azure Cosmos DB for MongoDB (vCore or RU-based)
- **Why?** Native JSON support, extremely fast reads, and geo-replication capabilities if needed
- **Integration:** Connection string stored in SWA Environment Variables

#### C. Intelligence Layer (Azure OpenAI)

- **Service:** Azure OpenAI Service
- **Models:** GPT-4o or GPT-3.5-Turbo
- **Use Cases:**
  - **"Ask the Architect":** Chatbot helper
  - **Prompt Refinement:** Suggesting improvements to user inputs
  - **Search:** Semantic search capabilities (embeddings)

#### D. The "Sync Engine" (GitHub Action)

- **Trigger:** On push to `main`
- **Logic:**
  1. Checkout code
  2. Parse Markdown & Frontmatter
  3. Upsert documents to Cosmos DB
  4. Build and Deploy Next.js app to SWA

---

## 4. Data Model

### Prompt Document Schema

```typescript
interface PromptDocument {
  _id: string;        // Unique ID
  slug: string;       // URL-friendly ID

  // Core Metadata
  title: string;
  type: 'how_to' | 'template' | 'explanation';
  difficulty: 'beginner' | 'intermediate' | 'advanced';

  // Classification
  category: string;
  topics: string[];
  platforms: string[];  // e.g., ["claude", "chatgpt"]

  // Content
  rawContent: string;     // Full markdown for "Guide" view
  templateCode: string;   // Extracted code for "Executor" view

  // Auto-extracted variables
  variables: PromptVariable[];

  meta: {
    author: string;
    lastSynced: Date;
    filePath: string;
  };
}
```text
---

## 5. Implementation Plan

### Phase 1: Azure Foundation (Days 1-3)

- **Resource Group:** Create `rg-prompt-library`
- **Cosmos DB:** Provision Cosmos DB for MongoDB account
- **Azure OpenAI:** Deploy a model (e.g., `gpt-4o-mini`) in a supported region (e.g., East US 2)
- **Static Web App:** Create the resource and link to GitHub

### Phase 2: Core Application (Weeks 1-2)

- **Parser Script:** Write Node.js script to sync Git → Cosmos
- **Next.js App:** Build the Gallery and Detail views
- **Deploy:** Configure `.github/workflows/azure-static-web-apps-*.yml`

### Phase 3: AI Enhancements (Week 3)

- **Chat Interface:** Implement the "Ask the Architect" chat using Azure OpenAI SDK
- **Risk Audit:** Add the risk analysis feature calling the Azure OpenAI endpoint

---

## 6. Infrastructure & Cost (Credit Usage)

Since you have free credits, we can use standard tiers for better performance.

| Service   | Tier Recommendation              | Est. Credit Consumption    |
|-----------|----------------------------------|----------------------------|
| Hosting   | Azure Static Web Apps (Standard) | ~$9.00/mo                  |
| Database  | Cosmos DB (Serverless)           | ~$5.00/mo (varies by usage)|
| AI        | Azure OpenAI (GPT-4o-mini)       | ~$2.00/mo (pay per token)  |
| **Total** |                                  | **~$16.00/mo (Covered by Credits)** |

---

## 7. Future Enhancements

- **Azure AI Search:** Implement Vector Search for semantic prompt discovery
- **Key Vault:** Securely manage API keys and secrets
