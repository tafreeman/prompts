# Prompt Layering Guide (System / Developer / User)

This guide explains how to break prompts from this library into **system**, **developer**, and **user** messages when integrating with tools like GitHub Copilot, M365 Copilot, and LLM APIs.

## 1. Layer Definitions

- **System message**
  - Purpose: Global, non-negotiable behavior and safety rules.
  - Scope: Organization-wide policies, security/compliance requirements, non-functional constraints.

- **Developer message**
  - Purpose: Task template, process, and preferred reasoning style.
  - Scope: How to perform the task, which frameworks to use (CoT, ToT, ReAct, RAG, reflection), and output schemas.

- **User message**
  - Purpose: Concrete request and inputs for this specific run.
  - Scope: Actual problem, pasted artifacts (code, docs, logs), and any run-specific preferences.

## 2. Mapping Library Prompts to Layers

When using prompts from this repo:

1. **System**
   - Keep this short and stable across tasks.
   - Example:
   ```
   You are a careful, security-aware AI assistant.
   - Follow organizational coding and security standards.
   - Never expose secrets or real credentials.
   - Prefer clarity and safety over brevity.
   ```

2. **Developer**
   - Take the **Prompt** section from the library file and adapt it here.
   - Include the **Goal**, **Context**, **Assumptions**, **Constraints**, **Process / Reasoning Style**, and **Output Requirements**.

3. **User**
   - Insert the specific request and inputs using the variables from the prompt.
   - Wrap large artifacts using the standard delimiters (e.g., `[[CONTEXT]]...[[/CONTEXT]]`).

## 3. Example: CoT Code Review (Developers)

Assume you are using `developers/code-review-assistant.md` (simplified example).

- **System**
  ```
  You are a senior software engineer.
  - Follow secure coding best practices.
  - Do not invent behavior that is not supported by the code.
  ```

- **Developer**
  ```
  Goal: Provide a structured, step-by-step code review.

  Process / Reasoning Style:
  - Use concise Chain-of-Thought: think through the code before writing the final review.
  - Do not expose raw reasoning; only present the final structured review.

  Output Requirements (Markdown):
  - Heading: Summary
  - Heading: Correctness issues (bulleted)
  - Heading: Security issues (bulleted)
  - Heading: Performance improvements (bulleted)
  - Heading: Readability & style (bulleted)
  ```

- **User**
  ```
  Please review the following pull request for security, correctness, and performance issues.

  [[CONTEXT]]
  <paste diff or code here>
  [[/CONTEXT]]
  ```

## 4. Example: ToT Architecture Decision (Advanced Techniques)

Using `advanced-techniques/tree-of-thoughts-template.md` in a layered setup:

- **System**
  ```
  You are an experienced software architect.
  - Provide objective, evidence-based recommendations.
  - Make trade-offs explicit.
  ```

- **Developer**
  ```
  Goal: Use Tree-of-Thoughts to explore multiple architecture options and select the best one.

  Process / Reasoning Style:
  - Generate 3–5 distinct branches (A, B, C...).
  - For each branch, list description, pros, cons, success probability, and score.
  - Prune weak branches early and explore promising ones in depth.
  - Backtrack explicitly if a branch becomes unviable.

  Output Requirements:
  - Human-readable summary with sections: Problem Understanding, Branch Generation, Branch Evaluation, Deep Exploration, Cross-Branch Synthesis, Final Recommendation.
  - JSON summary wrapped in [[OUTPUT_JSON]]...[[/OUTPUT_JSON]] following the schema in the ToT template.
  ```

- **User**
  ```
  **Problem**: [Describe the architecture decision]

  **Context**:
  [[CONTEXT]]
  - Domain and non-functional requirements
  - Constraints (budget, timeline, stack)
  - Existing systems
  [[/CONTEXT]]

  **Success Criteria**:
  - [List measurable success metrics]
  ```

## 5. Practical Tips

- Keep the **system** message stable; iterate mostly on **developer** and **user** messages.
- For production, use concise CoT (or hidden reasoning) to manage cost and latency.
- Use ToT and detailed CoT mainly for high-stakes or novel problems.
- Always define clear **Output Requirements** so downstream tools can consume results.

---

This guide is a starting point. As you evolve your internal conventions, extend this file with more concrete platform-specific examples (e.g., GitHub Copilot, M365 extensions, Azure OpenAI).