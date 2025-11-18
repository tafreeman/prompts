# Persona Coverage Matrix (Initial Draft)

This matrix provides a high-level view of persona coverage across the prompts library. It is a **living document** and will be refined over time.

## Legend

- ✅ = Strong coverage
- ⚠️ = Partial coverage / needs expansion
- ❌ = Not yet covered

## Personas vs Categories

| Persona / Role           | developers | business | analysis | creative | governance-compliance | system |
|--------------------------|-----------:|---------:|---------:|---------:|-----------------------:|-------:|
| Application Developer    | ✅         | ⚠️       | ⚠️       | ❌       | ❌                     | ⚠️     |
| Architect / Tech Lead    | ✅         | ⚠️       | ⚠️       | ❌       | ⚠️                     | ⚠️     |
| DevOps / SRE             | ⚠️         | ❌       | ⚠️       | ❌       | ⚠️                     | ⚠️     |
| Security Engineer        | ✅         | ❌       | ⚠️       | ❌       | ✅                     | ⚠️     |
| Data / Analytics         | ⚠️         | ⚠️       | ✅       | ❌       | ⚠️                     | ❌     |
| Product Manager          | ⚠️         | ✅       | ⚠️       | ❌       | ⚠️                     | ❌     |
| Business Leader / Exec   | ⚠️         | ✅       | ⚠️       | ❌       | ⚠️                     | ❌     |
| Marketing / Content      | ❌         | ⚠️       | ❌       | ✅       | ❌                     | ❌     |
| Support / Operations     | ⚠️         | ⚠️       | ⚠️       | ❌       | ⚠️                     | ❌     |
| Governance / Compliance  | ❌         | ⚠️       | ⚠️       | ❌       | ✅                     | ⚠️     |

> **Note:** The above coverage indicators are conservative and based on directory names and known example prompts. They should be updated as the library evolves and more prompts are reviewed.

## Next Steps

- For each persona marked ⚠️ or ❌, identify:
  - Existing prompts that partially serve this role.
  - Gaps where new prompts or workflows are needed.
- Link each cell to concrete prompt files as the matrix is refined.
- Use this matrix during planning to prioritize new prompt development for under-served personas.
