---

title: "Mobile Architecture Consultant"
category: "system"
tags: ["architect", "mobile-architecture", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Mobile Architecture Consultant

## Description

Designs mobile application architectures

## Use Cases

- Mobile Architecture for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Design mobile architecture for:

App Type: [app_type]
Target Platforms: [platforms]
User Base: [users]
Performance Requirements: [performance]
Security Needs: [security]

Include:
1. Architecture patterns
2. Backend integration
3. Offline capabilities
4. Security implementation
5. Performance optimization
6. Testing strategy
```

## Variables

- `[app_type]`: App Type
- `[performance]`: Performance
- `[platforms]`: Platforms
- `[security]`: Security
- `[users]`: Users

## Example Usage

**Input:**

```text
[app_type]: Telehealth Patient Companion App
[platforms]: iOS (SwiftUI) and Android (Kotlin/Jetpack Compose)
[users]: 1M+ patients, elderly demographic (accessibility focus)
[performance]: <2s startup time, smooth video calls on 4G networks
[security]: HIPAA compliant, biometric auth, no sensitive data stored on device
```

**Output:**

```text
## Mobile Architecture Design

### 1. Architecture Pattern
*   **MVVM-C (Model-View-ViewModel + Coordinator):**
    *   Decouples UI from business logic for testability.
    *   Coordinators handle navigation flow, enabling deep linking support.
*   **Modularization:** Feature-based modules (Auth, Appointments, VideoCall, Prescriptions) to speed up build times.

### 2. Backend Integration
*   **Protocol:** GraphQL (Apollo Client) to minimize over-fetching on mobile networks.
*   **Real-time:** WebSockets for chat and appointment status updates.
*   **Resilience:** Circuit breaker pattern for flaky network conditions.

### 3. Offline Capabilities
*   **Strategy:** "Offline-First" for read-only data (Prescription history).
*   **Storage:** Encrypted Realm/Room database.
*   **Sync:** Background sync worker to upload vitals when connectivity restores.

[... continues with security implementation and testing ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Architect prompts in this category
- Check the system folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
